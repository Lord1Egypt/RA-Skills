"""签名、密钥与规范化串。

规范化串必须与平台侧（Java CanonicalBuilder）逐字节一致：
    METHOD \\n PATH \\n SORTED_QUERY \\n TIMESTAMP \\n NONCE \\n BODY_SHA256 \\n AGENT_CODE
激活载荷：
    ACTIVATE \\n CODE_DIGEST \\n TIMESTAMP \\n NONCE \\n PUBKEY_FP \\n HW_FP_DIGEST
"""

import base64
import hashlib
import json
import os
import secrets
import time
from typing import Dict, Optional

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

# 国密 SM2 为可选依赖（gmssl）；未安装时仅支持 ED25519
try:  # pragma: no cover
    from gmssl import sm2 as _gmssl_sm2  # type: ignore
    _HAS_GMSSL = True
except Exception:  # pragma: no cover
    _HAS_GMSSL = False

SUPPORTED_ALGOS = ("ED25519", "SM2")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_hex_str(text: str) -> str:
    return sha256_hex(text.encode("utf-8"))


def new_nonce() -> str:
    return base64.urlsafe_b64encode(os.urandom(16)).decode().rstrip("=")


def now_ms() -> int:
    return int(time.time() * 1000)


def normalize_code(code: str) -> str:
    """激活码规范化：去分隔符、转大写（与后端一致）。"""
    return (code or "").replace("-", "").replace(" ", "").upper()


