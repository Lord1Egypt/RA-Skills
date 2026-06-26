"""Stack Overflow source for SCRY skill."""

from ..source_base import Source, SourceMeta
from .. import http, query, dates
from typing import Any, Dict, List
from urllib.parse import quote_plus


class StackOverflowSource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="stackoverflow",
            display_name="Stack Overflow",
            tier=2,
            emoji="\U0001f4cb",
            id_prefix="SO",
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

        url = (
            f"https://api.stackexchange.com/2.3/search/advanced"
            f"?order=desc"
            f"&sort=relevance"
            f"&q={quote_plus(core)}"
            f"&site=stackoverflow"
            f"&pagesize={min(dc['max_results'], 20)}"
            f"&filter=withbody"
        )

        # Add API key for higher rate limits if available
        so_key = config.get("SO_API_KEY", "")
        if so_key:
            url += f"&key={quote_plus(so_key)}"

        try:
            data = http.get(url, timeout=dc["timeout"])
        except http.HTTPError:
            return []

        questions = data.get("items", [])
        items = []
        for q in questions:
            title = q.get("title", "")
            if not title:
                continue

            item_url = q.get("link", "")
            question_id = q.get("question_id", "")

            # Parse date from creation_date (unix timestamp)
            item_date = None
            creation_date = q.get("creation_date")
            if creation_date:
                item_date = dates.timestamp_to_date(float(creation_date))

            # Extract snippet from body (strip HTML)
            body = q.get("body", "")
            if body:
                import re
                snippet = re.sub(r"<[^>]+>", "", body)[:300]
            else:
                snippet = ""

            owner = q.get("owner", {})
            author = owner.get("display_name", "") if isinstance(owner, dict) else ""

            tags = q.get("tags", [])
            relevance = query.compute_relevance(topic, f"{title} {' '.join(tags)}")

            items.append({
                "title": title,
                "url": item_url,
                "date": item_date,
                "relevance": relevance,
                "engagement": {
                    "score": q.get("score", 0),
                    "num_comments": q.get("answer_count", 0),
                    "views": q.get("view_count", 0),
                },
                "author": author,
                "snippet": snippet,
                "source_id": str(question_id),
                "tags": tags,
            })

        return items


def get_source():
    return StackOverflowSource()
