#!/usr/bin/env python3
"""
compare_profiles.py — Build a comparison table or CSV from multiple creator profiles.

Usage:
    python3 compare_profiles.py --profiles '<json array>' --format table
    python3 compare_profiles.py --profiles '<json array>' --format csv --output ~/comparison.csv
"""

import argparse
import csv
import io
import json
import sys


COMPARE_FIELDS = [
    ("handle",             lambda p: p.get("handle", "")),
    ("platform",           lambda p: p.get("platform", "")),
    ("display_name",       lambda p: p.get("display_name", "")),
    ("verified",           lambda p: "✅" if p.get("verified") else "❌"),
    ("followers",          lambda p: _fmt(p.get("stats", {}).get("followers"))),
    ("subscribers",        lambda p: _fmt(p.get("stats", {}).get("subscribers"))),
    ("total_posts",        lambda p: _fmt(p.get("stats", {}).get("total_posts"))),
    ("total_views",        lambda p: _fmt(p.get("stats", {}).get("total_views"))),
    ("engagement_rate",    lambda p: f"{p.get('stats', {}).get('engagement_rate', '')}%" if p.get("stats", {}).get("engagement_rate") is not None else ""),
    ("website",            lambda p: p.get("contact_info", {}).get("website", "")),
]


def _fmt(n) -> str:
    if n is None:
        return ""
    if n >= 1_000_000_000:
        return f"{n / 1_000_000_000:.1f}B"
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def build_rows(profiles: list[dict]) -> tuple[list[str], list[list[str]]]:
    headers = [f[0] for f in COMPARE_FIELDS]
    rows = []
    for p in profiles:
        rows.append([extractor(p) or "" for _, extractor in COMPARE_FIELDS])
    return headers, rows


def render_table(headers: list[str], rows: list[list[str]]) -> str:
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(cell))

    def fmt_row(cells):
        return "| " + " | ".join(c.ljust(col_widths[i]) for i, c in enumerate(cells)) + " |"

    sep = "| " + " | ".join("-" * w for w in col_widths) + " |"
    lines = [fmt_row(headers), sep] + [fmt_row(row) for row in rows]
    return "\n".join(lines)


def render_csv(headers: list[str], rows: list[list[str]]) -> str:
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(headers)
    w.writerows(rows)
    return out.getvalue()


def main():
    parser = argparse.ArgumentParser(description="Compare creator profiles.")
    parser.add_argument("--profiles", required=True, help="JSON array of profile objects")
    parser.add_argument("--format", choices=["table", "csv"], default="table")
    parser.add_argument("--output", default=None, help="Output file path (optional)")
    args = parser.parse_args()

    try:
        profiles = json.loads(args.profiles)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON — {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(profiles, list):
        print("Error: --profiles must be a JSON array", file=sys.stderr)
        sys.exit(1)

    headers, rows = build_rows(profiles)

    if args.format == "table":
        output = render_table(headers, rows)
    else:
        output = render_csv(headers, rows)

    if args.output:
        from pathlib import Path
        p = Path(args.output).expanduser().resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(output, encoding="utf-8")
        print(f"Saved: {p}")
    else:
        print(output)


if __name__ == "__main__":
    main()
