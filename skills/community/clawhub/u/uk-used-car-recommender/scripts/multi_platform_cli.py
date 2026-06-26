"""
多平台搜索 CLI - 支持 Gumtree + AutoTrader

使用方法：
python scripts/multi_platform_cli.py search \
  --make toyota --model yaris \
  --max-price 10000 \
  --postcode SW1A1AA \
  --platforms gumtree,autotrader \
  --limit 10
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

# 导入现有的 Gumtree 搜索
from cars.scraper import run_car_search as search_gumtree
from cars.urls import build_car_search_url

# 导入新的 AutoTrader 搜索
from cars.autotrader import search_autotrader


def postcode_to_location(postcode: str) -> str:
    """将英国邮编转换为城市名（简化版）"""
    # 伦敦邮编前缀
    london_prefixes = [
        "E", "EC", "N", "NW", "SE", "SW", "W", "WC",
        "BR", "CR", "DA", "EN", "HA", "IG", "KT", "RM", "SM", "TW", "UB"
    ]
    
    prefix = postcode.split()[0][:2].upper()
    
    if any(postcode.upper().startswith(lp) for lp in london_prefixes):
        return "London"
    
    # 其他主要城市邮编（简化映射）
    city_map = {
        "M": "Manchester",
        "B": "Birmingham",
        "L": "Liverpool",
        "LS": "Leeds",
        "G": "Glasgow",
        "EH": "Edinburgh",
        "BS": "Bristol",
        "NE": "Newcastle",
        "S": "Sheffield",
    }
    
    for prefix, city in city_map.items():
        if postcode.upper().startswith(prefix):
            return city
    
    return "uk"  # 默认全国


def merge_results(
    gumtree_result: dict[str, Any] | None,
    autotrader_result: dict[str, Any] | None,
) -> dict[str, Any]:
    """合并多个平台的搜索结果"""
    
    merged_items = []
    
    if gumtree_result and gumtree_result.get("ok"):
        merged_items.extend(gumtree_result["items"])
    
    if autotrader_result and autotrader_result.get("ok"):
        merged_items.extend(autotrader_result["items"])
    
    # 按价格排序
    merged_items.sort(key=lambda x: x.get("price") or 999999)
    
    return {
        "ok": True,
        "source": "multi_platform",
        "platforms": {
            "gumtree": {
                "ok": gumtree_result.get("ok") if gumtree_result else False,
                "total": gumtree_result.get("total", 0) if gumtree_result else 0,
                "error": gumtree_result.get("error") if gumtree_result else None,
            },
            "autotrader": {
                "ok": autotrader_result.get("ok") if autotrader_result else False,
                "total": autotrader_result.get("total", 0) if autotrader_result else 0,
                "error": autotrader_result.get("error") if autotrader_result else None,
            },
        },
        "total": len(merged_items),
        "items": merged_items,
    }


def main():
    parser = argparse.ArgumentParser(
        description="多平台二手车搜索 CLI - 支持 Gumtree + AutoTrader"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # search 命令
    search_parser = subparsers.add_parser("search", help="搜索二手车")
    
    # 平台选择
    search_parser.add_argument(
        "--platforms",
        default="gumtree,autotrader",
        help="搜索平台（逗号分隔），可选：gumtree, autotrader. 默认：gumtree,autotrader"
    )
    
    # 基础参数
    search_parser.add_argument("--make", help="品牌（如 toyota）")
    search_parser.add_argument("--model", help="车型（如 yaris）")
    search_parser.add_argument("--postcode", default="SW1A1AA", help="邮编（用于 AutoTrader）")
    search_parser.add_argument("--location", help="位置（用于 Gumtree，如 London 或 uk）")
    search_parser.add_argument("--radius", type=int, default=10, help="搜索半径（英里）")
    search_parser.add_argument("--min-price", type=int, help="最低价格")
    search_parser.add_argument("--max-price", type=int, help="最高价格")
    search_parser.add_argument("--min-year", type=int, help="最早年份")
    search_parser.add_argument("--max-year", type=int, help="最晚年份")
    search_parser.add_argument("--fuel-type", help="燃料类型（petrol, diesel, electric, hybrid）")
    search_parser.add_argument("--transmission", help="变速箱（manual, automatic）")
    search_parser.add_argument("--sort", default="price_low", help="排序方式")
    search_parser.add_argument("--limit", type=int, default=10, help="每个平台返回结果数量")
    
    args = parser.parse_args()
    
    if args.command == "search":
        platforms = [p.strip().lower() for p in args.platforms.split(",")]
        
        # 如果未提供 location，尝试从 postcode 推导
        location = args.location or postcode_to_location(args.postcode)
        
        results = {}
        
        # 搜索 Gumtree
        if "gumtree" in platforms:
            print("🔍 搜索 Gumtree...", file=sys.stderr)
            try:
                # 构建 Gumtree URL
                gumtree_url = build_car_search_url(
                    make=args.make,
                    model=args.model,
                    search_location=location,
                    max_price=args.max_price,
                    fuel_type=args.fuel_type,
                    transmission=args.transmission,
                )
                
                results["gumtree"] = search_gumtree(
                    search_url=gumtree_url,
                    limit=args.limit,
                )
                
                if results["gumtree"]["ok"]:
                    print(f"✓ Gumtree: 找到 {results['gumtree']['total']} 辆车", file=sys.stderr)
                else:
                    print(f"✗ Gumtree: {results['gumtree'].get('error')}", file=sys.stderr)
                    
            except Exception as e:
                print(f"✗ Gumtree 搜索失败: {e}", file=sys.stderr)
                results["gumtree"] = {"ok": False, "error": str(e), "items": [], "total": 0}
        
        # 搜索 AutoTrader
        if "autotrader" in platforms:
            print("🔍 搜索 AutoTrader...", file=sys.stderr)
            try:
                results["autotrader"] = search_autotrader(
                    make=args.make,
                    model=args.model,
                    postcode=args.postcode,
                    radius=args.radius,
                    max_price=args.max_price,
                    min_year=args.min_year,
                    max_year=args.max_year,
                    limit=args.limit,
                )
                
                if results["autotrader"]["ok"]:
                    print(f"✓ AutoTrader: 找到 {results['autotrader']['total']} 辆车", file=sys.stderr)
                else:
                    print(f"✗ AutoTrader: {results['autotrader'].get('error')}", file=sys.stderr)
                    
            except Exception as e:
                print(f"✗ AutoTrader 搜索失败: {e}", file=sys.stderr)
                results["autotrader"] = {"ok": False, "error": str(e), "items": [], "total": 0}
        
        # 合并结果
        merged = merge_results(
            results.get("gumtree"),
            results.get("autotrader")
        )
        
        # 🆕 添加销量推断分析
        if args.make and args.model and args.max_price and merged["ok"]:
            print("📊 分析市场数据...", file=sys.stderr)
            try:
                from cars.sales_inference import analyze_market_without_api
                
                market_analysis = analyze_market_without_api(
                    make=args.make,
                    model=args.model,
                    search_results=merged,
                    budget=args.max_price,
                )
                
                # 添加到结果中
                merged["market_intelligence"] = market_analysis
                
                # 输出分析摘要到 stderr
                pop = market_analysis['popularity_analysis']
                print(f"\n📈 市场分析摘要:", file=sys.stderr)
                print(f"  热度评分: {pop['popularity_score']}/100", file=sys.stderr)
                print(f"  供应水平: {pop['supply_description']} ({pop['total_listings']} 辆)", file=sys.stderr)
                print(f"  预计售出: {pop['estimated_days_to_sell']}", file=sys.stderr)
                print(f"  建议:", file=sys.stderr)
                for rec in pop['recommendations']:
                    print(f"    {rec}", file=sys.stderr)
                print(file=sys.stderr)
                
            except Exception as e:
                print(f"⚠️  市场分析失败: {e}", file=sys.stderr)
        
        # 输出 JSON
        print(json.dumps(merged, ensure_ascii=False, indent=2))
        
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
