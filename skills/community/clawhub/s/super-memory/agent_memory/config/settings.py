"""
统一配置层 — 聚合所有配置源（环境变量 > JSON 配置文件 > 默认值）

使用方式:
    from config.settings import settings

    # 获取配置值
    db_path = settings.get("database.path")
    api_key = settings.get("llm.openai_api_key")

    # 获取子配置对象
    mcp = settings.mcp_config
    smart = settings.smart_config

    # 重新加载环境变量
    settings.reload()
"""
from __future__ import annotations

import os
import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# 项目根目录
_ROOT = Path(__file__).resolve().parent.parent


class Settings:
    """
    统一配置管理器。

    配置优先级：环境变量 > JSON 配置文件 > 代码默认值

    聚合的配置域：
    - database: 数据库路径、连接参数
    - llm: LLM API 配置（OpenAI/SiliconFlow/自定义）
    - embedding: 向量嵌入配置
    - mcp: MCP Server 配置
    - smart: 智能记忆配置
    - tier: 冷热分层配置
    - auth: 认证配置
    - logging: 日志配置
    - compliance: 合规配置
    - server: Web/gRPC Server 配置
    - connection: 连接池与缓存
    - rate_limit: 速率限制
    - monitoring: 监控告警阈值
    - queue: 队列配置
    - distributed: 分布式集群配置
    - backup: 备份配置
    - misc: 杂项
    """

    _PROFILES: dict[str, dict[str, Any]] = {
        "dev": {
            "database.path": ":memory:",
            "logging.level": "DEBUG",
            "backup.encryption": False,
            "compliance.mode": "off",
            "cost.llm_daily_call_limit": 1000,
        },
        "prod": {
            "logging.level": "INFO",
            "backup.encryption": True,
            "compliance.mode": "gdpr",
            "cost.llm_daily_call_limit": 500,
            "auth.allow_insecure": False,
        },
    }

    _DEFAULTS: dict[str, Any] = {
        # ── 原有配置 ──────────────────────────────────
        "database.path": str(_ROOT / "memory.db"),
        "database.max_memories": 0,
        "llm.function": "openai",
        "llm.openai_api_key": "",
        "llm.openai_base_url": "https://api.openai.com/v1",
        "llm.openai_model": "gpt-4o-mini",
        "llm.siliconflow_api_key": "",
        "llm.siliconflow_base_url": "https://api.siliconflow.cn/v1",
        "llm.siliconflow_model": "Qwen/Qwen2.5-72B-Instruct",
        "llm.custom_api_key": "",
        "llm.custom_base_url": "",
        "llm.custom_model": "",
        "embedding.backend": "local",
        "embedding.model": "",
        "embedding.dim": 0,
        "embedding.hf_endpoint": "https://hf-mirror.com",
        "server.web_port": 8080,
        "server.admin_password": "",
        "auth.jwt_secret": "",
        "auth.token_expiry": 3600,
        "auth.allow_insecure": False,
        "logging.level": "INFO",
        "logging.file": "",
        "compliance.mode": "tag",
        "metrics.prefix": "agent_memory",
        "causal.window_sec": 3600,
        "data_dir": os.path.expanduser("~/.agent_memory"),

        # ── Connection & Pool ─────────────────────────
        "connection.db_pool_size": 5,
        "connection.cache_ttl": 300,

        # ── Rate Limiting ─────────────────────────────
        "rate_limit.window": 60,
        "rate_limit.cleanup_interval": 100,

        # ── Monitoring / Alerting ──────────────────────
        "monitoring.alert_cpu_threshold": 80.0,
        "monitoring.alert_memory_threshold": 85.0,
        "monitoring.alert_disk_threshold": 90.0,

        # ── Queue ──────────────────────────────────────
        "queue.event_queue_size": 4096,
        "queue.message_queue_size": 4096,

        # ── Distributed ────────────────────────────────
        "distributed.virtual_nodes": 256,
        "distributed.search_timeout": 5.0,
        "distributed.search_workers": 8,
        "distributed.hnsw_rebuild_threshold": 100,

        # ── Backup ─────────────────────────────────────
        "backup.interval_hours": 24,
        "backup.encryption": True,

        # ── Misc ───────────────────────────────────────
        "misc.max_content_length": 50000,
        "misc.export_batch_size": 1000,
        "misc.max_json_depth": 20,

        # ── Cost Control ───────────────────────────────
        "cost.llm_daily_call_limit": 500,
        "cost.llm_daily_cost_limit_usd": 5.0,
        "cost.compress_llm_budget": 10,
        "cost.causal_analysis_interval": 10,
        "cost.vacuum_allowed_hours": "1-5",
    }

    # 环境变量映射: config_key -> env_var_name
    _ENV_MAP: dict[str, str] = {
        # ── 原有映射 ──────────────────────────────────
        "database.path": "AGENT_MEMORY_DB_PATH",
        "database.max_memories": "AGENT_MEMORY_MAX_MEMORIES",
        "llm.function": "LLM_FUNCTION",
        "llm.openai_api_key": "OPENAI_API_KEY",
        "llm.openai_base_url": "OPENAI_BASE_URL",
        "llm.openai_model": "OPENAI_MODEL",
        "llm.siliconflow_api_key": "SILICONFLOW_API_KEY",
        "llm.siliconflow_base_url": "SILICONFLOW_BASE_URL",
        "llm.siliconflow_model": "SILICONFLOW_MODEL",
        "llm.custom_api_key": "CUSTOM_LLM_API_KEY",
        "llm.custom_base_url": "CUSTOM_LLM_BASE_URL",
        "llm.custom_model": "CUSTOM_LLM_MODEL",
        "embedding.backend": "AGENT_MEMORY_EMBEDDING_BACKEND",
        "embedding.model": "AGENT_MEMORY_EMBEDDING_MODEL",
        "embedding.dim": "AGENT_MEMORY_EMBEDDING_DIM",
        "embedding.hf_endpoint": "HF_ENDPOINT",
        "server.web_port": "AGENT_MEMORY_WEB_PORT",
        "server.admin_password": "AGENT_MEMORY_ADMIN_PASSWORD",
        "auth.jwt_secret": "AGENT_MEMORY_JWT_SECRET",
        "auth.token_expiry": "AGENT_MEMORY_TOKEN_EXPIRY",
        "auth.allow_insecure": "AGENT_MEMORY_ALLOW_INSECURE",
        "logging.level": "AGENT_MEMORY_LOG_LEVEL",
        "logging.file": "LOG_FILE",
        "compliance.mode": "AGENT_MEMORY_COMPLIANCE_MODE",
        "metrics.prefix": "AGENT_MEMORY_METRICS_PREFIX",
        "causal.window_sec": "AGENT_MEMORY_CAUSAL_WINDOW_SEC",
        "data_dir": "AGENT_MEMORY_DATA_DIR",

        # ── Connection & Pool ─────────────────────────
        "connection.db_pool_size": "AGENT_MEMORY_DB_POOL_SIZE",
        "connection.cache_ttl": "AGENT_MEMORY_CACHE_TTL",

        # ── Rate Limiting ─────────────────────────────
        "rate_limit.window": "AGENT_MEMORY_RATE_LIMIT_WINDOW",
        "rate_limit.cleanup_interval": "AGENT_MEMORY_RATE_LIMIT_CLEANUP_INTERVAL",

        # ── Monitoring / Alerting ──────────────────────
        "monitoring.alert_cpu_threshold": "AGENT_MEMORY_ALERT_CPU_THRESHOLD",
        "monitoring.alert_memory_threshold": "AGENT_MEMORY_ALERT_MEMORY_THRESHOLD",
        "monitoring.alert_disk_threshold": "AGENT_MEMORY_ALERT_DISK_THRESHOLD",

        # ── Queue ──────────────────────────────────────
        "queue.event_queue_size": "AGENT_MEMORY_EVENT_QUEUE_SIZE",
        "queue.message_queue_size": "AGENT_MEMORY_MESSAGE_QUEUE_SIZE",

        # ── Distributed ────────────────────────────────
        "distributed.virtual_nodes": "AGENT_MEMORY_VIRTUAL_NODES",
        "distributed.search_timeout": "AGENT_MEMORY_SEARCH_TIMEOUT",
        "distributed.search_workers": "AGENT_MEMORY_SEARCH_WORKERS",
        "distributed.hnsw_rebuild_threshold": "AGENT_MEMORY_HNSW_REBUILD_THRESHOLD",

        # ── Backup ─────────────────────────────────────
        "backup.interval_hours": "AGENT_MEMORY_BACKUP_INTERVAL_HOURS",
        "backup.encryption": "AGENT_MEMORY_BACKUP_ENCRYPTION",

        # ── Misc ───────────────────────────────────────
        "misc.max_content_length": "AGENT_MEMORY_MAX_CONTENT_LENGTH",
        "misc.export_batch_size": "AGENT_MEMORY_EXPORT_BATCH_SIZE",
        "misc.max_json_depth": "AGENT_MEMORY_MAX_JSON_DEPTH",

        # ── Cost Control ───────────────────────────────
        "cost.llm_daily_call_limit": "AGENT_MEMORY_COST_LLM_DAILY_CALL_LIMIT",
        "cost.llm_daily_cost_limit_usd": "AGENT_MEMORY_COST_LLM_DAILY_COST_LIMIT_USD",
        "cost.compress_llm_budget": "AGENT_MEMORY_COST_COMPRESS_LLM_BUDGET",
        "cost.causal_analysis_interval": "AGENT_MEMORY_COST_CAUSAL_ANALYSIS_INTERVAL",
        "cost.vacuum_allowed_hours": "AGENT_MEMORY_COST_VACUUM_ALLOWED_HOURS",
    }

    # 整数类型的配置键
    _INT_KEYS: frozenset[str] = frozenset({
        "database.max_memories", "server.web_port", "auth.token_expiry",
        "embedding.dim", "causal.window_sec",
        "connection.db_pool_size", "connection.cache_ttl",
        "rate_limit.window", "rate_limit.cleanup_interval",
        "queue.event_queue_size", "queue.message_queue_size",
        "distributed.virtual_nodes", "distributed.search_workers",
        "distributed.hnsw_rebuild_threshold",
        "backup.interval_hours",
        "misc.max_content_length", "misc.export_batch_size",
        "misc.max_json_depth",
        "cost.llm_daily_call_limit", "cost.compress_llm_budget",
        "cost.causal_analysis_interval",
    })

    # 浮点类型的配置键
    _FLOAT_KEYS: frozenset[str] = frozenset({
        "monitoring.alert_cpu_threshold",
        "monitoring.alert_memory_threshold",
        "monitoring.alert_disk_threshold",
        "distributed.search_timeout",
        "cost.llm_daily_cost_limit_usd",
    })

    # 布尔类型的配置键
    _BOOL_KEYS: frozenset[str] = frozenset({
        "auth.allow_insecure",
        "backup.encryption",
    })

    # 字符串类型但空值不应转为 False 的键
    _STRING_KEYS_ALLOW_EMPTY: frozenset[str] = frozenset({
        "llm.openai_api_key", "llm.siliconflow_api_key",
        "llm.custom_api_key", "server.admin_password",
        "logging.file",
    })

    def __init__(self, config_file: str | Path | None = None):
        self._config_file = Path(config_file) if config_file else None
        self._file_config: dict[str, Any] = {}
        self._overrides: dict[str, Any] = {}

        # 延迟加载的子配置
        self._mcp_config = None
        self._smart_config = None

        # 加载 JSON 配置文件
        if self._config_file and self._config_file.exists():
            self._load_file()

        # Apply profile from AGENT_MEMORY_PROFILE env var
        profile = os.environ.get("AGENT_MEMORY_PROFILE", "")
        if profile:
            self.apply_profile(profile)

    def _load_file(self):
        """从 JSON 文件加载配置"""
        try:
            with open(self._config_file, "r", encoding="utf-8") as f:
                self._file_config = json.load(f)
            logger.info("Settings loaded from %s", self._config_file)
        except Exception as e:
            logger.warning("Settings: failed to load %s: %s", self._config_file, e)

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值。

        优先级：覆盖值 > 环境变量 > JSON 文件 > 默认值

        Args:
            key: 点号分隔的配置键，如 "database.path"
            default: 所有源都未设置时的回退值
        """
        # 1. 覆盖值（运行时 set() 设置的）
        if key in self._overrides:
            return self._overrides[key]

        # 2. 环境变量
        env_var = self._ENV_MAP.get(key)
        if env_var:
            env_val = os.environ.get(env_var)
            if env_val is not None:
                return self._cast(key, env_val)

        # 3. JSON 文件
        file_val = self._get_nested(self._file_config, key)
        if file_val is not None:
            return file_val

        # 4. 默认值
        if key in self._DEFAULTS:
            return self._DEFAULTS[key]

        return default

    def set(self, key: str, value: Any):
        """运行时覆盖配置值"""
        self._overrides[key] = value

    def apply_profile(self, profile_name: str):
        """Apply a configuration profile.

        Profile values are only applied if the key has not been explicitly
        set via environment variables, JSON config, or runtime overrides.
        """
        if profile_name not in self._PROFILES:
            logger.warning("Unknown configuration profile: %s", profile_name)
            return
        for key, value in self._PROFILES[profile_name].items():
            # Don't override explicit settings
            if self.get(key) is None or self.get(key) == self._DEFAULTS.get(key):
                self._overrides.setdefault(key, value)
        logger.info("Applied configuration profile: %s", profile_name)

    def reload(self):
        """重新从环境变量和配置文件加载配置（清除运行时覆盖）。"""
        self._overrides.clear()
        self._file_config.clear()
        if self._config_file and self._config_file.exists():
            self._load_file()
        # 重置延迟加载的子配置
        self._mcp_config = None
        self._smart_config = None
        logger.info("Settings reloaded from environment and config file")

    def _cast(self, key: str, value: str) -> Any:
        """将环境变量字符串转换为适当类型"""
        # 布尔值
        if key in self._BOOL_KEYS:
            return value.lower() in ("true", "1", "yes")

        if value.lower() in ("true", "1", "yes"):
            return True
        if value.lower() in ("false", "0", "no", ""):
            if value == "" and key in self._STRING_KEYS_ALLOW_EMPTY:
                return value
            return False

        # 浮点数
        if key in self._FLOAT_KEYS:
            try:
                return float(value)
            except ValueError:
                logger.warning("配置项 %s 的值 '%s' 不是有效浮点数，保留原始字符串", key, value)
                return value

        # 整数
        if key in self._INT_KEYS:
            try:
                return int(value)
            except ValueError:
                logger.warning("配置项 %s 的值 '%s' 不是有效整数，保留原始字符串", key, value)
                return value

        return value

    @staticmethod
    def _get_nested(data: dict, key: str) -> Any:
        """从嵌套字典中获取值"""
        keys = key.split(".")
        current = data
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return None
        return current

    # ── 子配置对象访问 ──────────────────────────────

    @property
    def mcp_config(self):
        """获取 MCPConfig 实例（延迟加载）"""
        if self._mcp_config is None:
            from ..mcp_config import MCPConfig
            self._mcp_config = MCPConfig.from_env()
        return self._mcp_config

    @property
    def smart_config(self):
        """获取 SmartConfig 实例（延迟加载）"""
        if self._smart_config is None:
            from ..smart_config import SmartConfig
            self._smart_config = SmartConfig()
        return self._smart_config

    # ── 便捷属性 ──────────────────────────────────

    @property
    def db_path(self) -> str:
        return self.get("database.path")

    @property
    def llm_api_key(self) -> str:
        func = self.get("llm.function", "openai")
        if func == "siliconflow":
            return self.get("llm.siliconflow_api_key", "")
        elif func == "custom":
            return self.get("llm.custom_api_key", "")
        return self.get("llm.openai_api_key", "")

    @property
    def llm_base_url(self) -> str:
        func = self.get("llm.function", "openai")
        if func == "siliconflow":
            return self.get("llm.siliconflow_base_url", "https://api.siliconflow.cn/v1")
        elif func == "custom":
            return self.get("llm.custom_base_url", "")
        return self.get("llm.openai_base_url", "https://api.openai.com/v1")

    @property
    def llm_model(self) -> str:
        func = self.get("llm.function", "openai")
        if func == "siliconflow":
            return self.get("llm.siliconflow_model", "Qwen/Qwen2.5-72B-Instruct")
        elif func == "custom":
            return self.get("llm.custom_model", "")
        return self.get("llm.openai_model", "gpt-4o-mini")

    @property
    def embedding_backend(self) -> str:
        return self.get("embedding.backend", "local")

    @property
    def log_level(self) -> str:
        return self.get("logging.level", "INFO")

    # ── 新增便捷属性 ──────────────────────────────

    @property
    def db_pool_size(self) -> int:
        return self.get("connection.db_pool_size", 5)

    @property
    def cache_ttl(self) -> int:
        return self.get("connection.cache_ttl", 300)

    @property
    def rate_limit_window(self) -> int:
        return self.get("rate_limit.window", 60)

    @property
    def alert_cpu_threshold(self) -> float:
        return self.get("monitoring.alert_cpu_threshold", 80.0)

    @property
    def alert_memory_threshold(self) -> float:
        return self.get("monitoring.alert_memory_threshold", 85.0)

    @property
    def alert_disk_threshold(self) -> float:
        return self.get("monitoring.alert_disk_threshold", 90.0)

    @property
    def event_queue_size(self) -> int:
        return self.get("queue.event_queue_size", 4096)

    @property
    def message_queue_size(self) -> int:
        return self.get("queue.message_queue_size", 4096)

    @property
    def virtual_nodes(self) -> int:
        return self.get("distributed.virtual_nodes", 256)

    @property
    def search_timeout(self) -> float:
        return self.get("distributed.search_timeout", 5.0)

    @property
    def search_workers(self) -> int:
        return self.get("distributed.search_workers", 8)

    @property
    def backup_interval_hours(self) -> int:
        return self.get("backup.interval_hours", 24)

    @property
    def backup_encryption(self) -> bool:
        return self.get("backup.encryption", True)

    @property
    def max_content_length(self) -> int:
        return self.get("misc.max_content_length", 50000)

    @property
    def export_batch_size(self) -> int:
        return self.get("misc.export_batch_size", 1000)

    @property
    def max_json_depth(self) -> int:
        return self.get("misc.max_json_depth", 20)

    def to_dict(self) -> dict[str, Any]:
        """导出所有配置为字典（隐藏敏感值）"""
        result = {}
        for key in self._DEFAULTS:
            value = self.get(key)
            # 隐藏敏感值
            if any(s in key for s in ("api_key", "password", "secret", "jwt")):
                value = "***" if value else ""
            result[key] = value
        return result

    def __repr__(self) -> str:
        return f"Settings(file={self._config_file}, overrides={len(self._overrides)})"


# 全局单例
settings = Settings()
