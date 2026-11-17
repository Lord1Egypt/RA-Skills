#!/usr/bin/env python3
"""
CrossRef API wrapper.
Docs: https://api.crossref.org/swagger-ui/index.html
Rate limit: polite usage, no hard limit without API key.
"""

import urllib.request
import urllib.parse
import json
import time
from typing import Optional

CROSSREF_API = "https://api.crossref.org"


def _make_request(url: str) -> dict:
    time.sleep(0.3)
    req = urllib.request.Request(url, headers={"User-Agent": "LiteratureSearchSkill/1.0 (mailto:user@example.com)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": str(e.code), "message": e.reason}


def _parse_work(item: dict) -> dict:
    title_list = item.get("title", []) or []
    title = title_list[0] if title_list else ""

    authors = []
    for a in item.get("author", []) or []:
        given = a.get("given", "")
        family = a.get("family", "")
        authors.append({"name": f"{given} {family}".strip(), "orcid": a.get("ORCID", "")})

    published = ""
    pub_parts = item.get("published", {}) or {}
    date_parts = pub_parts.get("date-parts", [[None]]) or [[None]]
    if date_parts and date_parts[0]:
        parts = date_parts[0]
        published = "-".join(str(p) for p in parts if p is not None)

    year = date_parts[0][0] if date_parts and date_parts[0] and date_parts[0][0] else None

    doi = item.get("DOI", "")
    container = (item.get("container-title", []) or [""])[0]

    url_link = ""
    for link in item.get("link", []) or []:
        if link.get("content-type") == "text/html" or link.get("URL"):
            url_link = link.get("URL", "")
            break

    return {
        "source": "crossref",
        "id": doi,
        "title": title,
        "authors": authors,
        "abstract": item.get("abstract", ""),
        "published": published,
        "year": year,
        "doi": doi,
        "url": url_link or f"https://doi.org/{doi}" if doi else "",
        "pdf_url": "",
        "citation_count": item.get("is-referenced-by-count"),
        "container": container,
        "publisher": item.get("publisher", ""),
        "type": item.get("type", ""),
    }


def get_by_doi(doi: str) -> Optional[dict]:
    """Get paper metadata by DOI."""
    url = f"{CROSSREF_API}/works/{urllib.parse.quote(doi)}"
    data = _make_request(url)
    if "error" in data:
        return None
    msg = data.get("message", {})
    if not msg:
        return None
    return _parse_work(msg)


def search(
    query: str,
    max_results: int = 10,
    offset: int = 0,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    filter_type: Optional[str] = None,
) -> list[dict]:
    """Search CrossRef for scholarly works.

    Args:
        query: Search query string.
        max_results: Max results (default 10, max 100).
        offset: Result offset.
        year_from: Filter from year.
        year_to: Filter to year.
        filter_type: Filter by type (e.g. 'journal-article', 'book', 'proceedings-article').

    Returns:
        List of paper dicts.
    """
    params = {
        "query": query,
        "rows": str(min(max_results, 100)),
        "offset": str(offset),
    }

    filters = []
    if year_from and year_to:
        filters.append(f"from-pub-date:{year_from},until-pub-date:{year_to}")
    elif year_from:
        filters.append(f"from-pub-date:{year_from}")
    if filter_type:
        filters.append(f"type:{filter_type}")
    if filters:
        params["filter"] = ",".join(filters)

    url = f"{CROSSREF_API}/works?{urllib.parse.urlencode(params)}"
    data = _make_request(url)
    if "error" in data:
        return []

    items = data.get("message", {}).get("items", [])
    return [_parse_work(item) for item in items]


def get_bibtex(doi: str) -> Optional[str]:
    """Get BibTeX citation for a DOI."""
    url = f"{CROSSREF_API}/works/{urllib.parse.quote(doi)}/transform/application/x-bibtex"
    req = urllib.request.Request(url, headers={"Accept": "application/x-bibtex"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8")
    except Exception:
        return None
