#!/usr/bin/env python3
"""iFlytek ONE SEARCH API (万搜) - Aggregated search via Xfyun.

Environment variables:
    XFYUN_API_PASSWORD  - Required. API password from https://console.xfyun.cn/services/cbm

Usage:
    python search.py <query> [--limit N] [--no-rerank] [--no-fulltext] [--raw]

Examples:
    python search.py "美国现任总统是谁"
    python search.py "Python asyncio tutorial" --limit 5
    python search.py "量子计算最新进展" --no-rerank --raw
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

API_URL = "https://search-api-open.cn-huabei-1.xf-yun.com/v2/search"


def search(query: str, limit: int = 10, open_rerank: bool = True, open_full_text: bool = True) -> dict:
    api_password = os.environ.get("XFYUN_API_PASSWORD")
    if not api_password:
        print("Error: XFYUN_API_PASSWORD environment variable is not set.", file=sys.stderr)
        print("Get your API password from https://console.xfyun.cn/services/cbm", file=sys.stderr)
        sys.exit(1)

    payload = {
        "search_params": {
            "query": query,
            "limit": limit,
            "enhance": {
                "open_rerank": open_rerank,
                "open_full_text": open_full_text,
            },
        }
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {api_password}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Request failed: {e.reason}", file=sys.stderr)
        sys.exit(1)


def format_results(data: dict) -> str:
    lines = []
    if data.get("err_code") != "0" and data.get("err_code") != 0:
        return f"API Error (code {data.get('err_code')}): {json.dumps(data, ensure_ascii=False)}"

    payload = data.get("data", {})
    meta = payload.get("meta", {})
    if meta.get("query"):
        lines.append(f"Query: {meta['query']}")
        lines.append("")

    docs = payload.get("search_results", {}).get("documents", [])
    if not docs:
        lines.append("No results found.")
        return "\n".join(lines)

    for i, doc in enumerate(docs, 1):
        lines.append(f"## {i}. {doc.get('name', 'Untitled')}")
        lines.append(f"URL: {doc.get('url', 'N/A')}")
        summary = doc.get("summary", "")
        if summary:
            lines.append(f"Summary: {summary}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="iFlytek ONE SEARCH API (万搜)")
    parser.add_argument("query", help="Search query string")
    parser.add_argument("--limit", type=int, default=10, help="Max results (1-20, default 10)")
    parser.add_argument("--no-rerank", action="store_true", help="Disable result reranking")
    parser.add_argument("--no-fulltext", action="store_true", help="Disable full text retrieval")
    parser.add_argument("--raw", action="store_true", help="Output raw JSON response")
    args = parser.parse_args()

    result = search(
        query=args.query,
        limit=args.limit,
        open_rerank=not args.no_rerank,
        open_full_text=not args.no_fulltext,
    )

    if args.raw:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_results(result))


if __name__ == "__main__":
    main()
