#!/usr/bin/env python3
"""
Relic Self-Improvement - analyze vault state and generate improvements.

This script embodies the "aggressive evolution" mode of relic:
- Analyzes current self-model quality
- Identifies gaps and improvement opportunities
- Generates proposals for self-model updates
- Suggests refinements to the extraction/detection logic
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from vault_paths import get_vault_path

VAULT = get_vault_path()
INBOX = VAULT / 'inbox.ndjson'
FACETS = VAULT / 'facets.json'
SELF_MODEL = VAULT / 'self-model.md'
MANIFEST = VAULT / 'manifest.json'
PROPOSALS = VAULT / 'evolution' / 'proposals'


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_records() -> list[dict[str, Any]]:
    if not INBOX.exists():
        return []
    rows = []
    for line in INBOX.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def analyze_coverage(records: list[dict], facets: dict) -> dict:
    """Analyze how well facets cover the observations."""
    total = len(records)
    if total == 0:
        return {'coverage': 0, 'gaps': [], 'recommendation': 'capture_more'}

    # Count by type
    by_type = {}
    for r in records:
        t = r.get('type', 'unknown')
        by_type[t] = by_type.get(t, 0) + 1

    # Check facet coverage
    facet_counts = {
        'values': len(facets.get('values', [])),
        'preferences': len(facets.get('preferences', [])),
        'goals': len(facets.get('goals', {}).get('active', [])),
        'memories': len(facets.get('memories', [])),
    }

    # Identify gaps
    gaps = []
    if by_type.get('value', 0) > facet_counts['values'] * 1.5:
        gaps.append({'type': 'values', 'issue': 'under-distilled', 'count': by_type.get('value', 0)})
    if by_type.get('preference', 0) > facet_counts['preferences'] * 1.5:
        gaps.append({'type': 'preferences', 'issue': 'under-distilled', 'count': by_type.get('preference', 0)})
    if by_type.get('goal', 0) > facet_counts['goals']:
        gaps.append({'type': 'goals', 'issue': 'under-distilled', 'count': by_type.get('goal', 0)})

    # Calculate coverage score
    total_facets = sum(facet_counts.values())
    coverage = min(1.0, total_facets / max(1, total * 0.3))  # Target: 30% distillation ratio

    return {
        'coverage': coverage,
        'total_observations': total,
        'total_facets': total_facets,
        'by_type': by_type,
        'facet_counts': facet_counts,
        'gaps': gaps,
        'recommendation': 'distill' if gaps else 'capture' if coverage > 0.8 else 'stable'
    }


def analyze_quality(records: list[dict]) -> dict:
    """Analyze quality of captured observations."""
    if not records:
        return {'quality': 0, 'issues': []}

    issues = []

    # Check for low confidence observations
    low_confidence = [r for r in records if r.get('confidence', 1) < 0.6]
    if low_confidence:
        issues.append({'issue': 'low_confidence', 'count': len(low_confidence)})

    # Check for untagged observations
    untagged = [r for r in records if not r.get('tags')]
    if untagged:
        issues.append({'issue': 'missing_tags', 'count': len(untagged)})

    # Check for duplicate-like observations (similar text)
    texts = [r.get('text', '') for r in records]
    avg_length = sum(len(t) for t in texts) / max(1, len(texts))
    short_obs = [r for r in records if len(r.get('text', '')) < avg_length * 0.3]
    if short_obs:
        issues.append({'issue': 'too_brief', 'count': len(short_obs)})

    # Calculate quality score
    quality_factors = [
        1 - len(low_confidence) / max(1, len(records)),
        1 - len(untagged) / max(1, len(records)),
        1 - len(short_obs) / max(1, len(records)) * 0.5,
    ]
    quality = sum(quality_factors) / len(quality_factors)

    return {
        'quality': quality,
        'issues': issues,
        'avg_text_length': avg_length,
        'recommendation': 'review' if quality < 0.7 else 'good'
    }


def analyze_evolution(manifest: dict) -> dict:
    """Analyze relic evolution over time."""
    created = manifest.get('createdAt', '')
    updated = manifest.get('updatedAt', '')

    stats = manifest.get('stats', {})

    return {
        'created': created,
        'last_updated': updated,
        'total_observations': stats.get('totalObservations', 0),
        'unique_observations': stats.get('uniqueObservations', 0),
        'patterns_detected': stats.get('patternsDetected', 0),
        'evolution_rate': stats.get('totalObservations', 0) / max(1, stats.get('uniqueObservations', 1))
    }


def generate_improvement_proposal(coverage: dict, quality: dict, evolution: dict) -> dict:
    """Generate a proposal for self-improvement."""
    ts = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')

    improvements = []

    # Coverage-based improvements
    if coverage['recommendation'] == 'distill':
        improvements.append({
            'action': 'distill',
            'reason': f"Coverage at {coverage['coverage']:.0%}, gaps in: {[g['type'] for g in coverage['gaps']]}",
            'priority': 'high'
        })

    # Quality-based improvements
    if quality['recommendation'] == 'review':
        improvements.append({
            'action': 'review_observations',
            'reason': f"Quality score at {quality['quality']:.0%}, issues: {[i['issue'] for i in quality['issues']]}",
            'priority': 'medium'
        })

    # Evolution-based improvements
    if evolution['total_observations'] > evolution['unique_observations'] * 1.2:
        improvements.append({
            'action': 'deduplicate',
            'reason': f"Evolution rate {evolution['evolution_rate']:.2f} suggests duplicates",
            'priority': 'low'
        })

    proposal = {
        'id': f'improve-{ts}',
        'createdAt': now(),
        'type': 'self_improvement',
        'summary': f"Relic self-improvement: {len(improvements)} actions recommended",
        'improvements': improvements,
        'metrics': {
            'coverage': coverage['coverage'],
            'quality': quality['quality'],
            'total_observations': evolution['total_observations'],
            'patterns': evolution['patterns_detected']
        },
        'next_action': improvements[0]['action'] if improvements else 'monitor'
    }

    return proposal


def main():
    """Run self-improvement analysis."""
    records = load_records()

    facets = {}
    if FACETS.exists():
        facets = json.loads(FACETS.read_text(encoding='utf-8'))

    manifest = {}
    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))

    # Run analyses
    coverage = analyze_coverage(records, facets)
    quality = analyze_quality(records, manifest)
    evolution = analyze_evolution(manifest)

    # Generate proposal
    proposal = generate_improvement_proposal(coverage, quality, evolution)

    # Save proposal
    PROPOSALS.mkdir(parents=True, exist_ok=True)
    proposal_path = PROPOSALS / f"{proposal['id']}.json"
    proposal_path.write_text(json.dumps(proposal, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    # Output summary
    result = {
        'status': 'success',
        'proposal_id': proposal['id'],
        'proposal_path': str(proposal_path),
        'metrics': proposal['metrics'],
        'improvements': proposal['improvements'],
        'next_action': proposal['next_action']
    }
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()