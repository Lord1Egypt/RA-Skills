#!/usr/bin/env python3
"""淘宝精选 - 搜索/详情/短链接"""

import sys
import json
import urllib.request

PROXY_URL = "https://1439498936-lofjio3yzf.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = "tp_8k2mX9vQ4z"
TIMEOUT = 60


def call_proxy(rtype, params):
    """调用SCF代理"""
    data = json.dumps({"type": rtype, "params": params}).encode("utf-8")
    req = urllib.request.Request(
        PROXY_URL,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-Proxy-Token": PROXY_TOKEN,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"ok": False, "error": str(e)}


def format_results(data):
    """格式化搜索结果"""
    if not data.get("ok"):
        return f"搜索失败：{data.get('error', '未知错误')}"

    results = data.get("data", [])
    total = data.get("total", 0)

    if not results:
        return "没有找到符合条件的商品，建议换一个关键词试试。"

    lines = [f"共找到 {total} 件好货：\n"]

    for i, item in enumerate(results, 1):
        user_type = item.get("user_type", 0)
        shop_tag = "天猫" if user_type in (1, "1", "天猫") else "淘宝"
        title = item.get("title", "")
        price = item.get("price", "")
        final_price = item.get("final_price", "")
        coupon_info = item.get("coupon_info", "")
        sales = item.get("sales", 0)
        shop_title = item.get("shop_title", "")
        category = item.get("category_name", "")
        commission_rate = item.get("commission_rate", "")
        click_url = item.get("click_url", "")

        if final_price and final_price != price:
            price_str = f"¥{final_price}（原价¥{price}）"
        elif price:
            price_str = f"¥{price}"
        else:
            price_str = "价格未知"

        coupon_str = f" | 🎫{coupon_info}" if coupon_info else ""
        comm_str = f" | 收益{commission_rate}%" if commission_rate else ""
        url_str = f"\n   🔗{click_url}" if click_url else ""

        line = f"{i}. [{shop_tag}] {title}\n   {price_str}{coupon_str}{comm_str} | 销量{sales} | {shop_title} | {category}{url_str}"
        lines.append(line)

    return "\n\n".join(lines)


def format_item_info(data):
    """格式化商品详情"""
    if not data.get("ok"):
        return f"查询失败：{data.get('error', '未知错误')}"

    item = data.get("data", {})
    if not item:
        return "未找到该商品信息"

    user_type = item.get("user_type", 0)
    shop_tag = "天猫" if user_type in (1, "1") else "淘宝"
    title = item.get("title", "")
    brand = item.get("brand_name", "")
    shop = item.get("shop_title", "")
    category = item.get("category_name", "")
    reserve_price = item.get("reserve_price", "")
    zk_price = item.get("zk_final_price", "")
    final_price = item.get("final_price", "")
    coupon_info = item.get("coupon_info", "")
    sales = item.get("sales", 0)
    commission_rate = item.get("commission_rate", "")
    commission_amount = item.get("commission_amount", "")
    provcity = item.get("provcity", "")
    post_fee = item.get("post_fee", "")
    click_url = item.get("click_url", "")

    price_str = f"¥{final_price or zk_price}"
    if reserve_price and str(final_price or zk_price) != str(reserve_price):
        price_str += f"（原价¥{reserve_price}）"

    post_str = "包邮" if post_fee == "0.00" else f"邮费¥{post_fee}"

    lines = [
        f"[{shop_tag}] {title}",
        f"品牌：{brand} | 店铺：{shop} | {provcity}",
        f"价格：{price_str} | {post_str}",
    ]
    if coupon_info:
        lines.append(f"优惠券：{coupon_info}")
    if commission_rate:
        lines.append(f"收益：{commission_amount}元（{commission_rate}%）")
    if click_url:
        lines.append(f"购买链接：{click_url}")

    return "\n".join(lines)


def tool_search_goods(params):
    keyword = params.get("keyword", "")
    if not keyword:
        return json.dumps({"error": "keyword参数必填"}, ensure_ascii=False)

    p = {"keyword": keyword, "page_no": params.get("page", 1), "page_size": params.get("page_size", 20)}
    if params.get("is_tmall") is not None:
        p["is_tmall"] = params["is_tmall"]
    if params.get("has_coupon") is not None:
        p["has_coupon"] = params["has_coupon"]
    if params.get("price_min") is not None:
        p["start_price"] = params["price_min"]
    if params.get("price_max") is not None:
        p["end_price"] = params["price_max"]
    if params.get("sort"):
        p["sort"] = params["sort"]

    data = call_proxy("search", p)
    return json.dumps({"content": format_results(data)}, ensure_ascii=False)


def tool_get_item_info(params):
    item_id = params.get("item_id", "")
    if not item_id:
        return json.dumps({"error": "item_id参数必填"}, ensure_ascii=False)

    data = call_proxy("item_info", {"item_id": item_id})
    return json.dumps({"content": format_item_info(data)}, ensure_ascii=False)


def tool_get_short_url(params):
    url = params.get("url", "")
    if not url:
        return json.dumps({"error": "url参数必填"}, ensure_ascii=False)

    data = call_proxy("short_url", {"urls": [url]})
    if not data.get("ok"):
        return json.dumps({"content": f"生成失败：{data.get('error', '未知错误')}"}, ensure_ascii=False)

    short_urls = data.get("data", [])
    if short_urls and short_urls[0]:
        return json.dumps({"content": f"短链接：{short_urls[0]}"}, ensure_ascii=False)
    return json.dumps({"content": "生成失败：返回为空"}, ensure_ascii=False)


TOOLS = {
    "search_goods": tool_search_goods,
    "get_item_info": tool_get_item_info,
    "get_short_url": tool_get_short_url,
}


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "用法: python3 main.py <tool> '<json_params>'"}, ensure_ascii=False))
        sys.exit(1)

    tool = sys.argv[1]
    try:
        args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"参数JSON解析失败: {e}"}, ensure_ascii=False))
        sys.exit(1)

    if tool not in TOOLS:
        print(json.dumps({"error": f"未知工具: {tool}，可用工具: {', '.join(TOOLS.keys())}"}, ensure_ascii=False))
        sys.exit(1)

    try:
        result = TOOLS[tool](args)
        print(result)
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)
