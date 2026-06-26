"""Google News RSS source for SCRY skill."""

import xml.etree.ElementTree as ET
from ..source_base import Source, SourceMeta
from .. import http, query, dates
from typing import Any, Dict, List
from urllib.parse import quote_plus


# RFC 2822 date format used in RSS pubDate
# e.g. "Sat, 01 Mar 2026 12:00:00 GMT"
_RFC2822_FORMATS = [
    "%a, %d %b %Y %H:%M:%S %Z",
    "%a, %d %b %Y %H:%M:%S %z",
    "%d %b %Y %H:%M:%S %Z",
    "%d %b %Y %H:%M:%S %z",
]


def _parse_pub_date(date_str: str) -> str:
    """Parse RSS pubDate to YYYY-MM-DD."""
    if not date_str:
        return None
    from datetime import datetime, timezone
    for fmt in _RFC2822_FORMATS:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    # Fallback: try the generic parser
    dt = dates.parse_date(date_str)
    if dt:
        return dt.date().isoformat()
    return None


class GoogleNewsSource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="google_news",
            display_name="Google News",
            tier=3,
            emoji="\U0001f4f0",
            id_prefix="GN",
            has_engagement=False,
            requires_keys=[],
            requires_bins=[],
            domains=["news", "general"],
        )

    def is_available(self, config):
        return True

    def search(self, topic, from_date, to_date, depth, config):
        dc = self.depth_config(depth)
        core = query.extract_core_subject(topic)

        rss_url = (
            f"https://news.google.com/rss/search"
            f"?q={quote_plus(core)}"
            f"&hl=en-US"
            f"&gl=US"
            f"&ceid=US:en"
        )

        try:
            xml_text = http.fetch_rss(rss_url, timeout=dc["timeout"])
        except http.HTTPError:
            return []

        if not xml_text:
            return []

        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError:
            return []

        # RSS structure: <rss><channel><item>...</item></channel></rss>
        channel = root.find("channel")
        if channel is None:
            return []

        rss_items = channel.findall("item")
        items = []

        for rss_item in rss_items[:dc["max_results"]]:
            title = rss_item.findtext("title", "")
            if not title:
                continue

            item_url = rss_item.findtext("link", "")

            # Parse pubDate
            pub_date_str = rss_item.findtext("pubDate", "")
            item_date = _parse_pub_date(pub_date_str)

            # Source attribution from title (Google News format: "Title - Source")
            source_name = ""
            if " - " in title:
                parts = title.rsplit(" - ", 1)
                source_name = parts[-1].strip()

            description = rss_item.findtext("description", "")

            items.append({
                "title": title,
                "url": item_url,
                "date": item_date,
                "relevance": query.compute_relevance(topic, title),
                "engagement": None,
                "author": source_name,
                "snippet": description[:300] if description else "",
            })

        return items


def get_source():
    return GoogleNewsSource()
