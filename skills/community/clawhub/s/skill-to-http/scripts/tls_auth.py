#!/usr/bin/env python3
"""tls_auth.py — HTTP 类 skill 通用 TLS + API Key + HMAC 鉴权模板

这是一个独立模块，**完整 self-contained，可被三个 HTTP 类 skill 直接 copy**：
  - agent-easy-http
  - skill-to-http
  - skill-to-http-flash

规范文档：references/tls-auth-standard.md
"""

from __future__ import annotations

import hashlib
import hmac
import os
import secrets
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# ── 统一目录约定（K8s 容器友好） ────────────────────────────────────
# 优先级：
#   1. OPENCLAW_HTTP_ROOT 环境变量（最高）
#   2. <workspace>/.http/（推荐，挂 PVC 持久化，容器重启不丢）
#   3. ~/.http/（兜底，非 OpenClaw 环境）

def detect_http_root() -> Path:
    """探测 HTTP 类 skill 的持久化根目录。

    K8s Pod 场景下 ~/ 下的非 workspace 目录可能不挂 PVC，重启会丢；
    放在 workspace 下能跟着 PVC 一起持久化。
    """
    # 1. 环境变量显式覆盖
    env_root = os.environ.get("OPENCLAW_HTTP_ROOT")
    if env_root:
        return Path(env_root).expanduser()

    # 2. workspace 内 .http/
    workspace = os.environ.get(
        "OPENCLAW_WORKSPACE",
        str(Path.home() / ".openclaw" / "workspace"),
    )
    ws_path = Path(workspace)
    if ws_path.exists() and (ws_path / "skills").exists():
        return ws_path / ".http"

    # 3. 兜底
    return Path.home() / ".http"


HTTP_ROOT = detect_http_root()
CERT_DIR = HTTP_ROOT / "certs"          # TLS 证书三 skill 共用
SECRETS_DIR = HTTP_ROOT / "secrets"     # HMAC 各 skill 独立
API_KEYS_DIR = SECRETS_DIR / "api-keys"  # API Key 各 skill 独立

DEFAULT_CERT_PATH = CERT_DIR / "server.crt"
DEFAULT_KEY_PATH = CERT_DIR / "server.key"

# 鉴权时钟偏差容忍（秒）
HMAC_CLOCK_SKEW = 300


# ── 配置 dataclass ──────────────────────────────────────────────────
@dataclass
class TLSAuthConfig:
    """TLS + 鉴权 统一配置。三 skill 通用 schema。"""
    # TLS（默认关闭 - 证书生成/客户端导入有门槛，按需开启；0.0.0.0 暴露场景启动会 warning）
    tls_enabled: bool = False
    cert_path: str = str(DEFAULT_CERT_PATH)
    key_path: str = str(DEFAULT_KEY_PATH)

    # API Key（外部调用方鉴权）
    api_key: str = ""                   # 强制要求非空
    api_key_header: str = "X-API-Key"

    # Callback HMAC（agent 回调时的内部鉴权）
    callback_auth_enabled: bool = True
    callback_secret: str = ""           # init 时随机生成
    callback_sig_header: str = "X-Callback-Sig"
    callback_ts_header: str = "X-Callback-Ts"

    @classmethod
    def from_dict(cls, d: dict) -> "TLSAuthConfig":
        """从主 config dict 中提取 TLS/鉴权部分。"""
        return cls(
            tls_enabled=d.get("tls_enabled", False),
            cert_path=d.get("cert_path", str(DEFAULT_CERT_PATH)),
            key_path=d.get("key_path", str(DEFAULT_KEY_PATH)),
            api_key=d.get("api_key", ""),
            api_key_header=d.get("api_key_header", "X-API-Key"),
            callback_auth_enabled=d.get("callback_auth_enabled", True),
            callback_secret=d.get("callback_secret", ""),
            callback_sig_header=d.get("callback_sig_header", "X-Callback-Sig"),
            callback_ts_header=d.get("callback_ts_header", "X-Callback-Ts"),
        )

    def to_dict(self) -> dict:
        return {
            "tls_enabled": self.tls_enabled,
            "cert_path": self.cert_path,
            "key_path": self.key_path,
            "api_key": self.api_key,
            "api_key_header": self.api_key_header,
            "callback_auth_enabled": self.callback_auth_enabled,
            "callback_secret": self.callback_secret,
            "callback_sig_header": self.callback_sig_header,
            "callback_ts_header": self.callback_ts_header,
        }


# ── 随机密钥生成 ────────────────────────────────────────────────────
def generate_api_key() -> str:
    """生成 32 位 url-safe 随机字符串。"""
    return secrets.token_urlsafe(24)


def generate_hmac_secret() -> str:
    """生成 64 位 hex 随机字符串作为 HMAC 密钥。"""
    return secrets.token_hex(32)


# ── 文件持久化（用户可随时查回密钥）─────────────────────────────────
def ensure_dirs() -> None:
    """确保 <HTTP_ROOT>（默认 <workspace>/.http/ 或 ~/.http/）目录结构存在，权限 0700。"""
    HTTP_ROOT.mkdir(parents=True, exist_ok=True)
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    SECRETS_DIR.mkdir(parents=True, exist_ok=True)
    API_KEYS_DIR.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(HTTP_ROOT, 0o700)
        os.chmod(SECRETS_DIR, 0o700)
        os.chmod(API_KEYS_DIR, 0o700)
    except OSError:
        pass


