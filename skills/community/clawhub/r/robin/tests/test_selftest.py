from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_selftest_script_passes():
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "selftest.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "14/14 passed" in proc.stdout
