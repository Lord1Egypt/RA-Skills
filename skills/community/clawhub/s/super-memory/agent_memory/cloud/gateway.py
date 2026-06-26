"""Cloud API Gateway — multi-tenant routing, auth, rate limiting."""
from __future__ import annotations

import collections
import hashlib
import hmac
import json
import logging
import os
import sqlite3
import threading
import time
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)


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


class _TokenBucket:
    """Token bucket rate limiter for global QPS limiting."""

    def __init__(self, rate: float, capacity: int):
        """
        Args:
            rate: Tokens added per second
            capacity: Maximum tokens (burst capacity)
        """
        self.rate = rate
        self.capacity = capacity
        self._tokens = float(capacity)
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    def acquire(self, tokens: int = 1) -> tuple[bool, float]:
        """Try to acquire tokens. Returns (allowed, retry_after_seconds)."""
        with self._lock:
            now = time.monotonic()
            elapsed = now - self._last_refill
            self._tokens = min(self.capacity, self._tokens + elapsed * self.rate)
            self._last_refill = now

            if self._tokens >= tokens:
                self._tokens -= tokens
                return True, 0
            else:
                retry_after = (tokens - self._tokens) / self.rate
                return False, retry_after


@dataclass
class CloudConfig:
    api_key_hmac_secret: str = ""
    default_tier: str = "free"
    max_request_size_bytes: int = 1024 * 1024  # 1MB (see CloudGateway.MAX_REQUEST_SIZE_BYTES)
    enable_billing: bool = True
    enable_audit: bool = True
    cors_origins: list[str] = field(default_factory=list)
    max_json_depth: int = 20  # (see CloudGateway.MAX_JSON_DEPTH)
    db_path: str = ":memory:"

    @classmethod
    def from_env(cls) -> "CloudConfig":
        cors_str = os.environ.get("AGENT_MEMORY_CORS_ORIGINS", "")
        if cors_str.strip():
            cors_origins = [o.strip() for o in cors_str.split(",") if o.strip()]
        else:
            cors_origins = []
        return cls(
            api_key_hmac_secret=os.environ.get("AGENT_MEMORY_CLOUD_HMAC_SECRET", ""),
            default_tier=os.environ.get("AGENT_MEMORY_CLOUD_DEFAULT_TIER", "free"),
            enable_billing=os.environ.get("AGENT_MEMORY_CLOUD_BILLING", "true").lower() == "true",
            enable_audit=os.environ.get("AGENT_MEMORY_CLOUD_AUDIT", "true").lower() == "true",
            max_json_depth=int(os.environ.get("AGENT_MEMORY_MAX_JSON_DEPTH", "20")),
            db_path=os.environ.get("AGENT_MEMORY_CLOUD_DB_PATH", ":memory:"),
            cors_origins=cors_origins,
        )


