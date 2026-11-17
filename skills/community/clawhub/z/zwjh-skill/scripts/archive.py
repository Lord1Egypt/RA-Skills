# -*- coding: utf-8 -*-
"""
自动归档策略 —— 冷热分层 + 时间衰减，自动控制记忆膨胀。

核心算法：
  记忆热度分 = 0.6 * ln(access_count + 1) + 0.4 * exp(-days_since_access / 30)

  热 (score ≥ 0.7): 保持原样，不处理
  温 (0.3 ≤ score < 0.7): 抽取式摘要（保留关键句），存入 archive 表
  冷 (score < 0.3): 仅保留事实抽取结果，高压缩比归档

自动触发: autopilot 末尾自动调用 archive.run()
硬件感知: 批处理大小按 hardware.tier 分配
"""

from __future__ import annotations

import json
import math
import os
import re
import sqlite3
from collections import Counter
from datetime import datetime, timedelta

from . import config, embeddings, store
from .hardware import get_plan


# ── 热度分层阈值 ─────────────────────────────────────────────────────────
HOT_THRESHOLD = 0.7       # ≥ 此值为热
WARM_THRESHOLD = 0.3      # ≥ 此值为温，< 此值为冷

# 时间衰减半衰期（天）
DECAY_HALF_LIFE = 30


def compute_heat(access_count: int, days_since_access: float) -> float:
    """
    计算记忆热度分（0~1）。
    
    公式：0.6 * ln(access_count + 1) + 0.4 * exp(-days / 30)
    - access_count 越大，热度越高（对数增长，避免刷屏）
    - days_since_access 越大，热度越低（指数衰减）
    """
    freq_score = math.log(access_count + 1)  # ln(1)=0, ln(2)=0.69, ln(5)=1.61
    # 归一化到 0~1（ln(10)≈2.3 作为上限）
    freq_normalized = min(freq_score / 2.3, 1.0)
    decay_score = math.exp(-days_since_access / DECAY_HALF_LIFE)
    return 0.6 * freq_normalized + 0.4 * decay_score


def classify_tier(heat: float) -> str:
    """根据热度分返回 hot / warm / cold。"""
    if heat >= HOT_THRESHOLD:
        return "hot"
    if heat >= WARM_THRESHOLD:
        return "warm"
    return "cold"


