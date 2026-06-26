#!/usr/bin/env python3
"""
Stock Briefing — 持仓简报生成
读取投资组合数据，结合消息面信息，生成综合分析简报

用法: python3 stock_briefing.py
"""

import urllib.request
import json
import os
from datetime import datetime

PORTFOLIO_FILE = os.path.expanduser("~/.investment-portfolio/holdings.jsonl")
HISTORY_FILE = os.path.expanduser("~/.investment-portfolio/history.log")

def read_portfolio():
    """读取持仓数据"""
    holdings = []
    if not os.path.exists(PORTFOLIO_FILE):
        return holdings
    with open(PORTFOLIO_FILE) as f:
        for line in f:
            if line.strip():
                holdings.append(json.loads(line))
    return holdings

def get_code(name):
    """名称到代码映射"""
    mapping = {
        "铜陵有色": "sz000630", "云铝股份": "sz000807", "神火股份": "sz000933",
        "四川黄金": "sz001337", "双鹭药业": "sz002038", "长城电工": "sh600192",
        "四川长虹": "sh600839", "华友钴业": "sh603799",
    }
    return mapping.get(name, "")

def get_current_prices(holdings):
    """批量获取当前价格"""
    codes = []
    for h in holdings:
        code = get_code(h["ticker"])
        if code:
            codes.append(code)

    if not codes:
        return {}

    url = "https://hq.sinajs.cn/list=" + ",".join(codes)
    req = urllib.request.Request(url, headers={"Referer": "https://finance.sina.com.cn"})
    resp = urllib.request.urlopen(req, timeout=15)
    text = resp.read().decode("gbk")

    prices = {}
    for line in text.strip().split("\n"):
        if "=" not in line:
            continue
        data = line.split("=", 1)[1].strip().strip('";\n')
        fields = data.split(",")
        if len(fields) >= 32 and fields[0]:
            prices[fields[0]] = {
                "current": float(fields[3]),
                "change_pct": round((float(fields[3]) - float(fields[2])) / float(fields[2]) * 100, 2),
                "open": float(fields[1]),
                "high": float(fields[4]),
                "low": float(fields[5]),
                "volume": int(fields[8]),
                "amount": float(fields[9]),
            }
    return prices

def generate_report():
    holdings = read_portfolio()
    if not holdings:
        print("  ❌ 持仓数据为空")
        return

    prices = get_current_prices(holdings)

    print(f"""
╔══════════════════════════════════════╗
║    📋 持仓综合简报                    ║
║    {datetime.now().strftime('%Y-%m-%d %H:%M')}             ║
╚══════════════════════════════════════╝""")

    # 汇总
    total_value = 0
    total_cost = 0
    total_pnl = 0

    print(f"\n  {'股票':>8} {'成本':>8} {'现价':>8} {'盈亏%':>7} {'市值':>10} {'消息面':>20}")
    print(f"  {'─'*65}")

    for h in holdings:
        ticker = h["ticker"]
        shares = h["shares"]
        buy_price = h["buy_price"]
        cost = shares * buy_price
        p = prices.get(ticker, {})
        current = p.get("current", h["current_price"])
        value = shares * current
        pnl = (current - buy_price) / buy_price * 100
        total_cost += cost
        total_value += value

        news = h.get("news", "")
        news_short = news[:18] + ".." if len(news) > 20 else news

        icon = "🟢🟢" if pnl > 5 else "🟢" if pnl > 0 else "🔶" if pnl > -3 else "🔴" if pnl > -5 else "🔴🔴"
        print(f"  {icon} {ticker:>6} {buy_price:>7.2f} {current:>7.2f} {pnl:>+6.1f}% {value:>9,.0f} {news_short:>20}")

    total_pnl = total_value - total_cost
    total_pnl_pct = total_pnl / total_cost * 100 if total_cost > 0 else 0

    print(f"  {'─'*65}")
    print(f"  总成本: ¥{total_cost:,.2f}")
    print(f"  总市值: ¥{total_value:,.2f}")
    print(f"  总盈亏: ¥{total_pnl:+,.2f} ({total_pnl_pct:+.1f}%)")

    # 六维快速评分
    print(f"\n  {'─'*65}")
    print(f"  📊 组合六维快速评估")
    print(f"  {'─'*65}")

    up_count = sum(1 for h in holdings for t in [h["ticker"]] for p in [prices.get(t, {})] if p.get("change_pct", 0) > 0)
    down_count = len(holdings) - up_count

    print(f"  今日上涨: {up_count}/{len(holdings)}  |  下跌: {down_count}/{len(holdings)}")
    print(f"  {'─'*65}")
    print(f"  ⚠️ 分析仅供参考，不构成投资建议")

if __name__ == "__main__":
    generate_report()
