#!/usr/bin/env python3
"""
Relic automatic capture hook with LLM-based extraction.

This hook is designed to be called after conversation events to passively
analyze and extract user observations without explicit trigger phrases.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

# Relic vault location - absolute path for hooks called from any directory
VAULT = Path('/Users/yexiaodong/.openclaw/workspace/projects/relic/vault')
INBOX = VAULT / 'inbox.ndjson'
MANIFEST = VAULT / 'manifest.json'


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def capture(text: str, obs_type: str = 'reflection', tags: list[str] = None,
            confidence: float = 0.7, source: str = 'auto-extracted') -> dict:
    """Capture an observation to the inbox."""
    if tags is None:
        tags = ['auto-captured']

    VAULT.mkdir(parents=True, exist_ok=True)
    if not INBOX.exists():
        INBOX.write_text('', encoding='utf-8')

    record = {
        'id': str(uuid4()),
        'ts': now(),
        'type': obs_type,
        'source': source,
        'text': text,
        'tags': tags,
        'confidence': confidence,
        'meta': {'hook': True, 'auto': True}
    }

    with INBOX.open('a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')

    return record


def main():
    """Main entry point - reads JSON from stdin (from LLM hook output)."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='JSON input from LLM or stdin')
    args = parser.parse_args()

    if not VAULT.exists():
        print(json.dumps({'status': 'skipped', 'reason': 'vault not initialized'}))
        return 0

    # Read input - either from --input or stdin
    if args.input:
        try:
            data = json.loads(args.input)
        except json.JSONDecodeError:
            data = {'observations': []}
    else:
        # Try to read from stdin
        try:
            if not sys.stdin.isatty():
                stdin_data = sys.stdin.read().strip()
                if stdin_data:
                    data = json.loads(stdin_data)
                else:
                    data = {'observations': []}
            else:
                data = {'observations': []}
        except:
            data = {'observations': []}

    observations = data.get('observations', [])
    if not observations:
        print(json.dumps({'status': 'no_observations', 'captured': 0}))
        return 0

    captured = []
    for obs in observations[:5]:  # Limit to 5 per call
        if isinstance(obs, dict) and obs.get('text'):
            record = capture(
                text=obs.get('text'),
                obs_type=obs.get('type', 'reflection'),
                tags=obs.get('tags', ['auto-extracted']),
                confidence=obs.get('confidence', 0.7)
            )
            captured.append({'id': record['id'], 'type': record['type']})

    result = {
        'status': 'success',
        'captured': len(captured),
        'observations': captured
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())