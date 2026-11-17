"""灵魂漫游协议（Soul Roaming Protocol）——第四级：跨世界身份互认。

核心问题：用户在世界A积累了身份、记忆、声誉，如何带到世界B？
传统方案：世界B重新注册，从零开始——割裂体验。
本协议：源世界签发"灵魂漫游证书"，目标世界验证后互认身份，记忆/声誉可选择性迁移。

证书结构：
{
  "soul_hash": "源世界的灵魂哈希",
  "source_world_id": "源世界ID",
  "target_world_id": "目标世界ID",
  "issued_at": 签发时间戳,
  "expires_at": 过期时间戳,
  "identity_proof": {
     "pubkey_b64": 公钥,
     "soul_hash_in_source": 源世界灵魂哈希,
     "reputation_score": 声誉分数（可选）,
     "account_age_days": 账号龄（可选）
  },
  "memory_manifest": [  // 记忆迁移清单（可选，用户选择性授权）
     {"memory_id": "...", "category": "...", "hash": "sha256内容哈希"}
  ],
  "signature": "源世界私钥对以上内容的签名"
}

目标世界验证：
1. 证书签名有效（源世界公钥验签）
2. 证书未过期
3. soul_hash 与公钥派生一致
4. 用户持有对应私钥（challenge-response 二次验证）

验证通过后，目标世界为该灵魂创建本地映射，身份/声誉互认。
记忆迁移：用户选择性授权后，源世界通过加密通道传输记忆内容，目标世界验证哈希后入库。

本模块为协议骨架，具体的跨世界通信通道和记忆加密传输在后续实现。
"""

import base64
import hashlib
import json
import time
import uuid
import logging
from typing import Dict, List, Optional, Set

from .keys import verify_signature, sign_with_device, derive_soul_hash_from_pubkey

logger = logging.getLogger(__name__)


class SoulRoamingCertificate:
    """灵魂漫游证书：源世界签发，目标世界验证。"""

    def __init__(
        self,
        cert_id: str,
        soul_hash: str,
        source_world_id: str,
        target_world_id: str,
        issued_at: float,
        expires_at: float,
        identity_proof: Dict,
        memory_manifest: Optional[List[Dict]] = None,
        signature_b64: Optional[str] = None,
    ):
        self.cert_id = cert_id
        self.soul_hash = soul_hash
        self.source_world_id = source_world_id
        self.target_world_id = target_world_id
        self.issued_at = issued_at
        self.expires_at = expires_at
        self.identity_proof = identity_proof
        self.memory_manifest = memory_manifest or []
        self.signature_b64 = signature_b64

    def canonical_payload(self) -> bytes:
        """生成签名字节流（排除 signature 字段，规范 JSON）。"""
        payload = {
            "cert_id": self.cert_id,
            "soul_hash": self.soul_hash,
            "source_world_id": self.source_world_id,
            "target_world_id": self.target_world_id,
            "issued_at": self.issued_at,
            "expires_at": self.expires_at,
            "identity_proof": self.identity_proof,
            "memory_manifest": self.memory_manifest,
        }
        return json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")

    def sign(self, source_world_private_key: bytes) -> str:
        """源世界用私钥签名证书。返回 base64 签名。"""
        sig = sign_with_device(source_world_private_key, self.canonical_payload())
        self.signature_b64 = base64.b64encode(sig).decode("ascii")
        return self.signature_b64

    def verify_signature(self, source_world_public_key: bytes) -> bool:
        """目标世界验证证书签名。"""
        if not self.signature_b64:
            return False
        try:
            sig = base64.b64decode(self.signature_b64)
        except Exception:
            return False
        return verify_signature(source_world_public_key, self.canonical_payload(), sig)

    def is_expired(self, now: Optional[float] = None) -> bool:
        return (now or time.time()) > self.expires_at

    def to_dict(self) -> Dict:
        return {
            "cert_id": self.cert_id,
            "soul_hash": self.soul_hash,
            "source_world_id": self.source_world_id,
            "target_world_id": self.target_world_id,
            "issued_at": self.issued_at,
            "expires_at": self.expires_at,
            "identity_proof": self.identity_proof,
            "memory_manifest": self.memory_manifest,
            "signature_b64": self.signature_b64,
        }

    @classmethod
    def from_dict(cls, d: Dict) -> "SoulRoamingCertificate":
        return cls(
            cert_id=d["cert_id"],
            soul_hash=d["soul_hash"],
            source_world_id=d["source_world_id"],
            target_world_id=d["target_world_id"],
            issued_at=d["issued_at"],
            expires_at=d["expires_at"],
            identity_proof=d.get("identity_proof", {}),
            memory_manifest=d.get("memory_manifest"),
            signature_b64=d.get("signature_b64"),
        )


