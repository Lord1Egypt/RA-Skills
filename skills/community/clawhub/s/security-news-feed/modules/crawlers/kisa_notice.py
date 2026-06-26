import time
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import urllib.parse
import requests
import shutil

from ..base_crawler import BaseCrawler
from ..utils import date_re, send_slack_message, clean_html_content
from ..notion_handler import Duplicate_check
from config import BOANISSUE_DATABASE_ID

class KISANoticeCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.source_name = "보호나라"
        self.base_url = "https://www.boho.or.kr"
        self.list_url = "https://www.boho.or.kr/kr/bbs/list.do?menuNo=205020&bbsId=B0000133"
        self.download_dir = os.path.join(os.getcwd(), "temp_downloads_notice") # Separate dir

    def run(self, collector):
        # 1. Scanning Phase
        scan_total = 0
        scan_success_count = 0
        scan_duplicate_count = 0
        scan_old_count = 0
        scan_error_count = 0
        
        # Cleanup start
        if os.path.exists(self.download_dir):
            shutil.rmtree(self.download_dir)
        os.makedirs(self.download_dir, exist_ok=True)
        
        driver = None
        try:
            options = Options()
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("--window-size=1920,1080")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            prefs = {
                "download.default_directory": self.download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            options.add_experimental_option("prefs", prefs)
            
            # 드라이버 실행
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
            driver.get(self.list_url)
            
            wait = WebDriverWait(driver, 30)
            try:
                # 테이블 태그를 기다림 (class name 변경 등에 대비)
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
                time.sleep(1) # 렌더링 안정화 대기
            except:
                print(f"[{self.source_name}] 테이블 로드 타임아웃.")
                return {
                     "source": self.source_name, "success": 0, "duplicate": 0, "old": 0, "error": 1, "total": 0
                }

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            # Select rows from table inside div.tbl
            rows = soup.select("div.tbl table tbody tr")
            if not rows:
                rows = soup.select("div.tbl table tr") # Fallback
            
            if not rows:
                print(f"[{self.source_name}] 게시글을 찾을 수 없습니다 (No rows).")
                return {
                     "source": self.source_name, "success": 0, "duplicate": 0, "old": 0, "error": 0, "total": 0
                }
            
            posts = []
            for row in rows:
                try:
                    tds = row.select("td")
                    # 공지사항 행은 td 개수가 다를 수 있음, 하지만 보통 5개 이상
                    if len(tds) < 4: continue
                    
                    # 제목 및 링크 (보통 2번째 td)
                    title_elem = tds[1].select_one("a")
                    if not title_elem: continue
                    
                    title = title_elem.get_text(strip=True)
                    href = title_elem.get('href')
                    if not href: continue
                    
                    if not href.startswith('http'):
                        href = urllib.parse.urljoin(self.base_url, href)
                    
                    # 날짜 (마지막 td가 보통 날짜인 경우가 많음, 또는 뒤에서 2번째)
                    date_text = tds[-1].get_text(strip=True)
                    
                    posts.append({'title': title, 'url': href, 'date': date_text})
                except Exception as e:
                    # print(f"Row parsing error: {e}")
                    continue
            
            scan_total = len(posts)
            
            for post in posts:
                try:
                    posting_date = date_re(post['date'])
                    if not posting_date: 
                        # 날짜 파싱 실패 시 오늘 날짜로 가정하거나 스킵
                        posting_date = datetime.now()
                    
                    
                    # 4. 상세 페이지 방문
                    # is_recent, Duplicate_check 확인
                    # [Fix] 90일 기준 (Aggregator와 동일하게 맞춤)
                    if not self.is_recent(posting_date, days=90):
                         scan_old_count += 1
                         continue

                    if Duplicate_check(post['url'], BOANISSUE_DATABASE_ID) == 1:
                        scan_duplicate_count += 1
                        continue

                    driver.get(post['url'])

                    # [Fix] URL Redirection Check
                    # 보호나라 공지사항 중 일부는 KRCERT(KNVD) 등으로 리다이렉트 될 수 있음
                    # 리다이렉트 된 최종 URL로 다시 한 번 중복 체크를 수행
                    try:
                        final_url = driver.current_url
                        if final_url and final_url != post['url']:
                            # print(f" [Info] URL Redirected: {post['url']} -> {final_url}")
                            if Duplicate_check(final_url, BOANISSUE_DATABASE_ID) == 1:
                                print(f" [Skip] Redirected URL Duplicate: {final_url}")
                                scan_duplicate_count += 1
                                continue
                            # URL 업데이트 (저장 시 최종 URL 사용)
                            post['url'] = final_url
                    except Exception as e:
                        print(f" [Warn] URL Check Error: {e}")

                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.content, div.board_detail_contents, div.tbl"))
                    )
                    
                    detail_soup = BeautifulSoup(driver.page_source, 'html.parser')
                    
                    # 본문 추출 (Selector 우선순위 적용)
                    content = ""
                    content_selectors = [
                        "div.content_html", 
                        "div.content",
                        "div.board_detail_contents", 
                        "div.board_detail_view",
                        "div.view_content"
                    ]
                    
                    for selector in content_selectors:
                        content_element = detail_soup.select_one(selector)
                        if content_element:
                            # [Fix] Use centralized cleaner for robust extraction
                            # Remove attachment sections first
                            for attach in content_element.select("div.board_detail_attach, ul.file_list, div.attach"):
                                attach.decompose()

                            content = clean_html_content(str(content_element))
                            break
                    
                    if not content:
                        print(f"Warning: Content extraction failed for {post['url']}")
                    
                    # 첨부파일 정보 추출
                    files_to_upload = []

                    # [New] 본문 이미지 다운로드 및 업로드
                    if content_element:
                        try:
                            img_tags = content_element.select("img")
                            for i, img in enumerate(img_tags):
                                img_src = img.get("src")
                                if img_src:
                                    # [Fix] Handle data URI
                                    if img_src.startswith("data:image"):
                                        try:
                                            # data:image/png;base64,.....
                                            header, encoded = img_src.split(",", 1)
                                            ext = "png" if "png" in header else "jpg"
                                            if "jpeg" in header: ext = "jpg"
                                            if "gif" in header: ext = "gif"
                                            
                                            import base64
                                            img_data = base64.b64decode(encoded)
                                            
                                            img_name = f"image_{int(time.time())}_{i}.{ext}"
                                            local_path = os.path.join(self.download_dir, img_name)
                                            
                                            with open(local_path, "wb") as f:
                                                f.write(img_data)
                                            
                                            files_to_upload.append({'name': img_name, 'path': local_path, 'type': 'image'})
                                            print(f"  Saved Base64 image: {img_name}")
                                            continue
                                        except Exception as e:
                                            print(f"  ❌ Failed to decode base64 image: {e}")
                                            continue

                                    if not img_src.startswith("http"):
                                        img_src = urllib.parse.urljoin(self.base_url, img_src)
                                    
                                    # 파일명 생성 (KISA viewImage.do 등 대응)
                                    parsed_url = urllib.parse.urlparse(img_src)
                                    img_name = os.path.basename(parsed_url.path)
                                    if not img_name or "viewImage" in img_name or not os.path.splitext(img_name)[1]:
                                        img_name = f"image_{int(time.time())}_{i}.jpg"
                                    
                                    # 다운로드
                                    try:
                                        print(f"  Downloading image: {img_name}")
                                        img_resp = requests.get(img_src, verify=False, timeout=10)
                                        if img_resp.status_code == 200:
                                            local_path = os.path.join(self.download_dir, img_name)
                                            # 중복 방지
                                            if os.path.exists(local_path):
                                                 base, ext = os.path.splitext(img_name)
                                                 local_path = os.path.join(self.download_dir, f"{base}_{int(time.time())}{ext}")
                                                 
                                            with open(local_path, 'wb') as f:
                                                f.write(img_resp.content)
                                            
                                            
                                            files_to_upload.append({'name': img_name, 'path': local_path, 'type': 'image'})
                                    except Exception as e:
                                        print(f"  ❌ Image download failed: {e}")
                        except Exception as e:
                            print(f"  ❌ Image processing error: {e}")

                    file_params_list = []
                    # onclick="fileDown('file_id', 'type_id', 'bbs_id')"
                    # Check both general a tags and those inside div.attach
                    attach_links = detail_soup.select("a[onclick*='fileDown']")
                    if not attach_links:
                        attach_links = detail_soup.select("div.attach a[onclick*='fileDown']")

                    for link in attach_links:
                        onclick = link.get('onclick', '')
                        match = re.search(r"fileDown\(['\"]([^'\"]+)['\"],\s*['\"]([^'\"]+)['\"],\s*['\"]([^'\"]+)['\"]", onclick)
                        if match:
                             file_params_list.append({
                                 "file_id": match.group(1),
                                 "type_id": match.group(2),
                                 "bbs_id": match.group(3),
                                 "name": link.get_text(strip=True)
                             })
                    
                    for idx, params in enumerate(file_params_list):
                        if idx > 0:
                            # Re-visit page for multiple downloads (KISA limitation?)
                            driver.get(post['url'])
                            time.sleep(2)
                        
                        print(f"  Downloading file {idx+1}/{len(file_params_list)}: {params['name']}")
                        downloaded_file = self.download_file_simple(
                            driver, params['file_id'], params['type_id'], params['bbs_id'], self.download_dir
                        )
                        if downloaded_file:
                             downloaded_file['type'] = 'file' # Default type
                             files_to_upload.append(downloaded_file)
                             print(f"  ✅ Downloaded: {downloaded_file['name']}")
                        else:
                             print(f"  ❌ Failed to download: {params['name']}")
                    
                    # 본문 마지막에 첨부파일 목록 추가 (텍스트로도 남김)
                    final_content = content
                    if file_params_list:
                        final_content += "\n\n[첨부파일]\n" + "\n".join([p['name'] for p in file_params_list])
                    
                    # 큐에 등록
                    collector.publish_article(
                        title=post['title'],
                        content=final_content, 
                        url=post['url'],
                        date=posting_date.strftime('%Y-%m-%d'),
                        category="보호나라", 
                        details=final_content, # Raw Content + Attachments List text
                        database_id=BOANISSUE_DATABASE_ID,
                        files=files_to_upload # Uploaded file paths
                    )
                    
                    scan_success_count += 1
                    
                except Exception as e:
                    print(f"[{self.source_name}-ERROR] 항목 처리 중 오류 ({post['title']}): {e}")
                    scan_error_count += 1
                    
        except Exception as e:
             print(f"[{self.source_name}-ERROR] 크롤링 실패: {e}")
             scan_error_count += 1
             
        finally:
            if driver:
                driver.quit()
            
            # Cleanup at exit
            # [Mod] Don't remove directory here, Consumer will clean up files
            # if os.path.exists(self.download_dir):
            #     shutil.rmtree(self.download_dir)
                 
        return {
            "source": self.source_name,
            "success": scan_success_count,
            "duplicate": scan_duplicate_count,
            "old": scan_old_count,
            "error": scan_error_count,
            "total": scan_total
        }

    def download_file_simple(self, driver, file_id, type_id, bbs_id, download_dir):
        try:
            before_time = time.time()
            js_cmd = f"fileDown('{file_id}', '{type_id}', '{bbs_id}');"
            driver.execute_script(js_cmd)
            
            # Wait for download
            for _ in range(60): # 30초 대기
                try:
                    current_files = os.listdir(download_dir)
                    new_files = []
                    for f in current_files:
                        if f.endswith(('.crdownload', '.tmp', '.part')) or f.startswith('.'): continue
                        file_path = os.path.join(download_dir, f)
                        if not os.path.isfile(file_path): continue
                        
                        # 0바이트 파일 무시
                        if os.path.getsize(file_path) == 0: continue

                        if os.path.getmtime(file_path) > before_time:
                            new_files.append((f, os.path.getmtime(file_path)))
                    
                    if new_files:
                        new_files.sort(key=lambda x: x[1], reverse=True)
                        new_file_name = new_files[0][0]
                        # 다운로드 완료 확인 (확장자 변경 등)
                        return {'path': os.path.join(download_dir, new_file_name), 'name': new_file_name}
                    
                    time.sleep(0.5)
                except:
                    time.sleep(0.5)
            return None
        except Exception as e:
            print(f"파일 다운로드 오류: {e}")
            return None
