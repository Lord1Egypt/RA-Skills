"""
Google News Crawler - RSS 기반
Intelligence Agent에서 마이그레이션
"""

import feedparser
from urllib.parse import quote
from datetime import datetime
import os
from ..base_crawler import BaseCrawler

class GoogleNewsCrawler(BaseCrawler):
    """Google News RSS 크롤러"""

    def __init__(self):
        super().__init__()
        self.source_name = "GoogleNews"
        self.keywords = [
            "Cybersecurity", "Security", "Vulnerability", "CVE",
            "Exploit", "Malware", "Ransomware", "Zero-day",
            "보안", "취약점", "해킹", "악성코드"
        ]

    def run(self, publisher_service):
        """Google News 수집"""
        processing_queue = []
        seen_urls = set()
        scan_total = 0
        scan_success_count = 0
        scan_duplicate_count = 0
        scan_error_count = 0

        print(f"--- {self.source_name} 크롤러 시작 ---")

        try:
            for keyword in self.keywords[:3]:  # 상위 3개 키워드만
                print(f"  키워드: {keyword}")

                try:
                    encoded_keyword = quote(keyword)
                    url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=en-US&gl=US&ceid=US:en"

                    feed = feedparser.parse(url)

                    for entry in feed.entries[:10]:  # 키워드당 10개
                        scan_total += 1

                        if entry.link in seen_urls:
                            scan_duplicate_count += 1
                            continue

                        seen_urls.add(entry.link)

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
                            'category': f"{self.source_name}_{keyword}",
                            'source': self.source_name
                        }

                        processing_queue.append(article)
                        scan_success_count += 1

                except Exception as e:
                    print(f"    ❌ Error: {str(e)[:50]}")
                    scan_error_count += 1

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
