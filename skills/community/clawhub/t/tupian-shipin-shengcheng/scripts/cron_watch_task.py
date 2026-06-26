#!/usr/bin/env python3
import argparse
import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from client import configure_client, request_json, terminal_status
from schedule_task_watch import remove_task_watch


NO_REPLY = "NO_REPLY"
STATE_DIR = Path.home() / ".openclaw" / "cron" / "watchers" / "veo2-openclaw"


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


def attempt_remove_job(job_id: str | None, job_name: str | None) -> None:
    if not job_id and not job_name:
        return
    remove_task_watch(job_id, job_name=job_name)


def _parse_json_response(response):
    raw = response.read()
    if not raw:
        return None
    text = raw.decode("utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw": text}


def send_clawx_im_reply(*, server_url: str, device_id: str, device_token: str, event_id: str, content: str) -> None:
    base_url = server_url.rstrip("/")
    url = f"{base_url}/api/v1/openclaw/bridge/reply"
    body = json.dumps(
        {
            "device_id": device_id,
            "device_token": device_token,
            "event_id": int(event_id),
            "content": content,
            "msg_type": "text",
        },
        ensure_ascii=False,
    ).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request) as response:
            _parse_json_response(response)
    except urllib.error.HTTPError as exc:
        payload = _parse_json_response(exc)
        detail = ""
        if isinstance(payload, dict):
            detail = str(payload.get("detail") or payload.get("message") or "").strip()
        raise RuntimeError(detail or f"ClawX IM reply failed with HTTP {exc.code}.") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Failed to send ClawX IM reply: {exc}") from exc


def send_easyclaw_reply(*, server_url: str, device_id: str, device_token: str, event_id: str, content: str) -> None:
    base_url = server_url.rstrip("/")
    url = f"{base_url}/api/v1/openclaw/bridge/reply"
    body = json.dumps(
        {
            "device_id": device_id,
            "device_token": device_token,
            "event_id": int(event_id),
            "content": content,
            "msg_type": "text",
        },
        ensure_ascii=False,
    ).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request) as response:
            _parse_json_response(response)
    except urllib.error.HTTPError as exc:
        payload = _parse_json_response(exc)
        detail = ""
        if isinstance(payload, dict):
            detail = str(payload.get("detail") or payload.get("message") or "").strip()
        raise RuntimeError(detail or f"easyclaw reply failed with HTTP {exc.code}.") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Failed to send easyclaw reply: {exc}") from exc


def fetch_easyclaw_events(*, server_url: str, device_id: str, device_token: str, limit: int = 100) -> list[dict]:
    base_url = server_url.rstrip("/")
    url = f"{base_url}/api/v1/openclaw/bridge/inbound?device_id={urllib.parse.quote(device_id)}&device_token={urllib.parse.quote(device_token)}&limit={limit}"
    request = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(request) as response:
            payload = _parse_json_response(response)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"easyclaw inbound query failed with HTTP {exc.code}.") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Failed to query easyclaw inbound events: {exc}") from exc
    if not isinstance(payload, dict):
        return []
    events = payload.get("events")
    if not isinstance(events, list):
        return []
    return [item for item in events if isinstance(item, dict)]


def resolve_easyclaw_event_id(
    *,
    server_url: str,
    device_id: str,
    device_token: str,
    event_id: str,
    message_id: str,
    sender_id: str,
    bot_id: str,
) -> str:
    resolved_event_id = str(event_id or "").strip()
    if resolved_event_id:
        return resolved_event_id

    events = fetch_easyclaw_events(
        server_url=server_url,
        device_id=device_id,
        device_token=device_token,
    )

    normalized_message_id = str(message_id or "").strip()
    normalized_sender_id = str(sender_id or "").strip()
    normalized_bot_id = str(bot_id or "").strip()
    exact_matches: list[dict] = []
    fallback_matches: list[dict] = []

    for event in events:
        current_event_id = event.get("event_id")
        if current_event_id in (None, ""):
            continue
        event_sender_id = str(event.get("user_id") or "").strip()
        event_bot_id = str(event.get("bot_id") or "").strip()
        event_message_id = str(event.get("inbound_message_id") or "").strip()
        event_chat_type = str(event.get("chat_type") or "").strip().lower()

        if normalized_sender_id and event_sender_id != normalized_sender_id:
            continue
        if normalized_bot_id and event_bot_id and event_bot_id != normalized_bot_id:
            continue
        if event_chat_type and event_chat_type != "direct":
            continue

        if normalized_message_id and event_message_id == normalized_message_id:
            exact_matches.append(event)
            continue
        fallback_matches.append(event)

    candidates = exact_matches or fallback_matches
    if not candidates:
        raise RuntimeError("Unable to resolve an easyclaw inbound event for background notification.")

    latest = max(candidates, key=lambda item: int(item.get("event_id") or 0))
    return str(latest.get("event_id") or "").strip()


