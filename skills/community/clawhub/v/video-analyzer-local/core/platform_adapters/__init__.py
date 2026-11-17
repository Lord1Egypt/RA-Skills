"""短视频平台适配器层 — 支持抖音/快手/B站/视频号"""

from .base import PlatformAdapter, PlatformMetadata, ShortVideoAnalysis
from .douyin import DouyinAdapter
from .kuaishou import KuaishouAdapter
from .bilibili import BilibiliAdapter
from .wechat_video import WechatVideoAdapter
from .router import PlatformRouter

__all__ = [
    "PlatformAdapter",
    "PlatformMetadata",
    "ShortVideoAnalysis",
    "DouyinAdapter",
    "KuaishouAdapter",
    "BilibiliAdapter",
    "WechatVideoAdapter",
    "PlatformRouter",
]
