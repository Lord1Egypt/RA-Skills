"""
store.py - SQLite 存储层
所有结构化维度的 CRUD 操作
进程级锁 + 线程安全 + FTS5 全文搜索 + 查询缓存
"""

from __future__ import annotations

import sqlite3
import threading
import hashlib
import time
import json
import logging
import os
from collections import deque

from ..storage.base import AbstractMemoryStore
from ..storage.agent_manager import AgentManager
from ..storage.fts_manager import FTSManager
from ..storage.cache_manager_store import StoreCacheManager
from ..models import MemoryInput

from ._file_lock import _FileLock
from ._schema import SchemaMigrator
from ._tasks import TaskManager
from ._maintenance import MaintenanceManager
from .circuit_breaker import StoreCircuitBreaker, retry_with_backoff

from pathlib import Path
from contextlib import contextmanager

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).parent.parent / "memory.db"

SQLITE_MAX_VARIABLES = 999


def _safe_int_env(key, default, min_val=None, max_val=None):
    """Parse environment variable as int with validation."""
    raw = os.environ.get(key)
    if raw is None:
        return default
    try:
        val = int(raw)
    except ValueError:
        logger.warning("环境变量 %s='%s' 不是有效整数，使用默认值 %d", key, raw, default)
        return default
    if min_val is not None and val < min_val:
        logger.warning("环境变量 %s=%d 低于最小值 %d，使用最小值", key, val, min_val)
        return min_val
    if max_val is not None and val > max_val:
        logger.warning("环境变量 %s=%d 超过最大值 %d，使用最大值", key, val, max_val)
        return max_val
    return val


def _chunked_placeholders(ids: list, chunk_size: int = SQLITE_MAX_VARIABLES) -> list[tuple[str, list]]:
    chunks = []
    for i in range(0, len(ids), chunk_size):
        chunk = ids[i:i + chunk_size]
        chunks.append((",".join("?" * len(chunk)), chunk))
    return chunks


