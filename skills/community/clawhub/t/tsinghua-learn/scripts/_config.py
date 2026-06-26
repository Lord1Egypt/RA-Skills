#!/usr/bin/env python3
"""
_config.py — 路径 + 配置 + 凭证集中管理
所有脚本通过 import _config 获取路径/配置/账号密码
凭证使用 Windows DPAPI 加密（非 Windows 回退 base64 编码）
"""
import os, json, base64, sys, ctypes
from ctypes import wintypes

_SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_CRED_FILE   = os.path.join(_SKILL_DIR, "credentials.json")
_CONFIG_FILE = os.path.join(_SKILL_DIR, "config.json")
_STATE_FILE  = os.path.join(_SKILL_DIR, "sessions", "learn_session.json")
_FP_FILE     = os.path.join(_SKILL_DIR, "profiles", "learn_fingerprint.json")
_PROFILE_DIR = os.path.join(_SKILL_DIR, "profiles", "learn_profile")
_UPLOAD_DIR  = os.path.join(_SKILL_DIR, "uploads")


def _load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


# ── DPAPI 加密工具（Windows）─────────────────────
_DPAPI_AVAILABLE = False

if sys.platform == "win32":
    try:
        class _DATA_BLOB(ctypes.Structure):
            _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_ubyte))]
        _crypt32 = ctypes.windll.crypt32
        _kernel32 = ctypes.windll.kernel32
        _CRYPTPROTECT_UI_FORBIDDEN = 0x1
        _DPAPI_AVAILABLE = True
    except Exception:
        pass


def _dpapi_encrypt(plaintext):
    """Windows DPAPI 加密，绑定当前用户账户。非 Windows 平台报错。"""
    if not _DPAPI_AVAILABLE:
        raise RuntimeError("DPAPI 仅支持 Windows 平台，无法加密凭据")
    data_bytes = plaintext.encode()
    data_in = _DATA_BLOB(len(data_bytes), ctypes.cast(ctypes.create_string_buffer(data_bytes), ctypes.POINTER(ctypes.c_ubyte)))
    data_out = _DATA_BLOB()
    entropy = _DATA_BLOB()
    if _crypt32.CryptProtectData(ctypes.byref(data_in), "tsinghua-learn", ctypes.byref(entropy),
                                 None, None, _CRYPTPROTECT_UI_FORBIDDEN, ctypes.byref(data_out)):
        raw = ctypes.string_at(data_out.pbData, data_out.cbData)
        _kernel32.LocalFree(data_out.pbData)
        return base64.b64encode(raw).decode()
    return base64.b64encode(plaintext.encode()).decode()


def _dpapi_decrypt(ciphertext):
    """Windows DPAPI 解密，仅当前用户可解密。非 Windows 平台报错。"""
    if not _DPAPI_AVAILABLE:
        raise RuntimeError("DPAPI 仅支持 Windows 平台，无法解密凭据")
    try:
        raw = base64.b64decode(ciphertext)
    except Exception:
        return ciphertext
    data_in = _DATA_BLOB(len(raw), ctypes.cast(ctypes.create_string_buffer(raw), ctypes.POINTER(ctypes.c_ubyte)))
    data_out = _DATA_BLOB()
    entropy = _DATA_BLOB()
    if _crypt32.CryptUnprotectData(ctypes.byref(data_in), None, ctypes.byref(entropy),
                                   None, None, _CRYPTPROTECT_UI_FORBIDDEN, ctypes.byref(data_out)):
        result = ctypes.string_at(data_out.pbData, data_out.cbData).decode()
        _kernel32.LocalFree(data_out.pbData)
        return result
    return ciphertext


def encode_cred(s):
    return _dpapi_encrypt(s)

def decode_cred(s):
    return _dpapi_decrypt(s)


# ── 配置 ──────────────────────────────────────
_cfg = None
def load_config():
    global _cfg
    if _cfg is not None:
        return _cfg
    if not os.path.exists(_CONFIG_FILE):
        _cfg = {}
    else:
        _cfg = _load_json(_CONFIG_FILE)
    return _cfg

def get_semester():
    """学期从 API 自动检测，此处仅作手动覆盖（可在 config.json 中添加 semester 字段）。"""
    return load_config().get("semester") or ""

_DOWNLOAD_DIR = os.path.join(_SKILL_DIR, "downloads")
def get_download_dir():
    return _DOWNLOAD_DIR


# ── 用户偏好配置 ────────────────────────────
def get_config(key, default=None):
    return load_config().get(key, default)

def auto_mark_read():
    return get_config("auto_mark_read", False)

def confirm_before_cleanup():
    return get_config("confirm_before_cleanup", True)

def confirm_before_download():
    return get_config("confirm_before_download", True)

def is_initialized():
    """检查是否已完成初始化：credentials.json 存在且 4 个字段均非空。"""
    creds = load_credentials()
    required = ["username", "password", "student_id", "name"]
    return all(creds.get(k) for k in required)


# ── 凭证 ──────────────────────────────────────
def load_credentials():
    """返回 dict: username, password, student_id, name（已解密）"""
    if not os.path.exists(_CRED_FILE):
        return {}
    cred = _load_json(_CRED_FILE)
    return {k: decode_cred(v) for k, v in cred.items()}

def save_credentials(username, password, student_id="", name=""):
    """Windows DPAPI 加密后写入 credentials.json（非 Windows 回退 base64 编码）"""
    data = {
        "username": encode_cred(username),
        "password": encode_cred(password),
        "student_id": encode_cred(student_id),
        "name": encode_cred(name),
    }
    with open(_CRED_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_student_id():
    return load_credentials().get("student_id", "")

def get_student_name():
    return load_credentials().get("name", "")

def get_username():
    return load_credentials().get("username", "")


# ── 路径 getter ──────────────────────────────
def get_state_file():
    return _STATE_FILE

def get_fp_file():
    return _FP_FILE

def get_profile_dir():
    return _PROFILE_DIR

def get_skill_dir():
    return _SKILL_DIR

def get_upload_dir():
    os.makedirs(_UPLOAD_DIR, exist_ok=True)
    return _UPLOAD_DIR

def get_submissions_log():
    """返回 submissions 日志文件路径。"""
    d = os.path.join(_SKILL_DIR, "submissions")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, "submissions_log.json")

def get_download_dir_abs():
    return get_download_dir()
