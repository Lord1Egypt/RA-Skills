#!/usr/bin/env python3
"""
Spotify News Fetcher
来源策略：
  1. RSS 直连（官方博客/新闻室/研究）
  2. DDG 搜索（TechCrunch、The Verge、MBW 等站内 Spotify 关键词）
  3. HN Algolia API
"""

import requests
import feedparser
import json
import time
import sys
import re
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional
from pathlib import Path

try:
    from ddgs import DDGS
    HAS_DDG = True
except ImportError:
    try:
        from duckduckgo_search import DDGS
        HAS_DDG = True
    except ImportError:
        HAS_DDG = False

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

# SSL verification is intentionally LEFT ENABLED (no bypass).
# Do NOT add ssl._create_default_https_context overrides here —
# that would weaken TLS for the entire process.

# ── Domain allowlist for DDG search results ──────────────────────────────────
# Only URLs whose hostname ends with one of these suffixes will be included.
# Edit this list to restrict or extend trusted news domains.
ALLOWED_DDG_DOMAINS: tuple = (
    'atspotify.com',
    'newsroom.spotify.com',
    'spotify.design',
    'techcrunch.com',
    'theverge.com',
    'musicbusinessworldwide.com',
    'billboard.com',
    'rollingstone.com',
    'pitchfork.com',
    'forbes.com',
    'reuters.com',
    'apnews.com',
    'bbc.com',
    'bbc.co.uk',
    'theguardian.com',
    'nytimes.com',
    'wsj.com',
    'wired.com',
    'engadget.com',
    'musicweek.com',
    'news.ycombinator.com',
)

# Default per-request network timeout (seconds). Overridable via sources.json settings.timeout.
_DEFAULT_TIMEOUT: int = 12


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0 Safari/537.36'
}


