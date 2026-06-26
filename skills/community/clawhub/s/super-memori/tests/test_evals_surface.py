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
    assert isinstance(payload['results'], list)
    assert payload['results'], 'eval surface should return cases'
    print('[OK] eval surface passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
