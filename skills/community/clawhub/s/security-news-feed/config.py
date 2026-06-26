# config.py
"""
이 파일은 프로젝트의 모든 설정값을 중앙에서 관리합니다.
환경 변수(.env)에서 API 키, 토큰, 데이터베이스 ID, 웹훅 URL 등을 로드합니다.
"""

import ssl
import os
import re
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

# .env 파일 로드 (상위 디렉토리 탐색)
import sys
from pathlib import Path

# 현재 파일에서부터 프로젝트 루트까지 .env 파일을 찾음
current_path = Path(__file__).resolve()
search_paths = [current_path]  # 현재 디렉토리
for _ in range(4):  # 최대 4단계 상위 경로 검색
    env_file = current_path / '.env'
    if env_file.exists():
        load_dotenv(env_file)
        break
    current_path = current_path.parent
else:
    # .env를 찾지 못하면 기본 동작 (현재 디�렉토리)
    load_dotenv()

# --- 전역 설정값 ---

# 스케줄러 실행 여부 (기본값: True)
RUN_SCHEDULER = os.getenv("RUN_SCHEDULER", "true").lower() == "true"

# SSL 인증서 검증 설정
# 보안: 기본값은 True (프로덕션에서 반드시 True 유지)
SSL_VERIFY = os.getenv("SSL_VERIFY", "true").lower() == "true"


def get_ssl_context():
    """
    SSL 컨텍스트 반환
    
    Returns:
        ssl.SSLContext: SSL 컨텍스트 (검증 활성화가 기본)
    
    WARNING: SSL_VERIFY=false는 개발 환경에서만 사용하세요.
    프로덕션에서는 반드시 True로 설정해야 MITM 공격을 방지할 수 있습니다.
    """
    context = ssl.create_default_context()
    
    if not SSL_VERIFY:
        # 개발 환경에서만 경고와 함께 비활성화
        print("[SECURITY WARNING] SSL verification is DISABLED. DO NOT USE IN PRODUCTION!")
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
    else:
        # 프로덕션: 검증 활성화 (기본값)
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
    
    return context


# 레거시 호환성을 위한 ssl_context (deprecated, get_ssl_context() 사용 권장)
ssl_context = get_ssl_context()

# Notion API 설정 (Security News Agent 전용)
NOTION_API_TOKEN = os.getenv("NOTION_API_KEY")
BOANISSUE_DATABASE_ID = os.getenv("SECURITY_NEWS_DATABASE_ID")
CVE_DATABASE_ID = os.getenv("SECURITY_CVE_DATABASE_ID", BOANISSUE_DATABASE_ID)
GUIDE_DATABASE_ID = os.getenv("SECURITY_GUIDE_DATABASE_ID", BOANISSUE_DATABASE_ID)
KEYWORD_STATS_DATABASE_ID = os.getenv("SECURITY_KEYWORD_STATS_DATABASE_ID", BOANISSUE_DATABASE_ID)

# LLM API (ZAI)
ZAI_API_KEY = os.getenv("SECURITY_NEWS_GLM_API_KEY") or os.getenv("GLM_API_KEY")

# LLM API (GLM - 지푸 인텔리전스)
SECURITY_LLM_API_KEY = os.getenv("SECURITY_NEWS_GLM_API_KEY") or os.getenv("GLM_API_KEY")
SECURITY_LLM_BASE_URL = os.getenv("GLM_BASE_URL", "https://api.z.ai/api/coding/paas/v4")
SECURITY_LLM_MODEL = os.getenv("SECURITY_LLM_MODEL", "glm-4.7")

# Slack Webhook URL (알림용)
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# Tistory 설정 (Selenium 자동화)
TISTORY_BLOG_NAME = os.getenv("TISTORY_BLOG_NAME", "rebugui")
CHROME_USER_DATA_DIR = os.getenv("CHROME_USER_DATA_DIR")
CHROME_PROFILE_NAME = os.getenv("CHROME_PROFILE_NAME", "Default")

