#!/usr/bin/env python3
from pathlib import Path
import shutil
import sys

TEMPLATE_DIR = Path(__file__).resolve().parents[1] / 'assets' / 'source-research-template'
TARGET_NAME = '.source-research'


def main():
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    target = root / TARGET_NAME
    if target.exists():
        print(f'[OK] Already exists: {target}')
        return 0
    shutil.copytree(TEMPLATE_DIR, target)
    print(f'[OK] Initialized: {target}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
