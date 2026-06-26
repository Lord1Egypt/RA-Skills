#!/usr/bin/env python3
"""Salesflare API request helper.

Examples:
  python3 scripts/sf_request.py --method GET --path /accounts --query limit=10
  python3 scripts/sf_request.py --method POST --path /tags --data-json '{"name":"VIP"}'
  python3 scripts/sf_request.py --method PATCH --path /opportunities/123 --data-file body.json

Auth:
  export SALESFLARE_API_KEY='...'
"""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


DEFAULT_BASE = os.environ.get("SALESFLARE_DEFAULT_BASE_URL", "https://api.salesflare.com")


def parse_query(parts: list[str]) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for p in parts:
        if "=" not in p:
            raise SystemExit(f"Invalid --query value '{p}'. Use key=value")
        k, v = p.split("=", 1)
        out.append((k, v))
    return out


def build_url(base: str, path: str, query_pairs: list[tuple[str, str]]) -> str:
    base = base.rstrip("/")
    if not path.startswith("/"):
        path = "/" + path
    if query_pairs:
        qs = urllib.parse.urlencode(query_pairs, doseq=True)
        return f"{base}{path}?{qs}"
    return f"{base}{path}"


def request_json(
    *,
    method: str,
    url: str,
    api_key: str,
    body: Any | None,
    timeout: int,
    max_retries: int,
    retry_base_s: float,
) -> tuple[int, Any]:
    payload = None
    if body is not None:
        payload = json.dumps(body).encode("utf-8")

    attempt = 0
    while True:
        req = urllib.request.Request(url, data=payload, method=method)
        req.add_header("Authorization", f"Bearer {api_key}")
        req.add_header("Accept", "application/json")
        if payload is not None:
            req.add_header("Content-Type", "application/json")

        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                status = int(r.getcode() or 200)
                raw = r.read().decode("utf-8", errors="replace")
                try:
                    return status, json.loads(raw) if raw else {}
                except json.JSONDecodeError:
                    return status, {"raw": raw}
        except urllib.error.HTTPError as e:
            status = int(e.code)
            raw = e.read().decode("utf-8", errors="replace")
            retryable = status in {429, 500, 502, 503, 504}
            if retryable and attempt < max_retries:
                delay = retry_base_s * (2**attempt)
                time.sleep(delay)
                attempt += 1
                continue
            try:
                return status, json.loads(raw) if raw else {"error": "http_error"}
            except json.JSONDecodeError:
                return status, {"error": "http_error", "raw": raw}


def auto_paginate(
    *,
    base: str,
    path: str,
    query_pairs: list[tuple[str, str]],
    api_key: str,
    timeout: int,
    max_retries: int,
    retry_base_s: float,
    limit: int,
    max_pages: int,
) -> tuple[int, dict[str, Any]]:
    # Remove caller-provided limit/offset so pagination is deterministic.
    cleaned = [(k, v) for (k, v) in query_pairs if k not in {"limit", "offset"}]

    all_items: list[Any] = []
    pages = 0
    offset = 0
    last_status = 200

    while pages < max_pages:
        page_q = cleaned + [("limit", str(limit)), ("offset", str(offset))]
        url = build_url(base, path, page_q)
        status, data = request_json(
            method="GET",
            url=url,
            api_key=api_key,
            body=None,
            timeout=timeout,
            max_retries=max_retries,
            retry_base_s=retry_base_s,
        )
        last_status = status
        if status < 200 or status >= 300:
            return status, {
                "error": "pagination_failed",
                "status": status,
                "offset": offset,
                "response": data,
            }

        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            # Common patterns: {data:[...]} or {items:[...]}
            if isinstance(data.get("data"), list):
                items = data["data"]
            elif isinstance(data.get("items"), list):
                items = data["items"]
            else:
                # Not a list-like response, return single page as-is.
                return status, {
                    "pages": pages + 1,
                    "count": 1,
                    "items": [data],
                }
        else:
            return status, {
                "pages": pages + 1,
                "count": 1,
                "items": [data],
            }

        all_items.extend(items)
        pages += 1
        if len(items) < limit:
            break
        offset += limit

    return last_status, {
        "pages": pages,
        "count": len(all_items),
        "items": all_items,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--method", default="GET", choices=["GET", "POST", "PUT", "PATCH", "DELETE"])
    ap.add_argument("--path", required=True, help="API path, e.g. /accounts or /opportunities/123")
    ap.add_argument("--query", action="append", default=[], help="Query pair key=value (repeatable)")
    ap.add_argument("--data-json", help="Inline JSON body")
    ap.add_argument("--data-file", help="Path to JSON body file")
    ap.add_argument("--base-url", default=os.environ.get("SALESFLARE_BASE_URL", DEFAULT_BASE))
    ap.add_argument("--api-key", default=os.environ.get("SALESFLARE_API_KEY"))
    ap.add_argument("--timeout", type=int, default=45)
    ap.add_argument("--max-retries", type=int, default=3)
    ap.add_argument("--retry-base-s", type=float, default=1.0)
    ap.add_argument("--paginate", action="store_true", help="Auto-paginate GET list endpoints")
    ap.add_argument("--page-limit", type=int, default=100)
    ap.add_argument("--max-pages", type=int, default=50)
    args = ap.parse_args()

    if not args.api_key:
        raise SystemExit("Missing API key. Set SALESFLARE_API_KEY or pass --api-key")

    body = None
    if args.data_json and args.data_file:
        raise SystemExit("Use either --data-json or --data-file, not both")
    if args.data_json:
        body = json.loads(args.data_json)
    elif args.data_file:
        with open(args.data_file, "r", encoding="utf-8") as f:
            body = json.load(f)

    q = parse_query(args.query)

    if args.paginate and args.method == "GET":
        status, data = auto_paginate(
            base=args.base_url,
            path=args.path,
            query_pairs=q,
            api_key=args.api_key,
            timeout=args.timeout,
            max_retries=args.max_retries,
            retry_base_s=args.retry_base_s,
            limit=args.page_limit,
            max_pages=args.max_pages,
        )
    else:
        url = build_url(args.base_url, args.path, q)
        status, data = request_json(
            method=args.method,
            url=url,
            api_key=args.api_key,
            body=body,
            timeout=args.timeout,
            max_retries=args.max_retries,
            retry_base_s=args.retry_base_s,
        )

    print(json.dumps({"status": status, "data": data}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
