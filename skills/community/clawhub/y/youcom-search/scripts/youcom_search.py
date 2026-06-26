#!/usr/bin/env python3
"""
you.com Free Web Search
No API key required.
"""

import urllib.request
import urllib.parse
import json
import sys
import argparse


def search(query: str, num_results: int = 5) -> dict:
    """Perform a free web search via you.com API."""
    params = {
        "query": query,
        "num_results": min(num_results, 10),
    }
    url = "https://api.you.com/v1/agents/search?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (compatible; OpenClaw/1.0)",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    results = data.get("results", {}).get("web", [])
    return {
        "query": query,
        "count": len(results),
        "results": [
            {
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "description": r.get("description", "")[:300],
                "snippets": r.get("snippets", [])[:2],
            }
            for r in results[:num_results]
        ],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="you.com free web search")
    parser.add_argument("query", help="Search query")
    parser.add_argument(
        "--num", "-n", type=int, default=5, help="Number of results (default: 5, max: 10)"
    )
    parser.add_argument(
        "--out", "-o", help="Write output to file instead of stdout"
    )
    args = parser.parse_args()

    try:
        result = search(args.query, args.num)
        output = json.dumps(result, indent=2, ensure_ascii=False)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(output)
        else:
            print(output)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)
