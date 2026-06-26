#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = ["aiohttp", "argparse"]
# ///
"""
ShopMind 全网比价工具 v2.1.0
支持：淘宝/天猫、京东、拼多多、抖音、快手、苏宁、唯品会、考拉、1688
"""

import os
import io
import csv
import json
import asyncio
import aiohttp
import argparse

INVITE_CODE = os.getenv("MAISHOU_INVITE_CODE") or "6110440"
OPENID = "564bdce0fa408fc9e1d5d42fd022ef0b"
API_BASE = "https://appapi.maishou88.com"
SHARE_API = "https://msapi.maishou88.com"

HEADERS = {
    "Accept": "application/json",
    "Referer": "https://hnbc018.kuaizhan.com/",
    "User-Agent": "Mozilla/5.0 AppleWebKit/537 Chrome/143 Safari/537",
}

PLATFORM_MAP = {
    "0": "全部", "1": "淘宝/天猫", "2": "京东", "3": "拼多多",
    "4": "苏宁", "5": "唯品会", "6": "考拉",
    "7": "抖音", "8": "快手", "10": "1688"
}

SESSION = None


def calc_savings(item):
    """计算省钱信息"""
    price = float(item.get("actualPrice") or 0)
    original = float(item.get("originalPrice") or price)
    coupon = float(item.get("couponPrice") or 0)
    final = max(price - coupon, 0) if coupon > 0 else price
    saved = original - final
    discount = round((final / original) * 10, 1) if original > 0 else 10
    return {
        "finalPrice": round(final, 2),
        "saved": round(saved, 2),
        "discount": f"{discount}折" if discount < 10 else "无折扣",
        "hasCoupon": coupon > 0,
        "couponAmount": coupon,
    }


async def search(keyword, source="0", page=1, sort="price", coupon="0",
                 min_price=0, max_price=999999, func=None, **kwargs):
    """搜索比价"""
    resp = await SESSION.post(
        f"{API_BASE}/api/v1/homepage/searchList",
        headers={
            **HEADERS,
            "User-Agent": "MaiShouApp/3.7.7 (iPhone; iOS 26.3; Scale/3.00)",
            "openid": OPENID,
            "version": "3.7.7.2",
        },
        data={
            "isCoupon": 1 if coupon == "1" else 0,
            "keyword": str(keyword),
            "openid": OPENID,
            "order": "desc",
            "page": int(page),
            "pddListId": "",
            "sort": "",
            "sourceType": str(source),
            "user_id": "",
        },
    )
    data = await resp.json(encoding="utf-8-sig") or {}
    rows = data.get("data") or []
    if not rows:
        return json.dumps({"success": True, "total": 0, "message": data.get("message") or "未找到相关商品"}, ensure_ascii=False)

    # 丰富数据
    items = []
    for v in rows:
        savings = calc_savings(v)
        items.append({
            "goodsId": v.get("goodsId"),
            "source": v.get("sourceType"),
            "sourceName": PLATFORM_MAP.get(str(v.get("sourceType")), "未知"),
            "title": v.get("title"),
            "shopName": v.get("shopName") or "",
            "originalPrice": float(v.get("originalPrice") or 0),
            "price": float(v.get("actualPrice") or 0),
            "finalPrice": savings["finalPrice"],
            "couponAmount": savings["couponAmount"],
            "saved": savings["saved"],
            "discount": savings["discount"],
            "hasCoupon": savings["hasCoupon"],
            "commission": v.get("commission") or "0",
            "monthSales": v.get("monthSales") or 0,
            "imageUrl": v.get("picUrl") or "",
        })

    # 价格过滤
    min_p = float(min_price)
    max_p = float(max_price)
    items = [i for i in items if min_p <= i["finalPrice"] <= max_p]

    # 排序
    if sort == "price":
        items.sort(key=lambda x: x["finalPrice"])
    elif sort == "price_desc":
        items.sort(key=lambda x: x["finalPrice"], reverse=True)
    elif sort == "sales":
        def parse_sales(s):
            s = str(s).replace("+", "").replace("万", "0000")
            try: return float(s)
            except: return 0
        items.sort(key=lambda x: parse_sales(x["monthSales"]), reverse=True)
    elif sort == "discount":
        items.sort(key=lambda x: x["saved"], reverse=True)
    elif sort == "commission":
        items.sort(key=lambda x: float(x["commission"]), reverse=True)

    # 添加排名
    for idx, item in enumerate(items):
        item["rank"] = idx + 1

    # 统计
    prices = [i["finalPrice"] for i in items if i["finalPrice"] > 0]
    stats = {
        "count": len(items),
        "lowestPrice": min(prices) if prices else 0,
        "highestPrice": max(prices) if prices else 0,
        "avgPrice": round(sum(prices) / len(prices), 2) if prices else 0,
        "couponCount": sum(1 for i in items if i["hasCoupon"]),
        "maxSaved": max((i["saved"] for i in items), default=0),
    }

    # 输出格式化文本
    lines = []
    lines.append(f"🛒 比价结果：{keyword}")
    lines.append(f"📊 {stats['count']}个商品 | 最低¥{stats['lowestPrice']} | 平均¥{stats['avgPrice']} | {stats['couponCount']}个有券")
    lines.append("")
    for item in items[:20]:
        tag = "✅" if item["rank"] == 1 else "  "
        coupon_tag = f" 🎫券{item['couponAmount']}元" if item["hasCoupon"] else ""
        save_tag = f" 省¥{item['saved']}" if item["saved"] > 0 else ""
        lowest = " (最低价)" if item["rank"] == 1 else ""
        lines.append(f"{tag} {item['rank']}. [{item['sourceName']}] ¥{item['finalPrice']}{lowest}{coupon_tag}{save_tag} {item['discount']}")
        lines.append(f"     {item['title'][:50]}")
        if item["shopName"]:
            lines.append(f"     🏪 {item['shopName']} | 月销 {item['monthSales']}")
        else:
            lines.append(f"     📈 月销 {item['monthSales']}")
        lines.append(f"     🆔 goodsId={item['goodsId']} source={item['source']}")
        lines.append("")

    return "\n".join(lines)


