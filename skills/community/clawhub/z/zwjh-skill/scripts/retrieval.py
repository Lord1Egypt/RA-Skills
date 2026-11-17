# -*- coding: utf-8 -*-
"""
检索层 —— 混合检索（语义 + 关键词 + 时间）+ RRF 融合 + 可解释召回。

v2.5.0 升级：
  - 三路召回：语义（ONNX BGE）/ 关键词（TF-IDF）/ 时间衰减
  - RRF（Reciprocal Rank Fusion）融合排序
  - 返回结果附命中理由分项（语义分/关键词分/时间分）
  - 无 ONNX 模型时自动回退纯 TF-IDF（行为同旧版）
  - 接口保持向后兼容
"""

from __future__ import annotations

import math
from collections import Counter
from datetime import datetime, timedelta

from . import config, embeddings, store
from .hardware import get_plan


# ── RRF 融合参数 ─────────────────────────────────────────────────────────
RRF_K = 60  # RRF 平滑常数（越大越平滑）

# 混合排序权重
WEIGHT_SEMANTIC = 0.5
WEIGHT_KEYWORD = 0.3
WEIGHT_TIME = 0.2

# 时间衰减半衰期（天）
TIME_DECAY_HALF_LIFE = 30


# ── 语义检索（ONNX BGE） ────────────────────────────────────────────────
def _semantic_search(query: str, top_k: int = 8) -> list[dict]:
    """
    语义检索：使用 ONNX BGE 模型编码 + 暴力余弦检索。
    模型不可用时返回空列表。
    """
    try:
        from . import embedder
    except ImportError:
        return []

    if not embedder.is_model_available():
        return []

    results = embedder.semantic_search(query, top_k=top_k * 2)  # 多取一些供融合
    if not results:
        return []

    conn = store.get_conn()
    enriched = []
    for r in results:
        row = conn.execute("SELECT * FROM memories WHERE id=?", (r["memory_id"],)).fetchone()
        if not row:
            continue
        enriched.append({
            "memory_id": r["memory_id"],
            "day": row["day"],
            "source": row["source"],
            "raw_text": row["raw_text"] or "",
            "semantic_score": r["score"],
        })
    return enriched[:top_k]


# ── 关键词检索（TF-IDF） ────────────────────────────────────────────────
def _keyword_search(query: str, top_k: int = 8) -> list[dict]:
    """
    关键词检索：TF-IDF 余弦相似度（旧版逻辑）。
    """
    plan = get_plan()
    q_tokens = embeddings.tokenize(query)
    if not q_tokens:
        return []
    mem_tokens = store.all_memory_tokens()
    if not mem_tokens:
        return []
    idf = embeddings.build_idf(mem_tokens)
    q_vec = embeddings.tfidf_query(q_tokens, idf)

    batch = plan["batch_size"]
    scored: list[tuple[float, int]] = []
    for i in range(0, len(mem_tokens), batch):
        chunk = mem_tokens[i : i + batch]
        for mid, toks in chunk:
            if not toks:
                continue
            d_vec = embeddings.tf_vector(toks)
            d_tfidf = Counter({t: f * idf.get(t, 1.0) for t, f in d_vec.items()})
            sc = embeddings.cosine(q_vec, d_tfidf)
            if sc > 0:
                scored.append((sc, mid))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:top_k]

    conn = store.get_conn()
    results = []
    for sc, mid in top:
        row = conn.execute("SELECT * FROM memories WHERE id=?", (mid,)).fetchone()
        if not row:
            continue
        results.append({
            "memory_id": mid,
            "day": row["day"],
            "source": row["source"],
            "raw_text": row["raw_text"] or "",
            "keyword_score": round(sc, 4),
        })
    return results


# ── 时间检索（时间衰减） ────────────────────────────────────────────────
def _time_search(query: str, top_k: int = 8) -> list[dict]:
    """
    时间检索：按时间衰减排序，越近的记忆分数越高。
    用于召回时间相关但语义/关键词不直接匹配的记忆。
    """
    mem_tokens = store.all_memory_tokens()
    if not mem_tokens:
        return []

    # 过滤包含查询关键词的记忆
    q_tokens = set(embeddings.tokenize(query))
    conn = store.get_conn()
    now = datetime.now()

    results = []
    for mid, toks in mem_tokens:
        if not toks:
            continue
        # 检查是否包含查询关键词
        if q_tokens and not (q_tokens & set(toks)):
            continue
        row = conn.execute("SELECT * FROM memories WHERE id=?", (mid,)).fetchone()
        if not row:
            continue
        # 计算时间衰减分
        last_access = row["last_accessed"] or row["created_at"]
        if last_access:
            try:
                access_dt = datetime.fromisoformat(last_access)
                days_since = (now - access_dt).days + (now - access_dt).seconds / 86400.0
            except Exception:
                days_since = 365  # 解析失败视为很远
        else:
            days_since = 365
        time_score = math.exp(-days_since / TIME_DECAY_HALF_LIFE)
        results.append({
            "memory_id": mid,
            "day": row["day"],
            "source": row["source"],
            "raw_text": row["raw_text"] or "",
            "time_score": round(time_score, 4),
        })

    # 按时间分排序
    results.sort(key=lambda x: x["time_score"], reverse=True)
    return results[:top_k]


