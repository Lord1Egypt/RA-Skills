#!/usr/bin/env python3
"""
雪场发现与数据库更新工具（只读查询 + 可选本地合并）
用法:
  python tools/resort_discovery.py discover '<json>'
  python tools/resort_discovery.py update-db

discover: 通过 OpenStreetMap Overpass API 搜索全球滑雪场，与本地数据库对比
update-db: 从 GitHub 拉取最新 resorts_db.json（仅用户显式触发）

网络请求（仅用户显式调用时触发，无后台自动联网）:
  - Overpass API (overpass-api.de, overpass.kumi.systems) — OSM 雪场查询
  - Nominatim (nominatim.openstreetmap.org) — 降级搜索
  - Open-Meteo Elevation API — 海拔补充
  - GitHub Raw (raw.githubusercontent.com) — 数据库同步（仅 update-db）

安全说明:
  - 所有网络请求仅在用户明确运行 discover 或 update-db 命令时触发
  - 不发送用户个人信息，仅查询公开的地理数据
  - 不执行任何外部脚本或二进制文件
  - _save_db() 仅修改本 skill 自带的 data/resorts_db.json 文件

v5.1: 扩展 60+ 搜索区域，覆盖欧洲 17 国、东欧、南美、澳洲等
"""

import json
import math
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta

# ─── 路径常量 ───

_TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
_SKILL_DIR = os.path.dirname(_TOOL_DIR)
_DATA_DIR = os.path.join(_SKILL_DIR, "data")
_DB_PATH = os.path.join(_DATA_DIR, "resorts_db.json")

# ─── 网络常量 ───

_GITHUB_RAW_URL = "https://raw.githubusercontent.com/wjyhahaha/ski-assistant/main/data/resorts_db.json"

_OVERPASS_MIRRORS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]

_NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

_UA = "ski-assistant/5.1"

# ─── 预定义搜索区域 ───

