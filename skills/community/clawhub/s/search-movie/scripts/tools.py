from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def search_movie(
    title: str,
    type: str,
    season: Optional[float] = None,
    episode: Optional[float] = None
) -> Dict[str, Any]:
    """
    搜索电影或电视剧资源。返回未验证的搜索结果列表，包含标题、链接和质量信息。使用此工具获取候选资源后，请从结果中选择最匹配的链接，然后使用 validate_video_url 工具验证其可播放性。
    
    Args:
        title: 电影或电视剧的标题
        type: 内容类型：movie（电影）或 tv（电视剧）
        season: 季数（仅限电视剧）
        episode: 集数（仅限电视剧）
    
    Returns:
        
    """
    arguments = {
        "title": title,
        "type": type,
        "season": season,
        "episode": episode
    }
    
    return call_api("1777316659782659", "search_movie", arguments)

def validate_video_url(
    url: null
) -> Dict[str, Any]:
    """
    验证特定视频链接的可播放性。接收一个视频播放页面的 URL 或 URL 数组，返回该链接是否可以正常播放。支持批量验证多个链接。只有通过验证的链接才能确保用户可以观看。
    
    Args:
        url: 要验证的视频播放页面 URL（单个或数组）
    
    Returns:
        
    """
    arguments = {
        "url": url
    }
    
    return call_api("1777316659782659", "validate_video_url", arguments)

