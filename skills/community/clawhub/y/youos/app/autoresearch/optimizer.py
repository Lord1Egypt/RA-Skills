"""Autoresearch optimization loop for YouOS."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.autoresearch.mutator import (
    ConfigSurface,
    apply_mutation,
    describe_mutation,
    get_mutable_surfaces,
    revert_mutation,
)
from app.autoresearch.run_log import ensure_table, log_iteration
from app.autoresearch.scorer import (
    Scorecard,
    compare_scorecards,
    draft_quality_case_weights,
    draft_quality_weighting_enabled,
    scorecard_from_eval_result,
)
from app.evaluation.service import EvalRequest, run_eval_suite


@dataclass
class IterationResult:
    iteration: int
    surface_name: str
    mutation_desc: str
    baseline_composite: float
    candidate_composite: float
    outcome: str  # "improved" | "neutral" | "regressed"
    kept: bool


@dataclass
class AutoresearchReport:
    run_tag: str
    started_at: str
    baseline: Scorecard
    final: Scorecard
    iterations: list[IterationResult] = field(default_factory=list)
    total_eval_runs: int = 0
    improvements_kept: int = 0
    reverted: int = 0


def run_autoresearch(
    configs_dir: Path,
    database_url: str,
    *,
    generate_fn: Any,
    max_iterations: int = 10,
    baseline_tag: str = "autoresearch_baseline",
    dry_run: bool = False,
    surface_filter: str | None = None,
) -> AutoresearchReport:
    """Run the autoresearch optimization loop.

    Args:
        configs_dir: Path to configs/ directory.
        database_url: SQLite database URL.
        generate_fn: Generation function matching the eval runner interface.
        max_iterations: Max total eval runs (including baseline).
        baseline_tag: Config tag for the baseline run.
        dry_run: If True, show plan without executing.
        surface_filter: Optional "retrieval" or "prompt_drafting" to limit scope.
    """
    run_tag = f"autoresearch_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    started_at = datetime.now(timezone.utc).isoformat()

    surfaces = get_mutable_surfaces(configs_dir, surface_filter=surface_filter)

    if dry_run:
        return _dry_run_report(surfaces, run_tag, started_at)

    # Ensure logging table exists
    ensure_table(database_url)

    # Draft-quality case weights (default off): computed ONCE from the current
    # draft_events log and applied to every scorecard this run, so baseline and
    # candidates stay comparable. Pushes the objective toward the cohorts where
    # real drafts get edited most. No data / disabled → None → equal weighting.
    case_weights: dict[str, float] | None = None
    try:
        if draft_quality_weighting_enabled(configs_dir):
            from app.core.stats import summarize_draft_events

            case_weights = draft_quality_case_weights(summarize_draft_events(database_url)) or None
    except Exception:
        case_weights = None

    # 1. Establish baseline
    baseline_result = run_eval_suite(
        EvalRequest(config_tag=f"{run_tag}_baseline"),
        generate_fn=generate_fn,
        database_url=database_url,
        configs_dir=configs_dir,
        persist=True,
    )
    baseline = scorecard_from_eval_result(baseline_result, configs_dir, case_weights=case_weights)
    eval_count = 1
    current_baseline = baseline

    report = AutoresearchReport(
        run_tag=run_tag,
        started_at=started_at,
        baseline=baseline,
        final=baseline,
    )

    # 2. Iterate over surfaces
    for surface in surfaces:
        if eval_count >= max_iterations:
            break

        mutation_desc = describe_mutation(surface)

        # Skip if at boundary
        if "at boundary" in mutation_desc:
            continue

        old_value = apply_mutation(surface, configs_dir)
        if old_value == surface.current_value:
            # No actual change (boundary)
            continue

        # Run eval with mutated config
        candidate_result = run_eval_suite(
            EvalRequest(config_tag=f"{run_tag}_iter{eval_count}"),
            generate_fn=generate_fn,
            database_url=database_url,
            configs_dir=configs_dir,
            persist=True,
        )
        eval_count += 1
        candidate = scorecard_from_eval_result(candidate_result, configs_dir, case_weights=case_weights)
        outcome = compare_scorecards(current_baseline, candidate)

        kept = outcome == "improved"
        if not kept:
            revert_mutation(surface, old_value, configs_dir)

        iteration = IterationResult(
            iteration=eval_count - 1,
            surface_name=surface.name,
            mutation_desc=mutation_desc,
            baseline_composite=current_baseline.composite,
            candidate_composite=candidate.composite,
            outcome=outcome,
            kept=kept,
        )
        report.iterations.append(iteration)

        log_iteration(
            database_url,
            run_tag=run_tag,
            iteration=eval_count - 1,
            surface_name=surface.name,
            mutation_desc=mutation_desc,
            baseline_composite=current_baseline.composite,
            candidate_composite=candidate.composite,
            outcome=outcome,
            kept=kept,
        )

        if kept:
            current_baseline = candidate
            report.improvements_kept += 1
        else:
            report.reverted += 1

    report.total_eval_runs = eval_count
    report.final = current_baseline

    # Write structured JSON run log
    _write_jsonl_entry(report, configs_dir)

    return report


def _write_jsonl_entry(report: AutoresearchReport, configs_dir: Path) -> None:
    """Append a JSON line to var/autoresearch_runs.jsonl."""
    root = configs_dir.parent
    jsonl_path = root / "var" / "autoresearch_runs.jsonl"
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)

    improvements = [it.surface_name for it in report.iterations if it.kept]
    regressions = [it.surface_name for it in report.iterations if it.outcome == "regressed"]

    entry = {
        "run_at": report.started_at,
        "iterations": report.total_eval_runs,
        "composite_score": report.final.composite,
        "improvements": improvements,
        "regressions": regressions,
        "config_snapshot": {
            "baseline_composite": report.baseline.composite,
            "final_composite": report.final.composite,
            "improvements_kept": report.improvements_kept,
            "reverted": report.reverted,
        },
    }
    with open(jsonl_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, default=str) + "\n")


def _dry_run_report(
    surfaces: list[ConfigSurface],
    run_tag: str,
    started_at: str,
) -> AutoresearchReport:
    """Build a report showing what would be mutated without doing it."""
    dummy = Scorecard(
        config_tag="dry_run",
        pass_rate=0.0,
        warn_rate=0.0,
        fail_rate=0.0,
        avg_keyword_hit=0.0,
        avg_confidence=0.0,
        composite=0.0,
    )
    report = AutoresearchReport(
        run_tag=run_tag,
        started_at=started_at,
        baseline=dummy,
        final=dummy,
    )
    for surface in surfaces:
        desc = describe_mutation(surface)
        report.iterations.append(
            IterationResult(
                iteration=0,
                surface_name=surface.name,
                mutation_desc=desc,
                baseline_composite=0.0,
                candidate_composite=0.0,
                outcome="dry_run",
                kept=False,
            )
        )
    return report


def format_report(report: AutoresearchReport) -> str:
    """Format an autoresearch report for terminal output."""
    lines: list[str] = []
    lines.append(f"YouOS Autoresearch — {report.started_at}")
    lines.append("━" * 50)

    if report.baseline.composite > 0 or report.final.composite > 0:
        lines.append(f"Baseline: {report.baseline.summary()}")
        lines.append("")

    for it in report.iterations:
        prefix = f"[{it.iteration}/{report.total_eval_runs or len(report.iterations)}]"
        if it.outcome == "dry_run":
            lines.append(f"  {it.mutation_desc}")
        elif it.outcome == "improved":
            lines.append(f"{prefix} Mutating {it.mutation_desc}\n  Improved: composite {it.baseline_composite:.2f} -> {it.candidate_composite:.2f} — keeping")
        elif it.outcome == "neutral":
            lines.append(f"{prefix} Mutating {it.mutation_desc}\n  Neutral: composite {it.baseline_composite:.2f} -> {it.candidate_composite:.2f} — reverting")
        else:
            lines.append(
                f"{prefix} Mutating {it.mutation_desc}\n  Regressed: composite {it.baseline_composite:.2f} -> {it.candidate_composite:.2f} — reverting"
            )

    lines.append("━" * 50)

    if report.total_eval_runs > 0:
        lines.append(f"Final: {report.final.summary()}")
        lines.append(f"Improvements kept: {report.improvements_kept} | Reverted: {report.reverted} | Iterations: {report.total_eval_runs}")
    else:
        lines.append(f"Dry run: {len(report.iterations)} surfaces would be mutated")

    return "\n".join(lines)
