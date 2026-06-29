# -*- coding: utf-8 -*-
"""
喜来登酒店技能 - ClawHub版
3个工具：search_sheraton_hotels / get_sheraton_hotel_info / search_sheraton_packages
数据源：飞猪MCP via fliggy-proxy SCF代理（万豪集团专区，自动过滤喜来登品牌）
纯标准库实现
"""
import os
import json
import urllib.request
import urllib.error
import sys

# ===== 品牌配置 =====
BRAND_NAME = "喜来登"
BRAND_EN = "Sheraton"

# ===== 代理配置 =====
PROXY_URL = os.environ.get("PROXY_URL", "")
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")


def _request(api_type, params, timeout=30):
    """调用fliggy-proxy统一请求函数"""
    body = json.dumps({"type": api_type, "params": params}, ensure_ascii=False)
    req = urllib.request.Request(
        PROXY_URL,
        data=body.encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-Proxy-Token": PROXY_TOKEN,
        },
        method="POST",
    )
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        data = json.loads(resp.read().decode("utf-8"))
        if data.get("status") == "error":
            return {"success": False, "error": data.get("message", "未知错误")}
        return {"success": True, "data": data.get("data", {})}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")[:200]
        return {"success": False, "error": f"HTTP {e.code}: {err_body}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def search_sheraton_hotels(dest_name, check_in=None, check_out=None,
                           keyword=None, max_price=None, sort=None, limit=10):
    """
    搜索喜来登酒店（万豪集团旗下）
    自动注入品牌关键词"喜来登"，用户只需提供城市即可
    """
    params = {"destName": dest_name}
    if check_in:
        params["checkInDate"] = check_in
    if check_out:
        params["checkOutDate"] = check_out
    # 自动注入品牌名，用户额外关键词追加
    brand_kw = BRAND_NAME
    if keyword:
        brand_kw = f"{BRAND_NAME} {keyword}"
    params["keyWords"] = brand_kw
    if max_price:
        params["maxPrice"] = int(max_price)
    if sort:
        params["sort"] = sort

    result = _request("search_marriott_hotels", params, timeout=30)
    if not result["success"]:
        return f"搜索失败: {result['error']}"

    items = result["data"].get("itemList", [])
    if not items:
        return f"未找到{dest_name}的{BRAND_NAME}酒店，建议调整搜索条件"

    items = items[:limit]

    lines = []
    lines.append(f"🏨 {dest_name}{BRAND_NAME}酒店搜索结果（{len(items)}家）\n")

    for i, item in enumerate(items, 1):
        name = item.get("name", "")
        price = item.get("price", "")
        star = item.get("star", "")
        address = item.get("address", "")
        poi = item.get("nearbyPoi", "")
        deco = item.get("decorationTime", "")
        url = item.get("detailUrl", "")
        shid = item.get("shid", "")

        lines.append(f"{i}. {name}")
        lines.append(f"   💰 {price}  ⭐ {star}")
        if address:
            lines.append(f"   📍 {address}")
        if poi:
            lines.append(f"   🚇 {poi}")
        if deco:
            lines.append(f"   🏗 装修: {deco}")
        if url:
            lines.append(f"   🔗 [点击预订]({url})")
        lines.append(f"   🆔 shid:{shid}")
        lines.append("")

    lines.append(f"💡 输入shid可查询酒店详情（交通/设施/政策/房型），输入关键词可查{BRAND_NAME}套餐")
    return "\n".join(lines)


