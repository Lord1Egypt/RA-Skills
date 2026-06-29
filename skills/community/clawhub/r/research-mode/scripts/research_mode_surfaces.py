from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from research_mode_adequacy import build_adequacy_operator_next_action
from research_mode_corpus import list_corpus_entries
from research_mode_finalization import (
    build_finalization_surface,
    expected_formats_for_primary_kind,
)
from research_mode_reliability import (
    build_reliability_attention,
    merge_operator_attention,
)
from research_mode_surface_delivery import (
    DELIVERY_CHANNEL_ADDRESSING_ERROR,
    DELIVERY_NOTIFICATION_ERROR,
    classify_delivery_error,
    notification_target_shape,
)
from research_mode_task import ResearchTask
from research_mode_utils import (
    ValidationError,
    effective_lock_stale_timeout_min,
    minutes_since,
    pending_result_path,
    read_json,
    read_jsonl,
    read_tsv_rows,
    resolve_under_task,
    scheduled_worker_timeout_seconds,
)

WARNING_GUIDANCE = {
    "review_state_contradiction": {
        "checklist": [
            "Check task status and review.status",
            "Check review.review_gated",
            "Check recent request-changes or resubmission",
        ],
        "note": "Do not run worker blindly; first verify review cycle and latest transition",
    },
    "missing_reviewable_artifact": {
        "checklist": [
            "Verify artifacts.final_report_path exists",
            "Verify delivery.primary_file exists",
            "Check if final report was generated",
        ],
        "note": "Do not approve task until reviewable artifact is confirmed",
    },
    "delivery_ready_but_missing_primary": {
        "checklist": [
            "Check delivery.primary_file path",
            "Verify delivery.ready flag",
            "Check delivery surface / mark-delivered trace",
        ],
        "note": "Do not consider deliverable delivered until primary_file is confirmed",
    },
    "delivery_artifact_handoff_failed": {
        "checklist": [
            "Check finalization.primary_deliverable_kind",
            "Check finalization.candidate_artifacts",
            "Set delivery.primary_file to the review-ready task-local artifact",
        ],
        "note": "Do not approve or deliver until the candidate artifact and delivery primary file agree",
    },
    "delivery_channel_addressing_failed": {
        "checklist": [
            "Check the delivery adapter target shape",
            "Verify whether the provider expects a channel, thread, topic, or file root target",
            "Retry only after the adapter target shape is corrected",
        ],
        "note": "The delivery adapter failed because the provider target shape was not accepted",
    },
    "delivery_notification_failed": {
        "checklist": [
            "Check the failed delivery intent error",
            "Verify the provider adapter and target availability",
            "Retry only after the error is understood",
        ],
        "note": "The delivery adapter reported a failed notification send",
    },
    "active_lock_in_terminal_state": {
        "checklist": [
            "Check lock.run_id and its age",
            "Look for stale execution after terminal transition",
            "Check recovery path for this run_id",
        ],
        "note": "Do not issue new blind manual override; first verify stale/recovery path",
    },
}


def _path_format(path_value: str | None) -> str | None:
    suffix = Path(str(path_value or "")).suffix.lower().lstrip(".")
    if suffix in {"md", "markdown"}:
        return "markdown"
    return suffix or None


def _resolve_state_task_path(state: dict[str, Any], path_value: Any) -> Path | None:
    path_text = str(path_value or "").strip()
    if not path_text:
        return None
    path = Path(path_text)
    if path.is_absolute():
        return path
    task_dir = (state.get("artifacts") or {}).get("task_dir")
    if not task_dir:
        return path
    try:
        return resolve_under_task(Path(task_dir), path_text, label="state path")
    except ValidationError:
        return None


def _matching_validated_artifact(
    state: dict[str, Any],
    primary_file: Any,
) -> dict[str, Any] | None:
    primary_path = _resolve_state_task_path(state, primary_file)
    if primary_path is None:
        return None
    primary_resolved = primary_path.resolve()
    for finding in (state.get("finalization") or {}).get("last_validation_findings") or []:
        if finding.get("check") != "candidate_artifact_inspection":
            continue
        for artifact in finding.get("artifacts") or []:
            if artifact.get("reasons"):
                continue
            if artifact.get("format") == "package":
                artifact_path = artifact.get("entrypoint_path")
            elif artifact.get("source") == "final_report_markdown":
                artifact_path = (state.get("artifacts") or {}).get("final_report_path")
            else:
                artifact_path = artifact.get("path")
            candidate_path = _resolve_state_task_path(state, artifact_path)
            if candidate_path is None:
                continue
            if candidate_path.resolve() == primary_resolved:
                return artifact
    return None


def _has_candidate_artifact_inspection(state: dict[str, Any]) -> bool:
    return any(
        finding.get("check") == "candidate_artifact_inspection"
        for finding in (state.get("finalization") or {}).get("last_validation_findings") or []
    )


def _state_file_exists(state: dict[str, Any], path_value: str | None) -> bool:
    if not path_value:
        return False
    path = _resolve_state_task_path(state, path_value)
    return bool(path) and path.exists()


DELIVERY_HANDOFF_WARNING_CODES = {
    "missing_reviewable_artifact",
    "delivery_ready_but_missing_primary",
    "delivery_artifact_handoff_failed",
}
DELIVERY_INTENT_WARNING_CODES = {
    DELIVERY_CHANNEL_ADDRESSING_ERROR,
    DELIVERY_NOTIFICATION_ERROR,
}


