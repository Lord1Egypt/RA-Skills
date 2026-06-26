from __future__ import annotations

import logging

import httpx

from src.models import NewsItem
from src.search.base import NewsSearchEngine

logger = logging.getLogger(__name__)


class TavilySearch(NewsSearchEngine):
    """Tavily 搜索引擎"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.tavily.com/search"

    @property
    def name(self) -> str:
        return "Tavily"

    async def search(self, query: str, max_age_days: int = 3) -> list[NewsItem]:
        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": "basic",
            "include_answer": False,
            "max_results": 10,
            "topic": "news",
        }
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.post(self.base_url, json=payload)
                resp.raise_for_status()
                data = resp.json()

            results = []
            for item in data.get("results", [])[:10]:
                results.append(NewsItem(
                    title=item.get("title", ""),
                    snippet=item.get("content", ""),
                    date=item.get("published_date", ""),
                    source=item.get("url", ""),
                    url=item.get("url", ""),
                ))
            return results
        except Exception as e:
            logger.warning("Tavily 搜索失败: %s", e)
            return []
