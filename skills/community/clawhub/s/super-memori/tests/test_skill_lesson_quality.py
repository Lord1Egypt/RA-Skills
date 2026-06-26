#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    proc = subprocess.run([str(ROOT / 'eval-memory.sh'), '--json'], capture_output=True, text=True, check=False)
    payload = json.loads(proc.stdout)
    assert payload['status'] in {'ok', 'warn'}
    assert payload['results'], 'expected eval cases'
    print('[OK] skill lesson quality eval passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