def compute_consistency_warnings(state: dict[str, Any]) -> dict[str, Any]:
    warnings: list[dict[str, Any]] = []
    status = state.get("status")
    review = state.get("review") or {}
    delivery = state.get("delivery") or {}
    lock = state.get("lock") or {}
    artifacts = state.get("artifacts") or {}
    final_report_path = artifacts.get("final_report_path")

    if status == "awaiting_review" and review.get("status") == "changes_requested":
        warnings.append(
            {
                "code": "review_state_contradiction",
                "message": "status=awaiting_review but review.status=changes_requested",
                "details": {
                    "task_status": status,
                    "review_status": review.get("status"),
                },
            }
        )

    terminal_statuses = ("awaiting_review", "complete", "cancelled", "failed")
    if status in terminal_statuses and lock.get("status") == "held":
        warnings.append(
            {
                "code": "active_lock_in_terminal_state",
                "message": f"task status={status} but lock is still held",
                "details": {
                    "task_status": status,
                    "lock_status": lock.get("status"),
                    "lock_run_id": lock.get("run_id"),
                },
            }
        )

    if status == "awaiting_review":
        final_report_exists = _state_file_exists(state, final_report_path)
        primary_file = delivery.get("primary_file")
        primary_exists = _state_file_exists(state, primary_file)
        finalization = state.get("finalization") or {}
        candidate_artifacts = finalization.get("candidate_artifacts") or []
        has_structured_outputs = bool(
            ((state.get("working_memory") or {}).get("output_contract") or {}).get(
                "outputs"
            )
            or delivery.get("outputs")
        )
        if delivery.get("review_ready") and candidate_artifacts and not primary_file:
            warnings.append(
                {
                    "code": "delivery_artifact_handoff_failed",
                    "message": "task is review-ready with candidate artifacts but no delivery.primary_file",
                    "details": {
                        "primary_deliverable_kind": finalization.get(
                            "primary_deliverable_kind"
                        ),
                        "candidate_artifacts_count": len(candidate_artifacts),
                        "primary_file": primary_file,
                    },
                }
            )
        primary_kind = str(finalization.get("primary_deliverable_kind") or "")
        expected_formats = expected_formats_for_primary_kind(primary_kind)
        if (
            delivery.get("review_ready")
            and _has_candidate_artifact_inspection(state)
            and primary_file
            and not has_structured_outputs
            and expected_formats
            and "package" not in expected_formats
        ):
            artifact = _matching_validated_artifact(state, primary_file)
            actual_format = str((artifact or {}).get("format") or "").strip().lower()
            primary_format = actual_format or _path_format(str(primary_file or ""))
            if not artifact or actual_format not in expected_formats:
                warnings.append(
                    {
                        "code": "delivery_artifact_handoff_failed",
                        "message": "task is review-ready but delivery.primary_file does not match the validated primary deliverable format",
                        "details": {
                            "primary_deliverable_kind": finalization.get(
                                "primary_deliverable_kind"
                            ),
                            "expected_formats": sorted(expected_formats),
                            "actual_format": actual_format or None,
                            "primary_file": primary_file,
                            "primary_file_format": primary_format,
                        },
                    }
                )
        if not final_report_exists and not primary_exists:
            warnings.append(
                {
                    "code": "missing_reviewable_artifact",
                    "message": "task in awaiting_review but no valid final_report_path or primary_file exists",
                    "details": {
                        "final_report_path": final_report_path,
                        "primary_file": primary_file,
                    },
                }
            )

    if delivery.get("ready"):
        primary_file = delivery.get("primary_file")
        primary_exists = _state_file_exists(state, primary_file)
        if not primary_exists:
            warnings.append(
                {
                    "code": "delivery_ready_but_missing_primary",
                    "message": "delivery.ready=true but primary_file is missing or invalid",
                    "details": {
                        "primary_file": primary_file,
                    },
                }
            )

    for intent in state.get("delivery_intents") or []:
        if not isinstance(intent, dict) or intent.get("status") != "failed":
            continue
        error_code = str(intent.get("error_code") or "").strip() or (
            classify_delivery_error(intent.get("error")) or DELIVERY_NOTIFICATION_ERROR
        )
        if error_code not in DELIVERY_INTENT_WARNING_CODES:
            error_code = DELIVERY_NOTIFICATION_ERROR
        warnings.append(
            {
                "code": error_code,
                "message": intent.get("error") or "delivery notification failed",
                "details": {
                    "delivery_intent_id": intent.get("id"),
                    "provider_target_shape": intent.get("provider_target_shape")
                    or notification_target_shape(intent.get("notification_target")),
                },
            }
        )

    operator_guidance = []
    for warning in warnings:
        code = str(warning.get("code") or "")
        guidance = WARNING_GUIDANCE.get(code, {})
        operator_guidance.append(
            {
                "warning_code": code,
                "checklist": guidance.get("checklist", []),
                "note": guidance.get("note", ""),
            }
        )

    return {
        "warnings": warnings,
        "has_warnings": len(warnings) > 0,
        "operator_guidance": operator_guidance,
    }


def _build_consistency_attention(state: dict[str, Any]) -> dict[str, Any]:
    consistency = compute_consistency_warnings(state)
    conditions: list[dict[str, Any]] = []
    recommended_actions: list[dict[str, Any]] = []

    for warning in consistency.get("warnings") or []:
        code = str(warning.get("code") or "")
        if code not in DELIVERY_HANDOFF_WARNING_CODES | DELIVERY_INTENT_WARNING_CODES:
            continue
        conditions.append(
            {
                "code": code
                if code in DELIVERY_INTENT_WARNING_CODES
                else "delivery_artifact_handoff_failed",
                "severity": "warning",
                "message": warning.get("message")
                or "Delivery artifact handoff needs operator review.",
                "details": {
                    "warning_code": code,
                    **(warning.get("details") or {}),
                },
            }
        )

    seen_action_codes: set[str] = set()
    for guidance in consistency.get("operator_guidance") or []:
        code = str(guidance.get("warning_code") or "")
        if (
            code not in DELIVERY_HANDOFF_WARNING_CODES | DELIVERY_INTENT_WARNING_CODES
            or code in seen_action_codes
        ):
            continue
        seen_action_codes.add(code)
        recommended_actions.append(
            {
                "kind": "manual_review",
                "warning_code": code
                if code in DELIVERY_INTENT_WARNING_CODES
                else "delivery_artifact_handoff_failed",
                "note": guidance.get("note")
                or "Inspect delivery.primary_file, candidate artifacts, and review state.",
                "checklist": guidance.get("checklist") or [],
            }
        )

    return {
        "status": "manual_review_needed" if conditions else "ok",
        "has_conditions": bool(conditions),
        "conditions": conditions,
        "recommended_actions": recommended_actions,
    }


def compute_budget_phase(
    *,
    budget: dict[str, Any],
    progress: dict[str, Any],
    total_sources: int,
    total_runtime_min: float | None = None,
) -> dict[str, Any]:
    phase = "normal"
    soft_pct = 0.80
    max_iter = int(budget.get("max_iterations") or 0)
    max_src = int(budget.get("max_sources") or 0)
    max_rt = float(budget.get("max_runtime_min") or 0)
    iter_count = int(progress.get("iteration_count") or 0)

    iteration_pct = max(0, min(iter_count / max_iter, 1.0)) if max_iter > 0 else 0.0
    source_pct = min(total_sources / max_src, 1.0) if max_src > 0 else 0.0
    runtime_pct = (
        min(total_runtime_min / max_rt, 1.0)
        if max_rt > 0 and total_runtime_min is not None
        else 0.0
    )

    candidates: list[tuple[str, float]] = []
    if max_src > 0:
        candidates.append(("sources", source_pct))
    if max_iter > 0:
        candidates.append(("iterations", iteration_pct))
    if max_rt > 0 and total_runtime_min is not None:
        candidates.append(("runtime", runtime_pct))

    dominant_limit = None
    dominant_ratio = -1.0
    for name, ratio in candidates:
        if ratio > dominant_ratio:
            dominant_limit = name
            dominant_ratio = ratio
        if ratio >= 1.0:
            phase = "hard_limit"
        elif ratio >= soft_pct and phase == "normal":
            phase = "soft_limit"

    return {
        "phase": phase,
        "soft_pct": soft_pct,
        "max_iterations": max_iter,
        "max_sources": max_src,
        "max_runtime_min": max_rt,
        "iteration_pct": round(iteration_pct, 4),
        "source_pct": round(source_pct, 4),
        "runtime_pct": round(runtime_pct, 4),
        "total_runtime_min": (
            round(total_runtime_min, 2) if total_runtime_min is not None else None
        ),
        "dominant_limit": dominant_limit,
    }


