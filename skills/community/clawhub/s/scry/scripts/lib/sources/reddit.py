"""Reddit source for SCRY skill."""

from ..source_base import Source, SourceMeta
from .. import http, query, dates
from typing import Any, Dict, List
from urllib.parse import quote_plus


class RedditSource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="reddit",
            display_name="Reddit",
            tier=2,
            emoji="\U0001f7e0",
            id_prefix="RD",
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
            f"https://www.reddit.com/search/.json"
            f"?q={quote_plus(core)}"
            f"&sort=relevance"
            f"&t=month"
            f"&limit={min(dc['max_results'], 25)}"
            f"&raw_json=1"
        )

        headers = {
            "User-Agent": "scry-skill/1.0 (Claude Code Skill)",
            "Accept": "application/json",
        }

        try:
            data = http.get(url, headers=headers, timeout=dc["timeout"])
        except http.HTTPError:
            return []

        children = data.get("data", {}).get("children", [])
        items = []
        for child in children:
            post = child.get("data", {})
            title = post.get("title", "")
            if not title:
                continue

            permalink = post.get("permalink", "")
            item_url = f"https://www.reddit.com{permalink}" if permalink else post.get("url", "")

            item_date = None
            created_utc = post.get("created_utc")
            if created_utc:
                item_date = dates.timestamp_to_date(created_utc)

            selftext = post.get("selftext", "")
            relevance = query.compute_relevance(topic, f"{title} {selftext[:200]}")

            items.append({
                "title": title,
                "url": item_url,
                "date": item_date,
                "relevance": relevance,
                "engagement": {
                    "score": post.get("score", 0),
                    "num_comments": post.get("num_comments", 0),
                    "upvote_ratio": post.get("upvote_ratio", 0.0),
                },
                "author": post.get("subreddit_name_prefixed", ""),
                "snippet": selftext[:300] if selftext else "",
                "extras": {
                    "subreddit": post.get("subreddit", ""),
                    "top_comments": [],
                },
            })

        return items


def get_source():
    return RedditSource()
