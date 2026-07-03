from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_chemical_info(
    name: str
) -> Dict[str, Any]:
    """
    
获取化学物质的详细信息

Args:
    name: 化学物质名称

    
    Args:
        name: null
    
    Returns:
        null
    """
    arguments = {
        "name": name
    }
    
    return call_api("1777419070952451", "get_chemical_info", arguments)

def search_chemical_by_cas(
    cas_number: str
) -> Dict[str, Any]:
    """
    
通过CAS号搜索化学物质信息

Args:
    cas_number: 化学物质的CAS号

    
    Args:
        cas_number: null
    
    Returns:
        null
    """
    arguments = {
        "cas_number": cas_number
    }
    
    return call_api("1777419070952451", "search_chemical_by_cas", arguments)

