#!/usr/bin/env python3
"""
Distill observations into structured facets and narrative self-model.

Enhanced version with:
- Semantic grouping by themes
- Pattern detection across observations
- Narrative generation for self-model
- Deduplication of similar observations
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
VOICE = VAULT / 'voice.md'
GOALS = VAULT / 'goals.md'
RELATIONSHIPS = VAULT / 'relationships.md'
MANIFEST = VAULT / 'manifest.json'
DISTILLABLE_TYPES = {
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
SEMANTIC_NOISE_PATTERNS = (
    re.compile(r'^fixed:\\n\\n\d+', re.IGNORECASE),
    re.compile(r'cannot read the spec', re.IGNORECASE),
    re.compile(r'\*\*options to proceed:\*\*', re.IGNORECASE),
    re.compile(r'/users/[^\s`]+', re.IGNORECASE),
    re.compile(r'fresh repo with just a readme', re.IGNORECASE),
    re.compile(r'need access to:', re.IGNORECASE),
    re.compile(r'please grant permission', re.IGNORECASE),
    re.compile(r'workspace coordination system', re.IGNORECASE),
    re.compile(r'can coordinate properly \(read spec, create tasks, delegate\)', re.IGNORECASE),
    re.compile(r'can read/write files in this repo path directly', re.IGNORECASE),
    re.compile(r'simplicity in code\\"\)\\n\d+', re.IGNORECASE),
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_records() -> list[dict[str, Any]]:
    """Load all observations from inbox."""
    if not INBOX.exists():
        return []
    rows = []
    for line in INBOX.read_text(encoding='utf-8').splitlines():
        normalized_line = line.strip()
        if not normalized_line:
            continue
        try:
            rows.append(json.loads(normalized_line))
        except json.JSONDecodeError:
            continue
    return rows


def is_semantic_noise_text(text: str) -> bool:
    """Return True when text looks like legacy tool or prompt chatter."""
    normalized = text.strip()
    if not normalized:
        return True
    if len(normalized) > 220:
        return True
    if normalized.count('`') + normalized.count('*') + normalized.count('{') >= 6:
        return True
    return any(pattern.search(normalized) for pattern in SEMANTIC_NOISE_PATTERNS)


def is_distillable_record(record: dict[str, Any]) -> bool:
    """Return True when a record is usable for distillation."""
    text = record.get('text')
    record_type = record.get('type')
    if not isinstance(text, str) or not text.strip():
        return False
    if is_semantic_noise_text(text):
        return False
    return isinstance(record_type, str) and record_type in DISTILLABLE_TYPES




def normalize_tags(value: Any) -> list[str]:
    """Normalize tags into a clean list of non-empty strings."""
    if not isinstance(value, list):
        return []
    return [tag.strip() for tag in value if isinstance(tag, str) and tag.strip()]


def normalize_confidence(value: Any) -> float:
    """Normalize confidence into a safe 0..1 float."""
    if isinstance(value, bool):
        return 0.0
    if isinstance(value, int | float):
        confidence = float(value)
        if 0 <= confidence <= 1:
            return confidence
    return 0.0


def normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    """Return a normalized record shape suitable for distillation."""
    return {
        **record,
        'tags': normalize_tags(record.get('tags')),
        'confidence': normalize_confidence(record.get('confidence')),
    }


def filter_distillable_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Drop malformed or unsupported legacy records before distillation."""
    return [normalize_record(record) for record in records if is_distillable_record(record)]
    """Extract key terms from text for similarity matching."""
    # Normalize and extract meaningful words
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    # Filter common words
    stop_words = {'this', 'that', 'with', 'from', 'have', 'been', 'were', 'they',
                  'their', 'would', 'could', 'should', 'about', 'into', 'than', 'then'}
    return set(w for w in words if w not in stop_words)


def compute_similarity(text1: str, text2: str) -> float:
    """Compute rough similarity between two texts based on shared terms."""
    terms1 = extract_key_terms(text1)
    terms2 = extract_key_terms(text2)
    if not terms1 or not terms2:
        return 0.0
    intersection = len(terms1 & terms2)
    union = len(terms1 | terms2)
    return intersection / union if union > 0 else 0.0


