#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Semantic Scholar bulk search script

Purpose
-------
Batch search papers from the Semantic Scholar Academic Graph API using:
    GET /graph/v1/paper/search/bulk

This script is suitable for literature retrieval tasks such as:
- Materials Science Multi Agent System
- agentic AI for materials discovery
- multi-agent systems in computational materials science

Features
--------
1. Uses the bulk search endpoint recommended for large-scale retrieval
2. Automatically handles token-based pagination
3. Saves raw results to JSONL (one JSON object per line)
4. Optionally exports a flattened CSV
5. Supports API key via environment variable
6. Includes retry logic for rate limits and transient server errors
7. Includes example command-line usages

Install
-------
pip install requests pandas

API key (recommended)
---------------------
export SEMANTIC_SCHOLAR_API_KEY="your_api_key"

Basic usage
-----------
python semantic_scholar_bulk_search.py

Example usages
--------------
1) Use default query:
python semantic_scholar_bulk_search.py

2) Search exact phrase:
python semantic_scholar_bulk_search.py \
    --query '"Materials Science Multi Agent System"'

3) A more realistic literature query:
python semantic_scholar_bulk_search.py \
    --query '("materials science" | "materials discovery" | "computational materials") + ("multi-agent" | "multi agent" | agentic | "autonomous agent" | "llm agent")'

4) Only search papers from 2020 onward:
python semantic_scholar_bulk_search.py \
    --year 2020-

5) Sort by citation count descending:
python semantic_scholar_bulk_search.py \
    --sort citationCount:desc

6) Sort by publication date descending:
python semantic_scholar_bulk_search.py \
    --sort publicationDate:desc

7) Only keep papers with at least 10 citations:
python semantic_scholar_bulk_search.py \
    --min-citation-count 10

8) Only retrieve papers with open-access PDF:
python semantic_scholar_bulk_search.py \
    --open-access-pdf

9) Limit to first 3 pages for quick testing:
python semantic_scholar_bulk_search.py \
    --max-pages 3

10) Save to custom JSONL file:
python semantic_scholar_bulk_search.py \
    --output my_results.jsonl

11) Export both JSONL and CSV:
python semantic_scholar_bulk_search.py \
    --output my_results.jsonl \
    --csv-output my_results.csv

12) Use a custom field list:
python semantic_scholar_bulk_search.py \
    --fields title,abstract,year,url,authors,citationCount,publicationDate,venue

13) A recommended query for your topic:
python semantic_scholar_bulk_search.py \
    --query '("materials science" | "materials informatics" | "materials discovery") + ("multi-agent system" | "multi-agent" | "agentic" | "llm agent" | "autonomous research agent")' \
    --year 2020- \
    --sort citationCount:desc \
    --csv-output materials_multi_agent.csv

Output
------
- JSONL: raw API results, one paper per line
- CSV: flattened results, convenient for Excel / pandas / screening

Notes
-----
1. Using an API key is optional but strongly recommended.
2. Bulk search uses token-based pagination, not offset/limit pagination.
3. For broad literature surveys, use a query with Boolean operators instead of a single rigid phrase.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Any, Dict, List, Optional

import requests

try:
    import pandas as pd
except ImportError:
    pd = None


BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"


def build_headers() -> Dict[str, str]:
    """
    Build request headers. API key is optional but recommended.
    """
    api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY", "").strip()
    headers = {
        "Accept": "application/json",
        "User-Agent": "semantic-scholar-bulk-search/1.0",
    }
    if api_key:
        headers["x-api-key"] = api_key
    return headers


