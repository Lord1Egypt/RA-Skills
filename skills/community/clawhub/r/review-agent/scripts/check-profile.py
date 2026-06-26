#!/usr/bin/env python3
"""check-profile.py — detect unfilled template placeholders in a Responder profile.

Scans a profile.md for leftover placeholder patterns (<e.g., …>, <your name>,
<open_id>, etc.). Emits a short report and a non-zero exit code if any are
found. Used by install.sh Phase B and new-session.sh to warn before a review
runs with a half-configured profile.

Usage:
  check-profile.py <profile_path>                    # verbose report
  check-profile.py <profile_path> --quiet            # only non-zero on findings
  check-profile.py <profile_path> --format=json

Exit codes:
  0 — clean
  1 — placeholders found
  2 — file missing or unreadable
"""
import argparse
import json
import re
import sys
from pathlib import Path


# Patterns that indicate an unfilled template placeholder.
# Deliberately conservative: we only flag forms the template itself uses.
PATTERNS = [
    (re.compile(r"<e\.g\.,?[^>]{0,200}>", re.I | re.S), "example-placeholder"),
    (re.compile(r"<your\s+[^>]{1,60}>",    re.I),       "your-<…>-placeholder"),
    (re.compile(r"<open_?id>",             re.I),       "<open_id> placeholder"),
    (re.compile(r"<name\s*/\s*role>",      re.I),       "<name/role> placeholder"),
    (re.compile(r"<subjects\s+they[^>]{0,80}>", re.I),  "<subjects they…> placeholder"),
    (re.compile(r"<notes>",                re.I),       "<notes> placeholder"),
]


def scan(text: str):
    hits = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for pat, label in PATTERNS:
            for m in pat.finditer(line):
                snippet = m.group(0)
                if len(snippet) > 80:
                    snippet = snippet[:77] + "…"
                hits.append({"line": lineno, "label": label, "snippet": snippet})
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("profile_path")
    ap.add_argument("--quiet", action="store_true",
                    help="suppress human-readable output; only set exit code")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args()

    p = Path(args.profile_path)
    if not p.exists():
        if args.format == "json":
            print(json.dumps({"error": f"file not found: {p}"}))
        else:
            print(f"error: file not found: {p}", file=sys.stderr)
        sys.exit(2)

    hits = scan(p.read_text())

    if args.format == "json":
        print(json.dumps({
            "profile": str(p),
            "placeholders_found": len(hits),
            "hits": hits,
        }, indent=2, ensure_ascii=False))
        sys.exit(1 if hits else 0)

    if not hits:
        if not args.quiet:
            print(f"\033[0;32m✓\033[0m profile looks filled in: {p}")
        sys.exit(0)

    if not args.quiet:
        print(f"\033[0;33m!\033[0m profile still contains {len(hits)} template placeholder(s):")
        print(f"  {p}")
        for h in hits[:10]:
            print(f"    line {h['line']:>3}  [{h['label']}]  {h['snippet']}")
        if len(hits) > 10:
            print(f"    … and {len(hits)-10} more")
        print()
        print("  → review quality will be generic until you edit these.")
        print(f"  → vim {p}")
    sys.exit(1)


if __name__ == "__main__":
    main()
