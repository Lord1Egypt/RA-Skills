"""
ValU AI 配置加载模块
支持 YAML 配置文件和环境变量
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass, field


# 默认配置
DEFAULT_CONFIG = {
    "app": {
        "name": "ValU AI 智能估值分析器",
        "version": "2.0.0",
        "debug": False,
        "language": "zh_CN"
    },
    "deepseek": {
        "api_key": "",
        "api_url": "https://api.deepseek.com/v1/chat/completions",
        "model": "deepseek-chat",
        "timeout": 180,
        "max_retries": 3
    },
    "data_sources": {
        "baostock": {"enabled": True, "priority": 1},
        "akshare": {"enabled": True, "priority": 2},
        "tushare": {"enabled": False, "token": ""}
    },
    "pricing": {
        "free": {"quota_per_week": 2},
        "pay_per_use": {"price": 9.9},
        "batch": {"price": 29.9, "max_stocks": 5},
        "packages": {
            "starter": {"times": 10, "original_price": 99, "discount_price": 79},
            "pro": {"times": 30, "original_price": 297, "discount_price": 199},
            "enterprise": {"times": 50, "original_price": 495, "discount_price": 299}
        }
    },
    "stock": {
        "default_days": 180,
        "batch_max_size": 5
    },
    "output": {
        "report_dir": "reports",
        "format": "markdown",
        "include_disclaimer": True
    },
    "logging": {
        "level": "INFO",
        "file": "valu_ai.log",
        "max_size": 10,
        "backup_count": 5
    },
    "storage": {
        "user_data_dir": "user_data",
        "use_database": False
    }
}


@dataclass
class DeepSeekConfig:
    """DeepSeek API 配置"""
    api_key: str = ""
    api_url: str = "https://api.deepseek.com/v1/chat/completions"
    model: str = "deepseek-chat"
    timeout: int = 180
    max_retries: int = 3


@dataclass
class PricingConfig:
    """定价配置"""
    free_quota_per_week: int = 2
    pay_per_use_price: float = 9.9
    batch_price: float = 29.9
    batch_max_stocks: int = 5

    @classmethod
    def from_dict(cls, data: Dict) -> 'PricingConfig':
        return cls(
            free_quota_per_week=data.get("free", {}).get("quota_per_week", 2),
            pay_per_use_price=data.get("pay_per_use", {}).get("price", 9.9),
            batch_price=data.get("batch", {}).get("price", 29.9),
            batch_max_stocks=data.get("batch", {}).get("max_stocks", 5)
        )


@dataclass
class AppConfig:
    """应用配置"""
    name: str = "ValU AI"
    version: str = "2.0.0"
    debug: bool = False
    language: str = "zh_CN"


class Config:
    """配置管理器"""

    _instance: Optional['Config'] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if Config._initialized:
            return

        self._config: Dict[str, Any] = {}
        self._config_path: Optional[Path] = None
        self._logger: Optional[logging.Logger] = None

        # 加载配置
        self._load_config()

        Config._initialized = True

    def _find_config_file(self) -> Optional[Path]:
        """查找配置文件"""
        # 查找顺序: config.yaml -> config.yml -> config.yaml.example
        base_dir = Path(__file__).parent

        for name in ["config.yaml", "config.yml"]:
            path = base_dir / name
            if path.exists():
                return path

        # 如果都没有，创建默认配置
        default_path = base_dir / "config.yaml"
        return default_path

    def _load_config(self):
        """加载配置文件"""
        config_path = self._find_config_file()
        self._config_path = config_path

        if config_path and config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    loaded = yaml.safe_load(f)
                    if loaded:
                        self._deep_merge(DEFAULT_CONFIG, loaded)
                        self._config = DEFAULT_CONFIG
                        print(f"[OK] Config loaded: {config_path}")
            except Exception as e:
                print(f"[WARN] Config load failed, using defaults: {e}")
                self._config = DEFAULT_CONFIG.copy()
        else:
            print("[INFO] No config file found, using defaults")
            self._config = DEFAULT_CONFIG.copy()

        # 加载环境变量
        self._load_env_vars()

    def _deep_merge(self, base: Dict, update: Dict) -> Dict:
        """深度合并字典"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
        return base

    def _load_env_vars(self):
        """加载环境变量"""
        # DeepSeek API Key
        env_api_key = os.environ.get("DEEPSEEK_API_KEY", "")
        if env_api_key:
            self._config["deepseek"]["api_key"] = env_api_key

        # 其他环境变量可以在这里添加
        env_debug = os.environ.get("VALU_DEBUG", "")
        if env_debug.lower() in ("true", "1", "yes"):
            self._config["app"]["debug"] = True

        env_log_level = os.environ.get("VALU_LOG_LEVEL", "")
        if env_log_level:
            self._config["logging"]["level"] = env_log_level.upper()

    @property
    def app(self) -> AppConfig:
        """获取应用配置"""
        app_data = self._config.get("app", {})
        return AppConfig(
            name=app_data.get("name", "ValU AI"),
            version=app_data.get("version", "2.0.0"),
            debug=app_data.get("debug", False),
            language=app_data.get("language", "zh_CN")
        )

    @property
    def deepseek(self) -> DeepSeekConfig:
        """获取 DeepSeek 配置"""
        ds_data = self._config.get("deepseek", {})
        return DeepSeekConfig(
            api_key=ds_data.get("api_key", ""),
            api_url=ds_data.get("api_url", "https://api.deepseek.com/v1/chat/completions"),
            model=ds_data.get("model", "deepseek-chat"),
            timeout=ds_data.get("timeout", 180),
            max_retries=ds_data.get("max_retries", 3)
        )

    @property
    def pricing(self) -> PricingConfig:
        """获取定价配置"""
        return PricingConfig.from_dict(self._config.get("pricing", {}))

    @property
    def stock_default_days(self) -> int:
        """获取默认历史数据天数"""
        return self._config.get("stock", {}).get("default_days", 180)

    @property
    def batch_max_stocks(self) -> int:
        """获取批量分析最大股票数"""
        return self._config.get("stock", {}).get("batch_max_size", 5)

    @property
    def report_dir(self) -> Path:
        """获取报告保存目录"""
        report_dir = self._config.get("output", {}).get("report_dir", "reports")
        path = Path(report_dir)
        path.mkdir(exist_ok=True)
        return path

    @property
    def user_data_dir(self) -> Path:
        """获取用户数据目录"""
        data_dir = self._config.get("storage", {}).get("user_data_dir", "user_data")
        path = Path(data_dir)
        path.mkdir(exist_ok=True)
        return path

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value

    def setup_logging(self) -> logging.Logger:
        """配置日志系统"""
        if self._logger:
            return self._logger

        log_config = self._config.get("logging", {})
        log_level = getattr(logging, log_config.get("level", "INFO"))
        log_file = log_config.get("file", "valu_ai.log")
        max_size = log_config.get("max_size", 10) * 1024 * 1024  # MB to bytes
        backup_count = log_config.get("backup_count", 5)

        # 创建日志目录
        log_path = Path(log_file)
        log_path.parent.mkdir(exist_ok=True)

        # 配置日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 文件处理器（带轮转）
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(log_level)

        # 创建 logger
        logger = logging.getLogger("ValU_AI")
        logger.setLevel(log_level)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        self._logger = logger
        return logger

    @property
    def logger(self) -> logging.Logger:
        """获取日志器"""
        if self._logger is None:
            return self.setup_logging()
        return self._logger

    def save(self, path: Optional[Path] = None):
        """保存配置到文件"""
        save_path = path or self._config_path
        if save_path is None:
            save_path = Path(__file__).parent / "config.yaml"

        with open(save_path, 'w', encoding='utf-8') as f:
            yaml.dump(self._config, f, allow_unicode=True, default_flow_style=False)

        print(f"[OK] Config saved: {save_path}")


