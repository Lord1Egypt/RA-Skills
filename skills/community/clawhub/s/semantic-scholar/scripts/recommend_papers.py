#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Semantic Scholar paper recommendations script.

Purpose
-------
Retrieve recommended papers from seed paper IDs using:
    POST /recommendations/v1/papers
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from typing import Any, Dict, List, Optional

import requests


BASE_URL = "https://api.semanticscholar.org/recommendations/v1/papers"


def build_headers() -> Dict[str, str]:
    api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY", "").strip()
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "semantic-scholar-recommendations/1.0",
    }
    if api_key:
        headers["x-api-key"] = api_key
    return headers


def request_with_retry(
    session: requests.Session,
    url: str,
    payload: Dict[str, Any],
    params: Dict[str, Any],
    headers: Dict[str, str],
    max_retries: int = 6,
    timeout: int = 60,
) -> Dict[str, Any]:
    for attempt in range(max_retries):
        try:
            response = session.post(
                url,
                params=params,
                headers=headers,
                json=payload,
                timeout=timeout,
            )
            if response.status_code == 200:
                data = response.json()
                if not isinstance(data, dict):
                    raise RuntimeError(f"Unexpected response type: {type(data)!r}")
                return data

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


def parse_id_list(raw: Optional[str]) -> List[str]:
    if not raw:
        return []
    return [value.strip() for value in raw.split(",") if value.strip()]


def flatten_authors(authors: Any) -> str:
    if not isinstance(authors, list):
        return ""
    return "; ".join(
        str(author.get("name"))
        for author in authors
        if isinstance(author, dict) and author.get("name")
    )


def flatten_open_access_pdf(open_access_pdf: Any) -> str:
    if isinstance(open_access_pdf, dict):
        return str(open_access_pdf.get("url", "") or "")
    return ""


def paper_to_csv_row(paper: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "paperId": paper.get("paperId"),
        "title": paper.get("title"),
        "year": paper.get("year"),
        "publicationDate": paper.get("publicationDate"),
        "citationCount": paper.get("citationCount"),
        "url": paper.get("url"),
        "venue": paper.get("venue"),
        "authors": flatten_authors(paper.get("authors")),
        "openAccessPdfUrl": flatten_open_access_pdf(paper.get("openAccessPdf")),
        "abstract": paper.get("abstract"),
    }


def export_csv(jsonl_path: str, csv_output: str) -> None:
    rows: List[Dict[str, Any]] = []
    with open(jsonl_path, "r", encoding="utf-8") as fin:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            payload = json.loads(line)
            rows.append(paper_to_csv_row(payload["paper"]))

    if not rows:
        print("[INFO] No rows available for CSV export.")
        return

    fieldnames = list(rows[0].keys())
    with open(csv_output, "w", encoding="utf-8-sig", newline="") as fout:
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"[DONE] CSV exported to: {csv_output}")


def recommend_papers(
    positive_ids: List[str],
    output_path: str,
    fields: str,
    limit: int = 20,
    negative_ids: Optional[List[str]] = None,
    pool_from: Optional[str] = None,
) -> int:
    if not positive_ids:
        raise ValueError("At least one positive paper ID is required.")

    headers = build_headers()
    session = requests.Session()
    params = {"fields": fields}
    payload: Dict[str, Any] = {
        "positivePaperIds": positive_ids,
    }
    params: Dict[str, Any] = {"fields": fields, "limit": limit}
    if negative_ids:
        payload["negativePaperIds"] = negative_ids
    if pool_from:
        payload["poolFrom"] = pool_from

    response_data = request_with_retry(
        session=session,
        url=BASE_URL,
        payload=payload,
        params=params,
        headers=headers,
    )
    recommendations = response_data.get("recommendedPapers", [])
    if not isinstance(recommendations, list):
        raise RuntimeError("Unexpected recommendations payload shape.")

    with open(output_path, "w", encoding="utf-8") as fout:
        for rank, paper in enumerate(recommendations, start=1):
            fout.write(
                json.dumps(
                    {
                        "rank": rank,
                        "seedPaperIds": positive_ids,
                        "negativePaperIds": negative_ids or [],
                        "paper": paper,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )

    print(f"[DONE] JSONL saved to: {output_path}")
    print(f"[DONE] Total recommendations written: {len(recommendations)}")
    return len(recommendations)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Get paper recommendations from Semantic Scholar seed papers."
    )
    parser.add_argument(
        "--positive-ids",
        type=str,
        required=True,
        help="Comma-separated positive seed paper IDs.",
    )
    parser.add_argument(
        "--negative-ids",
        type=str,
        default=None,
        help="Optional comma-separated negative seed paper IDs.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum number of recommendations to request. Default: 20",
    )
    parser.add_argument(
        "--pool-from",
        type=str,
        default=None,
        help="Optional pool selector supported by the recommendations API.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="paper_recommendations.jsonl",
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
        default="title,abstract,year,url,authors,citationCount,publicationDate,openAccessPdf,venue",
        help="Comma-separated fields to request for recommended papers.",
    )
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be at least 1.")
    return args


def main() -> None:
    args = parse_args()
    total_written = recommend_papers(
        positive_ids=parse_id_list(args.positive_ids),
        negative_ids=parse_id_list(args.negative_ids),
        output_path=args.output,
        fields=args.fields,
        limit=args.limit,
        pool_from=args.pool_from,
    )
    if args.csv_output and total_written > 0:
        export_csv(args.output, args.csv_output)


if __name__ == "__main__":
    main()
