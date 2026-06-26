from __future__ import annotations

import logging

import httpx

from src.models import NewsItem
from src.search.base import NewsSearchEngine

logger = logging.getLogger(__name__)


class SerpAPISearch(NewsSearchEngine):
    """SerpAPI 搜索引擎"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://serpapi.com/search"

    @property
    def name(self) -> str:
        return "SerpAPI"

    async def search(self, query: str, max_age_days: int = 3) -> list[NewsItem]:
        params = {
            "q": query,
            "api_key": self.api_key,
            "engine": "google",
            "tbm": "nws",
            "num": 10,
            "hl": "zh-cn",
            "gl": "cn",
        }
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.get(self.base_url, params=params)
                resp.raise_for_status()
                data = resp.json()

            results = []
            for item in data.get("news_results", [])[:10]:
                date_str = item.get("date", "")
                results.append(NewsItem(
                    title=item.get("title", ""),
                    snippet=item.get("snippet", ""),
                    date=date_str,
                    source=item.get("source", ""),
                    url=item.get("link", ""),
                ))
            return results
        except Exception as e:
            logger.warning("SerpAPI 搜索失败: %s", e)
            return []
