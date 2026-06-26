"""GDELT source for SCRY skill."""

from ..source_base import Source, SourceMeta
from .. import http, query, dates
from typing import Any, Dict, List
from urllib.parse import quote_plus


class GDELTSource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="gdelt",
            display_name="GDELT",
            tier=1,
            emoji="\U0001f30d",
            id_prefix="GD",
            has_engagement=False,
            requires_keys=[],
            requires_bins=[],
            domains=["news", "geopolitics"],
        )

    def is_available(self, config):
        return True

    def search(self, topic, from_date, to_date, depth, config):
        dc = self.depth_config(depth)
        core = query.extract_core_subject(topic)

        max_records = min(dc["max_results"], 250)
        url = (
            f"https://api.gdeltproject.org/api/v2/doc/doc"
            f"?query={quote_plus(core)}"
            f"&mode=artlist"
            f"&maxrecords={max_records}"
            f"&format=json"
            f"&sort=datedesc"
        )

        try:
            data = http.get(url, timeout=dc["timeout"])
        except http.HTTPError:
            return []

        articles = data.get("articles", [])
        items = []
        for article in articles:
            title = article.get("title", "")
            if not title:
                continue

            item_url = article.get("url", "")

            # Parse seendate: YYYYMMDDTHHMMSS format
            seendate = article.get("seendate", "")
            item_date = None
            if seendate:
                try:
                    # Format: 20260306T120000
                    date_part = seendate.split("T")[0]
                    if len(date_part) == 8:
                        item_date = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:8]}"
                except (IndexError, ValueError):
                    pass

            domain = article.get("domain", "")
            language = article.get("language", "")
            source_country = article.get("sourcecountry", "")

            items.append({
                "title": title,
                "url": item_url,
                "date": item_date,
                "relevance": query.compute_relevance(topic, title),
                "engagement": None,
                "snippet": "",
                "source_id": item_url,
                "extras": {
                    "domain": domain,
                    "language": language,
                    "source_country": source_country,
                },
            })

        return items


def get_source():
    return GDELTSource()
