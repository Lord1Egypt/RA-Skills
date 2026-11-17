# -*- coding: utf-8 -*-
"""
segments 批量筛选改善评估（矩阵级，segment_screen_eval.py）
=============================================================
按制作人指定算法，全市场矩阵级计算"每个买点对应持仓片段的收益"：
  1. cum = d['close']*d['adj_factor']（复权价 = 累计收益载体）
  2. df1 = cum.where(buy)；df2 = cum.where(sell)
  3. df3 = df2.bfill().where(buy)   # 卖点累计收益向前(过去)传递，买点处提取对应卖点
  4. seg_mult = df3/df1（=引擎 segments 权重"卖价除买价"）；seg_ret = seg_mult-1

评估目标：**入场点因子值能否筛选改善片段收益**（制作人核心诉求）——
对每个候选因子/入场前特征：
  · 取每个买点(片段)入场日的因子值 → 10 分位 → 各分位平均片段收益（等价 move_by_code X 排序）
  · 最优方向前 30% 买点的平均片段收益 vs 全局 → 改善量(pp) → 判断该特征是否值得做入场过滤器
全部矩阵级（一次 run_codes 拉 buy/sell/cum + 全部因子；无逐股循环）。

用法：python segment_screen_eval.py [N]   # N=只跑前 N 个清洗因子
"""
import sys, time, pickle
import numpy as np
import pandas as pd
from QuantAll import run_codes

PROJ = r"C:/Users/CMF/.workbuddy/skills/quantall/scripts"
XLSX = r"C:/Users/CMF/.workbuddy/skills/stock-deep-backtest/scripts/factor-screen-final-50.xlsx"

STRAT = (
    "ac=d['close']*d['adj_factor']\n"
    "ma_s=ac.rolling(5).mean()\nma_l=ac.rolling(20).mean()\n"
    "buy=(ma_s>ma_l)&(ma_s.shift(1)<=ma_l.shift(1))\n"
    "sell=(ma_s<ma_l)&(ma_s.shift(1)>=ma_l.shift(1))"
)

