from __future__ import annotations

import logging

import httpx

from src.models import NewsItem
from src.search.base import NewsSearchEngine

logger = logging.getLogger(__name__)


class BochaSearch(NewsSearchEngine):
    """Bocha（博查）搜索引擎"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.bochaai.com/v1/web-search"

    @property
    def name(self) -> str:
        return "Bocha"

    async def search(self, query: str, max_age_days: int = 3) -> list[NewsItem]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "query": query,
            "freshness": f"oneDay" if max_age_days <= 1 else "oneWeek" if max_age_days <= 7 else "oneMonth",
            "summary": False,
            "count": 10,
        }
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.post(self.base_url, headers=headers, json=payload)
                resp.raise_for_status()
                data = resp.json()

            results = []
            for item in data.get("data", {}).get("webPages", {}).get("value", [])[:10]:
                results.append(NewsItem(
                    title=item.get("name", ""),
                    snippet=item.get("snippet", ""),
                    date=item.get("dateLastCrawled", ""),
                    source=item.get("siteName", ""),
                    url=item.get("url", ""),
                ))
            return results
        except Exception as e:
            logger.warning("Bocha 搜索失败: %s", e)
            return []