_DISCOVERY_REGIONS = {
    # 中国
    "中国-崇礼": {"bbox": (40.5, 115.0, 41.2, 116.0), "country": "CN", "region_hint": "河北·崇礼"},
    "中国-北京延庆": {"bbox": (40.3, 115.7, 40.8, 116.8), "country": "CN", "region_hint": "北京"},
    "中国-张家口北": {"bbox": (41.0, 114.5, 42.0, 116.0), "country": "CN", "region_hint": "河北"},
    "中国-吉林": {"bbox": (42.5, 126.0, 44.5, 128.5), "country": "CN", "region_hint": "吉林"},
    "中国-黑龙江": {"bbox": (44.0, 126.5, 46.5, 129.0), "country": "CN", "region_hint": "黑龙江"},
    "中国-辽宁": {"bbox": (40.5, 123.0, 42.5, 125.5), "country": "CN", "region_hint": "辽宁"},
    "中国-新疆阿勒泰": {"bbox": (47.0, 86.5, 48.5, 89.0), "country": "CN", "region_hint": "新疆"},
    "中国-四川": {"bbox": (28.0, 101.0, 32.0, 104.5), "country": "CN", "region_hint": "四川"},
    "中国-云南": {"bbox": (26.0, 100.0, 28.5, 103.0), "country": "CN", "region_hint": "云南"},
    # 日本
    "日本-北海道西": {"bbox": (42.5, 139.5, 44.0, 142.0), "country": "JP", "region_hint": "北海道"},
    "日本-北海道东": {"bbox": (42.5, 142.0, 44.0, 145.0), "country": "JP", "region_hint": "北海道"},
    "日本-东北": {"bbox": (38.5, 139.0, 40.5, 141.0), "country": "JP", "region_hint": "本州东北"},
    "日本-中部北": {"bbox": (36.0, 137.5, 38.0, 140.0), "country": "JP", "region_hint": "本州中部"},
    "日本-中部南": {"bbox": (35.5, 136.0, 37.0, 138.5), "country": "JP", "region_hint": "本州中部"},
    "日本-关东": {"bbox": (35.8, 138.0, 37.0, 139.5), "country": "JP", "region_hint": "关东"},
    # 韩国
    "韩国-江原道": {"bbox": (37.3, 127.8, 38.3, 129.0), "country": "KR", "region_hint": "江原道"},
    # 法国
    "法国-萨瓦": {"bbox": (45.0, 6.0, 46.0, 7.2), "country": "FR", "region_hint": "法国阿尔卑斯"},
    "法国-上萨瓦": {"bbox": (45.7, 6.2, 46.5, 7.0), "country": "FR", "region_hint": "法国阿尔卑斯"},
    "法国-上阿尔卑斯": {"bbox": (44.5, 6.0, 45.2, 6.8), "country": "FR", "region_hint": "法国阿尔卑斯"},
    "法国-比利牛斯": {"bbox": (42.5, 0.0, 43.0, 2.0), "country": "FR", "region_hint": "法国比利牛斯"},
    # 瑞士
    "瑞士-瓦莱": {"bbox": (46.0, 7.0, 46.5, 8.5), "country": "CH", "region_hint": "瑞士"},
    "瑞士-格劳宾登": {"bbox": (46.5, 9.5, 47.0, 10.5), "country": "CH", "region_hint": "瑞士"},
    "瑞士-伯尔尼": {"bbox": (46.5, 7.5, 46.8, 8.2), "country": "CH", "region_hint": "瑞士"},
    "瑞士-中部": {"bbox": (46.8, 8.2, 47.2, 8.8), "country": "CH", "region_hint": "瑞士中部"},
    # 奥地利
    "奥地利-蒂罗尔": {"bbox": (46.8, 10.5, 47.5, 12.5), "country": "AT", "region_hint": "奥地利"},
    "奥地利-萨尔茨堡": {"bbox": (47.0, 12.5, 47.8, 14.0), "country": "AT", "region_hint": "奥地利"},
    "奥地利-福拉尔贝格": {"bbox": (47.0, 9.7, 47.5, 10.5), "country": "AT", "region_hint": "奥地利"},
    "奥地利-施蒂利亚": {"bbox": (47.3, 13.5, 47.8, 14.5), "country": "AT", "region_hint": "奥地利"},
    # 意大利
    "意大利-多洛米蒂": {"bbox": (46.2, 11.0, 47.0, 12.5), "country": "IT", "region_hint": "意大利北部"},
    "意大利-瓦莱达奥斯塔": {"bbox": (45.5, 7.0, 46.0, 7.8), "country": "IT", "region_hint": "意大利西北部"},
    "意大利-皮埃蒙特": {"bbox": (45.0, 7.5, 45.5, 8.5), "country": "IT", "region_hint": "意大利西北部"},
    "意大利-伦巴第": {"bbox": (46.0, 9.8, 46.5, 10.5), "country": "IT", "region_hint": "意大利北部"},
    "意大利-特伦蒂诺": {"bbox": (46.0, 10.8, 46.5, 11.5), "country": "IT", "region_hint": "意大利北部"},
    "意大利-威尼托": {"bbox": (46.3, 11.5, 46.8, 12.2), "country": "IT", "region_hint": "意大利东北部"},
    # 德国
    "德国-巴伐利亚": {"bbox": (47.3, 10.0, 47.7, 11.5), "country": "DE", "region_hint": "德国"},
    # 西班牙/安道尔
    "西班牙-比利牛斯": {"bbox": (42.4, 0.8, 42.8, 1.8), "country": "ES", "region_hint": "西班牙"},
    "安道尔": {"bbox": (42.5, 1.4, 42.7, 1.8), "country": "AD", "region_hint": "安道尔"},
    # 北欧
    "挪威-南部": {"bbox": (60.0, 7.5, 62.0, 10.5), "country": "NO", "region_hint": "挪威"},
    "挪威-中部": {"bbox": (62.0, 6.0, 63.0, 8.0), "country": "NO", "region_hint": "挪威"},
    "瑞典": {"bbox": (62.5, 12.5, 64.0, 14.0), "country": "SE", "region_hint": "瑞典"},
    "芬兰": {"bbox": (67.5, 24.5, 68.5, 25.5), "country": "FI", "region_hint": "芬兰"},
    # 东欧
    "斯洛文尼亚": {"bbox": (46.2, 13.5, 46.5, 14.0), "country": "SI", "region_hint": "斯洛文尼亚"},
    "斯洛伐克-塔特拉": {"bbox": (49.0, 19.3, 49.3, 20.2), "country": "SK", "region_hint": "斯洛伐克"},
    "捷克-克尔科诺谢": {"bbox": (50.6, 15.4, 50.9, 15.9), "country": "CZ", "region_hint": "捷克"},
    "波兰-塔特拉": {"bbox": (49.2, 19.7, 49.5, 20.2), "country": "PL", "region_hint": "波兰"},
    "罗马尼亚-喀尔巴阡": {"bbox": (45.5, 25.3, 45.8, 25.7), "country": "RO", "region_hint": "罗马尼亚"},
    "保加利亚-皮林": {"bbox": (41.6, 23.3, 41.8, 23.6), "country": "BG", "region_hint": "保加利亚"},
    "俄罗斯-索契": {"bbox": (43.6, 40.0, 43.8, 40.5), "country": "RU", "region_hint": "俄罗斯"},
    # 北美
    "美国-科罗拉多北": {"bbox": (39.3, -107.0, 40.0, -105.5), "country": "US", "region_hint": "科罗拉多"},
    "美国-科罗拉多南": {"bbox": (38.5, -107.0, 39.3, -105.5), "country": "US", "region_hint": "科罗拉多"},
    "美国-犹他": {"bbox": (40.2, -112.0, 41.2, -111.0), "country": "US", "region_hint": "犹他"},
    "美国-太浩湖": {"bbox": (38.7, -120.3, 39.4, -119.7), "country": "US", "region_hint": "加州"},
    "美国-怀俄明": {"bbox": (43.3, -111.0, 43.8, -110.5), "country": "US", "region_hint": "怀俄明"},
    "美国-蒙大拿": {"bbox": (45.0, -111.8, 45.5, -111.0), "country": "US", "region_hint": "蒙大拿"},
    "美国-佛蒙特": {"bbox": (43.5, -73.0, 44.5, -72.5), "country": "US", "region_hint": "佛蒙特"},
    "加拿大-惠斯勒": {"bbox": (49.5, -123.5, 50.5, -121.5), "country": "CA", "region_hint": "BC省"},
    "加拿大-落基山": {"bbox": (51.0, -116.0, 51.5, -115.5), "country": "CA", "region_hint": "阿尔伯塔"},
    "加拿大-魁北克": {"bbox": (47.5, -71.0, 48.0, -70.0), "country": "CA", "region_hint": "魁北克"},
    # 南半球
    "新西兰-南岛": {"bbox": (-44.5, 168.5, -43.0, 171.5), "country": "NZ", "region_hint": "南岛"},
    "新西兰-北岛": {"bbox": (-39.5, 175.5, -39.0, 176.5), "country": "NZ", "region_hint": "北岛"},
    "澳大利亚-新南威尔士": {"bbox": (-36.5, 148.0, -35.5, 148.5), "country": "AU", "region_hint": "澳洲"},
    "澳大利亚-维多利亚": {"bbox": (-37.0, 146.0, -36.5, 147.0), "country": "AU", "region_hint": "澳洲"},
    # 南美
    "智利-安第斯": {"bbox": (-33.0, -70.5, -32.5, -70.0), "country": "CL", "region_hint": "智利"},
    "阿根廷-安第斯": {"bbox": (-35.5, -70.5, -35.0, -70.0), "country": "AR", "region_hint": "阿根廷"},
    # 中东
    "阿联酋": {"bbox": (25.5, 55.3, 26.0, 55.8), "country": "AE", "region_hint": "阿联酋"},
}


