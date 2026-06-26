#!/usr/bin/env python3
"""Create a machine-readable program record for a DS/CV SOTA effort."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from sota_public_safety import sanitize_ref


def parse_baseline(items: list[str]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for item in items:
        if "=" not in item:
            raise SystemExit(f"invalid --baseline value: {item!r}, expected name=score")
        name, raw_score = item.split("=", 1)
        rows.append({"name": name.strip(), "score": float(raw_score.strip())})
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="Output JSON file.")
    parser.add_argument("--program-id", default="", help="Stable program identifier.")
    parser.add_argument("--campaign-id", default="", help="Alias for --program-id.")
    parser.add_argument("--problem", default="", help="One-sentence program goal.")
    parser.add_argument("--task", default="", help="Short task name or benchmark family.")
    parser.add_argument("--dataset", default="", help="Dataset or evaluation benchmark name.")
    parser.add_argument("--primary-metric", default="", help="Primary benchmark metric.")
    parser.add_argument("--metric", default="", help="Alias for --primary-metric.")
    parser.add_argument("--split", default="", help="Named split or evaluation surface.")
    parser.add_argument("--surface", action="append", default=[], help="Repeatable non-regression surface.")
    parser.add_argument("--baseline", action="append", default=[], help="Repeatable name=score baseline entry.")
    parser.add_argument("--paper", action="append", default=[], help="Repeatable frontier paper title or public URL.")
    parser.add_argument("--claim-threshold", default="", help="What qualifies as a real frontier win.")
    parser.add_argument(
        "--min-delta",
        type=float,
        default=0.0,
        help="Minimum meaningful delta before small-gain rerun policy applies.",
    )
    parser.add_argument(
        "--subagent-role",
        action="append",
        default=[],
        help="Repeatable bounded subagent role. Defaults to scout, reproducer, reviewer.",
    )
    parser.add_argument("--minimize", action="store_true", default=False, help="Treat lower metric values as better.")
    args = parser.parse_args()

    program_id = (args.program_id or args.campaign_id).strip()
    if not program_id:
        raise SystemExit("one of --program-id or --campaign-id is required")

    problem = (args.problem or args.task).strip()
    if not problem:
        raise SystemExit("one of --problem or --task is required")

    primary_metric = (args.primary_metric or args.metric).strip()
    if not primary_metric:
        raise SystemExit("one of --primary-metric or --metric is required")

    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "schema_version": "1.2",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "program_id": program_id,
        "problem": problem,
        "benchmark": {
            "task": args.task,
            "dataset": args.dataset,
            "split": args.split,
            "primary_metric": primary_metric,
            "goal_direction": "minimize" if args.minimize else "maximize",
            "non_regression_surfaces": args.surface,
            "claim_threshold": args.claim_threshold,
            "minimum_delta": args.min_delta,
        },
        "baselines": parse_baseline(args.baseline),
        "frontier_sources": [sanitize_ref(item) for item in args.paper],
        "rerun_policy": {
            "required_for_small_delta": True,
            "small_delta_threshold": args.min_delta,
            "minimum_reruns": 2,
            "seed_strategy": "adjacent",
            "acceptance_rule": "",
        },
        "agents": {
            "main_thread_role": "planner",
            "subagent_roles": args.subagent_role or ["scout", "reproducer", "reviewer"],
            "notes": "",
        },
        "runtime_policy": {
            "allowed_runtimes": [
                "local_python",
                "public_artifacts",
                "repo_local_tests",
            ],
            "forbidden_env_vars": [
                "OPENAI_API_KEY",
                "ANTHROPIC_API_KEY",
                "GOOGLE_API_KEY",
                "CEREBRAS_API_KEY",
                "AZURE_OPENAI_API_KEY",
            ],
            "notes": "Treat third-party frameworks that require paid API keys as reference-only unless they can run through local tools or public artifacts.",
        },
        "queues": {
            "research_backlog": [],
            "prove_it": [],
            "promotion": [],
        },
        "review_surfaces": {
            "execution_dashboard_path": "",
            "runtime_summary_paths": [],
            "qa_summary_paths": [],
            "benchmark_panel_roots": [],
            "curated_cases": [],
        },
        "claim_safety": {
            "source_audit_paths": [],
            "leakage_audit_paths": [],
            "contamination_status": "",
            "notes": "",
        },
        "artifacts": {
            "program_summary_path": "",
            "scoreboard_path": "",
            "review_packet_path": "",
        },
        "evidence_requirements": {
            "required_artifacts": [
                "leaderboard_snapshot",
                "paper_triage",
                "candidate_card_or_candidate_record",
                "review_packet",
            ],
            "notes": "",
        },
        "decision": {
            "status": "research",
            "reason": "",
        },
    }

    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