class SpotifyNewsFetcher:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / 'config' / 'sources.json'
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        self.timeout = int(self.config['settings'].get('timeout', _DEFAULT_TIMEOUT))
        self.max_per_source = self.config['settings']['max_news_per_source']

    # ─────────────────────────────────────────────────────
    def fetch_all(self, hours: int = 24) -> List[Dict]:
        all_news = []
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)

        # ── 1. RSS sources ──
        for source in self.config['sources']:
            if source.get('_disabled'):
                continue
            src_type = source.get('type', 'rss')
            try:
                print(f"正在抓取 [RSS]: {source['name']}...", end=' ', flush=True)
                if src_type == 'hn_api':
                    items = self._fetch_hn(source, cutoff)
                else:
                    items = self._fetch_rss(source, cutoff)
                all_news.extend(items)
                print(f"✓ {len(items)} 条")
                time.sleep(0.5)
            except Exception as e:
                print(f"✗ {str(e)[:80]}")

        # ── 2. DDG search fallback ──
        if HAS_DDG:
            ddg_items = self._fetch_ddg(hours=hours)
            if ddg_items:
                print(f"DDG 搜索补充: ✓ {len(ddg_items)} 条")
            all_news.extend(ddg_items)
        else:
            print("⚠️  ddgs 未安装，跳过搜索补充（pip install duckduckgo-search）")

        return all_news

    # ─────────────────────────────────────────────────────
    def _fetch_rss(self, source: Dict, cutoff: datetime) -> List[Dict]:
        keyword = source.get('keyword_filter', '').lower()
        resp = requests.get(
            source['url'],
            timeout=self.timeout,
            headers=HEADERS,
            verify=True,  # Explicit: TLS verification ON
        )
        resp.raise_for_status()
        feed = feedparser.parse(resp.content)
        result = []

        for entry in feed.entries[:self.max_per_source]:
            title = entry.get('title', '').strip()
            if not title:
                continue
            summary_raw = entry.get('summary', '') or entry.get('description', '')

            # 关键词过滤
            if keyword:
                haystack = (title + ' ' + summary_raw).lower()
                if keyword not in haystack:
                    continue

            pub = self._parse_time(entry)
            if pub and pub < cutoff:
                continue

            result.append({
                'title': title,
                'url': entry.get('link', ''),
                'summary': self._clean_html(summary_raw),
                'published': pub or datetime.now(timezone.utc),
                'source': source['name'],
                'language': source['language'],
                'category': source['category'],
                'score': 0,
            })
        return result

    def _fetch_hn(self, source: Dict, cutoff: datetime) -> List[Dict]:
        resp = requests.get(
            source['url'],
            timeout=self.timeout,
            headers=HEADERS,
            verify=True,  # Explicit: TLS verification ON
        )
        data = resp.json()
        result = []
        for hit in data.get('hits', []):
            title = hit.get('title', '').strip()
            if not title or 'spotify' not in title.lower():
                continue
            ts = hit.get('created_at_i')
            pub = datetime.fromtimestamp(ts, tz=timezone.utc) if ts else datetime.now(timezone.utc)
            if pub < cutoff:
                continue
            result.append({
                'title': title,
                'url': hit.get('url') or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
                'summary': '',
                'published': pub,
                'source': 'Hacker News Spotify',
                'language': 'en',
                'category': 'community',
                'score': hit.get('points', 0),
            })
        return result

    def _fetch_ddg(self, hours: int = 24) -> List[Dict]:
        """
        用 DDG News 搜索 Spotify 相关新闻，覆盖官方博客 + 媒体报道
        """
        queries = [
            'spotify new feature product',
            'spotify engineering algorithm',
            'spotify music streaming news',
            'spotify podcast update',
            'spotify business revenue',
        ]
        timelimit = 'd' if hours <= 24 else 'w'
        results = []
        seen_urls = set()

        # Domain allowlist: only keep results from trusted news domains.
        # Internal/private hostnames will naturally fail this check, preventing
        # accidental access to intranet endpoints via search results.
        allowed_domains = ALLOWED_DDG_DOMAINS

        try:
            with DDGS() as ddgs:
                for query in queries:
                    try:
                        hits = list(ddgs.news(query, max_results=8, timelimit=timelimit))
                        for h in hits:
                            url = h.get('url', '')
                            if not url or url in seen_urls:
                                continue
                            # Allow only trusted domains; reject everything else
                            # (including any intranet or metadata-service URLs)
                            try:
                                from urllib.parse import urlparse as _up
                                hostname = _up(url).hostname or ''
                            except Exception:
                                hostname = ''
                            if not any(hostname == d or hostname.endswith('.' + d)
                                       for d in allowed_domains):
                                continue
                            title = h.get('title', '').strip()
                            body = h.get('body', '')
                            # 必须包含 spotify
                            if 'spotify' not in (title + body).lower():
                                continue
                            seen_urls.add(url)
                            source_name = self._infer_source(url)
                            category = self._infer_category(url)
                            # 解析发布时间
                            pub_str = h.get('date', '')
                            pub = datetime.now(timezone.utc)
                            if pub_str:
                                try:
                                    from dateutil import parser as dp
                                    pub = dp.parse(pub_str)
                                    if pub.tzinfo is None:
                                        pub = pub.replace(tzinfo=timezone.utc)
                                except Exception:
                                    pass
                            results.append({
                                'title': title,
                                'url': url,
                                'summary': body[:300],
                                'published': pub,
                                'source': source_name,
                                'language': 'en',
                                'category': category,
                                'score': 0,
                            })
                        time.sleep(0.3)
                    except Exception:
                        pass
        except Exception as e:
            print(f"  DDG 搜索异常: {e}", file=sys.stderr)

        return results

    # ─────────────────────────────────────────────────────
    @staticmethod
    def _infer_source(url: str) -> str:
        mapping = {
            'engineering.atspotify.com': 'Spotify Engineering Blog',
            'newsroom.spotify.com': 'Spotify Newsroom',
            'research.atspotify.com': 'Spotify Research',
            'spotify.design': 'Spotify Design',
            'techcrunch.com': 'TechCrunch',
            'theverge.com': 'The Verge',
            'musicbusinessworldwide.com': 'Music Business Worldwide',
            'billboard.com': 'Billboard',
        }
        for domain, name in mapping.items():
            if domain in url:
                return name
        return url.split('/')[2] if '/' in url else url

    @staticmethod
    def _infer_category(url: str) -> str:
        official = ['engineering.atspotify.com', 'newsroom.spotify.com',
                    'research.atspotify.com', 'spotify.design']
        for d in official:
            if d in url:
                return 'official' if 'newsroom' in url or 'spotify.design' not in url else 'design'
        return 'media'

    @staticmethod
    def _parse_time(entry) -> Optional[datetime]:
        for attr in ('published_parsed', 'updated_parsed'):
            t = entry.get(attr)
            if t:
                try:
                    return datetime(*t[:6], tzinfo=timezone.utc)
                except Exception:
                    pass
        for attr in ('published', 'updated'):
            s = entry.get(attr, '')
            if s:
                try:
                    from dateutil import parser as dp
                    dt = dp.parse(s)
                    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
                except Exception:
                    pass
        return None

    @staticmethod
    def _clean_html(html: str) -> str:
        if not html:
            return ''
        if HAS_BS4:
            text = BeautifulSoup(html, 'html.parser').get_text(' ', strip=True)
        else:
            text = re.sub(r'<[^>]+>', ' ', html)
        return ' '.join(text.split())[:300]


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--hours', type=int, default=24)
    args = p.parse_args()

    fetcher = SpotifyNewsFetcher()
    articles = fetcher.fetch_all(hours=args.hours)
    print(f"\n✅ 共抓取: {len(articles)} 条 Spotify 相关新闻")
    for a in articles[:10]:
        print(f"  [{a['source']}] {a['title']}")
        print(f"  {a['url']}")
