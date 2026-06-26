"""Shared configuration helpers for paper2spec.

This module centralizes project-level environment loading and stable path
resolution so all scripts behave consistently across sessions.
"""

from __future__ import annotations

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"


def load_project_env() -> None:
    """Best-effort load of project `.env` file without overriding shell vars."""
    try:
        from dotenv import load_dotenv

        load_dotenv(ENV_PATH, override=False)
    except ImportError:
        # Keep working even when python-dotenv is unavailable.
        pass


def get_library_path(default: str = "./library") -> str:
    """Return library path from env, with a deterministic fallback.

    Priority:
      1) PAPER2SPEC_LIBRARY_PATH
      2) provided default
    """
    load_project_env()
    raw = os.getenv("PAPER2SPEC_LIBRARY_PATH", default).strip()
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    return str(path)


def get_init_status() -> dict[str, object]:
    """Return initialization status based on env marker + required capabilities."""
    load_project_env()

    marker = os.getenv("PAPER2SPEC_INIT_VERSION", "").strip()
    model = os.getenv("PAPER2SPEC_MODEL", "").strip()
    library = os.getenv("PAPER2SPEC_LIBRARY_PATH", "").strip()
    has_any_api_key = any(
        bool(os.getenv(k, "").strip())
        for k in ("DEEPSEEK_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY")
    )

    missing: list[str] = []
    if not marker:
        missing.append("PAPER2SPEC_INIT_VERSION")
    if not model:
        missing.append("PAPER2SPEC_MODEL")
    if not library:
        missing.append("PAPER2SPEC_LIBRARY_PATH")
    if not has_any_api_key:
        missing.append("{DEEPSEEK_API_KEY|OPENAI_API_KEY|ANTHROPIC_API_KEY}")

    return {
        "initialized": len(missing) == 0,
        "missing": missing,
        "init_version": marker,
        "library_path": get_library_path() if library else "",
    }