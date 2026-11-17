"""第 2 层：认证层（Session Manager）。

有状态会话：access token（短 TTL）+ refresh token（可轮换、可撤销）。
替代原无状态 HMAC token，支持即时吊销（丢设备一键踢下线）。

存储抽象（状态可外置）：SessionStore 接口。
  - SqliteSessionStore  默认：与账本同库 sessions 表，进程重启不丢失
  - MemorySessionStore  本地测试 / 无状态演示：进程内 dict，重启即失
  - RedisSessionStore   生产：跨实例共享，支持 TTL 自动清理
签名密钥经 KMS 抽象托管（可插拔 HSM）。
"""

import base64
import hashlib
import hmac
import json
import logging
import secrets
import threading
import time
import uuid

logger = logging.getLogger(__name__)


# ============================================================
# SessionStore 接口：第 2 层会话状态可外置（内存/SQLite/Redis）
# ============================================================


class SessionStore:
    """会话存储抽象：不绑定具体后端，供多数据中心部署切换。"""

    def save(
        self,
        session_id: str,
        soul_hash: str,
        refresh_hash: str,
        created_at: float,
        expires_at: float,
    ) -> None:
        raise NotImplementedError

    def get_by_refresh(self, refresh_hash: str):
        """按 refresh 哈希取会话，返回 (session_id, soul_hash, expires_at, revoked) 或 None。"""
        raise NotImplementedError

    def revoke(self, soul_hash: str, session_id: str = None) -> None:
        """吊销会话；session_id 为 None 时吊销该 soul 全部会话。"""
        raise NotImplementedError

    def close(self) -> None:
        """释放底层资源（如有）。默认无操作。"""


class SqliteSessionStore(SessionStore):
    """SQLite 后端（默认）：与账本同库 sessions 表，进程重启不丢失。

    复用 ledger.Storage 的连接与锁，不单独持有数据库资源。
    """

    def __init__(self, storage):
        self._storage = storage

    def save(self, session_id, soul_hash, refresh_hash, created_at, expires_at):
        self._storage.execute(
            "INSERT INTO sessions "
            "(session_id, soul_hash, refresh_hash, created_at, expires_at, revoked) "
            "VALUES (?, ?, ?, ?, ?, 0)",
            (session_id, soul_hash, refresh_hash, created_at, expires_at),
            shard_key=soul_hash,
        )

    def get_by_refresh(self, refresh_hash):
        rows = self._storage.query(
            "SELECT session_id, soul_hash, expires_at, revoked FROM sessions "
            "WHERE refresh_hash=?",
            (refresh_hash,),
            shard_key=None,
        )
        return rows[0] if rows else None

    def revoke(self, soul_hash, session_id=None):
        if session_id:
            self._storage.execute(
                "UPDATE sessions SET revoked=1 WHERE soul_hash=? AND session_id=?",
                (soul_hash, session_id),
                shard_key=soul_hash,
            )
        else:
            self._storage.execute(
                "UPDATE sessions SET revoked=1 WHERE soul_hash=?",
                (soul_hash,),
                shard_key=soul_hash,
            )


class MemorySessionStore(SessionStore):
    """内存后端（本地测试 / 无状态演示）：进程内 dict + 锁，重启即失。"""

    def __init__(self):
        self._sessions = {}  # refresh_hash -> (session_id, soul_hash, expires_at, revoked)
        self._lock = threading.Lock()

    def save(self, session_id, soul_hash, refresh_hash, created_at, expires_at):
        with self._lock:
            self._sessions[refresh_hash] = (session_id, soul_hash, expires_at, 0)

    def get_by_refresh(self, refresh_hash):
        with self._lock:
            return self._sessions.get(refresh_hash)

    def revoke(self, soul_hash, session_id=None):
        with self._lock:
            for rh, (sid, sh, exp, revoked) in list(self._sessions.items()):
                if sh == soul_hash and (session_id is None or sid == session_id):
                    self._sessions[rh] = (sid, sh, exp, 1)


