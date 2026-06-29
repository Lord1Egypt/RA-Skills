from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from research_mode_lifecycle_commands import load_result_payload
from research_mode_lifecycle_helpers import stale_lock
from research_mode_queue import read_queue_status
from research_mode_reliability import build_reliability_health_findings
from research_mode_registry import resolve_task_from_args
from research_mode_surfaces import build_summary_payload
from research_mode_utils import ValidationError, json_dump, pending_result_path


def _pending_result_file(task_dir: Path, state: dict[str, Any]) -> Path | None:
    lock = state.get("lock") or {}
    run_id = lock.get("run_id")
    if not run_id:
        return None
    candidate = pending_result_path(task_dir / ".tmp", run_id)
    return candidate if candidate.exists() else None


def build_health_payload(task, state: dict[str, Any]) -> dict[str, Any]:
    summary = build_summary_payload(task, state, findings_limit=0, sources_limit=0)
    findings: list[dict[str, Any]] = []
    recommended_actions: list[dict[str, Any]] = []

    consistency = summary.get("consistency") or {}
    for warning in consistency.get("warnings") or []:
        findings.append(
            {
                "code": warning.get("code") or "consistency_warning",
                "severity": "warning",
                "status": "manual_review_needed",
                "message": warning.get("message") or "State consistency warning",
                "details": warning.get("details") or {},
            }
        )
    for guidance in consistency.get("operator_guidance") or []:
        recommended_actions.append(
            {
                "kind": "manual_review",
                "warning_code": guidance.get("warning_code"),
                "note": guidance.get("note") or "",
                "checklist": guidance.get("checklist") or [],
            }
        )

    for finding in build_reliability_health_findings(state):
        findings.append(finding)
        recommended_actions.append(
            {
                "kind": "manual_review",
                "warning_code": finding.get("code"),
                "note": finding.get("message") or "Inspect reliability condition.",
            }
        )

    task_id = state.get("id")
    for finding in read_queue_status(task.task_dir.parent).get("findings") or []:
        details = finding.get("details") or {}
        if details.get("task_id") != task_id:
            continue
        findings.append(finding)
        recommended_actions.append(
            {
                "kind": "manual_review",
                "warning_code": finding.get("code"),
                "note": finding.get("message") or "Inspect queue state.",
            }
        )

    finalization = state.get("finalization") or {}
    finalization_status = str(finalization.get("status") or "")
    if finalization_status in {"rework", "needs_intervention"}:
        seen_finalization_reasons: set[str] = set()
        for validation_finding in finalization.get("last_validation_findings") or []:
            if validation_finding.get("passed"):
                continue
            for reason in validation_finding.get("reasons") or []:
                reason_code = str(reason or "").strip()
                if not reason_code or reason_code in seen_finalization_reasons:
                    continue
                seen_finalization_reasons.add(reason_code)
                status = (
                    "manual_review_needed"
                    if finalization_status == "needs_intervention"
                    else "repair_needed"
                )
                findings.append(
                    {
                        "code": reason_code,
                        "severity": "warning",
                        "status": status,
                        "message": "Finalization validation did not pass.",
                        "details": {
                            "finalization_status": finalization_status,
                            "check": validation_finding.get("check"),
                        },
                    }
                )
                recommended_actions.append(
                    {
                        "kind": "repair"
                        if finalization_status == "rework"
                        else "manual_review",
                        "warning_code": reason_code,
                        "command": "begin"
                        if finalization_status == "rework"
                        else "summary --format text",
                        "note": "Repair finalization defects before review.",
                    }
                )

    if not task.task_playbook_path.exists():
        findings.append(
            {
                "code": "missing_task_playbook",
                "severity": "warning",
                "status": "repair_needed",
                "message": "The derived task playbook is missing and can be regenerated.",
                "details": {"path": str(task.task_playbook_path)},
            }
        )
        recommended_actions.append(
            {
                "kind": "repair",
                "command": "recover --refresh-derived",
                "note": "Regenerate derived operator surfaces without changing task state.",
            }
        )

    lock = state.get("lock") or {}
    try:
        pending_result = _pending_result_file(task.task_dir, state)
    except ValidationError as exc:
        pending_result = None
        findings.append(
            {
                "code": "invalid_run_id",
                "severity": "error",
                "status": "manual_review_needed",
                "message": "The task lock run_id is invalid.",
                "details": {
                    "run_id": lock.get("run_id"),
                    "error": str(exc),
                },
            }
        )
        recommended_actions.append(
            {
                "kind": "manual_review",
                "warning_code": "invalid_run_id",
                "note": "Inspect state.json before recovery; health will not resolve a pending-result path for an invalid run_id.",
            }
        )
    if pending_result is not None:
        pending_details = {
            "result_file": str(pending_result),
            "run_id": lock.get("run_id"),
            "task_status": state.get("status"),
            "lock_status": lock.get("status"),
            "stale": stale_lock(state),
        }
        try:
            load_result_payload(pending_result)
        except ValidationError as exc:
            findings.append(
                {
                    "code": "invalid_pending_result",
                    "severity": "error",
                    "status": "manual_review_needed",
                    "message": "A pending worker result exists but is not a valid worker result payload.",
                    "details": {**pending_details, "error": str(exc)},
                }
            )
            recommended_actions.append(
                {
                    "kind": "manual_review",
                    "warning_code": "invalid_pending_result",
                    "note": "Inspect the pending result and task state before attempting recovery.",
                    "checklist": [
                        "Open the pending result JSON and verify whether it belongs to the active run.",
                        "Keep the file for bug-report context if the worker wrote an invalid payload.",
                        "Do not run recover until the payload has a valid worker-result shape.",
                    ],
                }
            )
        else:
            if (
                state.get("status") == "running"
                and lock.get("status") == "held"
                and stale_lock(state)
            ):
                findings.append(
                    {
                        "code": "pending_result_available",
                        "severity": "warning",
                        "status": "repair_needed",
                        "message": "A pending worker result exists and can be recovered explicitly.",
                        "details": pending_details,
                    }
                )
                recommended_actions.append(
                    {
                        "kind": "repair",
                        "command": "recover --apply-pending-result",
                        "note": "Run recover only after confirming the pending result belongs to the active run.",
                    }
                )
            elif state.get("status") == "running" and lock.get("status") == "held":
                findings.append(
                    {
                        "code": "active_pending_result_not_stale",
                        "severity": "warning",
                        "status": "blocked",
                        "message": "A pending worker result exists, but the active run is not stale yet.",
                        "details": pending_details,
                    }
                )
                recommended_actions.append(
                    {
                        "kind": "wait",
                        "warning_code": "active_pending_result_not_stale",
                        "note": "Wait for the active worker to finish, or rerun health after the lock becomes stale.",
                    }
                )
            else:
                findings.append(
                    {
                        "code": "pending_result_state_mismatch",
                        "severity": "error",
                        "status": "manual_review_needed",
                        "message": "A pending worker result exists, but task status does not allow automatic recovery.",
                        "details": pending_details,
                    }
                )
                recommended_actions.append(
                    {
                        "kind": "manual_review",
                        "warning_code": "pending_result_state_mismatch",
                        "note": "Inspect task state before resume, repair, or fresh continuation.",
                        "checklist": [
                            "Confirm whether the pending result belongs to the latest run.",
                            "Do not resume until the lock/result mismatch is resolved.",
                            "Use recover only for a running stale task with a valid pending result.",
                        ],
                    }
                )
    elif (
        state.get("status") == "running"
        and lock.get("status") == "held"
        and lock.get("run_id")
        and stale_lock(state)
    ):
        findings.append(
            {
                "code": "stale_run_without_pending_result",
                "severity": "warning",
                "status": "fresh_continuation_recommended",
                "message": "The active run is stale and has no pending worker result to recover.",
                "details": {
                    "run_id": lock.get("run_id"),
                    "task_status": state.get("status"),
                    "lock_status": lock.get("status"),
                    "stale": True,
                },
            }
        )
        recommended_actions.append(
            {
                "kind": "fresh_continuation",
                "command": "begin",
                "note": "Start a fresh continuation from saved state; begin will abandon the stale run and take a new lease.",
            }
        )

    statuses = {str(finding.get("status") or "") for finding in findings}
    if "manual_review_needed" in statuses:
        status = "manual_review_needed"
    elif "blocked" in statuses:
        status = "blocked"
    elif "repair_needed" in statuses:
        status = "repair_needed"
    elif "fresh_continuation_recommended" in statuses:
        status = "fresh_continuation_recommended"
    else:
        status = "ok"

    return {
        "status": status,
        "task_id": state.get("id"),
        "task_status": state.get("status"),
        "phase": state.get("phase"),
        "findings": findings,
        "recommended_actions": recommended_actions,
        "read_only": True,
        "task_dir": str(task.task_dir),
    }


def render_health_text(payload: dict[str, Any]) -> str:
    lines = [
        f"Health: {payload.get('status')}",
        f"Task: {payload.get('task_id')} ({payload.get('task_status')}, phase={payload.get('phase')})",
    ]
    findings = payload.get("findings") or []
    if findings:
        lines.append("Findings:")
        for finding in findings:
            lines.append(f"- {finding.get('code')}: {finding.get('message')}")
    actions = payload.get("recommended_actions") or []
    if actions:
        lines.append("Recommended actions:")
        for action in actions:
            label = action.get("command") or action.get("warning_code") or action.get("kind")
            note = action.get("note") or ""
            lines.append(f"- {label}: {note}" if note else f"- {label}")
    lines.append("Read-only: true")
    return "\n".join(lines) + "\n"


def health_command(args: argparse.Namespace) -> int:
    task = resolve_task_from_args(
        Path(args.root).expanduser().resolve(), research_id=args.id, path=args.path
    )
    state = task.read_state()
    payload = build_health_payload(task, state)
    if args.format == "text":
        sys.stdout.write(render_health_text(payload))
        return 0
    json_dump(payload)
    return 0
