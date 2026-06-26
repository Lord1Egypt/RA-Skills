#!/usr/bin/env python3
"""
you.com Content Extraction
Requires YOUCOM_API_KEY environment variable.
"""

import urllib.request
import json
import sys
import os
import argparse


def extract(urls: list, formats: list = None, crawl_timeout: int = 10, api_key: str = None) -> dict:
    """Extract clean content from URLs via you.com ydc-index API."""
    if not api_key:
        api_key = os.environ.get("YOUCOM_API_KEY")
    if not api_key:
        raise ValueError("YOUCOM_API_KEY environment variable is not set")

    if formats is None:
        formats = ["markdown", "metadata"]

    payload = json.dumps({
        "urls": urls,
        "formats": formats,
        "crawl_timeout": crawl_timeout
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://ydc-index.io/v1/contents",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "X-API-Key": api_key,
            "User-Agent": "Mozilla/5.0 (compatible; OpenClaw/1.0)",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    if isinstance(data, list):
        return {"results": data}
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="you.com content extraction")
    parser.add_argument("urls", nargs="+", help="One or more URLs to extract")
    parser.add_argument(
        "--formats",
        "-f",
        nargs="+",
        default=["markdown", "metadata"],
        choices=["markdown", "html", "metadata"],
        help="Output formats (default: markdown metadata)",
    )
    parser.add_argument(
        "--timeout",
        "-t",
        type=int,
        default=10,
        help="Crawl timeout per URL in seconds (default: 10, max: 60)",
    )
    parser.add_argument(
        "--out", "-o", help="Write output to file instead of stdout"
    )
    args = parser.parse_args()

    try:
        result = extract(args.urls, formats=args.formats, crawl_timeout=args.timeout)
        output = json.dumps(result, indent=2, ensure_ascii=False)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(output)
        else:
            print(output)
    except ValueError as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)
