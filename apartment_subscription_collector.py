#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏠 부동산 청약정보 수집 프로그램 v3.0
한국부동산원 청약홈 API를 활용하여 최신 청약 분양정보를 수집

Author: AI Assistant
License: MIT
Created: 2025-06-19
"""

import requests
import pandas as pd
import openpyxl
from openpyxl.utils import get_column_letter
from datetime import datetime
import os
import sys
from docx import Document
from docx.shared import Inches
import json
from collections import defaultdict
import re
import urllib.parse
import time
from bs4 import BeautifulSoup
import configparser

###########################
# 설정 및 초기화
###########################

class Config:
    """프로그램 설정 클래스"""
    
    def __init__(self):
        self.load_config()
    
    def load_config(self):
        """설정 파일 로드 또는 기본값 설정"""
        config = configparser.ConfigParser()
        config_file = 'config.ini'
        
        if os.path.exists(config_file):
            config.read(config_file, encoding='utf-8')
            self.api_key = config.get('API', 'service_key', fallback='')
            self.max_pages = config.getint('SETTINGS', 'max_pages', fallback=50)
            self.max_items_per_file = config.getint('SETTINGS', 'max_items_per_file', fallback=10)
            self.output_folder = config.get('PATHS', 'output_folder', fallback='결과물')
        else:
            # 기본값 설정
            self.api_key = ''
            self.max_pages = 50
            self.max_items_per_file = 10
            self.output_folder = '결과물'
            self.create_default_config(config_file)
    
    def create_default_config(self, config_file):
        """기본 설정 파일 생성"""
        config = configparser.ConfigParser()
        
        config['API'] = {
            'service_key': '여기에_발급받은_API_키를_입력하세요'
        }
        
        config['SETTINGS'] = {
            'max_pages': '50',
            'max_items_per_file': '10'
        }
        
        config['PATHS'] = {
            'output_folder': '결과물'
        }
        
        with open(config_file, 'w', encoding='utf-8') as f:
            config.write(f)
        
        print(f"✅ 기본 설정 파일이 생성되었습니다: {config_file}")
        print("📝 config.ini 파일을 열어서 API 키를 입력해주세요!")

def check_dependencies():
    """필요한 패키지 확인"""
    # 패키지명과 실제 임포트명 매핑
    package_mapping = {
        'requests': 'requests',
        'pandas': 'pandas', 
        'openpyxl': 'openpyxl',
        'python-docx': 'docx',
        'beautifulsoup4': 'bs4'
    }
    
    missing_packages = []
    
    for package_name, import_name in package_mapping.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print("❌ 필요한 패키지가 설치되지 않았습니다:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 다음 명령어로 설치해주세요:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def validate_api_key(api_key):
    """API 키 유효성 검사"""
    if not api_key or api_key == '여기에_발급받은_API_키를_입력하세요':
        print("❌ API 키가 설정되지 않았습니다!")
        print("📝 config.ini 파일을 열어서 발급받은 API 키를 입력해주세요.")
        print("🔑 API 키 발급 방법은 README.md 파일을 참조하세요.")
        return False
    
    # 기본적인 형식 검사
    if len(api_key) < 50:
        print("⚠️ API 키가 너무 짧습니다. 올바른 키인지 확인해주세요.")
        return False
    
    return True

###########################
# 유틸리티 함수들
###########################

def sanitize_filename(filename):
    """파일명에 사용할 수 없는 문자를 제거하고 안전한 파일명으로 변환"""
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = filename.replace(' ', '_').replace('/', '_')
    filename = re.sub(r'_+', '_', filename)
    if len(filename) > 50:
        filename = filename[:50]
    return filename.strip('_')

def create_output_folder(base_folder):
    """출력 폴더 생성"""
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
        print(f"📁 결과물 폴더 생성: {os.path.abspath(base_folder)}")
    return os.path.abspath(base_folder)

def print_progress_bar(current, total, prefix='Progress', suffix='Complete', length=50):
    """진행률 표시 바"""
    percent = (current / total) * 100
    filled_length = int(length * current // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {current}/{total} ({percent:.1f}%) {suffix}', end='')
    if current == total:
        print()

###########################
# 핵심 데이터 수집 함수들
###########################

def get_all_housing_data(service_key, max_pages=None):
    """
    모든 주택 유형의 청약 분양정보를 수집하는 함수 (기한이 지나지 않은 것만)
    
    Args:
        service_key (str): 공공데이터포털에서 발급받은 API 키
        max_pages (int, optional): 각 API별 최대 페이지 수 제한 (None이면 모든 데이터)
    
    Returns:
        list: 모든 주택 유형의 청약 분양정보 리스트
    """
    
    # URL 인코딩된 키인 경우 디코딩
    decoded_key = urllib.parse.unquote(service_key)
    
    # 다양한 주택 유형별 API 엔드포인트
    housing_apis = {
        '아파트': 'getAPTLttotPblancDetail',
        '오피스텔': 'getOFTLttotPblancDetail',
        '도시형생활주택': 'getULHLttotPblancDetail',
        '민간임대': 'getRentLttotPblancDetail',
        '분양상가': 'getMMLttotPblancDetail'
    }
    
    all_data = []
    today = datetime.now().strftime('%Y-%m-%d')
    
    print("🏠 모든 주택 유형의 청약정보 수집을 시작합니다...")
    print(f"🔑 사용 API 키: {decoded_key[:20]}{'...' if len(decoded_key) > 20 else ''}")
    print("📅 기한이 지나지 않은 청약만 수집합니다")
    print("🏗️ 수집 대상: 아파트, 오피스텔, 도시형생활주택, 민간임대, 분양상가")
    print("=" * 80)
    
    total_apis = len(housing_apis)
    current_api = 0
    
    for housing_type, api_endpoint in housing_apis.items():
        current_api += 1
        print(f"\n🏠 [{current_api}/{total_apis}] {housing_type} 청약정보 수집 중...")
        
        base_url = f"http://api.odcloud.kr/api/ApplyhomeInfoDetailSvc/v1/{api_endpoint}"
        page = 1
        housing_data = []
        
        while True:
            # API 요청 파라미터 정리
            params = {
                'serviceKey': decoded_key,
                'page': page,
                'perPage': 100,  # 한 페이지당 최대 100건
                'returnType': 'json'
            }
            
            try:
                response = requests.get(base_url, params=params, timeout=30)
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                    except json.JSONDecodeError:
                        print(f"❌ {housing_type} {page}페이지 JSON 파싱 실패")
                        break
                    
                    if 'data' in data and len(data['data']) > 0:
                        page_data = data['data']
                        
                        # 데이터 정리 및 기한 필터링
                        for row in page_data:
                            # 접수종료일 확인 (다양한 필드명 고려)
                            end_date = (row.get('RCEPT_ENDDE') or 
                                      row.get('SUBSCRPT_RCEPT_ENDDE') or 
                                      row.get('RECEPT_ENDDE'))
                            
                            # 기한이 지나지 않은 청약만 포함
                            if end_date and end_date >= today:
                                housing_info = {
                                    '주택유형': housing_type,
                                    '주택관리번호': row.get('HOUSE_MANAGE_NO'),
                                    '공고번호': row.get('PBLANC_NO'),
                                    '주택명': row.get('HOUSE_NM'),
                                    '주택구분': row.get('HOUSE_SECD_NM'),
                                    '세부구분': row.get('HOUSE_DTL_SECD_NM'),
                                    '공급지역': row.get('SUBSCRPT_AREA_CODE_NM'),
                                    '모집공고일': row.get('RCRIT_PBLANC_DE'),
                                    '접수시작일': row.get('RCEPT_BGNDE'),
                                    '접수종료일': end_date,
                                    '계약시작일': row.get('CNTRCT_CNCLS_BGNDE'),
                                    '계약종료일': row.get('CNTRCT_CNCLS_ENDDE'),
                                    '문의처 전화번호': row.get('MDHS_TELNO'),
                                    '공급위치 주소': row.get('HSSPLY_ADRES'),
                                    '사업주체명': row.get('BSNS_MBY_NM'),
                                    '시공사명': row.get('CNSTRCT_ENTRPS_NM'),
                                    '입주예정월': row.get('MVN_PREARNGE_YM'),
                                    '분양가 상한제 여부': row.get('PARCPRC_ULS_AT'),
                                    '투기과열지구 여부': row.get('SPECLT_RDN_EARTH_AT'),
                                    '홈페이지 주소': row.get('HMPG_ADRES'),
                                    '모집공고 상세 URL': row.get('PBLANC_URL'),
                                    '당첨자 발표일': row.get('PRZWNER_PRESNATN_DE'),
                                    '일반공급 접수 시작일': row.get('GNRL_RCEPT_BGNDE'),
                                    '일반공급 접수 종료일': row.get('GNRL_RCEPT_ENDDE'),
                                    '총 공급세대수': row.get('TOT_SUPLY_HSHLDCO'),
                                    '모델번호': row.get('MODEL_NO'),
                                    '전용면적': row.get('EXCLUSE_AR'),
                                    '공급금액 (분양최고급액)': row.get('SUPLY_AMOUNT'),
                                    '청약신청금': row.get('SUBSCRPT_REQST_AMOUNT'),
                                    '주택형': row.get('HOUSE_TY'),
                                    '청약접수 시작일': row.get('SUBSCRPT_RCEPT_BGNDE'),
                                    '청약접수 종료일': row.get('SUBSCRPT_RCEPT_ENDDE')
                                }
                                housing_data.append(housing_info)
                        
                        print(f"✅ {housing_type} {page}페이지: {len(page_data)}건 수집 완료 (진행중: {len([h for h in housing_data if h['주택유형'] == housing_type])}건)")
                        
                        # 다음 페이지가 없거나 max_pages 제한에 도달하면 종료
                        if len(page_data) < 100 or (max_pages and page >= max_pages):
                            break
                        
                        page += 1
                    else:
                        print(f"📄 {housing_type} {page}페이지: 더 이상 데이터가 없습니다.")
                        break
                        
                elif response.status_code == 404:
                    print(f"❌ {housing_type} API를 찾을 수 없습니다 (404) - 지원하지 않는 주택 유형일 수 있습니다.")
                    break
                else:
                    print(f"❌ {housing_type} API 요청 실패: HTTP {response.status_code}")
                    if page == 1:  # 첫 페이지 실패시에만 상세 에러 출력
                        print(f"❌ 응답 내용: {response.text[:200]}...")
                    break
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ {housing_type} 네트워크 오류: {str(e)}")
                break
            except Exception as e:
                print(f"❌ {housing_type} 예상치 못한 오류: {str(e)}")
                break
        
        # 해당 주택 유형의 수집 결과 추가
        type_count = len([h for h in housing_data if h['주택유형'] == housing_type])
        if type_count > 0:
            all_data.extend([h for h in housing_data if h['주택유형'] == housing_type])
            print(f"✅ {housing_type} 수집 완료: {type_count}건")
        else:
            print(f"⚠️ {housing_type}: 진행 중인 청약이 없습니다.")
        
        # API 호출 간격 조절 (서버 부하 방지)
        time.sleep(0.5)
    
    print(f"\n" + "=" * 80)
    print(f"🎉 모든 주택 유형 수집 완료! 총 {len(all_data)}건의 청약정보를 수집했습니다.")
    
    # 주택 유형별 요약
    type_summary = {}
    for item in all_data:
        housing_type = item.get('주택유형', 'Unknown')
        type_summary[housing_type] = type_summary.get(housing_type, 0) + 1
    
    if type_summary:
        print("📊 주택 유형별 수집 현황:")
        for house_type, count in type_summary.items():
            print(f"   🏠 {house_type}: {count}건")
    
    return all_data

def fetch_recruitment_notice_content(url, max_retries=3):
    """모집공고 상세 페이지에서 공고문 내용을 크롤링"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 공고문 내용 추출 (청약홈 사이트 구조에 따라)
            content_sections = []
            
            # 주요 정보 테이블들 추출
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                table_content = []
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        cell_texts = [cell.get_text(strip=True) for cell in cells]
                        table_content.append(' | '.join(cell_texts))
                
                if table_content:
                    content_sections.append('\n'.join(table_content))
            
            # div 내용들도 추출
            content_divs = soup.find_all('div', class_=['content', 'detail-content', 'notice-content'])
            for div in content_divs:
                text = div.get_text(strip=True)
                if len(text) > 50:  # 의미있는 내용만
                    content_sections.append(text)
            
            # 전체 텍스트가 너무 짧으면 body 전체에서 추출
            full_content = '\n\n'.join(content_sections)
            if len(full_content) < 200:
                body = soup.find('body')
                if body:
                    full_content = body.get_text(separator='\n', strip=True)
            
            # 텍스트 정리
            full_content = re.sub(r'\n\s*\n', '\n\n', full_content)  # 빈 줄 정리
            full_content = re.sub(r'\s+', ' ', full_content)  # 공백 정리
            
            return full_content[:50000]  # 최대 50,000자로 제한
            
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                return f"크롤링 실패: {str(e)}"
    
    return "크롤링 실패: 최대 재시도 횟수 초과"

