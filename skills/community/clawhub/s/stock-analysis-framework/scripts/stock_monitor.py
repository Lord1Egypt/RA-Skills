#!/usr/bin/env python3
"""
Stock Monitor — 实时盯盘监控脚本
监控持仓股票的价格、成交量、资金流向
支持异动检测和告警

用法: python3 stock_monitor.py [--portfolio PORTFOLIO_FILE] [--threshold 3]
"""

import urllib.request
import json
import sys
import os
from datetime import datetime

# 默认持仓列表（当无法读取portfolio文件时使用）
DEFAULT_STOCKS = [
    ("铜陵有色", "sz000630"),
    ("云铝股份", "sz000807"),
    ("神火股份", "sz000933"),
    ("四川黄金", "sz001337"),
    ("长城电工", "sh600192"),
    ("四川长虹", "sh600839"),
    ("华友钴业", "sh603799"),
]

def read_portfolio(filepath=None):
    """从投资组合数据文件读取持仓"""
    if filepath and os.path.exists(filepath):
        stocks = []
        with open(filepath) as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    h = json.loads(line)
                    code = h.get("code", "")
                    if not code:
                        # 需要从名称查代码
                        pass
                    stocks.append((h["ticker"], code or "sz000001"))
                except json.JSONDecodeError:
                    continue
        if stocks:
            return stocks
    return DEFAULT_STOCKS

def get_all_quotes(stocks):
    """批量获取所有持仓行情"""
    codes = [s[1] for s in stocks]
    url = "https://hq.sinajs.cn/list=" + ",".join(codes)
    req = urllib.request.Request(url, headers={"Referer": "https://finance.sina.com.cn"})
    resp = urllib.request.urlopen(req, timeout=15)
    text = resp.read().decode("gbk")

    results = []
    for line in text.strip().split("\n"):
        if "=" not in line:
            continue
        data = line.split("=", 1)[1].strip().strip('";\n')
        fields = data.split(",")
        if len(fields) >= 32 and fields[0]:
            results.append({
                "name": fields[0],
                "open": float(fields[1]),
                "prev_close": float(fields[2]),
                "current": float(fields[3]),
                "high": float(fields[4]),
                "low": float(fields[5]),
                "volume": int(fields[8]),
                "amount": float(fields[9]),
                "change_pct": round((float(fields[3]) - float(fields[2])) / float(fields[2]) * 100, 2)
            })
    return results

def check_alerts(quote, threshold):
    """检测异动"""
    alerts = []
    if quote["change_pct"] > threshold:
        alerts.append(f"🚨 快速拉升! +{quote['change_pct']:.1f}%")
    elif quote["change_pct"] < -threshold:
        alerts.append(f"🚨 快速下跌! {quote['change_pct']:.1f}%")

    amount_yi = quote["amount"] / 100000000
    if amount_yi > 5:
        alerts.append(f"⚡ 天量成交 ¥{amount_yi:.1f}亿")

    return alerts

def format_bar(value, max_val, width=10):
    """生成比较条"""
    bar_len = int(abs(value) / max_val * width) if max_val > 0 else 0
    bar_len = min(bar_len, width)
    if value > 0:
        return "🟢" + "█" * bar_len
    elif value < 0:
        return "🔴" + "█" * bar_len
    return "─" * 2

def monitor(threshold=3):
    stocks = DEFAULT_STOCKS
    portfolio_path = os.path.expanduser("~/.investment-portfolio/holdings.jsonl")
    if os.path.exists(portfolio_path):
        pf_stocks = read_portfolio(portfolio_path)
        if pf_stocks:
            stocks = pf_stocks

    print(f"""
╔══════════════════════════════════════╗
║    📡 实时盯盘监控                    ║
║    {datetime.now().strftime('%Y-%m-%d %H:%M')}              ║
╚══════════════════════════════════════╝""")

    quotes = get_all_quotes(stocks)
    if not quotes:
        print("  ❌ 无法获取行情数据")
        return

    # 计算最大成交额用于比较条
    max_amount = max(q["amount"] for q in quotes) if quotes else 1

    print(f"\n  {'股票':>8} {'现价':>7} {'涨跌幅':>8} {'成交额':>10} {'活跃度':>8} {'异动':>10}")
    print(f"  {'─'*55}")

    for q in quotes:
        chg = q["change_pct"]
        amount_yi = q["amount"] / 100000000
        alerts = check_alerts(q, threshold)
        alert_str = alerts[0][:10] if alerts else ""

        bar = format_bar(q["amount"], max_amount)
        print(f"  {q['name']:>8} {q['current']:>7.2f} {chg:>+7.2f}% {amount_yi:>7.2f}亿 {bar[:6]:>8} {alert_str:>10}")

    print(f"\n  {'─'*55}")
    print(f"  🚨 异动: 涨跌幅>{threshold}% 或 天量成交>5亿")
    print(f"  ⚠️ 分析仅供参考，不构成投资建议")

if __name__ == "__main__":
    threshold = 3
    if len(sys.argv) > 1 and sys.argv[1] == "--threshold":
        threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 3
    monitor(threshold)