class CloudGateway:
    # Request limits
    MAX_REQUEST_SIZE_BYTES = 1024 * 1024  # 1MB
    MAX_JSON_DEPTH = 20

    # Brute force protection
    BF_MAX_FAILURES = 5            # Max auth failures before block
    BF_BLOCK_SECONDS = 900         # 15 minutes block

    # Brute-force protection thresholds (internal)
    _BF_WINDOW_SECONDS = 300.0     # 5 minutes

    def __init__(self, config: Optional[CloudConfig] = None, tenant_manager=None, billing_engine=None):
        self.config = config or CloudConfig.from_env()
        self._tenant_manager = tenant_manager
        self._billing = billing_engine
        self._api_keys: dict[str, dict] = {}
        self._api_keys_lock = threading.Lock()
        self._request_log: collections.deque[dict] = collections.deque(maxlen=10000)

        # SQLite for API key persistence
        self._db = sqlite3.connect(self.config.db_path, check_same_thread=False)
        self._db_lock = threading.Lock()
        self._init_db()
        self._load_api_keys_from_db()

        # Global rate limiter: configurable via env
        global_qps = _safe_int_env("AGENT_MEMORY_GLOBAL_QPS", 1000, min_val=1)
        self._global_limiter = _TokenBucket(rate=global_qps, capacity=global_qps * 2)

    # ── Thread-safe DB helpers ────────────────────────────

    def _db_execute(self, sql, params=()):
        with self._db_lock:
            return self._db.execute(sql, params)

    def _db_executemany(self, sql, params_list):
        with self._db_lock:
            self._db.executemany(sql, params_list)

    def _db_commit(self):
        with self._db_lock:
            self._db.commit()

    # ── SQLite init & key persistence ──────────────────────

    def _init_db(self):
        self._db_execute("""
            CREATE TABLE IF NOT EXISTS api_keys (
                key_hash TEXT PRIMARY KEY,
                tenant_id TEXT NOT NULL,
                name TEXT,
                created_at REAL NOT NULL,
                last_used_at REAL,
                enabled INTEGER DEFAULT 1
            )
        """)
        self._db_execute("""
            CREATE INDEX IF NOT EXISTS idx_api_keys_tenant
            ON api_keys(tenant_id)
        """)
        self._db_execute("""CREATE TABLE IF NOT EXISTS brute_force_state (
            key TEXT PRIMARY KEY,
            fail_count INTEGER DEFAULT 0,
            locked_until REAL DEFAULT 0
        )""")
        self._db_commit()

    def _load_api_keys_from_db(self):
        """Load API keys from SQLite, reinitializing on corruption."""
        try:
            cursor = self._db.execute(
                "SELECT key_hash, tenant_id, name, created_at, last_used_at, enabled FROM api_keys"
            )
            with self._api_keys_lock:
                for row in cursor.fetchall():
                    key_hash, tenant_id, name, created_at, last_used_at, enabled = row
                    if enabled:
                        self._api_keys[key_hash] = {
                            "tenant_id": tenant_id,
                            "name": name,
                            "created_at": created_at,
                            "last_used_at": last_used_at,
                        }
                logger.info("Loaded %d API keys from SQLite", len(self._api_keys))
        except (sqlite3.DatabaseError, sqlite3.OperationalError) as e:
            logger.error("API Key 数据库损坏，正在重建: %s", e)
            try:
                self._db.close()
                if os.path.exists(self.config.db_path):
                    os.remove(self.config.db_path)
                self._db = sqlite3.connect(self.config.db_path, check_same_thread=False)
                self._init_db()
            except Exception as e2:
                logger.error("API Key 数据库重建失败: %s", e2)

    # ── API Key management ─────────────────────────────────

    def register_api_key(self, api_key: str, tenant_id: str, metadata: Optional[dict] = None):
        key_hash = self._hash_api_key(api_key)
        now = time.time()
        name = (metadata or {}).get("name", "")

        with self._api_keys_lock:
            self._api_keys[key_hash] = {
                "tenant_id": tenant_id,
                "name": name,
                "metadata": metadata or {},
                "created_at": now,
                "last_used_at": None,
            }

        self._db_execute(
            "INSERT OR REPLACE INTO api_keys (key_hash, tenant_id, name, created_at, last_used_at, enabled) "
            "VALUES (?, ?, ?, ?, NULL, 1)",
            (key_hash, tenant_id, name, now),
        )
        self._db_commit()
        logger.info("Registered API key for tenant: %s", tenant_id)

    def revoke_api_key(self, api_key: str):
        key_hash = self._hash_api_key(api_key)
        with self._api_keys_lock:
            self._api_keys.pop(key_hash, None)
        self._db_execute("DELETE FROM api_keys WHERE key_hash = ?", (key_hash,))
        self._db_commit()
        logger.info("Revoked API key (hash=%s…)", key_hash[:8])

    def list_api_keys(self, tenant_id: str) -> list[dict]:
        cursor = self._db_execute(
            "SELECT key_hash, tenant_id, name, created_at, last_used_at, enabled FROM api_keys WHERE tenant_id = ?",
            (tenant_id,),
        )
        result = []
        for row in cursor.fetchall():
            key_hash, tid, name, created_at, last_used_at, enabled = row
            result.append({
                "key_hash": key_hash,
                "tenant_id": tid,
                "name": name,
                "created_at": created_at,
                "last_used_at": last_used_at,
                "enabled": bool(enabled),
            })
        return result

    def authenticate(self, api_key: str) -> Optional[dict]:
        """Authenticate an API key. Returns tenant config or None."""
        if not api_key:
            return None
        key_hash = self._hash_api_key(api_key)
        with self._api_keys_lock:
            info = self._api_keys.get(key_hash)
            if info is not None:
                # Update last_used_at in both memory and SQLite
                now = time.time()
                info["last_used_at"] = now
        if info is not None:
            try:
                self._db_execute(
                    "UPDATE api_keys SET last_used_at = ? WHERE key_hash = ?",
                    (now, key_hash),
                )
                self._db_commit()
            except Exception:
                logger.warning("Failed to update last_used_at for key %s…", key_hash[:8])
        return info

    def _hash_api_key(self, api_key: str) -> str:
        if self.config.api_key_hmac_secret:
            return hmac.new(
                self.config.api_key_hmac_secret.encode(),
                api_key.encode(),
                hashlib.sha256,
            ).hexdigest()
        return hashlib.sha256(api_key.encode()).hexdigest()

    # ── Brute-force protection (DB-backed) ────────────────

    def _record_auth_failure(self, identifier: str):
        with self._db_lock:
            row = self._db.execute(
                "SELECT fail_count FROM brute_force_state WHERE key=?", (identifier,)
            ).fetchone()
            count = (row[0] + 1) if row else 1
            locked_until = time.time() + self.BF_BLOCK_SECONDS if count >= self.BF_MAX_FAILURES else 0
            self._db.execute(
                "INSERT OR REPLACE INTO brute_force_state VALUES (?, ?, ?)",
                (identifier, count, locked_until)
            )
            self._db.commit()

    def _record_auth_success(self, identifier: str):
        with self._db_lock:
            self._db.execute("DELETE FROM brute_force_state WHERE key=?", (identifier,))
            self._db.commit()

    def _is_blocked(self, identifier: str) -> bool:
        with self._db_lock:
            row = self._db.execute(
                "SELECT fail_count, locked_until FROM brute_force_state WHERE key=?",
                (identifier,)
            ).fetchone()
        if row and row[1] > time.time():
            return True  # Still locked
        return False

    def _get_bf_retry_after(self, identifier: str) -> Optional[int]:
        """Return seconds until the brute-force block expires for this identifier, or None."""
        with self._db_lock:
            row = self._db.execute(
                "SELECT locked_until FROM brute_force_state WHERE key=?",
                (identifier,)
            ).fetchone()
        if row and row[0] > time.time():
            remaining = int(row[0] - time.time()) + 1
            return remaining
        return None

    # ── JSON depth validation ──────────────────────────────

    @staticmethod
    def _measure_json_depth(obj) -> int:
        if isinstance(obj, dict):
            if not obj:
                return 1
            return 1 + max(CloudGateway._measure_json_depth(v) for v in obj.values())
        if isinstance(obj, list):
            if not obj:
                return 1
            return 1 + max(CloudGateway._measure_json_depth(v) for v in obj)
        return 0

    def validate_json_depth(self, data) -> bool:
        depth = self._measure_json_depth(data)
        return depth <= self.config.max_json_depth

    # ── Request processing ─────────────────────────────────

    def _authenticate_request(self, api_key: str, client_ip: str = "") -> tuple[bool, str, Optional[dict], Optional[int]]:
        """Authenticate a request with brute-force protection.

        Returns (success, error_message, key_info, retry_after_seconds).
        """
        # Check brute-force block for both IP and key hash
        identifiers = []
        if client_ip:
            identifiers.append(f"ip:{client_ip}")
        if api_key:
            identifiers.append(f"key:{self._hash_api_key(api_key)[:16]}")

        for ident in identifiers:
            if self._is_blocked(ident):
                retry_after = self._get_bf_retry_after(ident) or int(self.BF_BLOCK_SECONDS)
                logger.warning("Brute-force block active for %s, retry_after=%ds", ident, retry_after)
                return False, f"认证尝试过于频繁，请 {retry_after} 秒后重试", None, retry_after

        key_info = self.authenticate(api_key)
        if key_info is None:
            # Record failure for all identifiers
            for ident in identifiers:
                self._record_auth_failure(ident)
            return False, "API Key 无效，请检查或重新生成", None, None

        # Success — clear failure counters
        for ident in identifiers:
            self._record_auth_success(ident)
        return True, "", key_info, None

    def process_request(self, api_key: str, operation: str,
                        content_length: int = 0, client_ip: str = "",
                        request_body=None) -> tuple[bool, str, Optional[dict], Optional[int]]:
        """Process an authenticated API request with rate limiting."""
        # Global rate limit check
        allowed, retry_after = self._global_limiter.acquire()
        if not allowed:
            return False, f"系统繁忙，请 {int(retry_after) + 1} 秒后重试", None, int(retry_after) + 1

        # Auth with brute-force protection
        auth_ok, auth_msg, key_info, auth_retry_after = self._authenticate_request(api_key, client_ip)
        if not auth_ok:
            return False, auth_msg, None, auth_retry_after

        assert key_info is not None
        tenant_id: str = key_info["tenant_id"]

        if content_length > self.config.max_request_size_bytes:
            return False, "请求过大（最大 1MB），请减少内容后重试", key_info, None

        # JSON depth check
        if request_body is not None:
            if isinstance(request_body, str):
                try:
                    parsed = json.loads(request_body)
                except (json.JSONDecodeError, ValueError):
                    return False, "JSON 格式错误，请检查请求体", key_info, None
                if not self.validate_json_depth(parsed):
                    return False, "JSON 嵌套过深（最大 20 层），请简化数据结构", key_info, None
            elif not self.validate_json_depth(request_body):
                return False, "JSON 嵌套过深（最大 20 层），请简化数据结构", key_info, None

        # Billing/quota check via billing engine
        if self._billing and self.config.enable_billing:
            allowed, reason = self._billing.check_and_deduct(tenant_id, operation)
            if not allowed:
                return False, reason, key_info, None

        if self._tenant_manager:
            allowed, reason, retry_after = self._tenant_manager.check_quota(tenant_id, operation)
            if not allowed:
                return False, reason, key_info, retry_after

        return True, "", key_info, None

    def record_request(self, tenant_id: str, operation: str,
                       latency_ms: float, is_error: bool = False,
                       memory_id: Optional[str] = None):
        record = {
            "tenant_id": tenant_id,
            "operation": operation,
            "latency_ms": latency_ms,
            "is_error": is_error,
            "memory_id": memory_id,
            "timestamp": time.time(),
        }

        if self.config.enable_audit:
            self._request_log.append(record)

        if self._tenant_manager:
            self._tenant_manager.record_usage(
                tenant_id, operation, latency_ms, memory_id, is_error
            )

        if self._billing and self.config.enable_billing:
            self._billing.record_usage(tenant_id, operation, latency_ms, is_error)

    def get_request_log(self, tenant_id: Optional[str] = None, limit: int = 100) -> list[dict]:
        if tenant_id:
            logs = [r for r in self._request_log if r["tenant_id"] == tenant_id]
        else:
            logs = list(self._request_log)
        return logs[-limit:]

    def health_check(self) -> dict:
        """Return gateway health status."""
        return {
            "status": "healthy",
            "registered_keys": len(self._api_keys),
            "total_requests": len(self._request_log),
            "billing_enabled": self.config.enable_billing,
            "audit_enabled": self.config.enable_audit,
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def __repr__(self):
        return f"CloudGateway(keys={len(getattr(self, '_api_keys', {}))}, qps={getattr(self, '_global_limiter', None) and getattr(self._global_limiter, 'rate', 0) or 0})"

    def close(self):
        self._db.close()
