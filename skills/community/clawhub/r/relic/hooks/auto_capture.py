#!/usr/bin/env python3
"""
Relic auto-capture hook - called on Stop event.

This hook receives conversation data from OpenClaw and extracts observations
using pattern matching and keyword analysis.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

HOOKS_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = HOOKS_DIR.parent / 'scripts'
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import distill_facets
from vault_paths import get_vault_path

VAULT = get_vault_path()
INBOX = VAULT / 'inbox.ndjson'
MANIFEST = VAULT / 'manifest.json'
ALLOWED_TYPES = {'reflection', 'value', 'preference', 'goal'}
MAX_TEXT_LENGTH = 500
MAX_TAGS = 8
NOISE_PATTERNS = [
    re.compile(r'^exit code\b', re.IGNORECASE),
    re.compile(r'^(stdout|stderr)\s*:', re.IGNORECASE),
    re.compile(r'^allow this action\??$', re.IGNORECASE),
    re.compile(r'permission', re.IGNORECASE),
    re.compile(r'dangerouslydisablesandbox', re.IGNORECASE),
    re.compile(r'^/Users/', re.IGNORECASE),
]
FIRST_PERSON_PATTERNS = [
    re.compile(r'\bi\s+value\b', re.IGNORECASE),
    re.compile(r'\bi\s+prefer\b', re.IGNORECASE),
    re.compile(r'\bi\s+(?:really\s+)?like\b', re.IGNORECASE),
    re.compile(r'\bi\s+(?:really\s+)?dislike\b', re.IGNORECASE),
    re.compile(r'\bi\s+hate\b', re.IGNORECASE),
    re.compile(r'\bi\s+want\b', re.IGNORECASE),
    re.compile(r'\bi\s+plan\b', re.IGNORECASE),
    re.compile(r'\bmy\s+goal\s+is\b', re.IGNORECASE),
    re.compile(r'\bi\s+am\s+(?:working on|building|creating)\b', re.IGNORECASE),
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_observation(observation: dict[str, Any]) -> dict[str, Any] | None:
    text = observation.get('text')
    if not isinstance(text, str):
        return None

    normalized_text = ' '.join(text.strip().split())
    if not normalized_text:
        return None

    normalized_type = observation.get('type', 'reflection')
    if normalized_type not in ALLOWED_TYPES:
        normalized_type = 'reflection'

    raw_tags = observation.get('tags', ['auto-captured'])
    if not isinstance(raw_tags, list):
        raw_tags = ['auto-captured']

    normalized_tags = [
        str(tag).strip()
        for tag in raw_tags
        if isinstance(tag, str) and tag.strip()
    ][:MAX_TAGS]
    if not normalized_tags:
        normalized_tags = ['auto-captured']

    raw_confidence = observation.get('confidence', 0.7)
    if isinstance(raw_confidence, (int, float)):
        confidence = max(0.0, min(float(raw_confidence), 1.0))
    else:
        confidence = 0.7

    return {
        'text': normalized_text[:MAX_TEXT_LENGTH],
        'type': normalized_type,
        'tags': normalized_tags,
        'confidence': confidence,
    }


def capture(text: str, obs_type: str = 'reflection', tags: list[str] | None = None,
            confidence: float = 0.7, source: str = 'auto-extracted') -> dict[str, Any]:
    """Capture an observation to the inbox."""
    record = {
        'id': str(uuid4()),
        'ts': now(),
        'type': obs_type,
        'source': source,
        'text': text,
        'tags': tags or ['auto-captured'],
        'confidence': confidence,
        'meta': {'hook': True, 'auto': True}
    }

    VAULT.mkdir(parents=True, exist_ok=True)
    if not INBOX.exists():
        INBOX.write_text('', encoding='utf-8')

    with INBOX.open('a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')

    return record


def refresh_distilled_artifacts() -> None:
    """Refresh derived vault artifacts after successful capture."""
    distill_facets.VAULT = VAULT
    distill_facets.INBOX = INBOX
    distill_facets.FACETS = VAULT / 'facets.json'
    distill_facets.SELF_MODEL = VAULT / 'self-model.md'
    distill_facets.VOICE = VAULT / 'voice.md'
    distill_facets.GOALS = VAULT / 'goals.md'
    distill_facets.RELATIONSHIPS = VAULT / 'relationships.md'
    distill_facets.MANIFEST = MANIFEST
    distill_facets.main()


def extract_patterns(text: str) -> list[dict[str, Any]]:
    """Extract observations using pattern matching."""
    observations: list[dict[str, Any]] = []
    text_lower = text.lower()

    value_patterns = [
        r'i (?:really )?value ([^.]+)',
        r'i believe (?:that )?([^.]+)',
        r'(?:it is )?important (?:to me )?(?:that )?([^.]+)',
        r'my (?:core )?value is ([^.]+)',
    ]
    preference_patterns = [
        r'i prefer ([^.]+)',
        r'i (?:really )?like ([^.]+)',
        r'i (?:really )?dislike ([^.]+)',
        r'i hate ([^.]+)',
        r'i (?:usually |always )?tend to ([^.]+)',
    ]
    goal_patterns = [
        r'(?:^|\.\s+)my goal is (?:to )?([^.]+)',
        r'(?:^|\.\s+)goal is (?:to )?([^.]+)',
        r'i want (?:to )?([^.]+)',
        r'i plan (?:to )?([^.]+)',
        r'i am (?:working on|building|creating) ([^.]+)',
    ]

    for pattern in value_patterns:
        for match in re.findall(pattern, text_lower):
            if len(match) >= 10:
                observations.append({
                    'text': match.strip(),
                    'type': 'value',
                    'tags': ['auto-extracted', 'value'],
                    'confidence': 0.7,
                })

    for pattern in preference_patterns:
        for match in re.findall(pattern, text_lower):
            if len(match) >= 10:
                observations.append({
                    'text': match.strip(),
                    'type': 'preference',
                    'tags': ['auto-extracted', 'preference'],
                    'confidence': 0.65,
                })

    for pattern in goal_patterns:
        for match in re.findall(pattern, text_lower):
            if len(match) >= 10:
                observations.append({
                    'text': match.strip(),
                    'type': 'goal',
                    'tags': ['auto-extracted', 'goal'],
                    'confidence': 0.7,
                })

    return observations


def is_noisy_line(line: str) -> bool:
    """Return True when a line looks like tool or permission noise."""
    stripped = line.strip()
    if not stripped:
        return True
    if len(stripped) > 220 and not any(pattern.search(stripped) for pattern in FIRST_PERSON_PATTERNS):
        return True
    if stripped.count('{') + stripped.count('[') + stripped.count('`') + stripped.count('|') >= 6:
        return True
    return any(pattern.search(stripped) for pattern in NOISE_PATTERNS)


def filter_transcript(transcript: str) -> str:
    """Keep only likely user-signal lines from a transcript."""
    filtered_lines = [
        line.strip()
        for line in transcript.splitlines()
        if line.strip() and (not is_noisy_line(line) or any(pattern.search(line) for pattern in FIRST_PERSON_PATTERNS))
    ]
    return ' '.join(filtered_lines)


def parse_input(input_data: str) -> tuple[list[dict[str, Any]], str]:
    """Parse stdin and return observations or a transcript string."""
    try:
        data = json.loads(input_data)
    except json.JSONDecodeError:
        return [], input_data

    if isinstance(data, dict):
        observations = data.get('observations')
        if isinstance(observations, list):
            return observations, ''

        transcript = data.get('transcript')
        if isinstance(transcript, str):
            return [], transcript

    if isinstance(data, list):
        return data, ''

    return [], input_data


def main() -> int:
    """Main entry point - reads hook data from stdin."""
    if not VAULT.exists():
        print(json.dumps({'status': 'skipped', 'reason': 'vault not initialized'}))
        return 0

    try:
        input_data = sys.stdin.read().strip() if not sys.stdin.isatty() else ''
    except (OSError, ValueError) as exc:
        print(json.dumps({'status': 'error', 'reason': f'failed to read input: {exc}'}))
        return 1

    if not input_data:
        print(json.dumps({'status': 'skipped', 'reason': 'no input data'}))
        return 0

    observation_candidates, transcript = parse_input(input_data)
    if not observation_candidates and transcript:
        transcript = filter_transcript(transcript)
        if transcript:
            observation_candidates = extract_patterns(transcript)

    normalized_observations = [
        normalized
        for candidate in observation_candidates[:5]
        for normalized in [normalize_observation(candidate)]
        if normalized is not None
    ]

    if not normalized_observations:
        print(json.dumps({'status': 'success', 'captured': 0, 'reason': 'no observations found'}))
        return 0

    for observation in normalized_observations:
        capture(
            text=observation['text'],
            obs_type=observation['type'],
            tags=observation['tags'],
            confidence=observation['confidence'],
        )

    try:
        refresh_distilled_artifacts()
    except Exception as exc:
        print(json.dumps({
            'status': 'error',
            'captured': len(normalized_observations),
            'reason': f'capture succeeded but distillation failed: {exc}',
        }))
        return 1

    print(json.dumps({'status': 'success', 'captured': len(normalized_observations), 'distilled': True}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
