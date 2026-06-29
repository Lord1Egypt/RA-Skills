from __future__ import annotations

from typing import Any

TERMINAL_REASON_PREFIXES = (
    "completed:",
    "failed:",
    "stopped:",
    "rejected:",
)


def is_terminal_reason(reason: str | None) -> bool:
    text = str(reason or "").strip()
    return bool(text) and text.startswith(TERMINAL_REASON_PREFIXES)


def set_history_reason(state: dict[str, Any], reason: str | None) -> str | None:
    text = str(reason or "").strip() or None
    history = state.setdefault("history", {})
    history["last_reason"] = text
    if is_terminal_reason(text):
        history["last_terminal_reason"] = text
    return text


def reason_for_control_action(
    action: str,
    *,
    previous_status: str | None,
    result_status: str | None,
) -> str:
    if action == "pause":
        if result_status == "pause-requested":
            return "pause-requested:user"
        if result_status == "paused":
            return "paused:user"
        return f"noop:pause:{previous_status or 'unknown'}"
    if action == "resume":
        if previous_status == "paused" and result_status == "idle":
            return "resumed:user"
        return f"noop:resume:{previous_status or 'unknown'}"
    if action == "stop":
        if result_status == "stop-requested":
            return "stop-requested:user"
        if result_status == "cancelled":
            return "stopped:user"
        return f"noop:stop:{previous_status or 'unknown'}"
    return f"transition:{action}"


def reason_for_begin_short_circuit(
    *,
    status: str,
    last_terminal_reason: str | None = None,
) -> str:
    if status == "cancelled":
        return last_terminal_reason or "stopped:user"
    if status == "complete":
        return last_terminal_reason or "completed:done"
    if status == "failed":
        return last_terminal_reason or "failed:previous-error"
    if status == "paused":
        return "paused:user"
    return f"state:{status}"


def reason_for_finish(
    *,
    next_status: str,
    completion_triggered: str | None,
    completion_validation_passed: bool | None,
    stop_requested: bool,
    pause_requested: bool,
) -> str:
    if stop_requested or next_status == "cancelled":
        return "stopped:user"
    if next_status == "paused" or pause_requested:
        return "paused:user"
    if completion_validation_passed is False:
        return "rejected:completion-validation"
    if next_status == "complete":
        trigger = str(completion_triggered or "unknown")
        if trigger == "worker":
            return "completed:worker"
        if trigger == "budget":
            return "completed:budget"
        if trigger == "topic_saturated":
            return "completed:topic_saturated"
        return f"completed:{trigger}"
    if next_status == "awaiting_review":
        trigger = str(completion_triggered or "")
        if trigger == "budget":
            return "completed:budget"
        if trigger == "topic_saturated":
            return "completed:topic_saturated"
        return "awaiting_review:passed-validation"
    return "continued:iteration-complete"


def reason_for_failure(
    *,
    next_status: str,
    requires_user_input: bool,
    threshold_reached: bool,
    stop_requested: bool,
    pause_requested: bool,
) -> str:
    if stop_requested or next_status == "cancelled":
        return "stopped:user"
    if requires_user_input and next_status == "failed":
        return "failed:blocker"
    if threshold_reached and next_status == "failed":
        return "failed:error-threshold"
    if next_status == "paused" or pause_requested:
        return "paused:user"
    if next_status == "idle":
        return "retry:worker-error"
    return f"failed:{next_status}"


def record_manual_override(
    state: dict[str, Any],
    reason: str,
    description: str,
    changed_artifacts: list[str] | None = None,
) -> None:
    history = state.setdefault("history", {})
    audit_entries = history.setdefault("audit_trail", [])
    from research_mode_utils import utc_now

    entry: dict[str, Any] = {
        "at": utc_now(),
        "audit_marker": "manual_override",
        "override_reason": reason,
        "description": description,
    }
    if changed_artifacts:
        entry["changed_artifacts"] = changed_artifacts
    audit_entries.append(entry)
    history["last_audit_marker"] = "manual_override"
    history["last_reason"] = f"manual_override:{reason}"
