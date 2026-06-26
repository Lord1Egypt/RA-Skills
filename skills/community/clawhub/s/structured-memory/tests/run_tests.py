#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TEST_ROOT = Path(__file__).resolve().parent
CASES_DIR = TEST_ROOT / 'cases'
EXPECTED = json.loads((TEST_ROOT / 'expected.json').read_text(encoding='utf-8'))

PARSE = ROOT / 'skills/structured-memory/scripts/parse_daily_memory.py'
SUMMARY = ROOT / 'skills/structured-memory/scripts/summarize_daily_memory.py'
CRITICAL_FACTS = ROOT / 'skills/structured-memory/scripts/extract_critical_facts.py'
CRITICAL_FACT_CARDS = ROOT / 'skills/structured-memory/scripts/rebuild_critical_fact_cards.py'


def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def ensure_contains(name, actual_list, expected_list, errors):
    actual_text = ' '.join(actual_list) if isinstance(actual_list, list) else str(actual_list)
    for item in expected_list:
        if item not in actual_text:
            errors.append(f'{name}: missing expected `{item}`')


def ensure_not_contains(name, actual_list, forbidden_list, errors):
    actual_text = ' '.join(actual_list) if isinstance(actual_list, list) else str(actual_list)
    for item in forbidden_list:
        if item in actual_text:
            errors.append(f'{name}: unexpectedly contains `{item}`')


def flatten_summary(result):
    if isinstance(result, str):
        return result
    preview = result.get('preview', []) if isinstance(result, dict) else []
    topic_summaries = result.get('topic_summaries', {}) if isinstance(result, dict) else {}
    parts = []
    parts.extend(preview)
    if isinstance(topic_summaries, dict):
        for values in topic_summaries.values():
            if isinstance(values, list):
                parts.extend(values)
            else:
                parts.append(str(values))
    return ' '.join(str(x) for x in parts)


def main():
    total = 0
    failed = 0
    reports = []

    for case_file in sorted(CASES_DIR.glob('*.md')):
        case_name = case_file.stem
        total += 1
        parsed = json.loads(run(['python3', str(PARSE), str(case_file)]))
        summary_raw = run(['python3', str(SUMMARY), str(case_file)]).strip()
        try:
            summary_obj = json.loads(summary_raw)
        except json.JSONDecodeError:
            summary_obj = summary_raw
        critical_raw = run(['python3', str(CRITICAL_FACTS), str(case_file)]).strip()
        critical_obj = json.loads(critical_raw)
        summary_text = flatten_summary(summary_obj)
        exp = EXPECTED[case_name]
        errors = []

        for key in ['domains', 'modules', 'entities']:
            if key in exp:
                ensure_contains(key, parsed.get(key, []), exp[key].get('contains', []), errors)
                ensure_not_contains(key, parsed.get(key, []), exp[key].get('notContains', []), errors)

        if 'summary' in exp:
            ensure_contains('summary', summary_text, exp['summary'].get('contains', []), errors)
            ensure_not_contains('summary', summary_text, exp['summary'].get('notContains', []), errors)

        if 'critical_facts' in exp:
            fact_values = [f.get('value', '') for f in critical_obj.get('facts', [])]
            fact_types = [f.get('fact_type', '') for f in critical_obj.get('facts', [])]
            fact_domains = [' '.join(f.get('domains', [])) for f in critical_obj.get('facts', [])]
            fact_modules = [' '.join(f.get('modules', [])) for f in critical_obj.get('facts', [])]
            fact_projects = [f.get('related_project', '') for f in critical_obj.get('facts', [])]
            fact_entities = [f.get('related_entity', '') for f in critical_obj.get('facts', [])]
            cf = exp['critical_facts']
            if 'contains' in cf:
                ensure_contains('critical_facts', fact_values, cf.get('contains', []), errors)
            if 'notContains' in cf:
                ensure_not_contains('critical_facts', fact_values, cf.get('notContains', []), errors)
            if 'types' in cf:
                ensure_contains('critical_fact_types', fact_types, cf.get('types', []), errors)
            if 'domains' in cf:
                ensure_contains('critical_fact_domains', fact_domains, cf.get('domains', []), errors)
            if 'modules' in cf:
                ensure_contains('critical_fact_modules', fact_modules, cf.get('modules', []), errors)
            if 'related_project' in cf:
                ensure_contains('critical_fact_related_project', fact_projects, cf.get('related_project', []), errors)
            if 'related_entity' in cf:
                ensure_contains('critical_fact_related_entity', fact_entities, cf.get('related_entity', []), errors)

        if errors:
            failed += 1
            reports.append({'case': case_name, 'ok': False, 'errors': errors, 'parsed': parsed, 'summary': summary_obj})
        else:
            reports.append({'case': case_name, 'ok': True})

    malformed_asset = ROOT / 'skills/structured-memory/tests/assets-critical-facts-malformed.md'
    total += 1
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        cf_dir = tmpdir / 'critical-facts'
        cards_dir = tmpdir / 'cards'
        cf_dir.mkdir(parents=True, exist_ok=True)
        (cf_dir / 'services.md').write_text(malformed_asset.read_text(encoding='utf-8'), encoding='utf-8')
        out = run([
            'python3', str(CRITICAL_FACT_CARDS),
            '--critical-facts-dir', str(cf_dir),
            '--cards-dir', str(cards_dir),
        ])
        card_path = cards_dir / 'openclaw.md'
        errors = []
        if not card_path.exists():
            errors.append('critical_fact_cards: expected openclaw.md to be created for malformed input fixture')
        else:
            text = card_path.read_text(encoding='utf-8')
            ensure_contains('critical_fact_cards', text, ['openclaw-gateway.service'], errors)
            ensure_not_contains('critical_fact_cards', text, ['Traceback', 'ValueError'], errors)
        if errors:
            failed += 1
            reports.append({'case': 'critical-fact-cards-malformed', 'ok': False, 'errors': errors, 'output': out})
        else:
            reports.append({'case': 'critical-fact-cards-malformed', 'ok': True})

    print(json.dumps({'total': total, 'failed': failed, 'reports': reports}, ensure_ascii=False, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
