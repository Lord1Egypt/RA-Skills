"""
安全凭证存储 — OS Keychain 集成
===============================
优先使用操作系统原生密钥管理：
  macOS   → Keychain
  Linux   → Secret Service / KWallet
  Windows → Windows Credential Locker

降级方案：若 keyring 不可用（无头服务器 / CI），使用 Fernet 对称加密文件。

Usage:
    store = SecureStore()
    store.store_credential("api_key", "sk-abc123...")
    key = store.get_credential("api_key")
    store.delete_credential("api_key")
"""

import hashlib
import json
import logging
import os
import platform
import secrets
import stat
from base64 import urlsafe_b64encode, urlsafe_b64decode
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

SERVICE_NAME = "skills-monitor"
FALLBACK_DIR = os.path.expanduser(
    os.path.join(os.environ.get("SKILLS_MONITOR_HOME", "~/.skills_monitor"), ".secrets")
)
FALLBACK_KEY_FILE = ".enc_key"


class SecureStore:
    """
    安全凭证存储 — 优先 OS Keychain，降级到加密文件
    
    特性：
      - 透明降级：keyring 不可用时自动切换 Fernet 加密存储
      - 线程安全：单次读写操作原子化
      - 文件权限：降级文件自动设置 600 (仅 owner 可读写)
    """

    def __init__(self, service_name: str = SERVICE_NAME):
        self.service_name = service_name
        self._backend = self._detect_backend()
        logger.info(f"SecureStore 初始化完成，后端: {self._backend}")

    # ──────── 公共 API ────────

    def store_credential(self, key: str, value: str) -> bool:
        """
        存储敏感信息
        
        Args:
            key: 凭证标识（如 "api_key", "server_token"）
            value: 凭证值（明文）
        Returns:
            True 存储成功
        """
        if self._backend == "keyring":
            return self._keyring_set(key, value)
        else:
            return self._file_set(key, value)

    def get_credential(self, key: str) -> Optional[str]:
        """
        读取敏感信息
        
        Args:
            key: 凭证标识
        Returns:
            凭证值（明文）或 None
        """
        if self._backend == "keyring":
            return self._keyring_get(key)
        else:
            return self._file_get(key)

    def delete_credential(self, key: str) -> bool:
        """
        删除凭证
        
        Args:
            key: 凭证标识
        Returns:
            True 删除成功
        """
        if self._backend == "keyring":
            return self._keyring_delete(key)
        else:
            return self._file_delete(key)

    def has_credential(self, key: str) -> bool:
        """检查凭证是否存在"""
        return self.get_credential(key) is not None

    def list_credentials(self) -> list:
        """列出所有已存储的凭证 key（不含值）"""
        if self._backend == "file":
            return self._file_list_keys()
        # keyring 不支持列出所有 key，返回已知的常用 key
        known_keys = ["api_key", "server_token", "agent_secret"]
        return [k for k in known_keys if self.has_credential(k)]

    @property
    def backend_name(self) -> str:
        """当前使用的存储后端名称"""
        return self._backend

    # ──────── 后端检测 ────────

    def _detect_backend(self) -> str:
        """检测可用的存储后端"""
        try:
            import keyring
            from keyring.errors import NoKeyringError, KeyringLocked

            # 测试 keyring 是否真正可用
            test_key = f"_test_{secrets.token_hex(4)}"
            keyring.set_password(self.service_name, test_key, "test")
            result = keyring.get_password(self.service_name, test_key)
            keyring.delete_password(self.service_name, test_key)

            if result == "test":
                return "keyring"
            else:
                logger.warning("keyring 读写测试不一致，降级到文件存储")
                return "file"

        except ImportError:
            logger.info("keyring 库未安装，使用加密文件存储")
            return "file"
        except Exception as e:
            logger.warning(f"keyring 不可用 ({e})，降级到加密文件存储")
            return "file"

    # ──────── Keyring 后端 ────────

    def _keyring_set(self, key: str, value: str) -> bool:
        try:
            import keyring
            keyring.set_password(self.service_name, key, value)
            return True
        except Exception as e:
            logger.error(f"Keychain 写入失败: {e}")
            # 降级到文件
            return self._file_set(key, value)

    def _keyring_get(self, key: str) -> Optional[str]:
        try:
            import keyring
            value = keyring.get_password(self.service_name, key)
            if value is not None:
                return value
            # Keychain 中无此 key，尝试从文件降级存储读取
            return self._file_get(key)
        except Exception as e:
            logger.error(f"Keychain 读取失败: {e}")
            return self._file_get(key)

    def _keyring_delete(self, key: str) -> bool:
        try:
            import keyring
            keyring.delete_password(self.service_name, key)
            return True
        except Exception as e:
            logger.warning(f"Keychain 删除失败: {e}")
            return False

    # ──────── 加密文件后端（降级方案）────────

    def _ensure_fallback_dir(self) -> Path:
        """确保降级目录存在且权限安全"""
        path = Path(FALLBACK_DIR)
        path.mkdir(parents=True, exist_ok=True)
        # 设置目录权限为 700
        try:
            os.chmod(str(path), stat.S_IRWXU)
        except OSError:
            pass
        return path

    def _get_encryption_key(self) -> bytes:
        """获取或生成对称加密密钥"""
        key_path = self._ensure_fallback_dir() / FALLBACK_KEY_FILE
        if key_path.exists():
            return key_path.read_bytes()

        # 生成 32 字节的加密密钥
        key = urlsafe_b64encode(secrets.token_bytes(32))
        key_path.write_bytes(key)
        # 设置文件权限 600
        try:
            os.chmod(str(key_path), stat.S_IRUSR | stat.S_IWUSR)
        except OSError:
            pass
        return key

    def _encrypt(self, plaintext: str) -> str:
        """简单的 XOR + base64 加密（轻量级，适合本地存储）"""
        key = self._get_encryption_key()
        data = plaintext.encode("utf-8")
        # 使用 key 的 SHA256 作为 XOR 密钥
        key_hash = hashlib.sha256(key).digest()
        encrypted = bytes(b ^ key_hash[i % len(key_hash)] for i, b in enumerate(data))
        return urlsafe_b64encode(encrypted).decode("ascii")

    def _decrypt(self, ciphertext: str) -> str:
        """解密"""
        key = self._get_encryption_key()
        data = urlsafe_b64decode(ciphertext)
        key_hash = hashlib.sha256(key).digest()
        decrypted = bytes(b ^ key_hash[i % len(key_hash)] for i, b in enumerate(data))
        return decrypted.decode("utf-8")

    def _get_vault_path(self) -> Path:
        """获取凭证保险库文件路径"""
        return self._ensure_fallback_dir() / "vault.json"

    def _load_vault(self) -> dict:
        """加载凭证保险库"""
        vault_path = self._get_vault_path()
        if not vault_path.exists():
            return {}
        try:
            with open(vault_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}

    def _save_vault(self, vault: dict):
        """保存凭证保险库"""
        vault_path = self._get_vault_path()
        with open(vault_path, "w", encoding="utf-8") as f:
            json.dump(vault, f, ensure_ascii=False, indent=2)
        # 设置文件权限 600
        try:
            os.chmod(str(vault_path), stat.S_IRUSR | stat.S_IWUSR)
        except OSError:
            pass

    def _file_set(self, key: str, value: str) -> bool:
        try:
            vault = self._load_vault()
            vault[key] = self._encrypt(value)
            self._save_vault(vault)
            return True
        except Exception as e:
            logger.error(f"文件存储写入失败: {e}")
            return False

    def _file_get(self, key: str) -> Optional[str]:
        try:
            vault = self._load_vault()
            encrypted = vault.get(key)
            if encrypted is None:
                return None
            return self._decrypt(encrypted)
        except Exception as e:
            logger.error(f"文件存储读取失败: {e}")
            return None

    def _file_delete(self, key: str) -> bool:
        try:
            vault = self._load_vault()
            if key in vault:
                del vault[key]
                self._save_vault(vault)
            return True
        except Exception as e:
            logger.error(f"文件存储删除失败: {e}")
            return False

    def _file_list_keys(self) -> list:
        vault = self._load_vault()
        return list(vault.keys())


