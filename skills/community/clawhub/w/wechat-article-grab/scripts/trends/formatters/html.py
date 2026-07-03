"""
trends/formatters/html.py - HTML card layout output
"""

import html as html_module
from datetime import datetime
from urllib.parse import quote
from core.models import ScoredArticle, TrendingResult
from trends.formatters.base import BaseFormatter
from core import sanitize_http_url, safe_href_url, safe_wechat_account_id, parse_count


class HtmlFormatter(BaseFormatter):
    """Format articles as HTML card layout."""

    def format(self) -> str:
        """Format articles as HTML card grid."""
        return self._generate_html()

    def _generate_html(self) -> str:
        """Generate complete HTML document."""
        time_range = self._get_time_range()
        cards_html = self._generate_cards()

        if not cards_html:
            return self._generate_empty_state()

        keyword_esc = html_module.escape(str(self.keyword), quote=False)
        time_range_esc = html_module.escape(str(time_range), quote=False)

        return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>公众号爆款数据分析报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: #f5f5f5;
            padding: 16px;
            color: #333;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .report-header {{
            background: linear-gradient(135deg, #07c160 0%, #1aad19 100%);
            color: white;
            padding: 20px 24px;
            border-radius: 12px;
            margin-bottom: 20px;
        }}
        .report-header h1 {{ font-size: 20px; margin-bottom: 8px; }}
        .report-header .keyword {{ font-size: 14px; opacity: 0.9; }}
        .card-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 16px;
        }}
        .card {{
            background: white;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: transform 0.2s, box-shadow 0.2s;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        .card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        }}
        .card-title-row {{
            border-bottom: 1px solid #f0f0f0;
            padding-bottom: 10px;
            display: flex;
            align-items: flex-start;
            gap: 6px;
        }}
        .card-index {{ font-size: 15px; font-weight: 700; color: #07c160; min-width: 20px; }}
        .card-title {{
            font-size: 15px;
            font-weight: 700;
            color: #1a1a1a;
            text-decoration: none;
            line-height: 1.5;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            transition: color 0.2s;
        }}
        .card-title:hover {{ color: #07c160; }}
        .card-meta {{ font-size: 13px; color: #999; padding: 8px 0; }}
        .author-link {{ color: #666; text-decoration: none; transition: color 0.2s; }}
        .author-link:hover {{ color: #07c160; }}
        .meta-divider {{ margin: 0 6px; }}
        .pub-time {{ color: #999; }}
        .card-stats {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 16px;
            margin: 0 -16px;
            background: linear-gradient(135deg, #f0f9f4, #fff);
            flex-wrap: wrap;
            gap: 8px;
        }}
        .read-count {{ font-size: 12px; color: #666; }}
        .category-tag {{
            font-size: 12px;
            color: #1aad19;
            background: #e8f8ed;
            padding: 2px 8px;
            border-radius: 4px;
        }}
        .view-note-btn {{ color: #07c160; text-decoration: none; font-size: 14px; font-weight: 500; }}
        .view-note-btn:hover {{ opacity: 0.7; }}
        .card-summary {{ font-size: 13px; color: #666; line-height: 1.5; padding: 8px 0; border-bottom: 1px dashed #f0f0f0; }}
        .quality-badge {{ font-size: 11px; padding: 2px 6px; border-radius: 4px; margin-left: 8px; vertical-align: middle; }}
        .quality-good {{ background: #e8f8ed; color: #07c160; }}
        .quality-fair {{ background: #fff3cd; color: #856404; }}
        .quality-poor {{ background: #f8d7da; color: #721c24; }}
        .card-interactions {{ display: flex; gap: 12px; padding: 8px 12px; background: #f8f9fa; border-radius: 6px; font-size: 12px; color: #666; }}
        .interaction-item {{ display: flex; align-items: center; gap: 4px; }}
        .interaction-rate {{ margin-left: auto; color: #07c160; font-weight: 600; }}
        .data-note {{ text-align: center; color: #999; font-size: 12px; margin-top: 20px; padding: 12px; background: white; border-radius: 8px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="report-header">
            <h1>公众号爆款数据分析报告</h1>
            <div class="keyword">关键词：{keyword_esc} | 时间范围：{time_range_esc}</div>
        </div>
        <div class="card-grid">
            {cards_html}
        </div>
        <div class="data-note">
            数据来源：公众号爆款文章查询，每日19点更新昨日热门内容<br>
            备注：互动数据为入库快照，实时数据可能持续增长
        </div>
    </div>
</body>
</html>'''

    def _get_time_range(self) -> str:
        """Get time range string from start_date."""
        # This would need start_date from somewhere - default to 30 days
        return "近30天"

    def _generate_cards(self) -> str:
        """Generate HTML for article cards."""
        scored = self.get_scored_articles()
        if not scored:
            return ''

        cards = []
        for idx, item_data in enumerate(scored):
            card = self._generate_card(item_data, idx)
            if card:
                cards.append(card)

        return ''.join(cards)

    def _generate_card(self, item_data: ScoredArticle, idx: int) -> str:
        """Generate HTML for single card."""
        article = item_data.article
        m = article.metrics

        # Title processing
        title = article.title
        if not title or title.strip() == '':
            summary = article.summary
            if summary:
                title = summary.replace('\n', ' ').replace('\r', ' ').strip()[:30]
                if len(summary) > 30:
                    title = title + '...'
        if not title or title.strip() == '':
            title = '无标题'
        title_esc = html_module.escape(str(title), quote=False)

        # Time formatting
        pub_time = article.public_time
        if pub_time:
            try:
                month = int(pub_time[5:7])
                day = int(pub_time[8:10])
                time_esc = html_module.escape(f"{month}月{day}日", quote=False)
            except Exception:
                time_esc = '--'
        else:
            time_esc = '--'

        # Summary
        summary_text = article.summary
        if summary_text:
            summary_esc = html_module.escape(summary_text.replace('\n', ' ').replace('\r', ' ').strip())
            if len(summary_esc) > 80:
                summary_esc = summary_esc[:80] + '...'
        else:
            summary_esc = ''

        # Interaction stats
        likes = self._format_count(m.like_count)
        comments = self._format_count(m.comment_count)
        shares = self._format_count(m.share_count)
        interaction_rate = self._get_interaction_rate(m)

        # Title quality badge
        title_quality = item_data.title_quality
        if title_quality >= 90:
            quality_badge = '<span class="quality-badge quality-good">✅ 优质</span>'
        elif title_quality >= 70:
            quality_badge = '<span class="quality-badge quality-fair">⚠️ 一般</span>'
        else:
            quality_badge = '<span class="quality-badge quality-poor">❌ 标题党</span>'

        # Links - prefer short URL via photoId
        note_link = safe_href_url(article.article_url)
        acc_safe = safe_wechat_account_id(article.account_id)
        if acc_safe:
            author_link = safe_href_url(f"https://open.weixin.qq.com/qr/code?username={quote(acc_safe, safe='')}")
        else:
            author_link = "#"

        account_name = html_module.escape(str(article.account_name), quote=False)
        cat_name = html_module.escape(str(article.category_name), quote=False)

        # Clicks display
        clicks = m.clicks_count
        if clicks >= 10000:
            clicks_display = f"{clicks/10000:.1f}万"
        else:
            clicks_display = str(clicks)

        return f'''
        <div class="card">
            <div class="card-title-row">
                <span class="card-index">{idx + 1}.</span>
                <a href="{note_link}" class="card-title" target="_blank" rel="noopener noreferrer">{title_esc}</a>
                {quality_badge}
            </div>
            {'<div class="card-summary">' + summary_esc + '</div>' if summary_esc else ''}
            <div class="card-meta">
                <a href="{author_link}" class="author-link" target="_blank" rel="noopener noreferrer">{account_name}</a>
                <span class="meta-divider">·</span>
                <span class="pub-time">发布日期：{time_esc}</span>
            </div>
            <div class="card-stats">
                <span class="read-count">📖 {clicks_display}阅读</span>
                <span class="category-tag">{cat_name}</span>
                <a href="{note_link}" class="view-note-btn" target="_blank" rel="noopener noreferrer">查看作品 ↗</a>
            </div>
            <div class="card-interactions">
                <span class="interaction-item" title="点赞">👍 {likes}</span>
                <span class="interaction-item" title="评论">💬 {comments}</span>
                <span class="interaction-item" title="分享">🔗 {shares}</span>
                <span class="interaction-rate" title="互动率">📊 {interaction_rate}</span>
            </div>
        </div>'''

    def _format_count(self, value: int) -> str:
        """Format count for display."""
        if value is None or value == 0:
            return '0'
        if value >= 10000:
            return f"{value/10000:.1f}万"
        return str(value)

    def _get_interaction_rate(self, m) -> str:
        """Calculate interaction rate."""
        total_inter = m.like_count + m.comment_count + m.share_count
        if m.clicks_count > 0:
            rate = (total_inter / m.clicks_count) * 100
            return f"{rate:.1f}%"
        return "--"

    def _generate_empty_state(self) -> str:
        """Generate empty state HTML."""
        return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>公众号爆款数据分析报告</title>
</head>
<body>
    <div class="container">
        <h2>暂无相关爆款数据</h2>
        <p>很抱歉，当前关键词暂无足够的爆款文章数据。</p>
        <p>建议更换为更热门的关键词，如"职场干货"、"育儿经验"、"情感故事"等。</p>
    </div>
</body>
</html>'''