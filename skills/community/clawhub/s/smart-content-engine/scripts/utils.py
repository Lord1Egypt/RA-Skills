#!/usr/bin/env python3
"""
content-engine 共享工具模块

提供内容管理、平台适配、订阅校验、数据格式化等通用功能。
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional


# ============================================================
# 常量定义
# ============================================================

DEFAULT_DATA_DIR = os.path.join(os.path.expanduser("~"), ".openclaw-bdi", "content-engine")

# 内容状态流转: 草稿→待审核→已排期→已发布→已归档
CONTENT_STATUSES = ["草稿", "待审核", "已排期", "已发布", "已归档"]

# 支持的平台列表
PLATFORMS = ["twitter", "linkedin", "wechat", "blog", "medium"]

# 平台显示名称映射
PLATFORM_NAMES = {
    "twitter": "Twitter / X",
    "linkedin": "LinkedIn",
    "wechat": "微信公众号",
    "blog": "博客",
    "medium": "Medium",
}

# 平台字符限制
PLATFORM_CHAR_LIMITS = {
    "twitter": 280,
    "linkedin": 3000,
    "wechat": 20000,
    "blog": 0,       # 博客无限制
    "medium": 0,      # Medium 无限制
}

# 状态流转规则（当前状态 -> 允许的下一状态列表）
STATUS_TRANSITIONS = {
    "草稿": ["待审核", "已归档"],
    "待审核": ["草稿", "已排期", "已归档"],
    "已排期": ["待审核", "已发布", "已归档"],
    "已发布": ["已归档"],
    "已归档": ["草稿"],
}


# ============================================================
# 数据目录管理
# ============================================================

def get_data_dir() -> str:
    """获取数据存储目录路径。

    优先读取环境变量 CE_DATA_DIR，若未设置则使用默认路径
    ~/.openclaw-bdi/content-engine/。
    自动创建目录（若不存在）。

    Returns:
        数据目录的绝对路径。
    """
    data_dir = os.environ.get("CE_DATA_DIR", DEFAULT_DATA_DIR)
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def get_data_file(filename: str) -> str:
    """获取数据文件的完整路径。

    Args:
        filename: 文件名（如 "contents.json"）。

    Returns:
        数据文件的绝对路径。
    """
    return os.path.join(get_data_dir(), filename)


# ============================================================
# JSON 输入输出
# ============================================================

def read_json_file(filepath: str) -> Any:
    """读取 JSON 文件并返回解析后的数据。

    Args:
        filepath: JSON 文件路径。

    Returns:
        解析后的数据对象。若文件不存在，返回空列表。
    """
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def write_json_file(filepath: str, data: Any) -> None:
    """将数据写入 JSON 文件。

    Args:
        filepath: 目标文件路径。
        data: 待写入的数据。
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


def output_json(data: Any) -> None:
    """将数据以 JSON 格式输出到标准输出。

    Args:
        data: 待输出的数据。
    """
    print(json.dumps(data, ensure_ascii=False, default=str))


def output_error(message: str, code: str = "ERROR") -> None:
    """输出标准错误响应到标准输出。

    Args:
        message: 错误描述信息。
        code: 错误代码，默认为 "ERROR"。
    """
    result = {
        "success": False,
        "error": {
            "code": code,
            "message": message,
        },
    }
    output_json(result)


def output_success(data: Any) -> None:
    """输出标准成功响应到标准输出。

    Args:
        data: 成功时返回的数据负载。
    """
    result = {
        "success": True,
        "data": data,
    }
    output_json(result)


# ============================================================
# 命令行参数解析
# ============================================================

