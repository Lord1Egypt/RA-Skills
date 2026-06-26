#!/usr/bin/env python3
"""
股智Alpha - 全市场扫描选股（Agent Skill 入口）

用法:
  python scripts/run_screener.py --top-n 20
  python scripts/run_screener.py --top-n 10 --codes 600036,000001,000333

输出: 终端表格 + .temp_screener_output.json
"""

import sys, os, time, argparse, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import numpy as np
from datetime import date

from src.collectors.ashare_collector import AshareCollector
from src.collectors.fund_flow_collector import FundFlowCollector
from src.screener.scoring_engine import ScoringEngine
from src.collectors.technical import add_technical_indicators


from src.stock_list import get_pool, get_name_map

# 名称映射
_STOCK_NAMES = get_name_map()

def get_stock_name(code):
    return _STOCK_NAMES.get(code, code)


def main():
    parser = argparse.ArgumentParser(description="股智Alpha - 全市场扫描")
    parser.add_argument("--top-n", type=int, default=20, help="输出数量")
    parser.add_argument("--codes", type=str, default=None, help="股票代码列表，逗号分隔")
    parser.add_argument("--no-flow", action="store_true", help="跳过资金流")
    parser.add_argument("--full-scan", action="store_true", help="全市场扫描(5466只，约5-10分钟)")
    args = parser.parse_args()

    # === Phase 0: 全量扫描 or 核心池 ===
    if args.full_scan:
        print("[DATA] 全市场快速扫描模式...", flush=True)
        from src.quick_scan import quick_scan
        quick_result = quick_scan(min_price=3.0, min_volume=5e5)
        if len(quick_result) == 0:
            print("[FAIL] 全量扫描无结果，回退到核心池")
            codes = get_pool(core_only=True)
        else:
            # 取Top 200做深度分析
            top_candidates = quick_result.head(200)["code"].tolist()
            print(f"[OK] 快速筛选完成: 取Top{len(top_candidates)}做深度分析")
            codes = top_candidates
    else:
        codes = args.codes.split(",") if args.codes else get_pool(core_only=True)

    if not codes:
        print("[FAIL] 无有效股票代码")
        return
    top_n = args.top_n

    print(f"[DATA] 正在采集 {len(codes)} 只股票行情数据...", flush=True)

    # === Phase 1: 行情 ===
    ac = AshareCollector()
    price_records = []
    failed_codes = []
    t0 = time.time()

    for i, code in enumerate(codes):
        df = ac.get_daily_hist(code, count=60)
        if df is not None and len(df) > 0:
            df["stock_code"] = code
            price_records.append(df)
        else:
            failed_codes.append(code)
        if (i + 1) % 20 == 0:
            print(f"  >> 行情 {i+1}/{len(codes)} ({time.time()-t0:.0f}s)", flush=True)

    if not price_records:
        print("[FAIL] 行情数据采集失败，请检查网络连接")
        return

    full_df = pd.concat(price_records, ignore_index=True)
    print(f"[OK] 行情: {len(full_df)} 行, {len(price_records)} 只股票")
    if failed_codes:
        print(f"[WARN] {len(failed_codes)} 只获取失败: {failed_codes[:5]}...")

    # === Phase 2: 技术指标 ===
    tech_df = add_technical_indicators(full_df)
    print("[OK] 技术指标计算完成")

    # === Phase 3: 资金流 ===
    flow_df = pd.DataFrame()
    if not args.no_flow:
        print("[DATA] 估算资金流(基于价量关系)...", flush=True)
        fc = FundFlowCollector()
        flow_df = fc.batch_fund_flow(codes, price_df=tech_df)
        if len(flow_df) > 0:
            n_stocks = len(flow_df["stock_code"].unique())
            print(f"[OK] 资金流: {len(flow_df)} 行 ({n_stocks} 只) — 价量估算")
        else:
            print("[WARN] 资金流估算失败，仅用技术面评分")
    else:
        print("[WARN] 资金流已跳过，仅用技术面评分")

    # === Phase 4: 评分 ===
    se = ScoringEngine()
    candidates = pd.DataFrame({"stock_code": codes})
    flow_input = flow_df if len(flow_df) > 0 else None
    scored = se.score(candidates, tech_df, flow_input)

    # 处理缺失维度
    missing = se.get_missing_dims()
    if flow_input is None or len(flow_input) == 0:
        missing.append("资金流(无数据)")

    # === Phase 5: 股票名称 ===
    scored["name"] = scored["stock_code"].apply(get_stock_name)

    # === Phase 6: 输出 ===
    top = scored.head(top_n)

    sep = "=" * 60
    print(f"\n{sep}")
    print(f"  股智Alpha - 精选股票池")
    print(f"  扫描日期: {date.today()}")
    print(f"  股票池: {len(codes)} 只 | 有效评分: {len(scored)} 只")
    if missing:
        print(f"  [WARN] 缺失维度: {', '.join(missing)}")
    print(sep)

    print(f"{'代码':>8} {'名称':<8} {'综评':>5} {'行为':>5} {'技术':>5} {'资金':>5} {'动量':>5} {'风险':>5} {'量能':>5}")
    print(f"{'-'*8} {'-'*8} {'-'*5} {'-'*5} {'-'*5} {'-'*5} {'-'*5} {'-'*5} {'-'*5}")

    for _, row in top.iterrows():
        code = row["stock_code"]
        name = row.get("name", code)[:6]
        total = f"{row['score_total']:.2f}" if pd.notna(row.get("score_total")) else "N/A"
        def fmt(col):
            v = row.get(col)
            return f"{v:.2f}" if pd.notna(v) else "N/A"
        print(f"{code:>8} {name:<8} {total:>5} {fmt('score_behavior')} {fmt('score_technical')} {fmt('score_fund_flow')} {fmt('score_momentum')} {fmt('score_risk')} {fmt('score_volume')}")

    print(f"\n{sep}")
    print("  [WARN] 免责声明：仅供参考，不构成投资建议。")
    print(f"{sep}")

    # === JSON 输出供 Agent 使用 ===
    top_json = []
    for _, row in top.iterrows():
        def sv(col):
            v = row.get(col)
            return round(float(v), 4) if pd.notna(v) else 0
        top_json.append({
            "code": row["stock_code"],
            "name": row.get("name", ""),
            "total_score": sv("score_total"),
            "behavior": sv("score_behavior"),
            "technical": sv("score_technical"),
            "fund_flow": sv("score_fund_flow"),
            "momentum": sv("score_momentum"),
            "risk": sv("score_risk"),
            "volume": sv("score_volume"),
        })

    out_path = os.path.join(os.path.dirname(__file__), "..", ".temp_screener_output.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"top": top_json, "missing_dims": missing, "date": str(date.today())}, f, ensure_ascii=False)
    print(f"\n[JSON] 结果已保存到 {out_path}")


if __name__ == "__main__":
    main()
