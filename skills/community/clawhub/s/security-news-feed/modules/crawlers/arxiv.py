"""
arXiv Crawler - 보안 관련 논문 수집
Intelligence Agent에서 마이그레이션
"""

import arxiv
from datetime import datetime
import os
from ..base_crawler import BaseCrawler

class ArxivCrawler(BaseCrawler):
    """arXiv 논문 크롤러"""

    def __init__(self):
        super().__init__()
        self.source_name = "arXiv"
        self.categories = ["cs.CR", "cs.LG", "cs.SE"]  # 보안, 머신러닝, 소프트웨어 엔지니어링
        self.keywords = [
            "security", "vulnerability", "attack", "malware",
            "privacy", "cryptography", "authentication", "network security",
            "adversarial", "federated learning", "differential privacy"
        ]

    def run(self, publisher_service):
        """arXiv 논문 수집"""
        processing_queue = []
        seen_urls = set()
        scan_total = 0
        scan_success_count = 0
        scan_duplicate_count = 0
        scan_error_count = 0

        print(f"--- {self.source_name} 크롤러 시작 ---")

        try:
            # arXiv 검색
            search = arxiv.Search(
                query=" OR ".join([f"cat:{cat}" for cat in self.categories]),
                max_results=30,
                sort_by=arxiv.SortCriterion.SubmittedDate
            )

            for result in search.results():
                scan_total += 1

                if result.entry_id in seen_urls:
                    scan_duplicate_count += 1
                    continue

                seen_urls.add(result.entry_id)

                # 키워드 필터링
                title_lower = result.title.lower()
                summary_lower = result.summary.lower()
                if not any(keyword in title_lower or keyword in summary_lower
                          for keyword in self.keywords):
                    continue

                # 중복 체크
                from modules.notion_handler import Duplicate_check
                if Duplicate_check(result.entry_id, self.source_name):
                    scan_duplicate_count += 1
                    continue

                article = {
                    'title': result.title,
                    'url': result.entry_id,
                    'content': result.summary,
                    'posting_date': result.published,
                    'category': f"{self.source_name}_{result.primary_category}",
                    'source': self.source_name,
                    'authors': [author.name for author in result.authors],
                    'categories': result.categories
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
