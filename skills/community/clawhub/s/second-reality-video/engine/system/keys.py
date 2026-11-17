# system/keys.py - 密钥管理（服务端签名密钥 + 用户身份密钥链路）
# ============================================================
# 职责分两层：
#   A. 服务端签名密钥（原有）：为鉴权层提供 HMAC 签名密钥的生成/持久化/加载。
#      - 无状态签名 token 在服务重启后仍可验证（密钥不随进程消失）
#      - 签名不可伪造（密钥仅服务端持有）
#   B. 用户身份密钥链路（定稿方案·Passkey 单设备）：
#      - 真实身份凭证 = Ed25519 私钥，仅驻留持有者单台设备安全区（内存态，永不上传）
#      - soul_hash = SHA-256(公钥字节)，公钥可公开围观，哈希只是 ID 不是秘密
#      - 登录 = 挑战-响应：服务端下发一次性 nonce，设备签名，服务端仅验签
#      - 服务端不存储、不接触任何私钥材料；私钥丢失 = 身份冻结（永久）
#
# 依赖方向：system/keys.py 无内部依赖（仅标准库 + cryptography），可被
#   api.py / ledger.py / audit_engine.py 引用。不反向依赖任何模块。
# ============================================================

import base64
import hashlib
import json
import os
import secrets
from typing import Dict, Optional

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

# HMAC-SHA256 签名密钥长度（32 字节 / 256 bit）
_KEY_BYTES = 32

# Ed25519 私钥 / 公钥原始字节长度
_ED25519_RAW_BYTES = 32


# ============================================================
# A. 服务端签名密钥（原有，勿动语义）
# ============================================================

def generate_key() -> bytes:
    """生成新的随机签名密钥。"""
    return secrets.token_bytes(_KEY_BYTES)


def load_or_create_key(key_path: str) -> bytes:
    """
    加载既有签名密钥；不存在则生成并持久化到 key_path。
    落盘后尝试收紧权限为 0600（POSIX；Windows 上为 no-op，无害）。
    """
    if key_path and os.path.exists(key_path):
        with open(key_path, "rb") as f:
            key = f.read()
        if key:
            return key
    key = generate_key()
    if key_path:
        os.makedirs(os.path.dirname(key_path), exist_ok=True)
        # 先写临时文件再原子替换，避免并发/中断留下半截密钥
        tmp_path = key_path + ".tmp"
        with open(tmp_path, "wb") as f:
            f.write(key)
        os.replace(tmp_path, key_path)
        try:
            os.chmod(key_path, 0o600)
        except OSError:
            pass  # Windows 不支持 POSIX 权限位，忽略
    return key


# ============================================================
# B. 用户身份密钥链路（定稿方案：Passkey 单设备 + 公钥指纹）
# ============================================================

def generate_user_keypair() -> Dict[str, bytes]:
    """
    生成用户身份密钥对。返回 {"secret": 私钥32B, "pubkey": 公钥32B}。
    私钥必须仅驻留设备安全区（内存态），任何路径均不得落盘/上传。
    """
    private_key = Ed25519PrivateKey.generate()
    secret = private_key.private_bytes(
        serialization.Encoding.Raw,
        serialization.PrivateFormat.Raw,
        serialization.NoEncryption(),
    )
    pubkey = private_key.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw
    )
    return {"secret": secret, "pubkey": pubkey}


def public_from_private(secret_raw: bytes) -> bytes:
    """由私钥派生对应公钥（设备端用）。"""
    return Ed25519PrivateKey.from_private_bytes(secret_raw).public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw
    )


def derive_soul_hash_from_pubkey(pubkey_raw: bytes) -> str:
    """
    单一权威身份派生规则：soul_hash = SHA-256(公钥字节)。
    公钥公开、哈希只是 ID；盗窃哈希无法冒充，签名需要私钥。
    """
    return hashlib.sha256(pubkey_raw).hexdigest()


def sign_with_device(secret_raw: bytes, message: bytes) -> bytes:
    """设备端签名：私钥批准签名动作（用户经生物识别在场验证后触发）。"""
    return Ed25519PrivateKey.from_private_bytes(secret_raw).sign(message)


