#!/usr/bin/env python3
"""研盾 · 仓位计算与止损策略"""
import json, sys, argparse, hashlib
from datetime import datetime

STOCK_MAP = {"sh600519": {"name":"贵州茅台","price":1194.45},"sz300750":{"name":"宁德时代","price":218.50}}

def calc(code, capital):
    info = STOCK_MAP.get(code, {"name":code, "price":100.0})
    # 确定性演示计算：基于标的代码hash生成固定风险分（可复现，非随机）
    seed = int(hashlib.md5(code.encode("utf-8")).hexdigest(), 16)
    risk_score = 20 + seed % 31  # 20-50 确定性区间
    pct_map = {20:25, 25:22, 30:20, 35:18, 40:15, 45:12, 50:10}
    suggested_pct = min(pct_map.get((risk_score//5)*5, 15), 25)
    stop_pct = round(-4 - (seed >> 8) % 5, 1)  # -4%~-8% 确定性区间
    
    return {
        "code": code, "name": info["name"],
        "price": info["price"],
        "risk_level": "低" if risk_score <= 25 else "中低" if risk_score <= 35 else "中",
        "suggested_pct": suggested_pct,
        "suggested_amount": round(capital * suggested_pct / 100),
        "stop_loss": round(info["price"] * (1 + stop_pct/100), 2),
        "stop_loss_pct": stop_pct,
        "data_source": "演示输出（基于标的代码的确定性规则，非真实投资建议）",
        "take_profit": round(info["price"] * (1 - stop_pct * 1.5 / 100), 2),
        "take_profit_pct": round(-stop_pct * 1.5, 1)
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--codes", default="sh600519")
    parser.add_argument("--capital", type=float, default=1000000)
    parser.add_argument("--output", choices=["json","text"], default="text")
    args = parser.parse_args()
    positions = {}
    for c in args.codes.split(","):
        c = c.strip()
        if c: positions[c] = calc(c, args.capital)
    result = {"date": datetime.now().strftime("%Y-%m-%d"), "total_capital": args.capital, "positions": positions}
    if args.output == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for code, p in positions.items():
            print(f"🛡️ {p['name']}({code}) 仓位建议")
            print(f"  风险等级: {p['risk_level']}")
            print(f"  建议仓位: {p['suggested_pct']}% ≈ ¥{p['suggested_amount']:,}")
            print(f"  止损价: ¥{p['stop_loss']} ({p['stop_loss_pct']}%)")
            print(f"  止盈价: ¥{p['take_profit']} ({p['take_profit_pct']}%)")

if __name__ == "__main__":
    main()
