from __future__ import annotations

from typing import Any

from research_mode_adequacy import build_adequacy_operator_next_action
from research_mode_finalization import build_finalization_surface
from research_mode_reliability import build_reliability_attention
from research_mode_surfaces import compute_budget_phase, compute_consistency_warnings
from research_mode_task import ResearchTask
from research_mode_utils import (
    append_tsv_row,
    compact_text,
    minutes_since,
    read_json,
    read_jsonl,
    read_tsv_rows,
)

RUNS_TSV_COLUMNS = [
    "timestamp",
    "iteration",
    "run_id",
    "phase",
    "outcome",
    "normalized_reason",
    "meaningful_progress",
    "new_sources_count",
    "new_findings_count",
    "duplicate_sources_count",
    "duplicate_findings_count",
    "low_yield_streak",
    "topic_saturated",
    "short_summary",
]


def render_task_playbook(task: ResearchTask, state: dict[str, Any]) -> str:
    progress = state.get("progress") or {}
    working_memory = state.get("working_memory") or {}
    budget = state.get("budget") or {}
    delivery = state.get("delivery") or {}
    saturation = state.get("saturation") or {}
    errors = state.get("errors") or {}
    artifacts = state.get("artifacts") or {}
    history = state.get("history") or {}
    preflight_raw = state.get("preflight")
    preflight_configured = isinstance(preflight_raw, dict)
    preflight = preflight_raw if preflight_configured else {}
    adequacy = state.get("adequacy") or {}
    recent_runs = list(reversed(read_tsv_rows(task.runs_path)[-3:]))
    analysis = state.get("analysis") or {}
    runtime_meta: dict[str, Any] = {}
    if task.runtime_meta_path.exists():
        try:
            loaded_meta = read_json(task.runtime_meta_path)
            if isinstance(loaded_meta, dict):
                runtime_meta = loaded_meta
        except Exception:
            runtime_meta = {}

    lines = [f"# {state.get('title') or state.get('id')}", ""]
    lines.extend(
        [
            "## Identity",
            "",
            f"- ID: `{state.get('id')}`",
            f"- Status: `{state.get('status')}`",
            f"- Phase: `{state.get('phase')}`",
            f"- Created at: {state.get('created_at') or '-'}",
            f"- Updated at: {state.get('updated_at') or '-'}",
        ]
    )
    task_status = state.get("status")
    finalization = build_finalization_surface(state)
    if task_status == "finalize":
        attempt = int(finalization.get("attempt_count") or 0)
        max_att = int(finalization.get("max_attempts") or 3)
        lines.append(
            f"- ⚠️  Finalization failed — worker should rework (attempt {attempt}/{max_att})"
        )
    elif task_status == "awaiting_review":
        lines.append("- 🔍 Awaiting human review before final completion")
    elif finalization.get("status") == "needs_intervention":
        lines.append("- 🚨 Finalization stalled — human intervention required")
    lines.append("")
    lines.extend(
        [
            "## Goal",
            "",
            state.get("goal") or "(goal not provided)",
            "",
            "## Progress snapshot",
            "",
            f"- Iterations: {int(progress.get('iteration_count') or 0)} / {budget.get('max_iterations') or 'open'}",
            f"- Meaningful iterations: {int(progress.get('meaningful_iterations') or 0)}",
            f"- Last iteration at: {progress.get('last_iteration_at') or '-'}",
            f"- Last meaningful progress at: {progress.get('last_meaningful_progress_at') or '-'}",
            f"- Last transition: {history.get('last_transition') or '-'}",
            f"- Last reason: {history.get('last_reason') or '-'}",
            f"- Last terminal reason: {history.get('last_terminal_reason') or '-'}",
            f"- Low-yield streak: {int(saturation.get('consecutive_low_yield') or 0)} / {int(saturation.get('low_yield_threshold') or 0) or '-'}",
            f"- Topic saturated: {'yes' if saturation.get('topic_saturated') else 'no'}",
            f"- Failures: {int(errors.get('failure_count') or 0)} (consecutive {int(errors.get('consecutive_failures') or 0)})",
            f"- Milestone cadence: every {int(delivery.get('milestone_every_iterations') or 0) or '-'} meaningful iterations",
            "",
            "## Preflight",
            "",
            f"- Configured: {'yes' if preflight_configured else 'no'}",
            f"- Done: {'yes' if preflight.get('done') else 'no'}",
            f"- Decision: `{preflight.get('decision') or '-'}`",
            f"- Target phase: `{preflight.get('target_phase') or '-'}`",
            f"- Iteration: {int(preflight.get('iteration_index') or 0)} / {int(preflight.get('iteration_limit') or 0) or '-'}",
            f"- Artifact: `{preflight.get('artifact_markdown') or '-'}`",
            f"- Completed at: {preflight.get('completed_at') or '-'}",
        ]
    )
    preflight_warnings = preflight.get("warnings") or []
    if preflight_warnings:
        lines.extend(["", "### Preflight warnings", ""])
        lines.extend(f"- {item}" for item in preflight_warnings[:10])
    preflight_blockers = preflight.get("blockers") or []
    if preflight_blockers:
        lines.extend(["", "### Preflight blockers", ""])
        lines.extend(f"- {item}" for item in preflight_blockers[:10])
    lines.extend(
        [
            "",
            "## Budget",
            "",
        ]
    )
    iter_count = int(progress.get("iteration_count") or 0)
    total_src = len(read_jsonl(task.sources_path))
    budget_phase_info = compute_budget_phase(
        budget=budget,
        progress=progress,
        total_sources=total_src,
        total_runtime_min=(
            minutes_since(state.get("created_at")) if state.get("created_at") else None
        ),
    )
    lines.extend(
        [
            f"- Budget phase: `{budget_phase_info['phase']}`",
            f"- Iteration budget: {iter_count} / {budget_phase_info['max_iterations'] or 'open'} ({budget_phase_info['iteration_pct']:.0%})",
            f"- Source budget: {total_src} / {budget_phase_info['max_sources'] or 'open'} ({budget_phase_info['source_pct']:.0%})",
            f"- Soft limit threshold: {budget_phase_info['soft_pct']:.0%}",
            f"- Dominant limit: {budget_phase_info['dominant_limit'] or 'none'}",
        ]
    )
    if (
        budget_phase_info["max_runtime_min"] > 0
        or budget_phase_info["total_runtime_min"] is not None
    ):
        runtime_total = budget_phase_info["total_runtime_min"]
        runtime_total_display = (
            f"{runtime_total:.2f}" if runtime_total is not None else "-"
        )
        lines.append(
            f"- Runtime budget: {runtime_total_display} / {budget_phase_info['max_runtime_min'] or 'open'} min ({budget_phase_info['runtime_pct']:.0%})"
        )
    lines.append("")
    adequacy_action = (
        adequacy.get("operator_next_action")
        or build_adequacy_operator_next_action(state, adequacy)
    )
    lines.extend(
        [
            "## Adequacy",
            "",
            f"- Status: `{adequacy.get('status') or 'not_started'}`",
            f"- Attempts: {int(adequacy.get('attempt_count') or 0)} / {int(adequacy.get('max_attempts') or 2)}",
            f"- Recommended next phase: `{adequacy.get('recommended_next_phase') or '-'}`",
            f"- Recommended next angle: {adequacy.get('recommended_next_angle') or '-'}",
            f"- Operator next action: `{(adequacy_action or {}).get('kind') or '-'}`",
        ]
    )
    gaps = adequacy.get("coverage_gaps") or []
    if gaps:
        lines.extend(["", "### Coverage gaps", ""])
        for item in gaps[:5]:
            if isinstance(item, dict):
                text = item.get("gap") or item.get("reason") or item.get("text")
            else:
                text = str(item)
            if text:
                lines.append(f"- {text}")
    reasons = adequacy.get("blocking_reasons") or []
    if reasons:
        lines.extend(["", "### Blocking reasons", ""])
        for item in reasons[:5]:
            if isinstance(item, dict):
                text = item.get("reason") or item.get("text")
            else:
                text = str(item)
            if text:
                lines.append(f"- {text}")
    lines.append("")
    lines.extend(
        [
            "## Working memory",
            "",
            "### Summary",
            "",
            working_memory.get("summary") or "(empty)",
            "",
        ]
    )

    next_angle = working_memory.get("next_angle")
    if next_angle:
        lines.extend(["### Next angle", "", next_angle, ""])

    constraints = working_memory.get("constraints") or []
    if constraints:
        lines.extend(["### Constraints", ""])
        lines.extend(f"- {item}" for item in constraints)
        lines.append("")

    deliverable = working_memory.get("deliverable")
    if deliverable:
        lines.extend(["### Deliverable", "", deliverable, ""])

    user_instructions = working_memory.get("user_instructions") or []
    if user_instructions:
        lines.extend(["### User instructions", ""])
        lines.extend(f"- {item}" for item in user_instructions)
        lines.append("")

    open_questions = working_memory.get("open_questions") or []
    if open_questions:
        lines.extend(["### Open questions", ""])
        lines.extend(f"- {item}" for item in open_questions)
        lines.append("")

    lines.extend(
        [
            "## Analysis runtime",
            "",
            f"- Runtime prepared: {'yes' if task.runtime_meta_path.exists() else 'no'}",
            f"- Runtime tool: {runtime_meta.get('tool') or '-'}",
            f"- Venv python: {runtime_meta.get('venv_python') or '-'}",
            f"- Installed packages: {', '.join(runtime_meta.get('packages_installed') or []) or '-'}",
            f"- SQLite ready: {'yes' if runtime_meta.get('sqlite_ready') else 'no'}",
            f"- Default SQLite DB: {runtime_meta.get('default_sqlite_db_path') or task.sqlite_db_path}",
            f"- SQLite schema path: {runtime_meta.get('sqlite_schema_path') or task.sqlite_schema_path}",
            f"- SQLite queries dir: {runtime_meta.get('sqlite_queries_dir') or task.sqlite_queries_dir}",
            f"- Screenshots dir: {task.workspace_screenshots_dir}",
            f"- Vision dir: {task.workspace_vision_dir}",
            f"- Last iteration used code: {'yes' if analysis.get('last_iteration_code_used') else 'no'}",
            f"- Code used recently: {'yes' if analysis.get('code_used_recently') else 'no'}",
            f"- Last code run at: {analysis.get('last_code_run_at') or '-'}",
            f"- Last iteration used DB: {'yes' if analysis.get('last_iteration_database_used') else 'no'}",
            f"- Database used recently: {'yes' if analysis.get('database_used_recently') else 'no'}",
            f"- Last database run at: {analysis.get('last_database_run_at') or '-'}",
            f"- Last iteration used vision: {'yes' if analysis.get('last_iteration_vision_used') else 'no'}",
            f"- Vision used recently: {'yes' if analysis.get('vision_used_recently') else 'no'}",
            f"- Last vision run at: {analysis.get('last_vision_run_at') or '-'}",
        ]
    )
    last_packages = analysis.get("last_packages_used") or []
    if last_packages:
        lines.append(f"- Last packages used in result: {', '.join(last_packages)}")
    last_analysis_artifacts = analysis.get("last_analysis_artifacts") or []
    if last_analysis_artifacts:
        lines.append("- Last analysis artifacts:")
        for artifact in last_analysis_artifacts[:10]:
            kind = artifact.get("kind") or "artifact"
            artifact_path = artifact.get("path") or "-"
            note_text = artifact.get("note")
            bullet = f"  - [{kind}] {artifact_path}"
            if note_text:
                bullet += f" — {note_text}"
            lines.append(bullet)
    last_database_summary = analysis.get("last_database_summary") or {}
    if last_database_summary:
        lines.append(
            f"- Last database purpose: {last_database_summary.get('purpose') or '-'}"
        )
        tables = last_database_summary.get("tables") or []
        if tables:
            lines.append(f"- Last database tables: {', '.join(str(t) for t in tables)}")
        row_counts = last_database_summary.get("row_counts") or {}
        if row_counts:
            lines.append("- Last database row counts:")
            for table_name, row_count in row_counts.items():
                lines.append(f"  - {table_name}: {row_count}")
    last_database_artifacts = analysis.get("last_database_artifacts") or []
    if last_database_artifacts:
        lines.append("- Last database artifacts:")
        for artifact in last_database_artifacts[:10]:
            kind = artifact.get("kind") or "artifact"
            artifact_path = artifact.get("path") or "-"
            note_text = artifact.get("note")
            bullet = f"  - [{kind}] {artifact_path}"
            if note_text:
                bullet += f" — {note_text}"
            lines.append(bullet)
    last_vision_summary = analysis.get("last_vision_summary") or {}
    if last_vision_summary:
        lines.append(f"- Last vision purpose: {last_vision_summary.get('purpose') or '-'}")
        if last_vision_summary.get("images_reviewed") is not None:
            lines.append(
                f"- Last vision images reviewed: {last_vision_summary.get('images_reviewed')}"
            )
        if last_vision_summary.get("confidence"):
            lines.append(
                f"- Last vision confidence: {last_vision_summary.get('confidence')}"
            )
    last_vision_artifacts = analysis.get("last_vision_artifacts") or []
    if last_vision_artifacts:
        lines.append("- Last vision artifacts:")
        for artifact in last_vision_artifacts[:10]:
            kind = artifact.get("kind") or "artifact"
            artifact_path = artifact.get("path") or "-"
            note_text = artifact.get("note")
            bullet = f"  - [{kind}] {artifact_path}"
            if note_text:
                bullet += f" — {note_text}"
            lines.append(bullet)
    lines.append("")

    corpus = state.get("corpus") or {}
    lines.extend(
        [
            "## Corpus",
            "",
            f"- Mode: `{corpus.get('mode') or 'web'}`",
            f"- Files attached: {len(corpus.get('entries') or [])}",
        ]
    )
    for entry in (corpus.get("entries") or [])[:10]:
        lines.append(
            f"- {entry.get('path')} ({int(entry.get('size_bytes') or 0)} bytes)"
        )
    lines.append("")

    completion = state.get("completion") or {}
    last_validation = completion.get("last_validation") or {}
    if last_validation:
        lines.extend(
            [
                "## Completion validation",
                "",
                f"- Passed: {'yes' if last_validation.get('passed') else 'no'}",
                f"- Triggered by: {last_validation.get('triggered_by') or '-'}",
                f"- Phase: {last_validation.get('phase') or '-'}",
                f"- Evidence: sources={last_validation.get('total_sources', 0)}, findings={last_validation.get('total_findings', 0)}",
            ]
        )
        reasons = last_validation.get("reasons") or []
        if reasons:
            lines.append("- Reasons:")
            lines.extend(f"  - {item}" for item in reasons)
        deliverable_checks = (last_validation.get("deliverable_validation") or {}).get(
            "checks"
        ) or []
        if deliverable_checks:
            lines.append("- Deliverable checks:")
            for check in deliverable_checks:
                kind = check.get("kind") or "unknown"
                status = "passed" if check.get("passed") else "failed"
                lines.append(f"  - {kind}: {status}")
        lines.append("")

    review = state.get("review") or {}
    review_status = review.get("status") or "pending"
    revision_count = int(review.get("revision_count") or 0)
    if revision_count > 0 or review_status != "pending":
        lines.extend(
            [
                "## Review",
                "",
                f"- Status: `{review_status}`",
                f"- Revision count: {revision_count}",
                f"- Last reviewed at: {review.get('last_reviewed_at') or '-'}",
            ]
        )
        if review.get("last_feedback"):
            lines.append(f"- Last feedback: {review.get('last_feedback')}")
        if review.get("approved_artifact_path"):
            lines.append(
                f"- Approved artifact: `{review.get('approved_artifact_path')}`"
            )
        review_history = review.get("history") or []
        if review_history:
            lines.append("- Review history:")
            for entry in review_history[-5:]:
                action = entry.get("action") or "unknown"
                at = entry.get("at") or "-"
                feedback = entry.get("feedback") or "-"
                revision = entry.get("revision")
                rev_str = f" rev={revision}" if revision else ""
                lines.append(f"  - {at}: {action}{rev_str} — {feedback}")
        lines.append("")

    finalization = build_finalization_surface(state)
    fin_status = finalization.get("status")
    if fin_status:
        lines.extend(
            [
                "## Validation scorecard",
                "",
                f"- Status: `{fin_status}`",
                f"- Attempts: {int(finalization.get('attempt_count') or 0)} / {int(finalization.get('max_attempts') or 3)}",
                f"- Last validated at: {finalization.get('last_validated_at') or '-'}",
            ]
        )
        next_action = finalization.get("operator_next_action") or {}
        if next_action.get("kind"):
            lines.append(
                f"- Operator next action: `{next_action.get('kind')}` — {next_action.get('label') or '-'}"
            )
            if next_action.get("rationale"):
                lines.append(f"  - Rationale: {next_action.get('rationale')}")
            reasons = next_action.get("reasons") or []
            if reasons:
                lines.append(
                    "  - Reasons: " + ", ".join(str(item) for item in reasons[:5])
                )
        if finalization.get("inferred_user_need"):
            lines.append(f"- Inferred user need: {finalization.get('inferred_user_need')}")
        if finalization.get("intended_recipient"):
            lines.append(f"- Intended recipient: {finalization.get('intended_recipient')}")
        if finalization.get("primary_deliverable_kind"):
            lines.append(
                f"- Primary deliverable kind: {finalization.get('primary_deliverable_kind')}"
            )
        output_decision = finalization.get("output_decision") or {}
        if output_decision:
            lines.append(
                "- Output decision: "
                f"primary={output_decision.get('primary_output_id') or '-'} "
                f"required={', '.join(output_decision.get('required_output_ids') or []) or '-'}"
            )
        decision = finalization.get("deliverable_decision") or {}
        if decision:
            lines.append(
                "- Deliverable format decision: "
                f"{decision.get('selected_kind') or '-'} "
                f"(source={decision.get('source') or '-'}, "
                f"feasible={decision.get('feasible_kind') or '-'})"
            )
        if finalization.get("internal_artifacts_count") or finalization.get(
            "candidate_artifacts_count"
        ):
            lines.append(
                "- Artifact roles: "
                f"internal={finalization.get('internal_artifacts_count')}, "
                f"candidate={finalization.get('candidate_artifacts_count')}"
            )
        validation_evidence = finalization.get("validation_evidence") or []
        if validation_evidence:
            lines.append("- Validation evidence:")
            for item in validation_evidence[:5]:
                kind = item.get("kind") or "evidence"
                summary = item.get("summary") or item.get("note") or "-"
                lines.append(f"  - [{kind}] {summary}")
        findings = finalization.get("last_validation_findings") or []
        if findings:
            passed_count = sum(1 for f in findings if f.get("passed"))
            total_count = len(findings)
            lines.append(f"- Checks: {passed_count}/{total_count} passed")
            for finding in findings:
                check = finding.get("check") or "unknown"
                passed = "PASS" if finding.get("passed") else "FAIL"
                reasons_str = ", ".join(finding.get("reasons") or []) or "ok"
                lines.append(f"  - {check}: {passed} ({reasons_str})")
        lines.append("")

    reliability_attention = build_reliability_attention(state)
    lines.extend(
        [
            "## Reliability",
            "",
            f"- Status: `{reliability_attention.get('status') or 'ok'}`",
        ]
    )
    reliability = state.get("reliability") or {}
    counters = reliability.get("failure_counters") or {}
    if counters:
        lines.append("- Failure counters:")
        for code, counter in sorted(counters.items()):
            if not isinstance(counter, dict):
                continue
            lines.append(
                f"  - `{code}`: status={counter.get('status') or '-'}, "
                f"count={int(counter.get('count') or 0)}, "
                f"fingerprint={counter.get('fingerprint') or '-'}"
            )
    conditions = reliability_attention.get("conditions") or []
    if conditions:
        lines.append("- Conditions:")
        for condition in conditions[:5]:
            lines.append(
                f"  - `{condition.get('code')}`: {condition.get('message') or '-'}"
            )
    lines.append("")

    delivery = state.get("delivery") or {}
    consistency = compute_consistency_warnings(state)
    delivery_warnings = [
        warning
        for warning in consistency.get("warnings") or []
        if str(warning.get("code") or "")
        in {
            "missing_reviewable_artifact",
            "delivery_ready_but_missing_primary",
            "delivery_artifact_handoff_failed",
            "delivery_channel_addressing_failed",
            "delivery_notification_failed",
        }
    ]
    if (
        delivery.get("outputs")
        or
        delivery.get("primary_file")
        or delivery.get("review_ready")
        or delivery.get("ready")
        or delivery_warnings
    ):
        lines.extend(
            [
                "## Delivery",
                "",
                f"- Review ready: {'yes' if delivery.get('review_ready') else 'no'}",
                f"- Ready: {'yes' if delivery.get('ready') else 'no'}",
                f"- Primary file: {delivery.get('primary_file') or '-'}",
            ]
        )
        outputs = delivery.get("outputs") or []
        if outputs:
            lines.append("- Outputs:")
            for item in outputs:
                lines.append(
                    f"  - {item.get('id') or '-'}: {item.get('path') or '-'} "
                    f"({item.get('role') or '-'})"
                )
        if delivery_warnings:
            lines.append("- Handoff warnings:")
            for warning in delivery_warnings:
                code = warning.get("code") or "unknown"
                message = warning.get("message") or "-"
                lines.append(f"  - `{code}`: {message}")
        attachments = delivery.get("attachments") or []
        if attachments:
            lines.append("- Attachments:")
            for att in attachments:
                lines.append(f"  - {att}")
        lines.append("")

    if recent_runs:
        lines.extend(["## Recent run outcomes", ""])
        for run in recent_runs:
            iteration = run.get("iteration") or "-"
            phase = run.get("phase") or "-"
            outcome = run.get("outcome") or "-"
            reason = run.get("normalized_reason") or "-"
            summary = run.get("short_summary") or "-"
            lines.append(
                f"- iter={iteration} | phase={phase} | outcome={outcome} | reason={reason} | {summary}"
            )
        lines.append("")

    lines.extend(
        [
            "## Artifacts",
            "",
            f"- State: `{task.state_path}`",
            f"- Sources JSONL: `{task.sources_path}`",
            f"- Findings JSONL: `{task.findings_path}`",
            f"- Recovery log JSONL: `{task.task_dir / 'recovery-log.jsonl'}`",
            f"- Iterations dir: `{task.iterations_dir}`",
            f"- Input dir: `{task.input_dir}`",
            f"- Corpus dir: `{task.corpus_dir}`",
            f"- Corpus manifest: `{task.corpus_manifest_path}`",
            f"- Runs TSV: `{task.runs_path}`",
            f"- Playbook: `{task.task_playbook_path}`",
            f"- Workspace dir: `{task.workspace_dir}`",
            f"- Workspace analysis dir: `{task.workspace_analysis_dir}`",
            f"- Workspace tools dir: `{task.workspace_tools_dir}`",
            f"- Workspace data dir: `{task.workspace_data_dir}`",
            f"- Workspace outputs dir: `{task.workspace_outputs_dir}`",
            f"- Workspace tmp dir: `{task.workspace_tmp_dir}`",
            f"- Workspace screenshots dir: `{task.workspace_screenshots_dir}`",
            f"- Workspace vision dir: `{task.workspace_vision_dir}`",
            f"- SQLite DB path: `{task.sqlite_db_path}`",
            f"- SQLite schema path: `{task.sqlite_schema_path}`",
            f"- SQLite queries dir: `{task.sqlite_queries_dir}`",
            f"- SQLite imports dir: `{task.sqlite_imports_dir}`",
            f"- Runtime dir: `{task.runtime_dir}`",
        ]
    )
    final_report_path = artifacts.get("final_report_path")
    if final_report_path:
        lines.append(f"- Final report: `{final_report_path}`")

    consistency = compute_consistency_warnings(state)
    if consistency.get("has_warnings"):
        lines.extend(["", "## State warnings", ""])
        for w in consistency.get("warnings") or []:
            lines.append(f"- {w.get('message')}")
        guidance = consistency.get("operator_guidance") or []
        if guidance:
            lines.extend(["", "## Operator guidance", ""])
            for g in guidance:
                code = g.get("warning_code", "unknown")
                note = g.get("note", "")
                if note:
                    lines.append(f"- **{code}**: {note}")

    return "\n".join(lines).rstrip() + "\n"


