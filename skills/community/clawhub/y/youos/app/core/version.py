"""Single source of truth for the YouOS version.

Several places had hardcoded version strings that drifted (settings default,
/api/config, the UI footers). This resolves the version once. YouOS is a
repo-based local-first app, so ``pyproject.toml`` is the truth and stays
correct without a reinstall; installed package metadata is the fallback for a
non-editable install.
"""

from __future__ import annotations

from pathlib import Path

_FALLBACK = "0.0.0"


def get_version() -> str:
    # 1. pyproject.toml in the repo root (accurate without reinstall).
    try:
        import tomllib

        pyproject = Path(__file__).resolve().parents[2] / "pyproject.toml"
        if pyproject.exists():
            data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
            version = data.get("project", {}).get("version")
            if version:
                return str(version)
    except Exception:
        pass

    # 2. Installed distribution metadata (PyPI / non-editable installs).
    try:
        import importlib.metadata

        return importlib.metadata.version("youos")
    except Exception:
        return _FALLBACK
