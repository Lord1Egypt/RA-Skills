#!/usr/bin/env python3
import os
import time
from pathlib import Path
from datetime import datetime

BASE = Path('/root/.picoclaw/workspace/state/telegram-native-audio')
LOG_FILE = BASE / 'cleanup.log'
RETENTION_DAYS = 15
RETENTION_SECONDS = RETENTION_DAYS * 24 * 60 * 60
TARGET_DIRS = ['sent', 'processed', 'tmp', 'done', 'outbox', 'inbox']
TARGET_EXTS = {'.mp3', '.ogg', '.oga', '.wav', '.m4a', '.opus', '.json'}


def log(msg: str):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f'[{ts}] {msg}\n'
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(line)
    print(line, end='')


def should_delete(path: Path, now: float) -> bool:
    if not path.is_file():
        return False
    if path.suffix.lower() not in TARGET_EXTS:
        return False
    age = now - path.stat().st_mtime
    return age >= RETENTION_SECONDS


def main():
    now = time.time()
    deleted = 0
    errors = 0
    scanned = 0

    log(
        'cleanup start | '
        f'retention_days={RETENTION_DAYS} | '
        f'retention_seconds={RETENTION_SECONDS} | '
        f'target_dirs={",".join(TARGET_DIRS)} | '
        f'target_exts={",".join(sorted(TARGET_EXTS))}'
    )

    for dirname in TARGET_DIRS:
        d = BASE / dirname
        if not d.exists() or not d.is_dir():
            continue
        for path in d.rglob('*'):
            if path.is_file():
                scanned += 1
                try:
                    if should_delete(path, now):
                        path.unlink()
                        deleted += 1
                        log(f'deleted: {path}')
                except Exception as e:
                    errors += 1
                    log(f'error deleting {path}: {e}')

    log(f'cleanup done | scanned={scanned} deleted={deleted} errors={errors}')


if __name__ == '__main__':
    main()