def main():
    only = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    t0 = time.time()

    dfx = pd.read_excel(XLSX).dropna(subset=["code"])
    if only:
        dfx = dfx.head(only)
    factors = [(r["name"], r["code"], r["IR"]) for _, r in dfx.iterrows()]
    print(f"[因子库] {len(factors)} 个，单次 run_codes 批量拉取...")

    codes = {"cum": "out=d['close']*d['adj_factor']",
             "buy": STRAT + "\nout=buy",
             "sell": STRAT + "\nout=sell"}
    for name, code, _ in factors:
        codes[name] = code
    res = run_codes(codes, PROJ)
    dfs = res["dfs"]
    miss = set(codes) - set(dfs)
    assert not miss, f"缺失 {miss} {res['error']['message']}"
    cum, buy, sell = dfs["cum"], dfs["buy"], dfs["sell"]
    print(f"[矩阵] cum={cum.shape} 拉取完成（{time.time()-t0:.1f}s）")

    # ---- 制作人算法：矩阵级买点片段收益 ----
    df1 = cum.where(buy)
    df2 = cum.where(sell)
    df3 = df2.bfill().where(buy)
    seg_mult = df3 / df1
    seg_ret = seg_mult - 1.0
    mask = buy.values & np.isfinite(seg_ret.values)
    rows_t, cols_t = np.where(mask)
    stocks = list(buy.columns)
    S = pd.DataFrame({"code": [stocks[j] for j in cols_t],
                      "entry": buy.index[rows_t],
                      "seg_mult": seg_mult.values[mask],
                      "seg_ret": seg_ret.values[mask]})
    print(f"[片段] 有效={len(S):,}（未平仓已过滤）均值={S['seg_ret'].mean()*100:.2f}% 胜率={(S['seg_ret']>0).mean()*100:.1f}%（{time.time()-t0:.1f}s）")

    # 预建 入场日→行号、股票→列号 映射（所有因子复用）
    row_idx = {t: i for i, t in enumerate(buy.index)}
    col_idx = {c: j for j, c in enumerate(buy.columns)}
    ri = np.array([row_idx[t] for t in S["entry"]], dtype=int)
    ci = np.array([col_idx[c] for c in S["code"]], dtype=int)

    # ---- 逐因子：入场日因子值 → 每日截面排名 → 分位片段收益 + 筛选改善 ----
    # ⚠️ 关键：必须用"每日截面排名"（同 entry 日内 rank）而非全局排名——
    # 全市场受大盘影响因子值全体同涨同跌，全局排名会把牛市时段整体排到高分位，
    # 导致筛选结果高度时间聚集（选的是时段不是因子）。截面排名后每日内比较，排除大盘干扰。
    rows = []
    for name, code, ir in factors:
        f = dfs[name].to_numpy(dtype=float)
        vals = f[ri, ci]
        sub = S.assign(fv=vals).dropna(subset=["fv"])
        if len(sub) < 500:
            print(f"  ⚠️ {name}: 有效样本 {len(sub)} 过少，跳过")
            continue
        # 每日截面排名（0~1）：同一买入日内比较，排除大盘整体水平干扰
        sub["r"] = sub.groupby("entry")["fv"].rank(pct=True)
        # 分位（基于截面排名）
        sub["q"] = pd.qcut(sub["r"], 10, labels=False, duplicates="drop")
        g = sub.groupby("q")["seg_ret"].mean()
        if len(g) < 5:
            continue
        spread = g.iloc[-1] - g.iloc[0]
        global_mean = sub["seg_ret"].mean()
        if spread > 0:
            best = sub[sub["q"] >= 7]["seg_ret"].mean()
        else:
            best = sub[sub["q"] <= 2]["seg_ret"].mean()
        improve = best - global_mean
        trend = "升" if spread > 0 else "降"
        agree = (ir > 0) == (spread > 0)
        # ---- 时间分布诊断：最优方向前30%买点 vs 全样本 的季度分布 ----
        best_mask = sub["q"] >= 7 if spread > 0 else sub["q"] <= 2
        tq_all = sub.assign(qt=sub["entry"].dt.to_period("Q")).groupby("qt").size()
        tq_sel = sub.assign(qt=sub["entry"].dt.to_period("Q")).loc[best_mask].groupby("qt").size()
        share = (tq_sel / tq_all).mean()  # 各季度筛选占比均值（≈0.3 为均匀，偏离=时间聚集）
        share_max = (tq_sel / tq_all).max()
        share_min = (tq_sel / tq_all).min()
        rows.append({"name": name, "IR": ir,
                     "global": global_mean, "best30": best, "improve": improve,
                     "spread": spread, "trend": trend, "agree": agree, "n": len(sub),
                     "time_share_mean": share, "time_share_max": share_max, "time_share_min": share_min,
                     "curve": " ".join(f"{v*100:+.1f}" for v in g)})
    R = pd.DataFrame(rows).sort_values("improve", key=lambda s: s.abs(), ascending=False)


    # ---- 输出 ----
    print(f"\n{'='*110}\n[入场因子筛选改善评估·每日截面排名版]  {len(R)} 个因子（总耗时 {time.time()-t0:.1f}s）")
    print(f"方向与因子库 IR 一致 {int(R['agree'].sum())}/{len(R)}（{R['agree'].mean()*100:.0f}%）")
    print(f"全局平均片段收益 = {S['seg_ret'].mean()*100:.2f}%")
    print(f"时间分布列: 均值=各季度筛选占比均值(≈0.3均匀)  最大=单季筛选占比(>0.6=时间聚集⚠️)")
    print(f"\n{'因子':<16}{'IR':>7}{'全局%':>8}{'最优30%%':>9}{'改善pp':>8}{'首尾差pp':>9}{'方向':>4}{'一致':>4}{'时间均值':>8}{'时间最大':>8}{'n':>8}")
    print("-" * 110)
    for _, r in R.iterrows():
        flag_t = "⚠️聚集" if r["time_share_max"] > 0.6 else ""
        print(f"{r['name']:<16}{r['IR']:>7.2f}{r['global']*100:>8.2f}{r['best30']*100:>9.2f}"
              f"{r['improve']*100:>8.2f}{r['spread']*100:>9.2f}{r['trend']:>4}{'✅' if r['agree'] else '⚠️':>4}"
              f"{r['time_share_mean']*100:>7.1f}%{r['time_share_max']*100:>7.1f}%{flag_t:>8}{int(r['n']):>8,}")

    print(f"\n[筛选改善收益 Top10（最优方向前 30% 买点 vs 全局）]")
    print(R.head(10)[["name", "IR", "global", "best30", "improve", "trend"]].round(4).to_string(index=False))

    out = r"C:/Users/CMF/.workbuddy/skills/stock-deep-backtest/scripts/segment_screen_eval_result.csv"
    R.to_csv(out, index=False, encoding="utf-8-sig")
    with open(r"C:/Users/CMF/.workbuddy/skills/stock-deep-backtest/scripts/segment_matrix.pkl", "wb") as f:
        pickle.dump({"cum": cum, "buy": buy, "sell": sell, "seg_mult": seg_mult,
                     "seg_ret": seg_ret, "S": S}, f)
    print(f"\n[已存] {out} + segment_matrix.pkl   总耗时 {time.time()-t0:.1f}s")
    print("[DONE]")

if __name__ == "__main__":
    main()
