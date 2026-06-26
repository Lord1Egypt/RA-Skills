#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from super_memori_common import reciprocal_rank_fuse, temporal_relational_rerank  # noqa: E402


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    lexical = [
        {
            'chunk_id': 'older-fact',
            'source_path': '/tmp/older.md',
            'memory_type': 'semantic',
            'updated_at': '2026-01-01T00:00:00+0000',
            'reviewed': 1,
            'rank': -1.2,
            'relation_json': {'supersedes': []},
            'conflict_status': 'superseded',
            'source_confidence': 0.75,
        },
        {
            'chunk_id': 'newer-fact',
            'source_path': '/tmp/newer.md',
            'memory_type': 'semantic',
            'updated_at': '2026-04-10T00:00:00+0000',
            'reviewed': 1,
            'rank': -1.4,
            'relation_json': {'supersedes': ['older-fact']},
            'conflict_status': 'active',
            'source_confidence': 0.92,
        },
    ]
    semantic = [
        {
            'chunk_id': 'older-fact',
            'source_path': '/tmp/older.md',
            'memory_type': 'semantic',
            'updated_at': '2026-01-01T00:00:00+0000',
            'reviewed': 1,
            'semantic_score': 0.87,
            'relation_json': {'supersedes': []},
            'conflict_status': 'superseded',
            'source_confidence': 0.75,
        },
        {
            'chunk_id': 'newer-fact',
            'source_path': '/tmp/newer.md',
            'memory_type': 'semantic',
            'updated_at': '2026-04-10T00:00:00+0000',
            'reviewed': 1,
            'semantic_score': 0.82,
            'relation_json': {'supersedes': ['older-fact']},
            'conflict_status': 'active',
            'source_confidence': 0.92,
        },
    ]

    fused = reciprocal_rank_fuse(lexical, semantic, limit=5)
    reranked = temporal_relational_rerank(fused, limit=5)
    assert_true(reranked[0]['chunk_id'] == 'newer-fact', 'newer superseding fact should outrank older superseded fact')

    contradictory = [
        {
            'chunk_id': 'low-confidence-claim',
            'source_path': '/tmp/claim-a.md',
            'memory_type': 'semantic',
            'updated_at': '2026-04-11T00:00:00+0000',
            'reviewed': 1,
            'fusion_score': 0.020,
            'relation_json': {'contradicts': ['high-confidence-claim']},
            'conflict_status': 'active',
            'source_confidence': 0.45,
        },
        {
            'chunk_id': 'high-confidence-claim',
            'source_path': '/tmp/claim-b.md',
            'memory_type': 'semantic',
            'updated_at': '2026-04-11T00:00:00+0000',
            'reviewed': 1,
            'fusion_score': 0.019,
            'relation_json': {},
            'conflict_status': 'active',
            'source_confidence': 0.93,
        },
    ]
    reranked_conflict = temporal_relational_rerank(contradictory, limit=5)
    assert_true(reranked_conflict[0]['chunk_id'] == 'high-confidence-claim', 'higher-confidence contradictory claim should win')

    print('[OK] temporal retrieval rerank cases passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
