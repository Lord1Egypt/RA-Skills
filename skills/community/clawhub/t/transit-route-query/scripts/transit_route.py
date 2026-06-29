# -*- coding: utf-8 -*-
"""
公交地铁线路查询 - ClawHub技能脚本
零配置即装即用，通过SCF代理调用高德API
1个工具：公交地铁路线查询
"""
import json
import urllib.request
import urllib.error

# ============ 配置 ============
GAODE_PROXY = "https://1439498936-bl10af74fl.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = "tp_8k2mX9vQ4z"
TIMEOUT = 15

_METRO_KEYWORDS = ["地铁", "号线", "城轨", "磁浮", "市域", "轻轨"]


def _is_metro(line_name):
    return any(kw in line_name for kw in _METRO_KEYWORDS)


# ============ 代理调用 ============
def _call_gaode(api, params):
    body = json.dumps({"type": api, "params": params}).encode("utf-8")
    req = urllib.request.Request(
        GAODE_PROXY, data=body,
        headers={"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            data = json.loads(r.read().decode("utf-8"))
            if isinstance(data, dict) and data.get("code") == 0 and "data" in data:
                return data["data"]
            return data
    except urllib.error.HTTPError as e:
        err = ""
        try: err = e.read().decode("utf-8", errors="replace")[:200]
        except: pass
        return {"error": "proxy error " + str(e.code) + ": " + err}
    except Exception as e:
        return {"error": "request error: " + str(e)}


# ============ 工具1：公交地铁路线查询 ============
def _format_segments(segments):
    """解析路线段，返回结构化步骤列表"""
    steps = []
    for seg in segments:
        bus = seg.get("bus", {})
        bls = bus.get("buslines", [])
        walking = seg.get("walking", {})

        if bls:
            for bl in bls:
                name = bl.get("name", "").split("(")[0]
                dep_stop = bl.get("departure_stop", {}).get("name", "")
                arr_stop = bl.get("arrival_stop", {}).get("name", "")
                via = bl.get("via_num", "")
                is_metro = _is_metro(name)
                steps.append({
                    "type": "metro" if is_metro else "bus",
                    "name": name,
                    "dep_stop": dep_stop,
                    "arr_stop": arr_stop,
                    "via": via,
                })
        
        if walking and walking.get("distance", "0") != "0":
            try:
                wd = int(float(walking.get("distance", 0)))
                if wd > 0:
                    steps.append({"type": "walk", "distance": wd})
            except (ValueError, TypeError):
                pass

    return steps


def _get_nearest_station(steps, route_type):
    """获取最近的上车站（第一个地铁站或公交站）"""
    for step in steps:
        if step.get("type") in ("metro", "bus"):
            if route_type == "metro" and step["type"] != "metro":
                continue
            return f"{step['dep_stop']}（{step['name']}）"
    return ""


def query_route(params):
    """查询从出发地到目的地的公交地铁路线，自动规划最优换乘方案。"""
    origin = params.get("origin", "")
    destination = params.get("destination", "")
    city = params.get("city", "")
    strategy = params.get("strategy", "0")

    if not origin: return "请提供出发地，如：三里屯、南京路、浦东机场"
    if not destination: return "请提供目的地，如：天安门、外滩、火车站"
    if not city: return "请提供所在城市，如：北京、上海、广州"

    # strategy: 0=最快, 1=最少换乘, 2=最少步行
    strategy_map = {"0": "0", "1": "1", "2": "2"}
    s = strategy_map.get(str(strategy), "0")

    gaode_params = {
        "origin_address": origin,
        "origin_city": city,
        "destination_address": destination,
        "destination_city": city,
        "city": city,
        "strategy": s,
    }

    data = _call_gaode("transit_route_by_address", gaode_params)
    if isinstance(data, dict) and "error" in data:
        return "路线查询失败: " + data["error"]

    if not isinstance(data, dict) or data.get("status") != "1":
        return f"😔 未找到{origin}→{destination}的公交地铁路线。建议检查地址或换用更具体的地点名。"

    transits = data.get("route", {}).get("transits", [])
    if not transits:
        return f"😔 未找到{origin}→{destination}的公交地铁路线。建议检查地址或换用更具体的地点名。"

    # 分组：地铁优先、公交次之
    metro_routes = []
    bus_routes = []
    for route in transits[:8]:
        all_steps = _format_segments(route.get("segments", []))
        has_metro = any(s.get("type") == "metro" for s in all_steps)
        if has_metro:
            metro_routes.append((route, all_steps))
        else:
            bus_routes.append((route, all_steps))

    strategy_label = {"0": "最快", "1": "少换乘", "2": "少步行"}.get(s, "最快")

    lines = [f"🚇 {origin} → {destination} 公交地铁路线（{strategy_label}优先）", ""]

    # 地铁方案
    if metro_routes:
        lines.append(f"━━━ 🚇 地铁/城轨方案（{len(metro_routes)}条）━━━")
        lines.append("")
        for i, (route, steps) in enumerate(metro_routes[:3], 1):
            duration = int(route.get("duration", 0) or 0)
            cost = route.get("cost", "0")
            walking = int(route.get("walking_distance", 0) or 0)

            cost_str = f"¥{float(cost):.0f}" if cost and cost != "0" else ""
            duration_str = f"约{round(duration / 60)}分钟"
            walk_str = f"步行{walking}米" if walking > 0 else ""
            detail_parts = [duration_str]
            if cost_str: detail_parts.append(cost_str)
            if walk_str: detail_parts.append(walk_str)

            lines.append(f"**方案{i}** {' | '.join(detail_parts)}")

            for step in steps:
                if step["type"] in ("metro", "bus"):
                    icon = "🚇" if step["type"] == "metro" else "🚌"
                    via_str = f"{step['via']}站" if step.get("via") else ""
                    lines.append(f"  {icon} {step['name']}: {step['dep_stop']}→{step['arr_stop']}（{via_str}）")
                elif step["type"] == "walk":
                    lines.append(f"  🚶 步行{step['distance']}米")

            # 提示最近上车站
            nearest = _get_nearest_station(steps, "metro")
            if nearest and i == 1:
                lines.append(f"  💡 最近的地铁站: {nearest}")
            lines.append("")

    # 公交方案
    if bus_routes:
        lines.append(f"━━━ 🚌 公交方案（{len(bus_routes)}条）━━━")
        lines.append("")
        for i, (route, steps) in enumerate(bus_routes[:2], 1):
            duration = int(route.get("duration", 0) or 0)
            cost = route.get("cost", "0")
            walking = int(route.get("walking_distance", 0) or 0)

            cost_str = f"¥{float(cost):.0f}" if cost and cost != "0" else ""
            duration_str = f"约{round(duration / 60)}分钟"
            walk_str = f"步行{walking}米" if walking > 0 else ""
            detail_parts = [duration_str]
            if cost_str: detail_parts.append(cost_str)
            if walk_str: detail_parts.append(walk_str)

            lines.append(f"**方案{i}** {' | '.join(detail_parts)}")

            for step in steps:
                if step["type"] == "bus":
                    via_str = f"{step['via']}站" if step.get("via") else ""
                    lines.append(f"  🚌 {step['name']}: {step['dep_stop']}→{step['arr_stop']}（{via_str}）")
                elif step["type"] == "walk":
                    lines.append(f"  🚶 步行{step['distance']}米")
            lines.append("")

    lines.append("💡 以上时间和费用为预估值，实际可能因运营调整变化")
    lines.append("💡 可在高德地图/百度地图APP查看实时公交到站信息")

    return "\n".join(lines)
