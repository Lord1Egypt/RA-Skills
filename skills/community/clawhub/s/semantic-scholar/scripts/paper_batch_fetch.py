#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Semantic Scholar paper batch fetch script.

Purpose
-------
Fetch paper metadata in batches using:
    POST /graph/v1/paper/batch

Features
--------
1. Reads paper IDs from CLI or file
2. Sends batched POST requests with retry/backoff
3. Saves raw results to JSONL
4. Optionally exports a flattened CSV
5. Supports API key via environment variable
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import requests


BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/batch"


def build_headers() -> Dict[str, str]:
    api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY", "").strip()
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "semantic-scholar-paper-batch/1.0",
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
) -> List[Dict[str, Any]]:
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
                if not isinstance(data, list):
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


def load_ids_from_file(path: str) -> List[str]:
    ids: List[str] = []
    with open(path, "r", encoding="utf-8") as fin:
        for line in fin:
            value = line.strip()
            if value:
                ids.append(value)
    return ids


def parse_id_args(ids_arg: Optional[str], ids_file: Optional[str]) -> List[str]:
    ids: List[str] = []
    if ids_arg:
        ids.extend([value.strip() for value in ids_arg.split(",") if value.strip()])
    if ids_file:
        ids.extend(load_ids_from_file(ids_file))

    # Deduplicate while preserving order.
    seen = set()
    deduped: List[str] = []
    for item in ids:
        if item in seen:
            continue
        seen.add(item)
        deduped.append(item)
    return deduped


def chunked(items: List[str], chunk_size: int) -> Iterable[List[str]]:
    for index in range(0, len(items), chunk_size):
        yield items[index : index + chunk_size]


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
        "influentialCitationCount": paper.get("influentialCitationCount"),
        "url": paper.get("url"),
        "venue": paper.get("venue"),
        "publicationTypes": json.dumps(paper.get("publicationTypes", []), ensure_ascii=False),
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
            rows.append(paper_to_csv_row(json.loads(line)))

    if not rows:
        print("[INFO] No rows available for CSV export.")
        return

    fieldnames = list(rows[0].keys())
    with open(csv_output, "w", encoding="utf-8-sig", newline="") as fout:
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"[DONE] CSV exported to: {csv_output}")


def fetch_papers(
    ids: List[str],
    output_path: str,
    fields: str,
    chunk_size: int = 500,
    sleep_seconds: float = 0.5,
) -> int:
    if not ids:
        raise ValueError("No paper IDs provided.")

    headers = build_headers()
    session = requests.Session()
    params = {"fields": fields}

    total_written = 0
    with open(output_path, "w", encoding="utf-8") as fout:
        for index, batch_ids in enumerate(chunked(ids, chunk_size), start=1):
            payload = {"ids": batch_ids}
            records = request_with_retry(
                session=session,
                url=BASE_URL,
                payload=payload,
                params=params,
                headers=headers,
            )

            written_this_batch = 0
            for record in records:
                if not record:
                    continue
                fout.write(json.dumps(record, ensure_ascii=False) + "\n")
                written_this_batch += 1

            total_written += written_this_batch
            print(
                f"[INFO] Batch {index}: requested {len(batch_ids)} IDs, wrote {written_this_batch} records, total written = {total_written}"
            )
            if sleep_seconds > 0:
                time.sleep(sleep_seconds)

    print(f"[DONE] JSONL saved to: {output_path}")
    print(f"[DONE] Total records written: {total_written}")
    return total_written


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Batch fetch paper metadata from Semantic Scholar."
    )
    parser.add_argument(
        "--ids",
        type=str,
        default=None,
        help="Comma-separated paper IDs.",
    )
    parser.add_argument(
        "--ids-file",
        type=str,
        default=None,
        help="Text file with one paper ID per line.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="paper_batch_results.jsonl",
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
        default="title,abstract,year,url,authors,citationCount,influentialCitationCount,publicationDate,publicationTypes,openAccessPdf,venue",
        help="Comma-separated fields to request.",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=500,
        help="Number of IDs per request. Default: 500",
    )
    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=0.5,
        help="Sleep interval between requests. Default: 0.5",
    )
    args = parser.parse_args()

    if not args.ids and not args.ids_file:
        parser.error("Provide --ids or --ids-file.")
    if args.chunk_size < 1:
        parser.error("--chunk-size must be at least 1.")
    return args


def main() -> None:
    args = parse_args()
    ids = parse_id_args(args.ids, args.ids_file)
    total_written = fetch_papers(
        ids=ids,
        output_path=args.output,
        fields=args.fields,
        chunk_size=args.chunk_size,
        sleep_seconds=args.sleep_seconds,
    )
    if args.csv_output and total_written > 0:
        export_csv(args.output, args.csv_output)


if __name__ == "__main__":
    main()