def deduplicate_observations(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Remove exact duplicates while preserving distinct observations."""
    deduped_by_key: dict[tuple[str, str], dict[str, Any]] = {}

    for record in records:
        record_type = str(record.get('type', 'unknown'))
        record_text = ' '.join(str(record.get('text', '')).split())
        key = (record_type, record_text.casefold())
        existing = deduped_by_key.get(key)

        if existing is None:
            deduped_by_key[key] = record
            continue

        existing_confidence = existing.get('confidence', 0)
        record_confidence = record.get('confidence', 0)
        if record_confidence > existing_confidence:
            deduped_by_key[key] = record
            continue

        if record_confidence == existing_confidence and len(record_text) > len(str(existing.get('text', ''))):
            deduped_by_key[key] = record

    return list(deduped_by_key.values())


def detect_patterns(records: list[dict[str, Any]]) -> dict[str, list[str]]:
    """Detect recurring themes and patterns across observations."""
    tag_counts: dict[str, int] = defaultdict(int)
    tag_texts: dict[str, list[str]] = defaultdict(list)

    for r in records:
        for tag in r.get('tags', []):
            tag_counts[tag] += 1
            tag_texts[tag].append(r.get('text', ''))

    # Patterns are tags that appear multiple times
    patterns = {}
    for tag, count in sorted(tag_counts.items(), key=lambda x: -x[1]):
        if count >= 2:
            patterns[tag] = tag_texts[tag]

    return patterns


def group_by_theme(records: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Group observations into thematic clusters."""
    themes: dict[str, list[dict[str, Any]]] = defaultdict(list)

    # Define theme keywords
    theme_keywords = {
        'code_quality': ['immutability', 'modularity', 'file-organization', 'code-quality', 'limits'],
        'testing': ['testing', 'tdd', 'coverage'],
        'security': ['security', 'owasp', 'validation', 'boundaries'],
        'reliability': ['error-handling', 'reliability'],
        'workflow': ['research-first', 'reuse', 'parallel-execution', 'agent-orchestration'],
        'identity': ['identity', 'fidelity', 'relic', 'cyberpunk2077', 'evolution'],
        'communication': ['communication-style', 'concise', 'tone'],
        'data_control': ['local-first', 'data-ownership'],
    }

    for record in records:
        matched_theme = False
        record_tags = record.get('tags', [])
        for theme, keywords in theme_keywords.items():
            if any(keyword in record_tags for keyword in keywords):
                themes[theme].append(record)
                matched_theme = True
        if not matched_theme:
            themes['general'].append(record)

    return dict(themes)


def generate_narrative_section(title: str, records: list[dict[str, Any]]) -> str:
    """Generate a narrative section from records."""
    if not records:
        return f"## {title}\n\nNo observations captured yet.\n"

    lines = [f"## {title}\n\n"]

    # Sort by confidence, then by timestamp
    sorted_records = sorted(records, key=lambda x: (-x.get('confidence', 0), x.get('ts', '')))

    for r in sorted_records[:10]:  # Top 10 most confident
        text = r.get('text', '')
        confidence = r.get('confidence', 0)
        tags = r.get('tags', [])

        # Format as narrative statement
        lines.append(f"- {text}")
        if tags:
            lines.append(f"  _(tags: {', '.join(tags)}, confidence: {confidence:.0%})_")
        lines.append("")

    return "\n".join(lines)


def generate_self_model(records: list[dict[str, Any]], patterns: dict[str, list[str]]) -> str:
    """Generate a narrative self-model document."""
    themes = group_by_theme(records)

    lines = [
        "# Self Model\n\n",
        "> Distilled from captured observations. Last updated: " +
        datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC') + "\n\n",
        "---\n\n",
    ]

    # Core identity summary
    identity_records = themes.get('identity', [])
    if identity_records:
        lines.append("## Core Identity\n\n")
        for r in identity_records[:5]:
            lines.append(f"- {r.get('text', '')}\n")
        lines.append("\n")

    # Values section
    value_records = [r for r in records if r.get('type') == 'value']
    if value_records:
        lines.append(generate_narrative_section("Core Values", value_records))

    # Preferences section
    preference_records = [r for r in records if r.get('type') == 'preference']
    if preference_records:
        lines.append(generate_narrative_section("Preferences", preference_records))

    # Workflow section
    workflow_records = themes.get('workflow', [])
    if workflow_records:
        lines.append(generate_narrative_section("Workflow & Process", workflow_records))

    # Security section
    security_records = themes.get('security', [])
    if security_records:
        lines.append(generate_narrative_section("Security Mindset", security_records))

    # Testing section
    testing_records = themes.get('testing', [])
    if testing_records:
        lines.append(generate_narrative_section("Testing Philosophy", testing_records))

    # Communication style
    communication_records = themes.get('communication', [])
    tone_records = [r for r in records if r.get('type') == 'tone']
    all_comm = communication_records + tone_records
    if all_comm:
        lines.append(generate_narrative_section("Communication Style", all_comm))

    # Recurring patterns
    if patterns:
        lines.append("## Recurring Patterns\n\n")
        for pattern, texts in sorted(patterns.items(), key=lambda x: -len(x[1]))[:5]:
            lines.append(f"### {pattern}\n\n")
            for text in texts[:3]:
                lines.append(f"- {text}\n")
            lines.append("\n")

    lines.append("---\n\n")
    lines.append(f"*Total observations: {len(records)}*\n")

    return "".join(lines)


def generate_voice_profile(records: list[dict[str, Any]]) -> str:
    """Generate voice/style profile."""
    tone_records = [r for r in records if r.get('type') == 'tone']
    communication_records = [r for r in records if 'communication' in r.get('tags', [])]

    lines = [
        "# Voice Profile\n\n",
        "> Extracted communication style and preferences.\n\n",
    ]

    if tone_records or communication_records:
        for r in (tone_records + communication_records):
            lines.append(f"- {r.get('text', '')}\n")
    else:
        lines.append("- No specific voice traits captured yet.\n")

    # Extract stylistic hints from all text
    all_text = " ".join(r.get('text', '') for r in records)
    if 'concise' in all_text.lower():
        lines.append("\n**Detected preference:** Concise, direct communication.\n")
    if 'opinionated' in all_text.lower():
        lines.append("\n**Detected preference:** Opinionated, decisive statements.\n")
    if 'bloated' in all_text.lower() or 'corporate' in all_text.lower():
        lines.append("\n**Dislikes:** Bloated corporate language, unnecessary verbosity.\n")

    return "".join(lines)


def generate_goals_doc(records: list[dict[str, Any]]) -> str:
    """Generate goals document."""
    goal_records = [r for r in records if r.get('type') == 'goal']
    instruction_records = [r for r in records if r.get('type') == 'instruction']

    lines = [
        "# Goals\n\n",
        "> Active and long-term objectives extracted from observations.\n\n",
    ]

    if goal_records:
        lines.append("## Active Goals\n\n")
        for r in goal_records:
            lines.append(f"- {r.get('text', '')}\n")
        lines.append("\n")

    if instruction_records:
        lines.append("## Project Instructions\n\n")
        for r in instruction_records:
            lines.append(f"- {r.get('text', '')}\n")
        lines.append("\n")

    if not goal_records and not instruction_records:
        lines.append("No goals captured yet.\n")

    return "".join(lines)


def generate_relationships_doc(records: list[dict[str, Any]]) -> str:
    """Generate relationships document from captured relationship observations."""
    relationship_records = [r for r in records if r.get('type') == 'relationship']

    lines = [
        "# Relationships\n\n",
        "> Captured relationship observations and social context.\n\n",
    ]

    if relationship_records:
        for record in relationship_records:
            lines.append(f"- {record.get('text', '')}\n")
    else:
        lines.append("No relationships captured yet.\n")

    return "".join(lines)


def write(path: Path, content: str) -> None:
    """Write content to path, creating parent dirs if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def build_facets(records: list[dict[str, Any]], deduped: list[dict[str, Any]]) -> dict[str, Any]:
    """Build structured facets JSON."""
    def texts_by_type(typ: str) -> list[str]:
        return [r.get('text', '') for r in deduped if r.get('type') == typ]

    facets = {
        'preferences': texts_by_type('preference'),
        'values': texts_by_type('value'),
        'goals': {
            'active': texts_by_type('goal'),
            'longTerm': []
        },
        'tone': {
            'style': texts_by_type('tone'),
            'likes': [],
            'dislikes': []
        },
        'projects': texts_by_type('project'),
        'relationships': texts_by_type('relationship'),
        'memories': texts_by_type('memory'),
        'instructions': texts_by_type('instruction'),
        'reflection': texts_by_type('reflection'),
        'stats': {
            'totalRecords': len(records),
            'dedupedRecords': len(deduped),
            'lastUpdated': now()
        }
    }

    return facets


def main(argv: list[str] = None) -> None:
    """Main distillation entry point."""
    records = load_records()
    if not records:
        print(json.dumps({'records': 0, 'message': 'No observations to distill'}, indent=2))
        return

    distillable_records = filter_distillable_records(records)
    if not distillable_records:
        print(json.dumps({'records': len(records), 'distillable': 0, 'message': 'No usable observations to distill'}, indent=2))
        return

    # Deduplicate similar observations
    deduped = deduplicate_observations(distillable_records)

    # Detect patterns
    patterns = detect_patterns(deduped)

    # Build structured facets
    facets = build_facets(distillable_records, deduped)
    FACETS.write_text(json.dumps(facets, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    # Generate narrative documents
    write(SELF_MODEL, generate_self_model(deduped, patterns))
    write(VOICE, generate_voice_profile(deduped))
    write(GOALS, generate_goals_doc(deduped))
    write(RELATIONSHIPS, generate_relationships_doc(deduped))

    # Update manifest
    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    else:
        manifest = {'name': 'relic', 'version': 1, 'createdAt': now(), 'mode': 'local-first'}
    manifest['updatedAt'] = now()
    manifest['stats'] = {
        'totalObservations': len(records),
        'distillableObservations': len(distillable_records),
        'uniqueObservations': len(deduped),
        'patternsDetected': len(patterns)
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    # Output summary
    result = {
        'records': len(records),
        'distillable': len(distillable_records),
        'deduped': len(deduped),
        'patterns': len(patterns),
        'facetsPath': str(FACETS),
        'selfModelPath': str(SELF_MODEL),
        'topPatterns': list(patterns.keys())[:5] if patterns else []
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()