def request_with_retry(
    session: requests.Session,
    url: str,
    params: Dict[str, Any],
    headers: Dict[str, str],
    max_retries: int = 6,
    timeout: int = 60,
) -> Dict[str, Any]:
    """
    Send GET request with retry logic for:
    - rate limits (429)
    - transient server errors (5xx)
    - network errors

    Returns parsed JSON on success.
    """
    for attempt in range(max_retries):
        try:
            response = session.get(url, params=params, headers=headers, timeout=timeout)

            if response.status_code == 200:
                return response.json()

            if response.status_code == 429:
                wait_time = min(2 ** attempt, 30)
                print(
                    f"[WARN] HTTP 429 Too Many Requests. Sleeping {wait_time}s before retry...",
                    file=sys.stderr,
                )
                time.sleep(wait_time)
                continue

            if 500 <= response.status_code < 600:
                wait_time = min(2 ** attempt, 30)
                print(
                    f"[WARN] HTTP {response.status_code} server error. Sleeping {wait_time}s before retry...",
                    file=sys.stderr,
                )
                time.sleep(wait_time)
                continue

            raise RuntimeError(
                f"Request failed with HTTP {response.status_code}\nResponse body:\n{response.text}"
            )

        except requests.RequestException as exc:
            wait_time = min(2 ** attempt, 30)
            print(
                f"[WARN] Network/request error: {exc}. Sleeping {wait_time}s before retry...",
                file=sys.stderr,
            )
            time.sleep(wait_time)

    raise RuntimeError("Request failed after maximum retries.")


def flatten_authors(authors: Any) -> str:
    """
    Convert author list to a readable string.
    """
    if not authors:
        return ""
    if not isinstance(authors, list):
        return ""
    names = []
    for author in authors:
        if isinstance(author, dict):
            name = author.get("name")
            if name:
                names.append(str(name))
    return "; ".join(names)


def flatten_open_access_pdf(open_access_pdf: Any) -> str:
    """
    Extract open access PDF URL if available.
    """
    if isinstance(open_access_pdf, dict):
        return str(open_access_pdf.get("url", "") or "")
    return ""


def paper_to_csv_row(paper: Dict[str, Any]) -> Dict[str, Any]:
    """
    Flatten one paper record for CSV export.
    """
    return {
        "paperId": paper.get("paperId"),
        "title": paper.get("title"),
        "year": paper.get("year"),
        "publicationDate": paper.get("publicationDate"),
        "citationCount": paper.get("citationCount"),
        "url": paper.get("url"),
        "venue": paper.get("venue"),
        "publicationTypes": json.dumps(paper.get("publicationTypes", []), ensure_ascii=False),
        "authors": flatten_authors(paper.get("authors")),
        "openAccessPdfUrl": flatten_open_access_pdf(paper.get("openAccessPdf")),
        "abstract": paper.get("abstract"),
    }


def export_csv(jsonl_path: str, csv_output: str) -> None:
    """
    Export JSONL results to CSV.
    """
    if pd is None:
        raise RuntimeError(
            "CSV export requires pandas. Please install it with: pip install pandas"
        )

    rows: List[Dict[str, Any]] = []
    with open(jsonl_path, "r", encoding="utf-8") as fin:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            paper = json.loads(line)
            rows.append(paper_to_csv_row(paper))

    df = pd.DataFrame(rows)
    df.to_csv(csv_output, index=False, encoding="utf-8-sig")
    print(f"[DONE] CSV exported to: {csv_output}")


