#!/usr/bin/env python3
"""
arXiv API wrapper.
Docs: https://info.arxiv.org/help/api/user-manual.html
Rate limit: no hard limit, but be polite (>3s between requests).
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import time
from typing import Optional

ARXIV_API = "http://export.arxiv.org/api/query"
ARXIV_NS = "{http://www.w3.org/2005/Atom}"


def _safe_text(el, tag):
    child = el.find(tag)
    return child.text.strip() if child is not None and child.text else ""


def _parse_author(author_el):
    name = _safe_text(author_el, f"{ARXIV_NS}name")
    return {"name": name}


def _parse_entry(entry):
    title = _safe_text(entry, f"{ARXIV_NS}title").replace("\n", " ").strip()
    summary = _safe_text(entry, f"{ARXIV_NS}summary").replace("\n", " ").strip()
    arxiv_id_full = _safe_text(entry, f"{ARXIV_NS}id")
    arxiv_id = arxiv_id_full.split("/abs/")[-1] if "/abs/" in arxiv_id_full else arxiv_id_full
    published = _safe_text(entry, f"{ARXIV_NS}published")
    updated = _safe_text(entry, f"{ARXIV_NS}updated")
    doi_el = entry.find(f"{ARXIV_NS}link[@title='doi']")
    doi = doi_el.get("href", "").replace("https://doi.org/", "") if doi_el is not None else ""

    authors = [_parse_author(a) for a in entry.findall(f"{ARXIV_NS}author")]

    categories = [c.get("term", "") for c in entry.findall(f"{ARXIV_NS}category")]

    links = [l.get("href", "") for l in entry.findall(f"{ARXIV_NS}link")]

    return {
        "source": "arxiv",
        "id": arxiv_id,
        "title": title,
        "authors": authors,
        "abstract": summary,
        "published": published,
        "updated": updated,
        "doi": doi,
        "categories": categories,
        "url": arxiv_id_full,
        "pdf_url": next((l for l in links if l.endswith(".pdf")), ""),
        "citation_count": None,
    }


def search(
    query: str,
    max_results: int = 10,
    start: int = 0,
    sort_by: str = "relevance",
    sort_order: str = "descending",
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
) -> list[dict]:
    """Search arXiv for papers.

    Args:
        query: Search query string (supports arXiv query syntax).
        max_results: Max results to return (default 10, max ~100).
        start: Offset for pagination.
        sort_by: 'relevance', 'lastUpdatedDate', or 'submittedDate'.
        sort_order: 'ascending' or 'descending'.
        year_from: Filter by earliest publication year (optional).
        year_to: Filter by latest publication year (optional).

    Returns:
        List of paper dicts with keys: source, id, title, authors, abstract,
        published, updated, doi, categories, url, pdf_url, citation_count.
    """
    params = {
        "search_query": query,
        "start": str(start),
        "max_results": str(min(max_results, 100)),
        "sortBy": sort_by,
        "sortOrder": sort_order,
    }
    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
    time.sleep(0.5)

    req = urllib.request.Request(url, headers={"User-Agent": "LiteratureSearchSkill/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read().decode("utf-8")

    root = ET.fromstring(data)
    entries = root.findall(f"{ARXIV_NS}entry")
    results = [_parse_entry(e) for e in entries]

    if year_from:
        results = [r for r in results if r["published"] and int(r["published"][:4]) >= year_from]
    if year_to:
        results = [r for r in results if r["published"] and int(r["published"][:4]) <= year_to]

    return results


def get_paper(arxiv_id: str) -> Optional[dict]:
    """Get a single paper by arXiv ID."""
    results = search(f"id:{arxiv_id}", max_results=1)
    return results[0] if results else None
