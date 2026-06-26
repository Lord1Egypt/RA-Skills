#!/usr/bin/env python3
"""途牛旅行助手 v2.0.0 - 酒店/机票/火车票/景点门票/邮轮/度假全品类查询预订
17个工具覆盖途牛全品类API，含图片渲染和服务间互推荐"""

import sys
import json
import os
import ssl
import urllib.request
import urllib.error
from datetime import datetime, timedelta

_ALLOWED_PROXY_HOSTS = [
    "ap-guangzhou.tencentscf.com",
]

PROXY_URL = os.environ.get("PROXY_URL", "")
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")


def _validate_proxy_url(url):
    if not url:
        return False
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        host = parsed.hostname or ""
        return any(host.endswith(allowed) for allowed in _ALLOWED_PROXY_HOSTS)
    except Exception:
        return False


def _post(type_name, params):
    if not _validate_proxy_url(PROXY_URL):
        return {"error": "PROXY_URL未配置或指向未授权主机，仅允许腾讯云SCF代理端点"}
    if not PROXY_TOKEN:
        return {"error": "PROXY_TOKEN未配置"}

    ctx = ssl.create_default_context()
    ctx.verify_mode = ssl.CERT_REQUIRED
    ctx.check_hostname = True

    body = json.dumps({"type": type_name, "params": params}, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(PROXY_URL, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("X-Proxy-Token", PROXY_TOKEN)
    try:
        with urllib.request.urlopen(req, timeout=120, context=ctx) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("code") == 0:
                return data.get("data", {})
            return data
    except urllib.error.HTTPError as e:
        err = ""
        try:
            err = e.read().decode("utf-8")[:300]
        except:
            pass
        return {"error": "HTTP " + str(e.code) + ": " + err}
    except Exception as e:
        return {"error": str(e)}


# ==================== 格式化层 ====================

def _format_hotel_list(result, city_name):
    if isinstance(result, dict) and result.get("error"):
        return result
    hotels = result.get("hotels", []) if isinstance(result, dict) else []
    if not hotels:
        return result

    lines = ["**" + city_name + "** 酒店推荐：\n"]
    for i, h in enumerate(hotels[:10], 1):
        name = h.get("hotelName", "未知")
        star = h.get("starName", "")
        price = h.get("lowestPrice", "")
        score = h.get("commentScore", "")
        pic = h.get("firstPic", "")

        details = []
        if star: details.append(star)
        if price: details.append("¥" + str(price) + "起")
        if score: details.append(str(score) + "分")
        line = "**" + str(i) + ". " + name + "**"
        if details:
            line += " | " + " | ".join(details)
        lines.append(line)
        if pic:
            lines.append("![酒店图片](" + pic + ")")

    lines.append("\n💡 价格实时变动，以实际预订为准")
    lines.append("📋 附加服务：🎫推荐" + city_name + "景点 | 🚄查去" + city_name + "的火车票 | ✈️查去" + city_name + "的机票 | 🚢查去" + city_name + "的邮轮")
    return {"formatted": "\n".join(lines)}


def _format_cruise_list(result):
    if isinstance(result, dict) and result.get("error"):
        return result
    real_data = result.get("data", {}) if isinstance(result, dict) else {}
    rows = real_data.get("rows", []) if isinstance(real_data, dict) else []
    count = real_data.get("count", 0) if isinstance(real_data, dict) else 0
    if not rows:
        return result

    lines = ["为你找到 **" + str(count) + "** 个邮轮产品：\n"]
    for i, r in enumerate(rows[:8], 1):
        name = r.get("productName", "未知")
        price = r.get("price", "")
        tour_day = r.get("tourDay", "")
        brand = r.get("cruiseBrand", "")
        pic = r.get("picUrl", "")

        details = []
        if price: details.append("¥" + str(price) + "起")
        if tour_day: details.append(str(tour_day) + "天")
        if brand: details.append(brand)
        line = "**" + str(i) + ". " + name + "**"
        if details:
            line += " | " + " | ".join(details)
        lines.append(line)
        if pic:
            lines.append("![邮轮图片](" + pic + ")")

    lines.append("\n💡 价格为起价参考，具体以下单为准")
    lines.append("📋 附加服务：🏨推荐目的地酒店 | 🚄查火车票 | ✈️查机票 | 🎫推荐景点门票")
    return {"formatted": "\n".join(lines)}


def _format_hotel_detail(result):
    if isinstance(result, dict) and result.get("error"):
        return result
    if not result or (not result.get("hotelName") and not result.get("hotelId")):
        return result

    name = result.get("hotelName", "未知酒店")
    star = result.get("starName", "")
    city = result.get("cityName", "")
    score = result.get("commentScore", "")
    pic = result.get("firstPic", "")

    lines = ["**" + name + "**"]
    if pic:
        lines.append("![酒店图片](" + pic + ")")
    lines.append("")

    info = []
    if star: info.append("⭐ " + star)
    if score: info.append("评分 " + str(score))
    if city: info.append("📍 " + city)
    if info:
        lines.append(" | ".join(info))
    lines.append("")

    room_types = result.get("roomTypes", [])
    if isinstance(room_types, list) and room_types:
        lines.append("**房型及价格**（共" + str(len(room_types)) + "种房型）\n")
        for i, rt in enumerate(room_types, 1):
            rt_name = rt.get("roomTypeName", "")
            bed = rt.get("bedType", "")
            size = rt.get("roomSize", "")
            floor = rt.get("floor", "")
            rt_pic = ""
            images = rt.get("images", [])
            if isinstance(images, list) and images:
                rt_pic = images[0]

            header = "**" + str(i) + ". " + rt_name + "**"
            details = []
            if bed and bed != "未知床型": details.append(bed)
            if size: details.append(str(size) + "㎡")
            if floor: details.append(floor)
            if details:
                header += " | " + " | ".join(details)
            lines.append(header)
            if rt_pic:
                lines.append("![" + rt_name + "](" + rt_pic + ")")

            rate_plans = rt.get("ratePlans", [])
            if isinstance(rate_plans, list):
                for rp in rate_plans:
                    rp_name = rp.get("ratePlanName", "")
                    price = rp.get("rmbPrices", "")
                    meal = rp.get("mealText", "")
                    cancel = rp.get("cancelText", "")
                    parts = []
                    if price: parts.append("¥" + str(price))
                    if meal: parts.append(meal)
                    if cancel: parts.append("取消：" + str(cancel))
                    if parts:
                        lines.append("   • " + (rp_name + ": " if rp_name else "") + " | ".join(parts))
            lines.append("")

    dest = city or name
    lines.append("📋 附加服务：🎫推荐" + dest + "景点 | 🚄查去" + dest + "的火车票 | ✈️查去" + dest + "的机票")
    return {"formatted": "\n".join(lines)}


def _format_flight_list(result, departure, destination):
    if isinstance(result, dict) and result.get("error"):
        return result
    data = result.get("data", []) if isinstance(result, dict) else []
    if not data:
        return result

    direct = [f for f in data if f.get("type") == "直飞"]
    transfer = [f for f in data if f.get("type") != "直飞"]

    lines = ["**" + departure + " → " + destination + "** 航班信息：\n"]

    if direct:
        lines.append("✈️ **直飞航班**")
        for f in direct[:8]:
            airline = f.get("airlineCompany", "")
            fnum = f.get("flightNumber", "")
            dep_t = f.get("departureTime", "")[11:16] if len(f.get("departureTime", "")) > 11 else f.get("departureTime", "")
            arr_t = f.get("arrivalTime", "")[11:16] if len(f.get("arrivalTime", "")) > 11 else f.get("arrivalTime", "")
            dur = f.get("totalDuration", "")
            price = f.get("basePrice", "")
            price_str = "¥" + str(price) if price else ""
            lines.append("**" + airline + fnum + "** " + dep_t + "→" + arr_t + " | " + dur + (" | " + price_str if price_str else ""))
        lines.append("")

    if transfer:
        lines.append("🔄 **中转航班**")
        for f in transfer[:4]:
            airline = f.get("airlineCompany", "")
            fnum = f.get("flightNumber", "")
            dep_t = f.get("departureTime", "")[11:16] if len(f.get("departureTime", "")) > 11 else f.get("departureTime", "")
            arr_t = f.get("arrivalTime", "")[11:16] if len(f.get("arrivalTime", "")) > 11 else f.get("arrivalTime", "")
            dur = f.get("totalDuration", "")
            price = f.get("basePrice", "")
            price_str = "¥" + str(price) if price else ""
            lines.append("**" + airline + fnum + "** " + dep_t + "→" + arr_t + " | " + dur + (" | " + price_str if price_str else ""))
        lines.append("")

    lines.append("💡 票价实时变动，以实际下单为准")
    lines.append("📋 附加服务：🏨推荐" + destination + "酒店 | 🚄查去" + destination + "的火车票 | 🎫推荐" + destination + "景点 | 🚢查去" + destination + "的邮轮")
    return {"formatted": "\n".join(lines)}


def _format_cabin_detail(result, departure, destination, flight_no):
    if isinstance(result, dict) and result.get("error"):
        return result
    if isinstance(result, dict) and result.get("successCode") is False:
        return result

    cabin_info = result.get("cabinInfo", [])
    if not isinstance(cabin_info, list) or not cabin_info:
        return result

    lines = ["**" + departure + " → " + destination + "** 航班 " + flight_no + " 舱位详情：\n"]
    for i, cabin in enumerate(cabin_info[:15], 1):
        cabin_class = cabin.get("cabinClass", "")
        price = cabin.get("basePrice", "")
        seats = cabin.get("remainingSeats", "")
        baggage = cabin.get("baggageInfo", "")
        meal = cabin.get("mealCode", "")
        refund = cabin.get("refundChangeRule", "")

        parts = ["**" + str(i) + ". " + cabin_class + "**"]
        if price: parts.append("¥" + str(price))
        if seats and str(seats) not in ("0", ""): parts.append("余" + str(seats) + "座")
        lines.append(" | ".join(parts))

        details = []
        if baggage and baggage != "null": details.append("🧳 " + baggage)
        if meal and meal != "null": details.append("🍽️ " + meal)
        if refund and refund != "null": details.append("📋 退改：" + refund)
        if details:
            lines.append("   " + " | ".join(details))
        lines.append("")

    lines.append("💡 票价实时变动，以实际下单为准")
    lines.append("📋 附加服务：🏨推荐" + destination + "酒店 | 🚄查去" + destination + "的火车票")
    return {"formatted": "\n".join(lines)}


def _format_train_list(result, departure, destination):
    if isinstance(result, dict) and result.get("error"):
        return result
    data = result.get("data", []) if isinstance(result, dict) else []
    if not data:
        return result

    lines = ["**" + departure + " → " + destination + "** 火车票信息：\n"]
    for i, t in enumerate(data[:10], 1):
        num = t.get("trainNum", "")
        dep_s = t.get("departStationName", "")
        arr_s = t.get("destStationName", "")
        dep_t = t.get("departTime", "")
        arr_t = t.get("arriveTime", "")
        dur = t.get("duration", "")
        yz = t.get("price", "") or t.get("lowestPrice", "")
        price_str = "¥" + str(yz) if yz else ""
        lines.append("**" + str(i) + ". " + num + "** " + dep_s + dep_t + "→" + arr_s + arr_t + " | " + dur + (" | " + price_str if price_str else ""))

    lines.append("\n💡 时刻和票价为参考数据，具体以购票时为准")
    lines.append("📋 附加服务：🏨推荐" + destination + "酒店 | ✈️查去" + destination + "的机票 | 🎫推荐" + destination + "景点 | 🚢查去" + destination + "的邮轮")
    return {"formatted": "\n".join(lines)}


def _format_train_detail(result, train_num, arr_city):
    if isinstance(result, dict) and result.get("error"):
        return result
    if isinstance(result, dict) and result.get("successCode") is False:
        return result

    data = result.get("data", {}) if isinstance(result, dict) else {}
    if not isinstance(data, dict):
        data = {}
    train_info = data.get("trainInfo", {})
    if not isinstance(train_info, dict) or not train_info:
        return result

    num = train_info.get("trainNum", train_num)
    train_type = train_info.get("trainTypeName", "")
    dep_station = train_info.get("departStationName", "")
    arr_station = train_info.get("destStationName", "")
    dep_time = train_info.get("departTime", "")
    arr_time = train_info.get("arriveTime", "")
    duration = train_info.get("duration", "")
    sale_status = train_info.get("saleStatus", "")

    lines = ["**" + num + "次 " + train_type + "**"]
    lines.append(dep_station + " → " + arr_station)
    lines.append("出发 " + dep_time + " | 到达 " + arr_time + " | 全程 " + duration)
    if sale_status:
        lines.append("状态：" + sale_status)
    lines.append("")

    seat_info = data.get("seatInfo", [])
    if isinstance(seat_info, list) and seat_info:
        lines.append("**座位类型及票价**\n")
        for seat in seat_info:
            seat_name = seat.get("seatName", "")
            price = seat.get("price", "")
            left = seat.get("leftNumber", "")
            status = seat.get("seatStatus", "")
            parts = ["**" + seat_name + "**"]
            if price: parts.append("¥" + str(price))
            if str(left) not in ("0", ""):
                parts.append("余" + str(left) + "张")
            elif status:
                parts.append(status)
            if str(left) == "0" or (not left and not status):
                parts.append("无票")
            lines.append(" | ".join(parts))
        lines.append("")

    dest = arr_city or arr_station
    lines.append("💡 票价实时变动，以实际下单为准")
    lines.append("📋 附加服务：🏨推荐" + dest + "酒店 | ✈️查去" + dest + "的机票 | 🎫推荐" + dest + "景点")
    return {"formatted": "\n".join(lines)}


def _format_ticket_list(result, scenic_name):
    if isinstance(result, dict) and result.get("error"):
        return result
    data = result.get("data", []) if isinstance(result, dict) else []
    if not data:
        return result

    lines = ["**" + scenic_name + "** 门票信息：\n"]
    for i, t in enumerate(data[:10], 1):
        name = t.get("productName", "") or t.get("ticketName", "")
        price = t.get("price", "") or t.get("lowestPrice", "")
        parts = ["**" + str(i) + ". " + name + "**"]
        if price: parts.append("¥" + str(price))
        lines.append(" | ".join(parts))

    lines.append("\n💡 门票价格实时变动，以实际购买为准")
    lines.append("📋 附加服务：🏨推荐目的地酒店 | 🚄查火车票 | ✈️查机票 | 🚢查邮轮产品")
    return {"formatted": "\n".join(lines)}


def _format_holiday_list(result):
    if isinstance(result, dict) and result.get("error"):
        return result
    data = result.get("data", []) if isinstance(result, dict) else []
    if not data:
        return result

    lines = ["**度假产品推荐：**\n"]
    for i, h in enumerate(data[:10], 1):
        name = h.get("productName", "") or h.get("title", "")
        price = h.get("price", "") or h.get("lowestPrice", "")
        tour_day = h.get("tourDay", "")
        parts = ["**" + str(i) + ". " + name + "**"]
        if price: parts.append("¥" + str(price) + "起")
        if tour_day: parts.append(str(tour_day) + "天")
        lines.append(" | ".join(parts))

    lines.append("\n💡 价格为起价参考，具体以下单为准")
    lines.append("📋 附加服务：🏨搜索目的地酒店 | ✈️查询机票 | 🚄查询火车票 | 🎫查询景点门票 | 🚢查询邮轮产品")
    return {"formatted": "\n".join(lines)}


# ==================== 酒店工具 ====================

def tool_tuniu_hotel_search(params):
    """途牛酒店搜索：按城市+日期搜索酒店，支持关键词/商圈/翻页，含酒店图片"""
    if "cityName" not in params and "queryId" not in params:
        return {"error": "首页查询需传cityName，翻页查询需传queryId+pageNum"}
    result = _post("tuniu_hotel_search", params)
    dest = params.get("keyword", "") or params.get("cityName", "")
    return _format_hotel_list(result, dest)


def tool_tuniu_hotel_detail(params):
    """途牛酒店详情：查看房型报价获取下单参数，含酒店及房型图片"""
    if "hotelId" not in params and "hotelName" not in params:
        return {"error": "需传hotelId或hotelName"}
    result = _post("tuniu_hotel_detail", params)
    return _format_hotel_detail(result)


def tool_tuniu_hotel_create_order(params):
    """途牛酒店下单：预订酒店房间"""
    for r in ["hotelId", "roomId", "preBookParam", "checkInDate", "checkOutDate",
              "roomCount", "roomGuests", "contactName", "contactPhone"]:
        if r not in params:
            return {"error": "缺少必填参数: " + r}
    return _post("tuniu_hotel_create_order", params)


# ==================== 机票工具 ====================

def tool_tuniu_flight_search(params):
    """途牛机票搜索：按出发/到达城市+日期搜索航班，支持6种查询模式"""
    for r in ["departureCityName", "arrivalCityName", "departureDate"]:
        if r not in params:
            return {"error": "缺少必填参数: " + r}
    result = _post("tuniu_flight_search", params)
    return _format_flight_list(result, params.get("departureCityName", ""), params.get("arrivalCityName", ""))


def tool_tuniu_flight_cabin_detail(params):
    """途牛机票舱位详情：查看各舱位价格和退改规则，返回cabinPriceId用于下单"""
    for r in ["departureCityName", "arrivalCityName", "departureDate", "flightNo"]:
        if r not in params:
            return {"error": "缺少必填参数: " + r}
    result = _post("tuniu_flight_cabin_detail", params)
    return _format_cabin_detail(result, params.get("departureCityName", ""), params.get("arrivalCityName", ""), params.get("flightNo", ""))


def tool_tuniu_flight_booking_info(params):
    """途牛机票预订信息：获取下单必填字段说明"""
    return _post("tuniu_flight_booking_info", params)


def tool_tuniu_flight_save_order(params):
    """途牛机票下单：预订机票"""
    for r in ["departureCityName", "arrivalCityName", "departureDate", "flightNo", "cabinPriceId", "tourists"]:
        if r not in params:
            return {"error": "缺少必填参数: " + r}
    return _post("tuniu_flight_save_order", params)


def tool_tuniu_flight_cancel_order(params):
    """途牛机票取消订单"""
    if "orderId" not in params:
        return {"error": "缺少orderId"}
    return _post("tuniu_flight_cancel_order", params)


# ==================== 火车票工具 ====================

def tool_tuniu_train_search(params):
    """途牛火车票搜索：按城市日期搜索车次，支持6种排序"""
    if "departureCityName" not in params and "queryId" not in params:
        return {"error": "首页查询需传departureCityName，翻页查询需传queryId"}
    result = _post("tuniu_train_search", params)
    return _format_train_list(result, params.get("departureCityName", ""), params.get("arrivalCityName", ""))


def tool_tuniu_train_detail(params):
    """途牛火车票车次详情：查看余票价格获取预订参数"""
    for r in ["departureStationName", "arrivalStationName", "departureDate", "trainNum"]:
        if r not in params:
            return {"error": "缺少必填参数: " + r}
    result = _post("tuniu_train_detail", params)
    return _format_train_detail(result, params.get("trainNum", ""), params.get("arrivalStationName", ""))


def tool_tuniu_train_book(params):
    """途牛火车票预订：下单预订火车票"""
    for r in ["resources", "adultTourists", "contact"]:
        if r not in params:
            return {"error": "缺少必填参数: " + r}
    return _post("tuniu_train_book", params)


def tool_tuniu_train_order_detail(params):
    """途牛火车票订单详情"""
    if "orderId" not in params:
        return {"error": "缺少orderId"}
    return _post("tuniu_train_order_detail", params)


def tool_tuniu_train_cancel_order(params):
    """途牛火车票取消订单"""
    if "orderId" not in params:
        return {"error": "缺少orderId"}
    return _post("tuniu_train_cancel_order", params)


# ==================== 门票工具 ====================

def tool_tuniu_ticket_query(params):
    """途牛景点门票查询：按景点名搜索门票价格票种"""
    if "scenic_name" not in params:
        return {"error": "缺少scenic_name"}
    result = _post("tuniu_ticket_query", params)
    return _format_ticket_list(result, params.get("scenic_name", ""))


def tool_tuniu_ticket_create_order(params):
    """途牛门票下单：预订景点门票"""
    for r in ["product_id", "resource_id", "depart_date", "adult_num",
              "contact_name", "contact_mobile", "tourist_1_name",
              "tourist_1_mobile", "tourist_1_cert_type", "tourist_1_cert_no"]:
        if r not in params:
            return {"error": "缺少必填参数: " + r}
    return _post("tuniu_ticket_create_order", params)


# ==================== 邮轮工具 ====================

def tool_tuniu_cruise_search(params):
    """途牛邮轮搜索：按日期范围和航线搜索邮轮产品，含邮轮图片"""
    if "departsDateBegin" not in params:
        params["departsDateBegin"] = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    if "departsDateEnd" not in params:
        params["departsDateEnd"] = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    result = _post("tuniu_cruise_search", params)
    return _format_cruise_list(result)


# ==================== 度假工具 ====================

def tool_tuniu_holiday_search(params):
    """途牛度假产品搜索：搜索跟团游、自由行等度假产品"""
    result = _post("tuniu_holiday_search", params)
    return _format_holiday_list(result)


# ==================== 工具路由 ====================

TOOLS = {
    # 酒店
    "tuniu_hotel_search": tool_tuniu_hotel_search,
    "tuniu_hotel_detail": tool_tuniu_hotel_detail,
    "tuniu_hotel_create_order": tool_tuniu_hotel_create_order,
    # 机票
    "tuniu_flight_search": tool_tuniu_flight_search,
    "tuniu_flight_cabin_detail": tool_tuniu_flight_cabin_detail,
    "tuniu_flight_booking_info": tool_tuniu_flight_booking_info,
    "tuniu_flight_save_order": tool_tuniu_flight_save_order,
    "tuniu_flight_cancel_order": tool_tuniu_flight_cancel_order,
    # 火车票
    "tuniu_train_search": tool_tuniu_train_search,
    "tuniu_train_detail": tool_tuniu_train_detail,
    "tuniu_train_book": tool_tuniu_train_book,
    "tuniu_train_order_detail": tool_tuniu_train_order_detail,
    "tuniu_train_cancel_order": tool_tuniu_train_cancel_order,
    # 门票
    "tuniu_ticket_query": tool_tuniu_ticket_query,
    "tuniu_ticket_create_order": tool_tuniu_ticket_create_order,
    # 邮轮
    "tuniu_cruise_search": tool_tuniu_cruise_search,
    # 度假
    "tuniu_holiday_search": tool_tuniu_holiday_search,
}


def main():
    if len(sys.argv) < 3:
        print(json.dumps({"error": "用法: python3 tuniu_travel.py <tool> '<json_params>'", "available_tools": list(TOOLS.keys())}, ensure_ascii=False))
        sys.exit(1)

    tool_name = sys.argv[1]
    try:
        params = json.loads(sys.argv[2])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": "参数JSON解析失败: " + str(e)}, ensure_ascii=False))
        sys.exit(1)

    if tool_name not in TOOLS:
        print(json.dumps({"error": "未知工具: " + tool_name, "available_tools": list(TOOLS.keys())}, ensure_ascii=False))
        sys.exit(1)

    try:
        result = TOOLS[tool_name](params)
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