def _read_json_file(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def append_session_notification(
    *,
    session_key: str,
    session_file: str,
    session_store_path: str,
    content: str,
) -> None:
    transcript_path = Path(session_file)
    if not transcript_path.exists():
        raise RuntimeError(f"Session transcript not found: {transcript_path}")
    transcript_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        existing_lines = transcript_path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise RuntimeError(f"Failed to read session transcript: {exc}") from exc

    parent_id = None
    for line in reversed(existing_lines[-200:]):
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if payload.get("type") != "message":
            continue
        message_id = str(payload.get("id") or "").strip()
        if message_id:
            parent_id = message_id
            break

    now = datetime.now(timezone.utc)
    transcript_entry = {
        "type": "message",
        "id": uuid4().hex[:8],
        "parentId": parent_id,
        "timestamp": now.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        "message": {
            "role": "assistant",
            "content": [{"type": "text", "text": content}],
            "timestamp": int(now.timestamp() * 1000),
        },
    }
    try:
        with transcript_path.open("a", encoding="utf-8", newline="\n") as handle:
            if existing_lines:
                handle.write("\n")
            handle.write(json.dumps(transcript_entry, ensure_ascii=False))
    except OSError as exc:
        raise RuntimeError(f"Failed to append session transcript: {exc}") from exc

    if not session_key or not session_store_path:
        return
    store_path = Path(session_store_path)
    store_payload = _read_json_file(store_path)
    if not isinstance(store_payload, dict):
        return
    entry = store_payload.get(session_key)
    if not isinstance(entry, dict):
        return
    entry = dict(entry)
    entry["updatedAt"] = int(now.timestamp() * 1000)
    entry["sessionFile"] = str(transcript_path)
    store_payload[session_key] = entry
    try:
        store_path.write_text(json.dumps(store_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"Failed to update session store: {exc}") from exc


def _first_non_empty(mapping: dict, keys: tuple[str, ...]) -> str | None:
    for key in keys:
        value = mapping.get(key)
        if value not in (None, ""):
            return str(value)
    return None


def _collect_media(payload) -> list[dict[str, str]]:
    if not isinstance(payload, (dict, list)):
        return []

    image_fields = (
        "image_url",
        "imageUrl",
        "image",
        "images",
        "output",
        "cover_url",
        "coverUrl",
        "preview_image_url",
        "previewImageUrl",
        "poster_url",
        "posterUrl",
    )
    video_fields = (
        "video_url",
        "videoUrl",
        "play_url",
        "playUrl",
        "download_url",
        "downloadUrl",
        "url",
    )

    items: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    def visit(node):
        if len(items) >= 10:
            return
        if isinstance(node, dict):
            object_type = str(node.get("object") or node.get("type") or "").strip().lower()
            for field in video_fields:
                value = node.get(field)
                if isinstance(value, str) and value.strip():
                    media_type = "image" if object_type == "image" else "video"
                    key = (media_type, value.strip())
                    if key not in seen:
                        seen.add(key)
                        items.append({"type": media_type, "url": value.strip(), "field": field})
            for field in image_fields:
                value = node.get(field)
                if isinstance(value, str) and value.strip():
                    key = ("image", value.strip())
                    if key not in seen:
                        seen.add(key)
                        items.append({"type": "image", "url": value.strip(), "field": field})
            for value in node.values():
                visit(value)
            return
        if isinstance(node, list):
            for entry in node:
                visit(entry)

    visit(payload)
    return items


def _error_message(payload: dict) -> str | None:
    if not isinstance(payload, dict):
        return None
    for key in ("err_reason", "error_message", "message", "detail", "msg"):
        value = payload.get(key)
        if value not in (None, ""):
            return str(value)
    error = payload.get("error")
    if isinstance(error, dict):
        return _error_message(error)
    if error not in (None, ""):
        return str(error)
    return None


def build_success_message(payload: dict, task_kind: str, label: str) -> str:
    resource_label = label or task_kind
    task_id = _first_non_empty(payload, ("request_id", "requestId", "task_id", "taskId", "id")) or "-"
    model = _first_non_empty(payload, ("model",))
    status = _first_non_empty(payload, ("status", "state", "task_status", "taskStatus")) or "completed"
    lines = [
        f"{task_kind} task completed: {resource_label}",
        f"Task ID: {task_id}",
        f"Status: {status}",
    ]
    if model:
        lines.append(f"Model: {model}")
    for media in _collect_media(payload)[:3]:
        if media["type"] == "image":
            lines.append(f"Image: {media['url']}")
        else:
            lines.append(f"Video: {media['url']}")
    if len(lines) <= 4:
        lines.append("Response:")
        lines.append(json.dumps(payload, ensure_ascii=False, indent=2))
    return "\n".join(lines)


def build_failed_message(payload: dict, task_kind: str, label: str) -> str:
    resource_label = label or task_kind
    task_id = _first_non_empty(payload, ("request_id", "requestId", "task_id", "taskId", "id")) or "-"
    status = _first_non_empty(payload, ("status", "state", "task_status", "taskStatus")) or "failed"
    error_message = _error_message(payload) or "Unknown error."
    return "\n".join(
        [
            f"{task_kind} task failed: {resource_label}",
            f"Task ID: {task_id}",
            f"Status: {status}",
            f"Error: {error_message}",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Check one VEO relay task for OpenClaw cron delivery.")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--task-kind", required=True)
    parser.add_argument("--label", default="")
    parser.add_argument("--watch-key", required=True)
    parser.add_argument("--job-name", default="")
    parser.add_argument("--job-id", default="")
    parser.add_argument("--base-url", default="", help=argparse.SUPPRESS)
    parser.add_argument("--api-token", default="", help=argparse.SUPPRESS)
    parser.add_argument("--api-key", default="", help=argparse.SUPPRESS)
    parser.add_argument("--api-secret", default="", help=argparse.SUPPRESS)
    parser.add_argument("--notify-clawx-event-id", default="", help=argparse.SUPPRESS)
    parser.add_argument("--notify-clawx-server-url", default="", help=argparse.SUPPRESS)
    parser.add_argument("--notify-clawx-device-id", default="", help=argparse.SUPPRESS)
    parser.add_argument("--notify-clawx-device-token", default="", help=argparse.SUPPRESS)
    parser.add_argument("--notify-easyclaw-event-id", default="", help=argparse.SUPPRESS)
    parser.add_argument("--notify-easyclaw-server-url", default="", help=argparse.SUPPRESS)
    parser.add_argument("--notify-easyclaw-device-id", default="", help=argparse.SUPPRESS)
    parser.add_argument("--notify-easyclaw-device-token", default="", help=argparse.SUPPRESS)
    parser.add_argument("--notify-easyclaw-message-id", default="", help=argparse.SUPPRESS)
    parser.add_argument("--notify-easyclaw-sender-id", default="", help=argparse.SUPPRESS)
    parser.add_argument("--notify-easyclaw-bot-id", default="", help=argparse.SUPPRESS)
    parser.add_argument("--notify-session-key", default="", help=argparse.SUPPRESS)
    parser.add_argument("--notify-session-id", default="", help=argparse.SUPPRESS)
    parser.add_argument("--notify-session-file", default="", help=argparse.SUPPRESS)
    parser.add_argument("--notify-session-store-path", default="", help=argparse.SUPPRESS)
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

    payload = request_json("GET", f"/veo2/custom_video/fetch/{args.task_id}")
    status = terminal_status(payload) or "running"
    if status == "running":
        print(NO_REPLY)
        return

    if status == "success":
        message = build_success_message(payload or {}, args.task_kind, args.label)
    else:
        message = build_failed_message(payload or {}, args.task_kind, args.label)

    notification_modes: list[str] = []
    external_notification_succeeded = False

    if (
        args.notify_easyclaw_server_url
        and args.notify_easyclaw_device_id
        and args.notify_easyclaw_device_token
        and (
            args.notify_easyclaw_event_id
            or args.notify_easyclaw_message_id
            or args.notify_easyclaw_sender_id
        )
    ):
        notification_modes.append("easyclaw-reply")
        try:
            resolved_event_id = resolve_easyclaw_event_id(
                server_url=args.notify_easyclaw_server_url,
                device_id=args.notify_easyclaw_device_id,
                device_token=args.notify_easyclaw_device_token,
                event_id=args.notify_easyclaw_event_id,
                message_id=args.notify_easyclaw_message_id,
                sender_id=args.notify_easyclaw_sender_id,
                bot_id=args.notify_easyclaw_bot_id,
            )
            send_easyclaw_reply(
                server_url=args.notify_easyclaw_server_url,
                device_id=args.notify_easyclaw_device_id,
                device_token=args.notify_easyclaw_device_token,
                event_id=resolved_event_id,
                content=message,
            )
        except RuntimeError as exc:
            save_state(
                state_path,
                {
                    "notified": False,
                    "task_id": str(args.task_id),
                    "task_kind": args.task_kind,
                    "status": status,
                    "job_name": args.job_name or None,
                    "job_id": args.job_id or None,
                    "last_notify_error": str(exc),
                    "last_notify_attempt_at": datetime.now(timezone.utc).isoformat(),
                },
            )
            print(NO_REPLY)
            return
        external_notification_succeeded = True
    elif args.notify_clawx_event_id and args.notify_clawx_server_url and args.notify_clawx_device_id and args.notify_clawx_device_token:
        notification_modes.append("clawx-im-reply")
        try:
            send_clawx_im_reply(
                server_url=args.notify_clawx_server_url,
                device_id=args.notify_clawx_device_id,
                device_token=args.notify_clawx_device_token,
                event_id=args.notify_clawx_event_id,
                content=message,
            )
        except RuntimeError as exc:
            save_state(
                state_path,
                {
                    "notified": False,
                    "task_id": str(args.task_id),
                    "task_kind": args.task_kind,
                    "status": status,
                    "job_name": args.job_name or None,
                    "job_id": args.job_id or None,
                    "last_notify_error": str(exc),
                    "last_notify_attempt_at": datetime.now(timezone.utc).isoformat(),
                },
            )
            print(NO_REPLY)
            return
        external_notification_succeeded = True

    if args.notify_session_file and args.notify_session_key:
        notification_modes.append("session-append")
        try:
            append_session_notification(
                session_key=args.notify_session_key,
                session_file=args.notify_session_file,
                session_store_path=args.notify_session_store_path,
                content=message,
            )
        except RuntimeError as exc:
            if not external_notification_succeeded:
                save_state(
                    state_path,
                    {
                        "notified": False,
                        "task_id": str(args.task_id),
                        "task_kind": args.task_kind,
                        "status": status,
                        "job_name": args.job_name or None,
                        "job_id": args.job_id or None,
                        "last_notify_error": str(exc),
                        "last_notify_attempt_at": datetime.now(timezone.utc).isoformat(),
                    },
                )
                print(NO_REPLY)
                return
            save_state(
                state_path,
                {
                    "notified": True,
                    "task_id": str(args.task_id),
                    "task_kind": args.task_kind,
                    "status": status,
                    "job_name": args.job_name or None,
                    "job_id": args.job_id or None,
                    "notification_mode": ",".join(notification_modes),
                    "notified_at": datetime.now(timezone.utc).isoformat(),
                    "session_append_error": str(exc),
                },
            )
            attempt_remove_job(args.job_id or None, args.job_name or None)
            print(NO_REPLY)
            return

    notification_mode = ",".join(notification_modes) or "announce"

    save_state(
        state_path,
        {
            "notified": True,
            "task_id": str(args.task_id),
            "task_kind": args.task_kind,
            "status": status,
            "job_name": args.job_name or None,
            "job_id": args.job_id or None,
            "notification_mode": notification_mode,
            "notified_at": datetime.now(timezone.utc).isoformat(),
        },
    )
    attempt_remove_job(args.job_id or None, args.job_name or None)
    if notification_mode != "announce":
        print(NO_REPLY)
        return
    print(message)


if __name__ == "__main__":
    main()
