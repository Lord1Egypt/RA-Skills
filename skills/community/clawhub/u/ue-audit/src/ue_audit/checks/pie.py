"""Opt-in PIE smoke check.

This starts Play-In-Editor, waits a short window, reads only the new log lines,
and stops PIE in a finally block. It is stateful but does not save assets.
"""

from __future__ import annotations

import re
import time
from typing import Any

from .base import AuditContext, bridge_error_message, finish_check, make_finding, new_check
from .logs import ERROR_PATTERNS, WARNING_PATTERNS
from ..report.model import Severity, Status


def _new_lines(ctx: AuditContext, cursor: int) -> tuple[list[str], int]:
    result = ctx.bridge.call("logs_read", {"lines": 500, "cursor": cursor})
    data = result.get("data") if isinstance(result, dict) and isinstance(result.get("data"), dict) else {}
    lines = data.get("lines") or []
    next_cursor = int(data.get("next_cursor") or cursor)
    return [str(line) for line in lines], next_cursor


def check_pie(ctx: AuditContext):
    check = new_check("PIE001", "PIE smoke (opt-in, stateful)")
    if not ctx.options.pie:
        check.status = Status.SKIP
        check.summary = "PIE smoke was not requested."
        check.details = {"reason": "pie_not_requested"}
        return check
    if not ctx.options.live or ctx.bridge is None:
        check.status = Status.UNKNOWN
        check.summary = "PIE smoke requires --live and a reachable bridge."
        check.details = {"reason": "bridge_unavailable", "error": ctx.bridge_error}
        return check

    details: dict[str, Any] = {
        "mode": ctx.options.pie_mode,
        "duration_s": ctx.options.pie_seconds,
        "started": False,
        "playing": False,
        "stopped": False,
        "states": [],
        "log_lines": 0,
        "error_count": 0,
        "warning_count": 0,
        "start_error": "",
        "stop_error": "",
    }

    try:
        before = ctx.bridge.call("pie_state", {})
        before_data = before.get("data") if isinstance(before, dict) and isinstance(before.get("data"), dict) else {}
        if before_data.get("is_playing"):
            check.status = Status.SKIP
            check.summary = "PIE was already running; the audit did not start or stop it."
            check.details = {**details, "reason": "pie_already_running"}
            return check
    except Exception as exc:  # noqa: BLE001
        check.status = Status.UNKNOWN
        check.summary = "Could not read PIE state."
        check.details = {**details, "reason": "pie_state_failed", "error": bridge_error_message(exc)}
        return check

    try:
        cursor_result = ctx.bridge.call("logs_read", {"lines": 1, "cursor": 0})
        cursor_data = (
            cursor_result.get("data")
            if isinstance(cursor_result, dict) and isinstance(cursor_result.get("data"), dict)
            else {}
        )
        before_cursor = int(cursor_data.get("next_cursor") or 0)
    except Exception:  # noqa: BLE001
        before_cursor = 0

    try:
        started_result = ctx.bridge.call_stateful("pie_start", {"mode": ctx.options.pie_mode})
        details["started"] = True
        details["start_result"] = started_result
    except Exception as exc:  # noqa: BLE001
        details["start_error"] = bridge_error_message(exc)
        details["reason"] = "pie_start_unavailable"
        check.status = Status.UNKNOWN
        check.severity = Severity.WARNING
        check.summary = "PIE could not be started; the smoke check is inconclusive."
        check.details = details
        check.add(
            make_finding(
                "PIE001",
                Severity.WARNING,
                Status.UNKNOWN,
                "PIE could not be started",
                details["start_error"],
                recommendation="Check the editor state and bridge API support; PIE smoke is opt-in and stateful.",
            )
        )
        return finish_check(check)

    try:
        deadline = time.time() + max(0.5, float(ctx.options.pie_seconds))
        while time.time() < deadline:
            time.sleep(0.5)
            try:
                state = ctx.bridge.call("pie_state", {})
            except Exception as exc:  # noqa: BLE001
                details["states"].append({"error": bridge_error_message(exc)})
                continue
            state_data = (
                state.get("data")
                if isinstance(state, dict) and isinstance(state.get("data"), dict)
                else {}
            )
            details["states"].append(
                {
                    "is_playing": bool(state_data.get("is_playing")),
                    "world": state_data.get("world", ""),
                    "time_seconds": state_data.get("time_seconds", 0),
                }
            )
            if state_data.get("is_playing"):
                details["playing"] = True
    finally:
        try:
            stop_result = ctx.bridge.call_stateful("pie_stop", {})
            details["stopped"] = True
            details["stop_result"] = stop_result
        except Exception as exc:  # noqa: BLE001
            details["stop_error"] = bridge_error_message(exc)

    if not details["playing"]:
        check.status = Status.UNKNOWN
        check.severity = Severity.WARNING
        check.summary = "PIE did not report is_playing during the smoke window."
        check.details = details
        check.add(
            make_finding(
                "PIE001",
                Severity.WARNING,
                Status.UNKNOWN,
                "PIE did not start playing",
                "pie_state never reported is_playing=true during the smoke window.",
                recommendation="Check whether PIE is blocked by a modal dialog or editor focus.",
            )
        )
        return finish_check(check)

    try:
        lines, _ = _new_lines(ctx, before_cursor)
    except Exception as exc:  # noqa: BLE001
        lines = []
        details["log_error"] = bridge_error_message(exc)
    details["log_lines"] = len(lines)
    for line in lines:
        if any(pattern.search(line) for pattern in ERROR_PATTERNS):
            details["error_count"] += 1
            if details["error_count"] <= 20:
                check.add(
                    make_finding(
                        "PIE001",
                        Severity.ERROR,
                        Status.FAIL,
                        "PIE log error",
                        line.strip()[:300],
                        recommendation="Inspect the new PIE log lines and fix the runtime error.",
                    )
                )
        elif any(pattern.search(line) for pattern in WARNING_PATTERNS):
            details["warning_count"] += 1

    if details["stop_error"]:
        check.add(
            make_finding(
                "PIE001",
                Severity.WARNING,
                Status.WARN,
                "PIE did not stop cleanly",
                details["stop_error"],
                recommendation="Stop PIE manually in the editor and check the bridge.",
            )
        )
    if details["error_count"]:
        check.status = Status.FAIL
        check.summary = f"PIE ran but produced {details['error_count']} error line(s)."
    elif details["stop_error"]:
        check.status = Status.WARN
        check.summary = "PIE ran; stop reported an error."
    else:
        check.status = Status.PASS
        check.summary = (
            f"PIE ran for {ctx.options.pie_seconds}s; "
            f"new log lines={details['log_lines']}, errors=0"
        )
    check.details = details
    return finish_check(check)
