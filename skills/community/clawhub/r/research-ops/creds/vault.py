#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""opencode skill 通用凭据保险箱（canonical 版本，各 skill 原样复制到 <skill>/creds/vault.py）

单文件加密 + 单一主密钥（纯 Python，仅依赖 cryptography）:
- 密文文件: <skill>/runtime/credentials.enc，格式 "v1:<b64salt>:<b64token>"
- 主密钥来源（按优先级）:
    1. 环境变量 OPENCODE_SKILL_MASTER_KEY     ← 跨机同步：各设备填同一个值（首选）
    2. 兼容旧环境变量 CAMPUS_MASTER_KEY / AIGW_MASTER_KEY / YUANBAO_MASTER_KEY
    3. OS keyring (service=opencode-skill, account=__master_key)
    4. 密钥文件 <skill>/runtime/vault/master.key (0600)
- 密文随 skill 文件夹同步到各设备；换机只需 export 同一个主密钥
- Scrypt 派生 Fernet key，每个保险箱文件独立 salt

API:
  vault_read() -> dict             读整箱（解不开抛 VaultLocked）
  vault_write(data)                写整箱（无主密钥则自动生成）
  vault_get(key) -> str            取一条（读不到返回 ""）
  vault_set(key, value)            存一条
  vault_delete(key) -> bool        删一条
  vault_keys() -> list             全部 key 名
  get_master_key(create=False) -> (key, source)
  set_master_key(value, where) -> where
  master_key_source() -> str|None
异常:
  VaultLocked  保险箱存在但缺主密钥/主密钥不匹配
