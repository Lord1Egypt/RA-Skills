"""账户抽象层（Account Abstraction）。

核心思想：主身份（灵魂私钥）只做"授权会话密钥"，日常操作由会话密钥签名。
会话密钥有三重约束：
  1. 额度上限（spend_limit）：累计操作金额不超过此值
  2. 时间上限（expires_at）：超过时间自动失效
  3. 操作范围（allowed_actions）：只能执行白名单内的操作

主身份可以随时吊销任何会话密钥。会话密钥用完即焚，主私钥几乎不暴露。

类似 ERC-4337 的设计哲学，但适配 Second-Reality 的灵魂身份体系。
"""

import time
import uuid
import logging
from typing import Dict, List, Optional, Set

logger = logging.getLogger(__name__)


class SessionKey:
    """会话密钥：有额度、时间、范围三重约束的临时授权密钥。"""

    def __init__(
        self,
        key_id: str,
        soul_hash: str,
        public_key_b64: str,
        spend_limit: float,
        expires_at: float,
        allowed_actions: Set[str],
        created_at: float,
        status: str = "active",
        spent_amount: float = 0.0,
    ):
        self.key_id = key_id
        self.soul_hash = soul_hash
        self.public_key_b64 = public_key_b64
        self.spend_limit = spend_limit
        self.expires_at = expires_at
        self.allowed_actions = allowed_actions
        self.created_at = created_at
        self.status = status  # active / revoked / expired / exhausted
        self.spent_amount = spent_amount

    def is_valid(self, action: str, amount: float, now: Optional[float] = None) -> tuple[bool, str]:
        """检查会话密钥是否可执行此操作。返回 (is_valid, reason)。"""
        now = now or time.time()
        if self.status != "active":
            return False, f"session key status={self.status}"
        if now > self.expires_at:
            return False, "session key expired"
        if action not in self.allowed_actions and "*" not in self.allowed_actions:
            return False, f"action '{action}' not in allowed_actions"
        if self.spent_amount + amount > self.spend_limit:
            return False, f"spend limit exceeded: {self.spent_amount + amount} > {self.spend_limit}"
        return True, "ok"

    def record_spend(self, amount: float) -> None:
        """记录已花费金额。"""
        self.spent_amount += amount
        if self.spent_amount >= self.spend_limit:
            self.status = "exhausted"
            logger.info("session key exhausted key_id=%s spent=%.2f limit=%.2f",
                        self.key_id, self.spent_amount, self.spend_limit)

    def to_dict(self) -> Dict:
        return {
            "key_id": self.key_id,
            "soul_hash": self.soul_hash,
            "public_key_b64": self.public_key_b64,
            "spend_limit": self.spend_limit,
            "expires_at": self.expires_at,
            "allowed_actions": sorted(self.allowed_actions),
            "created_at": self.created_at,
            "status": self.status,
            "spent_amount": self.spent_amount,
        }


