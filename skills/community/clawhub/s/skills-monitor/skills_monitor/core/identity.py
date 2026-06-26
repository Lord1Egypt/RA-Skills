"""
本地身份管理模块 v0.5.0
- 生成唯一 agent_id (UUID v4)
- 生成/验证 API Key (HMAC-SHA256)
- OS Keychain 安全存储 (keyring 优先，文件降级)
- API Key 生命周期管理 (轮换/撤销/TTL)
- 配置文件持久化 (~/.skills_monitor/config.json)
"""

import hashlib
import hmac
import json
import logging
import os
import secrets
import stat
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

def _default_home_dir() -> str:
    """
    允许通过环境变量重定向所有本地持久化目录，便于 CI/容器/沙盒运行。
    """
    return os.path.expanduser(os.environ.get("SKILLS_MONITOR_HOME", "~/.skills_monitor"))


DEFAULT_CONFIG_DIR = _default_home_dir()
CONFIG_FILE = "config.json"

DEFAULT_KEY_TTL_DAYS = 90
KEY_EXPIRY_WARNING_DAYS = 7
GRACE_PERIOD_HOURS = 24
MAX_ACTIVE_KEYS = 2


def _ensure_config_dir(config_dir: str = DEFAULT_CONFIG_DIR) -> Path:
    path = Path(config_dir)
    path.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(str(path), stat.S_IRWXU)
    except OSError:
        pass
    return path


def generate_agent_id() -> str:
    return str(uuid.uuid4())


def generate_api_key(agent_id: str, secret: Optional[str] = None) -> str:
    if secret is None:
        secret = secrets.token_hex(16)
    sig = hmac.new(secret.encode(), agent_id.encode(), hashlib.sha256).hexdigest()
    return f"sk-{sig[:32]}"


def hash_api_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode()).hexdigest()


def verify_api_key(api_key: str, stored_hash: str) -> bool:
    return hmac.compare_digest(hash_api_key(api_key), stored_hash)


