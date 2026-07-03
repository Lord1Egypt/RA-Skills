from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_all_dishes(
) -> Dict[str, Any]:
    """
    获取所有可用菜品的名称列表 (菜单)。
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659522563", "get_all_dishes", arguments)

def get_dish_content(
    dishName: str
) -> Dict[str, Any]:
    """
    根据提供的菜品名称获取其详细内容。
    
    Args:
        dishName: 要获取内容的菜品名称 (例如 '麻婆豆腐')
    
    Returns:
        
    """
    arguments = {
        "dishName": dishName
    }
    
    return call_api("1777316659522563", "get_dish_content", arguments)

