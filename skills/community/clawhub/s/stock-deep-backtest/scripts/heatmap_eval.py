# -*- coding: utf-8 -*-
"""
热力图统计评估（heatmap_eval.py）
=================================
绘图（move_by_code / group_by_code）完成后获得热力图统计（各分位的加权收益）。
本脚本对热力图数据做**分布感知评估**——⚠️ 评估对象是股市收益，高度偏态/长尾
（均值被少数极端片段拉高、中位常为负），不能只看加权均值：

对"筛选区域（如组合排序值高分位前 30%）vs 全局"评估：
  1. 均值提升 + 中位数提升 + 胜率提升（pp / %）
  2. 截尾敏感性：去 1%/99% 极端后提升是否仍在（>50% 保留 = 稳健）
  3. 时间分布：筛选买点的季度占比（均值≈0.3 均匀 / 最大>0.6 聚集⚠️）
  4. 显著性：bootstrap 1000 次提升的 95% 置信区间

用法：python heatmap_eval.py [K]   # K=高分位前 K 档作为筛选区（默认 3=前30%）
"""
import sys, time
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

# 5 因子组合（与 GUI 绘图同一组合：GTJA_Alpha74∩Alpha179∩Alpha70∩Alpha#44∩Alpha64）
COMBO_CODE = (
    "lo = d['low'] * d['adj_factor']; vwap = d['amount'] / d['vol'].replace(0, np.nan)\n"
    "sum_price20 = (lo * 0.35 + vwap * 0.65).rolling(20).sum()\n"
    "sum_meanvol20 = d['vol'].rolling(40).mean().rolling(20).sum()\n"
    "r74 = row_rank(sum_price20.rolling(7).corr(sum_meanvol20)) + row_rank(row_rank(vwap).rolling(6).corr(row_rank(d['vol'])))\n"
    "r74 = 1 - row_rank(r74)\n"
    "r179 = row_rank(vwap.rolling(4).corr(d['vol'])) * row_rank(row_rank(lo).rolling(12).corr(row_rank(d['vol'].rolling(50).mean())))\n"
    "r179 = 1 - row_rank(r179)\n"
    "r70 = 1 - row_rank(d['amount'].rolling(6).std())\n"
    "r44 = row_rank(-1 * (d['high'] * d['adj_factor']).rolling(5).corr(row_rank(d['vol'])))\n"
    "ac = d['close'] * d['adj_factor']; vwap2 = d['amount'] / d['vol'].replace(0, np.nan)\n"
    "corr1 = row_rank(vwap2).rolling(4).corr(row_rank(d['vol']))\n"
    "rank1 = row_rank(rolling_decay_linear(corr1, 4))\n"
    "corr2 = row_rank(ac).rolling(4).corr(row_rank(d['vol'].rolling(60).mean()))\n"
    "rank2 = row_rank(rolling_decay_linear(corr2.rolling(13).max(), 14))\n"
    "r64 = row_rank(-1 * np.maximum(rank1, rank2))\n"
    "combo = (r74 + r179 + r70 + r44 + r64) / 5\n"
    "out = row_rank(combo)"
)

def desc(s, label):
    """分布画像：均值/中位/胜率/截尾均值/分位数"""
    s = s.dropna()
    if len(s) == 0:
        return f"{label}: 空"
    lo, hi = np.nanpercentile(s, [1, 99])
    trim = s.clip(lo, hi)
    return (f"{label}: n={len(s):,} 均值={s.mean()*100:+.2f}% 中位={s.median()*100:+.2f}% "
            f"胜率={(s>0).mean()*100:.1f}% 截尾均值={trim.mean()*100:+.2f}% "
            f"p5={s.quantile(.05)*100:+.1f} p95={s.quantile(.95)*100:+.1f}")

