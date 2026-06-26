"""
敏感信息自动脱敏引擎 v0.5.0
============================
在数据上报到中心服务器之前，自动检测并脱敏以下敏感信息：
  - 用户文件路径 (/Users/xxx, /home/xxx, C:\\Users\\xxx)
  - IP 地址
  - Email 地址
  - 手机号码（中国大陆）
  - API Key / Bearer Token
  - 环境变量中的密钥
  - 自定义正则（可配置白名单）

Usage:
    sanitizer = DataSanitizer()
    clean_data = sanitizer.sanitize(raw_data)
"""

import json
import logging
import os
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)

# 默认脱敏规则
DEFAULT_PATTERNS = {
    "user_path_unix": {
        "pattern": r"/Users/[^/\s]+",
        "replacement": "~",
        "description": "macOS 用户路径",
    },
    "user_path_linux": {
        "pattern": r"/home/[^/\s]+",
        "replacement": "~",
        "description": "Linux 用户路径",
    },
    "user_path_windows": {
        "pattern": r"C:\\Users\\[^\\\s]+",
        "replacement": "~",
        "description": "Windows 用户路径",
    },
    "ip_address": {
        "pattern": r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b",
        "replacement": "[IP_REDACTED]",
        "description": "IPv4 地址",
    },
    "email": {
        "pattern": r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",
        "replacement": "[EMAIL_REDACTED]",
        "description": "Email 地址",
    },
    "phone_cn": {
        "pattern": r"\b1[3-9]\d{9}\b",
        "replacement": "[PHONE_REDACTED]",
        "description": "中国大陆手机号",
    },
    "api_key_sk": {
        "pattern": r"sk-[a-zA-Z0-9]{16,}",
        "replacement": "sk-[REDACTED]",
        "description": "API Key (sk-前缀)",
    },
    "bearer_token": {
        "pattern": r"Bearer\s+[a-zA-Z0-9._\-]{20,}",
        "replacement": "Bearer [REDACTED]",
        "description": "Bearer Token",
    },
    "env_secrets": {
        "pattern": r"(?:OPENAI_API_KEY|ANTHROPIC_API_KEY|SECRET_KEY|API_SECRET|ACCESS_TOKEN|PRIVATE_KEY)\s*=\s*[^\s]+",
        "replacement": "[ENV_SECRET_REDACTED]",
        "description": "环境变量密钥",
    },
    "jwt_token": {
        "pattern": r"eyJ[a-zA-Z0-9_-]{10,}\.eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}",
        "replacement": "[JWT_REDACTED]",
        "description": "JWT Token",
    },
}

# 白名单路径（不脱敏）
DEFAULT_WHITELIST = {
    "/usr/local",
    "/usr/bin",
    "/tmp",
    "/var",
    "/etc",
    "/opt",
}

CONFIG_FILE = os.path.expanduser("~/.skills_monitor/sanitizer_config.json")


class DataSanitizer:
    """敏感信息自动脱敏引擎"""

    def __init__(self, config_path: str = CONFIG_FILE):
        self._patterns: Dict[str, dict] = dict(DEFAULT_PATTERNS)
        self._whitelist: Set[str] = set(DEFAULT_WHITELIST)
        self._disabled_rules: Set[str] = set()
        self._compiled: Dict[str, re.Pattern] = {}
        self._stats: Dict[str, int] = {}  # 脱敏统计

        # 加载用户自定义配置
        self._load_config(config_path)
        self._compile_patterns()

    def _load_config(self, config_path: str):
        """加载用户自定义脱敏配置"""
        if not os.path.exists(config_path):
            return
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            # 合并自定义规则
            for name, rule in config.get("custom_patterns", {}).items():
                self._patterns[name] = rule
            # 合并白名单
            self._whitelist.update(config.get("whitelist", []))
            # 禁用的规则
            self._disabled_rules.update(config.get("disabled_rules", []))
        except Exception as e:
            logger.warning(f"加载脱敏配置失败: {e}")

    def _compile_patterns(self):
        """预编译正则表达式"""
        for name, rule in self._patterns.items():
            if name not in self._disabled_rules:
                try:
                    self._compiled[name] = re.compile(rule["pattern"])
                    self._stats[name] = 0
                except re.error as e:
                    logger.error(f"正则编译失败 [{name}]: {e}")

    # ──────── 核心脱敏 ────────

    def sanitize(self, data: Any) -> Any:
        """
        递归脱敏任意数据结构
        支持：dict / list / str / 嵌套结构
        """
        self._stats = {k: 0 for k in self._stats}  # 重置统计
        return self._sanitize_recursive(data)

    def _sanitize_recursive(self, obj: Any) -> Any:
        if isinstance(obj, dict):
            return {k: self._sanitize_recursive(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._sanitize_recursive(item) for item in obj]
        elif isinstance(obj, str):
            return self._sanitize_string(obj)
        else:
            return obj

    def _sanitize_string(self, text: str) -> str:
        """对单个字符串应用所有脱敏规则"""
        result = text
        for name, pattern in self._compiled.items():
            replacement = self._patterns[name].get("replacement", "[REDACTED]")

            def _replace(m, repl=replacement, rule_name=name):
                matched = m.group(0)
                # 白名单检查
                if any(matched.startswith(w) for w in self._whitelist):
                    return matched
                self._stats[rule_name] = self._stats.get(rule_name, 0) + 1
                return repl

            result = pattern.sub(_replace, result)
        return result

    def sanitize_path(self, path: str) -> str:
        """路径专用脱敏：/Users/lynn/project → ~/project"""
        if not path:
            return path
        home = os.path.expanduser("~")
        if path.startswith(home):
            return "~" + path[len(home):]
        # 其他用户路径
        result = re.sub(r"/Users/[^/]+", "~", path)
        result = re.sub(r"/home/[^/]+", "~", result)
        result = re.sub(r"C:\\Users\\[^\\]+", "~", result)
        return result

    # ──────── 统计 & 配置 ────────

    def get_stats(self) -> Dict[str, int]:
        """获取最近一次脱敏的统计"""
        return dict(self._stats)

    def get_total_redacted(self) -> int:
        """获取总脱敏次数"""
        return sum(self._stats.values())

    def save_default_config(self, path: str = CONFIG_FILE):
        """生成默认配置文件（供用户自定义）"""
        config = {
            "custom_patterns": {},
            "whitelist": list(self._whitelist),
            "disabled_rules": [],
            "_comment": "自定义脱敏配置。custom_patterns 中的规则会与默认规则合并。",
        }
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
