# -*- coding: utf-8 -*-
"""
D4 深入 · timeline 模式逐日曲线分析（timeline_analysis.py）
==========================================================
strategy_backtest(view="timeline") 返回逐日表格：收益%分布 / 收益排序分布 /
持仓分布 / 买点分布 / 卖点分布。引擎只绘制曲线、不支持继续分析——本脚本
用 run_codes **本地重建同一套每日指标**（结构化、可复现），并做深度诊断：

  1. 净值重建：组合日收益复利 → 年化/夏普/最大回撤/日胜率
  2. 收益排序分位：每日组合收益在全市场当日收益中的分位（>0.5=跑赢一半股票）
     → 选股能力的时序代理（均值/>0.5占比/趋势）
  3. 持仓比时序 vs 未来收益相关（择时能力检验：持仓是否在市场涨前增加）
  4. 交易活跃度：每日买点/卖点数 → 换手估算、交易集中期
  5. 时段分解：按季聚合 + 滚动 60 日夏普（D4，与 poc2 交叉验证）
  6. 极端日画像：收益 Top/Bottom 5% 日的 持仓/排序/交易 特征
  7. 双口径对照：本地组合净值 vs summary 逐笔口径（D7 红旗复用）

两种数据来源：
  - 默认：run_codes 本地重建（推荐，精确可复现）
  - 可选：解析 MCP timeline 文本文件（大结果落盘 .txt 时传入路径作交叉验证）
    用法: python timeline_analysis.py <timeline_结果.txt>
"""
import json, re, sys
import numpy as np
import pandas as pd

PROJ = r"C:/Users/CMF/.workbuddy/skills/quantall/scripts"

# ============ 数据来源 1：解析 MCP timeline 文本 ============
def parse_timeline_text(path):
    """解析 strategy_backtest(view=timeline) 的 '表格' 字段文本 → DataFrame。
    列：收益%分布 / 收益排序分布 / 持仓分布 / 买点分布 / 卖点分布（index=日期）。
    兼容两种输入：完整 JSON（含 "表格" 字段）或纯表格文本。"""
    txt = open(path, encoding="utf-8").read()
    # 兼容纯文本表格（第一行=表头，日期为 YYYYMMDD 或带横线日期）
    if "收益%分布" in txt and '"表格"' not in txt:
        body = txt
    else:
        m = re.search(r'"表格":\s*"((?:[^"\\]|\\.)*)"', txt, re.S)
        if not m:
            raise ValueError("未找到 timeline 表格块，请确认传入的是 timeline 结果的原始 JSON/文本")
        body = m.group(1).encode().decode("unicode_escape")
    lines = [l for l in body.split("\n") if l.strip()]
    header = lines[0].split()
    rows = []
    for l in lines[1:]:
        parts = l.split()
        if len(parts) >= 6:
            rows.append(parts[:6])
    df = pd.DataFrame(rows, columns=["date"] + header)
    # 兼容两种日期格式：%Y%m%d（本地重建）与 %Y-%m-%d（MCP timeline 文本）
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
    if df["date"].isna().all():
        df["date"] = pd.to_datetime(df["date"], format="%Y%m%d", errors="coerce")
    for c in header:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df.set_index("date").sort_index()

