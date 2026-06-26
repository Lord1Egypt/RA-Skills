"""
hierarchical.py - 层级记忆管理
短期(对话级) → 中期(天级) → 长期(永久)，自动流转
"""

from __future__ import annotations

import time
import json
import logging
import threading
from datetime import datetime

logger = logging.getLogger(__name__)


class HierarchicalMemory:
    """
    三级记忆层级：

    L1 短期记忆 (Short-term)
    - 生命周期: 单次对话 / 几小时
    - 容量: 50 条
    - 存储: 内存 buffer，不持久化
    - 用途: 当前对话上下文

    L2 中期记忆 (Mid-term)
    - 生命周期: 1-7 天
    - 容量: 500 条
    - 存储: SQLite (已持久化)
    - 用途: 近期对话回顾

    L3 长期记忆 (Long-term)
    - 生命周期: 永久
    - 容量: 无上限
    - 存储: SQLite + Chroma
    - 用途: 核心知识、决策、偏好

    流转规则:
    - L1 → L2: 对话结束 / buffer 满 → 自动沉淀
    - L2 → L3: 重要度 high / 被频繁检索 / 时间考验
    - L3 压缩: 低价值长期记忆 → 压缩为摘要
    """

    # 容量限制
    L1_CAPACITY = 50
    L2_CAPACITY = 500

    # L2 → L3 升级条件
    L2_TO_L3_MIN_AGE_DAYS = 3       # 至少存在 3 天
    L2_TO_L3_MIN_RETRIEVALS = 3     # 被检索至少 3 次
    L2_TO_L3_IMPORTANCE = "high"    # high 重要度直接升级

    # L1 空闲超时（秒）：超过此时间无新写入则自动 flush
    L1_IDLE_FLUSH_SEC = 600  # 10 分钟

    def __init__(self, store, quality=None):
        self.store = store
        self.quality = quality

        # L1 短期记忆 buffer（受 _l1_lock 保护，RLock 因 l1_add 内部调用 auto_consolidate 需要重入）
        self._l1_lock = threading.RLock()
        self._l1_buffer: list[dict] = []
        self._l1_session_id: str = datetime.now().strftime("session_%Y%m%d_%H%M%S")
        self._l1_last_activity: float = time.time()  # 最后一次写入时间
        # Fix #8: 持久化 + 恢复
        self._ensure_l1_table()
        self._l1_restore()

    # ── L1 短期记忆 ────────────────────────────────────

    def l1_add(self, content: str, role: str = "user", metadata: dict = None) -> dict:
        """
        添加到短期记忆 buffer。

        参数:
            content: 消息内容
            role: user / assistant / system
            metadata: 附加元数据
        """
        with self._l1_lock:
            self._l1_last_activity = time.time()
            entry = {
                "content": content,
                "role": role,
                "timestamp": int(time.time()),
                "session_id": self._l1_session_id,
                "metadata": metadata or {},
            }
            self._l1_buffer.append(entry)

            # 超容量则自动触发 consolidation（不再简单丢弃）
            if len(self._l1_buffer) > self.L1_CAPACITY:
                self.auto_consolidate()

            # Fix #8: 持久化
            self._l1_persist(entry)
            return entry

    def l1_get(self, last_n: int = 10) -> list[dict]:
        """获取最近 N 条短期记忆"""
        with self._l1_lock:
            return list(self._l1_buffer[-last_n:])

    def l1_context(self, max_tokens: int = 1500) -> str:
        """
        组装短期记忆为对话上下文。

        从最新的消息开始，逐步添加直到达到 token 预算。
        """
        with self._l1_lock:
            lines = []
            token_count = 0

            for entry in reversed(self._l1_buffer):
                role = entry["role"]
                content = entry["content"]

                # 估算 tokens
                est_tokens = len(content) * 1.5
                if token_count + est_tokens > max_tokens:
                    break

                prefix = {"user": "用户", "assistant": "助手", "system": "系统"}.get(role, role)
                lines.insert(0, f"{prefix}: {content}")
                token_count += est_tokens

            return "\n".join(lines)

    def l1_clear(self):
        """清空短期记忆（对话结束时调用）"""
        with self._l1_lock:
            self._l1_buffer = []
            self._l1_session_id = datetime.now().strftime("session_%Y%m%d_%H%M%S")
            self._l1_last_activity = time.time()
            try:
                self.store.conn.execute("DELETE FROM _l1_buffer")
                self.store.conn.commit()
            except Exception as e:
                logger.warning("hierarchical: %s", e)

    def session_end_flush(self, pipeline=None, deduplicator=None) -> dict:
        """
        会话结束时的自动 flush：consolidate → 沉淀到 L2 → 清空 L1。

        这是外部调用方（Agent 框架）在对话结束时应该调用的入口。
        返回: {"flushed": int, "merged": int, "dropped": int}
        """
        # 1. consolidation
        consolidate_result = self.auto_consolidate(pipeline=pipeline)

        # 2. L1→L2 沉淀
        written = self.l1_flush_to_l2(pipeline=pipeline, deduplicator=deduplicator)

        # 3. 清空 L1
        self.l1_clear()

        return {
            "flushed": len(written),
            "merged": consolidate_result.get("merged", 0),
            "dropped": consolidate_result.get("dropped", 0),
        }

    def auto_flush_if_idle(self, pipeline=None, deduplicator=None) -> dict:
        """
        空闲自动 flush：如果超过 L1_IDLE_FLUSH_SEC 没有新写入，
        自动将 L1 沉淀到 L2。

        适合在 heartbeat 或定时任务中调用。
        返回: {"flushed": int} 或 {"idle": False}（未超时）
        """
        with self._l1_lock:
            idle_sec = time.time() - self._l1_last_activity
            if idle_sec < self.L1_IDLE_FLUSH_SEC:
                return {"idle": False, "idle_sec": round(idle_sec)}

            if not self._l1_buffer:
                return {"idle": True, "idle_sec": round(idle_sec), "flushed": 0}

            return self.session_end_flush(pipeline=pipeline, deduplicator=deduplicator)

    # ── L1 自动 consolidation ──────────────────────────

    def auto_consolidate(self, pipeline=None, threshold: float = 0.7) -> dict:
        """
        自动 consolidation：buffer 满时触发。

        策略：
        1. 相似消息合并（相邻 + 同角色 + 文本相似度 > 0.7）
        2. 低价值消息淘汰（系统消息、极短消息、纯寒暄）
        3. 超出容量的部分自动沉淀到 L2

        返回: {"merged": int, "dropped": int, "flushed": int}
        """
        with self._l1_lock:
            if not self._l1_buffer:
                return {"merged": 0, "dropped": 0, "flushed": 0}

            merged = 0
            dropped = 0
            flushed = 0

            # 第一轮：过滤低价值消息
            TRIVIAL = {"ok", "好的", "嗯", "谢谢", "收到", "了解", "明白", "是的", "对",
                        "thanks", "ok", "yes", "no", "嗯嗯", "哈哈", "好的好的"}
            filtered = []
            for entry in self._l1_buffer:
                content = entry["content"].strip()
                # 跳过系统消息
                if entry["role"] == "system":
                    dropped += 1
                    continue
                # 跳过极短消息（< 5 字且是寒暄）
                if len(content) < 5 and content.lower() in {t.lower() for t in TRIVIAL}:
                    dropped += 1
                    continue
                # 跳过纯表情
                if all(ord(c) > 0x1F000 for c in content if c.strip()):
                    dropped += 1
                    continue
                filtered.append(entry)

            # 第二轮：合并相邻相似消息
            if len(filtered) > 1:
                merged_buffer = [filtered[0]]
                for entry in filtered[1:]:
                    prev = merged_buffer[-1]
                    # 同角色 + 相邻（时间差 < 60s）+ 文本相似 → 合并
                    if (entry["role"] == prev["role"]
                        and abs(entry["timestamp"] - prev["timestamp"]) < 60
                        and self._text_similarity(entry["content"], prev["content"]) > threshold):
                        # 合并：保留较长的那个，或拼接
                        if len(entry["content"]) > len(prev["content"]):
                            merged_buffer[-1] = entry
                        merged += 1
                    else:
                        merged_buffer.append(entry)
                filtered = merged_buffer

            # 第三轮：超出容量的沉淀到 L2
            if len(filtered) > self.L1_CAPACITY:
                overflow = filtered[:len(filtered) - self.L1_CAPACITY]
                filtered = filtered[len(filtered) - self.L1_CAPACITY:]

                if pipeline:
                    for entry in overflow:
                        content = entry["content"]
                        if entry["role"] != "system" and len(content.strip()) >= 10:
                            try:
                                pipeline.ingest(
                                    content=content,
                                    person_code="main",
                                    importance="medium",
                                    skip_throttle=True,
                                )
                                flushed += 1
                            except Exception as e:
                                logger.debug(f"L1 auto-flush 失败: {e}")

            self._l1_buffer = filtered

            # 持久化同步
            try:
                self.store.conn.execute("DELETE FROM _l1_buffer WHERE session_id = ?",
                                         (self._l1_session_id,))
                for entry in self._l1_buffer:
                    self._l1_persist(entry)
            except Exception as e:
                logger.warning("hierarchical: %s", e)

            if merged or dropped or flushed:
                logger.info(f"L1 consolidation: merged={merged}, dropped={dropped}, flushed={flushed}")

            return {"merged": merged, "dropped": dropped, "flushed": flushed}

    @staticmethod
    def _text_similarity(a: str, b: str) -> float:
        """快速文本相似度（Jaccard bigram），不依赖外部库"""
        def bigrams(s):
            s = s.lower()
            return set(s[i:i+2] for i in range(len(s) - 1))
        ba, bb = bigrams(a), bigrams(b)
        if not ba or not bb:
            return 0.0
        return len(ba & bb) / len(ba | bb)

    # ── L1 → L2 沉淀 ──────────────────────────────────

    def l1_flush_to_l2(self, pipeline=None, deduplicator=None) -> list[dict]:
        """
        将 L1 buffer 中的有价值内容沉淀到 L2（通过 pipeline 写入 SQLite）。

        参数:
            pipeline: IngestPipeline 实例
            deduplicator: MemoryDeduplicator 实例（可选，用于去重）

        返回: 写入的 memory 列表
        """
        if not pipeline:
            return []

        with self._l1_lock:
            if not self._l1_buffer:
                return []

            written = []
            for entry in self._l1_buffer:
                content = entry["content"]
                role = entry["role"]

                # 跳过系统消息和极短消息
                if role == "system" or len(content.strip()) < 10:
                    continue

                # 去重检查
                if deduplicator:
                    try:
                        dup_result = deduplicator.check_duplicate(content)
                        if dup_result.get("is_duplicate"):
                            logger.debug(f"L1→L2 跳过重复: {content[:30]}...")
                            continue
                    except Exception as e:
                        logger.warning("hierarchical: %s", e)

                # 角色映射到 person_code
                person_code = {"user": "main", "assistant": "main"}.get(role, "main")

                # 用 pipeline 写入
                result = pipeline.ingest(
                    content=content,
                    person_code=person_code,
                    importance="medium",  # L2 默认 medium
                )
                written.append(result)

            logger.info(f"L1→L2 沉淀: {len(written)} 条")
            return written

    # ── L2 → L3 升级 ──────────────────────────────────

    def l2_promote_to_l3(self) -> dict:
        """
        将符合条件的 L2 记忆升级为 L3（提升重要度）。

        条件（满足任一）:
        - 重要度已经是 high
        - 存活超过 N 天且被检索超过 M 次
        - 有显式正反馈

        返回: {"promoted": [memory_ids], "count": int}
        """
        now = int(time.time())
        promoted = []

        memories = self.store.query(limit=self.L2_CAPACITY, importance="medium")

        for mem in memories:
            mid = mem["memory_id"]
            age_days = (now - mem.get("time_ts", now)) / 86400

            should_promote = False
            reason = ""

            # 条件 1: 高重要度直接升
            if mem.get("importance") == "high":
                should_promote = True
                reason = "already_high"

            # 条件 2: 时间 + 检索次数
            elif age_days >= self.L2_TO_L3_MIN_AGE_DAYS:
                retrieval_count = 0
                if self.quality:
                    retrieval_count = self.quality._stats.get("retrievals", {}).get(mid, 0)

                if retrieval_count >= self.L2_TO_L3_MIN_RETRIEVALS:
                    should_promote = True
                    reason = f"frequently_retrieved ({retrieval_count}x)"

            # 条件 3: 正反馈
            if self.quality and not should_promote:
                feedback = self.quality._stats.get("feedback", {}).get(mid)
                if feedback and feedback.get("useful"):
                    should_promote = True
                    reason = "positive_feedback"

            if should_promote:
                # 升级：更新 importance 为 high
                self.store.conn.execute(
                    "UPDATE memories SET importance = 'high' WHERE memory_id = ?",
                    (mid,),
                )
                self.store.conn.commit()
                promoted.append({"memory_id": mid, "reason": reason})
                logger.info(f"L2→L3 升级: {mid[:30]}... ({reason})")

        return {"promoted": promoted, "count": len(promoted)}

    # ── L3 维护 ─────────────────────────────────────────

    def l3_demote(self, threshold_days: int = 365) -> list[str]:
        """
        将长期未被访问的 L3 记忆降级（标记为可压缩）。

        被降级的条件：
        - importance=medium（high 不降级）
        - 超过 threshold_days 天未被检索
        """
        now = int(time.time())
        demoted = []

        memories = self.store.query(importance="medium", limit=500)
        for mem in memories:
            age_days = (now - mem.get("time_ts", now)) / 86400
            if age_days > threshold_days:
                mid = mem["memory_id"]
                # 检查最近是否被检索
                retrieval_count = 0
                if self.quality:
                    retrieval_count = self.quality._stats.get("retrievals", {}).get(mid, 0)

                if retrieval_count == 0:
                    demoted.append(mid)

        return demoted

    # ── 全生命周期维护 ──────────────────────────────────

    def maintain(self, pipeline=None, deduplicator=None, decay=None) -> dict:
        """
        一键维护：执行 L1→L2→L3 全生命周期流转。

        步骤：
        1. L1 consolidation（合并、过滤）
        2. L1→L2 沉淀（带去重）
        3. L2→L3 升级（高频/高价值）
        4. 衰减分析（如果提供了 decay）

        参数:
            pipeline: IngestPipeline（L1→L2 用）
            deduplicator: MemoryDeduplicator（去重用）
            decay: MemoryDecay（衰减分析用）

        返回: 各阶段统计
        """
        result = {
            "consolidation": {},
            "l1_to_l2": 0,
            "l2_to_l3": 0,
            "demoted": 0,
            "decay": {},
        }

        # 1. L1 consolidation
        result["consolidation"] = self.auto_consolidate(pipeline=pipeline)

        # 2. L1 → L2
        if pipeline:
            flushed = self.l1_flush_to_l2(pipeline=pipeline, deduplicator=deduplicator)
            result["l1_to_l2"] = len(flushed)

        # 3. L2 → L3
        promote_result = self.l2_promote_to_l3()
        result["l2_to_l3"] = promote_result["count"]

        # 4. L3 降级检查
        demoted = self.l3_demote()
        result["demoted"] = len(demoted)

        # 5. 衰减分析
        if decay:
            try:
                result["decay"] = decay.analyze()
            except Exception as e:
                result["decay"] = {"error": str(e)}

        logger.info(f"层级维护完成: {result}")
        return result

    # ── L1 持久化（Fix #8）──────────────────────────────

    def _ensure_l1_table(self):
        try:
            self.store.conn.executescript("""
                CREATE TABLE IF NOT EXISTS _l1_buffer (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    role TEXT DEFAULT 'user',
                    timestamp INTEGER NOT NULL,
                    session_id TEXT NOT NULL,
                    metadata TEXT DEFAULT '{}',
                    created_at INTEGER NOT NULL DEFAULT (strftime('%s','now'))
                );
                CREATE INDEX IF NOT EXISTS idx_l1_session ON _l1_buffer(session_id);
            """)
            self.store.conn.commit()
        except Exception as e:
            logger.warning("hierarchical: %s", e)

    def _l1_persist(self, entry: dict):
        try:
            import json as _json
            self.store.conn.execute(
                "INSERT INTO _l1_buffer (content, role, timestamp, session_id, metadata) VALUES (?, ?, ?, ?, ?)",
                (entry["content"], entry["role"], entry["timestamp"],
                 entry["session_id"], _json.dumps(entry.get("metadata", {}), ensure_ascii=False)),
            )
            self.store.conn.commit()
        except Exception as e:
            logger.debug(f"L1 持久化失败: {e}")

    def _l1_restore(self):
        try:
            rows = self.store.conn.execute(
                "SELECT * FROM _l1_buffer WHERE session_id = ? ORDER BY id DESC LIMIT ?",
                (self._l1_session_id, self.L1_CAPACITY),
            ).fetchall()
            import json as _json
            restored = []
            for row in reversed(rows):
                meta = {}
                try:
                    meta = _json.loads(row["metadata"] or "{}")
                except Exception as e:
                    logger.warning("hierarchical: %s", e)
                restored.append({
                    "content": row["content"],
                    "role": row["role"],
                    "timestamp": row["timestamp"],
                    "session_id": row["session_id"],
                    "metadata": meta,
                })
            if restored:
                self._l1_buffer = restored
                logger.info(f"L1 恢复: {len(restored)} 条记忆")
        except Exception as e:
            logger.warning("hierarchical: %s", e)

    # ── 统计 ────────────────────────────────────────────

    def get_stats(self) -> dict:
        """各层级统计"""
        with self._l1_lock:
            l1_count = len(self._l1_buffer)
            l1_session_id = self._l1_session_id

        all_memories = self.store.query(limit=10000)

        l2_count = sum(1 for m in all_memories if m.get("importance") != "high")
        l3_count = sum(1 for m in all_memories if m.get("importance") == "high")

        return {
            "L1_short_term": {
                "count": l1_count,
                "capacity": self.L1_CAPACITY,
                "session_id": l1_session_id,
            },
            "L2_mid_term": {
                "count": l2_count,
                "capacity": self.L2_CAPACITY,
            },
            "L3_long_term": {
                "count": l3_count,
                "capacity": "unlimited",
            },
            "total": len(all_memories),
        }

    def generate_hierarchy_report(self) -> str:
        """生成层级记忆报告"""
        stats = self.get_stats()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        lines = [
            "# 🏗️ 层级记忆报告",
            "",
            f"**生成时间**: {now_str}",
            "",
            "## 各层级状态",
            "",
            f"### L1 短期记忆 (对话级)",
            f"- 容量: {stats['L1_short_term']['count']}/{stats['L1_short_term']['capacity']}",
            f"- 会话: {stats['L1_short_term']['session_id']}",
            "",
            f"### L2 中期记忆 (天级)",
            f"- 容量: {stats['L2_mid_term']['count']}/{stats['L2_mid_term']['capacity']}",
            "",
            f"### L3 长期记忆 (永久)",
            f"- 容量: {stats['L3_long_term']['count']}/{stats['L3_long_term']['capacity']}",
            "",
            f"**总计**: {stats['total']} 条记忆",
        ]

        return "\n".join(lines)
