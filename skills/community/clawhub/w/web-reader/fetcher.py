#!/usr/bin/env python3
"""Web Reader - Smart web content fetcher with archive support."""
import argparse
import json
import os
import sys

from lib.router import route
from lib.article import fetch_article
from lib.video import fetch_video
from lib.feishu import fetch_feishu


def main():
    parser = argparse.ArgumentParser(description="Fetch articles and download videos")
    parser.add_argument("url", nargs="?", help="URL to fetch")
    parser.add_argument("-o", "--output", default=".", help="Output directory")
    parser.add_argument("-q", "--quality", default="1080", help="Video quality (default: 1080)")
    parser.add_argument("--method", choices=["scrapling", "camoufox", "ytdlp", "feishu"], help="Force method")
    parser.add_argument("--selector", help="Force CSS selector")
    parser.add_argument("--urls-file", help="File with URLs (one per line)")
    parser.add_argument("--audio-only", action="store_true", help="Extract audio only (video)")
    parser.add_argument("--no-images", action="store_true", help="Skip image download (article)")
    parser.add_argument("--cookies-browser", help="Browser for cookies (e.g., chrome, firefox)")
    parser.add_argument("--category", help="Archive category subfolder name")
    parser.add_argument("--json-output", action="store_true", help="Output result as JSON (for programmatic use)")
    args = parser.parse_args()

    urls = []
    if args.urls_file:
        with open(args.urls_file) as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    elif args.url:
        urls = [args.url]
    else:
        parser.print_help()
        sys.exit(1)

    output_dir = args.output
    if args.category:
        output_dir = os.path.join(output_dir, args.category)
    os.makedirs(output_dir, exist_ok=True)

    results = []
    for url in urls:
        r = route(url)
        if args.method:
            r["method"] = args.method
        if args.selector:
            r["selector"] = args.selector

        if not args.json_output:
            print(f"\n{'='*60}")
            print(f"URL: {url}")
            print(f"Route: type={r['type']}, method={r['method']}")
            print(f"{'='*60}")

        if r["type"] == "video":
            result = fetch_video(url, output_dir, quality=args.quality,
                                 audio_only=args.audio_only,
                                 cookies_browser=args.cookies_browser)
        elif r["method"] == "feishu":
            result = fetch_feishu(url, output_dir, no_images=args.no_images)
        else:
            result = fetch_article(url, output_dir, r, no_images=args.no_images)

        results.append({"url": url, "type": r["type"], "method": r["method"],
                        "output": result, "category": args.category})

    if args.json_output:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(f"\n{'='*60}")
        print("Summary:")
        for item in results:
            status = item["output"] if item["output"] else "FAILED"
            print(f"  {item['url']} → {status}")
        print(f"{'='*60}")


if __name__ == "__main__":
    main()
