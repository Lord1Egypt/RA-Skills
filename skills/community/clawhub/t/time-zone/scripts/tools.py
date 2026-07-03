from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_current_time(
    timezone: Optional[str] = None
) -> Dict[str, Any]:
    """
    获取指定时区的当前时间
    
    Args:
        timezone: null
    
    Returns:
        
    """
    arguments = {
        "timezone": timezone
    }
    
    return call_api("1777316659725315", "get_current_time", arguments)

def convert_time(
    source_timezone: str,
    time: str,
    target_timezone: str
) -> Dict[str, Any]:
    """
    在不同时区之间转换时间
    
    Args:
        source_timezone: null
        time: null
        target_timezone: null
    
    Returns:
        
    """
    arguments = {
        "source_timezone": source_timezone,
        "time": time,
        "target_timezone": target_timezone
    }
    
    return call_api("1777316659725315", "convert_time", arguments)

