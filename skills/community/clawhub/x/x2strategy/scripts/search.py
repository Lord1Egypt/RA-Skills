#!/usr/bin/env python3
"""search.py — Search for quantitative finance papers.

Usage:
    python scripts/search.py "momentum trading strategy"
    python scripts/search.py "pairs trading volatility" --sources arxiv ssrn -n 5
    python scripts/search.py "mean reversion" -o results.json

Output: JSON array of search results.
"""

import argparse
import json
import logging
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from paper2spec.search import search


def main():
    parser = argparse.ArgumentParser(description="Search for quantitative finance papers.")
    parser.add_argument("query", help="Search query")
    parser.add_argument(
        "-n", "--max-results",
        type=int, default=10,
        help="Max results per source (default: 10)",
    )
    parser.add_argument(
        "--sources",
        nargs="+",
        default=["arxiv"],
        help="Sources to search (default: arxiv). Options: arxiv, ssrn",
    )
    parser.add_argument("-o", "--output", help="Output JSON path")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )

    results = search(args.query, max_results=args.max_results, sources=args.sources)

    output = [r.to_dict() for r in results]

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"✅ Wrote {len(results)} results to {args.output}")
    else:
        # Print summary to stdout
        for i, r in enumerate(results, 1):
            print(f"\n[{i}] {r.title}")
            print(f"    Source: {r.source} | {r.published}")
            print(f"    URL: {r.url}")
            if r.abstract:
                print(f"    Abstract: {r.abstract[:150]}...")

    print(f"\nTotal: {len(results)} results")


if __name__ == "__main__":
    main()
