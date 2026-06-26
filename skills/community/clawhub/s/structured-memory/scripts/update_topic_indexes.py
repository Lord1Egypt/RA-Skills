#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

MODULE_TO_DOMAIN = {
    'goal': 'strategy', 'roadmap': 'strategy', 'priority': 'strategy', 'planning': 'strategy', 'decision': 'strategy',
    'product': 'business', 'requirement': 'business', 'customer': 'business', 'delivery': 'business', 'growth': 'business', 'pricing': 'business',
    'org': 'organization', 'team': 'organization', 'management': 'organization', 'process': 'organization', 'meeting': 'organization', 'reporting': 'organization', 'recruiting': 'organization', 'performance': 'organization', 'onboarding': 'organization',
    'budget': 'finance', 'reimbursement': 'finance', 'payment': 'finance', 'tax': 'finance', 'invoice': 'finance',
    'contract': 'legal', 'compliance': 'legal', 'nda': 'legal', 'approval': 'legal', 'ip': 'legal',
    'milestone': 'project', 'schedule': 'project', 'risk': 'project', 'blocker': 'project', 'dependency': 'project', 'owner': 'project',
    'workflow': 'operations', 'support': 'operations', 'execution': 'operations', 'follow-up': 'operations', 'handoff': 'operations',
    'ai': 'tech', 'coding': 'tech', 'architecture': 'tech', 'infrastructure': 'tech', 'automation': 'tech', 'security': 'tech',
    'morning-brief': 'routines', 'cron': 'routines', 'reminder': 'routines', 'daily-report': 'routines', 'weekly-report': 'routines',
    'preference': 'personal', 'schedule-personal': 'personal', 'health': 'personal', 'mood': 'personal', 'learning': 'personal', 'reading': 'personal', 'movie': 'personal',
    'memory-system': 'meta', 'workflow-rule': 'meta', 'reply-style': 'meta', 'evaluation': 'meta',
    'uncategorized': 'misc',
}


def slugify(name: str) -> str:
    s = name.strip().replace(' ', '-')
    s = re.sub(r'[^A-Za-z0-9._-]+', '-', s)
    s = re.sub(r'-+', '-', s).strip('-')
    return s or 'unknown'


def extract_summary(memory_path: Path) -> str:
    import subprocess

    script = ROOT / 'skills/structured-memory/scripts/summarize_daily_memory.py'
    try:
        result = subprocess.run(
            ['python3', str(script), str(memory_path)],
            check=True,
            capture_output=True,
            text=True,
        )
        summary = result.stdout.strip()
        if summary:
            return summary[:300]
    except Exception:
        pass

    text = memory_path.read_text(encoding='utf-8')
    lines = [ln.strip('- ').strip() for ln in text.splitlines() if ln.strip().startswith('- ')]
    if not lines:
        return f'Indexed from {memory_path.name}'
    return '；'.join(lines[:2])[:300]


def append_section(path: Path, title: str, body_lines: list[str]):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(f'# {title}\n\n', encoding='utf-8')
    with path.open('a', encoding='utf-8') as f:
        for line in body_lines:
            f.write(line + '\n')
        f.write('\n')


def main():
    if len(sys.argv) != 3:
        raise SystemExit('Usage: update_topic_indexes.py <parsed_entry_json> <memory_markdown>')

    parsed_path = Path(sys.argv[1])
    memory_path = Path(sys.argv[2])
    entry = json.loads(parsed_path.read_text(encoding='utf-8'))
    date = entry['date']
    modules = entry.get('modules', [])
    entities = entry.get('entities', [])
    free_tags = entry.get('free_tags', [])
    system_tags = entry.get('system_tags', [])
    summary = extract_summary(memory_path)

    created_modules = []
    for module in modules:
        domain = MODULE_TO_DOMAIN.get(module)
        if not domain:
            continue
        mod_path = ROOT / 'memory-modules' / domain / f'{slugify(module)}.md'
        append_section(
            mod_path,
            module,
            [
                f'## {date}',
                f'- {summary}',
                f'  - source: {memory_path.relative_to(ROOT)}',
                f'  - entities: [{", ".join(entities)}]',
                f'  - system_tags: [{", ".join(system_tags)}]',
                f'  - free_tags: [{", ".join(free_tags)}]',
            ],
        )
        created_modules.append(str(mod_path.relative_to(ROOT)))

    created_entities = []
    for entity in entities:
        ent_path = ROOT / 'memory-entities' / f'{slugify(entity)}.md'
        append_section(
            ent_path,
            entity,
            [
                f'## {date}',
                f'- {summary}',
                f'  - source: {memory_path.relative_to(ROOT)}',
                f'  - modules: [{", ".join(modules)}]',
                f'  - system_tags: [{", ".join(system_tags)}]',
                f'  - free_tags: [{", ".join(free_tags)}]',
            ],
        )
        created_entities.append(str(ent_path.relative_to(ROOT)))

    print(json.dumps({
        'date': date,
        'created_modules': created_modules,
        'created_entities': created_entities,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