# 全局配置实例
_config: Optional[Config] = None


def get_config() -> Config:
    """获取配置单例"""
    global _config
    if _config is None:
        _config = Config()
    return _config


# 便捷访问函数
def get_pricing_config() -> PricingConfig:
    """获取定价配置"""
    return get_config().pricing


def get_deepseek_config() -> DeepSeekConfig:
    """获取 DeepSeek 配置"""
    return get_config().deepseek


def get_logger() -> logging.Logger:
    """获取日志器"""
    return get_config().logger


if __name__ == "__main__":
    # 测试配置加载
    print("=" * 50)
    print("ValU AI 配置测试")
    print("=" * 50)

    config = get_config()

    print(f"\n[App] {config.app.name} v{config.app.version}")
    print(f"[Debug] {config.app.debug}")

    print(f"\n[Pricing]")
    pricing = config.pricing
    print(f"   Free tier: {pricing.free_quota_per_week} times/week")
    print(f"   Per use: {pricing.pay_per_use_price} CNY/time")
    print(f"   Batch: {pricing.batch_price} CNY/batch (max {pricing.batch_max_stocks} stocks)")

    print(f"\n[Paths]")
    print(f"   Reports: {config.report_dir}")
    print(f"   User data: {config.user_data_dir}")

    print(f"\n[API Config]")
    ds = config.deepseek
    print(f"   API URL: {ds.api_url}")
    print(f"   模型: {ds.model}")
    print(f"   超时: {ds.timeout}秒")
    api_key_display = ds.api_key[:8] + "..." if len(ds.api_key) > 8 else "(not set)"
    print(f"   API Key: {api_key_display}")

    print("\n" + "=" * 50)
    print("[OK] Config test complete")
    print("=" * 50)
