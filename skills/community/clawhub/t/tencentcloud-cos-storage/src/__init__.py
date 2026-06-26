"""
TencentCloud-COS - 腾讯云对象存储管理
"""

from .cos_manager import (
    COSManager,
    COSCostManager,
    verify_config
)

__all__ = [
    'COSManager',
    'COSCostManager',
    'verify_config'
]

__version__ = '1.0.0'
