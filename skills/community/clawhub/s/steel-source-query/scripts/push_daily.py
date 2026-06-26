#!/usr/bin/env python3
"""
钢材价格定时推送脚本
支持每日自动生成价格日报并推送
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from scrape_price import query_price, scrape_zhaogang

# 数据目录
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

PRICE_FILE = DATA_DIR / "prices.json"
TREND_FILE = DATA_DIR / "trends.json"

# 默认推送配置
DEFAULT_QUERIES = [
    {"type": "螺纹钢", "region": "唐山"},
    {"type": "热轧板卷", "region": "唐山"},
    {"type": "冷轧板卷", "region": "上海"},
]


def load_prices() -> List[Dict]:
    """加载价格历史"""
    if PRICE_FILE.exists():
        with open(PRICE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def calculate_trend(steel_type: str, region: str, days: int = 7) -> Dict:
    """
    计算价格走势
    
    Returns:
        {
            "trend": "up"/"down"/"stable"/"unknown",
            "change": 涨跌额,
            "change_percent": 涨跌幅%,
            "high": 最高价,
            "low": 最低价,
            "avg": 平均价,
            "data_points": 数据点数量
        }
    """
    prices = load_prices()
    
    # 筛选该品种和地区的近期价格
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    relevant = [
        p for p in prices
        if p.get("type") == steel_type 
        and p.get("region") == region
        and p.get("date", "") >= cutoff_date
        and p.get("price") is not None
    ]
    
    if len(relevant) < 2:
        return {"trend": "unknown"}
    
    # 按日期排序
    relevant.sort(key=lambda x: x.get("date", ""))
    
    prices_list = [p["price"] for p in relevant]
    
    first_price = prices_list[0]
    last_price = prices_list[-1]
    
    change = last_price - first_price
    change_percent = (change / first_price * 100) if first_price else 0
    
    # 判断趋势
    if change_percent > 2:
        trend = "up"
    elif change_percent < -2:
        trend = "down"
    else:
        trend = "stable"
    
    return {
        "trend": trend,
        "change": round(change, 2),
        "change_percent": round(change_percent, 2),
        "high": max(prices_list),
        "low": min(prices_list),
        "avg": round(sum(prices_list) / len(prices_list), 2),
        "data_points": len(prices_list),
        "first_date": relevant[0].get("date"),
        "last_date": relevant[-1].get("date")
    }


def get_price_with_fallback(steel_type: str, region: str) -> Optional[Dict]:
    """
    获取价格（带多数据源回退）
    
    优先顺序：找钢网 → 缓存 → 失败
    """
    # 1. 尝试找钢网
    data = query_price("zhaogang", steel_type, region, cache_hours=2)
    if data and data.get("price"):
        return {
            "source": "找钢网",
            "price": data["price"],
            "date": data.get("date", datetime.now().strftime("%Y-%m-%d")),
            "unit": "元/吨"
        }
    
    # 2. 尝试缓存
    prices = load_prices()
    today = datetime.now().strftime("%Y-%m-%d")
    
    for p in sorted(prices, key=lambda x: x.get("timestamp", ""), reverse=True):
        if (p.get("type") == steel_type 
            and p.get("region") == region
            and p.get("price") is not None):
            return {
                "source": f"缓存 ({p.get('source', '未知')})",
                "price": p["price"],
                "date": p.get("date", today),
                "unit": "元/吨",
                "note": "使用缓存数据"
            }
    
    return None


def generate_report(queries: List[Dict] = None, days: int = 7) -> str:
    """
    生成价格日报
    
    Args:
        queries: 查询列表，默认使用 DEFAULT_QUERIES
        days: 走势天数
    """
    if queries is None:
        queries = DEFAULT_QUERIES
    
    today = datetime.now()
    
    lines = []
    lines.append("📊 钢材现货价格日报")
    lines.append(f"📅 {today.strftime('%Y年%m月%d日 %H:%M')}")
    lines.append("")
    lines.append("=" * 40)
    lines.append("")
    
    # 价格详情
    total_change = 0
    up_count = 0
    down_count = 0
    
    for query in queries:
        steel_type = query.get("type", "螺纹钢")
        region = query.get("region", "唐山")
        
        # 获取价格
        price_info = get_price_with_fallback(steel_type, region)
        
        # 计算走势
        trend = calculate_trend(steel_type, region, days)
        
        lines.append(f"🔸 {steel_type} ({region})")
        
        if price_info:
            lines.append(f"   💰 价格: {price_info['price']} 元/吨")
            lines.append(f"   📡 来源: {price_info['source']}")
            
            if trend.get("trend") != "unknown":
                trend_emoji = {"up": "📈", "down": "📉", "stable": "➡️"}
                change_str = f"{trend['change']:+.0f} ({trend['change_percent']:+.2f}%)"
                lines.append(f"   {trend_emoji.get(trend['trend'], '📊')} 走势: {change_str}")
                lines.append(f"   📊 区间: {trend['low']:.0f} ~ {trend['high']:.0f} 元/吨")
                
                # 统计
                if trend["trend"] == "up":
                    up_count += 1
                elif trend["trend"] == "down":
                    down_count += 1
                total_change += trend["change_percent"]
            else:
                lines.append("   ⚠️ 暂无走势数据")
        else:
            lines.append("   ❌ 暂无价格数据")
        
        lines.append("")
    
    # 汇总分析
    lines.append("=" * 40)
    lines.append("📈 市场概况")
    lines.append(f"   上涨: {up_count} 个品种")
    lines.append(f"   下跌: {down_count} 个品种")
    lines.append(f"   平均涨跌幅: {total_change/len(queries):+.2f}%")
    lines.append("")
    
    # 本地库存提示
    lines.append('💡 提示: 回复"查库存"查看本地钢贸商库存')
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="钢材价格日报推送")
    parser.add_argument("--test", action="store_true", help="测试模式，打印报告")
    parser.add_argument("--save", help="保存报告到文件")
    parser.add_argument("--types", help="指定品种，逗号分隔，如：螺纹钢,热轧板卷")
    parser.add_argument("--region", default="唐山", help="指定地区")
    parser.add_argument("--days", type=int, default=7, help="走势天数")
    
    args = parser.parse_args()
    
    # 构建查询列表
    if args.types:
        types = [t.strip() for t in args.types.split(",")]
        queries = [{"type": t, "region": args.region} for t in types]
    else:
        queries = DEFAULT_QUERIES
    
    # 生成报告
    report = generate_report(queries, args.days)
    
    if args.test:
        print(report)
    
    if args.save:
        with open(args.save, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n报告已保存: {args.save}")
    
    return report


if __name__ == "__main__":
    main()
