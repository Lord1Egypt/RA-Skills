#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from client import collect_media, configure_client, request_json, task_error_message, task_terminal_state
from schedule_task_watch import remove_task_watch


NO_REPLY = "NO_REPLY"
STATE_DIR = Path.home() / ".openclaw" / "cron" / "watchers" / "chanjing-openclaw"


def state_file_path(watch_key: str) -> Path:
    safe_key = "".join(char for char in watch_key if char.isalnum() or char in ("-", "_"))
    return STATE_DIR / f"{safe_key}.json"


def load_state(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def save_state(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def attempt_remove_job(job_id: str | None) -> None:
    if not job_id:
        return
    remove_task_watch(job_id)


def is_finished(status_value: str) -> bool:
    return status_value in {"success", "failed", "canceled"}


def build_success_message(task_payload: dict, task_kind: str, label: str) -> str:
    task = task_payload.get("task") or {}
    result_payload = task_payload.get("result_payload") or {}
    resource_label = label or result_payload.get("name") or result_payload.get("title") or task_kind
    lines = [
        f"{task_kind} task completed: {resource_label}",
        f"Task ID: #{task.get('id')}",
        f"Status: {task.get('status')}",
    ]
    upstream_resource_id = task.get("upstream_resource_id")
    if upstream_resource_id:
        lines.append(f"Resource ID: {upstream_resource_id}")
    media = collect_media(result_payload)[:3]
    for entry in media:
        media_type = entry.get("type")
        url = entry.get("url")
        if not url:
            continue
        if media_type == "image":
            lines.append(f"![{entry.get('label') or resource_label}]({url})")
        elif media_type == "video":
            lines.append(f"Video: {url}")
        elif media_type == "audio":
            lines.append(f"Audio: {url}")
    if not media and result_payload:
        lines.append("Result:")
        lines.append(json.dumps(result_payload, ensure_ascii=False, indent=2))
    return "\n".join(lines)


def build_failed_message(task_payload: dict, task_kind: str, label: str) -> str:
    task = task_payload.get("task") or {}
    resource_label = label or task_kind
    error_message = task_error_message(task_payload) or "Unknown error."
    lines = [
        f"{task_kind} task failed: {resource_label}",
        f"Task ID: #{task.get('id')}",
        f"Status: {task.get('status')}",
        f"Error: {error_message}",
    ]
    return "\n".join(lines)


def build_message(task_payload: dict, task_kind: str, label: str) -> str:
    task = task_payload.get("task") or {}
    status_value = task_terminal_state(task_payload) or task.get("status") or ""
    status_value = str(status_value).strip().lower()
    if status_value == "success":
        return build_success_message(task_payload, task_kind, label)
    return build_failed_message(task_payload, task_kind, label)


def main() -> None:
    parser = argparse.ArgumentParser(description="Check an async platform task for OpenClaw cron delivery.")
    parser.add_argument("--task-id", type=int, required=True)
    parser.add_argument("--task-kind", required=True)
    parser.add_argument("--label", default="")
    parser.add_argument("--watch-key", required=True)
    parser.add_argument("--job-id", default="")
    parser.add_argument("--base-url", default="", help=argparse.SUPPRESS)
    parser.add_argument("--api-token", default="", help=argparse.SUPPRESS)
    parser.add_argument("--api-key", default="", help=argparse.SUPPRESS)
    parser.add_argument("--api-secret", default="", help=argparse.SUPPRESS)
    args = parser.parse_args()

    configure_client(
        base_url=args.base_url or None,
        api_token=args.api_token or None,
        api_key=args.api_key or None,
        api_secret=args.api_secret or None,
    )

    state_path = state_file_path(args.watch_key)
    state = load_state(state_path)
    if state.get("notified"):
        print(NO_REPLY)
        return

    task_payload = request_json("GET", f"/openclaw/tasks/{args.task_id}", query={"sync": "true"})
    task = task_payload.get("task") or {}
    status_value = task_terminal_state(task_payload) or task.get("status") or ""
    status_value = str(status_value).strip().lower()

    if not is_finished(status_value):
        print(NO_REPLY)
        return

    message = build_message(task_payload, args.task_kind, args.label)
    save_state(
        state_path,
        {
            "notified": True,
            "task_id": args.task_id,
            "task_kind": args.task_kind,
            "status": status_value,
            "job_id": args.job_id or None,
            "notified_at": datetime.now(timezone.utc).isoformat(),
        },
    )
    attempt_remove_job(args.job_id or None)
    print(message)


if __name__ == "__main__":
    main()
