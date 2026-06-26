#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List
from urllib.parse import urlparse

from shared_utils import latest_run_stats, load_json, truncate_cn_note


def _is_http_url(url: str) -> bool:
    u = (url or "").strip()
    if not u:
        return False
    p = urlparse(u)
    return p.scheme in ("http", "https") and bool(p.netloc)


def build_digest(
    scored: List[Dict[str, Any]],
    deep_items: List[Dict[str, Any]],
    run_stats: Dict[str, Any],
    date_s: str,
    other_items: List[Dict[str, Any]] | None = None,
) -> str:
    if other_items is None:
        deep_urls = {x.get("url") for x in deep_items}
        others = [x for x in scored if x.get("url") not in deep_urls]
    else:
        others = other_items

    lines: List[str] = [
        f"# RSS Brew Daily Digest — {date_s}",
        "",
    ]

    if not scored:
        lines += [
            "## No new items today",
            "",
            "Pipeline still ran successfully.",
            "",
        ]
        g = run_stats.get("global", {}) if isinstance(run_stats, dict) else {}
        lines += [
            "### Run Stats",
            f"- total_entries: {g.get('total_entries', 0)}",
            f"- dedup: {g.get('dedup', 0)}",
            f"- old: {g.get('old', 0)}",
            f"- extract_fail: {g.get('extract_fail', 0)}",
            f"- fallback_used: {g.get('fallback_used', 0)}",
            f"- new: {g.get('new', 0)}",
        ]
        return "\n".join(lines) + "\n"

    lines += ["## Deep Set", ""]
    for i, a in enumerate(deep_items, start=1):
        final_score = a.get("final_score", 0.0)
        lines += [
            f"### {i}. {a.get('title','')}",
            f"- Score: {final_score:.2f}",
            f"- Category: {a.get('category','other')}",
            f"- Source: {a.get('source','')}  ",
            f"- URL: {a.get('url','')}",
            f"- English Summary: {a.get('english_summary','')}",
            f"- 中文摘要: {a.get('chinese_summary','')}",
        ]
        # --- UPDATED DEEP ANALYSIS CUTOFF ---
        # Changed from old legacy 'score >= 4' to new 'final_score >= 6.0'
        if final_score >= 6.0 and isinstance(a.get("deep_analysis"), dict):
            d = a["deep_analysis"]
            lines.append("- Deep Analysis:")
            for b in (d.get("paragraph_summaries") or [])[:5]:
                lines.append(f"  - {b}")
            if d.get("underwater_insights"):
                lines.append(f"  - Underwater Insights: {d.get('underwater_insights')}")
            quotes = d.get("golden_quotes") or []
            if quotes:
                lines.append("  - Golden Quotes:")
                for q in quotes[:2]:
                    lines.append(f"    - \"{q}\"")
        # Further Reading from enrichment
        web_context = (a.get("enrichment") or {}).get("web_context") or []
        if isinstance(web_context, list) and web_context:
            fr_lines: List[str] = []
            for w in web_context:
                if not isinstance(w, dict):
                    continue
                title_w = str(w.get("title", "")).strip()
                url_w = str(w.get("url", "")).strip()
                if title_w and _is_http_url(url_w):
                    fr_lines.append(f"  - [{title_w}]({url_w})")
                if len(fr_lines) >= 3:
                    break
            if fr_lines:
                lines.append("- Further Reading:")
                lines.extend(fr_lines)
        lines.append("")

    lines += ["## Other New Articles", ""]
    for a in others:
        note = truncate_cn_note((a.get("summary") or a.get("text") or ""), 160, 220)
        lines += [
            f"- {a.get('title','')}",
            f"  - Score: {a.get('final_score', 0.0):.2f}",
            f"  - Source: {a.get('source','')}",
            f"  - URL: {a.get('url','')}",
            f"  - 备注: {note}",
        ]

    g = run_stats.get("global", {}) if isinstance(run_stats, dict) else {}
    lines += [
        "",
        "## Pipeline Status",
        f"- total_new_articles: {len(scored)}",
        f"- deep_set_count: {len(deep_items)}",
        f"- total_entries_seen: {g.get('total_entries', 0)}",
        f"- dedup_hits: {g.get('dedup', 0)}",
        f"- extraction_fallback_used: {g.get('fallback_used', 0)}",
        f"- extraction_failures: {g.get('extract_fail', 0)}",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description="Write daily digest for RSS-Brew v2")
    ap.add_argument("--scored", required=True)
    ap.add_argument("--deep-set", required=True)
    ap.add_argument("--run-stats-dir", required=True)
    ap.add_argument("--other-set", required=False, help="optional explicit other-set.json (V2)")
    ap.add_argument("--output", required=False)
    ap.add_argument("--data-root", required=False)
    ap.add_argument("--date", required=False)
    args = ap.parse_args()

    scored = (load_json(Path(args.scored), {}) or {}).get("articles", []) or []
    deep_items = (load_json(Path(args.deep_set), {}) or {}).get("articles", []) or []
    other_items = None
    if args.other_set:
        other_items = (load_json(Path(args.other_set), {}) or {}).get("articles", []) or []
    run_stats = latest_run_stats(Path(args.run_stats_dir))

    date_s = args.date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    digest = build_digest(scored, deep_items, run_stats, date_s, other_items=other_items)

    if args.output:
        out_path = Path(args.output)
    elif args.data_root:
        out_path = Path(args.data_root) / "digests" / f"daily-digest-{date_s}.md"
    else:
        raise SystemExit("Provide --output or --data-root")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(digest, encoding="utf-8")
    print(f"[digest] wrote {out_path}")


if __name__ == "__main__":
    main()
