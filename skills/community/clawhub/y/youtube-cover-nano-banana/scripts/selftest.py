#!/usr/bin/env python3
"""Lightweight self-test for the ClawHub publishing contract."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ENTRYPOINT = ROOT / "scripts" / "create_thumbnail.py"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ENTRYPOINT), *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def test_dry_run() -> None:
    result = run("--copy", "Man fights tiger", "--dry-run")
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["generationConfig"]["responseMimeType"] == "application/json"


def test_invalid_args_contract() -> None:
    result = run("--copy", "   ", "--stdout-json")
    assert result.returncode == 2, result.stdout
    payload = json.loads(result.stdout)
    assert payload["ok"] is False
    assert payload["error"]["code"] == "invalid_arguments"


def main() -> int:
    test_dry_run()
    test_invalid_args_contract()
    print("selftest ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
