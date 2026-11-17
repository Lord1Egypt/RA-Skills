#!/usr/bin/env python3
"""
xiaxiayouhui-deals 跨平台比价接口封装（标准库实现，零第三方依赖）
免费、免 key，覆盖拼多多/京东/淘宝/苏宁/唯品会/抖音
服务地址: https://xiaxiayouhui.xyz
"""

import argparse
import json
import ssl
import sys
import urllib.parse
import urllib.request
from typing import Any

BASE_URL = "https://xiaxiayouhui.xyz"
TIMEOUT = 20

PLATFORM_NAMES = {
    "pdd": "拼多多",
    "jd": "京东",
    "tb": "淘宝",
    "sn": "苏宁",
    "vip": "唯品会",
    "dy": "抖音",
}

# 中文平台名 -> 平台 code
PLATFORM_CODES = {v: k for k, v in PLATFORM_NAMES.items()}


def _ssl_ctx() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def _get(path: str, params: dict[str, Any]) -> dict[str, Any]:
    """标准库 GET，返回 JSON"""
    query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    url = f"{BASE_URL}{path}" + (f"?{query}" if query else "")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=_ssl_ctx()) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        return {"success": False, "error": type(exc).__name__, "message": str(exc)}


def search_compare(keyword: str, limit: int = 10, platform: str | None = None) -> dict[str, Any]:
    """跨平台比价。platform 可传中文名或平台 code"""
    params: dict[str, Any] = {"q": keyword, "limit": str(limit)}
    if platform:
        params["platforms"] = PLATFORM_CODES.get(platform, platform)
    return _get("/api/skill/v1/compare", params)


def daily_deals(limit: int = 10) -> dict[str, Any]:
    return _get("/api/skill/v1/daily-deals", {"limit": str(limit)})


def parse_link(url: str) -> dict[str, Any]:
    return _get("/api/skill/v1/parse-link", {"url": url})


def local_coupons(radius: int = 5000, lat: float | None = None, lng: float | None = None) -> dict[str, Any]:
    params: dict[str, Any] = {"radius": str(radius)}
    if lat is not None:
        params["lat"] = str(lat)
    if lng is not None:
        params["lng"] = str(lng)
    return _get("/api/skill/v1/local", params)


def _fmt(v: Any) -> str:
    if v in (None, "", 0):
        return "-"
    return str(v)


def _to_float(v: Any) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return 9e9


def format_compare(data: dict[str, Any]) -> str:
    """把 compare 返回格式化为 Markdown 表格（按到手价升序）"""
    if not data.get("success"):
        return f"查询失败: {data.get('message') or data.get('error') or '未知错误'}"

    rows: list[dict[str, Any]] = []
    for code, block in (data.get("platforms") or {}).items():
        if not isinstance(block, dict) or not block.get("success"):
            continue
        for item in block.get("data") or []:
            rows.append({
                "platform": PLATFORM_NAMES.get(code, code),
                "name": item.get("goods_name", ""),
                "original": item.get("original_price"),
                "price": item.get("min_price"),
                "coupon_price": item.get("coupon_price"),
                "coupon_desc": item.get("coupon_desc", ""),
                "mall": item.get("mall_name", ""),
            })

    if not rows:
        return "未找到相关商品（部分平台可能暂无数据）"

    rows.sort(key=lambda r: _to_float(r["coupon_price"] or r["price"]))

    lines: list[str] = []
    cheapest = data.get("cheapest") or {}
    if cheapest:
        cplat = PLATFORM_NAMES.get(cheapest.get("platform", ""), cheapest.get("platform", ""))
        cprice = cheapest.get("coupon_price") or cheapest.get("min_price")
        lines.append(f"最低价: [{cplat}] {cheapest.get('goods_name', '')}  到手 {cprice}")
        lines.append("")

    lines.append("| 平台 | 商品 | 原价 | 到手价 | 优惠 | 店铺 |")
    lines.append("|------|------|------|--------|------|------|")
    for r in rows:
        name = r["name"][:28]
        if r["coupon_desc"]:
            coupon = r["coupon_desc"]
        elif r["coupon_price"] and r["price"] and _to_float(r["coupon_price"]) < _to_float(r["price"]):
            coupon = "有券"
        else:
            coupon = "-"
        final = r["coupon_price"] or r["price"]
        lines.append(
            f"| {r['platform']} | {name} | {_fmt(r['original'])} | {_fmt(final)} | {coupon} | {r['mall'][:16]} |"
        )
    return "\n".join(lines)


