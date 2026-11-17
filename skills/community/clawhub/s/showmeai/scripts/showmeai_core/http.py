"""HTTP transport with authentication, retries, and redacted errors."""

from __future__ import annotations

import json
import random
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any

from .errors import HttpError, SkillError


TRANSIENT_STATUS = {408, 425, 429, 500, 502, 503, 504}


def task_base_url(base_url: str) -> str:
    value = base_url.rstrip("/")
    return value[:-3] if value.endswith("/v1") else value


def encode_multipart(fields: dict[str, Any], files: list[tuple[str, Path]]) -> tuple[bytes, str]:
    boundary = f"----ShowMeAI{uuid.uuid4().hex}"
    parts: list[bytes] = []
    for name, value in fields.items():
        if value is None or value == "":
            continue
        text = str(value).lower() if isinstance(value, bool) else str(value)
        parts.append(
            (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'
                f"{text}\r\n"
            ).encode("utf-8")
        )
    for name, path in files:
        suffix = path.suffix.lower()
        content_type = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp",
        }.get(suffix, "application/octet-stream")
        parts.append(
            (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="{name}"; filename="{path.name}"\r\n'
                f"Content-Type: {content_type}\r\n\r\n"
            ).encode("utf-8")
            + path.read_bytes()
            + b"\r\n"
        )
    parts.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


class ApiClient:
    def __init__(self, base_url: str, api_key: str, retries: int = 5, sleep_fn=time.sleep) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.retries = retries
        self.sleep_fn = sleep_fn

    def api_url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def task_url(self, path: str) -> str:
        return f"{task_base_url(self.base_url)}/{path.lstrip('/')}"

    def request(
        self,
        method: str,
        url: str,
        *,
        body: bytes | None = None,
        content_type: str = "application/json",
        timeout: int = 300,
    ) -> tuple[bytes, dict[str, str]]:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        if body is not None:
            headers["Content-Type"] = content_type
        last_error: Exception | None = None
        for attempt in range(self.retries + 1):
            request = urllib.request.Request(url, method=method, headers=headers, data=body)
            try:
                with urllib.request.urlopen(request, timeout=timeout) as response:
                    return response.read(), dict(response.headers.items())
            except urllib.error.HTTPError as error:
                response_body = error.read().decode("utf-8", errors="replace")
                if self.api_key:
                    response_body = response_body.replace(self.api_key, "***REDACTED***")
                retryable = error.code in TRANSIENT_STATUS
                if not retryable or attempt >= self.retries:
                    raise HttpError(error.code, f"ShowMeAI request failed with HTTP {error.code}.", body=response_body, retryable=retryable) from error
                retry_after = error.headers.get("Retry-After", "") if error.headers else ""
                delay = float(retry_after) if retry_after.replace(".", "", 1).isdigit() else min(30.0, 1.5 * (2**attempt))
                self.sleep_fn(delay + random.uniform(0, min(1.0, delay * 0.1)))
                last_error = error
            except (urllib.error.URLError, TimeoutError) as error:
                if attempt >= self.retries:
                    raise SkillError("NETWORK_ERROR", f"ShowMeAI network request failed: {error}", retryable=True) from error
                self.sleep_fn(min(30.0, 1.5 * (2**attempt)) + random.uniform(0, 0.5))
                last_error = error
        raise SkillError("NETWORK_ERROR", f"ShowMeAI network request failed: {last_error}", retryable=True)

    def request_json(self, method: str, url: str, payload: Any | None = None, timeout: int = 300) -> dict[str, Any]:
        body = json.dumps(payload).encode("utf-8") if payload is not None else None
        raw, _headers = self.request(method, url, body=body, timeout=timeout)
        try:
            result = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise SkillError("RESPONSE_INVALID", "ShowMeAI returned non-JSON data for a JSON endpoint.") from error
        if not isinstance(result, dict):
            raise SkillError("RESPONSE_INVALID", "ShowMeAI JSON response must be an object.")
        return result

    def request_multipart(self, url: str, fields: dict[str, Any], files: list[tuple[str, Path]]) -> dict[str, Any]:
        body, content_type = encode_multipart(fields, files)
        raw, _headers = self.request("POST", url, body=body, content_type=content_type, timeout=300)
        try:
            result = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise SkillError("RESPONSE_INVALID", "ShowMeAI returned non-JSON multipart response.") from error
        if not isinstance(result, dict):
            raise SkillError("RESPONSE_INVALID", "ShowMeAI response must be an object.")
        return result

    def models(self) -> dict[str, Any]:
        return self.request_json("GET", self.api_url("models"), timeout=60)
