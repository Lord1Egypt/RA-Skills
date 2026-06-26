#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from super_memori_common import temporal_relational_rerank  # noqa: E402


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    results = [
        {
            'chunk_id': 'bootstrap',
            'source_path': '/tmp/memory/semantic/super-memori-bootstrap.md',
            'memory_type': 'semantic',
            'updated_at': '2026-04-21T00:00:00+0000',
            'reviewed': 1,
            'semantic_score': 0.95,
            'relation_json': {},
            'conflict_status': 'active',
            'source_confidence': 0.84,
            'snippet': 'Installed super_memori candidate runtime on this host.',
        },
        {
            'chunk_id': 'move-plan',
            'source_path': '/tmp/memory/episodic/benchmark-locomo/move-plan.md',
            'memory_type': 'episodic',
            'updated_at': '2026-04-21T00:00:00+0000',
            'reviewed': 1,
            'semantic_score': 0.90,
            'relation_json': {},
            'conflict_status': 'active',
            'source_confidence': 0.78,
            'snippet': 'Mira moved from Tomsk to Irkutsk last month. You are in Irkutsk now.',
        },
    ]
    reranked = temporal_relational_rerank(results, query='Where is Mira living now?', limit=5)
    assert_true(reranked[0]['chunk_id'] == 'move-plan', 'query-anchored benchmark conversation should outrank bootstrap semantic noise')
    assert_true(reranked[0]['query_anchor_multiplier'] > reranked[1]['query_anchor_multiplier'], 'matching document should receive larger query anchor multiplier')
    assert_true(reranked[1]['path_penalty_multiplier'] < 1.0, 'bootstrap path should receive semantic path penalty')
    print('[OK] semantic anchor rerank passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
