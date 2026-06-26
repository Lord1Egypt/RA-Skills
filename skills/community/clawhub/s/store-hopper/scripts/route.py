#!/usr/bin/env python3
"""
store-hopper: 路线规划与交通查询脚本
用法:
  单段: python3 route.py "<起点地址>" "<终点地址>" [--weather good|mild|bad] [--city 杭州]
  批量: python3 route.py pois.json "<起点>" --batch [--weather good|mild|bad] [--city 杭州]
输出:
  stdout: JSON 格式的交通方案
  stderr: 关键信息摘要（一行）

地理编码优先级:
  1. 高德地图 REST API（需 AMAP_KEY，精度最高）
  2. 百度地图 REST API（需 BAIDU_MAP_AK）
  3. 高德地图 Web POI 搜索（免费，无需 Key，中文 POI 精度极高）
  4. 腾讯地图 Web POI 搜索（免费，无需 Key，来自 lbs.qq.com/getPoint）
  5. Photon（免费备选，中文准确度一般）

环境变量（可选，提升准确率）:
  - AMAP_KEY: 高德地图 Web服务 API Key
  - BAIDU_MAP_AK: 百度地图 AK
"""

import argparse
import json
import math
import os
import sys
import time
import requests
from urllib.parse import quote


# ───────────────── 摘要输出 ─────────────────

def summary(msg: str):
    """输出一行关键摘要到 stderr"""
    sys.stderr.write(f"[路线] {msg}\n")
    sys.stderr.flush()


# ───────────────── 地理编码服务 ─────────────────

def geocode_amap_api(address: str) -> tuple:
    """高德地图 REST API 地理编码（需 AMAP_KEY，精度最高）"""
    key = os.environ.get("AMAP_KEY", "")
    if not key:
        return None, None
    url = f"https://restapi.amap.com/v3/geocode/geo?address={quote(address)}&key={key}"
    try:
        resp = requests.get(url, timeout=(2, 5))
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") == "1" and data.get("geocodes"):
            location = data["geocodes"][0]["location"]
            lon, lat = location.split(",")
            return float(lat), float(lon)
    except Exception:
        pass
    return None, None


def geocode_baidu_api(address: str) -> tuple:
    """百度地图 REST API 地理编码（需 BAIDU_MAP_AK）"""
    ak = os.environ.get("BAIDU_MAP_AK", "")
    if not ak:
        return None, None
    url = f"https://api.map.baidu.com/geocoding/v3/?address={quote(address)}&output=json&ak={ak}"
    try:
        resp = requests.get(url, timeout=(2, 5))
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") == 0 and data.get("result"):
            loc = data["result"]["location"]
            return loc["lat"], loc["lng"]
    except Exception:
        pass
    return None, None


def geocode_amap_web(address: str) -> tuple:
    """
    高德地图 Web POI 搜索（免费，无需 API Key）。
    利用 amap.com 网页端的 POI 搜索接口，对中文地名/店名/地标精度极高。
    """
    url = "https://www.amap.com/service/poiInfo"
    params = {
        "query_type": "TQUERY",
        "pagesize": "1",
        "pagenum": "1",
        "qii": "true",
        "cluster_state": "5",
        "need_utd": "true",
        "utd_sceneid": "1000",
        "div": "PC1000",
        "addr_poi_merge": "true",
        "is_classify": "true",
        "zoom": "11",
        "keywords": address,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.amap.com/",
    }
    try:
        resp = requests.get(url, params=params, timeout=(3, 5), headers=headers)
        resp.raise_for_status()
        data = resp.json()
        pois = data.get("data", {}).get("poi_list", [])
        if pois:
            lat = float(pois[0]["latitude"])
            lon = float(pois[0]["longitude"])
            return lat, lon
    except requests.exceptions.ConnectionError:
        raise  # 传播以禁用
    except Exception:
        pass
    return None, None


