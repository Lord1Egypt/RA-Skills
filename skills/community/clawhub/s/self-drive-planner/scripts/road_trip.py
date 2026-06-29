# -*- coding: utf-8 -*-
"""
自驾出行规划 - road-trip-planner
3工具: plan_route / search_poi_along / trip_weather
数据源: 高德地图SCF代理
"""

import os
import json
import urllib.request
import urllib.error
from datetime import datetime

# ===== 代理配置 =====
GAODE_PROXY = "https://1439498936-bl10af74fl.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")

# ===== 通用请求 =====
def _post_proxy(api_type, params):
    """调用高德SCF代理"""
    body = json.dumps({
        "type": api_type,
        "params": params
    }, ensure_ascii=False).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "X-Proxy-Token": PROXY_TOKEN
    }
    req = urllib.request.Request(GAODE_PROXY, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = ""
        try:
            err = e.read().decode("utf-8")[:300]
        except:
            pass
        return {"error": f"HTTP {e.code}: {err}"}
    except Exception as e:
        return {"error": str(e)}

# ===== 工具1: plan_route =====
def plan_route(origin, destination, waypoints="", strategy=0):
    """规划自驾路线"""
    # 调用高德驾车路线规划（地址版）
    params = {
        "origin_address": origin,
        "destination_address": destination,
        "strategy": str(strategy)
    }
    if waypoints.strip():
        params["waypoints_address"] = waypoints

    result = _post_proxy("driving_route_by_address", params)

    if "error" in result and "route" not in result:
        return json.dumps({"success": False, "error": result.get("error", "路线规划失败")}, ensure_ascii=False)

    route_data = result.get("route", result.get("data", {}).get("route", {}))
    paths = route_data.get("paths", [])

    if not paths:
        return json.dumps({"success": False, "error": "未找到可用路线"}, ensure_ascii=False)

    best = paths[0]
    distance_m = int(best.get("distance", 0))
    duration_s = int(best.get("duration", 0))
    tolls = float(best.get("tolls", 0))
    distance_km = distance_m / 1000
    duration_h = duration_s / 3600

    # 油耗估算
    fuel_rate = 8  # L/100km
    fuel_price = 8.0  # 元/L
    fuel_cost = round(distance_km / 100 * fuel_rate * fuel_price, 1)

    # 电费估算（新能源）
    ev_rate = 15  # kWh/100km
    ev_price = 0.6  # 元/kWh
    ev_cost = round(distance_km / 100 * ev_rate * ev_price, 1)

    total_cost_fuel = round(tolls + fuel_cost, 1)
    total_cost_ev = round(tolls + ev_cost, 1)

    # 途经城市
    via_cities = []
    steps = best.get("steps", [])
    for step in steps:
        cities = step.get("cities", [])
        for c in cities:
            name = c.get("name", "")
            if name and name not in via_cities and name != origin and name != destination:
                via_cities.append(name)

    # 疲劳驾驶分段建议（合并到3小时左右再分段，休息点去重）
    segments = []
    driving_hours = 0
    seg_start = origin
    seg_distance = 0
    seg_tolls = 0
    rest_points = []
    last_rest_city = ""

    for step in steps:
        step_dist = int(step.get("distance", 0)) / 1000
        step_time = int(step.get("duration", 0)) / 3600
        step_toll = float(step.get("tolls", 0))
        road_name = step.get("road", "")

        driving_hours += step_time
        seg_distance += step_dist
        seg_tolls += step_toll

        # 3小时以上才分段，超5小时强制分段
        should_break = driving_hours >= 3.0 or (driving_hours >= 2.5 and seg_distance > 300)
        force_break = driving_hours >= 5.0

        if should_break:
            # 找休息点（优先选不同城市名）
            rest_city = ""
            for c in step.get("cities", []):
                cn = c.get("name", "")
                if cn != last_rest_city:
                    rest_city = cn
                    break
            if not rest_city:
                for c in step.get("cities", []):
                    rest_city = c.get("name", "")
                    break
            rest_point = rest_city or road_name or f"行驶{round(seg_distance)}km处"

            # 去重：同城市名不重复分段（但超过5小时强制分段）
            if rest_point != last_rest_city or force_break:
                if rest_point == last_rest_city and force_break:
                    # 强制分段，用公里数区分
                    rest_point = f"{rest_point}附近(行驶{round(seg_distance)}km处)"

                rest_points.append(rest_point)
                last_rest_city = rest_city or rest_point

                segments.append({
                    "from": seg_start,
                    "to": rest_point,
                    "distance_km": round(seg_distance, 1),
                    "driving_hours": round(driving_hours, 1),
                    "tolls": round(seg_tolls, 1),
                    "suggestion": f"已连续驾驶{round(driving_hours,1)}小时，建议休息15-20分钟"
                })

                seg_start = rest_point
                driving_hours = 0
                seg_distance = 0
                seg_tolls = 0

    # 最后一段（短段或同城名合并到上一段）
    if seg_distance > 0:
        is_same_city = False
        if segments:
            last_to = segments[-1].get("to", "")
            # 去掉市/城区等后缀比较
            def _norm_city(s):
                for suffix in ["市", "城区", "自治州", "地区", "县"]:
                    s = s.replace(suffix, "")
                return s
            is_same_city = _norm_city(seg_start) == _norm_city(destination) or _norm_city(last_to) == _norm_city(destination)
        if segments and (seg_distance < 50 and driving_hours < 1 or is_same_city and seg_distance < 150):
            # 太短，合并到上一段
            last = segments[-1]
            last["to"] = destination
            last["distance_km"] = round(last["distance_km"] + seg_distance, 1)
            last["driving_hours"] = round(last["driving_hours"] + driving_hours, 1)
            last["tolls"] = round(last["tolls"] + seg_tolls, 1)
            if "suggestion" in last:
                last["suggestion"] = f"已连续驾驶{last["driving_hours"]}小时，建议休息15-20分钟"
        else:
            segments.append({
                "from": seg_start,
                "to": destination,
                "distance_km": round(seg_distance, 1),
                "driving_hours": round(driving_hours, 1),
                "tolls": round(seg_tolls, 1)
            })

    # 长段添加强制休息建议
    for seg in segments:
        if seg.get("driving_hours", 0) > 5:
            seg["suggestion"] = f"⚠️ 本段长达{seg["driving_hours"]}小时，强烈建议中途休息1-2次，每2-3小时停车活动"
            seg["force_rest"] = True

    # 夜间驾驶提醒
    night_warning = ""
    if duration_h > 6:
        night_warning = "⚠️ 长途自驾请避免夜间连续驾驶，22:00-06:00建议缩短连续驾驶至2小时以内"

    output = {
        "success": True,
        "origin": origin,
        "destination": destination,
        "waypoints": waypoints if waypoints.strip() else None,
        "distance_km": round(distance_km, 1),
        "duration_hours": round(duration_h, 1),
        "tolls_yuan": round(tolls, 1),
        "fuel_cost_yuan": fuel_cost,
        "ev_cost_yuan": ev_cost,
        "total_cost_fuel": total_cost_fuel,
        "total_cost_ev": total_cost_ev,
        "via_cities": via_cities[:10],
        "segments": segments,
        "rest_points": rest_points,
        "night_warning": night_warning,
        "tips": _generate_tips(distance_km, duration_h, tolls)
    }

    return json.dumps(output, ensure_ascii=False, indent=2)


def _generate_tips(distance_km, duration_h, tolls):
    """生成驾驶建议"""
    tips = []
    if distance_km > 500:
        tips.append("长途自驾建议提前检查轮胎、刹车、机油和冷却液")
    if distance_km > 300:
        tips.append("建议每2-3小时进服务区休息，避免疲劳驾驶")
    if tolls > 200:
        tips.append("过路费较高，可考虑走国道节省费用（但时间会增加）")
    if duration_h > 8:
        tips.append("单日驾驶超过8小时，强烈建议分两天走，中间住一晚")
    if not tips:
        tips.append("短途自驾，注意遵守交规，保持安全车距")
    return tips


# ===== 工具2: search_poi_along =====
def search_poi_along(location, poi_type, radius=5000):
    """搜索沿途服务设施"""
    # POI类型映射
    type_map = {
        "gas_station": "加油站",
        "charging": "充电站",
        "service_area": "服务区",
        "parking": "停车场",
        "restaurant": "餐厅"
    }
    type_keyword = type_map.get(poi_type, poi_type)

    # 先地理编码获取坐标
    geocode_result = _post_proxy("geocode", {"address": location})
    geocodes = geocode_result.get("geocodes", geocode_result.get("data", {}).get("geocodes", []))

    if not geocodes:
        # 尝试input_tips
        tips_result = _post_proxy("input_tips", {"keywords": location, "type": ""})
        tips = tips_result.get("tips", tips_result.get("data", {}).get("tips", []))
        if tips:
            first_tip = tips[0]
            location_str = first_tip.get("location", "")
            if not location_str:
                return json.dumps({"success": False, "error": f"无法定位：{location}"}, ensure_ascii=False)
        else:
            return json.dumps({"success": False, "error": f"无法定位：{location}"}, ensure_ascii=False)
    else:
        location_str = geocodes[0].get("location", "")

    if not location_str:
        return json.dumps({"success": False, "error": f"无法定位：{location}"}, ensure_ascii=False)

    # 周边搜索
    search_params = {
        "keywords": type_keyword,
        "location": location_str,
        "radius": str(radius),
        "offset": "10"
    }
    search_result = _post_proxy("poi_around", search_params)

    pois = search_result.get("pois", search_result.get("data", {}).get("pois", []))

    if not pois:
        return json.dumps({
            "success": True,
            "location": location,
            "poi_type": type_keyword,
            "count": 0,
            "results": [],
            "message": f"{location}附近{radius}米内未找到{type_keyword}"
        }, ensure_ascii=False)

    results = []
    for p in pois[:10]:
        results.append({
            "name": p.get("name", ""),
            "address": p.get("address", ""),
            "distance": p.get("distance", ""),
            "type": p.get("type", ""),
            "tel": p.get("tel", "")
        })

    output = {
        "success": True,
        "location": location,
        "poi_type": type_keyword,
        "count": len(results),
        "results": results
    }

    return json.dumps(output, ensure_ascii=False, indent=2)


# ===== 工具3: trip_weather =====
def trip_weather(cities):
    """查询沿途城市天气"""
    city_list = [c.strip() for c in cities.split(",") if c.strip()]

    if not city_list:
        return json.dumps({"success": False, "error": "请提供城市列表"}, ensure_ascii=False)

    results = []

    for city in city_list:
        # 先获取城市adcode
        district_result = _post_proxy("district", {"keywords": city, "subdistrict": "0"})
        districts = district_result.get("districts", district_result.get("data", {}).get("districts", []))

        adcode = ""
        city_name = city
        if districts:
            adcode = districts[0].get("adcode", "")
            city_name = districts[0].get("name", city)

        if not adcode:
            results.append({
                "city": city,
                "error": "无法获取城市编码"
            })
            continue

        # 查天气
        weather_result = _post_proxy("weather", {"city": adcode})
        lives = weather_result.get("lives", weather_result.get("data", {}).get("lives", []))

        if not lives:
            results.append({
                "city": city_name,
                "error": "无法获取天气数据"
            })
            continue

        w = lives[0]
        weather_text = w.get("weather", "")
        temp = w.get("temperature", "")
        wind_dir = w.get("winddirection", "")
        wind_power = w.get("windpower", "")
        humidity = w.get("humidity", "")

        # 驾驶建议
        advice = _weather_driving_advice(weather_text, temp, wind_power)

        results.append({
            "city": city_name,
            "weather": weather_text,
            "temperature": f"{temp}°C",
            "wind": f"{wind_dir} {wind_power}级",
            "humidity": f"{humidity}%",
            "driving_advice": advice
        })

    output = {
        "success": True,
        "query_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "cities": results
    }

    return json.dumps(output, ensure_ascii=False, indent=2)


def _weather_driving_advice(weather, temp_str, wind_power):
    """根据天气生成驾驶建议"""
    advice = []
    weather_lower = weather.lower() if weather else ""

    # 天气状况
    if any(kw in weather_lower for kw in ["暴", "大暴雨"]):
        advice.append("⛔ 暴雨天气，强烈建议推迟出行")
    elif any(kw in weather_lower for kw in ["雨"]):
        advice.append("⚠️ 雨天路滑，降低车速，保持安全车距")
    elif any(kw in weather_lower for kw in ["大雪", "暴雪"]):
        advice.append("⛔ 暴雪天气，建议推迟出行或选择高铁")
    elif any(kw in weather_lower for kw in ["雪", "冰雪"]):
        advice.append("⚠️ 雪天路滑，建议安装雪地胎，低速行驶")
    elif any(kw in weather_lower for kw in ["雾", "霾"]):
        advice.append("⚠️ 大雾天气，建议避开高速走国道，开启雾灯")

    # 温度
    try:
        temp = float(temp_str)
        if temp > 35:
            advice.append("🌡️ 高温天气，注意检查轮胎气压和冷却液，车内备水")
        elif temp < 0:
            advice.append("🧊 低温天气，注意防冻液、热车后再出发")
        elif temp < -10:
            advice.append("🧊 极寒天气，建议检查电瓶和防冻液，长时间停车后需热车")
    except (ValueError, TypeError):
        pass

    # 风力
    try:
        wp = int(wind_power)
        if wp >= 6:
            advice.append("💨 大风天气，注意侧风影响，降低车速")
    except (ValueError, TypeError):
        pass

    if not advice:
        advice.append("✅ 天气适宜自驾，注意安全驾驶")

    return "；".join(advice)


# ===== CLI入口 =====
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python road_trip.py <tool> <args_json>")
        print("Tools: plan_route, search_poi_along, trip_weather")
        sys.exit(1)

    tool = sys.argv[1]
    args = json.loads(sys.argv[2])

    if tool == "plan_route":
        print(plan_route(
            origin=args.get("origin", ""),
            destination=args.get("destination", ""),
            waypoints=args.get("waypoints", ""),
            strategy=args.get("strategy", 0)
        ))
    elif tool == "search_poi_along":
        print(search_poi_along(
            location=args.get("location", ""),
            poi_type=args.get("poi_type", "gas_station"),
            radius=args.get("radius", 5000)
        ))
    elif tool == "trip_weather":
        print(trip_weather(
            cities=args.get("cities", "")
        ))
    else:
        print(json.dumps({"error": f"未知工具: {tool}"}, ensure_ascii=False))
