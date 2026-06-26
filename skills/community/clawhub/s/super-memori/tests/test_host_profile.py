#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    proc = subprocess.run([str(ROOT / 'health-check.sh'), '--json'], capture_output=True, text=True, check=False)
    assert proc.returncode in (0, 2), proc.stdout + proc.stderr
    payload = json.loads(proc.stdout)
    assert any(c['name'] == 'host_profile' for c in payload['checks'])
    host_profile = next(c['detail'] for c in payload['checks'] if c['name'] == 'host_profile')
    assert isinstance(host_profile, dict)
    assert 'detected_profile' in host_profile
    print('[OK] host profile truth surface passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
