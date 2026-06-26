#!/usr/bin/env python3
"""Capture a new observation into the relic inbox."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from uuid import uuid4

from vault_paths import get_vault_path

VAULT = get_vault_path()
INBOX = VAULT / 'inbox.ndjson'
MANIFEST = VAULT / 'manifest.json'
ALLOWED_OBSERVATION_TYPES = {
    'preference',
    'value',
    'goal',
    'tone',
    'project',
    'relationship',
    'memory',
    'instruction',
    'reflection',
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def default_manifest() -> dict[str, object]:
    return {'name': 'relic', 'version': 1, 'createdAt': now(), 'mode': 'local-first'}


def validate_tags(tags: list[str] | None) -> list[str]:
    """Validate and normalize tags."""
    if tags is None:
        return []
    if not isinstance(tags, list):
        raise ValueError('tags must be a list of non-empty strings')

    normalized_tags = [tag.strip() for tag in tags if isinstance(tag, str) and tag.strip()]
    if len(normalized_tags) != len(tags):
        raise ValueError('tags must be a list of non-empty strings')
    return normalized_tags


def validate_capture_input(text: str, obs_type: str, tags: list[str] | None, confidence: float) -> list[str]:
    """Validate capture inputs and return normalized tags."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError('text must be a non-empty string')
    if obs_type not in ALLOWED_OBSERVATION_TYPES:
        raise ValueError(f'obs_type must be one of: {", ".join(sorted(ALLOWED_OBSERVATION_TYPES))}')
    if not isinstance(confidence, int | float) or isinstance(confidence, bool):
        raise ValueError('confidence must be a number between 0 and 1')
    if confidence < 0 or confidence > 1:
        raise ValueError('confidence must be between 0 and 1')
    return validate_tags(tags)


def load_manifest() -> dict[str, object]:
    """Load manifest or fall back to a minimal valid shape."""
    if not MANIFEST.exists():
        return default_manifest()

    try:
        content = json.loads(MANIFEST.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default_manifest()

    return content if isinstance(content, dict) else default_manifest()


def capture(text: str,
            obs_type: str = 'reflection',
            source: str = 'manual',
            tags: list[str] | None = None,
            confidence: float = 0.8) -> dict[str, object]:
    """Capture an observation and return the record."""
    normalized_tags = validate_capture_input(text, obs_type, tags, confidence)

    VAULT.mkdir(parents=True, exist_ok=True)
    INBOX.parent.mkdir(parents=True, exist_ok=True)
    if not INBOX.exists():
        INBOX.write_text('', encoding='utf-8')

    record = {
        'id': str(uuid4()),
        'ts': now(),
        'type': obs_type,
        'source': source,
        'text': text.strip(),
        'tags': normalized_tags,
        'confidence': float(confidence),
        'meta': {},
    }

    with INBOX.open('a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')

    manifest = load_manifest()
    manifest['updatedAt'] = now()
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    return record


def main(argv: list[str] | None = None) -> None:
    """Main entry point for CLI."""
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('text')
    parser.add_argument('--type', default='reflection', choices=sorted(ALLOWED_OBSERVATION_TYPES))
    parser.add_argument('--source', default='manual')
    parser.add_argument('--tag', action='append', default=[])
    parser.add_argument('--confidence', type=float, default=0.8)
    args = parser.parse_args(argv)

    record = capture(
        text=args.text,
        obs_type=args.type,
        source=args.source,
        tags=args.tag,
        confidence=args.confidence,
    )
    print(json.dumps(record, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
