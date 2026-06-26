import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import requests
import os
import shutil
from bs4 import BeautifulSoup
from datetime import datetime

from ..base_crawler import BaseCrawler
from ..utils import date_re, send_slack_message, clean_html_content
from ..notion_handler import Duplicate_check
from config import ssl_context, BOANISSUE_DATABASE_ID

class KRCERTCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.source_name = "KRCERT"
        # Updated RSS URLs (2026-03-09)
        self.rss_urls = [
            'https://knvd.krcert.or.kr/rss/security/notice',  # 보안공지
            'https://knvd.krcert.or.kr/rss/security/info',    # 보안정보 (CVE)
        ]
        self.download_dir = os.path.join(os.getcwd(), "temp_downloads_krcert")

    def run(self, publisher_service):
        processing_queue = []
        seen_urls = set()
        scan_total = 0
        scan_success_count = 0
        scan_duplicate_count = 0
        scan_old_count = 0
        scan_error_count = 0
        process_success_count = 0
        process_error_count = 0
        
        # Cleanup
        if os.path.exists(self.download_dir):
            shutil.rmtree(self.download_dir)
        os.makedirs(self.download_dir, exist_ok=True)

        try:
            print(f"--- {self.source_name} 크롤러 시작 ---")
            
            # 두 개의 RSS 피드 수집
            for rss_url in self.rss_urls:
                print(f"Fetching: {rss_url}")
                
                try:
                    with urllib.request.urlopen(rss_url, context=ssl_context, timeout=15) as response:
                        xml_data = response.read().decode('utf-8')

                    root = ET.fromstring(xml_data)
                    channel = root.find('channel')
                    if channel is None:
                        print(f"{self.source_name} RSS에서 'channel' 태그를 찾을 수 없습니다.")
                        continue

                    items = channel.findall('item')
                    scan_total += len(items)

                    for item_elem in items:
                        title = item_elem.findtext('title', default='제목 없음').strip()
                        link_url = item_elem.findtext('link', default='').strip()
                        rss_desc = item_elem.findtext('description', default='내용 없음').strip()
                        pub_date_str = item_elem.findtext('pubDate', default='').strip()

                        if not link_url:
                            continue

                        posting_date = date_re(pub_date_str)
                        if not posting_date:
                            scan_error_count += 1
                            continue

                        if not self.is_recent(posting_date):
                            scan_old_count += 1
                            continue

                        # URL 중복 체크
                        if link_url in seen_urls:
                            scan_duplicate_count += 1
                            continue
                        seen_urls.add(link_url)

                        # CVE 기사인지 확인하고 카테고리 설정
                        is_cve = title.startswith("CVE-")
                        if is_cve:
                            category_ = "krcert_cve"
                        else:
                            category_ = "KRCERT"

                        # Notion 중복 체크
                        duplicate_status = Duplicate_check(link_url, BOANISSUE_DATABASE_ID)
                        if duplicate_status == 0:
                            # 상세 페이지에서 내용 추출
                            final_content = clean_html_content(rss_desc)
                            files_to_upload = []
                            
                            try:
                                # 상세 페이지 방문
                                resp = requests.get(link_url, timeout=10, verify=False)
                                if resp.status_code == 200:
                                    detail_soup = BeautifulSoup(resp.content, 'html.parser')
                                    
                                    # 본문 추출
                                    content_div = detail_soup.find('div', class_='view_cont')
                                    if not content_div:
                                        content_div = detail_soup.find('div', class_='board_detail_contents')
                                    
                                    if content_div:
                                        final_content = clean_html_content(content_div.get_text(separator='\n'))
                                    
                                    # 첨부 파일 추출
                                    file_links = detail_soup.select('a[href*="download"]')
                                    for file_link in file_links:
                                        file_url = file_link.get('href', '')
                                        if file_url:
                                            files_to_upload.append(file_url)
                            
                            except Exception as e:
                                print(f"[{self.source_name}-DETAIL] Error: {e}")
                            
                            # 기사 데이터 생성
                            article_data = {
                                'title': title,
                                'content': final_content or "내용 없음",
                                'url': link_url,
                                'source': self.source_name,
                                'category': category_,
                                'posting_date': posting_date,
                                'files': files_to_upload
                            }
                            
                            # Publisher Service에 전달
                            if publisher_service:
                                try:
                                    publisher_service.add_article(article_data)
                                    process_success_count += 1
                                    print(f"✅ [{self.source_name}] {title[:50]}...")
                                except Exception as e:
                                    process_error_count += 1
                                    print(f"❌ [{self.source_name}-PUBLISH] {title[:30]}: {e}")
                            else:
                                # Publisher 없으면 큐에 저장
                                processing_queue.append(article_data)
                                process_success_count += 1
                        
                        else:
                            scan_duplicate_count += 1
                
                except Exception as e:
                    print(f"[{self.source_name}-RSS] Error fetching {rss_url}: {e}")
                    scan_error_count += 1
            
            print(f"--- {self.source_name} 크롤러 완료 ---")
            
            return {
                "source": self.source_name,
                "success": process_success_count,
                "duplicate": scan_duplicate_count,
                "old": scan_old_count,
                "error": scan_error_count,
                "total": scan_total,
                "queue": processing_queue
            }
        
        except Exception as e:
            print(f"[{self.source_name}-FATAL] Error: {e}")
            import traceback
            traceback.print_exc()
            
            return {
                "source": self.source_name,
                "success": 0,
                "duplicate": 0,
                "old": 0,
                "error": 1,
                "total": 0
            }
