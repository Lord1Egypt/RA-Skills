#!/usr/bin/env python3
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from uuid import uuid4


DEFAULT_PLATFORM_BASE_URL = "http://easyclaw.bar/shuzirenapi"
USER_PORTAL_URL = "http://easyclaw.bar/shuziren/user/"
KEY_SETUP_HINT = (
    f"Please open {USER_PORTAL_URL} to generate or view your platform token, "
    "then configure it in the OpenClaw skill."
)


class ConfigError(RuntimeError):
    pass


_CLIENT_CONFIG = {
    "base_url": "",
    "api_token": "",
    "api_key": "",
    "api_secret": "",
}


def require_env(name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise ConfigError(f"Missing required environment variable: {name}")
    return value


def configure_client(*, base_url=None, api_token=None, api_key=None, api_secret=None):
    updates = {
        "base_url": base_url,
        "api_token": api_token,
        "api_key": api_key,
        "api_secret": api_secret,
    }
    for key, value in updates.items():
        if value is None:
            continue
        _CLIENT_CONFIG[key] = str(value).strip()


def _configured_value(config_key, env_key):
    value = str(_CLIENT_CONFIG.get(config_key, "") or "").strip()
    if value:
        return value
    return os.environ.get(env_key, "").strip()


def api_base():
    base_url = _configured_value("base_url", "CHANJING_PLATFORM_BASE_URL") or DEFAULT_PLATFORM_BASE_URL
    base_url = base_url.rstrip("/")
    if base_url.endswith("/api"):
        return base_url
    return f"{base_url}/api"


def default_headers(content_type=None):
    platform_token = _configured_value("api_token", "CHANJING_PLATFORM_API_TOKEN")
    if platform_token:
        headers = {"X-API-Token": platform_token}
    else:
        api_key = _configured_value("api_key", "CHANJING_PLATFORM_API_KEY")
        api_secret = _configured_value("api_secret", "CHANJING_PLATFORM_API_SECRET")
        if not api_key or not api_secret:
            raise ConfigError(f"Platform key is not configured. {KEY_SETUP_HINT}")
        headers = {
            "X-API-Key": api_key,
            "X-API-Secret": api_secret,
        }
    if content_type:
        headers["Content-Type"] = content_type
    return headers


def build_url(path, query=None):
    cleaned_path = path if path.startswith("/") else f"/{path}"
    url = f"{api_base()}{cleaned_path}"
    if query:
        encoded = urllib.parse.urlencode(query, doseq=True)
        separator = "&" if "?" in url else "?"
        url = f"{url}{separator}{encoded}"
    return url


def parse_response(response):
    raw = response.read()
    if not raw:
        return None
    text = raw.decode("utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw": text}


def error_message_from_payload(payload):
    if isinstance(payload, dict):
        detail = payload.get("detail")
        if detail not in (None, ""):
            return str(detail)
        message = payload.get("message")
        if message not in (None, ""):
            return str(message)
    if payload not in (None, ""):
        return json.dumps(payload, ensure_ascii=False)
    return None


def request_json(method, path, query=None, payload=None):
    body = None
    headers = default_headers()
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(
        build_url(path, query=query),
        data=body,
        headers=headers,
        method=method.upper(),
    )
    try:
        with urllib.request.urlopen(request) as response:
            return parse_response(response)
    except urllib.error.HTTPError as exc:
        error_payload = parse_response(exc)
        if exc.code == 401:
            raise ConfigError(f"Platform key is invalid or expired. {KEY_SETUP_HINT}") from exc
        message = error_message_from_payload(error_payload)
        if message:
            raise RuntimeError(message) from exc
        raise RuntimeError(f"Platform request failed with HTTP {exc.code}.") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Failed to connect to platform: {exc}") from exc


def encode_multipart(fields, file_field, file_path):
    boundary = f"----OpenClawSkill{uuid4().hex}"
    file_path = Path(file_path)
    file_name = file_path.name
    mime_type = mimetypes.guess_type(file_name)[0] or "application/octet-stream"
    file_bytes = file_path.read_bytes()

    parts = []
    for key, value in fields.items():
        parts.append(f"--{boundary}\r\n".encode("utf-8"))
        parts.append(f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode("utf-8"))
        parts.append(str(value).encode("utf-8"))
        parts.append(b"\r\n")

    parts.append(f"--{boundary}\r\n".encode("utf-8"))
    parts.append(
        f'Content-Disposition: form-data; name="{file_field}"; filename="{file_name}"\r\n'.encode("utf-8")
    )
    parts.append(f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"))
    parts.append(file_bytes)
    parts.append(b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode("utf-8"))
    return boundary, b"".join(parts)


def upload_file(file_path, service):
    boundary, body = encode_multipart({"service": service}, "file", file_path)
    headers = default_headers(content_type=f"multipart/form-data; boundary={boundary}")
    request = urllib.request.Request(
        build_url("/files/upload"),
        data=body,
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request) as response:
            return parse_response(response)
    except urllib.error.HTTPError as exc:
        error_payload = parse_response(exc)
        if exc.code == 401:
            raise ConfigError(f"Platform key is invalid or expired. {KEY_SETUP_HINT}") from exc
        message = error_message_from_payload(error_payload)
        if message:
            raise RuntimeError(message) from exc
        raise RuntimeError(f"Platform upload failed with HTTP {exc.code}.") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Failed to upload file to platform: {exc}") from exc


def ensure_file_exists(file_path):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if not path.is_file():
        raise FileNotFoundError(f"Path is not a file: {path}")
    return path


def compact(value):
    if isinstance(value, dict):
        next_value = {}
        for key, item in value.items():
            compacted = compact(item)
            if compacted is not None:
                next_value[key] = compacted
        return next_value or None
    if isinstance(value, list):
        next_value = [compact(item) for item in value]
        next_value = [item for item in next_value if item is not None]
        return next_value or None
    if value in ("", None):
        return None
    return value


def parse_extra_json(raw_value):
    if not raw_value:
        return {}
    parsed = json.loads(raw_value)
    if not isinstance(parsed, dict):
        raise ValueError("extra json must be an object.")
    return parsed


def first_non_empty(mapping, keys):
    for key in keys:
        value = mapping.get(key)
        if value not in ("", None):
            return value
    return None


def collect_media(payload):
    if not isinstance(payload, (dict, list)):
        return []

    field_groups = {
        "image": (
            "cover_url",
            "coverUrl",
            "preview_image_url",
            "previewImageUrl",
            "avatar_url",
            "avatarUrl",
            "image_url",
            "imageUrl",
            "poster_url",
            "posterUrl",
            "thumbnail_url",
            "thumbnailUrl",
            "thumb_url",
            "thumbUrl",
            "pic_url",
            "picUrl",
        ),
        "video": (
            "video_url",
            "videoUrl",
            "preview_url",
            "previewUrl",
            "play_url",
            "playUrl",
            "download_url",
            "downloadUrl",
            "url",
        ),
        "audio": (
            "audio_url",
            "audioUrl",
        ),
    }
    label_keys = ("name", "title", "video_title", "videoTitle", "person_name", "personName")
    id_keys = ("id", "video_id", "videoId", "person_id", "personId", "audio_id", "audioId", "task_id")
    entries = []
    seen = set()

    def visit(node):
        if len(entries) >= 20:
            return
        if isinstance(node, dict):
            label = first_non_empty(node, label_keys)
            identifier = first_non_empty(node, id_keys)
            for media_type, fields in field_groups.items():
                for field in fields:
                    value = node.get(field)
                    if not isinstance(value, str):
                        continue
                    url = value.strip()
                    if not url:
                        continue
                    dedupe_key = (media_type, url)
                    if dedupe_key in seen:
                        continue
                    seen.add(dedupe_key)
                    entry = {
                        "type": media_type,
                        "url": url,
                        "field": field,
                    }
                    if label not in ("", None):
                        entry["label"] = str(label)
                    if identifier not in ("", None):
                        entry["id"] = str(identifier)
                    entries.append(entry)
                    if len(entries) >= 20:
                        return
            for value in node.values():
                visit(value)
                if len(entries) >= 20:
                    return
            return
        if isinstance(node, list):
            for item in node:
                visit(item)
                if len(entries) >= 20:
                    return

    visit(payload)
    return entries


def with_media_summary(payload):
    if not isinstance(payload, dict):
        return payload
    if "_openclaw_media" in payload:
        return payload
    media = collect_media(payload)
    if not media:
        return payload
    enriched = dict(payload)
    enriched["_openclaw_media"] = media
    return enriched


def print_json(payload):
    sys.stdout.write(json.dumps(with_media_summary(payload), ensure_ascii=False, indent=2))
    sys.stdout.write("\n")


def task_status_value(task_payload):
    task = (task_payload or {}).get("task") or {}
    return str(task.get("status") or "").strip().lower()


def task_progress_value(task_payload):
    task = (task_payload or {}).get("task") or {}
    return task.get("progress")


def _task_payload_containers(task_payload):
    containers = []
    if not isinstance(task_payload, dict):
        return containers
    for key in ("task", "result_payload", "response_payload"):
        value = task_payload.get(key)
        if isinstance(value, dict):
            containers.append(value)
    return containers


def task_error_message(task_payload):
    error_keys = (
        "error_message",
        "errorMessage",
        "error_msg",
        "errorMsg",
        "fail_reason",
        "failReason",
        "err_reason",
        "errReason",
        "err_msg",
        "errMsg",
        "reason",
    )
    fallback_keys = ("msg", "message", "detail")
    fallback_message = None
    for container in _task_payload_containers(task_payload):
        for key in error_keys:
            value = container.get(key)
            if value not in (None, ""):
                return str(value)
        if fallback_message is None:
            for key in fallback_keys:
                value = container.get(key)
                if value not in (None, ""):
                    fallback_message = str(value)
                    break
    if fallback_message and fallback_message.strip().lower() not in {"success", "ok"}:
        return fallback_message
    return None


def _task_upstream_status(task_payload):
    status_keys = (
        "status",
        "process_status",
        "processStatus",
        "video_status",
        "videoStatus",
        "audit_status",
        "auditStatus",
    )
    for container in _task_payload_containers(task_payload):
        for key in status_keys:
            value = container.get(key)
            if value not in (None, ""):
                return value
    return None


def task_terminal_state(task_payload):
    status_value = task_status_value(task_payload)
    if status_value in {"success", "failed", "canceled"}:
        return status_value

    task = (task_payload or {}).get("task") or {}
    task_type = str(task.get("task_type") or "").strip().lower()
    raw_status = _task_upstream_status(task_payload)
    status_text = str(raw_status).strip().lower() if raw_status not in (None, "") else ""
    status_number = int(status_text) if status_text and status_text.lstrip("-").isdigit() else None
    error_message = task_error_message(task_payload)

    if task_type == "video_synthesis":
        if status_number in {30, 2}:
            return "success"
        if status_number in {4, 5} or (status_number is not None and 40 <= status_number < 60):
            return "failed"
    if task_type in {"custom_person", "custom_voice"}:
        if status_number == 2:
            return "success"
        if status_number in {4, 5}:
            return "failed"

    if error_message:
        return "failed"
    return None


def wait_for_task_completion(task_id, *, timeout_seconds, poll_interval_seconds=30):
    deadline = time.monotonic() + max(1, int(timeout_seconds))
    while True:
        task_payload = request_json("GET", f"/openclaw/tasks/{task_id}", query={"sync": "true"})
        status_value = task_terminal_state(task_payload) or task_status_value(task_payload)
        if status_value in {"success", "failed", "canceled"}:
            return {
                "finished": True,
                "timed_out": False,
                "task_payload": task_payload,
            }
        if time.monotonic() >= deadline:
            return {
                "finished": False,
                "timed_out": True,
                "task_payload": task_payload,
            }
        sys.stdout.write(
            json.dumps(
                {
                    "action": "wait_for_task_completion",
                    "task_id": task_id,
                    "status": status_value or "unknown",
                    "progress": task_progress_value(task_payload),
                },
                ensure_ascii=False,
            )
        )
        sys.stdout.write("\n")
        sys.stdout.flush()
        time.sleep(max(1, int(poll_interval_seconds)))
