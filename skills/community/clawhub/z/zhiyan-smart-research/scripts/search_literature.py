#!/usr/bin/env python3
"""Search Crossref + PubMed. Output JSON for OpenClaw agent synthesis."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from literature import search_literature  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Smart Research literature search")
    parser.add_argument("query", nargs="+", help="Search query")
    parser.add_argument("--limit", type=int, default=10, help="Max papers (default 10)")
    parser.add_argument("--compact", action="store_true", help="Omit abstracts in output")
    args = parser.parse_args()
    query = " ".join(args.query).strip()
    if not query:
        print("Query is required", file=sys.stderr)
        return 1
    papers = search_literature(query, limit=args.limit)
    if args.compact:
        for p in papers:
            p.pop("abstract", None)
    out = {"query": query, "count": len(papers), "sources": ["crossref", "pubmed"], "papers": papers}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
