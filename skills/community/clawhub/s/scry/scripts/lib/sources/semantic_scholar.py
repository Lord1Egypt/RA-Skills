"""Semantic Scholar source for SCRY skill."""

from ..source_base import Source, SourceMeta
from .. import http, query, dates
from typing import Any, Dict, List
from urllib.parse import quote_plus


class SemanticScholarSource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="semantic_scholar",
            display_name="Semantic Scholar",
            tier=1,
            emoji="\U0001f393",
            id_prefix="SS",
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
            f"https://api.semanticscholar.org/graph/v1/paper/search"
            f"?query={quote_plus(core)}"
            f"&fields=title,url,year,citationCount,openAccessPdf,abstract"
            f"&limit={min(dc['max_results'], 100)}"
        )

        try:
            data = http.get(url, timeout=dc["timeout"])
        except http.HTTPError:
            return []

        papers = data.get("data", [])
        if not isinstance(papers, list):
            return []

        items = []
        for paper in papers:
            title = paper.get("title", "")
            if not title:
                continue

            paper_url = paper.get("url", "")
            if not paper_url:
                paper_id = paper.get("paperId", "")
                if paper_id:
                    paper_url = f"https://www.semanticscholar.org/paper/{paper_id}"

            # Try to get open access PDF URL
            oa_pdf = paper.get("openAccessPdf")
            pdf_url = oa_pdf.get("url", "") if isinstance(oa_pdf, dict) else ""

            abstract = paper.get("abstract", "") or ""

            # Build date from year
            item_date = None
            year = paper.get("year")
            if year:
                item_date = f"{year}-01-01"

            items.append({
                "title": title,
                "url": paper_url,
                "date": item_date,
                "relevance": query.compute_relevance(topic, f"{title} {abstract}"),
                "engagement": {
                    "citations": paper.get("citationCount", 0),
                },
                "author": "",
                "snippet": abstract[:400] if abstract else "",
                "pdf_url": pdf_url,
            })

        items.sort(key=lambda x: x["relevance"], reverse=True)
        return items[:dc["max_results"]]


def get_source():
    return SemanticScholarSource()
