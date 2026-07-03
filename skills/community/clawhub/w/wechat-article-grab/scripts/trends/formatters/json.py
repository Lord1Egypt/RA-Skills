"""
trends/formatters/json.py - JSON format output
"""

import json
from typing import List
from core.models import ScoredArticle, TrendingResult
from trends.formatters.base import BaseFormatter
from core import parse_count, sanitize_http_url, safe_wechat_account_id
from urllib.parse import quote


class JsonFormatter(BaseFormatter):
    """Format articles as JSON output."""

    def format(self) -> str:
        """Format articles as JSON string."""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    def to_dict(self) -> dict:
        """Convert result to dictionary for JSON serialization."""
        scored = self.get_scored_articles()

        items = []
        for item_data in scored:
            article = item_data.article
            photo_id = article.photo_id
            account_id = article.account_id
            acc_safe = safe_wechat_account_id(account_id)

            items.append({
                'category': article.category_name,
                'photoId': photo_id,
                'title': article.title or article.summary[:50],
                'summary': article.summary,
                'accountId': account_id,
                'accountName': article.account_name or account_id,
                'fans': article.fans,
                'publicTime': article.public_time,
                'noteLink': article.article_url,
                'authorLink': (
                    f"https://open.weixin.qq.com/qr/code?username={quote(acc_safe, safe='')}"
                    if acc_safe else ''
                ),
                'interactiveCount': article.metrics.interactive_count,
                'likeCount': article.metrics.like_count,
                'commentCount': article.metrics.comment_count,
                'shareCount': article.metrics.share_count,
                'clicksCount': article.metrics.clicks_count,
                'dataScore': round(item_data.data_score, 2),
            })

        return {
            'keyword': self.keyword,
            'total': len(items),
            'items': items
        }