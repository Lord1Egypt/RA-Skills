"""
birth_time_corrector.py - 时辰偏移计算
"""

from datetime import datetime, timedelta
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

# 一时辰 = 2 小时
HOURS_PER_SHIFT = 2

# 时辰名称映射（用于展示）
SHIFT_NAMES = {
    -4: "丑时末",
    -2: "子时中",
    0: "原时",
    2: "丑时初",
    4: "寅时初"
}


def generate_candidate_times(
    base_dt: datetime,
    max_shifts: int = 2
) -> List[datetime]:
    """
    生成候选时间列表（升序）
    
    参数：
    - base_dt: 原始出生时间
    - max_shifts: 最大偏移时辰数（1 或 2）
    
    返回：
    - 列表：[-2h, -1h, +1h, +2h] 对应的 datetime 对象（按升序）
    """
    if max_shifts not in (1, 2):
        raise ValueError(f"max_shifts 必须为 1 或 2，当前: {max_shifts}")
    
    candidates = []
    # 每偏移 1 时辰 = 2 小时
    for shift in [-max_shifts, -1, 1, max_shifts]:
        dt = base_dt + timedelta(hours=shift * HOURS_PER_SHIFT)
        candidates.append(dt)
    
    return sorted(candidates)


def calculate_shift_description(shift_hours: float) -> str:
    """
    生成偏移描述文本
    
    示例：
    - -2.0 → "提前1个时辰"
    - +4.0 → "推后2个时辰"
    """
    shifts = shift_hours / HOURS_PER_SHIFT
    if shifts < 0:
        return f"提前{abs(shifts):.0f}个时辰"
    else:
        return f"推后{shifts:.0f}个时辰"


def get_shift_name(shift_hours: float) -> str:
    """
    获取时辰偏移的通俗名称（如"子时中"、"丑时末"）
    
    注意：此为简化映射，实际需根据八字计算
    """
    rounded = round(shift_hours / 2) * 2  # 取最近的偶数小时
    return SHIFT_NAMES.get(int(rounded), f"偏移{shift_hours:.0f}小时")


def validate_birth_datetime(dt: datetime) -> Tuple[bool, str]:
    """
    验证出生时间是否合理
    
    返回：(is_valid, error_message)
    """
    now = datetime.utcnow()
    if dt > now:
        return False, "出生时间不能晚于当前时间"
    
    if dt.year < 1900:
        return False, "出生年份不能早于 1900 年"
    
    if dt.year > now.year + 1:
        return False, "出生年份超出合理范围"
    
    return True, ""


def calculate_timezone_offset(location: str) -> int:
    """
    根据地点计算时区偏移（小时）
    
    简化实现：仅返回中国主要城市时区
    实际应查询地理数据库或 API
    """
    # 中国标准时区：UTC+8
    china_cities = ["北京", "上海", "广州", "深圳", "杭州", "南京", "武汉", "成都", "重庆", "西安"]
    
    if location in china_cities:
        return 8
    
    # 其他地区可扩展
    return 8  # 默认东八区
