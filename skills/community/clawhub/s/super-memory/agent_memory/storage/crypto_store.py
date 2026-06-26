"""加密存储代理层 — 对敏感记忆内容做透明加解密

CryptoStore 代理 MemoryStore，在写入时自动加密标记为 confidential/private 的
记忆 content 字段，在读取时自动解密。其他字段（memory_id, importance 等）不受影响。

加密方案:
    - 使用 cryptography.fernet.Fernet 对称加密（AES-128-CBC + HMAC-SHA256）
    - 加密内容以 base64 编码存储，前缀 "ENC:" 标识
    - 密钥来源优先级: 环境变量 AGENT_MEMORY_ENCRYPTION_KEY > .encryption_key 文件

加密触发条件:
    - importance == "confidential"
    - sensitivity >= 4（即 sensitivity 为 "private"）

降级策略:
    - 如果 cryptography 未安装，CryptoStore 降级为透传模式，打印 warning
    - 如果 AGENT_MEMORY_ENCRYPTION_STRICT=true（默认），加密失败时对敏感内容抛出 ValueError
    - 如果 AGENT_MEMORY_ENCRYPTION_STRICT=false，允许降级为明文存储（不推荐）
"""

from __future__ import annotations

import base64
import logging
import os
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# ── Fernet 可用性检测 ──────────────────────────────────────────
try:
    from cryptography.fernet import Fernet
    _HAS_CRYPTO = True
except ImportError:
    _HAS_CRYPTO = False
    logger.warning(
        "crypto_store: cryptography 库未安装，CryptoStore 将降级为透传模式（不加密）。"
        "请运行 pip install cryptography 启用加密功能。"
    )

# ── 常量 ───────────────────────────────────────────────────────
_ENC_PREFIX = "ENC:"
_KEY_FILE = Path(__file__).parent / ".encryption_key"
_SENSITIVITY_LEVEL = {"public": 0, "normal": 1, "internal": 2, "confidential": 3, "private": 4}


