"""Lobsters source for SCRY skill."""

from ..source_base import Source, SourceMeta
from .. import http, query, dates
from typing import Any, Dict, List


class LobstersSource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="lobsters",
            display_name="Lobsters",
            tier=1,
            emoji="\U0001f99e",
            id_prefix="LB",
            has_engagement=True,
            requires_keys=[],
            requires_bins=[],
            domains=["tech", "dev"],
        )

    def is_available(self, config):
        return True

    def search(self, topic, from_date, to_date, depth, config):
        dc = self.depth_config(depth)
        core = query.extract_core_subject(topic)
        keywords = query.extract_keywords(topic)

        items = []
        seen_urls = set()

        # Fetch from both hottest and newest endpoints
        endpoints = ["https://lobste.rs/hottest.json", "https://lobste.rs/newest.json"]

        for endpoint in endpoints:
            try:
                stories = http.get(endpoint, timeout=dc["timeout"])
            except http.HTTPError:
                continue

            if not isinstance(stories, list):
                continue

            for story in stories:
                title = story.get("title", "")
                url = story.get("url") or story.get("comments_url", "")

                if not title or url in seen_urls:
                    continue

                # Filter by keyword match in title or tags
                title_lower = title.lower()
                tags = [t.lower() for t in story.get("tags", [])]
                tag_str = " ".join(tags)
                match_text = f"{title_lower} {tag_str}"

                relevance = query.compute_relevance(topic, match_text)
                if relevance < 0.1 and not any(kw in match_text for kw in keywords):
                    continue

                seen_urls.add(url)

                item_date = None
                created = story.get("created_at", "")
                if created:
                    dt = dates.parse_date(created)
                    if dt:
                        item_date = dt.date().isoformat()

                items.append({
                    "title": title,
                    "url": url,
                    "date": item_date,
                    "relevance": max(relevance, 0.1),
                    "engagement": {
                        "score": story.get("score", 0),
                        "num_comments": story.get("comment_count", 0),
                    },
                    "author": story.get("submitter_user", {}).get("username", "") if isinstance(story.get("submitter_user"), dict) else story.get("submitter_user", ""),
                    "snippet": story.get("description", ""),
                    "tags": story.get("tags", []),
                })

        # Sort by relevance then engagement
        items.sort(key=lambda x: (x["relevance"], x.get("engagement", {}).get("score", 0)), reverse=True)
        return items[:dc["max_results"]]


def get_source():
    return LobstersSource()
