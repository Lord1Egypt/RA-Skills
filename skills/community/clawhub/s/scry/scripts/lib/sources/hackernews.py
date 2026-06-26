"""Hacker News source for SCRY skill."""

from ..source_base import Source, SourceMeta
from .. import http, query, dates
from typing import Any, Dict, List
from urllib.parse import quote_plus


class HackerNewsSource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="hackernews",
            display_name="Hacker News",
            tier=1,
            emoji="\U0001f7e1",
            id_prefix="HN",
            has_engagement=True,
            requires_keys=[],
            requires_bins=[],
            domains=["tech", "dev", "general"],
        )

    def is_available(self, config):
        return True

    def search(self, topic, from_date, to_date, depth, config):
        dc = self.depth_config(depth)
        core = query.extract_core_subject(topic)

        # Convert from_date to unix timestamp for numericFilters
        from_dt = dates.parse_date(from_date)
        from_ts = int(from_dt.timestamp()) if from_dt else 0

        url = (
            f"https://hn.algolia.com/api/v1/search"
            f"?query={quote_plus(core)}"
            f"&tags=story"
            f"&numericFilters=created_at_i>{from_ts}"
            f"&hitsPerPage={dc['max_results']}"
        )

        try:
            data = http.get(url, timeout=dc["timeout"])
        except http.HTTPError:
            return []

        hits = data.get("hits", [])
        items = []
        for hit in hits:
            title = hit.get("title", "")
            if not title:
                continue

            item_url = hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}"
            created_at = hit.get("created_at", "")
            item_date = None
            if created_at:
                dt = dates.parse_date(created_at)
                if dt:
                    item_date = dt.date().isoformat()

            items.append({
                "title": title,
                "url": item_url,
                "date": item_date,
                "relevance": query.compute_relevance(topic, title),
                "engagement": {
                    "score": hit.get("points", 0),
                    "num_comments": hit.get("num_comments", 0),
                },
                "author": hit.get("author", ""),
                "snippet": "",
                "source_id": hit.get("objectID", ""),
            })

        return items

    def enrich(self, items, depth, config):
        """Fetch top comments for top 3 stories."""
        if depth == "quick":
            return items

        dc = self.depth_config(depth)
        sorted_items = sorted(items, key=lambda x: x.get("engagement", {}).get("score", 0), reverse=True)

        for item in sorted_items[:3]:
            object_id = item.get("source_id", "")
            if not object_id:
                continue

            url = f"https://hn.algolia.com/api/v1/items/{object_id}"
            try:
                data = http.get(url, timeout=dc["timeout"])
            except http.HTTPError:
                continue

            children = data.get("children", [])
            top_comments = []
            for child in children[:5]:
                text = child.get("text", "")
                if text:
                    # Strip HTML tags for snippet
                    import re
                    clean = re.sub(r"<[^>]+>", "", text)
                    top_comments.append({
                        "author": child.get("author", ""),
                        "text": clean[:300],
                    })

            if top_comments:
                item["top_comments"] = top_comments

        return items


def get_source():
    return HackerNewsSource()
