"""Instagram source for SCRY skill (via ScrapeCreators API)."""

from ..source_base import Source, SourceMeta
from .. import http, query, dates
from typing import Any, Dict, List


class InstagramSource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="instagram",
            display_name="Instagram",
            tier=2,
            emoji="\U0001f4f8",
            id_prefix="IG",
            has_engagement=True,
            requires_keys=["SCRAPECREATORS_API_KEY"],
            requires_bins=[],
            domains=["general"],
        )

    def is_available(self, config):
        return bool(config.get("SCRAPECREATORS_API_KEY"))

    def search(self, topic, from_date, to_date, depth, config):
        dc = self.depth_config(depth)
        core = query.extract_core_subject(topic)

        api_key = config.get("SCRAPECREATORS_API_KEY", "")
        url = "https://api.scrapecreators.com/v1/instagram/reels/search"
        headers = {
            "x-api-key": api_key,
        }
        body = {
            "keyword": core,
            "count": min(dc["max_results"], 20),
        }

        try:
            data = http.post(url, json_data=body, headers=headers, timeout=dc["timeout"])
        except http.HTTPError:
            return []

        # Response structure may vary; handle list or dict with results key
        results = data if isinstance(data, list) else data.get("data", data.get("results", []))
        if not isinstance(results, list):
            return []

        items = []
        for reel in results:
            title = reel.get("caption", "") or reel.get("title", "") or reel.get("desc", "")
            if not title:
                continue

            item_url = reel.get("url", "") or reel.get("permalink", "")
            reel_id = reel.get("id", "") or reel.get("media_id", "")

            # Parse date
            item_date = None
            taken_at = reel.get("taken_at") or reel.get("timestamp") or reel.get("createTime")
            if taken_at:
                try:
                    item_date = dates.timestamp_to_date(float(taken_at))
                except (ValueError, TypeError):
                    dt = dates.parse_date(str(taken_at))
                    if dt:
                        item_date = dt.date().isoformat()

            author = reel.get("owner", {}).get("username", "") if isinstance(reel.get("owner"), dict) else str(reel.get("author", reel.get("username", "")))

            items.append({
                "title": title[:300],
                "url": item_url,
                "date": item_date,
                "relevance": query.compute_relevance(topic, title),
                "engagement": {
                    "views": reel.get("viewCount", reel.get("view_count", 0)),
                    "likes": reel.get("likeCount", reel.get("like_count", 0)),
                    "num_comments": reel.get("commentCount", reel.get("comment_count", 0)),
                },
                "author": author,
                "snippet": title[:300],
                "source_id": str(reel_id),
            })

        return items


def get_source():
    return InstagramSource()
