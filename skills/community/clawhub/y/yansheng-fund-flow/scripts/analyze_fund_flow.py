#!/usr/bin/env python3
"""研声 · 资金流向分析脚本"""
import json, sys, argparse, hashlib
from datetime import datetime

def analyze_flow(codes):
    code_list = [c.strip() for c in codes.split(",")] if codes else []
    # 确定性演示数据：基于标的代码hash生成固定数值（可复现，非随机），明确标注为示例数据
    seed = int(hashlib.md5(",".join(code_list).encode("utf-8")).hexdigest(), 16)
    main_in = round(50 + seed % 150, 1)
    main_out = round(-150 + (seed >> 8) % 120, 1)
    sh_net = round(-10 + (seed >> 16) % 40, 1)
    sz_net = round(-5 + (seed >> 24) % 30, 1)
    result = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "data_source": "演示数据（基于标的代码的确定性规则生成，非真实市场资金流；仅供教学演示）",
        "market_total": {"main_inflow": main_in, "main_outflow": main_out},
        "north_flow": {"sh_net": sh_net, "sz_net": sz_net},
        "stocks": {}
    }
    result["market_total"]["net"] = round(result["market_total"]["main_inflow"] + result["market_total"]["main_outflow"], 1)
    result["north_flow"]["total_net"] = round(result["north_flow"]["sh_net"] + result["north_flow"]["sz_net"], 1)
    result["market_total"]["unit"] = "亿元"
    result["north_flow"]["unit"] = "亿元"
    for i, code in enumerate(code_list):
        v = (seed >> (i * 6)) % 100
        result["stocks"][code] = {
            "main_net": round((v % 16) - 5, 2),
            "main_signal": "主力净流入" if v % 10 > 4 else "主力净流出",
            "north_position": "增持" if (v >> 2) % 10 > 4 else "减持"
        }
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--codes", default="sh600519")
    parser.add_argument("--output", choices=["json","text"], default="text")
    args = parser.parse_args()
    result = analyze_flow(args.codes)
    if args.output == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        mt = result["market_total"]
        nf = result["north_flow"]
        print(f"💰 资金流向分析 ({result['date']}) — ⚠️ 演示数据，非真实市场资金流")
        print(f"主力资金: 净{mt['net']:.1f}亿元 (流入{mt['main_inflow']:.1f} / 流出{abs(mt['main_outflow']):.1f})")
        print(f"北向资金: 净{nf['total_net']:.1f}亿元 (沪{nf['sh_net']:.1f} / 深{nf['sz_net']:.1f})")
        print("⚠️ 以上数值为教学演示数据，不代表真实市场资金动向")

if __name__ == "__main__":
    main()
