"""密钥轮换管理（Key Rotation Manager）。

服务端签名密钥定期轮换，降低密钥泄露后的风险窗口。
- 活跃密钥（active）：用于签名新 token
- 历史密钥（retired）：只用于验证旧 token，不用于签名
- 密钥泄露时可紧急吊销（revoked）

用户身份密钥（Ed25519）的轮换通过凭证层的 bind/revoke 实现，不在此模块。
"""

import time
import uuid
import logging
from typing import Dict, List, Optional

from .keys import generate_key

logger = logging.getLogger(__name__)


class RotatingKey:
    """一把可轮换的服务端签名密钥。"""

    def __init__(
        self,
        key_id: str,
        key_bytes: bytes,
        created_at: float,
        status: str = "active",
        retired_at: Optional[float] = None,
    ):
        self.key_id = key_id
        self.key_bytes = key_bytes
        self.created_at = created_at
        self.status = status  # active / retired / revoked
        self.retired_at = retired_at

    def is_active(self) -> bool:
        return self.status == "active"

    def can_verify(self) -> bool:
        """active 和 retired 都可用于验证，revoked 不行。"""
        return self.status in ("active", "retired")

    def to_dict(self) -> Dict:
        return {
            "key_id": self.key_id,
            "created_at": self.created_at,
            "status": self.status,
            "retired_at": self.retired_at,
        }


class KeyRotationManager:
    """服务端签名密钥轮换管理器。

    默认轮换周期 30 天，可配置。每次轮换生成新密钥，旧密钥自动 retired。
    历史密钥保留用于验证旧 token，直到超过保留期后可清理。
    """

    DEFAULT_ROTATION_SECONDS = 30 * 24 * 3600  # 30天
    DEFAULT_RETENTION_SECONDS = 90 * 24 * 3600  # 历史密钥保留90天

    def __init__(
        self,
        storage=None,
        rotation_seconds: int = DEFAULT_ROTATION_SECONDS,
        retention_seconds: int = DEFAULT_RETENTION_SECONDS,
    ):
        self._storage = storage
        self.rotation_seconds = rotation_seconds
        self.retention_seconds = retention_seconds
        self._keys: Dict[str, RotatingKey] = {}
        self._active_key_id: Optional[str] = None
        self._init_storage()
        self._load_from_storage()

    def _init_storage(self) -> None:
        if not self._storage:
            return
        self._storage.execute("""
            CREATE TABLE IF NOT EXISTS key_rotation (
                key_id TEXT PRIMARY KEY,
                key_bytes BLOB NOT NULL,
                created_at REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'active',
                retired_at REAL
            )
        """)
        self._storage.execute("CREATE INDEX IF NOT EXISTS idx_kr_status ON key_rotation(status)")

    def _load_from_storage(self) -> None:
        if not self._storage:
            return
        rows = self._storage.query(
            "SELECT key_id, key_bytes, created_at, status, retired_at FROM key_rotation"
        )
        for r in rows:
            rk = RotatingKey(
                key_id=r[0], key_bytes=bytes(r[1]), created_at=r[2],
                status=r[3], retired_at=r[4],
            )
            self._keys[rk.key_id] = rk
            if rk.is_active():
                self._active_key_id = rk.key_id

    # ── 核心接口 ──────────────────────────────────────────────
    def get_active_key(self) -> RotatingKey:
        """获取当前活跃密钥（用于签名）。如果没有则创建。"""
        if self._active_key_id and self._active_key_id in self._keys:
            return self._keys[self._active_key_id]
        return self._create_initial_key()

    def get_key_for_verification(self, key_id: str) -> Optional[RotatingKey]:
        """根据 key_id 获取密钥（用于验证 token）。active 和 retired 都可返回。"""
        rk = self._keys.get(key_id)
        if rk and rk.can_verify():
            return rk
        return None

    def rotate_if_needed(self) -> Optional[RotatingKey]:
        """检查是否需要轮换，需要则轮换。返回新密钥（如果轮换了）或 None。"""
        if not self._active_key_id:
            return self._create_initial_key()
        active = self._keys[self._active_key_id]
        now = time.time()
        if now - active.created_at >= self.rotation_seconds:
            return self.rotate()
        return None

    def rotate(self) -> RotatingKey:
        """强制轮换：生成新活跃密钥，旧密钥 retired。"""
        now = time.time()
        # 旧密钥 retired
        if self._active_key_id:
            old = self._keys[self._active_key_id]
            old.status = "retired"
            old.retired_at = now
            if self._storage:
                self._storage.execute(
                    "UPDATE key_rotation SET status='retired', retired_at=? WHERE key_id=?",
                    (now, old.key_id),
                )
            logger.info("key retired key_id=%s after %.1f days",
                        old.key_id, (now - old.created_at) / 86400)
        # 新密钥 active
        new_key = self._create_key(now)
        logger.info("key rotated new_key_id=%s", new_key.key_id)
        return new_key

    def revoke_key(self, key_id: str) -> bool:
        """紧急吊销密钥（泄露时用）。吊销后该密钥不能用于验证。"""
        rk = self._keys.get(key_id)
        if not rk:
            return False
        rk.status = "revoked"
        if self._storage:
            self._storage.execute(
                "UPDATE key_rotation SET status='revoked' WHERE key_id=?", (key_id,)
            )
        logger.warning("key REVOKED key_id=%s (emergency)", key_id)
        # 如果吊销的是活跃密钥，立即创建新的
        if key_id == self._active_key_id:
            self._active_key_id = None
            self._create_initial_key()
        return True

    def cleanup_retired(self) -> int:
        """清理超过保留期的 retired 密钥。返回清理数量。"""
        now = time.time()
        cutoff = now - self.retention_seconds
        to_delete = [
            kid for kid, rk in self._keys.items()
            if rk.status == "retired" and rk.retired_at and rk.retired_at < cutoff
        ]
        for kid in to_delete:
            del self._keys[kid]
            if self._storage:
                self._storage.execute("DELETE FROM key_rotation WHERE key_id=?", (kid,))
        if to_delete:
            logger.info("cleanup retired keys count=%d (older than %.0f days)",
                        len(to_delete), self.retention_seconds / 86400)
        return len(to_delete)

    def list_keys(self, include_revoked: bool = False) -> List[RotatingKey]:
        """列出所有密钥（按创建时间倒序）。"""
        keys = list(self._keys.values())
        if not include_revoked:
            keys = [rk for rk in keys if rk.status != "revoked"]
        return sorted(keys, key=lambda k: k.created_at, reverse=True)

    # ── 内部 ──────────────────────────────────────────────────
    def _create_key(self, now: float) -> RotatingKey:
        key_id = uuid.uuid4().hex
        key_bytes = generate_key()
        rk = RotatingKey(key_id=key_id, key_bytes=key_bytes, created_at=now, status="active")
        self._keys[key_id] = rk
        self._active_key_id = key_id
        if self._storage:
            self._storage.execute(
                "INSERT INTO key_rotation (key_id, key_bytes, created_at, status, retired_at) "
                "VALUES (?, ?, ?, 'active', NULL)",
                (key_id, key_bytes, now),
            )
        return rk

    def _create_initial_key(self) -> RotatingKey:
        """创建初始活跃密钥（首次启动或活跃密钥被吊销后）。"""
        return self._create_key(time.time())