async def detail(id, source="1", func=None, **kwargs):
    """商品详情 + 购买链接"""
    params = {
        "goodsId": str(id),
        "sourceType": str(source),
        "inviteCode": INVITE_CODE,
        "supplierCode": "",
        "activityId": "",
        "isShare": "1",
        "token": "",
    }

    # 并发请求详情和链接
    detail_resp, link_resp = await asyncio.gather(
        SESSION.post(f"{API_BASE}/api/v3/goods/detail", json={**params, "keyword": "", "usageScene": 5}),
        SESSION.post(f"{SHARE_API}/api/v1/share/getTargetUrl", json={**params, "isDirectDetail": 0}),
    )

    detail_data = (await detail_resp.json(encoding="utf-8-sig") or {}).get("data") or {}
    link_data = (await link_resp.json(encoding="utf-8-sig") or {}).get("data") or {}

    if not detail_data.get("title") and not link_data.get("appUrl"):
        return "❌ 未找到商品详情"

    savings = calc_savings(detail_data)
    buy_url = link_data.get("appUrl") or link_data.get("schemaUrl") or ""
    copy_cmd = link_data.get("kl") or ""

    lines = []
    lines.append(f"📦 {detail_data.get('title', '未知商品')}")
    lines.append("")
    lines.append(f"💰 价格：¥{savings['finalPrice']}（原价 ¥{float(detail_data.get('originalPrice') or 0)}）")
    if savings["hasCoupon"]:
        lines.append(f"🎫 优惠券：{savings['couponAmount']}元  {savings['discount']}")
    if savings["saved"] > 0:
        lines.append(f"💵 省钱：¥{savings['saved']}")
    lines.append(f"📈 月销：{detail_data.get('monthSales', 0)}")
    lines.append(f"🏪 平台：{PLATFORM_MAP.get(str(source), '未知')}")
    if detail_data.get("shopName"):
        lines.append(f"🏬 店铺：{detail_data['shopName']}")
    lines.append("")
    if buy_url:
        lines.append(f"🔗 购买链接：{buy_url}")
    if copy_cmd:
        lines.append(f"📋 复制口令：{copy_cmd}")

    return "\n".join(lines)