###########################
# 파일 저장 함수들
###########################

def save_to_excel(data, filename):
    """엑셀 파일로 저장"""
    print(f"\n📊 엑셀 파일 생성 중: {filename}")
    
    df = pd.DataFrame(data)
    
    # 향후 청약 가능한 분양정보 필터링 (접수시작일이 오늘 이후)
    today = datetime.now().strftime("%Y-%m-%d")
    future_subscriptions = df[df['접수시작일'] >= today] if '접수시작일' in df.columns else pd.DataFrame()
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # 전체 데이터
        df.to_excel(writer, sheet_name='전체_청약정보', index=False)
        
        # 향후 청약 가능 데이터
        if not future_subscriptions.empty:
            future_subscriptions.to_excel(writer, sheet_name='향후_청약_가능', index=False)
        
        print(f"✅ 전체 데이터: {len(df)}건")
        print(f"✅ 향후 청약 가능: {len(future_subscriptions)}건")
    
    print(f"💾 엑셀 파일 저장 완료: {filename}")

def save_to_json(data, filename):
    """JSON 파일로 저장"""
    print(f"\n🔧 JSON 파일 생성 중: {filename}")
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 JSON 파일 저장 완료: {filename}")

def create_detailed_markdown(data, filename):
    """상세한 마크다운 파일 생성 (공고문 포함)"""
    print(f"\n📝 마크다운 파일 생성 중: {filename}")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# 🏠 전체 주택유형 청약정보 ({len(data)}건)\n\n")
        
        # 주택 유형별 요약
        type_summary = {}
        for item in data:
            housing_type = item.get('주택유형', 'Unknown')
            type_summary[housing_type] = type_summary.get(housing_type, 0) + 1
        
        if type_summary:
            f.write("## 📊 주택 유형별 현황\n\n")
            for house_type, count in type_summary.items():
                f.write(f"- **{house_type}**: {count}건\n")
            f.write("\n")
        
        f.write(f"**생성일시:** {datetime.now().strftime('%Y년 %m월 %d일 %H시 %M분')}\n\n")
        f.write("---\n\n")
        
        for i, item in enumerate(data, 1):
            f.write(f"## {i}. {item.get('주택명', '이름없음')}\n\n")
            
            # 주택 유형 배지 추가
            housing_type = item.get('주택유형', 'N/A')
            region = str(item.get('공급지역', 'N/A')).replace('-', '--')
            house_type = str(item.get('주택구분', 'N/A')).replace('-', '--')
            
            f.write(f"![주택유형](https://img.shields.io/badge/주택유형-{housing_type}-blue) ")
            f.write(f"![지역](https://img.shields.io/badge/지역-{region}-green) ")
            f.write(f"![유형](https://img.shields.io/badge/유형-{house_type}-orange)\n\n")
            
            # 상태 배지
            today = datetime.now().strftime("%Y-%m-%d")
            reception_start = str(item.get('접수시작일', ''))
            if reception_start and reception_start >= today:
                f.write("![상태](https://img.shields.io/badge/상태-접수예정-blue)\n\n")
            elif reception_start and reception_start != 'N/A':
                f.write("![상태](https://img.shields.io/badge/상태-접수완료-gray)\n\n")
            
            # 기본 정보
            f.write("### 📋 기본 정보\n\n")
            f.write("| 항목 | 내용 |\n")
            f.write("|------|------|\n")
            f.write(f"| 주택유형 | {item.get('주택유형', 'N/A')} |\n")
            f.write(f"| 주택구분 | {item.get('주택구분', 'N/A')} |\n")
            f.write(f"| 세부구분 | {item.get('세부구분', 'N/A')} |\n")
            f.write(f"| 공급지역 | {item.get('공급지역', 'N/A')} |\n")
            f.write(f"| 공급주소 | {item.get('공급위치 주소', 'N/A')} |\n")
            f.write(f"| 총 공급세대 | {item.get('총 공급세대수', 'N/A')} |\n")
            f.write(f"| 전용면적 | {item.get('전용면적', 'N/A')} |\n")
            f.write(f"| 입주예정월 | {item.get('입주예정월', 'N/A')} |\n")
            
            # 일정 정보
            f.write("\n### 📅 청약 일정\n\n")
            f.write("| 항목 | 일정 |\n")
            f.write("|------|------|\n")
            f.write(f"| 모집공고일 | {item.get('모집공고일', 'N/A')} |\n")
            f.write(f"| 접수시작일 | {item.get('접수시작일', 'N/A')} |\n")
            f.write(f"| 접수종료일 | {item.get('접수종료일', 'N/A')} |\n")
            f.write(f"| 당첨발표일 | {item.get('당첨자 발표일', 'N/A')} |\n")
            f.write(f"| 계약시작일 | {item.get('계약시작일', 'N/A')} |\n")
            f.write(f"| 계약종료일 | {item.get('계약종료일', 'N/A')} |\n")
            
            # 연락처 정보
            f.write("\n### 📞 연락처 및 사업정보\n\n")
            f.write("| 항목 | 내용 |\n")
            f.write("|------|------|\n")
            f.write(f"| 사업주체 | {item.get('사업주체명', 'N/A')} |\n")
            f.write(f"| 시공사 | {item.get('시공사명', 'N/A')} |\n")
            f.write(f"| 문의전화 | {item.get('문의처 전화번호', 'N/A')} |\n")
            
            # 링크 정보
            if item.get('홈페이지 주소') and str(item.get('홈페이지 주소')) != 'N/A':
                f.write(f"| 홈페이지 | [{item.get('홈페이지 주소')}]({item.get('홈페이지 주소')}) |\n")
            if item.get('모집공고 상세 URL') and str(item.get('모집공고 상세 URL')) != 'N/A':
                f.write(f"| 모집공고 | [{item.get('모집공고 상세 URL')}]({item.get('모집공고 상세 URL')}) |\n")
            
            # 모집공고문 전문 (있는 경우)
            notice_content = item.get('모집공고문_전문', '')
            if notice_content and notice_content != "URL 없음" and not notice_content.startswith("크롤링 실패"):
                f.write("\n### 📄 모집공고문 전문\n\n")
                f.write("```\n")
                f.write(notice_content[:5000])  # 최대 5,000자
                if len(notice_content) > 5000:
                    f.write("\n\n... (전문이 길어 일부만 표시됨) ...")
                f.write("\n```\n\n")
            
            f.write("---\n\n")
    
    print(f"💾 마크다운 파일 저장 완료: {filename}")

