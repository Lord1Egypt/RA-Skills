#!/usr/bin/env python3
"""Apply a proposal to the self-model, creating a snapshot first."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from vault_paths import get_vault_path

VAULT = get_vault_path()
PROPOSALS = VAULT / 'evolution' / 'proposals'
ACCEPTED = VAULT / 'evolution' / 'accepted'
SNAPSHOTS = VAULT / 'snapshots'
SELF_MODEL = VAULT / 'self-model.md'
FACETS = VAULT / 'facets.json'


def ts_now() -> str:
    return datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')


def resolve_proposal_path(proposal_id: str) -> Path:
    """Resolve a proposal ID to a file path within the proposals directory."""
    if Path(proposal_id).name != proposal_id or proposal_id.endswith('.json'):
        raise ValueError(f'Invalid proposal ID: {proposal_id}')

    proposal_path = (PROPOSALS / f'{proposal_id}.json').resolve()
    proposals_root = PROPOSALS.resolve()
    if proposal_path.parent != proposals_root:
        raise ValueError(f'Invalid proposal ID: {proposal_id}')

    return proposal_path


def apply(proposal_id: str) -> Path:
    """Apply a proposal and return the accepted path."""
    proposal_path = resolve_proposal_path(proposal_id)
    if not proposal_path.exists():
        raise FileNotFoundError(f'Proposal not found: {proposal_path}')

    snap_dir = SNAPSHOTS / ts_now()
    snap_dir.mkdir(parents=True, exist_ok=True)
    if SELF_MODEL.exists():
        shutil.copy2(SELF_MODEL, snap_dir / 'self-model.md')
    if FACETS.exists():
        shutil.copy2(FACETS, snap_dir / 'facets.json')

    proposal = json.loads(proposal_path.read_text(encoding='utf-8'))
    lines = ['# Self Model', '', 'Applied from proposal: ' + proposal['id'], '', '## Summary', proposal['summary'], '']
    if proposal.get('rationale'):
        lines.extend(['## Rationale'])
        lines.extend(f'- {x}' for x in proposal['rationale'])
        lines.append('')
    SELF_MODEL.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    ACCEPTED.mkdir(parents=True, exist_ok=True)
    accepted_path = ACCEPTED / proposal_path.name
    shutil.move(str(proposal_path), str(accepted_path))
    return accepted_path


def main(argv: list[str] = None) -> None:
    """Main entry point for CLI."""
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('proposal_id')
    args = parser.parse_args(argv)

    try:
        accepted_path = apply(args.proposal_id)
        print(str(accepted_path))
    except (FileNotFoundError, ValueError) as e:
        print(str(e), file=sys.stderr)
        raise SystemExit(1)


if __name__ == '__main__':
    main()