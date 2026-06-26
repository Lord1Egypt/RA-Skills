from __future__ import annotations

import asyncio
import logging
import re
from datetime import datetime, timedelta
from typing import Any, Dict, List

import requests

from src.models import NewsItem
from src.search.base import NewsSearchEngine

logger = logging.getLogger(__name__)

_MX_NEWS_URL = "https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search"
_MX_TIMEOUT = 30

_TYPE_MAP = {
    "INV_NEWS": "news",
    "REPORT": "report",
    "NOTICE": "announcement",
}

_TYPE_LABEL_MAP = {
    "INV_NEWS": "新闻",
    "REPORT": "研报",
    "NOTICE": "公告",
}

_TYPE_PRIORITY = {"news": 0, "report": 1, "announcement": 2}


def _parse_date(date_str: str) -> datetime:
    if not date_str:
        return datetime.min
    cleaned = re.sub(r"[年月]", "-", date_str).replace("日", " ").strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(cleaned[:len(fmt)], fmt)
        except ValueError:
            continue
    for fmt in ("%Y-%m-%d",):
        try:
            return datetime.strptime(cleaned.split()[0], fmt)
        except ValueError:
            continue
    return datetime.min


def _is_within_days(dt: datetime, max_age_days: int) -> bool:
    if dt == datetime.min:
        return True
    return dt >= datetime.now() - timedelta(days=max_age_days)


class MiaoxiangSearch(NewsSearchEngine):

    def __init__(self, api_key: str):
        self.api_key = api_key
        self._session = requests.Session()
        self._session.headers.update({
            "Content-Type": "application/json",
            "apikey": self.api_key,
        })
        logger.debug("MiaoxiangSearch 初始化成功")

    @property
    def name(self) -> str:
        return "MiaoxiangSearch"

    async def search(self, query: str, max_age_days: int = 3) -> list[NewsItem]:
        logger.debug("MiaoxiangSearch 查询: %s", query)
        try:
            result = await asyncio.to_thread(self._do_search, query)
            items = self._parse_results(result, max_age_days)
            logger.info("MiaoxiangSearch 返回 %d 条资讯 (query=%s)", len(items), query[:30])
            return items
        except Exception as e:
            logger.warning("MiaoxiangSearch 搜索失败: %s", e)
            raise

    def _do_search(self, query: str) -> Dict[str, Any]:
        resp = self._session.post(
            _MX_NEWS_URL,
            json={"query": query},
            timeout=_MX_TIMEOUT,
        )
        resp.raise_for_status()
        return resp.json()

    def _parse_results(self, result: Dict[str, Any], max_age_days: int) -> list[NewsItem]:
        status = result.get("status")
        if status != 0:
            msg = result.get("message", "")
            logger.warning("MiaoxiangSearch API error: status=%s, message=%s", status, msg)
            return []

        data = result.get("data", {})
        inner = data.get("data", {})
        search_response = inner.get("llmSearchResponse", {})
        raw_items = search_response.get("data", [])

        if not raw_items:
            logger.debug("MiaoxiangSearch: 无搜索结果")
            return []

        items: list[NewsItem] = []
        for raw in raw_items:
            info_type_raw = raw.get("informationType", "INV_NEWS")
            info_type = _TYPE_MAP.get(info_type_raw, "news")
            dt = _parse_date(raw.get("date", ""))

            if not _is_within_days(dt, max_age_days):
                continue

            title = raw.get("title", "")
            content = raw.get("content", "")
            snippet = content[:300] if content else ""

            ins_name = raw.get("insName", "")
            rating = raw.get("rating", "")
            type_label = _TYPE_LABEL_MAP.get(info_type_raw, "资讯")

            source_parts = []
            if ins_name:
                source_parts.append(ins_name)
            source_parts.append(type_label)
            if rating:
                source_parts.append(rating)
            source = "·".join(source_parts)

            date_str = raw.get("date", "")
            if isinstance(date_str, str) and len(date_str) > 10:
                date_str = date_str[:10]

            items.append(NewsItem(
                title=title,
                snippet=snippet,
                date=date_str,
                source=source,
                url="",
                info_type=info_type,
                content=content,
            ))

        items.sort(key=lambda x: _TYPE_PRIORITY.get(x.info_type, 9))
        return items
