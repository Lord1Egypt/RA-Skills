from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def getBaziDetail(
    solarDatetime: Optional[str] = None,
    lunarDatetime: Optional[str] = None,
    gender: float,
    eightCharProviderSect: Optional[float] = 2.0
) -> Dict[str, Any]:
    """
    根据时间（公历或农历）、性别来获取八字信息。solarDatetime和lunarDatetime必须传且只传其中一个。
    
    Args:
        solarDatetime: 用ISO时间格式表示的公历时间. 例如：`2008-03-01T13:00:00+08:00`。
        lunarDatetime: 农历时间。例如农历2000年5月初五中午12点整表示为：`2000-5-5 12:00:00`。
        gender: 传0表示女性，传1表示男性。
        eightCharProviderSect: 早晚子时配置。传1表示23:00-23:59日干支为明天，传2表示23:00-23:59日干支为当天。
    
    Returns:
        
    """
    arguments = {
        "solarDatetime": solarDatetime,
        "lunarDatetime": lunarDatetime,
        "gender": gender,
        "eightCharProviderSect": eightCharProviderSect
    }
    
    return call_api("1777316659717123", "getBaziDetail", arguments)

def getSolarTimes(
    bazi: str
) -> Dict[str, Any]:
    """
    根据八字获取公历时间列表。返回的时间格式为：YYYY-MM-DD hh:mm:ss。例如时间1998年7月31日下午2点整表示为：1998-07-31 14:00:00
    
    Args:
        bazi: 八字，按年柱、月柱、日柱、时柱顺序，用空格隔开。例如：戊寅 己未 己卯 辛未
    
    Returns:
        
    """
    arguments = {
        "bazi": bazi
    }
    
    return call_api("1777316659717123", "getSolarTimes", arguments)

def getChineseCalendar(
    solarDatetime: Optional[str] = None
) -> Dict[str, Any]:
    """
    获取指定公历时间（默认今天）的黄历信息。
    
    Args:
        solarDatetime: 用ISO时间格式表示的公历时间. 例如：`2008-03-01T13:00:00+08:00`。
    
    Returns:
        
    """
    arguments = {
        "solarDatetime": solarDatetime
    }
    
    return call_api("1777316659717123", "getChineseCalendar", arguments)

