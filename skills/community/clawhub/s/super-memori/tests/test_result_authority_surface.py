#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from super_memori_common import summarize_authority_surface  # noqa: E402


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    exact_results = [{
        'chunk_id': 'chunk-1',
        'source_path': '/tmp/memory/procedural/commands.md',
        'snippet': 'Run ./query-memory.sh --json for exact retrieval',
        'rank': -1.0,
        'fusion_sources': ['lexical'],
    }]
    exact_surface = summarize_authority_surface(exact_results, query='./query-memory.sh', mode_used='exact', degraded=False)
    expect(exact_surface['authoritative_result_present'] is True, 'exact lexical match should remain authoritative')
    expect(exact_surface['low_authority_only'] is False, 'exact lexical match must not be marked low-authority-only')
    expect(exact_surface['results'][0]['match_authority'] == 'exact', 'exact lexical match should classify as exact')

    fallback_results = [{
        'chunk_id': 'grep:/tmp/demo.md:12',
        'source_path': '/tmp/demo.md',
        'snippet': 'heuristic fallback snippet',
    }]
    fallback_surface = summarize_authority_surface(fallback_results, query='vague memory question', mode_used='exact', degraded=True)
    expect(fallback_surface['authoritative_result_present'] is False, 'grep fallback must not claim authoritative result present')
    expect(fallback_surface['low_authority_only'] is True, 'grep fallback should be low-authority-only')
    expect(fallback_surface['requires_low_authority_warning'] is True, 'degraded low-authority-only result should force a warning')
    expect(fallback_surface['results'][0]['match_authority'] == 'fallback', 'grep fallback should classify as fallback')

    hybrid_results = [{
        'chunk_id': 'chunk-h',
        'source_path': '/tmp/hybrid.md',
        'snippet': 'hybrid memory hit',
        'fusion_sources': ['lexical', 'semantic'],
        'semantic_score': 0.81,
        'lexical_rank': -1.3,
    }]
    hybrid_surface = summarize_authority_surface(hybrid_results, query='hybrid memory hit', mode_used='hybrid', degraded=False)
    expect(hybrid_surface['authoritative_result_present'] is True, 'hybrid hit should count as authoritative')
    expect(hybrid_surface['results'][0]['match_authority'] == 'hybrid', 'hybrid hit should classify as hybrid')

    print('[OK] result authority surface passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
