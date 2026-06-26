"""Bluesky source for SCRY skill."""

from ..source_base import Source, SourceMeta
from .. import http, query, dates
from typing import Any, Dict, List
from urllib.parse import quote_plus


class BlueskySource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="bluesky",
            display_name="Bluesky",
            tier=1,
            emoji="\U0001f98b",
            id_prefix="BT",
            has_engagement=True,
            requires_keys=[],
            requires_bins=[],
            domains=["tech", "news", "general"],
        )

    def is_available(self, config):
        return True

    def search(self, topic, from_date, to_date, depth, config):
        dc = self.depth_config(depth)
        core = query.extract_core_subject(topic)

        url = (
            f"https://api.bsky.app/xrpc/app.bsky.feed.searchPosts"
            f"?q={quote_plus(core)}"
            f"&limit={min(dc['max_results'], 25)}"
        )

        try:
            data = http.get(url, timeout=dc["timeout"])
        except http.HTTPError:
            return []

        posts = data.get("posts", [])
        if not isinstance(posts, list):
            return []

        items = []
        for post in posts:
            record = post.get("record", {})
            if not isinstance(record, dict):
                continue

            text = record.get("text", "")
            if not text:
                continue

            # Build a title from the first line or first 100 chars
            title = text.split("\n")[0][:100]
            if len(title) < len(text.split("\n")[0]):
                title += "..."

            # Build post URL from URI
            uri = post.get("uri", "")
            author_info = post.get("author", {})
            handle = author_info.get("handle", "") if isinstance(author_info, dict) else ""

            post_url = ""
            if uri and handle:
                # URI format: at://did:plc:xxx/app.bsky.feed.post/rkey
                parts = uri.split("/")
                if len(parts) >= 5:
                    rkey = parts[-1]
                    post_url = f"https://bsky.app/profile/{handle}/post/{rkey}"

            if not post_url:
                post_url = uri

            # Parse date
            item_date = None
            created_at = record.get("createdAt", "")
            if created_at:
                dt = dates.parse_date(created_at)
                if dt:
                    item_date = dt.date().isoformat()

            # Engagement metrics
            like_count = post.get("likeCount", 0)
            repost_count = post.get("repostCount", 0)
            reply_count = post.get("replyCount", 0)

            items.append({
                "title": title,
                "url": post_url,
                "date": item_date,
                "relevance": query.compute_relevance(topic, text),
                "engagement": {
                    "likes": like_count,
                    "reposts": repost_count,
                    "replies": reply_count,
                },
                "author": handle,
                "snippet": text[:300] if len(text) > 300 else text,
            })

        # Sort by relevance, then by total engagement
        items.sort(
            key=lambda x: (
                x["relevance"],
                sum(x.get("engagement", {}).values()),
            ),
            reverse=True,
        )
        return items[:dc["max_results"]]


def get_source():
    return BlueskySource()
