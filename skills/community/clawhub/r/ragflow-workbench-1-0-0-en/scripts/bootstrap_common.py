#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

# Reuse shared utilities where possible
from common import (
    HTTP_TIMEOUT,
    configure_stdio_utf8,
    decode_json_body,
    decode_response_text,
)


class BootstrapError(Exception):
    pass


def default_env_file() -> Path:
    return Path(__file__).resolve().parent.parent / ".env"


def read_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def write_env_file(path: Path, updates: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_env_file(path)
    existing.update({key: value for key, value in updates.items() if value is not None})
    lines = [f"{key}={value}" for key, value in sorted(existing.items())]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def http_json(
    base_url: str,
    path: str,
    *,
    method: str = "GET",
    body: dict[str, Any] | None = None,
    token: str | None = None,
) -> tuple[int, dict[str, Any] | None, dict[str, str], str]:
    """Low-level HTTP request for bootstrap flows.
    Returns (status, parsed_payload_or_None, headers_dict, raw_body_text).
    Unlike common.request_json, this does NOT raise on HTTP errors,
    allowing bootstrap scripts to inspect status codes directly.
    """
    url = f"{base_url.rstrip('/')}{path}"
    data = None
    headers: dict[str, str] = {"Accept": "application/json"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = token if token.startswith("Bearer ") else f"Bearer {token}"

    request_obj = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request_obj, timeout=HTTP_TIMEOUT) as response:
            text = response.read().decode("utf-8", errors="replace")
            payload = _try_json(text)
            return response.status, payload, dict(response.headers.items()), text
    except urllib.error.HTTPError as exc:
        text = exc.read().decode("utf-8", errors="replace")
        payload = _try_json(text)
        return exc.code, payload, dict(exc.headers.items()) if exc.headers else {}, text
    except urllib.error.URLError as exc:
        raise BootstrapError(f"请求失败: {exc.reason}") from None


def _try_json(text: str) -> dict[str, Any] | None:
    """Parse JSON only if it's a dict; returns None otherwise."""
    return decode_json_body(text.encode("utf-8")) if text else None


def extract_token(headers: dict[str, str], payload: dict[str, Any] | None) -> str | None:
    auth = headers.get("Authorization") or headers.get("authorization")
    if isinstance(auth, str) and auth.strip():
        token = auth.strip()
        return token if token.startswith("Bearer ") else f"Bearer {token}"

    if isinstance(payload, dict):
        data = payload.get("data")
        if isinstance(data, dict):
            token = data.get("token")
            if isinstance(token, str) and token.strip():
                token = token.strip()
                return token if token.startswith("Bearer ") else f"Bearer {token}"
    return None


def encrypt_password_via_docker(container_name: str, password: str) -> str:
    cmd = [
        "docker",
        "exec",
        container_name,
        "python3",
        "-c",
        (
            "import sys; sys.path.insert(0,'/ragflow'); "
            "from api.utils.crypt import crypt; print(crypt(%r))" % password
        ),
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    except OSError as exc:
        raise BootstrapError(f"无法执行 docker 命令: {exc}") from None

    encrypted = (result.stdout or "").strip()
    if result.returncode != 0 or not encrypted:
        err = (result.stderr or "").strip() or "未知错误"
        raise BootstrapError(
            f"通过容器加密密码失败，请确认容器名正确且服务已启动。stderr={err}"
        )
    return encrypted


def register_user(base_url: str, nickname: str, email: str, encrypted_password: str) -> dict[str, Any]:
    status, payload, _, text = http_json(
        base_url,
        "/v1/user/register",
        method="POST",
        body={"nickname": nickname, "email": email, "password": encrypted_password},
    )
    return {"status": status, "payload": payload, "raw": text}


def login_user(base_url: str, email: str, encrypted_password: str) -> str:
    status, payload, headers, text = http_json(
        base_url,
        "/v1/user/login",
        method="POST",
        body={"email": email, "password": encrypted_password},
    )
    if status != 200:
        raise BootstrapError(f"登录失败: HTTP {status}, body={text}")

    token = extract_token(headers, payload)
    if not token:
        raise BootstrapError("登录成功但未返回 Authorization/JWT。")
    return token


def get_or_create_api_token(base_url: str, jwt_token: str, token_name: str) -> str:
    status, payload, _, text = http_json(base_url, "/api/v1/system/tokens", token=jwt_token)
    if status != 200:
        raise BootstrapError(f"获取 API Token 列表失败: HTTP {status}, body={text}")

    if isinstance(payload, dict):
        data = payload.get("data")
        if isinstance(data, list):
            for item in data:
                if not isinstance(item, dict):
                    continue
                if item.get("name") == token_name and isinstance(item.get("token"), str):
                    token = item["token"].strip()
                    if token:
                        return token

    create_path = f"/api/v1/system/tokens?{urllib.parse.urlencode({'name': token_name})}"
    status, payload, _, text = http_json(base_url, create_path, method="POST", token=jwt_token)
    if status != 200:
        raise BootstrapError(f"创建 API Token 失败: HTTP {status}, body={text}")
    if not isinstance(payload, dict):
        raise BootstrapError("创建 API Token 响应格式异常。")

    data = payload.get("data")
    if not isinstance(data, dict) or not isinstance(data.get("token"), str) or not data.get("token").strip():
        raise BootstrapError(f"创建 API Token 响应缺少 token: {text}")
    return data["token"].strip()
