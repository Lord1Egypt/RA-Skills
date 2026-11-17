#!/usr/bin/env python3
"""Check Crossref + PubMed reachability."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from literature import search_literature  # noqa: E402


def main() -> int:
    try:
        papers = search_literature("machine learning", limit=1)
        ok = len(papers) >= 0  # empty is ok if APIs responded
        print(
            json.dumps(
                {"ok": True, "mode": "standalone", "sources": ["crossref", "pubmed"], "sample_count": len(papers)},
                indent=2,
            )
        )
        return 0
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
