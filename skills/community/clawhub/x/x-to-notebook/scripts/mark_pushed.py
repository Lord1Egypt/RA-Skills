"""Mark bookmark IDs as pushed to NotebookLM."""

import json
import sys
from pathlib import Path

PUSHED_PATH = Path.home() / ".openclaw" / "data" / "x-bookmarks-pushed.json"


def main():
    if len(sys.argv) < 2:
        print("Usage: mark_pushed.py <id1> [id2] [id3] ...", file=sys.stderr)
        sys.exit(1)

    new_ids = sys.argv[1:]

    existing = set()
    if PUSHED_PATH.exists():
        with open(PUSHED_PATH, "r", encoding="utf-8") as f:
            existing = set(json.load(f))

    existing.update(new_ids)

    PUSHED_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PUSHED_PATH, "w", encoding="utf-8") as f:
        json.dump(sorted(existing), f, indent=2)

    print(f"Marked {len(new_ids)} bookmark(s) as pushed (total: {len(existing)})")


if __name__ == "__main__":
    main()
