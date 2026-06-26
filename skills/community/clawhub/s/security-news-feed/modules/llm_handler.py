# modules/llm_handler.py
"""
z.ai API를 사용하여 텍스트를 요약하고 상세 분석하는 모듈입니다.
모든 LLM 관련 기능을 제공합니다.
"""

import re
import time
import threading
import logging
from typing import Optional, Tuple
from functools import wraps

import requests

from config import ZAI_API_KEY

# 프롬프트 템플릿 임포트
from .prompts.translation import SYSTEM_PROMPT as TRANSLATION_SYSTEM, USER_PROMPT_TEMPLATE as TRANSLATION_USER
from .prompts.title_generation import SYSTEM_PROMPT as TITLE_SYSTEM, USER_PROMPT_TEMPLATE as TITLE_USER
from .prompts.details_analysis import SYSTEM_PROMPT as DETAILS_SYSTEM, USER_PROMPT_TEMPLATE as DETAILS_USER
from .prompts.cve_advisory import SYSTEM_PROMPT as CVE_SYSTEM, USER_PROMPT_TEMPLATE as CVE_USER
from .prompts.summary import SYSTEM_PROMPT as SUMMARY_SYSTEM, USER_PROMPT_TEMPLATE as SUMMARY_USER
from .prompts.keywords import SYSTEM_PROMPT as KEYWORDS_SYSTEM, USER_PROMPT_TEMPLATE as KEYWORDS_USER
from .prompts.blog_post import SYSTEM_PROMPT as BLOG_SYSTEM, USER_PROMPT_TEMPLATE as BLOG_USER


# ========================
# 설정 및 로깅 설정
# ========================

DEFAULT_MODEL = "glm-4.7-flash"
ZAI_API_URL = "https://api.z.ai/api/coding/paas/v4/chat/completions"
LLM_LOCK = threading.Lock()

# 캐싱 설정
import hashlib

class LLMMCache:
    """
    API 응답 캐싱 유틸리티
    동일한 요청에 대한 API 비용 절감

    개선사항:
    - 캐시 크기 제한 (기본 1000개)
    - TTL 기반 만료 (기본 24시간)
    - 스레드 안전한 접근
    """
    def __init__(self, max_size: int = 1000, ttl_hours: int = 24):
        self.cache = {}
        self.timestamps = {}  # 캐시 생성 시간 추적
        self.max_size = max_size
        self.ttl_seconds = ttl_hours * 3600
        self.lock = threading.Lock()

    def generate_key(self, text: str, model: str, operation: str = "") -> str:
        """캐시 키 생성 (텍스트 해시 기반으로 최적화)"""
        # 텍스트만 해싱하여 메모리 사용량 감소
        text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        # operation은 요약/상세분석 등 구분을 위해 추가
        key = f"{model}:{operation}:{text_hash}"
        return hashlib.md5(key.encode()).hexdigest()

    def get(self, prompt: str, model: str) -> Optional[str]:
        """캐시된 응답 조회 (호환성 유지)"""
        # 기존 코드와의 호환성을 위해 prompt의 일부를 추출
        # prompt 형식: "SYSTEM:...\nUSER: {text}\n"
        text_match = re.search(r'USER:\s*\{(.+?)\}', prompt, re.DOTALL)
        if text_match:
            text = text_match.group(1)
        else:
            text = prompt[:2000]  # fallback

        key = self.generate_key(text, model)
        return self._get_with_lock(key)

    def _get_with_lock(self, key: str) -> Optional[str]:
        """스레드 안전한 캐시 조회"""
        with self.lock:
            if key not in self.cache:
                return None

            # TTL 확인
            if self._is_expired(key):
                del self.cache[key]
                del self.timestamps[key]
                return None

            return self.cache.get(key)

    def _is_expired(self, key: str) -> bool:
        """캐시 만료 확인"""
        if key not in self.timestamps:
            return True
        age = time.time() - self.timestamps[key]
        return age > self.ttl_seconds

    def set(self, text: str, model: str, response: str, operation: str = ""):
        """응답 캐싱 (크기 제한 및 TTL 적용)"""
        key = self.get_key_for_operation(text, model, operation)
        self._set_with_lock(key, response)

    def _set_with_lock(self, key: str, response: str):
        """스레드 안전한 캐시 저장"""
        with self.lock:
            # 크기 제한: 가장 오래된 항목 제거
            if len(self.cache) >= self.max_size and key not in self.cache:
                self._evict_oldest()

            self.cache[key] = response
            self.timestamps[key] = time.time()

    def _evict_oldest(self):
        """가장 오래된 캐시 항목 제거"""
        if not self.timestamps:
            return
        oldest_key = min(self.timestamps, key=self.timestamps.get)
        del self.cache[oldest_key]
        del self.timestamps[oldest_key]

    def clear(self):
        """캐시 초기화"""
        with self.lock:
            self.cache.clear()
            self.timestamps.clear()

    def get_cache_info(self) -> dict:
        """캐시 통계 정보 반환"""
        with self.lock:
            return {
                "size": len(self.cache),
                "max_size": self.max_size,
                "ttl_hours": self.ttl_seconds // 3600
            }

    # [추가] 연산별 캐시 키 생성 메서드
    def get_key_for_operation(self, text: str, model: str, operation: str) -> str:
        """
        연산별 캐시 키 생성 (직접 사용 시)
        Args:
            text: 캐싱할 텍스트
            model: 모델명
            operation: 'summary', 'details', 'translate' 등
        """
        return self.generate_key(text, model, operation)

