#!/usr/bin/env python3
"""Register zhizhi-math-coach scheduled reminder jobs with OpenClaw cron when available."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from learning_workspace_config import (  # noqa: E402
    DEFAULT_AUTOMATION_TASKS,
    load_config,
    update_config,
)


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def shell_quote(value: str) -> str:
    return "'" + value.replace("'", "'\"'\"'") + "'"


def existing_cron_output(openclaw_bin: str, workspace: Path) -> str:
    result = run([openclaw_bin, "cron", "list"], workspace)
    if result.returncode != 0:
        return ""
    return result.stdout + "\n" + result.stderr


def task_message(task: dict[str, Any], workspace: Path, config: dict[str, Any]) -> str:
    allow_writes = bool(config.get("automation", {}).get("allow_record_writes"))
    allow_worksheets = bool(config.get("automation", {}).get("allow_auto_worksheet_generation"))
    base = (
        "Use $zhizhi-math-coach for Zhizhi's math learning workspace. "
        f"Workspace path: {workspace}. "
        "Read .zhizhi-math-coach/config.json first. If Git sync is configured, pull latest learning data before reading records. "
    )
    if task.get("kind") == "weekly_review":
        purpose = (
            "Review this week's learning records, weak points, worksheet status, and due spaced reviews. "
            "Return a concise Chinese weekly summary and next-week suggestions for the parent. "
        )
    else:
        purpose = (
            "Check due weak points, ungraded worksheets, pending uploads, and stale short-term observations. "
            "Return concise Chinese reminders and the next suggested action for the parent. "
        )
    boundary = (
        f"Record writes allowed: {str(allow_writes).lower()}. "
        f"Automatic worksheet generation allowed: {str(allow_worksheets).lower()}. "
        "Unless explicitly allowed by config, do not modify memory, records, weak-point status, or generate worksheets. "
        "If files are changed and Git sync is configured, commit and push with sync_learning_repo.py after the task."
    )
    return base + purpose + boundary


def build_command(
    openclaw_bin: str,
    workspace: Path,
    task: dict[str, Any],
    timezone: str,
    model: str | None,
    thinking: str | None,
) -> list[str]:
    cmd = [
        openclaw_bin,
        "cron",
        "add",
        "--name",
        str(task["name"]),
        "--cron",
        str(task["cron"]),
        "--tz",
        timezone,
        "--session",
        str(task.get("session") or "isolated"),
        "--message",
        task_message(task, workspace, load_config(workspace) or {}),
        "--label",
        "zhizhi-math-coach",
        "--label",
        str(task.get("kind") or "math-learning"),
    ]
    if model:
        cmd.extend(["--model", model])
    if thinking:
        cmd.extend(["--thinking", thinking])
    return cmd


def print_command(cmd: list[str]) -> None:
    print(" ".join(shell_quote(part) if any(ch.isspace() for ch in part) else part for part in cmd))


def ensure_automation_config(workspace: Path, auto_register: bool, timezone: str | None) -> dict[str, Any]:
    config = load_config(workspace) or {}
    automation = config.get("automation", {})
    if not isinstance(automation, dict):
        automation = {}
    tasks = automation.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        tasks = DEFAULT_AUTOMATION_TASKS
    patch = {
        "automation": {
            "enabled": True,
            "scheduler": "openclaw-cron",
            "auto_register_when_supported": auto_register,
            "timezone": timezone or automation.get("timezone") or "Asia/Shanghai",
            "allow_record_writes": bool(automation.get("allow_record_writes")),
            "allow_auto_worksheet_generation": bool(automation.get("allow_auto_worksheet_generation")),
            "tasks": tasks,
            "registered_jobs": automation.get("registered_jobs") if isinstance(automation.get("registered_jobs"), list) else [],
        }
    }
    return update_config(workspace, patch)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Register zhizhi-math-coach OpenClaw cron reminder jobs.")
    parser.add_argument("--workspace", type=Path, default=Path("."), help="Personal learning repository root.")
    parser.add_argument("--openclaw-bin", default="openclaw", help="OpenClaw CLI binary name or path.")
    parser.add_argument("--model", help="Optional model override for cron runs.")
    parser.add_argument("--thinking", help="Optional thinking level override for cron runs.")
    parser.add_argument("--timezone", help="IANA timezone for scheduled reminders, for example Asia/Shanghai.")
    parser.add_argument("--print-only", action="store_true", help="Print commands without executing them.")
    parser.add_argument("--enable-config", action="store_true", help="Enable automation in .zhizhi-math-coach/config.json.")
    parser.add_argument("--auto-register", action="store_true", help="Persist auto_register_when_supported=true in config.")
    parser.add_argument("--force", action="store_true", help="Add jobs even if a job name already appears in openclaw cron list output.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workspace = args.workspace.resolve()
    if not workspace.exists():
        print(f"error: workspace does not exist: {workspace}", file=sys.stderr)
        return 2

    config = load_config(workspace)
    if args.enable_config or config is None:
        config = ensure_automation_config(workspace, args.auto_register, args.timezone)
    if config is None:
        print("error: missing .zhizhi-math-coach/config.json; run configure_learning_workspace.py first", file=sys.stderr)
        return 2

    automation = config.get("automation", {})
    if not isinstance(automation, dict) or not automation.get("enabled"):
        print("skipped: automation.enabled is false; pass --enable-config to enable scheduled reminders")
        return 0

    tasks = automation.get("tasks") if isinstance(automation.get("tasks"), list) else DEFAULT_AUTOMATION_TASKS
    timezone = str(args.timezone or automation.get("timezone") or "Asia/Shanghai")
    if args.timezone and args.timezone != automation.get("timezone"):
        config = update_config(workspace, {"automation": {"timezone": args.timezone}})
        automation = config.get("automation", {})
    commands = [
        build_command(args.openclaw_bin, workspace, task, timezone, args.model, args.thinking)
        for task in tasks
        if task.get("enabled", True)
    ]

    openclaw_path = shutil.which(args.openclaw_bin)
    if args.print_only or openclaw_path is None:
        if openclaw_path is None:
            print("openclaw CLI not found; scheduled tasks were not registered on this machine.")
        print("commands:")
        for cmd in commands:
            print_command(cmd)
        return 0

    existing = existing_cron_output(args.openclaw_bin, workspace)
    registered = []
    for cmd in commands:
        name = cmd[cmd.index("--name") + 1]
        if not args.force and name in existing:
            print(f"skipped: cron job already appears to exist: {name}")
            continue
        result = run(cmd, workspace)
        if result.returncode != 0:
            print(result.stderr.strip() or result.stdout.strip() or f"failed: {name}", file=sys.stderr)
            return result.returncode or 1
        print(result.stdout.strip() or f"registered: {name}")
        registered.append(
            {
                "name": name,
                "registered_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                "command": cmd,
                "output": result.stdout.strip(),
            }
        )

    if registered:
        old_jobs = automation.get("registered_jobs") if isinstance(automation.get("registered_jobs"), list) else []
        update_config(workspace, {"automation": {"registered_jobs": [*old_jobs, *registered]}})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
