from __future__ import annotations

from abc import ABC, abstractmethod

from src.models import NewsItem


class NewsSearchEngine(ABC):
    """新闻搜索引擎抽象基类"""

    @abstractmethod
    async def search(self, query: str, max_age_days: int = 3) -> list[NewsItem]:
        """搜索新闻，返回新闻条目列表"""

    @property
    @abstractmethod
    def name(self) -> str:
        """搜索引擎名称"""