# 전역 캐시 인스턴스
llm_cache = LLMMCache()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


# ========================
# 데코레이터 및 유틸리티
# ========================

def retry_with_backoff(max_retries: int = 3, initial_delay: int = 1):
    """
    API 호출 재시도 데코레이터
    지수 백오프(exponential backoff)로 재시도합니다.

    Args:
        max_retries: 최대 재시도 횟수
        initial_delay: 초기 대기 시간 (초)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retry_delay = initial_delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, requests.RequestException) as e:
                    if attempt < max_retries - 1:
                        logger.debug(f"{func.__name__} 재시도 {attempt + 1}/{max_retries}: {e}")
                        time.sleep(retry_delay)
                        retry_delay *= 2
                    else:
                        logger.error(f"{func.__name__} 최대 재시도 횟수 초과: {e}")
                        raise e
                except Exception as e:
                    logger.error(f"{func.__name__} 예상치 못은 오류: {e}")
                    raise e
            return None
        return wrapper
    return decorator


def extract_content_from_response(response: dict) -> str:
    """
    API 응답에서 content 추출
    캐싱을 적용하여 중복 요청을 방지합니다.

    Args:
        response: z.ai API 응답 딕셔너리

    Returns:
        추출된 content 문자열

    Raises:
        ValueError: 응답 형식이 올바르지 않은 경우
    """
    try:
        return response['choices'][0]['message']['content'].strip()
    except (KeyError, IndexError, TypeError) as e:
        logger.error(f"API 응답 파싱 실패: {e}")
        raise ValueError("Invalid API response format") from e


def remove_think_tags(text: str) -> str:
    """
    <think> 태그와 그 안의 내용을 모두 삭제

    Args:
        text: 처리할 텍스트

    Returns:
        <think> 태그가 제거된 텍스트
    """
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)


def call_zai_api(messages: list, model: str = DEFAULT_MODEL, max_retries: int = 3) -> dict:
    """
    z.ai API를 호출하는 공통 함수 (재시도 로직 포함)

    Args:
        messages: 메시지 리스트 (OpenAI Chat Completion 형식)
        model: 사용할 모델명
        max_retries: 최대 재시도 횟수 (기본 3회)

    Returns:
        API 응답 딕셔너리

    Raises:
        requests.RequestException: API 호출 실패 (최대 재시도 후)
    """
    headers = {
        "Content-Type": "application/json",
        "Accept-Language": "en-US,en",
        "Authorization": f"Bearer {ZAI_API_KEY}"
    }
    data = {
        "model": model,
        "messages": messages
    }

    # 재시도 로직 (지수 백오프)
    last_exception = None
    initial_delay = 1.0
    backoff_base = 2.0

    for attempt in range(max_retries):
        try:
            # 첫 시도가 아닐 때만 재시도 로깅
            if attempt > 0:
                logger.info(f"[Retry] API 재시도 {attempt + 1}/{max_retries}...")

            logger.debug(f"API 요청 - Model: {model}, Messages: {len(messages)}개")

            response = requests.post(ZAI_API_URL, headers=headers, json=data, timeout=120)

            # 디버깅: 응답 상태 로깅
            logger.debug(f"API 응답 - Status: {response.status_code}")

            if response.status_code != 200:
                # 400 오류 상세 정보 로깅
                logger.error(f"API 오류 상세: {response.status_code}")
                logger.error(f"응답 내용: {response.text[:500]}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout as e:
            last_exception = e
            logger.warning(f"[Retry] API timeout: {e}")

        except requests.exceptions.ConnectionError as e:
            last_exception = e
            logger.warning(f"[Retry] Connection error: {e}")

        except requests.exceptions.HTTPError as e:
            last_exception = e
            # status_code 안전하게 추출 (response가 None일 경우 대응)
            status_code = None
            if hasattr(e, 'response') and e.response is not None:
                status_code = e.response.status_code

            if status_code == 429:
                # Rate Limit - 마지막 시도이면 즉시 실패, 아니면 대기 후 재시도
                if attempt == max_retries - 1:
                    logger.error(f"[Retry] Rate limit exceeded and max retries ({max_retries}) reached")
                    raise
                # 더 긴 대기 시간 적용
                retry_after = e.response.headers.get('Retry-After')
                if retry_after:
                    wait_time = int(retry_after)
                else:
                    wait_time = 60
                logger.warning(f"[Retry] Rate limit exceeded. Waiting {wait_time}s...")
                time.sleep(wait_time)
                continue

            elif 500 <= status_code < 600:
                # 서버 오류 - 재시도
                logger.warning(f"[Retry] Server error ({status_code})")

            elif 400 <= status_code < 500:
                # 클라이언트 오류 - 즉시 실패
                logger.error(f"[Error] Client error ({status_code}): {e}")
                raise

            # 기타 HTTP 에러
            logger.warning(f"[Retry] HTTP error: {e}")

        except Exception as e:
            last_exception = e
            logger.warning(f"[Retry] Unexpected error: {e}")

        # 마지막 시도이면 예외 발생
        if attempt == max_retries - 1:
            error_msg = f"[Retry] API 호출이 {max_retries}회 시도 후 실패했습니다."
            if last_exception:
                logger.error(f"{error_msg} Last error: {type(last_exception).__name__}")
                raise last_exception
            else:
                logger.error(error_msg)
                raise Exception(f"API 호출 실패: 알 수 없는 오류 (재시도 {max_retries}회 소진)")

        # 대기 시간 계산 (지수 백오프)
        wait_time = initial_delay * (backoff_base ** attempt)
        logger.info(f"[Retry] {wait_time:.1f}초 후 재시도...")
        time.sleep(wait_time)

    # 도달하면 안 되지만 형식상
    raise Exception("API 호출 실패")


# ========================
# 공개 함수 (Public Functions)
# ========================

@retry_with_backoff(max_retries=3, initial_delay=1)
def translate_text(
    text: str,
    title: Optional[str] = None,
    target_lang: str = 'ko',
    model: str = DEFAULT_MODEL,
    use_cache: bool = True
) -> str:
    """
    z.ai API를 사용해 텍스트를 번역합니다.

    Args:
        text: 번역할 원본 텍스트
        title: 텍스트 제목 (로그용)
        target_lang: 목표 언어 (기본값: 'ko')
        model: 사용할 모델명
        use_cache: 캐싱 사용 여부

    Returns:
        번역된 텍스트
    """
    # 캐싱 확인 (스레드 안전)
    if use_cache:
        cache_key = llm_cache.get_key_for_operation(text, model, 'translate')
        cached = llm_cache._get_with_lock(cache_key)
        if cached:
            logger.debug(f"[CACHE HIT] translate_text (길이: {len(text)}자)")
            return cached

    messages = [
        {"role": "system", "content": TRANSLATION_SYSTEM},
        {"role": "user", "content": TRANSLATION_USER.format(text=text, target_lang=target_lang)}
    ]

    with LLM_LOCK:
        log_title = f" (제목: {title})" if title else ""
        logger.info(f"[LLM] 번역 중...{log_title}")
        response = call_zai_api(messages, model)
        result = extract_content_from_response(response)
        result = result.strip('"').strip("'")
        logger.info(f"[LLM] 번역 완료{log_title}")

    # 캐싱 저장
    if use_cache:
        llm_cache.set(text, model, result, operation='translate')

    return result


@retry_with_backoff(max_retries=3, initial_delay=1)
def generate_title_from_body(
    body_text: str,
    model: str = DEFAULT_MODEL,
    max_length: int = 50,
    use_cache: bool = True
) -> str:
    """
    본문 내용을 바탕으로 적절한 제목을 생성합니다.

    Args:
        body_text: 본문 텍스트
        model: 사용할 모델명
        max_length: 제목 최대 길이
        use_cache: 캐싱 사용 여부

    Returns:
        생성된 제목
    """
    # 본문이 너무 길면 자르기
    preview_body = body_text[:1000]

    # 캐싱 키 생성
    prompt_key = f"{TITLE_SYSTEM}:{TITLE_USER.format(body_text=preview_body, max_length=max_length)}"

    # 캐시 확인 (스레드 안전)
    if use_cache:
        cache_key = llm_cache.get_key_for_operation(prompt_key, model, 'title')
        cached = llm_cache._get_with_lock(cache_key)
        if cached:
            logger.debug(f"[CACHE HIT] generate_title_from_body (길이: {len(body_text)}자)")
            return cached

    messages = [
        {"role": "system", "content": TITLE_SYSTEM},
        {"role": "user", "content": TITLE_USER.format(
            body_text=preview_body,
            max_length=max_length
        )}
    ]

    with LLM_LOCK:
        logger.info(f"[LLM] 제목 생성 중...")
        response = call_zai_api(messages, model)
        title = extract_content_from_response(response)
        logger.info(f"[LLM] 제목 생성 완료")

    # 제목 정리
    title = re.sub(r'^제목[:\s]*', '', title)
    title = re.sub(r'^["\']|["\']$', '', title)
    title = title.strip()

    if len(title) > max_length:
        title = title[:max_length-3] + "..."

    # 캐시 저장
    if use_cache:
        llm_cache.set(prompt_key, model, title)

    return title if title else "주간 보안 트렌드 분석"


@retry_with_backoff(max_retries=3, initial_delay=1)
def generate_cve_title_from_body(
    body_text: str,
    model: str = DEFAULT_MODEL,
    max_length: int = 60
) -> str:
    """
    CVE 본문 내용을 바탕으로 적절한 제목을 생성합니다.

    Args:
        body_text: CVE 본문 텍스트
        model: 사용할 모델명
        max_length: 제목 최대 길이

    Returns:
        생성된 제목
    """
    messages = [
        {"role": "system", "content": TITLE_SYSTEM},
        {"role": "user", "content": TITLE_USER.format(
            body_text=body_text[:1000],
            max_length=max_length,
            preview_hint="(본문 길이 제한으로 일부만 표시)" if len(body_text) > 1000 else ""
        )}
    ]

    with LLM_LOCK:
        logger.info(f"[LLM] CVE 제목 생성 중...")
        response = call_zai_api(messages, model)
        title = extract_content_from_response(response)
        logger.info(f"[LLM] CVE 제목 생성 완료")

    # 제목 정리
    title = re.sub(r'^제목[:\s]*', '', title)
    title = re.sub(r'^["\']|["\']$', '', title)
    title = title.strip()

    if len(title) > max_length:
        title = title[:max_length-3] + "..."

    return title if title else "CVE 보안 분석 보고서"


@retry_with_backoff(max_retries=3, initial_delay=1)
def details_text(
    text: str,
    title: Optional[str] = None,
    model: str = DEFAULT_MODEL,
    use_cache: bool = True
) -> str:
    """
    z.ai API를 사용해 정보 보안 기술에 대한 상세 설명을 생성합니다.

    Args:
        text: 분석할 원본 텍스트
        title: 텍스트 제목 (로그용)
        model: 사용할 모델명
        use_cache: 캐싱 사용 여부

    Returns:
        상세 분석 텍스트
    """
    # 캐싱 확인 (스레드 안전)
    if use_cache:
        cache_key = llm_cache.get_key_for_operation(text, model, 'details')
        cached = llm_cache._get_with_lock(cache_key)
        if cached:
            logger.debug(f"[CACHE HIT] details_text (길이: {len(text)}자)")
            return cached

    messages = [
        {"role": "system", "content": DETAILS_SYSTEM},
        {"role": "user", "content": DETAILS_USER.format(text=text)}
    ]

    with LLM_LOCK:
        log_title = f" (제목: {title})" if title else ""
        logger.info(f"[LLM] 상세 분석 중...{log_title}")
        response = call_zai_api(messages, model)
        result = extract_content_from_response(response)
        logger.info(f"[LLM] 상세 분석 완료{log_title}")

    # 캐싱 저장
    if use_cache:
        llm_cache.set(text, model, result, operation='details')

    return result


@retry_with_backoff(max_retries=3, initial_delay=1)
def summarize_text(
    text: str,
    title: Optional[str] = None,
    model: str = DEFAULT_MODEL,
    use_cache: bool = True
) -> str:
    """
    z.ai API를 사용해 300자 이내의 간결한 요약문을 생성합니다.

    Args:
        text: 요약할 원본 텍스트
        title: 텍스트 제목 (로그용)
        model: 사용할 모델명
        use_cache: 캐싱 사용 여부

    Returns:
        요약된 텍스트
    """
    # 캐싱 확인 (스레드 안산)
    if use_cache:
        cache_key = llm_cache.get_key_for_operation(text, model, 'summary')
        cached = llm_cache._get_with_lock(cache_key)
        if cached:
            logger.debug(f"[CACHE HIT] summarize_text (길이: {len(text)}자)")
            return cached

    messages = [
        {"role": "system", "content": SUMMARY_SYSTEM},
        {"role": "user", "content": SUMMARY_USER.format(text=text)}
    ]

    with LLM_LOCK:
        log_title = f" (제목: {title})" if title else ""
        logger.info(f"[LLM] 요약 중...{log_title}")
        response = call_zai_api(messages, model)
        result = extract_content_from_response(response)
        logger.info(f"[LLM] 요약 완료{log_title}")

    # 캐싱 저장
    if use_cache:
        llm_cache.set(text, model, result, operation='summary')

    return result


def CVE_details_text(
    text: str,
    title: Optional[str] = None,
    model: str = DEFAULT_MODEL
) -> Tuple[str, str]:
    """
    z.ai API를 사용해 CVE 관련 기술적인 보안 권고문을 생성합니다.
    제목과 본문을 모두 반환합니다.

    Args:
        text: CVE 원본 텍스트
        title: 텍스트 제목 (로그용)
        model: 사용할 모델명

    Returns:
        (제목, 본문) 튜플
    """
    messages = [
        {"role": "system", "content": CVE_SYSTEM},
        {"role": "user", "content": CVE_USER.format(cve_text=text)}
    ]

    try:
        with LLM_LOCK:
            log_title = f" (제목: {title})" if title else ""
            logger.info(f"[LLM] CVE 리포트 생성 중...{log_title}")
            response = call_zai_api(messages, model)
            full_response = extract_content_from_response(response)
            logger.info(f"[LLM] CVE 리포트 생성 완료{log_title}")

        # 응답 품질 검증
        if len(full_response.strip()) < 50:
            logger.warning(f"CVE 응답이 너무 짧습니다: {len(full_response)}자")

        # 정규식 패턴 매칭
        title_patterns = [
            r'--제목 start---\s*\n(.*?)\n---제목 end---',
            r'--제목 start---(.*?)---제목 end---',
            r'제목[:\s]*(.*?)(?:\n\n|\n---|\n##|\Z)',
            r'#\s*(.*?)(?:\n\n|\n---|\Z)',
            r'start---\s*(.*?)\s*---end',
            r'^(.+?)(?:\n\n|\n##|\Z)',
        ]

        body_patterns = [
            r'--본문 start---\s*\n(.*?)\n---본문 end---',
            r'--본문 start---(.*?)---본문 end---',
            r'본문[:\s]*(.*?)(?:\n\n|\n---|\Z)',
            r'##\s*(.*?)(?:\n\n|\n---|\Z)',
            r'start---\s*(.*?)(?:\n\n|\Z)',
            r'^.+?\n\n(.*)',
        ]

        generated_title = None
        generated_body = None

        # 제목 추출 시도
        for pattern in title_patterns:
            title_match = re.search(pattern, full_response, re.DOTALL)
            if title_match:
                generated_title = title_match.group(1).strip()
                break

        # 본문 추출 시도
        for pattern in body_patterns:
            body_match = re.search(pattern, full_response, re.DOTALL)
            if body_match:
                generated_body = body_match.group(1).strip()
                break

        # 본문 추출 fallback
        if not generated_body:
            lines = full_response.strip().split('\n')
            if len(lines) > 1:
                body_lines = lines[1:]
                generated_body = '\n'.join(body_lines).strip()
            else:
                generated_body = full_response.strip()

            # 본문이 너무 짧으면 재생성 (순환 의존성 해결)
            if not generated_body or len(generated_body) < 100:
                logger.debug("CVE 본문이 부족하여 details_text로 재생성")
                generated_body = details_text(text, title, model)

        # 제목 생성 fallback
        if not generated_title:
            if generated_body and len(generated_body) > 50:
                generated_title = generate_cve_title_from_body(generated_body, model)
            else:
                generated_title = "CVE 보안 분석 보고서"

        # 최종 검증
        if not generated_title or len(generated_title) < 5:
            generated_title = "CVE 보안 분석 보고서"

        if not generated_body or len(generated_body) < 100:
            logger.debug("CVE 최종 검증에서 본문이 부족하여 details_text로 재생성")
            generated_body = details_text(text, title, model)

        logger.info(f"CVE 생성된 제목: {generated_title[:50]}...")
        logger.info(f"CVE 생성된 본문 길이: {len(generated_body)}자")

        return generated_title, generated_body

    except Exception as e:
        logger.error(f"CVE 리포트 생성 오류: {e}")
        return "CVE 보안 분석 보고서", "CVE 보안 분석 보고서"


@retry_with_backoff(max_retries=3, initial_delay=1)
def extract_and_explain_keywords(text: str, model: str = DEFAULT_MODEL) -> str:
    """
    z.ai API를 사용해 주요 기술 키워드 10개와 각 설명을 생성합니다.

    Args:
        text: 분석할 원본 텍스트
        model: 사용할 모델명

    Returns:
        키워드 설명 텍스트
    """
    messages = [
        {"role": "system", "content": KEYWORDS_SYSTEM},
        {"role": "user", "content": KEYWORDS_USER.format(text=text)}
    ]

    with LLM_LOCK:
        logger.info(f"[LLM] 주간 키워드 추출 중... ({model})")
        response = call_zai_api(messages, model)
        result = extract_content_from_response(response)
        logger.info(f"[LLM] 주간 키워드 추출 완료")

    return result


@retry_with_backoff(max_retries=3, initial_delay=1)
def generate_weekly_tech_blog_post(
    topic_or_combined_text: str,
    model: str = DEFAULT_MODEL
) -> Tuple[str, str]:
    """
    주간 기술 블로그 포스트를 생성합니다.
    1. 먼저 본문을 생성
    2. 생성된 본문을 기반으로 제목을 추출

    Args:
        topic_or_combined_text: 입력 정보 (뉴스 목록 등)
        model: 사용할 모델명

    Returns:
        (제목, 본문) 튜플
    """
    # 1. 본문 생성
    messages_body = [
        {"role": "system", "content": BLOG_SYSTEM},
        {"role": "user", "content": BLOG_USER.format(topic_or_combined_text=topic_or_combined_text)}
    ]

    with LLM_LOCK:
        logger.info(f"[LLM] 블로그 포스트 본문 생성 중... ({model})")
        response = call_zai_api(messages_body, model)
        generated_body = extract_content_from_response(response)
        logger.info(f"[LLM] 블로그 포스트 본문 생성 완료 (길이: {len(generated_body)})")

        if len(generated_body) < 100:
            logger.warning(f"생성된 본문이 너무 짧습니다:\n{generated_body}")

    # 2. 제목 생성
    title_messages = [
        {"role": "system", "content": TITLE_SYSTEM},
        {"role": "user", "content": f"""
