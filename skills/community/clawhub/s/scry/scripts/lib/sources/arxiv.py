"""ArXiv source for SCRY skill."""

import xml.etree.ElementTree as ET
from ..source_base import Source, SourceMeta
from .. import http, query, dates
from typing import Any, Dict, List
from urllib.parse import quote_plus


# Atom namespace
ATOM_NS = "{http://www.w3.org/2005/Atom}"


class ArxivSource(Source):
    def meta(self) -> SourceMeta:
        return SourceMeta(
            id="arxiv",
            display_name="ArXiv",
            tier=1,
            emoji="\U0001f4c4",
            id_prefix="AX",
            has_engagement=False,
            requires_keys=[],
            requires_bins=[],
            domains=["science", "academic"],
        )

    def is_available(self, config):
        return True

    def search(self, topic, from_date, to_date, depth, config):
        dc = self.depth_config(depth)
        core = query.extract_core_subject(topic)

        # Use relevance sort to get actually relevant papers, not just recent ones
        url = (
            f"http://export.arxiv.org/api/query"
            f"?search_query=all:{quote_plus(core)}"
            f"&sortBy=relevance"
            f"&sortOrder=descending"
            f"&max_results={dc['max_results'] + 10}"  # Fetch extra to filter
        )

        try:
            xml_text = http.get(url, timeout=dc["timeout"], raw=True)
        except http.HTTPError:
            return []

        return self._parse_atom_feed(xml_text, topic)

    def _parse_atom_feed(self, xml_text, topic):
        """Parse Atom XML response from ArXiv API."""
        items = []

        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError:
            return []

        for entry in root.findall(f"{ATOM_NS}entry"):
            title_elem = entry.find(f"{ATOM_NS}title")
            title = title_elem.text.strip().replace("\n", " ") if title_elem is not None and title_elem.text else ""

            if not title:
                continue

            # Get the abstract/summary
            summary_elem = entry.find(f"{ATOM_NS}summary")
            summary = summary_elem.text.strip().replace("\n", " ") if summary_elem is not None and summary_elem.text else ""

            # Get the link (prefer the abstract page link)
            url = ""
            for link in entry.findall(f"{ATOM_NS}link"):
                href = link.get("href", "")
                link_type = link.get("type", "")
                rel = link.get("rel", "")
                if rel == "alternate" or (not url and href):
                    url = href

            # Get the published date
            item_date = None
            published_elem = entry.find(f"{ATOM_NS}published")
            if published_elem is not None and published_elem.text:
                dt = dates.parse_date(published_elem.text.strip())
                if dt:
                    item_date = dt.date().isoformat()

            # Get authors
            authors = []
            for author_elem in entry.findall(f"{ATOM_NS}author"):
                name_elem = author_elem.find(f"{ATOM_NS}name")
                if name_elem is not None and name_elem.text:
                    authors.append(name_elem.text.strip())

            # Get categories
            categories = []
            for cat_elem in entry.findall(f"{ATOM_NS}category"):
                term = cat_elem.get("term", "")
                if term:
                    categories.append(term)

            items.append({
                "title": title,
                "url": url,
                "date": item_date,
                "relevance": query.compute_relevance(topic, f"{title} {summary}"),
                "engagement": None,
                "author": ", ".join(authors[:3]) + ("..." if len(authors) > 3 else ""),
                "snippet": summary[:400] if summary else "",
                "categories": categories,
            })

        return items

    def enrich(self, items, depth, config):
        """Try to fetch citation counts from Semantic Scholar for top items."""
        if depth == "quick":
            return items

        dc = self.depth_config(depth)

        for item in items[:5]:
            arxiv_url = item.get("url", "")
            if not arxiv_url:
                continue

            # Extract arxiv ID from URL
            arxiv_id = ""
            if "/abs/" in arxiv_url:
                arxiv_id = arxiv_url.split("/abs/")[-1]
            elif "/pdf/" in arxiv_url:
                arxiv_id = arxiv_url.split("/pdf/")[-1].replace(".pdf", "")

            if not arxiv_id:
                continue

            ss_url = f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}?fields=citationCount"
            try:
                data = http.get(ss_url, timeout=dc["timeout"])
                citation_count = data.get("citationCount", 0)
                if citation_count:
                    item["engagement"] = {"citations": citation_count}
            except http.HTTPError:
                continue

        return items


def get_source():
    return ArxivSource()
