# -*- coding: utf-8 -*-
"""
一键完整分析流程（run_full_attribution.py）
============================================
串行执行回测归因完整链路，输出结构化 JSON 供 HTML 报告渲染：
  ① 矩阵级片段收益（制作人算法：cum.where(buy/sell)+bfill）
  ② 单因子筛选改善（**每日截面排名** + **全局排名** 双口径对比 + 时间分布）
  ③ 双因子 intersect Top
  ④ 多因子贪心叠加（正改善起点）
  ⑤ 汇总结论

输出：scripts/full_attribution_result.json（供 HTML 使用）
"""
import sys, time, json
import numpy as np
import pandas as pd
from QuantAll import run_codes

PROJ = r"C:/Users/CMF/.workbuddy/skills/quantall/scripts"
XLSX = r"C:/Users/CMF/.workbuddy/skills/stock-deep-backtest/scripts/factor-screen-final-50.xlsx"
OUT = r"C:/Users/CMF/.workbuddy/skills/stock-deep-backtest/scripts/full_attribution_result.json"

# 可切换策略（第 1 个参数）：golden_cross / reversal / macd 等
STRATEGIES = {
    "golden_cross": {
        "label": "均线金叉 MA(5,20) 全市场",
        "strategy": (
            "ac=d['close']*d['adj_factor']\n"
            "ma_s=ac.rolling(5).mean()\nma_l=ac.rolling(20).mean()\n"
            "buy=(ma_s>ma_l)&(ma_s.shift(1)<=ma_l.shift(1))\n"
            "sell=(ma_s<ma_l)&(ma_s.shift(1)>=ma_l.shift(1))"
        ),
    },
    "reversal": {
        "label": "均值回归反转（20日跌15%买入，回0卖出）",
        "strategy": (
            "ac=d['close']*d['adj_factor']\n"
            "r20=ac.pct_change(20)\n"
            "buy=(r20<=-0.15)&(r20.shift(1)>-0.15)\n"
            "sell=(r20>=0)&(r20.shift(1)<0)"
        ),
    },
    "macd": {
        "label": "MACD 金叉（DIF上穿DEA买入，下穿卖出）",
        "strategy": (
            "ac=d['close']*d['adj_factor']\n"
            "ema12=ac.ewm(span=12,adjust=False).mean()\n"
            "ema26=ac.ewm(span=26,adjust=False).mean()\n"
            "dif=ema12-ema26\n"
            "dea=dif.ewm(span=9,adjust=False).mean()\n"
            "buy=(dif>dea)&(dif.shift(1)<=dea.shift(1))\n"
            "sell=(dif<dea)&(dif.shift(1)>=dea.shift(1))"
        ),
    },
}

