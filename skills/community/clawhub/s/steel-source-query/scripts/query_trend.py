#!/usr/bin/env python3
"""
钢材价格走势查询脚本
支持查询历史价格数据并生成趋势图表
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

# 数据目录
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# 历史数据文件
HISTORY_FILE = DATA_DIR / "price_history.json"


def get_history() -> Dict:
    """读取历史价格数据"""
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_history(data: Dict):
    """保存历史价格数据"""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def record_price(source: str, steel_type: str, region: str, price: float):
    """记录每日价格到历史数据"""
    history = get_history()
    key = f"{source}_{steel_type}_{region}"
    
    if key not in history:
        history[key] = []
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 检查今天是否已记录
    existing = [r for r in history[key] if r.get("date") == today]
    if not existing:
        history[key].append({
            "date": today,
            "price": price,
            "timestamp": datetime.now().isoformat()
        })
        # 只保留最近365天
        history[key] = sorted(history[key], key=lambda x: x["date"])[-365:]
        save_history(history)


def query_trend(source: str, steel_type: str, region: str, days: int = 30) -> List[Dict]:
    """查询价格走势"""
    history = get_history()
    key = f"{source}_{steel_type}_{region}"
    
    if key not in history or not history[key]:
        return []
    
    # 获取最近days天的数据
    all_data = sorted(history[key], key=lambda x: x["date"])
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    filtered_data = [
        r for r in all_data
        if start_date <= datetime.fromisoformat(r["date"]) <= end_date
    ]
    
    return filtered_data


def calculate_trend(data: List[Dict]) -> Dict:
    """计算趋势指标"""
    if not data or len(data) < 2:
        return {
            "trend": "unknown",
            "change_amount": 0,
            "change_percent": 0,
            "highest": None,
            "lowest": None,
            "average": None
        }
    
    prices = [r["price"] for r in data if "price" in r]
    if not prices:
        return {"trend": "unknown", "change_amount": 0, "change_percent": 0}
    
    first_price = prices[0]
    last_price = prices[-1]
    change_amount = last_price - first_price
    change_percent = (change_amount / first_price) * 100 if first_price else 0
    
    return {
        "trend": "up" if change_amount > 0 else "down" if change_amount < 0 else "stable",
        "change_amount": round(change_amount, 2),
        "change_percent": round(change_percent, 2),
        "highest": max(prices),
        "lowest": min(prices),
        "average": round(sum(prices) / len(prices), 2),
        "data_points": len(prices)
    }


def generate_chart(data: List[Dict], output_path: str):
    """生成ASCII或简单文本图表"""
    if not data:
        return "暂无数据"
    
    lines = []
    lines.append(f"价格走势图 (最近{len(data)}天)")
    lines.append("=" * 50)
    
    prices = [r["price"] for r in data if "price" in r]
    if not prices:
        return "无价格数据"
    
    max_price = max(prices)
    min_price = min(prices)
    price_range = max_price - min_price if max_price != min_price else 1
    
    # 简单的ASCII图表
    chart_height = 10
    for i in range(chart_height, -1, -1):
        level = min_price + (price_range * i / chart_height)
        line = f"{level:>8.0f} | "
        for r in data:
            if "price" in r:
                bar_height = ((r["price"] - min_price) / price_range) * chart_height
                line += "█" if bar_height >= i else " "
        lines.append(line)
    
    lines.append("         " + "-" * len(data))
    # 显示日期
    dates = [r["date"][-5:] for r in data]  # 只显示 MM-DD
    lines.append("         " + "".join([d[:2] for d in dates[::max(1, len(dates)//10)]]))
    
    return "\n".join(lines)


def format_trend_output(data: List[Dict], trend: Dict) -> str:
    """格式化趋势输出"""
    lines = []
    
    # 趋势摘要
    trend_emoji = {"up": "📈", "down": "📉", "stable": "➡️", "unknown": "❓"}
    lines.append(f"{trend_emoji.get(trend['trend'], '❓')} 趋势分析")
    lines.append(f"涨跌额: {trend['change_amount']:+.2f} 元/吨")
    lines.append(f"涨跌幅: {trend['change_percent']:+.2f}%")
    
    if trend.get("highest"):
        lines.append(f"最高价: {trend['highest']:.2f} 元/吨")
    if trend.get("lowest"):
        lines.append(f"最低价: {trend['lowest']:.2f} 元/吨")
    if trend.get("average"):
        lines.append(f"平均价: {trend['average']:.2f} 元/吨")
    
    lines.append("")
    
    # 详细数据
    if data:
        lines.append("历史价格明细:")
        lines.append(f"{'日期':<12} {'价格(元/吨)':<12} {'较昨日':<10}")
        lines.append("-" * 40)
        
        prev_price = None
        for r in data:
            price = r.get("price", "-")
            if prev_price and isinstance(price, (int, float)):
                diff = price - prev_price
                diff_str = f"{diff:+.2f}"
            else:
                diff_str = "-"
            
            lines.append(f"{r.get('date', '-'):<12} {price:<12} {diff_str:<10}")
            if isinstance(price, (int, float)):
                prev_price = price
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="钢材价格走势查询")
    parser.add_argument("--source", choices=["mysteel", "lange"], default="mysteel",
                        help="数据源")
    parser.add_argument("--type", required=True, help="钢材品种")
    parser.add_argument("--region", required=True, help="地区")
    parser.add_argument("--days", type=int, default=30, help="查询天数")
    parser.add_argument("--chart", action="store_true", help="生成图表")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    parser.add_argument("--record", help="记录今日价格 (格式: 价格数值)")
    
    args = parser.parse_args()
    
    # 如果需要记录价格
    if args.record:
        try:
            price = float(args.record)
            record_price(args.source, args.type, args.region, price)
            print(f"已记录 {args.type} {args.region} 价格: {price} 元/吨")
            return
        except ValueError:
            print("价格格式错误", file=sys.stderr)
            sys.exit(1)
    
    # 查询趋势
    data = query_trend(args.source, args.type, args.region, args.days)
    trend = calculate_trend(data)
    
    if args.json:
        output = {
            "trend": trend,
            "data": data
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(format_trend_output(data, trend))
        
        if args.chart:
            print("\n")
            print(generate_chart(data, "/tmp/trend_chart.txt"))


if __name__ == "__main__":
    main()
