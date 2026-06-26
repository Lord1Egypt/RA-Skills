#!/usr/bin/env python3
"""
you.com Deep Research
Requires YOUCOM_API_KEY environment variable.
"""

import urllib.request
import json
import sys
import os
import argparse


def research(query: str, depth: str = "standard", api_key: str = None) -> dict:
    """Perform deep research via you.com API."""
    if not api_key:
        api_key = os.environ.get("YOUCOM_API_KEY")
    if not api_key:
        raise ValueError("YOUCOM_API_KEY environment variable is not set")

    payload = json.dumps({"input": query, "research_effort": depth}).encode("utf-8")
    req = urllib.request.Request(
        "https://api.you.com/v1/research",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "X-API-Key": api_key,
            "User-Agent": "Mozilla/5.0 (compatible; OpenClaw/1.0)",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="you.com deep research")
    parser.add_argument("query", help="Research topic")
    parser.add_argument(
        "--depth",
        "-d",
        choices=["lite", "standard", "deep", "exhaustive"],
        default="standard",
        help="Research effort level (default: standard)",
    )
    parser.add_argument(
        "--out", "-o", help="Write output to file instead of stdout"
    )
    args = parser.parse_args()

    try:
        result = research(args.query, args.depth)
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
