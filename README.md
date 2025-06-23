# 🏠 부동산 청약정보 수집 프로그램 v3.0

**한국부동산원 청약홈 API를 활용하여 모든 주택유형의 최신 청약 분양정보를 수집하고 다양한 형태로 저장하는 종합 프로그램**

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## 📋 목차

- [주요 기능](#-주요-기능)
- [지원하는 주택 유형](#-지원하는-주택-유형)
- [API 키 발급 방법](#-api-키-발급-방법)
- [설치 및 설정](#-설치-및-설정)
- [사용 방법](#-사용-방법)
- [출력 파일 형태](#-출력-파일-형태)
- [문제 해결](#-문제-해결)
- [자주 묻는 질문](#-자주-묻는-질문)
- [업데이트 내역](#-업데이트-내역)
- [라이선스](#-라이선스)

## ✨ 주요 기능

- 🔄 **실시간 데이터 수집**: 한국부동산원 청약홈 API 연동
- 🏠 **5가지 주택유형 지원**: 아파트, 오피스텔, 도시형생활주택, 민간임대, 분양상가
- 📊 **3가지 출력 형태**: 엑셀, 마크다운, JSON
- 🕷️ **모집공고문 크롤링**: 상세한 공고문 내용까지 수집 (선택사항)
- 📈 **진행중인 청약만 필터링**: 접수기한이 지나지 않은 청약정보만 수집
- ⚙️ **설정 파일 지원**: 사용자 맞춤 설정 가능
- 🔧 **오류 처리**: 상세한 오류 메시지와 복구 가이드

## 🏗️ 지원하는 주택 유형

| 주택 유형 | API 엔드포인트 | 설명 |
|----------|---------------|------|
| 🏢 **아파트** | getAPTLttotPblancDetail | 일반 아파트 분양정보 |
| 🏬 **오피스텔** | getOFTLttotPblancDetail | 오피스텔 분양정보 |
| 🏘️ **도시형생활주택** | getULHLttotPblancDetail | 도시형생활주택 분양정보 |
| 🏠 **민간임대** | getRentLttotPblancDetail | 민간임대주택 정보 |
| 🏪 **분양상가** | getMMLttotPblancDetail | 상업시설 분양정보 |

## 🔑 API 키 발급 방법

### 1단계: 공공데이터포털 회원가입

1. **공공데이터포털 접속**
   - 웹브라우저에서 [https://www.data.go.kr](https://www.data.go.kr) 접속
   
2. **회원가입 진행**
   - 우측 상단 **"회원가입"** 클릭
   - **"개인회원"** 선택
   - 필수 정보 입력 (이름, 이메일, 휴대폰 등)
   - 이메일 인증 완료

### 2단계: API 서비스 신청

1. **API 페이지 접속**
   - [한국부동산원_청약홈 분양정보 조회 서비스](https://www.data.go.kr/data/15098547/openapi.do) 페이지로 이동
   
2. **활용신청 클릭**
   - 페이지 중앙의 **"활용신청"** 버튼 클릭
   
3. **개발계정 신청**
   ```
   신청구분: 개발계정
   활용목적: 개인 프로젝트 (또는 해당 목적)
   상세설명: 부동산 청약정보 분석 및 개인 학습용
   ```
   
4. **신청 완료**
   - 개발계정은 **즉시 승인**됩니다
   - 승인 완료 이메일 확인

### 3단계: API 키 확인 및 복사

1. **마이페이지 접속**
   - 로그인 후 우측 상단 **"마이페이지"** 클릭
   
2. **인증키 관리**
   - 좌측 메뉴에서 **"OpenAPI"** → **"인증키 관리"** 클릭
   
3. **API 키 복사**
   - **"일반 인증키(Encoding)"** 항목의 키를 전체 복사
   - 예시: `8hh8AZ2jOVkKYsVopVoWsnoKAkzJjYt6h4kQbqII9Wtohox3TJtCNvDCwl9M2rf0KgSm%2BDt0%2FQC%2B1obZC9uuZQ%3D%3D`

## 💻 설치 및 설정

### 시스템 요구사항

- **Python**: 3.8 이상
- **운영체제**: Windows, macOS, Linux
- **메모리**: 최소 2GB RAM 권장
- **디스크**: 최소 100MB 여유 공간

### 1단계: 프로그램 다운로드

```bash
# Git으로 다운로드 (권장)
git clone https://github.com/your-repo/apartment-subscription-collector.git
cd apartment-subscription-collector

# 또는 ZIP 파일 다운로드 후 압축 해제
```

### 2단계: 가상환경 생성 (권장)

```bash
# 가상환경 생성
python3 -m venv apartment_env

# 가상환경 활성화
# Windows:
apartment_env\Scripts\activate

# macOS/Linux:
source apartment_env/bin/activate
```

### 3단계: 패키지 설치

```bash
# 필요한 패키지 설치
pip install -r requirements.txt

# 또는 개별 설치
pip install requests pandas openpyxl python-docx beautifulsoup4 lxml
```

### 4단계: 설정 파일 구성

1. **프로그램 첫 실행**
   ```bash
   python apartment_subscription_collector.py
   ```
   
2. **config.ini 파일 자동 생성됨**
   ```ini
   [API]
   service_key = 여기에_발급받은_API_키를_입력하세요

   [SETTINGS]
   max_pages = 50
   max_items_per_file = 10

   [PATHS]
   output_folder = 결과물
   ```

3. **API 키 입력**
   - `config.ini` 파일을 텍스트 에디터로 열기
   - `service_key` 값을 발급받은 API 키로 교체
   - 파일 저장

## 🚀 사용 방법

### 기본 실행

```bash
# 프로그램 실행
python apartment_subscription_collector.py
```

### 실행 단계별 안내

**1단계: 패키지 확인**
```
🔍 1단계: 필요 패키지 확인...
✅ 모든 필요 패키지가 설치되어 있습니다.
```

**2단계: 설정 로드**
```
⚙️ 2단계: 설정 파일 로드...
✅ 설정 파일을 성공적으로 로드했습니다.
```

**3단계: API 키 검증**
```
🔑 3단계: API 키 검증...
✅ API 키가 설정되어 있습니다.
```

**4단계: 출력 폴더 준비**
```
📁 4단계: 출력 폴더 준비...
📁 결과물 폴더 생성: /path/to/결과물
```

**5단계: 청약정보 수집**
```
📊 5단계: 청약정보 수집...
🏠 [1/5] 아파트 청약정보 수집 중...
✅ 아파트 수집 완료: 156건
🏠 [2/5] 오피스텔 청약정보 수집 중...
✅ 오피스텔 수집 완료: 23건
...
```

**6단계: 모집공고문 크롤링 (선택)**
```
📄 6단계: 모집공고문 크롤링...
모집공고문도 크롤링하시겠습니까? (y/N): y
🕷️ 모집공고문 크롤링을 시작합니다...
크롤링 진행 |████████████████████████████████████████████████| 156/156 (100.0%) 완료
```

**7단계: 결과 파일 생성**
```
💾 7단계: 결과 파일 생성...
📊 엑셀 파일 생성 중: 결과물/청약정보_20250619.xlsx
📝 마크다운 파일 생성 중: 결과물/청약정보_20250619.md
🔧 JSON 파일 생성 중: 결과물/청약정보_20250619.json
```

### 설정 옵션 변경

**config.ini 파일 수정:**

```ini
[API]
# 발급받은 API 키
service_key = 여기에_실제_API_키_입력

[SETTINGS]
# 각 주택유형별 최대 수집 페이지 수 (1페이지 = 100건)
max_pages = 50

# NotebookLM용 파일의 항목당 개수
max_items_per_file = 10

[PATHS]
# 결과 파일이 저장될 폴더명
output_folder = 결과물
```

## 📁 출력 파일 형태

프로그램 실행 후 `결과물/` 폴더에 다음 파일들이 생성됩니다:

### 1. 📊 엑셀 파일 (`청약정보_YYYYMMDD.xlsx`)

**시트 구성:**
- **전체_청약정보**: 모든 수집된 데이터
- **향후_청약_가능**: 접수예정인 분양정보만

**주요 컬럼:**
| 컬럼명 | 설명 | 예시 |
|--------|------|------|
| 주택유형 | 수집된 주택의 종류 | 아파트, 오피스텔 |
| 주택명 | 분양하는 주택의 이름 | 힐스테이트 강남 |
| 공급지역 | 분양 지역 | 서울특별시 강남구 |
| 접수시작일 | 청약 접수 시작일 | 2025-06-25 |
| 접수종료일 | 청약 접수 종료일 | 2025-06-27 |
| 총 공급세대수 | 공급할 총 세대 수 | 324 |

### 2. 📝 마크다운 파일 (`청약정보_YYYYMMDD.md`)

**구성 요소:**
- 📊 주택 유형별 현황 요약
- 🏠 각 분양정보별 상세 정보
- 🏷️ 시각적 배지 (상태, 지역, 유형)
- 📅 청약 일정 테이블
- 📞 연락처 및 사업정보
- 📄 모집공고문 전문 (크롤링한 경우)

### 3. 🔧 JSON 파일 (`청약정보_YYYYMMDD.json`)

**데이터 구조:**
```json
[
  {
    "주택유형": "아파트",
    "주택관리번호": "2025000123",
    "주택명": "힐스테이트 강남",
    "주택구분": "민영",
    "공급지역": "서울특별시 강남구",
    "접수시작일": "2025-06-25",
    "접수종료일": "2025-06-27",
    "총 공급세대수": "324",
    "모집공고문_전문": "상세 공고문 내용..."
  }
]
```

## 🔧 문제 해결

### 자주 발생하는 오류와 해결방법

#### 1. API 키 관련 오류

**오류 메시지:**
```
❌ API 키가 설정되지 않았습니다!
```

**해결 방법:**
1. `config.ini` 파일이 있는지 확인
2. 파일 내 `service_key` 값 확인
3. API 키가 올바르게 복사되었는지 확인
4. 공공데이터포털에서 API 서비스 승인 상태 확인

#### 2. 패키지 설치 오류

**오류 메시지:**
```
❌ 필요한 패키지가 설치되지 않았습니다:
   - pandas
   - openpyxl
```

**해결 방법:**
```bash
# 가상환경 활성화 확인
source apartment_env/bin/activate  # macOS/Linux
# 또는
apartment_env\Scripts\activate  # Windows

# 패키지 재설치
pip install --upgrade pip
pip install -r requirements.txt

# 개별 패키지 설치
pip install pandas openpyxl python-docx beautifulsoup4
```

#### 3. 네트워크 연결 오류

**오류 메시지:**
```
❌ 아파트 네트워크 오류: Connection timeout
```

**해결 방법:**
1. 인터넷 연결 상태 확인
2. 방화벽 설정 확인
3. VPN 사용 시 비활성화 후 재시도
4. API 서버 상태 확인 (공공데이터포털 공지사항)

#### 4. 권한 오류

**오류 메시지:**
```
❌ 파일 저장 중 오류 발생: Permission denied
```

**해결 방법:**
```bash
# 현재 디렉토리 권한 확인
ls -la

# 권한 변경 (macOS/Linux)
chmod 755 .

# Windows에서는 관리자 권한으로 실행
```

### 로그 파일 확인

프로그램 실행 중 오류가 발생하면 다음 정보를 확인하세요:

1. **콘솔 출력**: 실행 중 표시되는 모든 메시지
2. **config.ini**: 설정 파일 내용
3. **Python 버전**: `python --version`
4. **패키지 버전**: `pip list`

## ❓ 자주 묻는 질문

### Q1. API 사용량 제한이 있나요?

**A:** 개발계정 기준으로 **일 40,000건**까지 요청 가능합니다. 현재 프로그램으로 수집하는 데이터는 약 2,000-3,000건 정도이므로 여유가 충분합니다.

### Q2. 크롤링이 실패하는 이유는?

**A:** 다음과 같은 이유로 크롤링이 실패할 수 있습니다:
- 모집공고 URL이 유효하지 않음
- 웹사이트 구조 변경
- 네트워크 연결 불안정
- 서버 부하로 인한 일시적 접근 제한

### Q3. 데이터가 실시간으로 업데이트되나요?

**A:** 네, 한국부동산원 API에서 제공하는 실시간 데이터를 수집합니다. 다만 API 서버의 업데이트 주기에 따라 약간의 지연이 있을 수 있습니다.

### Q4. 과거 청약 정보도 수집할 수 있나요?

**A:** 이 프로그램은 **현재 진행 중인 청약**(접수기한이 지나지 않은)만 수집합니다. 과거 청약 정보가 필요한 경우 별도 API나 데이터 소스를 이용해야 합니다.

### Q5. Mac/Linux에서도 동작하나요?

**A:** 네, Python으로 작성되어 Windows, macOS, Linux에서 모두 동작합니다. 다만 패키지 설치 명령어나 가상환경 활성화 방법이 운영체제별로 다를 수 있습니다.

### Q6. 설정 파일을 삭제했어요.

**A:** 프로그램을 다시 실행하면 `config.ini` 파일이 자동으로 생성됩니다. API 키만 다시 입력하면 됩니다.

### Q7. 특정 지역만 수집할 수 있나요?

**A:** 현재 버전에서는 모든 지역의 데이터를 수집한 후 엑셀이나 JSON 파일에서 필터링하여 사용하시면 됩니다. 향후 버전에서 지역 필터 기능을 추가할 예정입니다.

## 📈 API 사용량 모니터링

### 사용량 확인 방법

1. **공공데이터포털 로그인**
2. **마이페이지** → **OpenAPI** → **사용현황**
3. 일별/월별 사용량 확인

### 사용량 절약 팁

```python
# config.ini에서 페이지 수 제한
[SETTINGS]
max_pages = 10  # 적은 수로 설정하여 테스트

# 특정 주택유형만 수집하도록 코드 수정 (고급 사용자용)
```

## 🔒 보안 주의사항

### API 키 보안

1. **API 키 노출 금지**
   - GitHub, 블로그 등에 업로드 시 API 키 제거
   - `config.ini` 파일을 `.gitignore`에 추가

2. **키 관리**
   ```bash
   # config.ini 파일 권한 제한 (Linux/macOS)
   chmod 600 config.ini
   ```

3. **정기적 키 갱신**
   - 보안을 위해 주기적으로 API 키 재발급

## 📞 문의 및 지원

### 공식 지원 채널

- **공공데이터포털 고객센터**: 1566-0025
- **운영시간**: 09:00~18:00 (월~금)
- **이메일**: opendata@korea.kr

### 프로그램 관련 문의

프로그램 사용 중 문제가 발생하면 다음 정보와 함께 문의해주세요:

1. **운영체제**: Windows 10, macOS Big Sur 등
2. **Python 버전**: `python --version` 결과
3. **오류 메시지**: 전체 오류 메시지 복사
4. **실행 환경**: 가상환경 사용 여부
5. **설정 파일**: config.ini 내용 (API 키 제외)

## 🆕 업데이트 내역

### v3.0 (2025-06-19) - 배포용 버전
- ✅ **설정 파일 분리**: API 키 및 옵션을 config.ini로 분리
- ✅ **사용자 친화적 인터페이스**: 단계별 진행 안내
- ✅ **강화된 오류 처리**: 상세한 오류 메시지 및 해결 가이드
- ✅ **의존성 검사**: 자동 패키지 확인 및 설치 안내
- ✅ **진행률 표시**: 크롤링 진행 상황 시각화
- ✅ **선택적 크롤링**: 모집공고문 크롤링 여부 선택 가능

### v2.0 (2025-06-18)
- ✅ **모든 주택유형 지원**: 아파트, 오피스텔, 도시형생활주택, 민간임대, 분양상가
- ✅ **모집공고문 크롤링**: 상세 공고문 내용 수집
- ✅ **필터링 강화**: 진행 중인 청약만 수집

### v1.0 (2025-06-17)
- ✅ **기본 API 연동**: 아파트 분양정보 수집
- ✅ **다중 출력 형태**: 엑셀, 마크다운, JSON 지원

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

```
MIT License

Copyright (c) 2025 부동산 청약정보 수집 프로그램

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🎯 시작하기

준비가 되셨다면 다음 명령어로 시작하세요:

```bash
# 1. 패키지 설치
pip install -r requirements.txt

# 2. 프로그램 실행
python apartment_subscription_collector.py

# 3. API 키 설정 (config.ini 파일 수정)
# 4. 프로그램 재실행
```

**🏠 이제 최신 부동산 청약정보를 쉽게 수집하고 분석해보세요!** 