"""第 1 层：凭证层（Credential Vault）。

一个 soul 绑定多设备凭证（Ed25519 模拟 Passkey）。
服务端只存凭证公钥，私钥永不出设备安全区。
"""

import base64
import time
import uuid

from . import keys


class CredentialVault:
    """多设备凭证管理：绑定 / 吊销 / 验签。"""

    def __init__(self, storage):
        self._storage = storage

    def bind_credential(self, soul_hash: str, public_key: bytes, device_label: str = ""):
        """绑定一个设备凭证到 soul。public_key 为 32 字节原始公钥。返回 credential_id。"""
        credential_id = uuid.uuid4().hex
        self._storage.execute(
            "INSERT INTO credentials "
            "(soul_hash, credential_id, public_key, device_label, created_at, revoked) "
            "VALUES (?, ?, ?, ?, ?, 0)",
            (
                soul_hash,
                credential_id,
                base64.b64encode(public_key).decode("ascii"),
                device_label,
                time.time(),
            ),
        )
        return credential_id

    def revoke_credential(self, soul_hash: str, credential_id: str) -> bool:
        """吊销凭证（丢设备后一键踢下线）。"""
        self._storage.execute(
            "UPDATE credentials SET revoked=1 WHERE soul_hash=? AND credential_id=?",
            (soul_hash, credential_id),
        )
        return True

    def get_credentials(self, soul_hash: str):
        """返回该 soul 名下所有凭证（含已吊销）。"""
        rows = self._storage.query(
            "SELECT credential_id, public_key, device_label, revoked "
            "FROM credentials WHERE soul_hash=?",
            (soul_hash,),
        )
        return [
            {
                "credential_id": r[0],
                "public_key": base64.b64decode(r[1]),
                "device_label": r[2],
                "revoked": bool(r[3]),
            }
            for r in rows
        ]

    def verify_credential(
        self, soul_hash: str, credential_id: str, message: bytes, signature: bytes
    ) -> bool:
        """用指定凭证公钥验签。message/signature 为 bytes。"""
        rows = self._storage.query(
            "SELECT public_key, revoked FROM credentials "
            "WHERE soul_hash=? AND credential_id=?",
            (soul_hash, credential_id),
        )
        if not rows or rows[0][1]:
            return False
        pubkey = base64.b64decode(rows[0][0])
        return keys.verify_signature(pubkey, message, signature)
