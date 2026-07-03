"""
trends/analysis.py - Account comparison and analysis utilities
"""

from dataclasses import dataclass
from typing import Dict, List
from core.models import TrendingArticle, ArticleMetrics


@dataclass
class AccountStats:
    """Statistics for a single account"""
    account_name: str
    fans: int
    article_count: int
    total_clicks: int
    total_likes: int
    total_comments: int
    total_shares: int

    @property
    def avg_clicks(self) -> float:
        return self.total_clicks / self.article_count if self.article_count > 0 else 0

    @property
    def avg_likes(self) -> float:
        return self.total_likes / self.article_count if self.article_count > 0 else 0

    @property
    def avg_comments(self) -> float:
        return self.total_comments / self.article_count if self.article_count > 0 else 0

    @property
    def avg_shares(self) -> float:
        return self.total_shares / self.article_count if self.article_count > 0 else 0


def group_by_account(articles: List[TrendingArticle]) -> List[AccountStats]:
    """
    Group articles by account and calculate aggregated statistics.

    Args:
        articles: List of TrendingArticle objects

    Returns:
        List of AccountStats sorted by total_clicks descending
    """
    account_map: Dict[str, AccountStats] = {}

    for article in articles:
        account_name = article.account_name or article.account_id
        if not account_name:
            continue

        if account_name not in account_map:
            account_map[account_name] = AccountStats(
                account_name=account_name,
                fans=article.fans,
                article_count=0,
                total_clicks=0,
                total_likes=0,
                total_comments=0,
                total_shares=0,
            )

        stats = account_map[account_name]
        stats.article_count += 1
        stats.total_clicks += article.metrics.clicks_count
        stats.total_likes += article.metrics.like_count
        stats.total_comments += article.metrics.comment_count
        stats.total_shares += article.metrics.share_count

        # Update fans if larger value found
        if article.fans > stats.fans:
            stats.fans = article.fans

    # Sort by total_clicks descending
    return sorted(account_map.values(), key=lambda x: x.total_clicks, reverse=True)


def format_number(value: float) -> str:
    """Format number to Chinese format with 万/亿 suffix."""
    if value < 10000:
        return str(int(value))
    if value < 100000000:
        wan = value / 10000
        if wan >= 10:
            return f"{int(wan)}万"
        return f"{wan:.1f}万"
    yi = value / 100000000
    return f"{yi:.1f}亿"


def generate_comparison_table(account_stats: List[AccountStats], keyword: str) -> str:
    """
    Generate a comparison table for accounts.

    Args:
        account_stats: List of AccountStats objects
        keyword: Search keyword

    Returns:
        Formatted table string
    """
    if not account_stats:
        return f"⚠️ 未找到与「{keyword}」相关的公众号数据"

    lines = []
    lines.append(f"📊 公众号数据对比: {keyword}")
    lines.append("")
    lines.append(f"{'公众号':<15} {'粉丝':>8} {'文章':>5} {'平均阅读':>10} {'平均点赞':>10} {'平均评论':>8}")
    lines.append("-" * 65)

    for stats in account_stats[:15]:  # Top 15 accounts
        lines.append(
            f"{stats.account_name:<15} "
            f"{format_number(stats.fans):>8} "
            f"{stats.article_count:>5} "
            f"{format_number(stats.avg_clicks):>10} "
            f"{int(stats.avg_likes):>10,} "
            f"{int(stats.avg_comments):>8,}"
        )

    lines.append("-" * 65)
    lines.append(f"共 {len(account_stats)} 个公众号 | {sum(s.article_count for s in account_stats)} 篇文章")

    return "\n".join(lines)