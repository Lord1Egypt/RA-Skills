"""工具函数"""
import re
from pathlib import Path
from typing import Optional


def validate_date(date_str: str) -> bool:
    """验证日期格式 (YYYYMMDD)"""
    if not date_str or len(date_str) != 8:
        return False

    try:
        year = int(date_str[:4])
        month = int(date_str[4:6])
        day = int(date_str[6:8])
        return 2000 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31
    except (ValueError, IndexError):
        return False


def validate_amount(amount_str: str) -> bool:
    """验证金额格式"""
    if not amount_str:
        return False

    try:
        amount = float(amount_str)
        return amount >= 0
    except ValueError:
        return False


def clean_filename(filename: str) -> str:
    """清理文件名中的非法字符"""
    # Windows 文件名非法字符
    illegal_chars = r'[<>:"|?*]'
    cleaned = re.sub(illegal_chars, '_', filename)
    return cleaned.strip()


def get_file_size(path: str) -> int:
    """获取文件大小（字节）"""
    return Path(path).stat().st_size


def format_amount(amount: float) -> str:
    """格式化金额显示"""
    return f"{amount:.2f}"


def truncate(text: str, max_length: int = 50) -> str:
    """截断文本"""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."
