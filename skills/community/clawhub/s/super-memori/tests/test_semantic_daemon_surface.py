#!/usr/bin/env python3
from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from super_memori_common import ensure_semantic_daemon, semantic_daemon_ok, embed_texts  # noqa: E402


def main() -> int:
    ok, err = ensure_semantic_daemon()
    assert ok, err or 'semantic daemon failed to start'
    assert semantic_daemon_ok(), 'semantic daemon health check failed'

    timings = []
    vector_sizes = []
    for _ in range(3):
        start = time.perf_counter()
        vecs = embed_texts(['daemon warmup test'], prefix='query')
        elapsed = time.perf_counter() - start
        assert vecs and len(vecs[0]) > 10, 'expected embedding vector from daemon'
        timings.append(elapsed)
        vector_sizes.append(len(vecs[0]))

    assert len(set(vector_sizes)) == 1, f'expected stable embedding vector size, got {vector_sizes}'
    assert max(timings) < 1.0, f'daemon-backed embedding calls should stay fast after startup, got {timings}'
    assert timings[-1] <= timings[0] + 0.05, f'daemon-backed embedding calls regressed unexpectedly, got {timings}'

    print('[OK] semantic daemon surface passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
