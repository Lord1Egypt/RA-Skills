import requests
import xml.etree.ElementTree as ET
from datetime import datetime

from ..base_crawler import BaseCrawler
from ..utils import date_re, send_slack_message
from ..notion_handler import Duplicate_check
# from ..llm_handler import summarize_text, details_text # Moved to Processor
from config import BOANISSUE_DATABASE_ID

class BoanNewsCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.source_name = "보안뉴스"
        self.urls = [
            'http://www.boannews.com/media/news_rss.xml?skind=5',
            'http://www.boannews.com/media/news_rss.xml?skind=6',
            'http://www.boannews.com/media/news_rss.xml?mkind=1'
        ]
        self.namespaces = {'dc': 'http://purl.org/dc/elements/1.1/'}

    def run(self, publisher_service): # publisher_service: QueueCollector or PublisherService
        # 1. Scanning Phase
        seen_urls = set()
        scan_total = 0
        scan_success_count = 0
        scan_duplicate_count = 0
        scan_old_count = 0
        scan_error_count = 0
        
        # logger.info(f"[{self.source_name}] 스캔 시작 (Phase 1)...")
        
        for rss_url in self.urls:
            try:
                # logger.debug(f"  - {rss_url} 스캔 중...")
                response = requests.get(rss_url, timeout=15)
                response.raise_for_status()
                response.encoding = response.apparent_encoding
                root = ET.fromstring(response.text)
                channel = root.find('channel')

                if channel is None: continue

                items = channel.findall('item')
                scan_total += len(items)

                for item_elem in items:
                    try:
                        title = item_elem.findtext('title', default='제목 없음').strip()
                        link_url = item_elem.findtext('link', default='').strip()
                        original_content = item_elem.findtext('description', default='내용 없음').strip()
                        category_ = "보안뉴스"

                        pub_date_str = item_elem.findtext('pubDate', default='').strip()
                        if not pub_date_str:
                            dc_date = item_elem.find('dc:date', self.namespaces)
                            if dc_date is None:
                                dc_date = item_elem.find('{http://purl.org/dc/elements/1.1/}date')
                            if dc_date is not None and dc_date.text:
                                pub_date_str = dc_date.text.strip()

                        if not link_url: continue

                        posting_date = date_re(pub_date_str)
                        if not posting_date: continue

                        if rss_url.endswith('mkind=1') and "[긴급]" not in title:
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
                        if duplicate_status == 1:
                            scan_duplicate_count += 1
                            continue

                        # ---------------------------------------------------------
                        # 큐에 등록 (Producer-Consumer)
                        # ---------------------------------------------------------
                        try:
                            # publisher_service가 publisher_service일 수도 있고 QueueCollector일 수도 있음
                            # 둘 다 publish_article 메서드를 가짐
                            if publisher_service:
                                publisher_service.publish_article(
                                    title=title,
                                    content=original_content, # Raw Content
                                    url=link_url,
                                    date=posting_date.strftime('%Y-%m-%d'),
                                    category=category_,
                                    details=original_content, # Raw Content
                                    database_id=BOANISSUE_DATABASE_ID
                                )
                            
                            scan_success_count += 1
                        
                        except Exception as e:
                            print(f"[{self.source_name}-ERROR] 등록 중 오류 ({title}): {e}")
                            scan_error_count += 1
                        
                    except Exception as e:
                        # print(f"[{self.source_name}-WARN] 항목 파싱 오류: {e}")
                        scan_error_count += 1

            except Exception as e:
                # print(f"  [{self.source_name}-ERROR] RSS ({rss_url}) 로드 실패: {e}")
                send_slack_message(f"[ERROR] {self.source_name} RSS ({rss_url}) 오류: {e}")
                scan_error_count += 1
        
        return {
            "source": self.source_name,
            "success": scan_success_count,
            "duplicate": scan_duplicate_count,
            "old": scan_old_count,
            "error": scan_error_count,
            "total": scan_total
        }