# 발행 설정
ENABLE_NOTION_PUBLISHING = os.getenv("ENABLE_NOTION_PUBLISHING", "true").lower() == "true"
ENABLE_TISTORY_PUBLISHING = os.getenv("ENABLE_TISTORY_PUBLISHING", "false").lower() == "true"

# 주간 리포트(CVE, Weekly) 전용 발행 설정 (개별 제어)
ENABLE_WEEKLY_NOTION = os.getenv("ENABLE_WEEKLY_NOTION", "true").lower() == "true"
ENABLE_WEEKLY_TISTORY = os.getenv("ENABLE_WEEKLY_TISTORY", "false").lower() == "true"

# 스케줄러 설정 (추가)
SCHEDULER_INTERVAL_HOURS = int(os.getenv("SCHEDULER_INTERVAL_HOURS", "1"))  # 정기 크롤링 간격
KEYWORD_ANALYSIS_INTERVAL_HOURS = int(os.getenv("KEYWORD_ANALYSIS_INTERVAL_HOURS", "6"))  # 키워드 분석 간격

# 큐 및 스레드 설정 (메모리 관리)
MAX_QUEUE_SIZE = int(os.getenv("MAX_QUEUE_SIZE", "100"))  # 최대 큐 크기
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "2"))  # 최대 워커 스레드 수 (Chrome 메모리 최적화로 2로 감소)
MAX_CONSUMERS = int(os.getenv("MAX_CONSUMERS", "3"))  # 최대 컨슈머 스레드 수
MAX_ITEMS_PER_BATCH = int(os.getenv("MAX_ITEMS_PER_BATCH", "3"))  # 배치당 처리 건수

# Chrome 드라이버 설정 (메모리 최적화)
MAX_CHROME_DRIVERS = int(os.getenv("MAX_CHROME_DRIVERS", "2"))  # 동시 실행 Chrome 드라이버 최대 수
CHROME_DRIVER_TIMEOUT = int(os.getenv("CHROME_DRIVER_TIMEOUT", "30"))  # Chrome 드라이버 타임아웃 (초)
CHROME_HEADLESS_MODE = os.getenv("CHROME_HEADLESS_MODE", "new")  # headless 모드 (new 또는 old)

# LLM 캐시 설정
LLM_CACHE_MAX_SIZE = int(os.getenv("LLM_CACHE_MAX_SIZE", "1000"))  # LLM 캐시 최대 크기
LLM_CACHE_TTL_HOURS = int(os.getenv("LLM_CACHE_TTL_HOURS", "24"))  # LLM 캐시 TTL (시간)


# ========================
# 설정 검증 유틸리티
# ========================

class ConfigValidationError(ValueError):
    """설정 검증 오류"""
    pass


def _validate_required(value: Any, name: str) -> Any:
    """필수값 검증"""
    if value is None or (isinstance(value, str) and not value.strip()):
        raise ConfigValidationError(f"필수 환경 변수가 누락되었습니다: {name}")
    return value


def _validate_url(value: Optional[str], name: str) -> Optional[str]:
    """URL 형식 검증"""
    if value and value.strip():
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if not url_pattern.match(value.strip()):
            raise ConfigValidationError(f"잘못된 URL 형식: {name}={value}")
    return value


def _validate_database_id(value: Optional[str], name: str) -> Optional[str]:
    """Notion Database ID 형식 검증 (32자 hex)"""
    if value and value.strip():
        cleaned = value.strip()
        if len(cleaned) != 32 or not re.match(r'^[a-f0-9]{32}$', cleaned):
            print(f"[Warning] {name} 형식이 올바르지 않을 수 있습니다: {cleaned}")
    return value


def _validate_boolean(value: Any, name: str, default: bool) -> bool:
    """불리언 값 검증"""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ('true', '1', 'yes', 'on')
    return default


