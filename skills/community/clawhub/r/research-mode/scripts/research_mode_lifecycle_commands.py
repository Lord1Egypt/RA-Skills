from __future__ import annotations

import argparse
import hashlib
import shutil
import uuid
from pathlib import Path
from typing import Any

from research_mode_lifecycle_helpers import (
    build_revision_diff,
    clear_reviewable_candidate,
    compose_failure_update_text,
    compose_finish_update_text,
    compute_low_yield,
    make_work_order,
    render_default_final_report,
    should_notify,
    stale_lock,
    validate_candidate_final,
    validate_completion,
)
from research_mode_adequacy import (
    build_adequacy_operator_next_action,
    collect_adequacy_reasons,
    route_phase_for_adequacy_status,
)
from research_mode_surfaces import compute_budget_phase
from research_mode_payloads import (
    adequacy_defaults,
    finalization_defaults,
    normalize_analysis_artifacts,
    normalize_adequacy_review,
    normalize_database_artifacts,
    normalize_database_summary,
    normalize_findings,
    normalize_finalization_trace,
    normalize_sources,
    normalize_string_list,
    normalize_vision_artifacts,
    normalize_vision_summary,
)
from research_mode_reasons import (
    reason_for_begin_short_circuit,
    reason_for_failure,
    reason_for_finish,
    set_history_reason,
)
from research_mode_reliability import clear_failure_counter, record_failure_event
from research_mode_queue import acquire_global_queue, release_global_queue
from research_mode_reporting import append_run_log, refresh_task_playbook
from research_mode_runtime import (
    clear_bound_job,
    remove_cron_job,
    snapshot_job_binding,
    suspend_bound_job,
)
from research_mode_finalization import expected_formats_for_primary_kind
from research_mode_surface_delivery import (
    classify_delivery_error,
    notification_target_shape,
)
from research_mode_task import ResearchTask, StateManager
from research_mode_utils import (
    NO_ACTIVE_LEASE,
    ValidationError,
    append_jsonl,
    atomic_text_write,
    ensure_dir,
    json_dump,
    minutes_since,
    pending_result_path,
    parse_ts,
    read_json,
    resolve_under_task,
    scheduled_worker_timeout_seconds,
    utc_now,
)

FINAL_STATUSES = {"complete", "failed", "cancelled"}
REVIEW_WAIT_STATUSES = {"awaiting_review"}
PHASES = {"preflight", "search", "analyze", "synthesize", "verify", "finalize"}
PREFLIGHT_DECISIONS = {"go", "go_with_warnings", "needs_setup", "blocked", "skipped"}
WORKER_PREFLIGHT_DECISIONS = PREFLIGHT_DECISIONS - {"skipped"}


def _replace_state_contents(state: dict[str, Any], updated: dict[str, Any]) -> None:
    state.clear()
    state.update(updated)


def _record_completion_validation_rejection(
    state: dict[str, Any],
    *,
    run_id: str,
    phase: str,
    completion_validation: dict[str, Any],
    at: str,
) -> None:
    updated = record_failure_event(
        state,
        {
            "code": "completion_validation_retry_loop",
            "severity": "warning",
            "phase": phase,
            "run_id": run_id,
            "reasons": completion_validation.get("reasons") or [],
        },
        at=at,
    )
    _replace_state_contents(state, updated)


def _clear_completion_validation_retry_counter(
    state: dict[str, Any],
    *,
    at: str,
) -> None:
    counter = (
        ((state.get("reliability") or {}).get("failure_counters") or {}).get(
            "completion_validation_retry_loop"
        )
        or {}
    )
    if counter.get("status") != "active":
        return
    updated = clear_failure_counter(
        state,
        "completion_validation_retry_loop",
        at=at,
    )
    _replace_state_contents(state, updated)


def _normalize_preflight_payload(value: Any) -> dict[str, Any]:
    if value in (None, ""):
        value = {}
    if not isinstance(value, dict):
        raise ValidationError("preflight must be an object")
    decision = str(value.get("decision") or "go").strip() or "go"
    if decision not in WORKER_PREFLIGHT_DECISIONS:
        raise ValidationError(f"Unsupported preflight.decision: {decision}")
    return {
        "decision": decision,
        "warnings": normalize_string_list(value.get("warnings") or []),
        "blockers": normalize_string_list(value.get("blockers") or []),
        "notes": str(value.get("notes") or "").strip() or None,
    }


def _render_preflight_markdown(payload: dict[str, Any], preflight: dict[str, Any]) -> str:
    lines = [
        "# Research Preflight",
        "",
        f"- Decision: `{preflight['decision']}`",
        f"- Summary: {payload['summary']}",
    ]
    warnings = preflight.get("warnings") or []
    blockers = preflight.get("blockers") or []
    if warnings:
        lines.extend(["", "## Warnings", *[f"- {item}" for item in warnings]])
    if blockers:
        lines.extend(["", "## Blockers", *[f"- {item}" for item in blockers]])
    if preflight.get("notes"):
        lines.extend(["", "## Notes", str(preflight["notes"])])
    return "\n".join(lines).rstrip() + "\n"


def _run_v13_finalization_validation(
    task: ResearchTask,
    state: dict[str, Any],
    payload: dict[str, Any],
    report_markdown: str,
) -> dict[str, Any]:
    finalization = state.get("finalization") or {}
    max_attempts = int(finalization.get("max_attempts") or 3)
    current_attempts = int(finalization.get("attempt_count") or 0)

    validation_result = validate_candidate_final(
        task, state, payload, report_markdown=report_markdown
    )

    if validation_result["passed"]:
        return {
            **validation_result,
            "max_attempts": max_attempts,
            "attempt_count": current_attempts + 1,
        }

    if current_attempts + 1 >= max_attempts:
        return {
            **validation_result,
            "max_attempts": max_attempts,
            "attempt_count": current_attempts + 1,
            "status": "needs_intervention",
        }

    return {
        **validation_result,
        "max_attempts": max_attempts,
        "attempt_count": current_attempts + 1,
        "status": "rework",
    }


def _package_delivery_from_validation(
    validation_result: dict[str, Any] | None,
) -> dict[str, Any] | None:
    if not validation_result or not validation_result.get("passed"):
        return None
    for finding in validation_result.get("findings") or []:
        if finding.get("check") != "candidate_artifact_inspection":
            continue
        for artifact in finding.get("artifacts") or []:
            if artifact.get("format") != "package" or artifact.get("reasons"):
                continue
            package_path = artifact.get("package_path")
            entrypoint_path = artifact.get("entrypoint_path")
            if package_path and entrypoint_path:
                return {
                    "package_path": package_path,
                    "primary_file": entrypoint_path,
                    "attachments": artifact.get("attachments") or [],
                }
    return None


def _primary_file_from_validation(
    task: ResearchTask,
    validation_result: dict[str, Any] | None,
) -> str | None:
    if not validation_result or not validation_result.get("passed"):
        return None

    decision = validation_result.get("deliverable_decision") or {}
    selected_kind = str(decision.get("selected_kind") or "").strip().lower()
    expected_formats = expected_formats_for_primary_kind(selected_kind)
    if not expected_formats:
        return None

    for finding in validation_result.get("findings") or []:
        if finding.get("check") != "candidate_artifact_inspection":
            continue
        for artifact in finding.get("artifacts") or []:
            artifact_format = str(artifact.get("format") or "").strip().lower()
            if artifact_format not in expected_formats:
                continue
            if artifact.get("reasons"):
                continue
            if not artifact.get("exists") or not artifact.get("inside_task"):
                continue
            if artifact.get("is_file") is False:
                continue
            artifact_path = str(artifact.get("path") or "").strip()
            if not artifact_path:
                continue
            try:
                resolved = resolve_under_task(
                    task.task_dir, artifact_path, label="delivery primary artifact"
                )
            except ValidationError:
                continue
            if resolved.is_file():
                return str(resolved)
    return None


