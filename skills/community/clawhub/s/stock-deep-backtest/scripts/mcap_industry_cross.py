"""
D1 扩展 · 市值×行业 二维交叉归因 —— 金叉买点的"市值档 × 行业"收益矩阵。

与 group_by_attrs / group_by_code（原生单轴分组）互补：原生工具一次只能沿
X 或 Y 单轴分组（且层级叠加受"总细分<=1万"限制），本脚本用 run_codes 拉
买点/前向收益 + 起始市值（冻结在数据窗口起点），本地做二维交叉：
  · 行 = 起始市值十分位（1=最小盘 → 10=最大盘，row_rank 口径与原生一致）
  · 列 = 所属行业（买点数>=阈值的行业）
  · 值 = 该 (市值档, 行业) 组合下 买点后 20 日加权前向收益
输出：全表 + 最强/最弱组合 Top10 + 每市值档的行业集中度(有效行业数)。

用法：改 codes 里的策略代码即可复用（默认均线金叉 MA5/20）。
"""
import json, numpy as np, pandas as pd
from QuantAll import run_codes

PROJ = r"C:/Users/CMF/.workbuddy/skills/quantall/scripts"
DB = json.load(open(PROJ + "/DB_setting.json"))["db_path"]

# ---------- 1. 拉矩阵 ----------
codes = {
    "buy": """
ac = d['close'] * d['adj_factor']
ma_s = ac.rolling(5).mean()
ma_l = ac.rolling(20).mean()
out = (ma_s > ma_l) & (ma_s.shift(1) <= ma_l.shift(1))
""",
    "fwd20": """
ac = d['close'] * d['adj_factor']
out = ac.shift(-20)/ac - 1
""",
    # 起始市值：冻结在数据窗口起点（每只股票取窗口内首个有效市值，全期恒定）
    "mcap0": """
mcap = d['总市值'].ffill().bfill()
mcap0 = mcap.iloc[[0]].reindex(index=mcap.index).ffill()
out = mcap0
""",
}
res = run_codes(codes, PROJ)
dfs = res["dfs"]
assert set(codes) <= set(dfs), f"缺失: {set(codes)-set(dfs)} {res['error']['message']}"
buy, fwd, mcap0 = dfs["buy"], dfs["fwd20"], dfs["mcap0"]
print(f"[矩阵] buy={buy.shape} fwd20={fwd.shape} mcap0={mcap0.shape}  买点总数={int(buy.values.sum()):,}")

# ---------- 2. 股票属性（行业） ----------
import duckdb
con = duckdb.connect(DB, read_only=True)
attr = con.execute('SELECT "symbol","industry" FROM "stock_basic"').fetchdf()
con.close()
attr["symbol"] = attr["symbol"].astype(str)
code2ind = dict(zip(attr["symbol"], attr["industry"].fillna("未知")))

stocks = list(buy.columns)
ind_of = np.array([code2ind.get(str(s), "未知") for s in stocks], dtype=object)

# ---------- 3. 起始市值十分位（等频，与 row_rank 口径一致） ----------
m0 = mcap0.ffill().bfill().iloc[0]          # Series: 每只股票起始市值
m0_rank = m0.rank(pct=True)                  # 0~1 百分位
dec = np.clip(np.ceil(m0_rank * 10).astype(int), 1, 10)   # 1~10 档
print(f"[市值] 起始市值有效 {m0.notna().sum():,}/{len(m0):,}  十分位样本: 档1={int((dec==1).sum()):,} 档10={int((dec==10).sum()):,}")

# ---------- 4. 交叉表 ----------
mask = buy.values & np.isfinite(fwd.values)
vals = fwd.values[mask]
rows_t, cols_t = np.where(mask)              # (时间, 股票) 索引
inds = ind_of[cols_t]
decs = dec.values[cols_t]

df = pd.DataFrame({"ind": inds, "dec": decs, "r": vals})
g = df.groupby(["dec", "ind"])["r"].agg(["mean", "count"]).reset_index()
g = g[g["count"] >= 50]                      # 组合样本过少剔除
piv = g.pivot(index="dec", columns="ind", values="mean").reindex(
    index=range(1, 11))
cnt = g.pivot(index="dec", columns="ind", values="count").reindex(
    index=range(1, 11))

pd.set_option("display.width", 260, "display.max_columns", 100)
print(f"\n[交叉表] 市值档 × 行业（买点后20日加权收益%, 样本>=50）")
print(f"全局平均 = {vals.mean()*100:.2f}%   ({len(vals):,} 买点)")
print(piv.round(3).mul(100).to_string())

# ---------- 5. 最强/最弱组合 ----------
gg = g[g["count"] >= 100].copy()
gg["r%"] = gg["mean"] * 100
print(f"\n[最强组合 Top10]")
print(gg.sort_values("mean", ascending=False).head(10)[["dec", "ind", "r%", "count"]].to_string(index=False))
print(f"\n[最弱组合 Top10]")
print(gg.sort_values("mean").head(10)[["dec", "ind", "r%", "count"]].to_string(index=False))

# ---------- 6. 每档有效行业数与极差 ----------
print(f"\n[每市值档画像]")
for d in range(1, 11):
    sub = gg[gg["dec"] == d]
    if len(sub) == 0:
        print(f"  档{d}: 无有效行业")
        continue
    print(f"  档{d}: 有效行业{len(sub):3d}  均值{sub['r%'].mean():+5.2f}%  最好[{sub.loc[sub['r%'].idxmax(),'ind']} {sub['r%'].max():+.2f}%]  最差[{sub.loc[sub['r%'].idxmin(),'ind']} {sub['r%'].min():+.2f}%]")

print("\n[DONE] 市值×行业 二维交叉归因完成")
