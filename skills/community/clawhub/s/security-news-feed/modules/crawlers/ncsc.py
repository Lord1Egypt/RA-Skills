import time
import urllib.parse
import os
import shutil
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

from ..base_crawler import BaseCrawler
from ..utils import date_re, send_slack_message, clean_html_content
from ..notion_handler import Duplicate_check
from config import BOANISSUE_DATABASE_ID

class NCSCCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.source_name = "NCSC"
        self.download_dir = os.path.join(os.getcwd(), "temp_downloads_ncsc")

    def run(self, publisher_service):
        processing_queue = [] # Not used in Stream mode but kept for compatibility logic
        seen_urls = set()
        scan_total = 0
        scan_success_count = 0
        scan_duplicate_count = 0
        scan_old_count = 0
        scan_error_count = 0
        process_success_count = 0
        process_error_count = 0
        
        # Cleanup start
        if os.path.exists(self.download_dir):
            shutil.rmtree(self.download_dir)
        os.makedirs(self.download_dir, exist_ok=True)
        
        driver = None
        try:
            # 1. Scanning Phase
            options = Options()
            options.add_argument('--headless=new')
            options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

            prefs = {
                "download.default_directory": self.download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            options.add_experimental_option("prefs", prefs)

            try:
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
            except Exception as e:
                send_slack_message(f"[ERROR] {self.source_name} - ChromeDriver 설정 오류: {e}")
                return {
                    "source": self.source_name, "success": 0, "duplicate": 0, "old": 0, "error": 1, "total": 0
                }

            target_url = "https://www.ncsc.go.kr:4018"
            driver.get(target_url)

            driver.execute_script("goSubMenuPage('020000','020200')")
            time.sleep(5)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            board_list_table = soup.find('table', class_='board_list')
            
            if not board_list_table:
                return {
                    "source": self.source_name, "success": 0, "duplicate": 0, "old": 0, "error": 1, "total": 0
                }

            tr_tags = board_list_table.find('tbody').find_all('tr')
            if not tr_tags:
                return {
                    "source": self.source_name, "success": 0, "duplicate": 0, "old": 0, "error": 0, "total": 0
                }

            scan_total = len(tr_tags)
            
            for tr_tag in tr_tags:
                try:
                    td_tags = tr_tag.find_all('td')
                    if len(td_tags) < 3: continue
                    
                    title_cell = td_tags[1]
                    a_tag = title_cell.find('a')

                    if a_tag and a_tag.has_attr('onclick'):
                        article_title = a_tag.text.strip()
                        onclick_script = a_tag['onclick']
                        
                        posting_date_str = td_tags[2].text.strip()
                        posting_date = date_re(posting_date_str)

                        if not posting_date:
                            scan_error_count += 1
                            continue

                        if not self.is_recent(posting_date):
                            scan_old_count += 1
                            continue

                        # 상세 페이지 이동
                        time.sleep(2)
                        driver.execute_script(onclick_script)
                        time.sleep(3)
                        article_url = driver.current_url
                        
                        duplicate_status = Duplicate_check(article_url, BOANISSUE_DATABASE_ID)
                        if duplicate_status == 0:
                            # 상세 내용 추출 (Clean HTML 사용)
                            content_html = ""
                            try:
                                content_elem = driver.find_element(By.CLASS_NAME, 'editor_view')
                                raw_html = content_elem.get_attribute('outerHTML')
                                content_html = clean_html_content(raw_html)
                            except:
                                content_html = f"제목: {article_title}\nURL: {article_url}\n\n상세 내용은 첨부파일을 참조하세요."

                            # 파일 다운로드 처리
                            files_to_upload = []
                            try:
                                file_links = driver.find_elements(By.CSS_SELECTOR, "div.board_view_file a[onclick*='fn_downFile']")
                                if file_links:
                                    # 다운로드 디렉토리 비우기 (혹시 이전 파일이 남아있을 경우)
                                    for f in os.listdir(self.download_dir):
                                        try:
                                            os.remove(os.path.join(self.download_dir, f))
                                        except: pass
                                    
                                    # [New] 본문 이미지 다운로드
                                    try:
                                        img_elems = driver.find_elements(By.CSS_SELECTOR, "div.editor_view img")
                                        for idx, img in enumerate(img_elems):
                                            src = img.get_attribute('src')
                                            if src and not src.startswith('data:'):
                                                try:
                                                    r = requests.get(src, verify=False, timeout=10)
                                                    if r.status_code == 200:
                                                        parsed = urllib.parse.urlparse(src)
                                                        fname = os.path.basename(parsed.path)
                                                        if not fname or len(fname) > 50: 
                                                            fname = f"ncsc_img_{int(time.time())}_{idx}.jpg"
                                                        
                                                        local_path = os.path.join(self.download_dir, fname)
                                                        with open(local_path, 'wb') as f:
                                                            f.write(r.content)
                                                        files_to_upload.append({'name': fname, 'path': local_path, 'type': 'image'})
                                                except Exception as e:
                                                    print(f"[{self.source_name}] 이미지 다운로드 실패: {e}")
                                    except Exception as e:
                                        print(f"[{self.source_name}] 이미지 처리 오류: {e}")

                                    for link in file_links:
                                        file_name = link.text.strip()
                                        link.click()
                                        time.sleep(3) # 다운로드 대기
                                        
                                        # 파일 확인
                                        downloaded_files = os.listdir(self.download_dir)
                                        if downloaded_files:
                                            # 가장 최근 파일 찾기
                                            latest_file = max([os.path.join(self.download_dir, f) for f in downloaded_files], key=os.path.getctime)
                                            # 이름 보존
                                            # NCSC 파일은 이름이 깨질 수 있으나, 일단 최신 파일 사용
                                            files_to_upload.append({'name': file_name, 'path': latest_file, 'type': 'file'})
                                            
                            except Exception as e:
                                print(f"[{self.source_name}-ERROR] 파일 다운로드 실패: {e}")

                            # ---------------------------------------------------------
                            # 큐에 적재 (Producer-Consumer)
                            # ---------------------------------------------------------
                            try:
                                if publisher_service:
                                    publisher_service.publish_article(
                                        title=article_title,
                                        content=content_html,
                                        url=article_url,
                                        date=posting_date.strftime('%Y-%m-%d'),
                                        category="NCSC",
                                        details=content_html,
                                        database_id=BOANISSUE_DATABASE_ID,
                                        files=files_to_upload
                                    )
                                scan_success_count += 1

                            except Exception as e:
                                print(f"[{self.source_name}-ERROR] 큐 등록 중 오류 ({article_title}): {e}")
                                scan_error_count += 1
                        elif duplicate_status == 1:
                            scan_duplicate_count += 1
                        
                        driver.back()
                        time.sleep(2)
                except Exception as e:
                    # print(f"[{self.source_name}-ERROR] 항목 처리 중 오류: {e}")
                    scan_error_count += 1

        except Exception as e:
            # print(f"[{self.source_name}-ERROR] 크롤링 중 오류: {e}")
            scan_error_count += 1
        finally:
            if driver:
                driver.quit()
        
        return {
            "source": self.source_name,
            "success": process_success_count,
            "duplicate": scan_duplicate_count,
            "old": scan_old_count,
            "error": scan_error_count + process_error_count,
            "total": scan_total
        }

    def _extract_content(self, soup, title):
         # Deprecated
         return ""
