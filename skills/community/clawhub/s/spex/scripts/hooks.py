#!/usr/bin/env python3
"""Hooks system for spex CLI — find and execute hook scripts."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from common import _resolve_hook_roots, logger
from config import get_project_context


def find_hook(hook_name: str, workdir=None) -> Path | None:
    """Find the first executable hook file in priority order.

    Args:
        hook_name: Hook filename (e.g. "post-action").
        workdir: Working directory for spex_root resolution.

    Returns:
        Path to the first executable hook found, or None.
    """
    for root in _resolve_hook_roots(workdir):
        candidate = root / hook_name
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return candidate
    return None


def _build_event_data(event_type: str, payload: dict, workdir=None) -> dict:
    """Build the JSON event envelope from ProjectContext and payload.

    Args:
        event_type: The spex command that triggered this hook.
        payload: Command-specific audit information.
        workdir: Working directory for context resolution.

    Returns:
        Dict with user, email, workdir, event_type, and payload fields.
    """
    ctx = get_project_context(workdir)
    effective_workdir = workdir or (
        str(ctx.top_workdir) if ctx.in_git_workdir() else str(Path.cwd())
    )

    return {
        "user": ctx.user_name,
        "email": ctx.user_email,
        "workdir": str(effective_workdir),
        "event_type": event_type,
        "time": datetime.now().astimezone().isoformat(),
        "payload": payload,
    }


def run_hook(
    hook_name: str, event_data: dict, workdir=None,
) -> subprocess.CompletedProcess | None:
    """Find and execute a hook, piping JSON event data to stdin.

    If no hook is found, returns None.
    If the hook fails (non-zero exit), logs error to stderr.

    Args:
        hook_name: Hook filename to search for.
        event_data: JSON-serializable event envelope.
        workdir: Working directory for hook execution.

    Returns:
        CompletedProcess when a hook was executed, None when no hook found.
    """
    hook_path = find_hook(hook_name, workdir)
    if hook_path is None:
        return None

    payload = json.dumps(event_data)
    result = subprocess.run(
        [str(hook_path)],
        input=payload,
        capture_output=True,
        text=True,
        cwd=workdir,
    )
    if result.returncode != 0:
        logger.warning(
            "Hook '%s' exited with code %d:\nstderr: %s",
            hook_name, result.returncode, result.stderr.strip(),
        )
    return result


def run_post_action(event_type: str, payload: dict, workdir=None,
                    spec_name: str | None = None) -> None:
    """Convenience wrapper to run the post-action hook.

    Args:
        event_type: The spex command that triggered this hook.
        payload: Command-specific audit information.
        workdir: Working directory for hook execution.
        spec_name: Optional spec name added to the payload.
    """
    if spec_name:
        payload = {**payload, "spec_name": spec_name}
    data = _build_event_data(event_type, payload, workdir)
    run_hook("post-action", data, workdir)


def run_pre_action(event_type: str, payload: dict, workdir=None,
                   spec_name: str | None = None) -> None:
    """Convenience wrapper to run the pre-action hook.

    If the hook exits with a non-zero return code, terminates the process
    via ``sys.exit(1)``.

    Args:
        event_type: The spex command that triggered this hook.
        payload: Command-specific audit information.
        workdir: Working directory for hook execution.
        spec_name: Optional spec name added to the payload.
    """
    if spec_name:
        payload = {**payload, "spec_name": spec_name}
    data = _build_event_data(event_type, payload, workdir)
    result = run_hook("pre-action", data, workdir)
    if result is not None and result.returncode != 0:
        sys.exit(1)
