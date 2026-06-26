#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def safe_remove_if_contains(path: Path, date: str):
    if not path.exists() or not path.is_file():
        return False
    text = path.read_text(encoding='utf-8')
    marker = f'## {date}'
    if marker not in text:
        return False
    lines = text.splitlines()
    out = []
    i = 0
    changed = False
    while i < len(lines):
        if lines[i].strip() == marker:
            changed = True
            i += 1
            while i < len(lines) and not lines[i].startswith('## '):
                i += 1
            continue
        out.append(lines[i])
        i += 1
    while out and out[-1] == '':
        out.pop()
    path.write_text('\n'.join(out) + '\n', encoding='utf-8')
    return changed


def main():
    if len(sys.argv) != 2 or sys.argv[1] in {'-h', '--help'}:
        print('Usage: rebuild_one_day.py <YYYY-MM-DD>')
        print('Example: rebuild_one_day.py 2026-03-10')
        raise SystemExit(0 if len(sys.argv) == 2 else 1)
    date = sys.argv[1]
    memory_path = ROOT / 'memory' / f'{date}.md'
    parsed_path = ROOT / f'tmp.parsed-memory-{date}.json'
    index_path = ROOT / 'memory-index' / 'by-date.json'

    subprocess.run([
        'python3', str(ROOT / 'skills/structured-memory/scripts/parse_daily_memory.py'), str(memory_path)
    ], check=True, stdout=parsed_path.open('w', encoding='utf-8'))

    parsed = json.loads(parsed_path.read_text(encoding='utf-8'))

    # 先全局清掉这一天的旧索引，避免历史误分类残留。
    for candidate in (ROOT / 'memory-modules').rglob('*.md'):
        safe_remove_if_contains(candidate, date)
    for candidate in (ROOT / 'memory-entities').glob('*.md'):
        safe_remove_if_contains(candidate, date)
    for candidate in (ROOT / 'critical-facts').glob('*.md'):
        safe_remove_if_contains(candidate, date)

    subprocess.run([
        'python3', str(ROOT / 'skills/structured-memory/scripts/upsert_by_date_index.py'), str(index_path), str(parsed_path)
    ], check=True)
    subprocess.run([
        'python3', str(ROOT / 'skills/structured-memory/scripts/update_topic_indexes.py'), str(parsed_path), str(memory_path)
    ], check=True)
    subprocess.run([
        'python3', str(ROOT / 'skills/structured-memory/scripts/extract_critical_facts.py'), str(memory_path), '--write'
    ], check=True)
    subprocess.run([
        'python3', str(ROOT / 'skills/structured-memory/scripts/rebuild_critical_fact_cards.py')
    ], check=True)
    print(f'Rebuilt indexes, critical facts, and cards for {date}')


if __name__ == '__main__':
    main()
