#!/usr/bin/env python3
import argparse

from client import compact, ensure_file_exists, parse_extra_json, print_json, request_json, task_error_message, task_terminal_state, upload_file, wait_for_task_completion
from schedule_task_watch import WatchSchedulingError, build_watch_job_plan, remove_task_watch, schedule_task_watch


DEFAULT_WAIT_TIMEOUT_SECONDS = 1800


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Train a voice through the platform API.")
    parser.add_argument("--name", required=True)
    parser.add_argument("--audio-file")
    parser.add_argument("--audio-url")
    parser.add_argument("--callback-url", default="")
    parser.add_argument("--extra-json", default="")
    parser.add_argument("--watch-interval", default="1m")
    parser.add_argument("--wait-timeout-seconds", type=int, default=DEFAULT_WAIT_TIMEOUT_SECONDS)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.audio_file and not args.audio_url:
        raise SystemExit("Provide --audio-file or --audio-url.")

    upload_result = None
    audio_url = args.audio_url

    if args.audio_file:
        ensure_file_exists(args.audio_file)
        upload_result = upload_file(args.audio_file, "prompt_audio")
        audio_url = upload_result["full_path"]

    payload = compact(
        {
            "name": args.name,
            "training_audio_url": audio_url,
            "callback_url": args.callback_url,
            "extra_payload": parse_extra_json(args.extra_json),
        }
    )

    response = request_json("POST", "/openclaw/voices/train", payload=payload)
    task = (response or {}).get("task") or {}
    task_id = task.get("id")
    if not task_id:
        raise SystemExit("Voice training submission did not return task_id.")
    watcher = None
    watcher_error = None
    watcher_status = "unavailable"
    watch_command = None
    if task_id:
        plan = build_watch_job_plan(
            task_id=int(task_id),
            task_kind="voice",
            label=args.name,
            every=args.watch_interval,
        )
        watch_command = plan.get("shell_command")
        try:
            watcher = schedule_task_watch(
                task_id=int(task_id),
                task_kind="voice",
                label=args.name,
                every=args.watch_interval,
            )
            watcher_status = "scheduled"
        except WatchSchedulingError as exc:
            watcher_error = str(exc)
            watcher_status = "failed"

    completion = None
    watcher_removed = False
    final_task_payload = None
    if task_id:
        completion = wait_for_task_completion(
            int(task_id),
            timeout_seconds=args.wait_timeout_seconds,
            poll_interval_seconds=30,
        )
        final_task_payload = completion.get("task_payload") or {}
        if completion.get("finished") and (watcher or {}).get("job_id"):
            watcher_removed = remove_task_watch((watcher or {}).get("job_id"))
        if completion.get("timed_out"):
            raise SystemExit(
                f"Voice training timed out after {args.wait_timeout_seconds} seconds. Task ID: {task_id}"
            )
        final_status = task_terminal_state(final_task_payload) or "unknown"
        if final_status != "success":
            error_message = task_error_message(final_task_payload) or f"Task ended with status: {final_status or 'unknown'}"
            raise SystemExit(f"Voice training failed. Task ID: {task_id}. {error_message}")

    print_json(
        {
            "action": "train_voice",
            "submission": {
                "name": args.name,
                "task_id": task_id,
                "upstream_resource_id": task.get("upstream_resource_id"),
                "status": task.get("status"),
                "watcher_status": watcher_status,
                "watcher_job_id": (watcher or {}).get("job_id"),
                "notify_on_completion": watcher_status == "scheduled" and bool((watcher or {}).get("job_id")),
                "watch_command": watch_command,
            },
            "upload": upload_result,
            "request": payload,
            "response": response,
            "watcher": watcher,
            "watcher_error": watcher_error,
            "completion": completion,
            "final_task": (final_task_payload or {}).get("task") or {},
            "final_result": (final_task_payload or {}).get("result_payload") or {},
            "watcher_removed": watcher_removed,
        }
    )


if __name__ == "__main__":
    main()
