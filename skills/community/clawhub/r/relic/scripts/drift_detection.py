#!/usr/bin/env python3
"""
Drift detection for relic - identify changes and contradictions.

Analyzes the gap between current self-model and recent observations
to detect identity drift, contradictions, and evolution.
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from vault_paths import get_vault_path

VAULT = get_vault_path()
INBOX = VAULT / 'inbox.ndjson'
FACETS = VAULT / 'facets.json'
SELF_MODEL = VAULT / 'self-model.md'
DRIFT_REPORT = VAULT / 'drift-report.md'


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_records(limit: int = 50) -> list[dict[str, Any]]:
    """Load recent observations from inbox."""
    if not INBOX.exists():
        return []
    rows = []
    for line in INBOX.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows[-limit:] if limit else rows


def load_facets() -> dict[str, Any]:
    """Load current facets."""
    if FACETS.exists():
        return json.loads(FACETS.read_text(encoding='utf-8'))
    return {}


def load_self_model() -> str:
    """Load current self-model."""
    if SELF_MODEL.exists():
        return SELF_MODEL.read_text(encoding='utf-8')
    return ''


def extract_keywords(text: str) -> set[str]:
    """Extract meaningful keywords from text."""
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    stop_words = {
        'this', 'that', 'with', 'from', 'have', 'been', 'were', 'they',
        'their', 'would', 'could', 'should', 'about', 'into', 'than', 'then',
        'when', 'what', 'which', 'there', 'here', 'some', 'more', 'also'
    }
    return set(w for w in words if w not in stop_words)


def detect_new_topics(recent_records: list[dict],
                      current_facets: dict) -> list[dict]:
    """Detect topics in recent records not covered in facets."""
    # Get all text from facets
    facet_text = ' '.join(
        current_facets.get('values', []) +
        current_facets.get('preferences', []) +
        [v for g in current_facets.get('goals', {}).values() for v in g] +
        current_facets.get('memories', [])
    )
    facet_keywords = extract_keywords(facet_text)

    new_topics = []
    for record in recent_records:
        record_keywords = extract_keywords(record.get('text', ''))
        novel_keywords = record_keywords - facet_keywords

        # If more than 50% of keywords are new, it's a potential new topic
        if len(novel_keywords) > len(record_keywords) * 0.5:
            new_topics.append({
                'id': record.get('id'),
                'text': record.get('text'),
                'type': record.get('type'),
                'novel_keywords': list(novel_keywords)[:5],
                'ts': record.get('ts')
            })

    return new_topics


def detect_contradictions(recent_records: list[dict],
                          current_facets: dict) -> list[dict]:
    """Detect potential contradictions between records and facets."""
    contradictions = []

    # Define contradiction patterns
    contradiction_patterns = [
        (r'\b(?:don\'t|not|never|hate|dislike)\s+(\w+)', 'negative'),
        (r'\b(?:love|like|prefer|always|must)\s+(\w+)', 'positive'),
    ]

    # Check values and preferences for contradictions
    values = current_facets.get('values', [])
    preferences = current_facets.get('preferences', [])

    for record in recent_records:
        text = record.get('text', '').lower()

        # Check if record negates a known value/preference
        for existing in values + preferences:
            existing_lower = existing.lower()

            # Extract key terms from existing statement
            existing_terms = set(existing_lower.split())

            for pattern, sentiment in contradiction_patterns:
                matches = re.findall(pattern, text)
                for match in matches:
                    if match in existing_lower:
                        contradictions.append({
                            'id': record.get('id'),
                            'record_text': record.get('text'),
                            'conflicts_with': existing,
                            'type': 'potential_contradiction',
                            'sentiment_change': sentiment
                        })

    return contradictions


def detect_evolving_patterns(recent_records: list[dict]) -> list[dict]:
    """Detect patterns that are strengthening or emerging."""
    tag_frequency = defaultdict(list)

    for record in recent_records[-20:]:  # Last 20 records
        for tag in record.get('tags', []):
            tag_frequency[tag].append(record.get('text', ''))

    patterns = []
    for tag, texts in tag_frequency.items():
        if len(texts) >= 2:
            patterns.append({
                'tag': tag,
                'frequency': len(texts),
                'examples': texts[:3],
                'status': 'strengthening' if len(texts) >= 3 else 'emerging'
            })

    return sorted(patterns, key=lambda x: -x['frequency'])


def calculate_drift_score(new_topics: list, contradictions: list,
                          patterns: list) -> dict:
    """Calculate overall drift metrics."""
    return {
        'newTopicsCount': len(new_topics),
        'contradictionsCount': len(contradictions),
        'strengtheningPatterns': len([p for p in patterns if p['status'] == 'strengthening']),
        'emergingPatterns': len([p for p in patterns if p['status'] == 'emerging']),
        'driftLevel': 'high' if len(new_topics) > 5 or len(contradictions) > 0 else
                     'medium' if len(new_topics) > 2 else 'low',
        'recommendation': 'distill' if len(new_topics) > 3 or len(contradictions) > 0 else 'stable'
    }


def generate_drift_report(new_topics: list, contradictions: list,
                          patterns: list, drift_score: dict) -> str:
    """Generate human-readable drift report."""
    lines = [
        '# Drift Report\n\n',
        f'> Generated: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}\n\n',
        '---\n\n',
        '## Summary\n\n',
        f'- **Drift Level**: {drift_score["driftLevel"]}\n',
        f'- **New Topics**: {drift_score["newTopicsCount"]}\n',
        f'- **Potential Contradictions**: {drift_score["contradictionsCount"]}\n',
        f'- **Strengthening Patterns**: {drift_score["strengtheningPatterns"]}\n',
        f'- **Recommendation**: {drift_score["recommendation"]}\n\n',
    ]

    if new_topics:
        lines.append('## New Topics Detected\n\n')
        for topic in new_topics[:10]:
            lines.append(f"- **{topic['type']}**: {topic['text']}\n")
            if topic.get('novel_keywords'):
                lines.append(f"  - Novel terms: {', '.join(topic['novel_keywords'])}\n")
        lines.append('\n')

    if contradictions:
        lines.append('## Potential Contradictions\n\n')
        for c in contradictions:
            lines.append(f"- **{c['type']}**: \"{c['record_text']}\" conflicts with \"{c['conflicts_with']}\"\n")
        lines.append('\n')

    if patterns:
        lines.append('## Pattern Evolution\n\n')
        for p in patterns[:5]:
            status_emoji = '📈' if p['status'] == 'strengthening' else '📊'
            lines.append(f"- {status_emoji} **{p['tag']}** ({p['frequency']} occurrences, {p['status']})\n")
        lines.append('\n')

    lines.append('---\n\n')
    lines.append('*Run `python3 skill/relic/scripts/distill_facets.py` to incorporate changes.*\n')

    return ''.join(lines)


def detect_drift() -> dict:
    """Main drift detection function."""
    recent_records = load_records()
    if not recent_records:
        return {'status': 'no_data', 'message': 'No observations to analyze'}

    current_facets = load_facets()

    new_topics = detect_new_topics(recent_records, current_facets)
    contradictions = detect_contradictions(recent_records, current_facets)
    patterns = detect_evolving_patterns(recent_records)
    drift_score = calculate_drift_score(new_topics, contradictions, patterns)

    # Generate report
    report = generate_drift_report(new_topics, contradictions, patterns, drift_score)
    DRIFT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    DRIFT_REPORT.write_text(report, encoding='utf-8')

    return {
        'status': 'success',
        'driftScore': drift_score,
        'newTopics': len(new_topics),
        'contradictions': len(contradictions),
        'patterns': len(patterns),
        'reportPath': str(DRIFT_REPORT)
    }


def main(argv: list[str] = None) -> None:
    """Main entry point."""
    result = detect_drift()
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()