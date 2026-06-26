"""
旅游规划大虾 - 7860端口双系统
"""

from .main_shrimp import app, ShrimpGenerator
from .api_clients.fliggy_client import FliggyClient
from .api_clients.meituan_client import MeituanClient
from .api_clients.amap_client import AmapClient
from .api_clients.tencent_client import TencentMapClient

__all__ = [
    "app",
    "ShrimpGenerator",
    "FliggyClient",
    "MeituanClient",
    "AmapClient",
    "TencentMapClient"
]