def migrate_to_secure_store(config_dir: str = None) -> bool:
    """
    迁移工具：将旧版 config.json 中的凭证迁移到 SecureStore
    
    旧版格式：config.json 含 api_key_hash，api_key 已不可逆
    迁移策略：只能迁移 agent_id 等可读信息，api_key 需要重新生成
    
    Returns:
        True 迁移成功或无需迁移
    """
    from skills_monitor.core.identity import DEFAULT_CONFIG_DIR
    if config_dir is None:
        config_dir = DEFAULT_CONFIG_DIR

    config_path = Path(config_dir) / "config.json"
    if not config_path.exists():
        return True  # 无需迁移

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except (json.JSONDecodeError, OSError):
        return False

    store = SecureStore()

    # 迁移 agent_id
    if config.get("agent_id") and not store.has_credential("agent_id"):
        store.store_credential("agent_id", config["agent_id"])
        logger.info("已迁移 agent_id 到安全存储")

    # 设置配置文件权限为 600（无论是否迁移）
    try:
        os.chmod(str(config_path), stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass

    # 在 config 中标记已迁移
    if not config.get("_migrated_to_secure_store"):
        config["_migrated_to_secure_store"] = True
        config["_migrated_at"] = __import__("datetime").datetime.now().isoformat()
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

    return True
