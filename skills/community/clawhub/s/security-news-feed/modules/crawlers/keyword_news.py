import time
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import json
import re
from threading import Lock

# Selenium imports for Google News URL resolution
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

from ..base_crawler import BaseCrawler, KST
from ..notion_handler import Duplicate_check
from ..llm_handler import translate_text # Used in run
# from ..llm_handler import summarize_text, details_text # Moved to Processor
from ..utils import date_re
from ..notion_handler import url_cache
from config import BOANISSUE_DATABASE_ID

class KeywordNewsCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.source_name = "키워드 기반 뉴스"
        self.rss_urls = {
            # 일반 뉴스 (필터링 엄격)
            # '연합뉴스': 'https://www.yna.co.kr/rss/news.xml',
            # '동아일보': 'http://rss.donga.com/total.xml',
            # '한겨레': 'https://www.hani.co.kr/rss/',
            # '경향신문': 'https://www.khan.co.kr/rss/rssdata/total_news.xml',
            # 'SBS 뉴스': 'https://news.sbs.co.kr/news/newsflashRssFeed.do?plink=RSSREADER',
            # '전자신문': 'http://rss.etnews.co.kr/Section901.xml',
            # '국책브리핑': 'https://www.korea.kr/rss/policy.xml',
            
            # 보안 뉴스 (필터링 완화)
            'KRCERT 보안공지': 'https://knvd.krcert.or.kr/rss/security/notice',
            'KRCERT 보안정보': 'https://knvd.krcert.or.kr/rss/security/info',
            '보안뉴스': 'http://www.boannews.com/media/news_rss.xml',
            'ZDNet Korea': 'https://zdnet.co.kr/feed',
            'TheHackerNews': 'https://feeds.feedburner.com/TheHackersNews',
            'BleepingComputer': 'https://www.bleepingcomputer.com/feed/',
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.keywords = [
            # 1. 보안 정책 및 컴플라이언스
            '정보보호', '정보보안', '개인정보보안', '개인정보보호', '보안 정책', '보안 가이드',
            'ISMS', 'ISMS-P', 'ISO27001', 'GDPR', 'CSAP', '망분리', '클라우드 보안',
            '써티픽라이트', '공공기관', '개인정보3법', '마이데이터', 'CISO', 'CPO',

            # 2. 사고, 위협 및 공격 기법
            '해킹', '취약점', '랜섬웨어', '악성코드', '랜섬웨어', '크립토마이닝',
            '개인정보 유출', '데이터 유출', '침해사고', '정보보안 공격', '정보보안 취약점',
            '피싱', 'DDoS', 'APT', '지능형 지속위협', '랜섬피싱 공격', '피싱 메일',
            '공급망 공격', '공급망 보안', '크립토마이너', 'Zero-day', '백도어', 'WebShell',
            'SQL 인젝션', 'XSS', '디렉터리 트래버설', '브루트포스', '사회공학',
            'BEC', '비즈니스 이메일 송금기기', '딥페이크', '피싱', '스피어피싱 공용',

            # 3. 기술 및 솔루션
            '블록체인 보안', 'AI 보안', '클라우드 보안', 'IoT 보안', '메타버스 보안',
            'OT 보안', '패브릭 보안', '디지털서명', '다중서명', 'FIDO', '본인확인',
            'MFA', '이중인증', 'SOAR', 'SIEM', 'EDR', 'XDR', 'NDR', '보안 관제',
            '버그바운티', '모의해킹', '펜테스트', '위협 헌팅 및 펜테스트',

            # 4. 주요 위협 그룹 (북한 관련)
            '라자루스', 'Lazarus', '김수키', 'Kimsuky', '안다리엘', 'Andariel',
            '노스배후', '북한 해커',

            # 5. 기타 조치
            '보안 패치', '보안 업데이트', '긴급 보안 공지', '지원 종료', 'EOS',

            # 6. 영문 키워드
            'cybersecurity', 'infosec', 'information security',
            'data breach', 'hacked', 'vulnerability', 'ransomware', 'malware',
            'cyber attack', 'zero-day', 'supply chain attack', 'exploit',
            'phishing', 'social engineering', 'credential stuffing',
            'threat intelligence', 'incident response',
            'malware analysis', 'reverse engineering',
            'penetration testing', 'pentest',
            'ransomware gang', 'dark web',
            'exploit kit', 'cve',
            'identity theft', 'credential dumping',
            'cloud security', 'network security'
        ]

    def is_mostly_english(self, text, threshold=0.7):
        """
        뉴스 제목이 70% 이상 영문인지 확인합니다.
        """
        if not text:
            return False
        
        total_chars = len(text)
        english_chars = sum(1 for c in text if 'a' <= c.lower() <= 'z')
        
        ratio = english_chars / total_chars
        return ratio >= threshold

    def resolve_google_news_url_with_selenium(self, google_news_url):
        """
        Selenium을 사용하여 Google News URL을 실제 기사 URL로 변환합니다.
        JavaScript 리다이렉트도 처리할 수 있습니다.
        """
        if not SELENIUM_AVAILABLE:
            return google_news_url

        driver = None
        try:
            # Chrome 옵션 설정 (헤드리스 모드 + 메모리 최적화)
            chrome_options = Options()
            chrome_options.add_argument('--headless=new')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-images')
            chrome_options.add_argument('--disable-javascript')
            chrome_options.add_argument('--disable-software-rasterizer')
            chrome_options.add_argument('--disable-features=VizDisplayCompositor')
            chrome_options.add_argument('--disable-logging')
            chrome_options.add_argument('--log-level=3')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

            # WebDriver 초기화
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.set_page_load_timeout(30)  # 페이지 로드 타임아웃 설정

            # URL 로드
            driver.get(google_news_url)

            # JavaScript 리다이렉트 대기 (최대 10초)
            max_wait = 10
            start_time = time.time()

            while time.time() - start_time < max_wait:
                current_url = driver.current_url

                if 'google.com' not in current_url:
                    driver.quit()
                    return current_url

                time.sleep(0.5)

            # 실패 시 - 여전히 Google URL인 경우, 페이지 내의 링크 확인
            # 보통 해당 페이지는 리다이렉트가 아니라 "더 보기"를 클릭하면 링크를 보여주는 경우
            try:
                # 리다이렉트된 페이지에서 첫 번째 외부 링크 찾기
                links = driver.find_elements("tag name", "a")
                for link in links:
                    href = link.get_attribute('href')
                    if href and href.startswith('http') and 'google.com' not in href and 'gstatic.com' not in href:
                        # print(f"  [{self.source_name}-INFO] 리다이렉트 실패 후 페이지 내 링크 발견: {href}")
                        driver.quit()
                        return href
            except:
                pass

            # 실패 - 현재 URL 반환
            final_url = driver.current_url
            return final_url

        except Exception as e:
            # print(f"  [{self.source_name}-ERROR] Selenium URL 변환 실패: {e}")
            return google_news_url
        finally:
            # 드라이버 정리 (예외 발생 시에도 항상 실행)
            if driver:
                try:
                    driver.quit()
                except:
                    pass
    
    def resolve_google_news_url(self, google_news_url):
        """
        Google News URL을 실제 기사 URL로 변환합니다.
        Google News는 HTTP 리다이렉트 및 JavaScript 리다이렉트를 모두 사용할 수 있어,
        HTML 파싱을 통해 최종 URL을 추출합니다.
        """
        try:
            # 1단계: HTTP 리다이렉트 따라가기
            response = requests.get(google_news_url, headers=self.headers, timeout=10, allow_redirects=True)

            # Google News가 아닌 URL로 리다이렉트되었으므로 완료
            if 'news.google.com' not in response.url:
                return response.url

            # 2단계: 리다이렉트 체인 수동으로 따라가기 (이전 URL에서 에러 계속 리다이렉트)
            current_url = response.url
            for _ in range(3):  # 최대 3회 추가 리다이렉트 시도
                try:
                    resp = requests.get(current_url, headers=self.headers, timeout=5, allow_redirects=False)
                    if resp.status_code in [301, 302, 303, 307, 308] and 'Location' in resp.headers:
                        next_url = resp.headers['Location']
                        if 'google.com' not in next_url:
                            return next_url
                        current_url = next_url
                    else:
                        break
                except:
                    break

            # 3단계: HTML 파싱하여 JavaScript 리다이렉트 찾기
            soup = BeautifulSoup(response.text, 'html.parser')

            # 1. meta refresh 태그 확인
            meta_refresh = soup.find('meta', attrs={'http-equiv': re.compile('refresh', re.I)})
            if meta_refresh:
                content = meta_refresh.get('content', '')
                url_match = re.search(r'url=([^"\'>\s]+)', content, re.IGNORECASE)
                if url_match:
                    target_url = url_match.group(1)
                    if 'google.com' not in target_url:
                        return target_url

            # 2. script 태그에서 다양한 리다이렉트 패턴 찾기
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string:
                    script_text = script.string

                    # 패턴 1: window.location = "url"
                    location_match = re.search(r'window\.location\s*=\s*["\']([^"\']+)["\']', script_text)
                    if location_match:
                        target_url = location_match.group(1)
                        if 'google.com' not in target_url:
                            return target_url

                    # 패턴 2: window.location.replace("url")
                    replace_match = re.search(r'window\.location\.replace\s*\(\s*["\']([^"\']+)["\']\s*\)', script_text)
                    if replace_match:
                        target_url = replace_match.group(1)
                        if 'google.com' not in target_url:
                            return target_url

                    # 패턴 3: location.href = "url"
                    href_match = re.search(r'location\.href\s*=\s*["\']([^"\']+)["\']', script_text)
                    if href_match:
                        target_url = href_match.group(1)
                        if 'google.com' not in target_url:
                            return target_url

                    # 패턴 4: document.location = "url"
                    doc_location_match = re.search(r'document\.location\s*=\s*["\']([^"\']+)["\']', script_text)
                    if doc_location_match:
                        target_url = doc_location_match.group(1)
                        if 'google.com' not in target_url:
                            return target_url

                    # 패턴 5: 변수에 URL이 저장되어 나중에 사용되는 경우
                    # var url = "..."; window.location = url;
                    url_var_match = re.search(r'(?:var|let|const)\s+\w+\s*=\s*["\']([^"\']+)["\']', script_text)
                    if url_var_match:
                        target_url = url_var_match.group(1)
                        if target_url.startswith('http') and 'google.com' not in target_url:
                            return target_url

            # 4. Google이 아닌 URL로 이동하는 앵커 태그 찾기
            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href']
                if href.startswith('http') and 'google.com' not in href and 'gstatic.com' not in href:
                    return href

            # requests 기반 방법으로 최종 URL을 찾지 못한 경우
            # Selenium을 사용하여 JavaScript 리다이렉트 처리
            # print(f"  [{self.source_name}-INFO] requests 방법 실패, Selenium으로 재시도 중..")
            if SELENIUM_AVAILABLE:
                selenium_url = self.resolve_google_news_url_with_selenium(google_news_url)
                if 'google.com' not in selenium_url:
                    # print(f"  [{self.source_name}-SUCCESS] Selenium으로 URL 변환 성공")
                    return selenium_url
                else:
                    pass
                    # print(f"  [{self.source_name}-WARNING] Selenium으로도 URL 추출 실패")
            else:
                pass
                # print(f"  [{self.source_name}-WARNING] Selenium 미설치로 URL 추출 실패")

            return google_news_url

        except Exception as e:
            # print(f"  [{self.source_name}-ERROR] Google News URL 변환 실패: {e}")
            return google_news_url

    def fetch_chosun_content(self, url):
        """
        조선일보 페이지에서 JSON 데이터를 파싱하여 본문을 추출합니다.
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            # Fusion.globalContent={...}; 패턴 찾기
            pattern = r'Fusion\.globalContent\s*=\s*({.*?});'
            match = re.search(pattern, response.text, re.DOTALL)

            if match:
                data = json.loads(match.group(1))
                content_elements = data.get('content_elements', [])
                full_text = []
                for el in content_elements:
                    # type이 text인 요소만 추출
                    if el.get('type') == 'text':
                        full_text.append(el.get('content', ''))

                return '\n\n'.join(full_text)

        except Exception as e:
            print(f"[{self.source_name}-ERROR] 조선일보 본문 추출 실패: {e}")

        return None

    def batch_resolve_google_news_urls(self, google_news_urls, max_workers=2, timeout_per_url=10):
        """
        Google News URL들을 병렬로 변환합니다 (ThreadPoolExecutor 사용).

        Args:
            google_news_urls: 변환할 URL 리스트
            max_workers: 최대 워커 스레드 수 (기본 5개)
            timeout_per_url: 각 URL 변환 타임아웃 (초, 기본 10초)

        Returns:
            {original_url: resolved_url} 딕셔너리
        """
        if not google_news_urls:
            return {}

        result_map = {}

        def resolve_single_url(url_pair):
            """단일 URL 변환 함수 (타임아웃 포함)"""
            import concurrent.futures

            original_url, final_url = url_pair
            if 'news.google.com' not in final_url:
                return original_url, final_url

            try:
                # 타임아웃 내에서 URL 변환 시도
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(self.resolve_google_news_url, final_url)
                    resolved = future.result(timeout=timeout_per_url)  # 타임아웃 적용
                return original_url, resolved
            except concurrent.futures.TimeoutError:
                print(f"[{self.source_name}-WARN] URL 변환 타임아웃 ({timeout_per_url}초), 원본 URL 사용")
                return original_url, final_url
            except Exception as e:
                print(f"[{self.source_name}-WARN] URL 변환 실패: {str(e)[:50]}")
                return original_url, final_url

        print(f"[{self.source_name}] Google News URL 병렬 변환 시작 ({len(google_news_urls)}개, {max_workers}워커, 타임아웃 {timeout_per_url}초)...")

        # ThreadPoolExecutor로 병렬 처리
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(resolve_single_url, (url, url)): url
                for url in google_news_urls
            }

            completed = 0
            for future in as_completed(futures):
                try:
                    original_url, resolved_url = future.result(timeout=30)
                    result_map[original_url] = resolved_url
                    completed += 1

                    if completed % 5 == 0 or completed == len(google_news_urls):
                        print(f"[{self.source_name}] URL 변환 진행: {completed}/{len(google_news_urls)}")

                except Exception as e:
                    original_url = futures[future]
                    result_map[original_url] = original_url  # 실패 시 원본 URL 유지
                    print(f"[{self.source_name}-WARN] URL 처리 중 오류: {str(e)[:50]}")

        print(f"[{self.source_name}] URL 변환 완료: {len(result_map)}개")
        return result_map

    def run(self, publisher_service):
        start_time = time.time()

        # 1. Scanning Phase (데이터 수집)
        # ---------------------------------------------------------
        # print(f"[{self.source_name}] 스캔 시작 (Phase 1)...")

        all_entries = []
        for press, url in self.rss_urls.items():
            try:
                response = requests.get(url, headers=self.headers, timeout=30)
                if response.status_code != 200: continue

                feed = feedparser.parse(response.content)
                for entry in feed.entries:
                    entry['press'] = press
                    all_entries.append(entry)
            except Exception as e:
                print(f"[{self.source_name}-ERROR] '{press}' 피드 로드 실패: {e}")

        total_scan_items = len(all_entries)
        processing_queue = [] # LLM 처리를 위해 남겨둔 큐(Not used in Stream mode but kept for compatibility logic if needed, though effectively unused)
        seen_urls = set() # 이번 실행에서 처리한 URL 중복 방지

        # 집계 카운터
        scan_duplicate_count = 0
        scan_old_count = 0
        scan_unmatched_count = 0
        scan_error_count = 0
        scan_success_count = 0 # Initialized
        process_success_count = 0
        process_error_count = 0

        # [NEW] 1.5단계: 키워드 필터링 및 Google News URL 추출 (병렬 처리 전)
        google_news_entries = []
        filtered_entries = []

        # 일반 뉴스 사이트 (엄격한 필터링 필요)
        general_news_sites = ['연합뉴스', '동아일보', '한겨레', '경향신문', 'SBS 뉴스', '전자신문', '국책브리핑']

        # 보안 뉴스 사이트 (필터링 완화 - 모든 기사 통과)
        security_news_sites = ['KRCERT 보안공지', 'KRCERT 보안정보', '보안뉴스', 'ZDNet Korea', 'TheHackerNews', 'BleepingComputer']

        for entry in all_entries:
            title = entry.get('title', '제목 없음')
            link_url = entry.link
            press = entry.get('press', '')

            # A. 키워드 매칭
            title_lower = title.lower()

            # 일반 뉴스 사이트: 엄격한 필터링 (명확한 보안 키워드만)
            if press in general_news_sites:
                # 제외할 키워드 (보안과 관련 없는 "보안"이 포함된 단어)
                excluded_patterns = [
                    '국가 보안', '동물 보안', '식량 보안', '에너지 보안', '시설 보안',
                    '경비 보안', '물리 보안', '치안 보안', '공원 보안', '환경 보안',
                    '보건 복지', '보건', '보안관', '보안 등급', '1급 보안', '2급 보안',
                    '보안 입증', '보안 인증', '신용 보안', '안전 보안'
                ]

                # 제외 패턴이 있는지 먼저 체크
                if any(pattern in title for pattern in excluded_patterns):
                    scan_unmatched_count += 1
                    continue

                # 주요 보안 키워드만 매칭 (너무 일반적인 키워드 제외)
                strict_keywords = [
                    '정보보호', '정보보안', '개인정보보안', '개인정보보호', '개인정보 유출', '데이터 유출',
                    '해킹', '취약점', '랜섬웨어', '악성코드', '크립토마이닝',
                    '피싱', '스피어피싱', '보이스피싱', 'DDoS', 'APT', '지능형 지속위협',
                    'Zero-day', '백도어', 'WebShell', 'SQL 인젝션', 'XSS', '브루트포스',
                    'BEC', '비즈니스 이메일', '딥페이크',
                    '라자루스', '레이저우스', '김수키', '안다리엘', '노스배후', '북한 해커',
                    '보안 패치', '긴급 보안 공지', 'CVE-', '지원 종료', 'EOS',
                    'cybersecurity', 'infosec', 'information security', 'data breach',
                    'hacked', 'vulnerability', 'ransomware', 'malware', 'zero-day',
                    'phishing', 'supply chain attack', 'exploit', 'social engineering'
                ]

                # 보안 관련 키워드가 없는 경우 제외
                if not any(keyword.lower() in title_lower for keyword in strict_keywords):
                    scan_unmatched_count += 1
                    continue

                # "보안" 단어가 단독으로 사용된 경우 추가 체크
                if '보안' in title and not any(
                    keyword in title for keyword in [
                        '정보보안', '정보보호', '개인정보보안', '개인정보보호', '보안정책', '보안가이드',
                        '보안 공지', '보안 패치', '보안 업데이트', '보안 취약점', '보안 공격',
                        '보안 침해', '보안 사고', '사이버보안', '클라우드 보안', '네트워크 보안',
                        'iot 보안', 'ot 보안', '시스템 보안', '소프트웨어 보안', '앱 보안',
                        '모바일 보안', '금융 보안', '전자금융보안', '보안관제', '보안 솔루션',
                        '보안 프로그램', '보안 소프트웨어', '보안 시스템', '보안 업체',
                        '보안 기술', '보안 서비스', '보안 플랫폼', '보안 인프라'
                    ]
                ):
                    # "보안"만 단독으로 있는 경우 (예: "보안 체계", "보안 관" 등) 제외
                    scan_unmatched_count += 1
                    continue

            # 보안 뉴스 사이트: 기존 필터링 유지
            elif press in security_news_sites:
                if not any(keyword.lower() in title_lower for keyword in self.keywords):
                    scan_unmatched_count += 1
                    continue

            # Google News: 기존 필터링 유지
            else:
                if not any(keyword.lower() in title_lower for keyword in self.keywords):
                    scan_unmatched_count += 1
                    continue

            # B. Google News URL 분리
            if 'news.google.com' in link_url:
                google_news_entries.append(entry)
            else:
                filtered_entries.append(entry)

        print(f"[{self.source_name}] 필터링 완료: 키워드 일치 {len(google_news_entries) + len(filtered_entries)}개 (Google News: {len(google_news_entries)})")

        # [NEW] 1.6단계: Google News URL 병렬 변환
        google_news_url_map = {}
        if google_news_entries:
            google_news_urls = [entry.link for entry in google_news_entries]
            google_news_url_map = self.batch_resolve_google_news_urls(google_news_urls, max_workers=5)

        # 병렬 변환된 URL로 업데이트
        for entry in google_news_entries:
            original_url = entry.link
            if original_url in google_news_url_map:
                resolved_url = google_news_url_map[original_url]
                # 변환된 URL이 다른 경우에만 업데이트
                if resolved_url != original_url:
                    entry.link = resolved_url

        # 필터링된 항목들을 처리 목록에 추가
        filtered_entries.extend(google_news_entries)

        # [NEW] 2. 처리 단계 (필터링된 항목들만 처리)
        for i, entry in enumerate(filtered_entries):
            # 50개마다 스캔 진행 상황 출력
            if (i + 1) % 50 == 0:
                print(f"[{self.source_name}] 처리 진행 중.. {i + 1}/{len(filtered_entries)}")

            title = entry.get('title', '제목 없음')
            link_url = entry.link

            try:
                # B. 날짜 파싱 및 체크
                posting_date_str = entry.get('published', '')
                posting_date = None  # 초기화

                # 날짜 파싱 시도
                if posting_date_str:
                    posting_date = date_re(posting_date_str)

                if not posting_date:
                    # 파싱 실패 시 현재 시간 사용
                    posting_date = datetime.now(KST)
                    # print(f"[{self.source_name}] 기사 날짜 파싱 실패, 현재 시간 사용: {title} (Date: '{posting_date_str}')")

                # [임시 비활성화] 최신 기사 필터링
                # if not self.is_recent(posting_date, days=7):
                #     scan_old_count += 1
                #     continue

                # C. URL 변환(Google News)
                # Google News URL 변환 스킵 (속도 문제)
                # if 'news.google.com' in link_url:
                #     link_url = self.resolve_google_news_url(link_url)

                # [New] 이번 실행 내 중복 체크
                if link_url in seen_urls:
                    scan_duplicate_count += 1
                    continue
                
                seen_urls.add(link_url)

                # D. 로컬 캐시 기반 중복 체크 (빠른 체크, Notion API 호출 없음)
                normalized_url = url_cache.normalize_url(link_url)
                if url_cache.exists(normalized_url):
                    scan_duplicate_count += 1
                    continue
                
                # Google News URL이 변환되지 않은 경우 스킵 (중복 체크 신뢰성 문제)
                if 'news.google.com' in link_url:
                    scan_unmatched_count += 1
                    continue
                
                #     fetched_content = self.fetch_chosun_content(link_url)
                #     content = fetched_content if fetched_content else BeautifulSoup(entry.summary, 'html.parser').get_text('\n', strip=True)
                # else:
                #     content = BeautifulSoup(entry.summary, 'html.parser').get_text('\n', strip=True)
                content = BeautifulSoup(entry.summary, 'html.parser').get_text('\n', strip=True)

                if not content or len(content.strip()) < 50:
                    #print(f"[{self.source_name}] 본문 내용 부족(<50자): {title[:30]}...")
                    scan_error_count += 1
                    continue

                # ---------------------------------------------------------
                # 큐에 등록 (Producer-Consumer)
                # ---------------------------------------------------------
                try:
                    # print(f"[{self.source_name}] 유효한 기사 발견! 큐에 등록: {title[:30]}...")

                    # A. 영문 제목 번역 제거 (Producer 단계에서 번역하면 너무 느림, Consumer에서 처리)
                    # 번역은 Consumer의 2단계 본문 생성 과정에서 처리됨

                    # B. 카테고리 지정
                    category = entry.press
                    if getattr(entry, 'source', None) and hasattr(entry.source, 'title'):
                        category = entry.source.title

                    # KISA 보안공지 -> KRCERT/krcert_cve 카테고리 변환
                    if category == 'KISA 보안공지':
                        # CVE 기사인지 확인
                        if title.startswith("CVE-"):
                            category = "krcert_cve"
                        else:
                            category = "KRCERT"

                    if publisher_service:
                        publisher_service.publish_article(
                            title=title,
                            content=content, # Raw Content
                            url=link_url,
                            date=posting_date.strftime('%Y-%m-%d'),
                            category=category,
                            details=content, # Raw Content
                            database_id=BOANISSUE_DATABASE_ID
                        )
                        scan_success_count += 1  # [FIX] 큐에 등록 성공 시에만 증가
                    else:
                        # publisher_service가 None인 경우 (QueueCollector 사용 안 함)
                        print(f"[{self.source_name}-ERROR] publisher_service가 None이어서 큐에 등록 불가: {title[:30]}...")
                        scan_error_count += 1
                    
                except Exception as e:
                    print(f"[{self.source_name}-ERROR] 기사 등록 중 오류 ({title}): {e}")
                    scan_error_count += 1

            except Exception as e:
                print(f"[{self.source_name}-ERROR] 스캔 중 처리 오류 ({title}): {e}")
                scan_error_count += 1
                
        return {
            "source": self.source_name,
            "success": scan_success_count, # Use scan_success_count as success metric
            "duplicate": scan_duplicate_count,
            "old": scan_old_count,
            "error": scan_error_count + process_error_count,
            "unmatched": scan_unmatched_count,
            "total": total_scan_items
        }