아래 블로그 본문을 읽고, 가장 적절한 제목을 생성해 주세요.
- 제목은 한 줄로, 30자 이내로 작성해 주세요
- **"[주간 보안 브리핑] 핵심 이슈 요약"** 같은 형식을 권장합니다.
- 독자의 클릭을 유도할 수 있는 매력적인 제목이어야 합니다.

[블로그 본문]
{generated_body}
        """}
    ]

    with LLM_LOCK:
        logger.info(f"[LLM] 블로그 포스트 제목 생성 중... ({model})")
        response = call_zai_api(title_messages, model)
        generated_title = extract_content_from_response(response)
        logger.info(f"[LLM] 블로그 포스트 제목 생성 완료")

    return generated_title, generated_body


@retry_with_backoff(max_retries=3, initial_delay=1)
def summarize_with_llm(text: str, model: str = DEFAULT_MODEL) -> str:
    """
    z.ai API를 사용해 뉴스 요약을 수행합니다.
    (이전 함수명: summarize_with_ollama - 역할 동일)

    Args:
        text: 요약할 원본 텍스트
        model: 사용할 모델명

    Returns:
        요약된 텍스트
    """
    messages = [
        {"role": "system", "content": SUMMARY_SYSTEM},
        {"role": "user", "content": f"다음 내용을 간결하게 요약해줘:\n{text}"}
    ]

    with LLM_LOCK:
        logger.info(f"[LLM] 뉴스 요약 중... ({model})")
        response = call_zai_api(messages, model)
        result = extract_content_from_response(response)
        logger.info(f"[LLM] 뉴스 요약 완료")

    return result

# ========================
# 품질 검증 및 모니터링 (Quality & Monitoring)
# ========================

def validate_summary_quality(summary: str, original_content: str = "") -> tuple[bool, dict]:
    """
    요약 품질 검증
    
    Args:
        summary: 검증할 요약 텍스트
        original_content: 원본 내용 (선택사항)
    
    Returns:
        (is_valid, checks): 검증 결과 및 상세 체크
    """
    checks = {
        'min_length': len(summary) >= 50,
        'max_length': len(summary) <= 1000,
        'has_korean': bool(re.search(r'[가-힣]', summary)),
        'no_empty': len(summary.strip()) > 0,
        'no_repetition': len(set(summary.split())) > len(summary.split()) * 0.6,
        'has_meaningful_content': any(word in summary.lower() for word in 
                                    ['취약점', '공격', '보안', '해킹', 'CVE', '위협', '악성', '바이러스', '피싱'])
    }
    
    is_valid = all(checks.values())
    
    if not is_valid:
        failed_checks = [k for k, v in checks.items() if not v]
        logger.warning(f"[Quality] Summary quality check failed: {failed_checks}")
    
    return is_valid, checks


def get_quality_score(checks: dict) -> float:
    """품질 점수 계산 (0.0 ~ 1.0)"""
    if not checks:
        return 0.0
    return sum(checks.values()) / len(checks)


class PipelineMetrics:
    """
    파이프라인 메트릭 수집 클래스
    
    수집하는 데이터:
    - articles_collected: 수집된 기사 수
    - articles_published: Notion에 게시된 기사 수
    - summaries_generated: 생성된 요약 수
    - errors: 발생한 에러 목록
    - processing_time: 처리 시간 목록
    """
    
    def __init__(self):
        self.stats = {
            'articles_collected': 0,
            'articles_published': 0,
            'summaries_generated': 0,
            'duplicate_skipped': 0,
            'quality_failed': 0,
            'errors': [],
            'processing_time': [],
            'retry_count': 0
        }
        self.lock = threading.Lock()
    
    def increment(self, key: str, value: int = 1):
        """카운터 증가"""
        with self.lock:
            if key in self.stats:
                self.stats[key] += value
    
    def add_error(self, error: str):
        """에러 추가"""
        with self.lock:
            self.stats['errors'].append({
                'error': error,
                'timestamp': datetime.datetime.now().isoformat()
            })
    
    def add_processing_time(self, duration: float):
        """처리 시간 기록"""
        with self.lock:
            self.stats['processing_time'].append(duration)
    
    def get_summary(self) -> dict:
        """통계 요약 반환"""
        with self.lock:
            times = self.stats['processing_time']
            avg_time = sum(times) / len(times) if times else 0
            
            return {
                'collected': self.stats['articles_collected'],
                'published': self.stats['articles_published'],
                'summaries': self.stats['summaries_generated'],
                'duplicates_skipped': self.stats['duplicate_skipped'],
                'quality_failed': self.stats['quality_failed'],
                'total_errors': len(self.stats['errors']),
                'avg_processing_time': avg_time,
                'retry_count': self.stats['retry_count']
            }
    
    def print_summary(self):
        """통계 요약 출력"""
        summary = self.get_summary()
        print(f"\n{'='*50}")
        print(f"📊 파이프라인 메트릭")
        print(f"{'='*50}")
        print(f"수집 기사: {summary['collected']}")
        print(f"게시 완료: {summary['published']}")
        print(f"요약 생성: {summary['summaries']}")
        print(f"중복 건너뜀: {summary['duplicates_skipped']}")
        print(f"품질 실패: {summary['quality_failed']}")
        print(f"에러 수: {summary['total_errors']}")
        print(f"재시도 수: {summary['retry_count']}")
        print(f"평균 처리 시간: {summary['avg_processing_time']:.1f}초")
        print(f"{'='*50}\n")


# 전역 메트릭 인스턴스
_global_metrics = PipelineMetrics()


def get_metrics() -> PipelineMetrics:
    """전역 메트릭 인스턴스 반환"""
    return _global_metrics


# ============================================================================
# 2단계 블로그 생성 (인텔리전스 에이전트 방식)
# ============================================================================

def validate_content_quality(content: str) -> tuple[bool, dict]:
    """
    본문 품질 검증 (인텔리전스 에이전트 기반)

    Returns:
        (is_valid, checks): 검증 결과 및 상세 체크
    """
    checks = {
        'min_length': len(content) >= 2000,           # 최소 2000자 (인텔리전스 에이전트 기준)
        'max_length': len(content) <= 20000,          # 최대 20000자
        'has_korean': bool(re.search(r'[가-힣]', content)),  # 한글 포함
        'no_empty': len(content.strip()) > 0,         # 비어있지 않음
        'has_heading': bool(re.search(r'^#+\s', content, re.MULTILINE)),  # 헤딩 포함
        'has_structure': bool(re.search(r'(##|###|\*\*|1\.|2\.)', content)),  # 구조 포함
    }

    is_valid = all(checks.values())

    if not is_valid:
        failed_checks = [k for k, v in checks.items() if not v]
        logger.warning(f"[Quality] Content quality check failed: {failed_checks}")

    return is_valid, checks


@retry_with_backoff(max_retries=3, initial_delay=1)
def generate_blog_article_2step(
    title: str,
    url: str,
    summary: str,
    source: str = "보안뉴스",
    model: str = DEFAULT_MODEL,
    use_cache: bool = False  # 캐싱 비활성화 (매번 새로운 생성)
) -> tuple[str, str]:
    """
    2단계 블로그 기사 본문 생성 (인텔리전스 에이전트 방식)

    **중요**: 원문 제목은 그대로 사용합니다. 본문만 생성합니다.

    1단계: 요약 및 카테고리 생성
    2단계: 본문 생성 (순수 Markdown, 최소 2000자)

    Args:
        title: 원본 기사 제목 (그대로 사용)
        url: 원본 기사 URL
        summary: 원본 기사 요약
        source: 출처
        model: 사용할 모델명
        use_cache: 캐싱 사용 여부

    Returns:
        (generated_summary, content) 튜플
        - generated_summary: 생성된 요약 (3-4문장)
        - content: 생성된 본문 (2000자 이상 마크다운)
    """
    # 프롬프트 임포트
    from .prompts.blog_generation import SUMMARY_SYSTEM, SUMMARY_USER
    from .prompts.blog_generation import CONTENT_SYSTEM, CONTENT_USER

    # ===== 1단계: 요약 및 카테고리 생성 =====
    logger.info(f"[Step 1/2] Generating summary for: {title[:40]}...")

    summary_messages = [
        {"role": "system", "content": SUMMARY_SYSTEM},
        {"role": "user", "content": SUMMARY_USER.format(
            source=source,
            title=title,
            url=url,
            summary=summary
        )}
    ]

    with LLM_LOCK:
        summary_response = call_zai_api(summary_messages, model)
        summary_json = extract_content_from_response(summary_response)

    # JSON 파싱
    import json
    try:
        # JSON 코드 블록 추출
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', summary_json, re.DOTALL)
        json_str = json_match.group(1) if json_match else summary_json

        # JSON 범위 추출
        if '{' in json_str:
            start = json_str.find('{')
            brace_count = 0
            end = start
            for i in range(start, len(json_str)):
                if json_str[i] == '{':
                    brace_count += 1
                elif json_str[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end = i + 1
                        break
            json_str = json_str[start:end]

        metadata = json.loads(json_str)
        generated_summary = metadata.get('summary', summary)
        category = metadata.get('category', '취약점/해킹')

        logger.info(f"[Step 1/2] Summary generated - Category: {category}")

    except Exception as e:
        logger.warning(f"[Step 1/2] Summary parsing failed: {e}, using fallback")
        generated_summary = summary
        category = "취약점/해킹"

    # ===== 2단계: 본문 생성 =====
    logger.info(f"[Step 2/2] Generating content (minimum 2000 chars)...")

    content_messages = [
        {"role": "system", "content": CONTENT_SYSTEM},
        {"role": "user", "content": CONTENT_USER.format(
            source=source,
            original_title=title,
            url=url,
            original_summary=summary,
            generated_summary=generated_summary,
            category=category
        )}
    ]

    with LLM_LOCK:
        content_response = call_zai_api(content_messages, model)
        content = extract_content_from_response(content_response)

    # 본문 품질 검증
    is_valid, checks = validate_content_quality(content)

    if not is_valid:
        logger.warning(f"[Step 2/2] Content quality check failed: {checks}")

        # 최소 길이 미달 시 재생성 (1회만)
        if not checks['min_length']:
            logger.warning(f"[Step 2/2] Content too short ({len(content)} chars), regenerating...")

            with LLM_LOCK:
                content_response = call_zai_api(content_messages, model)
                content = extract_content_from_response(content_response)

            # 재검증
            is_valid, checks = validate_content_quality(content)
            logger.info(f"[Step 2/2] Regenerated content - Length: {len(content)}, Valid: {is_valid}")

    logger.info(f"[Step 2/2] Content generation complete - Length: {len(content)} chars, Valid: {is_valid}")

    return generated_summary, content
