"""Load and merge .linting-rules.yml configuration."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG_NAMES = [".linting-rules.yml", ".linting-rules.yaml", "linting-rules.yml"]

_DEFAULTS: dict[str, Any] = {
    "pylint": {
        "enabled": True,
        "min_score": 7.0,
        "disable": [],
        "enable": [],
        "max_line_length": 120,
    },
    "hardcoded_secrets": {
        "enabled": True,
        "skip_ip_check": False,
    },
    "fastapi_docstring": {
        "enabled": True,
        "severity": "warning",
    },
    "react_useeffect_deps": {
        "enabled": True,
        "severity": "warning",
    },
    "output": {
        "format": "markdown",
        "include_info": True,
    },
    "github": {
        "post_comment": True,
        "fail_on_error": True,
        "fail_on_warning": False,
    },
    "github_actions": {
        "polling_interval": 30,
        "max_timeout": 1800,
        "retry_attempts": 3,
    },
    "notifications": {
        "enabled": False,
        "channels": [],
    },
}


def _deep_merge(base: dict, override: dict) -> dict:
    result = dict(base)
    for key, val in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(val, dict):
            result[key] = _deep_merge(result[key], val)
        else:
            result[key] = val
    return result


def load_config(config_path: str | None = None, search_dir: str | None = None) -> dict[str, Any]:
    """Load config from file, falling back to defaults."""
    if config_path:
        path = Path(config_path)
    else:
        search_root = Path(search_dir) if search_dir else Path.cwd()
        path = None
        for name in DEFAULT_CONFIG_NAMES:
            candidate = search_root / name
            if candidate.exists():
                path = candidate
                break

    if path and path.exists():
        with open(path) as f:
            user_config = yaml.safe_load(f) or {}
        return _deep_merge(_DEFAULTS, user_config)

    return dict(_DEFAULTS)
