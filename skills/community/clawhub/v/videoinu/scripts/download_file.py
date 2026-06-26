#!/usr/bin/env python3
"""
Download core node files from a graph.

Usage:
    python3 download_file.py GRAPH_ID [--output-dir DIR] [--type image|video|audio]
    python3 download_file.py --urls URL1 URL2 ... [--output-dir DIR]

Output (JSON):
    {
      "output_dir": "/path/to/output",
      "downloaded": ["/path/to/file1.png", ...],
      "total": 3
    }
"""

import argparse
import json
import os
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from _common import require_access_key, api_get, _cookie_header

DEFAULT_OUTPUT_DIR = os.path.expanduser("~/Downloads/videoinu_results")


def download_one(url: str, output_dir: str, prefix: str, index: int) -> str:
    """Download a single URL. Returns local path."""
    # Extract extension from URL
    parsed_path = urllib.parse.urlparse(url).path
    ext = os.path.splitext(parsed_path)[1] or ".bin"
    filename = f"{prefix}_{index:03d}{ext}" if prefix else os.path.basename(parsed_path)
    local_path = os.path.join(output_dir, filename)

    req = urllib.request.Request(url, headers={"Cookie": _cookie_header()})
    with urllib.request.urlopen(req, timeout=120) as resp:
        with open(local_path, "wb") as f:
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                f.write(chunk)
    return local_path


def main():
    parser = argparse.ArgumentParser(description="Download core node files")
    parser.add_argument("graph_id", nargs="?", help="Graph ID to download files from")
    parser.add_argument("--urls", nargs="+", help="Direct URLs to download")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Output directory")
    parser.add_argument("--type", choices=["image", "video", "audio", "all"], default="all",
                        help="Filter by asset type (default: all)")
    parser.add_argument("--prefix", default="", help="File name prefix")
    parser.add_argument("--workers", type=int, default=5, help="Parallel download workers")
    args = parser.parse_args()

    if not args.urls and not args.graph_id:
        parser.error("Either GRAPH_ID or --urls is required")

    require_access_key()
    os.makedirs(args.output_dir, exist_ok=True)

    urls = []

    if args.urls:
        urls = args.urls
    else:
        # Fetch graph and extract URLs from asset core nodes
        data = api_get(f"/graph/{args.graph_id}")
        core_nodes = data.get("core_nodes", [])
        for node in core_nodes:
            if node.get("type") != "asset":
                continue
            asset_data = node.get("data", {})
            asset_type = asset_data.get("asset_type", "")
            if args.type != "all" and asset_type != args.type:
                continue
            url = asset_data.get("url")
            if url:
                urls.append(url)

    if not urls:
        print(json.dumps({"output_dir": args.output_dir, "downloaded": [], "total": 0}))
        return

    # Deduplicate while preserving order
    seen = set()
    unique_urls = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            unique_urls.append(u)

    downloaded = []
    errors = []

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {}
        for i, url in enumerate(unique_urls):
            fut = pool.submit(download_one, url, args.output_dir, args.prefix, i + 1)
            futures[fut] = url

        for fut in futures:
            try:
                path = fut.result()
                downloaded.append(path)
            except Exception as e:
                errors.append({"url": futures[fut], "error": str(e)})

    result = {
        "output_dir": args.output_dir,
        "downloaded": sorted(downloaded),
        "total": len(downloaded),
    }
    if errors:
        result["errors"] = errors

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
