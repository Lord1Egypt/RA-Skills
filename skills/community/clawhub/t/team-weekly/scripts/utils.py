#!/usr/bin/env python3
"""
team-weekly 共享工具模块

提供订阅校验、数据目录管理、日期处理、格式化等通用功能。
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple


# ============================================================
# 常量与配置
# ============================================================

ENV_SUBSCRIPTION_TIER = "TW_SUBSCRIPTION_TIER"
ENV_DATA_DIR = "TW_DATA_DIR"

DEFAULT_DATA_DIR = os.path.expanduser("~/.openclaw-bdi/team-weekly")

# 订阅等级配置
_SUBSCRIPTION_TIERS: Dict[str, Dict[str, Any]] = {
    "free": {
        "tier": "free",
        "max_members": 5,
        "templates": ["basic"],
        "features": [
            "worklog_crud",
            "basic_weekly_report",
        ],
        "price": "免费",
    },
    "paid": {
        "tier": "paid",
        "max_members": 30,
        "templates": ["basic", "tech", "marketing", "sales", "design"],
        "features": [
            "worklog_crud",
            "basic_weekly_report",
            "enhanced_weekly_report",
            "monthly_report",
            "workload_analysis",
            "project_tracking",
            "performance_trend",
        ],
        "price": "¥69/月",
    },
}


# ============================================================
# 数据目录管理
# ============================================================

def get_data_dir() -> str:
    """获取数据存储目录路径。

    优先读取环境变量 TW_DATA_DIR，否则使用默认路径
    ~/.openclaw-bdi/team-weekly/。

    Returns:
        数据目录的绝对路径。
    """
    return os.environ.get(ENV_DATA_DIR, DEFAULT_DATA_DIR)


def ensure_data_dir() -> str:
    """确保数据目录存在，若不存在则创建。

    Returns:
        数据目录的绝对路径。
    """
    data_dir = get_data_dir()
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def get_team_file() -> str:
    """获取团队配置文件路径。"""
    return os.path.join(get_data_dir(), "team.json")


def get_worklog_file() -> str:
    """获取工作日志文件路径。"""
    return os.path.join(get_data_dir(), "worklogs.json")


# ============================================================
# 订阅校验
# ============================================================

def check_subscription(tier: Optional[str] = None) -> Dict[str, Any]:
    """检查当前订阅等级并返回对应的限制配置。

    优先使用传入的 tier 参数，否则读取环境变量 TW_SUBSCRIPTION_TIER。
    若都未设置，默认为 "free" 等级。

    Args:
        tier: 订阅等级（"free" 或 "paid"），可选。

    Returns:
        包含订阅限制信息的字典。

    Raises:
        ValueError: 当传入的等级无效时抛出。
    """
    if tier is None:
        tier = os.environ.get(ENV_SUBSCRIPTION_TIER, "free")

    tier = tier.strip().lower()

    if tier not in _SUBSCRIPTION_TIERS:
        valid = ", ".join(_SUBSCRIPTION_TIERS.keys())
        raise ValueError(f"无效的订阅等级: {tier!r}，有效等级: {valid}")

    return dict(_SUBSCRIPTION_TIERS[tier])


def require_paid(feature_name: str) -> None:
    """校验当前订阅是否为付费版，否则抛出错误。

    Args:
        feature_name: 功能名称，用于错误提示。

    Raises:
        PermissionError: 当前为免费版时抛出。
    """
    sub = check_subscription()
    if sub["tier"] != "paid":
        raise PermissionError(
            f"「{feature_name}」为付费版功能。"
            f"当前为免费版，如需使用请升级至付费版（¥69/月）。"
        )


def check_feature(feature: str) -> bool:
    """检查当前订阅等级是否支持指定功能。

    Args:
        feature: 功能标识符。

    Returns:
        是否支持该功能。
    """
    sub = check_subscription()
    return feature in sub["features"]


# ============================================================
# JSON 输入输出
# ============================================================

def read_input_data(args: argparse.Namespace) -> Dict[str, Any]:
    """从命令行参数或文件读取 JSON 输入数据。

    支持两种方式：
    - --data: 直接传入 JSON 字符串
    - --data-file: 从文件读取 JSON

    Args:
        args: 解析后的命令行参数，需包含 data 和 data_file 属性。

    Returns:
        解析后的字典。

    Raises:
        ValueError: 当输入无效或 JSON 格式错误时抛出。
    """
    raw = None

    if hasattr(args, "data") and args.data:
        raw = args.data
    elif hasattr(args, "data_file") and args.data_file:
        try:
            with open(args.data_file, "r", encoding="utf-8") as f:
                raw = f.read()
        except FileNotFoundError:
            raise ValueError(f"数据文件不存在: {args.data_file}")
        except IOError as e:
            raise ValueError(f"读取数据文件失败: {e}")

    if not raw:
        raise ValueError("请通过 --data 或 --data-file 提供输入数据")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 解析失败: {e}")

    if not isinstance(data, dict):
        raise ValueError(f"期望输入为 JSON 对象，实际类型为 {type(data).__name__}")

    return data


def output_json(data: Any) -> None:
    """将数据以 JSON 格式输出到标准输出。"""
    print(json.dumps(data, ensure_ascii=False, default=str))


def output_error(message: str, code: str = "ERROR") -> None:
    """输出标准错误响应到标准输出。"""
    result = {
        "success": False,
        "error": {
            "code": code,
            "message": message,
        },
    }
    output_json(result)


def output_success(data: Any) -> None:
    """输出标准成功响应到标准输出。"""
    result = {
        "success": True,
        "data": data,
    }
    output_json(result)


# ============================================================
# 命令行参数解析
# ============================================================

def create_base_parser(description: str) -> argparse.ArgumentParser:
    """创建包含通用参数的基础解析器。

    Args:
        description: 工具描述文字。

    Returns:
        配置好的 ArgumentParser 实例。
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--action",
        required=True,
        help="要执行的操作",
    )
    parser.add_argument(
        "--data",
        default=None,
        help="JSON 格式的输入数据",
    )
    parser.add_argument(
        "--data-file",
        default=None,
        help="包含 JSON 数据的文件路径",
    )
    return parser


