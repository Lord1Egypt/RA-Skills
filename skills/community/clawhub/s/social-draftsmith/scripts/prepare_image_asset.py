#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description='Prepare a local image asset for publishing workflows')
    ap.add_argument('source')
    ap.add_argument('--dest-dir', default='/home/pi/.openclaw/workspace/social-assets')
    args = ap.parse_args()

    src = Path(args.source).expanduser().resolve()
    if not src.exists() or not src.is_file():
        print(json.dumps({'error': f'source file not found: {src}'}))
        sys.exit(1)

    dest_dir = Path(args.dest_dir).expanduser().resolve()
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    shutil.copy2(src, dest)

    print(json.dumps({
        'ok': True,
        'source': str(src),
        'prepared_path': str(dest),
    }, indent=2))


if __name__ == '__main__':
    main()