def _validate_int_range(value: Any, name: str, min_val: int, max_val: int, default: int) -> int:
    """정수 범위 검증"""
    try:
        int_val = int(value)
        if not (min_val <= int_val <= max_val):
            print(f"[Warning] {name}가 범위를 벗어남 ({min_val}-{max_val}), 기본값 사용: {default}")
            return default
        return int_val
    except (ValueError, TypeError):
        print(f"[Warning] {name}가 잘못된 정수값, 기본값 사용: {default}")
        return default


def validate_config() -> Dict[str, Any]:
    """
    모든 설정값을 검증하고 검증 결과를 반환

    Returns:
        설정값 통계 딕셔너리

    Raises:
        ConfigValidationError: 필수값이 누락된 경우
    """
    validation_errors = []

    # 필수값 검증
    try:
        _validate_required(NOTION_API_TOKEN, "NOTION_API_TOKEN")
    except ConfigValidationError as e:
        validation_errors.append(str(e))

    try:
        _validate_required(BOANISSUE_DATABASE_ID, "BOANISSUE_DATABASE_ID")
    except ConfigValidationError as e:
        validation_errors.append(str(e))

    # 선택적 URL 검증
    _validate_url(SLACK_WEBHOOK_URL, "SLACK_WEBHOOK_URL")

    # Database ID 형식 검증 (경고만)
    for db_id_key, db_id_value in [
        ("BOANISSUE_DATABASE_ID", BOANISSUE_DATABASE_ID),
        ("CVE_DATABASE_ID", CVE_DATABASE_ID),
        ("GUIDE_DATABASE_ID", GUIDE_DATABASE_ID),
        ("KEYWORD_STATS_DATABASE_ID", KEYWORD_STATS_DATABASE_ID),
    ]:
        if db_id_value:
            _validate_database_id(db_id_value, db_id_key)

    # 오류가 있으면 예외 발생
    if validation_errors:
        raise ConfigValidationError(
            f"\n환경 변수 설정 오류:\n" +
            "\n".join(f"  - {error}" for error in validation_errors) +
            "\n.env 파일을 확인해주세요."
        )

    # 검증 결과 통계 반환
    return {
        "total_checks": 15,
        "required_vars": 2,
        "optional_vars": 13,
        "validation_passed": True
    }


def get_config_summary() -> Dict[str, Any]:
    """
    설정값 요약 정보 반환 (민감 정보 제외)

    Returns:
        설정 요약 딕셔너리
    """
    return {
        "scheduler": {
            "enabled": RUN_SCHEDULER,
            "interval_hours": SCHEDULER_INTERVAL_HOURS,
            "keyword_interval_hours": KEYWORD_ANALYSIS_INTERVAL_HOURS
        },
        "publishing": {
            "notion_enabled": ENABLE_NOTION_PUBLISHING,
            "tistory_enabled": ENABLE_TISTORY_PUBLISHING,
            "weekly_notion": ENABLE_WEEKLY_NOTION,
            "weekly_tistory": ENABLE_WEEKLY_TISTORY
        },
        "performance": {
            "max_queue_size": MAX_QUEUE_SIZE,
            "max_workers": MAX_WORKERS,
            "max_consumers": MAX_CONSUMERS,
            "max_items_per_batch": MAX_ITEMS_PER_BATCH
        },
        "cache": {
            "llm_cache_max_size": LLM_CACHE_MAX_SIZE,
            "llm_cache_ttl_hours": LLM_CACHE_TTL_HOURS
        },
        "databases": {
            "boanissue": bool(BOANISSUE_DATABASE_ID),
            "cve": bool(CVE_DATABASE_ID),
            "guide": bool(GUIDE_DATABASE_ID),
            "keyword_stats": bool(KEYWORD_STATS_DATABASE_ID)
        }
    }


# 앱 시작 시 설정 검증 수행 (선택적 - 실제 사용 시 주석 해제)
if __name__ != "__main__":
    try:
        validate_config()
    except ConfigValidationError as e:
        print(f"[Config Error] {e}")
        # 개발 환경에서는 계속 실행, 프로덕션에서는 여기서 종료 가능