# ============================================================
# 日期与时间工具
# ============================================================

def today_str() -> str:
    """返回今天的日期字符串（YYYY-MM-DD）。"""
    return datetime.now().strftime("%Y-%m-%d")


def now_str() -> str:
    """返回当前时间字符串（YYYY-MM-DD HH:MM:SS）。"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_date(date_str: str) -> datetime:
    """解析日期字符串为 datetime 对象。

    支持格式：YYYY-MM-DD

    Args:
        date_str: 日期字符串。

    Returns:
        datetime 对象。

    Raises:
        ValueError: 日期格式不正确时抛出。
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"日期格式不正确: {date_str!r}，请使用 YYYY-MM-DD 格式")


def week_range_str(date: Optional[datetime] = None) -> Tuple[str, str]:
    """获取指定日期所在周的起止日期字符串（周一至周日）。

    Args:
        date: 指定日期，默认为今天。

    Returns:
        (周一日期, 周日日期) 的字符串元组。
    """
    if date is None:
        date = datetime.now()
    monday = date - timedelta(days=date.weekday())
    sunday = monday + timedelta(days=6)
    return monday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d")


def month_range_str(year: int, month: int) -> Tuple[str, str]:
    """获取指定月份的起止日期字符串。

    Args:
        year: 年份。
        month: 月份（1-12）。

    Returns:
        (月初日期, 月末日期) 的字符串元组。
    """
    import calendar
    _, last_day = calendar.monthrange(year, month)
    start = f"{year:04d}-{month:02d}-01"
    end = f"{year:04d}-{month:02d}-{last_day:02d}"
    return start, end


def parse_date_range(range_str: str) -> Tuple[str, str]:
    """解析日期范围字符串。

    支持格式：
    - "2024-01-01~2024-01-07"
    - "2024-01-01 to 2024-01-07"
    - "2024-01-01,2024-01-07"

    Args:
        range_str: 日期范围字符串。

    Returns:
        (起始日期, 结束日期) 的字符串元组。

    Raises:
        ValueError: 格式不正确时抛出。
    """
    import re
    parts = re.split(r'[~,]|\s+to\s+', range_str.strip())
    parts = [p.strip() for p in parts if p.strip()]
    if len(parts) != 2:
        raise ValueError(
            f"日期范围格式不正确: {range_str!r}，"
            f"请使用 'YYYY-MM-DD~YYYY-MM-DD' 格式"
        )
    # 验证两个日期格式
    parse_date(parts[0])
    parse_date(parts[1])
    return parts[0], parts[1]


# ============================================================
# 格式化工具
# ============================================================

def format_hours(hours: float) -> str:
    """将小时数格式化为可读字符串。

    Args:
        hours: 小时数。

    Returns:
        格式化后的字符串，例如 8.5 → "8.5h"，8.0 → "8h"
    """
    if hours == int(hours):
        return f"{int(hours)}h"
    return f"{hours:.1f}h"


def format_percentage(value: float, decimals: int = 1) -> str:
    """将小数格式化为百分比字符串。

    Args:
        value: 待格式化的小数值（0.156 表示 15.6%）。
        decimals: 百分比小数位数，默认为 1。

    Returns:
        百分比字符串，例如 0.156 → "15.6%"
    """
    try:
        num = float(value)
    except (TypeError, ValueError):
        raise TypeError(f"无法将 {value!r} 转换为数字")
    pct = num * 100
    return f"{pct:.{decimals}f}%"


def generate_id() -> str:
    """生成唯一 ID（基于时间戳 + 随机后缀）。

    Returns:
        唯一 ID 字符串。
    """
    import random
    import string
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{ts}_{suffix}"


# ============================================================
# 数据存储工具
# ============================================================

def load_json_file(filepath: str) -> Any:
    """加载 JSON 文件，若文件不存在返回 None。

    Args:
        filepath: JSON 文件路径。

    Returns:
        解析后的数据，文件不存在时返回 None。
    """
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def save_json_file(filepath: str, data: Any) -> None:
    """将数据保存为 JSON 文件。

    自动创建父目录。

    Args:
        filepath: 目标文件路径。
        data: 待保存的数据。
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


# ============================================================
# Markdown 表格生成
# ============================================================

def build_markdown_table(headers: List[str], rows: List[List[str]]) -> str:
    """生成 Markdown 格式表格。

    Args:
        headers: 表头列表。
        rows: 数据行列表，每行为字符串列表。

    Returns:
        Markdown 表格字符串。
    """
    if not headers:
        return ""

    lines = []
    # 表头
    lines.append("| " + " | ".join(str(h) for h in headers) + " |")
    # 分隔线
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    # 数据行
    for row in rows:
        # 确保行的列数与表头一致
        padded = list(row) + [""] * (len(headers) - len(row))
        lines.append("| " + " | ".join(str(c) for c in padded[:len(headers)]) + " |")

    return "\n".join(lines)
