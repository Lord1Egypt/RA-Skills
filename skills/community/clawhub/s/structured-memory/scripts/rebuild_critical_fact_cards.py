#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CRITICAL_FACTS_DIR = ROOT / 'critical-facts'
DEFAULT_CARDS_DIR = DEFAULT_CRITICAL_FACTS_DIR / 'cards'


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r'[^a-z0-9\u4e00-\u9fff]+', '-', text)
    text = re.sub(r'-+', '-', text).strip('-')
    return text or 'unknown'


def parse_scalar(value: str):
    value = value.strip()
    if value.startswith('[') and value.endswith(']'):
        inner = value[1:-1].strip()
        if not inner:
            return []
        parts = [x.strip().strip('"\'') for x in inner.split(',')]
        return [p for p in parts if p]
    return value


def parse_property_line(line: str):
    stripped = line.strip()
    if not stripped:
        return None
    normalized = stripped.replace('：', ':')
    m = re.match(r'^([A-Za-z0-9_-]+)\s*:\s*(.*)$', normalized)
    if not m:
        return None
    return m.group(1), m.group(2)


def parse_fact_files(critical_facts_dir: Path):
    facts = []
    for path in sorted(critical_facts_dir.glob('*.md')):
        text = path.read_text(encoding='utf-8')
        current_date = ''
        current = None
        for raw in text.splitlines():
            line = raw.rstrip('\n')
            if line.startswith('## '):
                current_date = line[3:].strip()
                continue
            if line.startswith('- entity: '):
                if current:
                    facts.append(current)
                current = {'entity': line.split(': ', 1)[1].strip(), 'date': current_date, 'bucket': path.stem}
                continue
            if current and line.startswith('  '):
                parsed = parse_property_line(line)
                if not parsed:
                    continue
                key, value = parsed
                current[key] = parse_scalar(value)
        if current:
            facts.append(current)
    return facts


def card_key(fact: dict) -> str:
    return fact.get('related_entity') or fact.get('related_project') or fact.get('entity') or 'unknown'


def render_card(name: str, facts: list[dict]) -> str:
    facts = sorted(facts, key=lambda f: (f.get('date', ''), f.get('fact_type', ''), f.get('value', '')))
    domains = sorted({d for f in facts for d in (f.get('domains') or [])})
    modules = sorted({m for f in facts for m in (f.get('modules') or [])})
    projects = sorted({p for f in facts if f.get('related_project') for p in [f.get('related_project')]})
    lines = [f'# {name}', '']
    if projects:
        lines.append(f'- related_projects: {projects}')
    if domains:
        lines.append(f'- domains: {domains}')
    if modules:
        lines.append(f'- modules: {modules}')
    lines.append('')

    by_date = {}
    for fact in facts:
        by_date.setdefault(fact.get('date', 'unknown'), []).append(fact)

    for date in sorted(by_date.keys(), reverse=True):
        lines.append(f'## {date}')
        for fact in by_date[date]:
            lines.append(f"- {fact.get('fact_type')}: {fact.get('value')}")
            if fact.get('sensitivity'):
                lines.append(f"  - sensitivity: {fact.get('sensitivity')}")
            if fact.get('source'):
                lines.append(f"  - source: {fact.get('source')}")
            if fact.get('note'):
                lines.append(f"  - note: {fact.get('note')}")
        lines.append('')
    return '\n'.join(lines).rstrip() + '\n'


def main():
    parser = argparse.ArgumentParser(description='Rebuild critical-fact object cards from critical-facts/*.md with tolerant parsing.')
    parser.add_argument('--critical-facts-dir', default=str(DEFAULT_CRITICAL_FACTS_DIR), help='Directory containing critical-facts markdown files')
    parser.add_argument('--cards-dir', default=str(DEFAULT_CARDS_DIR), help='Output directory for rebuilt cards')
    args = parser.parse_args()

    critical_facts_dir = Path(args.critical_facts_dir)
    cards_dir = Path(args.cards_dir)

    if cards_dir.exists():
        shutil.rmtree(cards_dir)
    cards_dir.mkdir(parents=True, exist_ok=True)

    facts = parse_fact_files(critical_facts_dir)
    grouped = {}
    for fact in facts:
        key = card_key(fact)
        grouped.setdefault(key, []).append(fact)

    written = []
    for key, group in grouped.items():
        path = cards_dir / f'{slugify(key)}.md'
        path.write_text(render_card(key, group), encoding='utf-8')
        try:
            written.append(str(path.relative_to(ROOT)))
        except ValueError:
            written.append(str(path))

    print('\n'.join(written))


if __name__ == '__main__':
    main()