def verify_signature(pubkey_raw: bytes, message: bytes, signature: bytes) -> bool:
    """服务端验签：只接受公钥与签名，永远不接触私钥。"""
    try:
        Ed25519PublicKey.from_public_bytes(pubkey_raw).verify(signature, message)
        return True
    except (InvalidSignature, ValueError):
        return False


def _b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def _b64_decode(value: str) -> bytes:
    return base64.b64decode(value)


def build_genesis_proof(secret_raw: bytes, declaration: Dict) -> Optional[Dict]:
    """
    构建创世注册证明（服务端可验证，且不接触私钥）：
      {"pubkey": b64(公钥), "declaration": 创世声明, "sig": b64(签名)}
    签名对象 = 声明的规范 JSON（sort_keys + ensure_ascii=False）。
    服务端验：1) 签名有效（公钥验声明） 2) soul_hash == SHA-256(公钥)。
    """
    if not isinstance(declaration, dict) or not declaration:
        return None
    pubkey = public_from_private(secret_raw)
    canonical = __import__("json").dumps(
        declaration, sort_keys=True, ensure_ascii=False
    )
    sig = sign_with_device(secret_raw, canonical.encode("utf-8"))
    return {
        "pubkey": _b64(pubkey),
        "declaration": declaration,
        "sig": _b64(sig),
    }


def verify_genesis_proof(genesis_proof: Dict) -> bool:
    """服务端整体验注册证明：公钥派生指纹 + 签名有效。"""
    if not isinstance(genesis_proof, dict):
        return False
    try:
        pubkey = _b64_decode(genesis_proof.get("pubkey", ""))
        canonical = __import__("json").dumps(
            genesis_proof.get("declaration"), sort_keys=True, ensure_ascii=False
        )
        sig = _b64_decode(genesis_proof.get("sig", ""))
    except Exception:
        return False
    if len(pubkey) != _ED25519_RAW_BYTES or len(sig) != 64:
        return False
    return verify_signature(pubkey, canonical.encode("utf-8"), sig)


# ============================================================
# C. Shamir 秘密共享（主身份私钥分片托管，恢复层用）
# ============================================================
# 域素数：257位素数 2^256 + 297（确定素数）。
# 大于 2^256 - 1，任何 32 字节私钥种子（作为整数）必然小于该素数，
# 保证所有 Ed25519 私钥种子都可以无报错拆分重组。
# 拆分重组得到的种子与原种子完全一致，cryptography 库自动处理 clamping。
_SHAMIR_PRIME = 2**256 + 297


def _eval_poly(coeffs, x, prime):
    """霍纳法求多项式值：coeffs[0] 为常数项（秘密）。"""
    y = 0
    for c in reversed(coeffs):
        y = (y * x + c) % prime
    return y


def _lagrange_at_zero(points, prime):
    """拉格朗日插值在 x=0 处的值（即恢复的秘密）。"""
    result = 0
    for i, (xi, yi) in enumerate(points):
        num = 1
        den = 1
        for j, (xj, _) in enumerate(points):
            if i == j:
                continue
            num = (num * (0 - xj)) % prime
            den = (den * (xi - xj)) % prime
        result = (result + yi * num * pow(den, prime - 2, prime)) % prime
    return result


def shamir_split(secret_bytes: bytes, threshold: int, num_shares: int):
    """把 secret_bytes 拆成 num_shares 份，任意 threshold 份可恢复。

    返回 [(x, y), ...]，x 从 1 开始递增；y 为域内整数。
    """
    if not (1 <= threshold <= num_shares):
        raise ValueError("threshold must satisfy 1 <= threshold <= num_shares")
    secret_int = int.from_bytes(secret_bytes, "big")
    if secret_int >= _SHAMIR_PRIME:
        raise ValueError("secret too large for Shamir field")
    coeffs = [secret_int] + [
        secrets.randbelow(_SHAMIR_PRIME) for _ in range(threshold - 1)
    ]
    shares = []
    for x in range(1, num_shares + 1):
        shares.append((x, _eval_poly(coeffs, x, _SHAMIR_PRIME)))
    return shares


def shamir_combine(shares) -> bytes:
    """由任意 threshold 份分片恢复原始 secret_bytes（32 字节）。"""
    if not shares:
        raise ValueError("no shares provided")
    secret_int = _lagrange_at_zero(shares, _SHAMIR_PRIME)
    return secret_int.to_bytes(32, "big")