def _delivery_outputs_from_validation(
    task: ResearchTask,
    validation_result: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    if not validation_result or not validation_result.get("passed"):
        return []
    output_decision = validation_result.get("output_decision") or {}
    primary_output_id = str(output_decision.get("primary_output_id") or "").strip()
    if not primary_output_id:
        return []

    outputs: list[dict[str, Any]] = []
    for finding in validation_result.get("findings") or []:
        if finding.get("check") != "candidate_artifact_inspection":
            continue
        if finding.get("mode") != "output_contract":
            continue
        for artifact in finding.get("artifacts") or []:
            if artifact.get("reasons"):
                continue
            if not artifact.get("exists") or not artifact.get("inside_task"):
                continue
            if artifact.get("is_file") is False:
                continue
            artifact_id = str(artifact.get("id") or "").strip()
            artifact_path = str(artifact.get("path") or "").strip()
            if not artifact_id or not artifact_path:
                continue
            try:
                resolved = resolve_under_task(
                    task.task_dir, artifact_path, label="delivery output artifact"
                )
            except ValidationError:
                continue
            if not resolved.is_file():
                continue
            output = {
                "id": artifact_id,
                "path": str(resolved),
                "role": str(artifact.get("role") or "").strip()
                or (
                    "primary_deliverable"
                    if artifact_id == primary_output_id
                    else "supporting_deliverable"
                ),
            }
            for key in ("media_type", "source_for", "derived_from"):
                value = str(artifact.get(key) or "").strip()
                if value:
                    output[key] = value
            outputs.append(output)
    return outputs


def _delivery_intent_id(
    *,
    task_id: str,
    run_id: str,
    transition: str,
    target: dict[str, Any],
) -> str:
    raw = "|".join(
        [
            task_id,
            run_id,
            transition,
            str(target.get("channel") or ""),
            str(target.get("chat_id") or ""),
            str(target.get("thread_id") or ""),
            str(target.get("topic_id") or ""),
        ]
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


def _upsert_delivery_intent(
    state: dict[str, Any],
    *,
    run_id: str,
    transition: str,
    update_text: str | None,
    primary_file: str | None,
    attachments: list[Any] | None = None,
) -> dict[str, Any]:
    now = utc_now()
    owner = state.get("owner") or {}
    target = {
        "channel": owner.get("channel"),
        "chat_id": owner.get("chat_id"),
        "thread_id": owner.get("thread_id"),
        "topic_id": owner.get("topic_id"),
    }
    missing_owner = not target.get("channel") or not target.get("chat_id")
    intent_id = _delivery_intent_id(
        task_id=str(state.get("id") or ""),
        run_id=run_id,
        transition=transition,
        target=target,
    )
    status = "blocked" if missing_owner else "pending"
    blocked_reason = "notification_blocked:missing_owner" if missing_owner else None
    intent = {
        "id": intent_id,
        "status": status,
        "run_id": run_id,
        "transition": transition,
        "created_at": now,
        "updated_at": now,
        "notification_target": target,
        "update_text": update_text,
        "primary_file": primary_file,
        "attachments": attachments or [],
        "blocked_reason": blocked_reason,
        "error": None,
    }
    intents = state.setdefault("delivery_intents", [])
    for existing in intents:
        if existing.get("id") == intent_id:
            existing_status = existing.get("status") or status
            existing.update(
                {
                    **intent,
                    "status": existing_status,
                    "created_at": existing.get("created_at") or now,
                    "sent_at": existing.get("sent_at"),
                    "error": existing.get("error"),
                }
            )
            intent = existing
            break
    else:
        intents.append(intent)
    state.setdefault("delivery", {})["notification_blocked"] = blocked_reason
    return dict(intent)


def begin_iteration(args: argparse.Namespace) -> int:
    task = ResearchTask.from_args(
        Path(args.root).expanduser().resolve(), research_id=args.id, path=args.path
    )
    initial_state = task.read_state()
    initial_lock = initial_state.get("lock") or {}
    pending_result: Path | None = None
    try:
        pending_result = _pending_result_path(task, initial_lock)
    except ValidationError:
        pending_result = None
    if (
        initial_state.get("status") == "running"
        and stale_lock(initial_state)
        and pending_result is not None
        and pending_result.exists()
    ):
        recovery = recover_pending_result(task, apply_pending_result=True)
        json_dump(recovery)
        return 0

    manager = StateManager(task)
    recovery_result = None
    with manager.editor() as state:
        now = utc_now()
        status = state.get("status")

        if state.get("control", {}).get("stop_requested") and status != "running":
            state["status"] = "cancelled"
            state["updated_at"] = now
            state["history"]["last_transition"] = "cancelled-before-begin"
            normalized_reason = set_history_reason(state, "stopped:user")
            json_dump(
                {
                    "status": "cancelled",
                    "reason": "stop_requested",
                    "normalized_reason": normalized_reason,
                }
            )
            return 0

        if state.get("control", {}).get("stop_requested") and status == "running":
            lock = state.get("lock") or {}
            if lock.get("status") == "held" and stale_lock(state):
                stale_run_id = lock.get("run_id")
                stale_iteration_index = int(lock.get("iteration_index") or 0)
                state["status"] = "cancelled"
                state["control"]["stop_requested"] = False
                state["updated_at"] = now
                state["lock"].update(
                    {
                        "status": "free",
                        "run_id": None,
                        "lease_token": NO_ACTIVE_LEASE,
                        "started_at": None,
                        "iteration_index": None,
                    }
                )
                state.setdefault("artifacts", {})["abandoned_run_id"] = stale_run_id
                state.setdefault("artifacts", {})["abandoned_at"] = now
                state.setdefault("history", {}).setdefault("audit_trail", []).append(
                    {
                        "at": now,
                        "event": "run_abandoned_on_stop",
                        "run_id": stale_run_id,
                        "iteration": stale_iteration_index,
                        "reason": "stale_lock_on_stop",
                    }
                )
                state["history"]["last_transition"] = "cancelled:stale-lock"
                normalized_reason = set_history_reason(state, "stopped:stale_lock")
                json_dump(
                    {
                        "status": "cancelled",
                        "reason": "stop_requested_with_stale_lock",
                        "normalized_reason": normalized_reason,
                        "abandoned_run_id": stale_run_id,
                    }
                )
                return 0
            state["status"] = "cancelled"
            state["control"]["stop_requested"] = False
            state["updated_at"] = now
            state["lock"].update(
                {
                    "status": "free",
                    "run_id": None,
                    "lease_token": NO_ACTIVE_LEASE,
                    "started_at": None,
                    "iteration_index": None,
                }
            )
            state["history"]["last_transition"] = "cancelled:user"
            normalized_reason = set_history_reason(state, "stopped:user")
            json_dump(
                {
                    "status": "cancelled",
                    "reason": "stop_requested",
                    "normalized_reason": normalized_reason,
                }
            )
            return 0

        if status == "paused":
            json_dump(
                {
                    "status": "paused",
                    "normalized_reason": reason_for_begin_short_circuit(
                        status="paused"
                    ),
                }
            )
            return 0

        if status in REVIEW_WAIT_STATUSES:
            review = state.get("review") or {}
            json_dump(
                {
                    "status": status,
                    "review_gated": True,
                    "wait_semantic": "awaiting_user_review",
                    "review_status": review.get("status") or "pending",
                    "revision_count": int(review.get("revision_count") or 0),
                    "last_feedback": review.get("last_feedback"),
                    "normalized_reason": reason_for_begin_short_circuit(status=status),
                }
            )
            return 0

        if status in FINAL_STATUSES:
            json_dump(
                {
                    "status": status,
                    "normalized_reason": reason_for_begin_short_circuit(
                        status=status,
                        last_terminal_reason=(state.get("history") or {}).get(
                            "last_terminal_reason"
                        ),
                    ),
                }
            )
            return 0

        if status == "running":
            if not stale_lock(state):
                age_min = minutes_since(state["lock"].get("started_at"))
                json_dump(
                    {
                        "status": "skipped",
                        "reason": "lock-active",
                        "normalized_reason": "deferred:lock-active",
                        "active_run_id": state["lock"].get("run_id"),
                        "age_min": None if age_min is None else round(age_min, 2),
                    }
                )
                return 0
            stale_run_id = state["lock"].get("run_id")
            stale_iteration_index = int(state["lock"].get("iteration_index") or 0)
            stale_phase = state.get("phase") or "search"
            recovery_result = None
            state["lock"]["recovered_count"] = (
                int(state["lock"].get("recovered_count") or 0) + 1
            )
            state["lock"]["last_recovered_from_run"] = stale_run_id

            recovery_result = task.salvage_partial_progress(
                stale_run_id=stale_run_id,
                stale_iteration_index=stale_iteration_index,
                stale_phase=stale_phase,
            )
            if recovery_result:
                state.setdefault("artifacts", {})["last_recovery_note_path"] = (
                    recovery_result.get("recovery_note_path")
                )
                state.setdefault("artifacts", {})["last_recovery_run_id"] = (
                    recovery_result.get("stale_run_id")
                )
                state.setdefault("artifacts", {})["last_recovery_result_file"] = (
                    recovery_result.get("result_file")
                )
                state.setdefault("artifacts", {})["last_recovery_at"] = (
                    recovery_result.get("recovered_at")
                )
                state.setdefault("history", {}).setdefault("audit_trail", []).append(
                    {
                        "at": now,
                        "event": "recovery_note_created",
                        "run_id": stale_run_id,
                        "iteration": stale_iteration_index,
                        "note_path": recovery_result.get("recovery_note_path"),
                    }
                )
            else:
                state.setdefault("artifacts", {})["last_recovery_note_path"] = None
                state.setdefault("artifacts", {})["abandoned_run_id"] = stale_run_id
                state.setdefault("artifacts", {})["abandoned_at"] = now
                state.setdefault("history", {}).setdefault("audit_trail", []).append(
                    {
                        "at": now,
                        "event": "run_abandoned",
                        "run_id": stale_run_id,
                        "iteration": stale_iteration_index,
                        "reason": "no_result_file",
                    }
                )

        run_id = uuid.uuid4().hex[:12]
        lease_token = uuid.uuid4().hex
        stale_timeout_min = int(state["lock"].get("stale_timeout_min") or 30)
        worker_timeout_seconds = scheduled_worker_timeout_seconds(state)
        queue_result = acquire_global_queue(
            task.task_dir.parent,
            task_id=state["id"],
            task_path=task.task_dir,
            run_id=run_id,
            lease_token=lease_token,
            stale_timeout_min=stale_timeout_min,
            policy=getattr(args, "queue_policy", "global_iteration_lock"),
        )
        if not queue_result.get("acquired"):
            queue = state.setdefault("queue", {})
            queue["status"] = "waiting"
            queue["waiting_since"] = queue.get("waiting_since") or now
            queue["position"] = queue_result.get("position")
            queue["blocked_by_task_id"] = queue_result.get("active_task_id")
            queue["blocked_by_run_id"] = queue_result.get("active_run_id")
            queue["active_task_id"] = queue_result.get("active_task_id")
            queue["active_run_id"] = queue_result.get("active_run_id")
            state["updated_at"] = now
            state["history"]["last_transition"] = "begin:queued"
            set_history_reason(state, queue_result.get("normalized_reason"))
            json_dump(
                {
                    "status": "skipped",
                    "reason": queue_result.get("reason"),
                    "normalized_reason": queue_result.get("normalized_reason"),
                    "active_task_id": queue_result.get("active_task_id"),
                    "active_run_id": queue_result.get("active_run_id"),
                    "queue_position": queue_result.get("position"),
                }
            )
            return 0
        preflight = state.get("preflight")
        if isinstance(preflight, dict) and not bool(preflight.get("done")):
            target_phase = str(
                preflight.get("target_phase") or state.get("phase") or "search"
            )
            if target_phase == "preflight":
                target_phase = "search"
            preflight["target_phase"] = target_phase
            preflight["iteration_index"] = int(preflight.get("iteration_index") or 0) + 1
            preflight["iteration_limit"] = int(preflight.get("iteration_limit") or 1)
            state["phase"] = "preflight"
        iteration_index = int(state["progress"].get("iteration_count") or 0) + 1
        state["status"] = "running"
        state["updated_at"] = now
        state["progress"]["last_attempt_at"] = now
        state["lock"].update(
            {
                "status": "held",
                "run_id": run_id,
                "lease_token": lease_token,
                "started_at": now,
                "iteration_index": iteration_index,
                "worker_timeout_seconds": worker_timeout_seconds,
            }
        )
        state["history"]["last_transition"] = "begin"
        state.setdefault("queue", {}).update(
            {
                "status": "running"
                if queue_result.get("status") != "disabled"
                else "disabled",
                "waiting_since": None,
                "position": None,
                "blocked_by_task_id": None,
                "blocked_by_run_id": None,
                "active_task_id": state["id"],
                "active_run_id": run_id,
                "last_acquired_at": now,
            }
        )
        work_order = make_work_order(state, task)
        if recovery_result:
            work_order["recovery_note"] = {
                "path": recovery_result.get("recovery_note_path"),
                "exists": recovery_result.get("recovery_note_exists"),
                "run_id": recovery_result.get("stale_run_id"),
                "iteration": recovery_result.get("stale_iteration_index"),
            }

    json_dump(work_order)
    return 0


def load_result_payload(path: Path) -> dict[str, Any]:
    payload = read_json(path)
    if not isinstance(payload, dict):
        raise ValidationError("result payload must be a JSON object")
    summary = str(payload.get("summary") or "").strip()
    if not summary:
        raise ValidationError("result payload requires non-empty 'summary'")
    phase = str(payload.get("phase") or "search")
    if phase not in PHASES:
        raise ValidationError(f"Unsupported phase: {phase}")
    notify = str(payload.get("notify_recommendation") or "auto")
    if notify not in {"auto", "silent", "milestone", "blocker", "final"}:
        raise ValidationError(f"Unsupported notify_recommendation: {notify}")
    adequacy = normalize_adequacy_review(payload.get("adequacy"))
    if phase == "verify" and adequacy is None:
        raise ValidationError("verify phase result requires 'adequacy'")
    return {
        "summary": summary,
        "next_angle": str(payload.get("next_angle") or "").strip() or None,
        "meaningful_progress": bool(payload.get("meaningful_progress", True)),
        "code_used": bool(payload.get("code_used", False)),
        "phase": phase,
        "open_questions": normalize_string_list(payload.get("open_questions") or []),
        "sources": normalize_sources(payload.get("sources") or []),
        "findings": normalize_findings(payload.get("findings") or []),
        "analysis_artifacts": normalize_analysis_artifacts(
            payload.get("analysis_artifacts") or []
        ),
        "packages_used": normalize_string_list(payload.get("packages_used") or []),
        "database_used": bool(payload.get("database_used", False)),
        "database_artifacts": normalize_database_artifacts(
            payload.get("database_artifacts") or []
        ),
        "database_summary": normalize_database_summary(payload.get("database_summary")),
        "vision_used": bool(payload.get("vision_used", False)),
        "vision_artifacts": normalize_vision_artifacts(
            payload.get("vision_artifacts") or []
        ),
        "vision_summary": normalize_vision_summary(payload.get("vision_summary")),
        "_preflight_explicit": "preflight" in payload,
        "preflight": _normalize_preflight_payload(payload.get("preflight")),
        "notify_recommendation": notify,
        "should_complete": bool(payload.get("should_complete", False)),
        "final_report_markdown": payload.get("final_report_markdown"),
        "adequacy": adequacy,
        "finalization": normalize_finalization_trace(payload.get("finalization")),
    }


def _finish_preflight_iteration_impl(
    task: ResearchTask,
    args: argparse.Namespace,
    payload: dict[str, Any],
    *,
    emit: bool = True,
) -> tuple[int, dict[str, Any]]:
    manager = StateManager(task)
    lease_token: str | None = None
    now = ""
    iteration_index = 0
    with manager.editor() as state:
        lock = state.get("lock") or {}
        if state.get("status") != "running" or lock.get("status") != "held":
            raise ValidationError("No active run to finish")
        if lock.get("run_id") != args.run_id:
            raise ValidationError(
                f"Active run id mismatch: expected {lock.get('run_id')}, got {args.run_id}"
            )
        if state.get("phase") != "preflight":
            raise ValidationError(
                "preflight phase result can only finish an active preflight lease"
            )
        lease_token = lock.get("lease_token")
        now = utc_now()
        iteration_index = int(lock.get("iteration_index") or 0)
        preflight = state.setdefault("preflight", {})
        result_preflight = payload["preflight"]
        decision = result_preflight["decision"]
        target_phase = str(preflight.get("target_phase") or "search")
        if target_phase == "preflight":
            target_phase = "search"
        artifact_rel = str(
            preflight.get("artifact_markdown")
            or "workspace/preflight/research-preflight.md"
        )
        artifact_path = task.task_dir / artifact_rel
        ensure_dir(artifact_path.parent)
        atomic_text_write(
            artifact_path,
            _render_preflight_markdown(payload, result_preflight),
        )
        preflight.update(
            {
                "done": True,
                "decision": decision,
                "iteration_index": int(preflight.get("iteration_index") or 1),
                "iteration_limit": int(preflight.get("iteration_limit") or 1),
                "artifact_markdown": artifact_rel,
                "blockers": result_preflight.get("blockers") or [],
                "warnings": result_preflight.get("warnings") or [],
                "completed_at": now,
                "target_phase": target_phase,
            }
        )
        state["phase"] = target_phase
        state["status"] = "paused" if decision in {"needs_setup", "blocked"} else "idle"
        state["updated_at"] = now
        state["working_memory"]["summary"] = payload["summary"]
        state["lock"].update(
            {
                "status": "free",
                "run_id": None,
                "lease_token": NO_ACTIVE_LEASE,
                "started_at": None,
                "iteration_index": None,
            }
        )
        state.setdefault("queue", {}).update(
            {
                "status": "free",
                "active_task_id": None,
                "active_run_id": None,
                "last_released_at": now,
            }
        )
        if state["status"] == "paused":
            suspend_bound_job(state, reason=f"preflight:{decision}", at=now)
        normalized_reason = set_history_reason(state, f"preflight:{decision}")
        state["history"]["last_transition"] = f"preflight:{decision}"
        state.setdefault("transactions", {})["finish"] = {
            "status": "committed",
            "run_id": args.run_id,
            "iteration": iteration_index,
            "committed_at": now,
            "outcome": state["status"],
            "normalized_reason": normalized_reason,
        }
        append_run_log(
            task,
            timestamp=now,
            iteration=iteration_index,
            run_id=args.run_id,
            phase="preflight",
            outcome=state["status"],
            normalized_reason=normalized_reason,
            meaningful_progress=False,
            new_sources_count=0,
            new_findings_count=0,
            duplicate_sources_count=0,
            duplicate_findings_count=0,
            low_yield_streak=0,
            topic_saturated=False,
            short_summary=payload["summary"],
        )
        result = {
            "status": state["status"],
            "normalized_reason": normalized_reason,
            "notify_user": False,
            "update_text": None,
            "summary": payload["summary"],
            "preflight": dict(preflight),
            "iteration_count": state["progress"]["iteration_count"],
            "queue_release": None,
        }

    queue_release = release_global_queue(
        task.task_dir.parent,
        task_id=state["id"],
        run_id=args.run_id,
        lease_token=lease_token,
        released_by="finish",
    )
    result["queue_release"] = queue_release
    refresh_task_playbook(task)
    if emit:
        json_dump(result)
    return 0, result


def _finish_iteration_impl(
    args: argparse.Namespace, *, emit: bool = True
) -> tuple[int, dict[str, Any]]:
    task = ResearchTask.from_args(
        Path(args.root).expanduser().resolve(), research_id=args.id, path=args.path
    )
    payload = load_result_payload(Path(args.result_file).expanduser().resolve())
    if payload["phase"] == "preflight":
        if payload.get("_preflight_explicit"):
            return _finish_preflight_iteration_impl(task, args, payload, emit=emit)
        raise ValidationError("preflight phase result requires explicit 'preflight' object")
    manager = StateManager(task)
    remove_job_id: str | None = None
    queue_release: dict[str, Any] | None = None
    lease_token: str | None = None
    update_text: str | None = None
    delivery_intent: dict[str, Any] | None = None
    completion_validation: dict[str, Any] | None = None
    budget_phase_info: dict[str, Any] = {}
    saturation: dict[str, Any] = {}
    total_sources: int = 0
    reached_max_runtime: bool = False
    total_runtime_min: float | None = None
    next_status: str = "idle"
    pre_edit_revision_snap = task.read_state().get("revision_snapshot") or {}
    normalized_reason: str | None = None
    notify_user: bool = False
    update_text: str | None = None
    delivery_intent: dict[str, Any] | None = None
    append_metrics: dict[str, int] = {}
    saved_report_path: str | None = None
    finalization_validation: dict[str, Any] | None = None
    now: str = ""
    iteration_index: int = 0

    with manager.editor() as state:
        lock = state.get("lock") or {}
        if state.get("status") != "running" or lock.get("status") != "held":
            raise ValidationError("No active run to finish")
        if lock.get("run_id") != args.run_id:
            raise ValidationError(
                f"Active run id mismatch: expected {lock.get('run_id')}, got {args.run_id}"
            )
        lease_token = lock.get("lease_token")

        now = utc_now()
        iteration_index = int(
            lock.get("iteration_index")
            or (int(state["progress"].get("iteration_count") or 0) + 1)
        )
        phase = payload["phase"]
        state.setdefault("transactions", {})["finish"] = {
            "status": "started",
            "run_id": args.run_id,
            "iteration": iteration_index,
            "started_at": now,
        }

        active_phase = str(state.get("phase") or "")
        if active_phase == "preflight" and phase != "preflight":
            raise ValidationError(
                "preflight lease requires a preflight phase result with explicit preflight object"
            )

        append_metrics = task.finish_iteration(args.run_id, payload)

        progress = state["progress"]
        progress["iteration_count"] = int(progress.get("iteration_count") or 0) + 1
        progress["last_iteration_at"] = now
        if payload["meaningful_progress"]:
            progress["meaningful_iterations"] = (
                int(progress.get("meaningful_iterations") or 0) + 1
            )
            progress["last_meaningful_progress_at"] = now
        state["updated_at"] = now
        state.setdefault("adequacy", adequacy_defaults())
        state.setdefault("finalization", finalization_defaults())
        state["phase"] = phase
        state["working_memory"]["summary"] = payload["summary"]
        if payload["next_angle"]:
            state["working_memory"]["next_angle"] = payload["next_angle"]
        if payload["open_questions"]:
            state["working_memory"]["open_questions"] = payload["open_questions"]
        state["errors"]["consecutive_failures"] = 0
        state["errors"]["last_error"] = None

        analysis = state.setdefault("analysis", {})
        code_used = bool(
            payload.get("code_used")
            or payload.get("analysis_artifacts")
            or payload.get("packages_used")
            or payload.get("database_used")
            or payload.get("database_artifacts")
        )
        analysis["last_iteration_code_used"] = code_used
        analysis["code_used_recently"] = bool(
            analysis.get("code_used_recently") or code_used
        )
        if code_used:
            analysis["last_code_run_at"] = now
            analysis["last_packages_used"] = payload.get("packages_used") or []
            analysis["last_analysis_artifacts"] = (
                payload.get("analysis_artifacts") or []
            )
            analysis["analysis_artifacts_count"] = len(
                payload.get("analysis_artifacts") or []
            )
        database_used = bool(
            payload.get("database_used")
            or payload.get("database_artifacts")
            or payload.get("database_summary")
        )
        analysis["last_iteration_database_used"] = database_used
        analysis["database_used_recently"] = bool(
            analysis.get("database_used_recently") or database_used
        )
        if database_used:
            analysis["last_database_run_at"] = now
            analysis["last_database_artifacts"] = (
                payload.get("database_artifacts") or []
            )
            analysis["last_database_summary"] = payload.get("database_summary")
        vision_used = bool(
            payload.get("vision_used")
            or payload.get("vision_artifacts")
            or payload.get("vision_summary")
        )
        analysis["last_iteration_vision_used"] = vision_used
        analysis["vision_used_recently"] = bool(
            analysis.get("vision_used_recently") or vision_used
        )
        if vision_used:
            analysis["last_vision_run_at"] = now
            analysis["last_vision_artifacts"] = payload.get("vision_artifacts") or []
            analysis["last_vision_summary"] = payload.get("vision_summary")

        saturation = state.setdefault("saturation", {})
        saturation["low_yield_threshold"] = int(
            saturation.get("low_yield_threshold") or 2
        )
        saturation["last_iteration_new_sources"] = append_metrics["new_sources"]
        saturation["last_iteration_new_findings"] = append_metrics["new_findings"]
        saturation["last_iteration_duplicate_sources"] = append_metrics[
            "duplicate_sources"
        ]
        saturation["last_iteration_duplicate_findings"] = append_metrics[
            "duplicate_findings"
        ]
        if compute_low_yield(append_metrics, payload):
            saturation["consecutive_low_yield"] = (
                int(saturation.get("consecutive_low_yield") or 0) + 1
            )
            saturation["last_low_yield_at"] = now
        else:
            saturation["consecutive_low_yield"] = 0
        saturation["topic_saturated"] = int(
            saturation.get("consecutive_low_yield") or 0
        ) >= int(saturation["low_yield_threshold"])

        max_iterations = int(state["budget"].get("max_iterations") or 0)
        reached_budget = (
            max_iterations > 0 and int(progress["iteration_count"]) >= max_iterations
        )
        max_sources = int(state["budget"].get("max_sources") or 0)
        existing_sources_count = (
            len(
                [
                    line
                    for line in task.sources_path.read_text(
                        encoding="utf-8"
                    ).splitlines()
                    if line.strip()
                ]
            )
            - append_metrics["new_sources"]
        )
        total_sources = existing_sources_count + append_metrics["new_sources"]
        reached_max_sources = max_sources > 0 and total_sources >= max_sources
        max_runtime_min = float(state["budget"].get("max_runtime_min") or 0)
        created_at = state.get("created_at")
        total_runtime_min = (
            minutes_since(created_at, now=parse_ts(now)) if created_at else None
        )
        reached_max_runtime = (
            max_runtime_min > 0
            and total_runtime_min is not None
            and total_runtime_min >= max_runtime_min
        )
        topic_saturated = (
            bool(saturation.get("topic_saturated")) and phase == "synthesize"
        )
        stop_requested = bool(state.get("control", {}).get("stop_requested"))
        pause_requested = bool(state.get("control", {}).get("pause_requested"))
        completion_triggered = None
        next_status = "idle"
        if stop_requested:
            next_status = "cancelled"
        elif payload["should_complete"]:
            next_status = "complete"
            completion_triggered = "worker"
        elif reached_budget:
            next_status = "complete"
            completion_triggered = "budget"
        elif reached_max_runtime:
            next_status = "complete"
            completion_triggered = "budget"
        elif reached_max_sources:
            next_status = "complete"
            completion_triggered = "budget"
        elif topic_saturated:
            next_status = "complete"
            completion_triggered = "topic_saturated"
        elif pause_requested:
            next_status = "paused"

        is_worker_initiated_final = completion_triggered == "worker" and payload.get(
            "should_complete"
        )
        adequacy_state = state.setdefault("adequacy", adequacy_defaults())
        if phase == "verify" and not stop_requested and not pause_requested:
            payload_adequacy = payload.get("adequacy")
            if not payload_adequacy:
                raise ValidationError("verify phase result requires 'adequacy'")

            max_attempts = int(adequacy_state.get("max_attempts") or 2)
            attempt_count = int(adequacy_state.get("attempt_count") or 0) + 1
            adequacy_state.update(payload_adequacy)
            adequacy_state["max_attempts"] = max_attempts
            adequacy_state["attempt_count"] = attempt_count
            adequacy_state["last_checked_at"] = now
            adequacy_state["last_checked_by"] = args.run_id

            status = str(adequacy_state.get("status") or "not_started")
            if status != "passed" and attempt_count >= max_attempts:
                status = "needs_intervention"
                adequacy_state["status"] = status

            routed_phase = route_phase_for_adequacy_status(status) or "verify"
            state["phase"] = routed_phase
            adequacy_state["recommended_next_phase"] = routed_phase
            next_status = "idle"
            completion_triggered = None
            clear_reviewable_candidate(state)

            if adequacy_state.get("recommended_next_angle"):
                state["working_memory"]["next_angle"] = adequacy_state[
                    "recommended_next_angle"
                ]
            adequacy_reasons = collect_adequacy_reasons(adequacy_state)
            if adequacy_reasons:
                current_questions = state["working_memory"].get("open_questions") or []
                merged_questions = list(dict.fromkeys([*current_questions, *adequacy_reasons]))
                state["working_memory"]["open_questions"] = merged_questions
            adequacy_state["operator_next_action"] = build_adequacy_operator_next_action(
                state,
                adequacy_state,
            )

        if next_status == "complete" and adequacy_state.get("status") != "passed":
            adequacy_state["status"] = "running"
            adequacy_state["last_checked_at"] = None
            adequacy_state["operator_next_action"] = None
            state["phase"] = "verify"
            adequacy_state["recommended_next_phase"] = "verify"
            clear_reviewable_candidate(state)
            next_status = "idle"

        if next_status == "complete":
            report = payload.get("final_report_markdown")
            if report is None or not str(report).strip():
                report = render_default_final_report(
                    task, state, payload, iteration_index
                )
            completion_validation = validate_completion(
                task,
                state,
                payload,
                phase=phase,
                report_markdown=str(report),
                triggered_by=str(completion_triggered or "unknown"),
            )
            state.setdefault("completion", {})["last_validation"] = {
                **completion_validation,
                "validated_at": now,
                "candidate_status": "complete",
            }
            if completion_validation["passed"]:
                _clear_completion_validation_retry_counter(state, at=now)
                if is_worker_initiated_final:
                    finalization_validation = _run_v13_finalization_validation(
                        task, state, payload, report_markdown=str(report)
                    )
                    finalization_state = state.setdefault(
                        "finalization", finalization_defaults()
                    )
                    payload_finalization = payload.get("finalization") or {}
                    for key in (
                        "inferred_user_need",
                        "intended_recipient",
                        "primary_deliverable_kind",
                        "internal_artifacts",
                        "candidate_artifacts",
                        "deliverable_decision",
                        "output_decision",
                        "blocking_defects",
                        "nonblocking_defects",
                        "revisions",
                        "validation_evidence",
                    ):
                        if key in payload_finalization:
                            finalization_state[key] = payload_finalization[key]
                    if finalization_validation.get("deliverable_decision"):
                        finalization_state["deliverable_decision"] = (
                            finalization_validation["deliverable_decision"]
                        )
                    if finalization_validation.get("output_decision"):
                        finalization_state["output_decision"] = (
                            finalization_validation["output_decision"]
                        )
                    finalization_state["last_validation_findings"] = (
                        finalization_validation.get("findings") or []
                    )
                    finalization_state["last_validated_at"] = now
                    finalization_state["attempt_count"] = (
                        int(finalization_state.get("attempt_count") or 0) + 1
                    )

                    if finalization_validation.get("passed"):
                        package_delivery = _package_delivery_from_validation(
                            finalization_validation
                        )
                        if package_delivery:
                            saved_report_path = None
                            state["artifacts"]["final_report_path"] = None
                            state["delivery"]["package_path"] = package_delivery[
                                "package_path"
                            ]
                            state["delivery"]["primary_file"] = package_delivery[
                                "primary_file"
                            ]
                            state["delivery"]["attachments"] = package_delivery[
                                "attachments"
                            ]
                        else:
                            atomic_text_write(
                                task.final_report_path,
                                str(report).rstrip() + "\n",
                            )
                            saved_report_path = str(task.final_report_path)
                            state["artifacts"]["final_report_path"] = saved_report_path
                            delivery_outputs = _delivery_outputs_from_validation(
                                task, finalization_validation
                            )
                            if delivery_outputs:
                                state["delivery"]["outputs"] = delivery_outputs
                                primary_output = next(
                                    (
                                        item
                                        for item in delivery_outputs
                                        if item.get("role")
                                        == "primary_deliverable"
                                    ),
                                    delivery_outputs[0],
                                )
                                state["delivery"]["primary_file"] = primary_output[
                                    "path"
                                ]
                                state["delivery"]["attachments"] = [
                                    str(item.get("path") or "")
                                    for item in delivery_outputs
                                    if item is not primary_output
                                ]
                            else:
                                primary_file = _primary_file_from_validation(
                                    task, finalization_validation
                                )
                                state["delivery"]["primary_file"] = (
                                    primary_file or saved_report_path
                                )
                        finalization_state["status"] = "passed"
                        state["delivery"]["review_ready"] = True
                        state["delivery"]["ready"] = False
                        next_status = "awaiting_review"
                        state["status"] = "awaiting_review"
                        revision_diff = build_revision_diff(
                            pre_edit_revision_snap, state
                        )
                        state["revision_diff"] = revision_diff
                        revision_snap = {
                            "final_report_path": saved_report_path,
                            "package_path": state["delivery"].get("package_path"),
                            "revision_count": int(
                                state.get("review", {}).get("revision_count") or 0
                            ),
                        }
                        state["revision_snapshot"] = revision_snap
                        review = state.setdefault("review", {})
                        review["review_gated"] = True
                        if review.get("status") == "changes_requested":
                            review["status"] = "pending"
                    else:
                        finalization_status = finalization_validation.get("status")
                        if finalization_status == "needs_intervention":
                            next_status = "idle"
                            state["status"] = "idle"
                            finalization_state["status"] = "needs_intervention"
                        else:
                            next_status = "finalize"
                            state["status"] = "finalize"
                            finalization_state["status"] = "rework"
                        clear_reviewable_candidate(state)
                        saved_report_path = None
                else:
                    atomic_text_write(task.final_report_path, str(report).rstrip() + "\n")
                    saved_report_path = str(task.final_report_path)
                    state["artifacts"]["final_report_path"] = saved_report_path
                    state.setdefault("finalization", finalization_defaults())["status"] = "passed"
                    state["delivery"]["primary_file"] = saved_report_path
                    state["delivery"]["review_ready"] = True
                    state["delivery"]["ready"] = False
                    next_status = "awaiting_review"
                    state["status"] = "awaiting_review"
                    review = state.setdefault("review", {})
                    review["review_gated"] = True
                    if review.get("status") == "changes_requested":
                        review["status"] = "pending"
            else:
                _record_completion_validation_rejection(
                    state,
                    run_id=args.run_id,
                    phase=phase,
                    completion_validation=completion_validation,
                    at=now,
                )
                next_status = "idle"
                clear_reviewable_candidate(state)

        normalized_reason = set_history_reason(
            state,
            reason_for_finish(
                next_status=next_status,
                completion_triggered=completion_triggered,
                completion_validation_passed=(
                    None
                    if completion_validation is None
                    else bool(completion_validation.get("passed"))
                ),
                stop_requested=stop_requested,
                pause_requested=pause_requested,
            ),
        )
        state["status"] = next_status

        if next_status in FINAL_STATUSES:
            remove_job_id = state.get("job", {}).get("job_id")
        elif next_status in REVIEW_WAIT_STATUSES:
            job = state.get("job") or {}
            if job.get("job_id"):
                suspend_bound_job(state, reason="awaiting_review", at=now)
                history = state.setdefault("history", {})
                history["last_job_binding"] = snapshot_job_binding(state)

        state["lock"].update(
            {
                "status": "free",
                "run_id": None,
                "lease_token": NO_ACTIVE_LEASE,
                "started_at": None,
                "iteration_index": None,
            }
        )
        state.setdefault("queue", {}).update(
            {
                "status": "free",
                "active_task_id": None,
                "active_run_id": None,
                "last_released_at": now,
            }
        )
        if next_status == "paused":
            state["control"]["pause_requested"] = False
            suspend_bound_job(state, reason="paused", at=now)
        if next_status in {"complete", "cancelled"}:
            state["control"]["stop_requested"] = False
        if next_status == "complete":
            job = state.get("job") or {}
            if job.get("job_id"):
                history = state.setdefault("history", {})
                history["last_job_binding"] = snapshot_job_binding(state)
        state["history"]["last_transition"] = f"finish:{next_status}"
        state.setdefault("transactions", {})["finish"] = {
            "status": "committed",
            "run_id": args.run_id,
            "iteration": iteration_index,
            "committed_at": now,
            "outcome": next_status,
            "normalized_reason": normalized_reason,
        }

        notify_user = should_notify(state, payload, next_status)
        if notify_user:
            update_text = compose_finish_update_text(
                state,
                payload,
                next_status,
                iteration_count=state["progress"]["iteration_count"],
                final_report_path=saved_report_path,
            )
            delivery_intent = _upsert_delivery_intent(
                state,
                run_id=args.run_id,
                transition=f"finish:{next_status}",
                update_text=update_text,
                primary_file=state.get("delivery", {}).get("primary_file"),
                attachments=state.get("delivery", {}).get("attachments") or [],
            )

        append_run_log(
            task,
            timestamp=now,
            iteration=iteration_index,
            run_id=args.run_id,
            phase=phase,
            outcome=next_status,
            normalized_reason=normalized_reason,
            meaningful_progress=payload["meaningful_progress"],
            new_sources_count=append_metrics["new_sources"],
            new_findings_count=append_metrics["new_findings"],
            duplicate_sources_count=append_metrics["duplicate_sources"],
            duplicate_findings_count=append_metrics["duplicate_findings"],
            low_yield_streak=int(saturation.get("consecutive_low_yield") or 0),
            topic_saturated=bool(saturation.get("topic_saturated")),
            short_summary=payload["summary"],
        )

    queue_release = release_global_queue(
        task.task_dir.parent,
        task_id=state["id"],
        run_id=args.run_id,
        lease_token=lease_token,
        released_by="finish",
    )

    budget_phase_info = compute_budget_phase(
        budget=state["budget"],
        progress=progress,
        total_sources=total_sources,
        total_runtime_min=total_runtime_min,
    )

    removal_payload = None
    if remove_job_id:
        removal_payload = remove_cron_job(remove_job_id)
        clear_bound_job(
            task, removed_job_id=remove_job_id, removal_payload=removal_payload
        )

    refresh_task_playbook(task)
    result = {
        "status": next_status,
        "normalized_reason": normalized_reason,
        "notify_user": notify_user,
        "update_text": update_text,
        "delivery_intent": delivery_intent,
        "owner": state.get("owner"),
        "summary": payload["summary"],
        "next_angle": payload["next_angle"],
        "final_report_path": saved_report_path,
        "iteration_count": state["progress"]["iteration_count"],
        "append_metrics": append_metrics,
        "topic_saturated": state.get("saturation", {}).get("topic_saturated"),
        "consecutive_low_yield": state.get("saturation", {}).get(
            "consecutive_low_yield"
        ),
        "completion_validation": completion_validation,
        "finalization_validation": finalization_validation,
        "removed_job_id": remove_job_id,
        "removal_payload": removal_payload,
        "budget_phase": budget_phase_info.get("phase"),
        "budget_phase_detail": budget_phase_info,
        "total_sources": total_sources,
        "total_runtime_min": budget_phase_info.get("total_runtime_min"),
        "reached_max_runtime": reached_max_runtime,
        "review_gated": next_status in REVIEW_WAIT_STATUSES,
        "queue_release": queue_release,
    }
    if emit:
        json_dump(result)
    return 0, result


def finish_iteration(args: argparse.Namespace) -> int:
    code, _result = _finish_iteration_impl(args, emit=True)
    return code


def _pending_result_path(task: ResearchTask, lock: dict[str, Any]) -> Path:
    return pending_result_path(task.tmp_dir, lock.get("run_id"))


def _consume_pending_result(result_file: Path) -> Path:
    consumed_path = result_file.with_name(f"{result_file.name}.applied")
    if consumed_path.exists():
        consumed_path = result_file.with_name(f"{result_file.name}.{uuid.uuid4().hex[:8]}.applied")
    shutil.move(str(result_file), str(consumed_path))
    return consumed_path


def _append_recovery_log(task: ResearchTask, entry: dict[str, Any]) -> Path:
    recovery_log_path = task.task_dir / "recovery-log.jsonl"
    append_jsonl(recovery_log_path, [entry])
    return recovery_log_path


def _record_invalid_pending_result(
    task: ResearchTask,
    *,
    run_id: str | None,
    result_file: Path,
    error: str,
) -> dict[str, Any] | None:
    queue_release = None
    release_run_id: str | None = None
    release_lease_token: str | None = None
    release_task_id: str | None = None
    now = utc_now()
    recovery_log_path = _append_recovery_log(
        task,
        {
            "at": now,
            "event": "pending_result_invalid",
            "run_id": run_id,
            "result_file": str(result_file),
            "error": error,
        },
    )
    with StateManager(task).editor() as state:
        lock = state.get("lock") or {}
        release_task_id = str(state.get("id") or task.task_dir.name)
        matches_active_lock = (
            state.get("status") == "running"
            and lock.get("status") == "held"
            and lock.get("run_id") == run_id
        )
        artifacts = state.setdefault("artifacts", {})
        artifacts["pending_result_invalid_path"] = str(result_file)
        artifacts["pending_result_invalid_error"] = error
        artifacts["pending_result_invalid_at"] = now
        artifacts["last_recovery_log_path"] = str(recovery_log_path)
        state.setdefault("history", {}).setdefault("audit_trail", []).append(
            {
                "at": now,
                "event": "pending_result_invalid",
                "run_id": run_id,
                "result_file": str(result_file),
                "error": error,
            }
        )
        if matches_active_lock and stale_lock(state):
            release_run_id = str(lock.get("run_id") or "")
            release_lease_token = str(lock.get("lease_token") or "")
            state["status"] = "idle"
            state["lock"].update(
                {
                    "status": "free",
                    "run_id": None,
                    "lease_token": NO_ACTIVE_LEASE,
                    "started_at": None,
                    "iteration_index": None,
                }
            )
            state.setdefault("queue", {}).update(
                {
                    "status": "free",
                    "active_task_id": None,
                    "active_run_id": None,
                    "last_released_at": now,
                }
            )
            artifacts["abandoned_run_id"] = run_id
            artifacts["abandoned_at"] = now
            state["history"]["last_transition"] = "recover:pending_result_invalid"
            set_history_reason(state, "recovery:pending_result_invalid")
        state["updated_at"] = now

    if release_run_id:
        queue_release = release_global_queue(
            task.task_dir.parent,
            task_id=release_task_id or task.task_dir.name,
            run_id=release_run_id,
            lease_token=release_lease_token,
            released_by="recover-invalid",
        )
    refresh_task_playbook(task)
    return queue_release


def recover_pending_result(
    task: ResearchTask, *, apply_pending_result: bool
) -> dict[str, Any]:
    state = task.read_state()
    lock = state.get("lock") or {}
    run_id = str(lock.get("run_id") or "")
    warnings: list[str] = []

    if not apply_pending_result:
        return {
            "status": "blocked",
            "run_id": run_id or None,
            "warnings": ["recover requires --apply-pending-result"],
        }
    if state.get("status") in FINAL_STATUSES or state.get("status") in REVIEW_WAIT_STATUSES:
        return {
            "status": "blocked",
            "run_id": run_id or None,
            "warnings": [f"task status does not allow pending recovery: {state.get('status')}"],
        }
    if state.get("status") != "running" or lock.get("status") != "held" or not run_id:
        return {
            "status": "no_pending_result",
            "run_id": run_id or None,
            "warnings": ["no active run lock"],
        }
    try:
        result_file = _pending_result_path(task, lock)
    except ValidationError as exc:
        return {
            "status": "blocked",
            "run_id": run_id,
            "applied_result_file": None,
            "consumed_result_file": None,
            "finish_status": None,
            "warnings": [str(exc)],
        }
    if not result_file.exists():
        return {
            "status": "no_pending_result",
            "run_id": run_id,
            "applied_result_file": str(result_file),
            "warnings": [],
        }
    if not stale_lock(state):
        return {
            "status": "blocked",
            "run_id": run_id,
            "applied_result_file": str(result_file),
            "warnings": ["active run is not stale"],
        }

    try:
        load_result_payload(result_file)
    except ValidationError as exc:
        warning = str(exc)
        queue_release = _record_invalid_pending_result(
            task,
            run_id=run_id,
            result_file=result_file,
            error=warning,
        )
        return {
            "status": "blocked",
            "run_id": run_id,
            "applied_result_file": str(result_file),
            "consumed_result_file": None,
            "finish_status": None,
            "warnings": [warning],
            "queue_release": queue_release,
        }

    finish_args = argparse.Namespace(
        root=str(task.task_dir.parent),
        id=state.get("id"),
        path=None,
        run_id=run_id,
        result_file=str(result_file),
    )
    _code, finish_result = _finish_iteration_impl(finish_args, emit=False)
    consumed_path = _consume_pending_result(result_file)
    now = utc_now()
    recovery_log_path = _append_recovery_log(
        task,
        {
            "at": now,
            "event": "pending_result_applied",
            "run_id": run_id,
            "result_file": str(result_file),
            "consumed_result_file": str(consumed_path),
            "finish_status": finish_result.get("status"),
        },
    )
    with StateManager(task).editor() as updated_state:
        updated_state.setdefault("artifacts", {})["last_pending_result_file"] = str(
            consumed_path
        )
        updated_state.setdefault("artifacts", {})["last_recovery_log_path"] = str(
            recovery_log_path
        )
        updated_state.setdefault("history", {}).setdefault("audit_trail", []).append(
            {
                "at": now,
                "event": "pending_result_applied",
                "run_id": run_id,
                "result_file": str(result_file),
                "consumed_result_file": str(consumed_path),
                "finish_status": finish_result.get("status"),
            }
        )
        updated_state["updated_at"] = now
    refresh_task_playbook(task)
    return {
        "status": "recovered",
        "run_id": run_id,
        "applied_result_file": str(result_file),
        "consumed_result_file": str(consumed_path),
        "recovery_log_path": str(recovery_log_path),
        "finish_status": finish_result.get("status"),
        "warnings": warnings,
        "finish": finish_result,
    }


def recover_derived_artifacts(task: ResearchTask) -> dict[str, Any]:
    before_exists = task.task_playbook_path.exists()
    refresh_task_playbook(task)
    refreshed_artifacts = [str(task.task_playbook_path)]
    return {
        "status": "refreshed" if not before_exists else "already_current",
        "refreshed_artifacts": refreshed_artifacts,
        "state_mutated": False,
    }


def recover_command(args: argparse.Namespace) -> int:
    task = ResearchTask.from_args(
        Path(args.root).expanduser().resolve(), research_id=args.id, path=args.path
    )
    if bool(getattr(args, "apply_pending_result", False)) and bool(
        getattr(args, "refresh_derived", False)
    ):
        raise ValidationError(
            "recover accepts only one repair action at a time: --apply-pending-result or --refresh-derived"
        )
    if bool(getattr(args, "refresh_derived", False)):
        result = recover_derived_artifacts(task)
        json_dump(result)
        return 0
    result = recover_pending_result(
        task, apply_pending_result=bool(args.apply_pending_result)
    )
    json_dump(result)
    return 0


def record_notification_command(args: argparse.Namespace) -> int:
    task = ResearchTask.from_args(
        Path(args.root).expanduser().resolve(), research_id=args.id, path=args.path
    )
    target_status = str(args.status)
    intent_id = str(args.delivery_intent_id)
    result: dict[str, Any] | None = None
    with StateManager(task).editor() as state:
        now = utc_now()
        intents = state.setdefault("delivery_intents", [])
        intent = next(
            (item for item in intents if item.get("id") == intent_id),
            None,
        )
        if intent is None:
            raise ValidationError(f"Unknown delivery intent: {intent_id}")

        previous_status = str(intent.get("status") or "pending")
        if previous_status == "sent" and target_status == "failed":
            raise ValidationError("Cannot mark a sent delivery intent as failed")

        sent_incremented = False
        if target_status == "sent":
            delivery = state.setdefault("delivery", {})
            if previous_status != "sent":
                delivery["sent_updates"] = int(delivery.get("sent_updates") or 0) + 1
                delivery["last_update_at"] = now
                sent_incremented = True
            delivery["notification_blocked"] = None
            intent["status"] = "sent"
            intent["sent_at"] = intent.get("sent_at") or now
            intent["error"] = None
            intent["error_code"] = None
            intent["provider_target_shape"] = None
            intent["blocked_reason"] = None
        elif target_status == "failed":
            intent["status"] = "failed"
            intent["failed_at"] = now
            intent["error"] = str(args.error or "").strip() or "delivery failed"
            error_code = (
                str(getattr(args, "error_code", "") or "").strip()
                or classify_delivery_error(intent.get("error"))
            )
            intent["error_code"] = error_code
            intent["provider_target_shape"] = notification_target_shape(
                intent.get("notification_target") or {}
            )
        else:
            raise ValidationError(f"Unsupported notification status: {target_status}")

        intent["updated_at"] = now
        state["updated_at"] = now
        state.setdefault("history", {}).setdefault("audit_trail", []).append(
            {
                "at": now,
                "event": "delivery_intent_recorded",
                "delivery_intent_id": intent_id,
                "previous_status": previous_status,
                "status": intent["status"],
                "error_code": intent.get("error_code"),
                "sent_incremented": sent_incremented,
            }
        )
        result = {
            "status": intent["status"],
            "delivery_intent_id": intent_id,
            "previous_status": previous_status,
            "error_code": intent.get("error_code"),
            "provider_target_shape": intent.get("provider_target_shape"),
            "sent_incremented": sent_incremented,
            "sent_updates": int(
                state.setdefault("delivery", {}).get("sent_updates") or 0
            ),
        }

    refresh_task_playbook(task)
    json_dump(result or {})
    return 0


def fail_iteration(args: argparse.Namespace) -> int:
    task = ResearchTask.from_args(
        Path(args.root).expanduser().resolve(), research_id=args.id, path=args.path
    )
    manager = StateManager(task)
    remove_job_id: str | None = None
    queue_release: dict[str, Any] | None = None
    lease_token: str | None = None
    update_text: str | None = None
    delivery_intent: dict[str, Any] | None = None
    with manager.editor() as state:
        lock = state.get("lock") or {}
        if state.get("status") != "running" or lock.get("status") != "held":
            raise ValidationError("No active run to fail")
        if lock.get("run_id") != args.run_id:
            raise ValidationError(
                f"Active run id mismatch: expected {lock.get('run_id')}, got {args.run_id}"
            )
        lease_token = lock.get("lease_token")

        now = utc_now()
        iteration_index = int(
            lock.get("iteration_index")
            or (int(state["progress"].get("iteration_count") or 0) + 1)
        )
        error_message = args.error.strip()
        state["errors"]["failure_count"] = (
            int(state["errors"].get("failure_count") or 0) + 1
        )
        state["errors"]["consecutive_failures"] = (
            int(state["errors"].get("consecutive_failures") or 0) + 1
        )
        state["errors"]["last_error"] = {
            "at": now,
            "run_id": args.run_id,
            "message": error_message,
        }

        threshold = int(state["errors"].get("failure_threshold") or 3)
        stop_requested = bool(state.get("control", {}).get("stop_requested"))
        pause_requested = bool(state.get("control", {}).get("pause_requested"))
        threshold_reached = state["errors"]["consecutive_failures"] >= threshold
        if stop_requested:
            next_status = "cancelled"
        elif args.requires_user_input or threshold_reached:
            next_status = "failed"
        elif pause_requested:
            next_status = "paused"
        else:
            next_status = "idle"

        task.write_iteration_markdown(
            iteration_index=iteration_index,
            run_id=args.run_id,
            status="failed",
            phase=state.get("phase") or "search",
            summary=f"Iteration failed: {error_message}",
            next_angle=state.get("working_memory", {}).get("next_angle"),
            meaningful_progress=False,
            sources=[],
            findings=[],
            open_questions=state.get("working_memory", {}).get("open_questions") or [],
            note="worker failure",
        )

        normalized_reason = set_history_reason(
            state,
            reason_for_failure(
                next_status=next_status,
                requires_user_input=bool(args.requires_user_input),
                threshold_reached=bool(threshold_reached),
                stop_requested=stop_requested,
                pause_requested=pause_requested,
            ),
        )
        state["status"] = next_status
        if next_status in FINAL_STATUSES:
            remove_job_id = state.get("job", {}).get("job_id")
        state["updated_at"] = now
        state["lock"].update(
            {
                "status": "free",
                "run_id": None,
                "lease_token": NO_ACTIVE_LEASE,
                "started_at": None,
                "iteration_index": None,
            }
        )
        state.setdefault("queue", {}).update(
            {
                "status": "free",
                "active_task_id": None,
                "active_run_id": None,
                "last_released_at": now,
            }
        )
        if next_status == "paused":
            state["control"]["pause_requested"] = False
            suspend_bound_job(state, reason="paused", at=now)
        if next_status in {"failed", "cancelled"}:
            state["control"]["stop_requested"] = False
        state["history"]["last_transition"] = f"fail:{next_status}"

        notify_user = bool(
            args.requires_user_input or next_status in {"failed", "cancelled"}
        )
        if notify_user:
            update_text = compose_failure_update_text(state, error_message, next_status)
            delivery_intent = _upsert_delivery_intent(
                state,
                run_id=args.run_id,
                transition=f"fail:{next_status}",
                update_text=update_text,
                primary_file=state.get("delivery", {}).get("primary_file"),
                attachments=state.get("delivery", {}).get("attachments") or [],
            )

        append_run_log(
            task,
            timestamp=now,
            iteration=iteration_index,
            run_id=args.run_id,
            phase=state.get("phase") or "search",
            outcome=f"failed:{next_status}",
            normalized_reason=normalized_reason,
            meaningful_progress=False,
            low_yield_streak=int(
                (state.get("saturation") or {}).get("consecutive_low_yield") or 0
            ),
            topic_saturated=bool(
                (state.get("saturation") or {}).get("topic_saturated")
            ),
            short_summary=f"Iteration failed: {error_message}",
        )

    queue_release = release_global_queue(
        task.task_dir.parent,
        task_id=state["id"],
        run_id=args.run_id,
        lease_token=lease_token,
        released_by="fail",
    )

    removal_payload = None
    if remove_job_id:
        removal_payload = remove_cron_job(remove_job_id)
        clear_bound_job(
            task, removed_job_id=remove_job_id, removal_payload=removal_payload
        )

    refresh_task_playbook(task)
    json_dump(
        {
            "status": next_status,
            "normalized_reason": normalized_reason,
            "notify_user": notify_user,
            "update_text": update_text,
            "delivery_intent": delivery_intent,
            "owner": state.get("owner"),
            "error": error_message,
            "failure_count": state["errors"]["failure_count"],
            "consecutive_failures": state["errors"]["consecutive_failures"],
            "removed_job_id": remove_job_id,
            "removal_payload": removal_payload,
            "queue_release": queue_release,
        }
    )
    return 0
