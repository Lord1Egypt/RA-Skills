# -*- coding: utf-8 -*-
"""
景点智能推荐 - ClawHub技能脚本
6个工具：景点搜索、景点附近酒店、景点交通、景点附近美食、火车票查询、机票查询
数据源：飞猪旅行 + 高德地图，通过SCF代理调用
"""
import json
import re
import urllib.request
import urllib.error

# ============ 配置 ============
FLIGGY_PROXY = "https://1439498936-6sysdjjt99.ap-guangzhou.tencentscf.com"
GAODE_PROXY = "https://1439498936-bl10af74fl.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = "tp_8k2mX9vQ4z"
TIMEOUT = 30

_CITIES = [
    "北京", "上海", "广州", "深圳", "成都", "杭州", "南京", "武汉", "长沙", "重庆",
    "西安", "厦门", "青岛", "大连", "昆明", "丽江", "桂林", "苏州", "珠海", "海口",
    "三亚", "天津", "济南", "沈阳", "哈尔滨", "长春", "郑州", "合肥", "福州", "南昌",
    "太原", "石家庄", "贵阳", "南宁", "兰州", "银川", "呼和浩特", "乌鲁木齐", "拉萨",
    "无锡", "宁波", "温州", "烟台", "威海", "佛山", "东莞", "中山", "惠州", "扬州",
    "镇江", "绍兴", "嘉兴", "湖州", "常州", "泰安", "曲阜", "洛阳", "开封", "敦煌",
]


