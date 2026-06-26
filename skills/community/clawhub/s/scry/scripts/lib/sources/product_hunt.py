"""Product Hunt source for SCRY skill."""

from ..source_base import Source, SourceMeta
from .. import http, query, dates
from typing import Any, Dict, List


GRAPHQL_QUERY = """\
{
  posts(order: RANKING, first: 20) {
    edges {
      node {
        name
        tagline
        url
        votesCount
        commentsCount
        createdAt
      }
    }
  }
}
"""


class ProductHuntSource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="product_hunt",
            display_name="Product Hunt",
            tier=2,
            emoji="\U0001f680",
            id_prefix="PH",
            has_engagement=True,
            requires_keys=["PRODUCTHUNT_TOKEN"],
            requires_bins=[],
            domains=["general"],
        )

    def is_available(self, config):
        return bool(config.get("PRODUCTHUNT_TOKEN"))

    def search(self, topic, from_date, to_date, depth, config):
        dc = self.depth_config(depth)
        core = query.extract_core_subject(topic)

        token = config.get("PRODUCTHUNT_TOKEN", "")
        url = "https://api.producthunt.com/v2/api/graphql"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        try:
            data = http.post(
                url,
                json_data={"query": GRAPHQL_QUERY},
                headers=headers,
                timeout=dc["timeout"],
            )
        except http.HTTPError:
            return []

        edges = (
            data.get("data", {})
            .get("posts", {})
            .get("edges", [])
        )

        items = []
        for edge in edges:
            node = edge.get("node", {})
            name = node.get("name", "")
            tagline = node.get("tagline", "")
            if not name:
                continue

            item_url = node.get("url", "")

            # Parse date
            item_date = None
            created_at = node.get("createdAt", "")
            if created_at:
                dt = dates.parse_date(created_at)
                if dt:
                    item_date = dt.date().isoformat()

            relevance = query.compute_relevance(topic, f"{name} {tagline}")

            items.append({
                "title": name,
                "url": item_url,
                "date": item_date,
                "relevance": relevance,
                "engagement": {
                    "score": node.get("votesCount", 0),
                    "num_comments": node.get("commentsCount", 0),
                },
                "author": "",
                "snippet": tagline[:300] if tagline else "",
            })

        # Sort by relevance to topic since GraphQL query doesn't filter by topic
        items.sort(key=lambda x: x["relevance"], reverse=True)
        return items[:dc["max_results"]]


def get_source():
    return ProductHuntSource()
