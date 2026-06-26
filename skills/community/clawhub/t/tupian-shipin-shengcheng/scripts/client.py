#!/usr/bin/env python3
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
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


def _env_first(*names):
    for name in names:
        value = os.environ.get(name, "").strip()
        if value:
            return value
    return ""


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


def _configured_value(config_key, *env_names):
    value = str(_CLIENT_CONFIG.get(config_key, "") or "").strip()
    if value:
        return value
    return _env_first(*env_names)


def api_base():
    base_url = _configured_value("base_url", "EASYCLAW_PLATFORM_BASE_URL", "CHANJING_PLATFORM_BASE_URL") or DEFAULT_PLATFORM_BASE_URL
    base_url = base_url.rstrip("/")
    if base_url.endswith("/api"):
        return base_url
    return f"{base_url}/api"


def default_headers(content_type=None):
    platform_token = _configured_value("api_token", "EASYCLAW_PLATFORM_API_TOKEN", "CHANJING_PLATFORM_API_TOKEN")
    if platform_token:
        headers = {"X-API-Token": platform_token}
    else:
        api_key = _configured_value("api_key", "EASYCLAW_PLATFORM_API_KEY", "CHANJING_PLATFORM_API_KEY")
        api_secret = _configured_value("api_secret", "EASYCLAW_PLATFORM_API_SECRET", "CHANJING_PLATFORM_API_SECRET")
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
        for key in ("detail", "message", "msg", "error"):
            value = payload.get(key)
            if value not in (None, ""):
                return str(value)
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


def build_multipart_body(fields=None, file_fields=None):
    boundary = f"----easyclaw-{uuid4().hex}"
    boundary_bytes = boundary.encode("ascii")
    body = bytearray()

    for name, value in fields or []:
        body.extend(b"--" + boundary_bytes + b"\r\n")
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"))
        body.extend(str(value).encode("utf-8"))
        body.extend(b"\r\n")

    for name, file_path in file_fields or []:
        with open(file_path, "rb") as handle:
            content = handle.read()
        filename = os.path.basename(file_path)
        mime_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        body.extend(b"--" + boundary_bytes + b"\r\n")
        body.extend(
            f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'.encode("utf-8")
        )
        body.extend(f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"))
        body.extend(content)
        body.extend(b"\r\n")

    body.extend(b"--" + boundary_bytes + b"--\r\n")
    return bytes(body), f"multipart/form-data; boundary={boundary}"


def request_multipart(method, path, *, query=None, fields=None, file_fields=None):
    body, content_type = build_multipart_body(fields=fields, file_fields=file_fields)
    headers = default_headers(content_type=content_type)
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


def print_json(payload):
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2))
    sys.stdout.write("\n")


def parse_payload_args(payload_json=None, payload_file=None):
    if payload_json and payload_file:
        raise ValueError("Provide only one of --payload-json or --payload-file.")
    if payload_json:
        parsed = json.loads(payload_json)
    elif payload_file:
        with open(payload_file, "r", encoding="utf-8") as handle:
            parsed = json.load(handle)
    else:
        raise ValueError("One of --payload-json or --payload-file is required.")
    if not isinstance(parsed, dict):
        raise ValueError("Payload must be a JSON object.")
    return parsed


def parse_name_value_args(items, *, label):
    parsed = []
    for raw_item in items or []:
        if "=" not in raw_item:
            raise ValueError(f"{label} must use name=value format: {raw_item}")
        name, value = raw_item.split("=", 1)
        name = name.strip()
        value = value.strip()
        if not name:
            raise ValueError(f"{label} name cannot be empty: {raw_item}")
        if not value:
            raise ValueError(f"{label} value cannot be empty: {raw_item}")
        parsed.append((name, value))
    return parsed


def first_non_empty(mapping, keys):
    if not isinstance(mapping, dict):
        return None
    for key in keys:
        value = mapping.get(key)
        if value not in ("", None):
            return value
    return None


def extract_task_id(payload):
    if not isinstance(payload, dict):
        return None
    data = payload.get("data")
    for container in (payload, data if isinstance(data, dict) else None):
        if not isinstance(container, dict):
            continue
        value = first_non_empty(container, ("request_id", "requestId", "task_id", "taskId", "id"))
        if value not in ("", None):
            return str(value)
    return None


def terminal_status(payload):
    if not isinstance(payload, dict):
        return None
    data = payload.get("data") if isinstance(payload.get("data"), dict) else None
    for container in (payload, data):
        if not isinstance(container, dict):
            continue
        raw_status = first_non_empty(container, ("status", "state", "task_status", "taskStatus"))
        if raw_status in (None, ""):
            continue
        status_text = str(raw_status).strip().lower()
        if status_text in {"completed", "complete", "success", "succeeded", "done", "finished"}:
            return "success"
        if status_text in {"failed", "error", "canceled", "cancelled"}:
            return "failed"
        if status_text in {"pending", "queued", "running", "processing", "submitted", "created"}:
            return "running"
    return None


def wait_for_task(task_id, *, timeout_seconds=1800, poll_interval_seconds=30):
    deadline = time.monotonic() + max(1, int(timeout_seconds))
    while True:
        payload = request_json("GET", f"/veo2/custom_video/fetch/{task_id}")
        status = terminal_status(payload)
        if status in {"success", "failed"}:
            return {
                "finished": True,
                "timed_out": False,
                "status": status,
                "payload": payload,
            }
        if time.monotonic() >= deadline:
            return {
                "finished": False,
                "timed_out": True,
                "status": status or "running",
                "payload": payload,
            }
        sys.stdout.write(
            json.dumps(
                {
                    "action": "wait_for_task",
                    "task_id": task_id,
                    "status": status or "running",
                },
                ensure_ascii=False,
            )
        )
        sys.stdout.write("\n")
        sys.stdout.flush()
        time.sleep(max(1, int(poll_interval_seconds)))
