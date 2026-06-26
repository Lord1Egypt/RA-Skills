#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    subprocess.run(['python3', str(ROOT / 'query-memory.sh'), 'no-such-memory-pattern-hopefully', '--json'], capture_output=True, text=True, check=False)
    proc = subprocess.run(['python3', str(ROOT / 'list-promotion-candidates.sh'), '--json'], capture_output=True, text=True, check=False)
    payload = json.loads(proc.stdout)
    assert payload['status'] == 'ok'
    assert isinstance(payload['candidates'], list)
    print('[OK] promotion candidate surface passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
