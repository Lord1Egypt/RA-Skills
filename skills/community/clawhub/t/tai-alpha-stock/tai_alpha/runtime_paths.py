"""Project root, default output directory, and SQLite DB path helpers."""

from __future__ import annotations

import os
from pathlib import Path

_ENV_OUTPUT_DIR = "TAI_ALPHA_OUTPUT_DIR"
_DEFAULT_OUTPUT_SUBDIR = "tai_alpha_output"


def find_project_root(start: Path | None = None) -> Path:
    """
    Walk upward from ``start`` (or this package's parent) for ``pyproject.toml``
    that declares this project (``tai-alpha-stock``).
    """
    here = (start or Path(__file__).resolve().parent.parent).resolve()
    for p in [here, *here.parents]:
        candidate = p / "pyproject.toml"
        if not candidate.is_file():
            continue
        try:
            text = candidate.read_text(encoding="utf-8")
        except OSError:
            continue
        if 'name = "tai-alpha-stock"' in text or "name = 'tai-alpha-stock'" in text:
            return p
    return Path(__file__).resolve().parent.parent


def default_output_dir(project_root: Path | None = None) -> Path:
    """
    Directory for generated artifacts (default SQLite DB lives here as
    ``tai_alpha.db`` unless ``TAI_ALPHA_DB_PATH`` is set — see
    ``tai_alpha.storage_sqlite.default_db_path``).

    Override with env ``TAI_ALPHA_OUTPUT_DIR`` (absolute or relative path).
    Default: ``<project_root>/tai_alpha_output``.
    """
    env = os.environ.get(_ENV_OUTPUT_DIR)
    if env:
        return Path(env).expanduser().resolve()
    root = project_root or find_project_root()
    return (root / _DEFAULT_OUTPUT_SUBDIR).resolve()


def ensure_output_dir(path: Path | None = None) -> Path:
    """Create the output directory if missing; return resolved path."""
    d = path if path is not None else default_output_dir()
    d.mkdir(parents=True, exist_ok=True)
    return d.resolve()