async def coupons(keyword="", source="0", page=1, func=None, **kwargs):
    """优惠券精选"""
    resp = await SESSION.post(
        f"{API_BASE}/api/v1/homepage/searchList",
        headers={
            **HEADERS,
            "User-Agent": "MaiShouApp/3.7.7 (iPhone; iOS 26.3; Scale/3.00)",
            "openid": OPENID,
            "version": "3.7.7.2",
        },
        data={
            "isCoupon": 1,
            "keyword": str(keyword),
            "openid": OPENID,
            "order": "desc",
            "page": int(page),
            "pddListId": "",
            "sort": "",
            "sourceType": str(source),
            "user_id": "",
        },
    )
    data = await resp.json(encoding="utf-8-sig") or {}
    rows = data.get("data") or []

    items = []
    for v in rows:
        savings = calc_savings(v)
        if savings["hasCoupon"]:
            items.append({**v, **savings})

    items.sort(key=lambda x: x["couponAmount"], reverse=True)

    lines = []
    lines.append(f"🎫 优惠券精选：{keyword or '全部'}")
    lines.append(f"📊 {len(items)}个有券商品")
    lines.append("")
    for idx, item in enumerate(items[:20]):
        lines.append(f"  {idx+1}. [{PLATFORM_MAP.get(str(item.get('sourceType')), '未知')}] 券{item['couponAmount']}元 → 券后¥{item['finalPrice']} 省¥{item['saved']}")
        lines.append(f"     {(item.get('title') or '')[:50]}")
        lines.append(f"     🆔 goodsId={item.get('goodsId')} source={item.get('sourceType')}")
        lines.append("")

    return "\n".join(lines)


async def hot(source="0", page=1, func=None, **kwargs):
    """热门爆品"""
    resp = await SESSION.post(
        f"{API_BASE}/api/v1/homepage/searchList",
        headers={
            **HEADERS,
            "User-Agent": "MaiShouApp/3.7.7 (iPhone; iOS 26.3; Scale/3.00)",
            "openid": OPENID,
            "version": "3.7.7.2",
        },
        data={
            "isCoupon": 0,
            "keyword": "",
            "openid": OPENID,
            "order": "desc",
            "page": int(page),
            "pddListId": "",
            "sort": "total_sales",
            "sourceType": str(source),
            "user_id": "",
        },
    )
    data = await resp.json(encoding="utf-8-sig") or {}
    rows = data.get("data") or []

    items = []
    for v in rows:
        savings = calc_savings(v)
        items.append({**v, **savings})

    lines = []
    lines.append(f"🔥 热门爆品：{PLATFORM_MAP.get(str(source), '全部')}")
    lines.append(f"📊 {len(items)}个商品")
    lines.append("")
    for idx, item in enumerate(items[:20]):
        coupon_tag = f" 🎫券{item['couponAmount']}元" if item["hasCoupon"] else ""
        lines.append(f"  {idx+1}. [{PLATFORM_MAP.get(str(item.get('sourceType')), '未知')}] ¥{item['finalPrice']}{coupon_tag} {item['discount']}")
        lines.append(f"     {(item.get('title') or '')[:50]}")
        lines.append(f"     📈 月销 {item.get('monthSales', 0)}")
        lines.append("")

    return "\n".join(lines)


async def main():
    global SESSION
    async with aiohttp.ClientSession(headers=HEADERS) as SESSION:
        parser = argparse.ArgumentParser(description="ShopMind 全网比价工具 v2.1.0")
        subs = parser.add_subparsers()

        # search
        p = subs.add_parser("search", help="搜索比价")
        p.add_argument("--keyword", required=True, help="搜索关键词")
        p.add_argument("--source", default="0", help="平台: 0全部 1淘宝 2京东 3拼多多 4苏宁 5唯品会 6考拉 7抖音 8快手 10:1688")
        p.add_argument("--page", type=int, default=1, help="页码")
        p.add_argument("--sort", default="price", help="排序: price|price_desc|sales|discount|commission")
        p.add_argument("--coupon", default="0", help="只看有券: 1=是 0=否")
        p.add_argument("--min_price", type=float, default=0, help="最低价格")
        p.add_argument("--max_price", type=float, default=999999, help="最高价格")
        p.set_defaults(func=search)

        # detail
        p = subs.add_parser("detail", help="商品详情+购买链接")
        p.add_argument("--id", required=True, help="商品ID（从搜索结果获取）")
        p.add_argument("--source", default="1", help="平台编号")
        p.set_defaults(func=detail)

        # coupons
        p = subs.add_parser("coupons", help="优惠券精选")
        p.add_argument("--keyword", default="", help="搜索关键词（可选）")
        p.add_argument("--source", default="0", help="平台编号")
        p.add_argument("--page", type=int, default=1, help="页码")
        p.set_defaults(func=coupons)

        # hot
        p = subs.add_parser("hot", help="热门爆品")
        p.add_argument("--source", default="0", help="平台编号")
        p.add_argument("--page", type=int, default=1, help="页码")
        p.set_defaults(func=hot)

        args = parser.parse_args()
        if hasattr(args, "func"):
            print(await args.func(**vars(args)))
        else:
            parser.print_help()


if __name__ == "__main__":
    asyncio.run(main())
