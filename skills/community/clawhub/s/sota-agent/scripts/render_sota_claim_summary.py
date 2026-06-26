#!/usr/bin/env python3
"""Render a concise markdown review from a SOTA candidate card."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from sota_public_safety import sanitize_ref


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit(f"expected JSON object in {path}")
    return payload


def sanitize_value(value: Any) -> Any:
    if isinstance(value, str):
        return sanitize_ref(value)
    if isinstance(value, list):
        cleaned = []
        for item in value:
            sanitized = sanitize_value(item)
            if sanitized in ("", [], {}):
                continue
            cleaned.append(sanitized)
        return cleaned
    if isinstance(value, dict):
        cleaned = {}
        for key, item in value.items():
            sanitized = sanitize_value(item)
            if sanitized in ("", [], {}):
                continue
            cleaned[key] = sanitized
        return cleaned
    return value


def add_field(lines: list[str], label: str, value: Any) -> None:
    value = sanitize_value(value)
    if value in (None, "", [], {}):
        return
    rendered = json.dumps(value, ensure_ascii=True, sort_keys=True) if isinstance(value, (list, dict)) else str(value)
    lines.append(f"- {label}: `{rendered}`")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-card", required=True, help="Path to the candidate card JSON.")
    parser.add_argument("--out", required=True, help="Path to the output markdown file.")
    args = parser.parse_args()

    card_path = Path(args.candidate_card).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()
    payload = load_json(card_path)

    lines = [f"# SOTA Claim Review: {payload.get('candidate_id') or 'unnamed'}", ""]
    for key in ("campaign_id", "candidate_id", "objective", "baseline", "created_utc"):
        add_field(lines, key, payload.get(key))
    lines.append("")

    hypothesis = payload.get("hypothesis") or {}
    lines.append("## Hypothesis")
    for key in ("summary", "novelty_type"):
        add_field(lines, key, hypothesis.get(key))
    borrowed = hypothesis.get("borrowed_from") or []
    for item in borrowed:
        lines.append(f"- borrowed_from: `{sanitize_ref(item)}`")
    lines.append("")

    execution = payload.get("execution") or {}
    lines.append("## Execution")
    for key in ("lane", "auth_mode", "compute_budget", "wall_time_budget", "critical_ablation_question"):
        add_field(lines, key, execution.get(key))
    for thread in execution.get("agent_threads") or []:
        add_field(lines, "agent_thread", thread)
    lines.append("")

    evaluation = payload.get("evaluation") or {}
    lines.append("## Evaluation")
    for key in ("benchmark_contract_path", "score", "delta_vs_baseline", "slice_scores", "reruns", "review_packet_path"):
        add_field(lines, key, evaluation.get(key))
    for key in ("failure_cases", "regression_notes"):
        values = evaluation.get(key) or []
        for item in values:
            lines.append(f"- {key[:-1] if key.endswith('s') else key}: `{sanitize_ref(item)}`")
    lines.append("")

    review = payload.get("claim_review") or {}
    lines.append("## Claim Review")
    for key in ("status", "wording"):
        add_field(lines, key, review.get(key))
    for item in review.get("blocked_by") or []:
        lines.append(f"- blocked_by: `{sanitize_ref(item)}`")
    for item in review.get("evidence_paths") or []:
        lines.append(f"- evidence_path: `{sanitize_ref(item)}`")
    lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