# ── RRF 融合排序 ─────────────────────────────────────────────────────────
def _rrf_fuse(lists: list[list[dict]], top_k: int = 8) -> list[dict]:
    """
    使用 RRF（Reciprocal Rank Fusion）融合多路召回结果。
    
    lists: [语义结果, 关键词结果, 时间结果]
    返回: 融合后的结果列表
    """
    rrf_scores: dict[int, float] = {}
    item_map: dict[int, dict] = {}

    for lst in lists:
        for rank, item in enumerate(lst, 1):
            mid = item["memory_id"]
            # RRF 得分 = Σ 1/(k + rank)
            rrf_scores[mid] = rrf_scores.get(mid, 0.0) + 1.0 / (RRF_K + rank)
            if mid not in item_map:
                item_map[mid] = item

    # 按 RRF 得分排序
    sorted_ids = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)

    results = []
    for mid in sorted_ids[:top_k]:
        item = item_map[mid].copy()
        item["rrf_score"] = round(rrf_scores[mid], 6)
        results.append(item)

    return results


# ── 可解释性：生成命中理由 ──────────────────────────────────────────────
def _generate_explanation(item: dict) -> dict:
    """
    生成命中理由分项。
    
    返回: {semantic, keyword, time, summary}
    """
    explanation = {
        "semantic": item.get("semantic_score"),
        "keyword": item.get("keyword_score"),
        "time": item.get("time_score"),
    }

    # 生成人类可读的摘要
    parts = []
    if explanation["semantic"] is not None and explanation["semantic"] > 0.5:
        parts.append("语义高度相关")
    elif explanation["semantic"] is not None and explanation["semantic"] > 0.3:
        parts.append("语义相关")
    if explanation["keyword"] is not None and explanation["keyword"] > 0.5:
        parts.append("关键词强匹配")
    elif explanation["keyword"] is not None and explanation["keyword"] > 0.2:
        parts.append("关键词匹配")
    if explanation["time"] is not None and explanation["time"] > 0.7:
        parts.append("近期记忆")
    elif explanation["time"] is not None and explanation["time"] > 0.3:
        parts.append("较近记忆")

    explanation["summary"] = " + ".join(parts) if parts else "综合召回"
    return explanation


# ── 混合检索（主入口） ─────────────────────────────────────────────────
def hybrid_search(query: str, top_k: int = 8, day_from: str | None = None,
                 day_to: str | None = None) -> list[dict]:
    """
    混合检索：三路召回 + RRF 融合 + 可解释输出。
    
    返回字段：memory_id, day, source, score, snippet, explanation
      - score: RRF 融合得分
      - explanation: {semantic, keyword, time, summary}
    
    向后兼容：无 ONNX 模型时自动回退纯 TF-IDF。
    """
    # 三路召回
    semantic_results = _semantic_search(query, top_k=top_k)
    keyword_results = _keyword_search(query, top_k=top_k)
    time_results = _time_search(query, top_k=top_k)

    # RRF 融合
    fused = _rrf_fuse([semantic_results, keyword_results, time_results], top_k=top_k * 2)

    # 过滤 + 生成解释
    results = []
    conn = store.get_conn()
    for item in fused:
        day = item.get("day", "")
        if day_from and day < day_from:
            continue
        if day_to and day > day_to:
            continue

        # 获取完整记忆信息
        row = conn.execute("SELECT * FROM memories WHERE id=?", (item["memory_id"],)).fetchone()
        if not row:
            continue

        store.update_access(item["memory_id"])
        text = row["raw_text"] or ""

        explanation = _generate_explanation(item)

        results.append({
            "memory_id": item["memory_id"],
            "day": day,
            "source": row["source"],
            "score": round(item.get("rrf_score", 0.0), 6),
            "snippet": text[:160],
            "explanation": explanation,
            # 保留原始分项得分（供高级用户/调试）
            "semantic_score": explanation["semantic"],
            "keyword_score": explanation["keyword"],
            "time_score": explanation["time"],
        })

    return results[:top_k]


# ── 向后兼容：旧版接口 ─────────────────────────────────────────────────
def semantic_search(query: str, top_k: int = 8, day_from: str | None = None,
                    day_to: str | None = None) -> list[dict]:
    """
    语义检索（向后兼容接口）。
    内部调用 hybrid_search，返回格式与旧版一致。
    """
    return hybrid_search(query, top_k=top_k, day_from=day_from, day_to=day_to)


def timeline_search(day_from: str | None, day_to: str | None,
                    keyword: str | None = None, limit: int = 100) -> list[dict]:
    """
    时间线检索：按日期区间（必填其一）返回记忆，可叠加关键词过滤。
    """
    mems = store.list_memories(day_from=day_from, day_to=day_to, limit=limit)
    out = []
    kw_tokens = embeddings.tokenize(keyword) if keyword else None
    for m in mems:
        if kw_tokens:
            mt = set(embeddings.tokenize(m["raw_text"]))
            if not (set(kw_tokens) & mt):
                continue
        store.update_access(m["id"])
        out.append({
            "memory_id": m["id"],
            "day": m["day"],
            "source": m["source"],
            "snippet": (m["raw_text"] or "")[:160],
        })
    return out


def ask(question: str, top_k: int = 5) -> str:
    """
    给 Agent 用的「记忆问答」：返回拼接后的相关记忆文本，便于直接引用。
    其他 skill 可调用此函数把长期记忆注入自己的上下文。
    """
    hits = hybrid_search(question, top_k=top_k)
    if not hits:
        return "（记忆底座中没有找到相关内容）"
    parts = []
    for h in hits:
        exp = h.get("explanation", {})
        reason = exp.get("summary", "") if exp else ""
        parts.append(f"[{h['day']} · {h['source']} · 相关度 {h['score']}]\n{h['snippet']}")
    return "\n\n".join(parts)


if __name__ == "__main__":
    r = hybrid_search("发布失败 根因", top_k=3)
    for x in r:
        print(x["day"], x["score"], x.get("explanation", {}).get("summary", ""), x["snippet"][:50])