class AccountAbstractionEngine:
    """账户抽象引擎：管理会话密钥的签发、验证、吊销。

    主身份（灵魂私钥）只做"授权会话密钥"，日常操作由会话密钥签名。
    """

    # 默认会话密钥参数
    DEFAULT_SPEND_LIMIT = 10_000.0
    DEFAULT_DURATION_SECONDS = 24 * 3600  # 24小时
    DEFAULT_ALLOWED_ACTIONS = {"read", "transfer_small", "interact"}

    def __init__(self, storage=None):
        self._storage = storage
        self._keys: Dict[str, SessionKey] = {}  # key_id -> SessionKey（内存缓存）
        self._init_storage()

    def _init_storage(self) -> None:
        if not self._storage:
            return
        self._storage.execute("""
            CREATE TABLE IF NOT EXISTS session_keys (
                key_id TEXT PRIMARY KEY,
                soul_hash TEXT NOT NULL,
                public_key_b64 TEXT NOT NULL,
                spend_limit REAL NOT NULL,
                expires_at REAL NOT NULL,
                allowed_actions TEXT NOT NULL,
                created_at REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'active',
                spent_amount REAL NOT NULL DEFAULT 0
            )
        """)
        self._storage.execute("CREATE INDEX IF NOT EXISTS idx_session_keys_soul ON session_keys(soul_hash)")
        self._storage.execute("CREATE INDEX IF NOT EXISTS idx_session_keys_status ON session_keys(status)")

    # ── 签发会话密钥 ──────────────────────────────────────────
    def issue_session_key(
        self,
        soul_hash: str,
        public_key_b64: str,
        spend_limit: Optional[float] = None,
        duration_seconds: Optional[int] = None,
        allowed_actions: Optional[Set[str]] = None,
    ) -> SessionKey:
        """主身份签发会话密钥。

        必须由主身份（灵魂私钥）签名授权后调用。此处只做落库，签名验证在上层完成。
        """
        key_id = uuid.uuid4().hex
        now = time.time()
        sk = SessionKey(
            key_id=key_id,
            soul_hash=soul_hash,
            public_key_b64=public_key_b64,
            spend_limit=spend_limit or self.DEFAULT_SPEND_LIMIT,
            expires_at=now + (duration_seconds or self.DEFAULT_DURATION_SECONDS),
            allowed_actions=allowed_actions or self.DEFAULT_ALLOWED_ACTIONS,
            created_at=now,
        )
        self._keys[key_id] = sk
        if self._storage:
            self._storage.execute(
                "INSERT INTO session_keys "
                "(key_id, soul_hash, public_key_b64, spend_limit, expires_at, "
                " allowed_actions, created_at, status, spent_amount) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    key_id, soul_hash, public_key_b64, sk.spend_limit, sk.expires_at,
                    ",".join(sorted(sk.allowed_actions)), now, "active", 0.0,
                ),
            )
        logger.info(
            "session key issued key_id=%s soul_hash=%s limit=%.2f expires=%ds actions=%d",
            key_id, soul_hash, sk.spend_limit, int(sk.expires_at - now), len(sk.allowed_actions),
        )
        return sk

    # ── 验证会话密钥 ──────────────────────────────────────────
    def validate_session_key(
        self,
        key_id: str,
        action: str,
        amount: float,
    ) -> tuple[bool, str, Optional[SessionKey]]:
        """验证会话密钥是否可执行此操作。返回 (is_valid, reason, session_key)。"""
        sk = self._get_key(key_id)
        if not sk:
            return False, "session key not found", None
        valid, reason = sk.is_valid(action, amount)
        return valid, reason, sk

    def consume_session_key(self, key_id: str, amount: float) -> bool:
        """消费会话密钥额度（操作执行成功后调用）。"""
        sk = self._get_key(key_id)
        if not sk:
            return False
        sk.record_spend(amount)
        if self._storage:
            self._storage.execute(
                "UPDATE session_keys SET spent_amount=?, status=? WHERE key_id=?",
                (sk.spent_amount, sk.status, key_id),
            )
        return True

    # ── 吊销会话密钥 ──────────────────────────────────────────
    def revoke_session_key(self, key_id: str, soul_hash: str) -> bool:
        """主身份吊销会话密钥。"""
        sk = self._get_key(key_id)
        if not sk or sk.soul_hash != soul_hash:
            return False
        sk.status = "revoked"
        if self._storage:
            self._storage.execute(
                "UPDATE session_keys SET status='revoked' WHERE key_id=?", (key_id,)
            )
        logger.info("session key revoked key_id=%s soul_hash=%s", key_id, soul_hash)
        return True

    def revoke_all_session_keys(self, soul_hash: str) -> int:
        """吊销某灵魂的所有活跃会话密钥（紧急情况）。"""
        count = 0
        for sk in self._keys.values():
            if sk.soul_hash == soul_hash and sk.status == "active":
                sk.status = "revoked"
                count += 1
        if self._storage:
            self._storage.execute(
                "UPDATE session_keys SET status='revoked' WHERE soul_hash=? AND status='active'",
                (soul_hash,),
            )
        logger.info("all session keys revoked soul_hash=%s count=%d", soul_hash, count)
        return count

    # ── 查询 ──────────────────────────────────────────────────
    def list_session_keys(self, soul_hash: str, include_inactive: bool = False) -> List[SessionKey]:
        """列出某灵魂的所有会话密钥。"""
        keys = [sk for sk in self._keys.values() if sk.soul_hash == soul_hash]
        if not include_inactive:
            keys = [sk for sk in keys if sk.status == "active"]
        return sorted(keys, key=lambda k: k.created_at, reverse=True)

    def get_session_key(self, key_id: str) -> Optional[SessionKey]:
        return self._get_key(key_id)

    # ── 内部 ──────────────────────────────────────────────────
    def _get_key(self, key_id: str) -> Optional[SessionKey]:
        if key_id in self._keys:
            return self._keys[key_id]
        # 从存储加载
        if self._storage:
            rows = self._storage.query(
                "SELECT key_id, soul_hash, public_key_b64, spend_limit, expires_at, "
                "allowed_actions, created_at, status, spent_amount "
                "FROM session_keys WHERE key_id=?",
                (key_id,),
            )
            if rows:
                r = rows[0]
                sk = SessionKey(
                    key_id=r[0], soul_hash=r[1], public_key_b64=r[2],
                    spend_limit=r[3], expires_at=r[4],
                    allowed_actions=set(r[5].split(",")) if r[5] else set(),
                    created_at=r[6], status=r[7], spent_amount=r[8],
                )
                self._keys[key_id] = sk
                return sk
        return None

    def cleanup_expired(self) -> int:
        """清理过期的会话密钥（标记为 expired）。返回清理数量。"""
        now = time.time()
        count = 0
        for sk in self._keys.values():
            if sk.status == "active" and now > sk.expires_at:
                sk.status = "expired"
                count += 1
        if self._storage:
            self._storage.execute(
                "UPDATE session_keys SET status='expired' WHERE status='active' AND expires_at < ?",
                (now,),
            )
        if count:
            logger.info("cleanup expired session keys count=%d", count)
        return count
