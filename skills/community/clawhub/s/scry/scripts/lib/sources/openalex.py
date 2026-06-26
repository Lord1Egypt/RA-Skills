"""OpenAlex source for SCRY skill."""

from ..source_base import Source, SourceMeta
from .. import http, query, dates
from typing import Any, Dict, List
from urllib.parse import quote_plus


class OpenAlexSource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="openalex",
            display_name="OpenAlex",
            tier=1,
            emoji="\U0001f4da",
            id_prefix="OA",
            has_engagement=True,
            requires_keys=[],
            requires_bins=[],
            domains=["science", "academic"],
        )

    def is_available(self, config):
        return True

    def search(self, topic, from_date, to_date, depth, config):
        dc = self.depth_config(depth)
        core = query.extract_core_subject(topic)

        url = (
            f"https://api.openalex.org/works"
            f"?search={quote_plus(core)}"
            f"&sort=cited_by_count:desc"
            f"&per_page={dc['max_results']}"
            f"&filter=from_publication_date:{from_date}"
            f"&mailto=scry-skill@example.com"
        )

        try:
            data = http.get(url, timeout=dc["timeout"])
        except http.HTTPError:
            return []

        results = data.get("results", [])
        if not isinstance(results, list):
            return []

        items = []
        for work in results:
            title = work.get("title", "") or work.get("display_name", "")
            if not title:
                continue

            work_url = work.get("doi", "") or work.get("id", "")
            if work_url and work_url.startswith("https://doi.org/"):
                pass  # already a full URL
            elif work_url and not work_url.startswith("http"):
                work_url = f"https://openalex.org/works/{work_url}"

            # Get open access URL if available
            oa = work.get("open_access", {})
            oa_url = ""
            if isinstance(oa, dict):
                oa_url = oa.get("oa_url", "") or ""

            # Parse publication date
            item_date = None
            pub_date = work.get("publication_date", "")
            if pub_date:
                dt = dates.parse_date(pub_date)
                if dt:
                    item_date = dt.date().isoformat()

            # Extract authors
            authorships = work.get("authorships", [])
            authors = []
            if isinstance(authorships, list):
                for authorship in authorships[:3]:
                    author_info = authorship.get("author", {})
                    if isinstance(author_info, dict):
                        name = author_info.get("display_name", "")
                        if name:
                            authors.append(name)

            author_str = ", ".join(authors)
            if len(authorships) > 3:
                author_str += "..."

            # Abstract can be in abstract_inverted_index
            snippet = ""
            abstract_index = work.get("abstract_inverted_index")
            if isinstance(abstract_index, dict):
                snippet = self._reconstruct_abstract(abstract_index)[:400]

            items.append({
                "title": title,
                "url": oa_url or work_url,
                "date": item_date,
                "relevance": query.compute_relevance(topic, f"{title} {snippet}"),
                "engagement": {
                    "citations": work.get("cited_by_count", 0),
                },
                "author": author_str,
                "snippet": snippet,
            })

        items.sort(key=lambda x: x["relevance"], reverse=True)
        return items[:dc["max_results"]]

    @staticmethod
    def _reconstruct_abstract(inverted_index):
        """Reconstruct abstract text from OpenAlex inverted index format."""
        if not inverted_index:
            return ""

        # inverted_index is {word: [position, ...], ...}
        word_positions = []
        for word, positions in inverted_index.items():
            if isinstance(positions, list):
                for pos in positions:
                    word_positions.append((pos, word))

        word_positions.sort(key=lambda x: x[0])
        return " ".join(word for _, word in word_positions)


def get_source():
    return OpenAlexSource()