class IdentityManager:
    """身份管理器 v0.5.0 — Keychain 集成 + Key 生命周期"""

    def __init__(self, config_dir: str = DEFAULT_CONFIG_DIR):
        self.config_dir = _ensure_config_dir(config_dir)
        self.config_path = self.config_dir / CONFIG_FILE
        self._config: Dict[str, Any] = {}
        self._secure_store = None
        self._load()
        self._init_secure_store()

    def _init_secure_store(self):
        try:
            from skills_monitor.core.secure_store import SecureStore
            self._secure_store = SecureStore()
        except Exception as e:
            logger.warning(f"SecureStore 初始化失败: {e}")
            self._secure_store = None

    def _load(self):
        if self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as f:
                self._config = json.load(f)

    def _save(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self._config, f, ensure_ascii=False, indent=2)
        try:
            os.chmod(str(self.config_path), stat.S_IRUSR | stat.S_IWUSR)
        except OSError:
            pass

    @property
    def is_initialized(self) -> bool:
        return bool(self._config.get("agent_id"))

    @property
    def agent_id(self) -> Optional[str]:
        return self._config.get("agent_id")

    @property
    def api_key(self) -> Optional[str]:
        """从 Keychain 读取 API Key（降级返回 None）"""
        if self._secure_store:
            return self._secure_store.get_credential("api_key")
        return None

    # ──────── 初始化 ────────

    def initialize(self, force: bool = False, ttl_days: int = DEFAULT_KEY_TTL_DAYS) -> Dict[str, str]:
        """首次初始化：生成 agent_id + api_key，存入 Keychain"""
        if self.is_initialized and not force:
            return {
                "agent_id": self._config["agent_id"],
                "api_key": "(已初始化，API Key 仅首次显示)",
                "status": "already_initialized",
            }

        agent_id = generate_agent_id()
        api_key = generate_api_key(agent_id, secrets.token_hex(16))
        now = datetime.now()
        expires_at = (now + timedelta(days=ttl_days)).isoformat() if ttl_days > 0 else None

        self._config = {
            "agent_id": agent_id,
            "api_key_hash": hash_api_key(api_key),
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
            "skills_dir": "",
            "settings": {
                "auto_collect": True,
                "buffer_size": 100,
                "flush_interval_seconds": 60,
            },
            "key_lifecycle": {
                "version": 1,
                "keys": [{
                    "hash": hash_api_key(api_key),
                    "version": 1,
                    "created_at": now.isoformat(),
                    "expires_at": expires_at,
                    "status": "active",
                }],
            },
            "consent": {"data_collection_agreed": False, "agreed_at": None},
        }
        self._save()

        # 存入安全存储
        if self._secure_store:
            self._secure_store.store_credential("api_key", api_key)
            self._secure_store.store_credential("agent_id", agent_id)

        return {
            "agent_id": agent_id,
            "api_key": api_key,
            "status": "initialized",
            "config_path": str(self.config_path),
            "key_expires_at": expires_at,
            "secure_store": self._secure_store.backend_name if self._secure_store else "none",
        }

    # ──────── 验证 ────────

    def verify(self, api_key: str) -> bool:
        """验证 API Key（支持多 Key + 过期检测）"""
        lifecycle = self._config.get("key_lifecycle", {})
        keys = lifecycle.get("keys", [])

        if not keys:
            # 向后兼容 v0.4.0
            return verify_api_key(api_key, self._config.get("api_key_hash", ""))

        api_hash = hash_api_key(api_key)
        now = datetime.now()
        changed = False

        for entry in keys:
            if entry["status"] not in ("active", "grace_period"):
                continue
            # 检查过期
            exp = entry.get("expires_at")
            if exp:
                try:
                    if now > datetime.fromisoformat(exp):
                        entry["status"] = "expired"
                        changed = True
                        continue
                except ValueError:
                    pass
            if hmac.compare_digest(entry.get("hash", ""), api_hash):
                if changed:
                    self._save()
                return True

        if changed:
            self._save()
        return False

    # ──────── Key 轮换 ────────

    def rotate_key(self, ttl_days: int = DEFAULT_KEY_TTL_DAYS) -> Dict[str, str]:
        """生成新 Key，旧 Key 进入宽限期（24h）"""
        if not self.is_initialized:
            raise RuntimeError("Agent 未初始化")

        now = datetime.now()
        lifecycle = self._config.setdefault("key_lifecycle", {"keys": [], "version": 0})
        keys = lifecycle.setdefault("keys", [])

        # 旧 Key 标记为宽限期
        grace_until = (now + timedelta(hours=GRACE_PERIOD_HOURS)).isoformat()
        for entry in keys:
            if entry["status"] == "active":
                entry["status"] = "grace_period"
                entry["grace_until"] = grace_until

        # 生成新 Key
        new_version = lifecycle.get("version", 0) + 1
        new_key = generate_api_key(self.agent_id, secrets.token_hex(16))
        expires_at = (now + timedelta(days=ttl_days)).isoformat() if ttl_days > 0 else None

        keys.append({
            "hash": hash_api_key(new_key),
            "version": new_version,
            "created_at": now.isoformat(),
            "expires_at": expires_at,
            "status": "active",
        })

        # 限制最多保留 MAX_ACTIVE_KEYS 个非 revoked key
        active_keys = [k for k in keys if k["status"] in ("active", "grace_period")]
        if len(active_keys) > MAX_ACTIVE_KEYS:
            for k in active_keys[:-MAX_ACTIVE_KEYS]:
                k["status"] = "revoked"

        lifecycle["version"] = new_version
        self._config["api_key_hash"] = hash_api_key(new_key)
        self._config["updated_at"] = now.isoformat()
        self._save()

        if self._secure_store:
            self._secure_store.store_credential("api_key", new_key)

        return {
            "new_api_key": new_key,
            "key_version": new_version,
            "expires_at": expires_at,
            "old_key_status": "grace_period",
            "grace_until": grace_until,
        }

    # ──────── Key 撤销 ────────

    def revoke_key(self, key_version: int = None) -> Dict[str, Any]:
        """立即撤销指定版本的 Key（默认撤销当前所有 Key）"""
        lifecycle = self._config.get("key_lifecycle", {})
        keys = lifecycle.get("keys", [])
        revoked = 0

        for entry in keys:
            if entry["status"] in ("active", "grace_period"):
                if key_version is None or entry.get("version") == key_version:
                    entry["status"] = "revoked"
                    entry["revoked_at"] = datetime.now().isoformat()
                    revoked += 1

        self._config["updated_at"] = datetime.now().isoformat()
        self._save()

        if self._secure_store and key_version is None:
            self._secure_store.delete_credential("api_key")

        return {"revoked_count": revoked, "status": "all_keys_revoked" if key_version is None else "key_revoked"}

    # ──────── Key 状态检查 ────────

    def check_key_health(self) -> Dict[str, Any]:
        """检查 Key 健康状态（过期提醒等）"""
        lifecycle = self._config.get("key_lifecycle", {})
        keys = lifecycle.get("keys", [])
        now = datetime.now()
        warnings = []
        active_count = 0

        for entry in keys:
            if entry["status"] == "active":
                active_count += 1
                exp = entry.get("expires_at")
                if exp:
                    try:
                        exp_dt = datetime.fromisoformat(exp)
                        days_left = (exp_dt - now).days
                        if days_left <= 0:
                            warnings.append(f"Key v{entry.get('version')} 已过期！")
                            entry["status"] = "expired"
                        elif days_left <= KEY_EXPIRY_WARNING_DAYS:
                            warnings.append(f"Key v{entry.get('version')} 将在 {days_left} 天后过期")
                    except ValueError:
                        pass

        if warnings:
            self._save()

        return {
            "active_keys": active_count,
            "total_keys": len(keys),
            "warnings": warnings,
            "healthy": len(warnings) == 0 and active_count > 0,
            "secure_store": self._secure_store.backend_name if self._secure_store else "none",
        }

    # ──────── GDPR 同意记录 ────────

    def record_consent(self, agreed: bool = True):
        """记录用户数据收集同意"""
        consent = self._config.setdefault("consent", {})
        consent["data_collection_agreed"] = agreed
        consent["agreed_at"] = datetime.now().isoformat() if agreed else None
        self._config["updated_at"] = datetime.now().isoformat()
        self._save()

    def has_consent(self) -> bool:
        """检查用户是否已同意数据收集"""
        return self._config.get("consent", {}).get("data_collection_agreed", False)

    # ──────── 原有方法 ────────

    def update_settings(self, **kwargs):
        settings = self._config.setdefault("settings", {})
        settings.update(kwargs)
        self._config["updated_at"] = datetime.now().isoformat()
        self._save()

    def set_skills_dir(self, skills_dir: str):
        self._config["skills_dir"] = str(skills_dir)
        self._config["updated_at"] = datetime.now().isoformat()
        self._save()

    def get_config(self) -> Dict[str, Any]:
        """获取当前配置（脱敏 — 不含 hash/key）"""
        cfg = dict(self._config)
        cfg.pop("api_key_hash", None)
        lifecycle = cfg.get("key_lifecycle", {})
        for k in lifecycle.get("keys", []):
            k.pop("hash", None)
        return cfg
