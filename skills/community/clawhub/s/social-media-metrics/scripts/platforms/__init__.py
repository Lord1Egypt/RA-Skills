from __future__ import annotations

from typing import Dict, Type

from .bilibili import BilibiliPlatform
from .youtube import YouTubePlatform
from .douyin import DouyinPlatform
from .kuaishou import KuaishouPlatform
from .xiaohongshu import XiaohongshuPlatform
from .wechat_video import WechatVideoPlatform
from .tiktok import TikTokPlatform
from .instagram import InstagramPlatform
from .toutiao import ToutiaoPlatform
from .baijiahao import BaijihaoPlatform
from .haokan import HaokanPlatform
from .iqiyi import IqiyiPlatform

PLATFORM_REGISTRY: Dict[str, Type] = {
    "bilibili": BilibiliPlatform,
    "youtube": YouTubePlatform,
    "douyin": DouyinPlatform,
    "kuaishou": KuaishouPlatform,
    "xiaohongshu": XiaohongshuPlatform,
    "wechat_video": WechatVideoPlatform,
    "tiktok": TikTokPlatform,
    "instagram": InstagramPlatform,
    "toutiao": ToutiaoPlatform,
    "baijiahao": BaijihaoPlatform,
    "haokan": HaokanPlatform,
    "iqiyi": IqiyiPlatform,
}

__all__ = ["PLATFORM_REGISTRY"]
