#!/usr/bin/env python3
"""Compatibility wrapper for the modular skill usefulness audit CLI."""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from skill_usefulness_audit_lib import *  # noqa: F401,F403
from skill_usefulness_audit_lib.cli import main
import skill_usefulness_audit_lib.risk_quality as _risk_quality


def scan_skill(skill_md: Path) -> dict[str, object]:
    _risk_quality.read_text = read_text
    return _risk_quality.scan_skill(skill_md)


if __name__ == "__main__":
    raise SystemExit(main())
