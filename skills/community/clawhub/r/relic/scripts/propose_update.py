#!/usr/bin/env python3
"""Generate a proposal for updating the self-model."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from vault_paths import get_vault_path

VAULT = get_vault_path()
FACETS = VAULT / 'facets.json'
SELF_MODEL = VAULT / 'self-model.md'
PROPOSALS = VAULT / 'evolution' / 'proposals'


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def propose() -> Path:
    """Generate a proposal and return its path."""
    ts = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    facets = json.loads(FACETS.read_text(encoding='utf-8')) if FACETS.exists() else {}
    summary_parts = []
    if facets.get('values'):
        summary_parts.append('values: ' + '; '.join(facets['values'][:5]))
    if facets.get('preferences'):
        summary_parts.append('preferences: ' + '; '.join(facets['preferences'][:5]))
    if facets.get('goals', {}).get('active'):
        summary_parts.append('goals: ' + '; '.join(facets['goals']['active'][:5]))

    proposal = {
        'id': ts,
        'createdAt': now(),
        'summary': 'Refresh distilled self-model from current facets',
        'rationale': summary_parts or ['Not enough structured evidence yet; create a baseline refresh.'],
        'changes': [
            {
                'target': 'self-model.md',
                'kind': 'replace',
                'details': 'Rewrite self-model from current distilled facets and recent evidence.'
            }
        ]
    }
    PROPOSALS.mkdir(parents=True, exist_ok=True)
    out = PROPOSALS / f'{ts}.json'
    out.write_text(json.dumps(proposal, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return out


def main(argv: list[str] = None) -> None:
    """Main entry point."""
    proposal_path = propose()
    print(str(proposal_path))


if __name__ == '__main__':
    main()