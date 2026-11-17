# -*- coding: utf-8 -*-
"""
记忆健康度 —— 审计 + 压缩 + 快照。

解决「记忆膨胀」痛点：记忆越多越慢、重复越多越乱。
  - audit   : 产出健康度评分与问题清单
  - compact : 合并近似重复、对陈旧记忆做抽取式摘要（可观测、可清理）
  - snapshot: 导出可恢复的完整快照（JSON）

评分模型（0~100）：从满分扣减各类「熵」：
  陈旧记忆占比、孤儿实体（无任何关系）、冲突事实、近似重复。
"""

from __future__ import annotations

import json
import math
import os
import re
from collections import Counter
from datetime import datetime, date, timedelta

from . import config, embeddings, store, version
from .hardware import get_plan


def _db_size_mb() -> float:
    try:
        return os.path.getsize(config.DB_PATH) / (1024.0 * 1024.0)
    except Exception:
        return 0.0


def audit() -> dict:
    plan = get_plan()
    n_mem = store.count_memories()
    n_ent = store.count_entities()
    n_rel = store.count_relations()
    n_conflict = len(store.all_facts_with_conflict())

    # 陈旧记忆
    stale_cut = (datetime.now() - timedelta(days=config.STALE_DAYS)).isoformat(timespec="seconds")
    conn = store.get_conn()
    n_stale = conn.execute(
        "SELECT COUNT(*) FROM memories WHERE last_accessed < ?", (stale_cut,)
    ).fetchone()[0]

    # 孤儿实体（无任何关系）
    orphan = 0
    for e in store.list_entities(limit=5000):
        rels = store.relations_of(e["id"])
        if not rels:
            orphan += 1

    # 近似重复（抽样，避免全量 O(n^2) 卡顿；按硬件档位控制样本）
    near_dup = _estimate_near_dup(plan)

    score = 100.0
    score -= min(30.0, (n_stale / max(n_mem, 1)) * 60)          # 陈旧最多 -30
    score -= min(20.0, (orphan / max(n_ent, 1)) * 30)            # 孤儿最多 -20
    score -= min(15.0, n_conflict * 3)                           # 冲突每个 -3
    score -= min(15.0, near_dup * 2)                             # 近似重复每个 -2
    score = max(0.0, round(score, 1))

    return {
        "tier": plan["tier"],
        "score": score,
        "memories": n_mem,
        "entities": n_ent,
        "relations": n_rel,
        "stale_memories": n_stale,
        "orphan_entities": orphan,
        "conflicting_facts": n_conflict,
        "near_duplicates": near_dup,
        "db_size_mb": round(_db_size_mb(), 2),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }


def _estimate_near_dup(plan: dict, sample: int = 300) -> int:
    """抽样估计近似重复数（控制开销）。"""
    mems = store.all_memory_tokens()
    if len(mems) > sample:
        step = len(mems) // sample
        mems = mems[::step][:sample]
    cnt = 0
    for i in range(len(mems)):
        id_i, toks_i = mems[i]
        set_i = set(toks_i)
        if not set_i:
            continue
        for j in range(i + 1, len(mems)):
            id_j, toks_j = mems[j]
            set_j = set(toks_j)
            if not set_j:
                continue
            jac = embeddings.jaccard(set_i, set_j)
            if jac >= config.NEAR_DUP_JACCARD:
                cnt += 1
    return cnt


def compact(dry_run: bool = True, old_days: int = 60) -> dict:
    """
    压缩：对陈旧记忆做抽取式摘要并合并近似重复。

    dry_run=True 只返回计划，不落库；设为 False 才真正执行。
    压缩是「可观测、可清理」的：先报告，再按需执行。
    """
    plan = get_plan()
    cutoff = (datetime.now() - timedelta(days=old_days)).isoformat(timespec="seconds")
    conn = store.get_conn()
    old = conn.execute(
        "SELECT * FROM memories WHERE created_at < ? AND access_count < 3 ORDER BY day ASC",
        (cutoff,),
    ).fetchall()

    plan_out = []
    # 按天聚合摘要
    by_day: dict[str, list[str]] = {}
    for m in old:
        by_day.setdefault(m["day"], []).append(m["raw_text"] or "")

    for day, texts in by_day.items():
        digest = _extractive_summary(texts, plan)
        plan_out.append({"day": day, "src_count": len(texts), "digest": digest[:200]})
        if not dry_run and not store.has_digest_for_day(day):
            # 仅在该天尚无摘要时落库，避免重复执行 compact 时累加重复摘要
            store.add_memory(
                day, "digest", digest,
                embeddings.norm_hash(embeddings.tokenize("摘要" + day + digest)),
                embeddings.tokenize(digest), importance=0.3,
            )

    if not dry_run:
        store.vacuum()

    return {"dry_run": dry_run, "candidates": len(old),
            "digests": plan_out[:20]}


def _extractive_summary(texts: list[str], plan: dict, max_sent: int = 3) -> str:
    """极简抽取式摘要：按 token 频次给句子打分，取 top-N。零依赖。"""
    sents: list[str] = []
    for t in texts:
        for s in re.split(r"[。！？\n;；]", t):
            s = s.strip()
            if len(s) >= 8:
                sents.append(s)
    if not sents:
        return ""
    freq: Counter = Counter()
    for s in sents:
        for tk in embeddings.tokenize(s):
            freq[tk] += 1
    scored = sorted(sents, key=lambda s: sum(freq[tk] for tk in embeddings.tokenize(s)),
                    reverse=True)
    return "；".join(scored[:max_sent])


def snapshot(out_path: str | None = None) -> str:
    """导出完整快照（实体/关系/事实/配置 + 记忆指纹），供备份/恢复。"""
    config.ensure_dirs()
    if out_path is None:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = str(config.ZWJH_DIR / f"snapshot_{stamp}.json")
    data = {
        "version": version.VERSION,
        "exported_at": datetime.now().isoformat(timespec="seconds"),
        "entities": store.list_entities(limit=100000),
        "relations": _dump_relations(),
        "facts": _dump_facts(),
        "memories": store.dump_memories(),
        "config": config.load_config(),
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return out_path


def _dump_relations() -> list[dict]:
    conn = store.get_conn()
    rows = conn.execute("SELECT * FROM relations").fetchall()
    return [dict(r) for r in rows]


def _dump_facts() -> list[dict]:
    conn = store.get_conn()
    rows = conn.execute("SELECT * FROM facts").fetchall()
    return [dict(r) for r in rows]


if __name__ == "__main__":
    import pprint
    pprint.pprint(audit())
    pprint.pprint(compact(dry_run=True))
