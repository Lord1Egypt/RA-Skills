#!/usr/bin/env python3
"""研盾 · 风险评估脚本"""
import json, sys, argparse, hashlib
from datetime import datetime

STOCK_MAP = {
    "sh600519": {"name": "贵州茅台"}, "sz300750": {"name": "宁德时代"},
    "sz000858": {"name": "五粮液"}, "sh601318": {"name": "中国平安"},
}

def assess(code):
    info = STOCK_MAP.get(code, {"name": code})
    dims = ["fundamental", "technical", "sentiment", "liquidity", "tail"]
    dim_names = {"fundamental":"基本面", "technical":"技术面", "sentiment":"舆情", "liquidity":"流动性", "tail":"尾部"}
    dim_risks = {"fundamental":"消费复苏节奏", "technical":"短期涨幅", "sentiment":"无明显负面", "liquidity":"成交活跃", "tail":"政策不确定性"}
    
    # 确定性演示评分：基于标的代码hash生成固定分数（同一标的结果可复现，非随机）
    seed = int(hashlib.md5(code.encode("utf-8")).hexdigest(), 16)
    scores = {}
    for i, d in enumerate(dims):
        scores[d] = 15 + (seed >> (i * 4)) % 46  # 15-60 确定性区间
    overall = round(sum(scores.values()) / len(scores))
    level = "低" if overall <= 25 else "中低" if overall <= 35 else "中" if overall <= 45 else "中高" if overall <= 55 else "高"
    
    return {
        "code": code, "name": info["name"], "date": datetime.now().strftime("%Y-%m-%d"),
        "overall_risk": level, "overall_score": overall,
        "data_source": "演示评分（基于标的代码的确定性规则，非真实风控结论）",
        "dimensions": {d: {"score": s, "level": "低" if s<=25 else "中低" if s<=35 else "中" if s<=45 else "中高" if s<=55 else "高",
                           "key_risk": dim_risks.get(d, "")} for d, s in zip(dims, scores.values())}
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--codes", default="sh600519")
    parser.add_argument("--output", choices=["json","text"], default="text")
    args = parser.parse_args()
    results = {}
    for c in args.codes.split(","):
        c = c.strip()
        if c: results[c] = assess(c)
    if args.output == "json":
        print(json.dumps({"date": datetime.now().strftime("%Y-%m-%d"), "assessments": results}, ensure_ascii=False, indent=2))
    else:
        for code, r in results.items():
            print(f"🛡️ {r['name']}({code}) 风险评估")
            print(f"  综合风险: {r['overall_risk']} (评分: {r['overall_score']})")
            for d, v in r['dimensions'].items():
                print(f"  {'基本面' if d=='fundamental' else '技术面' if d=='technical' else '舆情' if d=='sentiment' else '流动性' if d=='liquidity' else '尾部'}: {v['level']} - {v['key_risk']}")

if __name__ == "__main__":
    main()
