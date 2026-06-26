#!/usr/bin/env python3
"""Search public-api-lists for agent-friendly API candidates."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any

SOURCE_URL = "https://public-api-lists.github.io/public-api-lists/api/all.json"
CACHE_PATH = Path(os.environ.get("PUBLIC_API_FINDER_CACHE", "~/.cache/public-api-finder/all.json")).expanduser()
CACHE_TTL_SECONDS = 24 * 60 * 60


def load_data(refresh: bool = False) -> list[dict[str, Any]]:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    fresh = CACHE_PATH.exists() and (time.time() - CACHE_PATH.stat().st_mtime) < CACHE_TTL_SECONDS
    if refresh or not fresh:
        with urllib.request.urlopen(SOURCE_URL, timeout=20) as res:
            data = json.load(res)
        CACHE_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
    else:
        data = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    return data.get("entries", [])


def tokens(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", text.lower()) if len(t) > 1}


def score(entry: dict[str, Any], query_tokens: set[str]) -> int:
    hay = " ".join(str(entry.get(k, "")) for k in ("name", "description", "category"))
    hay_tokens = tokens(hay)
    name_tokens = tokens(str(entry.get("name", "")))
    category_tokens = tokens(str(entry.get("category", "")))
    desc_tokens = tokens(str(entry.get("description", "")))
    return (
        5 * len(query_tokens & name_tokens)
        + 4 * len(query_tokens & category_tokens)
        + 2 * len(query_tokens & desc_tokens)
        + len(query_tokens & hay_tokens)
    )


def filter_entries(entries: list[dict[str, Any]], args: argparse.Namespace) -> list[dict[str, Any]]:
    q_tokens = tokens(args.query or "")
    out = []
    for e in entries:
        if args.category and args.category.lower() not in str(e.get("category", "")).lower():
            continue
        if args.no_auth and str(e.get("auth", "")).lower() != "no":
            continue
        if args.https and not e.get("https"):
            continue
        if args.cors and args.cors.lower() != str(e.get("cors", "")).lower():
            continue
        s = score(e, q_tokens) if q_tokens else 1
        if q_tokens and s == 0:
            continue
        item = dict(e)
        item["score"] = s
        out.append(item)
    return sorted(out, key=lambda x: (-x["score"], str(x.get("category", "")), str(x.get("name", ""))))[: args.limit]


def markdown(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "No matching public APIs found. Try broader terms or remove filters."
    lines = []
    for i, e in enumerate(rows, 1):
        auth = e.get("auth", "Unknown")
        https = "yes" if e.get("https") else "no"
        cors = e.get("cors", "Unknown")
        lines.append(
            f"{i}. **{e.get('name')}** ({e.get('category')}) — {e.get('description')}\n"
            f"   - URL: {e.get('url')}\n"
            f"   - Auth: `{auth}` · HTTPS: {https} · CORS: {cors} · score: {e.get('score')}"
        )
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Search public-api-lists for API candidates")
    ap.add_argument("query", nargs="?", default="", help="Search terms, e.g. 'weather forecast' or 'crypto prices'")
    ap.add_argument("--category", help="Filter by category substring")
    ap.add_argument("--no-auth", action="store_true", help="Only APIs that list Auth as No")
    ap.add_argument("--https", action="store_true", help="Only HTTPS APIs")
    ap.add_argument("--cors", choices=["Yes", "No", "Unknown"], help="Filter by CORS value")
    ap.add_argument("--limit", type=int, default=8, help="Maximum results")
    ap.add_argument("--json", action="store_true", help="Emit JSON")
    ap.add_argument("--refresh", action="store_true", help="Refresh local cache")
    args = ap.parse_args()

    try:
        rows = filter_entries(load_data(args.refresh), args)
    except Exception as exc:
        print(f"public-api-finder: failed to load API list: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        print(markdown(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
