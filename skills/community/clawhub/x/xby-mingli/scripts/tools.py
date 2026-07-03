from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_ziwei_chart(
    date: str,
    time_index: int,
    gender: str,
    calendar: Optional[str] = "solar",
    is_leap_month: Optional[bool] = False,
    format: Optional[str] = "markdown",
    language: Optional[str] = "zh-CN",
    longitude: Optional[float] = None,
    latitude: Optional[float] = None,
    use_solar_time: Optional[bool] = False,
    birth_hour: Optional[int] = None,
    birth_minute: Optional[int] = None
) -> Dict[str, Any]:
    """
    获取紫微斗数排盘信息，包含命盘十二宫、主星、辅星、四化等详细信息
    
    Args:
        date: 出生日期，格式：YYYY-MM-DD，例如：2000-08-16
        time_index: 出生时辰序号（0-12）
        gender: 性别：男 或 女
        calendar: 历法类型：solar(阳历) 或 lunar(农历)
        is_leap_month: 是否为闰月（仅当calendar=lunar时有效）
        format: null
        language: null
        longitude: 出生地经度，用于真太阳时修正
        latitude: 出生地纬度
        use_solar_time: 是否启用真太阳时修正
        birth_hour: 精确出生小时（0-23）
        birth_minute: 精确出生分钟（0-59）
    
    Returns:
        
    """
    arguments = {
        "date": date,
        "time_index": time_index,
        "gender": gender,
        "calendar": calendar,
        "is_leap_month": is_leap_month,
        "format": format,
        "language": language,
        "longitude": longitude,
        "latitude": latitude,
        "use_solar_time": use_solar_time,
        "birth_hour": birth_hour,
        "birth_minute": birth_minute
    }
    
    return call_api("1777419070986243", "get_ziwei_chart", arguments)

def get_ziwei_fortune(
    birth_date: str,
    time_index: int,
    gender: str,
    calendar: Optional[str] = "solar",
    is_leap_month: Optional[bool] = False,
    query_date: Optional[str] = None,
    format: Optional[str] = "markdown",
    language: Optional[str] = "zh-CN"
) -> Dict[str, Any]:
    """
    获取紫微斗数运势信息，包含大限、流年、流月、流日、流时的运势详情
    
    Args:
        birth_date: 出生日期，格式：YYYY-MM-DD
        time_index: 出生时辰序号（0-12）
        gender: 性别：男 或 女
        calendar: null
        is_leap_month: null
        query_date: 查询运势的日期，格式：YYYY-MM-DD
        format: null
        language: null
    
    Returns:
        
    """
    arguments = {
        "birth_date": birth_date,
        "time_index": time_index,
        "gender": gender,
        "calendar": calendar,
        "is_leap_month": is_leap_month,
        "query_date": query_date,
        "format": format,
        "language": language
    }
    
    return call_api("1777419070986243", "get_ziwei_fortune", arguments)

def analyze_ziwei_palace(
    birth_date: str,
    time_index: int,
    gender: str,
    palace_name: str,
    calendar: Optional[str] = "solar",
    is_leap_month: Optional[bool] = False,
    format: Optional[str] = "markdown",
    language: Optional[str] = "zh-CN"
) -> Dict[str, Any]:
    """
    分析紫微斗数特定宫位的详细信息
    
    Args:
        birth_date: 出生日期，格式：YYYY-MM-DD
        time_index: 出生时辰序号（0-12）
        gender: null
        palace_name: 要分析的宫位名称
        calendar: null
        is_leap_month: null
        format: null
        language: null
    
    Returns:
        
    """
    arguments = {
        "birth_date": birth_date,
        "time_index": time_index,
        "gender": gender,
        "palace_name": palace_name,
        "calendar": calendar,
        "is_leap_month": is_leap_month,
        "format": format,
        "language": language
    }
    
    return call_api("1777419070986243", "analyze_ziwei_palace", arguments)

def list_fortune_systems(
    detailed: Optional[bool] = False
) -> Dict[str, Any]:
    """
    列出所有可用的命理系统（紫微斗数、八字、占星等）
    
    Args:
        detailed: 是否输出更详细信息
    
    Returns:
        
    """
    arguments = {
        "detailed": detailed
    }
    
    return call_api("1777419070986243", "list_fortune_systems", arguments)

def get_bazi_chart(
    date: str,
    time_index: int,
    gender: str,
    calendar: Optional[str] = "solar",
    is_leap_month: Optional[bool] = False,
    format: Optional[str] = "markdown",
    language: Optional[str] = "zh-CN"
) -> Dict[str, Any]:
    """
    获取八字（四柱）排盘信息，包含年月日时四柱、十神、五行、地支藏干等详细信息
    
    Args:
        date: 出生日期，格式：YYYY-MM-DD
        time_index: 出生时辰序号（0-12）
        gender: null
        calendar: null
        is_leap_month: null
        format: null
        language: null
    
    Returns:
        
    """
    arguments = {
        "date": date,
        "time_index": time_index,
        "gender": gender,
        "calendar": calendar,
        "is_leap_month": is_leap_month,
        "format": format,
        "language": language
    }
    
    return call_api("1777419070986243", "get_bazi_chart", arguments)

def get_bazi_fortune(
    birth_date: str,
    time_index: int,
    gender: str,
    calendar: Optional[str] = "solar",
    is_leap_month: Optional[bool] = False,
    query_date: Optional[str] = None,
    format: Optional[str] = "markdown",
    language: Optional[str] = "zh-CN"
) -> Dict[str, Any]:
    """
    获取八字运势信息，包含大运、流年等详情
    
    Args:
        birth_date: 出生日期，格式：YYYY-MM-DD
        time_index: 出生时辰序号（0-12）
        gender: null
        calendar: null
        is_leap_month: null
        query_date: 查询运势的日期，格式：YYYY-MM-DD
        format: null
        language: null
    
    Returns:
        
    """
    arguments = {
        "birth_date": birth_date,
        "time_index": time_index,
        "gender": gender,
        "calendar": calendar,
        "is_leap_month": is_leap_month,
        "query_date": query_date,
        "format": format,
        "language": language
    }
    
    return call_api("1777419070986243", "get_bazi_fortune", arguments)

def analyze_bazi_element(
    birth_date: str,
    time_index: int,
    gender: str,
    calendar: Optional[str] = "solar",
    is_leap_month: Optional[bool] = False,
    format: Optional[str] = "markdown",
    language: Optional[str] = "zh-CN"
) -> Dict[str, Any]:
    """
    分析八字五行强弱，包含五行分数、平衡度、缺失五行等
    
    Args:
        birth_date: 出生日期，格式：YYYY-MM-DD
        time_index: 出生时辰序号（0-12）
        gender: null
        calendar: null
        is_leap_month: null
        format: null
        language: null
    
    Returns:
        
    """
    arguments = {
        "birth_date": birth_date,
        "time_index": time_index,
        "gender": gender,
        "calendar": calendar,
        "is_leap_month": is_leap_month,
        "format": format,
        "language": language
    }
    
    return call_api("1777419070986243", "analyze_bazi_element", arguments)

