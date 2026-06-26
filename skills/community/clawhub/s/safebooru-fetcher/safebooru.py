#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Safebooru Fetcher (DAPI-only, download-only)

- Uses Safebooru DAPI JSON to search posts and download original images.

Examples:
  python3 safebooru.py "genshin_impact maid" 5 --sort score_desc --min-score 5
  python3 safebooru.py "blue_archive shiroko" 10 --page 2 --sort id_desc
  python3 safebooru.py --suggest genshin

Notes:
- Pagination: DAPI uses `pid` (0-based page index). CLI uses --page (1-based).
- Sorting is expressed via tag tokens like `sort:score:desc`.
"""

from __future__ import annotations

import argparse
import os
import time
from typing import List

from safebooru_fetcher import (
    SORT_MAP,
    build_tags,
    download_file,
    fetch_posts,
    suggest_tags,
)

DEFAULT_OUT = "./downloads"


def _safe_slug(text: str, max_len: int = 50) -> str:
    import re
    text = text.strip().replace(" ", "_")
    text = re.sub(r"[^a-zA-Z0-9_\-]+", "_", text)
    return text[:max_len].strip("_") or "safebooru"


def main() -> None:
    parser = argparse.ArgumentParser(description="Safebooru DAPI downloader")
    parser.add_argument("tags", nargs="?", help="space-separated tags, e.g. 'genshin_impact maid'")
    parser.add_argument("count", nargs="?", type=int, default=5, help="how many images to download")

    parser.add_argument("--page", type=int, default=1, help="page number (1-based). DAPI uses pid=page-1")
    parser.add_argument(
        "--sort",
        choices=sorted(SORT_MAP.keys()),
        default="id_desc",
        help="sorting strategy",
    )
    parser.add_argument("--min-score", type=int, default=None, help="filter by score >= N")
    parser.add_argument(
        "--exclude",
        default="",
        help="comma-separated tags to exclude, e.g. 'comic,greyscale'",
    )
    parser.add_argument("--out", default=DEFAULT_OUT, help="output directory")

    parser.add_argument("--suggest", metavar="PATTERN", help="suggest tags by name pattern (uses tag DAPI)")

    args = parser.parse_args()

    if args.suggest:
        items = suggest_tags(args.suggest, limit=50)
        if not items:
            print("(no matches)")
            return
        for name, cnt in items[:50]:
            print(f"{name}\t{cnt}")
        return

    if not args.tags:
        parser.print_help()
        return

    exclude = [x.strip() for x in args.exclude.split(",") if x.strip()]
    tags_expr = build_tags(
        args.tags,
        sort=args.sort,
        min_score=args.min_score,
        exclude=exclude,
    )

    limit = int(args.count)
    page = max(1, int(args.page))

    print("=" * 60)
    print("Safebooru DAPI Downloader")
    print("=" * 60)
    print(f"tags: {tags_expr}")
    print(f"page: {page} | limit: {limit}")

    posts = fetch_posts(tags_expr, limit=limit, page=page)
    if not posts:
        print("No results found. Try different tags, lower limit, or different sort.")
        return

    os.makedirs(args.out, exist_ok=True)
    slug = _safe_slug(args.tags)

    downloaded: List[str] = []
    for idx, post in enumerate(posts[:limit], 1):
        from urllib.parse import urlsplit
        ext = os.path.splitext(urlsplit(post.file_url).path)[1] or ".jpg"
        filename = f"{slug}_{post.id}{ext}"
        path = os.path.join(args.out, filename)

        print(f"\n[{idx}/{limit}] id={post.id} downloading...")
        try:
            download_file(post.file_url, path)
            size_kb = os.path.getsize(path) / 1024
            print(f"  OK ({size_kb:.1f} KB) -> {path}")
            downloaded.append(os.path.abspath(path))
        except Exception as e:
            print(f"  FAILED: {e}")

        time.sleep(0.6)

    print("\n" + "=" * 60)
    print(f"Done! Downloaded {len(downloaded)} / {limit} images")
    print(f"Output directory: {os.path.abspath(args.out)}")


if __name__ == "__main__":
    main()