def save_api_key(skill_name: str, key: str) -> Path:
    """保存 API Key 到 <HTTP_ROOT>/secrets/api-keys/<skill>.key（0600）。"""
    ensure_dirs()
    path = API_KEYS_DIR / f"{skill_name}.key"
    path.write_text(key)
    os.chmod(path, 0o600)
    return path


def save_hmac_secret(skill_name: str, secret: str) -> Path:
    """保存 HMAC secret 到 <HTTP_ROOT>/secrets/<skill>.hmac（0600）。"""
    ensure_dirs()
    path = SECRETS_DIR / f"{skill_name}.hmac"
    path.write_text(secret)
    os.chmod(path, 0o600)
    return path


def load_api_key(skill_name: str) -> Optional[str]:
    """从 <HTTP_ROOT> 读回 API Key（用户查询用）。"""
    path = API_KEYS_DIR / f"{skill_name}.key"
    if path.exists():
        return path.read_text().strip()
    return None


def load_hmac_secret(skill_name: str) -> Optional[str]:
    """从 <HTTP_ROOT> 读回 HMAC secret。"""
    path = SECRETS_DIR / f"{skill_name}.hmac"
    if path.exists():
        return path.read_text().strip()
    return None


# ── HMAC 签名/验证 ──────────────────────────────────────────────────
def compute_callback_signature(secret: str, job_id: str, timestamp: int) -> str:
    """计算回调签名：HMAC-SHA256(secret, f'{job_id}.{timestamp}')。

    返回 hex 字符串。
    """
    msg = f"{job_id}.{timestamp}".encode()
    return hmac.new(secret.encode(), msg, hashlib.sha256).hexdigest()


def verify_callback_signature(
    secret: str,
    job_id: str,
    timestamp: int,
    signature: str,
    clock_skew: int = HMAC_CLOCK_SKEW,
) -> tuple[bool, str]:
    """验证回调签名。

    返回 (is_valid, error_msg)。
    """
    # 时间窗口校验（防重放）
    now = int(time.time())
    if abs(now - timestamp) > clock_skew:
        return False, f"timestamp out of range ({clock_skew}s)"

    expected = compute_callback_signature(secret, job_id, timestamp)
    if not hmac.compare_digest(expected, signature):
        return False, "signature mismatch"

    return True, ""


# ── 启动前校验 ───────────────────────────────────────────────────────
def validate_config(cfg: TLSAuthConfig, skill_name: str) -> list[str]:
    """启动前对配置做硬校验，返回错误列表（空=通过）。

    强制要求：
    - API Key 必须非空（HTTPS 暴露场景下没鉴权太危险）
    - callback_auth_enabled=True 时 callback_secret 必须非空
    - tls_enabled=True 时 cert/key 文件必须存在
    """
    errors: list[str] = []

    if not cfg.api_key:
        errors.append(
            f"api_key 不能为空。请运行 `python3 scripts/init_wizard.py` 自动生成，"
            f"或自行设置后写入 {API_KEYS_DIR / (skill_name + '.key')}"
        )

    if cfg.callback_auth_enabled and not cfg.callback_secret:
        errors.append(
            f"callback_auth_enabled=true 但 callback_secret 为空。"
            f"请运行 init wizard 自动生成"
        )

    if cfg.tls_enabled:
        if not Path(cfg.cert_path).exists():
            errors.append(
                f"TLS 已启用但证书不存在：{cfg.cert_path}\n"
                f"  请运行 `python3 scripts/gen_cert.py --san auto` 生成"
            )
        if not Path(cfg.key_path).exists():
            errors.append(f"TLS 已启用但私钥不存在：{cfg.key_path}")

    return errors


def print_startup_info(cfg: TLSAuthConfig, skill_name: str) -> None:
    """启动时打印用户可见的密钥位置（不打印密钥本身）。"""
    print()
    print("=" * 60)
    print(f"  🔐 鉴权配置（{skill_name}）")
    print("=" * 60)
    print(f"  TLS         : {'✅ 已启用（HTTPS）' if cfg.tls_enabled else 'ℹ️  未启用（HTTP 模式）'}")
    print(f"  API Key     : ✅ 已设置（{len(cfg.api_key)} 位）")
    print(f"  Callback Auth: {'✅ 已启用' if cfg.callback_auth_enabled else '❌ 未启用'}")
    print()
    print("  📂 密钥/证书路径（可随时查回）：")
    if cfg.tls_enabled:
        print(f"     证书 : {cfg.cert_path}")
        print(f"     私钥 : {cfg.key_path}")
    print(f"     APIKey: {API_KEYS_DIR / (skill_name + '.key')}")
    if cfg.callback_auth_enabled:
        print(f"     HMAC : {SECRETS_DIR / (skill_name + '.hmac')}")
    print()
    print("  💡 客户端调用示例：")
    proto = "https" if cfg.tls_enabled else "http"
    print(f"     curl -H '{cfg.api_key_header}: <api-key>' \\")
    if cfg.tls_enabled:
        print(f"          --cacert {cfg.cert_path} \\")
    print(f"          {proto}://<your-host>:<port>/health")
    print("=" * 60)
    print()