# ─── 工具函数 ───

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """计算两个经纬度之间的距离（公里）"""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _fetch_json(url: str, retries: int = 2) -> dict:
    """带重试的 JSON 请求"""
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception:
            if attempt < retries:
                time.sleep(1 * (attempt + 1))
            else:
                raise


def _load_db() -> dict:
    """加载本地雪场数据库"""
    try:
        with open(_DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"_meta": {"version": "0.0.0", "updated": "", "source": ""}}


def _save_db(db: dict):
    """保存雪场数据库"""
    os.makedirs(_DATA_DIR, exist_ok=True)
    with open(_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


# ─── Overpass / Nominatim 查询 ───

def _query_overpass(bbox: tuple, timeout: int = 25) -> list:
    """通过 Overpass API 查询指定区域内的滑雪场，自动重试多个节点。"""
    south, west, north, east = bbox
    query = f"""
[out:json][timeout:{timeout}];
(
  way["landuse"="winter_sports"]({south},{west},{north},{east});
  relation["landuse"="winter_sports"]({south},{west},{north},{east});
  relation["site"="piste"]({south},{west},{north},{east});
);
out center tags;
"""
    data = f"data={query}".encode("utf-8")
    last_err = None

    for attempt, mirror in enumerate(_OVERPASS_MIRRORS):
        try:
            req = urllib.request.Request(mirror, data=data, method="POST",
                                        headers={"User-Agent": _UA})
            with urllib.request.urlopen(req, timeout=timeout + 10) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            return result.get("elements", [])
        except Exception as e:
            last_err = e
            if attempt < len(_OVERPASS_MIRRORS) - 1:
                time.sleep(3)

    # 所有节点失败，延迟后最终重试
    time.sleep(8)
    try:
        req = urllib.request.Request(_OVERPASS_MIRRORS[0], data=data, method="POST",
                                    headers={"User-Agent": _UA})
        with urllib.request.urlopen(req, timeout=timeout + 15) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        return result.get("elements", [])
    except Exception:
        raise last_err or Exception("所有 Overpass 节点不可用")


def _query_nominatim_fallback(bbox: tuple, overpass_err) -> list:
    """Overpass 不可用时，使用 Nominatim 搜索 ski resort 作为降级方案。"""
    south, west, north, east = bbox
    all_elements = []
    seen_ids = set()
    for keyword in ["ski resort", "ski area", "滑雪场", "スキー場"]:
        params = {
            "q": keyword,
            "format": "json",
            "viewbox": f"{west},{north},{east},{south}",
            "bounded": 1,
            "limit": 30,
            "addressdetails": 1,
        }
        url = _NOMINATIM_URL + "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"User-Agent": _UA})
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                results = json.loads(resp.read().decode("utf-8"))
            for r in results:
                osm_id = r.get("osm_id", 0)
                if osm_id in seen_ids:
                    continue
                seen_ids.add(osm_id)
                elem = {
                    "type": "nominatim",
                    "id": osm_id,
                    "lat": float(r.get("lat", 0)),
                    "lon": float(r.get("lon", 0)),
                    "tags": {
                        "name": r.get("display_name", "").split(",")[0].strip(),
                        "source": "nominatim",
                    },
                }
                addr = r.get("address", {})
                if addr.get("country_code"):
                    elem["tags"]["country_code"] = addr["country_code"].upper()
                all_elements.append(elem)
            time.sleep(1.1)  # Nominatim 要求 1 请求/秒
        except Exception:
            continue

    if all_elements:
        return all_elements
    if overpass_err:
        raise overpass_err
    return []


# ─── 海拔查询 ───

def _fetch_elevation(lat: float, lon: float):
    """通过 Open-Meteo Elevation API 获取指定坐标的海拔高度。"""
    url = f"https://api.open-meteo.com/v1/elevation?latitude={lat}&longitude={lon}"
    try:
        data = _fetch_json(url)
        elevations = data.get("elevation", [])
        if elevations:
            return int(elevations[0])
    except Exception:
        pass
    return None


# ─── OSM 结果处理 ───

def _deduplicate_osm_results(elements: list) -> list:
    """对 OSM 结果按名称去重，优先保留 relation 类型。"""
    seen = {}
    for e in elements:
        name = e.get("tags", {}).get("name", "").strip()
        if not name:
            continue
        key = name.lower()
        existing = seen.get(key)
        if existing is None:
            seen[key] = e
        elif e.get("type") == "relation" and existing.get("type") != "relation":
            seen[key] = e
    return list(seen.values())


def _osm_element_to_resort(element: dict, country: str, region_hint: str) -> tuple:
    """将 OSM 元素转换为雪场数据格式。返回 (name, resort_dict)。"""
    tags = element.get("tags", {})
    center = element.get("center", {})
    lat = center.get("lat") or element.get("lat")
    lon = center.get("lon") or element.get("lon")

    name = tags.get("name", "")
    name_en = tags.get("name:en", "")
    website = tags.get("website") or tags.get("url") or tags.get("contact:website", "")
    is_nominatim = element.get("type") == "nominatim"

    resort = {
        "region": region_hint.split("/")[0] if "/" in region_hint else region_hint,
        "country": country,
        "latitude": round(lat, 4) if lat else None,
        "longitude": round(lon, 4) if lon else None,
        "source": "Nominatim" if is_nominatim else "OpenStreetMap-Overpass",
        "osm_id": f"{element.get('type', '?')}/{element.get('id', '?')}",
        "auto_discovered": True,
        "_needs_review": True,
    }
    if not is_nominatim:
        resort["osm_tags"] = {k: v for k, v in tags.items()
                              if k not in ("name", "name:en", "name:zh", "landuse", "type", "source")}
    if name_en:
        resort["name_en"] = name_en
    if website:
        resort["website"] = website

    return name, resort


# ─── 核心命令 ───

CST = timezone(timedelta(hours=8))


def discover_resorts(params: dict) -> str:
    """
    联网发现新雪场。
    参数:
      region - 搜索区域: "中国", "日本", "欧洲", "北美", "全部"，或具体如 "中国-崇礼"
      enrich - 是否补充海拔数据 (默认 true)
      merge  - 是否合并到本地数据库 (默认 false，仅预览)
      limit  - 单区域最大返回数量 (默认 50)
    """
    region_filter = params.get("region", "全部").strip()
    enrich = params.get("enrich", True)
    auto_merge = params.get("merge", False)
    limit = params.get("limit", 50)

    # 匹配搜索区域
    target_regions = {}
    if region_filter == "全部":
        target_regions = _DISCOVERY_REGIONS
    else:
        for name, info in _DISCOVERY_REGIONS.items():
            region_prefix = region_filter.rstrip("-")
            if (name == region_filter
                or name.startswith(region_prefix + "-")
                or region_filter in name
                or region_filter == info["country"]):
                target_regions[name] = info
    if not target_regions:
        avail = ", ".join(sorted(_DISCOVERY_REGIONS.keys()))
        return f"未知区域: {region_filter}\n可选区域: {avail}"

    # 加载本地数据库
    all_resorts = _load_db()
    existing_names = set()
    existing_coords = []
    for k, v in all_resorts.items():
        if k == "_meta" or not isinstance(v, dict):
            continue
        existing_names.add(k.lower())
        if "latitude" in v and "longitude" in v:
            existing_coords.append((v["latitude"], v["longitude"], k))

    lines = ["OpenStreetMap 雪场发现报告\n"]
    lines.append(f"搜索区域: {', '.join(target_regions.keys())}")
    lines.append(f"数据源: Overpass API -> Nominatim (备选)")
    lines.append(f"本地数据库现有: {len(existing_names)} 个雪场\n")

    all_discovered = []
    all_new = []
    all_matched = []
    errors = []
    data_sources_used = set()

    for region_name, region_info in sorted(target_regions.items()):
        lines.append(f"--- {region_name} ---")
        try:
            try:
                elements = _query_overpass(region_info["bbox"])
                elements = _deduplicate_osm_results(elements)
                data_sources_used.add("Overpass")
            except Exception as oe:
                elements = _query_nominatim_fallback(region_info["bbox"], oe)
                data_sources_used.add("Nominatim")

            src = "Nominatim" if any(e.get("type") == "nominatim" for e in elements) else "Overpass"
            lines.append(f"  {src} 返回: {len(elements)} 个滑雪区域")

            region_new = []
            region_matched = []

            for elem in elements[:limit]:
                name, resort_data = _osm_element_to_resort(
                    elem, region_info["country"], region_info["region_hint"])
                if not name or resort_data["latitude"] is None:
                    continue

                all_discovered.append(name)

                # 重复检测（名称模糊匹配 + 坐标距离匹配）
                is_existing = False
                matched_name = None

                name_lower = name.lower()
                name_zh = elem.get("tags", {}).get("name:zh", "").lower()
                for ek, ev in all_resorts.items():
                    if ek == "_meta" or not isinstance(ev, dict):
                        continue
                    existing = ek.lower()
                    existing_en = str(ev.get("name_en", "")).lower()
                    paren_name = ""
                    if "（" in existing and "）" in existing:
                        paren_name = existing.split("（")[1].split("）")[0].strip()
                    elif "(" in existing and ")" in existing:
                        paren_name = existing.split("(")[1].split(")")[0].strip()
                    # 精确匹配
                    if name_lower == existing or name_lower == existing_en:
                        is_existing, matched_name = True, ek
                        break
                    # 包含关系（至少4字符）
                    candidates = [existing, existing_en, paren_name]
                    for a in [name_lower, name_zh]:
                        for b in candidates:
                            if a and b and len(a) >= 4 and len(b) >= 4 and (a in b or b in a):
                                is_existing, matched_name = True, ek
                                break
                        if is_existing:
                            break
                    if is_existing:
                        break

                # 坐标匹配（1.5km 内视为同一雪场）
                if not is_existing and resort_data["latitude"] and resort_data["longitude"]:
                    for elat, elon, ename in existing_coords:
                        dist = haversine(resort_data["latitude"], resort_data["longitude"], elat, elon)
                        if dist < 1.5:
                            is_existing, matched_name = True, ename
                            break

                if is_existing:
                    region_matched.append((name, matched_name))
                    all_matched.append(name)
                else:
                    region_new.append((name, resort_data))
                    all_new.append((name, resort_data))

            if region_new:
                lines.append(f"  NEW ({len(region_new)}):")
                for rname, _ in region_new:
                    lines.append(f"    - {rname}")
            if region_matched:
                lines.append(f"  MATCHED ({len(region_matched)}):")
                for rname, mname in region_matched[:5]:
                    lines.append(f"    - {rname} -> {mname}")
                if len(region_matched) > 5:
                    lines.append(f"    ... and {len(region_matched)-5} more")
            if not region_new and not region_matched:
                lines.append("  (no new resorts found)")
            lines.append("")

            time.sleep(1)  # 避免 API 速率限制

        except Exception as ex:
            errors.append(f"{region_name}: {ex}")
            lines.append(f"  ERROR: {ex}\n")

    # 海拔补充
    if enrich and all_new:
        lines.append("--- Elevation Enrichment ---")
        enriched = 0
        for name, resort_data in all_new:
            if resort_data["latitude"] and resort_data["longitude"]:
                elev = _fetch_elevation(resort_data["latitude"], resort_data["longitude"])
                if elev is not None:
                    resort_data["elevation_base"] = elev
                    resort_data["elevation_top"] = elev + 300  # 粗估，需人工校准
                    enriched += 1
                time.sleep(0.3)
        lines.append(f"  Enriched: {enriched}/{len(all_new)}\n")

    # 合并
    merged_count = 0
    if auto_merge and all_new:
        db = _load_db()
        for name, resort_data in all_new:
            if name not in db:
                db[name] = resort_data
                merged_count += 1
        db["_meta"]["updated"] = datetime.now(CST).strftime("%Y-%m-%d")
        db["_meta"]["source"] = db["_meta"].get("source", "") + " + OSM auto-discover"
        _save_db(db)
        lines.append(f"Merged: {merged_count} new resorts into local DB")
        lines.append("Note: new resorts marked _needs_review=true\n")

    # 汇总
    lines.append("--- Summary ---")
    lines.append(f"OSM total found: {len(all_discovered)}")
    lines.append(f"Matched existing: {len(all_matched)}")
    lines.append(f"New discovered: {len(all_new)}")
    if auto_merge:
        lines.append(f"Merged to DB: {merged_count}")
    if errors:
        lines.append(f"Errors: {len(errors)}")

    # JSON 结果（供 Agent 解析）
    result = {
        "total_found": len(all_discovered),
        "matched": len(all_matched),
        "new": len(all_new),
        "merged": merged_count,
        "errors": errors,
        "new_resorts": [{"name": n, "latitude": d.get("latitude"), "longitude": d.get("longitude"),
                         "country": d.get("country"), "region": d.get("region")}
                        for n, d in all_new],
        "data_sources": sorted(data_sources_used),
    }
    lines.append("\n<!-- DISCOVER_JSON -->")
    lines.append(json.dumps(result, ensure_ascii=False))

    return "\n".join(lines)


def update_db() -> str:
    """从 GitHub 拉取最新 resorts_db.json 并更新本地数据库。"""
    import shutil

    # 备份
    backup_path = _DB_PATH + ".bak"
    if os.path.exists(_DB_PATH):
        shutil.copy2(_DB_PATH, backup_path)

    try:
        data = _fetch_json(_GITHUB_RAW_URL)
    except Exception as e:
        return json.dumps({"error": f"拉取失败: {e}"}, ensure_ascii=False)

    if not isinstance(data, dict) or "_meta" not in data:
        return json.dumps({"error": "远程文件格式异常（缺少 _meta）"}, ensure_ascii=False)

    # 对比版本
    local_data = _load_db()
    local_ver = local_data.get("_meta", {}).get("version", "0.0.0")
    local_updated = local_data.get("_meta", {}).get("updated", "")
    local_count = sum(1 for k, v in local_data.items() if k != "_meta" and isinstance(v, dict) and "latitude" in v)

    remote_ver = data.get("_meta", {}).get("version", "0.0.0")
    remote_updated = data.get("_meta", {}).get("updated", "")
    remote_count = sum(1 for k, v in data.items() if k != "_meta" and isinstance(v, dict) and "latitude" in v)

    # 写入
    _save_db(data)

    new_resorts = set(k for k, v in data.items() if k != "_meta" and isinstance(v, dict) and "latitude" in v)
    old_resorts = set(k for k, v in local_data.items() if k != "_meta" and isinstance(v, dict) and "latitude" in v) if local_count > 0 else set()
    added = sorted(new_resorts - old_resorts)
    removed = sorted(old_resorts - new_resorts)

    result = {
        "success": True,
        "version": {"old": local_ver, "new": remote_ver},
        "updated": {"old": local_updated, "new": remote_updated},
        "count": {"old": local_count, "new": remote_count},
        "added": added,
        "removed": removed,
        "backup": backup_path,
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


# ─── 主入口 ───

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "discover":
        params = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
        print(discover_resorts(params))
    elif cmd == "update-db":
        print(update_db())
    else:
        print(f"未知命令: {cmd}")
        print(__doc__)
        sys.exit(1)