def build_operator_attention(
    task: ResearchTask,
    state: dict[str, Any],
    *,
    lock_age_min: float | None = None,
    is_stale: bool = False,
) -> dict[str, Any]:
    conditions: list[dict[str, Any]] = []
    recommended_actions: list[dict[str, Any]] = []
    lock = state.get("lock") or {}
    run_id = lock.get("run_id")
    running_with_held_lock = (
        state.get("status") == "running"
        and lock.get("status") == "held"
        and bool(run_id)
    )

    if running_with_held_lock:
        pending_result = None
        pending_error = None
        try:
            pending_result = pending_result_path(task.tmp_dir, run_id)
        except ValidationError as exc:
            pending_error = str(exc)

        if pending_error:
            conditions.append(
                {
                    "code": "invalid_run_id",
                    "severity": "error",
                    "message": "The active lock run_id cannot be mapped to a safe pending result path.",
                    "details": {
                        "run_id": run_id,
                        "error": pending_error,
                    },
                }
            )
            recommended_actions.append(
                {
                    "kind": "manual_review",
                    "warning_code": "invalid_run_id",
                    "note": "Inspect state.json before attempting recovery.",
                }
            )
        elif pending_result is not None and pending_result.exists() and is_stale:
            conditions.append(
                {
                    "code": "pending_result_available",
                    "severity": "warning",
                    "message": "A stale worker left a pending result that should be recovered before continuing.",
                    "details": {
                        "run_id": run_id,
                        "result_file": str(pending_result),
                        "lock_age_min": round(lock_age_min, 2)
                        if lock_age_min is not None
                        else None,
                    },
                }
            )
            recommended_actions.append(
                {
                    "kind": "repair",
                    "command": "recover --apply-pending-result",
                    "note": "Apply the pending result through the lifecycle recovery path.",
                }
            )
        elif is_stale:
            conditions.append(
                {
                    "code": "stale_run_without_pending_result",
                    "severity": "warning",
                    "message": "The active run is stale and has no pending worker result to recover.",
                    "details": {
                        "run_id": run_id,
                        "lock_age_min": round(lock_age_min, 2)
                        if lock_age_min is not None
                        else None,
                    },
                }
            )
            recommended_actions.append(
                {
                    "kind": "fresh_continuation",
                    "command": "begin",
                    "note": "Start a fresh continuation; begin will abandon the stale run and lease new work.",
                }
            )

    condition_codes = {str(item.get("code") or "") for item in conditions}
    if "invalid_run_id" in condition_codes:
        status = "manual_review_needed"
    elif "pending_result_available" in condition_codes:
        status = "repair_needed"
    elif "stale_run_without_pending_result" in condition_codes:
        status = "fresh_continuation_recommended"
    else:
        status = "ok"

    base_attention = {
        "status": status,
        "has_conditions": bool(conditions),
        "conditions": conditions,
        "recommended_actions": recommended_actions,
    }
    merged_attention = merge_operator_attention(
        base_attention,
        _build_consistency_attention(state),
    )
    return merge_operator_attention(merged_attention, build_reliability_attention(state))


def format_source_bullet(source: dict[str, Any]) -> str:
    title = source.get("title") or source.get("url") or "untitled source"
    url = source.get("url")
    note = source.get("note")
    bullet = f"- {title}"
    if url:
        bullet += f" — {url}"
    if note:
        bullet += f" ({note})"
    return bullet


