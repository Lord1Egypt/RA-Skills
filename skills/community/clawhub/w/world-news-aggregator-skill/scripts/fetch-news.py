#!/usr/bin/env python3
"""
World News Aggregator - Fetch Script (Improved)
Enhanced with better error handling, more sources, and retry logic.

Usage:
    python fetch-news.py --sources tech,ai --limit 10 --hours 24
"""

import argparse
import json
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

try:
    import requests
    import feedparser
except ImportError:
    print("Installing dependencies...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    import requests
    import feedparser


# Improved source list with fallbacks
SOURCES = {
    "tech": [
        {"name": "TechCrunch", "url": "https://techcrunch.com/feed/", "type": "rss"},
        {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml", "type": "rss"},
        {"name": "Wired", "url": "https://www.wired.com/feed/rss", "type": "rss"},
        {"name": "Ars Technica", "url": "https://feeds.arstechnica.com/arstechnica/index", "type": "rss"},
        {"name": "Hacker News", "url": "https://hnrss.org/frontpage", "type": "rss"},
    ],
    "ai": [
        {"name": "arXiv AI", "url": "http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CV&sortBy=submittedDate&sortOrder=descending&max_results=10", "type": "atom"},
        {"name": "Google AI Blog", "url": "https://ai.googleblog.com/feeds/posts/default", "type": "rss"},
        {"name": "Papers With Code", "url": "https://paperswithcode.com/latest", "type": "html"},
    ],
    "stock": [
        {"name": "Yahoo Finance", "url": "https://finance.yahoo.com/news/rssindex", "type": "rss"},
        {"name": "Bloomberg ETF", "url": "https://www.bloomberg.com/feed/podcast/etf-report.xml", "type": "rss"},
    ],
    "mil": [
        {"name": "Defense News", "url": "https://www.defensenews.com/arc/outboundfeeds/rss/", "type": "rss"},
        {"name": "Naval News", "url": "https://www.navalnews.com/feed/", "type": "rss"},
    ],
    "cn-tech": [
        {"name": "36Kr", "url": "https://36kr.com/feed", "type": "rss"},
    ],
}

# User agents for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]


def fetch_rss(url: str, limit: int = 10, timeout: int = 10, retries: int = 2) -> List[Dict]:
    """Fetch and parse RSS feed with retry logic."""
    entries = []
    
    for attempt in range(retries + 1):
        try:
            headers = {"User-Agent": USER_AGENTS[attempt % len(USER_AGENTS)]}
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            
            feed = feedparser.parse(response.content)
            
            for entry in feed.entries[:limit]:
                entries.append({
                    "title": entry.get("title", "No title"),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", entry.get("updated", "")),
                    "summary": entry.get("summary", entry.get("description", ""))[:300] if entry.get("summary") or entry.get("description") else "",
                    "source": feed.feed.get("title", "Unknown"),
                })
            
            if entries:
                break  # Success
                
        except requests.exceptions.RequestException as e:
            if attempt < retries:
                print(f"  Retry {attempt + 1}/{retries} for {url}: {e}")
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                print(f"  Failed to fetch {url} after {retries} retries: {e}")
        except Exception as e:
            print(f"  Error parsing {url}: {e}")
            break
    
    return entries


def fetch_arxiv(url: str, limit: int = 10) -> List[Dict]:
    """Fetch and parse arXiv Atom feed."""
    entries = []
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        feed = feedparser.parse(response.content)
        
        for entry in feed.entries[:limit]:
            # Extract arXiv ID
            arxiv_id = ""
            for link in entry.links:
                if "arxiv.org/abs/" in link.href:
                    arxiv_id = link.href.split("/")[-1]
                    break
            
            # Extract authors
            authors = ", ".join([author.name for author in entry.authors]) if hasattr(entry, "authors") else ""
            
            entries.append({
                "title": entry.title,
                "link": entry.links[0].href if entry.links else "",
                "arxiv_id": arxiv_id,
                "published": entry.published[:10] if hasattr(entry, "published") and entry.published else "",
                "authors": authors,
                "summary": entry.summary[:300] if hasattr(entry, "summary") else "",
                "source": "arXiv",
            })
    except Exception as e:
        print(f"  Error fetching arXiv: {e}")
    
    return entries


def fetch_news(sources: List[str], limit: int = 10, hours: int = 24) -> Dict:
    """Fetch news from multiple sources with status tracking."""
    results = {}
    status = {}
    cutoff = datetime.now() - timedelta(hours=hours)
    
    for source_key in sources:
        if source_key not in SOURCES:
            print(f"Unknown source: {source_key}")
            continue
        
        print(f"\n📡 Fetching {source_key.upper()}...")
        results[source_key] = []
        status[source_key] = {"total": len(SOURCES[source_key]), "success": 0, "failed": 0}
        
        for source in SOURCES[source_key]:
            print(f"  → {source['name']}...", end=" ")
            
            if source["type"] == "atom":
                entries = fetch_arxiv(source["url"], limit)
            else:
                entries = fetch_rss(source["url"], limit)
            
            if entries:
                results[source_key].extend(entries)
                status[source_key]["success"] += 1
                print(f"✅ {len(entries)} items")
            else:
                status[source_key]["failed"] += 1
                print("❌ No items")
        
        # Limit total entries per category
        results[source_key] = results[source_key][:limit]
    
    return {"results": results, "status": status}


def format_markdown(data: Dict, format_type: str = "summary") -> str:
    """Format results as Markdown."""
    results = data["results"]
    status = data["status"]
    
    output = []
    output.append("# 🌍 全球信息参考\n")
    output.append(f"*更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
    
    # Status table
    output.append("## 📊 信息源状态\n")
    output.append("| 类别 | 成功 | 失败 | 状态 |")
    output.append("|------|------|------|------|")
    
    for source_key, stats in status.items():
        if stats["failed"] == 0:
            status_icon = "✅"
        elif stats["success"] > 0:
            status_icon = "⚠️"
        else:
            status_icon = "❌"
        output.append(f"| {source_key.upper()} | {stats['success']} | {stats['failed']} | {status_icon} |")
    
    output.append("")
    
    # Results
    for source_key, entries in results.items():
        if not entries:
            continue
        
        output.append(f"\n## {source_key.upper()}\n")
        
        for i, entry in enumerate(entries, 1):
            if format_type == "brief":
                output.append(f"{i}. **{entry['title']}** - {entry.get('published', '')[:10]}")
            else:
                output.append(f"\n### {entry['title']}\n")
                output.append(f"- **来源**: {entry.get('source', 'Unknown')}")
                if entry.get('published'):
                    output.append(f"- **时间**: {entry['published'][:19]}")
                if entry.get('arxiv_id'):
                    output.append(f"- **arXiv**: {entry['arxiv_id']}")
                if entry.get('authors'):
                    output.append(f"- **作者**: {entry['authors']}")
                if entry.get('summary'):
                    output.append(f"- **摘要**: {entry['summary']}...")
                output.append(f"- **链接**: {entry.get('link', 'N/A')}")
        
        output.append("\n---")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="World News Aggregator")
    parser.add_argument("--sources", type=str, default="tech,ai",
                        help="Comma-separated list of sources (tech,ai,stock,mil,cn-tech)")
    parser.add_argument("--limit", type=int, default=10,
                        help="Number of articles per source")
    parser.add_argument("--hours", type=int, default=24,
                        help="Time range in hours")
    parser.add_argument("--format", type=str, default="summary",
                        choices=["summary", "detailed", "brief"],
                        help="Output format")
    parser.add_argument("--output", type=str, default="markdown",
                        choices=["markdown", "json"],
                        help="Output format")
    
    args = parser.parse_args()
    sources = [s.strip() for s in args.sources.split(",")]
    
    print(f"🚀 Fetching news from: {', '.join(sources)}")
    print(f"📊 Limit: {args.limit} per source, Time range: {args.hours} hours\n")
    
    data = fetch_news(sources, args.limit, args.hours)
    
    if args.output == "json":
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        markdown = format_markdown(data, args.format)
        print(markdown)


if __name__ == "__main__":
    main()
