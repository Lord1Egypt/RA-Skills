"""
Hada.io (GeekNews) Crawler - RSS 기반
Intelligence Agent에서 마이그레이션
"""

import feedparser
from datetime import datetime
import os
from ..base_crawler import BaseCrawler

class HadaioCrawler(BaseCrawler):
    """Hada.io (GeekNews) RSS 크롤러"""

    def __init__(self):
        super().__init__()
        self.source_name = "Hada.io"
        self.rss_url = "https://news.hada.io/rss/news"

    def run(self, publisher_service):
        """Hada.io 수집"""
        processing_queue = []
        seen_urls = set()
        scan_total = 0
        scan_success_count = 0
        scan_duplicate_count = 0
        scan_error_count = 0

        print(f"--- {self.source_name} 크롤러 시작 ---")

        try:
            feed = feedparser.parse(self.rss_url)

            for entry in feed.entries[:30]:  # 상위 30개
                scan_total += 1

                link = entry.get("link", entry.get("id", ""))
                if link in seen_urls:
                    scan_duplicate_count += 1
                    continue

                seen_urls.add(link)

                # 중복 체크
                from modules.notion_handler import Duplicate_check
                if Duplicate_check(link, self.source_name):
                    scan_duplicate_count += 1
                    continue

                # 날짜 파싱
                try:
                    if entry.get("published_parsed"):
                        published = datetime(*entry.published_parsed[:6])
                    else:
                        published = datetime.now()
                except:
                    published = datetime.now()

                # 본문 추출
                content = entry.get("summary", "")
                if entry.get("content"):
                    content = entry.get("content", [{}])[0].get("value", content)

                article = {
                    'title': entry.title,
                    'url': link,
                    'content': content[:500],  # 500자로 제한
                    'posting_date': published,
                    'category': self.source_name,
                    'source': self.source_name
                }

                processing_queue.append(article)
                scan_success_count += 1

            print(f"--- {self.source_name} 크롤러 완료 ---")

            return {
                "source": self.source_name,
                "success": scan_success_count,
                "duplicate": scan_duplicate_count,
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
                "error": 1,
                "total": 0
            }