def parse_common_args(description: str = "content-engine 内容管理工具") -> argparse.ArgumentParser:
    """创建通用命令行参数解析器。

    Args:
        description: 工具描述文本。

    Returns:
        配置好通用参数的 ArgumentParser 实例。
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--action",
        required=True,
        help="操作类型",
    )
    parser.add_argument(
        "--data",
        default=None,
        help="JSON 格式的数据字符串",
    )
    parser.add_argument(
        "--data-file",
        default=None,
        help="JSON 数据文件路径",
    )
    return parser


def load_input_data(args: argparse.Namespace) -> Optional[Dict[str, Any]]:
    """从命令行参数加载输入数据。

    优先使用 --data 参数，其次尝试 --data-file 参数。

    Args:
        args: 解析后的命令行参数。

    Returns:
        解析后的字典数据，若无输入数据则返回 None。

    Raises:
        ValueError: 当 JSON 解析失败或文件读取失败时抛出。
    """
    if args.data:
        try:
            data = json.loads(args.data)
            if not isinstance(data, dict):
                raise ValueError(f"期望 JSON 对象，实际类型为 {type(data).__name__}")
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 解析失败: {e}")

    if args.data_file:
        if not os.path.exists(args.data_file):
            raise ValueError(f"数据文件不存在: {args.data_file}")
        try:
            with open(args.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError(f"期望 JSON 对象，实际类型为 {type(data).__name__}")
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"数据文件 JSON 解析失败: {e}")

    return None


# ============================================================
# 订阅校验
# ============================================================

_SUBSCRIPTION_TIERS: Dict[str, Dict[str, Any]] = {
    "free": {
        "tier": "free",
        "max_content": 20,
        "max_platforms": 2,
        "features": [
            "content_crud",
            "basic_adapt",
            "manual_publish",
            "markdown_export",
        ],
    },
    "paid": {
        "tier": "paid",
        "max_content": 500,
        "max_platforms": 5,
        "features": [
            "content_crud",
            "basic_adapt",
            "manual_publish",
            "markdown_export",
            "auto_publish",
            "all_platforms",
            "metrics",
            "calendar",
            "wechat",
            "mermaid_chart",
            "batch_adapt",
            "schedule",
        ],
    },
}


def check_subscription(tier: Optional[str] = None) -> Dict[str, Any]:
    """检查当前订阅等级并返回对应的限制配置。

    优先使用传入的 tier 参数，否则读取环境变量 CE_SUBSCRIPTION_TIER。
    若都未设置，默认为 "free" 等级。

    Args:
        tier: 订阅等级（"free" 或 "paid"），可选。

    Returns:
        包含订阅限制信息的字典。

    Raises:
        ValueError: 当传入的等级无效时抛出。
    """
    if tier is None:
        tier = os.environ.get("CE_SUBSCRIPTION_TIER", "free")

    tier = tier.strip().lower()

    if tier not in _SUBSCRIPTION_TIERS:
        valid = ", ".join(_SUBSCRIPTION_TIERS.keys())
        raise ValueError(f"无效的订阅等级: {tier!r}，有效等级: {valid}")

    return dict(_SUBSCRIPTION_TIERS[tier])


def require_paid_feature(feature_name: str, display_name: str) -> bool:
    """检查当前订阅是否支持指定功能。

    若不支持，输出升级提示并返回 False。

    Args:
        feature_name: 功能内部名称。
        display_name: 功能显示名称（用于提示信息）。

    Returns:
        True 表示功能可用，False 表示不可用（已输出错误信息）。
    """
    sub = check_subscription()
    if feature_name not in sub["features"]:
        output_error(
            f"「{display_name}」为付费版功能。当前为免费版，请升级至付费版（¥99/月）以使用此功能。",
            code="SUBSCRIPTION_REQUIRED",
        )
        return False
    return True


# ============================================================
# 内容引擎专用工具函数
# ============================================================

def validate_status(status: str) -> str:
    """校验内容状态是否合法。

    Args:
        status: 待校验的状态名称。

    Returns:
        合法的状态名称。

    Raises:
        ValueError: 当状态名称不合法时抛出。
    """
    if status not in CONTENT_STATUSES:
        valid = "、".join(CONTENT_STATUSES)
        raise ValueError(f"无效的内容状态: {status!r}，有效状态: {valid}")
    return status


def validate_platform(platform: str) -> str:
    """校验平台名称是否合法。

    Args:
        platform: 待校验的平台名称。

    Returns:
        合法的平台名称（小写）。

    Raises:
        ValueError: 当平台名称不合法时抛出。
    """
    platform = platform.strip().lower()
    if platform not in PLATFORMS:
        valid = "、".join(PLATFORMS)
        raise ValueError(f"无效的平台: {platform!r}，有效平台: {valid}")
    return platform


def validate_status_transition(current: str, target: str) -> bool:
    """校验状态流转是否合法。

    Args:
        current: 当前状态。
        target: 目标状态。

    Returns:
        True 表示流转合法。

    Raises:
        ValueError: 当流转不合法时抛出。
    """
    allowed = STATUS_TRANSITIONS.get(current, [])
    if target not in allowed:
        allowed_str = "、".join(allowed) if allowed else "无"
        raise ValueError(
            f"不允许从「{current}」变更为「{target}」。"
            f"当前状态允许变更为: {allowed_str}"
        )
    return True


def format_platform_name(platform: str) -> str:
    """获取平台的显示名称。

    Args:
        platform: 平台标识符（如 "twitter"）。

    Returns:
        平台显示名称（如 "Twitter / X"），未知平台返回原始值。
    """
    return PLATFORM_NAMES.get(platform.lower(), platform)


def truncate_text(text: str, max_len: int) -> str:
    """截断文本到指定长度。

    若文本超过 max_len，截断并在末尾添加省略号。

    Args:
        text: 原始文本。
        max_len: 最大长度。

    Returns:
        截断后的文本。若无需截断则返回原始文本。
    """
    if not text:
        return text
    if max_len <= 0:
        return text
    if len(text) <= max_len:
        return text
    # 保留空间给省略号
    if max_len <= 3:
        return text[:max_len]
    return text[:max_len - 3] + "..."


def count_chars(text: str, platform: str = "") -> int:
    """计算文本在指定平台的字符数。

    Twitter 中一个中文/日文/韩文字符占 2 个字符位；
    其他平台按实际字符数计算。

    Args:
        text: 待计算的文本。
        platform: 平台名称，影响计数规则。

    Returns:
        平台字符数。
    """
    if not text:
        return 0

    platform = platform.lower() if platform else ""

    if platform == "twitter":
        # Twitter: CJK 字符占 2 个字符位
        count = 0
        for ch in text:
            if _is_cjk_char(ch):
                count += 2
            else:
                count += 1
        return count
    else:
        # 其他平台按实际字符数计算
        return len(text)


def _is_cjk_char(ch: str) -> bool:
    """判断字符是否为 CJK（中日韩）字符。

    Args:
        ch: 单个字符。

    Returns:
        True 表示是 CJK 字符。
    """
    cp = ord(ch)
    # CJK 统一汉字基本区
    if 0x4E00 <= cp <= 0x9FFF:
        return True
    # CJK 扩展A区
    if 0x3400 <= cp <= 0x4DBF:
        return True
    # CJK 统一汉字扩展B区
    if 0x20000 <= cp <= 0x2A6DF:
        return True
    # CJK 兼容汉字
    if 0xF900 <= cp <= 0xFAFF:
        return True
    # 日文平假名/片假名
    if 0x3040 <= cp <= 0x30FF:
        return True
    # 韩文音节
    if 0xAC00 <= cp <= 0xD7AF:
        return True
    # 全角字符
    if 0xFF01 <= cp <= 0xFF60:
        return True
    return False


def sanitize_html(html: str) -> str:
    """清理 HTML 内容，移除危险标签和属性。

    保留基本格式标签（p, br, strong, em, a, img, h1-h6, ul, ol, li, blockquote）。
    移除 script, style, iframe, form 等危险标签。
    移除 on* 事件属性。

    Args:
        html: 原始 HTML 字符串。

    Returns:
        清理后的 HTML 字符串。
    """
    if not html:
        return html

    # 移除危险标签及其内容
    dangerous_tags = ["script", "style", "iframe", "form", "input", "textarea", "select", "button", "object", "embed"]
    for tag in dangerous_tags:
        # 移除开闭标签及内容
        pattern = re.compile(rf"<{tag}[^>]*>.*?</{tag}>", re.DOTALL | re.IGNORECASE)
        html = pattern.sub("", html)
        # 移除自闭合标签
        pattern = re.compile(rf"<{tag}[^>]*/?>", re.IGNORECASE)
        html = pattern.sub("", html)

    # 移除所有 on* 事件属性
    html = re.sub(r'\s+on\w+\s*=\s*["\'][^"\']*["\']', "", html, flags=re.IGNORECASE)
    html = re.sub(r"\s+on\w+\s*=\s*\S+", "", html, flags=re.IGNORECASE)

    # 移除 javascript: 链接
    html = re.sub(r'href\s*=\s*["\']javascript:[^"\']*["\']', 'href="#"', html, flags=re.IGNORECASE)

    return html.strip()


def generate_id(prefix: str = "CT") -> str:
    """生成唯一 ID。

    基于时间戳生成，格式为 前缀+时间戳。

    Args:
        prefix: ID 前缀，默认为 "CT"（内容）。

    Returns:
        唯一 ID 字符串。
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"{prefix}{timestamp}"


