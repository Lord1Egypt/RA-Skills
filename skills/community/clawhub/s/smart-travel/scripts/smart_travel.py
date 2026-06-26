# -*- coding: utf-8 -*-
"""
全能旅行助手 - ClawHub技能脚本
以行程规划为核心，16合1一站式旅行服务
数据源：飞猪旅行+高德地图+同程旅行+途牛旅游（均通过SCF代理），零配置
"""
import json
import re
import urllib.request
import urllib.error
from datetime import datetime, timedelta

# ============ 配置 ============
FLIGGY_PROXY = "https://1439498936-6sysdjjt99.ap-guangzhou.tencentscf.com"
GAODE_PROXY = "https://1439498936-bl10af74fl.ap-guangzhou.tencentscf.com"
TONGCHENG_PROXY = "https://1439498936-7vqpkiipef.ap-guangzhou.tencentscf.com"
TUNIU_PROXY = "https://1439498936-0junm3maxj.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = "tp_8k2mX9vQ4z"
FLIGGY_TIMEOUT = 60
GAODE_TIMEOUT = 15
TC_TIMEOUT = 60
TN_TIMEOUT = 60

_CITIES = [
    "北京", "上海", "广州", "深圳", "成都", "杭州", "南京", "武汉", "长沙", "重庆",
    "西安", "厦门", "青岛", "大连", "昆明", "丽江", "桂林", "苏州", "珠海", "海口",
    "三亚", "天津", "济南", "沈阳", "哈尔滨", "长春", "郑州", "合肥", "福州", "南昌",
    "太原", "石家庄", "贵阳", "南宁", "兰州", "银川", "呼和浩特", "乌鲁木齐", "拉萨",
    "无锡", "宁波", "温州", "烟台", "威海", "佛山", "东莞", "中山", "惠州", "扬州",
]


