"""配置管理"""
import os
import json
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 本地配置文件路径
CONFIG_FILE = PROJECT_ROOT / "config.json"

# 默认配置
DEFAULT_CONFIG = {
    "company_name": "你的公司名称",
    "person_name": "",  # 用于火车票
    "output_dir": str(PROJECT_ROOT / "output"),
}

# 运行时配置（从配置文件加载）
_config = None


def get_config() -> dict:
    """获取配置（带缓存）"""
    global _config
    if _config is None:
        _config = load_config()
    return _config


def load_config() -> dict:
    """加载配置（优先本地配置，否则使用默认）"""
    # 1. 检查本地配置文件
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                local_config = json.load(f)
            config = DEFAULT_CONFIG.copy()
            config.update(local_config)
            return config
        except (json.JSONDecodeError, IOError):
            pass

    # 2. 检查环境变量
    config = DEFAULT_CONFIG.copy()
    if os.getenv("COMPANY_NAME"):
        config["company_name"] = os.getenv("COMPANY_NAME")
    if os.getenv("PERSON_NAME"):
        config["person_name"] = os.getenv("PERSON_NAME")
    if os.getenv("OUTPUT_DIR"):
        config["output_dir"] = os.getenv("OUTPUT_DIR")

    return config


def save_config(config: dict) -> None:
    """保存配置到本地文件"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def is_configured() -> bool:
    """检查是否已配置（公司名称是否已设置）"""
    config = get_config()
    return bool(config.get("company_name") and config["company_name"] != "你的公司名称")


# 公司名称（用于发票命名）
COMPANY_NAME = get_config().get("company_name", "你的公司名称")

# 默认输出目录
DEFAULT_OUTPUT_DIR = Path(get_config().get("output_dir", str(PROJECT_ROOT / "output")))

# 支持的文件扩展名
SUPPORTED_EXTENSIONS = [".pdf", ".jpg", ".png", ".jpeg"]

# 最大批量处理数
MAX_BATCH_SIZE = 50

# 命名规则模板
NAMING_RULES = {
    "train": "{person}-{date}-{amount}-中国铁路",
    "didi": "{company}-{date}-{invoice_no}-{amount}-{seller}-发票",
    "trip": "{company}-{date}-{invoice_no}-{amount}-{seller}-行程单",
    "hotel": "{company}-{date}-{invoice_no}-{amount}-{seller}",
    "flight": "{company}-{date}-{invoice_no}-{amount}-{seller}-机票",
}

# 票据类型关键词（用于预判）
TYPE_KEYWORDS = {
    "train": ["中国铁路", "火车票", "rail", "train"],
    "didi": ["滴滴", "出租车", "didi", "打车"],
    "trip": ["行程单"],
    "hotel": ["酒店", "hotel", "住宿"],
    "flight": ["航空", "机票", "flight", "airline"],
}