# ── 归档器 ─────────────────────────────────────────────────────────────────
class Archiver:
    """自动归档器。"""

    def __init__(self):
        self._ensure_archive_table()

    def _ensure_archive_table(self) -> None:
        """确保归档表存在。"""
        conn = store.get_conn()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS archive (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_id INTEGER NOT NULL,
                original_text TEXT,                -- 原始文本（冷归档时保留备份）
                compressed_text TEXT NOT NULL,     -- 压缩后的文本
                tier TEXT NOT NULL,                -- hot / warm / cold
                heat_score REAL NOT NULL,
                archived_at TEXT NOT NULL,
                FOREIGN KEY(memory_id) REFERENCES memories(id) ON DELETE CASCADE
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_archive_memory ON archive(memory_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_archive_tier ON archive(tier)")
        conn.commit()

    def analyze(self) -> dict:
        """
        分析所有记忆的热度分布，返回统计信息。
        不修改任何数据。
        """
        conn = store.get_conn()
        rows = conn.execute(
            "SELECT id, raw_text, access_count, last_accessed FROM memories"
        ).fetchall()

        now = datetime.now()
        tiers = {"hot": 0, "warm": 0, "cold": 0}
        heat_scores = []

        for r in rows:
            last_access = datetime.fromisoformat(r["last_accessed"]) if r["last_accessed"] else now
            days_since = (now - last_access).days + (now - last_access).seconds / 86400.0
            heat = compute_heat(r["access_count"] or 0, days_since)
            tier = classify_tier(heat)
            tiers[tier] += 1
            heat_scores.append(heat)

        return {
            "total": len(rows),
            "tiers": tiers,
            "avg_heat": round(sum(heat_scores) / max(len(heat_scores), 1), 4),
            "min_heat": round(min(heat_scores) if heat_scores else 0, 4),
            "max_heat": round(max(heat_scores) if heat_scores else 0, 4),
        }

    def run(self, dry_run: bool = True) -> dict:
        """
        执行归档。
        
        dry_run=True: 只返回计划，不修改数据
        dry_run=False: 真正执行归档
        
        策略：
        - 热记忆：跳过
        - 温记忆：抽取式摘要（保留关键句），存入 archive 表
        - 冷记忆：高压缩比归档（仅保留事实抽取结果），存入 archive 表
        """
        plan = get_plan()
        batch_size = plan.get("batch_size", 60)

        conn = store.get_conn()
        rows = conn.execute(
            "SELECT id, raw_text, access_count, last_accessed, tokens_json FROM memories"
        ).fetchall()

        now = datetime.now()
        archived = {"hot": 0, "warm": 0, "cold": 0}
        archived_details = []

        for r in rows:
            last_access = datetime.fromisoformat(r["last_accessed"]) if r["last_accessed"] else now
            days_since = (now - last_access).days + (now - last_access).seconds / 86400.0
            heat = compute_heat(r["access_count"] or 0, days_since)
            tier = classify_tier(heat)

            if tier == "hot":
                archived["hot"] += 1
                continue

            # 检查是否已归档
            existing = conn.execute(
                "SELECT id FROM archive WHERE memory_id=?", (r["id"],)
            ).fetchone()
            if existing:
                archived[tier] += 1
                continue

            # 按热度分层压缩
            if tier == "warm":
                compressed = self._warm_compress(r["raw_text"] or "")
            else:  # cold
                compressed = self._cold_compress(r["raw_text"] or "")

            if not dry_run:
                conn.execute(
                    "INSERT INTO archive(memory_id, original_text, compressed_text, tier, heat_score, archived_at) "
                    "VALUES(?,?,?,?,?,?)",
                    (r["id"], r["raw_text"] if tier == "cold" else None,
                     compressed, tier, heat,
                     now.isoformat(timespec="seconds")),
                )

            archived[tier] += 1
            archived_details.append({
                "memory_id": r["id"],
                "tier": tier,
                "heat": round(heat, 4),
                "compressed_len": len(compressed),
                "original_len": len(r["raw_text"] or ""),
            })

        if not dry_run:
            conn.commit()

        return {
            "dry_run": dry_run,
            "total": len(rows),
            "archived": archived,
            "details": archived_details[:20],  # 只返回前 20 条详情
            "batch_size": batch_size,
            "tier": plan["tier"],
        }

    def _warm_compress(self, text: str) -> str:
        """
        温记忆压缩：抽取式摘要，保留关键句。
        压缩比约 30~50%。
        """
        sents = []
        for s in re.split(r"[。！？\n;；]", text):
            s = s.strip()
            if len(s) >= 6:
                sents.append(s)
        if not sents:
            return text[:100] if text else ""

        # 按 token 频次打分
        freq = Counter()
        for s in sents:
            for tk in embeddings.tokenize(s):
                freq[tk] += 1

        scored = sorted(sents, key=lambda s: sum(freq.get(tk, 0) for tk in embeddings.tokenize(s)),
                        reverse=True)
        # 保留 top-3 关键句
        return "；".join(scored[:3])

    def _cold_compress(self, text: str) -> str:
        """
        冷记忆压缩：仅保留事实抽取结果（实体+谓词+值）。
        压缩比约 70~90%。
        """
        # 极简事实抽取：找「X的Y是Z」模式
        facts = []
        for m in re.finditer(r"([\u4e00-\u9fff]{1,10})的([\u4e00-\u9fff]{1,8})[是为：:]\s*([^\n。；;]{1,30})", text):
            entity, predicate, value = m.groups()
            # 清理首尾噪声
            entity = entity.strip()
            predicate = predicate.strip()
            value = value.strip()
            if entity and predicate and value:
                facts.append("%s的%s是%s" % (entity, predicate, value))

        if facts:
            return " | ".join(facts[:5])  # 最多保留 5 条事实

        # 回退：截断到 50 字
        return text[:50] + "..." if len(text) > 50 else text

    def restore(self, memory_id: int) -> str | None:
        """
        从归档恢复原始文本（仅冷归档有原始文本备份）。
        返回原始文本，若不存在返回 None。
        """
        conn = store.get_conn()
        row = conn.execute(
            "SELECT original_text, tier FROM archive WHERE memory_id=?", (memory_id,)
        ).fetchone()
        if not row:
            return None
        return row["original_text"]  # 冷归档有，温归档为 None

    def get_archive_stats(self) -> dict:
        """获取归档统计信息。"""
        conn = store.get_conn()
        total = conn.execute("SELECT COUNT(*) FROM archive").fetchone()[0]
        by_tier = {}
        for tier in ("hot", "warm", "cold"):
            cnt = conn.execute("SELECT COUNT(*) FROM archive WHERE tier=?", (tier,)).fetchone()[0]
            by_tier[tier] = cnt

        # 计算压缩节省的空间
        orig_total = conn.execute(
            "SELECT SUM(LENGTH(original_text)) FROM archive"
        ).fetchone()[0] or 0
        comp_total = conn.execute(
            "SELECT SUM(LENGTH(compressed_text)) FROM archive"
        ).fetchone()[0] or 0

        saving_pct = (1 - comp_total / max(orig_total, 1)) * 100 if orig_total > 0 else 0

        return {
            "total_archived": total,
            "by_tier": by_tier,
            "original_size_kb": round(orig_total / 1024, 2),
            "compressed_size_kb": round(comp_total / 1024, 2),
            "saving_percent": round(saving_pct, 1),
        }


# ── 便捷函数 ─────────────────────────────────────────────────────────────────
def analyze() -> dict:
    """分析记忆热度分布。"""
    return Archiver().analyze()


def run_archive(dry_run: bool = True) -> dict:
    """执行归档。"""
    return Archiver().run(dry_run=dry_run)


def get_archive_stats() -> dict:
    """获取归档统计。"""
    return Archiver().get_archive_stats()


if __name__ == "__main__":
    import pprint
    print("=== 热度分析 ===")
    pprint.pprint(analyze())
    print("\n=== 归档计划 ===")
    pprint.pprint(run_archive(dry_run=True))
    print("\n=== 归档统计 ===")
    pprint.pprint(get_archive_stats())