# ============ 数据来源 2：run_codes 本地重建（默认） ============
def build_timeline_local(codes_buy_sell=None):
    """用 run_codes 拉 hold/ret，本地重建 timeline 每日指标。
    返回 (df, ret_w)：df=每日指标表，ret_w=截尾后全市场日收益（用于排序分位）"""
    from QuantAll import run_codes
    default_codes = {
        "hold": (
            "ac=d['close']*d['adj_factor']\n"
            "ma_s=ac.rolling(5).mean()\nma_l=ac.rolling(20).mean()\n"
            "buy=(ma_s>ma_l)&(ma_s.shift(1)<=ma_l.shift(1))\n"
            "sell=(ma_s<ma_l)&(ma_s.shift(1)>=ma_l.shift(1))\n"
            "out=hold_until(buy,sell)"
        ),
        "buy": (
            "ac=d['close']*d['adj_factor']\n"
            "ma_s=ac.rolling(5).mean()\nma_l=ac.rolling(20).mean()\n"
            "out=(ma_s>ma_l)&(ma_s.shift(1)<=ma_l.shift(1))"
        ),
        "sell": (
            "ac=d['close']*d['adj_factor']\n"
            "ma_s=ac.rolling(5).mean()\nma_l=ac.rolling(20).mean()\n"
            "out=(ma_s<ma_l)&(ma_s.shift(1)>=ma_l.shift(1))"
        ),
        "ret": "ac=d['close']*d['adj_factor']\nout=ac.pct_change()",
    }
    if codes_buy_sell:
        default_codes.update(codes_buy_sell)
    res = run_codes(default_codes, PROJ)
    dfs = res["dfs"]
    assert set(default_codes) <= set(dfs), f"缺失: {set(default_codes)-set(dfs)} {res['error']['message']}"
    hold, buy, sell, ret = dfs["hold"], dfs["buy"], dfs["sell"], dfs["ret"]

    lo, hi = np.nanpercentile(ret.values, [1, 99])
    ret_w = ret.clip(lo, hi)

    mask = hold & ret_w.notna()
    n_hold = mask.sum(axis=1)
    port = (mask * ret_w).sum(axis=1) / n_hold.replace(0, np.nan)
    port = port.replace([np.inf, -np.inf], np.nan).fillna(0.0)

    # 组合收益在全市场当日收益中的分位（升序排名，>0.5=跑赢一半股票）
    mkt_rank = ret_w.rank(axis=1, pct=True, na_option="keep")
    port_rank = mkt_rank.mask(~mask).mean(axis=1)  # 持仓股的平均分位

    df = pd.DataFrame({
        "收益%分布": port * 100,
        "收益排序分布": port_rank,
        "持仓分布": n_hold,
        "买点分布": buy.sum(axis=1),
        "卖点分布": sell.sum(axis=1),
    })
    return df, ret_w