###########################
# 메인 실행 함수
###########################

def main():
    """메인 실행 함수"""
    
    print("🏠 부동산 청약정보 수집 프로그램 v3.0")
    print("=" * 60)
    print("🏗️ 아파트, 오피스텔, 도시형생활주택, 민간임대, 분양상가")
    print("📅 접수기한이 지나지 않은 청약만 수집")
    print("=" * 60)
    
    # 1. 의존성 확인
    print("\n🔍 1단계: 필요 패키지 확인...")
    if not check_dependencies():
        return
    print("✅ 모든 필요 패키지가 설치되어 있습니다.")
    
    # 2. 설정 로드
    print("\n⚙️ 2단계: 설정 파일 로드...")
    config = Config()
    
    # 3. API 키 검증
    print("\n🔑 3단계: API 키 검증...")
    if not validate_api_key(config.api_key):
        return
    print("✅ API 키가 설정되어 있습니다.")
    
    # 4. 출력 폴더 생성
    print("\n📁 4단계: 출력 폴더 준비...")
    output_folder = create_output_folder(config.output_folder)
    
    # 5. 데이터 수집
    print("\n📊 5단계: 청약정보 수집...")
    try:
        subscription_data = get_all_housing_data(config.api_key, config.max_pages)
        
        if not subscription_data:
            print("⚠️ 현재 진행 중인 청약이 없습니다.")
            return
        
        print(f"✅ 총 {len(subscription_data)}건의 청약정보를 수집했습니다.")
        
    except Exception as e:
        print(f"❌ 데이터 수집 중 오류 발생: {str(e)}")
        return
    
    # 6. 공고문 크롤링 (선택사항)
    print(f"\n📄 6단계: 모집공고문 크롤링...")
    crawl_notices = input("모집공고문도 크롤링하시겠습니까? (y/N): ").lower().strip()
    
    if crawl_notices == 'y':
        print("🕷️ 모집공고문 크롤링을 시작합니다...")
        
        for i, item in enumerate(subscription_data, 1):
            notice_url = item.get('모집공고 상세 URL')
            if notice_url and str(notice_url) != 'N/A':
                print(f"[{i}/{len(subscription_data)}] 크롤링: {item.get('주택명', '이름없음')}")
                notice_content = fetch_recruitment_notice_content(notice_url)
                item['모집공고문_전문'] = notice_content
                
                # 진행률 표시
                print_progress_bar(i, len(subscription_data), prefix='크롤링 진행', suffix='완료')
                time.sleep(1)  # 서버 부하 방지
            else:
                item['모집공고문_전문'] = "URL 없음"
        
        print("\n✅ 모집공고문 크롤링 완료!")
    else:
        print("⏭️ 모집공고문 크롤링을 건너뜁니다.")
    
    # 7. 결과 파일 저장
    print("\n💾 7단계: 결과 파일 생성...")
    current_date = datetime.now().strftime("%Y%m%d")
    
    try:
        # JSON 파일 저장
        json_filename = os.path.join(output_folder, f"청약정보_{current_date}.json")
        save_to_json(subscription_data, json_filename)
        
        # 엑셀 파일 저장
        excel_filename = os.path.join(output_folder, f"청약정보_{current_date}.xlsx")
        save_to_excel(subscription_data, excel_filename)
        
        # 마크다운 파일 저장
        md_filename = os.path.join(output_folder, f"청약정보_{current_date}.md")
        create_detailed_markdown(subscription_data, md_filename)
        
        print("\n" + "=" * 60)
        print("🎉 청약정보 수집이 완료되었습니다!")
        print("=" * 60)
        print(f"📊 총 수집 건수: {len(subscription_data)}건")
        
        # 주택 유형별 요약
        type_summary = {}
        for item in subscription_data:
            housing_type = item.get('주택유형', 'Unknown')
            type_summary[housing_type] = type_summary.get(housing_type, 0) + 1
        
        if type_summary:
            print("\n📋 주택 유형별 수집 결과:")
            for house_type, count in type_summary.items():
                print(f"   🏠 {house_type}: {count}건")
        
        print(f"\n📁 저장 위치: {output_folder}")
        print("📋 생성된 파일:")
        print(f"   📊 {os.path.basename(excel_filename)} - 엑셀 파일")
        print(f"   📝 {os.path.basename(md_filename)} - 마크다운 파일")
        print(f"   🔧 {os.path.basename(json_filename)} - JSON 파일")
        
    except Exception as e:
        print(f"❌ 파일 저장 중 오류 발생: {str(e)}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ 사용자에 의해 프로그램이 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류가 발생했습니다: {str(e)}")
        print("📞 문제가 지속되면 README.md 파일의 문의처를 확인해주세요.")