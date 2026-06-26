"""
utils.py - 辅助函数
"""

import logging
from datetime import datetime, timedelta
from typing import Tuple, Optional
import re

logger = logging.getLogger(__name__)


def to_nongli(dt: datetime) -> Tuple[str, str, str, str, str]:
    """
    阳历转农历（依赖 zhdate 库）
    
    返回：(年干, 年支, 月, 日, 时)
    示例：("癸", "酉", "五", "初一", "子")
    
    若未安装 zhdate，抛出 RuntimeError
    """
    try:
        from zhdate import ZhDate
        lunar = ZhDate.from_datetime(dt)
        
        # 计算年干
        year = lunar.lunar_year
        tiangan_idx = (year - 4) % 10
        tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"][tiangan_idx]
        
        # 计算年支
        nianzhi_idx = (year - 4) % 12
        nianzhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"][nianzhi_idx]
        
        # 农历月、日、时需要转换
        # zhdate 提供 lunar_month, lunar_day
        # 时辰需根据小时计算
        lunar_month_str = _lunar_month_to_chinese(lunar.lunar_month)
        lunar_day_str = _lunar_day_to_chinese(lunar.lunar_day)
        shichen = _hour_to_shichen(dt.hour)
        
        return tiangan, nianzhi, lunar_month_str, lunar_day_str, shichen
        
    except ImportError:
        raise RuntimeError(
            "未安装 zhdate 库，请运行: pip install zhdate\n"
            "参考：https://pypi.org/project/zhdate/"
        )


def _lunar_month_to_chinese(month: int) -> str:
    """数字月转中文（仅用于展示）"""
    mapping = {
        1: "正", 2: "二", 3: "三", 4: "四", 5: "五",
        6: "六", 7: "七", 8: "八", 9: "九", 10: "十",
        11: "冬", 12: "腊"
    }
    return mapping.get(month, str(month))


def _lunar_day_to_chinese(day: int) -> str:
    """农历日转中文"""
    # 简化：1-10为"初一"~"初十"，11-20为"十一"~"二十"，21-30为"廿一"~"三十"
    if day <= 10:
        prefix = "初"
        suffix = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"][day - 1]
    elif day <= 20:
        prefix = "十"
        suffix = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"][day - 11]
    else:
        prefix = "廿"
        suffix = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"][day - 21]
    
    # 特殊：二十 → "二十"（不是"廿十"）
    if day == 20:
        return "二十"
    
    return prefix + suffix


def _hour_to_shichen(hour: int) -> str:
    """24小时制转十二时辰"""
    shichen_map = {
        23: "子", 0: "子",
        1: "丑", 2: "丑",
        3: "寅", 4: "寅",
        5: "卯", 6: "卯",
        7: "辰", 8: "辰",
        9: "巳", 10: "巳",
        11: "午", 12: "午",
        13: "未", 14: "未",
        15: "申", 16: "申",
        17: "酉", 18: "酉",
        19: "戌", 20: "戌",
        21: "亥", 22: "亥"
    }
    return shichen_map.get(hour, "未知")


def calculate_true_solar_time(
    birth_dt: datetime,
    longitude: float,
    latitude: Optional[float] = None
) -> datetime:
    """
    计算真太阳时
    
    原理：根据经度差调整地方时到真太阳时
    公式：真太阳时 = 地方时 + 时差
        时差 = (120° - 经度) × 4分钟/度
    
    参数：
    - birth_dt: 出生时间（地方时）
    - longitude: 出生地经度（度，东经为正）
    - latitude: 出生地纬度（度，暂不使用）
    
    返回：真太阳时（datetime 对象）
    """
    # 每度经度对应 4 分钟
    time_diff_minutes = (120.0 - longitude) * 4
    
    # 转换为 timedelta
    delta = timedelta(minutes=time_diff_minutes)
    
    return birth_dt + delta


def parse_birth_datetime(
    dt_str: str,
    timezone: str = "Asia/Shanghai"
) -> datetime:
    """
    解析出生时间字符串
    
    支持格式：
    - ISO 8601: "1993-04-01T14:00:00+08:00"
    - 简写: "1993-04-01 14:00:00"
    - 无秒: "1993-04-01 14:00"
    
    返回：带时区信息的 datetime 对象
    """
    # 清理空格
    dt_str = dt_str.strip()
    
    # 替换 Date separator
    dt_str = dt_str.replace(" ", "T")
    
    # 如果缺少时区，假设为 Asia/Shanghai (UTC+8)
    if "+" not in dt_str and "Z" not in dt_str:
        dt_str += "+08:00"
    
    try:
        return datetime.fromisoformat(dt_str)
    except ValueError as e:
        raise ValueError(f"无法解析时间字符串 '{dt_str}': {e}")


def generate_cache_key(
    birth_dt: datetime,
    gender: str,
    extra: Optional[str] = None
) -> str:
    """
    生成命盘缓存键
    
    格式：ziwei:YYYYMMDDHHmm:gender[:extra]
    """
    key = f"ziwei:{birth_dt.strftime('%Y%m%d%H%M')}:{gender.upper()}"
    if extra:
        key += f":{extra}"
    return key


def validate_gender(gender: str) -> bool:
    """验证性别参数"""
    return gender.upper() in ["M", "F", "男", "女", "MALE", "FEMALE"]


def normalize_gender(gender: str) -> str:
    """标准化性别为 'M' 或 'F'"""
    gender = gender.upper()
    if gender in ["男", "MALE", "M"]:
        return "M"
    elif gender in ["女", "FEMALE", "F"]:
        return "F"
    else:
        raise ValueError(f"无效性别: {gender}")


def extract_year_from_packet(packet: Dict[str, Any]) -> Optional[int]:
    """从 StandardDataPacket 中提取出生年份"""
    birth_info = packet.get("data", {}).get("birth_info", {})
    birth_dt = birth_info.get("birth_dt", "")
    if birth_dt:
        try:
            dt = datetime.fromisoformat(birth_dt.replace("Z", "+00:00"))
            return dt.year
        except ValueError:
            pass
    return None


def format_iso_datetime(dt: datetime) -> str:
    """格式化 ISO 8601 时间字符串（带 Z 后缀）"""
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


# 导出常用函数
__all__ = [
    "to_nongli",
    "calculate_true_solar_time",
    "parse_birth_datetime",
    "generate_cache_key",
    "validate_gender",
    "normalize_gender",
    "extract_year_from_packet",
    "format_iso_datetime",
]