class MemoryStore(AbstractMemoryStore):
    _DEFAULT_CACHE_SIZE_KB = -16000

    # Connection management
    _CONN_CLEANUP_INTERVAL = 100   # Clean up dead thread connections every N calls
    _BUSY_TIMEOUT_MS = _safe_int_env("AGENT_MEMORY_BUSY_TIMEOUT", 5000, min_val=100, max_val=60000)  # SQLite busy timeout — fast fail is better than long wait

    # Content limits
    MAX_CONTENT_LENGTH = 50_000    # Max content length in characters

    # Cache limits
    _CACHE_MAX_SIZE = 1000         # Max items in LRU cache
    _CACHE_TTL_SECONDS = 300       # Cache TTL (5 minutes)

    # WAL auto-checkpoint
    _WAL_CHECKPOINT_INTERVAL = 1000  # Checkpoint every 1000 writes (increased from 100 for better bulk throughput)

    # Stats cache
    _STATS_CACHE_TTL = 60  # Cache stats for 60 seconds

    # Magic number constants (M3)
    _SECONDS_PER_DAY = 86400          # Seconds in a day
    _CONTENT_PREVIEW_LENGTH = 200     # Content preview truncation length

    # Count cache (M8)
    _COUNT_CACHE_TTL = 60             # Cache count() for 60 seconds

    def __init__(self, db_path: str = None, use_write_batcher: bool = False, batcher_config: dict = None, use_connection_pool: bool = False, pool_size: int = 20, permission_matrix=None, _degraded_mode=False):
        from ..utils import _validate_path
        self.db_path = str(db_path or DB_PATH)
        if self.db_path != ":memory:":
            self.db_path = _validate_path(self.db_path)
        self._lock_path = self.db_path + ".lock"
        self._local = threading.local()
        self._thread_lock = threading.Lock()
        self._cache_size_kb = _safe_int_env("AGENT_MEMORY_CACHE_SIZE_KB", self._DEFAULT_CACHE_SIZE_KB, min_val=1024, max_val=1048576)
        self._permission_matrix = permission_matrix
        self._degraded_mode = _degraded_mode

        # Circuit breaker for database operations
        self._circuit_breaker = StoreCircuitBreaker(
            failure_threshold=5,
            recovery_timeout=30.0,
        )

        # Connection pool (optional, replaces thread-local connections when enabled)
        self._connection_pool = None
        if use_connection_pool:
            from agent_memory.store.connection_pool import SQLiteConnectionPool
            self._connection_pool = SQLiteConnectionPool(self.db_path, max_connections=pool_size)

        # 委托管理器
        self._cache_mgr = StoreCacheManager(db_path=self.db_path)
        self._fts_mgr = FTSManager(conn_provider=lambda: self.conn)
        self._agent_mgr = AgentManager(
            conn_provider=lambda: self.conn,
            transaction_provider=self.transaction,
        )

        # Fix (Issue 3): 向量存储引用，由 MemorySystem 注入
        # 用于 write-through 清理（归档/删除时同步清理向量）
        self._embedding_store_ref = None

        # Fix (Issue 3): 最大记忆数限制
        self._max_memories = int(os.environ.get("AGENT_MEMORY_MAX_MEMORIES", "0"))  # 0=不限制

        # S5: 缓存计数器 — 避免 _enforce_max_memories 每次执行 COUNT(*)
        self._memory_count_cache = None  # (count, timestamp)
        self._count_cache_lock = threading.Lock()

        # Fix (#17): 连接追踪 — 记录所有线程的连接，支持 close_all()
        self._all_conns = {}
        self._all_conns_lock = threading.Lock()
        # Note: _write_count and _conn_cleanup_counter are incremented without locks.
        # This is acceptable: they trigger best-effort maintenance (WAL checkpoint,
        # stale connection cleanup) where slight inaccuracy is tolerable.
        self._conn_cleanup_counter = 0

        # WAL auto-checkpoint write counter
        self._write_count = 0

        # PII detection on write (optional, configurable)
        self._pii_check_on_write = os.environ.get("AGENT_MEMORY_PII_CHECK_ON_WRITE", "").lower() == "true"

        # Backup lock (threading.Lock for intra-process mutual exclusion)
        self._backup_lock = threading.Lock()

        # Stats cache
        self._stats_cache = None
        self._stats_cache_time = 0

        # Count cache (M8)
        self._cached_count = None
        self._cached_count_time = 0

        # Sub-managers
        self._schema = SchemaMigrator(self.get_connection, self.transaction)
        self._tasks_mgr = TaskManager(self.get_connection, self.transaction, self._invalidate_cache)
        self._maintenance = MaintenanceManager(
            self.get_connection, self, self.db_path, self._BUSY_TIMEOUT_MS
        )

        # Sub-managers (extracted responsibilities — lazy-initialized)
        self._version_mgr = None
        self._link_mgr = None
        self._stats_mgr = None

        # 先初始化连接，再建表，再初始化 FTS
        _ = self.conn  # 触发连接创建
        self._schema.ensure_schema(fts_mgr=self._fts_mgr)
        self._init_fts()

        # Write batcher for high-concurrency scenarios
        self._write_batcher = None
        if use_write_batcher:
            from .write_batcher import WriteBatcher
            config = batcher_config or {}
            self._write_batcher = WriteBatcher(self, **config)

        # StorageBackend interface (lazy-initialized)
        self._backend = None

        # Consent manager (optional, loaded from environment)
        self._consent_manager = None
        consent_file = os.environ.get("AGENT_MEMORY_CONSENT_FILE")
        if consent_file:
            try:
                from agent_memory.privacy.consent import ConsentManager
                self._consent_manager = ConsentManager(consent_file)
                logger.info(f"Consent manager loaded from {consent_file}")
            except Exception as e:
                logger.warning(f"Failed to load consent manager: {e}")

        # Auto-initialize crypto store for confidential memories
        self._crypto_store = None
        if os.environ.get("AGENT_MEMORY_ENCRYPTION_KEY") or os.environ.get("AGENT_MEMORY_AUTO_ENCRYPT", "").lower() == "true":
            try:
                from agent_memory.storage.crypto_store import CryptoStore
                self._crypto_store = CryptoStore(self)
                logger.info("CryptoStore initialized for automatic encryption")
            except Exception as e:
                logger.warning(f"CryptoStore initialization failed: {e}")

        # Startup integrity check (skip for in-memory / degraded mode)
        if not _degraded_mode and self.db_path != ":memory:":
            self._startup_integrity_check()

    @classmethod
    def create_degraded(cls):
        """Create a degraded in-memory store for when the main DB is unavailable."""
        store = cls(db_path=":memory:", _degraded_mode=True)
        logger.warning("Running in DEGRADED mode — using in-memory storage, data will be lost on restart")
        return store

    def get_connection(self) -> sqlite3.Connection:
        """获取当前线程的数据库连接（公共接口）。

        线程安全：每个线程首次调用时创建独立连接，后续复用。
        连接配置：WAL 模式 + 外键约束 + busy_timeout。
        """
        if not hasattr(self._local, 'conn') or self._local.conn is None:
            self._local.conn = sqlite3.connect(self.db_path, isolation_level=None)
            self._local.conn.row_factory = sqlite3.Row
            self._local.conn.execute("PRAGMA journal_mode=WAL")
            self._local.conn.execute("PRAGMA foreign_keys=ON")
            self._local.conn.execute("PRAGMA synchronous=NORMAL")
            self._local.conn.execute(f"PRAGMA cache_size={self._cache_size_kb}")
            self._local.conn.execute(f"PRAGMA busy_timeout={self._BUSY_TIMEOUT_MS}")
            with self._all_conns_lock:
                self._all_conns[threading.get_ident()] = self._local.conn
        self._conn_cleanup_counter += 1
        if self._conn_cleanup_counter % self._CONN_CLEANUP_INTERVAL == 0:
            self._cleanup_stale_conns()
        return self._local.conn

    def _cleanup_stale_conns(self):
        """Only close connections from dead threads, not active ones."""
        alive_tids = {t.ident for t in threading.enumerate() if t.is_alive() and t.ident is not None}
        stale = [tid for tid in list(self._all_conns.keys()) if tid not in alive_tids]
        for tid in stale:
            try:
                conn = self._all_conns.pop(tid, None)
                if conn:
                    conn.close()
            except Exception as e:
                logger.debug("连接关闭失败: %s", e)

    @property
    def conn(self):
        """线程安全的连接获取（委托给 get_connection()）"""
        return self.get_connection()

    @property
    def write_batcher(self):
        """Access the write batcher for batch submissions."""
        return self._write_batcher

    @property
    def pool(self):
        """Access the connection pool (if enabled)."""
        return self._connection_pool

    @property
    def backend(self):
        """Get the StorageBackend interface for this store."""
        if self._backend is None:
            from agent_memory.store.backend import SQLiteBackend
            self._backend = SQLiteBackend(self)
        return self._backend

    @property
    def versions(self):
        """Access the VersionManager."""
        if self._version_mgr is None:
            from agent_memory.store.version_manager import VersionManager
            self._version_mgr = VersionManager(self)
        return self._version_mgr

    @property
    def links(self):
        """Access the LinkManager."""
        if self._link_mgr is None:
            from agent_memory.store.link_manager import LinkManager
            self._link_mgr = LinkManager(self)
        return self._link_mgr

    @property
    def stats(self):
        """Access the StatsManager."""
        if self._stats_mgr is None:
            from agent_memory.store.stats_manager import StatsManager
            self._stats_mgr = StatsManager(self)
        return self._stats_mgr

    @contextmanager
    def transaction(self, process_safe: bool = True):
        """原子事务上下文管理器。

        Fix (P0): 移除 _FileLock — SQLite WAL 模式本身支持一个写者 + 多个读者并发，
        加 fcntl 文件锁会导致所有写操作完全串行化，多 Agent 场景下系统卡死。

        并发控制交给：
        - PRAGMA journal_mode=WAL（单写者 + 多读者）
        - PRAGMA busy_timeout=5000（写冲突时快速失败，由 circuit breaker 处理重试）
        - SQLite 内部的锁机制

        process_safe 参数保留向后兼容，但不再使用文件锁。
        文件锁 (_FileLock) 仅保留给注册表等非 SQLite 资源使用。
        """
        if not self._circuit_breaker.allow_request():
            raise RuntimeError("存储熔断器已开启 — 操作被拒绝")

        conn = self.conn
        try:
            conn.execute("BEGIN IMMEDIATE")
            yield conn
            conn.commit()
            self._circuit_breaker.record_success()
        except BaseException:
            conn.rollback()
            self._circuit_breaker.record_failure()
            raise

    def _init_fts(self):
        """初始化 FTS5 全文搜索（委托给 FTSManager）"""
        self._fts_mgr.init_fts()

    def _startup_integrity_check(self):
        """Check database integrity on startup. Attempt recovery if corrupted."""
        try:
            conn = self.conn
            result = conn.execute("PRAGMA integrity_check").fetchone()
            if isinstance(result, dict):
                status = result.get("integrity_check", "ok")
            else:
                status = result[0] if result else "unknown"

            if status != "ok":
                logger.error("Database integrity check FAILED: %s", status)
                return self._attempt_recovery()

            logger.debug("Database integrity check passed")
            return True
        except Exception as e:
            logger.error("Database integrity check error: %s", e)
            return self._attempt_recovery()

    def _attempt_recovery(self):
        """Attempt to recover from a corrupted database.

        Recovery strategy:
        1. Backup corrupted file
        2. Try to restore from most recent backup
        3. If no backup, create fresh database
        """
        import shutil
        from pathlib import Path

        corrupted_path = str(self.db_path) + ".corrupted"
        try:
            shutil.move(str(self.db_path), corrupted_path)
            logger.warning(f"Moved corrupted DB to {corrupted_path}")
        except Exception as e:
            logger.error(f"Failed to move corrupted DB: {e}")

        # Try to find and restore from backup
        backup_dir = Path(str(self.db_path)).parent / "backups"
        if backup_dir.exists():
            backups = sorted(backup_dir.glob("*.db"), key=lambda p: p.stat().st_mtime, reverse=True)
            if backups:
                latest_backup = backups[0]
                try:
                    shutil.copy2(str(latest_backup), str(self.db_path))
                    logger.info(f"Restored from backup: {latest_backup}")
                    return True
                except Exception as e:
                    logger.error(f"Failed to restore from backup {latest_backup}: {e}")

        # No backup available, will create fresh DB
        logger.warning("No backup available, creating fresh database")
        return False

    def execute_sql(self, sql, params=None, fetch=False):
        """Execute SQL through the store's managed connection.

        This is the ONLY method external code should use for direct SQL access.
        It provides:
        - Circuit breaker protection
        - Automatic retry with backoff
        - Connection management

        Args:
            sql: SQL statement
            params: Query parameters (tuple or dict)
            fetch: If True, return fetched rows; if False, return cursor

        Returns:
            List of rows if fetch=True, cursor otherwise
        """
        def _execute():
            conn = self.conn
            if params:
                cursor = conn.execute(sql, params)
            else:
                cursor = conn.execute(sql)

            if fetch:
                return [dict(row) for row in cursor.fetchall()]
            return cursor

        return retry_with_backoff(_execute, circuit_breaker=self._circuit_breaker)

    def execute_script(self, sql_script):
        """Execute multiple SQL statements (for schema creation).

        Args:
            sql_script: Multiple SQL statements separated by semicolons

        Returns:
            True if successful
        """
        def _execute():
            conn = self.conn
            conn.executescript(sql_script)
            return True

        return retry_with_backoff(_execute, circuit_breaker=self._circuit_breaker)

    def register_schema(self, component_name, schema_sql):
        """Register a component's schema with the store.

        Components should use this instead of directly creating tables.
        The schema is tracked and managed by SchemaMigrator.

        Args:
            component_name: Name of the component (e.g., "digital_twin", "achievements")
            schema_sql: CREATE TABLE IF NOT EXISTS statements

        Returns:
            True if schema was applied successfully
        """
        try:
            self.execute_script(schema_sql)
            logger.debug("Schema registered for component: %s", component_name)
            return True
        except Exception as e:
            logger.error("Failed to register schema for %s: %s", component_name, e)
            return False

    def rebuild_fts(self) -> dict:
        """
        Fix (Issue 2): 重建 FTS 索引（委托给 FTSManager）。

        S-15 安全确认: 使用 INSERT INTO ... SELECT 纯 SQL 语句填充 FTS，
        数据在 SQLite 引擎内部流转，不会加载到 Python 内存，无 OOM 风险。

        返回: {"rebuilt": bool, "count": int, "error": str}
        """
        result = self._fts_mgr.rebuild_fts()
        return result

    def _invalidate_cache(self):
        """写入时清除缓存 + 递增跨进程版本号（Fix #5）— 委托给 StoreCacheManager"""
        self._cache_mgr.invalidate_cache()

    def _maybe_wal_checkpoint(self):
        """Auto-checkpoint WAL if write count exceeds threshold."""
        self._write_count += 1
        if self._write_count >= self._WAL_CHECKPOINT_INTERVAL:
            self._write_count = 0
            try:
                conn = self.get_connection()
                conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
                logger.debug("WAL 自动 checkpoint 完成")
            except Exception as e:
                logger.warning("WAL checkpoint 失败: %s", e)

    # ── 写入 ──────────────────────────────────────────────

    def insert(self, mem: MemoryInput) -> str:
        return self.insert_memory(
            content=mem.content,
            importance=mem.importance,
            topics=mem.topics,
            nature_code=mem.nature_code,
            person_id=mem.person_id,
            tool_codes=mem.tool_codes,
            knowledge_codes=mem.knowledge_codes,
            emotion=mem.emotion,
            source=mem.source,
            agent_id=mem.agent_id,
            owner_agent_id=mem.owner_agent_id,
            team_id=mem.team_id,
            session_id=mem.session_id,
            memory_id=mem.memory_id,
            timestamp=mem.timestamp,
            expires_at=mem.expires_at,
            tags=mem.tags,
            metadata=mem.metadata,
            significance=mem.significance,
            is_private=mem.is_private,
            tenant_id=mem.tenant_id,
            embedding=mem.embedding,
            temporal_context=mem.temporal_context,
        )

    def insert_memory(
        self,
        memory_id: str,
        time_id: str,
        time_ts: int,
        person_id: str,
        nature_id: str,
        content: str,
        content_hash: str,
        topics: list[str] = None,
        tools: list[str] = None,
        knowledge_types: list[str] = None,
        importance: str = "medium",
        is_aggregated: bool = False,
        source_count: int = 1,
        owner_agent_id: str = "_system",
        visibility: str = "team",
        valence: float = 0.0,
        arousal: float = 0.2,
        dominance: float = 0.5,
        significance: str = "notable",
        confidence: float = 0.5,
        primary_emotions: str = "{}",
        compound_emotions: str = "[]",
        # Phase 2.1: 双时间线字段
        valid_from: float = None,
        valid_until: float = None,
        occurrence_time: float = None,
        mention_time: float = None,
        # 多租户隔离
        tenant_id: str = "default",
        # 原子覆写：INSERT OR REPLACE（用于 import_json overwrite 策略）
        upsert: bool = False,
        # 返回类型控制
        return_dict: bool = False,
        # 权限检查参数
        _requester_role: str = None,
        _requester_department: str = None,
    ):
        """写入一条记忆记录。

        参数:
            return_dict: 为 True 时始终返回 dict（含 memory_id + status），
                         为 False 时保持原有行为（正常返回 str，重复/空返回 dict）。
            _requester_role: 请求者角色（用于权限检查，如 "admin", "member"）
            _requester_department: 请求者部门（用于权限检查，如 "engineering"）

        返回:
            return_dict=False: memory_id (str) 或 dict（重复/空内容）
            return_dict=True:  {"memory_id": str, "status": str, ...}
        """
        # 权限检查：写入权限
        if self._permission_matrix and _requester_role and _requester_department:
            sensitivity = self._visibility_to_sensitivity(visibility)
            if not self._permission_matrix.check_access(_requester_role, _requester_department, sensitivity, "write"):
                if return_dict:
                    return {"memory_id": memory_id, "status": "permission_denied", "written": False, "reason": "权限不足：访问级别不够"}
                return {"memory_id": memory_id, "written": False, "reason": "权限不足：访问级别不够"}

        if content and len(content) > self.MAX_CONTENT_LENGTH:
            logger.warning("内容超长 (%d > %d)，将被截断", len(content), self.MAX_CONTENT_LENGTH)
            content = content[:self.MAX_CONTENT_LENGTH]
        with self.transaction() as conn:
            result = self._do_insert(conn, memory_id, time_id, time_ts, person_id, nature_id,
                            content, content_hash, topics, tools, knowledge_types,
                            importance, is_aggregated, source_count, owner_agent_id, visibility,
                            valence, arousal, dominance, significance, confidence,
                            primary_emotions, compound_emotions,
                            valid_from, valid_until, occurrence_time, mention_time,
                            tenant_id, upsert=upsert)
            if isinstance(result, dict) and result.get("reason") == "内容重复":
                if return_dict:
                    return {"memory_id": result.get("memory_id"), "status": "duplicate", "written": False, "reason": "内容重复"}
                return result
            if isinstance(result, dict) and result.get("reason") == "内容为空":
                if return_dict:
                    return {"memory_id": None, "status": "empty", "written": False, "reason": "内容为空"}
                return result
            if isinstance(result, dict) and result.get("status") == "duplicate_skipped":
                if return_dict:
                    return {"memory_id": result.get("memory_id"), "status": "duplicate_skipped", "written": False}
                return result
            self._invalidate_cache()
            if self._max_memories > 0:
                self._enforce_max_memories(conn=conn)
            self._maybe_wal_checkpoint()

        logger.info("memory_inserted", extra={
            "event": "memory_inserted",
            "memory_id": memory_id,
            "content_length": len(content) if content else 0,
            "tenant_id": tenant_id or "default",
        })
        if return_dict:
            return {"memory_id": memory_id, "status": "stored", "written": True}
        return memory_id

    def insert_memory_in_txn(
        self,
        txn_conn: sqlite3.Connection,
        memory_id: str,
        time_id: str,
        time_ts: int,
        person_id: str,
        nature_id: str,
        content: str,
        content_hash: str,
        topics: list[str] = None,
        tools: list[str] = None,
        knowledge_types: list[str] = None,
        importance: str = "medium",
        is_aggregated: bool = False,
        source_count: int = 1,
        owner_agent_id: str = "_system",
        visibility: str = "team",
        valence: float = 0.0,
        arousal: float = 0.2,
        dominance: float = 0.5,
        significance: str = "notable",
        confidence: float = 0.5,
        primary_emotions: str = "{}",
        compound_emotions: str = "[]",
        # Phase 2.1: 双时间线字段
        valid_from: float = None,
        valid_until: float = None,
        occurrence_time: float = None,
        mention_time: float = None,
        # 多租户隔离
        tenant_id: str = "default",
        # 返回类型控制
        return_dict: bool = False,
    ):
        """Fix (Issue 1): 在外部事务中写入记忆记录。

        由 pipeline.ingest() 调用，与 embedding_store.add() 共享同一事务，
        确保结构化数据+向量的原子性。

        txn_conn: 由 store.transaction() 提供的连接，调用方管理 commit/rollback。

        参数:
            return_dict: 为 True 时始终返回 dict（含 memory_id + status），
                         为 False 时保持原有行为。
        """
        result = self._do_insert(txn_conn, memory_id, time_id, time_ts, person_id, nature_id,
                        content, content_hash, topics, tools, knowledge_types,
                        importance, is_aggregated, source_count, owner_agent_id, visibility,
                        valence, arousal, dominance, significance, confidence,
                        primary_emotions, compound_emotions,
                        valid_from, valid_until, occurrence_time, mention_time,
                        tenant_id)
        if isinstance(result, dict) and result.get("reason") == "内容重复":
            if return_dict:
                return {"memory_id": result.get("memory_id"), "status": "duplicate", "written": False, "reason": "内容重复"}
            return result
        if isinstance(result, dict) and result.get("reason") == "内容为空":
            if return_dict:
                return {"memory_id": None, "status": "empty", "written": False, "reason": "内容为空"}
            return result
        if isinstance(result, dict) and result.get("status") == "duplicate_skipped":
            if return_dict:
                return {"memory_id": result.get("memory_id"), "status": "duplicate_skipped", "written": False}
            return result

        self._invalidate_cache()

        if self._max_memories > 0:
            self._enforce_max_memories(conn=txn_conn)

        if return_dict:
            return {"memory_id": memory_id, "status": "stored", "written": True}
        return memory_id

    def _sanitize_content(self, content: str) -> str:
        """Remove null bytes, control characters, and fix surrogate pairs."""
        if not content:
            return content
        # Remove null bytes
        content = content.replace('\x00', '')
        # Remove control characters except newline/tab
        content = ''.join(c for c in content if c >= ' ' or c in '\n\r\t')
        # Handle surrogate pairs — encode to utf-8 with errors='surrogatepass' then decode
        try:
            content.encode('utf-8', errors='strict')
        except UnicodeEncodeError:
            content = content.encode('utf-8', errors='surrogatepass').decode('utf-8', errors='replace')
        return content

    def _do_insert(
        self,
        conn: sqlite3.Connection,
        memory_id: str,
        time_id: str,
        time_ts: int,
        person_id: str,
        nature_id: str,
        content: str,
        content_hash: str,
        topics: list[str] = None,
        tools: list[str] = None,
        knowledge_types: list[str] = None,
        importance: str = "medium",
        is_aggregated: bool = False,
        source_count: int = 1,
        owner_agent_id: str = "_system",
        visibility: str = "team",
        valence: float = 0.0,
        arousal: float = 0.2,
        dominance: float = 0.5,
        significance: str = "notable",
        confidence: float = 0.5,
        primary_emotions: str = "{}",
        compound_emotions: str = "[]",
        # Phase 2.1: 双时间线字段
        valid_from: float = None,
        valid_until: float = None,
        occurrence_time: float = None,
        mention_time: float = None,
        # 多租户隔离
        tenant_id: str = "default",
        # 原子覆写
        upsert: bool = False,
    ):
        self._cache_mgr.increment_writes()

        # 空值守卫：content 为 None 或空白时直接返回
        if not content or not content.strip():
            return {"memory_id": None, "written": False, "reason": "内容为空"}
        content = content.strip()
        content = self._sanitize_content(content)

        # Auto-encrypt confidential memories
        if importance == "confidential" or visibility == "private":
            try:
                from agent_memory.storage.crypto_store import CryptoStore
                if not hasattr(self, '_crypto_store') or self._crypto_store is None:
                    self._crypto_store = CryptoStore(self)
                # The crypto store will handle encryption transparently
                content = self._crypto_store.encrypt_content(content, needs_encrypt=True)
                logger.debug("Auto-encrypted confidential memory content")
            except Exception as e:
                logger.warning(f"Failed to encrypt confidential memory: {e}")
                # In strict mode, reject unencrypted confidential data
                if os.environ.get("AGENT_MEMORY_STRICT_ENCRYPTION", "").lower() == "true":
                    return {"memory_id": "", "status": "encryption_failed", "reason": f"无法加密机密内容: {e}"}

        # Check for duplicate content
        computed_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        existing = conn.execute(
            "SELECT memory_id FROM memories WHERE content_hash=? AND deleted=0 LIMIT 1",
            (computed_hash,)
        ).fetchone()
        if existing:
            return {"memory_id": existing[0], "written": False, "reason": "内容重复"}

        insert_sql = "INSERT OR REPLACE INTO memories" if upsert else "INSERT OR IGNORE INTO memories"
        cursor = conn.execute(
            f"""{insert_sql}
               (memory_id, time_id, time_ts, person_id, nature_id,
                content, content_hash, importance, is_aggregated, source_count,
                owner_agent_id, visibility, valence, arousal, dominance,
                significance, confidence, primary_emotions, compound_emotions,
                valid_from, valid_until, occurrence_time, mention_time,
                tenant_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (memory_id, time_id, time_ts, person_id, nature_id,
             content, computed_hash, importance, int(is_aggregated), source_count,
             owner_agent_id, visibility, valence, arousal, dominance,
             significance, confidence, primary_emotions, compound_emotions,
             valid_from, valid_until, occurrence_time, mention_time,
             tenant_id),
        )

        # BUG-11: INSERT OR IGNORE 时检查是否实际插入了行
        if not upsert and cursor.rowcount == 0:
            logger.info("记忆 %s 已存在，跳过插入", memory_id)
            return {"memory_id": memory_id, "status": "duplicate_skipped"}

        # upsert 时先清理旧关联数据，再重新插入
        if upsert:
            self._delete_memory_associations(conn, [memory_id], include_embedding=False)

        if topics:
            for i, topic in enumerate(topics):
                conn.execute(
                    """INSERT OR IGNORE INTO memory_topics (memory_id, topic_code, is_primary)
                       VALUES (?, ?, ?)""",
                    (memory_id, topic, 1 if i == 0 else 0),
                )

        if tools:
            for tool_id in tools:
                conn.execute(
                    """INSERT OR IGNORE INTO memory_tools (memory_id, tool_id)
                       VALUES (?, ?)""",
                    (memory_id, tool_id),
                )

        if knowledge_types:
            for kid in knowledge_types:
                conn.execute(
                    """INSERT OR IGNORE INTO memory_knowledge (memory_id, knowledge_id)
                       VALUES (?, ?)""",
                    (memory_id, kid),
                )

        # 同步 FTS（在同一事务内，保证原子性）
        if self._fts_mgr.has_fts:
            try:
                # v12: 中文内容做 jieba 分词后写入 FTS
                from ..storage.fts_manager import _tokenize_chinese
                fts_content = _tokenize_chinese(content)
                conn.execute(
                    "INSERT OR IGNORE INTO memories_fts(memory_id, content) VALUES (?, ?)",
                    (memory_id, fts_content),
                )
            except Exception as e:
                logger.warning("store: FTS insert failed for memory %s: %s", memory_id, e)
                # S8: 不再设置全局 has_fts=False — 单条 FTS 写入失败不应影响后续写入

        # S5: insert 成功后递增缓存计数器
        with self._count_cache_lock:
            if self._memory_count_cache is not None:
                self._memory_count_cache = (self._memory_count_cache[0] + 1, self._memory_count_cache[1])

    def _delete_memory_associations(self, conn, memory_ids, include_fts=True, include_embedding=True):
        """Delete all association records for the given memory IDs.

        Eliminates the repeated DELETE FROM memory_topics/tools/knowledge/links pattern.
        """
        if not memory_ids:
            return
        for placeholders, chunk_ids in _chunked_placeholders(memory_ids):
            for table in ("memory_topics", "memory_tools", "memory_knowledge"):
                conn.execute(f"DELETE FROM {table} WHERE memory_id IN ({placeholders})", chunk_ids)
            if include_fts and self._fts_mgr.has_fts:
                try:
                    conn.execute(f"DELETE FROM memories_fts WHERE memory_id IN ({placeholders})", chunk_ids)
                except Exception as e:
                    logger.warning("store: %s", e)
        for placeholders, chunk_ids in _chunked_placeholders(memory_ids, SQLITE_MAX_VARIABLES // 2):
            conn.execute(
                f"DELETE FROM memory_links WHERE source_id IN ({placeholders}) OR target_id IN ({placeholders})",
                chunk_ids + chunk_ids,
            )
        if include_embedding and self._embedding_store_ref:
            try:
                self._embedding_store_ref.delete_batch(memory_ids)
            except Exception as e:
                logger.warning("store: %s", e)

    def _enforce_max_memories(self, conn=None):
        """
        Fix (Issue 3): 超过最大记忆数时自动清理。

        策略：
        1. 仅清理 low 重要度的记忆
        2. 按 quality_score（如有）或 time_ts 降序保留最新的
        3. high 重要度永不自动清理

        S5: 使用缓存计数器避免每次 COUNT(*) 全表扫描。
        缓存在 insert 成功时递增，delete/purge 时递减，超时后回退到 COUNT(*)。

        参数:
            conn: 可选的事务连接。如果提供，在同一事务内执行删除操作，
                  保证与调用方（如 insert_memory_in_txn）的原子性。
                  如果为 None，使用 self.conn。
        """
        effective_conn = conn or self.conn
        try:
            # S5: 优先使用缓存计数器
            count = self._get_cached_memory_count(effective_conn)
            if count <= self._max_memories:
                return

            excess = count - self._max_memories
            # 删除最旧的 low 记忆
            rows = effective_conn.execute(
                """SELECT memory_id FROM memories
                   WHERE importance = 'low' AND deleted=0
                   ORDER BY time_ts ASC, COALESCE(last_accessed_ts, 0) ASC
                   LIMIT ?""",
                (excess,),
            ).fetchall()

            to_delete = [r["memory_id"] for r in rows]

            # 如果 low 不够，删除最旧的 medium
            if len(to_delete) < excess:
                remaining = excess - len(to_delete)
                medium_rows = effective_conn.execute(
                    """SELECT memory_id FROM memories
                       WHERE importance = 'medium' AND deleted=0
                       ORDER BY time_ts ASC, COALESCE(last_accessed_ts, 0) ASC
                       LIMIT ?""",
                    (remaining,),
                ).fetchall()
                to_delete.extend(r["memory_id"] for r in medium_rows)

            if to_delete:
                self._delete_memory_associations(effective_conn, to_delete, include_embedding=False)
                # Delete the memories themselves
                for placeholders, chunk_ids in _chunked_placeholders(to_delete):
                    effective_conn.execute(f"DELETE FROM memories WHERE memory_id IN ({placeholders})", chunk_ids)

                if self._embedding_store_ref and to_delete:
                    try:
                        self._embedding_store_ref.delete_batch(to_delete)
                    except Exception as e:
                        logger.warning("嵌入删除失败（将在维护时清理）: %s", e)

                self._invalidate_cache()
                # S5: 更新缓存计数器
                self._decrement_memory_count_cache(len(to_delete))
                logger.info(f"容量清理: 删除 {len(to_delete)} 条记忆（上限 {self._max_memories}）")
        except Exception as e:
            logger.warning("store: %s", e)

    def cleanup_orphaned_embeddings(self):
        """Remove embeddings that have no corresponding memory in the DB."""
        if not self._embedding_store_ref:
            return 0
        try:
            all_embedding_ids = self._embedding_store_ref.list_ids() if hasattr(self._embedding_store_ref, 'list_ids') else []
            if not all_embedding_ids:
                return 0
            existing = set()
            for i in range(0, len(all_embedding_ids), 500):
                chunk = all_embedding_ids[i:i+500]
                placeholders = ",".join("?" * len(chunk))
                rows = self.conn.execute(
                    f"SELECT memory_id FROM memories WHERE memory_id IN ({placeholders})",
                    chunk
                ).fetchall()
                existing.update(r[0] for r in rows)
            orphans = [eid for eid in all_embedding_ids if eid not in existing]
            if orphans:
                self._embedding_store_ref.delete_batch(orphans)
                logger.info("清理了 %d 个孤立嵌入", len(orphans))
            return len(orphans)
        except Exception as e:
            logger.warning("孤立嵌入清理失败: %s", e)
            return 0

    def _batch_delete_memories(self, memory_ids: list[str], reason: str = "eviction"):
        """批量删除记忆（含关联清理 + 向量清理）"""
        if not memory_ids:
            return
        with self.transaction() as conn:
            self._delete_memory_associations(conn, memory_ids, include_embedding=False)
            for placeholders, chunk_ids in _chunked_placeholders(memory_ids):
                conn.execute(f"DELETE FROM memories WHERE memory_id IN ({placeholders})", chunk_ids)

        # 清理向量（Fix: 使用批量删除替代 N+1 循环）
        if self._embedding_store_ref:
            try:
                self._embedding_store_ref.delete_batch(memory_ids)
            except Exception as e:
                logger.warning("store: %s", e)

        self._invalidate_cache()
        # S5: 递减缓存计数器
        self._decrement_memory_count_cache(len(memory_ids))

    def delete_memory(self, memory_id: str, reason: str = "user_delete", permanent: bool = False) -> dict:
        """Delete a memory (soft by default, permanent if specified)."""
        mem = self.get_memory(memory_id)
        if not mem:
            return {"deleted": False, "memory_id": memory_id, "reason": "记忆不存在"}

        if permanent:
            self._batch_delete_memories([memory_id], reason=reason)
            logger.info("memory_deleted", extra={
                "event": "memory_deleted",
                "memory_id": memory_id,
                "permanent": True,
                "tenant_id": mem.get("tenant_id", "default"),
            })
            self._maybe_wal_checkpoint()
            return {"deleted": True, "memory_id": memory_id, "reason": reason, "soft_delete": False}

        # 软删除
        # Note: Soft delete retains PII in content field until purge_deleted() is called.
        # For GDPR compliance, call purge_deleted(older_than_days=3) regularly,
        # or set AGENT_MEMORY_AUTO_PURGE_DAYS=3 to auto-purge on maintain.
        now = time.time()
        with self.transaction() as conn:
            cursor = conn.execute(
                "UPDATE memories SET deleted=1, deleted_at=? WHERE memory_id=? AND deleted=0",
                (now, memory_id),
            )
            if cursor.rowcount == 0:
                return {"deleted": False, "memory_id": memory_id, "reason": "记忆不存在或已被删除"}
        self._invalidate_cache()
        # S5: 软删除递减缓存计数器
        self._decrement_memory_count_cache(1)
        logger.info("memory_deleted", extra={
            "event": "memory_deleted",
            "memory_id": memory_id,
            "permanent": False,
            "tenant_id": mem.get("tenant_id", "default"),
        })
        self._maybe_wal_checkpoint()
        return {"deleted": True, "memory_id": memory_id, "reason": reason, "soft_delete": True}

    def restore_memory(self, memory_id: str) -> dict:
        """Restore a soft-deleted memory."""
        _restore_start = time.time()
        with self.transaction() as conn:
            cursor = conn.execute(
                "UPDATE memories SET deleted=0, deleted_at=NULL WHERE memory_id=? AND deleted=1",
                (memory_id,),
            )
            if cursor.rowcount == 0:
                return {"restored": False, "memory_id": memory_id, "reason": "记忆不存在或未被软删除 — 确认ID正确且已使用 forget 删除"}
        self._invalidate_cache()
        # S5: 恢复递增缓存计数器
        with self._count_cache_lock:
            if self._memory_count_cache is not None:
                self._memory_count_cache = (self._memory_count_cache[0] + 1, self._memory_count_cache[1])
        _restore_elapsed = time.time() - _restore_start
        logger.info("memory_restored", extra={
            "event": "memory_restored",
            "memory_id": memory_id,
            "duration_ms": int(_restore_elapsed * 1000),
        })
        return {"restored": True, "memory_id": memory_id}

    def bookmark(self, memory_id: str) -> dict:
        """Bookmark a memory for quick access."""
        with self.transaction():
            conn = self.conn
            cursor = conn.execute(
                "UPDATE memories SET bookmarked = 1 WHERE memory_id = ? AND deleted = 0",
                (memory_id,),
            )
            if cursor.rowcount == 0:
                return {"bookmarked": False, "reason": "记忆不存在"}
            return {"bookmarked": True, "memory_id": memory_id}

    def unbookmark(self, memory_id: str) -> dict:
        """Remove bookmark from a memory."""
        with self.transaction():
            conn = self.conn
            conn.execute("UPDATE memories SET bookmarked = 0 WHERE memory_id = ?", (memory_id,))
            return {"unbookmarked": True, "memory_id": memory_id}

    def get_bookmarks(self, limit: int = 50, offset: int = 0) -> list:
        """Get all bookmarked memories."""
        conn = self.conn
        rows = conn.execute(
            "SELECT * FROM memories WHERE bookmarked = 1 AND deleted = 0 ORDER BY time_ts DESC LIMIT ? OFFSET ?",
            (limit, offset),
        ).fetchall()
        return [dict(r) for r in rows]

    def purge_deleted(self, older_than_days: int = 30) -> dict:
        """永久清理软删除超过指定天数的记录。

        参数:
            older_than_days: 清理多少天前的软删除记录（默认 30 天）

        返回: {"purged": int, "older_than_days": int}
        """
        cutoff = time.time() - older_than_days * self._SECONDS_PER_DAY
        # M9: 单条 DELETE + rowcount 替代 SELECT + 批量删除
        with self.transaction() as conn:
            # 先收集要删除的 ID（用于清理关联数据和向量）
            rows = conn.execute(
                "SELECT memory_id FROM memories WHERE deleted=1 AND deleted_at IS NOT NULL AND deleted_at < ?",
                (cutoff,),
            ).fetchall()
            memory_ids = [r["memory_id"] for r in rows]
            if not memory_ids:
                return {"purged": 0, "older_than_days": older_than_days}
            # 清理关联数据
            self._delete_memory_associations(conn, memory_ids, include_embedding=False)
            # 删除记忆本身
            for placeholders, chunk_ids in _chunked_placeholders(memory_ids):
                conn.execute(f"DELETE FROM memories WHERE memory_id IN ({placeholders})", chunk_ids)
        # 清理向量
        if self._embedding_store_ref:
            try:
                self._embedding_store_ref.delete_batch(memory_ids)
            except Exception as e:
                logger.warning("store: %s", e)
        self._invalidate_cache()
        logger.info(f"Purged {len(memory_ids)} soft-deleted memories older than {older_than_days} days")
        return {"purged": len(memory_ids), "older_than_days": older_than_days}

    def insert_link(
        self,
        source_id: str,
        target_id: str,
        link_type: str,
        weight: float = 1.0,
        reason: str = None,
    ):
        """插入一条关联关系。Delegates to LinkManager."""
        return self.links.insert_link(source_id, target_id, link_type, weight, reason)

    # ── 查询 ──────────────────────────────────────────────

    def get_memory(self, memory_id: str) -> dict | None:
        """Get a single memory by ID. Returns dict or None."""
        batch = self.get_memories([memory_id])
        if memory_id in batch:
            return batch[memory_id]
        return None

    def get_memories(self, memory_ids: list[str]) -> dict[str, dict]:
        """批量获取记忆（解决 N+1 查询问题）"""
        if not memory_ids:
            return {}
        ids = [mid for mid in dict.fromkeys(memory_ids) if mid]
        if not ids:
            return {}

        all_rows = []
        for placeholders, chunk_ids in _chunked_placeholders(ids):
            rows = self.conn.execute(
                f"SELECT * FROM memories WHERE memory_id IN ({placeholders}) AND deleted=0", chunk_ids
            ).fetchall()
            all_rows.extend(rows)

        topics_map = self._batch_get_topics(ids)
        tools_map = self._batch_get_tools(ids)
        knowledge_map = self._batch_get_knowledge(ids)
        links_map = self._batch_get_links(ids)

        result = {}
        for row in all_rows:
            mem = dict(row)
            mid = mem["memory_id"]
            mem["topics"] = topics_map.get(mid, [])
            mem["tools"] = tools_map.get(mid, [])
            mem["knowledge"] = knowledge_map.get(mid, [])
            mem["links"] = links_map.get(mid, [])
            result[mid] = mem
        return result

    # ── 记忆版本化（流式更新）────────────────────────

    def update_memory(
        self,
        memory_id: str,
        new_content: str,
        change_reason: str = None,
        importance: str = None,
        topics: list[str] = None,
    ) -> dict:
        """Update memory content and metadata. Creates a new version."""
        import json as _json

        with self.transaction() as conn:
            row = conn.execute(
                "SELECT content, content_hash, importance FROM memories WHERE memory_id = ? AND deleted=0",
                (memory_id,),
            ).fetchone()

            if not row:
                return {"memory_id": memory_id, "version": 0, "changed": False, "error": "未找到"}

            old_content = row["content"]
            old_importance = row["importance"]

            new_hash = hashlib.sha256(new_content.encode()).hexdigest()
            if new_hash == row["content_hash"]:
                return {"memory_id": memory_id, "version": 0, "changed": False, "reason": "内容完全相同"}

            current_topics = [t["code"] for t in self._batch_get_topics([memory_id]).get(memory_id, [])]

            ver_row = conn.execute(
                "SELECT COALESCE(MAX(version_id), 0) as v FROM memory_versions WHERE memory_id = ?",
                (memory_id,),
            ).fetchone()
            next_version = (ver_row["v"] if ver_row else 0) + 1

            conn.execute(
                """INSERT INTO memory_versions
                   (memory_id, content, content_hash, importance, topics_json, change_reason)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    memory_id,
                    old_content,
                    row["content_hash"],
                    old_importance,
                    _json.dumps(current_topics, ensure_ascii=False),
                    change_reason or "update",
                ),
            )

            update_fields = ["content = ?", "content_hash = ?", "created_at = strftime('%s','now')"]
            update_params = [new_content, new_hash]

            if importance is not None:
                update_fields.append("importance = ?")
                update_params.append(importance)

            update_params.append(memory_id)
            conn.execute(
                f"UPDATE memories SET {', '.join(update_fields)} WHERE memory_id = ?",
                update_params,
            )

            if topics is not None:
                conn.execute("DELETE FROM memory_topics WHERE memory_id = ?", (memory_id,))
                if topics:
                    # Batch insert instead of loop
                    values = [(memory_id, topic, 1 if i == 0 else 0) for i, topic in enumerate(topics)]
                    conn.executemany(
                        "INSERT OR IGNORE INTO memory_topics (memory_id, topic_code, is_primary) VALUES (?, ?, ?)",
                        values,
                    )

            if self._fts_mgr.has_fts:
                try:
                    from ..storage.fts_manager import _tokenize_chinese
                    conn.execute("DELETE FROM memories_fts WHERE memory_id = ?", (memory_id,))
                    conn.execute(
                        "INSERT INTO memories_fts(memory_id, content) VALUES (?, ?)",
                        (memory_id, _tokenize_chinese(new_content)),
                    )
                except Exception as e:
                    logger.warning("store: %s", e)

        self._invalidate_cache()
        self._maybe_wal_checkpoint()

        logger.info(f"记忆版本更新: {memory_id} → v{next_version} ({change_reason or 'update'})")
        return {
            "memory_id": memory_id,
            "version": next_version,
            "old_content": old_content[:self._CONTENT_PREVIEW_LENGTH],
            "new_content": new_content[:self._CONTENT_PREVIEW_LENGTH],
            "changed": True,
        }

    def revert_to_version(self, memory_id: str, version_number: int) -> dict:
        """Revert a memory to a specific version. Delegates to VersionManager.

        Args:
            memory_id: The memory to revert
            version_number: Version number to revert to (1-based)

        Returns:
            dict with 'reverted' bool and 'memory_id'
        """
        return self.versions.revert_to_version(memory_id, version_number)

    def get_memory_versions(self, memory_id: str) -> list[dict]:
        """获取记忆的完整版本历史（从旧到新）。Delegates to VersionManager.

        返回: [{"version_id": int, "content": str, "importance": str, "change_reason": str, "created_at": int}, ...]
        """
        return self.versions.get_versions(memory_id)

    def query(
        self,
        time_from: int = None,
        time_to: int = None,
        person_id: str = None,
        nature_id: str = None,
        topic_code: str = None,
        tool_id: str = None,
        knowledge_id: str = None,
        importance: str = None,
        keyword: str = None,
        significance: str = None,
        limit: int = 50,
        offset: int = 0,
        query_agent_id: str = None,
        team_id: str = "default",
        include_public: bool = True,
        # 权限过滤参数
        _role: str = None,
        _department: str = None,
    ) -> list[dict]:
        """Query memories with filters. Returns list[dict]."""
        _query_start = time.time()
        use_permission_filter = query_agent_id is not None

        # 生成缓存键
        cache_key_raw = f"q:{time_from}:{time_to}:{person_id}:{nature_id}:{topic_code}:{tool_id}:{knowledge_id}:{importance}:{keyword}:{significance}:{limit}:{offset}:{query_agent_id}:{team_id}"
        cache_key = f"qh:{hashlib.md5(cache_key_raw.encode()).hexdigest()}"
        cached = self._cache_mgr.cache_get(cache_key)
        if cached is not None:
            return cached

        # FTS 快速路径：仅关键词查询
        if keyword and self._fts_mgr.has_fts and not any([time_from, time_to, person_id, nature_id, topic_code, tool_id, knowledge_id, importance]):
            try:
                results = self._fts_mgr.query_fts(keyword, limit)
                if use_permission_filter:
                    results = self._apply_visibility_filter(results, query_agent_id, team_id, include_public)
                # 无 agent_id 时：单用户模式，不过滤 visibility
                self._cache_mgr.cache_set(cache_key, results)
                return results
            except Exception as e:
                logger.warning("store: FTS query failed (fast path): %s", e)
                # S8: 不再设置全局 has_fts=False — 单次查询失败不应禁用 FTS

        # 构建查询条件
        conditions = []
        params = []

        # 权限过滤条件
        if use_permission_filter:
            vis_clause, vis_params = self._build_visibility_where(query_agent_id, team_id, include_public)
            conditions.append(vis_clause)
            params.extend(vis_params)
        else:
            # 无 agent_id 时：单用户模式，所有可见性均可访问
            pass  # 不添加 visibility 过滤

        # 时间范围条件
        if time_from is not None:
            conditions.append("m.time_ts >= ?")
            params.append(time_from)
        if time_to is not None:
            conditions.append("m.time_ts <= ?")
            params.append(time_to)

        # 其他过滤条件
        if person_id:
            conditions.append("m.person_id = ?")
            params.append(person_id)
        if nature_id:
            conditions.append("m.nature_id = ?")
            params.append(nature_id)
        if importance:
            conditions.append("m.importance = ?")
            params.append(importance)
        if significance:
            conditions.append("m.significance = ?")
            params.append(significance)

        # 关键词查询
        if keyword:
            if self._fts_mgr.has_fts:
                try:
                    # 使用 FTS 加速关键词查询
                    fts_results = self._fts_mgr.query_fts(keyword, limit * 2)
                    fts_ids = [r["memory_id"] for r in fts_results]
                    if fts_ids:
                        chunks = _chunked_placeholders(fts_ids)
                        if len(chunks) == 1:
                            conditions.append(f"m.memory_id IN ({chunks[0][0]})")
                            params.extend(chunks[0][1])
                        else:
                            or_parts = []
                            for ph, chunk_ids in chunks:
                                or_parts.append(f"m.memory_id IN ({ph})")
                                params.extend(chunk_ids)
                            conditions.append(f"({' OR '.join(or_parts)})")
                    else:
                        # FTS 无结果，使用 LIKE
                        conditions.append("m.content LIKE ?")
                        params.append(f"%{keyword}%")
                except Exception as e:
                    logger.warning("store: FTS query failed (keyword path): %s", e)
                    # S8: 不再设置全局 has_fts=False
                    conditions.append("m.content LIKE ?")
                    params.append(f"%{keyword}%")
            else:
                conditions.append("m.content LIKE ?")
                params.append(f"%{keyword}%")

        # 构建 WHERE 子句
        where = " AND ".join(conditions) if conditions else "1=1"

        # 构建 SQL 查询
        joins = []
        if topic_code:
            joins.append("JOIN memory_topics mt ON m.memory_id = mt.memory_id")
        if tool_id:
            joins.append("JOIN memory_tools mt2 ON m.memory_id = mt2.memory_id")
        if knowledge_id:
            joins.append("JOIN memory_knowledge mk ON m.memory_id = mk.memory_id")

        join_clause = " ".join(joins)

        sql = f"""
            SELECT DISTINCT m.* FROM memories m
            {join_clause}
            WHERE m.deleted=0 AND {where}
            {"AND mt.topic_code LIKE ?" if topic_code else ""}
            {"AND mt2.tool_id = ?" if tool_id else ""}
            {"AND mk.knowledge_id = ?" if knowledge_id else ""}
            ORDER BY m.time_ts DESC
            LIMIT ? OFFSET ?
        """

        # 添加主题、工具、知识类型参数
        if topic_code:
            params.append(topic_code + "%")
        if tool_id:
            params.append(tool_id)
        if knowledge_id:
            params.append(knowledge_id)
        params.extend([limit, offset])

        # 执行查询
        rows = self.conn.execute(sql, params).fetchall()

        # 批量获取关联数据
        memory_ids = [row["memory_id"] for row in rows]
        topics_map = self._batch_get_topics(memory_ids)
        tools_map = self._batch_get_tools(memory_ids)
        knowledge_map = self._batch_get_knowledge(memory_ids)

        # 构建结果
        results = []
        for row in rows:
            mem = dict(row)
            mid = mem["memory_id"]
            mem["topics"] = topics_map.get(mid, [])
            mem["tools"] = tools_map.get(mid, [])
            mem["knowledge"] = knowledge_map.get(mid, [])
            results.append(mem)

        # 应用权限过滤
        if use_permission_filter:
            results = self._apply_visibility_filter(results, query_agent_id, team_id, include_public)

        # PermissionMatrix 读取权限过滤：按 sensitivity 过滤结果
        if self._permission_matrix and _role and _department:
            filtered = []
            for r in results:
                sensitivity = self._visibility_to_sensitivity(r.get("visibility", "team"))
                if self._permission_matrix.check_access(_role, _department, sensitivity, "read"):
                    filtered.append(r)
            results = filtered

        # 缓存结果
        self._cache_mgr.cache_set(cache_key, results)
        _query_elapsed = time.time() - _query_start
        logger.info("store_query_completed", extra={
            "event": "store_query_completed",
            "result_count": len(results),
            "duration_ms": int(_query_elapsed * 1000),
            "tenant_id": team_id or "default",
        })
        return results

    def _visibility_to_sensitivity(self, visibility: str) -> str:
        """Map store visibility values to PermissionMatrix sensitivity levels."""
        mapping = {
            "public": "public",
            "team": "internal",
            "private": "confidential",
            "restricted": "restricted",
        }
        return mapping.get(visibility, "internal")

    def _apply_visibility_filter(self, memories: list[dict], query_agent_id: str, team_id: str, include_public: bool) -> list[dict]:
        """应用可见性过滤（委托给 AgentManager）"""
        return self._agent_mgr.apply_visibility_filter(memories, query_agent_id, team_id, include_public)

    def _build_visibility_where(self, agent_id: str, team_id: str, include_public: bool = True) -> tuple[str, list]:
        """构建可见性 SQL WHERE 子句（M5: 消除 query() 和 query_agent_memories() 的重复逻辑）

        返回: (where_clause, params) — 可直接拼入 SQL 的 WHERE 条件和参数列表
        """
        vis_parts = []
        params = []
        vis_parts.append("m.owner_agent_id = ?")
        params.append(agent_id)
        vis_parts.append("(m.visibility = 'team' AND m.owner_agent_id IN (SELECT agent_id FROM agents WHERE team_id = ?))")
        params.append(team_id)
        if include_public:
            vis_parts.append("m.visibility = 'public'")
        vis_parts.append("(m.memory_id IN ("
            "SELECT memory_id FROM memory_permissions "
            "WHERE agent_id = ? AND (expires_at IS NULL OR expires_at > ?)"
        "))")
        params.append(agent_id)
        params.append(int(time.time()))
        return f"({' OR '.join(vis_parts)})", params

    def get_linked(self, memory_id: str, link_type: str = None, max_depth: int = 1) -> list[dict]:
        """Get linked memories. Delegates to LinkManager."""
        return self.links.get_linked(memory_id, link_type=link_type, depth=max_depth)

    # ── 待办任务管理（委托给 TaskManager）──────────────────

    def add_task(self, *args, **kwargs):
        return self._tasks_mgr.add_task(*args, **kwargs)

    def update_task_status(self, *args, **kwargs):
        return self._tasks_mgr.update_task_status(*args, **kwargs)

    def get_tasks(self, *args, **kwargs):
        return self._tasks_mgr.get_tasks(*args, **kwargs)

    def check_overdue(self, *args, **kwargs):
        return self._tasks_mgr.check_overdue(*args, **kwargs)

    def get_task_stats(self, *args, **kwargs):
        return self._tasks_mgr.get_task_stats(*args, **kwargs)

    # ── 内部方法 ──────────────────────────────────────────

    def _get_topics(self, memory_id: str) -> list[dict]:
        """Deprecated: use _batch_get_topics([memory_id]).get(memory_id, []) instead."""
        import warnings
        warnings.warn("_get_topics() is deprecated, use _batch_get_topics()", DeprecationWarning, stacklevel=2)
        rows = self.conn.execute(
            "SELECT topic_code, is_primary FROM memory_topics WHERE memory_id = ?", (memory_id,)
        ).fetchall()
        return [{"code": r["topic_code"], "is_primary": bool(r["is_primary"])} for r in rows]

    def _get_tools(self, memory_id: str) -> list[str]:
        """Deprecated: use _batch_get_tools([memory_id]).get(memory_id, []) instead."""
        import warnings
        warnings.warn("_get_tools() is deprecated, use _batch_get_tools()", DeprecationWarning, stacklevel=2)
        rows = self.conn.execute("SELECT tool_id FROM memory_tools WHERE memory_id = ?", (memory_id,)).fetchall()
        return [r["tool_id"] for r in rows]

    def _get_knowledge(self, memory_id: str) -> list[str]:
        """Deprecated: use _batch_get_knowledge([memory_id]).get(memory_id, []) instead."""
        import warnings
        warnings.warn("_get_knowledge() is deprecated, use _batch_get_knowledge()", DeprecationWarning, stacklevel=2)
        rows = self.conn.execute("SELECT knowledge_id FROM memory_knowledge WHERE memory_id = ?", (memory_id,)).fetchall()
        return [r["knowledge_id"] for r in rows]

    def _batch_get_relation(self, table, memory_id_col, select_cols, memory_ids, transform=None):
        """Generic batch relation fetcher. Eliminates duplicate chunking/query logic."""
        if not memory_ids:
            return {}
        result = {mid: [] for mid in memory_ids}
        for placeholders, chunk_ids in _chunked_placeholders(memory_ids):
            rows = self.conn.execute(
                f"SELECT {memory_id_col}, {select_cols} FROM {table} WHERE {memory_id_col} IN ({placeholders})",
                chunk_ids,
            ).fetchall()
            for row in rows:
                mid = row[0]
                if mid in result:
                    if transform:
                        result[mid].append(transform(row))
                    else:
                        result[mid].append(row[1:])
        return result

    def _batch_get_topics(self, memory_ids: list[str]) -> dict[str, list[dict]]:
        return self._batch_get_relation(
            "memory_topics", "memory_id", "topic_code, is_primary", memory_ids,
            transform=lambda row: {"code": row[1], "is_primary": bool(row[2])},
        )

    def _batch_get_tools(self, memory_ids: list[str]) -> dict[str, list[str]]:
        return self._batch_get_relation(
            "memory_tools", "memory_id", "tool_id", memory_ids,
            transform=lambda row: row[1],
        )

    def _batch_get_knowledge(self, memory_ids: list[str]) -> dict[str, list[str]]:
        return self._batch_get_relation(
            "memory_knowledge", "memory_id", "knowledge_id", memory_ids,
            transform=lambda row: row[1],
        )

    # S5: 缓存计数器辅助方法
    _MEMORY_COUNT_CACHE_TTL = 300  # 缓存有效期 5 分钟

    def _get_cached_memory_count(self, conn) -> int:
        """获取活跃记忆数，优先使用缓存，过期或无缓存时回退到 COUNT(*)。"""
        now = time.time()
        with self._count_cache_lock:
            if (self._memory_count_cache is not None and
                    now - self._memory_count_cache[1] < self._MEMORY_COUNT_CACHE_TTL):
                return self._memory_count_cache[0]
            # 回退到 COUNT(*)
            count = conn.execute("SELECT COUNT(*) FROM memories WHERE deleted=0").fetchone()[0]
            self._memory_count_cache = (count, now)
            return count

    def _decrement_memory_count_cache(self, n: int = 1):
        """递减缓存计数器（删除/清理时调用）。"""
        with self._count_cache_lock:
            if self._memory_count_cache is not None:
                self._memory_count_cache = (max(0, self._memory_count_cache[0] - n), self._memory_count_cache[1])

    def _batch_get_links(self, memory_ids: list[str]) -> dict[str, list[dict]]:
        if not memory_ids:
            return {}
        all_rows = []
        for placeholders, chunk_ids in _chunked_placeholders(memory_ids):
            rows = self.conn.execute(
                f"SELECT * FROM memory_links WHERE source_id IN ({placeholders}) OR target_id IN ({placeholders})",
                chunk_ids + chunk_ids,
            ).fetchall()
            all_rows.extend(rows)
        result = {}
        for r in all_rows:
            for mid in (r["source_id"], r["target_id"]):
                if mid in memory_ids:
                    result.setdefault(mid, []).append(dict(r))
        return result

    def close(self):
        """Close the store and release resources."""
        try:
            # WAL checkpoint before closing to prevent WAL file bloat
            for conn in list(self._all_conns.values()):
                try:
                    conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
                except Exception:
                    pass
        except Exception:
            pass
        finally:
            if self._write_batcher:
                self._write_batcher.stop(timeout=10)
            if hasattr(self._local, 'conn') and self._local.conn:
                self._local.conn.close()
                # Fix (#17): 从全局追踪中移除
                with self._all_conns_lock:
                    self._all_conns.pop(threading.get_ident(), None)
                self._local.conn = None

    def close_all(self):
        """Close all threads' database connections."""
        with self._all_conns_lock:
            for tid, conn in list(self._all_conns.items()):
                try:
                    conn.close()
                except Exception as e:
                    logger.warning("store: %s", e)
            self._all_conns.clear()
        if hasattr(self._local, 'conn'):
            self._local.conn = None

    # ── Agent 管理 ─────────────────────────────────────

    def register_agent(self, agent_id: str, agent_name: str, team_id: str = "default", capabilities: list[str] = None) -> dict:
        """注册 Agent（委托给 AgentManager）"""
        return self._agent_mgr.register_agent(agent_id, agent_name, team_id, capabilities)

    def get_agent(self, agent_id: str) -> dict | None:
        """获取 Agent 信息（委托给 AgentManager）"""
        return self._agent_mgr.get_agent(agent_id)

    def get_agents_batch(self, agent_ids: list[str]) -> dict[str, dict]:
        """批量获取 Agent 信息（委托给 AgentManager）"""
        return self._agent_mgr.get_agents_batch(agent_ids)

    def list_agents(self, team_id: str = None) -> list[dict]:
        """列出所有活跃 Agent（委托给 AgentManager）"""
        return self._agent_mgr.list_agents(team_id)

    # ── 权限管理 ───────────────────────────────────────

    def grant_permission(self, memory_id: str, agent_id: str, granted_by: str, permission: str = "read", expires_at: int = None) -> bool:
        """授予权限（委托给 AgentManager）"""
        return self._agent_mgr.grant_permission(memory_id, agent_id, granted_by, permission, expires_at)

    def revoke_permission(self, memory_id: str, agent_id: str) -> bool:
        """撤销权限（委托给 AgentManager）"""
        return self._agent_mgr.revoke_permission(memory_id, agent_id)

    def check_permission(self, memory_id: str, agent_id: str, required: str = "read") -> bool:
        """检查权限（委托给 AgentManager）"""
        return self._agent_mgr.check_permission(memory_id, agent_id, required)

    def check_permission_batch(self, memory_ids: list[str], agent_id: str, required: str = "read") -> set[str]:
        """批量检查权限（委托给 AgentManager）"""
        return self._agent_mgr.check_permission_batch(memory_ids, agent_id, required)

    def query_agent_memories(self, agent_id: str, team_id: str = "default", query_agent_id: str = None, include_public: bool = True, limit: int = 50, **kwargs) -> list[dict]:
        if not query_agent_id:
            return self.query(limit=limit, **kwargs)

        conditions = []
        params = []

        vis_clause, vis_params = self._build_visibility_where(query_agent_id, team_id, include_public)
        conditions.append(vis_clause)
        params.extend(vis_params)

        if agent_id:
            conditions.append("m.owner_agent_id = ?")
            params.append(agent_id)

        for field in ("importance", "nature_id", "person_id"):
            val = kwargs.get(field)
            if val:
                conditions.append(f"m.{field} = ?")
                params.append(val)
        if kwargs.get("time_from"):
            conditions.append("m.time_ts >= ?")
            params.append(kwargs["time_from"])
        if kwargs.get("time_to"):
            conditions.append("m.time_ts <= ?")
            params.append(kwargs["time_to"])

        where = " AND ".join(conditions) if conditions else "1=1"

        rows = self.conn.execute(
            f"SELECT * FROM memories m WHERE m.deleted=0 AND {where} ORDER BY m.time_ts DESC LIMIT ?",
            params + [limit],
        ).fetchall()

        memory_ids = [r["memory_id"] for r in rows]
        topics_map = self._batch_get_topics(memory_ids)
        tools_map = self._batch_get_tools(memory_ids)

        results = []
        for row in rows:
            mem = dict(row)
            mid = mem["memory_id"]
            mem["topics"] = topics_map.get(mid, [])
            mem["tools"] = tools_map.get(mid, [])
            results.append(mem)
        return results

    def get_aggregated_stats(self, owner_agent_id: str = "") -> dict:
        """Get aggregated stats with caching. Delegates to StatsManager."""
        return self.stats.get_aggregated_stats(owner_agent_id)

    # ── 跨 Agent 关联 ─────────────────────────────────

    def add_agent_association(self, source_agent: str, target_agent: str, memory_id: str, assoc_type: str = "shares_knowledge", reason: str = None) -> bool:
        try:
            with self.transaction() as conn:
                conn.execute(
                    """INSERT INTO agent_associations (source_agent, target_agent, memory_id, association_type, reason)
                       VALUES (?, ?, ?, ?, ?)""",
                    (source_agent, target_agent, memory_id, assoc_type, reason),
                )
            return True
        except Exception as e:
            logger.debug("store: link write: %s", e)
            return False

    def get_agent_associations(self, agent_id: str, direction: str = "both") -> list[dict]:
        if direction == "incoming":
            rows = self.conn.execute(
                """SELECT aa.*, m.content as memory_content, m.owner_agent_id
                   FROM agent_associations aa
                   JOIN memories m ON aa.memory_id = m.memory_id
                   WHERE aa.target_agent = ? AND m.deleted=0""", (agent_id,),
            ).fetchall()
        elif direction == "outgoing":
            rows = self.conn.execute(
                """SELECT aa.*, m.content as memory_content, m.owner_agent_id
                   FROM agent_associations aa
                   JOIN memories m ON aa.memory_id = m.memory_id
                   WHERE aa.source_agent = ? AND m.deleted=0""", (agent_id,),
            ).fetchall()
        else:
            rows = self.conn.execute(
                """SELECT aa.*, m.content as memory_content, m.owner_agent_id
                   FROM agent_associations aa
                   JOIN memories m ON aa.memory_id = m.memory_id
                   WHERE (aa.source_agent = ? OR aa.target_agent = ?) AND m.deleted=0""",
                (agent_id, agent_id),
            ).fetchall()
        return [dict(r) for r in rows]

    # ── 维护操作（委托给 MaintenanceManager）──────────────

    def get_io_stats(self, *args, **kwargs):
        return self._maintenance.get_io_stats(*args, **kwargs)

    def optimize(self, *args, **kwargs):
        return self._maintenance.optimize(*args, **kwargs)

    def vacuum(self, *args, **kwargs):
        return self._maintenance.vacuum(*args, **kwargs)

    def check_integrity(self, *args, **kwargs):
        return self._maintenance.check_integrity(*args, **kwargs)

    def auto_maintain(self, *args, **kwargs):
        return self._maintenance.auto_maintain(*args, **kwargs)

    def get_storage_stats(self, *args, **kwargs):
        return self._maintenance.get_storage_stats(*args, **kwargs)

    def count(self) -> int:
        """Return total memory count (excluding soft-deleted)."""
        now = time.time()
        if (self._cached_count is not None and
            now - self._cached_count_time < self._COUNT_CACHE_TTL):
            return self._cached_count
        row = self.conn.execute("SELECT COUNT(*) FROM memories WHERE deleted=0").fetchone()
        result = row[0] if row else 0
        self._cached_count = result
        self._cached_count_time = now
        return result

    def create_link(self, source_id: str, target_id: str, link_type: str, weight: float = 1.0, reason: str = ""):
        """Deprecated: use insert_link() instead."""
        return self.insert_link(source_id, target_id, link_type, weight, reason)

    def create_indexes(self):
        """Deprecated: schema is auto-created on init. This method is kept for backward compatibility only."""
        self._schema.ensure_schema(fts_mgr=self._fts_mgr)

    def backup(self, backup_path: str):
        """Create a backup of the database."""
        if not self._backup_lock.acquire(blocking=False):
            raise RuntimeError("另一个备份正在进行中")
        _backup_start = time.time()
        try:
            import os

            if not os.path.exists(self.db_path):
                logger.error(f"数据库文件不存在: {self.db_path}")
                return

            db_size = os.path.getsize(self.db_path)
            if db_size == 0:
                logger.error(f"数据库文件为空: {self.db_path}")
                return

            logger.info(f"开始在线备份: {self.db_path} ({db_size} bytes) -> {backup_path}")

            # 修复 Windows 上的权限问题：先删除旧备份
            if os.name == 'nt' and os.path.exists(backup_path):
                try:
                    os.unlink(backup_path)
                except Exception:
                    pass

            # 使用 SQLite backup API（在线备份，不阻塞读写）
            src_conn = sqlite3.connect(self.db_path)
            dst_conn = sqlite3.connect(backup_path)
            try:
                with dst_conn:
                    src_conn.backup(dst_conn)
                _backup_elapsed = time.time() - _backup_start
                backup_size = os.path.getsize(backup_path)
                logger.info("store_backup_completed", extra={
                    "event": "store_backup_completed",
                    "backup_path": backup_path,
                    "size_bytes": backup_size,
                    "duration_ms": int(_backup_elapsed * 1000),
                })
            finally:
                src_conn.close()
                dst_conn.close()
        except Exception as e:
            logger.error("备份失败: %s", e)
        finally:
            self._backup_lock.release()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __repr__(self):
        count = self._memory_count_cache[0] if self._memory_count_cache else '?'
        return f"MemoryStore(db={self.db_path!r}, memories={count})"