def main():
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    t0 = time.time()
    codes = {"cum": "out=d['close']*d['adj_factor']",
             "buy": STRAT + "\nout=buy",
             "sell": STRAT + "\nout=sell",
             "combo": COMBO_CODE}
    res = run_codes(codes, PROJ)
    dfs = res["dfs"]
    assert set(codes) <= set(dfs), f"缺失 {set(codes)-set(dfs)}"
    cum, buy, sell, combo = dfs["cum"], dfs["buy"], dfs["sell"], dfs["combo"]

    # ---- 制作人矩阵算法：买点片段收益 ----
    df1 = cum.where(buy); df2 = cum.where(sell)
    df3 = df2.bfill().where(buy)
    seg_ret = df3 / df1 - 1.0
    mask = buy.values & np.isfinite(seg_ret.values)
    rows_t, cols_t = np.where(mask)
    stocks = list(buy.columns)
    S = pd.DataFrame({"code": [stocks[j] for j in cols_t],
                      "entry": buy.index[rows_t],
                      "seg_ret": seg_ret.values[mask]})
    # 入场日组合排序值
    row_idx = {t: i for i, t in enumerate(buy.index)}
    col_idx = {c: j for j, c in enumerate(buy.columns)}
    ri = np.array([row_idx[t] for t in S["entry"]], dtype=int)
    ci = np.array([col_idx[c] for c in S["code"]], dtype=int)
    cv = combo.to_numpy(dtype=float)[ri, ci]
    S["combo"] = cv
    S = S.dropna(subset=["combo"])
    S["quarter"] = S["entry"].dt.to_period("Q").astype(str)

    GLOBAL = S["seg_ret"]
    print(f"========== 热力图统计评估（组合排序值 × 片段收益） ==========")
    print(f"有效片段={len(S):,}  全局分布画像:")
    print("  " + desc(GLOBAL, "全局"))

    # ---- 1. 10 分位分布画像（等价热力图 Y 轴 10 档） ----
    print(f"\n[1. 组合排序值 10 分位 → 片段收益分布画像]")
    S["q"] = pd.qcut(S["combo"], 10, labels=False, duplicates="drop")
    for q in range(10):
        sub = S[S["q"] == q]
        print("  " + desc(sub["seg_ret"], f"q{q}"))

    # ---- 2. 筛选区域（高分位前 K 档 = 前 10K%）vs 全局 ----
    print(f"\n[2. 筛选评估：组合排序值前 {K*10}%（q>={10-K}）vs 全局]")
    sel = S[S["q"] >= (10 - K)]
    g, s = GLOBAL, sel["seg_ret"]
    # 均值/中位/胜率提升
    imp_mean = s.mean() - g.mean()
    imp_med = s.median() - g.median()
    imp_win = (s > 0).mean() - (g > 0).mean()
    print(f"  均值提升: {imp_mean*100:+.2f}pp   中位提升: {imp_med*100:+.2f}pp   胜率提升: {imp_win*100:+.1f}pp")
    # 截尾敏感性
    lo, hi = np.nanpercentile(g, [1, 99])
    g_t = g.clip(lo, hi); s_t = s.clip(lo, hi)
    imp_t = s_t.mean() - g_t.mean()
    keep = imp_t / imp_mean * 100 if imp_mean != 0 else 0
    print(f"  截尾后均值提升: {imp_t*100:+.2f}pp（保留 {keep:.0f}%{' ✅ 稳健' if keep>50 else ' ⚠️ 依赖极端值'}）")
    # 时间分布
    tq_all = S.groupby("quarter").size()
    tq_sel = sel.groupby("quarter").size()
    share = (tq_sel / tq_all.reindex(tq_sel.index))
    print(f"  时间分布: 各季筛选占比均值 {share.mean()*100:.1f}%（≈{K*10}% 均匀）  最大 {share.max()*100:.1f}%{' ⚠️ 聚集' if share.max()>0.6 else ' ✅ 均匀'}")
    # 胜率
    print(f"  筛选区胜率 {(s>0).mean()*100:.1f}% vs 全局 {(g>0).mean()*100:.1f}%")

    # ---- 3. 显著性（bootstrap） ----
    print(f"\n[3. 显著性检验（bootstrap 1000 次）]")
    rng = np.random.default_rng(42)
    diffs = []
    n_s = len(s)
    for _ in range(1000):
        boot_s = rng.choice(s.values, n_s, replace=True)
        boot_g = rng.choice(g.values, n_s, replace=True)
        diffs.append(boot_s.mean() - boot_g.mean())
    d = np.array(diffs)
    ci = np.percentile(d, [2.5, 97.5])
    print(f"  提升 95% CI: [{ci[0]*100:+.2f}pp, {ci[1]*100:+.2f}pp]"
          f"{'  ✅ 显著>0' if ci[0] > 0 else '  ⚠️ CI 含 0/负，不显著'}")

    # ---- 4. 极端片段影响 ----
    print(f"\n[4. 极端片段影响]")
    top1 = s.nlargest(max(1, int(len(s)*0.01)))
    print(f"  筛选区头部1% 收益 {top1.mean()*100:+.1f}%（剔除后均值 {s.drop(top1.index).mean()*100:+.2f}%）")

    print(f"\n[DONE] 热力图评估完成  耗时 {time.time()-t0:.1f}s")

if __name__ == "__main__":
    main()
