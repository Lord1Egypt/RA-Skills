"""Parsing helpers for `bb-browser site ... --json` subprocess output."""

from __future__ import annotations

import json
from subprocess import CompletedProcess
from typing import Any


def parse_site_json_output(result: CompletedProcess) -> dict[str, Any]:
    """Parse stdout from `bb-browser site <adapter> ... --json`.

    On failure, bb-browser typically exits with code 1 and prints a JSON object
    to stdout (e.g. ``success: false``, ``error``, ``hint``); stderr is often
    empty. Callers must not rely on stderr alone.
    """
    stdout = (result.stdout or "").strip()
    stderr = (result.stderr or "").strip()

    if result.returncode != 0:
        if stdout:
            try:
                parsed = json.loads(stdout)
            except json.JSONDecodeError:
                parsed = None
            if isinstance(parsed, dict) and parsed.get("error"):
                msg = str(parsed["error"])
                hint = parsed.get("hint")
                if hint:
                    msg = f"{msg}. Hint: {hint}"
                blob = f"{msg} {hint or ''}".lower()
                if any(
                    k in blob
                    for k in ("daemon", "cdp", "chrome not connected", "websocket")
                ):
                    return {"error": "daemon_disconnected", "detail": msg[:500]}
                return {"error": msg}
        tail = stderr or stdout[:500] or "(no output)"
        blob = tail.lower()
        if any(
            k in blob
            for k in ("daemon", "cdp", "chrome not connected", "websocket")
        ):
            return {"error": "daemon_disconnected", "detail": tail[:500]}
        return {"error": f"Exit code {result.returncode}: {tail[:300]}"}

    if not stdout:
        return {"error": "Empty response"}
    try:
        return json.loads(stdout)
    except json.JSONDecodeError as e:
        return {"error": f"JSON parse error: {e}"}
