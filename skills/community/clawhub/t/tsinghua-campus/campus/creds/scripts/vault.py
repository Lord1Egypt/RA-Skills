"""vault.py — 统一凭据保险箱（单文件加密 + 单一主密钥）

设计:
- 所有凭据存于**单个**文件 runtime/credentials.enc（Fernet 加密的 JSON）
  → 随 SKILL 文件夹同步，即可跨机携带（密文）
- 解密只需**一个**主密钥，来源优先级:
    1. 环境变量 CAMPUS_MASTER_KEY   ← 跨机同步用：各设备填同一个值
    2. OS keyring 单条 (campus-skill:__master_key)  ← 本机绑定，自动生成
    3. 密钥文件 runtime/vault/master.key (0600)     ← keyring 不可用时兜底
- 主密钥经 Scrypt 派生 Fernet key；每个保险箱文件头带独立 salt
- 文件格式: "v1:<b64salt>:<b64token>"
- 旧格式 credentials.json（keyring:/fernet: 引用）首次读取时自动迁移

多系统:
- 纯 Python（cryptography + 标准库），无 OS 相关分支
- 环境变量名固定 CAMPUS_MASTER_KEY，各平台一致

接口:
  vault_read() -> dict          读整箱
  vault_write(data)             写整箱（无主密钥则自动生成）
  vault_get(key) -> str         取一条明文（读不到返回 ""）
  vault_set(key, value)         存一条
  vault_delete(key)             删一条
  vault_keys() -> list          全部 key
  get_master_key(create)        取主密钥 (值, 来源)
  set_master_key(value, where)  显式设置主密钥（迁移用）
"""
import os
import sys
import json
import base64
import secrets

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "shared", "scripts"))
import common

MASTER_KEY_ENV = "CAMPUS_MASTER_KEY"
KEYRING_SERVICE = "campus-skill"
KEYRING_ACCOUNT = "__master_key"

VAULT_FILE = str(common.runtime_dir("credentials.enc"))
LEGACY_FILE = str(common.runtime_dir("credentials.json"))
KEY_FILE = str(common.runtime_dir("vault", "master.key"))
_LEGACY_FERNET_KEY_FILE = str(common.runtime_dir("vault", "vault.key"))

_KEYRING_CACHE = None  # True / False / None(未检测)


class VaultLocked(Exception):
    """保险箱存在但无法解密（缺主密钥 / 主密钥不匹配）"""


# ==================== keyring 探测 ====================

def _keyring_ok():
    """检测系统 keyring 是否可用（实际 set/get 探测，避免伪后端）。"""
    global _KEYRING_CACHE
    if _KEYRING_CACHE is not None:
        return _KEYRING_CACHE
    try:
        import keyring
        keyring.set_password(KEYRING_SERVICE, "_probe", "1")
        v = keyring.get_password(KEYRING_SERVICE, "_probe")
        keyring.delete_password(KEYRING_SERVICE, "_probe")
        _KEYRING_CACHE = (v == "1")
    except Exception:
        _KEYRING_CACHE = False
    return _KEYRING_CACHE


# ==================== 主密钥读写 ====================

def _keyring_get_master():
    try:
        import keyring
        return keyring.get_password(KEYRING_SERVICE, KEYRING_ACCOUNT) or ""
    except Exception:
        return ""


def _keyring_set_master(value):
    import keyring
    keyring.set_password(KEYRING_SERVICE, KEYRING_ACCOUNT, value)


def _keyring_del_master():
    try:
        import keyring
        keyring.delete_password(KEYRING_SERVICE, KEYRING_ACCOUNT)
    except Exception:
        pass


def _file_get_master():
    if not os.path.exists(KEY_FILE):
        return ""
    try:
        with open(KEY_FILE, encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return ""


def _file_set_master(value):
    os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)
    with open(KEY_FILE, "w", encoding="utf-8") as f:
        f.write(value)
    try:
        os.chmod(KEY_FILE, 0o600)
    except Exception:
        pass


