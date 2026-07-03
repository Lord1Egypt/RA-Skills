from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def bazi_calculate(
    birth_date: str,
    birth_time: str
) -> Dict[str, Any]:
    """
    
Calculate BaZi (Eight Characters) for fortune telling / 计算生辰八字用于算命

Args:
    birth_date: Birth date in YYYY-MM-DD format / 出生日期，格式YYYY-MM-DD
    birth_time: Birth time in HH:MM format / 出生时间，格式HH:MM

Returns:
    Detailed BaZi calculation result / 详细的八字计算结果

    
    Args:
        birth_date: null
        birth_time: null
    
    Returns:
        null
    """
    arguments = {
        "birth_date": birth_date,
        "birth_time": birth_time
    }
    
    return call_api("1777419068792835", "bazi_calculate", arguments)

def calendar_convert(
    date: str,
    convert_to: str,
    is_leap: Optional[bool] = False
) -> Dict[str, Any]:
    """
    
Convert between solar and lunar calendar / 公历农历互转

Args:
    date: Date in YYYY-MM-DD format / 日期，格式YYYY-MM-DD
    convert_to: Convert to "lunar" or "solar" / 转换为"lunar"或"solar"
    is_leap: Is leap month (only for lunar to solar conversion) / 是否闰月（仅用于农历转公历）

Returns:
    Calendar conversion result / 历法转换结果

    
    Args:
        date: null
        convert_to: null
        is_leap: null
    
    Returns:
        null
    """
    arguments = {
        "date": date,
        "convert_to": convert_to,
        "is_leap": is_leap
    }
    
    return call_api("1777419068792835", "calendar_convert", arguments)

def huangli_query(
    date: str
) -> Dict[str, Any]:
    """
    
Query Chinese almanac (Huangli) for a specific date / 查询指定日期的黄历信息

Args:
    date: Date in YYYY-MM-DD format / 日期，格式YYYY-MM-DD

Returns:
    Detailed almanac information / 详细的黄历信息

    
    Args:
        date: null
    
    Returns:
        null
    """
    arguments = {
        "date": date
    }
    
    return call_api("1777419068792835", "huangli_query", arguments)

def fortune_daily(
    date: str
) -> Dict[str, Any]:
    """
    
Get daily fortune and recommendations / 获取每日运势和建议

Args:
    date: Date in YYYY-MM-DD format / 日期，格式YYYY-MM-DD

Returns:
    Daily fortune analysis / 每日运势分析

    
    Args:
        date: null
    
    Returns:
        null
    """
    arguments = {
        "date": date
    }
    
    return call_api("1777419068792835", "fortune_daily", arguments)

def jieqi_query(
    year: int
) -> Dict[str, Any]:
    """
    
Query 24 solar terms (Jie Qi) for a year / 查询一年的二十四节气

Args:
    year: Year to query / 查询的年份

Returns:
    List of solar terms for the year / 该年的节气列表

    
    Args:
        year: null
    
    Returns:
        null
    """
    arguments = {
        "year": year
    }
    
    return call_api("1777419068792835", "jieqi_query", arguments)

def wuxing_analyze(
    birth_date: str,
    birth_time: str
) -> Dict[str, Any]:
    """
    
Analyze Wu Xing (Five Elements) from birth info / 根据出生信息分析五行

Args:
    birth_date: Birth date in YYYY-MM-DD format / 出生日期，格式YYYY-MM-DD
    birth_time: Birth time in HH:MM format / 出生时间，格式HH:MM

Returns:
    Wu Xing analysis result / 五行分析结果

    
    Args:
        birth_date: null
        birth_time: null
    
    Returns:
        null
    """
    arguments = {
        "birth_date": birth_date,
        "birth_time": birth_time
    }
    
    return call_api("1777419068792835", "wuxing_analyze", arguments)

