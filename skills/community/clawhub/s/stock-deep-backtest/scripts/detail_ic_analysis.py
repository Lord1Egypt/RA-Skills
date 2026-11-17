# -*- coding: utf-8 -*-
"""
D8 · 个股收益横截面归因（detail 模式利用）—— 把 strategy_backtest(view="detail")
返回的"每只股票标量指标"当成标签向量，做横截面 IC/IR 式分析：

strategy_backtest(view="detail") 返回 5590 只股票 × 7 指标：
  总收益率-% / 年化收益率-% / 最大回撤-% / 夏普率 / 胜率-% / 盈亏比 / 基准收益率(自身)-%
（注意：是"每股票一个标量"，不是时间曲线；但作为横截面标签已足够做因子归因）

分析内容：
  1. 收益分布画像：总收益率/年化/夏普/胜率/回撤 的分位数与异常股
  2. 因子横截面 IC：个股总收益率 vs 各因子（起始市值/入场动量/波动/量比/估值）的 Pearson 相关
     （= 策略收益的因子暴露，横截面口径，等价"线性 IC"）
  3. 行业分组收益：各行业 平均总收益/胜率/样本数（与 group_by_attrs 回测图层口径交叉验证）
  4. 市值档×收益：起始市值十分位 → 平均总收益（与 group_by_code 交叉验证）
  5. 极端股画像：收益 Top/Bottom 1% 的特征（是否集中在某行业/市值档）

用法：改 codes 里的策略代码即可复用于任意策略。
依赖：QuantAll venv + detail 输出 JSON 文件路径（MCP 大结果落盘时）。
"""
import json, os, sys
import numpy as np
import pandas as pd
from QuantAll import run_codes

PROJ = r"C:/Users/CMF/.workbuddy/skills/quantall/scripts"
DB = json.load(open(PROJ + "/DB_setting.json"))["db_path"]

# ---------- 0. detail 结果文件（MCP 大结果落盘路径，可改） ----------
DETAIL_FILE = sys.argv[1] if len(sys.argv) > 1 else (
    r"C:/Users/CMF/.workbuddy/projects/c-Users-CMF-.workbuddy-skills/"
    r"a80d3562-be44-49fd-ae4d-367085c4452d/tool-results/"
    r"mcp-connector-proxy-_A___strategy_backtest-1787837630373-543580.txt")
raw = json.load(open(DETAIL_FILE, encoding="utf-8"))["result"]
perf = {k: pd.Series(v, name=k) for k, v in raw.items()}
df = pd.DataFrame(perf)
df.index.name = "code"
print(f"[detail] 股票数={len(df)}  指标={list(df.columns)}")

# ---------- 1. 收益分布画像 ----------
print(f"\n{'='*64}\n[1. 收益分布画像]")
for c in ["总收益率-%", "年化收益率-%", "最大回撤-%", "夏普率", "胜率-%"]:
    s = df[c].dropna()
    q = s.quantile([0, .01, .05, .25, .5, .75, .95, .99, 1])
    print(f"  {c}: 均值{s.mean():+.2f}  " +
          " ".join(f"p{int(p*100)}={v:+.2f}" for p, v in q.items()))

# ---------- 2. 拉因子矩阵（横截面标签的右侧：因子值） ----------
codes = {
    # 起始市值（冻结窗口起点）——与 D1 市值分组同口径
    "mcap0": "mcap=d['总市值'].ffill().bfill(); mcap0=mcap.iloc[[0]].reindex(index=mcap.index).ffill(); out=mcap0",
    # 入场前动量（数据中期固定截面：取每个股票序列前 1/2 处的 20 日动量）
    "mom":   "ac=d['close']*d['adj_factor']; out=ac.pct_change(20)",
    # 波动率（60日）
    "vol60": "ac=d['close']*d['adj_factor']; out=ac.pct_change().rolling(60).std()",
    # 量比
    "volr":  "out=d['vol']/d['vol'].rolling(20).mean()",
    # 估值
    "pe":    "out=d['市盈率TTM']",
}
res = run_codes(codes, PROJ)
dfs = res["dfs"]
assert set(codes) <= set(dfs), f"缺失: {set(codes)-set(dfs)} {res['error']['message']}"

