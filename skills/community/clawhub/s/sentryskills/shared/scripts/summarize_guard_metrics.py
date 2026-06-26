#!/usr/bin/env python3
"""Summarize self-guard metrics from index.jsonl."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, List


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Summarize self-guard index metrics")
    p.add_argument("index_log", help="Path to index.jsonl")
    p.add_argument("--out", default="", help="Optional output JSON path")
    return p.parse_args()


def read_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def pct(part: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return round(part * 100.0 / total, 2)


def action_rates(rows: List[Dict[str, Any]]) -> Dict[str, float]:
    total = len(rows)
    cnt = Counter(str(r.get("final_action", "unknown")) for r in rows)
    intercept = cnt.get("downgrade", 0) + cnt.get("block", 0)
    return {
        "allow_rate": pct(cnt.get("allow", 0), total),
        "downgrade_rate": pct(cnt.get("downgrade", 0), total),
        "block_rate": pct(cnt.get("block", 0), total),
        "intercept_rate": pct(intercept, total),
    }


def build_group_summary(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(rows)
    cnt = Counter(str(r.get("final_action", "unknown")) for r in rows)
    durations = [int(r.get("duration_ms", 0)) for r in rows]
    retry_hits = sum(1 for r in rows if "RT_RETRY_THRESHOLD" in set(r.get("reason_codes", [])))
    return {
        "total_turns": total,
        "action_counts": dict(cnt),
        "rates_percent": action_rates(rows),
        "decision_latency_ms": {
            "avg": round(mean(durations), 2) if durations else 0.0,
            "max": max(durations) if durations else 0,
            "min": min(durations) if durations else 0,
        },
        "retry_rate": pct(retry_hits, total),
    }


def main() -> None:
    args = parse_args()
    path = Path(args.index_log).resolve()
    if not path.exists():
        raise FileNotFoundError(f"index log not found: {path}")

    rows = list(read_jsonl(path))
    total = len(rows)
    if total == 0:
        print("No records.")
        return

    reason_counter = Counter()
    by_policy = defaultdict(list)
    by_session = defaultdict(list)

    for r in rows:
        by_policy[str(r.get("policy_profile", "unknown"))].append(r)
        by_session[str(r.get("session_id", "unknown"))].append(r)
        for rc in r.get("reason_codes", []):
            reason_counter[str(rc)] += 1

    summary = {
        "overall": build_group_summary(rows),
        "by_policy_profile": {k: build_group_summary(v) for k, v in sorted(by_policy.items())},
        "by_session": {k: build_group_summary(v) for k, v in sorted(by_session.items())},
        "top_reason_codes": reason_counter.most_common(10),
    }

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if args.out:
        out = Path(args.out).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Saved: {out}")


if __name__ == "__main__":
    main()
