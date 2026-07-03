from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def 长亭 IP 情报查询(
    ip: str
) -> Dict[str, Any]:
    """
    基于长亭威胁情报，获取给定 IP 的威胁情报信息，包括 IP 地址、地理位置、ASN、历史恶意行为等信息
    
    Args:
        ip: IP address
    
    Returns:
        
    """
    arguments = {
        "ip": ip
    }
    
    return call_api("1777316659365891", "长亭 IP 情报查询", arguments)