def format_generic(data: dict[str, Any]) -> str:
    """daily/parse/local 的通用输出：优先表格，结构不符则回退 JSON"""
    if not data.get("success"):
        return f"查询失败: {data.get('message') or data.get('error') or '未知错误'}"

    items: list[Any] = []
    for key in ("data", "items", "list"):
        val = data.get(key)
        if isinstance(val, list) and val:
            items = val
            break
        if isinstance(val, dict):
            for sub in ("items", "list", "data"):
                if isinstance(val.get(sub), list) and val.get(sub):
                    items = val[sub]
                    break
            if items:
                break

    if not items:
        return json.dumps(data, ensure_ascii=False, indent=2)

    lines = ["| 平台 | 商品 | 到手价 | 优惠 | 店铺 |", "|------|------|--------|------|------|"]
    for item in items:
        if not isinstance(item, dict):
            continue
        plat = PLATFORM_NAMES.get(item.get("platform", ""), item.get("platform", "-"))
        name = str(item.get("goods_name") or item.get("title") or "")[:28]
        final = item.get("coupon_price") or item.get("min_price") or item.get("price")
        coupon = item.get("coupon_desc") or "-"
        mall = str(item.get("mall_name") or item.get("shop") or "")[:16]
        lines.append(f"| {plat} | {name} | {_fmt(final)} | {coupon} | {mall} |")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="xiaxiayouhui 跨平台比价（免 key）")
    sub = parser.add_subparsers(dest="command")

    p_search = sub.add_parser("search", help="跨平台比价")
    p_search.add_argument("keyword", help="搜索关键词")
    p_search.add_argument("--limit", type=int, default=10, help="每平台结果数(3-20)")
    p_search.add_argument("--platform", help="限定平台: 淘宝/京东/拼多多/抖音/苏宁/唯品会")
    p_search.add_argument("--json", action="store_true", help="输出原始 JSON")

    p_daily = sub.add_parser("daily", help="每日精选优惠")
    p_daily.add_argument("--limit", type=int, default=10)
    p_daily.add_argument("--json", action="store_true")

    p_parse = sub.add_parser("parse", help="解析商品链接/口令")
    p_parse.add_argument("url", help="商品链接或口令文本")
    p_parse.add_argument("--json", action="store_true")

    p_local = sub.add_parser("local", help="本地生活优惠")
    p_local.add_argument("--lat", type=float, help="纬度")
    p_local.add_argument("--lng", type=float, help="经度")
    p_local.add_argument("--radius", type=int, default=5000, help="半径(米)")
    p_local.add_argument("--json", action="store_true")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "search":
        res = search_compare(args.keyword, args.limit, args.platform)
        print(json.dumps(res, ensure_ascii=False, indent=2) if args.json else format_compare(res))
    elif args.command == "daily":
        res = daily_deals(args.limit)
        print(json.dumps(res, ensure_ascii=False, indent=2) if args.json else format_generic(res))
    elif args.command == "parse":
        res = parse_link(args.url)
        print(json.dumps(res, ensure_ascii=False, indent=2) if args.json else format_generic(res))
    elif args.command == "local":
        res = local_coupons(args.radius, args.lat, args.lng)
        print(json.dumps(res, ensure_ascii=False, indent=2) if args.json else format_generic(res))


if __name__ == "__main__":
    main()


# ── 引流信息（固定输出，prepare_release.py 自动补齐）─────────────
def _print_leadgen():
    print("")
    print("💡 更多实用 AI 效率工具和技能，领取自媒体 IP&超级个体&一人公司资料，关注公众号「桂皮AI实战」")
    print("📱 加入自媒体&AI 副业变现交流群：https://e418e2e692454bfaa8b6206e3f0ba789.app.codebuddy.work")


if __name__ == "__main__":
    _print_leadgen()
