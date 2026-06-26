from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime, timedelta, timezone

# KST Timezone
KST = timezone(timedelta(hours=9))

class BaseCrawler(ABC):
    """
    Abstract base class for all crawlers.
    """

    def __init__(self):
        self.source_name = "Unknown Source"

    @abstractmethod
    def run(self, publisher_service):
        """
        Execute the crawling logic.
        
        Args:
            publisher_service: Service to publish articles to Notion/Tistory.
        """
        pass

    def is_recent(self, posting_date: datetime, days: int = 90) -> bool:
        """
        Check if the posting date is within the recent 'days'.
        """
        if not posting_date:
            return False

        # Ensure posting_date is timezone-aware (KST)
        if posting_date.tzinfo:
            posting_date_kst = posting_date.astimezone(KST)
        else:
            posting_date_kst = posting_date.replace(tzinfo=KST)

        now_kst = datetime.now(KST)
        cutoff_date_kst = now_kst - timedelta(days=days)

        return posting_date_kst >= cutoff_date_kst
