"""
金融数据工具包配置管理器
加载数据源配置和API密钥。
"""
import os
import json
from pathlib import Path


# 基础路径
SCRIPT_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = SCRIPT_DIR.parent
CONFIG_DIR = PROJECT_DIR / "config"


def get_config() -> dict:
    """从 YAML 加载配置或返回默认值。"""
    try:
        import yaml
        config_path = CONFIG_DIR / "data_sources.yaml"
        if config_path.exists():
            with open(config_path) as f:
                cfg = yaml.safe_load(f)
            _resolve_env_vars(cfg)
            return cfg
    except ImportError:
        pass

    # 回退默认值（无需外部配置）
    return {
        "china_market": {
            "primary": {
                "stock_data": "akshare",
            },
            "optional": {
                "tushare_token": os.getenv("TUSHARE_TOKEN"),
            },
        },
        "rate_limits": {
            "akshare": 5,
        },
    }


def _resolve_env_vars(obj):
    """递归解析配置值中的 ${ENV_VAR} 引用。"""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and v.startswith("${") and v.endswith("}"):
                env_key = v[2:-1]
                obj[k] = os.getenv(env_key)
            elif isinstance(v, (dict, list)):
                _resolve_env_vars(v)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, str) and v.startswith("${") and v.endswith("}"):
                env_key = v[2:-1]
                obj[i] = os.getenv(env_key)
            elif isinstance(v, (dict, list)):
                _resolve_env_vars(v)
