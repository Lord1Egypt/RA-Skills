from __future__ import annotations

import sys
from pathlib import Path


def bootstrap_src() -> None:
    scripts_dir = Path(__file__).resolve().parent
    skill_root = scripts_dir.parent
    src_dir = skill_root / "src"
    script_path = str(scripts_dir)
    sys.path[:] = [entry for entry in sys.path if entry != script_path]
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))
