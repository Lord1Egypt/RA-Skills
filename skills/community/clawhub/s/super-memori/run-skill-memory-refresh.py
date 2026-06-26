#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
from skill_operational_memory import refresh_skill_operational_memory

if __name__ == "__main__":
    print(refresh_skill_operational_memory())
