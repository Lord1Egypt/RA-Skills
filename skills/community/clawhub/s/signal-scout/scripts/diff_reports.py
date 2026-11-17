#!/usr/bin/env python3
"""Diff signal-scout analysis.json snapshots across a product's full run history.

Watch mode re-runs the search phase for a product on a schedule and should
only surface what changed — re-showing the same 10 prospects every week
trains the user to ignore the report. Comparing only the two most recent
snapshots isn't enough for that: a prospect seen in week 1, absent in week 2,
then resurfacing in week 3 would read as "new" again against week 2 alone —
the tool would have no memory past one hop back. This script checks a
prospect's full run history instead, so "new" means genuinely never seen
before across every snapshot given, not just absent last time.

Prospects are matched by (type, name, source_url) — same person/segment
citing a new source counts as new evidence, not a duplicate. Snapshots are
ordered by each file's `generated_at` field, not by argument order or
filename, so passing paths out of order is harmless.

Usage:
    python3 diff_reports.py outputs/<slug>/analysis-*.json [--json]
    python3 diff_reports.py previous.json current.json                        # 2-file case still works
    python3 diff_reports.py outputs/<slug>/analysis-*.json --outcomes outputs/<slug>/outcomes.jsonl
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

SINGULAR = {"individuals": "individual", "segments": "segment", "companies": "company"}


def prospect_key(kind: str, item: dict[str, Any]) -> tuple[str, str, str]:
    return (kind, str(item.get("name", "")).strip().lower(), str(item.get("source_url", "")).strip())


def load_prospects(data: dict[str, Any]) -> dict[tuple[str, str, str], dict[str, Any]]:
    out: dict[tuple[str, str, str], dict[str, Any]] = {}
    for kind in ("individuals", "segments", "companies"):
        for item in data.get(kind) or []:
            if isinstance(item, dict):
                out[prospect_key(kind, item)] = item
    return out


def load_patterns(data: dict[str, Any]) -> dict[str, int]:
    out: dict[str, int] = {}
    for pattern in data.get("patterns") or []:
        if isinstance(pattern, dict):
            title = str(pattern.get("title", "")).strip()
            if title:
                out[title] = int(pattern.get("count") or 0)
    return out


def accumulate_history(
    snapshots: list[tuple[Path, dict[str, Any]]],
) -> tuple[dict[tuple[str, str, str], dict[str, Any]], dict[tuple[str, str, str], int], dict[tuple[str, str, str], str]]:
    """Fold chronologically-ordered (path, snapshot) pairs into everything ever
    seen: (prospect_by_key, times_seen, first_seen_at). Shared between this
    script's own history/current split and generate_report.py's novelty
    badges, so both compute "have we seen this before" the same way."""
    history_prospects: dict[tuple[str, str, str], dict[str, Any]] = {}
    first_seen: dict[tuple[str, str, str], str] = {}
    times_seen: dict[tuple[str, str, str], int] = {}
    for path, snapshot in snapshots:
        generated_at = str(snapshot.get("generated_at", path.stem))
        for key, item in load_prospects(snapshot).items():
            history_prospects[key] = item
            times_seen[key] = times_seen.get(key, 0) + 1
            first_seen.setdefault(key, generated_at)
    return history_prospects, times_seen, first_seen


class OutcomeIndex:
    """Look up a logged outcome by (name, source_url), falling back to name alone.

    log_outcome.py's --source-url is optional, so most historical records may
    not have one — the precise key disambiguates same-name prospects when
    it's available; the name-only fallback is best-effort otherwise and can
    collide across different prospects with the same name.
    """

    def __init__(self, path: Path | None) -> None:
        self.by_name_and_url: dict[tuple[str, str], dict[str, Any]] = {}
        self.by_name: dict[str, dict[str, Any]] = {}
        if not path or not path.exists():
            return
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            name = str(row.get("name", "")).strip().lower()
            if not name:
                continue
            date = str(row.get("date", ""))
            url = str(row.get("source_url", "")).strip()
            if url:
                # A url-tagged record only ever satisfies the exact (name, url) match —
                # it must not also populate the name-only fallback, or it would leak
                # onto a different prospect that merely shares this name.
                existing = self.by_name_and_url.get((name, url))
                if not existing or date >= str(existing.get("date", "")):
                    self.by_name_and_url[(name, url)] = row
            else:
                existing = self.by_name.get(name)
                if not existing or date >= str(existing.get("date", "")):
                    self.by_name[name] = row

    def lookup(self, name: str, url: str) -> dict[str, Any] | None:
        return self.by_name_and_url.get((name, url)) or self.by_name.get(name)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("snapshots", type=Path, nargs="+", help="2+ analysis.json paths, any order — sorted by generated_at")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON instead of a text summary")
    parser.add_argument("--outcomes", type=Path, help="outcomes.jsonl — flag resurfacing prospects that already have a logged outcome")
    args = parser.parse_args()

    if len(args.snapshots) < 2:
        parser.error("need at least 2 snapshots to diff")

    loaded = [(path, json.loads(path.read_text(encoding="utf-8"))) for path in args.snapshots]
    loaded.sort(key=lambda pair: str(pair[1].get("generated_at", "")))
    *history, (_current_path, current) = loaded

    history_prospects, times_seen, first_seen = accumulate_history(history)

    immediately_prior = load_prospects(history[-1][1])
    curr_prospects = load_prospects(current)
    outcomes = OutcomeIndex(args.outcomes)

    new_keys = set(curr_prospects) - set(history_prospects)
    recurring_keys = set(curr_prospects) & set(history_prospects)
    dropped_keys = set(immediately_prior) - set(curr_prospects)

    def annotate(key: tuple[str, str, str], item: dict[str, Any]) -> dict[str, Any]:
        out = dict(item)
        out["_type"] = key[0]
        record = outcomes.lookup(key[1], key[2])
        if record:
            out["_prior_outcome"] = f"{record.get('outcome', '?')} on {record.get('date', '?')}"
        return out

    new_prospects = [annotate(k, curr_prospects[k]) for k in new_keys]
    recurring_prospects = [
        annotate(k, curr_prospects[k]) | {"_times_seen": times_seen[k] + 1, "_first_seen": first_seen[k]}
        for k in recurring_keys
    ]
    dropped_prospects = [annotate(k, immediately_prior[k]) for k in dropped_keys]

    prev_patterns = load_patterns(history[-1][1])
    curr_patterns = load_patterns(current)
    grown_patterns = [
        {"title": title, "previous_count": prev_patterns.get(title, 0), "current_count": count}
        for title, count in curr_patterns.items()
        if count > prev_patterns.get(title, 0)
    ]

    if args.json:
        print(json.dumps({
            "new_prospects": new_prospects,
            "recurring_prospects": recurring_prospects,
            "dropped_prospects": dropped_prospects,
            "grown_patterns": grown_patterns,
        }, indent=2))
        return

    if not new_prospects and not recurring_prospects and not dropped_prospects and not grown_patterns:
        print("No changes since the previous snapshot.")
        return

    if new_prospects:
        print(f"NEW — never seen in {len(history)} prior snapshot(s) ({len(new_prospects)}):")
        for item in sorted(new_prospects, key=lambda x: -int(x.get("score") or 0)):
            label = SINGULAR.get(item["_type"], item["_type"])
            flag = f" [already logged: {item['_prior_outcome']}]" if "_prior_outcome" in item else ""
            print(f"  [{label}] {item.get('name', '(unnamed)')} — {item.get('score', '?')}/100 — {item.get('pain_signal', '')[:80]}{flag}")
        print()

    if recurring_prospects:
        decided = [p for p in recurring_prospects if "_prior_outcome" in p]
        print(f"RECURRING — already surfaced before, still showing up ({len(recurring_prospects)}):")
        for item in sorted(recurring_prospects, key=lambda x: -int(x.get("score") or 0)):
            label = SINGULAR.get(item["_type"], item["_type"])
            if "_prior_outcome" in item:
                flag = f" — already logged: {item['_prior_outcome']}"
            else:
                flag = f" — seen {item['_times_seen']}x, first {item['_first_seen']}"
            print(f"  [{label}] {item.get('name', '(unnamed)')}{flag}")
        if decided:
            print(f"  ({len(decided)} of these already have a logged outcome — resurfacing without a new "
                  "angle just repeats a decision the user already made)")
        print()

    if dropped_prospects:
        print(f"NO LONGER SURFACED ({len(dropped_prospects)}) — evidence may be stale or superseded:")
        for item in dropped_prospects:
            label = SINGULAR.get(item["_type"], item["_type"])
            print(f"  [{label}] {item.get('name', '(unnamed)')}")
        print()

    if grown_patterns:
        print("PATTERNS GROWING:")
        for pattern in grown_patterns:
            print(f"  {pattern['title']}: {pattern['previous_count']} → {pattern['current_count']}")


if __name__ == "__main__":
    main()