def build_summary_payload(
    task: ResearchTask,
    state: dict[str, Any],
    *,
    findings_limit: int = 5,
    sources_limit: int = 5,
) -> dict[str, Any]:
    findings_limit = max(0, findings_limit)
    sources_limit = max(0, sources_limit)
    all_findings = read_jsonl(task.findings_path)
    all_sources = read_jsonl(task.sources_path)
    recent_runs = list(reversed(read_tsv_rows(task.runs_path)[-3:]))
    recent_findings = all_findings[-findings_limit:] if findings_limit else []
    recent_sources = all_sources[-sources_limit:] if sources_limit else []
    progress = state.get("progress") or {}
    errors = state.get("errors") or {}
    budget = state.get("budget") or {}
    working_memory = state.get("working_memory") or {}
    final_report_path = state.get("artifacts", {}).get("final_report_path")
    final_report_exists = bool(final_report_path and Path(final_report_path).exists())
    budget_phase_info = compute_budget_phase(
        budget=budget,
        progress=progress,
        total_sources=len(all_sources),
        total_runtime_min=(
            minutes_since(state.get("created_at")) if state.get("created_at") else None
        ),
    )
    lock = state.get("lock") or {}
    lock_age_min = None
    timeout_min = effective_lock_stale_timeout_min(state)
    is_stale = False
    if lock.get("status") == "held" and lock.get("started_at"):
        lock_age_min = minutes_since(lock.get("started_at"))
        is_stale = lock_age_min is not None and lock_age_min > timeout_min
    operator_attention = build_operator_attention(
        task,
        state,
        lock_age_min=lock_age_min,
        is_stale=is_stale,
    )
    runtime_meta: dict[str, Any] = {}
    if task.runtime_meta_path.exists():
        try:
            loaded_meta = read_json(task.runtime_meta_path)
            if isinstance(loaded_meta, dict):
                runtime_meta = loaded_meta
        except Exception:
            runtime_meta = {}
    analysis_state = state.get("analysis") or {}
    adequacy_state = state.get("adequacy") or {}
    adequacy_operator_next_action = (
        adequacy_state.get("operator_next_action")
        or build_adequacy_operator_next_action(state, adequacy_state)
    )
    preflight_state_raw = state.get("preflight")
    preflight_configured = isinstance(preflight_state_raw, dict)
    preflight_state = preflight_state_raw if preflight_configured else {}
    preflight_artifact = preflight_state.get("artifact_markdown")
    preflight_artifact_path = None
    preflight_artifact_exists = False
    if preflight_artifact:
        artifact_path = Path(str(preflight_artifact))
        if not artifact_path.is_absolute():
            artifact_path = task.task_dir / artifact_path
        preflight_artifact_path = str(artifact_path)
        preflight_artifact_exists = artifact_path.exists()
    return {
        "id": state.get("id"),
        "title": state.get("title") or state.get("id"),
        "goal": state.get("goal"),
        "status": state.get("status"),
        "phase": state.get("phase"),
        "progress": {
            "iteration_count": int(progress.get("iteration_count") or 0),
            "meaningful_iterations": int(progress.get("meaningful_iterations") or 0),
            "max_iterations": budget.get("max_iterations") or 0,
            "last_iteration_at": progress.get("last_iteration_at"),
            "last_meaningful_progress_at": progress.get("last_meaningful_progress_at"),
        },
        "working_memory": {
            "summary": working_memory.get("summary") or "",
            "next_angle": working_memory.get("next_angle") or "",
            "open_questions": working_memory.get("open_questions") or [],
            "constraints": working_memory.get("constraints") or [],
            "deliverable": working_memory.get("deliverable"),
            "user_instructions": working_memory.get("user_instructions") or [],
            "contract": working_memory.get("contract"),
        },
        "history": {
            "last_transition": (state.get("history") or {}).get("last_transition"),
            "last_reason": (state.get("history") or {}).get("last_reason"),
            "last_terminal_reason": (state.get("history") or {}).get(
                "last_terminal_reason"
            ),
            "last_audit_marker": (state.get("history") or {}).get("last_audit_marker"),
            "audit_trail": (state.get("history") or {}).get("audit_trail") or [],
        },
        "corpus": {
            "mode": ((state.get("corpus") or {}).get("mode") or "web"),
            "entries": list_corpus_entries(task),
            "updated_at": (state.get("corpus") or {}).get("updated_at"),
        },
        "errors": {
            "failure_count": int(errors.get("failure_count") or 0),
            "consecutive_failures": int(errors.get("consecutive_failures") or 0),
            "last_error": errors.get("last_error"),
        },
        "saturation": {
            "consecutive_low_yield": int(
                (state.get("saturation") or {}).get("consecutive_low_yield") or 0
            ),
            "low_yield_threshold": int(
                (state.get("saturation") or {}).get("low_yield_threshold") or 0
            ),
            "last_iteration_new_sources": int(
                (state.get("saturation") or {}).get("last_iteration_new_sources") or 0
            ),
            "last_iteration_new_findings": int(
                (state.get("saturation") or {}).get("last_iteration_new_findings") or 0
            ),
            "last_iteration_duplicate_sources": int(
                (state.get("saturation") or {}).get("last_iteration_duplicate_sources")
                or 0
            ),
            "last_iteration_duplicate_findings": int(
                (state.get("saturation") or {}).get("last_iteration_duplicate_findings")
                or 0
            ),
            "last_low_yield_at": (state.get("saturation") or {}).get(
                "last_low_yield_at"
            ),
            "topic_saturated": bool(
                (state.get("saturation") or {}).get("topic_saturated")
            ),
        },
        "recent_runs": recent_runs,
        "recent_findings": recent_findings,
        "recent_sources": recent_sources,
        "totals": {
            "findings": len(all_findings),
            "sources": len(all_sources),
        },
        "review": {
            "status": ((state.get("review") or {}).get("status") or "pending"),
            "revision_count": int(
                (state.get("review") or {}).get("revision_count") or 0
            ),
            "last_feedback": (state.get("review") or {}).get("last_feedback"),
            "last_feedback_at": (state.get("review") or {}).get("last_feedback_at"),
            "last_reviewed_at": (state.get("review") or {}).get("last_reviewed_at"),
            "approved_artifact_path": (state.get("review") or {}).get(
                "approved_artifact_path"
            ),
            "review_gated": bool(
                (state.get("review") or {}).get("review_gated", False)
            ),
        },
        "adequacy": {
            "status": adequacy_state.get("status") or "not_started",
            "attempt_count": int(adequacy_state.get("attempt_count") or 0),
            "max_attempts": int(adequacy_state.get("max_attempts") or 2),
            "coverage_summary": adequacy_state.get("coverage_summary"),
            "coverage_gaps": adequacy_state.get("coverage_gaps") or [],
            "evidence_risks": adequacy_state.get("evidence_risks") or [],
            "contradictions": adequacy_state.get("contradictions") or [],
            "recommended_next_phase": adequacy_state.get("recommended_next_phase"),
            "recommended_next_angle": adequacy_state.get("recommended_next_angle"),
            "blocking_reasons": adequacy_state.get("blocking_reasons") or [],
            "operator_next_action": adequacy_operator_next_action,
        },
        "preflight": {
            "configured": preflight_configured,
            "done": bool(preflight_state.get("done", False)),
            "decision": preflight_state.get("decision"),
            "iteration_index": int(preflight_state.get("iteration_index") or 0),
            "iteration_limit": int(preflight_state.get("iteration_limit") or 0),
            "artifact_markdown": preflight_artifact,
            "artifact_path": preflight_artifact_path,
            "artifact_exists": preflight_artifact_exists,
            "warnings": preflight_state.get("warnings") or [],
            "blockers": preflight_state.get("blockers") or [],
            "target_phase": preflight_state.get("target_phase"),
            "completed_at": preflight_state.get("completed_at"),
        },
        "finalization": build_finalization_surface(state),
        "delivery": {
            "sent_updates": int((state.get("delivery") or {}).get("sent_updates") or 0),
            "last_update_at": (state.get("delivery") or {}).get("last_update_at"),
            "outputs": (state.get("delivery") or {}).get("outputs") or [],
            "primary_file": (state.get("delivery") or {}).get("primary_file"),
            "attachments": (state.get("delivery") or {}).get("attachments") or [],
            "ready": bool((state.get("delivery") or {}).get("ready")),
            "notification_blocked": (state.get("delivery") or {}).get(
                "notification_blocked"
            ),
            "intents": state.get("delivery_intents") or [],
        },
        "queue": {
            "status": (state.get("queue") or {}).get("status") or "free",
            "waiting_since": (state.get("queue") or {}).get("waiting_since"),
            "position": (state.get("queue") or {}).get("position"),
            "blocked_by_task_id": (state.get("queue") or {}).get(
                "blocked_by_task_id"
            ),
            "blocked_by_run_id": (state.get("queue") or {}).get("blocked_by_run_id"),
            "active_task_id": (state.get("queue") or {}).get("active_task_id"),
            "active_run_id": (state.get("queue") or {}).get("active_run_id"),
        },
        "analysis": {
            "runtime_prepared": task.runtime_meta_path.exists(),
            "runtime_tool": runtime_meta.get("tool"),
            "venv_python": runtime_meta.get("venv_python"),
            "installed_packages": runtime_meta.get("packages_installed") or [],
            "sqlite_ready": bool(runtime_meta.get("sqlite_ready")),
            "default_sqlite_db_path": runtime_meta.get("default_sqlite_db_path")
            or str(task.sqlite_db_path),
            "sqlite_schema_path": runtime_meta.get("sqlite_schema_path")
            or str(task.sqlite_schema_path),
            "sqlite_queries_dir": runtime_meta.get("sqlite_queries_dir")
            or str(task.sqlite_queries_dir),
            "sqlite_imports_dir": runtime_meta.get("sqlite_imports_dir")
            or str(task.sqlite_imports_dir),
            "workspace_screenshots_dir": str(task.workspace_screenshots_dir),
            "workspace_vision_dir": str(task.workspace_vision_dir),
            "last_iteration_code_used": bool(
                analysis_state.get("last_iteration_code_used")
            ),
            "code_used_recently": bool(analysis_state.get("code_used_recently")),
            "last_code_run_at": analysis_state.get("last_code_run_at"),
            "last_packages_used": analysis_state.get("last_packages_used") or [],
            "last_analysis_artifacts": (
                analysis_state.get("last_analysis_artifacts") or []
            ),
            "analysis_artifacts_count": int(
                analysis_state.get("analysis_artifacts_count") or 0
            ),
            "last_iteration_database_used": bool(
                analysis_state.get("last_iteration_database_used")
            ),
            "database_used_recently": bool(
                analysis_state.get("database_used_recently")
            ),
            "last_database_run_at": analysis_state.get("last_database_run_at"),
            "last_database_artifacts": (
                analysis_state.get("last_database_artifacts") or []
            ),
            "last_database_summary": analysis_state.get("last_database_summary"),
            "last_iteration_vision_used": bool(
                analysis_state.get("last_iteration_vision_used")
            ),
            "vision_used_recently": bool(analysis_state.get("vision_used_recently")),
            "last_vision_run_at": analysis_state.get("last_vision_run_at"),
            "last_vision_artifacts": (
                analysis_state.get("last_vision_artifacts") or []
            ),
            "last_vision_summary": analysis_state.get("last_vision_summary"),
        },
        "job": {
            "job_id": (state.get("job") or {}).get("job_id"),
            "mode": (state.get("job") or {}).get("mode"),
            "tick_every_min": (state.get("job") or {}).get("tick_every_min"),
            "enabled": (state.get("job") or {}).get("enabled"),
            "suspended_reason": (state.get("job") or {}).get("suspended_reason"),
            "suspended_at": (state.get("job") or {}).get("suspended_at"),
            "has_schedule_template": bool(
                (state.get("job") or {}).get("schedule_template")
            ),
        },
        "final_report": {
            "path": final_report_path,
            "exists": final_report_exists,
        },
        "artifacts": {
            "task_playbook_path": str(task.task_playbook_path),
            "task_playbook_exists": task.task_playbook_path.exists(),
            "runs_path": str(task.runs_path),
            "runs_exists": task.runs_path.exists(),
            "input_dir": str(task.input_dir),
            "corpus_dir": str(task.corpus_dir),
            "corpus_manifest_path": str(task.corpus_manifest_path),
            "workspace_dir": str(task.workspace_dir),
            "workspace_analysis_dir": str(task.workspace_analysis_dir),
            "workspace_tools_dir": str(task.workspace_tools_dir),
            "workspace_data_dir": str(task.workspace_data_dir),
            "workspace_outputs_dir": str(task.workspace_outputs_dir),
            "workspace_tmp_dir": str(task.workspace_tmp_dir),
            "workspace_screenshots_dir": str(task.workspace_screenshots_dir),
            "workspace_vision_dir": str(task.workspace_vision_dir),
            "sqlite_db_path": str(task.sqlite_db_path),
            "sqlite_schema_path": str(task.sqlite_schema_path),
            "sqlite_queries_dir": str(task.sqlite_queries_dir),
            "sqlite_imports_dir": str(task.sqlite_imports_dir),
            "runtime_dir": str(task.runtime_dir),
            "runtime_meta_path": str(task.runtime_meta_path),
            "last_recovery_note_path": (state.get("artifacts") or {}).get(
                "last_recovery_note_path"
            ),
            "last_recovery_run_id": (state.get("artifacts") or {}).get(
                "last_recovery_run_id"
            ),
            "last_recovery_result_file": (state.get("artifacts") or {}).get(
                "last_recovery_result_file"
            ),
            "last_recovery_at": (state.get("artifacts") or {}).get("last_recovery_at"),
            "last_recovery_log_path": (state.get("artifacts") or {}).get(
                "last_recovery_log_path"
            ),
            "last_pending_result_file": (state.get("artifacts") or {}).get(
                "last_pending_result_file"
            ),
        },
        "lock": {
            "status": lock.get("status"),
            "run_id": lock.get("run_id"),
            "started_at": lock.get("started_at"),
            "stale_timeout_min": lock.get("stale_timeout_min"),
            "effective_stale_timeout_min": timeout_min,
            "worker_timeout_seconds": scheduled_worker_timeout_seconds(state),
            "lock_age_min": round(lock_age_min, 2)
            if lock_age_min is not None
            else None,
            "is_stale": is_stale,
        },
        "operator_attention": operator_attention,
        "completion": (state.get("completion") or {}).get("last_validation"),
        "consistency": compute_consistency_warnings(state),
        "task_dir": str(task.task_dir),
        "budget_phase": budget_phase_info,
        "revision_diff": state.get("revision_diff"),
        "evidence_gaps": (
            state.get("evidence_gaps")
            or {
                "evidence_gaps": [],
                "high_risk_assumptions": [],
                "recommended_next_checks": [],
                "has_open_gaps": False,
            }
        ),
    }


