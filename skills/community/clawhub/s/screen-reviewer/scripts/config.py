#!/usr/bin/env python3
"""
配置管理模块 — 负责加载、保存、合并用户配置
数据目录: ~/.screen-reviewer/
"""

import os
import yaml

DATA_DIR = os.path.expanduser("~/.screen-reviewer")
CONFIG_PATH = os.path.join(DATA_DIR, "config.yaml")
PID_FILE = os.path.join(DATA_DIR, ".capture.pid")
PAUSE_FILE = os.path.join(DATA_DIR, ".paused")

DEFAULT_CONFIG = {
    "capture": {
        "interval_seconds": 5,
        "jpeg_quality": 60,
        "smart_detect": True,
        "change_threshold": 5,  # 至少 N% 像素变化才算"屏幕有变化"
    },
    "privacy": {
        "blacklist_apps": ["1Password", "Keychain Access", "密码"],
    },
    "ocr": {
        "enabled": True,
        "languages": ["zh-Hans", "zh-Hant", "en"],
        "max_text_length": 500,
    },
    "report": {
        "ai_provider": "openai",        # openai / claude / ollama
        "ai_model": "gpt-4o-mini",
        "api_key_env": "OPENAI_API_KEY", # 从哪个环境变量读 API Key
        "generation_hour": 8,
        "ollama_url": "http://localhost:11434",
    },
    "cleanup": {
        "keep_days": 3,
    },
    "categories": {
        "high_value": [
            "Cursor", "VS Code", "Code", "Xcode", "Terminal",
            "iTerm2", "Warp", "GitHub Desktop", "GitLab",
        ],
        "medium_value": [
            "Safari", "Google Chrome", "Firefox", "Arc",
            "Notion", "Obsidian", "飞书", "钉钉", "Slack",
            "Figma", "Sketch", "Preview", "Pages", "Numbers",
        ],
        "low_value": [
            "微信", "QQ", "微博", "Twitter", "Instagram",
            "TikTok", "抖音", "小红书", "Bilibili", "YouTube",
            "Netflix", "爱奇艺",
        ],
    },
}


def ensure_dirs():
    """创建 ~/.screen-reviewer 下的子目录"""
    for subdir in ["screenshots", "logs", "reports"]:
        os.makedirs(os.path.join(DATA_DIR, subdir), exist_ok=True)


def _deep_merge(base: dict, override: dict):
    """递归合并：override 中的值覆盖 base 中同名的值"""
    for k, v in override.items():
        if k in base and isinstance(base[k], dict) and isinstance(v, dict):
            _deep_merge(base[k], v)
        else:
            base[k] = v


def load_config() -> dict:
    """加载配置文件；若不存在，先用默认值创建一份"""
    ensure_dirs()
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            user_cfg = yaml.safe_load(f) or {}
        merged = _deep_merge_copy(DEFAULT_CONFIG, user_cfg)
        return merged
    else:
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()


def _deep_merge_copy(base: dict, override: dict) -> dict:
    """返回合并后的新字典，不修改原字典"""
    import copy
    result = copy.deepcopy(base)
    _deep_merge(result, override)
    return result


def save_config(config: dict):
    """保存配置到 YAML 文件"""
    ensure_dirs()
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
