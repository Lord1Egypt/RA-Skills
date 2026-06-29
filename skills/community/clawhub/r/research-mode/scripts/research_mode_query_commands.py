from __future__ import annotations

import argparse
import sys
from pathlib import Path

from research_mode_corpus import list_corpus_entries
from research_mode_queue import read_queue_status
from research_mode_registry import list_task_records, resolve_task_from_args
from research_mode_surfaces import (
    build_summary_payload,
    build_synthesis_payload,
    render_summary_text,
    render_synthesis_markdown,
)
from research_mode_utils import (
    ensure_dir,
    effective_lock_stale_timeout_min,
    json_dump,
    minutes_since,
    scheduled_worker_timeout_seconds,
)


def status_command(args: argparse.Namespace) -> int:
    task = resolve_task_from_args(
        Path(args.root).expanduser().resolve(), research_id=args.id, path=args.path
    )
    state = task.read_state()
    if args.format == "text":
        summary = build_summary_payload(task, state, findings_limit=0, sources_limit=0)
        if task.resolved_implicitly:
            summary["resolved_implicitly"] = True
        sys.stdout.write(render_summary_text(summary))
        return 0
    payload = dict(state)
    payload.setdefault("artifacts", {})["task_playbook_path"] = str(
        task.task_playbook_path
    )
    payload.setdefault("artifacts", {})["runs_path"] = str(task.runs_path)
    payload.setdefault("artifacts", {})["input_dir"] = str(task.input_dir)
    payload.setdefault("artifacts", {})["corpus_dir"] = str(task.corpus_dir)
    payload.setdefault("artifacts", {})["corpus_manifest_path"] = str(
        task.corpus_manifest_path
    )
    payload.setdefault("corpus", {})["mode"] = (
        payload.setdefault("corpus", {}).get("mode") or "web"
    )
    payload.setdefault("corpus", {})["entries"] = list_corpus_entries(task)
    lock = state.get("lock") or {}
    if lock.get("status") == "held" and lock.get("started_at"):
        lock_age_min = minutes_since(lock.get("started_at"))
        timeout_min = effective_lock_stale_timeout_min(state)
        payload["lock"]["lock_age_min"] = (
            round(lock_age_min, 2) if lock_age_min is not None else None
        )
        payload["lock"]["effective_stale_timeout_min"] = timeout_min
        payload["lock"]["worker_timeout_seconds"] = scheduled_worker_timeout_seconds(
            state
        )
        payload["lock"]["is_stale"] = (
            lock_age_min is not None and lock_age_min > timeout_min
        )
    if task.resolved_implicitly:
        payload["resolved_implicitly"] = True
    json_dump(payload)
    return 0


def summary_command(args: argparse.Namespace) -> int:
    task = resolve_task_from_args(
        Path(args.root).expanduser().resolve(), research_id=args.id, path=args.path
    )
    state = task.read_state()
    summary = build_summary_payload(
        task,
        state,
        findings_limit=args.findings_limit,
        sources_limit=args.sources_limit,
    )
    if task.resolved_implicitly:
        summary["resolved_implicitly"] = True
    if args.format == "text":
        sys.stdout.write(render_summary_text(summary))
        return 0
    json_dump(summary)
    return 0


def preflight_command(args: argparse.Namespace) -> int:
    task = resolve_task_from_args(
        Path(args.root).expanduser().resolve(), research_id=args.id, path=args.path
    )
    state = task.read_state()
    preflight_raw = state.get("preflight")
    configured = isinstance(preflight_raw, dict)
    preflight = preflight_raw if configured else {}
    artifact_rel = preflight.get("artifact_markdown")
    artifact_path = None
    artifact_exists = False
    if artifact_rel:
        path = Path(str(artifact_rel))
        if not path.is_absolute():
            path = task.task_dir / path
        artifact_path = str(path)
        artifact_exists = path.exists()
    payload = {
        "id": state.get("id"),
        "status": state.get("status"),
        "phase": state.get("phase"),
        "preflight": {
            "configured": configured,
            "done": bool(preflight.get("done", False)),
            "decision": preflight.get("decision"),
            "iteration_index": int(preflight.get("iteration_index") or 0),
            "iteration_limit": int(preflight.get("iteration_limit") or 0),
            "artifact_markdown": artifact_rel,
            "artifact_path": artifact_path,
            "artifact_exists": artifact_exists,
            "warnings": preflight.get("warnings") or [],
            "blockers": preflight.get("blockers") or [],
            "target_phase": preflight.get("target_phase"),
            "completed_at": preflight.get("completed_at"),
        },
    }
    if args.format == "text":
        p = payload["preflight"]
        lines = [
            f"Preflight: {state.get('id')}",
            f"Status: {'done' if p['done'] else 'pending' if p['configured'] else 'not configured'}",
            f"Decision: {p.get('decision') or '-'}",
            f"Target phase: {p.get('target_phase') or '-'}",
            f"Artifact: {p.get('artifact_markdown') or '-'}",
        ]
        if p.get("warnings"):
            lines.append("Warnings:")
            lines.extend(f"- {item}" for item in p["warnings"])
        if p.get("blockers"):
            lines.append("Blockers:")
            lines.extend(f"- {item}" for item in p["blockers"])
        sys.stdout.write("\n".join(lines).rstrip() + "\n")
        return 0
    json_dump(payload)
    return 0


def draft_report_command(args: argparse.Namespace) -> int:
    task = resolve_task_from_args(
        Path(args.root).expanduser().resolve(), research_id=args.id, path=args.path
    )
    state = task.read_state()
    synthesis = build_synthesis_payload(
        task,
        state,
        findings_limit=args.findings_limit,
        sources_limit=args.sources_limit,
    )
    if args.format == "json":
        json_dump(synthesis)
        return 0
    sys.stdout.write(render_synthesis_markdown(synthesis))
    return 0


def list_tasks(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve()
    ensure_dir(root)
    tasks = [
        {
            "id": record.get("id"),
            "status": record.get("status"),
            "phase": record.get("phase"),
            "goal": record.get("goal"),
            "job_id": record.get("job_id"),
            "iteration_count": record.get("iteration_count"),
            "updated_at": record.get("updated_at"),
            "task_dir": record.get("task_dir"),
        }
        for record in list_task_records(root)
    ]
    if args.format == "text":
        if not tasks:
            sys.stdout.write("No research tasks found.\n")
            return 0
        for task in tasks:
            sys.stdout.write(
                f"- {task['id']} | {task['status']} | phase={task['phase']} | iterations={task['iteration_count']} | updated={task['updated_at']}\n"
            )
        return 0
    json_dump({"tasks": tasks, "count": len(tasks)})
    return 0


def queue_status_command(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve()
    ensure_dir(root)
    payload = read_queue_status(root)
    if args.format == "text":
        if payload.get("active_task_id"):
            sys.stdout.write(
                "Queue: running global research worker\n"
                f"Active: {payload.get('active_task_id')} / {payload.get('active_run_id')}\n"
            )
        else:
            sys.stdout.write("Queue: free\n")
        waiters = payload.get("waiters") or []
        if waiters:
            sys.stdout.write(f"Waiters: {len(waiters)}\n")
            for idx, waiter in enumerate(waiters, start=1):
                sys.stdout.write(
                    f"- {idx}. {waiter.get('task_id')} since {waiter.get('first_waiting_at')}\n"
                )
        findings = payload.get("findings") or []
        if findings:
            sys.stdout.write("Findings:\n")
            for finding in findings:
                sys.stdout.write(
                    f"- {finding.get('code')}: {finding.get('message')}\n"
                )
        return 0
    json_dump(payload)
    return 0
