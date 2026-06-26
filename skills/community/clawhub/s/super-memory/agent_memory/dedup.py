"""
dedup.py - 语义级记忆去重
防止语义相近但文字不同的记忆重复存储
"""

from __future__ import annotations

import hashlib
import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)


class MemoryDeduplicator:
    """
    三层去重：
    1. 精确去重 — content_hash 完全相同（已有）
    2. 近似去重 — 文本相似度 > 阈值
    3. 语义去重 — embedding 余弦相似度 > 阈值

    去重策略：
    - 保留较新/较高优先的版本
    - 旧版本标记为重复（不删除，保留溯源）
    - 合并两个版本的元数据（主题、标签等）
    """

    # 相似度阈值
    TEXT_SIMILARITY_THRESHOLD = 0.85   # 文本相似度阈值
    SEMANTIC_SIMILARITY_THRESHOLD = 0.92  # 语义相似度阈值（更严格，避免误判）
    CONFLICT_LOW = 0.60   # 低于此：不相关
    CONFLICT_HIGH = 0.85  # 高于此：重复，不是冲突

    def __init__(self, store, embedding_store=None):
        self.store = store
        self.embedding_store = embedding_store

    def check_duplicate(self, content: str, time_window_hours: int = 24) -> dict:
        """
        检查新内容是否与已有记忆重复。

        修复 (P0): O(n²) → O(n) 滑动窗口
        - 精确去重走 content_hash 索引（O(1)）
        - 近似去重只看最近 24h（原来是 72h），最多 50 条候选
        - 有 FTS 时用 FTS 缩小候选集再比对

        参数:
            content: 待写入的内容
            time_window_hours: 只检查这个时间窗口内的记忆（默认 24h）

        返回:
        {
            "is_duplicate": bool,
            "duplicate_of": str | None,
            "similarity": float,
            "method": str,
            "action": str,
        }
        """
        import time
        now = int(time.time())
        window_start = now - time_window_hours * 3600

        # 1. 精确去重（content_hash 索引，O(1)）
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        exact = self.store.conn.execute(
            "SELECT memory_id FROM memories WHERE content_hash = ? AND time_ts >= ?",
            (content_hash, window_start),
        ).fetchone()
        if exact:
            return {
                "is_duplicate": True,
                "duplicate_of": exact["memory_id"],
                "similarity": 1.0,
                "method": "exact",
                "action": "skip",
            }

        # 2. 近似去重 — 候选集缩小到 24h 内最多 50 条
        #    有 FTS 时先用 FTS 缩小范围
        MAX_CANDIDATES = 50

        if self.store._has_fts and len(content.strip()) >= 3:
            # FTS 候选：只搜内容相似的
            candidates = self.store._query_fts(content[:200], MAX_CANDIDATES)
            candidates = [m for m in candidates if m.get("time_ts", 0) >= window_start]
        else:
            # 降级：按时间倒序取最近的
            candidates = self.store.query(limit=MAX_CANDIDATES, time_from=window_start)

        if not candidates:
            return {"is_duplicate": False, "duplicate_of": None, "similarity": 0, "method": "none", "action": "keep_both"}

        # 3. 文本相似度（候选集已缩小到 ≤50 条，不再是 O(n²) 全量）
        best_text_score = 0
        best_text_id = None
        for mem in candidates:
            score = self._text_similarity(content, mem.get("content", ""))
            if score > best_text_score:
                best_text_score = score
                best_text_id = mem["memory_id"]

        if best_text_score >= self.TEXT_SIMILARITY_THRESHOLD:
            return {
                "is_duplicate": True,
                "duplicate_of": best_text_id,
                "similarity": round(best_text_score, 4),
                "method": "text",
                "action": self._decide_action(content, best_text_id, best_text_score),
            }

        # 4. 语义相似度（如果 embedding 可用）
        if self.embedding_store:
            try:
                results = self.embedding_store.search(content, top_k=5)
                for r in results:
                    if r["score"] >= self.SEMANTIC_SIMILARITY_THRESHOLD:
                        return {
                            "is_duplicate": True,
                            "duplicate_of": r["memory_id"],
                            "similarity": round(r["score"], 4),
                            "method": "semantic",
                            "action": self._decide_action(content, r["memory_id"], r["score"]),
                        }
            except Exception as e:
                logger.warning("dedup: %s", e)

        return {
            "is_duplicate": False,
            "duplicate_of": None,
            "similarity": round(max(best_text_score, 0), 4),
            "method": "none",
            "action": "keep_both",
        }

    def deduplicate_batch(self, memory_ids: list[str] = None) -> dict:
        """
        批量去重：扫描现有记忆，找出并处理重复项。

        修复 (P0): O(n²) 两两比对 → 大分桶 + 小窗口内比较
        - 先按 content_hash 分桶（精确重复 O(n)）
        - 对非精确重复，按 bigram 签名分桶（近似重复只在桶内比较）
        - 限制单批最多扫描 200 条

        参数:
            memory_ids: 指定要检查的记忆 ID 列表（None=全部）

        返回:
        {
            "total_scanned": int,
            "duplicates_found": int,
            "merged": [{"kept": str, "removed": str, "similarity": float}],
            "groups": [[str]],
        }
        """
        MAX_SCAN = 200

        if memory_ids:
            memories = [self.store.get_memory(mid) for mid in memory_ids[:MAX_SCAN]]
            memories = [m for m in memories if m]
        else:
            memories = self.store.query(limit=MAX_SCAN)

        if len(memories) < 2:
            return {"total_scanned": len(memories), "duplicates_found": 0, "merged": [], "groups": []}

        # Phase 1: 精确去重 — content_hash 分桶（O(n)）
        hash_buckets: dict[str, list[dict]] = {}
        for mem in memories:
            h = mem.get("content_hash", "")
            if h:
                if h not in hash_buckets:
                    hash_buckets[h] = []
                hash_buckets[h].append(mem)

        # Phase 2: 近似去重 — 大分桶签名（减少比较次数）
        #   对每条记忆取前 100 字符的 bigram 集合的 hash 作为桶键
        #   同桶内的记忆才做精细比较
        sig_buckets: dict[str, list[dict]] = {}
        for mem in memories:
            content = mem.get("content", "")[:100]
            if not content:
                continue
            # 取 top 5 个最短的 bigram 作为签名（类似 LSH）
            grams = sorted(self._char_ngrams(self._normalize(content), 2))[:20]
            sig = hashlib.md5("|".join(grams).encode()).hexdigest()[:8]
            if sig not in sig_buckets:
                sig_buckets[sig] = []
            sig_buckets[sig].append(mem)

        # Phase 3: 合并
        imp_order = {"high": 0, "medium": 1, "low": 2}
        visited = set()
        duplicate_groups = []
        merged = []

        # 精确重复桶
        for h, group in hash_buckets.items():
            if len(group) > 1:
                duplicate_groups.append([m["memory_id"] for m in group])

        # 近似重复桶（桶内比对，不再全量两两）
        for sig, bucket in sig_buckets.items():
            if len(bucket) < 2:
                continue
            # 桶内排序后依次比较
            bucket_sorted = sorted(bucket, key=lambda m: m.get("time_ts", 0))
            for i, mem_a in enumerate(bucket_sorted):
                if mem_a["memory_id"] in visited:
                    continue
                group = [mem_a["memory_id"]]
                for mem_b in bucket_sorted[i+1:]:
                    if mem_b["memory_id"] in visited:
                        continue
                    score = self._text_similarity(
                        mem_a.get("content", ""), mem_b.get("content", "")
                    )
                    if score >= self.TEXT_SIMILARITY_THRESHOLD:
                        group.append(mem_b["memory_id"])
                if len(group) > 1:
                    duplicate_groups.append(group)
                    visited.update(group)

        # 执行合并
        all_group_ids = set()
        for group in duplicate_groups:
            all_group_ids.update(group)
        memories_cache = {m["memory_id"]: m for m in memories if m.get("memory_id") in all_group_ids}

        for group in duplicate_groups:
            memories_in_group = [memories_cache[mid] for mid in group if mid in memories_cache]
            if len(memories_in_group) < 2:
                continue

            memories_in_group.sort(key=lambda m: (
                imp_order.get(m.get("importance", "medium"), 1),
                -(m.get("time_ts", 0)),
            ))

            keeper = memories_in_group[0]
            for dup in memories_in_group[1:]:
                self._mark_duplicate(dup["memory_id"], keeper["memory_id"])
                merged.append({
                    "kept": keeper["memory_id"],
                    "removed": dup["memory_id"],
                    "similarity": self._text_similarity(
                        keeper.get("content", ""), dup.get("content", ""),
                    ),
                })

        return {
            "total_scanned": len(memories),
            "duplicates_found": sum(len(g) - 1 for g in duplicate_groups),
            "merged": merged,
            "groups": duplicate_groups,
        }

    def _text_similarity(self, a: str, b: str) -> float:
        """
        文本相似度（Jaccard + 编辑距离混合）。
        比纯 embedding 快，适合大量初筛。
        """
        if not a or not b:
            return 0.0
        if a == b:
            return 1.0

        # 标准化
        a_norm = self._normalize(a)
        b_norm = self._normalize(b)

        if a_norm == b_norm:
            return 0.99

        # Jaccard 相似度（基于字符 bigram）
        set_a = set(self._char_ngrams(a_norm, 2))
        set_b = set(self._char_ngrams(b_norm, 2))

        if not set_a or not set_b:
            return 0.0

        intersection = len(set_a & set_b)
        union = len(set_a | set_b)

        return intersection / union if union > 0 else 0.0

    @staticmethod
    def _normalize(text: str) -> str:
        """标准化文本"""
        text = text.lower().strip()
        text = re.sub(r'\s+', ' ', text)  # 合并空白
        text = re.sub(r'[^\w\u4e00-\u9fff\s]', '', text)  # 去标点
        return text

    @staticmethod
    def _char_ngrams(text: str, n: int) -> list[str]:
        """字符 n-gram"""
        return [text[i:i+n] for i in range(len(text) - n + 1)]

    def _decide_action(self, new_content: str, existing_id: str, similarity: float) -> str:
        """决定如何处理重复

        Fix (P0): 新内容 importance 更高时不应 skip，否则关键信息丢失。
        场景：先说"Chroma 好用"(low)，后说"Chroma 好用，注意 HNSW 参数 M=32"(high)
        → 文本相似度 >0.98 但新内容含关键信息，不能 skip。
        """
        existing = self.store.get_memory(existing_id)
        if not existing:
            return "keep_both"

        # 新内容明显更长/更详细 → 合并（新覆盖旧）
        if len(new_content) > len(existing.get("content", "")) * 1.5:
            return "merge"

        # 极高相似度 → 跳过（但仅当新内容不比旧的更重要）
        if similarity >= 0.98:
            # 检查新内容是否包含更多信息（更长即更多信息）
            if len(new_content) > len(existing.get("content", "")):
                return "merge"
            return "skip"

        # 相似度高但不完全一样 → 标记关联
        return "link"

    def _mark_duplicate(self, duplicate_id: str, keeper_id: str):
        """标记一条记忆为重复"""
        self.store.insert_link(
            source_id=duplicate_id,
            target_id=keeper_id,
            link_type="duplicate_of",
            weight=0.1,
            reason="语义去重",
        )

    def check_conflict(self, content: str, time_window_hours: int = 72) -> dict:
        """
        检测新内容是否与旧记忆存在潜在冲突。

        修复 (P0): 候选集从 50 → 30，只看 72h 内

        冲突 ≠ 重复：
        - 重复：内容几乎一样（相似度 > 0.85）
        - 冲突：主题相似但结论可能矛盾（相似度 0.60~0.85）

        返回:
        {
            "has_conflict": bool,
            "conflicts": [{"memory_id": str, "content": str, "similarity": float}, ...],
        }
        """
        import time
        now = int(time.time())
        window_start = now - time_window_hours * 3600

        MAX_CONFLICT_CANDIDATES = 30

        # 只取时间窗口内的记忆
        candidates = self.store.query(limit=MAX_CONFLICT_CANDIDATES, time_from=window_start)

        if not candidates:
            return {"has_conflict": False, "conflicts": []}

        conflicts = []
        for mem in candidates:
            existing_content = mem.get("content", "")
            if existing_content == content:
                continue

            score = self._text_similarity(content, existing_content)

            if self.CONFLICT_LOW <= score < self.CONFLICT_HIGH:
                conflicts.append({
                    "memory_id": mem.get("memory_id", ""),
                    "content": existing_content[:100],
                    "similarity": round(score, 4),
                })

        conflicts.sort(key=lambda x: -x["similarity"])

        return {
            "has_conflict": len(conflicts) > 0,
            "conflicts": conflicts[:3],
        }

    def get_stats(self) -> dict:
        """去重统计"""
        rows = self.store.conn.execute(
            "SELECT COUNT(*) as cnt FROM memory_links WHERE link_type = 'duplicate_of'"
        ).fetchone()
        return {
            "duplicate_links": rows["cnt"] if rows else 0,
            "text_threshold": self.TEXT_SIMILARITY_THRESHOLD,
            "semantic_threshold": self.SEMANTIC_SIMILARITY_THRESHOLD,
        }
