"""
timeline.py - 记忆时间旅行系统
快照 / 差异对比 / 来源追溯

三层能力：
  snapshot — 保存某一时刻的记忆全貌
  diff     — 对比两个时刻，看学到了什么 / 忘记了什么
  blame    — 追溯一条记忆的完整来源链
"""

from __future__ import annotations

import os
import json
import time
import uuid
import hashlib
import logging
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════
# Schema（独立表，不污染主 schema）
# ═══════════════════════════════════════════════════════════
TIMELINE_SCHEMA = """
-- 快照元数据
CREATE TABLE IF NOT EXISTS memory_snapshots (
    snapshot_id     TEXT PRIMARY KEY,
    label           TEXT,                    -- 用户标签（如 "2026-04-01"）
    description     TEXT,                    -- 可选描述
    at_ts           INTEGER NOT NULL,        -- 快照时间点（Unix timestamp）
    memory_count    INTEGER DEFAULT 0,       -- 当时的记忆总数
    high_count      INTEGER DEFAULT 0,       -- high 记忆数
    medium_count    INTEGER DEFAULT 0,
    low_count       INTEGER DEFAULT 0,
    topic_summary   TEXT DEFAULT '{}',       -- JSON: {topic_code: count} 当时的主题分布
    content_hash    TEXT,                    -- 快照内容指纹（用于去重）
    created_at      INTEGER NOT NULL DEFAULT (strftime('%s','now'))
);

-- 快照记忆条目（引用当时存在的记忆）
CREATE TABLE IF NOT EXISTS memory_snapshot_items (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_id     TEXT NOT NULL,
    memory_id       TEXT NOT NULL,
    content         TEXT NOT NULL,            -- 快照时的内容（记忆可能被压缩/修改）
    importance      TEXT NOT NULL,
    topics          TEXT DEFAULT '[]',        -- JSON: 快照时的主题标签
    time_ts         INTEGER NOT NULL,         -- 原始记忆时间
    created_at      INTEGER NOT NULL DEFAULT (strftime('%s','now')),
    FOREIGN KEY (snapshot_id) REFERENCES memory_snapshots(snapshot_id),
    UNIQUE(snapshot_id, memory_id)
);

CREATE INDEX IF NOT EXISTS idx_snap_ts ON memory_snapshots(at_ts);
CREATE INDEX IF NOT EXISTS idx_snap_label ON memory_snapshots(label);
CREATE INDEX IF NOT EXISTS idx_snap_item_sid ON memory_snapshot_items(snapshot_id);
CREATE INDEX IF NOT EXISTS idx_snap_item_mid ON memory_snapshot_items(memory_id);
"""


