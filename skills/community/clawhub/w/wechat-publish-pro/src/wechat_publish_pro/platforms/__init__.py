"""
平台适配器

支持微信公众号等平台发布。
"""

from .base import ImageUploadResult, Platform, PlatformType, PublishRequest, PublishResult
from .wechat import WeChatPlatform

__all__ = [
    "Platform",
    "PlatformType",
    "PublishRequest",
    "PublishResult",
    "ImageUploadResult",
    "WeChatPlatform",
]
