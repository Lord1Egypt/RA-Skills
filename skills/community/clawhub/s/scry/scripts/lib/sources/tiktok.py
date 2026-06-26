"""TikTok source for SCRY skill (via ScrapeCreators API)."""

from ..source_base import Source, SourceMeta
from .. import http, query, dates
from typing import Any, Dict, List


class TikTokSource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="tiktok",
            display_name="TikTok",
            tier=2,
            emoji="\U0001f3b5",
            id_prefix="TK",
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
        url = "https://api.scrapecreators.com/v1/tiktok/search/keyword"
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
        for video in results:
            title = video.get("desc", "") or video.get("title", "")
            if not title:
                continue

            item_url = video.get("url", "") or video.get("video_url", "")
            video_id = video.get("id", "") or video.get("video_id", "")
            if not item_url and video_id:
                item_url = f"https://www.tiktok.com/video/{video_id}"

            # Parse date
            item_date = None
            create_time = video.get("createTime") or video.get("create_time")
            if create_time:
                try:
                    item_date = dates.timestamp_to_date(float(create_time))
                except (ValueError, TypeError):
                    pass

            author = video.get("author", {}).get("uniqueId", "") if isinstance(video.get("author"), dict) else str(video.get("author", ""))

            # Engagement stats may be nested under stats or at top level
            stats = video.get("stats", video)

            items.append({
                "title": title[:300],
                "url": item_url,
                "date": item_date,
                "relevance": query.compute_relevance(topic, title),
                "engagement": {
                    "views": stats.get("playCount", 0),
                    "likes": stats.get("diggCount", 0),
                    "num_comments": stats.get("commentCount", 0),
                    "shares": stats.get("shareCount", 0),
                },
                "author": author,
                "snippet": title[:300],
                "source_id": str(video_id),
            })

        return items


def get_source():
    return TikTokSource()