class MemoryTimeline:
    """记忆时间旅行：snapshot → diff → blame（v8.3 增强版）"""

    def __init__(self, store, llm_fn=None):
        """
        参数:
            store: MemoryStore 实例
            llm_fn: LLM 函数（用于成长总结）
        """
        self.store = store
        self.llm_fn = llm_fn
        self._ensure_timeline_schema()

    def _ensure_timeline_schema(self):
        """建表（幂等）"""
        conn = self.store.conn
        conn.executescript(TIMELINE_SCHEMA)
        conn.commit()

    # ═══════════════════════════════════════════════════════
    # SNAPSHOT — 保存某一时刻的记忆全貌
    # ═══════════════════════════════════════════════════════

    def take_snapshot(self, label: str = None, at_ts: int = None, description: str = None) -> dict:
        """
        在指定时间点创建记忆快照。

        参数:
            label: 快照标签（如 "2026-04-01"，不传则自动生成）
            at_ts: 快照时间点（Unix timestamp，默认 = 现在）
            description: 可选描述

        返回:
            {"snapshot_id": str, "label": str, "memory_count": int, ...}
        """
        at_ts = at_ts or int(time.time())
        label = label or datetime.fromtimestamp(at_ts).strftime("%Y-%m-%d_%H%M")

        # 查询该时间点存在的所有记忆（created_at <= at_ts）
        rows = self.store.conn.execute(
            """SELECT m.*, GROUP_CONCAT(mt.topic_code) as topic_codes
               FROM memories m
               LEFT JOIN memory_topics mt ON m.memory_id = mt.memory_id
               WHERE m.created_at <= ?
               GROUP BY m.memory_id
               ORDER BY m.time_ts DESC""",
            (at_ts,)
        ).fetchall()

        if not rows:
            return {
                "snapshot_id": None,
                "label": label,
                "memory_count": 0,
                "message": "该时间点无记忆",
            }

        # 统计
        counts = {"high": 0, "medium": 0, "low": 0}
        topic_dist = defaultdict(int)
        items = []
        content_parts = []

        for row in rows:
            mem = dict(row)
            imp = mem.get("importance", "medium")
            counts[imp] = counts.get(imp, 0) + 1

            topics_str = mem.get("topic_codes", "") or ""
            topic_list = [t.strip() for t in topics_str.split(",") if t.strip()]
            for t in topic_list:
                topic_dist[t] += 1

            items.append({
                "memory_id": mem["memory_id"],
                "content": mem["content"],
                "importance": imp,
                "topics": topic_list,
                "time_ts": mem["time_ts"],
            })
            content_parts.append(mem["content"])

        # 内容指纹
        fingerprint = hashlib.sha256(
            "|".join(sorted(content_parts)).encode()
        ).hexdigest()[:16]

        snapshot_id = str(uuid.uuid4())[:12]

        # 写入快照元数据
        with self.store.transaction() as conn:
            conn.execute(
                """INSERT INTO memory_snapshots
                   (snapshot_id, label, description, at_ts, memory_count,
                    high_count, medium_count, low_count, topic_summary, content_hash)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (snapshot_id, label, description, at_ts, len(rows),
                 counts["high"], counts["medium"], counts["low"],
                 json.dumps(dict(topic_dist), ensure_ascii=False), fingerprint),
            )

            # 写入快照条目
            for item in items:
                conn.execute(
                    """INSERT OR IGNORE INTO memory_snapshot_items
                       (snapshot_id, memory_id, content, importance, topics, time_ts)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (snapshot_id, item["memory_id"], item["content"],
                     item["importance"], json.dumps(item["topics"], ensure_ascii=False),
                     item["time_ts"]),
                )

        logger.info(f"📸 快照已保存: {label} ({len(rows)} 条记忆)")

        return {
            "snapshot_id": snapshot_id,
            "label": label,
            "at": datetime.fromtimestamp(at_ts).isoformat(),
            "memory_count": len(rows),
            "by_importance": counts,
            "top_topics": dict(sorted(topic_dist.items(), key=lambda x: -x[1])[:10]),
            "content_hash": fingerprint,
        }

    def list_snapshots(self, limit: int = 50) -> list[dict]:
        """列出所有快照（按时间倒序）"""
        rows = self.store.conn.execute(
            """SELECT * FROM memory_snapshots
               ORDER BY at_ts DESC LIMIT ?""",
            (limit,)
        ).fetchall()
        return [dict(r) for r in rows]

    def get_snapshot(self, snapshot_id: str) -> dict | None:
        """获取快照详情（含所有记忆条目）"""
        meta = self.store.conn.execute(
            "SELECT * FROM memory_snapshots WHERE snapshot_id = ?",
            (snapshot_id,)
        ).fetchone()
        if not meta:
            return None

        items = self.store.conn.execute(
            """SELECT memory_id, content, importance, topics, time_ts
               FROM memory_snapshot_items
               WHERE snapshot_id = ?
               ORDER BY time_ts DESC""",
            (snapshot_id,)
        ).fetchall()

        return {
            "meta": dict(meta),
            "memories": [dict(r) for r in items],
        }

    def delete_snapshot(self, snapshot_id: str) -> bool:
        """删除快照"""
        with self.store.transaction() as conn:
            conn.execute("DELETE FROM memory_snapshot_items WHERE snapshot_id = ?", (snapshot_id,))
            conn.execute("DELETE FROM memory_snapshots WHERE snapshot_id = ?", (snapshot_id,))
        return True

    # ═══════════════════════════════════════════════════════
    # DIFF — 对比两个时刻
    # ═══════════════════════════════════════════════════════

    def diff(
        self,
        from_ts: int = None,
        to_ts: int = None,
        from_snapshot: str = None,
        to_snapshot: str = None,
        topic: str = None,
    ) -> dict:
        """
        对比两个时间点的记忆差异。

        支持两种模式：
        1. 按时间戳：from_ts / to_ts
        2. 按快照 ID：from_snapshot / to_snapshot

        返回:
            {
                "added": [...],      # 新增的记忆
                "removed": [...],    # 消失的记忆
                "changed": [...],    # 重要度变化的记忆
                "stats": {...}       # 汇总统计
            }
        """
        # 获取两组记忆 ID 集合
        if from_snapshot and to_snapshot:
            from_ids = self._get_snapshot_memory_ids(from_snapshot)
            to_ids = self._get_snapshot_memory_ids(to_snapshot)
            from_data = self._get_snapshot_data(from_snapshot)
            to_data = self._get_snapshot_data(to_snapshot)
            # 从快照元数据获取时间戳
            from_meta = self.store.conn.execute(
                "SELECT at_ts FROM memory_snapshots WHERE snapshot_id = ?", (from_snapshot,)
            ).fetchone()
            to_meta = self.store.conn.execute(
                "SELECT at_ts FROM memory_snapshots WHERE snapshot_id = ?", (to_snapshot,)
            ).fetchone()
            from_ts = from_meta["at_ts"] if from_meta else 0
            to_ts = to_meta["at_ts"] if to_meta else int(time.time())
        else:
            from_ts = from_ts or 0
            to_ts = to_ts or int(time.time())
            from_data = self._query_memories_at(from_ts, topic)
            to_data = self._query_memories_at(to_ts, topic)
            from_ids = set(from_data.keys())
            to_ids = set(to_data.keys())

        # 差异计算
        added_ids = to_ids - from_ids
        removed_ids = from_ids - to_ids
        common_ids = from_ids & to_ids

        # 新增的记忆
        added = []
        for mid in added_ids:
            mem = to_data.get(mid, {})
            added.append({
                "memory_id": mid,
                "content": mem.get("content", "")[:200],
                "importance": mem.get("importance", "medium"),
                "topics": mem.get("topics", []),
                "time_ts": mem.get("time_ts", 0),
            })
        added.sort(key=lambda x: -x["time_ts"])

        # 消失的记忆
        removed = []
        for mid in removed_ids:
            mem = from_data.get(mid, {})
            removed.append({
                "memory_id": mid,
                "content": mem.get("content", "")[:200],
                "importance": mem.get("importance", "medium"),
            })

        # 重要度变化
        changed = []
        for mid in common_ids:
            old_imp = from_data.get(mid, {}).get("importance", "medium")
            new_imp = to_data.get(mid, {}).get("importance", "medium")
            if old_imp != new_imp:
                changed.append({
                    "memory_id": mid,
                    "content": to_data.get(mid, {}).get("content", "")[:200],
                    "old_importance": old_imp,
                    "new_importance": new_imp,
                })

        # 新增主题分析
        from_topics = defaultdict(int)
        to_topics = defaultdict(int)
        for mem in from_data.values():
            for t in mem.get("topics", []):
                from_topics[t] += 1
        for mem in to_data.values():
            for t in mem.get("topics", []):
                to_topics[t] += 1

        new_topics = {t: c for t, c in to_topics.items() if t not in from_topics}
        grown_topics = {
            t: {"before": from_topics[t], "after": to_topics[t]}
            for t in to_topics
            if t in from_topics and to_topics[t] > from_topics[t]
        }

        # 时间范围
        from datetime import datetime
        from_dt = datetime.fromtimestamp(
            min(m.get("time_ts", to_ts) for m in to_data.values()) if to_data else to_ts
        ).strftime("%Y-%m-%d")
        to_dt = datetime.fromtimestamp(to_ts).strftime("%Y-%m-%d")

        stats = {
            "from_total": len(from_ids),
            "to_total": len(to_ids),
            "net_change": len(added_ids) - len(removed_ids),
            "added_count": len(added_ids),
            "removed_count": len(removed_ids),
            "changed_count": len(changed),
            "new_topics": new_topics,
            "growing_topics": grown_topics,
            "period": f"{from_dt} → {to_dt}",
        }

        return {
            "added": added[:50],       # 上限 50 条
            "removed": removed[:30],
            "changed": changed[:30],
            "stats": stats,
        }

    def diff_natural(self, from_ts: int = None, to_ts: int = None,
                     from_snapshot: str = None, to_snapshot: str = None) -> str:
        """自然语言风格的差异描述"""
        result = self.diff(from_ts, to_ts, from_snapshot, to_snapshot)
        stats = result["stats"]

        lines = [f"📊 记忆变化: {stats['period']}"]
        lines.append(f"  总量: {stats['from_total']} → {stats['to_total']} (净增 {stats['net_change']})")
        lines.append(f"  新增: {stats['added_count']} | 消失: {stats['removed_count']} | 变化: {stats['changed_count']}")

        if result["added"]:
            lines.append(f"\n🆕 新增记忆 ({len(result['added'])} 条，显示前10):")
            for m in result["added"][:10]:
                dt = datetime.fromtimestamp(m["time_ts"]).strftime("%m-%d")
                lines.append(f"  [{dt}] {m['content'][:80]}")

        if result["removed"]:
            lines.append(f"\n🗑️ 消失的记忆 ({len(result['removed'])} 条):")
            for m in result["removed"][:5]:
                lines.append(f"  - {m['content'][:60]}")

        if result["changed"]:
            lines.append(f"\n🔄 重要度变化 ({len(result['changed'])} 条):")
            for m in result["changed"][:5]:
                lines.append(f"  {m['old_importance']} → {m['new_importance']}: {m['content'][:60]}")

        if stats["new_topics"]:
            lines.append(f"\n💡 新出现的主题:")
            for t, c in sorted(stats["new_topics"].items(), key=lambda x: -x[1])[:5]:
                lines.append(f"  {t}: {c} 条")

        if stats["growing_topics"]:
            lines.append(f"\n📈 增长的主题:")
            for t, info in sorted(stats["growing_topics"].items(),
                                   key=lambda x: -(x[1]["after"] - x[1]["before"]))[:5]:
                lines.append(f"  {t}: {info['before']} → {info['after']}")

        return "\n".join(lines)

    # ═══════════════════════════════════════════════════════
    # BLAME — 追溯一条记忆的完整来源链
    # ═══════════════════════════════════════════════════════

    def blame(self, memory_id: str) -> dict:
        """
        追溯一条记忆的完整来源和演化历史。

        返回:
            {
                "memory": {...},           # 记忆本体
                "origin": {...},           # 来源信息
                "lineage": [...],          # 因果链（前因→后果）
                "related": [...],          # 相关记忆
                "snapshots": [...],        # 出现在哪些快照中
                "distill_origin": {...},   # 蒸馏来源（如果是蒸馏产物）
                "version_history": [...],  # 版本变化（基于去重结果）
            }
        """
        # 1. 获取记忆本体
        memory = self.store.get_memory(memory_id)
        if not memory:
            return {"error": f"记忆不存在: {memory_id}"}

        # 2. 来源信息
        from datetime import datetime
        origin = {
            "memory_id": memory_id,
            "created_at": datetime.fromtimestamp(memory["created_at"]).isoformat(),
            "created_at_human": _human_time_ago(memory["created_at"]),
            "memory_time": datetime.fromtimestamp(memory["time_ts"]).isoformat(),
            "memory_time_human": _human_time_ago(memory["time_ts"]),
            "importance": memory.get("importance", "medium"),
            "owner_agent": memory.get("owner_agent_id", "_system"),
            "visibility": memory.get("visibility", "team"),
            "is_aggregated": bool(memory.get("is_aggregated", 0)),
            "source_count": memory.get("source_count", 1),
        }

        # 3. 因果链（memory_links）
        lineage = self._build_lineage(memory_id)

        # 4. 相关记忆（同主题 + 关联记忆）
        related = self._find_related_memories(memory)

        # 5. 快照追溯
        snapshots = self._find_snapshots_for_memory(memory_id)

        # 6. 蒸馏来源
        distill_origin = self._trace_distill_origin(memory_id)

        # 7. 版本历史（检查是否有同 content_hash 的其他版本）
        version_history = self._trace_version_history(memory)

        return {
            "memory": {
                "memory_id": memory_id,
                "content": memory["content"],
                "importance": memory.get("importance"),
                "topics": memory.get("topics", []),
                "tools": memory.get("tools", []),
                "knowledge": memory.get("knowledge", []),
            },
            "origin": origin,
            "lineage": lineage,
            "related": related[:10],
            "snapshots": snapshots,
            "distill_origin": distill_origin,
            "version_history": version_history,
        }

    def blame_natural(self, memory_id: str) -> str:
        """自然语言风格的来源描述"""
        result = self.blame(memory_id)
        if "error" in result:
            return result["error"]

        mem = result["memory"]
        origin = result["origin"]

        lines = [f"🔍 记忆来源追溯"]
        lines.append(f"  ID: {mem['memory_id']}")
        lines.append(f"  内容: {mem['content'][:100]}")
        lines.append(f"  创建: {origin['created_at_human']} ({origin['created_at'][:10]})")
        lines.append(f"  记忆时间: {origin['memory_time_human']}")
        lines.append(f"  重要度: {origin['importance']}")

        if origin["is_aggregated"]:
            lines.append(f"  📦 聚合记忆（合并了 {origin['source_count']} 条）")

        if origin["owner_agent"] != "_system":
            lines.append(f"  🤖 来源 Agent: {origin['owner_agent']}")

        # 因果链
        if result["lineage"]["causes"]:
            lines.append(f"\n  ⛓️ 前因（由什么触发）:")
            for c in result["lineage"]["causes"][:5]:
                lines.append(f"    ← [{c['link_type']}] {c['content'][:60]}")

        if result["lineage"]["effects"]:
            lines.append(f"\n  🔗 后果（触发了什么）:")
            for e in result["lineage"]["effects"][:5]:
                lines.append(f"    → [{e['link_type']}] {e['content'][:60]}")

        # 相关记忆
        if result["related"]:
            lines.append(f"\n  📎 相关记忆 ({len(result['related'])} 条):")
            for r in result["related"][:5]:
                lines.append(f"    • {r['content'][:60]} (相似度 {r['score']:.2f})")

        # 快照
        if result["snapshots"]:
            lines.append(f"\n  📸 存在于 {len(result['snapshots'])} 个快照:")
            for s in result["snapshots"][:5]:
                lines.append(f"    • {s['label']} ({s['at'][:10]})")

        # 蒸馏来源
        if result["distill_origin"]:
            do = result["distill_origin"]
            lines.append(f"\n  🧪 蒸馏来源:")
            lines.append(f"    来自主题: {do.get('topic_code', 'N/A')}")
            if do.get("source_memory_count"):
                lines.append(f"    基于 {do['source_memory_count']} 条原始记忆")

        # 版本变化
        if result["version_history"]:
            lines.append(f"\n  📜 版本历史:")
            for v in result["version_history"][:5]:
                lines.append(f"    v{v['version']}: {v['content'][:50]} ({v['timestamp'][:10]})")

        return "\n".join(lines)

    # ═══════════════════════════════════════════════════════
    # 内部方法
    # ═══════════════════════════════════════════════════════

    def _query_memories_at(self, at_ts: int, topic: str = None) -> dict[str, dict]:
        """查询 at_ts 之前存在的所有记忆，返回 {memory_id: data}"""
        if topic:
            rows = self.store.conn.execute(
                """SELECT m.*, GROUP_CONCAT(mt.topic_code) as topic_codes
                   FROM memories m
                   LEFT JOIN memory_topics mt ON m.memory_id = mt.memory_id
                   WHERE m.created_at <= ?
                   GROUP BY m.memory_id
                   HAVING topic_codes LIKE ?""",
                (at_ts, f"%{topic}%")
            ).fetchall()
        else:
            rows = self.store.conn.execute(
                """SELECT m.*, GROUP_CONCAT(mt2.topic_code) as topic_codes
                   FROM memories m
                   LEFT JOIN memory_topics mt2 ON m.memory_id = mt2.memory_id
                   WHERE m.created_at <= ?
                   GROUP BY m.memory_id""",
                (at_ts,)
            ).fetchall()

        result = {}
        for row in rows:
            mem = dict(row)
            topics_str = mem.pop("topic_codes", "") or ""
            mem["topics"] = [t.strip() for t in topics_str.split(",") if t.strip()]
            result[mem["memory_id"]] = mem
        return result

    def _get_snapshot_memory_ids(self, snapshot_id: str) -> set[str]:
        """获取快照中的记忆 ID 集合"""
        rows = self.store.conn.execute(
            "SELECT memory_id FROM memory_snapshot_items WHERE snapshot_id = ?",
            (snapshot_id,)
        ).fetchall()
        return {r["memory_id"] for r in rows}

    def _get_snapshot_data(self, snapshot_id: str) -> dict[str, dict]:
        """获取快照中的记忆数据 {memory_id: data}"""
        rows = self.store.conn.execute(
            """SELECT memory_id, content, importance, topics, time_ts
               FROM memory_snapshot_items WHERE snapshot_id = ?""",
            (snapshot_id,)
        ).fetchall()
        result = {}
        for r in rows:
            mem = dict(r)
            mem["topics"] = json.loads(mem.get("topics", "[]") or "[]")
            result[mem["memory_id"]] = mem
        return result

    def _build_lineage(self, memory_id: str) -> dict:
        """构建因果链（前因 + 后果）"""
        # 前因（我是 target 的链接）
        causes_rows = self.store.conn.execute(
            """SELECT ml.*, m.content as source_content
               FROM memory_links ml
               JOIN memories m ON ml.source_id = m.memory_id
               WHERE ml.target_id = ?
               ORDER BY ml.weight DESC""",
            (memory_id,)
        ).fetchall()

        # 后果（我是 source 的链接）
        effects_rows = self.store.conn.execute(
            """SELECT ml.*, m.content as target_content
               FROM memory_links ml
               JOIN memories m ON ml.target_id = m.memory_id
               WHERE ml.source_id = ?
               ORDER BY ml.weight DESC""",
            (memory_id,)
        ).fetchall()

        causes = [dict(r) for r in causes_rows]
        effects = [dict(r) for r in effects_rows]

        return {
            "causes": [
                {
                    "memory_id": r["source_id"],
                    "content": r["source_content"],
                    "link_type": r["link_type"],
                    "weight": r["weight"],
                    "reason": r.get("reason"),
                }
                for r in causes
            ],
            "effects": [
                {
                    "memory_id": r["target_id"],
                    "content": r["target_content"],
                    "link_type": r["link_type"],
                    "weight": r["weight"],
                    "reason": r.get("reason"),
                }
                for r in effects
            ],
        }

    def _find_related_memories(self, memory: dict) -> list[dict]:
        """找相关记忆（同主题 + 同时间窗口）"""
        mid = memory["memory_id"]
        time_ts = memory["time_ts"]
        topics = memory.get("topics", [])

        # 同主题记忆
        related = []
        seen_ids = {mid}

        if topics:
            topic_codes = [t.get("code", t) if isinstance(t, dict) else t for t in topics[:3]]
            for tc in topic_codes:
                rows = self.store.conn.execute(
                    """SELECT m.memory_id, m.content, m.time_ts
                       FROM memories m
                       JOIN memory_topics mt ON m.memory_id = mt.memory_id
                       WHERE mt.topic_code = ? AND m.memory_id != ?
                       ORDER BY ABS(m.time_ts - ?) LIMIT 5""",
                    (tc, mid, time_ts)
                ).fetchall()
                for r in rows:
                    rid = r["memory_id"]
                    if rid not in seen_ids:
                        seen_ids.add(rid)
                        related.append({
                            "memory_id": rid,
                            "content": r["content"][:150],
                            "time_ts": r["time_ts"],
                            "score": 0.8,
                            "reason": f"同主题: {tc}",
                        })

        # 时间窗口内相邻记忆
        window_rows = self.store.conn.execute(
            """SELECT memory_id, content, time_ts
               FROM memories
               WHERE memory_id != ? AND ABS(time_ts - ?) < 3600
               ORDER BY ABS(time_ts - ?)
               LIMIT 5""",
            (mid, time_ts, time_ts)
        ).fetchall()
        for r in window_rows:
            rid = r["memory_id"]
            if rid not in seen_ids:
                seen_ids.add(rid)
                hours_ago = abs(r["time_ts"] - time_ts) / 3600
                related.append({
                    "memory_id": rid,
                    "content": r["content"][:150],
                    "time_ts": r["time_ts"],
                    "score": max(0.5, 1.0 - hours_ago),
                    "reason": f"时间相邻 ({hours_ago:.1f}h)",
                })

        related.sort(key=lambda x: -x["score"])
        return related

    def _find_snapshots_for_memory(self, memory_id: str) -> list[dict]:
        """查找记忆出现在哪些快照中"""
        rows = self.store.conn.execute(
            """SELECT s.snapshot_id, s.label, s.at_ts, s.memory_count
               FROM memory_snapshots s
               JOIN memory_snapshot_items si ON s.snapshot_id = si.snapshot_id
               WHERE si.memory_id = ?
               ORDER BY s.at_ts DESC""",
            (memory_id,)
        ).fetchall()
        return [
            {
                "snapshot_id": r["snapshot_id"],
                "label": r["label"],
                "at": datetime.fromtimestamp(r["at_ts"]).isoformat(),
                "total_memories": r["memory_count"],
            }
            for r in rows
        ]

    def _trace_distill_origin(self, memory_id: str) -> dict | None:
        """追溯蒸馏来源（如果有的话）"""
        try:
            # 检查 distill_topics 表中哪些包含了这个 memory
            rows = self.store.conn.execute(
                """SELECT topic_id, topic_code, summary, source_count, source_ids
                   FROM distill_topics
                   WHERE source_ids LIKE ?""",
                (f"%{memory_id}%",)
            ).fetchall()

            if rows:
                r = rows[0]
                return {
                    "topic_id": r["topic_id"],
                    "topic_code": r["topic_code"],
                    "summary_preview": (r["summary"] or "")[:200],
                    "source_memory_count": r["source_count"],
                }
        except Exception as e:
            logger.warning("timeline: %s", e)
        return None

    def _trace_version_history(self, memory: dict) -> list[dict]:
        """追溯版本变化 — 优先查 memory_versions 表，fallback 到 content_hash"""
        mid = memory["memory_id"]
        versions = []

        # 方式1: 查 memory_versions 表（v6.0 版本化功能）
        try:
            rows = self.store.conn.execute(
                """SELECT version_id, content, importance, change_reason, created_at, is_current
                   FROM memory_versions
                   WHERE memory_id = ?
                   ORDER BY version_id ASC""",
                (mid,)
            ).fetchall()

            if rows:
                for r in rows:
                    versions.append({
                        "version": r["version_id"],
                        "memory_id": mid,
                        "content": (r["content"] or "")[:100],
                        "importance": r["importance"],
                        "timestamp": datetime.fromtimestamp(r["created_at"]).isoformat() if r["created_at"] else None,
                        "change_reason": r.get("change_reason"),
                        "is_current": bool(r.get("is_current", 0)),
                    })
                return versions
        except Exception as e:
            logger.warning("timeline: %s", e)

        # 方式2: fallback — 基于 content_hash 去重关联
        content_hash = memory.get("content_hash")
        if not content_hash:
            return []

        rows = self.store.conn.execute(
            """SELECT memory_id, content, importance, time_ts, created_at
               FROM memories
               WHERE content_hash = ? AND memory_id != ?
               ORDER BY created_at ASC""",
            (content_hash, mid)
        ).fetchall()

        for i, r in enumerate(rows):
            versions.append({
                "version": i + 1,
                "memory_id": r["memory_id"],
                "content": r["content"][:100],
                "importance": r["importance"],
                "timestamp": datetime.fromtimestamp(r["created_at"]).isoformat(),
            })

        # 加上当前记忆作为最新版本
        versions.append({
            "version": len(versions) + 1,
            "memory_id": mid,
            "content": memory["content"][:100],
            "importance": memory.get("importance", "medium"),
            "timestamp": datetime.fromtimestamp(memory["created_at"]).isoformat(),
            "is_current": True,
        })

        return versions

    # ═══════════════════════════════════════════════════════
    # v8.3: 成长快照（增强版快照，含情感/认知状态）
    # ═══════════════════════════════════════════════════════

    def take_growth_snapshot(self, label: str = None, at_ts: int = None) -> dict:
        """
        创建成长快照：在普通快照基础上增加情感/认知状态分析。

        额外记录：
        1. 情感状态分布（正面/中性/负面比例）
        2. 认知活跃度（最近7天的新记忆数）
        3. 知识覆盖度（有记忆的主题数 / 总注册主题数）
        4. 关键成就（importance=high/breakthrough 的记忆）

        参数:
            label: 快照标签
            at_ts: 快照时间点

        返回: 增强版快照信息
        """
        at_ts = at_ts or int(time.time())
        label = label or f"成长_{datetime.fromtimestamp(at_ts).strftime('%Y-%m-%d')}"

        base_snapshot = self.take_snapshot(label=label, at_ts=at_ts, description="成长快照")
        if not base_snapshot.get("snapshot_id"):
            return base_snapshot

        growth_data = self._compute_growth_metrics(at_ts)

        try:
            self.store.conn.execute(
                "UPDATE memory_snapshots SET description = ? WHERE snapshot_id = ?",
                (json.dumps(growth_data, ensure_ascii=False), base_snapshot["snapshot_id"]),
            )
        except Exception as e:
            logger.warning("timeline: %s", e)

        return {**base_snapshot, "growth_metrics": growth_data}

    def _compute_growth_metrics(self, at_ts: int) -> dict:
        """计算成长指标"""
        seven_days_ago = at_ts - 7 * 86400
        thirty_days_ago = at_ts - 30 * 86400

        try:
            recent_count = self.store.conn.execute(
                "SELECT COUNT(*) FROM memories WHERE time_ts >= ? AND time_ts <= ?",
                (seven_days_ago, at_ts),
            ).fetchone()[0]

            total_count = self.store.conn.execute(
                "SELECT COUNT(*) FROM memories WHERE time_ts <= ?",
                (at_ts,),
            ).fetchone()[0]

            positive = self.store.conn.execute(
                "SELECT COUNT(*) FROM memories WHERE valence > 0.2 AND time_ts <= ?",
                (at_ts,),
            ).fetchone()[0]

            negative = self.store.conn.execute(
                "SELECT COUNT(*) FROM memories WHERE valence < -0.2 AND time_ts <= ?",
                (at_ts,),
            ).fetchone()[0]

            achievements = self.store.conn.execute(
                "SELECT content, time_ts FROM memories "
                "WHERE importance IN ('high', 'breakthrough', 'milestone') "
                "AND time_ts >= ? AND time_ts <= ? ORDER BY time_ts DESC LIMIT 5",
                (thirty_days_ago, at_ts),
            ).fetchall()

            topic_count = self.store.conn.execute(
                "SELECT COUNT(DISTINCT topic_code) FROM memory_topics mt "
                "JOIN memories m ON mt.memory_id = m.memory_id WHERE m.time_ts <= ?",
                (at_ts,),
            ).fetchone()[0]

            avg_confidence = self.store.conn.execute(
                "SELECT AVG(confidence) FROM memories WHERE time_ts <= ?",
                (at_ts,),
            ).fetchone()[0] or 0.5

        except Exception:
            return {}

        neutral = max(0, total_count - positive - negative)
        return {
            "cognitive_activity": {
                "recent_7d_count": recent_count,
                "total_count": total_count,
                "activity_ratio": round(recent_count / max(1, total_count), 3),
            },
            "emotion_distribution": {
                "positive": positive,
                "neutral": neutral,
                "negative": negative,
                "positive_ratio": round(positive / max(1, total_count), 3),
            },
            "knowledge_coverage": {
                "active_topics": topic_count,
                "avg_confidence": round(avg_confidence, 3),
            },
            "recent_achievements": [
                {"content": r["content"][:100], "time_ts": r["time_ts"]}
                for r in (achievements or [])
            ],
        }

    # ═══════════════════════════════════════════════════════
    # v8.3: 增量总结（两个快照之间的成长总结）
    # ═══════════════════════════════════════════════════════

    def growth_summary(
        self,
        from_snapshot: str = None,
        to_snapshot: str = None,
        from_ts: int = None,
        to_ts: int = None,
        use_llm: bool = True,
    ) -> dict:
        """
        生成两个时间点之间的成长总结。

        参数:
            from_snapshot/to_snapshot: 快照 ID
            from_ts/to_ts: 时间戳（如果没有快照）
            use_llm: 是否使用 LLM 生成自然语言总结

        返回: {
            "period": str,
            "diff": dict,
            "growth_indicators": dict,
            "narrative": str,
        }
        """
        diff_result = self.diff(
            from_ts=from_ts, to_ts=to_ts,
            from_snapshot=from_snapshot, to_snapshot=to_snapshot,
        )

        from_growth = self._compute_growth_metrics(from_ts or 0)
        to_growth = self._compute_growth_metrics(to_ts or int(time.time()))

        growth_indicators = self._compute_growth_delta(from_growth, to_growth)

        narrative = ""
        if use_llm and self.llm_fn:
            narrative = self._generate_growth_narrative(diff_result, growth_indicators)
        else:
            narrative = self._generate_rule_based_narrative(diff_result, growth_indicators)

        return {
            "period": diff_result.get("stats", {}).get("period", ""),
            "diff": diff_result,
            "growth_indicators": growth_indicators,
            "from_metrics": from_growth,
            "to_metrics": to_growth,
            "narrative": narrative,
        }

    def _compute_growth_delta(self, from_metrics: dict, to_metrics: dict) -> dict:
        """计算两个时间点的成长增量"""
        if not from_metrics or not to_metrics:
            return {"delta_available": False}

        from_activity = from_metrics.get("cognitive_activity", {})
        to_activity = to_metrics.get("cognitive_activity", {})
        from_emotion = from_metrics.get("emotion_distribution", {})
        to_emotion = to_metrics.get("emotion_distribution", {})
        from_knowledge = from_metrics.get("knowledge_coverage", {})
        to_knowledge = to_metrics.get("knowledge_coverage", {})

        return {
            "delta_available": True,
            "memory_growth": to_activity.get("total_count", 0) - from_activity.get("total_count", 0),
            "activity_change": to_activity.get("recent_7d_count", 0) - from_activity.get("recent_7d_count", 0),
            "emotion_shift": round(
                to_emotion.get("positive_ratio", 0) - from_emotion.get("positive_ratio", 0), 3
            ),
            "topic_growth": to_knowledge.get("active_topics", 0) - from_knowledge.get("active_topics", 0),
            "confidence_change": round(
                to_knowledge.get("avg_confidence", 0.5) - from_knowledge.get("avg_confidence", 0.5), 3
            ),
            "new_achievements": len(to_metrics.get("recent_achievements", [])),
        }

    def _generate_rule_based_narrative(self, diff_result: dict, growth: dict) -> str:
        """基于规则生成成长叙事"""
        parts = []
        stats = diff_result.get("stats", {})

        net = stats.get("net_change", 0)
        if net > 0:
            parts.append(f"记忆总量增长了 {net} 条")
        elif net < 0:
            parts.append(f"记忆总量减少了 {abs(net)} 条")

        if growth.get("delta_available"):
            topic_g = growth.get("topic_growth", 0)
            if topic_g > 0:
                parts.append(f"涉足的主题领域增加了 {topic_g} 个")

            emotion_shift = growth.get("emotion_shift", 0)
            if emotion_shift > 0.1:
                parts.append("整体情绪倾向更加积极")
            elif emotion_shift < -0.1:
                parts.append("整体情绪倾向有所下降")

            conf_change = growth.get("confidence_change", 0)
            if conf_change > 0.05:
                parts.append("知识置信度有所提升")
            elif conf_change < -0.05:
                parts.append("知识置信度有所下降，可能遇到了新的不确定问题")

        new_topics = stats.get("new_topics", {})
        if new_topics:
            top_new = sorted(new_topics.items(), key=lambda x: -x[1])[:3]
            parts.append(f"新探索的主题: {', '.join(t for t, _ in top_new)}")

        return "；".join(parts) + "。" if parts else "该时间段内无明显变化。"

    def _generate_growth_narrative(self, diff_result: dict, growth: dict) -> str:
        """用 LLM 生成成长叙事"""
        if not self.llm_fn:
            return self._generate_rule_based_narrative(diff_result, growth)

        stats = diff_result.get("stats", {})
        added = diff_result.get("added", [])[:5]
        added_summary = "\n".join(
            f"- {m.get('content', '')[:80]}" for m in added
        )

        growth_text = json.dumps(growth, ensure_ascii=False, indent=2) if growth else "无数据"

        prompt = f"""基于以下记忆系统的变化数据，写一段成长总结（100-200字）。

时间段: {stats.get('period', '未知')}
记忆变化: 净增 {stats.get('net_change', 0)} 条
新增主题: {list(stats.get('new_topics', {}).keys())[:5]}
增长的主题: {list(stats.get('growing_topics', {}).keys())[:5]}

新增记忆摘要:
{added_summary}

成长指标:
{growth_text}

要求：用第二人称（"你"），语气温暖但客观，突出关键变化和成长。"""

        try:
            return self.llm_fn(prompt)
        except Exception:
            return self._generate_rule_based_narrative(diff_result, growth)

    # ═══════════════════════════════════════════════════════
    # v8.3: 时间点回溯（查看任意时间点的认知状态）
    # ═══════════════════════════════════════════════════════

    def recall_at(
        self,
        at_ts: int,
        topic: str = None,
        limit: int = 20,
    ) -> dict:
        """
        回溯到指定时间点，查看当时的认知状态。

        参数:
            at_ts: 目标时间点（Unix timestamp）
            topic: 限定主题
            limit: 返回条数

        返回: {
            "at": str,
            "total_memories": int,
            "memories": [dict],
            "emotion_snapshot": dict,
            "topic_distribution": dict,
            "key_memories": [dict],
        }
        """
        memories_data = self._query_memories_at(at_ts, topic)

        if not memories_data:
            return {
                "at": datetime.fromtimestamp(at_ts).isoformat(),
                "total_memories": 0,
                "memories": [],
                "emotion_snapshot": {},
                "topic_distribution": {},
                "key_memories": [],
            }

        all_mems = list(memories_data.values())
        all_mems.sort(key=lambda x: x.get("time_ts", 0), reverse=True)

        emotion_snapshot = self._compute_emotion_snapshot(all_mems)
        topic_dist = defaultdict(int)
        for m in all_mems:
            for t in m.get("topics", []):
                topic_dist[t] += 1

        key_memories = [
            m for m in all_mems
            if m.get("importance") in ("high", "breakthrough", "milestone")
        ][:5]

        return {
            "at": datetime.fromtimestamp(at_ts).isoformat(),
            "total_memories": len(all_mems),
            "memories": [
                {
                    "memory_id": m.get("memory_id"),
                    "content": (m.get("content") or "")[:200],
                    "importance": m.get("importance", "medium"),
                    "time_ts": m.get("time_ts", 0),
                    "valence": m.get("valence", 0.0),
                }
                for m in all_mems[:limit]
            ],
            "emotion_snapshot": emotion_snapshot,
            "topic_distribution": dict(sorted(topic_dist.items(), key=lambda x: -x[1])[:15]),
            "key_memories": [
                {
                    "memory_id": m.get("memory_id"),
                    "content": (m.get("content") or "")[:150],
                    "importance": m.get("importance"),
                    "time_ts": m.get("time_ts", 0),
                }
                for m in key_memories
            ],
        }

    def _compute_emotion_snapshot(self, memories: list[dict]) -> dict:
        """计算记忆集合的情感快照"""
        if not memories:
            return {}

        valences = [m.get("valence", 0.0) for m in memories if m.get("valence") is not None]
        arousals = [m.get("arousal", 0.2) for m in memories if m.get("arousal") is not None]

        if not valences:
            return {"average_valence": 0.0, "average_arousal": 0.2}

        avg_valence = sum(valences) / len(valences)
        avg_arousal = sum(arousals) / len(arousals) if arousals else 0.2

        positive = sum(1 for v in valences if v > 0.2)
        negative = sum(1 for v in valences if v < -0.2)
        neutral = len(valences) - positive - negative

        return {
            "average_valence": round(avg_valence, 3),
            "average_arousal": round(avg_arousal, 3),
            "positive_count": positive,
            "neutral_count": neutral,
            "negative_count": negative,
            "dominant_mood": "positive" if avg_valence > 0.15 else ("negative" if avg_valence < -0.15 else "neutral"),
        }

    # ═══════════════════════════════════════════════════════
    # 便捷查询
    # ═══════════════════════════════════════════════════════

    def get_timeline_stats(self) -> dict:
        """时间旅行系统统计"""
        snapshots = self.store.conn.execute(
            "SELECT COUNT(*) as cnt FROM memory_snapshots"
        ).fetchone()

        total_items = self.store.conn.execute(
            "SELECT COUNT(*) as cnt FROM memory_snapshot_items"
        ).fetchone()

        # 最早/最晚记忆
        earliest = self.store.conn.execute(
            "SELECT MIN(created_at) as ts FROM memories"
        ).fetchone()
        latest = self.store.conn.execute(
            "SELECT MAX(created_at) as ts FROM memories"
        ).fetchone()

        # 按天分布
        daily = self.store.conn.execute(
            """SELECT DATE(time_ts, 'unixepoch', 'localtime') as day, COUNT(*) as cnt
               FROM memories
               GROUP BY day
               ORDER BY day DESC
               LIMIT 30"""
        ).fetchall()

        return {
            "snapshots_count": snapshots["cnt"] if snapshots else 0,
            "snapshot_items_count": total_items["cnt"] if total_items else 0,
            "earliest_memory": datetime.fromtimestamp(earliest["ts"]).isoformat() if earliest and earliest["ts"] else None,
            "latest_memory": datetime.fromtimestamp(latest["ts"]).isoformat() if latest and latest["ts"] else None,
            "daily_distribution": [
                {"date": r["day"], "count": r["cnt"]}
                for r in daily
            ],
        }

    def auto_snapshot_if_needed(self, interval_hours: int = 24) -> dict | None:
        """自动快照：距离上次快照超过 interval_hours 就拍一张"""
        last = self.store.conn.execute(
            "SELECT MAX(at_ts) as last_ts FROM memory_snapshots"
        ).fetchone()

        now = int(time.time())
        if last and last["last_ts"]:
            elapsed = now - last["last_ts"]
            if elapsed < interval_hours * 3600:
                return None  # 还不需要

        # 检查是否有新记忆
        if last and last["last_ts"]:
            new_count = self.store.conn.execute(
                "SELECT COUNT(*) as cnt FROM memories WHERE created_at > ?",
                (last["last_ts"],)
            ).fetchone()["cnt"]
            if new_count == 0:
                return None  # 没有新记忆

        return self.take_snapshot(
            label=datetime.now().strftime("%Y-%m-%d"),
            description="自动快照",
        )


