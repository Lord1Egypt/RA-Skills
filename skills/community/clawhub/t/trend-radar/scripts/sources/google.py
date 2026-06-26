"""
Google Trends — daily trending searches via RSS feed, zero API key.
"""

import urllib.request
import re
from datetime import datetime, timezone

_RSS_TEMPLATE = "https://trends.google.com/trending/rss?geo={geo}"

_GEO_MAP = {
    "us": "US", "usa": "US", "united-states": "US",
    "uk": "GB", "gb": "GB", "united-kingdom": "GB",
    "japan": "JP", "jp": "JP",
    "india": "IN", "in": "IN",
    "brazil": "BR", "br": "BR",
    "china": "CN", "cn": "CN",
    "germany": "DE", "de": "DE",
    "france": "FR", "fr": "FR",
    "canada": "CA", "ca": "CA",
    "australia": "AU", "au": "AU",
    "korea": "KR", "kr": "KR", "south-korea": "KR",
    "mexico": "MX", "mx": "MX",
    "spain": "ES", "es": "ES",
    "italy": "IT", "it": "IT",
    "russia": "RU", "ru": "RU",
    "turkey": "TR", "tr": "TR",
    "indonesia": "ID",
    "singapore": "SG", "sg": "SG",
    "global": "US",
}


def fetch(region: str = "US", top: int = 10, timeout: int = 15) -> dict:
    """Fetch daily trending searches from Google Trends RSS.

    Returns:
        {
            "source": "google",
            "label": "Google Trends",
            "emoji": "🔍",
            "region": <region>,
            "fetched_at": <ISO>,
            "items": [{"rank": 1, "title": "...", "traffic": "200K+", "url": "..."}, ...]
        }
    """
    geo = _GEO_MAP.get(region.lower(), region.upper())
    url = _RSS_TEMPLATE.format(geo=geo)

    req = urllib.request.Request(url, headers={
        "User-Agent": "TrendRadar/1.0 (OpenClaw Skill)",
        "Accept": "application/xml, text/xml, application/rss+xml",
    })

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            xml = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return _error(region, str(e))

    items = _parse_rss(xml, top)

    return {
        "source": "google",
        "label": "Google Trends",
        "emoji": "🔍",
        "region": geo,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "items": items,
    }


def _parse_rss(xml: str, top: int):
    """Lightweight regex-based RSS parser (no xml.etree needed for simple structure)."""
    items = []
    item_blocks = re.findall(r"<item>(.*?)</item>", xml, re.DOTALL)

    for i, block in enumerate(item_blocks[:top], 1):
        title_m = re.search(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", block)
        link_m = re.search(r"<link>(.*?)</link>", block)
        traffic_m = re.search(r"<ht:approx_traffic>(.*?)</ht:approx_traffic>", block)
        news_title_m = re.search(r"<ht:news_item_title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</ht:news_item_title>", block)

        title = title_m.group(1).strip() if title_m else "Unknown"
        link = link_m.group(1).strip() if link_m else ""
        traffic = traffic_m.group(1).strip() if traffic_m else ""
        news = news_title_m.group(1).strip() if news_title_m else ""

        item = {"rank": i, "title": title, "url": link}
        if traffic:
            item["traffic"] = traffic
        if news:
            item["related_news"] = news

        items.append(item)

    return items


def _error(region: str, msg: str) -> dict:
    return {
        "source": "google",
        "label": "Google Trends",
        "emoji": "🔍",
        "region": region,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "error": msg,
        "items": [],
    }