def get_sheraton_hotel_info(shid=None, hotel_name=None, review_keyword=None):
    """
    查询喜来登酒店详情（交通/景点/设施/政策/房型）
    """
    if not shid and not hotel_name:
        return "请提供shid（从搜索结果获取）或hotel_name"

    params = {}
    if shid:
        params["shid"] = int(shid)
    if hotel_name:
        params["hotelName"] = hotel_name
    if review_keyword:
        params["reviewKeyword"] = review_keyword

    result = _request("get_marriott_hotel_info", params, timeout=20)
    if not result["success"]:
        return f"查询失败: {result['error']}"

    items = result["data"].get("itemList", [])
    if not items:
        return "未找到酒店详情"

    item = items[0]
    hotel_info = item.get("hotelInfo", {})
    url = item.get("detailUrl", "")

    lines = []

    basic = hotel_info.get("酒店基础信息", {})
    name = basic.get("酒店名称", "")
    address = basic.get("酒店地址", "")
    level = basic.get("酒店等级", "")
    rooms_count = basic.get("房间数量", "")
    open_time = basic.get("开业时间", "")
    deco_time = basic.get("装修时间", basic.get("最新装修时间", ""))
    checkin_method = basic.get("入住方式", "")
    pool = basic.get("恒温泳池", "")

    lines.append(f"🏨 {name} 详情\n")
    lines.append(f"📍 地址: {address}")
    lines.append(f"⭐ 等级: {level}")
    if rooms_count:
        lines.append(f"🏠 房间数: {rooms_count}")
    if open_time:
        lines.append(f"📅 开业: {open_time}")
    if deco_time:
        lines.append(f"🏗 装修: {deco_time}")
    if pool:
        lines.append(f"🏊 恒温泳池: {pool}")
    if checkin_method:
        lines.append(f"🔑 入住方式: {checkin_method}")

    policy = hotel_info.get("酒店政策", {})
    if policy:
        lines.append("\n📋 酒店政策")
        checkin_out = policy.get("入离政策", "")
        if checkin_out:
            lines.append(f"  ⏰ {checkin_out}")
        breakfast = policy.get("早餐政策", "")
        if breakfast:
            lines.append(f"  🍳 早餐: {breakfast}")
        deposit = policy.get("押金政策", "")
        if deposit:
            lines.append(f"  💳 押金: {deposit}")
        pet = policy.get("宠物政策", "")
        if pet:
            lines.append(f"  🐾 宠物: {pet}")

    nearby = hotel_info.get("酒店周边", {})
    if nearby:
        lines.append("\n🗺 周边信息")
        for cat, info in nearby.items():
            if info:
                lines.append(f"  【{cat}】")
                spots = info.split(";") if isinstance(info, str) else [info]
                for s in spots[:3]:
                    s = s.strip()
                    if s:
                        lines.append(f"    · {s}")

    facility = hotel_info.get("酒店设施", {})
    if facility:
        lines.append("\n🏢 酒店设施")
        for cat, info in facility.items():
            if info:
                lines.append(f"  【{cat}】{info}")

    room_layers = item.get("roomLayers", [])
    if room_layers:
        lines.append(f"\n🛏 房型（{len(room_layers)}种）")
        for r in room_layers[:6]:
            rname = r.get("name", "")
            hot = r.get("热门设施", "")
            bed = r.get("床政策", "")
            info_str = ""
            if hot:
                info_str += f" {hot}"
            if bed:
                info_str += f" | {bed}"
            lines.append(f"  · {rname}{info_str}")
        if len(room_layers) > 6:
            lines.append(f"  ...还有{len(room_layers) - 6}种房型")

    if url:
        lines.append(f"\n🔗 [点击预订]({url})")

    return "\n".join(lines)


def search_sheraton_packages(keyword=None, hotel_name=None,
                             province_or_city=None, sort=None, limit=10):
    """
    搜索喜来登酒店套餐优惠（含早/连住/门票等打包产品）
    自动注入品牌关键词"喜来登"
    """
    params = {}
    # 自动注入品牌名
    if keyword:
        params["keyword"] = f"{BRAND_NAME} {keyword}"
    elif hotel_name:
        params["hotelName"] = hotel_name
    elif province_or_city:
        params["keyword"] = f"{BRAND_NAME} {province_or_city}"
        params["provinceOrCity"] = province_or_city
    else:
        params["keyword"] = BRAND_NAME
    if province_or_city and "provinceOrCity" not in params:
        params["provinceOrCity"] = province_or_city
    if sort:
        params["sortType"] = sort

    result = _request("search_marriott_packages", params, timeout=30)
    if not result["success"]:
        return f"搜索失败: {result['error']}"

    items = result["data"].get("itemList", [])
    if not items:
        return f"未找到{BRAND_NAME}套餐"

    items = items[:limit]

    lines = []
    search_kw = keyword or hotel_name or province_or_city or BRAND_NAME
    lines.append(f"🎁 {search_kw}{BRAND_NAME}套餐搜索结果（{len(items)}个）\n")

    for i, item in enumerate(items, 1):
        title = item.get("title", "")
        price = item.get("price", "")
        sell = item.get("sellPoint", "")
        benefit = item.get("benefit", "")
        url = item.get("detailUrl", "")

        lines.append(f"{i}. {title}")
        lines.append(f"   💰 {price}")
        if sell:
            sell = sell.replace("。，", "；").replace(",,", "，")
            lines.append(f"   ✨ {sell[:150]}")
        if benefit:
            lines.append(f"   🏷 {benefit}")
        if url:
            lines.append(f"   🔗 [点击预订]({url})")
        lines.append("")

    lines.append("💡 套餐通常比单订更优惠，含早餐/门票/连住折扣等")
    return "\n".join(lines)


# ===== 命令行入口 =====
def main():
    if len(sys.argv) < 3:
        print("用法: python sheraton_hotel.py <tool> <args_json>")
        print("  tool: search | detail | packages")
        print('  示例: python sheraton_hotel.py search \'{"dest_name":"上海"}\'')
        return

    tool = sys.argv[1]
    try:
        args = json.loads(sys.argv[2])
    except json.JSONDecodeError:
        print(f"参数JSON解析失败: {sys.argv[2]}")
        return

    if tool == "search":
        print(search_sheraton_hotels(**args))
    elif tool == "detail":
        print(get_sheraton_hotel_info(**args))
    elif tool == "packages":
        print(search_sheraton_packages(**args))
    else:
        print(f"未知工具: {tool}，可选: search / detail / packages")


if __name__ == "__main__":
    main()