def mid_series(m):
    """每列取中间时点（约 60% 处）的截面值，避免窗口起点 NaN/停牌噪声"""
    t = int(len(m) * 0.6)
    return m.iloc[t]

factors = {}
for name in codes:
    factors[name] = mid_series(dfs[name].ffill().bfill())
F = pd.DataFrame(factors)
F.index = F.index.astype(str)
print(f"[因子] {list(F.columns)}  截面股票数={len(F)}")

# ---------- 3. 因子横截面 IC（个股总收益 vs 因子） ----------
print(f"\n{'='*64}\n[2. 因子横截面 IC（个股总收益率 vs 因子，Pearson）]")
tab = df.join(F, how="inner").dropna(subset=["总收益率-%"])
print(f"  有效样本={len(tab)}")
for f in F.columns:
    sub = tab[["总收益率-%", f]].dropna()
    if len(sub) > 100:
        ic = sub["总收益率-%"].corr(sub[f])
        ic_s = sub["总收益率-%"].rank().corr(sub[f].rank())  # Spearman ≈ rank 后 Pearson（免 scipy）
        print(f"  {f:8s} vs 总收益 : pearson={ic:+.3f}  spearman={ic_s:+.3f}  (n={len(sub):,})")

# ---------- 4. 行业分组（duckdb 读 stock_basic） ----------
import duckdb
con = duckdb.connect(DB, read_only=True)
attr = con.execute('SELECT "symbol","industry" FROM "stock_basic"').fetchdf()
con.close()
attr["symbol"] = attr["symbol"].astype(str)
ind_map = dict(zip(attr["symbol"], attr["industry"].fillna("未知")))
df["行业"] = df.index.map(lambda c: ind_map.get(str(c), "未知"))

print(f"\n{'='*64}\n[3. 行业分组收益（个股总收益率均值，样本>=30）]")
g = df.groupby("行业").agg(
    平均总收益=("总收益率-%", "mean"), 中位总收益=("总收益率-%", "median"),
    胜率=("胜率-%", "mean"), 样本=("总收益率-%", "size"),
).query("样本>=30").sort_values("平均总收益", ascending=False)
print(f"  最好5行业:\n{g.head(5).round(2).to_string()}")
print(f"  最差5行业:\n{g.tail(5).round(2).to_string()}")

# ---------- 5. 市值档 × 收益（交叉验证 group_by_code） ----------
print(f"\n{'='*64}\n[4. 市值档 × 收益（起始市值十分位）]")
m0 = dfs["mcap0"].ffill().bfill().iloc[0]
m0_rank = m0.rank(pct=True)
dec = pd.Series(np.clip(np.ceil(m0_rank * 10).astype(int), 1, 10), index=m0.index.astype(str))
tab2 = df.join(dec.rename("档"), how="inner").dropna(subset=["总收益率-%"])
print(tab2.groupby("档")["总收益率-%"].agg(["mean", "median", "count"]).round(2).to_string())

# ---------- 6. 极端股画像 ----------
print(f"\n{'='*64}\n[5. 极端股画像（收益 Top/Bottom 1%）]")
n = max(1, int(len(df) * 0.01))
top = df.nlargest(n, "总收益率-%")
bot = df.nsmallest(n, "总收益率-%")
def prof(g, label):
    ind_top = g["行业"].value_counts().head(3)
    md = g["总收益率-%"].median()
    print(f"  {label}: 中位总收益 {md:+.1f}%  行业Top3={dict(ind_top)}  最大回撤均值 {g['最大回撤-%'].mean():.1f}%")
prof(top, "Top1%")
prof(bot, "Bot1%")

print("\n[DONE] D8 个股收益横截面归因完成")
