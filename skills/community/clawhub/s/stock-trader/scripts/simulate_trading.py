#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股模拟交易 - 激进型策略
用法: python simulate_trading.py [命令]
命令: start(开始模拟) / report(查看报告) / reset(重置)
"""

import sys
import subprocess
import re
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

# 交易记录文件
RECORD_FILE = "/root/.openclaw/workspace/skills/stock-trader/data/trading_record.json"

# 激进型策略配置
STRATEGY = {
    "name": "激进型",
    "init_cash": 50000,  # 初始资金5万
    "max_position": 0.9,  # 最高9成仓位
    "min_position": 0.3,  # 最低3成仓位
    "stop_loss": -0.07,  # 止损7%
    "take_profit": 0.15,  # 止盈15%
    "trade_ratio": 0.5,   # 每次交易5成仓位
    "chase_threshold": 0.05,  # 追涨阈值：涨幅>5%可追
    "cut_loss_threshold": -0.03,  # 杀跌阈值：跌幅>-3%可割
}

# 热门强势股池（激进型追热点）
HOT_STOCKS = [
    ("sz002475", "立讯精密"),
    ("sz300750", "宁德时代"),
    ("sh688981", "中芯国际"),
    ("sz300059", "东方财富"),
    ("sz002594", "比亚迪"),
    ("sh600519", "贵州茅台"),
    ("sz300274", "阳光电源"),
    ("sz002371", "北方华创"),
    ("sh601012", "隆基绿能"),
    ("sz000063", "中兴通讯"),
]

def ensure_data_dir():
    """确保数据目录存在"""
    os.makedirs(os.path.dirname(RECORD_FILE), exist_ok=True)
    if not os.path.exists(RECORD_FILE):
        with open(RECORD_FILE, 'w') as f:
            json.dump({
                "init_cash": STRATEGY["init_cash"],
                "current_cash": STRATEGY["init_cash"],
                "positions": {},
                "trades": [],
                "daily_reports": [],
                "start_date": datetime.now().strftime("%Y-%m-%d")
            }, f, indent=2, ensure_ascii=False)

def load_record():
    """加载交易记录"""
    ensure_data_dir()
    with open(RECORD_FILE, 'r') as f:
        return json.load(f)

def save_record(record):
    """保存交易记录"""
    with open(RECORD_FILE, 'w') as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

def get_stock_price(stock_code):
    """获取股票实时价格"""
    url = f"https://qt.gtimg.cn/q={stock_code}"
    try:
        result = subprocess.run(["curl", "-s", url], capture_output=True, timeout=10)
        data = result.stdout.decode('gbk', errors='ignore').strip()
        if not data or "v_" not in data:
            return None
        match = re.search(r'"([^"]+)"', data)
        if not match:
            return None
        fields = match.group(1).split("~")
        if len(fields) < 35:
            return None
        return {
            "name": fields[1],
            "code": fields[2],
            "price": float(fields[3]),
            "change_percent": float(fields[32]) if fields[32] else 0,
            "yesterday_close": float(fields[4]),
        }
    except:
        return None

def simulate_trade():
    """激进型模拟交易"""
    record = load_record()
    current_cash = record["current_cash"]
    positions = record.get("positions", {})
    
    print(f"\n{'='*70}")
    print(f"🚀 A股模拟交易 - {STRATEGY['name']}策略")
    print(f"{'='*70}")
    print(f"\n📊 当前账户状态:")
    print(f"  现金: {current_cash:.2f}元")
    print(f"  持仓数: {len(positions)}只")
    
    total_value = current_cash
    position_value = 0
    
    # 计算持仓市值
    for code, info in positions.items():
        data = get_stock_price(code)
        if data:
            cost = info["price"]
            current = data["price"]
            pos_value = info["shares"] * current
            pos_cost = info["shares"] * cost
            profit = pos_value - pos_cost
            profit_pct = (profit / pos_cost) * 100 if pos_cost > 0 else 0
            position_value += pos_value
            print(f"  • {data['name']}({code}): 持仓{info['shares']}股")
            print(f"    成本:{cost:.2f} → 现价:{current:.2f} ({profit_pct:+.2f}%)")
    
    total_value += position_value
    total_profit = total_value - STRATEGY["init_cash"]
    total_profit_pct = (total_profit / STRATEGY["init_cash"]) * 100
    
    print(f"\n  📈 总市值: {total_value:.2f}元")
    print(f"  💰 总收益: {total_profit:+.2f}元 ({total_profit_pct:+.2f}%)")
    
    # 激进型交易策略
    print(f"\n{'─'*70}")
    print(f"⚡ 激进型交易策略分析")
    print('─' * 70)
    
    # 检查是否需要调仓
    position_ratio = position_value / total_value if total_value > 0 else 0
    
    # 追涨杀跌：检查强势股
    opportunities = []
    risks = []
    
    for code, name in HOT_STOCKS:
        data = get_stock_price(code)
        if not data:
            continue
        
        change = data["change_percent"]
        
        # 追涨：涨幅>5%且有仓位
        if change > 5:
            if code not in positions:
                opportunities.append((code, name, change, "追涨"))
        
        # 杀跌：跌幅>-5%且持有
        if code in positions and change < -5:
            pos = positions[code]
            if pos.get("profit_pct", 0) < STRATEGY["cut_loss_threshold"] * 100:
                risks.append((code, name, change, "割肉"))
    
    # 建议操作
    print(f"\n📋 今日操作建议:")
    
    if opportunities and position_ratio < STRATEGY["max_position"]:
        print(f"\n  🔥 追涨机会 (强势股):")
        for code, name, change, action in opportunities[:3]:
            print(f"    • {name}({code}): +{change:.2f}% → 建议{action}")
    
    if risks:
        print(f"\n  ⚠️ 风险提示 (需割肉):")
        for code, name, change, action in risks[:3]:
            print(f"    • {name}({code}): {change:.2f}% → 建议{action}")
    
    if not opportunities and not risks:
        print(f"  • 今日无明显操作信号，保持观望")
    
    # 更新记录
    record["current_cash"] = current_cash
    record["positions"] = positions
    record["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_record(record)
    
    print(f"\n{'='*70}")
    print("💡 激进型策略特点:")
    print("  • 高仓位运行 (8-9成)")
    print("  • 追涨强势股 (>5%涨幅)")
    print("  • 杀跌果断 (>3%亏损即割)")
    print("  • 短线为主，快进快出")
    print("="*70 + "\n")

def show_report():
    """显示交易报告"""
    record = load_record()
    
    print(f"\n{'='*70}")
    print(f"📊 模拟交易报告 - {STRATEGY['name']}策略")
    print(f"{'='*70}")
    print(f"\n📅 起始日期: {record.get('start_date', '未知')}")
    print(f"💰 初始资金: {record['init_cash']:.2f}元")
    print(f"💵 当前现金: {record['current_cash']:.2f}元")
    
    # 计算持仓
    positions = record.get("positions", {})
    position_value = 0
    
    for code, info in positions.items():
        data = get_stock_price(code)
        if data:
            position_value += info["shares"] * data["price"]
    
    total_value = record["current_cash"] + position_value
    total_profit = total_value - record["init_cash"]
    total_profit_pct = (total_profit / record["init_cash"]) * 100
    
    print(f"📈 持仓市值: {position_value:.2f}元 ({len(positions)}只)")
    print(f"💎 总资产: {total_value:.2f}元")
    print(f"📊 总收益: {total_profit:+.2f}元 ({total_profit_pct:+.2f}%)")
    
    trades = record.get("trades", [])
    print(f"\n📝 交易记录: {len(trades)}笔")
    
    print(f"\n{'='*70}\n")

def daily_report():
    """每日收盘报告"""
    record = load_record()
    
    current_cash = record["current_cash"]
    positions = record.get("positions", {})
    
    # 获取所有持仓实时值
    total_stock_value = 0
    position_details = []
    
    for code, info in positions.items():
        data = get_stock_price(code)
        if data:
            current_value = info["shares"] * data["price"]
            cost_value = info["shares"] * info["price"]
            profit = current_value - cost_value
            profit_pct = (profit / cost_value) * 100 if cost_value > 0 else 0
            total_stock_value += current_value
            position_details.append({
                "code": code,
                "name": data["name"],
                "shares": info["shares"],
                "cost": info["price"],
                "current": data["price"],
                "profit": profit,
                "profit_pct": profit_pct
            })
    
    total_assets = current_cash + total_stock_value
    total_profit = total_assets - STRATEGY["init_cash"]
    total_profit_pct = (total_profit / STRATEGY["init_cash"]) * 100
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    print(f"\n{'='*70}")
    print(f"📈 每日收盘报告 - {today}")
    print(f"策略: {STRATEGY['name']} | 初始资金: {STRATEGY['init_cash']}元")
    print(f"{'='*70}")
    
    print(f"\n💰 资产情况:")
    print(f"  现金: {current_cash:.2f}元")
    print(f"  持仓: {total_stock_value:.2f}元 ({len(positions)}只)")
    print(f"  总资产: {total_assets:.2f}元")
    
    emoji = "📈" if total_profit >= 0 else "📉"
    print(f"\n  {emoji} 总收益: {total_profit:+.2f}元 ({total_profit_pct:+.2f}%)")
    
    if position_details:
        print(f"\n📊 持仓明细:")
        print(f"  {'股票':<10}{'代码':<10}{'持仓':>6}{'成本':>8}{'现价':>8}{'盈亏':>10}")
        print(f"  {'─'*60}")
        for p in position_details:
            p_emoji = "📈" if p["profit"] >= 0 else "📉"
            print(f"  {p['name']:<8}{p['code']:<10}{p['shares']:>6}{p['cost']:>8.2f}{p['current']:>8.2f}{p_emoji}{p['profit_pct']:>8.2f}%")
    
    # 记录日报
    daily_report = {
        "date": today,
        "cash": current_cash,
        "stock_value": total_stock_value,
        "total_assets": total_assets,
        "profit": total_profit,
        "profit_pct": total_profit_pct,
        "positions": len(positions)
    }
    
    reports = record.get("daily_reports", [])
    reports.append(daily_report)
    record["daily_reports"] = reports[-30:]  # 保留最近30天
    save_record(record)
    
    print(f"\n{'='*70}")
    print("💡 激进型策略今日表现")
    print(f"{'='*70}\n")

def reset_trading():
    """重置交易"""
    ensure_data_dir()
    with open(RECORD_FILE, 'w') as f:
        json.dump({
            "init_cash": STRATEGY["init_cash"],
            "current_cash": STRATEGY["init_cash"],
            "positions": {},
            "trades": [],
            "daily_reports": [],
            "start_date": datetime.now().strftime("%Y-%m-%d")
        }, f, indent=2, ensure_ascii=False)
    print(f"✅ 已重置交易账户，初始资金: {STRATEGY['init_cash']}元")

def main():
    if len(sys.argv) < 2:
        # 默认显示交易界面
        simulate_trade()
        return
    
    command = sys.argv[1]
    
    if command in ["start", "交易", "模拟"]:
        simulate_trade()
    elif command in ["report", "报告", "查看"]:
        show_report()
    elif command in ["daily", "收盘", "日报"]:
        daily_report()
    elif command in ["reset", "重置"]:
        reset_trading()
    else:
        print("用法:")
        print("  python simulate_trading.py        # 启动交易")
        print("  python simulate_trading.py report  # 查看报告")
        print("  python simulate_trading.py daily   # 每日收盘报告")
        print("  python simulate_trading.py reset   # 重置账户")

if __name__ == "__main__":
    main()
