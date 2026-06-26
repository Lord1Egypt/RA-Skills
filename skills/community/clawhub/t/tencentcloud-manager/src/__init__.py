"""
TencentCloud-Manager - 腾讯云资源统一管理
"""

from .tencentcloud_manager import (
    TencentCloudManager,
    verify_config
)

__all__ = [
    'TencentCloudManager',
    'verify_config'
]

__version__ = '1.0.0'
