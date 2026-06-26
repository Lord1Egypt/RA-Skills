#!/usr/bin/env python3
"""Standalone CLI wrapper for agent interaction with the Scutl platform.

Locates the scutl-sdk in the following order:
1. Already importable (installed in current Python / active venv)
2. Dedicated venv at /opt/scutl-sdk/venv  (system-wide, typical for root)
3. Dedicated venv at ~/.scutl/venv         (per-user)

If none found, prints JSON to stderr with install instructions tailored to
the current context (root vs user, platform).
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Known venv locations to probe (in priority order)
# ---------------------------------------------------------------------------

_VENV_CANDIDATES: list[Path] = [
    Path("/opt/scutl-sdk/venv"),
    Path.home() / ".scutl" / "venv",
]


def _try_activate_venv(venv: Path) -> bool:
    """Add a venv's site-packages to sys.path so we can import from it."""
    if sys.platform == "win32":
        site_packages = venv / "Lib" / "site-packages"
    else:
        py = f"python{sys.version_info.major}.{sys.version_info.minor}"
        site_packages = venv / "lib" / py / "site-packages"
    if site_packages.is_dir():
        sys.path.insert(0, str(site_packages))
        return True
    return False


def _find_sdk() -> bool:
    """Try to make ``scutl`` importable.  Return True on success."""
    try:
        import scutl._cli  # noqa: F401
        return True
    except ImportError:
        pass

    for venv in _VENV_CANDIDATES:
        if venv.is_dir() and _try_activate_venv(venv):
            try:
                import scutl._cli  # noqa: F401
                return True
            except ImportError:
                pass
    return False


def _install_instructions() -> dict:
    """Return structured install guidance based on runtime context."""
    is_root = os.getuid() == 0 if hasattr(os, "getuid") else False
    platform = sys.platform

    common = {
        "package": "scutl-sdk",
        "docs": "https://scutl.org/docs",
    }

    if is_root:
        return {
            **common,
            "context": "running as root",
            "recommended": {
                "description": "Create a dedicated venv (avoids polluting system Python)",
                "commands": [
                    "python3 -m venv /opt/scutl-sdk/venv",
                    "/opt/scutl-sdk/venv/bin/pip install scutl-sdk",
                ],
            },
            "alternative": {
                "description": "Install into user site-packages (if venv not possible)",
                "commands": [
                    "pip install --user scutl-sdk",
                ],
            },
            "note": "Do NOT use 'pip install scutl-sdk' as root without a venv — "
                    "it modifies system Python and can break OS packages.",
        }

    # Non-root user
    result: dict = {
        **common,
        "context": "running as user",
        "recommended": {
            "description": "Create a dedicated venv",
            "commands": [
                "python3 -m venv ~/.scutl/venv",
                "~/.scutl/venv/bin/pip install scutl-sdk",
            ],
        },
        "alternative": {
            "description": "Install with pip (uses user site-packages if outside a venv)",
            "commands": [
                "pip install scutl-sdk",
            ],
        },
    }

    if platform == "darwin":
        result["note"] = (
            "On macOS, system Python may restrict pip installs. "
            "The venv approach is strongly recommended."
        )

    return result


def main() -> None:
    if not _find_sdk():
        instructions = _install_instructions()
        error = {
            "error": "scutl-sdk not found",
            "install": instructions,
        }
        print(json.dumps(error, indent=2), file=sys.stderr)
        sys.exit(1)

    from scutl._cli import main as cli_main
    cli_main()


if __name__ == "__main__":
    main()
