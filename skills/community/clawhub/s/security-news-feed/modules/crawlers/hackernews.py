"""
HackerNews Crawler - RSS 기반
Intelligence Agent에서 마이그레이션
"""

import feedparser
from datetime import datetime
import os
from ..base_crawler import BaseCrawler

class HackerNewsCrawler(BaseCrawler):
    """HackerNews RSS 크롤러"""

    def __init__(self):
        super().__init__()
        self.source_name = "HackerNews"
        self.rss_url = "https://hnrss.org/frontpage"
        self.keywords = [
            "security", "vulnerability", "attack", "malware",
            "privacy", "cryptography", "authentication", "network",
            "exploit", "hack", "breach", "cve",
            "ai", "machine learning", "agent", "automation"
        ]

    def run(self, publisher_service):
        """HackerNews 수집"""
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

                if entry.link in seen_urls:
                    scan_duplicate_count += 1
                    continue

                seen_urls.add(entry.link)

                # 키워드 필터링
                title_lower = entry.title.lower()
                summary_lower = entry.get("summary", "").lower()
                if not any(keyword in title_lower or keyword in summary_lower
                          for keyword in self.keywords):
                    continue

                # 중복 체크
                from modules.notion_handler import Duplicate_check
                if Duplicate_check(entry.link, self.source_name):
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

                article = {
                    'title': entry.title,
                    'url': entry.link,
                    'content': entry.get("summary", ""),
                    'posting_date': published,
                    'category': self.source_name,
                    'source': self.source_name,
                    'comments_url': entry.get("comments", "")
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
