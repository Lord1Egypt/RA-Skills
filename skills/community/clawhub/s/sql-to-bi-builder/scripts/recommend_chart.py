#!/usr/bin/env python3.11
"""Recommend chart types from inferred semantics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List


def recommend_for_query(query: Dict) -> Dict:
    metrics = query.get("metrics", [])
    dimensions = query.get("dimensions", [])
    time_fields = query.get("time_fields", [])

    if not metrics:
        return {"id": query.get("id"), "chart": "table", "confidence": 0.4, "reason": "No metrics detected"}

    if time_fields:
        return {"id": query.get("id"), "chart": "line", "confidence": 0.85, "reason": "Time field + metrics"}

    if len(dimensions) == 0:
        return {"id": query.get("id"), "chart": "kpi", "confidence": 0.9, "reason": "Aggregate-only result"}

    if len(dimensions) >= 1 and len(metrics) == 1:
        return {"id": query.get("id"), "chart": "bar", "confidence": 0.8, "reason": "One dimension + one metric"}

    if len(dimensions) >= 1 and len(metrics) > 1:
        return {"id": query.get("id"), "chart": "grouped_bar", "confidence": 0.75, "reason": "One or more dimensions + multiple metrics"}

    return {"id": query.get("id"), "chart": "table", "confidence": 0.5, "reason": "Fallback"}


def apply_overrides(reco: Dict, query_sem: Dict, chart_hints: Dict[str, str]) -> Dict:
    qid = query_sem.get("id")
    hint = (chart_hints.get(qid) or "auto").strip().lower()

    if hint and hint != "auto":
        reco = dict(reco)
        reco["chart"] = hint
        reco["confidence"] = 1.0
        reco["reason"] = "Overridden by metadata chart hint"
    return reco


def main() -> None:
    parser = argparse.ArgumentParser(description="Recommend chart types")
    parser.add_argument("--input", required=True, help="Path to semantic_catalog.json")
    parser.add_argument(
        "--query-catalog",
        required=False,
        help="Optional path to query_catalog.json for chart_hint overrides",
    )
    parser.add_argument("--output", required=True, help="Path to chart_plan.json")
    args = parser.parse_args()

    sem = json.loads(Path(args.input).read_text(encoding="utf-8"))
    sem_queries: List[Dict] = sem.get("queries", [])

    chart_hints: Dict[str, str] = {}
    if args.query_catalog:
        qc = json.loads(Path(args.query_catalog).read_text(encoding="utf-8"))
        chart_hints = {q.get("id"): q.get("chart_hint", "auto") for q in qc.get("queries", [])}

    chart_items = []
    for sq in sem_queries:
        reco = recommend_for_query(sq)
        reco = apply_overrides(reco, sq, chart_hints)
        chart_items.append(reco)

    out = {
        "query_count": len(chart_items),
        "charts": chart_items,
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Recommended charts for {len(chart_items)} queries -> {out_path}")


if __name__ == "__main__":
    main()
