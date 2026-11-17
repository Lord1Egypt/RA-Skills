#!/usr/bin/env python3
"""淘宝精选比价 - 2项能力，标品比价+非标品看销量"""

import os
import sys
import json
import urllib.request
import urllib.error

# FC代理地址（密钥在代理侧，代码里不放Key）
PROXY_URL = os.environ.get("PROXY_URL", "https://taobao-on-proxy-biaggfugvr.cn-hangzhou.fcapp.run")
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "tp_8k2mX9vQ4z")
TIMEOUT = 30


def _call_proxy(tool, arguments):
    """调用FC代理"""
    body = json.dumps({"tool": tool, "arguments": arguments}, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(
        PROXY_URL, data=body,
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


def format_results(data):
    """格式化搜索结果为可读文本"""
    if "error" in data:
        return "搜索失败：{}".format(data["error"])

    results = data.get("results", [])
    total = data.get("total", 0)
    page = data.get("page", 1)

    if not results:
        return "没有找到符合条件的商品，建议换一个关键词试试。"

    lines = ["共找到 {} 件好货（第{}页）：\n".format(total, page)]

    for i, item in enumerate(results, 1):
        shop_type = item.get("user_type", "")
        title = item.get("title", "")
        price = item.get("price", "")
        final_price = item.get("final_price", "")
        coupon = item.get("coupon_info", "")
        sales = item.get("sales", "")
        shop = item.get("shop_title", "")
        category = item.get("category_name", "")
        click_url = item.get("click_url", "")

        if final_price and final_price != price:
            price_str = "¥{}（原价¥{}）".format(final_price, price)
        else:
            price_str = "¥{}".format(price)

        coupon_str = " | 券{}".format(coupon) if coupon else ""
        sales_str = " | 已售{}".format(sales) if sales else ""

        line = "{}. [{}] {}\n   {}{}{} | {} | {}\n   链接:{}".format(
            i, shop_type, title, price_str, coupon_str, sales_str, shop, category, click_url)
        lines.append(line)

    lines.append("\n> 数据来源：淘宝联盟·精选好货，自动筛选包邮+消保+高评分商品")
    return "\n\n".join(lines)


# ==================== 工具函数 ====================

def tool_search_standard(params):
    """标品搜索 - 3C数码家电等品牌型号明确的商品，按到手价排序"""
    arguments = {"keyword": params["keyword"], "page": params.get("page", 1)}
    is_tmall = params.get("is_tmall", True)
    arguments["is_tmall"] = is_tmall
    if params.get("price_min") is not None:
        arguments["price_min"] = params["price_min"]
    if params.get("price_max") is not None:
        arguments["price_max"] = params["price_max"]

    data = _call_proxy("search_standard", arguments)
    return format_results(data)


def tool_search_lifestyle(params):
    """非标品搜索 - 服饰美妆家居等看销量和口碑的商品，按销量排序"""
    arguments = {"keyword": params["keyword"], "page": params.get("page", 1)}
    if params.get("is_tmall") is not None:
        arguments["is_tmall"] = params["is_tmall"]
    if params.get("price_min") is not None:
        arguments["price_min"] = params["price_min"]
    if params.get("price_max") is not None:
        arguments["price_max"] = params["price_max"]

    data = _call_proxy("search_lifestyle", arguments)
    return format_results(data)


# ==================== 工具路由 ====================

TOOLS = {
    "search_standard": tool_search_standard,
    "search_lifestyle": tool_search_lifestyle,
}


def main():
    if len(sys.argv) < 3:
        print(json.dumps({"error": "用法: python3 main.py <tool> '<json_params>'"}, ensure_ascii=False))
        sys.exit(1)

    tool_name = sys.argv[1]
    try:
        params = json.loads(sys.argv[2])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": "参数JSON解析失败: " + str(e)}, ensure_ascii=False))
        sys.exit(1)

    if tool_name not in TOOLS:
        print(json.dumps({"error": "未知工具: {}，可用工具: {}".format(tool_name, ", ".join(TOOLS.keys()))}, ensure_ascii=False))
        sys.exit(1)

    try:
        result = TOOLS[tool_name](params)
        print(json.dumps({"content": result}, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
