#!/usr/bin/env python3
"""Render agent-facing exports from current relic state."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from vault_paths import get_vault_path

VAULT = get_vault_path()
FACETS = VAULT / 'facets.json'
SELF_MODEL = VAULT / 'self-model.md'
VOICE = VAULT / 'voice.md'
GOALS = VAULT / 'goals.md'
OUT = VAULT / 'exports' / 'agent-prompt.md'


def render() -> Path:
    """Render the export and return its path."""
    facets = json.loads(FACETS.read_text(encoding='utf-8')) if FACETS.exists() else {}
    self_model = SELF_MODEL.read_text(encoding='utf-8') if SELF_MODEL.exists() else ''
    voice = VOICE.read_text(encoding='utf-8') if VOICE.exists() else ''
    goals = GOALS.read_text(encoding='utf-8') if GOALS.exists() else ''

    lines = [
        '# Relic Agent Prompt',
        '',
        'Use this as a bounded, human-auditable approximation of the person represented by the relic vault.',
        '',
        '## Distilled self model',
        self_model.strip(),
        '',
        '## Voice',
        voice.strip(),
        '',
        '## Goals',
        goals.strip(),
        '',
        '## Structured facets',
        '```json',
        json.dumps(facets, ensure_ascii=False, indent=2),
        '```',
        ''
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text('\n'.join(lines), encoding='utf-8')
    return OUT


def main(argv: list[str] = None) -> None:
    """Main entry point."""
    export_path = render()
    print(str(export_path))


if __name__ == '__main__':
    main()