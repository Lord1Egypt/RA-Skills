#!/usr/bin/env python3
"""Phase 3 helper: merge evaluation outputs from GLM and Codex.

Takes two evaluation JSON files and produces merged recommendations
with confidence scores and agreement tracking.

Usage:
  python3 scripts/merge_evaluations.py --eval-a PATH --eval-b PATH --output PATH
"""

from __future__ import annotations

import json
import argparse
from pathlib import Path


def merge(eval_a: list[dict], eval_b: list[dict], confidence_threshold: float = 0.7) -> list[dict]:
    """Merge two evaluation lists into deduplicated recommendations."""
    by_target: dict[str, list[dict]] = {}

    for entry in eval_a:
        key = entry.get("target", "") + "|" + entry.get("type", "")
        by_target.setdefault(key, []).append({**entry, "_source": "eval-a"})

    for entry in eval_b:
        key = entry.get("target", "") + "|" + entry.get("type", "")
        by_target.setdefault(key, []).append({**entry, "_source": "eval-b"})

    merged: list[dict] = []
    rec_id = 0

    for key, entries in by_target.items():
        sources = list({e["_source"] for e in entries})
        agreed = len(sources) > 1

        # Take the entry with higher confidence, or first one
        best = max(entries, key=lambda e: e.get("confidence", 0.5))
        confidence = best.get("confidence", 0.5)

        if agreed:
            confidence = min(confidence + 0.1, 1.0)

        if confidence < confidence_threshold:
            continue

        rec_id += 1
        merged.append({
            "id": f"rec-{rec_id:03d}",
            "type": best.get("type", "refactor"),
            "severity": _classify_severity(confidence),
            "target": best.get("target", ""),
            "title": best.get("title", ""),
            "rationale": best.get("rationale", ""),
            "proposed_action": best.get("proposed_action", ""),
            "confidence": round(confidence, 2),
            "agreed_by": sources,
        })

    merged.sort(key=lambda r: -r["confidence"])
    return merged


def _classify_severity(confidence: float) -> str:
    if confidence >= 0.85:
        return "green"
    if confidence >= 0.7:
        return "yellow"
    return "red"


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge evaluation outputs")
    parser.add_argument("--eval-a", type=Path, required=True)
    parser.add_argument("--eval-b", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--threshold", type=float, default=0.7)
    args = parser.parse_args()

    a = json.loads(args.eval_a.read_text()) if args.eval_a.exists() else []
    b = json.loads(args.eval_b.read_text()) if args.eval_b.exists() else []
    result = merge(a, b, confidence_threshold=args.threshold)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2))
    print(f"Merged {len(result)} recommendations above threshold {args.threshold}")


if __name__ == "__main__":
    main()
