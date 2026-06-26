"""HTTP helpers for swagger-skills.

This module intentionally has a small dependency surface. It uses ``requests``
when available because generated API clients are meant to be easy to read and
modify.
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse


def validate_python_runtime() -> None:
    """Fail early on Python versions known to break common dependencies."""

    version = sys.version_info
    install_help = (
        "可选安装方式：\n"
        "1. Windows winget：winget install Python.Python.3.12\n"
        "2. uv：uv python install 3.12\n"
        "3. Python 官网下载页"
    )
    if version.releaselevel != "final":
        raise RuntimeError(
            "当前 Python 是预发布版本 "
            f"{version.major}.{version.minor}.{version.micro}-{version.releaselevel}，"
            "第三方依赖可能无法正常导入。请使用稳定版 Python 3.10 或更高版本，"
            "并建议在本地虚拟环境中运行。\n\n"
            + install_help
        )
    if version < (3, 10):
        raise RuntimeError(
            f"当前 Python 版本是 {version.major}.{version.minor}.{version.micro}。"
            "请使用稳定版 Python 3.10 或更高版本运行 swagger-skills。\n\n"
            + install_help
        )


def ensure_pip_available() -> None:
    """Ensure pip is available for the current interpreter."""

    if importlib.util.find_spec("pip") is not None:
        return
    print("当前 Python 环境缺少 pip，正在尝试启用 ensurepip。")
    try:
        subprocess.check_call([sys.executable, "-m", "ensurepip", "--upgrade"])
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            "当前 Python 环境缺少 pip，且 ensurepip 启用失败。"
            "请先创建本地虚拟环境，或安装带 pip 的稳定版 Python。"
        ) from exc


def ensure_requirements_installed(packages: dict[str, str] | None = None) -> None:
    """Install missing dependencies from the root requirements.txt."""

    validate_python_runtime()
    package_map = packages or {"requests": "requests"}
    missing = [
        requirement_name
        for import_name, requirement_name in package_map.items()
        if importlib.util.find_spec(import_name) is None
    ]
    if not missing:
        return

    ensure_pip_available()

    requirements_path = Path(__file__).resolve().parents[1] / "requirements.txt"
    if not requirements_path.exists():
        package_list = " ".join(missing)
        command = [sys.executable, "-m", "pip", "install", *missing]
        print(f"检测到依赖缺失，正在安装：{package_list}")
    else:
        command = [sys.executable, "-m", "pip", "install", "-r", str(requirements_path)]
        print(f"检测到依赖缺失，正在根据 {requirements_path} 安装依赖。")

    try:
        subprocess.check_call(command, env={**os.environ, "PIP_DISABLE_PIP_VERSION_CHECK": "1"})
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            "依赖自动安装失败。常见原因是全局 Python 环境被 PEP 668 管理、pip 不可用、"
            "网络不可达，或 Python 版本不受依赖支持。请在本地虚拟环境中安装依赖后重试。"
        ) from exc


validate_python_runtime()
ensure_requirements_installed({"requests": "requests"})

import requests


DEFAULT_DOC_AUTH = {
    "type": "basic",
    "username": "",
    "password": "",
}


def load_json(path: str | Path) -> dict[str, Any]:
    """Load a UTF-8 JSON object from disk."""

    with Path(path).open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise ValueError(f"JSON 文件必须是对象：{path}")
    return data


def save_json(path: str | Path, data: dict[str, Any]) -> None:
    """Write a UTF-8 JSON object to disk."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        file.write("\n")


def make_session(auth_config: dict[str, Any] | None = None) -> requests.Session:
    """Create a requests session with optional documentation authentication."""

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "swagger-skills/1.0",
            "Accept": "application/json, application/yaml, text/yaml, text/html, */*",
        }
    )

    auth = auth_config or {}
    if auth.get("type", "basic") == "basic" and auth.get("username"):
        session.auth = (auth.get("username", ""), auth.get("password", ""))

    return session


def fetch_text(
    url: str,
    auth_config: dict[str, Any] | None = None,
    timeout: int = 30,
) -> tuple[str, str]:
    """Fetch text content and return ``(text, final_url)``."""

    session = make_session(auth_config)
    response = session.get(url, timeout=timeout)
    response.raise_for_status()
    return response.text, response.url


def call_api(
    method: str,
    url: str,
    *,
    params: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    json_body: Any | None = None,
    data: Any | None = None,
    timeout: int = 30,
) -> requests.Response:
    """Call a generated business API endpoint."""

    response = requests.request(
        method=method.upper(),
        url=url,
        params=params,
        headers=headers,
        json=json_body,
        data=data,
        timeout=timeout,
    )
    response.raise_for_status()
    return response


def join_url(base_url: str, path: str) -> str:
    """Join a base URL and an API path without losing path prefixes."""

    if not base_url:
        return path

    parsed_base = urlparse(base_url)
    base_path = parsed_base.path.strip("/")
    request_path = path.lstrip("/")
    # Some Swagger specs include the service prefix in both server/basePath and paths.
    # Avoid generating /service/service/... when joining those values.
    if base_path and request_path == base_path:
        request_path = ""
    elif base_path and request_path.startswith(base_path + "/"):
        request_path = request_path[len(base_path) + 1 :]

    return urljoin(base_url.rstrip("/") + "/", request_path)


def load_domain_config(config_path: str | Path) -> dict[str, Any]:
    """Load ``config/domains.json`` for generated clients."""

    return load_json(config_path)


def resolve_base_url(domain_config: dict[str, Any], document_id: str) -> str:
    """Resolve a document's base URL from ``domains.json``."""

    documents = domain_config.get("documents", {})
    document = documents.get(document_id)
    if not document:
        raise KeyError(f"domains.json 中不存在文档配置：{document_id}")
    base_url = document.get("base_url") or document.get("servers", [{}])[0].get("url")
    if not base_url:
        raise KeyError(f"文档配置缺少 base_url：{document_id}")
    return str(base_url)
