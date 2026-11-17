#!/usr/bin/env python3
"""Crossref + PubMed literature search (stdlib only, no backend)."""
from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

TIMEOUT = 12
CROSSREF_BASE = "https://api.crossref.org/works"
PUBMED_SEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_SUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"


def crossref_mailto() -> str:
    return os.environ.get("CROSSREF_MAILTO", "smart-research@openclaw.local").strip()


def _fetch_json(url: str, headers: dict | None = None) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "application/json", **(headers or {})})
    req.add_header("User-Agent", f"SmartResearch/1.0 (mailto:{crossref_mailto()})")
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode())


def _fetch_text(url: str) -> str:
    req = urllib.request.Request(url)
    req.add_header("User-Agent", f"SmartResearch/1.0 (mailto:{crossref_mailto()})")
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read().decode()


def _strip_jats(html: str | None) -> str | None:
    if not html:
        return None
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


def search_crossref(query: str, limit: int = 8) -> list[dict]:
    params = urllib.parse.urlencode(
        {
            "query": query,
            "rows": str(limit),
            "select": "DOI,title,author,published,abstract,URL,container-title",
        }
    )
    url = f"{CROSSREF_BASE}?{params}"
    try:
        data = _fetch_json(url)
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError):
        return []
    items = data.get("message", {}).get("items") or []
    papers = []
    for idx, item in enumerate(items):
        doi = item.get("DOI")
        authors = [
            " ".join(p for p in [a.get("given"), a.get("family")] if p)
            for a in item.get("author") or []
        ]
        authors = [a for a in authors if a]
        year = (item.get("published") or {}).get("date-parts", [[None]])[0][0]
        papers.append(
            {
                "id": f"crossref:{doi}" if doi else f"crossref:idx-{idx}",
                "title": (item.get("title") or ["Untitled"])[0],
                "authors": authors,
                "year": year,
                "doi": doi,
                "abstract": _strip_jats(item.get("abstract")),
                "url": item.get("URL") or (f"https://doi.org/{doi}" if doi else None),
                "source": "crossref",
                "journal": (item.get("container-title") or [None])[0],
            }
        )
    return papers


def search_pubmed(query: str, limit: int = 8) -> list[dict]:
    search_params = urllib.parse.urlencode(
        {"db": "pubmed", "term": query, "retmax": str(limit), "retmode": "json"}
    )
    try:
        search_data = json.loads(_fetch_text(f"{PUBMED_SEARCH}?{search_params}"))
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError):
        return []
    ids = (search_data.get("esearchresult") or {}).get("idlist") or []
    if not ids:
        return []
    summary_params = urllib.parse.urlencode({"db": "pubmed", "id": ",".join(ids), "retmode": "json"})
    try:
        summary_data = json.loads(_fetch_text(f"{PUBMED_SUMMARY}?{summary_params}"))
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError):
        return []
    result = summary_data.get("result") or {}
    papers = []
    for pmid in ids:
        item = result.get(pmid)
        if not item:
            continue
        pubdate = item.get("pubdate") or ""
        year_match = re.search(r"\d{4}", pubdate)
        doi_match = re.search(r"doi:\s*(.+)", item.get("elocationid") or "", re.I)
        papers.append(
            {
                "id": f"pubmed:{pmid}",
                "title": item.get("title") or "Untitled",
                "authors": [a.get("name", "") for a in item.get("authors") or [] if a.get("name")],
                "year": int(year_match.group()) if year_match else None,
                "doi": doi_match.group(1).strip() if doi_match else None,
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                "source": "pubmed",
                "journal": item.get("source"),
            }
        )
    return papers


def _dedupe_key(paper: dict) -> str:
    doi = paper.get("doi")
    if doi:
        return f"doi:{doi.lower()}"
    return f"title:{paper.get('title', '').lower()[:80]}"


def _score(paper: dict, query: str) -> int:
    q = query.lower()
    title = paper.get("title", "").lower()
    score = 0
    if q in title:
        score += 10
    for token in [t for t in q.split() if len(t) > 2]:
        if token in title:
            score += 2
        abstract = (paper.get("abstract") or "").lower()
        if token in abstract:
            score += 1
    year = paper.get("year")
    if year and year >= __import__("datetime").date.today().year - 5:
        score += 1
    return score


def search_literature(query: str, limit: int = 10) -> list[dict]:
    trimmed = query.strip()
    if not trimmed:
        return []
    per_source = max(limit, 8)
    merged: list[dict] = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = {
            pool.submit(search_crossref, trimmed, per_source): "crossref",
            pool.submit(search_pubmed, trimmed, per_source): "pubmed",
        }
        for fut in as_completed(futures):
            try:
                merged.extend(fut.result())
            except Exception:
                pass
    seen: set[str] = set()
    unique: list[dict] = []
    for paper in merged:
        key = _dedupe_key(paper)
        if key in seen:
            continue
        seen.add(key)
        unique.append(paper)
    ranked = sorted(unique, key=lambda p: _score(p, trimmed), reverse=True)
    return ranked[:limit]
