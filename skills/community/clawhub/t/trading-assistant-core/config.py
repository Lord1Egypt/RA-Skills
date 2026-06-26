#!/usr/bin/env python3
"""
Trading Assistant Configuration
交易助手系统配置管理

Configuration is loaded from:
1. Environment variables (.env file)
2. watchlist.txt (user-defined stock list)
3. config.json (optional, for advanced settings)

配置来源:
1. 环境变量 (.env 文件)
2. watchlist.txt (用户自定义股票列表)
3. config.json (可选，高级配置)
"""

from copy import deepcopy
from pathlib import Path
import json
import os

# Security: Do not use load_dotenv() to prevent automatic .env file loading.
# API keys must be set via standard environment variables only.
# This prevents accidental exposure of unrelated secrets from parent directories.

# 项目根目录
PROJECT_ROOT = Path(__file__).parent

# 配置文件路径
CONFIG_FILE = PROJECT_ROOT / "config.json"
DATA_DIR = PROJECT_ROOT / "data"
LOG_DIR = PROJECT_ROOT / "logs"

# 确保目录存在
DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# 默认配置
DEFAULT_CONFIG = {
    # 数据源配置
    "data_sources": {
        "primary": "twelve_data",
        "fallback": "alpha_vantage",
        "twelve_data": {
            "enabled": True,
            "rate_limit": 800  # 次/天
        },
        "alpha_vantage": {
            "enabled": True,
            "rate_limit": 25  # 次/天
        }
    },
    
    # 技术分析参数
    "technical_analysis": {
        # 支撑/阻力位
        "support_resistance": {
            "lookback_days": 60,  # 回看天数
            "min_touches": 2,     # 最少触碰次数
            "tolerance_pct": 1.0  # 价格容差百分比
        },
        
        # 买卖信号
        "trading_signals": {
            "rsi_period": 14,
            "rsi_oversold": 30,
            "rsi_overbought": 70,
            "macd_fast": 12,
            "macd_slow": 26,
            "macd_signal": 9,
            "ma_short": 20,
            "ma_long": 50
        },
        
        # 仓位计算
        "position_sizing": {
            "default_risk_pct": 2.0,  # 默认单笔风险 2%
            "max_position_pct": 20.0, # 单只股票最大仓位 20%
            "risk_levels": {
                "conservative": 1.0,   # 保守：1% 风险
                "moderate": 2.0,       # 稳健：2% 风险
                "aggressive": 3.0      # 进取：3% 风险
            }
        }
    },
    
    # 止盈止损
    "stop_loss_take_profit": {
        "default_stop_loss_pct": 8.0,    # 默认止损 8%
        "default_take_profit_pct": 20.0, # 默认止盈 20%
        "trailing_stop": True,           # 启用移动止损
        "trailing_pct": 5.0              # 移动止损百分比
    },
    
    # 实时监控
    "realtime_monitor": {
        "enabled": True,
        "check_interval_seconds": 60,    # 检查间隔 60 秒
        "price_change_threshold": 5.0,   # 价格波动阈值 5%
        "volume_spike_threshold": 2.0,   # 成交量异常阈值 2 倍
        "alert_channels": ["feishu"]     # 推送渠道
    },
    
    # 推送配置
    "notifications": {
        "feishu": {
            "enabled": False,
            "chat_id": "",
            "webhook_url": ""
        }
    },
    
    # 自选股列表
    "watchlist": [
        "NVDA", "TSLA", "AAPL", "MSFT", "GOOGL",
        "SPY", "QQQ", "IBKR", "PAAS", "BTBT"
    ],
    
    # 风险偏好
    "risk_profile": "moderate"  # conservative/moderate/aggressive
}

def _apply_env_overrides(config):
    """Apply optional notification settings from environment variables."""
    config = deepcopy(config)

    feishu_chat_id = os.environ.get("FEISHU_CHAT_ID")
    feishu_webhook_url = (
        os.environ.get("FEISHU_WEBHOOK_URL")
        or os.environ.get("FEISHU_WEBHOOK")
    )

    if feishu_chat_id or feishu_webhook_url:
        feishu_config = config.setdefault("notifications", {}).setdefault("feishu", {})
        feishu_config["enabled"] = True
        if feishu_chat_id:
            feishu_config["chat_id"] = feishu_chat_id
        if feishu_webhook_url:
            feishu_config["webhook_url"] = feishu_webhook_url

    return config


def load_config():
    """加载配置文件"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            config = json.load(f)
            # 合并默认配置
            return _apply_env_overrides({**DEFAULT_CONFIG, **config})
    return _apply_env_overrides(DEFAULT_CONFIG)

def save_config(config):
    """保存配置文件"""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def get_api_keys():
    """从环境变量获取 API Keys
    
    安全说明:
    - 仅从标准环境变量读取，不读取其他项目的.env 文件
    - 支持的 API Key: 标准环境变量中的 API 密钥
    - 不会访问父目录或其他项目的配置文件
    """
    keys = {}
    
    # 从标准环境变量读取
    twelve_key = os.environ.get("TWELVE_DATA_API_KEY")
    av_key = os.environ.get("ALPHA_VANTAGE_API_KEY")
    
    if twelve_key:
        keys["TWELVE_DATA_API_KEY"] = twelve_key
    if av_key:
        keys["ALPHA_VANTAGE_API_KEY"] = av_key
    
    return keys

def get_api_key(provider):
    """获取单个 API Key (兼容函数)
    
    Args:
        provider: API 提供商名称 ('twelve_data', 'TWELVE_DATA', 'alpha_vantage', 'ALPHA_VANTAGE')
    
    Returns:
        str: API Key 或 None
    """
    provider = provider.upper()
    
    if provider in ["TWELVE_DATA", "TWELVE"]:
        return os.environ.get("TWELVE_DATA_API_KEY")
    elif provider in ["ALPHA_VANTAGE", "ALPHA", "AV"]:
        return os.environ.get("ALPHA_VANTAGE_API_KEY")
    else:
        # 尝试直接匹配
        return os.environ.get(f"{provider}_API_KEY")

# 初始化配置
config = load_config()

if __name__ == "__main__":
    # 测试配置
    print("🔧 Trading Assistant 配置测试")
    print("=" * 60)
    
    cfg = load_config()
    print(f"✅ 配置加载成功")
    print(f"📊 风险偏好：{cfg['risk_profile']}")
    print(f"📈 自选股数量：{len(cfg['watchlist'])}")
    print(f"🔑 API Keys: {len(get_api_keys())} 个")
    print(f"📁 数据目录：{DATA_DIR}")
    print(f"📝 日志目录：{LOG_DIR}")
    print("=" * 60)