def geocode_tencent_web(address: str, city_hint: str = "") -> tuple:
    """
    腾讯地图 Web POI 搜索（免费，无需 API Key）。
    利用 lbs.qq.com/getPoint 页面的内置 h5gw 搜索接口。
    search API 需要 boundary 参数指定城市，有 city_hint 时精度极高。
    无 city_hint 时降级到 suggestion API（支持混合关键词）。
    """
    _TENCENT_KEY = "NQQBZ-YDDK4-7G2UP-XCWS6-VMOB5-S5BN3"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://lbs.qq.com/getPoint/",
    }
    try:
        # 优先用 search API（需要 city_hint 分离到 boundary）
        if city_hint:
            keyword = address.replace(city_hint, "").strip() or address
            resp = requests.get(
                "https://h5gw.map.qq.com/ws/place/v1/search",
                params={
                    "boundary": f"region({city_hint},0)",
                    "keyword": keyword,
                    "apptag": "lbsplace_search",
                    "key": _TENCENT_KEY,
                    "output": "json",
                    "page_size": "1",
                },
                headers=headers,
                timeout=(3, 5),
            )
            resp.raise_for_status()
            data = resp.json()
            if data.get("status") == 0 and data.get("data"):
                loc = data["data"][0]["location"]
                return float(loc["lat"]), float(loc["lng"])

        # 降级到 suggestion API（支持混合关键词，无需分离城市）
        resp = requests.get(
            "https://h5gw.map.qq.com/ws/place/v1/suggestion",
            params={
                "keyword": address,
                "region": city_hint or "",
                "region_fix": "1" if city_hint else "0",
                "key": _TENCENT_KEY,
                "apptag": "lbsplace_sug",
                "output": "json",
            },
            headers=headers,
            timeout=(3, 5),
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") == 0 and data.get("data"):
            loc = data["data"][0]["location"]
            return float(loc["lat"]), float(loc["lng"])
    except requests.exceptions.ConnectionError:
        raise  # 传播以禁用
    except Exception:
        pass
    return None, None


def geocode_photon(address: str) -> tuple:
    """Photon 地理编码（免费备选，中文准确度一般）"""
    url = f"https://photon.komoot.io/api/?q={quote(address)}&limit=1&lang=default"
    headers = {"User-Agent": "store-hopper/1.0"}
    try:
        resp = requests.get(url, timeout=(3, 5), headers=headers)
        resp.raise_for_status()
        data = resp.json()
        if data.get("features"):
            coords = data["features"][0]["geometry"]["coordinates"]
            return coords[1], coords[0]  # GeoJSON: [lon, lat] → (lat, lon)
    except requests.exceptions.ConnectionError:
        raise  # 传播以禁用
    except Exception:
        pass
    return None, None


# 主要城市中心坐标（用于异常检测）
CITY_CENTERS = {
    "北京": (39.90, 116.40), "上海": (31.23, 121.47), "广州": (23.13, 113.26),
    "深圳": (22.54, 114.06), "杭州": (30.27, 120.15), "成都": (30.57, 104.07),
    "武汉": (30.59, 114.30), "南京": (32.06, 118.80), "重庆": (29.56, 106.55),
    "西安": (34.26, 108.94), "长沙": (28.23, 112.94), "天津": (39.08, 117.20),
    "苏州": (31.30, 120.62), "青岛": (36.07, 120.38), "厦门": (24.48, 118.09),
    "大连": (38.91, 121.60), "三亚": (18.25, 109.50), "桂林": (25.27, 110.29),
    "丽江": (26.87, 100.23), "大理": (25.59, 100.23), "昆明": (25.04, 102.71),
    "郑州": (34.75, 113.65), "合肥": (31.82, 117.23), "福州": (26.07, 119.30),
}

# 记录不可用的 geocoder，避免反复超时
_disabled_geocoders = set()


def get_city_center(city: str) -> tuple:
    """获取城市中心坐标，用于异常检测"""
    if city in CITY_CENTERS:
        return CITY_CENTERS[city]
    for k, v in CITY_CENTERS.items():
        if k in city or city in k:
            return v
    return None, None


def geocode(address: str, city_hint: str = "") -> tuple:
    """
    地理编码，返回 (lat, lon) 或 (None, None)。
    city_hint: 可选的城市名，用于：
      1. 给地址补充城市前缀提升准确度
      2. 对结果做异常检测
    """
    # 如果地址中不含城市名且有 city_hint，自动补全
    full_address = address
    if city_hint and city_hint not in address:
        full_address = f"{city_hint}{address}"

    geocoders = [
        ("amap_api", lambda addr: geocode_amap_api(addr)),      # 首选：高德 REST API（需 Key）
        ("baidu_api", lambda addr: geocode_baidu_api(addr)),     # 备选：百度 REST API（需 Key）
        ("amap_web", lambda addr: geocode_amap_web(addr)),       # 免费首选：高德 Web POI 搜索
        ("tencent_web", lambda addr: geocode_tencent_web(addr, city_hint)),  # 免费备选：腾讯 Web POI 搜索
        ("photon", lambda addr: geocode_photon(addr)),           # 最终兜底：Photon
    ]

    center_lat, center_lon = get_city_center(city_hint) if city_hint else (None, None)

    for name, func in geocoders:
        if name in _disabled_geocoders:
            continue
        try:
            lat, lon = func(full_address)
        except Exception:
            _disabled_geocoders.add(name)
            continue
        if lat is not None and lon is not None:
            # 异常检测：结果偏离城市中心 > 50km 则丢弃
            if center_lat is not None:
                dist_to_center = _haversine(lat, lon, center_lat, center_lon)
                if dist_to_center > 50:
                    continue
            return lat, lon

    # 如果补全了城市前缀但全部失败，用原始地址再试一次
    if full_address != address:
        for name, func in geocoders:
            if name in _disabled_geocoders:
                continue
            try:
                lat, lon = func(address)
            except Exception:
                _disabled_geocoders.add(name)
                continue
            if lat is not None and lon is not None:
                if center_lat is not None:
                    dist_to_center = _haversine(lat, lon, center_lat, center_lon)
                    if dist_to_center > 50:
                        continue
                return lat, lon

    return None, None


# ───────────────── 距离计算 ─────────────────

def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Haversine 公式计算两点间直线距离（公里）。参数: (纬度1, 经度1, 纬度2, 经度2)"""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """公开接口，参数: (纬度1, 经度1, 纬度2, 经度2)"""
    return _haversine(lat1, lon1, lat2, lon2)


# ───────────────── 交通估算 ─────────────────

def estimate_transport(distance_km: float, weather_tag: str = "good") -> dict:
    """根据距离和天气估算交通方案"""
    walk_min = distance_km * 13
    drive_min = max(3, distance_km * 3 + 2)
    taxi_cost = 11 if distance_km <= 3 else 11 + (distance_km - 3) * 2.5

    if weather_tag == "bad":
        recommended = "打车"
        walk_min = None
    elif distance_km < 1:
        recommended = "步行"
    elif distance_km <= 3:
        recommended = "步行或打车"
    else:
        recommended = "打车"

    result = {
        "estimated_distance_km": round(distance_km, 2),
        "time_estimates": {
            "walk_min": round(walk_min) if walk_min else None,
            "drive_min": round(drive_min),
        },
        "cost_estimates": {
            "taxi_yuan": round(taxi_cost, 1),
        },
        "recommended": recommended,
    }
    if weather_tag == "bad":
        result["weather_adjustment"] = "恶劣天气，建议全程打车"
    return result


# ───────────────── 单段路线 ─────────────────

def single_route(start: str, end: str, weather_tag: str = "good", city: str = "") -> dict:
    """查询单段路线"""
    lat1, lon1 = geocode(start, city)
    lat2, lon2 = geocode(end, city)

    geocoded = lat1 is not None and lat2 is not None
    if geocoded:
        distance = haversine(lat1, lon1, lat2, lon2)
    else:
        distance = 2.0

    result = estimate_transport(distance, weather_tag)
    result["start"] = start
    result["end"] = end
    result["geocoded"] = geocoded
    if geocoded:
        result["start_coord"] = {"lat": lat1, "lon": lon1}
        result["end_coord"] = {"lat": lat2, "lon": lon2}

    if geocoded:
        summary(f"{start} → {end} | {distance:.1f}km | {result['recommended']}({result['time_estimates']['drive_min']}min)")
    else:
        summary(f"{start} → {end} | ~2.0km(估) | 地理编码失败，使用默认距离")

    return result


# ───────────────── 批量路线 ─────────────────

def batch_route(pois_file: str, start_point: str = "", weather_tag: str = "good", city: str = "") -> dict:
    """
    批量路线规划：
    1. 对所有 POI 做地理编码（带城市上下文 + 异常检测）
    2. 贪心最近邻算法排序
    3. 生成 N-1 个 segment（相邻 POI 之间的连接段）
    """
    with open(pois_file, "r", encoding="utf-8") as f:
        pois = json.load(f)

    if len(pois) == 0:
        summary("无 POI 输入")
        return {"error": "POI 列表为空", "ordered_pois": [], "segments": []}

    # 从 POI 地址中推断城市（如果未传入）
    if not city:
        for poi in pois:
            addr = poi.get("address", "")
            for c in CITY_CENTERS:
                if c in addr:
                    city = c
                    break
            if city:
                break

    # 地理编码所有 POI
    coords = []
    geocode_ok = 0
    geocode_fail = 0
    for poi in pois:
        addr = poi.get("address", poi.get("name", ""))
        lat, lon = geocode(addr, city)
        coords.append((lat, lon, poi))
        if lat is not None:
            geocode_ok += 1
        else:
            geocode_fail += 1
        time.sleep(0.3)  # 轻量限速（高德 web 接口较宽松）

    has_coords = geocode_ok > 0

    if not has_coords:
        default_dist = 2.0
        segments = []
        total_dist = 0
        total_cost = 0
        for i in range(len(pois) - 1):
            transport = estimate_transport(default_dist, weather_tag)
            segments.append({
                "from": pois[i].get("name", ""),
                "to": pois[i + 1].get("name", ""),
                "distance_km": default_dist,
                "geocoded": False,
                **transport,
            })
            total_dist += default_dist
            total_cost += transport["cost_estimates"]["taxi_yuan"]

        summary(f"{len(pois)}站 | 编码全失败 | 默认{default_dist}km/段 | 总~{round(total_dist, 1)}km")
        return {
            "ordered_pois": pois,
            "segments": segments,
            "total_distance_km": round(total_dist, 2),
            "total_cost_yuan": round(total_cost, 1),
            "weather_tag": weather_tag,
            "geocode_stats": {"ok": 0, "fail": len(pois)},
            "note": "地理编码不可用，使用默认距离估算",
        }

    # ── 贪心最近邻排序 ──
    if start_point:
        slat, slon = geocode(start_point, city)
        if slat is None:
            slat, slon = next((c[0], c[1]) for c in coords if c[0] is not None)
    else:
        slat, slon = next((c[0], c[1]) for c in coords if c[0] is not None)

    visited = [False] * len(coords)
    order = []
    cur_lat, cur_lon = slat, slon

    for _ in range(len(coords)):
        best_idx = -1
        best_dist = float("inf")
        for i, (lat, lon, _) in enumerate(coords):
            if visited[i] or lat is None:
                continue
            d = haversine(cur_lat, cur_lon, lat, lon)
            if d < best_dist:
                best_dist = d
                best_idx = i
        if best_idx >= 0:
            visited[best_idx] = True
            lat, lon, poi = coords[best_idx]
            order.append((poi, lat, lon))
            cur_lat, cur_lon = lat, lon

    # 把没有坐标的 POI 追加到末尾
    for i, (lat, lon, poi) in enumerate(coords):
        if not visited[i]:
            order.append((poi, None, None))

    # ── 生成 N-1 个 segment ──
    ordered_pois = [o[0] for o in order]
    segments = []
    total_dist = 0
    total_cost = 0

    for i in range(len(order) - 1):
        poi_a, lat_a, lon_a = order[i]
        poi_b, lat_b, lon_b = order[i + 1]

        if lat_a is not None and lat_b is not None:
            dist = haversine(lat_a, lon_a, lat_b, lon_b)
            geocoded = True
        else:
            dist = 2.0
            geocoded = False

        transport = estimate_transport(dist, weather_tag)
        segments.append({
            "from": poi_a.get("name", ""),
            "to": poi_b.get("name", ""),
            "distance_km": round(dist, 2),
            "geocoded": geocoded,
            **transport,
        })
        total_dist += dist
        total_cost += transport["cost_estimates"]["taxi_yuan"]

    summary(
        f"{len(ordered_pois)}站 | 编码{geocode_ok}/{geocode_ok + geocode_fail} | "
        f"总距离{round(total_dist, 1)}km | 预估¥{round(total_cost)}"
    )

    return {
        "ordered_pois": ordered_pois,
        "segments": segments,
        "total_distance_km": round(total_dist, 2),
        "total_cost_yuan": round(total_cost, 1),
        "weather_tag": weather_tag,
        "geocode_stats": {"ok": geocode_ok, "fail": geocode_fail},
    }


# ───────────────── CLI ─────────────────

def main():
    parser = argparse.ArgumentParser(description="路线规划与交通查询")
    parser.add_argument("start_or_file", help="起点地址 或 POI JSON 文件路径")
    parser.add_argument("end", nargs="?", default="", help="终点地址（单段模式）")
    parser.add_argument("--mode", default="", help="交通方式偏好")
    parser.add_argument("--batch", action="store_true", help="批量路线规划模式")
    parser.add_argument("--weather", default="good", help="天气标签（good/mild/bad）")
    parser.add_argument("--city", default="", help="城市名（提升地理编码准确度）")
    args = parser.parse_args()

    if args.batch:
        result = batch_route(args.start_or_file, args.end, args.weather, args.city)
    else:
        result = single_route(args.start_or_file, args.end, args.weather, args.city)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
