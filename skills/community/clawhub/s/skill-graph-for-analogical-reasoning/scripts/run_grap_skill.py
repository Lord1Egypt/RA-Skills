#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys


def main() -> int:
    bundled_src = Path(__file__).resolve().parents[1] / "python-package" / "src"
    if bundled_src.exists():
        sys.path.insert(0, str(bundled_src))

    try:
        from auto_grap_skill.cli import main as local_main
        old_argv = sys.argv[:]
        try:
            sys.argv = ["grap-skill", *sys.argv[1:]]
            return int(local_main() or 0)
        finally:
            sys.argv = old_argv
    except Exception:
        pass

    module_command = [sys.executable, "-m", "auto_grap_skill", *sys.argv[1:]]
    module_probe = subprocess.run(
        [sys.executable, "-c", "import auto_grap_skill"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if module_probe.returncode == 0:
        return subprocess.call(module_command)

    command = shutil.which("grap-skill")
    if command:
        return subprocess.call([command, *sys.argv[1:]])

    sys.stderr.write(
        "grap-skill is not available. Use the bundled python-package copy in this skill or install the GitHub Python package for this project first.\n"
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
