"""Mastodon source for SCRY skill."""

from ..source_base import Source, SourceMeta
from .. import http, query, dates
from typing import Any, Dict, List
from urllib.parse import quote_plus


class MastodonSource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="mastodon",
            display_name="Mastodon",
            tier=1,
            emoji="\U0001f418",
            id_prefix="MT",
            has_engagement=True,
            requires_keys=[],
            requires_bins=[],
            domains=["tech", "general"],
        )

    def is_available(self, config):
        return True

    def search(self, topic, from_date, to_date, depth, config):
        dc = self.depth_config(depth)
        core = query.extract_core_subject(topic)
        keywords = query.extract_keywords(topic)

        # Use public hashtag timeline (no auth required)
        # Try main keywords as hashtags
        all_statuses = []
        seen_ids = set()
        limit = min(dc["max_results"], 40)

        # Try each keyword as a hashtag
        for kw in keywords[:3]:
            tag = kw.strip().lower().replace(" ", "")
            if not tag or len(tag) < 3:
                continue
            tag_url = f"https://mastodon.social/api/v1/timelines/tag/{quote_plus(tag)}?limit={limit}"
            try:
                statuses = http.get(tag_url, timeout=dc["timeout"])
                if isinstance(statuses, list):
                    for s in statuses:
                        sid = s.get("id", "")
                        if sid and sid not in seen_ids:
                            seen_ids.add(sid)
                            all_statuses.append(s)
            except http.HTTPError:
                continue

        statuses = all_statuses
        items = []
        for status in statuses:
            content = status.get("content", "")
            # Strip HTML tags for title/snippet
            import re
            clean_content = re.sub(r"<[^>]+>", "", content).strip()
            if not clean_content:
                continue

            title = clean_content[:200]

            item_url = status.get("url", "")
            created_at = status.get("created_at", "")
            item_date = None
            if created_at:
                dt = dates.parse_date(created_at)
                if dt:
                    item_date = dt.date().isoformat()

            account = status.get("account", {})
            author = account.get("acct", "")

            items.append({
                "title": title,
                "url": item_url,
                "date": item_date,
                "relevance": query.compute_relevance(topic, clean_content),
                "engagement": {
                    "likes": status.get("favourites_count", 0),
                    "reposts": status.get("reblogs_count", 0),
                    "replies": status.get("replies_count", 0),
                },
                "author": author,
                "snippet": clean_content[:500],
                "source_id": str(status.get("id", "")),
            })

        return items


def get_source():
    return MastodonSource()
