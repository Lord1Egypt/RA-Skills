"""
trends - Trending article data fetching, scoring, sorting and formatting.
"""

from trends.api import fetch_trending_data
from trends.scoring import (
    calculate_title_quality,
    calculate_relevance_score,
    calculate_data_score,
    score_article,
)
from trends.sorting import merge_and_sort, ensure_category_diversity
from trends.formatters import (
    BaseFormatter,
    TextFormatter,
    JsonFormatter,
    HtmlFormatter,
    get_formatter,
)

__all__ = [
    # API
    'fetch_trending_data',
    # Scoring
    'calculate_title_quality',
    'calculate_relevance_score',
    'calculate_data_score',
    'score_article',
    # Sorting
    'merge_and_sort',
    'ensure_category_diversity',
    # Formatters
    'BaseFormatter',
    'TextFormatter',
    'JsonFormatter',
    'HtmlFormatter',
    'get_formatter',
]