class RedisSessionStore(SessionStore):
    """Redis 后端（生产，跨实例共享状态）。

    需 redis-py：pip install redis。每个 refresh 哈希为键存 JSON 负载并设
    TTL（过期自动清理）；另维护 soul -> {refresh_hash} 索引集合，吊销 O(会话数/soul)。
    """

    def __init__(self, client, key_prefix: str = "soul:session"):
        if client is None:
            raise ValueError("RedisSessionStore requires a redis client")
        self._redis = client
        self._prefix = key_prefix

    def _key(self, refresh_hash: str) -> str:
        return f"{self._prefix}:sess:{refresh_hash}"

    def _soul_index(self, soul_hash: str) -> str:
        return f"{self._prefix}:soul:{soul_hash}"

    def save(self, session_id, soul_hash, refresh_hash, created_at, expires_at):
        ttl = max(1, int(expires_at - created_at))
        payload = json.dumps([session_id, soul_hash, expires_at, 0], ensure_ascii=False)
        self._redis.setex(self._key(refresh_hash), ttl, payload)
        self._redis.sadd(self._soul_index(soul_hash), refresh_hash)  # 吊销索引

    def get_by_refresh(self, refresh_hash):
        raw = self._redis.get(self._key(refresh_hash))
        if not raw:
            return None
        session_id, soul_hash, expires_at, revoked = json.loads(raw)
        return (session_id, soul_hash, expires_at, revoked)

    def revoke(self, soul_hash, session_id=None):
        for rh in self._redis.smembers(self._soul_index(soul_hash)) or set():
            raw = self._redis.get(self._key(rh))
            if not raw:
                continue
            data = json.loads(raw)
            if session_id is None or data[0] == session_id:
                data[3] = 1
                self._redis.set(self._key(rh), json.dumps(data, ensure_ascii=False))


# ============================================================
# SessionManager：签发 / 验签 / 轮换 / 吊销
# ============================================================