def render_summary_text(summary: dict[str, Any]) -> str:
    progress = summary["progress"]
    errors = summary["errors"]
    working_memory = summary["working_memory"]
    max_iterations = progress["max_iterations"] or "open"
    lines = []
    if summary.get("resolved_implicitly"):
        lines.append("Resolved active task automatically.")
    lines.extend(
        [
            f"Research: {summary['title']} ({summary['id']})"
            if summary.get("title") and summary.get("title") != summary.get("id")
            else f"Research: {summary['id']}",
            f"Status: {summary['status']}",
        ]
    )
    preflight = summary.get("preflight") or {}
    if preflight.get("configured"):
        decision = preflight.get("decision") or "-"
        done = "done" if preflight.get("done") else "pending"
        target = preflight.get("target_phase") or "-"
        artifact = preflight.get("artifact_markdown") or "-"
        lines.append(
            f"Preflight: {done}, decision={decision}, target={target}, artifact={artifact}"
        )
        warnings = preflight.get("warnings") or []
        if warnings:
            lines.append(f"Preflight warnings: {'; '.join(str(w) for w in warnings[:3])}")
        blockers = preflight.get("blockers") or []
        if blockers:
            lines.append(f"Preflight blockers: {'; '.join(str(b) for b in blockers[:3])}")
    else:
        lines.append("Preflight: not configured")
    lock_info = summary.get("lock") or {}
    if lock_info.get("status") == "held":
        age = lock_info.get("lock_age_min")
        stale = lock_info.get("is_stale")
        timeout = (
            lock_info.get("effective_stale_timeout_min")
            or lock_info.get("stale_timeout_min")
            or 30
        )
        if age is not None:
            age_str = f"{age:.1f}m"
            stale_str = " (STALE)" if stale else " (active)"
            lines.append(f"Lock: held {age_str}{stale_str}, timeout={timeout}m")
    attention = summary.get("operator_attention") or {}
    if attention.get("status") and attention.get("status") != "ok":
        lines.append(f"Operator attention: {attention.get('status')}")
        for condition in (attention.get("conditions") or [])[:5]:
            code = condition.get("code") or "unknown"
            message = condition.get("message") or ""
            lines.append(f"- {code}: {message}" if message else f"- {code}")
        for action in (attention.get("recommended_actions") or [])[:3]:
            label = action.get("command") or action.get("warning_code") or action.get("kind")
            note = action.get("note") or ""
            lines.append(f"Recommended action: {label} — {note}" if note else f"Recommended action: {label}")
    queue = summary.get("queue") or {}
    if queue.get("status") == "waiting":
        lines.append("Queue: waiting for global research worker")
        if queue.get("blocked_by_task_id") or queue.get("blocked_by_run_id"):
            lines.append(
                f"Blocked by: {queue.get('blocked_by_task_id') or '-'} / {queue.get('blocked_by_run_id') or '-'}"
            )
        if queue.get("position"):
            lines.append(f"Queue position: {queue.get('position')}")
    elif queue.get("status") == "running":
        lines.append(
            f"Queue: running as {queue.get('active_task_id') or '-'} / {queue.get('active_run_id') or '-'}"
        )
    lines.extend(
        [
            f"Phase: {summary['phase']}",
            f"Goal: {summary.get('goal') or '-'}",
            f"Iterations: {progress['iteration_count']} / {max_iterations}",
            f"Meaningful iterations: {progress['meaningful_iterations']}",
            f"Sources collected: {summary['totals']['sources']}",
            f"Findings collected: {summary['totals']['findings']}",
        ]
    )
    job = summary.get("job") or {}
    if job.get("job_id"):
        enabled = job.get("enabled")
        cron_state = "enabled" if enabled is True else "disabled" if enabled is False else "unknown"
        schedule = job.get("tick_every_min") or job.get("mode") or "-"
        cron_line = f"Cron: {cron_state}, every={schedule}"
        if job.get("suspended_reason"):
            cron_line += f", reason={job.get('suspended_reason')}"
        lines.append(cron_line)
    elif job.get("has_schedule_template"):
        lines.append("Cron: template available, no bound job")
    bp = summary.get("budget_phase") or {}
    if bp:
        lines.append(
            f"Budget: phase={bp.get('phase')}, "
            f"iter_pct={bp.get('iteration_pct', 0):.0%}, "
            f"src_pct={bp.get('source_pct', 0):.0%}, "
            f"rt_pct={bp.get('runtime_pct', 0):.0%}, "
            f"limit={bp.get('dominant_limit') or 'none'}"
        )
    adequacy = summary.get("adequacy") or {}
    if adequacy:
        gaps = adequacy.get("coverage_gaps") or adequacy.get("blocking_reasons") or []
        gap_text = ""
        if gaps:
            first_gap = gaps[0]
            if isinstance(first_gap, dict):
                gap_text = first_gap.get("gap") or first_gap.get("reason") or first_gap.get("text") or ""
            else:
                gap_text = str(first_gap)
        lines.append(
            "Adequacy: "
            f"status={adequacy.get('status')}, "
            f"attempts={adequacy.get('attempt_count')}/{adequacy.get('max_attempts')}, "
            f"next={adequacy.get('recommended_next_phase') or '-'}"
            + (f", gap={gap_text}" if gap_text else "")
        )
    lines.extend(
        [
            f"Failures: {errors['failure_count']} (consecutive {errors['consecutive_failures']})",
            f"Last meaningful progress: {progress.get('last_meaningful_progress_at') or '-'}",
            f"Working summary: {working_memory.get('summary') or '-'}",
            f"Next angle: {working_memory.get('next_angle') or '-'}",
        ]
    )
    analysis = summary.get("analysis") or {}
    if analysis.get("runtime_prepared"):
        installed = analysis.get("installed_packages") or []
        pkg_text = ", ".join(installed[:5]) if installed else "none"
        lines.append(
            f"Analysis runtime: prepared, tool={analysis.get('runtime_tool') or '-'}, packages={pkg_text}"
        )
    if analysis.get("sqlite_ready"):
        lines.append(
            f"SQLite helper: ready, db={analysis.get('default_sqlite_db_path') or '-'}"
        )
    if analysis.get("last_iteration_code_used") or analysis.get("code_used_recently"):
        lines.append(
            f"Code-assisted analysis: recent={'yes' if analysis.get('code_used_recently') else 'no'}, last_at={analysis.get('last_code_run_at') or '-'}"
        )
        artifacts = analysis.get("last_analysis_artifacts") or []
        if artifacts:
            lines.append("Recent analysis artifacts:")
            for artifact in artifacts[:5]:
                kind = artifact.get("kind") or "artifact"
                artifact_path = artifact.get("path") or "-"
                note = artifact.get("note")
                suffix = f" — {note}" if note else ""
                lines.append(f"- [{kind}] {artifact_path}{suffix}")
    if analysis.get("last_iteration_database_used") or analysis.get(
        "database_used_recently"
    ):
        db_summary = analysis.get("last_database_summary") or {}
        lines.append(
            f"SQLite-backed analysis: recent={'yes' if analysis.get('database_used_recently') else 'no'}, last_at={analysis.get('last_database_run_at') or '-'}"
        )
        if db_summary.get("purpose"):
            lines.append(f"DB purpose: {db_summary.get('purpose')}")
        if db_summary.get("tables"):
            lines.append(
                f"DB tables: {', '.join(str(t) for t in (db_summary.get('tables') or [])[:8])}"
            )
        db_artifacts = analysis.get("last_database_artifacts") or []
        if db_artifacts:
            lines.append("Recent database artifacts:")
            for artifact in db_artifacts[:5]:
                kind = artifact.get("kind") or "artifact"
                artifact_path = artifact.get("path") or "-"
                note = artifact.get("note")
                suffix = f" — {note}" if note else ""
                lines.append(f"- [{kind}] {artifact_path}{suffix}")
    if analysis.get("last_iteration_vision_used") or analysis.get(
        "vision_used_recently"
    ):
        vision_summary = analysis.get("last_vision_summary") or {}
        lines.append(
            f"Vision-assisted analysis: recent={'yes' if analysis.get('vision_used_recently') else 'no'}, last_at={analysis.get('last_vision_run_at') or '-'}"
        )
        if vision_summary.get("purpose"):
            lines.append(f"Vision purpose: {vision_summary.get('purpose')}")
        if vision_summary.get("confidence"):
            lines.append(f"Vision confidence: {vision_summary.get('confidence')}")
        vision_artifacts = analysis.get("last_vision_artifacts") or []
        if vision_artifacts:
            lines.append("Recent vision artifacts:")
            for artifact in vision_artifacts[:5]:
                kind = artifact.get("kind") or "artifact"
                artifact_path = artifact.get("path") or "-"
                note = artifact.get("note")
                suffix = f" — {note}" if note else ""
                lines.append(f"- [{kind}] {artifact_path}{suffix}")
    history = summary.get("history") or {}
    if history.get("last_transition"):
        lines.append(f"Last transition: {history.get('last_transition')}")
    if history.get("last_reason"):
        lines.append(f"Last reason: {history.get('last_reason')}")
    if history.get("last_terminal_reason"):
        lines.append(f"Last terminal reason: {history.get('last_terminal_reason')}")
    saturation = summary.get("saturation") or {}
    lines.append(
        f"Low-yield streak: {saturation.get('consecutive_low_yield', 0)} / {saturation.get('low_yield_threshold', 0) or '-'}"
    )
    lines.append(
        f"Topic saturated: {'yes' if saturation.get('topic_saturated') else 'no'}"
    )
    lines.append(
        "Last append metrics: "
        f"+sources={saturation.get('last_iteration_new_sources', 0)}, "
        f"+findings={saturation.get('last_iteration_new_findings', 0)}, "
        f"dup_sources={saturation.get('last_iteration_duplicate_sources', 0)}, "
        f"dup_findings={saturation.get('last_iteration_duplicate_findings', 0)}"
    )
    review = summary.get("review") or {}
    is_review_gated = summary.get("status") == "awaiting_review"
    if is_review_gated:
        lines.append(
            "Status note: awaiting_user_review — cron short-circuits; "
            "use approve/request-changes/stop to proceed"
        )
        last_feedback = review.get("last_feedback")
        revision_count = review.get("revision_count") or 0
        if last_feedback:
            lines.append(f"  Pending feedback (rev {revision_count}): {last_feedback}")
        review_status = review.get("status") or "pending"
        if review_status != "pending":
            lines.append(f"  Review status: {review_status}")
        audit_marker = (summary.get("history") or {}).get("last_audit_marker")
        if audit_marker:
            lines.append(f"  Audit: {audit_marker}")
    if review.get("status") and review.get("status") != "pending":
        lines.append(
            f"Review: status={review.get('status')}, "
            f"revision={review.get('revision_count')}, "
            f"last_feedback={review.get('last_feedback') or '-'}"
        )
    elif review.get("revision_count", 0) > 0:
        lines.append(f"Review: revision={review.get('revision_count')}")
    finalization = summary.get("finalization") or {}
    if finalization.get("status"):
        lines.append(
            f"Finalization: status={finalization.get('status')}, "
            f"attempts={finalization.get('attempt_count')}/{finalization.get('max_attempts')}"
        )
        next_action = finalization.get("operator_next_action") or {}
        if next_action.get("kind"):
            lines.append(
                f"Operator next action: {next_action.get('kind')} — "
                f"{next_action.get('label') or '-'}"
            )
            if next_action.get("rationale"):
                lines.append(f"  Rationale: {next_action.get('rationale')}")
            reasons = next_action.get("reasons") or []
            if reasons:
                lines.append(f"  Reasons: {', '.join(str(r) for r in reasons[:5])}")
        if finalization.get("inferred_user_need"):
            lines.append(f"Finalization need: {finalization.get('inferred_user_need')}")
        if finalization.get("intended_recipient"):
            lines.append(f"Finalization recipient: {finalization.get('intended_recipient')}")
        if finalization.get("primary_deliverable_kind"):
            lines.append(
                f"Primary deliverable: {finalization.get('primary_deliverable_kind')}"
            )
        if (
            finalization.get("internal_artifacts_count")
            or finalization.get("candidate_artifacts_count")
            or finalization.get("validation_evidence_count")
        ):
            lines.append(
                "Finalization artifacts: "
                f"internal={finalization.get('internal_artifacts_count')}, "
                f"candidate={finalization.get('candidate_artifacts_count')}, "
                f"evidence={finalization.get('validation_evidence_count')}"
            )
        blocking_defects = finalization.get("blocking_defects") or []
        if blocking_defects:
            lines.append(f"Blocking defects ({len(blocking_defects)}):")
            for defect in blocking_defects[:5]:
                text = defect.get("summary") or defect.get("text") or json.dumps(
                    defect, ensure_ascii=False
                )
                lines.append(f"  - {text}")
        findings = finalization.get("last_validation_findings") or []
        if findings:
            lines.append("Validation scorecard:")
            for f in findings:
                check = f.get("check") or "unknown"
                passed = "PASS" if f.get("passed") else "FAIL"
                reasons_str = ", ".join(f.get("reasons") or []) or "ok"
                lines.append(f"  [{passed}] {check}: {reasons_str}")
    revision_diff = summary.get("revision_diff") or {}
    if revision_diff.get("changes"):
        lines.append(
            f"Revision diff: rev {revision_diff.get('revision_from')} -> {revision_diff.get('revision_to')}"
        )
        for change in revision_diff.get("changes") or []:
            lines.append(f"  - {change}")
    evidence_gaps = summary.get("evidence_gaps") or {}
    if evidence_gaps.get("has_open_gaps"):
        gaps = evidence_gaps.get("evidence_gaps") or []
        assumptions = evidence_gaps.get("high_risk_assumptions") or []
        checks = evidence_gaps.get("recommended_next_checks") or []
        lines.append(f"Evidence gaps ({len(gaps)}):")
        for gap in gaps[:5]:
            lines.append(f"  - {gap}")
        if assumptions:
            lines.append(f"High-risk assumptions ({len(assumptions)}):")
            for a in assumptions:
                lines.append(f"  - {a}")
        if checks:
            lines.append("Recommended next checks:")
            for c in checks:
                lines.append(f"  - {c}")
    delivery = summary.get("delivery") or {}
    if delivery.get("primary_file") or delivery.get("ready"):
        lines.append(
            f"Delivery: ready={delivery.get('ready')}, "
            f"primary={delivery.get('primary_file') or '-'}"
        )
    corpus = summary.get("corpus") or {}
    lines.append(
        f"Corpus: mode={corpus.get('mode') or 'web'}, files={len(corpus.get('entries') or [])}"
    )
    constraints = working_memory.get("constraints") or []
    if constraints:
        lines.extend(["Constraints:"])
        for item in constraints:
            lines.append(f"- {item}")
    deliverable = working_memory.get("deliverable")
    if deliverable:
        lines.append(f"Deliverable: {deliverable}")
    contract = working_memory.get("contract")
    if contract:
        sections = contract.get("required_sections") or []
        sheets = contract.get("required_sheets") or []
        if sections:
            lines.append(f"Contract sections: {', '.join(sections)}")
        if sheets:
            lines.append(f"Contract sheets: {', '.join(sheets)}")
    user_instructions = working_memory.get("user_instructions") or []
    if user_instructions:
        lines.extend(["User instructions:"])
        for item in user_instructions:
            lines.append(f"- {item}")
    open_questions = working_memory.get("open_questions") or []
    if open_questions:
        lines.extend(["Open questions:"])
        for question in open_questions:
            lines.append(f"- {question}")
    recent_runs = summary.get("recent_runs") or []
    if recent_runs:
        lines.extend([f"Recent run outcomes ({len(recent_runs)}):"])
        for run in recent_runs:
            iteration = run.get("iteration") or "-"
            phase = run.get("phase") or "-"
            outcome = run.get("outcome") or "-"
            normalized_reason = run.get("normalized_reason") or "-"
            short_summary = run.get("short_summary") or "-"
            lines.append(
                f"- iter={iteration} | phase={phase} | outcome={outcome} | reason={normalized_reason} | {short_summary}"
            )
    recent_findings = summary.get("recent_findings") or []
    if recent_findings:
        lines.extend(
            [
                f"Recent findings ({len(recent_findings)} of {summary['totals']['findings']}):"
            ]
        )
        for finding in recent_findings:
            kind = finding.get("kind") or "note"
            text = finding.get("text") or json.dumps(finding, ensure_ascii=False)
            lines.append(f"- [{kind}] {text}")
    recent_sources = summary.get("recent_sources") or []
    if recent_sources:
        lines.extend(
            [
                f"Recent sources ({len(recent_sources)} of {summary['totals']['sources']}):"
            ]
        )
        for source in recent_sources:
            lines.append(format_source_bullet(source))
    final_report = summary.get("final_report") or {}
    if final_report.get("exists"):
        lines.append(f"Final report: {final_report.get('path')}")
    completion = summary.get("completion") or {}
    if completion:
        lines.append(
            f"Completion validation: {'passed' if completion.get('passed') else 'failed'}"
        )
        reasons = completion.get("reasons") or []
        if reasons:
            lines.append(
                f"Completion reasons: {', '.join(str(item) for item in reasons)}"
            )
        deliverable_checks = (completion.get("deliverable_validation") or {}).get(
            "checks"
        ) or []
        if deliverable_checks:
            lines.append("Deliverable checks:")
            for check in deliverable_checks:
                kind = check.get("kind") or "unknown"
                status = "passed" if check.get("passed") else "failed"
                lines.append(f"- {kind}: {status}")
    artifacts = summary.get("artifacts") or {}
    recovery_note_path = artifacts.get("last_recovery_note_path")
    if recovery_note_path:
        lines.append(f"Recovery note: {recovery_note_path}")
    recovery_log_path = artifacts.get("last_recovery_log_path")
    if recovery_log_path:
        lines.append(f"Recovery log: {recovery_log_path}")
    pending_result_file = artifacts.get("last_pending_result_file")
    if pending_result_file:
        lines.append(f"Recovered pending result: {pending_result_file}")
    if artifacts.get("task_playbook_exists"):
        lines.append(f"Task playbook: {artifacts.get('task_playbook_path')}")
    if artifacts.get("runs_exists"):
        lines.append(f"Runs TSV: {artifacts.get('runs_path')}")
    if artifacts.get("input_dir"):
        lines.append(f"Input dir: {artifacts.get('input_dir')}")
    if artifacts.get("corpus_dir"):
        lines.append(f"Corpus dir: {artifacts.get('corpus_dir')}")
    if artifacts.get("corpus_manifest_path"):
        lines.append(f"Corpus manifest: {artifacts.get('corpus_manifest_path')}")
    consistency = summary.get("consistency") or {}
    if consistency.get("has_warnings"):
        lines.append("State warnings:")
        for w in consistency.get("warnings") or []:
            lines.append(f"- {w.get('message')}")
        guidance = consistency.get("operator_guidance") or []
        if guidance:
            lines.append("Operator guidance:")
            for g in guidance:
                code = g.get("warning_code", "unknown")
                note = g.get("note", "")
                if note:
                    lines.append(f"- {code}: {note}")
                checklist = g.get("checklist") or []
                if checklist:
                    for item in checklist[:2]:
                        lines.append(f"  - {item}")
    lines.append(f"Task dir: {summary['task_dir']}")
    return "\n".join(lines) + "\n"


