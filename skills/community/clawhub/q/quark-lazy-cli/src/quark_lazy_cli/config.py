"""配置管理：统一 env 加载和读取

用法：
    from quark_lazy_cli.config import get_settings, settings
    settings = get_settings()  # 懒加载，优先用这个
    # 或
    from quark_lazy_cli.config import settings  # 仅读属性，不触发初始化
"""
import os
from dotenv import load_dotenv

# 全局懒加载单例
_settings = None
_warned_keys: set = set()


def get_settings(env_path: str = None) -> "Config":
    """懒加载 Config 单例，首次调用时初始化。优先级：命令行 > 环境变量 > .env"""
    global _settings
    if env_path:
        load_dotenv(env_path, override=False)
    if _settings is None:
        _settings = Config()
    elif env_path:
        _settings = Config()
    _settings._check_all_defaults()
    return _settings


# 模块级懒加载 settings（触发 __init__ 时才 load_dotenv）
def __getattr__(name):
    global _settings
    if name == "settings":
        if _settings is None:
            _settings = Config()
        return _settings
    if _settings is None:
        _settings = Config()
    return getattr(_settings, name)


class Config:
    """配置类，属性为懒加载（属性本身才读 os.getenv，__init__ 不读）"""

    # 必填参数（无默认值，缺失则报错）
    _required = ["QAS_HOST", "QAS_API_TOKEN", "LAZY_CLI_LLM_OPENAI_API_KEY", "LAZY_CLI_LLM_OPENAI_API_BASE"]

    # 可选参数（带默认值）
    _defaults = {
        "LAZY_CLI_DEBUG": "false",
        "LAZY_CLI_ADVISOR": "human",
        "LAZY_CLI_EP_SELECTION_POLICY": "prefer_quality",
        "LAZY_CLI_SEARCH_EXPIRATION_DAYS": "7",
        "LAZY_CLI_MAX_SEARCH_BREADTH": "10",
        "LAZY_CLI_DRILL_MAX_DEPTH": "3",
        "LAZY_CLI_REPORT_DIR": "./report",
        "LAZY_CLI_LOG_DIR": "./logs",
        "LAZY_CLI_LLM_OPENAI_API_BASE": "",
        "LAZY_CLI_LLM_OPENAI_API_KEY": "",
        "LAZY_CLI_LLM_OPENAI_MODEL": "MiniMax-M2.7",
        "LAZY_CLI_LLM_TEMPERATURE": "0.4",
        "LAZY_CLI_AGENT_MSG_DIR": "./message",
        "LAZY_CLI_HUMAN_FILTER": "true",
        "LAZY_CLI_SEARCH_BATCH_DISP": "30",
        "LAZY_CLI_AGENT_POLL_INTERVAL": "15",
        "QAS_BRANCH": "",  # 未来功能，固定空，不显示 INFO
    }

    # 启动时不显示 INFO 的变量（未来功能/内部用）
    _hidden_keys = {"QAS_BRANCH"}

    def __init__(self, env_path: str = None):
        # 优先级：shell 环境变量 > --env 指定文件 > 默认 .env
        # shell 环境变量始终最高（override=False 保持已存在的值不变）
        if env_path:
            load_dotenv(env_path, override=False)
        elif os.path.exists(".env"):
            load_dotenv(".env", override=False)
        # 启动时一次性缓存所有变量，后续只读缓存
        self._cache = {}
        for key, default in self._defaults.items():
            self._cache[key] = os.getenv(key, default)

    def _check_all_defaults(self) -> None:
        """启动时 INFO：报告所有使用默认值且非隐藏的变量"""
        import sys
        for key, default in self._defaults.items():
            if key in self._hidden_keys:
                continue
            if key not in os.environ:
                sys.stderr.write(f"[Config] 环境变量 {key} 未设置，使用默认值: {default}\n")

    def get(self, key: str, default=None):
        return os.getenv(key, default)

    def check_missing(self) -> list:
        """返回缺失的必填参数名列表"""
        return [k for k in self._required if not os.getenv(k)]

    def _require(self, key: str, display_name: str) -> str:
        """必填 key 访问：为空则 ERROR"""
        v = os.getenv(key, "")
        if not v:
            raise RuntimeError(f"缺少环境变量 {key}（{display_name}）")
        return v

    def _using_default(self, key: str) -> bool:
        """检查环境变量是否使用了默认值（key 不在当前环境中）"""
        return key not in os.environ

    def _warn(self, key: str, default_val: str) -> None:
        global _warned_keys
        if key not in _warned_keys:
            _warned_keys.add(key)
            import sys
            sys.stderr.write(f"[Config] 环境变量 {key} 未设置，使用默认值: {default_val}\n")

    # QAS 核心
    @property
    def qas_host(self) -> str:
        return self._require("QAS_HOST", "QAS 服务地址")

    @property
    def qas_token(self) -> str:
        return self._require("QAS_API_TOKEN", "QAS API Token")

    # 常用配置
    @property
    def debug(self) -> bool:
        return self._cache.get("LAZY_CLI_DEBUG", "false").lower() == "true"

    @property
    def advisor(self) -> str:
        return self._cache.get("LAZY_CLI_ADVISOR", "human").lower()

    @property
    def ep_selection_policy(self) -> str:
        return self._cache.get("LAZY_CLI_EP_SELECTION_POLICY", "prefer_quality")

    @property
    def search_expiration_days(self) -> int:
        return int(self._cache.get("LAZY_CLI_SEARCH_EXPIRATION_DAYS", "7"))

    @property
    def max_search_breadth(self) -> int:
        return int(self._cache.get("LAZY_CLI_MAX_SEARCH_BREADTH", "10"))

    @property
    def drill_max_depth(self) -> int:
        return int(self._cache.get("LAZY_CLI_DRILL_MAX_DEPTH", "3"))

    @property
    def report_dir(self) -> str:
        return self._cache.get("LAZY_CLI_REPORT_DIR", "./report")

    @property
    def log_dir(self) -> str:
        return self._cache.get("LAZY_CLI_LOG_DIR", "./logs")

    @property
    def llm_api_base(self) -> str:
        v = self._cache.get("LAZY_CLI_LLM_OPENAI_API_BASE", "")
        if not v:
            raise RuntimeError("缺少环境变量 LAZY_CLI_LLM_OPENAI_API_BASE（llm 顾问必填）")
        return v.rstrip("/")

    @property
    def llm_api_key(self) -> str:
        v = self._cache.get("LAZY_CLI_LLM_OPENAI_API_KEY", "")
        if not v:
            raise RuntimeError("缺少环境变量 LAZY_CLI_LLM_OPENAI_API_KEY（llm 顾问必填）")
        return v

    @property
    def llm_model(self) -> str:
        return self._cache.get("LAZY_CLI_LLM_OPENAI_MODEL", "MiniMax-M2.7")

    @property
    def llm_temperature(self) -> float:
        return float(self._cache.get("LAZY_CLI_LLM_TEMPERATURE", "0.4"))

    @property
    def agent_msg_dir(self) -> str:
        return self._cache.get("LAZY_CLI_AGENT_MSG_DIR", "./message")

    @property
    def agent_poll_interval(self) -> int:
        return int(self._cache.get("LAZY_CLI_AGENT_POLL_INTERVAL", "15"))

    @property
    def human_filter(self) -> bool:
        return self._cache.get("LAZY_CLI_HUMAN_FILTER", "true").lower() == "true"

    @property
    def search_batch_disp(self) -> int:
        return int(self._cache.get("LAZY_CLI_SEARCH_BATCH_DISP", "30"))

    @property
    def qas_branch(self) -> str:
        return self._cache.get("QAS_BRANCH", "")
