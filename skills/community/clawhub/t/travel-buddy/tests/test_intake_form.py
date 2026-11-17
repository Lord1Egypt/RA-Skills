#!/usr/bin/env python3
"""Run tests/test_intake_form.js, which executes the intake form's own JavaScript.

The behavioural assertions live in JavaScript because the thing under test is JavaScript: the form
validates and assembles the intake JSON in the browser, and a Python test could only re-implement
that logic and then agree with itself. What this wrapper adds is membership of the suite, so
`pytest tests/` covers the file where every traveller answer enters the pipeline -- which until
2026-08-30 nothing did.

A missing `node` SKIPS, and says so on stderr rather than passing quietly: a green suite that
silently stopped exercising the form is the failure mode the form's own defects were made of.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "tests" / "test_intake_form.js"


def main() -> int:
    node = shutil.which("node")
    if not node:
        print("SKIPPED: node is not on PATH, so the intake form was NOT exercised. The form is "
              "the entry point for every traveller answer; install Node to run these.",
              file=sys.stderr)
        return 0
    proc = subprocess.run([node, str(SUITE)], capture_output=True, text=True, cwd=ROOT)
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    return proc.returncode


def test_intake_form() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