def build_synthesis_payload(
    task: ResearchTask,
    state: dict[str, Any],
    *,
    findings_limit: int = 12,
    sources_limit: int = 12,
) -> dict[str, Any]:
    all_findings = read_jsonl(task.findings_path)
    all_sources = read_jsonl(task.sources_path)
    findings_limit = max(0, findings_limit)
    sources_limit = max(0, sources_limit)
    selected_findings = all_findings[-findings_limit:] if findings_limit else []
    selected_sources = all_sources[-sources_limit:] if sources_limit else []
    progress = state.get("progress") or {}
    working_memory = state.get("working_memory") or {}
    budget = state.get("budget") or {}
    budget_phase_info = compute_budget_phase(
        budget=budget,
        progress=progress,
        total_sources=len(all_sources),
        total_runtime_min=(
            minutes_since(state.get("created_at")) if state.get("created_at") else None
        ),
    )
    from research_mode_lifecycle_helpers import (
        build_evidence_gaps,
        compute_source_quality_score,
        enrich_findings_with_provenance,
    )

    provenance_findings = enrich_findings_with_provenance(
        selected_findings, selected_sources
    )
    scored_sources = [
        {**src, "quality": compute_source_quality_score(src)}
        for src in selected_sources
    ]
    evidence_gaps = build_evidence_gaps(state)
    return {
        "id": state.get("id"),
        "title": state.get("title") or state.get("id"),
        "goal": state.get("goal") or "",
        "status": state.get("status"),
        "phase": state.get("phase"),
        "iteration_count": int(progress.get("iteration_count") or 0),
        "meaningful_iterations": int(progress.get("meaningful_iterations") or 0),
        "working_summary": working_memory.get("summary") or "",
        "next_angle": working_memory.get("next_angle") or "",
        "open_questions": working_memory.get("open_questions") or [],
        "constraints": working_memory.get("constraints") or [],
        "deliverable": working_memory.get("deliverable"),
        "contract": working_memory.get("contract"),
        "user_instructions": working_memory.get("user_instructions") or [],
        "saturation": {
            "consecutive_low_yield": int(
                (state.get("saturation") or {}).get("consecutive_low_yield") or 0
            ),
            "low_yield_threshold": int(
                (state.get("saturation") or {}).get("low_yield_threshold") or 0
            ),
            "topic_saturated": bool(
                (state.get("saturation") or {}).get("topic_saturated")
            ),
        },
        "findings": provenance_findings,
        "sources": scored_sources,
        "totals": {
            "findings": len(all_findings),
            "sources": len(all_sources),
        },
        "task_dir": str(task.task_dir),
        "budget_phase": budget_phase_info,
        "evidence_gaps": evidence_gaps,
        "review": state.get("review") or {},
        "revision_count": int((state.get("review") or {}).get("revision_count") or 0),
    }


