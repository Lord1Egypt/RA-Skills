#!/usr/bin/env python3
"""
PubMed Literature Search Script (E-utilities, no API key required)
Uses NCBI E-utilities to search and retrieve literature metadata.

Usage:
  python search_pubmed.py --query "cognitive behavioral therapy" --max 30
  python search_pubmed.py --query "empathy" --max 50 --mindate 2015

No API key required. Rate limit: 3 req/sec (without key).
Set EMAIL env var for NCBI to contact you if there are issues.
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET


PUBMED_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
EMAIL = "yourname@example.com"  # Replace with your email for NCBI courtesy


def _get(url: str, retries: int = 3) -> str:
    """Fetch a URL with retry, return decoded text."""
    req = urllib.request.Request(url, headers={"User-Agent": f"psych-lit-search/1.0 ({EMAIL})"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8")
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(1)


def search_pubmed(
    query: str,
    max_results: int = 30,
    mindate: str = "",
    maxdate: str = "",
    retstart: int = 0,
) -> dict:
    """
    Search PubMed using E-utilities (no API key required).

    Args:
        query: Search query (supports MeSH and full syntax)
        max_results: Max number of results to return
        mindate: Start date (YYYY/YYYY-MM-DD)
        maxdate: End date (YYYY/YYYY-MM-DD)
        retstart: Offset for pagination (0-based)

    Returns:
        dict with 'total', 'hits' list, and metadata
    """
    # Step 1: esearch — get PMID list
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": str(max_results),
        "retstart": str(retstart),
        "sort": "relevance",
        "retmode": "xml",
        "email": EMAIL,
    }
    if mindate:
        search_params["mindate"] = mindate
    if maxdate:
        search_params["maxdate"] = maxdate

    search_url = f"{PUBMED_BASE}/esearch.fcgi?{urllib.parse.urlencode(search_params)}"
    try:
        search_xml = _get(search_url)
    except Exception as e:
        return {"error": f"PubMed esearch failed: {e}"}

    root = ET.fromstring(search_xml)
    total_node = root.find("Count")
    total = int(total_node.text) if total_node is not None and total_node.text.isdigit() else 0

    pmids = [id_node.text for id_node in root.findall("IdList/Id") if id_node.text]
    if not pmids:
        return {"query": query, "database": "PubMed", "total": 0, "hits": []}

    # Step 2: efetch — get detailed metadata for PMIDs
    fetch_params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml",
        "email": EMAIL,
    }
    fetch_url = f"{PUBMED_BASE}/efetch.fcgi?{urllib.parse.urlencode(fetch_params)}"
    try:
        fetch_xml = _get(fetch_url)
    except Exception as e:
        return {"error": f"PubMed efetch failed: {e}"}

    # Be nice to NCBI
    time.sleep(0.34)

    root = ET.fromstring(fetch_xml)
    hits = []

    for article in root.findall(".//PubmedArticle"):
        pmid_node = article.find(".//PMID")
        pmid = pmid_node.text if pmid_node is not None else ""

        # Title
        title_node = article.find(".//ArticleTitle")
        title = title_node.text.strip() if title_node is not None and title_node.text else "N/A"

        # Abstract (can have multiple parts)
        abstract_parts = article.findall(".//Abstract/AbstractText")
        abstract = " ".join(
            p.text.strip() for p in abstract_parts if p.text
        )

        # Authors
        authors = []
        for au in article.findall(".//Author"):
            lastname = au.findtext("LastName", "").strip()
            forename = au.findtext("ForeName", "").strip()
            if lastname:
                authors.append(f"{lastname} {forename}".strip())
        authors_str = "; ".join(authors)

        # Journal
        journal_node = article.find(".//Journal/Title")
        journal = journal_node.text.strip() if journal_node is not None and journal_node.text else "N/A"

        # Year
        year_node = article.find(".//PubDate/Year")
        if year_node is None:
            year_node = article.find(".//PubDate/MedlineDate")
        year = ""
        if year_node is not None and year_node.text:
            year = year_node.text[:4].strip()

        # DOI
        doi = ""
        for art_id in article.findall(".//ArticleId[@IdType='doi']"):
            if art_id.text:
                doi = art_id.text
        doi_link = f"https://doi.org/{doi}" if doi else f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

        # Keywords (MeSH headings)
        mesh_terms = []
        for mesh in article.findall(".//MeshHeading/DescriptorName"):
            if mesh.text:
                mesh_terms.append(mesh.text)
        keywords_str = "; ".join(mesh_terms) if mesh_terms else ""

        # Publication types
        pub_types = []
        for pt in article.findall(".//PublicationType"):
            if pt.text:
                pub_types.append(pt.text)

        hits.append({
            "title": title,
            "authors": authors_str,
            "year": year or "N/A",
            "journal": journal,
            "doi": doi or "N/A",
            "url": doi_link,
            "abstract": abstract,
            "keywords": keywords_str,
            "pmid": pmid,
            "publication_types": "; ".join(pub_types),
            "database": "PubMed",
        })

    return {
        "query": query,
        "database": "PubMed",
        "total": total,
        "hits": hits,
    }


def main():
    parser = argparse.ArgumentParser(description="Search PubMed for academic literature (no API key required)")
    parser.add_argument("--query", required=True, help="Search query (supports MeSH terms)")
    parser.add_argument("--max", type=int, default=30, help="Maximum results to return (default 30)")
    parser.add_argument("--mindate", default="", help="Start date filter, e.g. 2015 or 2015-01-01")
    parser.add_argument("--maxdate", default="", help="End date filter, e.g. 2024 or 2024-12-31")
    parser.add_argument("--email", default=EMAIL, help="Your email (for NCBI courtesy)")
    args = parser.parse_args()

    global EMAIL
    EMAIL = args.email or EMAIL

    result = search_pubmed(args.query, args.max, args.mindate, args.maxdate)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
