#!/usr/bin/env python3
"""arXiv search script for Claude Code skill."""

import argparse
import json
import sys
from pathlib import Path

# Add src to path (scripts -> arxiv-search -> skills -> .claude -> project root)
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from arxiv_client import ArxivClient


def main():
    parser = argparse.ArgumentParser(description="Search arXiv papers")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--max-results", type=int, default=10, help="Max results")
    parser.add_argument(
        "--sort-by",
        choices=["relevance", "submitted_date", "last_updated"],
        default="relevance",
        help="Sort criterion",
    )
    parser.add_argument("--category", help="arXiv category filter (e.g., cs.AI)")
    parser.add_argument("--date-from", help="Filter from date (YYYY-MM-DD)")
    parser.add_argument("--date-to", help="Filter until date (YYYY-MM-DD)")
    parser.add_argument(
        "--output",
        choices=["json", "text"],
        default="text",
        help="Output format",
    )

    args = parser.parse_args()

    client = ArxivClient()

    try:
        results = client.search(
            query=args.query,
            max_results=args.max_results,
            sort_by=args.sort_by,
            category=args.category,
            date_from=args.date_from,
            date_to=args.date_to,
        )
    except Exception as e:
        print(f"Error searching arXiv: {e}", file=sys.stderr)
        sys.exit(1)

    if not results:
        print("No papers found matching your query.")
        sys.exit(0)

    if args.output == "json":
        output = [r.to_dict() for r in results]
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(f"\nFound {len(results)} papers:\n")
        print("=" * 70)

        for i, r in enumerate(results, 1):
            # Truncate abstract for display
            abstract = r.abstract[:200].replace("\n", " ")
            if len(r.abstract) > 200:
                abstract += "..."

            # Truncate author list
            authors = r.authors[:3]
            if len(r.authors) > 3:
                authors_str = ", ".join(authors) + f" (+{len(r.authors) - 3} more)"
            else:
                authors_str = ", ".join(authors)

            print(f"[{i}] {r.title}")
            print(f"    arXiv ID  : {r.arxiv_id}")
            print(f"    Authors   : {authors_str}")
            print(f"    Published : {r.published.strftime('%Y-%m-%d')}")
            print(f"    Categories: {', '.join(r.categories)}")
            print(f"    Abstract  : {abstract}")
            print(f"    PDF       : {r.pdf_url}")
            print("-" * 70)

        print(
            "\nTo add papers to Zotero, use the zotero-add skill with the arxiv_id."
        )


if __name__ == "__main__":
    main()
