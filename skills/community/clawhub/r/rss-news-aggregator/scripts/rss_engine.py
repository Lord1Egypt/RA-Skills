"""
RSS News Aggregator - RSS订阅聚合与新闻抓取引擎
"""
import feedparser
import requests
import html2text
from datetime import datetime
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse


class RSSAggregator:
    """RSS 订阅聚合器：多源抓取、过滤、摘要、报告"""

    # 内置热门 RSS 源
    BUILTIN_FEEDS = {
        "tech": {
            "Hacker News": "https://news.ycombinator.com/rss",
            "Ars Technica": "https://feeds.arstechnica.com/arstechnica/index",
            "TechCrunch": "https://techcrunch.com/feed/",
        },
        "ai": {
            "HuggingFace Blog": "https://huggingface.co/blog/feed.xml",
            "AI News": "https://www.artificialintelligence-news.com/feed/",
        },
        "dev": {
            "Dev.to": "https://dev.to/feed",
            "StackOverflow Blog": "https://stackoverflow.blog/feed/",
        },
        "cn": {
            "阮一峰科技周刊": "https://github.com/ruanyf/weekly/releases.atom",
        },
    }

    def __init__(self, timeout: int = 15):
        self.feeds: Dict[str, str] = {}
        self.timeout = timeout
        self._h2t = html2text.HTML2Text()
        self._h2t.ignore_links = False
        self._h2t.ignore_images = True

    def add_feed(self, url: str, name: str) -> None:
        """添加 RSS 订阅源"""
        self.feeds[name] = url

    def remove_feed(self, name: str) -> None:
        """移除订阅源"""
        self.feeds.pop(name, None)

    def list_feeds(self) -> Dict[str, str]:
        """列出所有已添加的订阅源"""
        return dict(self.feeds)

    def get_builtin_feeds(self, category: str) -> Dict[str, str]:
        """获取内置分类订阅源"""
        return dict(self.BUILTIN_FEEDS.get(category, {}))

    def _parse_date(self, entry) -> Optional[str]:
        """解析文章发布时间"""
        if hasattr(entry, 'published'):
            return entry.published
        if hasattr(entry, 'updated'):
            return entry.updated
        return None

    def _extract_summary(self, entry) -> str:
        """提取文章摘要"""
        # 优先使用 summary
        raw = ""
        if hasattr(entry, 'summary'):
            raw = entry.summary
        elif hasattr(entry, 'description'):
            raw = entry.description
        elif hasattr(entry, 'content'):
            raw = entry.content[0].value if entry.content else ""

        # 转为纯文本并截断
        try:
            text = self._h2t.handle(raw)
            text = text.replace('\n', ' ').strip()
            return text[:300] + ("..." if len(text) > 300 else "")
        except Exception:
            return raw[:300] + ("..." if len(raw) > 300 else "")

    def fetch_feed(self, name: str, url: str, limit: int = 10) -> List[Dict[str, Any]]:
        """抓取单个 RSS 源的文章"""
        articles = []
        try:
            feed = feedparser.parse(url, request_headers={"User-Agent": "RSSAggregator/1.0"})
            for entry in feed.entries[:limit]:
                article = {
                    "title": getattr(entry, 'title', 'Untitled'),
                    "link": getattr(entry, 'link', ''),
                    "published": self._parse_date(entry),
                    "summary": self._extract_summary(entry),
                    "source": name,
                    "author": getattr(entry, 'author', ''),
                }
                articles.append(article)
        except Exception as e:
            articles.append({
                "title": f"[ERROR] Failed to fetch {name}",
                "link": "",
                "published": None,
                "summary": str(e),
                "source": name,
                "author": "",
            })
        return articles

    def fetch_all(self, limit_per_feed: int = 10, total_limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """抓取所有订阅源的文章"""
        all_articles = []
        for name, url in self.feeds.items():
            articles = self.fetch_feed(name, url, limit=limit_per_feed)
            all_articles.extend(articles)

        # 去重（按链接）
        seen = set()
        unique = []
        for a in all_articles:
            link = a.get("link", "")
            if link and link not in seen:
                seen.add(link)
                unique.append(a)
            elif not link:
                unique.append(a)

        # 按发布时间排序（如果有）
        try:
            unique.sort(key=lambda x: x.get("published") or "", reverse=True)
        except Exception:
            pass

        if total_limit:
            unique = unique[:total_limit]
        return unique

    def filter_by_keyword(self, articles: List[Dict[str, Any]], keywords: List[str], mode: str = "include") -> List[Dict[str, Any]]:
        """按关键词过滤文章
        mode: include(包含任一关键词) / exclude(排除所有关键词)
        """
        if not keywords:
            return articles

        keywords = [k.lower() for k in keywords]
        filtered = []
        for article in articles:
            text = f"{article.get('title', '')} {article.get('summary', '')}".lower()
            has_keyword = any(k in text for k in keywords)
            if mode == "include" and has_keyword:
                filtered.append(article)
            elif mode == "exclude" and not has_keyword:
                filtered.append(article)
        return filtered

    def generate_markdown_report(self, articles: List[Dict[str, Any]], title: str = "RSS 聚合报告") -> str:
        """生成 Markdown 格式聚合报告"""
        lines = [f"# {title}", f"\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n", f"共 {len(articles)} 篇文章\n", "---\n"]

        for article in articles:
            lines.append(f"## {article.get('title', 'Untitled')}")
            lines.append(f"- **来源**: {article.get('source', 'Unknown')}")
            if article.get('published'):
                lines.append(f"- **时间**: {article['published']}")
            if article.get('author'):
                lines.append(f"- **作者**: {article['author']}")
            if article.get('link'):
                lines.append(f"- **链接**: {article['link']}")
            if article.get('summary'):
                lines.append(f"\n{article['summary']}\n")
            lines.append("---\n")

        return "\n".join(lines)

    def generate_text_report(self, articles: List[Dict[str, Any]], title: str = "RSS 聚合报告") -> str:
        """生成纯文本格式聚合报告"""
        lines = [f"=== {title} ===", f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}", f"共 {len(articles)} 篇文章\n"]

        for i, article in enumerate(articles, 1):
            lines.append(f"[{i}] {article.get('title', 'Untitled')}")
            lines.append(f"    来源: {article.get('source', 'Unknown')}")
            if article.get('published'):
                lines.append(f"    时间: {article['published']}")
            if article.get('link'):
                lines.append(f"    链接: {article['link']}")
            if article.get('summary'):
                lines.append(f"    摘要: {article['summary'][:200]}")
            lines.append("")

        return "\n".join(lines)

    def search_by_source(self, articles: List[Dict[str, Any]], source_name: str) -> List[Dict[str, Any]]:
        """按来源名称筛选文章"""
        return [a for a in articles if source_name.lower() in a.get("source", "").lower()]