# ============================================================
# D. 服务端签名密钥托管抽象（KMS，可插拔 HSM）
# ============================================================

class KmsKeyProvider:
    """服务端签名密钥托管抽象。默认文件后端，生产可替换为 HSM/云 KMS。"""

    def get_or_create_key(self, key_id: str) -> bytes:
        raise NotImplementedError


class FileKmsProvider(KmsKeyProvider):
    """文件后端 KMS：密钥落盘到 key_dir/key_id（生产应替换为 HSM）。"""

    def __init__(self, key_dir: str):
        self.key_dir = key_dir

    def get_or_create_key(self, key_id: str) -> bytes:
        return load_or_create_key(os.path.join(self.key_dir, key_id))


class CloudKmsProvider(KmsKeyProvider):
    """云 KMS 后端（生产用）：密钥由云 HSM 托管，本地进程不持久化明文密钥。

    信封加密模型：
      - KEK（主密钥）由云 KMS 托管，永不下发到本进程
      - DEK（数据密钥）经 KMS 生成，加密密文落库，明文仅内存短存
    用法（生产，client 为对应云厂商 SDK 的适配器）：
      from my_kms_adapter import client   # 腾讯云 KMS / AWS KMS / 阿里云 KMS ...
      kms = CloudKmsProvider(client)
      key = kms.get_or_create_key("session_signing_key")
    client 约定实现以下方法：
      - create_key(key_id) -> None          创建主密钥（幂等）
      - generate_data_key(key_id) -> (plaintext, ciphertext)
        生成数据密钥，返回明文+密文对
      - decrypt(ciphertext) -> plaintext     解密数据密钥

    本地未注入云客户端（client=None）时自动降级文件后端（演示/测试），
    构造时打印一次警告，便于发现漏配。
    """

    def __init__(self, client=None, key_dir: Optional[str] = None):
        self._client = client
        self._key_dir = key_dir or "."
        # 信封加密元数据存储：key_id -> encrypted_dek（base64）
        self._envelope_path = os.path.join(self._key_dir, ".kms_envelope.json")
        self._envelopes: Dict[str, str] = {}
        self._load_envelopes()
        if client is None:
            print(
                "[kms] CloudKmsProvider 未注入云客户端，降级为文件后端"
                f"（{os.path.join(self._key_dir, '<key_id>')}）；生产环境请注入云 KMS client"
            )

    def _load_envelopes(self) -> None:
        """加载已持久化的信封密文（加密的 DEK）。"""
        try:
            with open(self._envelope_path, "r") as f:
                self._envelopes = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._envelopes = {}

    def _save_envelopes(self) -> None:
        """持久化信封密文。"""
        os.makedirs(self._key_dir, exist_ok=True)
        with open(self._envelope_path, "w") as f:
            json.dump(self._envelopes, f)

    def get_or_create_key(self, key_id: str) -> bytes:
        if self._client is None:
            # 演示/测试降级：文件持久化（与 FileKmsProvider 等价，生产不可用）
            return load_or_create_key(os.path.join(self._key_dir, key_id))

        # 信封加密：首次创建 DEK 并用云 KMS 加密，后续从密文解密
        if key_id in self._envelopes:
            # 已有信封：用云 KMS 解密 DEK 密文 → 明文
            encrypted_dek = base64.b64decode(self._envelopes[key_id])
            plaintext_dek = self._client.decrypt(encrypted_dek)
            return plaintext_dek

        # 首次创建：请求云 KMS 生成数据密钥对
        try:
            self._client.create_key(key_id)
        except Exception:
            pass  # 幂等：密钥已存在不报错
        plaintext_dek, encrypted_dek = self._client.generate_data_key(key_id)
        self._envelopes[key_id] = base64.b64encode(encrypted_dek).decode("ascii")
        self._save_envelopes()
        return plaintext_dek


__all__ = [
    "generate_key",
    "load_or_create_key",
    "generate_user_keypair",
    "public_from_private",
    "derive_soul_hash_from_pubkey",
    "sign_with_device",
    "verify_signature",
    "build_genesis_proof",
    "verify_genesis_proof",
    "shamir_split",
    "shamir_combine",
    "KmsKeyProvider",
    "FileKmsProvider",
    "CloudKmsProvider",
]