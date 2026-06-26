#!/usr/bin/env python3
"""
RA-Skills registry updater.

Discovers NEW community skills from upstream sources and appends their metadata
to registry.json (it does not re-download content — bulk_download.py does that).
Designed to run on a schedule (see .github/workflows/update-registry.yml).

Currently enumerates ClawHub (cursor-paginated API, the largest source). Other
sources have no central listing API and are synced when their catalogs change.

Usage:
  CLAWHUB_TOKEN=<token> python3 tools/update_registry.py
  python3 tools/update_registry.py --dry-run
  python3 tools/update_registry.py --max-pages 5     # limit enumeration (testing)

Exit code 0 always; prints how many new skills were added. The workflow checks
`git status` to decide whether to commit.
"""
import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
REGISTRY = ROOT / "registry.json"
CLAWHUB_API = "https://clawhub.ai/api/v1"
CLAWHUB_TOKEN = os.environ.get("CLAWHUB_TOKEN", "")


def _headers():
    h = {"User-Agent": "RA-Skills-updater/1.0 (Mozilla/5.0 compatible)"}
    if CLAWHUB_TOKEN:
        h["Authorization"] = f"Bearer {CLAWHUB_TOKEN}"
    return h


def _get(url, retries=3, timeout=30):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=_headers())
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read())
        except Exception:
            time.sleep(1.5 * (attempt + 1))
    return None


def clawhub_entry(item):
    """Map a ClawHub list item to an RA-Skills registry entry."""
    slug = item.get("slug", "")
    topics = item.get("topics") or []
    tags = item.get("tags") or []
    if isinstance(tags, dict):
        tags = [k for k in tags if k != "latest"]
    category = (topics[0] if topics else (tags[0] if tags else "community")).lower()
    lv = item.get("latestVersion")
    version = lv.get("version") if isinstance(lv, dict) else ""
    return {
        "name": item.get("displayName") or slug,
        "description": item.get("summary") or "",
        "category": category,
        "categoryLabel": category.replace("-", " ").title(),
        "source": "ClawHub",
        "tags": sorted(str(t) for t in tags),
        "platforms": [],
        "author": "",
        "version": version or "",
        "license": "",
        "installCmd": f"hermes skills install clawhub/{slug}",
        "sourceUrl": f"https://clawhub.ai/skills/{slug}",
        "identifier": slug,
    }


def enumerate_clawhub(max_pages=0):
    """Yield all ClawHub list items via cursor pagination."""
    cursor = None
    pages = 0
    while True:
        params = {"limit": "100"}
        if cursor:
            params["cursor"] = cursor
        data = _get(f"{CLAWHUB_API}/skills?{urllib.parse.urlencode(params)}")
        if not isinstance(data, dict):
            break
        items = data.get("items") or []
        for it in items:
            if it.get("slug"):
                yield it
        cursor = data.get("nextCursor")
        pages += 1
        if not cursor or not items:
            break
        if max_pages and pages >= max_pages:
            break
        time.sleep(0.1)


def main():
    ap = argparse.ArgumentParser(description="Discover & add new community skills to registry.json")
    ap.add_argument("--dry-run", action="store_true", help="Don't write registry.json")
    ap.add_argument("--max-pages", type=int, default=0, help="Cap ClawHub pages (0=all)")
    args = ap.parse_args()

    if not REGISTRY.exists():
        print(f"registry.json not found at {REGISTRY}", file=sys.stderr)
        sys.exit(1)

    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    skills = data.get("skills", [])
    existing = {s.get("identifier") for s in skills if s.get("source") == "ClawHub"}
    print(f"Registry: {len(skills):,} skills ({len(existing):,} ClawHub). Enumerating ClawHub...")

    seen = 0
    new_entries = []
    for item in enumerate_clawhub(args.max_pages):
        seen += 1
        if item["slug"] not in existing:
            new_entries.append(clawhub_entry(item))
            existing.add(item["slug"])
        if seen % 2000 == 0:
            print(f"  scanned {seen:,} | new so far {len(new_entries):,}")

    print(f"Scanned {seen:,} ClawHub skills; {len(new_entries):,} are NEW.")

    if not new_entries:
        print("Registry already up to date.")
        return

    if args.dry_run:
        print("DRY RUN — not writing. Sample new:", [e['identifier'] for e in new_entries[:5]])
        return

    skills.extend(new_entries)
    data["skills"] = skills
    data["community"] = data.get("community", 0) + len(new_entries)
    data["total"] = data.get("total", 0) + len(new_entries)
    REGISTRY.write_text(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    print(f"Added {len(new_entries):,} new skills. Registry now {data['total']:,} total.")


if __name__ == "__main__":
    main()