def now_iso() -> str:
    """返回当前时间的 ISO 格式字符串。

    Returns:
        ISO 格式时间字符串，如 "2026-03-19T10:30:00"。
    """
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def today_str() -> str:
    """返回今天的日期字符串。

    Returns:
        日期字符串，格式为 "YYYY-MM-DD"。
    """
    return datetime.now().strftime("%Y-%m-%d")


def calculate_days_until(date_str: str) -> int:
    """计算从今天到指定日期的天数。

    Args:
        date_str: 日期字符串，格式为 YYYY-MM-DD 或 ISO 格式。

    Returns:
        距今天数（正数表示未来，负数表示过去）。
    """
    try:
        if "T" in date_str:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            dt = dt.replace(tzinfo=None)
        else:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
        delta = dt - datetime.now()
        return delta.days
    except (ValueError, TypeError):
        return 0


def get_week_range(date_str: Optional[str] = None) -> Dict[str, str]:
    """获取指定日期所在周的起止日期。

    Args:
        date_str: 日期字符串（YYYY-MM-DD），默认为今天。

    Returns:
        包含 start 和 end 键的字典，值为日期字符串。
    """
    if date_str:
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            dt = datetime.now()
    else:
        dt = datetime.now()

    # 周一为起始
    start = dt - timedelta(days=dt.weekday())
    end = start + timedelta(days=6)
    return {
        "start": start.strftime("%Y-%m-%d"),
        "end": end.strftime("%Y-%m-%d"),
    }


def get_month_range(date_str: Optional[str] = None) -> Dict[str, str]:
    """获取指定日期所在月的起止日期。

    Args:
        date_str: 日期字符串（YYYY-MM-DD），默认为今天。

    Returns:
        包含 start 和 end 键的字典，值为日期字符串。
    """
    if date_str:
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            dt = datetime.now()
    else:
        dt = datetime.now()

    start = dt.replace(day=1)
    # 下月第一天减一天 = 本月最后一天
    if dt.month == 12:
        end = dt.replace(year=dt.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        end = dt.replace(month=dt.month + 1, day=1) - timedelta(days=1)

    return {
        "start": start.strftime("%Y-%m-%d"),
        "end": end.strftime("%Y-%m-%d"),
    }
