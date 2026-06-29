#!/usr/bin/env python3
"""淘宝天天特卖 - 商品查询

配合独立SCF函数 taobao-tiantian-proxy 使用。
SCF负责：缓存全量数据(5min TTL) + 硬筛选(天猫店+有品牌) + 排序 + 分页 + 短链生成
脚本负责：发送参数、接收结果、格式化输出、构建用户提示语

3个工具：
  list_items  — 分页浏览天天特卖商品，支持4种排序
  get_detail  — 获取单条商品详情
  get_stats   — 频道统计与类目分布
"""

import sys
import json
import urllib.request
import urllib.error

# ===== 配置 =====
PROXY_URL = "https://1439498936-49sz8cryfx.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = "tp_8k2mX9vQ4z"

TIMEOUT = 30
PAGE_SIZE = 40
SORT_LABELS = {
    "sales_desc": "销量优先",
    "price_asc": "价格从低到高",
    "price_desc": "价格从高到低",
    "commission_desc": "推荐热度优先",
}


def _scf_call(tool, params):
    """调用SCF代理"""
    payload = json.dumps({"tool": tool, "params": params}).encode("utf-8")
    req = urllib.request.Request(
        PROXY_URL, data=payload,
        headers={"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}


def _format_item(item):
    """格式化单条商品"""
    return {
        "title": item.get("title", ""),
        "brand": item.get("brand_name", ""),
        "shop": item.get("shop_title", ""),
        "category": item.get("category_name", ""),
        "price": item.get("final_price", ""),
        "original_price": item.get("original_price", ""),
        "coupon": item.get("coupon_info", ""),
        "promo": item.get("promo_tags", ""),
        "annual_sales": item.get("annual_vol", ""),
        "image": item.get("pict_url", ""),
        "buy_url": item.get("click_url", ""),
        "coupon_url": item.get("coupon_url", ""),
    }


def tool_list_items(params):
    """获取天天特卖商品列表（分页+排序）"""
    page = int(params.get("page", 1) or 1)
    if page < 1:
        page = 1
    sort = params.get("sort", "sales_desc") or "sales_desc"

    data = _scf_call("list", {"page": page, "sort": sort})

    if "error" in data:
        return json.dumps({
            "content": "",
            "summary": f"查询失败：{data['error']}，请稍后重试。"
        }, ensure_ascii=False)

    results = data.get("results", [])
    total = data.get("total", 0)
    total_pages = data.get("total_pages", 0)
    page_size = data.get("page_size", PAGE_SIZE)
    from_cache = data.get("from_cache", False)
    current_sort = data.get("sort", sort)

    if not results:
        return json.dumps({
            "content": "",
            "summary": "暂无天天特卖好货，请稍后再试。"
        }, ensure_ascii=False)

    # 格式化商品列表
    items = [_format_item(item) for item in results]

    # 构建提示语
    page_start = (page - 1) * page_size + 1
    page_end = min(page * page_size, total)
    has_more = page_end < total
    sort_label = SORT_LABELS.get(current_sort, "销量优先")

    hints = []
    hints.append(f"天天特卖好货共{total}条，100%天猫品牌店精选，当前按「{sort_label}」排列。")
    if has_more:
        hints.append(f'第{page}/{total_pages}页，显示第{page_start}-{page_end}条，还有{total - page_end}条。说"下一页"查看更多。')
    else:
        hints.append(f"第{page}/{total_pages}页，显示第{page_start}-{page_end}条，已到最后一页。")

    return json.dumps({
        "content": json.dumps(items, ensure_ascii=False, indent=2),
        "summary": " ".join(hints)
    }, ensure_ascii=False)


def tool_get_detail(params):
    """获取单条商品详情"""
    item_id = params.get("item_id", "")

    if not item_id:
        return json.dumps({
            "content": "",
            "summary": "请提供商品ID（item_id）。"
        }, ensure_ascii=False)

    data = _scf_call("detail", {"item_id": item_id})

    if "error" in data:
        return json.dumps({
            "content": "",
            "summary": f"查询失败：{data['error']}，该商品可能已下架。"
        }, ensure_ascii=False)

    item = _format_item(data)

    # 构建详情提示语
    hints = []
    title = item.get("title", "商品")
    brand = item.get("brand", "")
    price = item.get("price", "")
    original = item.get("original_price", "")
    coupon = item.get("coupon", "")
    buy_url = item.get("buy_url", "")

    hints.append(f"「{title}」")
    if brand:
        hints.append(f"品牌：{brand}")
    if price:
        if original and original != price:
            hints.append(f"到手价¥{price}（原价¥{original}）")
        else:
            hints.append(f"价格¥{price}")
    if coupon:
        hints.append(f"优惠：{coupon}")
    if buy_url:
        hints.append(f"购买链接：{buy_url}")
    coupon_url = item.get("coupon_url", "")
    if coupon_url:
        hints.append(f"领券链接：{coupon_url}")

    return json.dumps({
        "content": json.dumps(item, ensure_ascii=False, indent=2),
        "summary": " ".join(hints)
    }, ensure_ascii=False)


def tool_get_stats(params):
    """获取频道统计信息"""
    data = _scf_call("stats", {})

    if "error" in data:
        return json.dumps({
            "content": "",
            "summary": f"查询失败：{data['error']}，请稍后重试。"
        }, ensure_ascii=False)

    total = data.get("total_items", 0)
    from_cache = data.get("from_cache", False)
    cache_age = data.get("cache_age", 0)
    cache_ttl = data.get("cache_ttl", 300)
    categories = data.get("top_categories", [])

    hints = []
    hints.append(f"天天特卖频道当前共{total}条精选好货（100%天猫品牌店）。")
    if from_cache:
        hints.append(f"数据缓存{cache_age}秒前刷新（{cache_ttl}秒TTL），商品按场次轮换保持新鲜。")
    else:
        hints.append("数据刚从官方API实时拉取。")

    if categories:
        cat_parts = [f"{c['name']}({c['count']}条)" for c in categories[:5]]
        hints.append('热门类目：' + '、'.join(cat_parts) + '…说"看洗护"或"看零食"可按品类浏览。')

    return json.dumps({
        "content": json.dumps(data, ensure_ascii=False, indent=2),
        "summary": " ".join(hints)
    }, ensure_ascii=False)


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
