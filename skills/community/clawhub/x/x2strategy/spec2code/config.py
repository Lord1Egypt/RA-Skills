"""Shared configuration for spec2code.

Reuses the same .env / library path as paper2spec so both halves of
the pipeline share a single configuration surface.
"""

from __future__ import annotations

import os
from pathlib import Path

# Import shared config from paper2spec
from paper2spec.config import load_project_env, get_library_path, PROJECT_ROOT


def get_backtest_timeout() -> int:
    """Max seconds for a single backtest execution."""
    load_project_env()
    return int(os.getenv("SPEC2CODE_BACKTEST_TIMEOUT", "300"))


def get_data_cache_dir() -> str:
    """Directory for caching downloaded market data."""
    load_project_env()
    raw = os.getenv("SPEC2CODE_DATA_CACHE", str(PROJECT_ROOT / "data_cache"))
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    path.mkdir(parents=True, exist_ok=True)
    return str(path)
