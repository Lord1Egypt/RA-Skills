"""
core - Core data models and utilities for Wechat Article Reader

This module re-exports the public API from submodules (models, security, utils)
for convenient access via `from core import ...`.
"""

from __future__ import annotations

# =============================================================================
# Re-exports from core.models
# =============================================================================
from core.models import (
    parse_count,
    ArticleMetrics,
    TrendingArticle,
    ScoredArticle,
    Category,
    TrendingResult,
)

# =============================================================================
# Re-exports from core.security
# =============================================================================
from core.security import (
    sanitize_http_url,
    safe_href_url,
    safe_wechat_account_id,
    safe_filename_from_keyword,
)

# =============================================================================
# Re-exports from core.utils
# =============================================================================
from core.utils import (
    format_number,
    resolve_article_url,
)

# =============================================================================
# Type aliases
# =============================================================================

MetricsDict = dict
ArticleDict = dict
ScoredArticleDict = dict
RawCategories = dict

# =============================================================================
# Module-level convenience exports
# =============================================================================

# Pre-defined Category singletons for direct import convenience
LOW_FAN_EXPLOSIVE = Category.LOW_FAN_EXPLOSIVE
TEN_W_READING = Category.TEN_W_READING
ORIGINAL_RANK = Category.ORIGINAL_RANK
ONE_W_READING = Category.ONE_W_READING


# =============================================================================
# Public API
# =============================================================================

__all__ = [
    # Functions
    'parse_count',
    'format_number',
    'resolve_article_url',
    'sanitize_http_url',
    'safe_href_url',
    'safe_wechat_account_id',
    'safe_filename_from_keyword',
    # Data classes
    'ArticleMetrics',
    'TrendingArticle',
    'ScoredArticle',
    'Category',
    'TrendingResult',
    # Type aliases
    'MetricsDict',
    'ArticleDict',
    'ScoredArticleDict',
    'RawCategories',
    # Category singletons
    'LOW_FAN_EXPLOSIVE',
    'TEN_W_READING',
    'ORIGINAL_RANK',
    'ONE_W_READING',
]