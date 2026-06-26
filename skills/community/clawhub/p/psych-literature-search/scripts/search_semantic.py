#!/usr/bin/env python3
"""
Semantic Scholar Literature Search Script (no API key required)
Uses the Semantic Scholar REST API (PI to search and retrieve literature metadata.

Usage:
  python search_semantic.py --query "cognitive behavioral therapy" --max 30
  python search_semantic.py --query "empathy" --max 50 --year 2015-2024

No API key required. Rate limit: 100 req/5min (unauthenticated).
Use a larger --batch-size for bulk retrieval (max 500 per request).
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.parse
import urllib.error


S2_BASE = "https://api.semanticscholar.org/graph/v1"


def search_semantic(
    query: str,
    max_results: int = 30,
    year_range: str = "",
    venue_filter: str = "",
    batch_size: int = 100,
) -> dict:
    """
    Search Semantic Scholar via the Paper Search API (no key required).

    Args:
        query: Search query string
        max_results: Maximum number of results to return
        year_range: Year filter, e.g. "2015-2024" or "2020"
        venue_filter: Filter by venue name (partial match)
        batch_size: Number of results per API request (max 500)

    Returns:
        dict with 'total', 'hits' list, and metadata
    """
    all_hits = []
    offset = 0
    limit = min(batch_size, max_results)

    # Build year filter for query string if provided
    search_query = query
    if year_range:
        search_query = f"{query} year:{year_range}"

    while len(all_hits) < max_results:
        params = urllib.parse.urlencode({
            "query": search_query,
            "limit": str(limit),
            "offset": str(offset),
            "fields": "title,authors,year,venue,doi,abstract,externalIds,url,citationCount,influentialCitationCount,fieldsOfStudy",
        })
        url = f"{S2_BASE}/paper/search?{params}"

        req = urllib.request.Request(url, headers={
            "Accept": "application/json",
            "User-Agent": "psych-lit-search/1.0",
        })

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            return {"error": f"Semantic Scholar HTTP {e.code}: {body[:400]}"}
        except Exception as e:
            return {"error": str(e)}

        # Rate-limit courtesy
        time.sleep(6)  # 100 req/5min = 1 req/3s, use 6s to be safe

        papers = data.get("data", [])
        total = data.get("total", 0)

        if not papers:
            break

        for paper in papers:
            if len(all_hits) >= max_results:
                break

            authors_list = paper.get("authors", [])
            authors_str = "; ".join(
                a.get("name", "") for a in authors_list if a.get("name")
            )

            # Extract DOI
            ext_ids = paper.get("externalIds", {})
            doi = ext_ids.get("DOI", "")
            doi_link = f"https://doi.org/{doi}" if doi else (paper.get("url") or "")

            # Keywords: use fieldsOfStudy as proxy
            fos = paper.get("fieldsOfStudy", [])
            keywords_str = "; ".join(f for f in fos if f) if fos else ""

            # Year
            year = paper.get("year", "")
            year_str = str(year) if year else "N/A"

            all_hits.append({
                "title": paper.get("title", "N/A"),
                "authors": authors_str,
                "year": year_str,
                "journal": paper.get("venue", "N/A"),
                "doi": doi or "N/A",
                "url": doi_link,
                "abstract": paper.get("abstract", ""),
                "keywords": keywords_str,
                "citations": paper.get("citationCount", 0),
                "influential_citations": paper.get("influentialCitationCount", 0),
                "fields_of_study": "; ".join(fos) if fos else "",
                "database": "Semantic Scholar",
            })

        offset += limit
        if len(papers) < limit:
            break  # no more results

    return {
        "query": query,
        "database": "Semantic Scholar",
        "total": total if 'total' in dir() else len(all_hits),
        "hits": all_hits[:max_results],
    }


def main():
    parser = argparse.ArgumentParser(description="Search Semantic Scholar (no API key required)")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--max", type=int, default=30, help="Maximum results (default 30)")
    parser.add_argument("--year", default="", help="Year filter, e.g. '2015-2024' or '2020'")
    parser.add_argument("--venue", default="", help="Filter by venue name")
    args = parser.parse_args()

    result = search_semantic(args.query, args.max, args.year, args.venue)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
