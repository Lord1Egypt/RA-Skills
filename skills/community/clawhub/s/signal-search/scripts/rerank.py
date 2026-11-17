"""scripts/rerank.py - 零依赖语义重排（P2 补强）。

复用 embed.embed / embed.similarity 计算"查询 × 各候选源"的语义相似度，对 (docs, scores)
做重排，把综合分写入 scores[i]["rerank_score"]；编排层截断/汇总在有 rerank_score 时优先
按它排序，从而让"语义相关但被 lexical weighted 排低"的源有机会进入最终 Top-N 并领先呈现。

method 支持：
  - "semantic" : 纯语义余弦（归一化后）
  - "bm25_rrf" : 保留现有 词重叠/词频 基线（等价于按原 weighted 排序，零额外计算）
  - "hybrid"   : 语义余弦 × alpha + 词频基线 × (1-alpha)，两路各自 min-max 归一后融合

零依赖护栏：
  - config.rerank.enabled 默认 false（合约硬门槛），仅开启后介入；
  - SIGNAL_SEARCH_OFFLINE 环境不介入，保护离线 eval；
  - 无 sentence-transformers 时 embed 自动降级为 64 维关键词哈希向量，仍可算余弦，不强制加载重依赖；
  - embed 任意异常均被吞，降级回 lexical 基线，绝不让主检索崩溃。
"""

import os
from typing import Any, Dict, List, Optional, Tuple

_DEFAULT_METHOD = "bm25_rrf"
_DEFAULT_TOP_K = 20
_DEFAULT_ALPHA = 0.5


def _active(cfg: Optional[dict]) -> bool:
    """rerank 是否介入：开启且非离线环境。"""
    if not (cfg or {}).get("rerank", {}).get("enabled", False):
        return False
    if os.environ.get("SIGNAL_SEARCH_OFFLINE"):
        return False
    return True


def _doc_text(d: dict) -> str:
    """候选源的语义表征文本：标题 + 摘要 + 正文（正文过长是噪声，截断到 2000 字）。"""
    parts = [d.get("title", "") or "", d.get("snippet", "") or "", d.get("text", "") or ""]
    text = " ".join(p for p in parts if p).strip()
    return text[:2000]


def _minmax(vals: List[float]) -> List[float]:
    """min-max 归一化到 [0,1]；全平或空时返回全 1（避免除以 0）。"""
    if not vals:
        return []
    lo, hi = min(vals), max(vals)
    if hi - lo < 1e-9:
        return [1.0] * len(vals)
    return [(v - lo) / (hi - lo) for v in vals]


def rerank(
    docs: List[Dict[str, Any]],
    scores: List[Dict[str, Any]],
    query: str,
    cfg: dict,
    tr: Any = None,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """对 (docs, scores) 按语义相关度重排，返回重排后的同序配对列表。

    默认关 / 离线 / 无候选时直接原序返回，保证调用方契约不变；任何异常降级回 lexical 基线。
    """
    if not _active(cfg):
        return docs, scores
    n = min(len(docs), len(scores))
    if n == 0:
        return docs, scores

    rc = (cfg or {}).get("rerank", {}) or {}
    method = rc.get("method", _DEFAULT_METHOD)
    top_k = int(rc.get("top_k", _DEFAULT_TOP_K) or _DEFAULT_TOP_K)
    alpha = float(rc.get("alpha", _DEFAULT_ALPHA))

    docs, scores = docs[:n], scores[:n]
    lex_norm = _minmax([float(s.get("weighted", 0.0) or 0.0) for s in scores])

    # 取向量：任何失败都降级回 lexical 基线（bm25_rrf 语义无效）
    q_vec = None
    d_vecs = None
    try:
        import embed

        q_out = embed.embed([query or ""])
        q_vec = q_out[0] if q_out else None
        d_vecs = embed.embed([_doc_text(d) for d in docs])
        used_st = getattr(embed, "_TRY_ST", False)
    except Exception:
        q_vec, d_vecs, used_st = None, None, False

    if method == "bm25_rrf" or q_vec is None or d_vecs is None:
        keys = lex_norm
        fell_back = q_vec is None or d_vecs is None
    else:
        sem_norm = _minmax([embed.similarity(q_vec, dv) for dv in d_vecs])
        if method == "semantic":
            keys = sem_norm
        else:  # hybrid
            keys = [s * alpha + l * (1.0 - alpha) for s, l in zip(sem_norm, lex_norm)]
        fell_back = False

    order = sorted(range(n), key=lambda i: keys[i], reverse=True)
    reranked = [docs[i] for i in order]
    reranked_scores = [scores[i] for i in order]
    for i, idx in enumerate(order):
        reranked_scores[i]["rerank_score"] = keys[idx]

    if 0 < top_k < len(reranked):
        reranked = reranked[:top_k]
        reranked_scores = reranked_scores[:top_k]

    if tr is not None:
        tr.event(
            "rerank",
            {
                "method": method,
                "alpha": alpha if method == "hybrid" else None,
                "n": len(reranked),
                "semantic_model": bool(used_st),
                "fallback_lexical": fell_back,
            },
        )
    return reranked, reranked_scores
