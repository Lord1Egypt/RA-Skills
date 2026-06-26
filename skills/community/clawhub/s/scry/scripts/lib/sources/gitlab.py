"""GitLab source for SCRY skill."""

from ..source_base import Source, SourceMeta
from .. import http, query, dates
from typing import Any, Dict, List
from urllib.parse import quote_plus


class GitLabSource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="gitlab",
            display_name="GitLab",
            tier=1,
            emoji="\U0001f98a",
            id_prefix="GL",
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

        per_page = min(dc["max_results"], 100)
        url = (
            f"https://gitlab.com/api/v4/projects"
            f"?search={quote_plus(core)}"
            f"&order_by=last_activity_at"
            f"&sort=desc"
            f"&per_page={per_page}"
        )

        try:
            data = http.get(url, timeout=dc["timeout"])
        except http.HTTPError:
            return []

        if not isinstance(data, list):
            return []

        items = []
        for project in data:
            name = project.get("name", "")
            name_with_ns = project.get("name_with_namespace", name)
            description = project.get("description", "") or ""

            title = name_with_ns if name_with_ns else name
            if not title:
                continue

            item_url = project.get("web_url", "")

            # Parse last_activity_at
            last_activity = project.get("last_activity_at", "")
            item_date = None
            if last_activity:
                dt = dates.parse_date(last_activity)
                if dt:
                    item_date = dt.date().isoformat()

            star_count = project.get("star_count", 0)
            forks_count = project.get("forks_count", 0)

            items.append({
                "title": title,
                "url": item_url,
                "date": item_date,
                "relevance": query.compute_relevance(topic, f"{title} {description}"),
                "engagement": {
                    "stars": star_count,
                    "forks": forks_count,
                },
                "snippet": description[:500],
                "source_id": str(project.get("id", "")),
                "author": project.get("namespace", {}).get("name", "") if isinstance(project.get("namespace"), dict) else "",
            })

        return items


def get_source():
    return GitLabSource()
