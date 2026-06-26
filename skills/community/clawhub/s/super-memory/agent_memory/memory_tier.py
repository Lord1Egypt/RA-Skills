"""v8.6 — memory_tier.py — 记忆冷热分层 + 自动蒸馏触发

分层策略:
    HOT  (最近7天 + 被检索≥3次) → LRU 内存缓存
    WARM (正常使用)              → 主数据库
    COLD (30天未检索)           → 归档数据库
    EXPIRED (TTL到期)           → 软删除

自动蒸馏:
    同类记忆≥5条 → 触发 LLM 压缩为1条摘要
"""

from __future__ import annotations

import time
import json
import os
import sqlite3
import logging
import threading
from collections import OrderedDict
from datetime import datetime
from typing import Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class TierConfig:
    hot_window_days: int = 7
    hot_access_threshold: int = 3
    cold_window_days: int = 30
    default_ttl_days: int = 365
    lru_max_size: int = 1000
    compress_similar_threshold: int = 5
    compress_batch_size: int = 10
    archive_db_path: str = "memory_archive.db"


class LRUCache:
    """线程安全的 LRU 缓存"""

    def __init__(self, max_size: int = 1000):
        self._cache: OrderedDict = OrderedDict()
        self._max_size = max_size
        self._lock = threading.Lock()

    def get(self, key: str):
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
                return self._cache[key]
            return None

    def put(self, key: str, value):
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            self._cache[key] = value
            if len(self._cache) > self._max_size:
                self._cache.popitem(last=False)

    def remove(self, key: str):
        with self._lock:
            self._cache.pop(key, None)

    def contains(self, key: str) -> bool:
        with self._lock:
            return key in self._cache

    def size(self) -> int:
        with self._lock:
            return len(self._cache)

    def clear(self):
        with self._lock:
            self._cache.clear()

    def keys(self):
        with self._lock:
            return list(self._cache.keys())


