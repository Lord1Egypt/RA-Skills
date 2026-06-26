#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Callable


class SkillHttpError(RuntimeError):
    """Readable HTTP/JSON error for command-line skill scripts."""


def make_debug_logger(component: str) -> Callable[[bool, str], None]:
    def debug_log(enabled: bool, message: str) -> None:
        if enabled:
            print(f"DEBUG {component}: {message}", file=sys.stderr)

    return debug_log


def build_url(base_url: str, path: str, query: dict[str, Any] | None = None) -> str:
    url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
    if not query:
        return url

    filtered_query = {
        key: value
        for key, value in query.items()
        if value is not None and str(value).strip()
    }
    if not filtered_query:
        return url

    return f"{url}?{urllib.parse.urlencode(filtered_query)}"


def fetch_json(url: str, timeout: int) -> dict:
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json"},
        method="GET",
    )
    return request_json(request, timeout)


def post_json(url: str, timeout: int, payload: dict) -> dict:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        method="POST",
    )
    return request_json(request, timeout)


def request_json(request: urllib.request.Request, timeout: int) -> dict:
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
            if not isinstance(payload, dict):
                raise SkillHttpError("服务返回格式不是 JSON 对象")
            return payload
    except urllib.error.HTTPError as exc:
        raise SkillHttpError(f"服务暂时返回 HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise SkillHttpError(f"网络请求失败：{exc.reason}") from exc
    except TimeoutError as exc:
        raise SkillHttpError("网络请求超时") from exc
    except OSError as exc:
        raise SkillHttpError(f"网络请求失败：{exc}") from exc
    except json.JSONDecodeError as exc:
        raise SkillHttpError("服务返回了无法解析的 JSON") from exc
    except Exception as exc:
        if isinstance(exc, SkillHttpError):
            raise
        raise SkillHttpError(f"请求处理失败：{exc}") from exc
