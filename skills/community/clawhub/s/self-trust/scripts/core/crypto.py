# -*- coding: utf-8 -*-
"""self-trust 可选的本地静态加密（opt-in，默认关）。

设计（方案 C：两种密钥路线都支持，默认 passphrase）：
- 算法：AES-256-GCM（AEAD，认证加密，防篡改）；密钥派生 passphrase → PBKDF2-HMAC-SHA256。
- 密钥路线：
  - passphrase：用户记密码，每次 CLI 需 --pass 或 SELFTRUST_PASS 环境变量。密钥不在磁盘。
  - key-file：自动生成 32 字节随机 key 存本地文件（权限锁 600），无感。key 与密文同目录→防云同步泄露/窥探够用，防定向窃取不足。
- 文件格式：MAGIC 头 + 模式字节(P=passphrase / K=key-file) + salt(仅 P) + nonce(12) + ciphertext。
- 透明集成：模块级 session 携带本次调用的密钥材料；contract.py / audit.py 在读写时自动加解密。
  非加密契约（无 MAGIC、无 crypto.enabled）→ 明文直读，向后兼容。

依赖：cryptography（仅启用加密时需要，非加密路径纯 stdlib）。缺失时报清晰可操作错误。
"""
from __future__ import annotations

import base64
import json
import os
import secrets
from pathlib import Path
from typing import Any

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    _HAVE_CRYPTO = True
except ImportError:  # pragma: no cover — 仅在未装 cryptography 时触发
    _HAVE_CRYPTO = False

MAGIC = b"STENC1\n"          # 加密文件魔数（检测 + 防误当明文 json 解析）
PBKDF2_ITER = 200_000        # PBKDF2 迭代次数（2026 年消费级足够）
SALT_LEN = 16
NONCE_LEN = 12
KEY_LEN = 32                 # AES-256
MODE_PASS = b"P"             # passphrase 派生密钥
MODE_KEY = b"K"              # raw key-file


class CryptoError(Exception):
    """加密子系统错误（基类）。"""


class InvalidPassphrase(CryptoError):
    """密码错误 / 数据损坏（GCM tag 校验失败）。"""


class CryptoUnavailable(CryptoError):
    """未安装 cryptography 却尝试加密/解密。"""


# ── 模块级 session（单次 CLI 调用内有效，测试间需 reset）──────────────
_session: dict = {}          # {"passphrase": str} | {"key_file": Path} | {}
_audit_encrypted: bool = False


def set_session(*, passphrase: str | None = None,
                key_file: str | Path | None = None) -> None:
    """设置本次调用的密钥材料。passphrase 与 key_file 互斥，皆空=清 session。"""
    global _session
    if passphrase is not None:
        _session = {"passphrase": passphrase}
    elif key_file is not None:
        _session = {"key_file": Path(key_file)}
    else:
        _session = {}


def reset_session() -> None:
    """清空 session + audit 加密标志（测试隔离用）。"""
    global _session, _audit_encrypted
    _session = {}
    _audit_encrypted = False


def get_session() -> dict:
    return dict(_session)


def have_session() -> bool:
    return bool(_session)


def set_audit_encrypted(flag: bool) -> None:
    """声明审计日志（audit/*.jsonl）是否加密（由契约 crypto.enabled 驱动）。"""
    global _audit_encrypted
    _audit_encrypted = bool(flag)


def is_encrypted(blob: bytes) -> bool:
    """文件内容是否为本模块加密格式。"""
    return blob.startswith(MAGIC)


# ── 底层原语 ──────────────────────────────────────────────────────────
def _require_crypto() -> None:
    if not _HAVE_CRYPTO:
        raise CryptoUnavailable(
            "加密功能需安装 cryptography："
            "pip install cryptography")


def _load_key(key_file: str | Path) -> bytes:
    """读取 key-file 模式的 raw key（32 字节 raw 或 64 十六进制）。"""
    p = Path(key_file)
    if not p.is_file():
        raise CryptoError(f"密钥文件不存在: {p}")
    data = p.read_bytes()
    if len(data) == KEY_LEN:
        return data
    if len(data) == KEY_LEN * 2:
        try:
            return bytes.fromhex(data.decode("ascii").strip())
        except (ValueError, UnicodeDecodeError):
            pass
    raise CryptoError(
        f"密钥文件格式错误（须 32 字节 raw 或 64 位十六进制，得到 {len(data)} 字节）")


