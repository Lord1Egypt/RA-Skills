#!/usr/bin/env python3
"""
Showstart Skill API Client
秀动演出查询 API 客户端
"""

import requests
import json
import time
from typing import Optional, Dict, Any

# API 配置
BASE_URL = "http://skill.showstart.com"

# 频率限制：1秒1次，10分钟60次
_last_request_time = 0
_min_interval = 1.0  # 1秒


def _rate_limit():
    """简单的频率限制"""
    global _last_request_time
    current_time = time.time()
    elapsed = current_time - _last_request_time
    if elapsed < _min_interval:
        time.sleep(_min_interval - elapsed)
    _last_request_time = time.time()


def _make_request(params: Dict[str, Any]) -> Optional[Dict]:
    """发送 API 请求"""
    _rate_limit()
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error: {e}", file=__import__('sys').stderr)
        return None


def get_activity(activity_id: int) -> Optional[Dict]:
    """
    查询演出详情
    
    Args:
        activity_id: 演出ID
    
    Returns:
        演出详情数据
    """
    result = _make_request({"id": activity_id})
    if result and result.get("success"):
        return result.get("result")
    return None


def search_keyword(keyword: str, page_no: int = 1, page_size: int = 20) -> Optional[Dict]:
    """
    关键字搜索演出
    
    Args:
        keyword: 搜索关键字
        page_no: 页码，默认1
        page_size: 每页数量，默认20，最大100
    
    Returns:
        搜索结果
    """
    result = _make_request({
        "keyword": keyword,
        "pageNo": page_no,
        "pageSize": page_size
    })
    if result and result.get("success"):
        return result.get("result")
    return None


def search_city(city: str, category: Optional[str] = None, 
                style: Optional[str] = None, page_no: int = 1, 
                page_size: int = 20) -> Optional[Dict]:
    """
    城市搜索（支持模糊搜索）
    
    Args:
        city: 城市名称（支持模糊，如"京"匹配"北京"）
        category: 分类名称（可选）
        style: 风格名称（可选）
        page_no: 页码
        page_size: 每页数量
    
    Returns:
        搜索结果
    """
    params = {
        "city": city,
        "pageNo": page_no,
        "pageSize": page_size
    }
    if category:
        params["category"] = category
    if style:
        params["style"] = style
    
    result = _make_request(params)
    if result and result.get("success"):
        return result.get("result")
    return None


def search_category(category: str, city: Optional[str] = None,
                   style: Optional[str] = None, page_no: int = 1,
                   page_size: int = 20) -> Optional[Dict]:
    """
    分类搜索（支持模糊搜索）
    
    Args:
        category: 分类名称（如"音乐节"、"演唱会"）
        city: 城市名称（可选）
        style: 风格名称（可选）
        page_no: 页码
        page_size: 每页数量
    
    Returns:
        搜索结果
    """
    params = {
        "category": category,
        "pageNo": page_no,
        "pageSize": page_size
    }
    if city:
        params["city"] = city
    if style:
        params["style"] = style
    
    result = _make_request(params)
    if result and result.get("success"):
        return result.get("result")
    return None


def search_style(style: str, city: Optional[str] = None,
                category: Optional[str] = None, page_no: int = 1,
                page_size: int = 20) -> Optional[Dict]:
    """
    风格搜索（支持模糊搜索）
    
    Args:
        style: 风格名称（如"摇滚"、"流行"）
        city: 城市名称（可选）
        category: 分类名称（可选）
        page_no: 页码
        page_size: 每页数量
    
    Returns:
        搜索结果
    """
    params = {
        "style": style,
        "pageNo": page_no,
        "pageSize": page_size
    }
    if city:
        params["city"] = city
    if category:
        params["category"] = category
    
    result = _make_request(params)
    if result and result.get("success"):
        return result.get("result")
    return None


def search_name(name: str, page_no: int = 1, page_size: int = 20) -> Optional[Dict]:
    """
    艺人/场地名搜索（支持模糊搜索）
    
    Args:
        name: 艺人名或场地名
        page_no: 页码
        page_size: 每页数量
    
    Returns:
        搜索结果
    """
    result = _make_request({
        "name": name,
        "pageNo": page_no,
        "pageSize": page_size
    })
    if result and result.get("success"):
        return result.get("result")
    return None


def search_nearby(longitude: float, latitude: float, 
                 page_no: int = 1, page_size: int = 20) -> Optional[Dict]:
    """
    经纬度搜索(附近演出)
    
    Args:
        longitude: 经度
        latitude: 纬度
        page_no: 页码
        page_size: 每页数量
    
    Returns:
        按距离排序的搜索结果
    """
    result = _make_request({
        "loc": f"{longitude},{latitude}",
        "pageNo": page_no,
        "pageSize": page_size
    })
    if result and result.get("success"):
        return result.get("result")
    return None


def get_all_artists() -> Optional[Dict]:
    """
    获取所有有演出的艺人列表（排重）
    
    Returns:
        {
            "total": 艺人总数,
            "artists": ["艺人名1", "艺人名2", ...]
        }
    """
    result = _make_request({"allart": 1})
    if result and result.get("success"):
        return result.get("result")
    return None


