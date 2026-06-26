#!/usr/bin/env python3
"""
Auto Publisher - News Fetching Script
Fetches global mainstream news from configurable sources (RSS, NewsAPI, custom).
Outputs structured JSON for the publisher to process.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import logging
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from html import unescape

# For full-text fetching
from html.parser import HTMLParser

# Setup logging
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "fetcher.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("news-fetcher")

# History file to track published articles (avoid duplicates)
HISTORY_FILE = Path(__file__).parent.parent / "data" / "published_history.json"


def load_history() -> set:
    """Load set of previously published article hashes."""
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()


def save_history(history: set):
    """Save published article hashes."""
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(list(history), f)


def article_hash(title: str, source_url: str) -> str:
    """Generate a unique hash for an article."""
    content = f"{title}|{source_url}"
    return hashlib.md5(content.encode()).hexdigest()


def strip_html(text: str) -> str:
    """Remove HTML tags from text."""
    clean = re.sub(r"<[^>]+>", "", text)
    return unescape(clean).strip()


def fetch_full_article(url: str, timeout: int = 15) -> str:
    """
    Fetch full article content from URL using simple readability-like extraction.
    Returns cleaned text content.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml",
        }
        req = Request(url, headers=headers)
        with urlopen(req, timeout=timeout) as response:
            html = response.read().decode("utf-8", errors="ignore")
        
        content = ""
        
        # Strategy 1: Extract all <p> tags (works for many Chinese news sites)
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL | re.IGNORECASE)
        if paragraphs and len(''.join(paragraphs)) > 200:
            content = '\n\n'.join(paragraphs)
        
        # Strategy 2: Try <article> tag
        if not content:
            article_match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL | re.IGNORECASE)
            if article_match:
                content = article_match.group(1)
        
        # Strategy 3: Try common content div patterns
        if not content:
            content_match = re.search(r'<div[^>]*class=["\'][^"\']*(?:cont_show|content|article|post|entry)[^"\']*["\'][^>]*>(.*?)</div>', html, re.DOTALL | re.IGNORECASE)
            if content_match:
                content = content_match.group(1)
        
        # Strategy 4: Fallback to body
        if not content:
            body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL | re.IGNORECASE)
            content = body_match.group(1) if body_match else html
        
        # Remove scripts, styles, nav, footer, etc.
        for tag in ['script', 'style', 'nav', 'footer', 'header', 'aside', 'iframe']:
            content = re.sub(f'<{tag}[^>]*>.*?</{tag}>', '', content, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove remaining HTML tags
        text = strip_html(content)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Only return if we got meaningful content (>200 chars)
        if len(text) > 200:
            return text.strip()[:8000]
        else:
            logger.warning(f"Extracted content too short ({len(text)} chars) for {url}")
            return ""
    except Exception as e:
        logger.warning(f"Failed to fetch full article from {url}: {e}")
        return ""


def fetch_url(url: str, timeout: int = 15) -> bytes:
    """Fetch content from URL with proper headers."""
    headers = {
        "User-Agent": "OpenClaw-AutoPublisher/1.0 (News Aggregator)",
        "Accept": "application/rss+xml, application/xml, text/xml, application/json, */*",
    }
    req = Request(url, headers=headers)
    with urlopen(req, timeout=timeout) as response:
        return response.read()


# ============================================================
# RSS Feed Parser
# ============================================================

class RSSFetcher:
    """Fetch news from RSS/Atom feeds."""

    def __init__(self, source_config: dict):
        self.url = source_config["url"]
        self.name = source_config.get("name", self.url)
        self.max_items = source_config.get("max_items", 10)

    def fetch(self) -> list:
        """Fetch and parse RSS feed, return list of news items."""
        logger.info(f"Fetching RSS: {self.name} ({self.url})")
        try:
            content = fetch_url(self.url)
            return self._parse_feed(content)
        except Exception as e:
            logger.error(f"Failed to fetch RSS '{self.name}': {e}")
            return []

    def _parse_feed(self, content: bytes) -> list:
        """Parse RSS/Atom XML content."""
        root = ET.fromstring(content)
        items = []

        # RSS 2.0
        for item in root.findall(".//item"):
            items.append(self._parse_rss_item(item))
            if len(items) >= self.max_items:
                break

        # Atom
        if not items:
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            for entry in root.findall(".//atom:entry", ns):
                items.append(self._parse_atom_entry(entry, ns))
                if len(items) >= self.max_items:
                    break

        return items

    def _parse_rss_item(self, item) -> dict:
        """Parse a single RSS item."""
        title = item.findtext("title", "").strip()
        link = item.findtext("link", "").strip()
        description = strip_html(item.findtext("description", ""))
        pub_date = item.findtext("pubDate", "")
        content_encoded = item.findtext(
            "{http://purl.org/rss/1.0/modules/content/}encoded", ""
        )

        # Extract image from content or media
        image_url = ""
        media_content = item.find("{http://search.yahoo.com/mrss/}content")
        if media_content is not None:
            image_url = media_content.get("url", "")
        elif media_content is None:
            # Try to find image in description/content
            img_match = re.search(r'<img[^>]+src=["\']([^"\']+)', content_encoded or description or "")
            if img_match:
                image_url = img_match.group(1)

        # Extract categories/tags
        tags = [cat.text for cat in item.findall("category") if cat.text]

        # Get content: prefer content:encoded, then description, then fetch full article
        content = strip_html(content_encoded) if content_encoded else description
        if len(content) < 500 and link:
            # Try to fetch full article if content is too short
            logger.info(f"Fetching full article: {title[:50]}...")
            full_content = fetch_full_article(link)
            if full_content and len(full_content) > len(content):
                content = full_content

        return {
            "title": title,
            "summary": description[:500] if description else "",
            "content": content,
            "source_url": link,
            "source_name": self.name,
            "published_date": pub_date,
            "image_url": image_url,
            "tags": tags[:10],  # Limit tags
        }

    def _parse_atom_entry(self, entry, ns) -> dict:
        """Parse a single Atom entry."""
        title = entry.findtext("atom:title", "", ns).strip()
        link_el = entry.find("atom:link[@rel='alternate']", ns)
        if link_el is None:
            link_el = entry.find("atom:link", ns)
        link = link_el.get("href", "") if link_el is not None else ""
        summary = strip_html(entry.findtext("atom:summary", "", ns))
        content = strip_html(entry.findtext("atom:content", "", ns))
        updated = entry.findtext("atom:updated", "", ns)

        tags = [cat.get("term", "") for cat in entry.findall("atom:category", ns)]

        return {
            "title": title,
            "summary": summary[:500],
            "content": content or summary,
            "source_url": link,
            "source_name": self.name,
            "published_date": updated,
            "image_url": "",
            "tags": [t for t in tags if t][:10],
        }


# ============================================================
# NewsAPI Fetcher
# ============================================================

class NewsAPIFetcher:
    """Fetch news from NewsAPI.org."""

    BASE_URL = "https://newsapi.org/v2"

    def __init__(self, source_config: dict):
        api_key_env = source_config.get("api_key_env", "NEWS_API_KEY")
        self.api_key = os.environ.get(api_key_env, "")
        self.category = source_config.get("category", "general")
        self.country = source_config.get("country", "us")
        self.query = source_config.get("query", "")
        self.max_items = source_config.get("max_items", 10)
        self.name = source_config.get("name", "NewsAPI")

    def fetch(self) -> list:
        """Fetch top headlines from NewsAPI."""
        if not self.api_key:
            logger.warning("NEWS_API_KEY not set, skipping NewsAPI source")
            return []

        logger.info(f"Fetching from NewsAPI: category={self.category}")
        try:
            if self.query:
                url = (
                    f"{self.BASE_URL}/everything?"
                    f"q={self.query}&sortBy=publishedAt"
                    f"&pageSize={self.max_items}&apiKey={self.api_key}"
                )
            else:
                url = (
                    f"{self.BASE_URL}/top-headlines?"
                    f"country={self.country}&category={self.category}"
                    f"&pageSize={self.max_items}&apiKey={self.api_key}"
                )

            content = fetch_url(url)
            data = json.loads(content)

            if data.get("status") != "ok":
                logger.error(f"NewsAPI error: {data.get('message')}")
                return []

            items = []
            for article in data.get("articles", []):
                items.append({
                    "title": article.get("title", ""),
                    "summary": article.get("description", "")[:500],
                    "content": article.get("content", "") or article.get("description", ""),
                    "source_url": article.get("url", ""),
                    "source_name": article.get("source", {}).get("name", self.name),
                    "published_date": article.get("publishedAt", ""),
                    "image_url": article.get("urlToImage", ""),
                    "tags": [],
                })
            return items

        except Exception as e:
            logger.error(f"NewsAPI fetch failed: {e}")
            return []


# ============================================================
# Custom API Fetcher
# ============================================================

class CustomAPIFetcher:
    """Fetch news from a custom REST API endpoint."""

    def __init__(self, source_config: dict):
        self.url = source_config["url"]
        self.name = source_config.get("name", "Custom API")
        self.headers = source_config.get("headers", {})
        self.response_path = source_config.get("response_path", "articles")
        self.field_mapping = source_config.get("field_mapping", {})
        self.max_items = source_config.get("max_items", 10)

    def fetch(self) -> list:
        """Fetch from custom API."""
        logger.info(f"Fetching from custom API: {self.name}")
        try:
            headers = {"User-Agent": "OpenClaw-AutoPublisher/1.0"}
            headers.update(self.headers)

            # Resolve env vars in headers
            for k, v in headers.items():
                if v.startswith("$"):
                    headers[k] = os.environ.get(v[1:], "")

            req = Request(self.url, headers=headers)
            with urlopen(req, timeout=15) as response:
                data = json.loads(response.read())

            # Navigate to articles array using response_path
            articles_data = data
            for key in self.response_path.split("."):
                if isinstance(articles_data, dict):
                    articles_data = articles_data.get(key, [])

            if not isinstance(articles_data, list):
                logger.error(f"Expected list at '{self.response_path}', got {type(articles_data)}")
                return []

            # Map fields
            mapping = {
                "title": "title",
                "summary": "summary",
                "content": "content",
                "source_url": "url",
                "published_date": "date",
                "image_url": "image",
                "tags": "tags",
            }
            mapping.update(self.field_mapping)

            items = []
            for article in articles_data[:self.max_items]:
                items.append({
                    "title": article.get(mapping["title"], ""),
                    "summary": str(article.get(mapping["summary"], ""))[:500],
                    "content": article.get(mapping["content"], ""),
                    "source_url": article.get(mapping["source_url"], ""),
                    "source_name": self.name,
                    "published_date": article.get(mapping["published_date"], ""),
                    "image_url": article.get(mapping["image_url"], ""),
                    "tags": article.get(mapping["tags"], []),
                })
            return items

        except Exception as e:
            logger.error(f"Custom API fetch failed: {e}")
            return []


# ============================================================
# Default RSS Sources (fallback)
# ============================================================

DEFAULT_RSS_SOURCES = [
    {
        "type": "rss",
        "url": "https://feeds.bbci.co.uk/news/world/rss.xml",
        "name": "BBC World News",
        "max_items": 5,
    },
    {
        "type": "rss",
        "url": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
        "name": "New York Times World",
        "max_items": 5,
    },
    {
        "type": "rss",
        "url": "https://www.aljazeera.com/xml/rss/all.xml",
        "name": "Al Jazeera",
        "max_items": 5,
    },
    {
        "type": "rss",
        "url": "https://feeds.reuters.com/reuters/worldNews",
        "name": "Reuters World",
        "max_items": 5,
    },
]


def get_fetcher(source_config: dict):
    """Factory function to create appropriate fetcher."""
    source_type = source_config.get("type", "rss").lower()

    if source_type == "rss":
        return RSSFetcher(source_config)
    elif source_type == "newsapi":
        return NewsAPIFetcher(source_config)
    elif source_type == "custom":
        return CustomAPIFetcher(source_config)
    else:
        logger.warning(f"Unknown source type: {source_type}, defaulting to RSS")
        return RSSFetcher(source_config)


def main():
    parser = argparse.ArgumentParser(description="Fetch news from configured sources")
    parser.add_argument("--config", required=True, help="Path to config.json")
    parser.add_argument("--max", type=int, default=0, help="Override max total articles")
    parser.add_argument("--no-dedup", action="store_true", help="Skip deduplication")
    parser.add_argument("--source", help="Only fetch from specific source name")
    args = parser.parse_args()

    # Load config
    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)

    sources = config.get("news_sources", DEFAULT_RSS_SOURCES)

    # Filter by source name if specified
    if args.source:
        sources = [s for s in sources if s.get("name", "").lower() == args.source.lower()]
        if not sources:
            logger.error(f"Source '{args.source}' not found in config")
            sys.exit(1)

    # Load dedup history
    history = set() if args.no_dedup else load_history()

    # Fetch from all sources
    all_articles = []
    for source in sources:
        fetcher = get_fetcher(source)
        articles = fetcher.fetch()
        logger.info(f"Fetched {len(articles)} articles from {source.get('name', 'unknown')}")
        all_articles.extend(articles)

    # Deduplication
    unique_articles = []
    for article in all_articles:
        h = article_hash(article["title"], article["source_url"])
        if h not in history:
            unique_articles.append(article)
            history.add(h)

    # Apply max limit
    posts_per_day = args.max or config.get("publishing", {}).get("posts_per_day", 10)
    unique_articles = unique_articles[:posts_per_day]

    # Save updated history
    if not args.no_dedup:
        save_history(history)

    logger.info(f"Total unique articles ready: {len(unique_articles)}")

    # Output JSON
    print(json.dumps(unique_articles, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
