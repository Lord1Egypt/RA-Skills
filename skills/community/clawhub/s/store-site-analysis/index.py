import os
import json
import asyncio
from typing import List, Dict, Any

import aiohttp
from jinja2 import Environment, FileSystemLoader

# ================== 配置 ==================
AMAP_KEY = os.getenv("AMAP_KEY")
AMAP_JS_KEY = os.getenv("AMAP_JS_KEY", AMAP_KEY)

if not AMAP_KEY:
    raise RuntimeError("缺少环境变量 AMAP_KEY")

# ================== 高德 API ==================
GEOCODE_URL = "https://restapi.amap.com/v3/geocode/geo"
AROUND_URL = "https://restapi.amap.com/v3/place/around"
REGEO_URL = "https://restapi.amap.com/v3/geocode/regeo"
TRAFFIC_URL = "https://restapi.amap.com/v3/traffic/status/rectangle"

HEADERS = {"User-Agent": "store-site-analysis/1.2"}

# ================== 工具 ==================
def split_location(loc: str):
    return tuple(map(float, loc.split(",")))

async def fetch_json(session: aiohttp.ClientSession, url: str, params: dict):
    async with session.get(url, params=params, headers=HEADERS) as resp:
        return await resp.json()

# ================== 高德封装 ==================
async def geocode(session: aiohttp.ClientSession, address: str):
    data = await fetch_json(session, GEOCODE_URL, {
        "key": AMAP_KEY, "address": address, "output": "json"
    })
    geo = data.get("geocodes", [{}])[0]
    if not geo:
        raise ValueError(f"地址解析失败: {address}")
    return geo["location"], geo.get("formatted_address", "")

async def around_search(session: aiohttp.ClientSession, location: str, **kwargs):
    pois = []
    offset = kwargs.get("offset", 50)
    for page in range(1, 3):
        params = {
            "key": AMAP_KEY,
            "location": location,
            "radius": kwargs.get("radius", 1000),
            "offset": offset,
            "page": page,
            "output": "json"
        }
        if kwargs.get("keywords"):
            params["keywords"] = kwargs["keywords"]
        if kwargs.get("types"):
            params["types"] = kwargs["types"]

        data = await fetch_json(session, AROUND_URL, params)
        batch = data.get("pois", [])
        pois.extend(batch)
        if len(batch) < offset:
            break
    return pois

async def regeocode(session: aiohttp.ClientSession, location: str):
    data = await fetch_json(session, REGEO_URL, {
        "key": AMAP_KEY, "location": location, "output": "json"
    })
    return data.get("regeocode", {})

async def traffic_status(session: aiohttp.ClientSession, location: str, radius=5000):
    try:
        lng, lat = split_location(location)
        r = radius / 100000
        rect = f"{lng-r},{lat-r};{lng+r},{lat+r}"
        data = await fetch_json(session, TRAFFIC_URL, {
            "key": AMAP_KEY, "rectangle": rect, "output": "json"
        })
        return data.get("trafficinfo", {})
    except Exception:
        return {}

# ================== 单地址分析 ==================
async def analyze_single(session, address, business_keyword, radius, business_type):
    location, formatted = await geocode(session, address)
    lng, lat = split_location(location)

    # competitor_types = business_type or "050000|060000|070000"
    competitor_types = business_type or "050000"

    competitors, facilities, addr_info, traffic = await asyncio.gather(
        around_search(session, location, keywords=business_keyword, types=competitor_types, radius=radius),
        around_search(session, location, types="120000|150500|141200|050000|060100|170000", radius=radius),
        regeocode(session, location),
        traffic_status(session, location, radius)
    )

    comp_breakdown = {}
    for p in competitors:
        t = p.get("type", "其他")
        comp_breakdown[t] = comp_breakdown.get(t, 0) + 1

    ac = addr_info.get("addressComponent", {})

    return {
        "address": address,
        "location": location,
        "formatted_address": formatted,
        "district": ac.get("district"),
        "township": ac.get("township"),
        "city": ac.get("city"),
        "lng": lng,
        "lat": lat,
        "radius": radius,
        "competitor_count": len(competitors),
        "competitors": [
            {
                "name": p.get("name"),
                "address": p.get("address"),
                "type": p.get("type"),
                "distance": p.get("distance"),
                "location": p.get("location")
            } for p in competitors[:30]
        ],
        "facility_count": len(facilities),
        "facilities": [
            {
                "name": p.get("name"),
                "type": p.get("type"),
                "distance": p.get("distance"),
                "location": p.get("location")
            } for p in facilities
        ],
        "competitor_type_breakdown": comp_breakdown,
        "traffic_status": traffic.get("evaluation", {}).get("status"),
        "traffic_description": traffic.get("description")
    }

