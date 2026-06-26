#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    proc = subprocess.run([str(ROOT / 'audit-memory.sh'), '--json'], capture_output=True, text=True, check=False)
    payload = json.loads(proc.stdout)
    assert payload['vector_state'] in {'ok', 'semantic-unbuilt', 'stale-vectors', 'orphan-vectors'}
    if payload['vector_point_count'] == 0:
        assert payload['vector_state'] == 'semantic-unbuilt'
    print('[OK] semantic-unbuilt state classification passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
