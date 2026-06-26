#!/usr/bin/env python3
"""Initialize a new relic vault with default structure."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from vault_paths import get_vault_path

VAULT = get_vault_path()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json_if_missing(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def write_text_if_missing(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return
    path.write_text(content, encoding='utf-8')


def default_manifest(ts: str) -> dict[str, object]:
    return {
        'name': 'relic',
        'version': 1,
        'createdAt': ts,
        'updatedAt': ts,
        'mode': 'local-first',
    }


def default_facets() -> dict[str, object]:
    return {
        'preferences': [],
        'values': [],
        'goals': {'active': [], 'longTerm': []},
        'tone': {'style': [], 'likes': [], 'dislikes': []},
        'projects': [],
        'relationships': [],
    }


def init() -> Path:
    """Initialize vault structure and return path."""
    VAULT.mkdir(parents=True, exist_ok=True)
    (VAULT / 'evolution' / 'proposals').mkdir(parents=True, exist_ok=True)
    (VAULT / 'evolution' / 'accepted').mkdir(parents=True, exist_ok=True)
    (VAULT / 'evolution' / 'rejected').mkdir(parents=True, exist_ok=True)
    (VAULT / 'snapshots').mkdir(parents=True, exist_ok=True)
    (VAULT / 'exports').mkdir(parents=True, exist_ok=True)

    ts = now()
    write_json_if_missing(VAULT / 'manifest.json', default_manifest(ts))

    inbox = VAULT / 'inbox.ndjson'
    if not inbox.exists():
        inbox.write_text('', encoding='utf-8')

    write_json_if_missing(VAULT / 'facets.json', default_facets())
    write_text_if_missing(VAULT / 'self-model.md', '# Self Model\n\nA distilled narrative model has not been generated yet.\n')
    write_text_if_missing(VAULT / 'voice.md', '# Voice\n\nNo voice profile yet.\n')
    write_text_if_missing(VAULT / 'goals.md', '# Goals\n\nNo goals distilled yet.\n')
    write_text_if_missing(VAULT / 'relationships.md', '# Relationships\n\nNo relationship model yet.\n')
    write_text_if_missing(VAULT / 'exports' / 'agent-prompt.md', '# Agent Prompt\n\nNo export rendered yet.\n')

    return VAULT


def main() -> None:
    """Main entry point."""
    init()
    print(str(VAULT))


if __name__ == '__main__':
    main()