# ═══════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════

def _human_time_ago(ts: int) -> str:
    """时间戳转 'X天前' / 'X小时前' 等"""
    delta = time.time() - ts
    if delta < 60:
        return "刚刚"
    elif delta < 3600:
        return f"{int(delta // 60)} 分钟前"
    elif delta < 86400:
        return f"{int(delta // 3600)} 小时前"
    elif delta < 2592000:
        return f"{int(delta // 86400)} 天前"
    else:
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")


def parse_date_to_ts(date_str: str) -> int:
    """
    解析日期字符串为 Unix timestamp。

    支持格式：
      - "2026-04-01"       → 当天 00:00:00
      - "2026-04-01 14:30" → 精确时间
      - "7d" / "7 days"    → 7天前
      - "1m" / "1 month"   → 1个月前
      - "today"            → 今天 00:00:00
      - "yesterday"        → 昨天 00:00:00
    """
    date_str = date_str.strip().lower()

    if date_str == "today":
        dt = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return int(dt.timestamp())

    if date_str == "yesterday":
        dt = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        return int(dt.timestamp())

    # 相对时间：7d, 1m, 2w
    import re
    rel_match = re.match(r'^(\d+)\s*(d|day|days|w|week|weeks|m|month|months|h|hour|hours)$', date_str)
    if rel_match:
        num = int(rel_match.group(1))
        unit = rel_match.group(2)[0]
        if unit == 'h':
            delta = timedelta(hours=num)
        elif unit == 'd':
            delta = timedelta(days=num)
        elif unit == 'w':
            delta = timedelta(weeks=num)
        elif unit == 'm':
            delta = timedelta(days=num * 30)
        else:
            delta = timedelta(days=num)
        return int((datetime.now() - delta).timestamp())

    # 绝对日期
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(date_str, fmt)
            return int(dt.timestamp())
        except ValueError:
            continue

    raise ValueError(f"无法解析日期: {date_str}，支持格式: YYYY-MM-DD, 7d, 1m, today, yesterday")
