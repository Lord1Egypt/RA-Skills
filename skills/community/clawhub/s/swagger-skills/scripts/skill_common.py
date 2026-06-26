"""Generated skill domain and config helpers.

This module is copied or regenerated into each business skill output.
All API clients resolve base URLs through this module — do not hardcode domains.
"""

from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

_DOMAIN_CONFIG_CACHE: dict[str, dict[str, Any]] = {}


def find_skill_root(start: Path | None = None) -> Path:
    """Locate skill root by walking up to config/domains.json."""

    start = start or Path(__file__).resolve()
    for parent in [start, *start.parents]:
        if (parent / "config" / "domains.json").exists():
            return parent
    raise RuntimeError("未找到 config/domains.json，请确认当前文件位于生成的 skill 目录内。")


def load_domain_config(config_path: str | Path | None = None) -> dict[str, Any]:
    """Load and cache config/domains.json."""

    path = Path(config_path) if config_path else find_skill_root() / "config" / "domains.json"
    key = str(path.resolve())
    if key in _DOMAIN_CONFIG_CACHE:
        return _DOMAIN_CONFIG_CACHE[key]
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise ValueError(f"domains.json 必须是 JSON 对象：{path}")
    _DOMAIN_CONFIG_CACHE[key] = data
    return data


def _document_config(domain_config: dict[str, Any], document_id: str) -> dict[str, Any]:
    documents = domain_config.get("documents", {})
    document = documents.get(document_id)
    if not document:
        raise KeyError(f"domains.json 中不存在文档配置：{document_id}")
    return document


def resolve_base_url(document_id: str, *, config_path: str | Path | None = None) -> str:
    """Resolve API base URL: env override → base_url → servers[0].url."""

    domain_config = load_domain_config(config_path)
    document = _document_config(domain_config, document_id)
    env_key = document.get("env_key")
    if env_key:
        override = os.environ.get(str(env_key), "").strip()
        if override:
            return override.rstrip("/")
    base_url = document.get("base_url") or document.get("servers", [{}])[0].get("url")
    if not base_url:
        raise KeyError(f"文档配置缺少 base_url：{document_id}")
    return str(base_url).rstrip("/")


def join_url(base_url: str, path: str) -> str:
    """Join base URL and API path without duplicating service prefixes."""

    if not base_url:
        return path

    parsed_base = urlparse(base_url)
    base_path = parsed_base.path.strip("/")
    request_path = path.lstrip("/")
    if base_path and request_path == base_path:
        request_path = ""
    elif base_path and request_path.startswith(base_path + "/"):
        request_path = request_path[len(base_path) + 1 :]

    return urljoin(base_url.rstrip("/") + "/", request_path)


def apply_path_params(path_template: str, path_params: dict[str, Any] | None) -> str:
    """Replace {param} placeholders in a path template."""

    path = path_template
    for key, value in (path_params or {}).items():
        path = path.replace("{" + key + "}", str(value))
    return path


def join_api_url(
    document_id: str,
    path_template: str,
    path_params: dict[str, Any] | None = None,
    *,
    config_path: str | Path | None = None,
) -> str:
    """Build full request URL for one document and path template."""

    base_url = resolve_base_url(document_id, config_path=config_path)
    path = apply_path_params(path_template, path_params)
    return join_url(base_url, path)


def get_field_mapping_enabled(*, config_path: str | Path | None = None) -> bool:
    """Return whether response field key mapping is enabled (default True)."""

    domain_config = load_domain_config(config_path)
    field_mapping = domain_config.get("field_mapping")
    if isinstance(field_mapping, dict) and "enabled" in field_mapping:
        return bool(field_mapping["enabled"])
    return True


def get_default_timeout(*, config_path: str | Path | None = None) -> int:
    """Return default HTTP timeout from domains.json defaults."""

    domain_config = load_domain_config(config_path)
    defaults = domain_config.get("defaults", {})
    if isinstance(defaults, dict):
        timeout = defaults.get("timeout")
        if timeout is not None:
            return int(timeout)
    return 30


def skill_root() -> Path:
    """Return cached skill root path."""

    return find_skill_root(Path(__file__).resolve())


@lru_cache(maxsize=1)
def field_index_path() -> Path:
    """Return path to openapi_field_index.json at skill root."""

    return skill_root() / "openapi_field_index.json"
