# modules/utils.py

import requests
import datetime
import re
import time
import threading
from enum import Enum
from config import SLACK_WEBHOOK_URL
from datetime import datetime, timezone


# ========================
# Circuit Breaker Pattern
# ========================

class CircuitState(Enum):
    """회로 차단기 상태"""
    CLOSED = "closed"      # 정상 작동
    OPEN = "open"          # 차단됨 (요청 거부)
    HALF_OPEN = "half_open"  # 부분 열림 (복구 시도 중)


class CircuitBreaker:
    """
    회로 차단기 패턴 구현
    외부 API 호출 실패 시 연쇄적 장애 방지

    Usage:
        breaker = CircuitBreaker("NotionAPI", failure_threshold=5, timeout=60)

        @breaker
        def call_notion_api():
            # API 호출
            ...

        또는:
        if breaker.call():
            result = api_function()
    """
    def __init__(self, name: str, failure_threshold: int = 5, timeout: int = 60):
        self.name = name
        self.failure_threshold = failure_threshold
        self.timeout = timeout  # 회로 차단 후 재시도 대기 시간 (초)
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.lock = threading.Lock()

    def _is_timeout_expired(self) -> bool:
        """타임아웃이 만료되었는지 확인"""
        if self.last_failure_time is None:
            return True
        return (time.time() - self.last_failure_time) >= self.timeout

    def _record_failure(self):
        """실패 기록 및 상태 전환"""
        with self.lock:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
                print(f"[CircuitBreaker] {self.name}: 회로 차단됨 (실패 {self.failure_count}회)")

    def _record_success(self):
        """성공 기록 및 상태 복구"""
        with self.lock:
            self.failure_count = 0
            self.last_failure_time = None
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
                print(f"[CircuitBreaker] {self.name}: 회로 복구됨")

    def __call__(self, func):
        """데코레이터로 사용"""
        def wrapper(*args, **kwargs):
            return self.call(func, *args, **kwargs)
        return wrapper

    def call(self, func=None, *args, **kwargs):
        """
        함수 실행을 위한 래퍼
        회로가 열려있으면 None 반환 및 예외 발생 방지
        """
        with self.lock:
            if self.state == CircuitState.OPEN:
                if self._is_timeout_expired():
                    self.state = CircuitState.HALF_OPEN
                    print(f"[CircuitBreaker] {self.name}: 복구 시도 (HALF_OPEN)")
                else:
                    raise CircuitBreakerOpenError(
                        f"CircuitBreaker '{self.name}' is OPEN. "
                        f"Rejecting request. Fails: {self.failure_count}"
                    )

        try:
            if func is None and args and callable(args[0]):
                # 데코레이터로 호출된 경우: func은 첫 번째 인자
                actual_func = args[0]
                actual_args = args[1:]
                result = actual_func(*actual_args, **kwargs)
            else:
                # 직접 호출된 경우
                if func is None:
                    raise ValueError("func must be provided")
                result = func(*args, **kwargs)

            self._record_success()
            return result

        except Exception as e:
            self._record_failure()
            raise e


class CircuitBreakerOpenError(Exception):
    """회로 차단기가 열려있을 때 발생하는 예외"""
    pass


# 전역 회로 차단기 인스턴스 (선택적 사용)
notion_api_breaker = CircuitBreaker("NotionAPI", failure_threshold=5, timeout=60)
llm_api_breaker = CircuitBreaker("LLMAPI", failure_threshold=3, timeout=30)

def filter_bmp_characters(s):
    """
    주어진 문자열에서 BMP(Basic Multilingual Plane) 외부의 문자를 제거합니다.
    """
    if not isinstance(s, str):
        return s  # 문자열이 아니면 그대로 반환
    return "".join(c for c in s if ord(c) <= 0xFFFF)

def calc_str_width(s):
    """
    한글 등 동아시아 문자를 2칸, 그 외는 1칸으로 계산하여 문자열의 표시 너비를 반환합니다.
    """
    import unicodedata
    width = 0
    for c in s:
        if unicodedata.east_asian_width(c) in ['W', 'F']:
            width += 2
        else:
            width += 1
    return width

def pad_str(s, width, align='left', fillchar=' '):
    """
    calc_str_width를 고려하여 문자열을 패딩합니다.
    """
    current_width = calc_str_width(s)
    padding_len = max(0, width - current_width)
    
    if align == 'left':
        return s + (fillchar * padding_len)
    elif align == 'right':
        return (fillchar * padding_len) + s
    elif align == 'center':
        left_pad = padding_len // 2
        right_pad = padding_len - left_pad
        return (fillchar * left_pad) + s + (fillchar * right_pad)
    else:
        return s

def send_slack_message(message):
    """
    주어진 메시지를 Slack으로 전송합니다.
    """
    payload = {"text": message}
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=10)
        response.raise_for_status()  # HTTP 오류 발생 시 예외를 발생시킴
        # print("슬랙 메시지 전송 성공!")
    except requests.exceptions.RequestException as e:
        print(f"슬랙 메시지 전송 실패: {e}")


