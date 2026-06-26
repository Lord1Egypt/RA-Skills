#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def normalize_piece(obj):
    if isinstance(obj, dict):
        if 'results' in obj:
            return list(obj.get('results', [])), list(obj.get('failures', []))
        if 'comboHoldings' in obj:
            return list(obj.get('comboHoldings', [])), list(obj.get('failures', []))
    if isinstance(obj, list):
        return list(obj), []
    raise ValueError(f'Unsupported JSON structure in piece: {type(obj).__name__}')


def main():
    ap = argparse.ArgumentParser(description='Merge Xueqiu combo-holdings batch JSON files into one normalized payload.')
    ap.add_argument('inputs', nargs='+', help='JSON batch files')
    ap.add_argument('--output', required=True, help='Output JSON path')
    args = ap.parse_args()

    combos = {}
    failures = {}
    for path_str in args.inputs:
        path = Path(path_str)
        items, piece_failures = normalize_piece(load_json(path))
        for item in items:
            combos[item['combo_symbol']] = item
        for item in piece_failures:
            failures[item['combo_symbol']] = item

    for sym in list(failures.keys()):
        if sym in combos:
            failures.pop(sym, None)

    out = {
        'comboCount': len(combos) + len(failures),
        'successComboCount': len(combos),
        'failureCount': len(failures),
        'failures': sorted(failures.values(), key=lambda x: x['combo_symbol']),
        'comboHoldings': sorted(combos.values(), key=lambda x: x['combo_symbol'])
    }
    Path(args.output).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    print(args.output)


if __name__ == '__main__':
    main()