# ============ 代理调用 ============
def _call_fliggy(rtype, params):
    """调用飞猪SCF代理"""
    body = json.dumps({"type": rtype, "params": params}, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(
        FLIGGY_PROXY, data=body,
        headers={"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=FLIGGY_TIMEOUT) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = ""
        try: err = e.read().decode("utf-8", errors="replace")[:300]
        except: pass
        return {"error": "proxy error " + str(e.code) + ": " + err}
    except Exception as e:
        return {"error": "request error: " + str(e)}


def _call_gaode(api, params):
    """调用高德SCF代理，自动解包data层"""
    body = json.dumps({"type": api, "params": params}).encode("utf-8")
    req = urllib.request.Request(
        GAODE_PROXY, data=body,
        headers={"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=GAODE_TIMEOUT) as r:
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


def _call_tongcheng(rtype, params):
    """调用同程SCF代理"""
    body = json.dumps({"type": rtype, "params": params}, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(
        TONGCHENG_PROXY, data=body,
        headers={"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TC_TIMEOUT) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = ""
        try: err = e.read().decode("utf-8", errors="replace")[:300]
        except: pass
        return {"error": "proxy error " + str(e.code) + ": " + err}
    except Exception as e:
        return {"error": "request error: " + str(e)}


def _call_tuniu(rtype, params):
    """调用途牛SCF代理"""
    body = json.dumps({"type": rtype, "params": params}, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(
        TUNIU_PROXY, data=body,
        headers={"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TN_TIMEOUT) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = ""
        try: err = e.read().decode("utf-8", errors="replace")[:300]
        except: pass
        return {"error": "proxy error " + str(e.code) + ": " + err}
    except Exception as e:
        return {"error": "request error: " + str(e)}


def _safe_str(val, default=""):
    """防御 None 和字符串 'None'"""
    if val is None:
        return default
    s = str(val).strip()
    if s == "None" or s == "null":
        return default
    return s


# ============ 高德通用 ============
def _gaode_geocode(address, city=""):
    params = {"address": address}
    if city: params["city"] = city
    data = _call_gaode("geocode", params)
    if isinstance(data, dict) and data.get("status") == "1":
        geocodes = data.get("geocodes", [])
        if geocodes:
            loc = geocodes[0].get("location", "")
            if loc and "," in loc:
                parts = loc.split(",")
                return (parts[0], parts[1])
    return (None, None)


def _gaode_food_search(location, keywords="", city="", radius=3000, limit=10):
    params = {"location": location, "types": "050000", "radius": radius, "sortrule": "weight", "offset": limit, "page": 1, "extensions": "all"}
    if keywords: params["keywords"] = keywords
    if city: params["city"] = city
    data = _call_gaode("poi_around", params)
    if isinstance(data, dict) and data.get("status") == "1":
        return data.get("pois", [])
    return []


def _gaode_driving(origin, destination, city):
    params = {"origin_address": origin, "origin_city": city, "destination_address": destination, "destination_city": city, "strategy": "0"}
    data = _call_gaode("driving_route_by_address", params)
    if isinstance(data, dict):
        paths = data.get("route", {}).get("paths", [])
        if paths:
            path = paths[0]
            distance = int(path.get("distance", 0) or 0)
            duration = int(path.get("duration", 0) or 0)
            taxi_cost_raw = data.get("route", {}).get("taxi_cost", "0")
            try:
                taxi_cost = "¥" + str(int(taxi_cost_raw)) + "左右"
            except:
                taxi_cost = _estimate_taxi_cost(distance)
            return {"distance_km": round(distance / 1000, 1), "duration_min": round(duration / 60), "taxi_cost": taxi_cost}
    return {}


def _gaode_transit(origin, destination, city):
    params = {"origin_address": origin, "origin_city": city, "destination_address": destination, "destination_city": city, "city": city, "strategy": "0"}
    data = _call_gaode("transit_route_by_address", params)
    if isinstance(data, dict):
        return data.get("route", {}).get("transits", [])
    return []


def _gaode_take_taxi(slon, slat, sname, dlon, dlat, dname):
    result = _call_gaode("schema_take_taxi", {"slon": slon, "slat": slat, "sname": sname, "dlon": dlon, "dlat": dlat, "dname": dname})
    if isinstance(result, dict) and "uri" in result:
        return result["uri"]
    return ""


# ============ 辅助 ============
def _estimate_taxi_cost(distance_m):
    distance_km = distance_m / 1000
    if distance_km <= 0: return "¥0"
    if distance_km <= 3: return "¥14左右"
    cost = 14 + (distance_km - 3) * 2.5
    return "¥" + str(int(cost)) + "左右"

def _is_metro_line(line_name):
    return any(kw in line_name for kw in ["地铁", "号线", "城轨", "磁浮", "市域", "轻轨"])

def _extract_city(query):
    for city in _CITIES:
        if city in query: return city
    return ""

def _extract_dest(query):
    m = re.search(r"去(.{2,8}?)(玩|旅游|旅行|度假|出差|住)", query)
    if m:
        dest = m.group(1).strip()
        dest = re.sub(r"\d+天?$", "", dest).strip()
        dest = re.sub(r"(的|了|一|两|附近|周边|景区|区域|一带)$", "", dest).strip()
        if len(dest) >= 2: return dest
    m = re.search(r"(.{2,6}?)(旅游|旅行|度假|游玩|周末游|亲子游|蜜月游|自由行)", query)
    if m:
        dest = m.group(1).strip()
        dest = re.sub(r"[\d天]+$", "", dest).strip()
        dest = re.sub(r"(去|到|的|了|附近|周边|景区|一带)$", "", dest).strip()
        if len(dest) >= 2: return dest
    return ""

def _build_tips(current_tool, dest=""):
    all_tools = [
        ("行程规划", "行程规划"), ("火车票查询", "火车票查询"), ("机票查询", "机票查询"),
        ("酒店搜索", "酒店搜索"), ("景点门票", "景点门票"), ("万豪酒店", "万豪酒店"),
        ("美食推荐", "美食推荐"), ("市内交通", "市内交通"), ("打车链接", "打车链接"),
        ("天气查询", "天气查询"), ("汽车票搜索", "汽车票搜索"), ("跟团游", "跟团游"),
        ("邮轮搜索", "邮轮搜索"), ("度假线路", "度假线路"),
    ]
    tips = []
    for tool_key, label in all_tools:
        if tool_key == current_tool: continue
        if dest:
            mapping = {
                "行程规划": "规划" + dest + "行程", "火车票查询": "查去" + dest + "的火车票",
                "机票查询": "查去" + dest + "的机票", "酒店搜索": "推荐" + dest + "酒店",
                "景点门票": "推荐" + dest + "景点", "万豪酒店": "搜索" + dest + "万豪酒店",
                "美食推荐": "推荐" + dest + "美食", "市内交通": dest + "市内交通",
                "打车链接": dest + "一键打车", "天气查询": dest + "天气预报",
                "汽车票搜索": "查去" + dest + "的汽车票", "跟团游": "推荐" + dest + "跟团游",
                "邮轮搜索": "搜索" + dest + "邮轮", "度假线路": "推荐" + dest + "度假线路",
            }
            tips.append(mapping.get(tool_key, label))
        else:
            tips.append(label)
    return "\n\n💡 我还能帮你：" + " | ".join(tips)

def _parse_flyai_text(data):
    if isinstance(data, str):
        if data.strip() == "" or data.strip() == "null": return None
        return data
    if isinstance(data, dict):
        if "error" in data: return "搜索失败: " + data["error"]
        if "raw_text" in data: return data["raw_text"]
        inner = data.get("data", data)
        if inner is None: inner = {}
        if isinstance(inner, str): return inner
        if isinstance(inner, dict):
            item_list = inner.get("itemList", [])
            if item_list: return _format_items(item_list)
            return json.dumps(inner, ensure_ascii=False, indent=2)
    return str(data)

def _normalize_item(item):
    info = item.get("info")
    if isinstance(info, dict):
        return {"name": info.get("title", ""), "price": info.get("price", ""), "jumpUrl": info.get("jumpUrl", ""),
                "address": info.get("address", ""), "star": info.get("star", ""), "scoreDesc": info.get("scoreDesc", ""),
                "ticketPrice": info.get("ticketPrice", ""), "detailUrl": info.get("detailUrl", "")}
    return {"name": item.get("name", item.get("title", "")), "price": item.get("price", item.get("ticketPrice", "")),
            "jumpUrl": item.get("jumpUrl", item.get("detailUrl", "")), "address": item.get("address", ""),
            "star": item.get("star", ""), "scoreDesc": item.get("scoreDesc", item.get("rating", "")),
            "ticketPrice": item.get("ticketPrice", ""), "detailUrl": item.get("detailUrl", "")}

def _format_items(items):
    lines = []
    for i, item in enumerate(items[:10], 1):
        it = _normalize_item(item)
        name = it["name"] or "未知"
        line = str(i) + ". " + name
        details = []
        if it.get("star") and str(it["star"]).strip(): details.append(str(it["star"]).strip())
        if it.get("scoreDesc") and str(it["scoreDesc"]).strip(): details.append("⭐" + str(it["scoreDesc"]).strip())
        if it.get("price") and str(it["price"]).strip(): details.append("¥" + str(it["price"]).strip() + "起")
        if details: line += "  " + " | ".join(details)
        lines.append(line)
        if it.get("address"): lines.append("   📍 " + it["address"])
        url = it.get("jumpUrl") or it.get("detailUrl", "")
        if url: lines.append("   🔗 " + url)
    return "\n".join(lines)

def _format_train_items(items):
    lines = []
    for i, item in enumerate(items[:10], 1):
        name = item.get("name", item.get("title", ""))
        dep_time = item.get("depDateTime", "")
        arr_time = item.get("arrDateTime", "")
        price = item.get("price", item.get("ticketPrice", ""))
        seat = item.get("seatClassName", "")
        duration = item.get("duration", "")
        line = str(i) + ". " + name
        if dep_time and arr_time: line += "  " + dep_time + "→" + arr_time
        if duration: line += " ⏱️" + duration
        if price: line += " ¥" + str(price)
        if seat: line += " " + seat
        lines.append(line)
    return "\n".join(lines)

def _format_flight_items(items):
    lines = []
    for i, item in enumerate(items[:10], 1):
        journeys = item.get("journeys", [])
        price = item.get("ticketPrice", "")
        url = item.get("jumpUrl", "")
        total_duration = item.get("totalDuration", "")
        if journeys:
            j = journeys[0]
            jtype = j.get("journeyType", "")
            segments = j.get("segments", [])
            if segments:
                s = segments[0]
                airline = s.get("marketingTransportName", "")
                flight_no = s.get("marketingTransportNo", "")
                dep = s.get("depStationShortName", s.get("depStationName", ""))
                dep_time = s.get("depDateTime", "").split(" ")[1][:5] if " " in s.get("depDateTime", "") else s.get("depDateTime", "")
                last_s = segments[-1]
                arr = last_s.get("arrStationShortName", last_s.get("arrStationName", ""))
                arr_time = last_s.get("arrDateTime", "").split(" ")[1][:5] if " " in last_s.get("arrDateTime", "") else last_s.get("arrDateTime", "")
                line = str(i) + ". " + airline + " " + flight_no + " [" + jtype + "]"
                lines.append(line)
                lines.append("   " + dep_time + " " + dep + " → " + arr_time + " " + arr + " (" + str(total_duration) + "min)")
                if price: lines.append("   ¥" + str(price))
                if url: lines.append("   🔗 " + url)
                lines.append("")
    return "\n".join(lines)


# ============ 工具函数 ============

def travel_plan(params):
    """行程规划：智能推荐行程方案，涵盖景点+酒店+交通。"""
    query = params.get("query", "")
    if not query: return "请描述你的旅行需求，如：3天2晚上海游"
    result = _call_fliggy("fliggy_ai_search", {"query": query})
    text = _parse_flyai_text(result)
    if text is None: return "未找到行程方案，建议换个描述试试"
    dest = _extract_dest(query) or _extract_city(query) or ""
    return text + _build_tips("行程规划", dest)


def search_train(params):
    """火车票查询：查询火车票/高铁票的余票、价格和时刻表。"""
    query = params.get("query", "")
    if not query: return "请描述火车票需求，如：北京到上海明天的火车"
    result = _call_fliggy("fliggy_ai_search", {"query": query})
    text = _parse_flyai_text(result)
    if text is None: return "未找到火车票信息，建议换个描述试试"
    dest = _extract_city(query) or ""
    return text + _build_tips("火车票查询", dest)


def search_flight(params):
    """机票查询：查询国内航班实时票价、航班号、起降时间。"""
    query = params.get("query", "")
    if not query: return "请描述机票需求，如：上海到三亚7月1号机票"
    result = _call_fliggy("fliggy_ai_search", {"query": query})
    text = _parse_flyai_text(result)
    if text is None: return "未找到航班信息，建议换个描述试试"
    dest = _extract_city(query) or ""
    return text + _build_tips("机票查询", dest)


def _format_hotel_items(items):
    """格式化酒店搜索结果，展示8个关键字段"""
    lines = []
    for i, item in enumerate(items[:10], 1):
        name = _safe_str(item.get("name", item.get("title", "")), "未知酒店")
        price = _safe_str(item.get("price", ""))
        star = _safe_str(item.get("star", ""))
        address = _safe_str(item.get("address", ""))
        brand = _safe_str(item.get("brandName", ""))
        decoration = _safe_str(item.get("decorationTime", ""))
        detail_url = _safe_str(item.get("detailUrl", item.get("jumpUrl", "")))
        poi = _safe_str(item.get("interestsPoi", ""))
        main_pic = _safe_str(item.get("mainPic", ""))

        lines.append(str(i) + ". 🏨 " + name)
        detail_parts = []
        if price and price != "0":
            if "¥" in price:
                detail_parts.append("💰 " + price + "起")
            else:
                detail_parts.append("💰 ¥" + price + "起")
        if star:
            detail_parts.append("⭐ " + star)
        if brand:
            detail_parts.append("🏷️ " + brand)
        if decoration and decoration != "0":
            detail_parts.append("🔧 " + decoration + "装修")
        if detail_parts:
            lines.append("   " + " | ".join(detail_parts))
        info_parts = []
        if address:
            info_parts.append("📍 " + address)
        if poi:
            info_parts.append("🗺️ " + poi)
        if info_parts:
            lines.append("   " + " | ".join(info_parts))
        if detail_url:
            lines.append("   🔗 预订: " + detail_url)
        if main_pic:
            lines.append("   ![酒店图片](" + main_pic + ")")
        lines.append("")
    lines.append("⚠️ 价格实时变动，以实际下单为准")
    return "\n".join(lines)


def _extract_keywords(query, city):
    """从query中移除城市名和常见停用词，提取关键词"""
    kw = query
    if city:
        kw = kw.replace(city, "")
    for w in ["酒店", "住宿", "住", "推荐", "附近", "周边", "左右", "以内", "以下", "预算", "元", "块钱", "的", "有", "没", "什么", "哪个", "哪家", "好", "便宜", "性价比高"]:
        kw = kw.replace(w, "")
    kw = re.sub(r"\d+", "", kw)
    kw = kw.strip()
    return kw if len(kw) >= 2 else ""


def search_hotel(params):
    """酒店搜索：搜索酒店，返回实时价格、星级、品牌、地址、酒店图片和预订链接。"""
    query = params.get("query", "")
    if not query: return "请描述酒店需求，如：杭州西湖附近酒店"
    city = _extract_city(query)
    dest = _extract_dest(query) or city or ""
    # 优先走 search_hotels 路由获取结构化数据（含图片）
    if city:
        keywords = _extract_keywords(query, city)
        scf_params = {"destName": city}
        if keywords:
            scf_params["keyWords"] = keywords
        result = _call_fliggy("search_hotels", scf_params)
        if isinstance(result, dict) and "error" not in result:
            inner = result.get("data", result)
            if isinstance(inner, dict):
                item_list = inner.get("itemList", [])
                if item_list:
                    return _format_hotel_items(item_list) + _build_tips("酒店搜索", dest)
    # 回退到AI文本
    result = _call_fliggy("fliggy_ai_search", {"query": query})
    text = _parse_flyai_text(result)
    if text is None: return "未找到酒店信息，建议换个描述试试"
    return text + _build_tips("酒店搜索", dest)


def _extract_poi_keyword(query, city):
    kw = query
    if city:
        kw = kw.replace(city, "")
    for w in ["门票", "票价", "票", "景区", "景点", "推荐", "附近", "周边", "的", "有什么", "哪个", "哪家", "好", "好玩", "查询", "搜索", "一下", "帮我", "看看"]:
        kw = kw.replace(w, "")
    kw = re.sub(r"\d+", "", kw)
    kw = kw.strip()
    return kw if len(kw) >= 2 else ""


def _format_poi_items(item_list):
    lines = []
    for i, item in enumerate(item_list[:10], 1):
        if item is None: item = {}
        name = _safe_str(item.get("name", ""), "未知景点")
        address = _safe_str(item.get("address", ""))
        category = _safe_str(item.get("category", ""))
        poi_level = _safe_str(item.get("poiLevel", ""))
        free_status = _safe_str(item.get("freePoiStatus", ""))
        jump_url = _safe_str(item.get("jumpUrl", ""))
        main_pic = _safe_str(item.get("mainPic", ""))
        description = _safe_str(item.get("description", ""))
        ticket_info = item.get("ticketInfo")
        ticket_price = ""
        ticket_name = ""
        if ticket_info and isinstance(ticket_info, dict):
            ticket_price = _safe_str(ticket_info.get("price", ""))
            ticket_name = _safe_str(ticket_info.get("ticketName", ""))
        lines.append(str(i) + ". 🏛️ " + name)
        detail_parts = []
        if poi_level: detail_parts.append(poi_level + "A景区")
        if category: detail_parts.append(category)
        if free_status == "FREE":
            detail_parts.append("免费")
        elif free_status == "NOT_FREE" and ticket_price:
            detail_parts.append("💰 " + ticket_price)
        elif free_status == "NOT_FREE":
            detail_parts.append("需购票")
        if detail_parts: lines.append("   " + " | ".join(detail_parts))
        info_parts = []
        if address: info_parts.append("📍 " + address)
        if ticket_name and ticket_price: info_parts.append("🎫 " + ticket_name + " " + ticket_price)
        if info_parts: lines.append("   " + " | ".join(info_parts))
        if description and len(description) > 10:
            desc = description[:80] + "..." if len(description) > 80 else description
            lines.append("   📝 " + desc)
        if jump_url: lines.append("   🔗 " + jump_url)
        if main_pic: lines.append("   ![景点图片](" + main_pic + ")")
        lines.append("")
    lines.append("⚠️ 门票价格实时变动，以实际下单为准")
    return "\n".join(lines)


def search_poi(params):
    """景点门票：搜索景点门票，返回门票价格和购票链接。"""
    query = params.get("query", "")
    if not query: return "请描述景点需求，如：上海迪士尼门票"
    city = _extract_city(query)
    keyword = _extract_poi_keyword(query, city)
    if keyword:
        poi_params = {"keyword": keyword}
        if city: poi_params["cityName"] = city
        result = _call_fliggy("search_poi", poi_params)
        if isinstance(result, dict) and "error" not in result:
            inner = result.get("data", result)
            if isinstance(inner, dict):
                item_list = inner.get("itemList", [])
                if item_list:
                    header = "🏛️ 找到以下景点"
                    if city: header += "（" + city + "）"
                    if keyword: header += "（关键词：" + keyword + "）"
                    header += "：\n\n"
                    dest = _extract_dest(query) or city or ""
                    return header + _format_poi_items(item_list) + _build_tips("景点门票", dest)
    result = _call_fliggy("fliggy_ai_search", {"query": query})
    text = _parse_flyai_text(result)
    if text is None: return "未找到景点信息，建议换个描述试试"
    dest = _extract_city(query) or ""
    return text + _build_tips("景点门票", dest)


def search_marriott_hotel(params):
    """万豪酒店搜索：搜索万豪集团旗下酒店。"""
    query = params.get("query", "")
    if not query: return "请描述万豪酒店需求，如：上海万豪酒店"
    result = _call_fliggy("search_marriott_hotels", {"query": query})
    text = _parse_flyai_text(result)
    if text is None:
        result = _call_fliggy("fliggy_ai_search", {"query": query + " 万豪"})
        text = _parse_flyai_text(result)
    if text is None: return "未找到万豪酒店信息"
    dest = _extract_city(query)
    return text + _build_tips("万豪酒店", dest)


def get_marriott_hotel_info(params):
    """万豪酒店详情：获取万豪酒店详细信息。"""
    query = params.get("query", "")
    if not query: return "请提供万豪酒店名称"
    result = _call_fliggy("get_marriott_hotel_info", {"query": query})
    if isinstance(result, dict) and result.get("status") == 1:
        result = _call_fliggy("fliggy_ai_search", {"query": query + " 详细信息"})
    text = _parse_flyai_text(result)
    if text is None: return "未找到该万豪酒店详情"
    return text


def search_marriott_package(params):
    """万豪套餐搜索：搜索万豪集团在售套餐商品。"""
    query = params.get("query", "")
    if not query: return "请描述万豪套餐需求"
    result = _call_fliggy("search_marriott_packages", {"query": query})
    inner = result.get("data", result) if isinstance(result, dict) else result
    if inner is None or (isinstance(result, dict) and result.get("status") == 0 and result.get("data") is None):
        result = _call_fliggy("fliggy_ai_search", {"query": query})
    text = _parse_flyai_text(result)
    if text is None: return "未找到万豪套餐信息"
    dest = _extract_city(query)
    return text + _build_tips("万豪酒店", dest)


def search_food(params):
    """美食推荐：基于位置搜索周边餐厅美食。"""
    query = params.get("query", "")
    if not query: return "请描述美食需求，如：上海南京路附近火锅"
    dest = _extract_dest(query) or _extract_city(query)
    city = _extract_city(query)
    if not dest: dest = query.strip()[:8]
    lng, lat = _gaode_geocode(dest, city)
    if not lng: return "无法解析「" + dest + "」的位置，请告诉我具体城市和地点"
    keywords = ""
    for kw in ["火锅", "日料", "粤菜", "烧烤", "咖啡", "甜品", "川菜", "湘菜", "西餐", "海鲜", "早茶", "小吃"]:
        if kw in query: keywords = kw; break
    pois = _gaode_food_search(location=lng + "," + lat, keywords=keywords, city=city or dest, radius=3000, limit=10)
    if not pois: return "未找到" + dest + "附近的餐厅" + _build_tips("美食推荐", dest)
    lines = ["🍜 找到 " + str(len(pois)) + " 家 " + dest + "附近餐厅：", ""]
    for i, poi in enumerate(pois, 1):
        name = poi.get("name", "未知")
        type_name = poi.get("type", "")
        cuisine = ""
        if type_name:
            parts = type_name.split(";")
            if len(parts) >= 2: cuisine = parts[1]
        cuisine_tag = " [" + cuisine + "]" if cuisine else ""
        rating = poi.get("rating", "") or (poi.get("biz_ext", {}) or {}).get("rating", "")
        cost = poi.get("cost", "") or (poi.get("biz_ext", {}) or {}).get("cost", "")
        address = poi.get("address", "")
        lines.append(str(i) + ". " + name + cuisine_tag)
        detail_parts = []
        if rating and rating not in ("0", "-1"): detail_parts.append("⭐" + str(rating))
        if cost and cost not in ("0", "-1"): detail_parts.append("人均¥" + str(cost))
        if detail_parts: lines.append("   " + " | ".join(detail_parts))
        if address: lines.append("   📍 " + address)
        lines.append("")
    lines.append("💡 评分和价格仅供参考，建议出发前电话确认")
    return "\n".join(lines) + _build_tips("美食推荐", city or dest)


def search_transport(params):
    """市内交通：查询从A到B的打车预估和公交地铁路线。"""
    query = params.get("query", "")
    if not query: return "请描述交通需求，如：上海浦东机场到外滩"
    city = _extract_city(query)
    m = re.search(r"(.{2,15}?)到(.{2,15})", query)
    if not m: return "请说明出发地和目的地，如：浦东机场到外滩（上海）" + _build_tips("市内交通")
    origin = m.group(1).strip()
    destination = m.group(2).strip()
    for c in _CITIES:
        if origin.startswith(c): origin = origin[len(c):].strip(); break
    if not city: return "请告诉我城市名" + _build_tips("市内交通")

    lines = ["📍 " + origin + " → " + destination + " 交通方式", ""]

    driving = _gaode_driving(origin, destination, city)
    taxi_uri = ""
    if driving:
        lines.append("━━━ 🚗 打车/驾车 ━━━")
        lines.append("距离" + str(driving["distance_km"]) + "公里 | 约" + str(driving["duration_min"]) + "分钟 | " + driving["taxi_cost"])
        origin_lng, origin_lat = _gaode_geocode(origin, city)
        dest_lng, dest_lat = _gaode_geocode(destination, city)
        if origin_lng and dest_lng:
            taxi_uri = _gaode_take_taxi(slon=origin_lng, slat=origin_lat, sname=origin, dlon=dest_lng, dlat=dest_lat, dname=destination)
            if taxi_uri:
                lines.append("🚕 一键打车：点击直接跳高德APP打车 → " + taxi_uri)
        lines.append("")

    transit_routes = _gaode_transit(origin, destination, city)
    if transit_routes:
        real_metro = []
        real_bus = []
        for route in transit_routes:
            is_metro = False
            for seg in route.get("segments", []):
                for bl in seg.get("bus", {}).get("buslines", []):
                    if _is_metro_line(bl.get("name", "")): is_metro = True; break
            if is_metro: real_metro.append(route)
            else: real_bus.append(route)

        if real_metro:
            lines.append("━━━ 🚇 地铁/城轨 ━━━")
            for i, route in enumerate(real_metro[:2], 1):
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
                        lines.append("  " + l["name"] + ": " + l["dep"] + "→" + l["arr"])
            lines.append("")

        if real_bus:
            lines.append("━━━ 🚌 公交 ━━━")
            for i, route in enumerate(real_bus[:2], 1):
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
        return "未找到合适的交通方案，建议使用地图APP导航。" + _build_tips("市内交通", city)
    lines.append("💡 以上时间和费用为预估值，实际可能因路况变化")
    return "\n".join(lines) + _build_tips("市内交通", city)


def search_weather(params):
    """天气查询：查询目的地天气预报，辅助行程安排。"""
    query = params.get("query", "")
    if not query: return "请输入城市名查询天气，如：三亚天气预报"
    city = _extract_city(query)
    if not city:
        dest = _extract_dest(query)
        if dest:
            for c in _CITIES:
                if dest.startswith(c) or c.startswith(dest): city = c; break
        if not city: return "请告诉我城市名" + _build_tips("天气查询")

    result = _call_gaode("weather", {"city": city, "extensions": "all"})
    if not isinstance(result, dict): return "天气查询失败，请稍后重试" + _build_tips("天气查询", city)
    forecasts = result.get("forecasts", [])
    if not forecasts: return "未找到" + city + "的天气预报" + _build_tips("天气查询", city)

    forecast = forecasts[0]
    city_name = forecast.get("city", city)
    casts = forecast.get("casts", [])
    lines = ["🌤️ " + city_name + " 天气预报", ""]
    for cast in casts[:5]:
        date = cast.get("date", "")
        week = cast.get("week", "")
        dayweather = cast.get("dayweather", "")
        nightweather = cast.get("nightweather", "")
        daytemp = cast.get("daytemp", "")
        nighttemp = cast.get("nighttemp", "")
        daywind = cast.get("daywind", "")
        daypower = cast.get("daypower", "")
        weather_str = dayweather
        if nightweather and nightweather != dayweather:
            weather_str = dayweather + "转" + nightweather
        temp_str = nighttemp + "°~" + daytemp + "°" if nighttemp and daytemp else ""
        wind_str = ""
        if daywind and daypower: wind_str = daywind + daypower + "级"
        line = date + "（" + week + "） " + weather_str + " " + temp_str
        if wind_str: line = line + " " + wind_str
        lines.append(line)
    lines.append("")
    lines.append("💡 天气仅供参考，出行前请再次确认")
    return "\n".join(lines) + _build_tips("天气查询", city)


def take_taxi_link(params):
    """打车链接：生成高德一键打车链接。"""
    query = params.get("query", "")
    if not query: return "请描述打车需求，如：从浦东机场到外滩（上海）"
    city = _extract_city(query)
    m = re.search(r"(.{2,15}?)到(.{2,15})", query)
    if not m: return "请说明出发地和目的地"
    origin = m.group(1).strip()
    destination = m.group(2).strip()
    for c in _CITIES:
        if origin.startswith(c): origin = origin[len(c):].strip(); break
    if not city: return "请告诉我城市名"
    origin_lng, origin_lat = _gaode_geocode(origin, city)
    dest_lng, dest_lat = _gaode_geocode(destination, city)
    if not origin_lng or not dest_lng: return "无法解析位置，请用更具体的地址"
    uri = _gaode_take_taxi(slon=origin_lng, slat=origin_lat, sname=origin, dlon=dest_lng, dlat=dest_lat, dname=destination)
    if uri:
        return "🚕 一键打车链接：点击直接跳高德APP打车 → " + uri + "\n\n" + "📍 " + origin + " → " + destination + "（" + city + "）"
    return "无法生成打车链接，请尝试用地图APP手动叫车" + _build_tips("打车链接", city)

# ============ 新增工具（同程+途牛） ============

def _extract_two_cities(query):
    """从自然语言中提取出发城市和到达城市"""
    m = re.search(r"(.{2,6}?)到(.{2,6}?)(的|汽车|大巴|票|班次|$)", query)
    if not m:
        m = re.search(r"(.{2,6}?)至(.{2,6})", query)
    if not m:
        return ("", "")
    dep = m.group(1).strip()
    arr = m.group(2).strip()
    for c in _CITIES:
        if dep.startswith(c): dep = c; break
    for c in _CITIES:
        if arr.startswith(c): arr = c; break
    return (dep, arr)


def _extract_date(query):
    """从自然语言中提取日期，支持 明天/后天/X月X日"""
    today = datetime.now()
    if "后天" in query:
        return (today + timedelta(days=2)).strftime("%Y-%m-%d")
    if "明天" in query or "明日" in query:
        return (today + timedelta(days=1)).strftime("%Y-%m-%d")
    if "今天" in query or "今日" in query:
        return today.strftime("%Y-%m-%d")
    m = re.search(r"(\d{1,2})月(\d{1,2})[日号]", query)
    if m:
        month = int(m.group(1))
        day = int(m.group(2))
        year = today.year
        if month < today.month or (month == today.month and day < today.day):
            year += 1
        try:
            return datetime(year, month, day).strftime("%Y-%m-%d")
        except:
            pass
    m = re.search(r"(\d{4})-(\d{1,2})-(\d{1,2})", query)
    if m:
        return m.group(0)
    return today.strftime("%Y-%m-%d")


def bus_search(params):
    """汽车票搜索：查询长途汽车票和城际大巴班次。"""
    query = params.get("query", "")
    if not query: return "请描述汽车票需求，如：上海到苏州明天的汽车票"
    departure, destination = _extract_two_cities(query)
    if not departure or not destination:
        return "请说明出发城市和到达城市，如：上海到苏州的汽车票" + _build_tips("汽车票搜索")
    date = _extract_date(query)
    result = _call_tongcheng("tongcheng_bus_search", {"departure": departure, "destination": destination, "date": date})
    if isinstance(result, dict) and "error" in result:
        return "搜索失败: " + result["error"]
    item_list = []
    if isinstance(result, dict):
        inner = result.get("data")
        if isinstance(inner, dict):
            item_list = inner.get("buses", inner.get("itemList", []))
            if item_list is None: item_list = []
    if not item_list:
        return "未找到" + departure + "→" + destination + "的汽车班次，建议更换城市或日期重试" + _build_tips("汽车票搜索", destination)
    lines = ["🚌 找到 " + departure + "→" + destination + " 的汽车班次（" + date + "）：", ""]
    for i, item in enumerate(item_list[:15], 1):
        if item is None: item = {}
        name = _safe_str(item.get("coachNo", item.get("title", "")), "未知班次")
        dep_time = _safe_str(item.get("depTime", ""))
        arr_time = _safe_str(item.get("arrTime", ""))
        bus_type = _safe_str(item.get("coachType", item.get("busType", "")))
        price = _safe_str(item.get("price", ""))
        duration = _safe_str(item.get("runTimeDesc", item.get("runTime", "")))
        dep_station = _safe_str(item.get("depStationName", item.get("depStation", "")))
        arr_station = _safe_str(item.get("arrStationName", item.get("arrStation", "")))
        left_tickets = _safe_str(item.get("leftTicketNum", ""))
        redirect_url = _safe_str(item.get("redirectUrl", item.get("jumpUrl", "")))
        lines.append(str(i) + ". 🚌 " + name)
        detail_parts = []
        if dep_time: detail_parts.append("发车" + dep_time)
        if arr_time: detail_parts.append("到达" + arr_time)
        if duration: detail_parts.append("用时" + duration)
        if detail_parts: lines.append("   " + " | ".join(detail_parts))
        station_parts = []
        if dep_station: station_parts.append(dep_station)
        if arr_station: station_parts.append(arr_station)
        if station_parts: lines.append("   📍 " + " → ".join(station_parts))
        extra_parts = []
        if bus_type: extra_parts.append("🚐 " + bus_type)
        if price and price != "0": extra_parts.append("💰 ¥" + price)
        if left_tickets and left_tickets != "0": extra_parts.append("🎫 余" + left_tickets + "张")
        if extra_parts: lines.append("   " + " | ".join(extra_parts))
        if redirect_url: lines.append("   🔗 预订: " + redirect_url)
        lines.append("")
    lines.append("⚠️ 班次和票价实时变动，以实际下单为准")
    return "\n".join(lines) + _build_tips("汽车票搜索", destination)


def travel_search(params):
    """跟团游搜索：搜索跟团游和自由行旅游产品。"""
    query = params.get("query", "")
    if not query: return "请描述跟团游需求，如：三亚跟团游、日本亲子游"
    # 提取目的地
    dest = _extract_dest(query) or _extract_city(query) or ""
    if not dest:
        for kw in ["日本", "韩国", "东南亚", "欧洲", "美国", "澳洲", "泰国", "越南", "柬埔寨", "云南", "西藏", "新疆"]:
            if kw in query:
                dest = kw
                break
    if not dest:
        dest = query.strip()[:6]
    # 提取主题关键词
    keyword = ""
    for kw in ["亲子", "蜜月", "温泉", "海岛", "滑雪", "潜水", "自驾", "古镇", "红色", "研学"]:
        if kw in query:
            keyword = kw
            break
    proxy_params = {"destination": dest}
    if keyword:
        proxy_params["keyword"] = keyword
    result = _call_tongcheng("tongcheng_travel_search", proxy_params)
    if isinstance(result, dict) and "error" in result:
        return "搜索失败: " + result["error"]
    item_list = []
    if isinstance(result, dict):
        inner = result.get("data")
        if isinstance(inner, dict):
            item_list = inner.get("trips", inner.get("itemList", []))
            if item_list is None: item_list = []
    if not item_list:
        hint = "，主题「" + keyword + "」" if keyword else ""
        return "未找到去" + dest + "的跟团游产品" + hint + "，建议更换目的地或主题重试" + _build_tips("跟团游", dest)
    lines = ["👥 找到去" + dest + "的跟团游/自由行产品", ""]
    for i, item in enumerate(item_list[:15], 1):
        if item is None: item = {}
        name = _safe_str(item.get("name", item.get("title", "")), "未知产品")
        price = _safe_str(item.get("price", ""))
        days_match = re.search(r'(\d+)天(\d+)?晚?', name)
        days_str = (days_match.group(1) + "天" + (days_match.group(2) + "晚" if days_match and days_match.group(2) else "")) if days_match else ""
        label_list = item.get("labelList", [])
        if isinstance(label_list, list) and label_list:
            labels = "、".join(str(l) for l in label_list if l)
        else:
            labels = _safe_str(item.get("tag", item.get("tags", "")))
        dest_list = item.get("destList", [])
        if isinstance(dest_list, list) and dest_list:
            dest_str = "、".join(str(d) for d in dest_list if d)
        else:
            dest_str = _safe_str(item.get("destination", item.get("destCity", "")))
        jump_url = _safe_str(item.get("redirectUrl", item.get("jumpUrl", item.get("clawRedirectUrl", ""))))
        comment_num = _safe_str(item.get("commentNum", ""))
        scenery_list = item.get("sceneryNameList", [])
        if isinstance(scenery_list, list) and scenery_list:
            scenery_str = "、".join(str(s) for s in scenery_list[:5] if s)
            if len(scenery_list) > 5:
                scenery_str += "等" + str(len(scenery_list)) + "个景点"
        else:
            scenery_str = ""
        lines.append(str(i) + ". 👥 " + name)
        detail_parts = []
        if days_str: detail_parts.append("📅 " + days_str)
        if price and price != "0": detail_parts.append("💰 ¥" + price + "起")
        if comment_num: detail_parts.append("💬 " + comment_num + "条评价")
        if detail_parts: lines.append("   " + " | ".join(detail_parts))
        if dest_str: lines.append("   📍 目的地: " + dest_str)
        if scenery_str: lines.append("   🏛️ 含景点: " + scenery_str)
        if labels: lines.append("   🏷️ " + labels)
        if jump_url: lines.append("   🔗 预订: " + jump_url)
        lines.append("")
    lines.append("⚠️ 价格实时变动，以实际下单为准")
    return "\n".join(lines) + _build_tips("跟团游", dest)


def cruise_search(params):
    """邮轮搜索：搜索邮轮旅游产品，支持按航线查询。"""
    query = params.get("query", "")
    if not query: return "请描述邮轮需求，如：日本邮轮、东南亚航线"
    # 提取航线关键词
    cruise_line = ""
    for kw in ["日本", "韩国", "东南亚", "地中海", "加勒比", "阿拉斯加", "北欧", "三峡", "南极", "北极"]:
        if kw in query:
            cruise_line = kw
            break
    # 日期范围默认：今天 ~ +90天
    today = datetime.now()
    date_begin = today.strftime("%Y-%m-%d")
    date_end = (today + timedelta(days=90)).strftime("%Y-%m-%d")
    proxy_params = {"departsDateBegin": date_begin, "departsDateEnd": date_end}
    if cruise_line:
        proxy_params["cruiseLineName"] = cruise_line
    result = _call_tuniu("tuniu_cruise_search", proxy_params)
    if isinstance(result, dict) and "error" in result:
        return "搜索失败: " + result["error"]
    # 途牛邮轮API返回三层嵌套: proxy.data.data.rows
    item_list = []
    if isinstance(result, dict):
        inner = result.get("data")
        if isinstance(inner, dict):
            if not inner.get("success", True):
                msg = _safe_str(inner.get("msg", ""))
                if msg:
                    return "API返回失败: " + msg
            real_data = inner.get("data", {})
            if isinstance(real_data, dict):
                item_list = real_data.get("rows", [])
                if item_list is None: item_list = []
    if not item_list:
        hint = "「" + cruise_line + "」" if cruise_line else ""
        return "未找到" + hint + "邮轮产品，建议更换航线或日期重试" + _build_tips("邮轮搜索", cruise_line)
    header = "🚢 找到以下邮轮产品"
    if cruise_line:
        header += "（航线：" + cruise_line + "）"
    header += "（" + date_begin + " ~ " + date_end + "）：\n\n"
    lines = [header]
    for i, item in enumerate(item_list[:15], 1):
        if item is None: item = {}
        product_name = _safe_str(item.get("productName", ""), "未知邮轮产品")
        cruise_brand = _safe_str(item.get("cruiseBrand", ""))
        tour_day = _safe_str(item.get("tourDay", ""))
        price = _safe_str(item.get("price", ""))
        satisfaction = _safe_str(item.get("satisfaction", ""))
        people_num = _safe_str(item.get("peopleNum", ""))
        departure_port = _safe_str(item.get("departurePortName", ""))
        ticket_type = _safe_str(item.get("ticketTypeName", ""))
        departs_date_begin = _safe_str(item.get("departsDateBegin", ""))
        departs_date_end = _safe_str(item.get("departsDateEnd", ""))
        product_id = _safe_str(item.get("productId", ""))
        depart_cities = item.get("departCityName", [])
        if isinstance(depart_cities, list) and depart_cities:
            depart_city = _safe_str(depart_cities[0])
        else:
            depart_city = _safe_str(depart_cities)
        cruise_lines = item.get("cruiseLineName", [])
        if isinstance(cruise_lines, list) and cruise_lines:
            cruise_line_str = "、".join([_safe_str(c) for c in cruise_lines if c])
        else:
            cruise_line_str = _safe_str(cruise_lines)
        tags = item.get("customConditionName", [])
        if isinstance(tags, list) and tags:
            tag_str = " | ".join([_safe_str(t) for t in tags[:3] if t])
        else:
            tag_str = ""
        booking_url = "https://www.tuniu.com/tour/" + product_id if product_id else ""
        lines.append(str(i) + ". 🚢 " + product_name)
        detail_parts = []
        if cruise_brand: detail_parts.append("🛳️ " + cruise_brand)
        if tour_day and tour_day != "0": detail_parts.append("📅 " + tour_day + "天行程")
        if price and price != "0": detail_parts.append("💰 ¥" + price + "起")
        if ticket_type: detail_parts.append("🎫 " + ticket_type)
        if detail_parts: lines.append("   " + " | ".join(detail_parts))
        info_parts = []
        if depart_city: info_parts.append("出发城市: " + depart_city)
        if departure_port: info_parts.append("登船港: " + departure_port)
        if cruise_line_str: info_parts.append("航线: " + cruise_line_str)
        if departs_date_begin and departs_date_end: info_parts.append("出发日期: " + departs_date_begin + " ~ " + departs_date_end)
        if info_parts: lines.append("   📍 " + " | ".join(info_parts))
        rating_parts = []
        if satisfaction and satisfaction != "0": rating_parts.append("满意度" + satisfaction + "%")
        if people_num and people_num != "0": rating_parts.append(people_num + "人出游")
        if rating_parts: lines.append("   📊 " + " | ".join(rating_parts))
        if tag_str: lines.append("   🏷️ " + tag_str)
        if booking_url: lines.append("   🔗 " + booking_url)
        pic_url = _safe_str(item.get("picUrl", ""))
        if pic_url: lines.append("   ![邮轮图片](" + pic_url + ")")
        lines.append("")
    lines.append("⚠️ 价格实时变动，以实际下单为准")
    return "\n".join(lines) + _build_tips("邮轮搜索", cruise_line)


def holiday_search(params):
    """度假线路搜索：搜索度假旅游线路产品，支持按关键词和出发城市筛选。"""
    query = params.get("query", "")
    if not query: return "请描述度假需求，如：三亚度假、从上海出发去日本"
    # 提取关键词
    keyword = ""
    for kw in ["三亚", "日本", "云南", "西藏", "新疆", "泰国", "越南", "欧洲", "美国", "澳洲", "韩国", "柬埔寨", "新加坡", "马来西亚"]:
        if kw in query:
            keyword = kw
            break
    if not keyword:
        keyword = _extract_dest(query) or _extract_city(query) or ""
    # 提取出发城市
    depart_city = ""
    for c in _CITIES:
        if c + "出发" in query or "从" + c in query:
            depart_city = c
            break
    proxy_params = {}
    if keyword:
        proxy_params["keyword"] = keyword
    if depart_city:
        proxy_params["departCityName"] = depart_city
    result = _call_tuniu("tuniu_holiday_search", proxy_params)
    if isinstance(result, dict) and "error" in result:
        return "搜索失败: " + result["error"]
    # 途牛度假API返回三层嵌套: proxy.data.data.rows
    item_list = []
    if isinstance(result, dict):
        inner = result.get("data")
        if isinstance(inner, dict):
            if not inner.get("success", True):
                msg = _safe_str(inner.get("msg", ""))
                if msg:
                    return "API返回失败: " + msg
            real_data = inner.get("data", {})
            if isinstance(real_data, dict):
                item_list = real_data.get("rows", [])
                if item_list is None: item_list = []
    if not item_list:
        hints = []
        if keyword: hints.append("关键词「" + keyword + "」")
        if depart_city: hints.append("从" + depart_city + "出发")
        hint = "、".join(hints)
        return "未找到" + hint + "的度假产品，建议调整条件重试" + _build_tips("度假线路", keyword)
    is_hot = not keyword and not depart_city
    if is_hot:
        header = "🏖️ 热门度假产品推荐：\n\n"
    else:
        header = "🏖️ 找到以下度假产品"
        conditions = []
        if keyword: conditions.append("关键词：" + keyword)
        if depart_city: conditions.append("出发：" + depart_city)
        if conditions:
            header += "（" + " | ".join(conditions) + "）"
        header += "：\n\n"
    lines = [header]
    for i, item in enumerate(item_list[:15], 1):
        if item is None: item = {}
        product_name = _safe_str(item.get("productName", ""), "未知度假产品")
        tour_day = _safe_str(item.get("tourDay", ""))
        price = _safe_str(item.get("price", ""))
        satisfaction = _safe_str(item.get("satisfaction", ""))
        people_num = _safe_str(item.get("peopleNum", ""))
        product_id = _safe_str(item.get("productId", ""))
        is_new = _safe_str(item.get("isNewproduct", ""))
        depart_cities = item.get("departCityName", [])
        if isinstance(depart_cities, list) and depart_cities:
            depart_city_str = "、".join([_safe_str(c) for c in depart_cities if c])
        else:
            depart_city_str = _safe_str(depart_cities)
        tags = item.get("customConditionName", [])
        if isinstance(tags, list) and tags:
            tag_str = " | ".join([_safe_str(t) for t in tags[:3] if t])
        else:
            tag_str = ""
        booking_url = "https://www.tuniu.com/tour/" + product_id if product_id else ""
        display_name = product_name
        if is_new and is_new != "0":
            display_name = "🆕 " + display_name
        lines.append(str(i) + ". 🏖️ " + display_name)
        detail_parts = []
        if tour_day and tour_day != "0": detail_parts.append("📅 " + tour_day + "天行程")
        if price and price != "0": detail_parts.append("💰 ¥" + price + "起")
        if depart_city_str: detail_parts.append("🚩 " + depart_city_str + "出发")
        if detail_parts: lines.append("   " + " | ".join(detail_parts))
        rating_parts = []
        if satisfaction and satisfaction != "0": rating_parts.append("满意度" + satisfaction + "%")
        if people_num and people_num != "0": rating_parts.append(people_num + "人出游")
        if rating_parts: lines.append("   📊 " + " | ".join(rating_parts))
        if tag_str: lines.append("   🏷️ " + tag_str)
        if booking_url: lines.append("   🔗 " + booking_url)
        lines.append("")
    lines.append("⚠️ 价格实时变动，以实际下单为准")
    return "\n".join(lines) + _build_tips("度假线路", keyword)
