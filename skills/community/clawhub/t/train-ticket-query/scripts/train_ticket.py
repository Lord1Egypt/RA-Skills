# -*- coding: utf-8 -*-
"""
火车票查询 - ClawHub技能脚本
零配置即装即用，通过SCF代理调用飞猪+高德API + 12306余票直查
3个工具：火车票查询（含余票）、去火车站交通、住宿推荐
"""
import os
import json
import re
import time
import urllib.request
import urllib.error
from datetime import datetime, timedelta

# ============ 配置 ============
FLIGGY_PROXY = "https://1439498936-6sysdjjt99.ap-guangzhou.tencentscf.com"
GAODE_PROXY = "https://1439498936-bl10af74fl.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")
TIMEOUT = 30

# 12306站名编码缓存
_STATION_MAP = None
_STATION_MAP_TS = 0
_STATION_MAP_TTL = 86400  # 24小时过期

_CITIES = [
    "北京", "上海", "广州", "深圳", "成都", "杭州", "南京", "武汉", "长沙", "重庆",
    "西安", "厦门", "青岛", "大连", "昆明", "丽江", "桂林", "苏州", "珠海", "海口",
    "三亚", "天津", "济南", "沈阳", "哈尔滨", "长春", "郑州", "合肥", "福州", "南昌",
    "太原", "石家庄", "贵阳", "南宁", "兰州", "银川", "呼和浩特", "乌鲁木齐", "拉萨",
    "无锡", "宁波", "温州", "烟台", "威海", "佛山", "东莞", "中山", "惠州", "扬州",
]


