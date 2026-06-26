#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    proc = subprocess.run(
        ['python3', str(ROOT / 'repair-memory.sh'), '--plan', '--json'],
        capture_output=True,
        text=True,
        check=False,
    )
    payload = json.loads(proc.stdout)
    assert 'actions' in payload, 'repair plan must include actions'
    assert 'warnings' in payload, 'repair plan must include warnings'
    assert proc.returncode in (0, 2), 'repair plan should be advisory, not crash'
    print('[OK] repair plan surface passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