def get_master_key(create=False):
    """返回 (主密钥, 来源)。来源: env / keyring / file；无则 (None, None)。

    create=True 且三处皆无时，生成随机主密钥并落到 keyring（优先）或密钥文件。
    """
    env = os.environ.get(MASTER_KEY_ENV, "").strip()
    if env:
        return env, "env"
    if _keyring_ok():
        v = _keyring_get_master()
        if v:
            return v, "keyring"
    v = _file_get_master()
    if v:
        return v, "file"
    if create:
        v = secrets.token_urlsafe(32)
        _store_new_master(v)
        return v, master_key_source()
    return None, None


def _store_new_master(value):
    """新生成的主密钥落盘（keyring 优先，兜底密钥文件）。"""
    if _keyring_ok():
        try:
            _keyring_set_master(value)
            return "keyring"
        except Exception:
            pass
    _file_set_master(value)
    return "file"


def set_master_key(value, where="auto"):
    """显式设置主密钥（迁移/换密钥用）。where: auto/keyring/file/env-note。

    设到 keyring 或密钥文件；环境变量需用户自行 export（返回值提示）。
    返回实际写入的位置。
    """
    if where in ("auto", "keyring") and _keyring_ok():
        try:
            _keyring_set_master(value)
            return "keyring"
        except Exception:
            if where == "keyring":
                raise
    _file_set_master(value)
    return "file"


def master_key_source():
    """当前主密钥来源（不创建）: env/keyring/file/None。"""
    if os.environ.get(MASTER_KEY_ENV, "").strip():
        return "env"
    if _keyring_ok() and _keyring_get_master():
        return "keyring"
    if _file_get_master():
        return "file"
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
    """加密整箱写盘（无主密钥则自动生成）。"""
    from cryptography.fernet import Fernet
    master, _ = get_master_key(create=True)
    salt = os.urandom(16)
    f = Fernet(_fernet_key(master, salt))
    token = f.encrypt(json.dumps(data, ensure_ascii=False).encode("utf-8"))
    payload = "v1:" + base64.urlsafe_b64encode(salt).decode("ascii") + ":" + token.decode("ascii")
    _atomic_write(VAULT_FILE, payload)


def vault_read():
    """读整箱并解密。文件不存在返回 {}；无法解密抛 VaultLocked。"""
    from cryptography.fernet import Fernet
    if not os.path.exists(VAULT_FILE):
        _migrate_legacy()
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
            "未找到主密钥。请设置环境变量 CAMPUS_MASTER_KEY（跨机同步时各设备填同一值），"
            "或重新配置凭据。")
    try:
        raw = Fernet(_fernet_key(master, salt)).decrypt(token.encode("ascii"))
    except Exception:
        raise VaultLocked("主密钥与保险箱不匹配（请检查 CAMPUS_MASTER_KEY 是否正确）")
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception:
        return {}


# ==================== 对外的单条接口 ====================

def vault_get(key):
    """取一条明文（读不到/解不开返回 ""）。"""
    try:
        return vault_read().get(key, "")
    except VaultLocked as e:
        common.log(f"[vault] 读取失败: {e}")
        return ""
    except Exception as e:
        common.log(f"[vault] 读取异常: {e}")
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


# ==================== 旧格式迁移 ====================

def _legacy_decrypt(key, ref):
    """解旧 credentials.json 的引用值（keyring: / fernet:）。"""
    if not ref:
        return ""
    if ref.startswith("keyring:"):
        acc = ref[len("keyring:"):]
        if not acc.startswith("campus:"):
            acc = f"campus:{key}"
        try:
            import keyring
            return keyring.get_password(KEYRING_SERVICE, acc) or ""
        except Exception:
            return ""
    body = ref[len("fernet:"):] if ref.startswith("fernet:") else ref
    try:
        from cryptography.fernet import Fernet
        if not os.path.exists(_LEGACY_FERNET_KEY_FILE):
            return ""
        with open(_LEGACY_FERNET_KEY_FILE, "rb") as f:
            fk = f.read()
        return Fernet(fk).decrypt(body.encode("ascii")).decode("utf-8")
    except Exception:
        return ""


