from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def search_user(
    keyword: str,
    page: Optional[int] = 1.0
) -> Dict[str, Any]:
    """
    
搜索哔哩哔哩用户信息。

Args:
    keyword: 用户名关键词
    page: 页码，默认为1

Returns:
    包含用户搜索结果的字典数据

    
    Args:
        keyword: null
        page: null
    
    Returns:
        null
    """
    arguments = {
        "keyword": keyword,
        "page": page
    }
    
    return call_api("1777419073309699", "search_user", arguments)

def search_and_recommend_videos(
    keyword: str,
    count: Optional[int] = 15.0
) -> Dict[str, Any]:
    """
    
搜索并推荐相关视频，提供详细的推荐理由和总结

Args:
    keyword: 搜索关键词（如"AI"）
    count: 推荐视频数量，默认15条

Returns:
    包含推荐视频和总结的字典

    
    Args:
        keyword: null
        count: null
    
    Returns:
        null
    """
    arguments = {
        "keyword": keyword,
        "count": count
    }
    
    return call_api("1777419073309699", "search_and_recommend_videos", arguments)

def get_user_id_by_name(
    username: str,
    return_details: Optional[bool] = False
) -> Dict[str, Any]:
    """
    
通过用户名获取用户ID，支持精确搜索和详细信息返回

Args:
    username: 用户名
    return_details: 是否返回详细信息，默认False只返回用户ID

Returns:
    如果return_details=False: {"user_id": int} 或 {"error": str}
    如果return_details=True: {"users": list, "exact_match": bool} 或 {"error": str}

    
    Args:
        username: null
        return_details: null
    
    Returns:
        null
    """
    arguments = {
        "username": username,
        "return_details": return_details
    }
    
    return call_api("1777419073309699", "get_user_id_by_name", arguments)

def get_video_danmaku(
    video_input: str,
    page: Optional[int] = 0.0
) -> Dict[str, Any]:
    """
    
获取视频的弹幕数据。支持视频链接或BV号输入。

Args:
    video_input: 视频链接或BV号
                支持格式：
                - BV号: BV1iv8CzVE2w
                - 完整链接: https://www.bilibili.com/video/BV1iv8CzVE2w/?spm_id_from=333.1387.homepage.video_card.click
                - 短链接: bilibili.com/video/BV1iv8CzVE2w
    page: 分P页码，从0开始，默认为0（第一个分P）

Returns:
    包含弹幕数据和视频信息的字典

    
    Args:
        video_input: null
        page: null
    
    Returns:
        null
    """
    arguments = {
        "video_input": video_input,
        "page": page
    }
    
    return call_api("1777419073309699", "get_video_danmaku", arguments)

def get_user_dynamics(
    username: str,
    count: Optional[int] = 10.0
) -> Dict[str, Any]:
    """
    
获取指定用户的最新动态

Args:
    username: 用户名（如"技术爬爬虾"）
    count: 要获取的动态数量，默认10条

Returns:
    包含用户动态信息的字典

    
    Args:
        username: null
        count: null
    
    Returns:
        null
    """
    arguments = {
        "username": username,
        "count": count
    }
    
    return call_api("1777419073309699", "get_user_dynamics", arguments)

def get_user_videos(
    username: str,
    count: Optional[int] = 10.0
) -> Dict[str, Any]:
    """
    
获取指定用户的最新投稿视频

Args:
    username: 用户名（如"技术爬爬虾"）
    count: 要获取的视频数量，默认10条

Returns:
    包含用户投稿视频信息的字典

    
    Args:
        username: null
        count: null
    
    Returns:
        null
    """
    arguments = {
        "username": username,
        "count": count
    }
    
    return call_api("1777419073309699", "get_user_videos", arguments)

def get_user_collections(
    username: str
) -> Dict[str, Any]:
    """
    
获取指定用户的合集信息

Args:
    username: 用户名（如"技术爬爬虾"）

Returns:
    包含用户合集信息的字典

    
    Args:
        username: null
    
    Returns:
        null
    """
    arguments = {
        "username": username
    }
    
    return call_api("1777419073309699", "get_user_collections", arguments)

def get_collection_videos(
    username: str,
    collection_name: Optional[str] = "",
    collection_id: Optional[int] = 0.0,
    count: Optional[int] = 10.0
) -> Dict[str, Any]:
    """
    
获取指定用户合集中的视频列表

Args:
    username: 用户名（如"技术爬爬虾"）
    collection_name: 合集名称，可选
    collection_id: 合集ID，可选
    count: 要获取的视频数量，默认10条

Returns:
    包含合集视频信息的字典

    
    Args:
        username: null
        collection_name: null
        collection_id: null
        count: null
    
    Returns:
        null
    """
    arguments = {
        "username": username,
        "collection_name": collection_name,
        "collection_id": collection_id,
        "count": count
    }
    
    return call_api("1777419073309699", "get_collection_videos", arguments)

def search_collection_by_keyword(
    username: str,
    keyword: str,
    count: Optional[int] = 10.0
) -> Dict[str, Any]:
    """
    
在指定用户的所有合集中搜索包含关键词的视频

Args:
    username: 用户名（如"技术爬爬虾"）
    keyword: 搜索关键词（如"MCP"、"AI与大模型"等）
    count: 每个合集最多返回的视频数量，默认10条

Returns:
    包含搜索结果的字典

    
    Args:
        username: null
        keyword: null
        count: null
    
    Returns:
        null
    """
    arguments = {
        "username": username,
        "keyword": keyword,
        "count": count
    }
    
    return call_api("1777419073309699", "search_collection_by_keyword", arguments)