class MemoryTierManager:
    """记忆冷热分层管理器

    功能:
    - HOT 层: LRU 内存缓存最近/高频访问的记忆
    - COLD 层: 30天未访问自动迁移到归档库
    - TTL 过期: 支持每条记忆自定义 TTL
    - 自动压缩: 同类记忆≥5条触发 LLM 蒸馏
    """

    def __init__(self, store=None, config: TierConfig = None, distill=None):
        self._store = store
        self._config = config or TierConfig()
        self._distill = distill
        self._hot_cache = LRUCache(max_size=self._config.lru_max_size)

        self._stats = {
            "promotions": 0,
            "demotions": 0,
            "evictions": 0,
            "archivals": 0,
            "expirations": 0,
            "compressions": 0,
            "cache_hits": 0,
            "cache_misses": 0,
        }
        self._last_scan = 0

    @property
    def store(self):
        return self._store

    @property
    def hot_cache(self):
        return self._hot_cache

    def get_stats(self) -> dict:
        return dict(self._stats)

    def get_hot_memory(self, memory_id: str) -> Optional[dict]:
        """从热缓存获取记忆"""
        result = self._hot_cache.get(memory_id)
        if result is not None:
            self._stats["cache_hits"] += 1
        else:
            self._stats["cache_misses"] += 1
        return result

    def promote_to_hot(self, memory_id: str, memory: dict):
        """将记忆提升到热层"""
        if not self._hot_cache.contains(memory_id):
            self._stats["promotions"] += 1
        self._hot_cache.put(memory_id, memory)

    def demote_from_hot(self, memory_id: str):
        """将记忆从热层降级"""
        if self._hot_cache.contains(memory_id):
            self._hot_cache.remove(memory_id)
            self._stats["demotions"] += 1

    def record_access(self, memory_id: str, memory: dict):
        """记录一次记忆访问，触发热层评估"""
        access_key = f"access:{memory_id}"
        now = int(time.time())
        access_log = self._hot_cache.get(access_key) or []
        access_log.append(now)
        cutoff = now - self._config.hot_window_days * 86400
        access_log = [t for t in access_log if t >= cutoff]
        self._hot_cache.put(access_key, access_log)

        if len(access_log) >= self._config.hot_access_threshold:
            self.promote_to_hot(memory_id, memory)

    def scan_and_tier(self) -> dict:
        """扫描全量记忆，执行分层操作"""
        now = int(time.time())
        hot_cutoff = now - self._config.hot_window_days * 86400
        cold_cutoff = now - self._config.cold_window_days * 86400

        result = {
            "hot_promoted": 0,
            "hot_demoted": 0,
            "cold_archived": 0,
            "expired": 0,
            "compressed": 0,
        }

        if not self._store:
            return result

        hot_memory_ids = set()
        for key in self._hot_cache.keys():
            if not key.startswith("access:"):
                hot_memory_ids.add(key)

        conn = self._store.conn
        try:
            rows = conn.execute(
                "SELECT memory_id, time_ts FROM memories WHERE deleted = 0 ORDER BY time_ts DESC LIMIT 5000"
            ).fetchall()

            for row in rows:
                memory_id = row["memory_id"]
                time_ts = row["time_ts"]

                if memory_id.startswith("cache_"):
                    continue

                if time_ts >= hot_cutoff:
                    if memory_id not in hot_memory_ids and self._hot_cache.size() < self._config.lru_max_size:
                        mem = self._store.get_memory(memory_id)
                        if mem:
                            self.promote_to_hot(memory_id, mem)
                            result["hot_promoted"] += 1

                if time_ts < cold_cutoff and not self._is_recently_accessed(memory_id, cold_cutoff):
                    archived = self._migrate_to_cold(memory_id)
                    if archived:
                        result["cold_archived"] += 1
                        if memory_id in hot_memory_ids:
                            self.demote_from_hot(memory_id)
                            result["hot_demoted"] += 1

            expired = self._process_expired()
            result["expired"] = expired

            compressed = self._trigger_compression()
            result["compressed"] = compressed

        except Exception as e:
            logger.warning("memory_tier: %s", e)

        self._last_scan = now
        return result

    def _is_recently_accessed(self, memory_id: str, cutoff: int) -> bool:
        access_key = f"access:{memory_id}"
        access_log = self._hot_cache.get(access_key) or []
        return any(t >= cutoff for t in access_log)

    def _migrate_to_cold(self, memory_id: str) -> bool:
        """将记忆迁移到归档数据库"""
        if not self._store:
            return False

        mem = self._store.get_memory(memory_id)
        if not mem:
            return False

        try:
            archive_path = os.path.join(
                os.path.dirname(self._store._db_path) if hasattr(self._store, '_db_path') else ".",
                self._config.archive_db_path
            )

            archive_conn = sqlite3.connect(archive_path)
            archive_conn.row_factory = sqlite3.Row
            archive_conn.execute("PRAGMA journal_mode=WAL")

            archive_conn.execute("""
                CREATE TABLE IF NOT EXISTS cold_memories (
                    memory_id TEXT PRIMARY KEY, time_id TEXT, time_ts INTEGER, person_id TEXT,
                    nature_id TEXT, content TEXT, content_hash TEXT,
                    topics TEXT, tools TEXT, knowledge_types TEXT,
                    importance TEXT, valence REAL, arousal REAL, dominance REAL,
                    significance TEXT, confidence REAL, primary_emotions TEXT,
                    compound_emotions TEXT, owner_agent_id TEXT, visibility TEXT,
                    archived_at INTEGER, original_deleted INTEGER DEFAULT 0
                )
            """)

            archive_conn.execute("""
                INSERT OR REPLACE INTO cold_memories VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                mem.get("memory_id"), mem.get("time_id"), mem.get("time_ts"),
                mem.get("person_id"), mem.get("nature_id"), mem.get("content"),
                mem.get("content_hash"), json.dumps(mem.get("topics", []), ensure_ascii=False),
                json.dumps(mem.get("tools", []), ensure_ascii=False),
                json.dumps(mem.get("knowledge_types", []), ensure_ascii=False),
                mem.get("importance"), mem.get("valence"), mem.get("arousal"),
                mem.get("dominance"), mem.get("significance"), mem.get("confidence"),
                mem.get("primary_emotions"), mem.get("compound_emotions"),
                mem.get("owner_agent_id"), mem.get("visibility"),
                int(time.time()), 0
            ))
            archive_conn.commit()

            self._store.conn.execute(
                "UPDATE memories SET deleted = 1 WHERE memory_id = ?", (memory_id,)
            )
            self._store.conn.commit()
            archive_conn.close()

            self._stats["archivals"] += 1
            logger.debug(f"Archived cold memory: {memory_id}")
            return True

        except Exception as e:
            logger.warning("memory_tier: %s", e)
            return False

    def retrieve_from_cold(self, memory_id: str) -> Optional[dict]:
        """从归档库恢复冷记忆"""
        archive_path = os.path.join(
            os.path.dirname(self._store._db_path) if hasattr(self._store, '_db_path') else ".",
            self._config.archive_db_path
        )

        if not os.path.exists(archive_path):
            return None

        try:
            archive_conn = sqlite3.connect(archive_path)
            archive_conn.row_factory = sqlite3.Row
            row = archive_conn.execute(
                "SELECT * FROM cold_memories WHERE memory_id = ?", (memory_id,)
            ).fetchone()
            archive_conn.close()

            if row:
                result = dict(row)
                result["is_cold"] = True
                return result
            return None
        except Exception as e:
            logger.warning("memory_tier: %s", e)
            return None

    def restore_from_cold(self, memory_id: str) -> bool:
        """将冷记忆恢复到热层"""
        cold = self.retrieve_from_cold(memory_id)
        if not cold or not self._store:
            return False

        try:
            self._store.insert_memory(
                memory_id=cold["memory_id"], time_id=cold.get("time_id", ""),
                time_ts=cold["time_ts"], person_id=cold.get("person_id", ""),
                nature_id=cold.get("nature_id", ""), content=cold.get("content", ""),
                content_hash=cold.get("content_hash", ""),
                topics=json.loads(cold.get("topics", "[]")),
                tools=json.loads(cold.get("tools", "[]")),
                knowledge_types=json.loads(cold.get("knowledge_types", "[]")),
                importance=cold.get("importance", "medium"),
                valence=cold.get("valence", 0.0),
                arousal=cold.get("arousal", 0.0),
                dominance=cold.get("dominance", 0.5),
                significance=cold.get("significance", ""),
                confidence=cold.get("confidence", 0.0),
                primary_emotions=cold.get("primary_emotions", ""),
                compound_emotions=cold.get("compound_emotions", ""),
                owner_agent_id=cold.get("owner_agent_id", ""),
                visibility=cold.get("visibility", "private"),
            )

            archive_path = os.path.join(
                os.path.dirname(self._store._db_path) if hasattr(self._store, '_db_path') else ".",
                self._config.archive_db_path
            )
            archive_conn = sqlite3.connect(archive_path)
            archive_conn.execute(
                "DELETE FROM cold_memories WHERE memory_id = ?", (memory_id,)
            )
            archive_conn.commit()
            archive_conn.close()

            return True
        except Exception as e:
            logger.warning("memory_tier: %s", e)
            return False

    def _process_expired(self) -> int:
        """处理 TTL 过期的记忆"""
        if not self._store:
            return 0

        now = int(time.time())
        expired_count = 0

        try:
            rows = self._store.conn.execute(
                "SELECT memory_id, custom_ttl, time_ts FROM memories WHERE deleted = 0 AND custom_ttl IS NOT NULL AND custom_ttl > 0"
            ).fetchall()

            for row in rows:
                ttl = row["custom_ttl"] or self._config.default_ttl_days * 86400
                expiry = row["time_ts"] + ttl
                if expiry <= now:
                    self._store.conn.execute(
                        "UPDATE memories SET deleted = 1 WHERE memory_id = ?",
                        (row["memory_id"],)
                    )
                    expired_count += 1

            if expired_count > 0:
                self._store.conn.commit()
                self._stats["expirations"] += expired_count

        except sqlite3.OperationalError as e:
            logger.debug("memory_tier: expiration sweep: %s", e)

        return expired_count

    def _trigger_compression(self) -> int:
        """检测同类记忆并触发蒸馏压缩"""
        if not self._store or not self._distill:
            return 0

        try:
            topic_counts = self._store.conn.execute("""
                SELECT mt.topic as topic_code, COUNT(*) as cnt
                FROM memory_topics mt
                JOIN memories m ON mt.memory_id = m.memory_id
                WHERE m.deleted = 0
                GROUP BY mt.topic
                HAVING cnt >= ?
                LIMIT ?
            """, (self._config.compress_similar_threshold, self._config.compress_batch_size)).fetchall()

            compressed = 0
            for row in topic_counts:
                try:
                    self._distill.distill(since_ts=0)
                    compressed += 1
                except Exception as e:
                    logger.debug(f"Compression failed for topic {row['topic_code']}: {e}")

            if compressed > 0:
                self._stats["compressions"] += compressed

            return compressed
        except Exception:
            return 0

    def set_ttl(self, memory_id: str, ttl_days: int):
        """为记忆设置自定义 TTL"""
        if not self._store:
            return
        self._store.conn.execute(
            "UPDATE memories SET custom_ttl = ? WHERE memory_id = ?",
            (ttl_days * 86400, memory_id)
        )
        self._store.conn.commit()

    def get_ttl(self, memory_id: str) -> Optional[int]:
        """获取记忆的 TTL（天数）"""
        if not self._store:
            return None
        try:
            row = self._store.conn.execute(
                "SELECT custom_ttl, time_ts FROM memories WHERE memory_id = ?",
                (memory_id,)
            ).fetchone()
            if row:
                if row["custom_ttl"] and row["custom_ttl"] > 0:
                    return row["custom_ttl"] // 86400
                return self._config.default_ttl_days
        except sqlite3.OperationalError as e:
            logger.debug("memory_tier: ttl lookup: %s", e)
        return None

    def get_cold_stats(self) -> dict:
        """获取冷存储统计"""
        archive_path = os.path.join(
            os.path.dirname(self._store._db_path) if hasattr(self._store, '_db_path') else ".",
            self._config.archive_db_path
        )

        stats = {"cold_count": 0, "archive_size_mb": 0}
        if os.path.exists(archive_path):
            stats["archive_size_mb"] = os.path.getsize(archive_path) / (1024 * 1024)
            try:
                conn = sqlite3.connect(archive_path)
                count = conn.execute("SELECT COUNT(*) FROM cold_memories").fetchone()[0]
                conn.close()
                stats["cold_count"] = count
            except Exception as e:
                logger.warning("memory_tier: %s", e)
        return stats

    def get_tier_distribution(self) -> dict:
        """获取各层记忆分布"""
        hot_count = sum(1 for k in self._hot_cache.keys() if not k.startswith("access:"))

        warm_count = 0
        if self._store:
            try:
                warm_count = self._store.conn.execute(
                    "SELECT COUNT(*) FROM memories WHERE deleted = 0"
                ).fetchone()[0]
            except Exception as e:
                logger.warning("memory_tier: %s", e)

        cold_stats = self.get_cold_stats()

        return {
            "hot": hot_count,
            "warm": warm_count,
            "cold": cold_stats["cold_count"],
            "total": hot_count + warm_count + cold_stats["cold_count"],
        }