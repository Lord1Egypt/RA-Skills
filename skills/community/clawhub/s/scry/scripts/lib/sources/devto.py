"""Dev.to source for SCRY skill."""

from ..source_base import Source, SourceMeta
from .. import http, query, dates
from typing import Any, Dict, List
from urllib.parse import quote_plus


# Common tags that map from topic keywords
TAG_MAP = {
    "python": "python",
    "javascript": "javascript",
    "typescript": "typescript",
    "react": "react",
    "vue": "vue",
    "angular": "angular",
    "rust": "rust",
    "go": "go",
    "golang": "go",
    "node": "node",
    "nodejs": "node",
    "docker": "docker",
    "kubernetes": "kubernetes",
    "k8s": "kubernetes",
    "aws": "aws",
    "ai": "ai",
    "ml": "machinelearning",
    "machine learning": "machinelearning",
    "deep learning": "deeplearning",
    "llm": "llm",
    "chatgpt": "chatgpt",
    "openai": "openai",
    "webdev": "webdev",
    "devops": "devops",
    "css": "css",
    "html": "html",
    "java": "java",
    "swift": "swift",
    "ruby": "ruby",
    "rails": "rails",
    "django": "django",
    "flask": "flask",
    "nextjs": "nextjs",
    "svelte": "svelte",
}


class DevtoSource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="devto",
            display_name="Dev.to",
            tier=1,
            emoji="\U0001f4dd",
            id_prefix="DV",
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

        # Try to find a matching tag
        tag = None
        for kw in keywords:
            kw_lower = kw.lower()
            if kw_lower in TAG_MAP:
                tag = TAG_MAP[kw_lower]
                break

        # Build URL
        url = f"https://dev.to/api/articles?per_page={dc['max_results']}&top=30"
        if tag:
            url += f"&tag={quote_plus(tag)}"

        try:
            articles = http.get(url, timeout=dc["timeout"])
        except http.HTTPError:
            return []

        if not isinstance(articles, list):
            return []

        items = []
        for article in articles:
            title = article.get("title", "")
            if not title:
                continue

            article_url = article.get("url", "")
            description = article.get("description", "")

            relevance = query.compute_relevance(topic, f"{title} {description}")

            # If no tag was used, filter by minimum relevance
            if not tag and relevance < 0.1:
                continue

            item_date = None
            published = article.get("published_at", "")
            if published:
                dt = dates.parse_date(published)
                if dt:
                    item_date = dt.date().isoformat()

            items.append({
                "title": title,
                "url": article_url,
                "date": item_date,
                "relevance": max(relevance, 0.2) if tag else relevance,
                "engagement": {
                    "score": article.get("positive_reactions_count", 0),
                    "num_comments": article.get("comments_count", 0),
                },
                "author": article.get("user", {}).get("username", "") if isinstance(article.get("user"), dict) else "",
                "snippet": description[:300] if description else "",
                "tags": article.get("tag_list", []),
            })

        items.sort(key=lambda x: x["relevance"], reverse=True)
        return items[:dc["max_results"]]


def get_source():
    return DevtoSource()