def render_synthesis_markdown(synthesis: dict[str, Any]) -> str:
    lines = [
        f"# Draft report — {synthesis['title']}",
        "",
        "## Goal",
        "",
        synthesis.get("goal") or "(goal not provided)",
        "",
        "## Current status",
        "",
        f"- Status: `{synthesis.get('status')}`",
        f"- Phase: `{synthesis.get('phase')}`",
        f"- Iterations: {synthesis.get('iteration_count')} (meaningful: {synthesis.get('meaningful_iterations')})",
        f"- Sources collected: {synthesis['totals']['sources']}",
        f"- Findings collected: {synthesis['totals']['findings']}",
        f"- Low-yield streak: {(synthesis.get('saturation') or {}).get('consecutive_low_yield', 0)} / {((synthesis.get('saturation') or {}).get('low_yield_threshold', 0) or '-')}",
        f"- Topic saturated: {'yes' if (synthesis.get('saturation') or {}).get('topic_saturated') else 'no'}",
    ]
    bp = synthesis.get("budget_phase") or {}
    if bp:
        lines.extend(
            [
                f"- Budget phase: `{bp.get('phase')}` "
                f"(iter {bp.get('iteration_pct', 0):.0%}, "
                f"src {bp.get('source_pct', 0):.0%}, "
                f"rt {bp.get('runtime_pct', 0):.0%}, "
                f"limit={bp.get('dominant_limit') or 'none'})"
            ]
        )
    lines.extend(
        [
            "",
            "## Working synthesis",
            "",
            synthesis.get("working_summary") or "(no working summary yet)",
            "",
        ]
    )

    constraints = synthesis.get("constraints") or []
    if constraints:
        lines.extend(["## Constraints", ""])
        for item in constraints:
            lines.append(f"- {item}")
        lines.append("")

    deliverable = synthesis.get("deliverable")
    if deliverable:
        lines.extend(["## Target deliverable", "", deliverable, ""])

    contract = synthesis.get("contract")
    if contract:
        sections = contract.get("required_sections") or []
        sheets = contract.get("required_sheets") or []
        lines.append("## Deliverable contract")
        if sections:
            lines.append("- Required sections:")
            for s in sections:
                lines.append(f"  - {s}")
        if sheets:
            lines.append("- Required sheets:")
            for s in sheets:
                lines.append(f"  - {s}")
        if not (sections or sheets):
            lines.append("- (contract defined, no specific requirements listed)")
        lines.append("")

    user_instructions = synthesis.get("user_instructions") or []
    if user_instructions:
        lines.extend(["## User instructions", ""])
        for item in user_instructions:
            lines.append(f"- {item}")
        lines.append("")

    findings = synthesis.get("findings") or []
    if findings:
        lines.extend(["## Key findings", ""])
        for finding in findings:
            kind = finding.get("kind") or "note"
            text = finding.get("text") or json.dumps(finding, ensure_ascii=False)
            provenance = finding.get("provenance") or {}
            tier = provenance.get("tier", "unknown")
            badge_map = {
                "high": "[●●●]",
                "medium": "[●●○]",
                "low": "[●○○]",
                "reserve": "[○○○]",
            }
            badge = badge_map.get(tier, "[???]")
            refs = finding.get("source_urls") or []
            bullet = f"- **{kind}** {badge}: {text}"
            if refs:
                bullet += f" (refs: {', '.join(refs)})"
            conf_parts = []
            if tier and tier != "unknown":
                conf_parts.append(f"conf={tier}")
            src_count = provenance.get("source_count", 0)
            if src_count:
                conf_parts.append(f"src={src_count}")
            if conf_parts:
                bullet += f" [{', '.join(conf_parts)}]"
            lines.append(bullet)
        lines.append("")
    else:
        lines.extend(
            ["## Key findings", "", "- Findings have not been accumulated yet.", ""]
        )

    open_questions = synthesis.get("open_questions") or []
    if open_questions:
        lines.extend(["## Open questions", ""])
        for question in open_questions:
            lines.append(f"- {question}")
        lines.append("")

    next_angle = synthesis.get("next_angle")
    if next_angle:
        lines.extend(["## Next angle", "", next_angle, ""])

    sources = synthesis.get("sources") or []
    if sources:
        lines.extend(["## Evidence base", ""])
        for source in sources:
            quality = source.get("quality") or {}
            qbadge_map = {
                "strong": "●●",
                "standard": "●○",
                "weak": "○○",
                "poor": "··",
            }
            qbadge = qbadge_map.get(quality.get("tier", ""), "??")
            title = source.get("title") or source.get("url") or "untitled source"
            url = source.get("url")
            note = source.get("note")
            bullet = f"- [{qbadge}] " + (f"[{title}]({url})" if url else title)
            if quality.get("factors"):
                bullet += f" (quality: {', '.join(quality['factors'])})"
            if note:
                bullet += f" — {note}"
            lines.append(bullet)
        lines.append("")
    else:
        lines.extend(
            ["## Evidence base", "", "- Sources have not been accumulated yet.", ""]
        )

    evidence_gaps = synthesis.get("evidence_gaps") or {}
    if evidence_gaps.get("has_open_gaps"):
        gaps = evidence_gaps.get("evidence_gaps") or []
        assumptions = evidence_gaps.get("high_risk_assumptions") or []
        next_checks = evidence_gaps.get("recommended_next_checks") or []
        lines.extend(["## Evidence gaps", ""])
        for gap in gaps:
            lines.append(f"- {gap}")
        if assumptions:
            lines.append("")
            lines.append("**High-risk assumptions:**")
            for a in assumptions:
                lines.append(f"- {a}")
        if next_checks:
            lines.append("")
            lines.append("**Recommended checks:**")
            for c in next_checks:
                lines.append(f"- {c}")
        lines.append("")

    review = synthesis.get("review") or {}
    revision_count = synthesis.get("revision_count") or 0
    if revision_count > 0:
        lines.extend(["## Review context", ""])
        lines.append(f"- Revision count: {revision_count}")
        review_status = review.get("status") or "pending"
        lines.append(f"- Review status: {review_status}")
        last_feedback = review.get("last_feedback")
        if last_feedback:
            lines.append(f"- Last feedback: {last_feedback}")
        lines.append("")

    lines.extend(
        [
            "## Notes for finalization",
            "",
            "- Use this draft as synthesis scaffolding, not as the final truth.",
            "- Before marking the research complete, verify that the key claims are supported by the cited evidence base.",
            "- Remove any repeated findings and tighten the narrative for the final report.",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"
