from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess  # nosec B404
from pathlib import Path
from typing import Any

from research_mode_control_commands import bind_job
from research_mode_payloads import build_initial_state
from research_mode_runtime import (
    clear_bound_job,
    extract_json_from_stdout,
    remove_cron_job,
    render_worker_prompt_text,
)
from research_mode_task import ResearchTask
from research_mode_utils import (
    ValidationError,
    atomic_json_write,
    ensure_dir,
    slugify,
    validate_research_id,
)
from research_mode_reporting import refresh_task_playbook


def _parse_simple_every_seconds(value: str) -> int | None:
    raw = str(value or "").strip().lower()
    match = re.fullmatch(r"(\d+)\s*([smhd])", raw)
    if not match:
        return None
    amount = int(match.group(1))
    unit = match.group(2)
    multipliers = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    return amount * multipliers[unit]


def _schedule_warnings(args: argparse.Namespace) -> list[dict[str, Any]]:
    warnings: list[dict[str, Any]] = []
    interval_seconds = _parse_simple_every_seconds(str(args.every))
    timeout_seconds = int(args.timeout_seconds)
    if interval_seconds is not None and timeout_seconds > interval_seconds:
        warnings.append(
            {
                "code": "timeout_exceeds_interval",
                "message": (
                    "The worker timeout is longer than the cron interval; "
                    "overlapping ticks will be skipped by the global queue."
                ),
                "every": str(args.every),
                "interval_seconds": interval_seconds,
                "timeout_seconds": timeout_seconds,
                "recommended_action": (
                    "Use a cron interval at least as long as the worker timeout, "
                    "or accept skipped ticks."
                ),
            }
        )
    return warnings


def create_task_from_args(
    args: argparse.Namespace,
    *,
    state_version: int,
    depth_presets: dict[str, dict[str, int]],
) -> tuple[ResearchTask, dict[str, Any], str]:
    root = Path(args.root).expanduser().resolve()
    ensure_dir(root)
    title = args.title or args.goal
    research_id = (
        args.id or f"{dt.datetime.now().strftime('%Y-%m-%d')}-{slugify(title)}"
    )
    research_id = validate_research_id(research_id)
    args.id = research_id
    task = ResearchTask.from_args(root, research_id=research_id)
    if task.exists():
        raise ValidationError(f"Research task already exists: {research_id}")
    task.ensure_layout()
    state = build_initial_state(
        args, task, state_version=state_version, depth_presets=depth_presets
    )
    atomic_json_write(task.state_path, state)
    refresh_task_playbook(task, state)
    return task, state, research_id


def preview_task_from_args(
    args: argparse.Namespace,
    *,
    state_version: int,
    depth_presets: dict[str, dict[str, int]],
) -> tuple[ResearchTask, dict[str, Any], str]:
    root = Path(args.root).expanduser().resolve()
    title = args.title or args.goal
    research_id = (
        args.id or f"{dt.datetime.now().strftime('%Y-%m-%d')}-{slugify(title)}"
    )
    research_id = validate_research_id(research_id)
    args.id = research_id
    task = ResearchTask.from_args(root, research_id=research_id)
    if task.exists():
        raise ValidationError(f"Research task already exists: {research_id}")
    state = build_initial_state(
        args, task, state_version=state_version, depth_presets=depth_presets
    )
    return task, state, research_id


def build_schedule_preview(
    state: dict[str, Any],
    task: ResearchTask,
    args: argparse.Namespace,
    *,
    script_path: Path,
) -> dict[str, Any]:
    prompt = render_worker_prompt_text(state, task, script_path)
    name = args.name or f"research-{state['id']}"
    cmd = [
        "openclaw",
        "cron",
        "add",
        "--name",
        name,
        "--session",
        "isolated",
        "--every",
        args.every,
        "--message",
        prompt,
        "--timeout-seconds",
        str(args.timeout_seconds),
        "--thinking",
        args.thinking,
        "--json",
        "--no-deliver",
    ]
    if args.agent:
        cmd.extend(["--agent", args.agent])
    if args.model:
        cmd.extend(["--model", args.model])
    if args.light_context:
        cmd.append("--light-context")
    return {
        "status": "dry-run",
        "command": cmd,
        "prompt": prompt,
        "warnings": _schedule_warnings(args),
    }


def schedule_task(task: ResearchTask, args: argparse.Namespace, *, script_path: Path) -> dict[str, Any]:
    state = task.read_state()
    existing_job_id = state.get("job", {}).get("job_id")
    if existing_job_id and not getattr(args, "replace_existing", False):
        raise ValidationError(
            f"Task already has a bound cron job: {existing_job_id}. Use --replace-existing to replace it."
        )
    if existing_job_id and getattr(args, "replace_existing", False):
        removal_payload = remove_cron_job(existing_job_id)
        clear_bound_job(
            task, removed_job_id=existing_job_id, removal_payload=removal_payload
        )
        state = task.read_state()

    if args.dry_run:
        return build_schedule_preview(state, task, args, script_path=script_path)

    preview = build_schedule_preview(state, task, args, script_path=script_path)
    cmd = preview["command"]
    name = args.name or f"research-{state['id']}"
    completed = subprocess.run(  # nosec B603
        cmd, capture_output=True, text=True, check=True
    )
    payload = extract_json_from_stdout(completed.stdout)
    job_id = payload.get("jobId") or payload.get("id")
    if not job_id:
        raise ValidationError(f"Cron add returned JSON without job id: {payload}")
    bind_args = argparse.Namespace(
        root=args.root,
        id=state["id"],
        path=str(task.task_dir),
        job_id=job_id,
        mode="recurring",
        every=args.every,
        silent=True,
        schedule_template={
            "mode": "recurring",
            "tick_every_min": args.every,
            "name": name,
            "thinking": args.thinking,
            "agent": args.agent,
            "model": args.model,
            "light_context": args.light_context,
            "timeout_seconds": args.timeout_seconds,
        },
    )
    bind_job(bind_args)
    return {
        "status": "scheduled",
        "job_id": job_id,
        "task_id": state["id"],
        "every": args.every,
        "thinking": args.thinking,
        "warnings": preview.get("warnings") or [],
    }
