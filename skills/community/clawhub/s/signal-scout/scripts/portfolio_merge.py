#!/usr/bin/env python3
"""Cross-reference signal-scout reports across multiple products.

For a founder or agency running several products, the same person, community,
or company can show up as a prospect in more than one product's research —
e.g. a Reddit user who'd want both a meal-planning app and a budgeting app, or
a company whose hiring signal is relevant to two different B2B tools. That
overlap is a real signal: it means one outreach conversation could open the
door for multiple products, or that a segment is worth a shared content push.

This script does ONLY the deterministic part: it groups prospects across N
analysis.json files by exact match on source_url or normalized name, and
reports groups that appear in 2+ products. It does not re-score, re-rank, or
judge fit across products — that comparison is a judgment call for whoever
reads the output.

Each product argument may be a single file or a glob matching every snapshot
saved for that product (per the SKILL.md storage convention); cross-referencing
runs against the full cumulative set of prospects ever seen for that product
(reusing diff_reports.py's own history accumulation), not just its latest
snapshot — a prospect dropped from product A's most recent run can still be
worth surfacing if it's currently live in product B's.

Usage:
    python3 portfolio_merge.py productA/analysis.json productB/analysis.json ...
    python3 portfolio_merge.py --label "Shelfie=a.json" --label "Budgetly=b.json"
    python3 portfolio_merge.py "outputs/shelfie/analysis-*.json" "outputs/budgetly/analysis-*.json"
    python3 portfolio_merge.py a.json b.json c.json --out merged.json
"""

from __future__ import annotations

import argparse
import glob
import json
import re
from pathlib import Path
from typing import Any

import diff_reports


def normalize_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(name or "").strip().lower()).strip()


def load_report(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_paths(pattern: str) -> list[Path]:
    """A plain path or a glob — either way, every matching file, sorted.
    glob.glob() already returns a literal path unchanged when it exists and
    has no metacharacters, so this is one code path for both the old
    single-file case and the new multi-snapshot-per-product case."""
    matches = sorted(Path(p) for p in glob.glob(pattern))
    if not matches:
        raise SystemExit(f"No files matched: {pattern!r}")
    return matches


def parse_labeled_args(raw_labels: list[str], positional: list[str]) -> list[tuple[str, list[Path]]]:
    products: list[tuple[str, list[Path]]] = []
    for entry in raw_labels:
        if "=" not in entry:
            raise SystemExit(f"--label must be NAME=path, got: {entry!r}")
        label, _, pattern = entry.partition("=")
        products.append((label.strip(), resolve_paths(pattern.strip())))
    for pattern in positional:
        paths = resolve_paths(pattern)
        loaded = [(p, load_report(p)) for p in paths]
        latest_path, latest_data = max(loaded, key=lambda pair: str(pair[1].get("generated_at", pair[0].stem)))
        label = str(latest_data.get("title") or latest_path.stem)
        products.append((label, paths))
    return products


def build_cross_references(
    products: list[tuple[str, dict[tuple[str, str, str], dict[str, Any]]]],
) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str], dict[str, Any]] = {}

    for label, prospects in products:
        for (kind, _norm_name, url), item in prospects.items():
            name = str(item.get("name", "")).strip()
            keys = set()
            if url:
                keys.add(("url", url))
            norm = normalize_name(name)
            if norm:
                keys.add(("name", norm))
            if not keys:
                continue
            for key in keys:
                group = groups.setdefault(key, {"kind": kind, "name": name, "appearances": []})
                group["appearances"].append({
                    "product": label,
                    "score": item.get("score"),
                    "stage": item.get("stage"),
                    "why_fit": item.get("why_fit") or item.get("content_angle") or item.get("bd_angle") or "",
                    "source_url": url,
                })

    # Merge groups that share either key but describe the same prospect (e.g. matched
    # by url in one pass and by name in another) by deduping on (kind, name, url) triples
    # already captured per-appearance, then keep only groups spanning 2+ distinct products.
    merged: list[dict[str, Any]] = []
    seen_appearance_sets: list[frozenset] = []
    for group in groups.values():
        distinct_products = {a["product"] for a in group["appearances"]}
        if len(distinct_products) < 2:
            continue
        signature = frozenset((a["product"], a["source_url"]) for a in group["appearances"])
        if signature in seen_appearance_sets:
            continue
        seen_appearance_sets.append(signature)
        merged.append({
            "kind": group["kind"],
            "name": group["name"],
            "products": sorted(distinct_products),
            "appearances": group["appearances"],
        })

    merged.sort(key=lambda g: len(g["products"]), reverse=True)
    return merged


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "reports", nargs="*",
        help="analysis.json paths or globs (e.g. 'outputs/acme/analysis-*.json'); "
        "label defaults to the latest snapshot's title",
    )
    parser.add_argument("--label", action="append", default=[], help="NAME=path_or_glob, for an explicit label")
    parser.add_argument("--out", type=Path, help="Write the merged cross-reference as JSON")
    args = parser.parse_args()

    if not args.reports and not args.label:
        parser.error("provide at least two report paths (positional or --label NAME=path)")

    entries = parse_labeled_args(args.label, args.reports)
    if len(entries) < 2:
        parser.error("need at least 2 reports to cross-reference")

    products: list[tuple[str, dict[tuple[str, str, str], dict[str, Any]]]] = []
    snapshot_counts: dict[str, int] = {}
    for label, paths in entries:
        loaded = [(p, load_report(p)) for p in paths]
        loaded.sort(key=lambda pair: str(pair[1].get("generated_at", pair[0].stem)))
        history_prospects, _times_seen, _first_seen = diff_reports.accumulate_history(loaded)
        products.append((label, history_prospects))
        snapshot_counts[label] = len(paths)

    cross_refs = build_cross_references(products)

    summary = ", ".join(f"{label} ({snapshot_counts[label]} snapshot(s))" for label, _ in products)
    print(f"{len(products)} products loaded: {summary}\n")
    if not cross_refs:
        print("No prospects overlap across products (matched by source_url or normalized name).")
    else:
        print(f"{len(cross_refs)} prospect(s) appear in 2+ products:\n")
        for group in cross_refs:
            product_list = ", ".join(group["products"])
            print(f"[{group['kind']}] {group['name']} — in {len(group['products'])} products: {product_list}")
            for appearance in group["appearances"]:
                score = appearance.get("score")
                score_str = f"{score}" if score is not None else "?"
                print(f"    {appearance['product']}: score {score_str}, stage {appearance.get('stage', '?')}")
            print()

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "products": [label for label, _ in products],
            "cross_references": cross_refs,
        }
        args.out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"Merged cross-reference written: {args.out.resolve()}")


if __name__ == "__main__":
    main()
