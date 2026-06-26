#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TARGETS = [
    ROOT / 'memory-index' / 'by-date.json',
    ROOT / 'memory-modules',
    ROOT / 'memory-entities',
]


def fingerprint_path(path: Path) -> str:
    h = hashlib.sha256()
    if path.is_file():
        h.update(path.read_bytes())
    elif path.is_dir():
        for p in sorted(x for x in path.rglob('*') if x.is_file()):
            h.update(str(p.relative_to(ROOT)).encode())
            h.update(b'\0')
            h.update(p.read_bytes())
            h.update(b'\0')
    return h.hexdigest()


def snapshot() -> dict[str, str]:
    return {str(p.relative_to(ROOT)): fingerprint_path(p) for p in TARGETS}


def main():
    if len(sys.argv) != 2 or sys.argv[1] in {'-h', '--help'}:
        print('Usage: check_idempotency.py <YYYY-MM-DD>')
        print('Example: check_idempotency.py 2026-03-10')
        raise SystemExit(0 if len(sys.argv) == 2 else 1)
    date = sys.argv[1]
    cmd = ['python3', str(ROOT / 'skills/structured-memory/scripts/rebuild_one_day.py'), date]

    before = snapshot()
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    after1 = snapshot()
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    after2 = snapshot()

    stable = after1 == after2
    changed_on_first = before != after1

    print('Idempotency check:')
    print(f'- first rebuild changed state: {changed_on_first}')
    print(f'- second rebuild stable: {stable}')

    if not stable:
        print('Mismatch targets:')
        for key in after1:
            if after1[key] != after2.get(key):
                print(f'  - {key}')
        raise SystemExit(1)


if __name__ == '__main__':
    main()