"""
import base64
import json
import os
import secrets
import sys

MASTER_KEY_ENV = "OPENCODE_SKILL_MASTER_KEY"
LEGACY_MASTER_KEY_ENVS = ("CAMPUS_MASTER_KEY", "AIGW_MASTER_KEY", "YUANBAO_MASTER_KEY")
KEYRING_SERVICE = "opencode-skill"
KEYRING_ACCOUNT = "__master_key"

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNTIME_DIR = os.path.join(SKILL_ROOT, "runtime")
VAULT_FILE = os.path.join(RUNTIME_DIR, "credentials.enc")
KEY_FILE = os.path.join(RUNTIME_DIR, "vault", "master.key")

_KEYRING_CACHE = None


class VaultLocked(Exception):
    """保险箱存在但无法解密（缺主密钥 / 主密钥不匹配）"""


# ==================== 主密钥来源 ====================

def _keyring_ok():
    global _KEYRING_CACHE
    if _KEYRING_CACHE is not None:
        return _KEYRING_CACHE
    try:
        import keyring
        keyring.set_password(KEYRING_SERVICE, "_probe", "1")
        ok = keyring.get_password(KEYRING_SERVICE, "_probe") == "1"
        try:
            keyring.delete_password(KEYRING_SERVICE, "_probe")
        except Exception:
            pass
        _KEYRING_CACHE = ok
    except Exception:
        _KEYRING_CACHE = False
    return _KEYRING_CACHE


def _env_master():
    v = (os.environ.get(MASTER_KEY_ENV) or "").strip()
    if v:
        return v, "env"
    for name in LEGACY_MASTER_KEY_ENVS:
        v = (os.environ.get(name) or "").strip()
        if v:
            return v, f"env:{name}"
    return "", None


def _keyring_master():
    if not _keyring_ok():
        return "", None
    try:
        import keyring
        return (keyring.get_password(KEYRING_SERVICE, KEYRING_ACCOUNT) or "").strip(), "keyring"
    except Exception:
        return "", None


def _file_master():
    if not os.path.exists(KEY_FILE):
        return "", None
    try:
        with open(KEY_FILE, encoding="utf-8") as f:
            return f.read().strip(), "file"
    except Exception:
        return "", None


def get_master_key(create=False):
    """返回 (主密钥, 来源)。来源: env / env:<legacy> / keyring / file；无则 (None, None)。"""
    for fn in (_env_master, _keyring_master, _file_master):
        v, src = fn()
        if v:
            return v, src
    if create:
        v = secrets.token_urlsafe(32)
        return v, _store_master(v)
    return None, None


def _store_master(value):
    if _keyring_ok():
        try:
            import keyring
            keyring.set_password(KEYRING_SERVICE, KEYRING_ACCOUNT, value)
            return "keyring"
        except Exception:
            pass
    os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)
    with open(KEY_FILE, "w", encoding="utf-8") as f:
        f.write(value)
    try:
        os.chmod(KEY_FILE, 0o600)
    except Exception:
        pass
    return "file"


def set_master_key(value, where="auto"):
    """显式设置主密钥（迁移/换密钥）。where: auto/keyring/file。返回写入位置。"""
    if where in ("auto", "keyring") and _keyring_ok():
        try:
            import keyring
            keyring.set_password(KEYRING_SERVICE, KEYRING_ACCOUNT, value)
            return "keyring"
        except Exception:
            if where == "keyring":
                raise
    os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)
    with open(KEY_FILE, "w", encoding="utf-8") as f:
        f.write(value)
    try:
        os.chmod(KEY_FILE, 0o600)
    except Exception:
        pass
    return "file"


def master_key_source():
    for fn in (_env_master, _keyring_master, _file_master):
        v, src = fn()
        if v:
            return src
    return None


# ==================== 加解密 ====================

def _fernet_key(master, salt):
    from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
    kdf = Scrypt(salt=salt, length=32, n=2 ** 14, r=8, p=1)
    return base64.urlsafe_b64encode(kdf.derive(master.encode("utf-8")))


def _atomic_write(path, text, mode=0o600):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    try:
        os.chmod(tmp, mode)
    except Exception:
        pass
    os.replace(tmp, path)


def vault_write(data):
    from cryptography.fernet import Fernet
    master, _ = get_master_key(create=True)
    salt = os.urandom(16)
    token = Fernet(_fernet_key(master, salt)).encrypt(
        json.dumps(data, ensure_ascii=False).encode("utf-8"))
    payload = "v1:" + base64.urlsafe_b64encode(salt).decode("ascii") + ":" + token.decode("ascii")
    _atomic_write(VAULT_FILE, payload)
    return VAULT_FILE


def vault_read():
    from cryptography.fernet import Fernet
    if not os.path.exists(VAULT_FILE):
        return {}
    with open(VAULT_FILE, encoding="utf-8") as f:
        payload = f.read().strip()
    if not payload:
        return {}
    if not payload.startswith("v1:"):
        raise VaultLocked("保险箱格式不支持（非 v1）")
    try:
        _, b64salt, token = payload.split(":", 2)
        salt = base64.urlsafe_b64decode(b64salt)
    except Exception:
        raise VaultLocked("保险箱文件损坏")
    master, _ = get_master_key(create=False)
    if not master:
        raise VaultLocked(
            f"未找到主密钥。请设置环境变量 {MASTER_KEY_ENV}（跨机同步时各设备填同一值），或重新配置凭据。")
    try:
        raw = Fernet(_fernet_key(master, salt)).decrypt(token.encode("ascii"))
    except Exception:
        raise VaultLocked(f"主密钥与保险箱不匹配（检查 {MASTER_KEY_ENV} 是否正确）")
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception:
        return {}


# ==================== 单条接口 ====================

def vault_get(key):
    try:
        return vault_read().get(key, "")
    except VaultLocked:
        return ""
    except Exception:
        return ""


def vault_set(key, value):
    data = vault_read()
    data[key] = value
    vault_write(data)


def vault_delete(key):
    data = vault_read()
    if key in data:
        del data[key]
        vault_write(data)
        return True
    return False


def vault_keys():
    try:
        return sorted(vault_read().keys())
    except Exception:
        return []


def as_env(prefixes=None):
    """把保险箱内容展开成 os.environ 可用的 dict；可选按前缀过滤。"""
    data = vault_read()
    if prefixes:
        data = {k: v for k, v in data.items() if k.startswith(tuple(prefixes))}
    return data


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="opencode 通用凭据保险箱")
    ap.add_argument("--test", action="store_true", help="加解密往返自测（用临时文件）")
    ap.add_argument("--status", action="store_true", help="主密钥来源与保险箱状态")
    a = ap.parse_args()
    if a.test:
        import tempfile
        tmp = os.path.join(tempfile.gettempdir(), "opencode_vault_selftest.enc")
        _ov = VAULT_FILE
        globals()["VAULT_FILE"] = tmp
        os.environ.setdefault(MASTER_KEY_ENV, "selftest-" + secrets.token_hex(8))
        try:
            probe = {"k1": "甲", "k2": "乙"}
            vault_write(probe)
            ok = vault_read() == probe
        finally:
            globals()["VAULT_FILE"] = _ov
            try:
                os.remove(tmp)
            except Exception:
                pass
        print(json.dumps({"status": "ok" if ok else "error", "roundtrip_ok": ok,
                          "master_key_source": "env(selftest)"}, ensure_ascii=False))
    elif a.status:
        print(json.dumps({
            "status": "ok",
            "vault_file": VAULT_FILE,
            "vault_exists": os.path.exists(VAULT_FILE),
            "master_key_source": master_key_source(),
            "keyring_ok": _keyring_ok(),
            "keys": vault_keys(),
        }, ensure_ascii=False, indent=2))
