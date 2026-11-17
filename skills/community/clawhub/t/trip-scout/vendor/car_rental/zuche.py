"""
神州租车网点查询

通过 C 端公开 JSON API 获取城市列表和网点列表。
仅需 Referer 头，无需登录/Cookie/签名。

API 端点:
  - 城市列表: POST https://www.zuche.com/api/gw.do?uri=/action/carrctapi/order/cityList/v1
  - 网点列表: POST https://www.zuche.com/api/gw.do?uri=/action/carrctapi/order/deptList/v1
"""

from __future__ import annotations

import json
from typing import Any
from urllib.parse import quote

import requests

from .models import StoreInfo


_BASE_URL = "https://www.zuche.com/api/gw.do"
_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/126.0.0.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "https://www.zuche.com/",
    "Origin": "https://www.zuche.com",
}

# 模块级缓存: {城市名: cityId}
_city_cache: dict[str, str] | None = None


def _get_city_list() -> dict[str, str]:
    """获取神州租车全量城市列表，返回 {城市名: cityId}"""
    global _city_cache
    if _city_cache is not None:
        return _city_cache

    resp = requests.post(
        _BASE_URL,
        params={"uri": "/action/carrctapi/order/cityList/v1"},
        data="data=%7B%7D",
        headers=_HEADERS,
        timeout=15,
    )
    data = resp.json()
    if data.get("code") != 1:
        raise RuntimeError(f"神州租车城市列表API异常: code={data.get('code')}, msg={data.get('busiCode')}")

    content = data.get("content", {})
    mapping: dict[str, str] = {}

    for city in content.get("hotCities", []):
        name = city.get("cityName", "")
        cid = city.get("cityId", "")
        if name and cid:
            mapping[name] = cid

    all_cities = content.get("allCities", {})
    if isinstance(all_cities, dict):
        for _letter, cities in all_cities.items():
            if isinstance(cities, list):
                for city in cities:
                    name = city.get("cityName", "")
                    cid = city.get("cityId", "")
                    if name and cid:
                        mapping[name] = cid
    elif isinstance(all_cities, list):
        for city in all_cities:
            name = city.get("cityName", "")
            cid = city.get("cityId", "")
            if name and cid:
                mapping[name] = cid

    _city_cache = mapping
    return mapping


def _resolve_city_id(city_name: str) -> str:
    """城市名 -> cityId，支持精确匹配和包含匹配"""
    cities = _get_city_list()

    # 精确匹配
    if city_name in cities:
        return cities[city_name]

    # 包含匹配（如"乌鲁木齐市" -> "乌鲁木齐"）
    for name, cid in cities.items():
        if city_name in name or name in city_name:
            return cid

    raise ValueError(f"神州租车未找到城市: {city_name}")


def _parse_store(dept: dict[str, Any], district_name: str | None = None) -> StoreInfo:
    """将神州 API 网点 JSON 映射为 StoreInfo"""
    name = dept.get("deptName", "") or ""
    in_station = dept.get("inStationFlag", 0)

    # 机场/火车站推断（inStationFlag==1 表示机场店内；名称关键词兜底，
    # 因为实测大量机场店 inStationFlag 为 0，需靠名称识别）
    is_airport = in_station in (1, "1") or "机场" in name
    is_train = any(k in name for k in ("高铁", "火车站", "动车"))

    return StoreInfo(
        name=name,
        address=dept.get("deptAddress") or "",
        phone=dept.get("deptPhone") or dept.get("servicePhone") or "",
        work_time=dept.get("workTime") or dept.get("specialWorkTime") or "",
        source="zuche",
        lat=dept.get("deptLat") or None,
        lon=dept.get("deptLon") or None,
        district=district_name,
        is_self_service=bool(dept.get("selfServiceFlag")),
        is_airport=is_airport,
        is_train_station=is_train,
    )


def get_stores(city_name: str) -> list[StoreInfo]:
    """查询神州租车某城市的全部网点"""
    city_name = (city_name or "").strip()
    if not city_name:
        raise ValueError("城市名不能为空")

    city_id = _resolve_city_id(city_name)

    # body 需与 cityList 一致做 URL 编码（data=<encoded JSON>）
    body_json = json.dumps(
        {"cityId": city_id, "entrance": 1, "pickupFlag": 1}, separators=(",", ":")
    )
    resp = requests.post(
        _BASE_URL,
        params={"uri": "/action/carrctapi/order/deptList/v1"},
        data=f"data={quote(body_json, safe='')}",
        headers=_HEADERS,
        timeout=15,
    )
    data = resp.json()
    if data.get("code") != 1:
        raise RuntimeError(f"神州租车网点列表API异常: code={data.get('code')}, msg={data.get('busiCode')}")

    stores: list[StoreInfo] = []
    for district in data.get("content", {}).get("districtList", []):
        district_name = district.get("districtName")
        for dept in district.get("deptList", []):
            stores.append(_parse_store(dept, district_name))

    return stores
