"""Wikipedia source for SCRY skill."""

from ..source_base import Source, SourceMeta
from .. import http, query, dates
from typing import Any, Dict, List
from urllib.parse import quote_plus
import re


class WikipediaSource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="wikipedia",
            display_name="Wikipedia",
            tier=1,
            emoji="\U0001f4d6",
            id_prefix="WK",
            has_engagement=False,
            requires_keys=[],
            requires_bins=[],
            domains=["general", "reference"],
        )

    def is_available(self, config):
        return True

    def search(self, topic, from_date, to_date, depth, config):
        dc = self.depth_config(depth)
        core = query.extract_core_subject(topic)

        limit = min(dc["max_results"], 50)
        url = (
            f"https://en.wikipedia.org/w/api.php"
            f"?action=query"
            f"&list=search"
            f"&srsearch={quote_plus(core)}"
            f"&format=json"
            f"&srlimit={limit}"
        )

        try:
            data = http.get(url, timeout=dc["timeout"])
        except http.HTTPError:
            return []

        results = data.get("query", {}).get("search", [])
        items = []
        for result in results:
            title = result.get("title", "")
            if not title:
                continue

            # Strip HTML from snippet
            snippet = result.get("snippet", "")
            snippet = re.sub(r"<[^>]+>", "", snippet).strip()

            # Build URL with underscores
            title_slug = title.replace(" ", "_")
            item_url = f"https://en.wikipedia.org/wiki/{title_slug}"

            # Parse timestamp
            timestamp = result.get("timestamp", "")
            item_date = None
            if timestamp:
                dt = dates.parse_date(timestamp)
                if dt:
                    item_date = dt.date().isoformat()

            items.append({
                "title": title,
                "url": item_url,
                "date": item_date,
                "relevance": query.compute_relevance(topic, title),
                "engagement": None,
                "snippet": snippet,
                "source_id": str(result.get("pageid", "")),
            })

        return items


def get_source():
    return WikipediaSource()
