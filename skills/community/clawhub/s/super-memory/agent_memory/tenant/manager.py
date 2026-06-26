"""Tenant management with isolation, quotas, and metering.

Fixes applied:
- Per-tenant locks instead of global lock (serialization bottleneck)
- _RateLimiter: periodic cleanup of expired windows + SQLite persistence
- Concurrent slots: TTL-based release with background cleanup thread
- Storage quota enforcement (max_memories, max_storage_mb)
- check_write_allowed() unified gate
"""
from __future__ import annotations

import json
import logging
import os
import sqlite3
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)

# How long a concurrent slot can be held before automatic release (seconds)
_CONCURRENT_SLOT_TTL = 30
# How often the cleanup thread runs (seconds)
_CLEANUP_INTERVAL = 10
# Run _cleanup_expired every N rate-limiter checks
_RATE_CLEANUP_INTERVAL = 100


class TenantTier(Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


@dataclass
class TenantQuota:
    max_memories: int = 10000
    max_storage_mb: float = 100.0
    max_requests_per_minute: int = 60
    max_requests_per_day: int = 10000
    max_concurrent_queries: int = 5
    allowed_operations: frozenset = field(default_factory=lambda: frozenset({
        "remember", "recall", "context", "delete", "feedback"
    }))

    @classmethod
    def for_tier(cls, tier: TenantTier) -> "TenantQuota":
        if tier == TenantTier.FREE:
            return cls(
                max_memories=10000,
                max_storage_mb=100.0,
                max_requests_per_minute=60,
                max_requests_per_day=10000,
                max_concurrent_queries=5,
                allowed_operations=frozenset({"remember", "recall", "context", "delete"}),
            )
        elif tier == TenantTier.PRO:
            return cls(
                max_memories=100000,
                max_storage_mb=1000.0,
                max_requests_per_minute=300,
                max_requests_per_day=100000,
                max_concurrent_queries=20,
                allowed_operations=frozenset({
                    "remember", "recall", "context", "delete", "feedback",
                    "maintain", "spirit", "export", "distill",
                }),
            )
        else:  # ENTERPRISE
            return cls(
                max_memories=-1,
                max_storage_mb=-1,
                max_requests_per_minute=-1,
                max_requests_per_day=-1,
                max_concurrent_queries=-1,
                allowed_operations=frozenset({
                    "remember", "recall", "context", "delete", "feedback",
                    "maintain", "spirit", "export", "distill", "federation",
                    "compliance", "audit", "admin",
                }),
            )


@dataclass
class TenantConfig:
    tenant_id: str
    name: str
    tier: TenantTier = TenantTier.FREE
    quota: Optional[TenantQuota] = None
    is_active: bool = True
    created_at: float = 0.0
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        if self.quota is None:
            self.quota = TenantQuota.for_tier(self.tier)
        if self.created_at == 0.0:
            self.created_at = time.time()


class _RateLimiter:
    """Sliding-window rate limiter with periodic cleanup and SQLite persistence."""

    def __init__(self, persist_db: Optional[sqlite3.Connection] = None):
        self._windows: dict[str, list[float]] = {}
        self._lock = threading.Lock()
        self._check_count = 0
        self._persist_db = persist_db
        # Restore persisted state on init
        if self._persist_db is not None:
            self._restore()

    def _restore(self):
        """Restore rate-limit windows from SQLite."""
        try:
            rows = self._persist_db.execute(
                "SELECT key, timestamps_json FROM rate_limit_state"
            ).fetchall()
            now = time.time()
            for row in rows:
                timestamps = json.loads(row[1])
                # Only restore non-expired entries (within 24h)
                valid = [t for t in timestamps if t > now - 86400]
                if valid:
                    self._windows[row[0]] = valid
        except Exception as e:
            logger.debug("Rate limiter restore failed: %s", e)

    def _persist(self):
        """Persist current rate-limit windows to SQLite."""
        if self._persist_db is None:
            return
        try:
            self._persist_db.execute("DELETE FROM rate_limit_state")
            for key, timestamps in self._windows.items():
                if timestamps:  # Only persist non-empty windows
                    self._persist_db.execute(
                        "INSERT INTO rate_limit_state (key, timestamps_json) VALUES (?, ?)",
                        (key, json.dumps(timestamps)),
                    )
            self._persist_db.commit()
        except Exception as e:
            logger.debug("Rate limiter persist failed: %s", e)

    def _cleanup_expired(self):
        """Remove keys with empty or fully-expired windows."""
        now = time.time()
        expired_keys = []
        for key, timestamps in self._windows.items():
            # Filter out expired timestamps
            self._windows[key] = [t for t in timestamps if t > now - 86400]
            if not self._windows[key]:
                expired_keys.append(key)
        for key in expired_keys:
            del self._windows[key]
        if expired_keys:
            self._persist()

    def check(self, tenant_id: str, operation: str, limit: int, window_sec: int = 60) -> dict:
        """Check rate limit and return detailed result.

        Returns:
            {"allowed": bool, "retry_after_seconds": int or None}
        """
        key = f"{tenant_id}:{operation}:{window_sec}"
        now = time.time()
        cutoff = now - window_sec

        with self._lock:
            self._check_count += 1
            if self._check_count % _RATE_CLEANUP_INTERVAL == 0:
                self._cleanup_expired()

            if key not in self._windows:
                self._windows[key] = []
            self._windows[key] = [t for t in self._windows[key] if t > cutoff]

            if len(self._windows[key]) >= limit:
                # Calculate retry_after: time until the oldest request in the window expires
                oldest = self._windows[key][0]
                retry_after = int(oldest + window_sec - now) + 1
                return {"allowed": False, "retry_after_seconds": max(retry_after, 1)}
            self._windows[key].append(now)
            # Periodically persist (every N checks, not every check)
            if self._check_count % _RATE_CLEANUP_INTERVAL == 0:
                self._persist()
            return {"allowed": True, "retry_after_seconds": None}


class TenantManager:
    """Manages tenant quotas, rate limiting, concurrent query limits, and metering.

    Fixes vs original:
    - Per-tenant locks instead of a single global lock
    - Rate limiter with cleanup and persistence
    - Concurrent slots with TTL-based auto-release
    - Storage quota enforcement
    """

    # Rate limiting defaults
    DEFAULT_RATE_WINDOW_SEC = 60        # Default rate limit window
    DEFAULT_DAILY_WINDOW_SEC = 86400    # 24 hours

    # Concurrent query defaults
    DEFAULT_MAX_CONCURRENT = 5          # Default max concurrent queries

    # Metering batch defaults
    _METERING_BATCH_SIZE = 100          # Flush every 100 records
    _METERING_FLUSH_INTERVAL = 5.0      # Or every 5 seconds

    def __init__(self, db_path: Optional[str] = None):
        from ..utils import _validate_path
        self.db_path = db_path or os.environ.get(
            "AGENT_MEMORY_TENANT_DB", ":memory:"
        )
        if self.db_path != ":memory:":
            self.db_path = _validate_path(self.db_path)
        self._tenants: dict[str, TenantConfig] = {}
        self._tenants_lock = threading.RLock()
        self._tenant_locks: dict[str, threading.Lock] = {}
        self._locks_lock = threading.Lock()  # protects _tenant_locks
        self._rate_limiter: Optional[_RateLimiter] = None
        # Concurrent tracking: tenant_id -> list of (slot_id, acquire_timestamp)
        self._concurrent: dict[str, list[tuple[str, float]]] = {}
        self._concurrent_lock = threading.Lock()
        self._slot_counter = 0
        self._metering_db: Optional[sqlite3.Connection] = None
        self._cleanup_thread: Optional[threading.Thread] = None
        self._shutdown_event = threading.Event()
        self._metering_buffer = []
        self._last_flush_time = time.time()
        self._metering_lock = threading.Lock()
        self._stopped = False
        self._init_metering()
        self._load_tenants_from_db()

    def _get_tenant_lock(self, tenant_id: str) -> threading.Lock:
        """Get or create a per-tenant lock."""
        with self._locks_lock:
            if tenant_id not in self._tenant_locks:
                self._tenant_locks[tenant_id] = threading.Lock()
            return self._tenant_locks[tenant_id]

    def _cleanup_tenant_lock(self, tenant_id: str):
        """Remove a per-tenant lock when tenant is removed."""
        with self._locks_lock:
            self._tenant_locks.pop(tenant_id, None)

    def _init_metering(self):
        if self.db_path == ":memory:":
            self._metering_db = sqlite3.connect(":memory:", check_same_thread=False)
        else:
            self._metering_db = sqlite3.connect(self.db_path, check_same_thread=False)
        self._metering_db.execute("""
            CREATE TABLE IF NOT EXISTS tenant_usage (
                tenant_id TEXT NOT NULL,
                operation TEXT NOT NULL,
                timestamp REAL NOT NULL,
                latency_ms REAL,
                memory_id TEXT,
                error INTEGER DEFAULT 0
            )
        """)
        self._metering_db.execute("""
            CREATE INDEX IF NOT EXISTS idx_usage_tenant_ts
            ON tenant_usage(tenant_id, timestamp)
        """)
        self._metering_db.execute("""
            CREATE TABLE IF NOT EXISTS rate_limit_state (
                key TEXT PRIMARY KEY,
                timestamps_json TEXT NOT NULL
            )
        """)
        self._metering_db.execute("""
            CREATE TABLE IF NOT EXISTS tenants (
                tenant_id TEXT PRIMARY KEY,
                tier TEXT NOT NULL DEFAULT 'free',
                config_json TEXT NOT NULL,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            )
        """)
        self._metering_db.commit()

        # Initialize rate limiter with persistence
        self._rate_limiter = _RateLimiter(persist_db=self._metering_db)

        # Start background cleanup thread for stale concurrent slots
        self._cleanup_thread = threading.Thread(
            target=self._cleanup_loop, daemon=True, name="tenant-concurrent-cleanup"
        )
        self._cleanup_thread.start()

        # Start periodic metering flush timer
        self._flush_timer = threading.Timer(self._METERING_FLUSH_INTERVAL, self._periodic_flush)
        self._flush_timer.daemon = True
        self._flush_timer.start()

    def _cleanup_loop(self):
        """Background thread that releases stale concurrent slots."""
        while not self._shutdown_event.is_set():
            self._shutdown_event.wait(_CLEANUP_INTERVAL)
            if self._shutdown_event.is_set():
                break
            self._release_stale_concurrent_slots()

    def _release_stale_concurrent_slots(self):
        """Release concurrent slots held longer than TTL."""
        now = time.time()
        with self._concurrent_lock:
            for tenant_id in list(self._concurrent.keys()):
                active = []
                released = 0
                for slot_id, acquire_ts in self._concurrent[tenant_id]:
                    if now - acquire_ts > _CONCURRENT_SLOT_TTL:
                        released += 1
                    else:
                        active.append((slot_id, acquire_ts))
                if released > 0:
                    self._concurrent[tenant_id] = active
                    logger.warning(
                        "Released %d stale concurrent slots for tenant %s",
                        released, tenant_id,
                    )

    def register_tenant(self, config: TenantConfig) -> TenantConfig:
        """Register a new tenant with configuration."""
        lock = self._get_tenant_lock(config.tenant_id)
        with lock:
            with self._tenants_lock:
                if config.tenant_id in self._tenants:
                    raise ValueError(f"租户 '{config.tenant_id}' 已存在")
                self._tenants[config.tenant_id] = config
            self._persist_tenant(config)
        logger.info("Registered tenant: %s (tier=%s)", config.tenant_id, config.tier.value)
        return config

    def get_tenant(self, tenant_id: str) -> Optional[TenantConfig]:
        with self._tenants_lock:
            return self._tenants.get(tenant_id)

    def update_tenant(self, tenant_id: str, **kwargs) -> Optional[TenantConfig]:
        lock = self._get_tenant_lock(tenant_id)
        with lock:
            with self._tenants_lock:
                config = self._tenants.get(tenant_id)
                if config is None:
                    return None
                for key, value in kwargs.items():
                    if hasattr(config, key):
                        setattr(config, key, value)
                if "tier" in kwargs:
                    config.quota = TenantQuota.for_tier(kwargs["tier"])
            self._persist_tenant(config)
            return config

    def deactivate_tenant(self, tenant_id: str) -> bool:
        lock = self._get_tenant_lock(tenant_id)
        with lock:
            with self._tenants_lock:
                config = self._tenants.get(tenant_id)
                if config is None:
                    return False
                config.is_active = False
        return True

    def check_quota(self, tenant_id: str, operation: str) -> tuple[bool, str, Optional[int]]:
        """Check if tenant has remaining quota."""
        with self._tenants_lock:
            config = self._tenants.get(tenant_id)
        if config is None:
            return False, f"租户 '{tenant_id}' 不存在，请确认租户ID或联系管理员", None
        if not config.is_active:
            return False, f"租户 '{tenant_id}' 已停用，请联系管理员恢复", None

        quota = config.quota

        if operation not in quota.allowed_operations:
            return False, f"当前套餐（{config.tier.value}）不支持此操作，请升级套餐", None

        if quota.max_requests_per_minute > 0:
            result = self._rate_limiter.check(
                tenant_id, operation, quota.max_requests_per_minute, window_sec=self.DEFAULT_RATE_WINDOW_SEC
            )
            if not result["allowed"]:
                retry_after = result["retry_after_seconds"]
                return False, f"请求频率超限（{quota.max_requests_per_minute}次/分钟），请稍后重试", retry_after

        if quota.max_requests_per_day > 0:
            result = self._rate_limiter.check(
                tenant_id, operation, quota.max_requests_per_day, window_sec=self.DEFAULT_DAILY_WINDOW_SEC
            )
            if not result["allowed"]:
                retry_after = result["retry_after_seconds"]
                return False, f"日请求量超限（{quota.max_requests_per_day}次/天），请明天再试或升级套餐", retry_after

        return True, "", None

    def check_storage_quota(self, tenant_id: str, memory_count: Optional[int] = None,
                            storage_bytes: Optional[int] = None) -> tuple[bool, str]:
        """Check storage quotas (memory count and storage size).

        The caller is responsible for providing current usage numbers
        (typically obtained from TenantIsolationManager.get_tenant_stats()).
        """
        with self._tenants_lock:
            config = self._tenants.get(tenant_id)
        if config is None:
            return False, f"Tenant '{tenant_id}' not found"

        quota = config.quota

        if quota.max_memories > 0 and memory_count is not None:
            if memory_count >= quota.max_memories:
                return False, f"Memory count limit exceeded: {memory_count}/{quota.max_memories}"

        if quota.max_storage_mb > 0 and storage_bytes is not None:
            storage_mb = storage_bytes / (1024 * 1024)
            if storage_mb >= quota.max_storage_mb:
                return False, f"存储空间超限（{storage_mb:.1f}/{quota.max_storage_mb}MB），请清理或升级套餐"

        return True, ""

    def check_write_allowed(self, tenant_id: str, operation: str = "remember",
                            memory_count: Optional[int] = None,
                            storage_bytes: Optional[int] = None) -> tuple[bool, str, Optional[int]]:
        """Unified gate that checks all quotas before allowing a write operation.

        Checks: tenant exists + active, operation allowed, rate limits,
        concurrent limits, storage quotas.

        Returns:
            (allowed, reason, retry_after_seconds)
        """
        # 1. Quota + rate limit
        allowed, reason, retry_after = self.check_quota(tenant_id, operation)
        if not allowed:
            return False, reason, retry_after

        # 2. Concurrent limit
        if not self.check_concurrent(tenant_id):
            with self._tenants_lock:
                config = self._tenants.get(tenant_id)
            limit = config.quota.max_concurrent_queries if config and hasattr(config, 'quota') else 0
            return False, f"并发查询超限（当前套餐最多 {limit} 个并发），请等待或升级套餐", None

        # 3. Storage quota
        allowed, reason = self.check_storage_quota(tenant_id, memory_count, storage_bytes)
        if not allowed:
            return False, reason, None

        return True, "", None

    def check_concurrent(self, tenant_id: str) -> bool:
        with self._tenants_lock:
            config = self._tenants.get(tenant_id)
        if config is None:
            return False
        limit = config.quota.max_concurrent_queries
        if limit <= 0:
            return True
        with self._concurrent_lock:
            current = len(self._concurrent.get(tenant_id, []))
            return current < limit

    def acquire_concurrent(self, tenant_id: str) -> str | None:
        """Acquire a concurrent execution slot. Returns slot_id or None.

        Returns:
            slot_id if slot acquired, None if no slots available.
            When tenant has no concurrent limit, returns "unlimited".
        """
        with self._concurrent_lock:
            with self._tenants_lock:
                config = self._tenants.get(tenant_id)
            if config is None:
                return None
            limit = config.quota.max_concurrent_queries
            if limit <= 0:
                return "unlimited"  # Changed from True to str
            current = len(self._concurrent.get(tenant_id, []))
            if current >= limit:
                return None
            self._slot_counter += 1
            slot_id = f"{tenant_id}:{self._slot_counter}"
            if tenant_id not in self._concurrent:
                self._concurrent[tenant_id] = []
            self._concurrent[tenant_id].append((slot_id, time.time()))
            return slot_id

    def release_concurrent(self, tenant_id: str, slot_id: str = None):
        """Release a previously acquired concurrent slot."""
        if slot_id == "unlimited":
            return  # No slot to release
        with self._concurrent_lock:
            if tenant_id not in self._concurrent:
                return
            slots = self._concurrent[tenant_id]
            if slot_id:
                # Remove the specific slot
                self._concurrent[tenant_id] = [s for s in slots if s[0] != slot_id]
            else:
                # Fallback: remove oldest (backward compatible)
                self._concurrent[tenant_id] = slots[1:] if len(slots) > 1 else []
            if not self._concurrent[tenant_id]:
                del self._concurrent[tenant_id]

    def record_usage(self, tenant_id: str, operation: str, latency_ms: float,
                     memory_id: Optional[str] = None, is_error: bool = False):
        """Record a usage event for billing."""
        with self._metering_lock:
            self._metering_buffer.append((
                tenant_id, operation, time.time(), latency_ms,
                memory_id, int(is_error)
            ))

            should_flush = (
                len(self._metering_buffer) >= self._METERING_BATCH_SIZE or
                time.time() - self._last_flush_time >= self._METERING_FLUSH_INTERVAL
            )

        if should_flush:
            self._flush_metering()

    def _flush_metering(self):
        """Flush buffered metering records to SQLite."""
        with self._metering_lock:
            if not self._metering_buffer:
                return
            records = self._metering_buffer[:]
            self._metering_buffer.clear()
            self._last_flush_time = time.time()

        try:
            self._metering_db.executemany(
                "INSERT INTO tenant_usage VALUES (?, ?, ?, ?, ?, ?)",
                records
            )
            self._metering_db.commit()
        except Exception as e:
            logger.warning("计量数据写入失败: %s", e)

    def _periodic_flush(self):
        """Periodically flush metering buffer."""
        self._flush_metering()
        if not self._stopped:
            self._flush_timer = threading.Timer(self._METERING_FLUSH_INTERVAL, self._periodic_flush)
            self._flush_timer.daemon = True
            self._flush_timer.start()

    def get_usage(self, tenant_id: str, since: float = 0) -> list[dict]:
        cursor = self._metering_db.execute(
            "SELECT operation, COUNT(*), AVG(latency_ms), SUM(error) "
            "FROM tenant_usage WHERE tenant_id = ? AND timestamp > ? "
            "GROUP BY operation",
            (tenant_id, since)
        )
        return [
            {"operation": row[0], "count": row[1], "avg_latency_ms": round(row[2] or 0, 2), "errors": row[3]}
            for row in cursor.fetchall()
        ]

    def get_billing_summary(self, tenant_id: str, period_days: int = 30) -> dict:
        since = time.time() - (period_days * 86400)
        usage = self.get_usage(tenant_id, since)
        with self._tenants_lock:
            config = self._tenants.get(tenant_id)
        return {
            "tenant_id": tenant_id,
            "tier": config.tier.value if config else "unknown",
            "period_days": period_days,
            "operations": usage,
            "total_requests": sum(u["count"] for u in usage),
            "total_errors": sum(u["errors"] for u in usage),
        }

    def list_tenants(self) -> list[TenantConfig]:
        with self._tenants_lock:
            return list(self._tenants.values())

    def remove_tenant(self, tenant_id: str) -> bool:
        """Remove a tenant and clean up its lock."""
        lock = self._get_tenant_lock(tenant_id)
        with lock:
            with self._tenants_lock:
                if tenant_id not in self._tenants:
                    return False
                del self._tenants[tenant_id]
            self._delete_tenant_from_db(tenant_id)
        self._cleanup_tenant_lock(tenant_id)
        # Clean up concurrent tracking
        with self._concurrent_lock:
            self._concurrent.pop(tenant_id, None)
        logger.info("Removed tenant: %s", tenant_id)
        return True

    def _persist_tenant(self, config: TenantConfig):
        """Persist tenant config to SQLite."""
        try:
            config_json = json.dumps({
                "tenant_id": config.tenant_id,
                "name": config.name,
                "tier": config.tier.value,
                "max_memories": config.quota.max_memories,
                "max_storage_mb": config.quota.max_storage_mb,
                "max_requests_per_minute": config.quota.max_requests_per_minute,
                "max_requests_per_day": config.quota.max_requests_per_day,
                "max_concurrent_queries": config.quota.max_concurrent_queries,
                "allowed_operations": list(config.quota.allowed_operations),
                "is_active": config.is_active,
                "created_at": config.created_at,
                "metadata": config.metadata,
            })
            self._metering_db.execute(
                """INSERT OR REPLACE INTO tenants (tenant_id, tier, config_json, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?)""",
                (config.tenant_id, config.tier.value, config_json, config.created_at, time.time())
            )
            self._metering_db.commit()
        except Exception as e:
            logger.warning("租户配置持久化失败: %s", e)

    def _delete_tenant_from_db(self, tenant_id: str):
        """Remove tenant config from SQLite."""
        try:
            self._metering_db.execute(
                "DELETE FROM tenants WHERE tenant_id = ?", (tenant_id,)
            )
            self._metering_db.commit()
        except Exception as e:
            logger.warning("租户配置删除失败: %s", e)

    def _load_tenants_from_db(self):
        """Load tenant configs from SQLite on startup."""
        try:
            rows = self._metering_db.execute(
                "SELECT tenant_id, config_json FROM tenants"
            ).fetchall()
            with self._tenants_lock:
                for row in rows:
                    try:
                        data = json.loads(row[1])
                        config = self._tenant_config_from_dict(data)
                        self._tenants[row[0]] = config
                    except Exception as e:
                        logger.warning("加载租户 %s 配置失败: %s", row[0], e)
                if self._tenants:
                    logger.info("从数据库加载了 %d 个租户配置", len(self._tenants))
        except Exception as e:
            logger.warning("加载租户配置失败: %s", e)

    def _tenant_config_from_dict(self, data: dict) -> TenantConfig:
        """Reconstruct TenantConfig from persisted dict."""
        tier = TenantTier(data.get("tier", "free"))
        quota = TenantQuota.for_tier(tier)
        # Override with persisted values
        quota.max_memories = data.get("max_memories", quota.max_memories)
        quota.max_storage_mb = data.get("max_storage_mb", quota.max_storage_mb)
        quota.max_requests_per_minute = data.get("max_requests_per_minute", quota.max_requests_per_minute)
        quota.max_requests_per_day = data.get("max_requests_per_day", quota.max_requests_per_day)
        quota.max_concurrent_queries = data.get("max_concurrent_queries", quota.max_concurrent_queries)
        if "allowed_operations" in data:
            quota.allowed_operations = frozenset(data["allowed_operations"])
        return TenantConfig(
            tenant_id=data["tenant_id"],
            name=data.get("name", data["tenant_id"]),
            tier=tier,
            quota=quota,
            is_active=data.get("is_active", True),
            created_at=data.get("created_at", 0.0),
            metadata=data.get("metadata", {}),
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def __repr__(self):
        return f"TenantManager(tenants={len(getattr(self, '_tenants', {}))})"

    def close(self):
        """Flush buffers and stop background threads."""
        self._stopped = True
        if self._flush_timer:
            self._flush_timer.cancel()
            self._flush_timer = None
        self._flush_metering()
        self._shutdown_event.set()
        if self._cleanup_thread and self._cleanup_thread.is_alive():
            self._cleanup_thread.join(timeout=5)
        # Persist rate limiter state before closing
        if self._rate_limiter is not None:
            self._rate_limiter._persist()
        if self._metering_db:
            self._metering_db.close()
