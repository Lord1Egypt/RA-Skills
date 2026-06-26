import requests
from bs4 import BeautifulSoup
from datetime import datetime
import xml.etree.ElementTree as ET

from ..base_crawler import BaseCrawler
from ..utils import date_re, send_slack_message
from ..notion_handler import Duplicate_check
from config import BOANISSUE_DATABASE_ID

class DailySecuCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.source_name = "데일리시큐"
        self.rss_url = "https://www.dailysecu.com/rss/S1N2.xml"

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
        
        # print(f"[{self.source_name}] 스캔 시작 (Phase 1)...")
        try:
            response = requests.get(self.rss_url, timeout=15)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            
            root = ET.fromstring(response.text)
            channel = root.find('channel')
            if channel is None:
                # print(f"[{self.source_name}-INFO] RSS 채널을 찾을 수 없습니다.")
                return {
                    "source": self.source_name, "success": 0, "duplicate": 0, "old": 0, "error": 1, "total": 0
                }

            items = channel.findall('item')
            if not items:
                return {
                    "source": self.source_name, "success": 0, "duplicate": 0, "old": 0, "error": 0, "total": 0
                }

            scan_total = len(items)

            for item in items:
                title = item.findtext('title', default='제목 없음').strip()
                link_url = item.findtext('link', default='').strip()
                original_content = item.findtext('description', default='내용 없음').strip()
                
                pub_date_str = item.findtext('pubDate', default='').strip()
                if not pub_date_str:
                    dc_date = item.find('{http://purl.org/dc/elements/1.1/}date')
                    if dc_date is not None:
                        pub_date_str = dc_date.text.strip()

                if not link_url: continue

                posting_date = date_re(pub_date_str)
                if not posting_date:
                    # print(f"[{self.source_name}-SKIP] 날짜 변환 실패: {title}")
                    scan_error_count += 1
                    continue
                
                if not self.is_recent(posting_date):
                    scan_old_count += 1
                    continue

                # [New] 이번 실행 내 중복 체크
                if link_url in seen_urls:
                    scan_duplicate_count += 1
                    continue
                seen_urls.add(link_url)

                duplicate_status = Duplicate_check(link_url, BOANISSUE_DATABASE_ID)
                if duplicate_status == 0:
                    # ---------------------------------------------------------
                    # 큐에 적재 (Producer-Consumer)
                    # ---------------------------------------------------------
                    try:
                        # print(f"[{self.source_name}] ✨ 유효 기사 발견! 큐에 등록: {title[:30]}...")

                        if publisher_service:
                            publisher_service.publish_article(
                                title=title,
                                content=original_content, # Raw Content
                                url=link_url,
                                date=posting_date.strftime('%Y-%m-%d'),
                                category="데일리시큐",
                                details=original_content, # Raw Content
                                database_id=BOANISSUE_DATABASE_ID
                            )
                        scan_success_count += 1

                    except Exception as e:
                        print(f"[{self.source_name}-ERROR] 큐 등록 중 오류 ({title}): {e}")
                        scan_error_count += 1
                        
                elif duplicate_status == 1:
                    scan_duplicate_count += 1
            
        except Exception as e:
            print(f"[{self.source_name}-ERROR] 스캔 중 오류: {e}")
            send_slack_message(f"[ERROR] {self.source_name} 스캔 중 오류: {e}")
            scan_error_count += 1

        return {
            "source": self.source_name,
            "success": process_success_count,
            "duplicate": scan_duplicate_count,
            "old": scan_old_count,
            "error": scan_error_count + process_error_count,
            "total": scan_total
        }