def main():
    strat_key = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in STRATEGIES else "golden_cross"
    CFG = STRATEGIES[strat_key]
    STRAT = CFG["strategy"]
    t0 = time.time()
    dfx = pd.read_excel(XLSX).dropna(subset=["code"])
    factors = [(r["name"], r["code"], r["IR"]) for _, r in dfx.iterrows()]

    codes = {"cum": "out=d['close']*d['adj_factor']",
             "buy": STRAT + "\nout=buy",
             "sell": STRAT + "\nout=sell"}
    for name, code, _ in factors:
        codes[name] = code
    res = run_codes(codes, PROJ)
    dfs = res["dfs"]
    assert set(codes) <= set(dfs), f"缺失 {set(codes)-set(dfs)}"
    cum, buy, sell = dfs["cum"], dfs["buy"], dfs["sell"]

    # ---- ① 矩阵级片段收益 ----
    df1 = cum.where(buy); df2 = cum.where(sell)
    df3 = df2.bfill().where(buy)
    seg_ret = df3 / df1 - 1.0
    mask = buy.values & np.isfinite(seg_ret.values)
    rows_t, cols_t = np.where(mask)
    stocks = list(buy.columns)
    S = pd.DataFrame({"code": [stocks[j] for j in cols_t],
                      "entry": buy.index[rows_t],
                      "seg_ret": seg_ret.values[mask]})
    GLOBAL = float(S["seg_ret"].mean())
    GLOBAL_MED = float(S["seg_ret"].median())
    WIN = float((S["seg_ret"] > 0).mean())
    S["quarter"] = S["entry"].dt.to_period("Q").astype(str)
    q_share_all = S.groupby("quarter").size() / len(S)

    row_idx = {t: i for i, t in enumerate(buy.index)}
    col_idx = {c: j for j, c in enumerate(buy.columns)}
    ri = np.array([row_idx[t] for t in S["entry"]], dtype=int)
    ci = np.array([col_idx[c] for c in S["code"]], dtype=int)

    # ---- ② 单因子双口径 ----
    single_rows = []
    for name, code, ir in factors:
        f = dfs[name].to_numpy(dtype=float)[ri, ci]
        sub = S.assign(fv=f).dropna(subset=["fv"])
        if len(sub) < 500:
            continue
        # 截面排名
        sub["r_cs"] = sub.groupby("entry")["fv"].rank(pct=True)
        # 全局排名
        sub["r_gl"] = sub["fv"].rank(pct=True)
        g_cs = sub.groupby(pd.qcut(sub["r_cs"], 10, labels=False, duplicates="drop"))["seg_ret"].mean()
        g_gl = sub.groupby(pd.qcut(sub["r_gl"], 10, labels=False, duplicates="drop"))["seg_ret"].mean()
        if len(g_cs) < 5 or len(g_gl) < 5:
            continue
        spread_cs = float(g_cs.iloc[-1] - g_cs.iloc[0])
        spread_gl = float(g_gl.iloc[-1] - g_gl.iloc[0])
        # 最优方向（按截面排名）
        if spread_cs > 0:
            best_cs = float(sub[sub["r_cs"] >= 0.7]["seg_ret"].mean())
            best_mask_cs = sub["r_cs"] >= 0.7
        else:
            best_cs = float(sub[sub["r_cs"] <= 0.3]["seg_ret"].mean())
            best_mask_cs = sub["r_cs"] <= 0.3
        if spread_gl > 0:
            best_gl = float(sub[sub["r_gl"] >= 0.7]["seg_ret"].mean())
        else:
            best_gl = float(sub[sub["r_gl"] <= 0.3]["seg_ret"].mean())
        improve_cs = best_cs - GLOBAL
        improve_gl = best_gl - GLOBAL
        # 时间分布（截面排名筛选）：每季度"筛选买点/该季全样本买点"占比
        tmp = sub.assign(sel=best_mask_cs)
        tq_all = tmp.groupby("quarter").size()
        tq_sel = tmp.loc[tmp["sel"]].groupby("quarter").size()
        share = (tq_sel / tq_all.reindex(tq_sel.index)).mean()   # 各季占比均值（≈0.3 均匀）
        share_max = (tq_sel / tq_all.reindex(tq_sel.index)).max()
        single_rows.append({
            "name": name, "IR": ir,
            "cs_improve": improve_cs, "gl_improve": improve_gl,
            "cs_best": best_cs, "gl_best": best_gl,
            "cs_spread": spread_cs, "gl_spread": spread_gl,
            "time_share_mean": float(share), "time_share_max": float(share_max),
            "n": int(len(sub)),
        })
    R = pd.DataFrame(single_rows)

    # ---- ③ 双因子 intersect（截面排名，Top8 正改善池） ----
    top8 = R.sort_values("cs_improve", ascending=False).head(8)
    # 重建 best 掩码供组合用
    best_masks = {}
    for name, code, ir in factors:
        if name not in set(top8["name"]):
            continue
        f = dfs[name].to_numpy(dtype=float)[ri, ci]
        sub = S.assign(fv=f).dropna(subset=["fv"])
        sub["r"] = sub.groupby("entry")["fv"].rank(pct=True)
        best_masks[name] = (sub["r"] >= 0.7 if (ir > 0) else sub["r"] <= 0.3).reindex(S.index, fill_value=False)
    pairs = []
    t8 = list(top8["name"])
    for i in range(len(t8)):
        for j in range(i + 1, len(t8)):
            both = best_masks[t8[i]] & best_masks[t8[j]]
            n = int(both.sum())
            if n < 200:
                continue
            imp = float(S.loc[both, "seg_ret"].mean() - GLOBAL)
            pairs.append({"fA": t8[i], "fB": t8[j], "improve": imp, "n": n})
    pairs.sort(key=lambda x: abs(x["improve"]), reverse=True)

    # ---- ④ 多因子贪心叠加（前30%交集，正改善） ----
    greedy = []
    chosen = []
    cur_imp = 0.0
    pool = list(top8["name"])
    for step in range(min(5, len(pool))):
        best_next, best_imp = None, cur_imp
        for name in pool:
            if name in chosen:
                continue
            combo_mask = pd.Series(True, index=S.index)
            for c in chosen + [name]:
                combo_mask &= best_masks[c]
            n = int(combo_mask.sum())
            if n < 200:
                continue
            imp = float(S.loc[combo_mask, "seg_ret"].mean() - GLOBAL)
            if imp > best_imp:
                best_next, best_imp = name, imp
        if best_next is None:
            break
        chosen.append(best_next)
        cur_imp = best_imp
        greedy.append({"step": len(chosen), "factor": best_next, "cum_improve": cur_imp})

    # ---- ⑤ 汇总 ----
    result = {
        "meta": {
            "strategy": CFG["label"],
            "n_stocks": int(buy.shape[1]),
            "date_range": f"{buy.index[0].date()} → {buy.index[-1].date()}",
            "n_segments": len(S),
            "global_ret": GLOBAL, "global_med": GLOBAL_MED, "win_rate": WIN,
            "n_factors": len(R), "agree_frac": float((R["cs_spread"].apply(lambda s: (s > 0)) == (R["IR"] > 0)).mean()),
            "runtime_s": round(time.time() - t0, 1),
        },
        "single_cs": R.sort_values("cs_improve", ascending=False).head(15).to_dict("records"),
        "single_gl": R.sort_values("gl_improve", key=lambda s: s.abs(), ascending=False).head(10).to_dict("records"),
        "pairs": pairs[:12],
        "greedy": greedy,
        "quarter_share": {str(k): float(v) for k, v in q_share_all.items()},
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"[DONE] 结果已存 {OUT}  耗时 {result['meta']['runtime_s']}s")
    print(f"  全局片段收益 {GLOBAL*100:.2f}% | 片段数 {len(S):,} | 因子数 {len(R)}")
    print(f"  截面排名改善 Top5: " + ", ".join(f"{r['name']}={r['cs_improve']*100:+.2f}pp" for r in result['single_cs'][:5]))
    print(f"  贪心最终: {cur_imp*100:+.2f}pp  ({' ∩ '.join(chosen)})")

if __name__ == "__main__":
    main()
