#!/usr/bin/env python3
"""Run the bundled X Layer Execution Guard runtime from an installed skill."""
from __future__ import annotations

import runpy
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
RUNTIME = SKILL_ROOT / "runtime"

if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))

runpy.run_module("execution_guard.cli", run_name="__main__")
