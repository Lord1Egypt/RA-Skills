"""scripts/batch.py - 批量检索（V11 补强）。逐条调用 orchestrate.retrieve。"""

from typing import Any, Dict, List


def run_batch(
    queries: List[str], constraints: dict = None, cfg: dict = None
) -> List[Dict[str, Any]]:
    import orchestrate

    out = []
    for q in queries:
        out.append(orchestrate.retrieve(q, constraints or {}, cfg=cfg))
    return out
