#!/usr/bin/env python3
"""Call yanleaf.com public SQL→ER parse API."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

DEFAULT_API = "https://yanleaf.com/api/tools/er-diagram/parse"
TIMEOUT = 30


def parse_sql_via_api(sql: str, api_url: str = DEFAULT_API) -> list[dict[str, Any]]:
    """
    POST {sql} to yanleaf parse API.
    Returns list-of-tables on success.
    Raises RuntimeError with a clear message on failure / rate limit.
    """
    if not sql or not sql.strip():
        raise ValueError("SQL content is empty")

    body = json.dumps({"sql": sql}).encode("utf-8")
    req = urllib.request.Request(
        api_url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "er-diagram-skill/1.0 (+https://yanleaf.com)",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode("utf-8")
            data = json.loads(err_body)
            msg = data.get("message") or err_body
        except Exception:
            msg = str(e)
        if e.code == 429:
            raise RuntimeError(f"接口限流（429）: {msg}") from e
        raise RuntimeError(f"API HTTP {e.code}: {msg}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"无法连接 yanleaf API: {e.reason}") from e

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"API 返回非 JSON: {raw[:200]}") from e

    code = payload.get("code")
    if code != 200:
        raise RuntimeError(payload.get("message") or f"API error code={code}")

    data = payload.get("data")
    if not isinstance(data, list):
        raise RuntimeError("API data 字段不是表数组")
    return data
