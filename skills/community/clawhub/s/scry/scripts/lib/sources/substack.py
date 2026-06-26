"""Substack source for SCRY skill."""

from ..source_base import Source, SourceMeta
from .. import http, query, dates
from typing import Any, Dict, List
from urllib.parse import quote_plus


class SubstackSource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="substack",
            display_name="Substack",
            tier=2,
            emoji="\U0001f4ec",
            id_prefix="SB",
            has_engagement=True,
            requires_keys=[],
            requires_bins=[],
            domains=["general"],
        )

    def is_available(self, config):
        return True

    def search(self, topic, from_date, to_date, depth, config):
        dc = self.depth_config(depth)
        core = query.extract_core_subject(topic)

        url = (
            f"https://substack.com/api/v1/post/search"
            f"?query={quote_plus(core)}"
            f"&page=0"
            f"&limit={min(dc['max_results'], 20)}"
        )

        try:
            data = http.get(url, timeout=dc["timeout"])
        except http.HTTPError:
            return []

        # Response may be a list or dict with posts key
        posts = data if isinstance(data, list) else data.get("posts", data.get("results", []))
        if not isinstance(posts, list):
            return []

        items = []
        for post in posts:
            title = post.get("title", "")
            if not title:
                continue

            item_url = post.get("canonical_url", "") or post.get("url", "")
            subtitle = post.get("subtitle", "") or post.get("description", "")

            # Parse date
            item_date = None
            post_date = post.get("post_date", "") or post.get("published_at", "") or post.get("created_at", "")
            if post_date:
                dt = dates.parse_date(post_date)
                if dt:
                    item_date = dt.date().isoformat()

            # Author info
            author = ""
            pub = post.get("publishedBylines", post.get("publication", {}))
            if isinstance(pub, dict):
                author = pub.get("name", "")
            elif isinstance(pub, list) and pub:
                author = pub[0].get("name", "") if isinstance(pub[0], dict) else ""

            relevance = query.compute_relevance(topic, f"{title} {subtitle}")

            items.append({
                "title": title,
                "url": item_url,
                "date": item_date,
                "relevance": relevance,
                "engagement": {
                    "likes": post.get("reaction_count", 0),
                    "num_comments": post.get("comment_count", 0),
                },
                "author": author,
                "snippet": subtitle[:300] if subtitle else "",
            })

        return items


def get_source():
    return SubstackSource()
