#!/usr/bin/env python3
import argparse
import json

from client import compact, ensure_file_exists, parse_extra_json, print_json, request_json, task_error_message, task_terminal_state, upload_file, wait_for_task_completion
from schedule_task_watch import WatchSchedulingError, build_watch_job_plan, remove_task_watch, schedule_task_watch


DEFAULT_WAIT_TIMEOUT_SECONDS = 1800


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Synthesize a talking-head video through the platform API.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--digital-human-id", required=True)

    parser.add_argument("--voice-id", default="")
    parser.add_argument("--script", default="")
    parser.add_argument("--audio-file")
    parser.add_argument("--audio-file-id")
    parser.add_argument("--audio-url")

    parser.add_argument("--background-file")
    parser.add_argument("--background-file-id")
    parser.add_argument("--background-url")

    parser.add_argument("--width", type=int)
    parser.add_argument("--height", type=int)
    parser.add_argument("--callback-url", default="")
    parser.add_argument("--extra-json", default="")
    parser.add_argument("--watch-interval", default="1m")
    parser.add_argument("--wait-timeout-seconds", type=int, default=DEFAULT_WAIT_TIMEOUT_SECONDS)

    parser.add_argument("--model", type=int, choices=[0, 1])
    parser.add_argument("--resolution-rate", type=int, choices=[0, 1])
    parser.add_argument("--compliance-watermark-position", type=int, choices=[0, 1, 2, 3])

    watermark_group = parser.add_mutually_exclusive_group()
    watermark_group.add_argument("--add-compliance-watermark", dest="add_compliance_watermark", action="store_true")
    watermark_group.add_argument("--no-add-compliance-watermark", dest="add_compliance_watermark", action="store_false")
    parser.set_defaults(add_compliance_watermark=None)

    subtitle_group = parser.add_mutually_exclusive_group()
    subtitle_group.add_argument("--subtitle-show", dest="subtitle_show", action="store_true")
    subtitle_group.add_argument("--no-subtitle-show", dest="subtitle_show", action="store_false")
    parser.set_defaults(subtitle_show=None)
    parser.add_argument("--subtitle-font-type", default="")
    parser.add_argument("--subtitle-font-size", type=int)
    parser.add_argument("--subtitle-font-color", default="")
    parser.add_argument("--subtitle-border-color", default="")
    parser.add_argument("--subtitle-border-width", type=int)
    parser.add_argument("--subtitle-x", type=int)
    parser.add_argument("--subtitle-y", type=int)
    parser.add_argument("--subtitle-width", type=int)
    parser.add_argument("--subtitle-height", type=int)
    parser.add_argument("--subtitle-asr-type", type=int, choices=[0, 1])
    parser.add_argument("--subtitle-items-json", default="")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    audio_upload = None
    background_upload = None

    use_tts = bool(args.script)
    if not use_tts and not any([args.audio_file, args.audio_file_id, args.audio_url]):
        raise SystemExit("Provide --script for TTS, or provide one of --audio-file, --audio-file-id, --audio-url.")

    audio_file_id = args.audio_file_id
    audio_url = args.audio_url
    if args.audio_file:
        ensure_file_exists(args.audio_file)
        audio_upload = upload_file(args.audio_file, "make_video_audio")
        audio_file_id = audio_upload["upstream_file_id"]

    background_file_id = args.background_file_id
    background_url = args.background_url
    if args.background_file:
        ensure_file_exists(args.background_file)
        background_upload = upload_file(args.background_file, "make_video_background")
        background_file_id = background_upload["upstream_file_id"]

    subtitle_items = None
    if args.subtitle_items_json:
        subtitle_items = json.loads(args.subtitle_items_json)
        if not isinstance(subtitle_items, list):
            raise SystemExit("--subtitle-items-json must be a JSON array.")

    subtitle_enabled = args.subtitle_show is not False

    payload = compact(
        {
            "title": args.title,
            "digital_human_id": args.digital_human_id,
            "voice_id": args.voice_id,
            "script": args.script,
            "audio_file_id": audio_file_id,
            "audio_url": audio_url,
            "background_file_id": background_file_id,
            "background_url": background_url,
            "video_width": args.width,
            "video_height": args.height,
            "model": args.model,
            "resolution_rate": args.resolution_rate,
            "add_compliance_watermark": args.add_compliance_watermark,
            "compliance_watermark_position": args.compliance_watermark_position if args.add_compliance_watermark else None,
            "subtitle_show": subtitle_enabled,
            "subtitle_font_type": args.subtitle_font_type,
            "subtitle_font_size": args.subtitle_font_size,
            "subtitle_font_color": args.subtitle_font_color,
            "subtitle_border_color": args.subtitle_border_color,
            "subtitle_border_width": args.subtitle_border_width,
            "subtitle_x": args.subtitle_x,
            "subtitle_y": args.subtitle_y,
            "subtitle_width": args.subtitle_width,
            "subtitle_height": args.subtitle_height,
            "subtitle_asr_type": args.subtitle_asr_type,
            "subtitle_items": subtitle_items,
            "callback_url": args.callback_url,
            "extra_payload": parse_extra_json(args.extra_json),
        }
    )

    response = request_json("POST", "/openclaw/videos/talking-head", payload=payload)
    task = (response or {}).get("task") or {}
    task_id = task.get("id")
    if not task_id:
        raise SystemExit("Video generation submission did not return task_id.")
    watcher = None
    watcher_error = None
    watcher_status = "unavailable"
    watch_command = None
    plan = build_watch_job_plan(
        task_id=int(task_id),
        task_kind="video",
        label=args.title,
        every=args.watch_interval,
    )
    watch_command = plan.get("shell_command")
    if task_id:
        try:
            watcher = schedule_task_watch(
                task_id=int(task_id),
                task_kind="video",
                label=args.title,
                every=args.watch_interval,
            )
            watcher_status = "scheduled"
        except WatchSchedulingError as exc:
            watcher_error = str(exc)
            watcher_status = "failed"

    submission = {
        "title": args.title,
        "script": args.script,
        "digital_human_id": args.digital_human_id,
        "task_id": task_id,
        "upstream_resource_id": task.get("upstream_resource_id"),
        "status": task.get("status"),
        "watcher_status": watcher_status,
        "watcher_job_id": (watcher or {}).get("job_id"),
        "notify_on_completion": watcher_status == "scheduled" and bool((watcher or {}).get("job_id")),
        "watch_command": watch_command,
    }
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
                f"Video generation timed out after {args.wait_timeout_seconds} seconds. Task ID: {task_id}"
            )
        final_status = task_terminal_state(final_task_payload) or "unknown"
        if final_status != "success":
            error_message = task_error_message(final_task_payload) or f"Task ended with status: {final_status or 'unknown'}"
            raise SystemExit(f"Video generation failed. Task ID: {task_id}. {error_message}")

    print_json(
        {
            "action": "synthesize_talking_video",
            "submission": submission,
            "audio_upload": audio_upload,
            "background_upload": background_upload,
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
