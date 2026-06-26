#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

DOMAIN_BITS = {
    'strategy': 0,
    'business': 1,
    'organization': 2,
    'finance': 3,
    'legal': 4,
    'project': 5,
    'operations': 6,
    'tech': 7,
    'routines': 8,
    'personal': 9,
    'meta': 10,
    'misc': 11,
}


def uniq(seq):
    seen = set()
    out = []
    for x in seq:
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return out


def mask_for(domains):
    mask = 0
    for d in domains:
        if d not in DOMAIN_BITS:
            raise ValueError(f'Unknown domain: {d}')
        mask |= 1 << DOMAIN_BITS[d]
    return mask


def main():
    if len(sys.argv) != 3:
        raise SystemExit('Usage: upsert_by_date_index.py <index_json> <entry_json>')

    index_path = Path(sys.argv[1])
    entry = json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'))

    required = ['date', 'domains']
    for key in required:
        if key not in entry:
            raise SystemExit(f'Missing required field: {key}')

    date = entry['date']
    domains = uniq(entry.get('domains', []))
    modules = uniq(entry.get('modules', []))
    entities = uniq(entry.get('entities', []))
    system_tags = uniq(entry.get('system_tags', []))
    free_tags = uniq(entry.get('free_tags', []))
    priority = entry.get('priority', 'medium')

    if index_path.exists():
        data = json.loads(index_path.read_text(encoding='utf-8') or '{}')
    else:
        data = {}

    data[date] = {
        'mask': mask_for(domains),
        'domains': domains,
        'modules': modules,
        'entities': entities,
        'system_tags': system_tags,
        'free_tags': free_tags,
        'priority': priority,
    }

    index_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Updated {index_path} for {date}')


if __name__ == '__main__':
    main()
