# -*- coding: utf-8 -*-
"""
双因子/多因子组合筛选改善评估（segment_combo_eval.py）
=====================================================
基于制作人矩阵算法（cum.where(buy/sell) + bfill → 买点片段收益）与单因子筛选
改善评估（segment_screen_eval.py），进一步做**组合筛选**：

组合逻辑（两步：先筛选、再融合）：
  1. 单因子最优方向前 30% 买点子集（IR>0 → 高分位 q7-9；IR<0 → 低分位 q0-2）
  2. **双因子 intersect**：因子A∩因子B 各自最优方向前 30% 的交集 → 片段收益 vs 全局 vs 单因子
  3. **双因子 rank 融合**：两因子 row_rank 后按方向调整（IR<0 → 1-rank）取平均 → 10 分位 → 前 30% 买点
  4. **多因子逐步叠加**：在最优组合基础上逐个追加因子（贪心），报告累计改善

输出：双因子组合 TopN（intersect 与 rank 融合对比）+ 多因子贪心叠加曲线。
全部矩阵级（一次 run_codes 拉 buy/sell/cum + 全部因子）。

用法：python segment_combo_eval.py [K]   # K=取单因子改善 TopK 做组合（默认 8）
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

def main():
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    t0 = time.time()

    dfx = pd.read_excel(XLSX).dropna(subset=["code"])
    factors = [(r["name"], r["code"], r["IR"]) for _, r in dfx.iterrows()]
    print(f"[因子库] {len(factors)} 个，单次 run_codes 批量拉取...")

    codes = {"cum": "out=d['close']*d['adj_factor']",
             "buy": STRAT + "\nout=buy",
             "sell": STRAT + "\nout=sell"}
    for name, code, _ in factors:
        codes[name] = code
    res = run_codes(codes, PROJ)
    dfs = res["dfs"]
    assert set(codes) <= set(dfs), f"缺失 {set(codes)-set(dfs)}"
    cum, buy, sell = dfs["cum"], dfs["buy"], dfs["sell"]

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
    GLOBAL = S["seg_ret"].mean()
    print(f"[片段] 有效={len(S):,} 全局均值={GLOBAL*100:.2f}%（{time.time()-t0:.1f}s）")

    # 入场日→行/列 映射
    row_idx = {t: i for i, t in enumerate(buy.index)}
    col_idx = {c: j for j, c in enumerate(buy.columns)}
    ri = np.array([row_idx[t] for t in S["entry"]], dtype=int)
    ci = np.array([col_idx[c] for c in S["code"]], dtype=int)

    # ---- 1. 单因子筛选改善（top 排序）· 每日截面排名 ----
    single = {}
    for name, code, ir in factors:
        f = dfs[name].to_numpy(dtype=float)[ri, ci]
        sub = S.assign(fv=f).dropna(subset=["fv"])
        if len(sub) < 500:
            continue
        sub["r"] = sub.groupby("entry")["fv"].rank(pct=True)   # ⚠️ 每日截面排名，排除大盘干扰
        if ir > 0:
            best_mask = sub["r"] >= 0.7
        else:
            best_mask = sub["r"] <= 0.3
        imp = sub.loc[best_mask, "seg_ret"].mean() - GLOBAL
        single[name] = {"ir": ir, "imp": imp, "sub": sub, "best": best_mask}

    # 单因子按正改善排序（排除负改善因子，贪心起点必须是有效正改善）
    top = sorted([(n, d) for n, d in single.items() if d["imp"] > 0],
                 key=lambda kv: kv[1]["imp"], reverse=True)[:K]
    # 把每个因子的 best 掩码对齐到 S 的索引（sub 是 S 的子集，用 reindex）
    for name, d in single.items():
        d["best"] = d["best"].reindex(S.index, fill_value=False)
    print(f"\n[单因子 Top{K}]（全局 {GLOBAL*100:.2f}%，按正改善排序）")
    for name, d in top:
        print(f"  {name:<18} IR={d['ir']:+.2f}  改善={d['imp']*100:+.2f}pp")

    # ---- 2. 双因子 intersect（各自最优方向前 30% 交集） ----
    print(f"\n[双因子 intersect Top15]（{K}×{K} 组合）")
    pairs = []
    for i in range(len(top)):
        for j in range(i + 1, len(top)):
            na, da = top[i]; nb, db = top[j]
            both = da["best"] & db["best"]
            n_sel = int(both.sum())
            if n_sel < 200:
                continue
            imp = S.loc[both, "seg_ret"].mean() - GLOBAL
            # 相对各自单因子提升
            imp_a = S.loc[both, "seg_ret"].mean() - S.loc[da["best"], "seg_ret"].mean()
            pairs.append((na, nb, imp, imp_a, n_sel))
    pairs.sort(key=lambda x: abs(x[2]), reverse=True)
    for na, nb, imp, imp_a, n in pairs[:15]:
        print(f"  {na:<16}∩{nb:<16} 改善={imp*100:+.2f}pp (较单因子{imp_a*100:+.2f}) n={n:,}")

    # ---- 3. 双因子 rank 融合（方向调整后平均排名） ----
    print(f"\n[双因子 rank 融合 Top15]")
    fus = []
    for i in range(len(top)):
        for j in range(i + 1, len(top)):
            na, da = top[i]; nb, db = top[j]
            # sub 是 S 子集，先对齐回 S 索引
            ra = da["sub"]["r"].reindex(S.index)
            rb = db["sub"]["r"].reindex(S.index)
            ra = ra if da["ir"] > 0 else 1 - ra
            rb = rb if db["ir"] > 0 else 1 - rb
            combo = (ra + rb) / 2
            m = combo.notna()
            if int(m.sum()) < 200:
                continue
            thr = combo[m].quantile(0.7)
            best_mask = (combo >= thr) & m
            imp = S.loc[best_mask, "seg_ret"].mean() - GLOBAL
            fus.append((na, nb, imp, int(best_mask.sum())))
    fus.sort(key=lambda x: abs(x[2]), reverse=True)
    for na, nb, imp, n in fus[:15]:
        print(f"  {na:<16}+{nb:<16} 改善={imp*100:+.2f}pp n={n:,}")

    # ---- 4. 多因子贪心叠加（从最优单因子起逐个加，取交集/融合最优） ----
    print(f"\n[多因子贪心叠加]（基于 rank 融合，逐步追加）")
    chosen = [top[0][0]]
    cur_imp = top[0][1]["imp"]
    for step in range(1, min(5, len(top))):
        best_next, best_imp = None, cur_imp
        for name, d in top:
            if name in chosen:
                continue
            # 与已选组合求交集（方向调整后各自前 30% 再交，与单因子筛选同阈值）
            combo_mask = pd.Series(True, index=S.index)
            for c in chosen + [name]:
                cd = single[c]
                rk = cd["sub"]["r"].reindex(S.index)
                rk = rk if cd["ir"] > 0 else 1 - rk
                combo_mask &= (rk >= rk.quantile(0.7))
            n_sel = int(combo_mask.sum())
            if n_sel < 200:
                continue
            imp = S.loc[combo_mask, "seg_ret"].mean() - GLOBAL
            if imp > best_imp:
                best_next, best_imp = name, imp
        if best_next is None:
            break
        chosen.append(best_next)
        cur_imp = best_imp
        print(f"  第{step+1}步 +{best_next:<16} 累计改善={best_imp*100:+.2f}pp")

    print(f"\n[最终组合] {' ∩ '.join(chosen)}")
    print(f"[已存] scripts/segment_combo_eval_result.csv")
    out = r"C:/Users/CMF/.workbuddy/skills/stock-deep-backtest/scripts/segment_combo_eval_result.csv"
    pd.DataFrame(pairs, columns=["fA", "fB", "improve", "vs_single", "n"]).to_csv(
        out, index=False, encoding="utf-8-sig")
    print(f"  总耗时 {time.time()-t0:.1f}s")
    print("[DONE]")

if __name__ == "__main__":
    main()
