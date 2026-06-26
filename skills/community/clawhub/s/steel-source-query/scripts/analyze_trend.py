#!/usr/bin/env python3
"""
钢材价格走势分析脚本
提供详细的价格分析和可视化建议
"""

import argparse
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple

# 数据目录
DATA_DIR = Path(__file__).parent.parent / "data"
PRICE_FILE = DATA_DIR / "prices.json"


def load_prices() -> List[Dict]:
    """加载价格历史"""
    if PRICE_FILE.exists():
        with open(PRICE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def analyze_trend(steel_type: str, region: str, days: int = 30) -> Dict:
    """
    深度分析价格走势
    
    Returns:
        {
            "trend_direction": "up"/"down"/"stable",
            "trend_strength": "strong"/"moderate"/"weak",
            "volatility": 波动率,
            "analysis": "分析结论",
            "forecast": "短期预测",
            "recommendation": "建议"
        }
    """
    prices = load_prices()
    
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    relevant = [
        p for p in prices
        if p.get("type") == steel_type
        and p.get("region") == region
        and p.get("date", "") >= cutoff_date
        and p.get("price") is not None
    ]
    
    if len(relevant) < 3:
        return {
            "trend_direction": "unknown",
            "analysis": "数据不足，无法分析",
            "recommendation": "建议等待更多数据"
        }
    
    # 按日期排序
    relevant.sort(key=lambda x: x.get("date", ""))
    
    prices_list = [p["price"] for p in relevant]
    dates = [p["date"] for p in relevant]
    
    # 基础统计
    first_price = prices_list[0]
    last_price = prices_list[-1]
    high = max(prices_list)
    low = min(prices_list)
    avg = sum(prices_list) / len(prices_list)
    
    # 涨跌计算
    total_change = last_price - first_price
    total_change_percent = (total_change / first_price * 100) if first_price else 0
    
    # 波动率计算（标准差/平均值）
    variance = sum((p - avg) ** 2 for p in prices_list) / len(prices_list)
    std_dev = variance ** 0.5
    volatility = (std_dev / avg * 100) if avg else 0
    
    # 趋势方向
    if total_change_percent > 3:
        trend_direction = "up"
    elif total_change_percent < -3:
        trend_direction = "down"
    else:
        trend_direction = "stable"
    
    # 趋势强度
    abs_change = abs(total_change_percent)
    if abs_change > 10:
        trend_strength = "strong"
    elif abs_change > 5:
        trend_strength = "moderate"
    else:
        trend_strength = "weak"
    
    # 分析结论
    analysis_parts = []
    
    if trend_direction == "up":
        analysis_parts.append(f"近{days}天价格上涨 {total_change_percent:.2f}%")
    elif trend_direction == "down":
        analysis_parts.append(f"近{days}天价格下跌 {abs(total_change_percent):.2f}%")
    else:
        analysis_parts.append(f"近{days}天价格基本稳定，波动在 {total_change_percent:.2f}% 以内")
    
    analysis_parts.append(f"价格区间: {low:.0f} ~ {high:.0f} 元/吨")
    analysis_parts.append(f"波动率: {volatility:.2f}%")
    
    # 短期预测
    if trend_direction == "up" and trend_strength == "strong":
        forecast = "强势上涨，短期可能继续上行"
    elif trend_direction == "up":
        forecast = "温和上涨，需关注回调风险"
    elif trend_direction == "down" and trend_strength == "strong":
        forecast = "下跌明显，短期可能继续探底"
    elif trend_direction == "down":
        forecast = "小幅下跌，可能企稳"
    else:
        forecast = "震荡整理，方向不明"
    
    # 建议
    if trend_direction == "up" and volatility < 5:
        recommendation = "上涨趋势稳定，可考虑适量采购"
    elif trend_direction == "up" and volatility >= 5:
        recommendation = "上涨但波动较大，建议分批采购"
    elif trend_direction == "down":
        recommendation = "价格下行，建议观望或按需采购"
    else:
        recommendation = "行情震荡，建议按需采购"
    
    return {
        "trend_direction": trend_direction,
        "trend_strength": trend_strength,
        "volatility": round(volatility, 2),
        "total_change": round(total_change, 2),
        "total_change_percent": round(total_change_percent, 2),
        "high": round(high, 2),
        "low": round(low, 2),
        "avg": round(avg, 2),
        "data_points": len(prices_list),
        "analysis": "；".join(analysis_parts),
        "forecast": forecast,
        "recommendation": recommendation,
        "dates": {
            "start": dates[0],
            "end": dates[-1]
        }
    }


def compare_regions(steel_type: str, regions: List[str]) -> str:
    """对比不同地区的价格"""
    lines = []
    lines.append(f"📊 {steel_type} 地区价格对比")
    lines.append("")
    
    region_prices = []
    for region in regions:
        result = analyze_trend(steel_type, region, days=1)  # 只取最新
        if result.get("avg"):
            region_prices.append((region, result["avg"]))
    
    if not region_prices:
        lines.append("暂无数据")
        return "\n".join(lines)
    
    # 排序
    region_prices.sort(key=lambda x: x[1], reverse=True)
    
    lines.append("价格从高到低:")
    for i, (region, price) in enumerate(region_prices, 1):
        lines.append(f"  {i}. {region}: {price:.0f} 元/吨")
    
    # 价差分析
    if len(region_prices) >= 2:
        max_price = region_prices[0][1]
        min_price = region_prices[-1][1]
        diff = max_price - min_price
        lines.append(f"\n最高与最低价差: {diff:.0f} 元/吨")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="钢材价格走势分析")
    parser.add_argument("--type", default="螺纹钢", help="钢材品种")
    parser.add_argument("--region", default="唐山", help="地区")
    parser.add_argument("--days", type=int, default=30, help="分析天数")
    parser.add_argument("--compare", help="对比多个地区，逗号分隔")
    
    args = parser.parse_args()
    
    if args.compare:
        # 地区对比模式
        regions = [r.strip() for r in args.compare.split(",")]
        report = compare_regions(args.type, regions)
    else:
        # 单品种深度分析
        result = analyze_trend(args.type, args.region, args.days)
        
        lines = []
        lines.append(f"📈 {args.type} ({args.region}) 价格走势分析")
        
        if result.get("trend_direction") == "unknown":
            lines.append(result["analysis"])
        else:
            lines.append(f"分析周期: {result['dates']['start']} ~ {result['dates']['end']}")
            lines.append("")
            
            # 趋势方向
            trend_emojis = {"up": "📈 上涨", "down": "📉 下跌", "stable": "➡️ 平稳"}
            lines.append(f"走势方向: {trend_emojis.get(result['trend_direction'], '❓ 未知')}")
            lines.append(f"趋势强度: {result['trend_strength']}")
            lines.append("")
            
            # 详细数据
            lines.append("📊 统计数据:")
            lines.append(f"  涨跌幅: {result['total_change_percent']:+.2f}%")
            lines.append(f"  涨跌额: {result['total_change']:+.0f} 元/吨")
            lines.append(f"  最高价: {result['high']:.0f} 元/吨")
            lines.append(f"  最低价: {result['low']:.0f} 元/吨")
            lines.append(f"  平均价: {result['avg']:.0f} 元/吨")
            lines.append(f"  波动率: {result['volatility']:.2f}%")
            lines.append("")
            
            # 分析结论
            lines.append("📝 分析结论:")
            lines.append(f"  {result['analysis']}")
            lines.append("")
            
            # 预测和建议
            lines.append("🔮 短期预测:")
            lines.append(f"  {result['forecast']}")
            lines.append("")
            lines.append("💡 操作建议:")
            lines.append(f"  {result['recommendation']}")
        
        report = "\n".join(lines)
    
    print(report)
    return report


if __name__ == "__main__":
    main()
