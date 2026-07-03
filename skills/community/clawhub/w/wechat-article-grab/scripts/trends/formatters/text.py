"""
trends/formatters/text.py - Text format output
"""

from core.models import ScoredArticle, TrendingResult
from trends.formatters.base import BaseFormatter
from core import parse_count, format_number


class TextFormatter(BaseFormatter):
    """Format articles as plain text."""

    def format(self) -> str:
        """Format articles as plain text output."""
        lines = []

        if self.keyword:
            lines.append(f"📊 关键词: {self.keyword}")
        lines.append("-" * 60)

        scored = self.get_scored_articles()

        for i, scored_article in enumerate(scored, 1):
            article = scored_article.article
            m = article.metrics

            lines.append(f"\n{'='*50}")
            lines.append(f"📄 {i}. {article.title}")
            lines.append(f"🔗 {article.article_url}")
            lines.append(f"👤 {article.account_name} | 📅 {article.public_time}")

            # 粉丝数和类别
            fans_str = format_number(article.fans) if article.fans else "未知"
            cat_str = article.category_name or ""
            lines.append(f"👥 粉丝: {fans_str} | 🏷️ {cat_str}")

            # 互动数据
            lines.append(
                f"📊 点赞: {m.like_count:,} | 分享: {m.share_count:,} "
                f"| 评论: {m.comment_count:,} | 阅读: {m.clicks_count:,}"
            )

            # 文章正文/摘要
            content_preview = article.content if article.content else article.summary
            if content_preview:
                preview_len = 3500
                preview = content_preview[:preview_len] + "\n[...]" if len(content_preview) > preview_len else content_preview
                lines.append(f"📝 正文:\n{preview}")

        lines.append("\n" + "=" * 50)
        lines.append(f"共 {len(scored)} 条数据")

        return '\n'.join(lines)