class CryptoStore:
    """加密存储代理层 — 代理 MemoryStore，对敏感内容透明加解密。

    用法:
        store = MemoryStore(...)
        crypto_store = CryptoStore(store)

        # 正常使用，与 MemoryStore 接口一致
        crypto_store.insert_memory(...)
        results = crypto_store.query(...)
        # 返回结果中已加密的内容会自动解密
    """

    _SAFE_PROXY_ATTRS = frozenset({
        "conn", "db_path", "_has_fts", "_fts_mgr", "_agent_mgr",
        "get_stats", "count_memories", "get_schema_version",
        "create_indexes", "optimize", "vacuum", "rebuild_fts",
        "close", "close_all",
    })

    def __init__(self, store):
        """初始化 CryptoStore。

        Args:
            store: 被代理的 MemoryStore 实例
        """
        self._store = store
        self._fernet: Optional[Fernet] = None

        if _HAS_CRYPTO:
            self._fernet = self._init_fernet()

    @property
    def is_active(self) -> bool:
        """返回加密是否真正启用（Fernet 实例可用）。"""
        return self._fernet is not None

    @staticmethod
    def _is_strict_mode() -> bool:
        """检查是否为严格模式（默认 True）。

        环境变量 AGENT_MEMORY_ENCRYPTION_STRICT:
        - "false" / "0" / "no" → 非严格模式，允许降级为明文
        - 其他（包括未设置）→ 严格模式，敏感内容加密失败时抛出异常
        """
        val = os.environ.get("AGENT_MEMORY_ENCRYPTION_STRICT", "true").strip().lower()
        return val not in ("false", "0", "no")

    # ── 密钥管理 ───────────────────────────────────────────────

    def _init_fernet(self) -> Optional[Fernet]:
        """初始化 Fernet 实例，优先从环境变量获取密钥，其次从文件加载。"""
        key = self._load_key()
        if key is None:
            key = Fernet.generate_key()
            self._save_key(key)
            logger.info("crypto_store: 已生成新加密密钥并保存到 %s", _KEY_FILE)
        try:
            return Fernet(key)
        except Exception as e:
            logger.warning("crypto_store: 密钥无效，降级为透传模式: %s", e)
            return None

    def _load_key(self) -> Optional[bytes]:
        """从环境变量或密钥文件加载密钥。"""
        # 优先环境变量
        env_key = os.environ.get("AGENT_MEMORY_ENCRYPTION_KEY")
        if env_key:
            try:
                key = env_key.encode("utf-8") if isinstance(env_key, str) else env_key
                # 验证是否为合法的 Fernet 密钥
                Fernet(key)
                return key
            except Exception as e:
                logger.debug("Env key Fernet validation failed: %s", e)
                try:
                    padded = env_key + "=" * (-len(env_key) % 4)
                    key = padded.encode("utf-8")
                    Fernet(key)
                    return key
                except Exception as e:
                    logger.warning("crypto_store: 环境变量 AGENT_MEMORY_ENCRYPTION_KEY 无效: %s", e)

        # 其次从文件加载
        if _KEY_FILE.exists():
            try:
                key = _KEY_FILE.read_bytes().strip()
                Fernet(key)
                return key
            except Exception as e:
                logger.warning("crypto_store: 密钥文件 %s 无效: %s", _KEY_FILE, e)

        return None

    def _save_key(self, key: bytes) -> None:
        """将密钥保存到文件。"""
        try:
            _KEY_FILE.write_bytes(key)
            try:
                os.chmod(_KEY_FILE, 0o600)
            except (OSError, AttributeError):
                pass
        except OSError as e:
            logger.warning("crypto_store: 无法保存密钥文件 %s: %s", _KEY_FILE, e)

    # ── 加密判断 ───────────────────────────────────────────────

    @staticmethod
    def _needs_encrypt(memory: dict) -> bool:
        """判断记忆是否需要加密。

        条件: importance == "confidential" 或 sensitivity >= 4（即 "private"）
        """
        importance = memory.get("importance", "")
        if importance == "confidential":
            return True

        sensitivity = memory.get("sensitivity", "")
        level = _SENSITIVITY_LEVEL.get(sensitivity, 0)
        if level >= 4:
            return True

        return False

    @staticmethod
    def _is_encrypted(content: str) -> bool:
        """判断内容是否已加密（以 ENC: 前缀标识）。"""
        return isinstance(content, str) and content.startswith(_ENC_PREFIX)

    # ── 公开加解密方法 ─────────────────────────────────────────

    def encrypt_content(self, content: str, *, needs_encrypt: bool = False) -> str:
        """加密内容，返回 "ENC:" + base64 编码的密文。

        如果加密不可用或内容为空，返回原文。
        在严格模式下，如果内容需要加密（needs_encrypt=True）但加密不可用，抛出 ValueError。
        """
        if not content or self._fernet is None:
            if needs_encrypt and self._is_strict_mode() and content:
                raise ValueError(
                    "加密不可用但内容需要加密（importance=confidential 或 sensitivity>=4）。"
                    "请安装 cryptography 库或设置 AGENT_MEMORY_ENCRYPTION_STRICT=false 允许降级为明文。"
                )
            return content
        try:
            encrypted = self._fernet.encrypt(content.encode("utf-8"))
            return _ENC_PREFIX + encrypted.decode("utf-8")
        except Exception as e:
            if needs_encrypt:
                raise ValueError(
                    f"加密失败且内容需要加密: {e}。"
                    "敏感内容不允许以明文存储。"
                ) from e
            logger.warning("crypto_store: 加密失败，非敏感内容返回原文: %s", e)
            return content

    def decrypt_content(self, content: str) -> str:
        """解密内容，去除 "ENC:" 前缀后解码。

        如果内容不是加密格式或解密失败，返回原文。
        """
        if not self._is_encrypted(content) or self._fernet is None:
            return content
        try:
            encrypted_b64 = content[len(_ENC_PREFIX):]
            decrypted = self._fernet.decrypt(encrypted_b64.encode("utf-8"))
            return decrypted.decode("utf-8")
        except Exception as e:
            logger.warning("crypto_store: 解密失败，返回原文: %s", e)
            return content

    # ── 内部加解密辅助 ─────────────────────────────────────────

    def _encrypt_memory(self, memory: dict) -> dict:
        """如果记忆需要加密，加密其 content 字段。返回新 dict。

        严格模式下，如果内容需要加密但加密不可用，抛出 ValueError。
        """
        if not self._needs_encrypt(memory):
            return memory
        mem = dict(memory)
        content = mem.get("content", "")
        if content and not self._is_encrypted(content):
            mem["content"] = self.encrypt_content(content, needs_encrypt=True)
        return mem

    def _decrypt_memory(self, memory: dict) -> dict:
        """如果记忆的 content 已加密，解密之。返回新 dict。"""
        content = memory.get("content", "")
        if self._is_encrypted(content):
            mem = dict(memory)
            mem["content"] = self.decrypt_content(content)
            return mem
        return memory

    def _decrypt_memories(self, memories: list[dict]) -> list[dict]:
        """批量解密记忆列表。"""
        return [self._decrypt_memory(m) for m in memories]

    # ── 代理 MemoryStore 接口 ──────────────────────────────────

    def __getattr__(self, name):
        if name in self._SAFE_PROXY_ATTRS:
            return getattr(self._store, name)
        raise AttributeError(
            f"CryptoStore does not expose '{name}' to prevent bypassing encryption. "
            f"Use explicit CryptoStore methods instead."
        )

    def insert_memory(self, memory_id: str, time_id: str, time_ts: int,
                      person_id: str, nature_id: str, content: str,
                      content_hash: str, topics: list[str] = None,
                      tools: list[str] = None, knowledge_types: list[str] = None,
                      importance: str = "medium", **kwargs) -> str:
        """写入记忆 — 自动加密敏感内容。"""
        mem = {
            "memory_id": memory_id, "time_id": time_id, "time_ts": time_ts,
            "person_id": person_id, "nature_id": nature_id, "content": content,
            "content_hash": content_hash, "topics": topics or [],
            "tools": tools or [], "knowledge_types": knowledge_types or [],
            "importance": importance,
        }
        mem.update(kwargs)
        encrypted_mem = self._encrypt_memory(mem)

        return self._store.insert_memory(
            memory_id=encrypted_mem["memory_id"],
            time_id=encrypted_mem["time_id"],
            time_ts=encrypted_mem["time_ts"],
            person_id=encrypted_mem["person_id"],
            nature_id=encrypted_mem["nature_id"],
            content=encrypted_mem["content"],
            content_hash=encrypted_mem["content_hash"],
            topics=encrypted_mem["topics"],
            tools=encrypted_mem["tools"],
            knowledge_types=encrypted_mem["knowledge_types"],
            importance=encrypted_mem["importance"],
            **{k: v for k, v in encrypted_mem.items()
               if k not in {"memory_id", "time_id", "time_ts", "person_id",
                            "nature_id", "content", "content_hash", "topics",
                            "tools", "knowledge_types", "importance"}}
        )

    def get_memory(self, memory_id: str) -> dict | None:
        """获取单条记忆 — 自动解密。"""
        mem = self._store.get_memory(memory_id)
        if mem is None:
            return None
        return self._decrypt_memory(mem)

    def get_memories(self, memory_ids: list[str]) -> dict[str, dict]:
        """批量获取记忆 — 自动解密。"""
        results = self._store.get_memories(memory_ids)
        return {mid: self._decrypt_memory(m) for mid, m in results.items()}

    def query(self, *args, **kwargs) -> list[dict]:
        """查询记忆 — 返回结果自动解密。"""
        results = self._store.query(*args, **kwargs)
        return self._decrypt_memories(results)

    def update_memory(self, memory_id: str, **fields) -> dict:
        """更新记忆 — 如果包含 content 且需要加密，自动加密。"""
        if "content" in fields:
            # 需要判断该记忆是否需要加密
            existing = self._store.get_memory(memory_id)
            if existing:
                merged = dict(existing)
                merged.update(fields)
                if self._needs_encrypt(merged):
                    fields = dict(fields)
                    content = fields["content"]
                    if content and not self._is_encrypted(content):
                        fields["content"] = self.encrypt_content(content)
        return self._store.update_memory(memory_id, **fields)

    def search(self, keyword: str, limit: int = 50) -> list[dict]:
        """全文搜索 — 返回结果自动解密。"""
        results = self._store.search(keyword, limit)
        return self._decrypt_memories(results)

    # ── 生命周期代理 ───────────────────────────────────────────

    def close(self):
        return self._store.close()

    def create_indexes(self):
        return self._store.create_indexes()