def purge_legacy_keyring(keys):
    """删除旧的 per-credential keyring 条目（值已在保险箱里，避免明文冗余副本）。

    旧格式 account = "campus:<key>"（较新）或 "campus"（更旧的共享条目）。
    返回删除条数。
    """
    if not _keyring_ok():
        return 0
    import keyring
    removed = 0
    for acc in [f"campus:{k}" for k in keys] + ["campus"]:
        try:
            if keyring.get_password(KEYRING_SERVICE, acc):
                keyring.delete_password(KEYRING_SERVICE, acc)
                removed += 1
        except Exception:
            pass
    if removed:
        common.log(f"[vault] 已清理旧 keyring 条目 {removed} 条")
    return removed


def _migrate_legacy():
    """把旧 credentials.json 迁进新保险箱（仅当新箱不存在时）。"""
    if os.path.exists(VAULT_FILE) or not os.path.exists(LEGACY_FILE):
        return
    try:
        with open(LEGACY_FILE, encoding="utf-8") as f:
            stored = json.load(f)
    except Exception:
        return
    if not isinstance(stored, dict) or not stored:
        return
    data = {}
    for k, ref in stored.items():
        val = _legacy_decrypt(k, ref)
        if val:
            data[k] = val
    if not data:
        return
    vault_write(data)
    # 清理旧 keyring 条目（已复制进保险箱，去掉明文冗余副本）
    purge_legacy_keyring(list(stored.keys()))
    try:
        os.replace(LEGACY_FILE, LEGACY_FILE + ".migrated")
    except Exception:
        pass
    common.log(f"[vault] 已从 credentials.json 迁移 {len(data)} 条凭据到 credentials.enc")


# ==================== 向后兼容（旧 API） ====================

def vault_encrypt(key, plaintext):
    """[已废弃] 兼容旧调用：写入保险箱并返回引用标记。"""
    vault_set(key, plaintext)
    return f"vault:{key}"


def vault_decrypt(key, ciphertext):
    """[已废弃] 兼容旧调用：从保险箱取明文。"""
    return vault_get(key)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="凭据保险箱（加密 + 单主密钥）")
    ap.add_argument("--test", action="store_true", help="自测加解密往返")
    ap.add_argument("--status", action="store_true", help="主密钥来源与保险箱状态")
    args = ap.parse_args()
    if args.test:
        import tempfile
        tmp = os.path.join(tempfile.gettempdir(), "campus_vault_selftest.enc")
        _ov, _ol = VAULT_FILE, LEGACY_FILE
        VAULT_FILE = tmp
        LEGACY_FILE = tmp + ".legacy"
        try:
            probe = {"k1": "甲-值", "k2": "乙-值", "k3": "aaa"}
            vault_write(probe)
            got = vault_read()
            ok = all(got.get(k) == v for k, v in probe.items())
            vault_set("k1", "AAA")
            vault_set("k2", "BBB")
            isolated = (vault_get("k1") == "AAA" and vault_get("k2") == "BBB")
        finally:
            VAULT_FILE, LEGACY_FILE = _ov, _ol
            for f in (tmp, tmp + ".legacy"):
                try:
                    os.remove(f)
                except Exception:
                    pass
        common.output_json({
            "status": "ok" if (ok and isolated) else "error",
            "platform": common.detect_platform(),
            "master_key_source": master_key_source(),
            "keyring_ok": _keyring_ok(),
            "roundtrip_ok": ok,
            "isolated_ok": isolated,
        })
    elif args.status:
        common.output_json({
            "status": "ok",
            "vault_file": VAULT_FILE,
            "vault_exists": os.path.exists(VAULT_FILE),
            "master_key_source": master_key_source(),
            "keyring_ok": _keyring_ok(),
            "keys": vault_keys(),
        })
