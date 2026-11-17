#!/usr/bin/env python3
"""smart-message-plus: HTTP helper (stdlib only, explicit timeout, error normalization)."""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
import uuid


class HttpError(Exception):
    def __init__(self, status: int, body: str, url: str = ""):
        self.status = status
        self.body = body
        self.url = url
        super().__init__(f"HTTP {status}: {body[:200]}")


def request(
    url: str,
    body=None,
    headers: dict | None = None,
    method: str | None = None,
    timeout: int = 15,
    retries: int = 1,
    retry_backoff: float = 1.5,
    raw_body: bytes | None = None,
) -> tuple[int, dict]:
    """JSON in / JSON out. Returns (status, parsed_json). Retries on 429/5xx/network error."""
    hdrs = {"Content-Type": "application/json", **(headers or {})}
    data = raw_body if raw_body is not None else (
        json.dumps(body).encode("utf-8") if body is not None else None
    )
    last_err: Exception | None = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                text = resp.read().decode("utf-8", "replace")
                return resp.status, _parse(text)
        except urllib.error.HTTPError as e:
            text = ""
            try:
                text = e.read().decode("utf-8", "replace")
            except OSError:
                pass
            if e.code in (429, 500, 502, 503, 504) and attempt < retries:
                time.sleep(retry_backoff * (attempt + 1))
                last_err = HttpError(e.code, text, url)
                continue
            return e.code, _parse(text)
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            last_err = e
            if attempt < retries:
                time.sleep(retry_backoff * (attempt + 1))
                continue
            raise HttpError(0, f"network error: {e}", url) from e
    raise HttpError(0, f"exhausted retries: {last_err}", url)


def _parse(text: str) -> dict:
    if not text:
        return {}
    try:
        obj = json.loads(text)
        return obj if isinstance(obj, dict) else {"_raw": obj}
    except json.JSONDecodeError:
        return {"_raw": text}


def multipart_upload(
    url: str,
    fields: dict,
    file_field: str,
    file_name: str,
    file_bytes: bytes,
    file_mime: str,
    headers: dict | None = None,
    timeout: int = 60,
) -> tuple[int, dict]:
    """Multipart/form-data upload via stdlib."""
    boundary = uuid.uuid4().hex
    parts = []
    for k, v in fields.items():
        parts.append(
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
        )
    parts.append(
        (
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"{file_field}\"; "
            f"filename=\"{file_name}\"\r\nContent-Type: {file_mime}\r\n\r\n"
        ).encode()
        + file_bytes
        + b"\r\n"
    )
    parts.append(f"--{boundary}--\r\n".encode())
    body = b"".join(parts)
    hdrs = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        **(headers or {}),
    }
    return request(url, headers=hdrs, timeout=timeout, raw_body=body)