def date_re(date_str):
    """
    다양한 날짜 포맷을 받아 타임존을 고려한 datetime 객체로 변환합니다.
    변환 실패 시 None을 반환합니다.
    """
    if not isinstance(date_str, str) or not date_str.strip():
        return None
    date_str = date_str.strip()

    try:
        # 이 포맷은 한글 '월'과 공백을 포함하므로, strptime으로 직접 파싱
        return datetime.strptime(date_str, "%m월 %d, %Y")
    except ValueError:
        pass
    
    # 2. 'YYYY년 MM월 DD일' 형식 처리
    if '년' in date_str and '월' in date_str and '일' in date_str:
        try:
            date_digits = re.sub(r'[^0-9]', '', date_str)
            return datetime.strptime(date_digits, "%Y%m%d")
        except ValueError:
            pass

    # 1. NVD CVE의 'Z' 포맷 (UTC) 처리
    if date_str.endswith('Z'):
        try:
            dt_naive = datetime.strptime(date_str.removesuffix('Z'), "%Y-%m-%dT%H:%M:%S.%f")
            return dt_naive.replace(tzinfo=timezone.utc)
        except ValueError:
            try:
                dt_naive = datetime.strptime(date_str.removesuffix('Z'), "%Y-%m-%dT%H:%M:%S")
                return dt_naive.replace(tzinfo=timezone.utc)
            except ValueError:
                pass

    # 2. KRCERT의 'GMT' 포맷 (UTC) 처리
    elif date_str.endswith('GMT'):
        try:
            dt_naive = datetime.strptime(date_str.removesuffix(' GMT'), "%a, %d %b %Y %H:%M:%S")
            return dt_naive.replace(tzinfo=timezone.utc)
        except ValueError:
            pass

    # 3. 그 외 다른 표준 포맷들 처리
    for fmt in (
        "%a, %d %b %Y %H:%M:%S %z",  # RSS 표준 포맷 (e.g., +0900)
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%Y.%m.%d %H:%M:%S",
        "%Y.%m.%d %H:%M",
        "%Y.%m.%d",
        "%a, %d %b %Y %H:%M:%S", # No offset
    ):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    print(f"[DEBUG] date_re: 지원하지 않는 날짜 포맷입니다 - '{date_str}'")
    return None

def clean_html_content(raw_html):
    """
    HTML 콘텐츠를 정리하여 깨끗한 텍스트로 반환합니다.
    - 블록 태그(p, div, br, li, tr 등)는 줄바꿈으로 변환
    - 인라인 태그(span, b, strong 등)는 내용 유지 및 줄바꿈 없음
    - 테이블(tr, td) 구조를 Markdown 표로 변환
    - 과도한 공백 및 줄바꿈 제거
    """
    if not raw_html:
        return ""

    from bs4 import BeautifulSoup, NavigableString
    soup = BeautifulSoup(raw_html, 'html.parser')

    # 1. <br> 태그 처리 (줄바꿈)
    for br in soup.find_all('br'):
        br.replace_with("__BR__")

    # 2. 테이블 태그 처리 (Markdown 스타일로 변환)
    for table in soup.find_all('table'):
        rows = table.find_all('tr')
        if not rows:
            continue
            
        md_table_lines = []
        has_header = False
        
        # Determine column count from the first row
        cols_count = 0
        
        for i, tr in enumerate(rows):
            cells = tr.find_all(['th', 'td'])
            if not cells: 
                continue
                
            row_text = []
            is_header_row = False
            for cell in cells:
                cell_text = cell.get_text(strip=True)
                row_text.append(cell_text)
                if cell.name == 'th':
                    is_header_row = True
            
            # Markdown Row: | Cell | Cell |
            md_line = "| " + " | ".join(row_text) + " |"
            md_table_lines.append(md_line)
            
            if i == 0:
                cols_count = len(row_text)
                if is_header_row:
                    has_header = True
            
            # If explicit header row, add separator line immediately after
            if i == 0 and has_header:
                 sep_line = "| " + " | ".join(["---"] * cols_count) + " |"
                 md_table_lines.append(sep_line)
        
        # If no explicit header tag but valid table, maybe add a dummy separator if desired?
        # For now, strict markdown requires header. If missing, First row becomes header visually.
        if i == 0 and not has_header and cols_count > 0:
             # Force first row as header if no th found, to maintain table structure in some viewers
             sep_line = "| " + " | ".join(["---"] * cols_count) + " |"
             md_table_lines.append(sep_line)

        # Replace table content with Markdown string + markers
        # 테이블 앞뒤로 블록 구분자 추가
        table_str = "\n" + "\n".join(md_table_lines) + "\n"
        table.replace_with(NavigableString(f"__BLOCK__{table_str}__BLOCK__"))

    # 3. 블록 태그 처리 (문단 구분)
    # table은 이미 처리했으므로 제외
    block_tags = ['p', 'div', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'article', 'section']
    for tag in soup.find_all(block_tags):
        tag.append(NavigableString("__BLOCK__"))

    # 4. 텍스트 추출 (구분자=" " 사용)
    text = soup.get_text(separator=" ", strip=True)

    # 5. 마커를 실제 줄바꿈으로 변환
    # __BLOCK__ -> \n\n (Notion에서 별도 블록으로 분리됨)
    # __BR__ -> \n (Notion 블록 내 줄바꿈)
    text = text.replace("__BLOCK__", "\n\n")
    text = text.replace("__BR__", "\n")

    # 6. 공백 정리
    # 마커 주변 등에 생긴 과도한 공백 정리
    text = re.sub(r' +', ' ', text) # 연속된 공백 -> 공백 1개
    text = re.sub(r' \n', '\n', text) # 줄바꿈 앞 공백 제거
    text = re.sub(r'\n ', '\n', text) # 줄바꿈 뒤 공백 제거
    
    # 7. 연속된 줄바꿈을 최대 3개(빈 줄 2개)로 제한
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    
    return text.strip()
