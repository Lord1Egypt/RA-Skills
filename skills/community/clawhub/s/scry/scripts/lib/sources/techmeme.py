"""Techmeme source for SCRY skill."""

from ..source_base import Source, SourceMeta
from .. import http, query, dates
from typing import Any, Dict, List
import xml.etree.ElementTree as ET
import re
from email.utils import parsedate_to_datetime


class TechmemeSource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="techmeme",
            display_name="Techmeme",
            tier=1,
            emoji="\U0001f4f0",
            id_prefix="TM",
            has_engagement=False,
            requires_keys=[],
            requires_bins=[],
            domains=["tech", "news"],
        )

    def is_available(self, config):
        return True

    def search(self, topic, from_date, to_date, depth, config):
        dc = self.depth_config(depth)
        core = query.extract_core_subject(topic)
        keywords = query.extract_keywords(topic)

        try:
            xml_text = http.fetch_rss("https://www.techmeme.com/feed.xml", timeout=dc["timeout"])
        except http.HTTPError:
            return []

        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError:
            return []

        # RSS 2.0: channel/item
        channel = root.find("channel")
        if channel is None:
            # Try Atom format
            rss_items = root.findall("item")
        else:
            rss_items = channel.findall("item")

        items = []
        for rss_item in rss_items:
            title = rss_item.findtext("title", "").strip()
            if not title:
                continue

            # Filter by keyword match in title
            title_lower = title.lower()
            matched = any(kw.lower() in title_lower for kw in keywords)
            if not matched and core.lower() not in title_lower:
                continue

            link = rss_item.findtext("link", "").strip()
            description = rss_item.findtext("description", "").strip()
            # Strip HTML from description
            snippet = re.sub(r"<[^>]+>", "", description).strip()

            # Parse pubDate (RFC 2822 format, e.g. "Thu, 06 Mar 2026 12:00:00 GMT")
            pub_date = rss_item.findtext("pubDate", "").strip()
            item_date = None
            if pub_date:
                try:
                    dt = parsedate_to_datetime(pub_date)
                    item_date = dt.strftime("%Y-%m-%d")
                except (ValueError, TypeError):
                    # Fallback to dates module
                    dt = dates.parse_date(pub_date)
                    if dt:
                        item_date = dt.date().isoformat()

            items.append({
                "title": title,
                "url": link,
                "date": item_date,
                "relevance": query.compute_relevance(topic, title),
                "engagement": None,
                "snippet": snippet[:500],
                "source_id": link,
            })

            if len(items) >= dc["max_results"]:
                break

        return items


def get_source():
    return TechmemeSource()
