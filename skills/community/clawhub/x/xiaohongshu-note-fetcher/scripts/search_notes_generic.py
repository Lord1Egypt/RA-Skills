#!/usr/bin/env python3
"""Generic Xiaohongshu note-search API caller."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def parse_kv(items: List[str]) -> List[Tuple[str, str]]:
    out: List[Tuple[str, str]] = []
    for item in items:
        if "=" not in item:
            raise ValueError(f"Invalid --param format: {item}. Use key=value")
        k, v = item.split("=", 1)
        k = k.strip()
        if not k:
            raise ValueError(f"Invalid key in --param: {item}")
        out.append((k, v))
    return out


def build_headers(args: argparse.Namespace) -> Dict[str, str]:
    headers: Dict[str, str] = {"Accept": "application/json"}
    if args.auth_mode == "bearer":
        headers[args.auth_header] = f"Bearer {args.token}"
    elif args.auth_mode == "apikey":
        headers[args.auth_header] = args.token
    for k, v in parse_kv(args.header):
        headers[k] = v
    return headers


def main() -> int:
    parser = argparse.ArgumentParser(description="Call a custom Xiaohongshu notes API endpoint.")
    parser.add_argument("--base-url", required=True, help="API endpoint URL, e.g. https://example.com/search")
    parser.add_argument("--token", default="", help="API token/key")
    parser.add_argument("--token-file", default="", help="Read token/key from file")
    parser.add_argument("--auth-mode", choices=["none", "bearer", "apikey"], default="bearer")
    parser.add_argument("--auth-header", default="Authorization", help="Header name for auth token")
    parser.add_argument("--keyword", required=True, help="Search keyword")
    parser.add_argument("--page", type=int, default=1, help="Page number, start from 1")
    parser.add_argument("--keyword-param", default="keyword", help="Keyword query parameter name")
    parser.add_argument("--page-param", default="page", help="Page query parameter name")
    parser.add_argument("--param", action="append", default=[], help="Extra query params in key=value format")
    parser.add_argument("--header", action="append", default=[], help="Extra headers in key=value format")
    parser.add_argument("--timeout", type=int, default=30, help="Request timeout in seconds")
    parser.add_argument("--output", default="", help="Optional path to save response JSON/text")
    args = parser.parse_args()

    if args.page < 1:
        parser.error("--page must be >= 1")

    token = args.token
    if args.token_file:
        token = Path(args.token_file).read_text(encoding="utf-8").strip()
    if args.auth_mode != "none" and not token:
        parser.error("Provide --token or --token-file when auth-mode is bearer/apikey")
    args.token = token

    query_items: List[Tuple[str, str]] = [
        (args.keyword_param, args.keyword),
        (args.page_param, str(args.page)),
    ]
    query_items.extend(parse_kv(args.param))
    query_string = urlencode(query_items)

    sep = "&" if "?" in args.base_url else "?"
    url = f"{args.base_url}{sep}{query_string}"
    req = Request(url=url, headers=build_headers(args), method="GET")

    with urlopen(req, timeout=args.timeout) as resp:
        raw = resp.read().decode("utf-8", errors="replace")

    if args.output:
        Path(args.output).write_text(raw, encoding="utf-8")

    try:
        payload = json.loads(raw)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    except json.JSONDecodeError:
        print(raw)
    return 0


if __name__ == "__main__":
    sys.exit(main())
