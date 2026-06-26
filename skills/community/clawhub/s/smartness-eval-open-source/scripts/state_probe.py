#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
WORKSPACE = SKILL_DIR.parent.parent


def read_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        return default


def probe_quality_gate_prompt() -> int:
    target = WORKSPACE / 'scripts' / 'thought-quality-gate-v5.py'
    if not target.exists():
        print('GATE_DIMS: False False')
        return 1
    try:
        content = target.read_text(encoding='utf-8')
    except OSError:
        print('GATE_DIMS: False False')
        return 1
    has_logic = 'logic_completeness' in content
    has_data = 'data_support' in content
    print(f'GATE_DIMS: {has_logic} {has_data}')
    return 0 if (has_logic and has_data) else 1


def probe_latency_state_count() -> int:
    data = read_json(WORKSPACE / 'state' / 'response-latency-metrics.json', {'records': []})
    records = data.get('records', []) if isinstance(data, dict) else []
    print(json.dumps({'count': len(records)}, ensure_ascii=False))
    return 0


def probe_rule_candidates() -> int:
    data = read_json(WORKSPACE / 'state' / 'rule-candidates.json', {})
    if isinstance(data, dict):
        count = int(data.get('count', 0))
        payload = data
        payload.setdefault('count', count)
    elif isinstance(data, list):
        payload = {'count': len(data), 'items': data}
    else:
        payload = {'count': 0}
    print(json.dumps(payload, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description='State probe for openclaw-smartness-eval')
    parser.add_argument('--probe', required=True,
                        choices=['quality-gate-prompt', 'latency-state-count', 'rule-candidates'])
    args = parser.parse_args()

    if args.probe == 'quality-gate-prompt':
        return probe_quality_gate_prompt()
    if args.probe == 'latency-state-count':
        return probe_latency_state_count()
    return probe_rule_candidates()


if __name__ == '__main__':
    raise SystemExit(main())
