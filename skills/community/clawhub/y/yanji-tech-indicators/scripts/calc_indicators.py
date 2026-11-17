#!/usr/bin/env python3
"""研技 · 技术指标计算脚本"""
import json, sys, argparse
from datetime import datetime

STOCK_MAP = {
    "sh600519": {"name": "贵州茅台"}, "sz300750": {"name": "宁德时代"},
    "sz000858": {"name": "五粮液"}, "sh601318": {"name": "中国平安"},
    "sz300059": {"name": "东方财富"}, "sh600036": {"name": "招商银行"},
}

def calc_indicators(code):
    info = STOCK_MAP.get(code, {"name": code})
    price = 100.0  # 演示基准价（非真实行情）
    result = {
        "data_source": "演示数据（固定基准价计算，非真实行情；仅供教学演示）",
        "code": code,
        "name": info["name"],
        "date": datetime.now().strftime("%Y-%m-%d"),
        "indicators": {
            "macd": {"dif": round(price * 0.02, 2), "dea": round(price * 0.015, 2),
                     "hist": round(price * 0.005, 2), "signal": "金叉运行中"},
            "rsi": {"rsi6": 58.5, "rsi12": 52.3, "rsi24": 48.0, "signal": "中性偏强"},
            "kdj": {"k": 65.2, "d": 60.8, "j": 74.0, "signal": "偏多"},
            "boll": {"mid": round(price, 2), "upper": round(price * 1.08, 2),
                     "lower": round(price * 0.92, 2), "position": "中轨上方"},
            "ma_signal": "多头排列（MA5>MA10>MA20>MA60）",
            "volume_signal": "量价配合良好"
        },
        "support_resistance": {
            "support": [round(price * 0.95, 2), round(price * 0.90, 2), round(price * 0.85, 2)],
            "resistance": [round(price * 1.05, 2), round(price * 1.10, 2), round(price * 1.15, 2)]
        }
    }
    return result

def main():
    parser = argparse.ArgumentParser(description="技术指标计算")
    parser.add_argument("--code", default="sh600519")
    parser.add_argument("--indicators", default="macd,rsi,kdj,boll")
    parser.add_argument("--output", choices=["json","text"], default="text")
    args = parser.parse_args()
    
    result = calc_indicators(args.code)
    
    if args.output == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        ind = result["indicators"]
        sr = result["support_resistance"]
        print(f"📈 {result['name']}({result['code']}) 技术指标分析")
        print(f"MACD: {ind['macd']['signal']} (DIF={ind['macd']['dif']})")
        print(f"RSI: {ind['rsi']['signal']} (RSI6={ind['rsi']['rsi6']})")
        print(f"KDJ: {ind['kdj']['signal']} (K={ind['kdj']['k']})")
        print(f"布林带: {ind['boll']['position']}")
        print(f"均线: {ind['ma_signal']}")
        print(f"量价: {ind['volume_signal']}")
        print(f"支撑位: {sr['support']}")
        print(f"压力位: {sr['resistance']}")

if __name__ == "__main__":
    main()
