from __future__ import annotations

import logging

import httpx

from src.models import NewsItem
from src.search.base import NewsSearchEngine

logger = logging.getLogger(__name__)


class BraveSearch(NewsSearchEngine):
    """Brave 搜索引擎"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.search.brave.com/res/v1/news/search"

    @property
    def name(self) -> str:
        return "Brave"

    async def search(self, query: str, max_age_days: int = 3) -> list[NewsItem]:
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": self.api_key,
        }
        params = {
            "q": query,
            "count": 10,
            "freshness": f"pd{max_age_days}" if max_age_days <= 7 else "pw",
        }
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.get(self.base_url, headers=headers, params=params)
                resp.raise_for_status()
                data = resp.json()

            results = []
            for item in data.get("results", [])[:10]:
                item_data = item if isinstance(item, dict) else {}
                results.append(NewsItem(
                    title=item_data.get("title", ""),
                    snippet=item_data.get("description", ""),
                    date=item_data.get("age", ""),
                    source=item_data.get("source", ""),
                    url=item_data.get("url", ""),
                ))
            return results
        except Exception as e:
            logger.warning("Brave 搜索失败: %s", e)
            return []
