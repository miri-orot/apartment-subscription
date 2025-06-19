#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏠 부동산 청약정보 수집 프로그램 v3.0 - 설치 스크립트

이 스크립트는 프로그램 실행을 위한 환경을 자동으로 설정합니다.
"""

import os
import sys
import subprocess
import platform

def print_header():
    """프로그램 헤더 출력"""
    print("=" * 60)
    print("🏠 부동산 청약정보 수집 프로그램 v3.0 설치")
    print("=" * 60)
    print("📋 이 스크립트는 다음을 자동으로 수행합니다:")
    print("   1. Python 버전 확인")
    print("   2. 가상환경 생성")
    print("   3. 필요 패키지 설치")
    print("   4. 설정 파일 생성")
    print("=" * 60)

def check_python_version():
    """Python 버전 확인"""
    print("\n🔍 Python 버전 확인 중...")
    
    version = sys.version_info
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} 감지됨")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 이상이 필요합니다!")
        print("📥 https://www.python.org/downloads/ 에서 최신 버전을 다운로드하세요.")
        return False
    
    return True

def create_virtual_environment():
    """가상환경 생성"""
    print("\n🏗️ 가상환경 생성 중...")
    
    venv_name = "apartment_env"
    
    if os.path.exists(venv_name):
        print(f"✅ 가상환경 '{venv_name}'이 이미 존재합니다.")
        return venv_name
    
    try:
        subprocess.run([sys.executable, "-m", "venv", venv_name], check=True)
        print(f"✅ 가상환경 '{venv_name}' 생성 완료")
        return venv_name
    except subprocess.CalledProcessError as e:
        print(f"❌ 가상환경 생성 실패: {e}")
        return None

def install_packages(venv_name):
    """필요 패키지 설치"""
    print("\n📦 필요 패키지 설치 중...")
    
    # 가상환경의 pip 경로 확인
    system = platform.system()
    if system == "Windows":
        pip_path = os.path.join(venv_name, "Scripts", "pip")
        python_path = os.path.join(venv_name, "Scripts", "python")
    else:
        pip_path = os.path.join(venv_name, "bin", "pip")
        python_path = os.path.join(venv_name, "bin", "python")
    
    # pip 업그레이드
    try:
        subprocess.run([python_path, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        print("✅ pip 업그레이드 완료")
    except subprocess.CalledProcessError:
        print("⚠️ pip 업그레이드 건너뜀")
    
    # requirements.txt 파일 확인 및 설치
    if os.path.exists("requirements.txt"):
        try:
            subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
            print("✅ requirements.txt 패키지 설치 완료")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 패키지 설치 실패: {e}")
    
    # 개별 패키지 설치
    packages = [
        "requests>=2.25.1",
        "pandas>=1.3.0",
        "openpyxl>=3.0.7",
        "python-docx>=0.8.11",
        "beautifulsoup4>=4.9.3",
        "lxml>=4.6.3"
    ]
    
    for package in packages:
        try:
            subprocess.run([pip_path, "install", package], check=True)
            print(f"✅ {package.split('>=')[0]} 설치 완료")
        except subprocess.CalledProcessError as e:
            print(f"❌ {package} 설치 실패: {e}")
            return False
    
    return True

def create_config_file():
    """설정 파일 생성"""
    print("\n⚙️ 설정 파일 생성 중...")
    
    config_content = """[API]
service_key = 여기에_발급받은_API_키를_입력하세요

[SETTINGS]
max_pages = 50
max_items_per_file = 10

[PATHS]
output_folder = 결과물
"""
    
    try:
        with open("config.ini", "w", encoding="utf-8") as f:
            f.write(config_content)
        print("✅ config.ini 파일 생성 완료")
        return True
    except Exception as e:
        print(f"❌ 설정 파일 생성 실패: {e}")
        return False

def print_instructions(venv_name):
    """사용 방법 안내"""
    system = platform.system()
    
    if system == "Windows":
        activate_cmd = f"{venv_name}\\Scripts\\activate"
    else:
        activate_cmd = f"source {venv_name}/bin/activate"
    
    print("\n" + "=" * 60)
    print("🎉 설치가 완료되었습니다!")
    print("=" * 60)
    print("📝 다음 단계를 진행하세요:")
    print()
    print("1. API 키 설정:")
    print("   - config.ini 파일을 텍스트 에디터로 열기")
    print("   - service_key 값을 발급받은 API 키로 변경")
    print("   - 파일 저장")
    print()
    print("2. 프로그램 실행:")
    if system == "Windows":
        print(f"   {activate_cmd}")
        print("   python apartment_subscription_collector.py")
    else:
        print(f"   {activate_cmd}")
        print("   python apartment_subscription_collector.py")
    print()
    print("🔑 API 키 발급 방법은 README.md 파일을 참조하세요!")
    print("📞 문제가 있으면 README.md의 문제 해결 섹션을 확인하세요.")
    print("=" * 60)

def main():
    """메인 함수"""
    print_header()
    
    # Python 버전 확인
    if not check_python_version():
        return False
    
    # 가상환경 생성
    venv_name = create_virtual_environment()
    if not venv_name:
        return False
    
    # 패키지 설치
    if not install_packages(venv_name):
        print("\n❌ 패키지 설치 중 오류가 발생했습니다.")
        print("💡 수동으로 다음 명령어를 실행해보세요:")
        print(f"   {venv_name}/bin/activate")  # Linux/macOS
        print("   pip install -r requirements.txt")
        return False
    
    # 설정 파일 생성
    if not create_config_file():
        return False
    
    # 사용 방법 안내
    print_instructions(venv_name)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️ 설치가 사용자에 의해 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류가 발생했습니다: {e}")
        sys.exit(1) 