# ================== 热力图 ==================
def render_heatmap(result: Dict[str, Any], output_path: str):
    env = Environment(loader=FileSystemLoader("."))
    tmpl = env.get_template("heatmap_template.html")

    html = tmpl.render(
        address=result["address"],
        district=result["district"],
        township=result["township"],
        competitor_count=result["competitor_count"],
        facility_count=result["facility_count"],
        lng=result["lng"],
        lat=result["lat"],
        radius=result["radius"],
        amap_js_key=AMAP_JS_KEY,
        competitors_json=json.dumps([c for c in result["competitors"] if c.get("location")]),
        facilities_json=json.dumps([f for f in result["facilities"] if f.get("location")])
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

# ================== 多地址对比 ==================
def calc_scores(competitors, facilities, traffic_status, radius):
    metro = [f for f in facilities if "地铁" in f.get("type", "") or "轨道" in f.get("type", "")]
    residence = [f for f in facilities if any(k in f.get("type", "") for k in ["住宅", "小区", "公寓"])]
    commercial = [f for f in facilities if any(k in f.get("type", "") for k in ["商场", "购物", "写字楼", "商务"])]

    scores = {
        "competitor": max(0, 100 - len(competitors) * 5),
        "facility": min(100, len(facilities) * 3),
        "traffic": min(100, len(metro) * 25 + (20 if traffic_status == "1" else 0)),
        "commercial": min(100, len(commercial) * 15),
        "residence": min(100, len(residence) * 8)
    }
    scores["total"] = round(
        scores["competitor"] * 0.25 +
        scores["facility"] * 0.20 +
        scores["traffic"] * 0.20 +
        scores["commercial"] * 0.20 +
        scores["residence"] * 0.15
    )
    return scores, len(metro), len(residence), len(commercial)

def render_compare(results: List[Dict[str, Any]], output_path: str):
    env = Environment(loader=FileSystemLoader("."))
    tmpl = env.get_template("compare_template.html")

    dims = ["竞品密度", "配套丰富度", "交通便捷度", "商业活跃度", "居住潜力"]

    radar_charts = {}
    for dim in dims:
        radar_charts[dim] = {}
        for r in results:
            name = r["district"] or r["address"]
            radar_charts[dim][name] = [
                r["scores"]["competitor"],
                r["scores"]["facility"],
                r["scores"]["traffic"],
                r["scores"]["commercial"],
                r["scores"]["residence"]
            ]

    def make_col(key, fn):
        return [{"name": r["district"] or r["address"], "value": fn(r)} for r in results]

    def best(arr, better):
        return min(arr, key=lambda x: x["value"])["name"] if better == "min" else max(arr, key=lambda x: x["value"])["name"]

    table_data = {
        "competitor_count": make_col("c", lambda r: r["competitor_count"]),
        "facility_count": make_col("f", lambda r: r["facility_count"]),
        "metro_count": make_col("m", lambda r: r["metro_count"]),
        "residence_count": make_col("r", lambda r: r["residence_count"]),
        "commercial_count": make_col("b", lambda r: r["commercial_count"]),
        "traffic_status": make_col("t", lambda r: {
            "name": r["district"] or r["address"],
            "value": {
                "1": "畅通", "2": "基本畅通", "3": "轻度拥堵",
                "4": "中度拥堵", "5": "严重拥堵"
            }.get(r["traffic_status"], "未知"),
            "badge": {
                "1": "badge-green", "2": "badge-yellow"
            }.get(r["traffic_status"], "badge-red")
        }),
        "district": make_col("d", lambda r: f'{r["district"]}·{r["township"]}')
    }

    table_data["competitor_count"].append({"name": "✅ 最优", "value": best(table_data["competitor_count"], "min")})
    table_data["facility_count"].append({"name": "✅ 最优", "value": best(table_data["facility_count"], "max")})
    table_data["metro_count"].append({"name": "✅ 最优", "value": best(table_data["metro_count"], "max")})
    table_data["residence_count"].append({"name": "✅ 最优", "value": best(table_data["residence_count"], "max")})
    table_data["commercial_count"].append({"name": "✅ 最优", "value": best(table_data["commercial_count"], "max")})

    html = tmpl.render(
        addresses=[{
            "name": r["district"] or r["address"],
            "location": r["location"],
            "radius": r["radius"],
            "competitors": [c for c in r["competitors"] if c.get("location")]
        } for r in results],
        colors_json=json.dumps(["#e74c3c", "#3498db", "#2ecc71", "#e67e22", "#9b59b6"][:len(results)]),
        addresses_json=json.dumps([{
            "name": r["district"] or r["address"],
            "location": r["location"],
            "radius": r["radius"],
            "competitors": [{"location": c["location"]} for c in r["competitors"] if c.get("location")]
        } for r in results]),
        radar_json=json.dumps(radar_charts),
        score_bars=[{
            "name": r["district"] or r["address"],
            "total_score": r["scores"]["total"],
            "color": ["#e74c3c", "#3498db", "#2ecc71", "#e67e22", "#9b59b6"][i],
            "percent": r["scores"]["total"]
        } for i, r in enumerate(results)],
        rankings=[{
            "name": f'{r["district"]}（{r["township"]}）',
            "total_score": r["scores"]["total"]
        } for r in results],
        table_data={k: v for k, v in table_data.items()},
        amap_js_key=AMAP_JS_KEY,
        timestamp=__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

# ================== Skill 入口 ==================
async def main(args: Dict[str, Any]):
    address = args.get("address")
    if not address:
        raise ValueError("缺少必要参数 address")

    async with aiohttp.ClientSession() as session:
        result = await analyze_single(
            session,
            address,
            args.get("business_keyword", "奶茶店|咖啡厅|小吃快餐|便利店"),
            args.get("radius", 1000),
            args.get("business_type", "")
        )

    output_dir = args.get("output_dir", "/tmp/store-site-analysis")
    safe_name = "".join(c for c in address if c.isalnum() or c in "_-").rstrip("_")[:50]
    html_path = f"{output_dir}/{safe_name}_heatmap.html"

    render_heatmap(result, html_path)
    result["heatmap_html"] = html_path
    result["analysis_summary"] = (
        f"已生成选址分析报告，包含 {result['competitor_count']} 个竞品和 "
        f"{result['facility_count']} 个配套设施的分布可视化。"
    )

    return result

# ================== 多地址对比入口 ==================
async def compare(args: Dict[str, Any]):
    addresses = args.get("addresses", [])
    if not isinstance(addresses, list) or len(addresses) < 2:
        raise ValueError("多地址对比至少需要 2 个地址")
    if len(addresses) > 5:
        raise ValueError("最多支持 5 个地址同时对比")

    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(*[
            analyze_single(
                session,
                addr,
                args.get("business_keyword", "奶茶店|咖啡厅|小吃快餐|便利店"),
                args.get("radius", 1000),
                args.get("business_type", "")
            ) for addr in addresses
        ])

    for r in results:
        scores, metro, residence, commercial = calc_scores(
            r["competitors"], r["facilities"], r["traffic_status"], r["radius"]
        )
        r["scores"] = scores
        r["metro_count"] = metro
        r["residence_count"] = residence
        r["commercial_count"] = commercial

    results.sort(key=lambda x: x["scores"]["total"], reverse=True)

    output_dir = args.get("output_dir", "/tmp/store-site-analysis")
    safe_name = "_vs_".join(addresses)[:80]
    html_path = f"{output_dir}/{safe_name}_compare.html"
    render_compare(results, html_path)

    return {
        "summary": f"完成 {len(addresses)} 个地址的对比分析",
        "rankings": [
            {
                "rank": i + 1,
                "address": r["address"],
                "district": r["district"],
                "township": r["township"],
                "total_score": r["scores"]["total"],
                "detail": {
                    "competitor_score": r["scores"]["competitor"],
                    "facility_score": r["scores"]["facility"],
                    "traffic_score": r["scores"]["traffic"],
                    "commercial_score": r["scores"]["commercial"],
                    "residence_score": r["scores"]["residence"]
                },
                "competitor_count": r["competitor_count"],
                "facility_count": r["facility_count"],
                "metro_count": r["metro_count"],
                "residence_count": r["residence_count"],
                "commercial_count": r["commercial_count"],
                "traffic_status": r["traffic_status"]
            }
            for i, r in enumerate(results)
        ],
        "compare_html": html_path,
        "recommendation": (
            f"{results[0]['district']}（{results[0]['township']}）"
            f"综合得分最高（{results[0]['scores']['total']}分），最推荐作为选址目标。"
        )
    }