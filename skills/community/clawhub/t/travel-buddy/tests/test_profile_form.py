#!/usr/bin/env python3
"""Run tests/test_profile_form.js, which executes the profile form's own JavaScript.

Same division of labour as tests/test_intake_form.py: the behaviour under test IS JavaScript, so
asserting it in Python would mean re-implementing the form's logic and then agreeing with itself.
What this wrapper adds is membership of the suite.

The profile form is the first screen a new traveller sees and the only one whose answers are kept
between trips, and nothing ran a line of it until 2026-09-12 — which is how three columns that end
up as exact string comparisons downstream came to accept anything the traveller typed and silently
mean nothing.

A missing `node` SKIPS, and says so on stderr rather than passing quietly: a green suite that
silently stopped exercising the form is the failure mode the form's own defects were made of.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "tests" / "test_profile_form.js"


def main() -> int:
    node = shutil.which("node")
    if not node:
        print("SKIPPED: node is not on PATH, so the profile form was NOT exercised. It is the "
              "first screen a traveller sees and the only one whose answers persist; install "
              "Node to run these.", file=sys.stderr)
        return 0
    result = subprocess.run([node, str(SUITE)], cwd=ROOT, text=True, capture_output=True)
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    return result.returncode


def test_profile_form() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