# ============ 分析主体 ============
def analyze(df, ret_w=None, label="timeline", offset_days=0):
    """offset_days: 与 strategy_backtest 的 offset 对齐，裁掉前 N 个预热交易日。
    默认 0 = 自动从首个持仓日裁剪（MCP timeline 从首个持仓日 2024-09-27 开始，
    本地重建含更早的空仓/预热期，自动对齐到同一起点）。"""
    if offset_days:
        df = df.iloc[offset_days:]
    else:
        first = df.index[df["持仓分布"] > 0]
        if len(first):
            df = df.loc[first[0]:]
    print(f"\n{'='*68}\n[{label}] 交易日数={len(df)}  日期 {df.index[0].date()} → {df.index[-1].date()}")

    # ---- 1. 净值重建 ----
    s = df["收益%分布"] / 100
    nav = (1 + s).cumprod()
    n = len(s)
    ann = (1 + s).prod() ** (252 / n) - 1
    sharpe = s.mean() / s.std() * np.sqrt(252) if s.std() > 0 else 0
    win = (s > 0).mean()
    dd = (nav / nav.cummax() - 1).min()
    print(f"\n[1. 净值重建] 累计{(nav.iloc[-1]-1)*100:.1f}%  年化{ann*100:.1f}%  夏普{sharpe:.2f}  日胜率{win*100:.1f}%  最大回撤{dd*100:.1f}%")

    # ---- 2. 收益排序分位（选股能力代理） ----
    rk = df["收益排序分布"].dropna()
    if len(rk):
        print(f"\n[2. 收益排序分位] 均值{rk.mean():.3f}  中位{rk.median():.3f}  >0.5占比{(rk>0.5).mean()*100:.1f}%  "
              f"趋势(前半年{ rk.iloc[:int(len(rk)/2)].mean():.3f} → 后半年{ rk.iloc[int(len(rk)/2):].mean():.3f})")

    # ---- 3. 持仓比 vs 未来收益（择时能力） ----
    hold_ratio = df["持仓分布"] / df["持仓分布"].max()
    fwd5 = (s.shift(-5).rolling(5, min_periods=1).sum())
    fwd20 = (s.shift(-20).rolling(20, min_periods=1).sum())
    corr5 = hold_ratio.corr(fwd5)
    corr20 = hold_ratio.corr(fwd20)
    # 未来市场收益（全市场等权）
    if ret_w is not None:
        mkt = ret_w.mean(axis=1).fillna(0.0)
        mfwd5 = (mkt.shift(-5).rolling(5, min_periods=1).sum())
        mcorr5 = hold_ratio.corr(mfwd5)
        print(f"\n[3. 择时检验] 持仓比 vs 未来5日组合收益 r={corr5:+.3f} | vs 未来20日 r={corr20:+.3f} | vs 未来5日市场 r={mcorr5:+.3f}")
        print(f"  （r≈0 → 持仓变化不择时，靠持续暴露；r>0 → 持仓在市场好前增加=有择时）")
    else:
        print(f"\n[3. 择时检验] 持仓比 vs 未来5日组合收益 r={corr5:+.3f} | vs 未来20日 r={corr20:+.3f}")

    # ---- 4. 交易活跃度 ----
    tr = df["买点分布"].sum() + df["卖点分布"].sum()
    active = (df["买点分布"] > 0).mean()
    print(f"\n[4. 交易活跃度] 总买点{int(df['买点分布'].sum()):,} 总卖点{int(df['卖点分布'].sum()):,}  "
          f"有买点交易日{active*100:.0f}%  日均买点{df['买点分布'].mean():.0f}  峰值{int(df['买点分布'].max()):,}")

    # ---- 5. 时段分解（按季 + 滚动夏普） ----
    q = s.resample("QE").apply(lambda x: (1 + x).prod() - 1)
    q_ann = (1 + q) ** 4 - 1
    print(f"\n[5. 时段分解] 按季收益(年化口径):")
    for t, v in q_ann.items():
        print(f"    {t.date()}  {v*100:7.1f}%")
    roll = s.rolling(60).mean() / s.rolling(60).std() * np.sqrt(252)
    print(f"  滚动60日夏普 [{roll.min():.2f} ~ {roll.max():.2f}]  末值{roll.iloc[-1]:.2f}")
    conc = q_ann.abs().sort_values(ascending=False)
    tot = (1 + s).prod() - 1
    print(f"  最大单季贡献 {conc.iloc[0]*100:.1f}% 占全期累计{tot*100:.1f}% 的 {conc.iloc[0]/tot*100 if tot>0 else float('nan'):.0f}%")

    # ---- 6. 极端日画像 ----
    df2 = df.assign(日收益=s).dropna(subset=["收益排序分布"])
    top = df2.nlargest(int(len(df2)*0.05), "日收益")
    bot = df2.nsmallest(int(len(df2)*0.05), "日收益")
    print(f"\n[6. 极端日画像（Top/Bottom 5% 交易日）]")
    print(f"    最好5%日: 持仓比均值{top['持仓分布'].mean()/df['持仓分布'].max()*100:.0f}%  排序分位{top['收益排序分布'].mean():.3f}  买点{top['买点分布'].mean():.0f}")
    print(f"    最差5%日: 持仓比均值{bot['持仓分布'].mean()/df['持仓分布'].max()*100:.0f}%  排序分位{bot['收益排序分布'].mean():.3f}  买点{bot['买点分布'].mean():.0f}")

    # ---- 7. 双口径对照提示 ----
    print(f"\n[7. 口径对照提示] 本地组合年化{ann*100:.1f}%（连续复利口径）→ 与 strategy_backtest summary 逐笔口径对照（D7）；"
          f"符号相反 = 收益依赖何时在场 = 假有效红旗。")

    return {"nav": nav, "ann": ann, "sharpe": sharpe, "q_ann": q_ann}

# ============ 入口 ============
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].endswith(".txt"):
        df = parse_timeline_text(sys.argv[1])
        analyze(df, label="MCP timeline 文本解析")
    else:
        df, ret_w = build_timeline_local()
        analyze(df, ret_w=ret_w, label="run_codes 本地重建")
        # 自测：把本地重建数据写成表格文本 → parse 回读 → 应逐列一致（验证 parse 路径，含带横线日期格式）
        body = "  " + "  ".join(df.columns) + "\n" + "\n".join(
            f"{t.strftime('%Y-%m-%d')}  " + "  ".join(f"{v:.6f}" if pd.notna(v) else "NaN" for v in row)
            for t, row in df.iterrows())
        import tempfile, os
        tmp = os.path.join(tempfile.gettempdir(), "_timeline_selftest.txt")
        open(tmp, "w", encoding="utf-8").write(body)
        df2 = parse_timeline_text(tmp)
        ok = np.allclose(df.values.astype(float), df2.values.astype(float), equal_nan=True, atol=1e-6)
        print(f"\n[自测] parse_timeline_text 回读一致性: {'✅ 通过' if ok else '❌ 失败'}  ({len(df2)} 行)")
        os.remove(tmp)
    print("\n[DONE] timeline 深入分析完成")