class SessionManager:
    """有状态会话管理。签名密钥经 KMS 抽象托管（可插拔 HSM）。"""

    def __init__(
        self,
        storage=None,
        kms_provider=None,
        session_store: SessionStore = None,
        access_ttl: int = 900,
        refresh_ttl: int = 604800,
        key_rotation=None,
    ):
        # 向后兼容：未显式传 session_store 时，包装传入的 storage 为 SQLite 后端
        if session_store is None:
            if storage is None:
                raise ValueError("must provide either storage or session_store")
            session_store = SqliteSessionStore(storage)
        self._store = session_store
        # 兼容属性：SQLite 后端下指向账本连接；其余后端为 None。
        # 供既有审计/管理代码读取（新代码应使用公开方法 get_session_id）。
        self._storage = getattr(session_store, "_storage", None)
        self._kms = kms_provider
        self.access_ttl = access_ttl
        self.refresh_ttl = refresh_ttl
        # 可选：服务端签名密钥轮换（key_rotation.KeyRotationManager）。
        #   签发走活跃密钥并内嵌 key_id；验证按 key_id 取密钥——
        #   retired 仍可验旧 token，revoked 即刻令其全部失效。
        #   None 时回落 KMS 静态密钥（原行为，向后兼容）。
        self._key_rotation = key_rotation

    def get_session_id(self, refresh_hash: str):
        """按 refresh 哈希查 session_id（三种后端通吃，审计/管理接口用）。"""
        entry = self._store.get_by_refresh(refresh_hash)
        return entry[0] if entry else None

    def _signing_key(self) -> bytes:
        """取当前签名密钥：轮换管理器激活时走活跃密钥（惰性检查轮换周期）。"""
        if self._key_rotation is not None:
            self._key_rotation.rotate_if_needed()
            return self._key_rotation.get_active_key().key_bytes
        return self._kms.get_or_create_key("session_signing_key")

    def _sign(self, payload: bytes) -> bytes:
        return hmac.new(self._signing_key(), payload, hashlib.sha256).digest()

    def _verify_sig(self, payload: bytes, sig: bytes, key_id: str = "") -> bool:
        """按 token 内嵌 key_id 选择验证密钥。

        - 带 key_id：从轮换管理器取（retired 可验，revoked 拒绝）
        - 无 key_id（旧版 token）：用当前签名密钥验证
        """
        if key_id and self._key_rotation is not None:
            rk = self._key_rotation.get_key_for_verification(key_id)
            if rk is None:
                return False  # 密钥已吊销或不存在：该密钥签发的 token 全部失效
            key_bytes = rk.key_bytes
        else:
            key_bytes = self._signing_key()
        return hmac.compare_digest(
            hmac.new(key_bytes, payload, hashlib.sha256).digest(), sig
        )

    def issue(self, soul_hash: str, pubkey_fingerprint: str = ""):
        """签发 access + refresh。返回 (access_token, refresh_token)。

        参数：
          pubkey_fingerprint  设备公钥指纹（SHA-256(公钥) 的前 32 hex）。绑定到
                              access token：若此设备凭证被吊销（/credentials/revoke），
                              所有关联 access token 立即失效。
                              为空时按"无设备绑定"旧模式签发（仅 soul 维度）。
        """
        now = time.time()
        exp = now + self.access_ttl
        payload_dict = {"soul": soul_hash, "exp": exp}
        if pubkey_fingerprint:
            payload_dict["pkfp"] = pubkey_fingerprint
        if self._key_rotation is not None:
            # 内嵌签名密钥 ID：验证端据此选择验证密钥（支持轮换后验旧 token）
            payload_dict["kid"] = self._key_rotation.get_active_key().key_id
        payload = json.dumps(payload_dict, sort_keys=True).encode("utf-8")
        access_token = (
            base64.urlsafe_b64encode(payload).decode("ascii")
            + "."
            + base64.urlsafe_b64encode(self._sign(payload)).decode("ascii")
        )
        refresh_token = secrets.token_urlsafe(32)
        session_id = uuid.uuid4().hex
        refresh_hash = hashlib.sha256(refresh_token.encode("utf-8")).hexdigest()
        self._store.save(session_id, soul_hash, refresh_hash, now, now + self.refresh_ttl)
        logger.info(
            "session issued soul_hash=%s session_id=%s access_ttl=%ds pkfp_bound=%s",
            soul_hash,
            session_id,
            self.access_ttl,
            "yes" if pubkey_fingerprint else "no",
        )
        return access_token, refresh_token

    def verify(self, access_token: str, credential_vault=None):
        """验 access token，返回 soul_hash 或 None。支持标准 Bearer 前缀。

        参数：
          credential_vault  若提供，则额外校验 token 中绑定的 pubkey_fingerprint
                            对应凭证未被吊销（/credentials/revoke 后即时失效）。
        """
        if not access_token:
            return None
        # 剥离标准Bearer头
        if access_token.startswith("Bearer "):
            access_token = access_token[7:]
        try:
            payload_b64, sig_b64 = access_token.split(".")
            payload = base64.urlsafe_b64decode(payload_b64.encode("ascii"))
            sig = base64.urlsafe_b64decode(sig_b64.encode("ascii"))
        except Exception:
            return None
        # 先解析 payload 再验签：签名密钥 ID（kid）在 payload 内
        try:
            data = json.loads(payload.decode("utf-8"))
        except Exception:
            return None
        if not self._verify_sig(payload, sig, key_id=data.get("kid", "")):
            return None
        if data.get("exp", 0) < time.time():
            return None
        # 设备绑定校验：若 token 包含 pkfp，则对应凭证必须仍有效
        pkfp = data.get("pkfp")
        if pkfp and credential_vault is not None:
            soul = data.get("soul")
            # 查找 pkfp 对应凭证是否仍激活
            creds = credential_vault.get_credentials(soul)
            valid_pkfp = any(
                hashlib.sha256(c["public_key"]).hexdigest()[: len(pkfp)] == pkfp
                and not c["revoked"]
                for c in creds
            )
            if not valid_pkfp:
                return None  # 凭证已吊销，token 立即失效
        return data.get("soul")

    def refresh(self, refresh_token: str, pubkey_fingerprint: str = ""):
        """轮换 refresh token，返回新的 (access_token, refresh_token) 或 None。

        关键修复：先 issue 新 session，再 revoke 旧 session（任一失败不留中间态）。
        """
        refresh_hash = hashlib.sha256(refresh_token.encode("utf-8")).hexdigest()
        entry = self._store.get_by_refresh(refresh_hash)
        if not entry:
            return None
        session_id, soul_hash, expires_at, revoked = entry
        if revoked or expires_at < time.time():
            return None
        try:
            # 先签发新 session（成功才继续）
            new_pair = self.issue(soul_hash, pubkey_fingerprint=pubkey_fingerprint)
            # 新 session 落库后再吊销旧 session（顺序保证失败时旧 session 仍可用）
            self._store.revoke(soul_hash, session_id)
            return new_pair
        except Exception:
            return None

    def revoke(self, soul_hash: str, session_id: str = None) -> bool:
        """吊销会话。session_id 为 None 时吊销该 soul 全部会话。"""
        self._store.revoke(soul_hash, session_id)
        return True

    def close(self) -> None:
        """释放会话存储底层资源（如有）。"""
        self._store.close()


__all__ = [
    "SessionManager",
    "SessionStore",
    "SqliteSessionStore",
    "MemorySessionStore",
    "RedisSessionStore",
]