def refresh_task_playbook(
    task: ResearchTask, state: dict[str, Any] | None = None
) -> None:
    if state is None:
        state = task.read_state()
    task.ensure_layout()
    task.task_playbook_path.write_text(
        render_task_playbook(task, state), encoding="utf-8"
    )


def append_run_log(
    task: ResearchTask,
    *,
    timestamp: str,
    iteration: int | None,
    run_id: str | None,
    phase: str | None,
    outcome: str,
    normalized_reason: str | None = None,
    meaningful_progress: bool | None,
    new_sources_count: int = 0,
    new_findings_count: int = 0,
    duplicate_sources_count: int = 0,
    duplicate_findings_count: int = 0,
    low_yield_streak: int | None = None,
    topic_saturated: bool | None = None,
    short_summary: str | None = None,
) -> None:
    append_tsv_row(
        task.runs_path,
        RUNS_TSV_COLUMNS,
        {
            "timestamp": timestamp,
            "iteration": iteration,
            "run_id": run_id,
            "phase": phase,
            "outcome": outcome,
            "normalized_reason": normalized_reason,
            "meaningful_progress": meaningful_progress,
            "new_sources_count": new_sources_count,
            "new_findings_count": new_findings_count,
            "duplicate_sources_count": duplicate_sources_count,
            "duplicate_findings_count": duplicate_findings_count,
            "low_yield_streak": low_yield_streak,
            "topic_saturated": topic_saturated,
            "short_summary": compact_text(short_summary),
        },
    )
