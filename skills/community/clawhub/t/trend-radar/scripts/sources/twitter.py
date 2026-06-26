"""
X/Twitter trends via trends24.in — HTML scraping, zero API key.
"""

import re
import urllib.request
from html.parser import HTMLParser
from datetime import datetime, timezone

_DEFAULT_URL = "https://trends24.in/"

_REGION_MAP = {
    "us": "united-states",
    "usa": "united-states",
    "united-states": "united-states",
    "uk": "united-kingdom",
    "united-kingdom": "united-kingdom",
    "japan": "japan",
    "jp": "japan",
    "india": "india",
    "in": "india",
    "brazil": "brazil",
    "br": "brazil",
    "china": "",
    "cn": "",
    "germany": "germany",
    "de": "germany",
    "france": "france",
    "fr": "france",
    "canada": "canada",
    "ca": "canada",
    "australia": "australia",
    "au": "australia",
    "korea": "south-korea",
    "kr": "south-korea",
    "south-korea": "south-korea",
    "mexico": "mexico",
    "mx": "mexico",
    "spain": "spain",
    "es": "spain",
    "italy": "italy",
    "it": "italy",
    "russia": "russia",
    "ru": "russia",
    "turkey": "turkey",
    "tr": "turkey",
    "indonesia": "indonesia",
    "id": "indonesia",
    "singapore": "singapore",
    "sg": "singapore",
    "global": "",
}


class _TrendParser(HTMLParser):
    """Extracts trend names from trends24.in HTML.

    The page uses <a class=trend-link> inside <ol class=trend-card__list>.
    Attributes may be unquoted.
    """

    def __init__(self):
        super().__init__()
        self._in_trend_link = False
        self.trends = []
        self._seen = set()

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            cls = dict(attrs).get("class", "")
            if "trend-link" in cls:
                self._in_trend_link = True

    def handle_endtag(self, tag):
        if self._in_trend_link and tag == "a":
            self._in_trend_link = False

    def handle_data(self, data):
        if self._in_trend_link:
            text = data.strip()
            if text and text not in self._seen:
                self._seen.add(text)
                self.trends.append(text)


def fetch(region: str = "global", top: int = 10, timeout: int = 15) -> dict:
    """Fetch trending topics from trends24.in.

    Returns:
        {
            "source": "twitter",
            "label": "X/Twitter",
            "emoji": "🐦",
            "region": <region>,
            "fetched_at": <ISO timestamp>,
            "items": [{"rank": 1, "title": "...", "url": "..."}, ...]
        }
    """
    slug = _REGION_MAP.get(region.lower(), region.lower())
    url = _DEFAULT_URL if not slug else f"{_DEFAULT_URL}{slug}/"

    req = urllib.request.Request(url, headers={
        "User-Agent": "TrendRadar/1.0 (OpenClaw Skill)",
        "Accept": "text/html",
        "Accept-Language": "en-US,en;q=0.9",
    })

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return _error(region, str(e))

    parser = _TrendParser()
    try:
        parser.feed(html)
    except Exception:
        pass

    if not parser.trends:
        fallback = _fallback_regex(html)
        if fallback:
            parser.trends = fallback

    items = []
    for i, trend in enumerate(parser.trends[:top], 1):
        search_q = trend.replace("#", "%23").replace(" ", "+")
        items.append({
            "rank": i,
            "title": trend,
            "url": f"https://x.com/search?q={search_q}",
        })

    return {
        "source": "twitter",
        "label": "X/Twitter",
        "emoji": "🐦",
        "region": region,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "items": items,
    }


def _fallback_regex(html: str):
    """Regex fallback if HTML parser didn't catch trends."""
    seen = set()
    results = []
    for m in re.finditer(r'class=["\']?[^"\']*trend-link[^"\']*["\']?[^>]*>([^<]+)<', html):
        t = m.group(1).strip()
        if t and t not in seen:
            seen.add(t)
            results.append(t)
    return results


def _error(region: str, msg: str) -> dict:
    return {
        "source": "twitter",
        "label": "X/Twitter",
        "emoji": "🐦",
        "region": region,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "error": msg,
        "items": [],
    }