# ============ 代理调用 ============
def _call_fliggy(rtype, params):
    body = json.dumps({"type": rtype, "params": params}, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(
        FLIGGY_PROXY, data=body,
        headers={"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = ""
        try: err = e.read().decode("utf-8", errors="replace")[:300]
        except: pass
        return {"error": "proxy error " + str(e.code) + ": " + err}
    except Exception as e:
        return {"error": "request error: " + str(e)}


def _call_gaode(api, params):
    body = json.dumps({"type": api, "params": params}).encode("utf-8")
    req = urllib.request.Request(
        GAODE_PROXY, data=body,
        headers={"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}


def _gaode_geocode(address, city=""):
    params = {"address": address}
    if city: params["city"] = city
    data = _call_gaode("geocode", params)
    if isinstance(data, dict) and data.get("code") == 0:
        geocodes = data.get("data", {}).get("geocodes", [])
        if geocodes:
            location = geocodes[0].get("location", "")
            if location and "," in location:
                lng, lat = location.split(",")
                return (lng, lat)
    return (None, None)


def _gaode_around(location, keywords="", city="", radius=3000, limit=10):
    params = {
        "location": location, "types": "050000", "radius": radius,
        "sortrule": "weight", "offset": limit, "page": 1, "extensions": "all",
    }
    if keywords: params["keywords"] = keywords
    if city: params["city"] = city
    data = _call_gaode("poi_around", params)
    if isinstance(data, dict) and data.get("code") == 0:
        return data.get("data", {}).get("pois", [])
    return []


def _gaode_driving(origin, destination):
    params = {"origin": origin, "destination": destination, "strategy": 0}
    data = _call_gaode("driving_route", params)
    if isinstance(data, dict) and data.get("code") == 0:
        paths = data.get("data", {}).get("route", {}).get("paths", [])
        if paths:
            p = paths[0]
            dist = int(p.get("distance", 0))
            dur = int(p.get("duration", 0))
            return {"distance_km": round(dist / 1000, 1), "duration_min": round(dur / 60), "taxi_cost": _estimate_taxi(dist)}
    return {}


def _gaode_transit(origin, destination, city):
    params = {"origin": origin, "destination": destination, "city": city, "strategy": 0, "nightflag": 0}
    data = _call_gaode("transit_route", params)
    if isinstance(data, dict) and data.get("code") == 0:
        return data.get("data", {}).get("route", {}).get("transits", [])
    return []


def _estimate_taxi(distance_m):
    km = distance_m / 1000
    if km <= 0: return "¥0"
    if km <= 3: return "¥14左右"
    return "¥" + str(int(14 + (km - 3) * 2.5)) + "左右"


def _is_metro(line_name):
    return any(kw in line_name for kw in ["地铁", "号线", "城轨", "磁浮", "市域", "轻轨"])


def _extract_city(query):
    for city in _CITIES:
        if city in query:
            return city
    m = re.search(r"([\u4e00-\u9fa5]{2,4})市", query)
    if m: return m.group(1)
    return ""


# ============ 关键词提取 ============
def _extract_poi_keyword(query, city):
    kw = query
    if city: kw = kw.replace(city, "")
    for w in ["门票", "票价", "票", "景区", "景点", "推荐", "附近", "周边", "的", "有什么", "哪个", "哪家", "好", "好玩", "查询", "搜索", "一下", "帮我", "看看"]:
        kw = kw.replace(w, "")
    kw = re.sub(r"\d+", "", kw)
    kw = kw.strip()
    return kw if len(kw) >= 2 else ""


def _extract_hotel_keyword(query, city):
    kw = query
    if city: kw = kw.replace(city, "")
    for w in ["酒店", "住宿", "推荐", "附近", "周边", "的", "左右", "以内", "以下", "有", "什么", "哪个", "哪家", "好", "查询", "搜索", "一下", "帮我", "看看", "便宜", "实惠", "元", "价格", "入住", "退房"]:
        kw = kw.replace(w, "")
    kw = re.sub(r"\d+月\d+日?", "", kw)
    kw = re.sub(r"\d+", "", kw)
    kw = kw.strip()
    return kw if len(kw) >= 2 else ""


# ============ 互提示 ============
def _build_tips(current_tool, city="", poi_name=""):
    all_tools = [
        ("景点搜索", "🎫"),
        ("酒店搜索", "🏨"),
        ("交通查询", "🚇"),
        ("美食推荐", "🍜"),
        ("火车票", "🚄"),
        ("机票", "✈️"),
    ]
    tips = []
    for tool_key, emoji in all_tools:
        if tool_key == current_tool:
            continue
        if tool_key == "景点搜索":
            if city: tips.append(emoji + "推荐" + city + "景点")
            else: tips.append(emoji + "景点搜索")
        elif tool_key == "酒店搜索":
            if city: tips.append(emoji + "推荐" + city + "酒店")
            else: tips.append(emoji + "酒店搜索")
        elif tool_key == "交通查询":
            if poi_name: tips.append(emoji + "前往" + poi_name + "交通")
            elif city: tips.append(emoji + city + "市内交通")
            else: tips.append(emoji + "交通查询")
        elif tool_key == "美食推荐":
            if poi_name: tips.append(emoji + poi_name + "附近美食")
            else: tips.append(emoji + "美食推荐")
        elif tool_key == "火车票":
            if city: tips.append(emoji + "查去" + city + "火车票")
            else: tips.append(emoji + "火车票查询")
        elif tool_key == "机票":
            if city: tips.append(emoji + "查去" + city + "机票")
            else: tips.append(emoji + "机票查询")
    return "\n\n📋 附加服务：\n" + " | ".join(tips)


# ============ 格式化 ============
def _format_ticket(ticket):
    if not ticket: return ""
    if isinstance(ticket, dict):
        price = ticket.get("price", "")
        name = ticket.get("ticketName", "")
        if price and name: return name + " " + price
        if price: return price
    if isinstance(ticket, str): return ticket
    return ""


def _format_poi_items(item_list):
    lines = []
    for i, p in enumerate(item_list, 1):
        name = p.get("name", "未知景点")
        level = p.get("poiLevel") or 0
        if isinstance(level, str):
            try: level = int(level)
            except: level = 0
        addr = p.get("address", "")
        desc = p.get("description", "")
        url = p.get("jumpUrl", "")
        ticket = p.get("ticketInfo", "")
        main_pic = p.get("mainPic", "")
        level_str = " · " + str(level) + "A级景区" if level >= 1 else ""
        lines.append("**" + str(i) + ". " + name + level_str + "**")
        if main_pic:
            lines.append("   ![景点图片](" + str(main_pic) + ")")
        if addr:
            lines.append("   📍 " + addr)
        if desc:
            lines.append("   📝 " + str(desc)[:80])
        ticket_str = _format_ticket(ticket)
        if ticket_str:
            lines.append("   🎫 " + ticket_str)
        if url:
            lines.append("   🔗 [查看详情/购票](" + url + ")")
        lines.append("")
    return "\n".join(lines)


def _format_hotel_items(item_list):
    lines = []
    for i, h in enumerate(item_list, 1):
        name = h.get("name", h.get("title", "未知酒店"))
        price = h.get("price", "")
        score = h.get("score", "")
        address = h.get("address", "")
        main_pic = h.get("mainPic", h.get("picUrl", ""))
        jump_url = h.get("jumpUrl", h.get("detailUrl", ""))
        lines.append("**" + str(i) + ". " + name + "**")
        if main_pic:
            lines.append("   ![酒店图片](" + str(main_pic) + ")")
        detail_parts = []
        if price: detail_parts.append("💰 " + str(price))
        if score: detail_parts.append("⭐ " + str(score))
        if address: detail_parts.append("📍 " + address)
        if detail_parts:
            lines.append("   " + " | ".join(detail_parts))
        if jump_url:
            lines.append("   🔗 [预订酒店](" + jump_url + ")")
        lines.append("")
    lines.append("💡 价格实时变动，以实际下单为准")
    return "\n".join(lines)


def _parse_flyai_text(data):
    if isinstance(data, str): return data
    if isinstance(data, dict):
        if "error" in data: return "搜索失败: " + data["error"]
        if "raw_text" in data: return data["raw_text"]
        inner = data.get("data", data)
        if inner is None: inner = {}
        if isinstance(inner, str): return inner
        if isinstance(inner, dict):
            item_list = inner.get("itemList", [])
            if item_list: return _format_poi_items(item_list)
            return json.dumps(inner, ensure_ascii=False, indent=2)
    return str(data)


def _format_train_items(item_list):
    lines = []
    for i, item in enumerate(item_list[:15], 1):
        for journey in item.get("journeys", []):
            for seg in journey.get("segments", []):
                transport = seg.get("marketingTransportName", "")
                transport_no = seg.get("marketingTransportNo", seg.get("transportNo", ""))
                dep_city = seg.get("depCityName", "")
                arr_city = seg.get("arrCityName", "")
                dep_station = seg.get("depStationShortName", seg.get("depStationName", ""))
                arr_station = seg.get("arrStationShortName", seg.get("arrStationName", ""))
                dep_time = seg.get("depDateTime", "")
                arr_time = seg.get("arrDateTime", "")
                duration = seg.get("duration", "")
                price = item.get("price", item.get("ticketPrice", ""))
                seat_class = seg.get("seatClassName", "")
                jump_url = item.get("jumpUrl", item.get("detailUrl", ""))
                lines.append(str(i) + ". " + transport + str(transport_no) + " " + dep_city + "→" + arr_city)
                dep_t = dep_time.split(" ")[-1] if " " in dep_time else dep_time
                arr_t = arr_time.split(" ")[-1] if " " in arr_time else arr_time
                lines.append("   " + dep_station + " " + dep_t + " → " + arr_station + " " + arr_t)
                detail_parts = []
                if price: detail_parts.append("💰 ¥" + str(price))
                if duration:
                    try:
                        dur = int(duration)
                        detail_parts.append("⏱️ " + str(dur // 60) + "时" + str(dur % 60) + "分")
                    except: pass
                if seat_class: detail_parts.append("💺 " + seat_class)
                if detail_parts: lines.append("   " + " | ".join(detail_parts))
                if jump_url: lines.append("   🔗 " + jump_url)
                lines.append("")
                break
    lines.append("⚠️ 余票和价格实时变动，以实际下单为准")
    return "\n".join(lines)


def _format_flight_items(item_list):
    lines = []
    for i, item in enumerate(item_list[:15], 1):
        for journey in item.get("journeys", []):
            for seg in journey.get("segments", []):
                transport = seg.get("marketingTransportName", "")
                transport_no = seg.get("marketingTransportNo", seg.get("transportNo", ""))
                dep_city = seg.get("depCityName", "")
                arr_city = seg.get("arrCityName", "")
                dep_station = seg.get("depStationShortName", seg.get("depStationName", ""))
                arr_station = seg.get("arrStationShortName", seg.get("arrStationName", ""))
                dep_term = seg.get("depTerm", "")
                arr_term = seg.get("arrTerm", "")
                dep_time = seg.get("depDateTime", "")
                arr_time = seg.get("arrDateTime", "")
                duration = seg.get("duration", "")
                price = item.get("price", item.get("ticketPrice", ""))
                seat_class = seg.get("seatClassName", "")
                jump_url = item.get("jumpUrl", item.get("detailUrl", ""))
                lines.append(str(i) + ". " + transport + str(transport_no) + " " + dep_city + "→" + arr_city)
                dep_t = dep_time.split(" ")[-1] if " " in dep_time else dep_time
                arr_t = arr_time.split(" ")[-1] if " " in arr_time else arr_time
                dep_parts = [dep_station]
                if dep_term: dep_parts.append(dep_term + "航站楼")
                arr_parts = [arr_station]
                if arr_term: arr_parts.append(arr_term + "航站楼")
                lines.append("   " + " ".join(dep_parts) + " " + dep_t + " → " + " ".join(arr_parts) + " " + arr_t)
                detail_parts = []
                if price: detail_parts.append("💰 ¥" + str(price))
                if duration:
                    try:
                        dur = int(duration)
                        detail_parts.append("⏱️ " + str(dur // 60) + "时" + str(dur % 60) + "分")
                    except: pass
                if seat_class: detail_parts.append("💺 " + seat_class)
                if detail_parts: lines.append("   " + " | ".join(detail_parts))
                if jump_url: lines.append("   🔗 " + jump_url)
                lines.append("")
                break
    lines.append("⚠️ 票价实时变动，以实际下单为准")
    return "\n".join(lines)


# ============ 工具1：景点搜索 ============
def poi_search(params):
    """景点搜索：搜索景点信息及门票，返回景点名称、等级、地址、图片和购票链接。"""
    city = params.get("city", "")
    keyword = params.get("keyword", "")
    category = params.get("category", "")
    level = params.get("level", 0)
    limit = params.get("limit", 10)
    if not city: return "请提供城市名，如：深圳、杭州、北京"

    search_kw = keyword
    if keyword:
        search_kw = _extract_poi_keyword(keyword, city)

    scf_params = {"cityName": city, "limit": min(limit, 20)}
    if search_kw: scf_params["keyword"] = search_kw
    if category: scf_params["category"] = category
    if level and int(level) > 0: scf_params["poiLevel"] = int(level)

    result = _call_fliggy("search_poi", scf_params)
    if isinstance(result, dict) and "error" in result:
        ai_query = keyword or city + "景点推荐"
        result = _call_fliggy("fliggy_ai_search", {"query": ai_query, "limit": limit})
        text = _parse_flyai_text(result)
        return text + _build_tips("景点搜索", city, keyword or city)

    if isinstance(result, dict):
        inner = result.get("data", result)
        if isinstance(inner, dict):
            items = inner.get("itemList", [])
            if items:
                desc_parts = ["（" + city]
                if keyword: desc_parts.append("·" + keyword)
                if level: desc_parts.append("·" + str(level) + "A级")
                desc_parts.append("）")
                text = "为您找到 " + str(len(items)) + " 个景点" + "".join(desc_parts) + "：\n\n"
                text += _format_poi_items(items)
                first_poi = items[0].get("name", "景点")
                return text + _build_tips("景点搜索", city, first_poi)

    return "😔 未找到符合条件的景点，建议调整搜索条件后重试。" + _build_tips("景点搜索", city)


# ============ 工具2：景点附近酒店 ============
def poi_hotel(params):
    """酒店搜索：搜索景点附近酒店，返回酒店名称、评分、价格、图片和预订链接。"""
    query = params.get("query", "")
    limit = params.get("limit", 10)
    if not query: return "请描述酒店需求，如：西湖附近酒店、故宫周边500元以内酒店"

    city = _extract_city(query)
    hotel_kw = _extract_hotel_keyword(query, city)

    scf_params = {"limit": min(limit, 20)}
    if city: scf_params["cityName"] = city
    if hotel_kw: scf_params["keyword"] = hotel_kw

    result = _call_fliggy("search_hotels", scf_params)
    if isinstance(result, dict) and "error" not in result:
        inner = result.get("data", result)
        if isinstance(inner, dict):
            items = inner.get("itemList", [])
            if items:
                text = "🏨 找到 " + str(len(items)) + " 家酒店：\n\n"
                text += _format_hotel_items(items)
                return text + _build_tips("酒店搜索", city)

    # 回退到 AI 文本搜索
    result = _call_fliggy("fliggy_ai_search", {"query": query, "limit": limit})
    text = _parse_flyai_text(result)
    return text + _build_tips("酒店搜索", city)


# ============ 工具3：景点交通 ============
def poi_transport(params):
    """交通查询：查询到景点的交通路线，包括打车、地铁、公交方案。"""
    origin = params.get("origin", "")
    destination = params.get("destination", "")
    city = params.get("city", "")
    if not origin: return "请提供出发地，如：上海虹桥站、浦东机场"
    if not destination: return "请提供景点名称，如：故宫、西湖"
    if not city: return "请提供城市名，如：北京、杭州"

    origin_lng, origin_lat = _gaode_geocode(origin, city)
    dest_lng, dest_lat = _gaode_geocode(destination, city)
    if not origin_lng or not dest_lng:
        return "无法解析地址，请确认「" + origin + "」和「" + destination + "」是否正确"

    lines = ["📍 " + origin + " → " + destination + " 交通方式", ""]

    driving = _gaode_driving(origin_lng + "," + origin_lat, dest_lng + "," + dest_lat)
    if driving:
        lines.append("━━━ 🚗 打车/驾车 ━━━")
        lines.append("距离" + str(driving["distance_km"]) + "公里 | 约" + str(driving["duration_min"]) + "分钟 | " + driving["taxi_cost"])
        lines.append("💡 可打开微信/支付宝「滴滴出行」小程序叫车")
        lines.append("")

    transit_routes = _gaode_transit(origin_lng + "," + origin_lat, dest_lng + "," + dest_lat, city)
    if transit_routes:
        metro_routes = [r for r in transit_routes if any(_is_metro(bl.get("name", "")) for seg in r.get("segments", []) for bl in seg.get("bus", {}).get("buslines", []))]
        bus_routes = [r for r in transit_routes if r not in metro_routes]
        if metro_routes:
            lines.append("━━━ 🚇 地铁/城轨 ━━━")
            for i, route in enumerate(metro_routes[:2], 1):
                duration = int(route.get("duration", 0) or 0)
                cost = route.get("cost", "0")
                all_lines = []
                for seg in route.get("segments", []):
                    for bl in seg.get("bus", {}).get("buslines", []):
                        name = bl.get("name", "").split("(")[0]
                        dep = bl.get("departure_stop", {}).get("name", "")
                        arr = bl.get("arrival_stop", {}).get("name", "")
                        all_lines.append({"name": name, "dep": dep, "arr": arr})
                cost_str = "¥" + cost if cost and cost != "0" else ""
                line_names = " → ".join(l["name"] for l in all_lines)
                detail_parts = ["约" + str(round(duration / 60)) + "分钟"]
                if cost_str: detail_parts.append(cost_str)
                lines.append("方案" + str(i) + ": " + line_names + " | " + " ".join(detail_parts))
                for l in all_lines:
                    if l["dep"] or l["arr"]:
                        lines.append("   " + l["name"] + ": " + l["dep"] + "→" + l["arr"])
            lines.append("")
        if bus_routes:
            lines.append("━━━ 🚌 公交 ━━━")
            for i, route in enumerate(bus_routes[:2], 1):
                duration = int(route.get("duration", 0) or 0)
                cost = route.get("cost", "0")
                all_lines = []
                for seg in route.get("segments", []):
                    for bl in seg.get("bus", {}).get("buslines", []):
                        all_lines.append(bl.get("name", "").split("(")[0])
                cost_str = "¥" + cost if cost and cost != "0" else ""
                line_names = " → ".join(all_lines)
                detail_parts = ["约" + str(round(duration / 60)) + "分钟"]
                if cost_str: detail_parts.append(cost_str)
                lines.append("方案" + str(i) + ": " + line_names + " | " + " ".join(detail_parts))
            lines.append("")

    if not driving and not transit_routes:
        return "未找到合适的交通方案，建议使用地图APP导航。" + _build_tips("交通查询", city, destination)
    lines.append("💡 以上时间和费用为预估值，实际可能因路况变化")
    return "\n".join(lines) + _build_tips("交通查询", city, destination)


# ============ 工具4：景点附近美食 ============
def poi_food(params):
    """美食推荐：搜索景点附近餐厅美食，返回餐厅名称、菜系、评分和人均消费。"""
    location_name = params.get("location", "")
    city = params.get("city", "")
    keywords = params.get("keywords", "")
    radius = params.get("radius", 3000)
    limit = params.get("limit", 10)
    if not location_name: return "请提供景点名称，如：故宫、西湖"
    if not city: return "请提供城市名，如：北京、杭州"

    lng, lat = _gaode_geocode(location_name, city)
    if not lng:
        return "无法解析「" + location_name + "」的位置，请尝试更具体的景点名"

    pois = _gaode_around(lng + "," + lat, keywords=keywords, city=city, radius=int(radius), limit=min(int(limit), 20))
    if not pois:
        kw_info = "「" + keywords + "」" if keywords else ""
        return "未找到" + location_name + "附近" + kw_info + "的餐厅" + _build_tips("美食推荐", city, location_name)

    lines = ["🍜 找到 " + str(len(pois)) + " 家 " + location_name + "附近餐厅：", ""]
    for i, poi in enumerate(pois, 1):
        name = poi.get("name", "未知")
        type_name = poi.get("type", "")
        cuisine = ""
        if type_name:
            parts = type_name.split(";")
            if len(parts) >= 2: cuisine = parts[1]
            elif len(parts) == 1: cuisine = parts[0]
        address = poi.get("address", "") or (poi.get("pname", "") + poi.get("cityname", "") + poi.get("adname", ""))
        rating = poi.get("rating", "")
        cost = poi.get("cost", "")
        tel = poi.get("tel", "")
        biz_ext = poi.get("biz_ext", {})
        if not rating and isinstance(biz_ext, dict): rating = biz_ext.get("rating", "")
        if not cost and isinstance(biz_ext, dict): cost = biz_ext.get("cost", "")
        cuisine_tag = " [" + cuisine + "]" if cuisine else ""
        lines.append(str(i) + ". " + name + cuisine_tag)
        if address: lines.append("   📍 " + address)
        detail_parts = []
        if rating and rating not in ("", "0", "-1"): detail_parts.append("⭐" + rating)
        if cost and cost not in ("", "0", "-1"): detail_parts.append("人均¥" + cost)
        if tel: detail_parts.append("📞" + tel)
        if detail_parts: lines.append("   " + " | ".join(detail_parts))
        lines.append("")
    lines.append("💡 以上信息来自地图数据，评分和价格仅供参考")
    return "\n".join(lines) + _build_tips("美食推荐", city, location_name)


# ============ 工具5：火车票查询 ============
def train_search(params):
    """火车票查询：搜索飞猪平台火车票，返回车次、时间、票价和购票链接。"""
    origin = params.get("origin", "")
    destination = params.get("destination", "")
    dep_date = params.get("dep_date", "")
    if not origin: return "请提供出发城市，如：北京"

    scf_params = {"origin": origin}
    if destination: scf_params["destination"] = destination
    if dep_date: scf_params["depDate"] = dep_date

    result = _call_fliggy("search_domestic_train", scf_params)
    if isinstance(result, dict):
        if "error" in result: return "搜索失败: " + result["error"]
        inner = result.get("data", result)
        if isinstance(inner, dict):
            items = inner.get("itemList", [])
            if items:
                return _format_train_items(items) + _build_tips("火车票", destination)
            return "未找到符合条件的车次" + _build_tips("火车票", destination)
    return str(result) + _build_tips("火车票", destination)


# ============ 工具6：机票查询 ============
def flight_search(params):
    """机票查询：搜索飞猪平台机票，返回航班、时间、票价和购票链接。"""
    origin = params.get("origin", "")
    destination = params.get("destination", "")
    dep_date = params.get("dep_date", "")
    back_date = params.get("back_date", "")
    if not origin: return "请提供出发城市，如：北京"

    scf_params = {"origin": origin}
    if destination: scf_params["destination"] = destination
    if dep_date: scf_params["depDate"] = dep_date
    if back_date: scf_params["backDate"] = back_date

    result = _call_fliggy("search_flight", scf_params)
    if isinstance(result, dict):
        if "error" in result: return "搜索失败: " + result["error"]
        inner = result.get("data", result)
        if isinstance(inner, dict):
            items = inner.get("itemList", [])
            if items:
                return _format_flight_items(items) + _build_tips("机票", destination)
            return "未找到符合条件的航班" + _build_tips("机票", destination)
    return str(result) + _build_tips("机票", destination)
