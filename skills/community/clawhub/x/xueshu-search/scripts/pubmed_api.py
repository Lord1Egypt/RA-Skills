#!/usr/bin/env python3
"""
PubMed E-utilities API wrapper.
Docs: https://www.ncbi.nlm.nih.gov/books/NBK25501/
Rate limit: 3 req/sec without API key, 10 req/sec with API key.
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import time
from typing import Optional

ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
ESUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def _esearch(query: str, max_results: int = 10, year_from: Optional[int] = None,
             year_to: Optional[int] = None) -> list[str]:
    """Search PubMed and return PMID list."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": str(min(max_results, 100)),
        "retmode": "xml",
        "sort": "relevance",
    }

    if year_from or year_to:
        params["mindate"] = str(year_from) if year_from else "1800"
        params["maxdate"] = str(year_to) if year_to else "3000"
        params["datetype"] = "pdat"

    url = f"{ESEARCH}?{urllib.parse.urlencode(params)}"
    time.sleep(0.4)

    req = urllib.request.Request(url, headers={"User-Agent": "LiteratureSearchSkill/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read().decode("utf-8")

    root = ET.fromstring(data)
    id_list = root.find(".//IdList")
    if id_list is None:
        return []
    return [id_elem.text for id_elem in id_list.findall("Id") if id_elem.text]


def _esummary(pmids: list[str]) -> list[dict]:
    """Fetch summaries for a list of PMIDs."""
    if not pmids:
        return []

    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml",
    }
    url = f"{ESUMMARY}?{urllib.parse.urlencode(params)}"
    time.sleep(0.4)

    req = urllib.request.Request(url, headers={"User-Agent": "LiteratureSearchSkill/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read().decode("utf-8")

    root = ET.fromstring(data)
    results = []
    for doc_sum in root.findall(".//DocSum"):
        pmid = doc_sum.findtext("Id", "")
        item_dict = {}
        for item in doc_sum.findall("Item"):
            name = item.get("Name", "")
            text = item.text or ""
            item_dict[name] = text

        authors_raw = []
        for item in doc_sum.findall("Item[@Name='AuthorList']/Item"):
            author_name = item.text or ""
            if author_name:
                authors_raw.append(author_name)

        results.append({
            "source": "pubmed",
            "id": pmid,
            "title": item_dict.get("Title", ""),
            "authors": [{"name": a} for a in authors_raw],
            "abstract": "",
            "published": item_dict.get("PubDate", ""),
            "year": int(item_dict.get("PubDate", "0")[:4]) if item_dict.get("PubDate") else None,
            "doi": item_dict.get("DOI", "").replace("https://doi.org/", ""),
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            "pdf_url": "",
            "citation_count": None,
            "source_journal": item_dict.get("Source", ""),
            "pub_types": item_dict.get("PubTypeList", "").split(";") if item_dict.get("PubTypeList") else [],
        })
    return results


def search(
    query: str,
    max_results: int = 10,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    fetch_abstracts: bool = False,
) -> list[dict]:
    """Search PubMed for biomedical papers.

    Args:
        query: Search query (supports PubMed query syntax, MeSH terms, field tags like [tiab]).
        max_results: Max results to return.
        year_from: Earliest publication year.
        year_to: Latest publication year.
        fetch_abstracts: Whether to also fetch abstracts (adds extra API call).

    Returns:
        List of paper dicts.
    """
    pmids = _esearch(query, max_results, year_from, year_to)
    if not pmids:
        return []

    results = _esummary(pmids)
    return results


def get_paper(pmid: str) -> Optional[dict]:
    """Get a single paper by PMID."""
    results = _esummary([pmid])
    return results[0] if results else None


def search_mesh(term: str) -> list[str]:
    """Simple helper: build a MeSH-tagged query term."""
    return [f"{term}[MeSH Terms]", f"{term}[tiab]"]
