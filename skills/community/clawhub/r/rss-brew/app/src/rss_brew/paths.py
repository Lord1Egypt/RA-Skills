from __future__ import annotations

import os
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent
APP_ROOT = PACKAGE_ROOT.parents[1]           # .../rss-brew/app
SKILL_ROOT = APP_ROOT.parent                 # .../rss-brew
LEGACY_SCRIPTS_ROOT = SKILL_ROOT / "scripts"
VENV_PYTHON = SKILL_ROOT / "venv" / "bin" / "python"
COMPAT_ROOT = PACKAGE_ROOT / "compat"
DOCS_ROOT = APP_ROOT / "docs"
TESTS_ROOT = APP_ROOT / "tests"

DEFAULT_DATA_ROOT = Path(
    os.environ.get("RSS_BREW_DATA_ROOT", "/root/workplace/2 Areas/rss-brew-data")
)


def resolve_data_root(explicit: str | None = None) -> Path:
    return Path(explicit) if explicit else DEFAULT_DATA_ROOT
