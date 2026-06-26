#!/usr/bin/env python3
"""
Relic capture hook - automatically capture observations from conversations.

This script is designed to be used as a PostToolUse or Stop hook.
It analyzes recent interactions and captures notable user statements.

Usage:
    # As a Stop hook in .claude/settings.json:
    python3 skill/relic/scripts/capture_hook.py --event stop

    # Manual invocation:
    python3 skill/relic/scripts/capture_hook.py --text "User's statement" --type value
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[3]
VAULT = ROOT / 'vault'
INBOX = VAULT / 'inbox.ndjson'
MANIFEST = VAULT / 'manifest.json'


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def capture(text: str,
            obs_type: str = 'reflection',
            source: str = 'conversation',
            tags: list[str] = None,
            confidence: float = 0.7) -> dict:
    """Capture an observation."""
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
        'meta': {'hook': True}
    }

    with INBOX.open('a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')

    return record


def extract_observations_from_text(text: str) -> list[dict]:
    """Extract potential observations from text using pattern matching."""
    observations = []

    # Pattern: "I value/prefer/want/like/dislike ..."
    value_patterns = [
        (r'i value ([^.]+)', 'value'),
        (r'i prefer ([^.]+)', 'preference'),
        (r'i want ([^.]+)', 'goal'),
        (r'i like ([^.]+)', 'preference'),
        (r'i dislike ([^.]+)', 'preference'),
        (r'i hate ([^.]+)', 'preference'),
        (r'i believe ([^.]+)', 'value'),
        (r'my goal is ([^.]+)', 'goal'),
        (r'remember (?:that )?([^.]+)', 'memory'),
        (r'capture (?:this: )?([^.]+)', 'instruction'),
    ]

    text_lower = text.lower()
    for pattern, obs_type in value_patterns:
        matches = re.findall(pattern, text_lower)
        for match in matches:
            if len(match) > 10:  # Only meaningful matches
                observations.append({
                    'text': match.strip(),
                    'type': obs_type,
                    'confidence': 0.75,
                    'tags': ['auto-extracted', 'pattern-match']
                })

    return observations


def main(argv: list[str] = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description='Relic capture hook')
    parser.add_argument('--event', choices=['stop', 'prompt', 'post-tool'],
                       default='stop', help='Hook event type')
    parser.add_argument('--text', help='Text to analyze for observations')
    parser.add_argument('--type', default='reflection', help='Observation type')
    parser.add_argument('--tags', nargs='*', default=[], help='Tags for observation')
    parser.add_argument('--confidence', type=float, default=0.7, help='Confidence level')
    parser.add_argument('--transcript', help='Path to transcript file (for stop events)')
    args = parser.parse_args(argv)

    if not VAULT.exists():
        # Vault not initialized, skip capture
        print('{"status": "skipped", "reason": "vault not initialized"}')
        return 0

    captured = []

    # Direct text capture
    if args.text:
        record = capture(
            text=args.text,
            obs_type=args.type,
            tags=args.tags or ['hook-captured'],
            confidence=args.confidence
        )
        captured.append(record)

    # Auto-extract from transcript
    elif args.event == 'stop' and args.transcript:
        try:
            transcript_path = Path(args.transcript)
            if transcript_path.exists():
                content = transcript_path.read_text(encoding='utf-8')
                extracted = extract_observations_from_text(content)
                for obs in extracted[:5]:  # Limit to 5 auto-extracted
                    record = capture(**obs)
                    captured.append(record)
        except Exception as e:
            print(json.dumps({'status': 'error', 'message': str(e)}))
            return 1

    result = {
        'status': 'success',
        'captured': len(captured),
        'observations': [{'id': r['id'], 'type': r['type']} for r in captured]
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())