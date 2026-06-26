#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DIRS = [
    ROOT / 'memory-modules',
    ROOT / 'memory-entities',
    ROOT / 'memory-index',
    ROOT / 'critical-facts',
]
INDEX_FILE = ROOT / 'memory-index' / 'by-date.json'
BOOTSTRAP_MARKER = ROOT / 'memory-index' / '.structured-memory-bootstrap-v1'
REBUILD_ONE_DAY = ROOT / 'skills/structured-memory/scripts/rebuild_one_day.py'


def ensure_structure():
    for d in DIRS:
        d.mkdir(parents=True, exist_ok=True)

    if not INDEX_FILE.exists():
        INDEX_FILE.write_text('{}\n', encoding='utf-8')
    else:
        try:
            data = json.loads(INDEX_FILE.read_text(encoding='utf-8') or '{}')
            if not isinstance(data, dict):
                raise ValueError('by-date.json must contain a JSON object')
        except Exception as e:
            raise SystemExit(f'Invalid {INDEX_FILE}: {e}')


def existing_memory_days() -> list[str]:
    memory_dir = ROOT / 'memory'
    if not memory_dir.exists():
        return []
    return sorted(p.stem for p in memory_dir.glob('*.md') if p.stem[:4].isdigit())


def should_backfill(force: bool) -> bool:
    if force:
        return True
    if BOOTSTRAP_MARKER.exists():
        return False
    try:
        data = json.loads(INDEX_FILE.read_text(encoding='utf-8') or '{}')
    except Exception:
        data = {}
    return not data


def backfill(days: list[str]):
    rebuilt = []
    for day in days:
        subprocess.run(['python3', str(REBUILD_ONE_DAY), day], check=True)
        rebuilt.append(day)
    BOOTSTRAP_MARKER.write_text(json.dumps({'days': rebuilt}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return rebuilt


def main():
    parser = argparse.ArgumentParser(description='Initialize structured-memory directories and perform first-run backfill of historical daily memory.')
    parser.add_argument('--no-backfill', action='store_true', help='Create the structure only; skip automatic historical backfill.')
    parser.add_argument('--force-backfill', action='store_true', help='Force a historical backfill even if bootstrap marker or index data already exists.')
    args = parser.parse_args()

    ensure_structure()

    print('Structured memory skeleton is ready:')
    for d in DIRS:
        print(f'- {d}')
    print(f'- {INDEX_FILE}')

    days = existing_memory_days()
    if args.no_backfill:
        print('Backfill skipped by --no-backfill.')
        return

    if not days:
        print('No historical daily memory files found; nothing to backfill.')
        BOOTSTRAP_MARKER.write_text(json.dumps({'days': []}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        return

    if should_backfill(args.force_backfill):
        rebuilt = backfill(days)
        print(f'Initial backfill completed for {len(rebuilt)} day(s).')
    else:
        print('Backfill already initialized; skipping automatic historical rebuild.')


if __name__ == '__main__':
    main()
