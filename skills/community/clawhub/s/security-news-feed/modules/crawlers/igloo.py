import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import urllib3

from ..base_crawler import BaseCrawler
from ..utils import date_re, send_slack_message
from ..notion_handler import Duplicate_check
# from ..llm_handler import summarize_text, details_text # Moved to Processor
from config import BOANISSUE_DATABASE_ID

# SSL 경고 비활성화
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class IglooCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.source_name = "이글루코퍼레이션"
        self.urls_to_crawl = [
            "https://www.igloo.co.kr/security-information/category/security/",
            "https://www.igloo.co.kr/security-information/category/ai/",
            "https://www.igloo.co.kr/security-information/category/tech-trends/"
        ]

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

        # 1. Scanning Phase
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        driver = None
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            articles = []
            unique_urls = set()

            for url in self.urls_to_crawl:
                try:
                    driver.get(url)
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.list_box > li"))
                    )
                    
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    for li in soup.select('ul.list_box > li'):
                        link_tag = li.find('a')
                        if not link_tag: continue
                        
                        href = link_tag.get('href')
                        if not href or href in unique_urls: continue
                        
                        unique_urls.add(href)
                        
                        title_elem = li.select_one('p.tit')
                        if not title_elem: title_elem = li.select_one('div.view_ttl h2')
                        if not title_elem: title_elem = li.select_one('div.txt_box strong')
                        if not title_elem: title_elem = li.select_one('h2')
                        
                        title = title_elem.get_text(strip=True) if title_elem else "?�목 ?�음"
                        
                        date_elem = li.select_one('div.date_box p')
                        date_text = date_elem.get_text(strip=True) if date_elem else ""
                        posting_date = date_re(date_text)
                        
                        articles.append({
                            "url": href,
                            "title": title,
                            "date": posting_date
                        })

                except Exception as e:
                    # print(f"[{self.source_name}-ERROR] '{url}' 목록 ?�집 �??�류: {e}")
                    scan_error_count += 1

            scan_total = len(articles)

            headers = {"User-Agent": "Mozilla/5.0"}
            
            for art in articles:
                try:
                    article_url = art["url"]
                    title = art["title"]
                    posting_date = art["date"]

                    # 1. ?�짜 체크 (90??
                    if posting_date:
                        if not self.is_recent(posting_date):
                            scan_old_count += 1
                            continue
                    
                    # 2. 중복 체크
                    if Duplicate_check(article_url, BOANISSUE_DATABASE_ID):
                        scan_duplicate_count += 1
                        continue

                    # SSL 검�?비활?�화 (verify=False)
                    # Scanning Phase?�서 ?�세 ?�이지 ?�근?�여 content/date ?�보
                    detail_response = requests.get(article_url, headers=headers, timeout=15, verify=False)
                    detail_response.raise_for_status()
                    detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
                    
                    if not title or title == "?�목 ?�음":
                        title_elem = detail_soup.select_one('div.view_ttl h2')
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                    
                    if not posting_date:
                        date_elem = detail_soup.select_one('div.date_box p:first-child')
                        date_text = date_elem.get_text(strip=True) if date_elem else ""
                        posting_date = date_re(date_text)
                        
                        if not posting_date:
                            scan_error_count += 1
                            continue
                        
                        if not self.is_recent(posting_date):
                            scan_old_count += 1
                            continue
                    
                    content_elem = detail_soup.select_one('div.view_cont')
                    content = content_elem.get_text('\n', strip=True) if content_elem else ""
                    
                    # ---------------------------------------------------------
                    # ?�에 ?�재 (Producer-Consumer)
                    # ---------------------------------------------------------
                    try:
                        # print(f"[{self.source_name}] ???�효 기사 발견! ?�에 ?�록: {title[:30]}...")

                        if publisher_service:
                            publisher_service.publish_article(
                                title=title,
                                content=content, # Raw Content
                                url=article_url,
                                date=posting_date.strftime('%Y-%m-%d'),
                                category="Igloo",
                                details=content, # Raw Content
                                database_id=BOANISSUE_DATABASE_ID
                            )
                        scan_success_count += 1
                        
                    except Exception as e:
                        print(f"[{self.source_name}-ERROR] ???�록 �??�류 ({title}): {e}")
                        scan_error_count += 1

                    scan_success_count += 1
                    time.sleep(0.5)
                    
                except Exception as e:
                    # print(f"[{self.source_name}-ERROR] ??�� 처리 �??�류: {e}")
                    scan_error_count += 1

        except Exception as e:
            # print(f"[{self.source_name}-ERROR] ?�롤�?�??�류: {e}")
            send_slack_message(f"[ERROR] {self.source_name} ?�롤�?�??�류: {e}")
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