# ============ 代理调用 ============
def _call_fliggy(rtype, params, timeout=None):
    body = json.dumps({"type": rtype, "params": params}, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(
        FLIGGY_PROXY, data=body,
        headers={"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN},
        method="POST",
    )
    _timeout = timeout or TIMEOUT
    try:
        with urllib.request.urlopen(req, timeout=_timeout) as r:
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
        with urllib.request.urlopen(req, timeout=15) as r:
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


# ============ 12306站名编码 ============
def _get_station_map():
    """下载并缓存12306站名编码表"""
    global _STATION_MAP, _STATION_MAP_TS
    now = time.time()
    if _STATION_MAP and (now - _STATION_MAP_TS) < _STATION_MAP_TTL:
        return _STATION_MAP

    url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            text = r.read().decode("utf-8")
        m = re.search(r"'(.+)'", text)
        if not m:
            return _STATION_MAP or {}
        entries = m.group(1).split("@")
        smap = {}
        for entry in entries:
            parts = entry.split("|")
            if len(parts) >= 3:
                name = parts[1]
                code = parts[2]
                if name and code:
                    smap[name] = code
        if smap:
            _STATION_MAP = smap
            _STATION_MAP_TS = now
        return _STATION_MAP or {}
    except Exception:
        return _STATION_MAP or {}


def _get_station_code(station_name):
    """获取火车站3字码"""
    smap = _get_station_map()
    if not smap:
        return ""
    code = smap.get(station_name)
    if code:
        return code
    if station_name.endswith("站"):
        code = smap.get(station_name[:-1])
        if code:
            return code
    for name, code in smap.items():
        if station_name in name or name in station_name:
            return code
    return ""


# ============ 12306余票查询 ============
def _query_12306_tickets(dep_code, arr_code, date):
    """查询12306余票信息"""
    url = f"https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={date}&leftTicketDTO.from_station_telecode={dep_code}&leftTicketDTO.to_station_telecode={arr_code}&purpose_codes=ADULT"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode("utf-8"))
    except Exception:
        return {}

    if data.get("httpstatus") != 200:
        return {}

    result = data.get("data", {})
    if isinstance(result, dict) and "result" in result:
        raw_list = result["result"]
    elif isinstance(result, list):
        raw_list = result
    else:
        return {}

    tickets = {}
    for raw in raw_list:
        parts = raw.split("|")
        if len(parts) < 21:
            continue
        train_no = parts[3]
        ticket_info = {
            "swz": parts[32] if len(parts) > 32 else "",
            "zy": parts[31] if len(parts) > 31 else "",
            "ze": parts[30] if len(parts) > 30 else "",
            "rw": parts[23] if len(parts) > 23 else "",
            "yw": parts[28] if len(parts) > 28 else "",
            "yz": parts[29] if len(parts) > 29 else "",
            "wz": parts[26] if len(parts) > 26 else "",
        }
        tickets[train_no] = ticket_info
    return tickets


def _get_remaining_tickets(data, date):
    """从飞猪结果中提取站名对，查询12306余票"""
    if isinstance(data, dict) and "error" in data:
        return {}
    inner = data.get("data", data) if isinstance(data, dict) else data
    if not isinstance(inner, dict) or inner is None:
        return {}
    item_list = inner.get("itemList", [])
    if not item_list:
        return {}

    station_pairs = set()
    for item in item_list:
        for journey in item.get("journeys", []):
            for seg in journey.get("segments", []):
                dep = seg.get("depStationShortName", seg.get("depStationName", ""))
                arr = seg.get("arrStationShortName", seg.get("arrStationName", ""))
                if dep and arr:
                    station_pairs.add((dep, arr))
    if not station_pairs:
        return {}

    all_tickets = {}
    for dep_station, arr_station in list(station_pairs)[:3]:
        dep_code = _get_station_code(dep_station)
        arr_code = _get_station_code(arr_station)
        if dep_code and arr_code:
            tickets = _query_12306_tickets(dep_code, arr_code, date)
            all_tickets.update(tickets)
            time.sleep(0.3)
    return all_tickets


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
                lng, lat = loc.split(",")
                return (lng, lat)
    return (None, None)


def _gaode_driving(origin, destination, city):
    params = {"origin_address": origin, "origin_city": city, "destination_address": destination, "destination_city": city, "strategy": "0"}
    data = _call_gaode("driving_route_by_address", params)
    if isinstance(data, dict) and data.get("status") == "1":
        paths = data.get("route", {}).get("paths", [])
        if paths:
            path = paths[0]
            distance = int(float(path.get("distance", 0)))
            duration = int(float(path.get("duration", 0)))
            return {
                "distance_km": round(distance / 1000, 1),
                "duration_min": round(duration / 60),
                "taxi_cost": _estimate_taxi_cost(distance),
            }
    return {}


def _gaode_transit(origin, destination, city):
    params = {"origin_address": origin, "origin_city": city, "destination_address": destination, "destination_city": city, "city": city, "strategy": "0"}
    data = _call_gaode("transit_route_by_address", params)
    if isinstance(data, dict) and data.get("status") == "1":
        return data.get("route", {}).get("transits", [])
    return []


def _estimate_taxi_cost(distance_m):
    distance_km = distance_m / 1000
    if distance_km <= 0: return "¥0"
    if distance_km <= 3: return "¥14左右"
    cost = 14 + (distance_km - 3) * 2.5
    return f"¥{int(cost)}左右"


def _is_metro_line(line_name):
    metro_keywords = ["地铁", "号线", "城轨", "磁浮", "市域", "轻轨"]
    return any(kw in line_name for kw in metro_keywords)


# ============ 日期智能解析 ============
def _smart_parse_date(date_str):
    now = datetime.now()
    today = now.date()
    if not date_str or not date_str.strip():
        if now.hour >= 20:
            default_date = today + timedelta(days=1)
            return (default_date.strftime("%Y-%m-%d"), f"您未指定日期，已默认查询明天（{default_date.strftime('%m月%d日')}）的车票")
        else:
            return (today.strftime("%Y-%m-%d"), f"您未指定日期，已默认查询今天（{today.strftime('%m月%d日')}）的车票")

    s = date_str.strip()
    year = now.year

    m = re.match(r'^(\d{4})[-/](\d{1,2})[-/](\d{1,2})$', s)
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        try: parsed = datetime(y, mo, d).date()
        except ValueError: return ("", f"日期格式有误：{date_str}")
        return _validate_date(parsed, today, date_str)

    m = re.match(r'^(\d{1,2})月(\d{1,2})日?$', s)
    if m:
        mo, d = int(m.group(1)), int(m.group(2))
        try: parsed = datetime(year, mo, d).date()
        except ValueError: return ("", f"日期格式有误：{date_str}")
        if parsed < today:
            try:
                next_year = datetime(year + 1, mo, d).date()
                if next_year <= today + timedelta(days=30):
                    return (next_year.strftime("%Y-%m-%d"), f"已自动调整为明年{mo}月{d}日")
            except ValueError: pass
        return _validate_date(parsed, today, date_str)

    m = re.match(r'^(\d{1,2})[-/](\d{1,2})$', s)
    if m:
        mo, d = int(m.group(1)), int(m.group(2))
        try: parsed = datetime(year, mo, d).date()
        except ValueError: return ("", f"日期格式有误：{date_str}")
        if parsed < today:
            try:
                next_year = datetime(year + 1, mo, d).date()
                if next_year <= today + timedelta(days=30):
                    return (next_year.strftime("%Y-%m-%d"), f"已自动调整为明年{mo}月{d}日")
            except ValueError: pass
        return _validate_date(parsed, today, date_str)

    if s == "今天": return (today.strftime("%Y-%m-%d"), "")
    if s == "明天": return ((today + timedelta(days=1)).strftime("%Y-%m-%d"), "")
    if s == "后天": return ((today + timedelta(days=2)).strftime("%Y-%m-%d"), "")

    return ("", f"无法识别日期格式：{date_str}，请输入如\"6月15日\"、\"6-15\"、\"明天\"等格式")


def _validate_date(parsed, today, date_str):
    if parsed < today:
        return (today.strftime("%Y-%m-%d"), f"您输入的{date_str}已过，已自动为您查询今天（{today.strftime('%m月%d日')}）的车票")
    if parsed > today + timedelta(days=30):
        return ("", f"暂无法查询{parsed.strftime('%m月%d日')}的车票，目前可查询未来30天内的车票")
    return (parsed.strftime("%Y-%m-%d"), "")


# ============ 工具1：火车票查询（含12306余票） ============
def _format_duration(minutes_str):
    try:
        minutes = int(minutes_str)
        h, m = divmod(minutes, 60)
        if h > 0 and m > 0: return f"{h}h{m}m"
        if h > 0: return f"{h}h"
        return f"{m}m"
    except (ValueError, TypeError):
        return str(minutes_str) if minutes_str else ""


def _format_datetime(dt_str):
    try:
        return dt_str.split(" ")[1][:5] if " " in dt_str else dt_str
    except (IndexError, TypeError):
        return str(dt_str) if dt_str else ""


def _is_same_station_transfer(journey):
    segments = journey.get("segments", [])
    if len(segments) < 2: return True
    for i in range(len(segments) - 1):
        arr = segments[i].get("arrStationShortName", segments[i].get("arrStationName", ""))
        dep = segments[i + 1].get("depStationShortName", segments[i + 1].get("depStationName", ""))
        if arr != dep: return False
    return True


def _format_single_train(lines, idx, item, ticket_info=None):
    journeys = item.get("journeys", [])
    if not journeys: return
    journey = journeys[0]
    segments = journey.get("segments", [])
    if not segments: return

    price = item.get("price", "")
    jump_url = item.get("jumpUrl", "")
    total_duration = item.get("totalDuration", "")
    seg = segments[0]
    train_type = seg.get("marketingTransportName", "")
    train_no = seg.get("marketingTransportNo", "")
    dep_short = seg.get("depStationShortName", seg.get("depStationName", ""))
    dep_time = _format_datetime(seg.get("depDateTime", ""))
    last_seg = segments[-1]
    arr_short = last_seg.get("arrStationShortName", last_seg.get("arrStationName", ""))
    arr_time = _format_datetime(last_seg.get("arrDateTime", ""))
    seat_class = seg.get("seatClassName", "")
    journey_type = journey.get("journeyType", "")

    if journey_type == "直达":
        type_label = "直达"
    else:
        type_label = "同站换乘" if _is_same_station_transfer(journey) else "跨站换乘"

    lines.append(f"**{idx}. {train_type} {train_no}** [{type_label}]")
    duration_str = _format_duration(total_duration) if total_duration else ""
    lines.append(f"   {dep_time} {dep_short} → {arr_time} {arr_short}（{duration_str}）")
    price_str = f"¥{price}" if price else "票价待查"
    seat_str = f" | {seat_class}" if seat_class else ""
    lines.append(f"   💰 {price_str}{seat_str}")

    # 12306余票
    if ticket_info and train_no in ticket_info:
        tickets = ticket_info[train_no]
        ticket_parts = []
        seat_order = [
            ("swz", "商务座"), ("zy", "一等座"), ("ze", "二等座"),
            ("rw", "软卧"), ("yw", "硬卧"), ("yz", "硬座"), ("wz", "无座"),
        ]
        for key, label in seat_order:
            val = tickets.get(key, "")
            if val:
                ticket_parts.append(f"{label}{val}")
        if ticket_parts:
            lines.append(f"   🎫 余票: {' | '.join(ticket_parts)}")

    if len(segments) > 1:
        transfer_duration = journey.get("transferDuration", "")
        for j, s in enumerate(segments, 1):
            s_type = s.get("marketingTransportName", "")
            s_no = s.get("marketingTransportNo", "")
            s_dep = _format_datetime(s.get("depDateTime", ""))
            s_arr = _format_datetime(s.get("arrDateTime", ""))
            s_dep_station = s.get("depStationShortName", s.get("depStationName", ""))
            s_arr_station = s.get("arrStationShortName", s.get("arrStationName", ""))
            lines.append(f"   ├ 第{j}段: {s_type} {s_no} {s_dep_station}{s_dep}→{s_arr_station}{s_arr}")
        if transfer_duration:
            lines.append(f"   ├ 中转等候: {_format_duration(transfer_duration)}")

    if jump_url:
        lines.append(f"   🔗 [预订→]({jump_url})")
    lines.append("")


def search_train(params):
    """火车票查询：查询火车票/高铁票的余票、价格和时刻表，含12306实时余票信息。"""
    departure = params.get("departure", "")
    destination = params.get("destination", "")
    dep_date = params.get("dep_date", "")
    seat_class = params.get("seat_class", "")
    transport_no = params.get("transport_no", "")

    if not departure: return "请提供出发城市，如：上海、北京"
    if not destination: return "请提供到达城市，如：北京、成都"

    parsed_date, date_hint = _smart_parse_date(dep_date)
    if not parsed_date: return date_hint

    args = {
        "origin": departure,
        "destination": destination,
        "depDate": parsed_date,
        "limit": 10,
    }
    if seat_class: args["seatClassName"] = seat_class
    if transport_no: args["transportNo"] = transport_no

    result = _call_fliggy("search_domestic_train", args)
    if isinstance(result, dict) and "error" in result:
        return "火车票查询失败: " + result["error"]

    ticket_info = {}
    try:
        ticket_info = _get_remaining_tickets(result, parsed_date)
    except Exception:
        pass

    inner = result.get("data", result)
    if inner is None:
        return f"😔 未找到{departure}→{destination}的火车票。可能该路线暂无直达或换乘方案，建议更换城市或调整日期。"

    item_list = inner.get("itemList", []) if isinstance(inner, dict) else []
    if not item_list:
        return f"未找到{departure}→{destination}的火车票。建议调整日期或城市后重试。"

    lines = [f"🚄 找到 {len(item_list)} 个车次方案 {departure}→{destination}（{parsed_date}）：", ""]

    direct_trains = []
    same_station_transit = []
    cross_station_transit = []
    for item in item_list:
        journeys = item.get("journeys", [])
        if journeys:
            jtype = journeys[0].get("journeyType", "")
            if jtype == "直达":
                direct_trains.append(item)
            elif _is_same_station_transfer(journeys[0]):
                same_station_transit.append(item)
            else:
                cross_station_transit.append(item)

    if direct_trains:
        lines.append(f"━━━ 直达车次 ({len(direct_trains)}个) ━━━")
        lines.append("")
        for i, item in enumerate(direct_trains, 1):
            _format_single_train(lines, i, item, ticket_info)

    if same_station_transit:
        lines.append(f"━━━ 同站换乘 ({len(same_station_transit)}个) ━━━")
        lines.append("")
        for i, item in enumerate(same_station_transit, 1):
            idx = len(direct_trains) + i
            _format_single_train(lines, idx, item, ticket_info)

    if cross_station_transit:
        lines.append(f"⚠️ 另有{len(cross_station_transit)}个跨站换乘方案未展示，如需查看请说「显示跨站换乘」")
        lines.append("")

    lines.append("⚠️ 票价和余票实时变动，以实际下单为准")
    lines.append("💡 点击预订链接可直接跳转购买")
    lines.append("")
    lines.append("📋 退票规则：开车前8天以上免手续费 | 48小时~8天扣5% | 24~48小时扣10% | 不足24小时扣20%")
    lines.append("")
    lines.append("📋 附加服务：1、查去火车站怎么走 2、推荐合适的住宿，回复数字即可")

    text = "\n".join(lines)
    if date_hint:
        text = f"📅 {date_hint}\n\n{text}"
    return text


# ============ 工具2：去火车站交通 ============
def query_transport(params):
    """去火车站交通：查询从出发地到火车站的打车预估和公交地铁路线。"""
    origin = params.get("origin", "")
    train_station = params.get("train_station", "")
    city = params.get("city", "")

    if not origin: return "请提供出发地，如：浦东机场、南京路100号"
    if not train_station: return "请提供火车站名，如：上海虹桥站、北京南站"
    if not city: return "请提供城市名，如：上海、北京"

    lines = [f"📍 {origin} → {train_station} 交通方式", ""]

    driving = _gaode_driving(origin, train_station, city)
    if driving:
        lines.append("━━━ 🚗 打车/驾车 ━━━")
        lines.append(f"距离{driving['distance_km']}公里 | 约{driving['duration_min']}分钟 | {driving['taxi_cost']}")
        lines.append("💡 可打开微信/支付宝「滴滴出行」小程序叫车")
        lines.append("")

    transit_routes = _gaode_transit(origin, train_station, city)
    if transit_routes:
        metro_routes = []
        bus_routes = []
        for route in transit_routes[:6]:
            is_metro = False
            for seg in route.get("segments", []):
                for bl in seg.get("bus", {}).get("buslines", []):
                    if _is_metro_line(bl.get("name", "")): is_metro = True; break
            if is_metro:
                metro_routes.append(route)
            else:
                bus_routes.append(route)

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
                cost_str = f"¥{cost}" if cost and cost != "0" else ""
                line_names = " → ".join(l["name"] for l in all_lines)
                detail_parts = [f"约{round(duration / 60)}分钟"]
                if cost_str: detail_parts.append(cost_str)
                lines.append(f"方案{i}: {line_names} | {' '.join(detail_parts)}")
                for l in all_lines:
                    if l["dep"] or l["arr"]:
                        lines.append(f"  {l['name']}: {l['dep']}→{l['arr']}")
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
                cost_str = f"¥{cost}" if cost and cost != "0" else ""
                line_names = " → ".join(all_lines)
                detail_parts = [f"约{round(duration / 60)}分钟"]
                if cost_str: detail_parts.append(cost_str)
                lines.append(f"方案{i}: {line_names} | {' '.join(detail_parts)}")
            lines.append("")

    if not driving and not transit_routes:
        return "未找到合适的交通方案，建议使用地图APP导航。"

    lines.append("💡 以上时间和费用为预估值，实际可能因路况变化")
    return "\n".join(lines)


# ============ 工具3：住宿推荐 ============
def _extract_city(text):
    for city in _CITIES:
        if city in text: return city
    return ""


def recommend_hotel(params):
    """住宿推荐：用自然语言描述住宿需求，AI智能匹配高分酒店并返回推荐和预订链接。"""
    query = params.get("query", "")
    if not query: return "请描述你的住宿需求，如：住哪个区域，预算多少，有什么偏好？"

    result = _call_fliggy("fliggy_ai_search", {"query": query}, timeout=60)
    if isinstance(result, dict) and "error" in result:
        return "住宿推荐失败: " + result["error"]

    inner = result.get("data", result) if isinstance(result, dict) else result
    if inner is None:
        return "😔 未找到符合条件的酒店。建议调整搜索条件后重试。"

    if isinstance(inner, str):
        content_text = inner
    elif isinstance(inner, dict):
        data_inner = inner.get("data")
        if isinstance(data_inner, str):
            content_text = data_inner
            sys_msg = inner.get("systemMessage")
            if sys_msg:
                content_text += f"\n\n📌 {sys_msg}"
        elif isinstance(data_inner, dict):
            items = data_inner.get("itemList", [])
            if items:
                lines = [f"🏨 找到 {len(items)} 家酒店：", ""]
                for i, h in enumerate(items[:10], 1):
                    info = h.get("info", h)
                    name = info.get("title", h.get("name", ""))
                    price = info.get("price", h.get("price", ""))
                    url = info.get("detailUrl", h.get("detailUrl", "")) or info.get("jumpUrl", "")
                    lines.append(f"**{i}. {name}**")
                    if price: lines.append(f"   💰 {price}")
                    if url: lines.append(f"   🔗 [预订→]({url})")
                    lines.append("")
                content_text = "\n".join(lines)
            else:
                content_text = "😔 未找到符合条件的酒店。建议调整搜索条件后重试。"
        else:
            content_text = "😔 未找到符合条件的酒店。"
    else:
        content_text = str(inner)

    content_text += "\n\n📋 附加服务："
    content_text += "\n· 回复1 → 查询前往酒店的交通路线"
    content_text += "\n· 回复2 → 查询火车票"
    return content_text