def _session_key() -> bytes:
    """从 session 取对称密钥（已派生/已加载）。"""
    if not _session:
        raise CryptoError("加密契约需要密钥材料：--pass / --key-file 或对应环境变量")
    if "passphrase" in _session:
        # passphrase 模式每次派生需 salt，密钥在 seal/unseal 内按 salt 现算
        raise CryptoError("passphrase 模式不能直接取静态 key（须带 salt 派生）")
    return _load_key(_session["key_file"])


def _session_passphrase() -> str:
    if not _session or "passphrase" not in _session:
        raise CryptoError("passphrase 模式需要密码：--pass 或 SELFTRUST_PASS")
    return _session["passphrase"]


# ── 对外 API ──────────────────────────────────────────────────────────
def seal(plaintext: bytes, *,
         passphrase: str | None = None,
         key: bytes | None = None) -> bytes:
    """加密字节 → 带 MAGIC 的 blob。passphrase 与 key 二选一（皆空则回退 session）。"""
    _require_crypto()
    if passphrase is None and key is None:
        if "passphrase" in _session:
            passphrase = _session["passphrase"]
        elif "key_file" in _session:
            key = _load_key(_session["key_file"])
    if passphrase is not None:
        salt = secrets.token_bytes(SALT_LEN)
        k = _derive_key(passphrase, salt)
        header = MODE_PASS + salt
    elif key is not None:
        k = key
        header = MODE_KEY
    else:
        raise CryptoError("seal 需要 passphrase 或 key（或先 set_session）")
    aes = AESGCM(k)
    nonce = secrets.token_bytes(NONCE_LEN)
    ct = aes.encrypt(nonce, plaintext, None)
    return MAGIC + header + nonce + ct


def unseal(blob: bytes, *,
           passphrase: str | None = None,
           key: bytes | None = None) -> bytes:
    """解密 blob → 明文字节。密码错误/损坏 → InvalidPassphrase。"""
    _require_crypto()
    if not is_encrypted(blob):
        raise CryptoError("非加密数据，无法解密（缺少魔数头）")
    body = blob[len(MAGIC):]
    mode = body[0:1]
    rest = body[1:]
    if mode == MODE_PASS:
        if passphrase is None:
            passphrase = _session_passphrase()
        salt = rest[:SALT_LEN]
        nonce = rest[SALT_LEN:SALT_LEN + NONCE_LEN]
        ct = rest[SALT_LEN + NONCE_LEN:]
        k = _derive_key(passphrase, salt)
    elif mode == MODE_KEY:
        if key is None:
            key = _session_key()
        k = key
        nonce = rest[:NONCE_LEN]
        ct = rest[NONCE_LEN:]
    else:
        raise CryptoError(f"未知加密模式字节: {mode!r}")
    aes = AESGCM(k)
    try:
        return aes.decrypt(nonce, ct, None)
    except Exception:  # GCM tag 校验失败：密码错或数据损坏
        raise InvalidPassphrase("密码错误，或数据已损坏")


def seal_json(obj: Any, **kw) -> bytes:
    return seal(json.dumps(obj, ensure_ascii=False, indent=2).encode("utf-8"), **kw)


def unseal_json(blob: bytes, **kw) -> Any:
    return json.loads(unseal(blob, **kw).decode("utf-8"))


def _derive_key(passphrase: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=KEY_LEN,
                     salt=salt, iterations=PBKDF2_ITER)
    return kdf.derive(passphrase.encode("utf-8"))


def generate_key_file(path: str | Path) -> Path:
    """生成随机 key 文件（权限 600），返回路径。key-file 模式初始化用。"""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    key = secrets.token_bytes(KEY_LEN)
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    if hasattr(os, "O_BINARY"):
        flags |= os.O_BINARY
    fd = os.open(str(p), flags, 0o600)
    try:
        os.write(fd, key)
    finally:
        os.close(fd)
    # 兜底确保权限（某些平台 O_CREAT mode 被 umask 影响）
    try:
        os.chmod(p, 0o600)
    except OSError:
        pass
    return p