def bulk_search_papers(
    query: str,
    output_path: str,
    fields: str,
    year: Optional[str] = None,
    sort: Optional[str] = None,
    min_citation_count: Optional[int] = None,
    open_access_pdf: Optional[bool] = None,
    publication_types: Optional[str] = None,
    fields_of_study: Optional[str] = None,
    venue: Optional[str] = None,
    max_pages: Optional[int] = None,
    sleep_seconds: float = 1.0,
) -> int:
    """
    Perform bulk search with token-based pagination.
    Save each paper record as one JSON line.

    Returns
    -------
    int
        Number of retrieved papers written to disk.
    """
    headers = build_headers()
    session = requests.Session()

    params: Dict[str, Any] = {
        "query": query,
        "fields": fields,
    }

    if year:
        params["year"] = year
    if sort:
        params["sort"] = sort
    if min_citation_count is not None:
        params["minCitationCount"] = min_citation_count
    if open_access_pdf is not None:
        params["openAccessPdf"] = str(open_access_pdf).lower()
    if publication_types:
        params["publicationTypes"] = publication_types
    if fields_of_study:
        params["fieldsOfStudy"] = fields_of_study
    if venue:
        params["venue"] = venue

    total_written = 0
    page_count = 0

    with open(output_path, "w", encoding="utf-8") as fout:
        while True:
            response_data = request_with_retry(
                session=session,
                url=BASE_URL,
                params=params,
                headers=headers,
            )

            if page_count == 0:
                estimated_total = response_data.get("total")
                print(f"[INFO] Estimated total matched papers: {estimated_total}")

            data = response_data.get("data", [])
            if not data:
                print("[INFO] No more data returned.")
                break

            for paper in data:
                fout.write(json.dumps(paper, ensure_ascii=False) + "\n")

            total_written += len(data)
            page_count += 1
            print(
                f"[INFO] Page {page_count}: wrote {len(data)} papers, total written = {total_written}"
            )

            next_token = response_data.get("token")
            if not next_token:
                print("[INFO] No continuation token found. Finished.")
                break

            if max_pages is not None and page_count >= max_pages:
                print(f"[INFO] Reached max_pages={max_pages}. Stopping early.")
                break

            params["token"] = next_token

            if sleep_seconds > 0:
                time.sleep(sleep_seconds)

    print(f"[DONE] JSONL saved to: {output_path}")
    print(f"[DONE] Total papers written: {total_written}")
    return total_written


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Batch search papers from Semantic Scholar Academic Graph API."
    )

    parser.add_argument(
        "--query",
        type=str,
        default='"Materials Science Multi Agent System"',
        help='Search query. Default: \'"Materials Science Multi Agent System"\'',
    )
    parser.add_argument(
        "--output",
        type=str,
        default="materials_science_multi_agent_system.jsonl",
        help="Output JSONL file path.",
    )
    parser.add_argument(
        "--csv-output",
        type=str,
        default=None,
        help="Optional CSV output path.",
    )
    parser.add_argument(
        "--fields",
        type=str,
        default="title,abstract,year,url,authors,citationCount,publicationDate,publicationTypes,openAccessPdf,venue",
        help="Comma-separated fields to request.",
    )
    parser.add_argument(
        "--year",
        type=str,
        default=None,
        help='Year filter, e.g. "2020-" or "2020-2025".',
    )
    parser.add_argument(
        "--sort",
        type=str,
        default=None,
        help='Optional sort, e.g. "citationCount:desc" or "publicationDate:desc".',
    )
    parser.add_argument(
        "--min-citation-count",
        type=int,
        default=None,
        help="Minimum citation count filter.",
    )
    parser.add_argument(
        "--open-access-pdf",
        action="store_true",
        help="Only retrieve papers with open access PDF.",
    )
    parser.add_argument(
        "--publication-types",
        type=str,
        default=None,
        help='Filter by publication types, e.g. "JournalArticle" or "Review".',
    )
    parser.add_argument(
        "--fields-of-study",
        type=str,
        default=None,
        help='Filter by field of study, e.g. "Materials Science".',
    )
    parser.add_argument(
        "--venue",
        type=str,
        default=None,
        help='Filter by venue name.',
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Maximum number of pages to retrieve, useful for quick testing.",
    )
    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=1.0,
        help="Sleep interval between page requests. Default: 1.0",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    total_written = bulk_search_papers(
        query=args.query,
        output_path=args.output,
        fields=args.fields,
        year=args.year,
        sort=args.sort,
        min_citation_count=args.min_citation_count,
        open_access_pdf=True if args.open_access_pdf else None,
        publication_types=args.publication_types,
        fields_of_study=args.fields_of_study,
        venue=args.venue,
        max_pages=args.max_pages,
        sleep_seconds=args.sleep_seconds,
    )

    if args.csv_output:
        if total_written == 0:
            print("[INFO] No results found, skipping CSV export.")
        else:
            export_csv(args.output, args.csv_output)


if __name__ == "__main__":
    main()