def credential_canonical(credential: dict) -> bytes:
    """身份凭证的规范化字节串（第三方独立验签的参考实现）。

    规则：去掉 sig 字段 → 键按字典序排序 → JSON 紧凑序列化（无空格）
          → **UTF-8 且不转义非 ASCII**（与 Java Jackson 默认行为一致）。
    注意：Python json.dumps 默认 ensure_ascii=True 会把中文转义为 \\uXXXX，
          导致与平台签名不一致 —— 必须显式设置 ensure_ascii=False。
    """
    payload = {k: v for k, v in credential.items() if k != "sig"}
    return json.dumps(dict(sorted(payload.items())), separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def build_canonical(method: str, path: str, query: Optional[Dict[str, str]],
                    timestamp: int, nonce: str, body: bytes, agent_code: str) -> str:
    q = ""
    if query:
        parts = []
        for k in sorted(query.keys()):
            v = query[k]
            if v is None:
                continue
            parts.append(f"{k}={v}")
        q = "&".join(parts)
    body_hash = sha256_hex(body or b"")
    return "\n".join([method.upper(), path, q, str(timestamp), nonce, body_hash, agent_code])


def build_activation_canonical(code_digest: str, timestamp: int, nonce: str,
                               pubkey_fp: str, hw_fp_digest: str) -> str:
    return "\n".join(["ACTIVATE", code_digest, str(timestamp), nonce,
                      pubkey_fp or "", hw_fp_digest or ""])


def build_rotate_canonical(agent_code: str, timestamp: int, nonce: str, new_pubkey_fp: str) -> str:
    return "\n".join(["ROTATE", agent_code, str(timestamp), nonce, new_pubkey_fp])


class KeyPair:
    """设备密钥对。私钥仅存在于本地，绝不上传。"""

    def __init__(self, algo: str, private_key, public_key):
        self.algo = algo
        self._private = private_key
        self._public = public_key

    # ---------- 生成 / 导入 ----------

    @staticmethod
    def generate(algo: str = "ED25519") -> "KeyPair":
        algo = algo.upper()
        if algo == "ED25519":
            priv = ed25519.Ed25519PrivateKey.generate()
            return KeyPair(algo, priv, priv.public_key())
        if algo == "SM2":
            if not _HAS_GMSSL:
                raise RuntimeError("SM2 需要安装 gmssl：pip install gmssl")
            private_hex = secrets.token_hex(32)
            sm2 = _gmssl_sm2.CryptSM2(private_key=private_hex, public_key="")
            public_hex = sm2._kg(int(private_hex, 16), sm2.ecc_table["g"])
            return KeyPair(algo, (private_hex, sm2), public_hex)
        raise ValueError(f"不支持的算法: {algo}")

    @classmethod
    def from_pem(cls, algo: str, private_pem: bytes, public_pem: bytes) -> "KeyPair":
        algo = algo.upper()
        if algo == "ED25519":
            priv = serialization.load_pem_private_key(private_pem, password=None)
            pub = serialization.load_pem_public_key(public_pem)
            return cls(algo, priv, pub)
        if algo == "SM2":
            if not _HAS_GMSSL:
                raise RuntimeError("SM2 需要安装 gmssl")
            private_hex = private_pem.decode().strip()
            public_hex = public_pem.decode().strip()
            sm2 = _gmssl_sm2.CryptSM2(private_key=private_hex, public_key=public_hex)
            return cls(algo, (private_hex, sm2), public_hex)
        raise ValueError(f"不支持的算法: {algo}")

    # ---------- 导出 ----------

    def private_bytes(self) -> bytes:
        if self.algo == "ED25519":
            return self._private.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption())
        return self._private[0].encode()

    def public_bytes(self) -> bytes:
        if self.algo == "ED25519":
            return self._public.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo)
        return self._public.encode()

    def public_x509_base64(self) -> str:
        """平台要求的上报格式：X.509 SubjectPublicKeyInfo 的 Base64。

        SM2 场景下平台侧使用 BouncyCastle 解析 EC SPKI；此处按 gmssl 的
        uncompressed point（04||X||Y）以 DER SPKI 结构封装（见 _sm2_spki_der）。
        """
        if self.algo == "ED25519":
            der = self._public.public_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PublicFormat.SubjectPublicKeyInfo)
        else:
            der = _sm2_spki_der(self._public)
        return base64.b64encode(der).decode()

    def fingerprint(self) -> str:
        """公钥指纹 = SHA-256(X.509 SPKI DER) 小写十六进制（与 Java getEncoded() 一致）。"""
        if self.algo == "ED25519":
            der = self._public.public_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PublicFormat.SubjectPublicKeyInfo)
        else:
            der = _sm2_spki_der(self._public)
        return sha256_hex(der)

    # ---------- 签名 ----------

    def sign(self, message: bytes) -> bytes:
        if self.algo == "ED25519":
            return self._private.sign(message)
        _, sm2 = self._private
        return bytes.fromhex(sm2.sign(message.hex()))

    def sign_base64(self, message: bytes) -> str:
        return base64.b64encode(self.sign(message)).decode()

    def verify(self, message: bytes, signature: bytes) -> bool:
        if self.algo == "ED25519":
            try:
                self._public.verify(signature, message)
                return True
            except Exception:
                return False
        return False  # SM2 验签由平台侧完成，客户端不自验


def _sm2_spki_der(public_hex: str) -> bytes:
    """将 SM2 未压缩点封装为 X.509 SubjectPublicKeyInfo DER（OID 1.2.156.10197.1.301）。"""
    point = bytes.fromhex(public_hex if public_hex.startswith("04") else "04" + public_hex)
    # EcpkParameters: 显式曲线参数（国密推荐曲线）；此处使用 OID 形式的 sm2p256v1
    curve_oid = bytes.fromhex("06082A811CCF5501822D")
    alg_id = bytes.fromhex("3013") + bytes.fromhex("06072A8648CE3D0201") + curve_oid
    bit_string = b"\x03" + _der_len(len(point) + 1) + b"\x00" + point
    body = alg_id + bit_string
    return b"\x30" + _der_len(len(body)) + body


def _der_len(n: int) -> bytes:
    if n < 0x80:
        return bytes([n])
    raw = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return bytes([0x80 | len(raw)]) + raw
