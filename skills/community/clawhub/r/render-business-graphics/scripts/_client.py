#!/usr/bin/env python3
"""Small standard-library HTTP client shared by the render skill scripts."""

from __future__ import annotations

import base64
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_BASE_URL = "https://chart.cqccjy.cn"
DEFAULT_TIMEOUT = 15.0


class ChartRenderHttpError(RuntimeError):
    """Raised when the render service cannot complete an HTTP request."""

    def __init__(self, message: str, *, status: int | None = None, details: Any = None) -> None:
        super().__init__(message)
        self.status = status
        self.details = details


def service_options(base_url: str | None, api_key: str | None, timeout: float | None) -> tuple[str, str, float]:
    resolved_url = (base_url or os.environ.get("CHART_RENDER_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
    resolved_key = api_key if api_key is not None else os.environ.get("CHART_RENDER_API_KEY", "")
    resolved_timeout = timeout if timeout is not None else float(
        os.environ.get("CHART_RENDER_HTTP_TIMEOUT_SECONDS", DEFAULT_TIMEOUT)
    )
    if resolved_timeout <= 0:
        raise ValueError("timeout must be greater than 0")
    return resolved_url, resolved_key, resolved_timeout


def request_bytes(
    base_url: str,
    path: str,
    *,
    method: str = "GET",
    body: bytes | None = None,
    api_key: str = "",
    timeout: float = DEFAULT_TIMEOUT,
    content_type: str | None = None,
) -> tuple[bytes, Any]:
    headers = {"Accept": "application/json"}
    if api_key:
        headers["X-API-Key"] = api_key
    if content_type:
        headers["Content-Type"] = content_type
    target_url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
    request = urllib.request.Request(
        target_url,
        data=body,
        headers=headers,
        method=method,
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read(), response.headers
    except urllib.error.HTTPError as error:
        raw_details = error.read()
        details: Any = raw_details.decode("utf-8", errors="replace")
        try:
            details = json.loads(details)
        except json.JSONDecodeError:
            pass
        message = details.get("message") if isinstance(details, dict) else None
        raise ChartRenderHttpError(
            str(message or f"chart render service returned HTTP {error.code}"),
            status=error.code,
            details=details,
        ) from error
    except urllib.error.URLError as error:
        raise ChartRenderHttpError(f"unable to reach chart render service at {target_url}: {error.reason}") from error


def request_json(
    base_url: str,
    path: str,
    *,
    api_key: str = "",
    timeout: float = DEFAULT_TIMEOUT,
) -> Any:
    raw, _headers = request_bytes(base_url, path, api_key=api_key, timeout=timeout)
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ChartRenderHttpError(f"service returned invalid JSON from {path}") from error


def read_json_input(path: str) -> Any:
    raw = __import__("sys").stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as error:
        source = "stdin" if path == "-" else path
        raise ValueError(f"invalid JSON in {source}: {error}") from error


def write_json(value: Any, output: str | None, *, indent: int = 2) -> None:
    rendered = json.dumps(value, ensure_ascii=False, indent=indent) + "\n"
    if output:
        target = Path(output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


def decode_data_url(data_url: str) -> tuple[str, bytes]:
    match = re.fullmatch(r"data:([^;,]+)(;base64)?,(.*)", data_url, flags=re.DOTALL)
    if not match:
        raise ValueError("catalog image is not a supported data URL")
    media_type, encoded, payload = match.groups()
    data = base64.b64decode(payload) if encoded else urllib.parse.unquote_to_bytes(payload)
    return media_type, data


def safe_filename(value: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip(".-")
    return normalized or "graphic"


def header_value(headers: Any, name: str) -> str | None:
    value = headers.get(name)
    return str(value) if value is not None else None