class SoulRoamingProtocol:
    """灵魂漫游协议管理器：证书签发、验证、跨世界身份映射。

    每个 Second-Reality 实例维护一个：
    - 本世界的世界ID和签名密钥对
    - 已知世界的公钥注册表（world_id -> public_key）
    - 灵魂漫游映射表（source_soul_hash -> local_soul_hash）
    """

    DEFAULT_CERT_TTL_SECONDS = 24 * 3600  # 证书默认24小时有效

    def __init__(
        self,
        world_id: str,
        world_private_key: bytes,
        world_public_key: bytes,
        storage=None,
    ):
        self.world_id = world_id
        self._world_private_key = world_private_key
        self._world_public_key = world_public_key
        self._storage = storage
        # 已知世界公钥注册表
        self._world_registry: Dict[str, bytes] = {}
        # 灵魂漫游映射：(source_world_id, source_soul_hash) -> local_soul_hash
        self._roaming_map: Dict[tuple, str] = {}
        self._init_storage()

    def _init_storage(self) -> None:
        if not self._storage:
            return
        self._storage.execute("""
            CREATE TABLE IF NOT EXISTS roaming_world_registry (
                world_id TEXT PRIMARY KEY,
                public_key_b64 TEXT NOT NULL,
                registered_at REAL NOT NULL
            )
        """)
        self._storage.execute("""
            CREATE TABLE IF NOT EXISTS roaming_soul_map (
                source_world_id TEXT NOT NULL,
                source_soul_hash TEXT NOT NULL,
                local_soul_hash TEXT NOT NULL,
                mapped_at REAL NOT NULL,
                cert_id TEXT,
                PRIMARY KEY (source_world_id, source_soul_hash)
            )
        """)

    # ── 世界注册表 ────────────────────────────────────────────
    def register_world(self, world_id: str, public_key: bytes) -> bool:
        """注册已知世界的公钥（用于验证该世界签发的漫游证书）。"""
        self._world_registry[world_id] = public_key
        if self._storage:
            self._storage.execute(
                "INSERT OR REPLACE INTO roaming_world_registry (world_id, public_key_b64, registered_at) "
                "VALUES (?, ?, ?)",
                (world_id, base64.b64encode(public_key).decode("ascii"), time.time()),
            )
        logger.info("roaming world registered world_id=%s", world_id)
        return True

    def get_world_public_key(self, world_id: str) -> Optional[bytes]:
        if world_id in self._world_registry:
            return self._world_registry[world_id]
        # 从存储加载
        if self._storage:
            rows = self._storage.query(
                "SELECT public_key_b64 FROM roaming_world_registry WHERE world_id=?",
                (world_id,),
            )
            if rows:
                pk = base64.b64decode(rows[0][0])
                self._world_registry[world_id] = pk
                return pk
        return None

    # ── 证书签发（源世界） ────────────────────────────────────
    def issue_roaming_certificate(
        self,
        soul_hash: str,
        target_world_id: str,
        identity_proof: Dict,
        memory_manifest: Optional[List[Dict]] = None,
        ttl_seconds: Optional[int] = None,
    ) -> SoulRoamingCertificate:
        """源世界为灵魂签发漫游证书。

        identity_proof 应包含：pubkey_b64, reputation_score, account_age_days 等。
        memory_manifest 是用户选择性授权的记忆迁移清单。
        """
        now = time.time()
        cert = SoulRoamingCertificate(
            cert_id=uuid.uuid4().hex,
            soul_hash=soul_hash,
            source_world_id=self.world_id,
            target_world_id=target_world_id,
            issued_at=now,
            expires_at=now + (ttl_seconds or self.DEFAULT_CERT_TTL_SECONDS),
            identity_proof=identity_proof,
            memory_manifest=memory_manifest,
        )
        cert.sign(self._world_private_key)
        logger.info(
            "roaming cert issued cert_id=%s soul=%s target=%s memory_items=%d",
            cert.cert_id, soul_hash, target_world_id, len(memory_manifest or []),
        )
        return cert

    # ── 证书验证（目标世界） ──────────────────────────────────
    def verify_roaming_certificate(
        self,
        cert: SoulRoamingCertificate,
        user_challenge_signature: Optional[bytes] = None,
        challenge_nonce: Optional[bytes] = None,
    ) -> tuple[bool, str]:
        """目标世界验证漫游证书。返回 (is_valid, reason)。

        验证步骤：
        1. 证书目标世界是本世界
        2. 证书未过期
        3. 源世界已注册，公钥可获取
        4. 证书签名有效（源世界公钥验签）
        5. soul_hash 与 identity_proof 中的公钥派生一致
        6. （可选）用户持有对应私钥（challenge-response 二次验证）
        """
        # 1. 目标世界
        if cert.target_world_id != self.world_id:
            return False, f"cert target_world_id={cert.target_world_id} != local={self.world_id}"
        # 2. 未过期
        if cert.is_expired():
            return False, "cert expired"
        # 3. 源世界已注册
        source_pk = self.get_world_public_key(cert.source_world_id)
        if not source_pk:
            return False, f"source world {cert.source_world_id} not registered"
        # 4. 签名有效
        if not cert.verify_signature(source_pk):
            return False, "cert signature invalid"
        # 5. soul_hash 与公钥一致
        pubkey_b64 = cert.identity_proof.get("pubkey_b64")
        if pubkey_b64:
            try:
                pubkey = base64.b64decode(pubkey_b64)
                derived_hash = derive_soul_hash_from_pubkey(pubkey)
                if derived_hash != cert.soul_hash:
                    return False, f"soul_hash mismatch: derived={derived_hash} != cert={cert.soul_hash}"
            except Exception as e:
                return False, f"pubkey decode failed: {e}"
        # 6. （可选）用户持有私钥
        if user_challenge_signature and challenge_nonce and pubkey_b64:
            try:
                pubkey = base64.b64decode(pubkey_b64)
                if not verify_signature(pubkey, challenge_nonce, user_challenge_signature):
                    return False, "user challenge-response failed"
            except Exception as e:
                return False, f"challenge verification failed: {e}"
        return True, "ok"

    # ── 灵魂映射（目标世界） ──────────────────────────────────
    def map_roaming_soul(
        self,
        cert: SoulRoamingCertificate,
        local_soul_hash: str,
    ) -> bool:
        """验证通过后，目标世界为漫游灵魂创建本地映射。"""
        key = (cert.source_world_id, cert.soul_hash)
        self._roaming_map[key] = local_soul_hash
        if self._storage:
            self._storage.execute(
                "INSERT OR REPLACE INTO roaming_soul_map "
                "(source_world_id, source_soul_hash, local_soul_hash, mapped_at, cert_id) "
                "VALUES (?, ?, ?, ?, ?)",
                (cert.source_world_id, cert.soul_hash, local_soul_hash, time.time(), cert.cert_id),
            )
        logger.info(
            "roaming soul mapped source=%s/%s -> local=%s",
            cert.source_world_id, cert.soul_hash, local_soul_hash,
        )
        return True

    def get_local_soul_hash(self, source_world_id: str, source_soul_hash: str) -> Optional[str]:
        """查询漫游灵魂的本地映射。"""
        key = (source_world_id, source_soul_hash)
        if key in self._roaming_map:
            return self._roaming_map[key]
        if self._storage:
            rows = self._storage.query(
                "SELECT local_soul_hash FROM roaming_soul_map "
                "WHERE source_world_id=? AND source_soul_hash=?",
                (source_world_id, source_soul_hash),
            )
            if rows:
                local = rows[0][0]
                self._roaming_map[key] = local
                return local
        return None

    # ── 记忆迁移（框架） ──────────────────────────────────────
    def build_memory_manifest(
        self,
        memory_items: List[Dict],
        user_selected_ids: Optional[Set[str]] = None,
    ) -> List[Dict]:
        """构建记忆迁移清单（用户选择性授权）。

        每个 memory_item 应包含：memory_id, category, content（用于计算哈希）。
        user_selected_ids 为用户选择迁移的记忆ID集合，None 表示全部。
        """
        manifest = []
        for item in memory_items:
            mid = item.get("memory_id")
            if not mid:
                continue
            if user_selected_ids and mid not in user_selected_ids:
                continue
            content = item.get("content", "")
            content_hash = hashlib.sha256(
                json.dumps(content, sort_keys=True, ensure_ascii=False).encode("utf-8")
            ).hexdigest()
            manifest.append({
                "memory_id": mid,
                "category": item.get("category", "general"),
                "hash": content_hash,
                "size_bytes": len(json.dumps(content).encode("utf-8")),
            })
        return manifest

    def verify_memory_integrity(self, memory_item: Dict, manifest_entry: Dict) -> bool:
        """目标世界验证迁移的记忆内容与清单哈希一致。"""
        content = memory_item.get("content", "")
        content_hash = hashlib.sha256(
            json.dumps(content, sort_keys=True, ensure_ascii=False).encode("utf-8")
        ).hexdigest()
        return content_hash == manifest_entry.get("hash")
