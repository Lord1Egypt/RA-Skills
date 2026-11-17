#!/usr/bin/env python3
"""
Semantic Scholar API wrapper.
Docs: https://api.semanticscholar.org/api-docs/graph
Rate limit: 100 requests per 5 minutes without API key.
With API key (free): higher rate limits. Get one at:
  https://www.semanticscholar.org/product/api#api-key-form
Set via env var: SEMANTIC_SCHOLAR_API_KEY
"""

import os
import urllib.request
import urllib.parse
import json
import time
from typing import Optional

S2_API = "https://api.semanticscholar.org/graph/v1"
FIELDS = "title,authors,abstract,year,publicationDate,externalIds,citationCount,url,openAccessPdf,journal,publicationVenue"
API_KEY = os.environ.get("SEMANTIC_SCHOLAR_API_KEY", "")

if API_KEY:
    S2_HEADERS = {"User-Agent": "LiteratureSearchSkill/1.0", "x-api-key": API_KEY}
else:
    S2_HEADERS = {"User-Agent": "LiteratureSearchSkill/1.0"}


def _make_request(url: str, retries: int = 3) -> dict:
    for attempt in range(retries):
        if attempt > 0:
            wait = 3 * (2 ** attempt)
            time.sleep(wait)
        else:
            time.sleep(1.0)
        req = urllib.request.Request(url, headers=S2_HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                if not API_KEY:
                    return {
                        "error": "429",
                        "message": (
                            "Rate limited. For reliable access, get a free API key at "
                            "https://www.semanticscholar.org/product/api#api-key-form "
                            "and set env var SEMANTIC_SCHOLAR_API_KEY."
                        ),
                    }
                if attempt < retries - 1:
                    continue
            return {"error": str(e.code), "message": e.reason}
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
                continue
            return {"error": "exception", "message": str(e)}
    return {"error": "max_retries", "message": "All retries exhausted"}


def _parse_paper(paper: dict) -> dict:
    authors = [{"name": a.get("name", ""), "authorId": a.get("authorId", "")}
               for a in paper.get("authors", [])]
    ext_ids = paper.get("externalIds", {}) or {}
    open_access = paper.get("openAccessPdf", {}) or {}
    venue = paper.get("publicationVenue") or paper.get("journal") or {}

    return {
        "source": "semantic_scholar",
        "id": paper.get("paperId", ""),
        "title": paper.get("title", ""),
        "authors": authors,
        "abstract": paper.get("abstract", ""),
        "year": paper.get("year"),
        "published": paper.get("publicationDate", ""),
        "doi": ext_ids.get("DOI", ""),
        "arxiv_id": ext_ids.get("ArXiv", ""),
        "url": paper.get("url", ""),
        "pdf_url": open_access.get("url", ""),
        "citation_count": paper.get("citationCount"),
        "venue": venue.get("name", "") if isinstance(venue, dict) else "",
        "journal": paper.get("journal", {}).get("name", "") if isinstance(paper.get("journal"), dict) else "",
    }


def search(
    query: str,
    max_results: int = 10,
    offset: int = 0,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    fields_of_study: Optional[list[str]] = None,
) -> list[dict]:
    """Search Semantic Scholar for papers.

    Args:
        query: Search query (supports boolean operators +, -, AND, OR).
        max_results: Max results to return (default 10, max 100).
        offset: Offset for pagination.
        year_from: Earliest publication year filter.
        year_to: Latest publication year filter.
        fields_of_study: Filter by fields like ['Computer Science', 'Medicine'].

    Returns:
        List of paper dicts.
    """
    params = {
        "query": query,
        "limit": str(min(max_results, 100)),
        "offset": str(offset),
        "fields": FIELDS,
    }
    if year_from and year_to:
        params["year"] = f"{year_from}-{year_to}"
    elif year_from:
        params["year"] = f"{year_from}-"
    elif year_to:
        params["year"] = f"-{year_to}"

    url = f"{S2_API}/paper/search?{urllib.parse.urlencode(params)}"
    data = _make_request(url)
    if "error" in data:
        return []

    results = []
    for paper in data.get("data", []):
        parsed = _parse_paper(paper)
        if fields_of_study:
            pass
        results.append(parsed)
    return results


def get_citations(paper_id: str, max_results: int = 20, offset: int = 0) -> list[dict]:
    """Get papers that cite the given paper."""
    params = {
        "limit": str(min(max_results, 100)),
        "offset": str(offset),
        "fields": FIELDS,
    }
    url = f"{S2_API}/paper/{paper_id}/citations?{urllib.parse.urlencode(params)}"
    data = _make_request(url)
    if "error" in data:
        return []
    return [_parse_paper(c.get("citingPaper", {})) for c in data.get("data", []) if c.get("citingPaper")]


def get_references(paper_id: str, max_results: int = 20, offset: int = 0) -> list[dict]:
    """Get papers referenced by the given paper."""
    params = {
        "limit": str(min(max_results, 100)),
        "offset": str(offset),
        "fields": FIELDS,
    }
    url = f"{S2_API}/paper/{paper_id}/references?{urllib.parse.urlencode(params)}"
    data = _make_request(url)
    if "error" in data:
        return []
    return [_parse_paper(r.get("citedPaper", {})) for r in data.get("data", []) if r.get("citedPaper")]


def get_paper(paper_id: str) -> Optional[dict]:
    """Get a single paper by Semantic Scholar paper ID or DOI."""
    identifier = paper_id
    if paper_id.startswith("10."):
        identifier = f"DOI:{paper_id}"
    elif paper_id.startswith("arxiv:"):
        identifier = f"ArXiv:{paper_id[6:]}"

    params = {"fields": FIELDS}
    url = f"{S2_API}/paper/{urllib.parse.quote(identifier)}?{urllib.parse.urlencode(params)}"
    data = _make_request(url)
    if "error" in data:
        return None
    return _parse_paper(data)


def search_author(author_name: str, max_results: int = 10) -> list[dict]:
    """Search for authors by name."""
    params = {"query": author_name, "limit": str(min(max_results, 100))}
    url = f"{S2_API}/author/search?{urllib.parse.urlencode(params)}"
    data = _make_request(url)
    if "error" in data:
        return []
    return data.get("data", [])


def get_author_papers(author_id: str, max_results: int = 20, offset: int = 0) -> list[dict]:
    """Get papers by a specific author."""
    params = {
        "limit": str(min(max_results, 100)),
        "offset": str(offset),
        "fields": FIELDS,
    }
    url = f"{S2_API}/author/{author_id}/papers?{urllib.parse.urlencode(params)}"
    data = _make_request(url)
    if "error" in data:
        return []
    return [_parse_paper(p) for p in data.get("data", [])]
