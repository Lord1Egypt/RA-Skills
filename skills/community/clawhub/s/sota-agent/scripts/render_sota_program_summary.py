#!/usr/bin/env python3
"""Render a concise markdown summary from structured SOTA program artifacts."""

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
    parser.add_argument("--program", required=True, help="Program JSON file.")
    parser.add_argument("--out", required=True, help="Output markdown file.")
    parser.add_argument("--candidate", help="Optional candidate JSON file.")
    parser.add_argument("--scoreboard", help="Optional scoreboard JSON file.")
    parser.add_argument("--review-packet", help="Optional review packet JSON file.")
    args = parser.parse_args()

    program = load_json(Path(args.program).expanduser().resolve())
    candidate = load_json(Path(args.candidate).expanduser().resolve()) if args.candidate else {}
    scoreboard = load_json(Path(args.scoreboard).expanduser().resolve()) if args.scoreboard else {}
    review_packet = load_json(Path(args.review_packet).expanduser().resolve()) if args.review_packet else {}

    lines = [f"# SOTA Program Summary: {program.get('program_id', 'unnamed-program')}", ""]

    add_field(lines, "problem", program.get("problem"))
    benchmark = program.get("benchmark") or {}
    add_field(lines, "task", benchmark.get("task"))
    add_field(lines, "dataset", benchmark.get("dataset"))
    add_field(lines, "split", benchmark.get("split"))
    add_field(lines, "primary_metric", benchmark.get("primary_metric"))
    add_field(lines, "goal_direction", benchmark.get("goal_direction"))
    add_field(lines, "claim_threshold", benchmark.get("claim_threshold"))
    add_field(lines, "minimum_delta", benchmark.get("minimum_delta"))
    surfaces = benchmark.get("non_regression_surfaces") or []
    for surface in surfaces:
        add_field(lines, "non_regression_surface", surface)
    lines.append("")

    baselines = program.get("baselines") or []
    if baselines:
        lines.append("## Baselines")
        for baseline in baselines:
            lines.append(f"- `{baseline.get('name')}`: `{baseline.get('score')}`")
        lines.append("")

    frontier_sources = program.get("frontier_sources") or []
    if frontier_sources:
        lines.append("## Frontier Sources")
        for source in frontier_sources:
            add_field(lines, "source", source)
        lines.append("")

    agents = program.get("agents") or {}
    runtime_policy = program.get("runtime_policy") or {}
    rerun_policy = program.get("rerun_policy") or {}
    if agents or runtime_policy or rerun_policy:
        lines.append("## Governance")
        add_field(lines, "main_thread_role", agents.get("main_thread_role"))
        for role in agents.get("subagent_roles") or []:
            add_field(lines, "subagent_role", role)
        add_field(lines, "agent_notes", agents.get("notes"))
        for runtime in runtime_policy.get("allowed_runtimes") or runtime_policy.get("allowed_auth") or []:
            add_field(lines, "allowed_runtime", runtime)
        for env_var in runtime_policy.get("forbidden_env_vars") or []:
            add_field(lines, "forbidden_env_var", env_var)
        add_field(lines, "runtime_notes", runtime_policy.get("notes"))
        add_field(lines, "small_delta_threshold", rerun_policy.get("small_delta_threshold"))
        add_field(lines, "minimum_reruns", rerun_policy.get("minimum_reruns"))
        add_field(lines, "seed_strategy", rerun_policy.get("seed_strategy"))
        add_field(lines, "acceptance_rule", rerun_policy.get("acceptance_rule"))
        lines.append("")

    review_surfaces = program.get("review_surfaces") or {}
    if review_surfaces:
        lines.append("## Review Surfaces")
        add_field(lines, "execution_dashboard_path", review_surfaces.get("execution_dashboard_path"))
        for item in review_surfaces.get("runtime_summary_paths") or []:
            add_field(lines, "runtime_summary_path", item)
        for item in review_surfaces.get("qa_summary_paths") or []:
            add_field(lines, "qa_summary_path", item)
        for item in review_surfaces.get("benchmark_panel_roots") or []:
            add_field(lines, "benchmark_panel_root", item)
        for item in review_surfaces.get("curated_cases") or []:
            add_field(lines, "curated_case", item)
        lines.append("")

    claim_safety = program.get("claim_safety") or {}
    if claim_safety:
        lines.append("## Claim Safety")
        for item in claim_safety.get("source_audit_paths") or []:
            add_field(lines, "source_audit_path", item)
        for item in claim_safety.get("leakage_audit_paths") or []:
            add_field(lines, "leakage_audit_path", item)
        add_field(lines, "contamination_status", claim_safety.get("contamination_status"))
        add_field(lines, "claim_safety_notes", claim_safety.get("notes"))
        lines.append("")

    if candidate:
        lines.append("## Candidate")
        add_field(lines, "candidate_id", candidate.get("candidate_id"))
        add_field(lines, "objective", candidate.get("objective"))
        hypothesis = candidate.get("hypothesis")
        if isinstance(hypothesis, dict):
            add_field(lines, "hypothesis_summary", hypothesis.get("summary"))
            add_field(lines, "novelty_type", hypothesis.get("novelty_type"))
            for item in hypothesis.get("borrowed_from") or []:
                add_field(lines, "borrowed_from", item)
        else:
            add_field(lines, "hypothesis", hypothesis)
        add_field(lines, "expected_win", candidate.get("expected_win"))
        for change in candidate.get("change_set") or []:
            add_field(lines, "change", change)
        execution = candidate.get("execution") or {}
        add_field(lines, "lane", execution.get("lane"))
        add_field(lines, "auth_mode", execution.get("auth_mode"))
        add_field(lines, "compute_budget", execution.get("compute_budget"))
        add_field(lines, "wall_time_budget", execution.get("wall_time_budget"))
        add_field(lines, "critical_ablation_question", execution.get("critical_ablation_question"))
        for thread in execution.get("agent_threads") or []:
            add_field(lines, "agent_thread", thread)
        evaluation = candidate.get("evaluation") or {}
        add_field(lines, "benchmark_contract_path", evaluation.get("benchmark_contract_path"))
        add_field(lines, "score", evaluation.get("score"))
        add_field(lines, "delta_vs_baseline", evaluation.get("delta_vs_baseline"))
        add_field(lines, "slice_scores", evaluation.get("slice_scores"))
        add_field(lines, "reruns", evaluation.get("reruns"))
        add_field(lines, "review_dashboard_path", evaluation.get("review_dashboard_path"))
        add_field(lines, "claim_safety_paths", evaluation.get("claim_safety_paths"))
        add_field(lines, "review_packet_path", evaluation.get("review_packet_path"))
        lines.append("")

    entries = scoreboard.get("entries") or []
    if entries:
        lines.append("## Scoreboard")
        add_field(lines, "metric_name", scoreboard.get("metric_name"))
        add_field(lines, "best_candidate", scoreboard.get("best_candidate"))
        for item in entries[:10]:
            lines.append(
                f"- rank `{item.get('rank')}`: `{item.get('candidate_id')}` score `{item.get('score')}` stage `{item.get('stage')}`"
            )
        lines.append("")

    if review_packet:
        lines.append("## Decision")
        decision = review_packet.get("decision") or {}
        add_field(lines, "status", decision.get("status"))
        add_field(lines, "reason", decision.get("reason"))
        lines.append("")

    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
