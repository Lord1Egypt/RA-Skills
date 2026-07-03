#!/usr/bin/env python3
"""
开店选址综合分析脚本
基于高德地图API，从人流量、用户群体、客流特点、消费情况、竞品情况五大维度
对目标地址进行开店选址综合评估，输出结构化JSON分析数据。

Usage:
    python analyze_location.py --address "北京市朝阳区三里屯太古里" --store-type "奶茶店" [--radius 1000] [--amap-key YOUR_KEY]

Output: JSON structure with all analysis dimensions
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
import os
from typing import Optional

# ============================================================
# 高德地图 Web服务 API 封装
# ============================================================

AMAP_BASE = "https://restapi.amap.com/v3"


def amap_request(endpoint: str, params: dict, api_key: str, retries: int = 3) -> dict:
    """通用高德API请求封装"""
    params["key"] = api_key
    params["output"] = "JSON"
    url = f"{AMAP_BASE}/{endpoint}?" + urllib.parse.urlencode(params)

    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "StoreLocationAnalysis/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if data.get("status") == "1":
                    return data
                else:
                    if attempt == retries - 1:
                        return {"status": "0", "info": data.get("info", "UNKNOWN_ERROR"), "raw": data}
        except Exception as e:
            if attempt == retries - 1:
                return {"status": "0", "info": str(e)}
            time.sleep(1)
    return {"status": "0", "info": "MAX_RETRIES_EXCEEDED"}


# ---- 1. 地理编码 ----
def geocode(address: str, api_key: str, city: str = "") -> Optional[dict]:
    """地址 → 经纬度坐标"""
    params = {"address": address}
    if city:
        params["city"] = city
    result = amap_request("geocode/geo", params, api_key)
    if result["status"] == "1" and result.get("geocodes"):
        geo = result["geocodes"][0]
        location = geo["location"].split(",")
        return {
            "lng": float(location[0]),
            "lat": float(location[1]),
            "formatted_address": geo.get("formatted_address", address),
            "adcode": geo.get("adcode", ""),
            "city": geo.get("city", ""),
            "district": geo.get("district", ""),
            "level": geo.get("level", ""),
        }
    return None


# ---- 2. 行政区查询 ----
def district_info(adcode: str, api_key: str) -> dict:
    """查询行政区信息"""
    result = amap_request("config/district", {"keywords": adcode, "subdistrict": 0}, api_key)
    if result["status"] == "1" and result.get("districts"):
        d = result["districts"][0]
        center = d["center"].split(",")
        return {
            "name": d.get("name", ""),
            "center": {"lng": float(center[0]), "lat": float(center[1])},
            "level": d.get("level", ""),
        }
    return {}


# ---- 3. 周边POI搜索 ----
POI_CATEGORIES = {
    # 居住
    "residential": {"keywords": "住宅小区|公寓|别墅", "types": "120300"},
    # 办公
    "office": {"keywords": "写字楼|商务楼|产业园区|创意园区", "types": "120200"},
    # 教育
    "education": {"keywords": "大学|中学|小学|幼儿园|培训机构", "types": "141200|141201|141203"},
    # 商业
    "commercial": {"keywords": "购物中心|商场|超市|便利店", "types": "060100|060400|060200"},
    # 餐饮
    "dining": {"keywords": "餐厅|饭店|小吃|咖啡厅|茶馆", "types": "050000"},
    # 交通
    "transport": {"keywords": "地铁站|公交站|火车站", "types": "150500|150700|150200"},
    # 医疗
    "medical": {"keywords": "医院|诊所|药店", "types": "090100|090200|090300"},
    # 娱乐
    "entertainment": {"keywords": "电影院|KTV|健身房|公园|景区", "types": "080100|080300|080500|110000"},
}


def search_around(lng: float, lat: float, keywords: str, api_key: str, radius: int = 1000,
                  types: str = "", offset: int = 50) -> list[dict]:
    """圆形区域POI搜索"""
    params = {
        "location": f"{lng},{lat}",
        "keywords": keywords,
        "radius": radius,
        "offset": offset,
        "page": 1,
        "extensions": "all",
    }
    if types:
        params["types"] = types

    result = amap_request("place/around", params, api_key)
    pois = []
    if result["status"] == "1" and result.get("pois"):
        for p in result["pois"]:
            ploc = p["location"].split(",")
            pois.append({
                "id": p.get("id", ""),
                "name": p.get("name", ""),
                "type": p.get("type", ""),
                "typecode": p.get("typecode", ""),
                "address": p.get("address", ""),
                "location": {"lng": float(ploc[0]), "lat": float(ploc[1])},
                "distance": int(p.get("distance", 0)),
                "biz_ext": p.get("biz_ext", {}),
            })
    return pois


def search_competitors(lng: float, lat: float, store_type: str, api_key: str, radius: int = 1000) -> list[dict]:
    """搜索竞品（同类店铺）"""
    all_competitors = []
    for page in range(1, 4):  # 最多3页
        params = {
            "location": f"{lng},{lat}",
            "keywords": store_type,
            "radius": radius,
            "offset": 25,
            "page": page,
            "extensions": "all",
        }
        result = amap_request("place/around", params, api_key)
        if result["status"] != "1":
            break
        pois = result.get("pois", [])
        if not pois:
            break
        for p in pois:
            ploc = p["location"].split(",")
            rating = p.get("biz_ext", {}).get("rating", "")
            all_competitors.append({
                "name": p.get("name", ""),
                "address": p.get("address", ""),
                "location": {"lng": float(ploc[0]), "lat": float(ploc[1])},
                "distance": int(p.get("distance", 0)),
                "rating": rating,
                "type": p.get("type", ""),
                "typecode": p.get("typecode", ""),
            })
    return all_competitors


# ---- 4. 交通态势 ----
def traffic_status(lng: float, lat: float, api_key: str, radius: int = 1000) -> dict:
    """查询圆形区域交通态势（作为实时人流量代理指标）"""
    result = amap_request("traffic/status/circle",
                          {"location": f"{lng},{lat}", "radius": min(radius, 5000)},
                          api_key)
    if result["status"] != "1":
        return {"available": False, "info": result.get("info", "")}

    evaluation = result.get("trafficinfo", {}).get("evaluation", {})
    description = evaluation.get("description", "")
    expedite = evaluation.get("expedite", "0%")
    congested = evaluation.get("congested", "0%")
    blocked = evaluation.get("blocked", "0%")
    unknown = evaluation.get("unknown", "0%")
    status_code = evaluation.get("status", "0")

    # 解析拥堵指数
    try:
        congestion_index = float(status_code)
    except (ValueError, TypeError):
        congestion_index = 0

    return {
        "available": True,
        "congestion_index": congestion_index,
        "description": description,
        "expedite_pct": expedite,
        "congested_pct": congested,
        "blocked_pct": blocked,
        "unknown_pct": unknown,
        # 状态: 0未知 1畅通 2缓行 3拥堵 4严重拥堵
        "status_text": {0: "未知", 1: "畅通", 2: "缓行", 3: "拥堵", 4: "严重拥堵"}.get(congestion_index, "未知"),
    }


# ---- 5. 周边设施聚类分析 ----
def analyze_surroundings(lng: float, lat: float, api_key: str, radius: int) -> dict:
    """综合分析周边配套设施"""
    results = {}
    total_pois = 0
    for category, config in POI_CATEGORIES.items():
        pois = search_around(lng, lat, config["keywords"], api_key, radius, types=config.get("types", ""))
        results[category] = {
            "count": len(pois),
            "top5": [{"name": p["name"], "distance": p["distance"]} for p in pois[:5]],
            "density_per_sqkm": round(len(pois) / (3.14159 * (radius / 1000) ** 2), 1) if radius > 0 else 0,
        }
        total_pois += len(pois)
    return {"categories": results, "total_pois": total_pois}


# ---- 6. 距离计算 ----
def haversine(lng1: float, lat1: float, lng2: float, lat2: float) -> float:
    """计算两点间距离(米)"""
    from math import radians, cos, sin, asin, sqrt
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    dlng = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlng / 2) ** 2
    return 2 * asin(sqrt(a)) * 6371000


# ---- 7. 多维度评分 ----
def compute_scores(geo_info: dict, surroundings: dict, traffic: dict,
                   competitors: list, store_type: str, radius: int) -> dict:
    """计算6维度选址评分 (0-100)"""
    scores = {}
    reasons = {}

    cats = surroundings["categories"]

    # ---- 7.1 人流量评分 (30%) ----
    # 结合交通拥堵指数 + POI总密度
    traffic_score = 0
    if traffic.get("available"):
        # 适中拥堵最佳 (太堵说明过度竞争，太畅通说明没人)
        ci = traffic.get("congestion_index", 0)
        if ci == 0:
            traffic_score = 50  # 未知按中等
        elif ci == 1:
            traffic_score = 35  # 太畅通，可能偏远
        elif ci == 2:
            traffic_score = 80  # 缓行 - 最佳
        elif ci == 3:
            traffic_score = 70  # 拥堵 - 人流量大但体验下降
        elif ci >= 4:
            traffic_score = 40  # 严重拥堵 - 过度拥堵

    total_pois = surroundings.get("total_pois", 0)
    density_score = min(100, total_pois / (radius / 200) * 25)  # 1000m范围50POI≈满分

    scores["foot_traffic"] = round(traffic_score * 0.5 + density_score * 0.5)
    reasons["foot_traffic"] = f"交通状态: {traffic.get('status_text', '未知')} | 周边POI总数: {total_pois}"

    # ---- 7.2 用户群体评分 (20%) ----
    # 根据居住+办公+教育POI密度判断目标客群丰富度
    residential_count = cats.get("residential", {}).get("count", 0)
    office_count = cats.get("office", {}).get("count", 0)
    education_count = cats.get("education", {}).get("count", 0)

    demo_raw = (residential_count * 0.4 + office_count * 0.35 + education_count * 0.25)
    demo_max = (radius / 200) * 3  # 1000m范围约15个POI满分
    scores["customer_demographics"] = round(min(100, demo_raw / max(demo_max, 1) * 100))
    reasons["customer_demographics"] = f"住宅: {residential_count}个 | 写字楼: {office_count}个 | 学校: {education_count}个"

    # ---- 7.3 客流特点评分 (15%) ----
    # 交通便利度（地铁站+公交站数量）
    transport_count = cats.get("transport", {}).get("count", 0)
    transport_score = min(100, transport_count * 15)
    scores["traffic_pattern"] = round(transport_score)
    reasons["traffic_pattern"] = f"地铁/公交站: {transport_count}个"

    # ---- 7.4 消费情况评分 (15%) ----
    # 商业密度 + 餐饮密度
    commercial_count = cats.get("commercial", {}).get("count", 0)
    dining_count = cats.get("dining", {}).get("count", 0)
    entertainment_count = cats.get("entertainment", {}).get("count", 0)

    consumption_raw = commercial_count * 0.25 + dining_count * 0.5 + entertainment_count * 0.25
    consumption_max = (radius / 200) * 4
    scores["spending_power"] = round(min(100, consumption_raw / max(consumption_max, 1) * 100))
    reasons["spending_power"] = f"商业设施: {commercial_count}个 | 餐饮: {dining_count}个 | 娱乐: {entertainment_count}个"

    # ---- 7.5 竞品分析评分 (15%) ----
    # 竞品越少分数越高（但0竞品也可能是市场空白=风险）
    competitor_count = len(competitors)
    if competitor_count == 0:
        comp_score = 50  # 空白市场，机会与风险并存
    elif competitor_count <= 3:
        comp_score = 90  # 轻度竞争
    elif competitor_count <= 7:
        comp_score = 70  # 适度竞争
    elif competitor_count <= 15:
        comp_score = 45  # 较激烈
    else:
        comp_score = 20  # 过度竞争

    # 竞品平均距离（距离越远越好）
    if competitors:
        avg_dist = sum(c["distance"] for c in competitors) / len(competitors)
        dist_bonus = min(20, avg_dist / 50)  # 距离远加分
        comp_score = min(100, comp_score + dist_bonus)

    scores["competition"] = round(comp_score)
    reasons["competition"] = f"竞品数量: {competitor_count}个 | 平均距离: {round(sum(c['distance'] for c in competitors) / max(len(competitors), 1))}m" if competitors else "竞品数量: 0个 | 空白市场"

    # ---- 7.6 综合宜居/商业环境评分 (5%) ----
    medical_count = cats.get("medical", {}).get("count", 0)
    env_score = min(100, medical_count * 10 + entertainment_count * 5)
    scores["environment"] = round(env_score)
    reasons["environment"] = f"医疗: {medical_count}个 | 娱乐: {entertainment_count}个"

    # ---- 综合加权评分 ----
    weights = {
        "foot_traffic": 0.30,
        "customer_demographics": 0.20,
        "traffic_pattern": 0.15,
        "spending_power": 0.15,
        "competition": 0.15,
        "environment": 0.05,
    }
    overall = sum(scores[k] * weights[k] for k in weights)
    scores["overall"] = round(overall)

    # 评级
    if overall >= 85:
        grade = "A - 强烈推荐"
    elif overall >= 70:
        grade = "B - 推荐"
    elif overall >= 55:
        grade = "C - 谨慎考虑"
    elif overall >= 40:
        grade = "D - 不推荐"
    else:
        grade = "E - 强烈不推荐"

    return {
        "scores": scores,
        "grade": grade,
        "reasons": reasons,
        "weights": weights,
    }


# ---- 8. 生成竞品对比分析 ----
def competitor_analysis(competitors: list) -> dict:
    """竞品深度分析"""
    if not competitors:
        return {
            "total": 0,
            "density_level": "空白市场",
            "avg_rating": 0,
            "distance_distribution": {},
            "top_competitors": [],
            "strategic_insight": "该区域无同类竞品，属于市场空白。建议优先入驻，抢占先发优势。但需验证该品类在此区域的接受度。",
        }

    # 距离分布
    near = sum(1 for c in competitors if c["distance"] <= 300)
    mid = sum(1 for c in competitors if 300 < c["distance"] <= 700)
    far = sum(1 for c in competitors if c["distance"] > 700)

    # 平均评分
    ratings = [float(c["rating"]) for c in competitors if c.get("rating") and c["rating"].replace(".", "").isdigit()]
    avg_rating = round(sum(ratings) / len(ratings), 1) if ratings else 0

    # 密度判定
    total = len(competitors)
    if total <= 2:
        density = "低竞争"
        insight = "竞品稀疏，市场空间充足。建议快速布局，建立品牌认知。"
    elif total <= 6:
        density = "适度竞争"
        insight = "存在一定竞争，但市场容量尚可。建议差异化定位，突出自身特色。"
    elif total <= 12:
        density = "较激烈"
        insight = "竞争较激烈，需要明确的差异化策略。建议分析竞品弱点，寻找切入点。"
    else:
        density = "过度竞争"
        insight = "竞品密集，红海市场。除非有显著的差异化优势或成本优势，否则不建议入场。"

    return {
        "total": total,
        "density_level": density,
        "avg_rating": avg_rating,
        "distance_distribution": {
            "near_0_300m": near,
            "mid_300_700m": mid,
            "far_700m_plus": far,
        },
        "top_competitors": sorted(competitors, key=lambda x: x["distance"])[:10],
        "strategic_insight": insight,
    }


# ============================================================
# 主分析流程
# ============================================================

def analyze(address: str, store_type: str, api_key: str, radius: int = 1000) -> dict:
    """执行完整的选址分析"""
    result = {
        "input": {
            "address": address,
            "store_type": store_type,
            "radius": radius,
        },
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    # Step 1: 地理编码
    geo_info = geocode(address, api_key)
    if not geo_info:
        return {"error": f"无法解析地址: {address}", "hint": "请检查地址格式是否正确，或尝试更具体的地标名称"}
    result["geo"] = geo_info
    lng, lat = geo_info["lng"], geo_info["lat"]

    # Step 2: 行政区信息
    dist_info = district_info(geo_info["adcode"], api_key)
    result["district"] = dist_info

    # Step 3: 周边设施分析（异步思路，但因API限制顺序执行）
    surroundings = analyze_surroundings(lng, lat, api_key, radius)
    result["surroundings"] = surroundings

    # Step 4: 实时交通态势
    traffic = traffic_status(lng, lat, api_key, radius)
    result["traffic"] = traffic

    # Step 5: 竞品搜索
    competitors = search_competitors(lng, lat, store_type, api_key, radius)
    result["competitors"] = competitor_analysis(competitors)

    # Step 6: 多维度评分
    scoring = compute_scores(geo_info, surroundings, traffic, competitors, store_type, radius)
    result["scoring"] = scoring

    return result


# ============================================================
# CLI入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="开店选址综合分析工具 - 基于高德地图API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python analyze_location.py --address "北京朝阳区三里屯太古里" --store-type "奶茶店"
  python analyze_location.py --address "上海市徐汇区衡山路" --store-type "咖啡店" --radius 1500
  python analyze_location.py --address "深圳市南山区科技园" --store-type "便利店" --amap-key YOUR_KEY
        """,
    )
    parser.add_argument("--address", required=True, help="目标地址")
    parser.add_argument("--store-type", required=True, help="开店类型（如：奶茶店、火锅店、便利店）")
    parser.add_argument("--radius", type=int, default=1000, help="分析半径(米)，默认1000")
    parser.add_argument("--amap-key", default="", help="高德地图Web服务API Key（也可通过AMAP_KEY环境变量设置）")
    parser.add_argument("--output", "-o", default="", help="输出JSON文件路径，默认输出到stdout")

    args = parser.parse_args()

    # 获取API Key
    api_key = args.amap_key or os.environ.get("AMAP_KEY", "")
    if not api_key:
        print(json.dumps({
            "error": "缺少高德地图API Key",
            "hint": "请通过 --amap-key 参数或 AMAP_KEY 环境变量提供",
            "get_key": "https://console.amap.com/dev/key/app",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    result = analyze(args.address, args.store_type, api_key, args.radius)

    output_json = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_json)
        print(f"分析完成，结果已保存至: {args.output}")
    else:
        print(output_json)


if __name__ == "__main__":
    main()