def format_artists_list(result: Optional[Dict]) -> str:
    """格式化艺人列表"""
    if not result:
        return "❌ 查询失败或无结果"
    
    artists = result.get('list', [])
    total = result.get('total', len(artists))
    
    lines = [
        f"🎤 共有 {total} 位艺人近期有演出",
        ""
    ]
    
    # 按字母排序
    sorted_artists = sorted(artists, key=lambda x: x.lower())
    
    for i, artist in enumerate(sorted_artists, 1):
        lines.append(f"{i:3d}. {artist}")
    
    return "\n".join(lines)


def format_activity(activity: Dict) -> str:
    """格式化单个活动信息"""
    lines = [
        f"🎵 {activity.get('title', 'Unknown')}",
        f"   📍 {activity.get('city', '')} - {activity.get('siteName', '')}",
        f"   📅 {activity.get('showTime', '')}",
        f"   💰 {activity.get('price', '')}",
    ]
    
    styles = activity.get('styles', [])
    if styles:
        lines.append(f"   🎸 {' / '.join(styles)}")
    
    show_type = activity.get('showTypeTagName', '')
    if show_type:
        lines.append(f"   🏷️ {show_type}")
    
    wish_count = activity.get('wishCount', 0)
    if wish_count:
        lines.append(f"   ⭐ 想看：{wish_count}")
    
    # 使用 wapUrl 移动端链接，PC 版不能购票
    wap_url = activity.get('wapUrl', '')
    if wap_url:
        lines.append(f"   🔗 购票链接：{wap_url}")
    
    lines.append(f"   ID: {activity.get('activityId', '')}")
    lines.append("")
    
    return "\n".join(lines)


def format_search_result(result: Optional[Dict]) -> str:
    """格式化搜索结果"""
    if not result:
        return "❌ 查询失败或无结果"
    
    activities = result.get('list', [])
    total = result.get('total', 0)
    page_no = result.get('pageNo', 1)
    page_size = result.get('pageSize', 100)
    
    lines = [
        f"📊 找到 {total} 个演出（第 {page_no} 页，每页 {page_size} 个）",
        ""
    ]
    
    for i, activity in enumerate(activities, 1):
        lines.append(f"【{i}】")
        lines.append(format_activity(activity))
    
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python showstart_api.py <command> [args...]")
        print("")
        print("Commands:")
        print("  activity <id>           - 查询演出详情")
        print("  keyword <keyword>       - 关键字搜索")
        print("  city <city> [category] [style]  - 城市搜索")
        print("  category <category> [city] [style] - 分类搜索")
        print("  style <style> [city] [category] - 风格搜索")
        print("  name <name>             - 艺人/场地搜索")
        print("  nearby <lng> <lat>      - 附近演出")
        print("  allart                  - 获取所有有演出的艺人列表")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "activity":
        if len(sys.argv) < 3:
            print("Usage: activity <id>")
            sys.exit(1)
        result = get_activity(int(sys.argv[2]))
        if result:
            print(format_activity(result))
        else:
            print("❌ 未找到演出")
    
    elif command == "keyword":
        if len(sys.argv) < 3:
            print("Usage: keyword <keyword>")
            sys.exit(1)
        result = search_keyword(sys.argv[2])
        print(format_search_result(result))
    
    elif command == "city":
        if len(sys.argv) < 3:
            print("Usage: city <city> [category] [style]")
            sys.exit(1)
        city = sys.argv[2]
        category = sys.argv[3] if len(sys.argv) > 3 else None
        style = sys.argv[4] if len(sys.argv) > 4 else None
        result = search_city(city, category, style)
        print(format_search_result(result))
    
    elif command == "category":
        if len(sys.argv) < 3:
            print("Usage: category <category> [city] [style]")
            sys.exit(1)
        category = sys.argv[2]
        city = sys.argv[3] if len(sys.argv) > 3 else None
        style = sys.argv[4] if len(sys.argv) > 4 else None
        result = search_category(category, city, style)
        print(format_search_result(result))
    
    elif command == "style":
        if len(sys.argv) < 3:
            print("Usage: style <style> [city] [category]")
            sys.exit(1)
        style = sys.argv[2]
        city = sys.argv[3] if len(sys.argv) > 3 else None
        category = sys.argv[4] if len(sys.argv) > 4 else None
        result = search_style(style, city, category)
        print(format_search_result(result))
    
    elif command == "name":
        if len(sys.argv) < 3:
            print("Usage: name <name>")
            sys.exit(1)
        result = search_name(sys.argv[2])
        print(format_search_result(result))
    
    elif command == "nearby":
        if len(sys.argv) < 4:
            print("Usage: nearby <longitude> <latitude>")
            sys.exit(1)
        result = search_nearby(float(sys.argv[2]), float(sys.argv[3]))
        print(format_search_result(result))
    
    elif command == "allart":
        result = get_all_artists()
        if result:
            print(format_artists_list(result))
        else:
            print("❌ 获取艺人列表失败")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
