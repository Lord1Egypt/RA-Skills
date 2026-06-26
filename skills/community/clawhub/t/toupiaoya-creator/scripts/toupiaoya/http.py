from __future__ import annotations

from typing import Any, Mapping, MutableMapping

import requests

from toupiaoya.constants import DEFAULT_TIMEOUT


def get(
    url: str,
    *,
    access_token: str | None = None,
    params: Mapping[str, Any] | None = None,
    extra_headers: MutableMapping[str, str] | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> requests.Response:
    headers: dict[str, str] = dict(extra_headers or {})
    if access_token:
        headers["X-Openclaw-Token"] = access_token
    return requests.get(url, params=dict(params) if params else None, headers=headers or None, timeout=timeout)


def post_json(
    url: str,
    json_body: Mapping[str, Any],
    *,
    access_token: str | None = None,
    extra_headers: MutableMapping[str, str] | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> requests.Response:
    """创建类 JSON POST；仅在有 token 时附加 X-Openclaw-Token（与 requests 自带 json= Content-Type 一致）。"""
    headers: dict[str, str] = dict(extra_headers or {})
    if access_token:
        headers["X-Openclaw-Token"] = access_token
    return requests.post(url, json=dict(json_body), headers=headers or None, timeout=timeout)


def post_multipart(
    url: str,
    *,
    files: Any,
    data: Mapping[str, Any] | None = None,
    access_token: str | None = None,
    extra_headers: MutableMapping[str, str] | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> requests.Response:
    """文件上传等多部分表单；不要设置 Content-Type，由 requests 自动带 boundary。"""
    headers: dict[str, str] = dict(extra_headers or {})
    if access_token:
        headers["X-Openclaw-Token"] = access_token
    return requests.post(url, files=files, data=data, headers=headers or None, timeout=timeout)
