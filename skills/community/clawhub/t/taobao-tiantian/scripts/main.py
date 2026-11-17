#!/usr/bin/env python3
"""淘宝天天特卖 - list_items/get_detail/get_stats"""

import os
import sys
import json
import urllib.request
import urllib.error

PROXY_URL = os.environ.get("PROXY_URL", "https://1439498936-49sz8cryfx.ap-guangzhou.tencentscf.com")
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "tp_8k2mX9vQ4z")
TIMEOUT = 30


def _call_proxy(tool_name, params):
    """调用SCF代理 - type+params格式"""
    body = json.dumps({"type": tool_name, "params": params}).encode("utf-8")
    req = urllib.request.Request(
        PROXY_URL, data=body, method="POST",
        headers={"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN},
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = ""
        try:
            err = e.read().decode("utf-8", errors="replace")[:300]
        except Exception:
            pass
        return {"ok": False, "error": "proxy error {}: {}".format(e.code, err)}
    except Exception as e:
        return {"ok": False, "error": "request error: {}".format(e)}


def _format_items(data):
    """格式化商品列表"""
    if not data.get("ok"):
        return "查询失败：" + data.get("error", "未知错误")
    items = data.get("data", [])
    if not items:
        return "暂无商品，请稍后再试"
    total = data.get("total", len(items))
    lines = ["共 {} 件特卖好货：\n".format(total)]
    for i, item in enumerate(items, 1):
        title = item.get("title", "")
        price = item.get("price", "")
        final_price = item.get("final_price", "")
        coupon = item.get("coupon_info", "")
        sales = item.get("sales", "")
        shop = item.get("shop_title", "")
        click_url = item.get("click_url", "")
        item_id = item.get("item_id", "")

        if final_price and final_price != price:
            price_str = "到手价¥{}（原价¥{}）".format(final_price, price)
        else:
            price_str = "¥{}".format(price)
        coupon_str = " | 券{}".format(coupon) if coupon else ""
        sales_str = " | 已售{}".format(sales) if sales else ""
        shop_str = " | {}".format(shop) if shop else ""

        line = "{}. {}{}{}\n   {}{}\n   item_id: {}".format(
            i, title, coupon_str, sales_str, price_str, shop_str, item_id)
        if click_url:
            line += "\n   链接: {}".format(click_url)
        lines.append(line)
    lines.append("\n> 数据来源：淘宝天天特卖频道")
    return "\n\n".join(lines)


def _format_detail(data):
    """格式化商品详情"""
    if not data.get("ok"):
        return "查询失败：" + data.get("error", "未知错误")
    item = data.get("data", {})
    if not item:
        return "未找到该商品信息"

    title = item.get("title", "")
    price = item.get("price", "")
    final_price = item.get("final_price", "")
    coupon = item.get("coupon_info", "")
    sales = item.get("sales", "")
    shop = item.get("shop_title", "")
    category = item.get("category_name", "")
    click_url = item.get("click_url", "")
    item_id = item.get("item_id", "")
    image = item.get("pict_url", "")

    lines = [title]
    lines.append("商品ID：{} | 店铺：{} | 分类：{}".format(item_id, shop, category))
    if final_price and final_price != price:
        lines.append("到手价：¥{}（原价¥{}）".format(final_price, price))
        if coupon:
            lines.append("优惠券：{}".format(coupon))
    else:
        lines.append("价格：¥{}".format(price))
    if sales:
        lines.append("销量：{}".format(sales))
    if image:
        lines.append("主图：{}".format(image))
    if click_url:
        lines.append("链接：{}".format(click_url))
    return "\n".join(lines)


def _format_stats(data):
    """格式化频道统计"""
    if not data.get("ok"):
        return "查询失败：" + data.get("error", "未知错误")
    stats = data.get("data", {})
    if not stats:
        return "暂无统计数据"
    lines = ["淘宝天天特卖频道统计："]
    for k, v in stats.items():
        lines.append("  {}: {}".format(k, v))
    return "\n".join(lines)


def tool_list_items(params):
    page = params.get("page", 1)
    sort = params.get("sort", 0)
    data = _call_proxy("list_items", {"page": page, "sort": sort})
    return json.dumps({"content": _format_items(data)}, ensure_ascii=False)


def tool_get_detail(params):
    item_id = params.get("item_id", "")
    if not item_id:
        return json.dumps({"error": "item_id参数必填"}, ensure_ascii=False)
    data = _call_proxy("get_detail", {"item_id": item_id})
    return json.dumps({"content": _format_detail(data)}, ensure_ascii=False)


def tool_get_stats(params):
    data = _call_proxy("get_stats", {})
    return json.dumps({"content": _format_stats(data)}, ensure_ascii=False)


TOOLS = {
    "list_items": tool_list_items,
    "get_detail": tool_get_detail,
    "get_stats": tool_get_stats,
}


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "用法: python3 main.py <tool> '<json_params>'"}, ensure_ascii=False))
        sys.exit(1)

    tool = sys.argv[1]
    try:
        args = json.loads(sys.argv[2])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": "参数JSON解析失败: {}".format(e)}, ensure_ascii=False))
        sys.exit(1)

    if tool not in TOOLS:
        print(json.dumps({"error": "未知工具: {}，可用工具: {}".format(tool, ", ".join(TOOLS.keys()))}, ensure_ascii=False))
        sys.exit(1)

    try:
        result = TOOLS[tool](args)
        print(result)
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)
