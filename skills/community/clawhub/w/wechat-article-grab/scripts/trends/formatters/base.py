"""
trends/formatters/base.py - Base formatter interface
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from core.models import ScoredArticle, TrendingResult


class BaseFormatter(ABC):
    """Base class for article formatters."""

    def __init__(self, result: TrendingResult, max_items: int = 10):
        """
        Initialize formatter with trending result.

        Args:
            result: TrendingResult containing articles to format
            max_items: Maximum number of articles to include
        """
        self.result = result
        self.max_items = max_items
        self.keyword = result.keyword

    @abstractmethod
    def format(self) -> str:
        """Format articles and return output string."""
        pass

    def get_scored_articles(self) -> List[ScoredArticle]:
        """Get scored articles (may be pre-computed or computed on-demand)."""
        return self.result.scored_articles[:self.max_items]