"""Report renderers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .model import Report


def write_json(payload: Any, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def render_json(report: Report, path: Path) -> Path:
    return write_json(report.to_dict(), path)
