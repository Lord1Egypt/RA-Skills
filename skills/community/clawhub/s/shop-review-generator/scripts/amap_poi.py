#!/usr/bin/env python3
"""
高德地图 POI 查询脚本

通过高德开放平台 API 查询店铺信息，包括名称、地址、评分、营业时间等。
也支持从高德地图分享链接中提取 POI ID 后直接查询详情。

使用方式:
    # 按关键词搜索店铺
    python amap_poi.py search "海底捞" --city "北京"

    # 从高德链接提取并查询
    python amap_poi.py link "https://amap.com/place/B0xxxxx"

    # 按 POI ID 查询详情
    python amap_poi.py detail "B0FFKG1GN2"

依赖: 仅需 Python 3 标准库（urllib），无需 pip install 任何包
"""

import json
import sys
import re
import ssl
import urllib.request
import urllib.parse
import urllib.error

# 处理 macOS 上 Python 的 SSL 证书问题
try:
    _ssl_context = ssl.create_default_context()
except Exception:
    _ssl_context = ssl._create_unverified_context()

try:
    import certifi
    _ssl_context.load_verify_locations(certifi.where())
except ImportError:
    # 没有 certifi，尝试不验证证书（开发环境可接受）
    _ssl_context = ssl._create_unverified_context()

AMAP_KEY = "e0c7d5a147d5a0b82563dabdb35e5a78"
BASE_URL = "https://restapi.amap.com/v3"


def search_poi(keyword: str, city: str = "", types: str = "050000") -> list[dict]:
    """
    关键词搜索 POI

    Args:
        keyword: 店铺名称关键词
        city: 城市名称（可选，提高精度）
        types: POI 类型编码，050000=餐饮服务

    Returns:
        POI 列表，每项包含 name, address, location, tel, rating, cost, type 等
    """
    params = {
        "key": AMAP_KEY,
        "keywords": keyword,
        "types": types,
        "city": city,
        "citylimit": "true" if city else "false",
        "offset": 10,
        "extensions": "all",
        "output": "json",
    }
    url = f"{BASE_URL}/place/text?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=10, context=_ssl_context) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"请求失败: {e}", file=sys.stderr)
        return []

    if data.get("status") != "1":
        print(f"API 错误: {data.get('info', '未知错误')}", file=sys.stderr)
        return []

    results = []
    for poi in data.get("pois", []):
        results.append(_extract_poi_info(poi))

    return results


def get_poi_detail(poi_id: str) -> dict | None:
    """
    按 POI ID 查询详情

    Args:
        poi_id: 高德 POI ID（如 B0FFKG1GN2）

    Returns:
        POI 详情字典，或 None
    """
    params = {
        "key": AMAP_KEY,
        "id": poi_id,
        "extensions": "all",
        "output": "json",
    }
    url = f"{BASE_URL}/place/detail?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=10, context=_ssl_context) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"请求失败: {e}", file=sys.stderr)
        return None

    if data.get("status") != "1":
        print(f"API 错误: {data.get('info', '未知错误')}", file=sys.stderr)
        return None

    pois = data.get("pois", [])
    if not pois:
        return None

    return _extract_poi_info(pois[0])


def extract_poi_id_from_url(url: str) -> str | None:
    """
    从高德地图 URL 中提取 POI ID

    支持的 URL 格式:
    - https://amap.com/place/B0FFKG1GN2
    - https://www.amap.com/place/B0FFKG1GN2
    - https://uri.amap.com/marker?poiid=B0FFKG1GN2
    - https://m.amap.com/share/xxx (需要进一步解析)
    - https://surl.amap.com/xxx (短链接)
    """
    # 标准 place 链接
    match = re.search(r'/place/([A-Z0-9]+)', url)
    if match:
        return match.group(1)

    # uri.amap.com 格式
    match = re.search(r'poiid=([A-Z0-9]+)', url)
    if match:
        return match.group(1)

    # 尝试跟随短链接重定向
    if 'surl.amap.com' in url or 'm.amap.com' in url:
        try:
            req = urllib.request.Request(url, method='HEAD')
            req.add_header('User-Agent', 'Mozilla/5.0')
            with urllib.request.urlopen(req, timeout=10, context=_ssl_context) as resp:
                final_url = resp.url
                match = re.search(r'/place/([A-Z0-9]+)', final_url)
                if match:
                    return match.group(1)
                match = re.search(r'poiid=([A-Z0-9]+)', final_url)
                if match:
                    return match.group(1)
        except Exception:
            pass

    return None


def _extract_poi_info(poi: dict) -> dict:
    """从高德 API 返回的 POI 数据中提取关键信息"""
    biz = poi.get("biz_ext", {})
    return {
        "id": poi.get("id", ""),
        "name": poi.get("name", ""),
        "type": poi.get("type", ""),
        "address": poi.get("address", ""),
        "city": poi.get("cityname", ""),
        "district": poi.get("adname", ""),
        "location": poi.get("location", ""),
        "tel": poi.get("tel", ""),
        "rating": biz.get("rating", poi.get("biz_ext", {}).get("rating", "")),
        "cost": biz.get("cost", ""),
        "open_time": poi.get("business", {}).get("opentime", "") if isinstance(poi.get("business"), dict) else "",
        "photos": [p.get("url", "") for p in poi.get("photos", [])[:3]],
    }


def _print_poi(poi: dict, index: int = 0):
    """格式化打印 POI 信息"""
    print(f"\n{'='*50}")
    if index:
        print(f"[{index}]")
    print(f"名称: {poi['name']}")
    print(f"类型: {poi['type']}")
    print(f"地址: {poi['city']}{poi['district']}{poi['address']}")
    if poi['tel']:
        print(f"电话: {poi['tel']}")
    if poi['rating']:
        print(f"评分: {poi['rating']}")
    if poi['cost']:
        print(f"人均: ¥{poi['cost']}")
    if poi['open_time']:
        print(f"营业: {poi['open_time']}")
    print(f"POI ID: {poi['id']}")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    action = sys.argv[1]

    if action == "search":
        keyword = sys.argv[2]
        city = ""
        for i, arg in enumerate(sys.argv):
            if arg == "--city" and i + 1 < len(sys.argv):
                city = sys.argv[i + 1]
        results = search_poi(keyword, city)
        if results:
            print(f"找到 {len(results)} 个结果:")
            for i, poi in enumerate(results, 1):
                _print_poi(poi, i)
        else:
            print("未找到结果")

    elif action == "link":
        url = sys.argv[2]
        poi_id = extract_poi_id_from_url(url)
        if poi_id:
            print(f"提取到 POI ID: {poi_id}")
            detail = get_poi_detail(poi_id)
            if detail:
                _print_poi(detail)
            else:
                print("查询详情失败")
        else:
            print(f"无法从 URL 中提取 POI ID: {url}")
            print("尝试从 URL 中提取店铺名称进行搜索...")

    elif action == "detail":
        poi_id = sys.argv[2]
        detail = get_poi_detail(poi_id)
        if detail:
            _print_poi(detail)
        else:
            print("查询失败")

    else:
        print(f"未知操作: {action}")
        print("支持: search, link, detail")
        sys.exit(1)
