import os
import time
import shutil
import urllib.parse
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

from ..base_crawler import BaseCrawler
from ..utils import date_re, send_slack_message, clean_html_content
from ..notion_handler import Duplicate_check
from config import GUIDE_DATABASE_ID

class BohoCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.source_name = "보호나라 가이드라인"
        self.base_url = "https://www.boho.or.kr"
        self.target_url = f"{self.base_url}/kr/bbs/list.do?menuNo=205021&bbsId=B0000127&page=1"
        self.download_dir = os.path.join(os.getcwd(), "temp_downloads_boho")

    def run(self, publisher_service):
        seen_urls = set()
        scan_total = 0
        scan_success_count = 0
        scan_duplicate_count = 0
        scan_old_count = 0
        scan_error_count = 0

        # 임시 다운로드 디렉토리 설정 (절대 경로로 변환)
        self.download_dir = os.path.abspath(os.path.join(os.getcwd(), "temp_downloads_boho"))

        # 디렉토리 정리 및 생성
        if os.path.exists(self.download_dir):
            try:
                shutil.rmtree(self.download_dir)
            except:
                pass  # 이미 삭제 중이거나 권한 문제 무시
        os.makedirs(self.download_dir, exist_ok=True)

        print(f"[{self.source_name}] 다운로드 디렉토리: {self.download_dir}")

        driver = None

        try:
            # Chrome WebDriver 설정
            options = Options()
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-software-rasterizer')
            options.add_argument("--window-size=1920,1080")

            # 다운로드 설정
            prefs = {
                "download.default_directory": self.download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": False,  # Chrome의 다운로드 확인 비활성화
                "plugins.always_open_pdf_externally": True
            }
            options.add_experimental_option("prefs", prefs)

            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

            # 게시판 목록 페이지 로드
            print(f"[{self.source_name}] 게시판 목록 로드 중...")
            driver.get(self.target_url)

            wait = WebDriverWait(driver, 20)
            try:
                # 테이블 로드 대기 (여러 선택자 시도)
                table_selectors = [
                    "table.board-list tbody tr",
                    "table.tbl_board tbody tr",
                    "div.board-list table tbody tr",
                    "table tbody tr"
                ]
                rows = None
                for selector in table_selectors:
                    try:
                        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                        rows = soup.select(selector)
                        if rows and len(rows) > 0:
                            print(f"[{self.source_name}] 테이블 선택자 찾음: {selector}, 총 {len(rows)}개 행")
                            break
                    except:
                        continue

                if not rows or len(rows) == 0:
                    print(f"[{self.source_name}] 테이블 로드 실패 - 현재 HTML 구조 확인 필요")
                    # 디버깅: 현재 HTML 저장
                    with open('boho_debug.html', 'w', encoding='utf-8') as f:
                        f.write(driver.page_source)
                    print(f"[{self.source_name}] 디버깅을 위해 boho_debug.html에 HTML 저장")
                    return {
                         "source": self.source_name, "success": 0, "duplicate": 0, "old": 0, "error": 1, "total": 0
                    }

            except Exception as e:
                print(f"[{self.source_name}] 테이블 로드 타임아웃: {e}")
                return {
                     "source": self.source_name, "success": 0, "duplicate": 0, "old": 0, "error": 1, "total": 0
                }

            # 게시글 목록 파싱 (이미 위에서 로드됨)
            posts = []  # 게시글 리스트 초기화

            for i, row in enumerate(rows):
                try:
                    tds = row.select("td")
                    if len(tds) < 4:
                        print(f"  [DEBUG] td 개수 부족: {len(tds)}, 스킵")
                        continue

                    # 디버깅: 모든 td 내용 출력
                    if i == 0:
                        print(f"  [DEBUG] 첫 번째 행의 td들: {[td.get_text(strip=True)[:30] for td in tds]}")

                    # 제목과 링크 추출
                    title_elem = None
                    title = ""
                    href_attr = ""

                    # 공지 게시글: 첫 번째 td는 "공지", 두 번째 td가 제목
                    # 일반 게시글: 첫 번째 td는 번호, 두 번째 td가 제목
                    for idx, td in enumerate(tds):
                        a_elem = td.select_one("a")
                        if a_elem and a_elem.get_text(strip=True):
                            title_elem = a_elem
                            title = str(title_elem.get_text(strip=True))
                            href_attr = title_elem.get('href')
                            break

                    if not title_elem:
                        print(f"  [DEBUG] 제목 링크 없음, 스킵")
                        continue

                    href = str(href_attr) if href_attr else ""
                    if not href:
                        continue

                    # 상대 URL을 절대 URL로 변환
                    href_str = str(href) if href else ""
                    if not href_str.startswith('http'):
                        href_str = urllib.parse.urljoin(self.base_url, href_str)

                    # 날짜 추출 (마지막 td = 게시일)
                    date_text = ""
                    if tds:
                        last_td = tds[-1]  # 마지막 td
                        date_raw = last_td.get_text(strip=True) if hasattr(last_td, 'get_text') else ""
                        date_text = str(date_raw) if date_raw else ""

                        print(f"  [DEBUG] 마지막 td 내용: '{date_text}'")

                        # 날짜 형식 검증 (YYYY-MM-DD 형식인지 확인)
                        if not re.match(r'\d{4}-\d{2}-\d{2}', date_text):
                            print(f"  [DEBUG] 날짜 형식 불일치: '{date_text}'")
                            date_text = ""

                    posts.append({'title': title, 'url': href_str, 'date': date_text})

                except Exception as e:
                    scan_error_count += 1
                    continue

            scan_total = len(posts)
            print(f"[{self.source_name}] 총 {scan_total}개의 게시글 발견")

            # 각 게시글 처리
            for i, post in enumerate(posts, 1):
                try:
                    # 날짜 파싱
                    raw_date = post['date']
                    print(f"  [DEBUG] 원본 날짜: '{raw_date}'")
                    posting_date = date_re(raw_date)
                    if not posting_date:
                        posting_date = datetime.now()
                        print(f"  [DEBUG] 날짜 파싱 실패, 현재 시간 사용")

                    print(f"  [DEBUG] 파싱된 날짜: {posting_date}")

                    # 중복 체크
                    if Duplicate_check(post['url'], GUIDE_DATABASE_ID) == 1:
                        scan_duplicate_count += 1
                        print(f"[{self.source_name}] 중복 항목 스킵: {post['title'][:30]}...")
                        continue

                    # 상세 페이지 방문 및 파일 다운로드
                    driver.get(post['url'])
                    time.sleep(2)

                    detail_soup = BeautifulSoup(driver.page_source, 'html.parser')

                    files_to_upload = []

                    # 보호나라 사이트: 첨부 파일 섹션 찾기
                    # 여러 패턴 시도: dl/dt/dd 구조, 첨부파일 관련 클래스
                    attach_section = None

                    # 1. dl 태그 내의 첨부파일 섹션
                    dls = detail_soup.select('dl')
                    for dl in dls:
                        dt = dl.select_one('dt')
                        if dt and '첨부파일' in dt.get_text(strip=True):
                            attach_section = dl
                            print(f"  [DEBUG] 첨부파일 섹션 찾음 (dl 구조)")
                            break

                    # 2. content 내의 첨부파일
                    if not attach_section:
                        content_div = detail_soup.select_one('div.content')
                        if content_div:
                            attach_section = content_div
                            print(f"  [DEBUG] content div 사용")

                    if attach_section:
                        # 다운로드 링크 찾기
                        file_links = attach_section.select('a')
                        print(f"  [DEBUG] {len(file_links)}개의 링크 발견")

                        for idx, file_link in enumerate(file_links, 1):
                            # 타입 어서션 추가
                            file_text = file_link.get_text(strip=True) if hasattr(file_link, 'get_text') else str(file_link)
                            if not file_text or file_text in ['다음 글', '이전 글', '목록으로']:
                                continue

                            onclick_val = file_link.get('onclick', '') if hasattr(file_link, 'get') else ''
                            href_val = file_link.get('href', '') if hasattr(file_link, 'get') else ''

                            print(f"  [DEBUG] 파일 {idx}: {file_text}")
                            print(f"  [DEBUG]   onclick: {str(onclick_val)[:50] if onclick_val else 'N/A'}")
                            print(f"  [DEBUG]   href: {href_val}")

                            # JavaScript 다운로드 함수가 있는 경우
                            onclick_str = str(onclick_val) if onclick_val else ''
                            if onclick_str and any(x in onclick_str for x in ['fnFileDownload', 'fnAttachDownload', 'downloadFile', 'fileDown']):
                                # 파라미터 추출 (보호나라는 fileDown 함수 사용)
                                match = re.search(r"fileDown\(([^)]+)\)", onclick_str)
                                if not match:
                                    match = re.search(r"fn\w+Download\(([^)]+)\)", onclick_str)

                                if match:
                                    params_str = match.group(1)
                                    downloaded_file = self.download_file_boho(
                                        driver, params_str, self.download_dir, file_text
                                    )
                                    if downloaded_file:
                                        files_to_upload.append(downloaded_file)
                                        print(f"  [SUCCESS] 다운로드 완료: {file_text}")

                            # 직접 다운로드 링크가 있는 경우
                            href_str = str(href_val) if href_val else ''
                            if href_str and href_str.startswith('/'):
                                downloaded_file = self.download_file_direct(
                                    driver, self.base_url + href_str, self.download_dir, file_text
                                )
                                if downloaded_file:
                                    files_to_upload.append(downloaded_file)
                                    print(f"  [SUCCESS] 다운로드 완료: {file_text}")

                    # 내용 추출 (contents 또는 content 클래스)
                    content_elem = detail_soup.select_one('div.contents') or detail_soup.select_one('div.content')

                    if content_elem:
                        # HTML을 직접 가져와서 clean_html_content로 처리
                        raw_html = str(content_elem)
                        content = clean_html_content(raw_html)
                        print(f"  [DEBUG] clean_html_content 사용 - 내용 길이: {len(content)}자")
                    else:
                        content = ""
                        print(f"  [DEBUG] 본문 요소를 찾지 못함")

                    # Notion에 게시
                    date_str = posting_date.strftime('%Y-%m-%d')

                    if publisher_service:
                        publisher_service.publish_article(
                            title=post['title'],
                            content=content[:2000],
                            url=post['url'],
                            date=date_str,
                            category="보호나라 가이드라인",
                            details=content,
                            database_id=GUIDE_DATABASE_ID,
                            files=files_to_upload
                        )
                        print(f"[{self.source_name}] ✅ 게시 완료: {post['title'][:30]}...")
                        scan_success_count += 1

                except Exception as e:
                    print(f"[{self.source_name}-ERROR] 처리 중 오류 ({post['title']}): {e}")
                    scan_error_count += 1

        except Exception as e:
            error_msg = f"{self.source_name} 크롤링 중 오류: {e}"
            print(f"[CRITICAL] {error_msg}")
            send_slack_message(f"[CRITICAL ERROR] {error_msg}")
            scan_error_count += 1
        finally:
            if driver:
                driver.quit()

        # 임시 파일 정리
        if os.path.exists(self.download_dir):
            shutil.rmtree(self.download_dir)

        return {
            "source": self.source_name,
            "success": scan_success_count,
            "duplicate": scan_duplicate_count,
            "old": scan_old_count,
            "error": scan_error_count,
            "total": scan_total
        }

    def download_file_boho(self, driver, params_str, download_dir, file_name):
        """
        보호나라 JavaScript 다운로드 함수를 통해 파일 다운로드
        """
        try:
            before_time = time.time()

            # JavaScript 실행 (fileDown 함수 사용)
            js_cmd = f"fileDown({params_str});"
            print(f"  [DEBUG] JavaScript 실행: {js_cmd}")
            driver.execute_script(js_cmd)

            # 다운로드 완료 대기 (최대 60초)
            for _ in range(120):
                try:
                    current_files = os.listdir(download_dir)
                    for f in current_files:
                        if f.endswith(('.crdownload', '.tmp', '.part')) or f.startswith('.'):
                            continue

                        file_path = os.path.join(download_dir, f)
                        if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
                            continue

                        if os.path.getmtime(file_path) > before_time:
                            print(f"  [DEBUG] 다운로드된 파일: {f} ({os.path.getsize(file_path)} bytes)")
                            return {'path': file_path, 'name': f}

                    time.sleep(0.5)
                except:
                    time.sleep(0.5)

            print(f"  [DEBUG] 다운로드 타임아웃: {file_name}")
            return None
        except Exception as e:
            print(f"보호나라 파일 다운로드 오류: {e}")
            return None

    def download_file_direct(self, driver, href, download_dir, file_name=""):
        """
        직접 링크를 통해 파일 다운로드
        """
        try:
            before_time = time.time()

            # 링크 클릭
            driver.find_element(By.CSS_SELECTOR, f"a[href='{href}']").click()

            # 다운로드 완료 대기
            for _ in range(120):
                try:
                    current_files = os.listdir(download_dir)
                    for f in current_files:
                        if f.endswith(('.crdownload', '.tmp', '.part')) or f.startswith('.'):
                            continue

                        file_path = os.path.join(download_dir, f)
                        if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
                            continue

                        if os.path.getmtime(file_path) > before_time:
                            return {'path': file_path, 'name': f}

                    time.sleep(0.5)
                except:
                    time.sleep(0.5)

            return None
        except Exception as e:
            print(f"직접 다운로드 오류: {e}")
            return None
