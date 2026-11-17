# -*- coding: utf-8 -*-
"""因子分析报告生成器：
自动扫描 stock-factor 技能 output/ 下所有 *.xlsx（每个 xlsx = 一个因子族），
读取并汇总统计分析，生成自包含 HTML 报告。新增 xlsx 会自动纳入，无需改代码。
"""
import pandas as pd, numpy as np, glob, os, base64, io, html
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
_fpath = r"C:\Windows\Fonts\msyh.ttc"
if os.path.exists(_fpath):
    try:
        fm.fontManager.addfont(_fpath)
    except Exception:
        pass
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SCRIPT_DIR, "output")

# 因子族「文件名stem → (展示名, 简称)」美化映射（仅用于显示与排序，缺失的 xlsx 会自动命名）。
# 不在下表里的 xlsx 也会被自动加载（用文件名当展示名），所以随时往 output/ 丢新文件即可。
NAME_MAP = {
    "facotr-Qlib_alpha158":      ("Qlib Alpha158",          "Alpha158"),
    "facotr-Qlib_alpha360":      ("Qlib Alpha360",          "Alpha360"),
    "factor-Alpha101":           ("WorldQuant Alpha101",     "Alpha101"),
    "factor-GTJA_Alpha191":      ("国泰君安 GTJA Alpha191",   "GTJA191"),
    "factor-Indicators":         ("TA-Lib 技术指标",        "TA"),
    "factor-stock_daily":        ("stock_daily 基础因子",     "Daily"),
    "factor-stock_report":       ("stock_report 财务因子",    "Report"),
    "factor-BarraCNE5":          ("Barra CNE5 风格",         "BarraCNE5"),
    "factor-Piotroski":          ("Piotroski F-Score",       "Piotroski"),
    "factor-AltmanZ":            ("Altman Z-Score",          "AltmanZ"),
    "factor-ClassicAnomalies":   ("经典学术异象",            "Anomaly"),
    "factor-FF_HXZ":             ("Fama-French / HXZ",       "FFHXZ"),
    "factor-CITIC_Shenwan":      ("中信/申万 风格",           "CITIC"),
    "factor-WorldQuant_formulaic": ("WorldQuant 公式化alpha扩展批", "WQext"),
    "factor-ReturnMoment":       ("收益高阶矩/52周高",        "RetMom"),
    "factor-Merton_CashFlow":    ("Merton 现金流收益率",      "Merton"),
}

# ---------- 自动发现 output/ 下所有 xlsx ----------
xlsx_files = sorted(glob.glob(os.path.join(OUT, "*.xlsx")))
if not xlsx_files:
    raise SystemExit("[error] output/ 下未找到任何 .xlsx，无法生成报告")

# 读取后需要、但缺失时补成 NaN 的必备列（保证脚本健壮性）
REQUIRED_NUM = ["IC", "IR", "time_potential", "stock_count", "feature_days",
                "start_date", "end_date", "top10%_IR", "bottom10%_IR", "coverage"]

def load_xlsx(path):
    df = pd.read_excel(path)
    if "name" not in df.columns:
        df["name"] = df.index.astype(str)
    if "code" not in df.columns:
        df["code"] = ""
    for c in REQUIRED_NUM:
        if c not in df.columns:
            df[c] = np.nan
    return df

def derive_names(stem):
    if stem in NAME_MAP:
        return NAME_MAP[stem]
    name = stem
    for p in ("factor-", "facotr-"):
        if name.startswith(p):
            name = name[len(p):]
    name = (name.replace("_", " ").strip()) or stem
    return (name, name[:12])

frames, fam_order, SHORT, FILES = [], [], {}, {}

# 先按 NAME_MAP 展示顺序加载已知族（文件存在才加载）
for stem in NAME_MAP:
    path = os.path.join(OUT, stem + ".xlsx")
    if not os.path.exists(path):
        continue
    fam, short = NAME_MAP[stem]
    try:
        df = load_xlsx(path)
    except Exception as e:
        print(f"[skip] {stem}: 读取失败 {e}")
        continue
    df["family"] = fam
    df["short"] = short
    frames.append(df); fam_order.append(fam); SHORT[fam] = short; FILES[fam] = stem + ".xlsx"
    print(f"[load] {fam}: {len(df)} rows")

# 再加载 NAME_MAP 之外的 xlsx（未知族，自动命名）
known_stems = set(NAME_MAP.keys())
for p in xlsx_files:
    stem = os.path.splitext(os.path.basename(p))[0]
    if stem in known_stems:
        continue
    fam, short = derive_names(stem)
    try:
        df = load_xlsx(p)
    except Exception as e:
        print(f"[skip] {stem}: 读取失败 {e}")
        continue
    df["family"] = fam; df["short"] = short
    frames.append(df); fam_order.append(fam); SHORT[fam] = short; FILES[fam] = os.path.basename(p)
    print(f"[load] {fam}: {len(df)} rows (auto)")

if not frames:
    raise SystemExit("[error] 没有任何可加载的 xlsx")

all_df = pd.concat(frames, ignore_index=True)
fams = fam_order
print(f"[load] TOTAL factors = {len(all_df)}, families = {len(fams)}")

# 动态调色板（支持任意数量因子族）
_base = list(plt.get_cmap("tab20").colors)  # 20 种
PALETTE = (_base * ((len(fams) // len(_base)) + 1))[:len(fams)]

# ---------- 指标计算 ----------
def fam_stats(df):
    ir = df["IR"].abs()
    return {
        "n": len(df),
        "eff": int((df["IR"].abs() > 0.3).sum()),
        "strong": int((df["IR"].abs() > 0.5).sum()),
        "mean_absIR": df["IR"].abs().mean(),
        "mean_IR": df["IR"].mean(),
        "median_IR": df["IR"].median(),
        "mean_absIC": df["IC"].abs().mean(),
        "mean_IC": df["IC"].mean(),
        "mean_tp": df["time_potential"].mean(),
        "tp_valid": int(df["time_potential"].notna().sum()),
        "top_name": df.loc[df["IR"].abs().idxmax(), "name"],
        "top_absIR": df["IR"].abs().max(),
    }

stats = {}
for fam in fams:
    stats[fam] = fam_stats(all_df[all_df.family == fam])

grand = {
    "n": len(all_df),
    "eff": int((all_df["IR"].abs() > 0.3).sum()),
    "strong": int((all_df["IR"].abs() > 0.5).sum()),
    "mean_absIR": all_df["IR"].abs().mean(),
    "mean_IC": all_df["IC"].mean(),
    "mean_tp": all_df["time_potential"].mean(),
}
date0 = all_df["start_date"].dropna().min()
date1 = all_df["end_date"].dropna().max()
sc_med = all_df["stock_count"].median()
sc_min = all_df["stock_count"].min()

print(f"[stats] effective(|IR|>0.3)={grand['eff']}, strong(|IR|>0.5)={grand['strong']}")

# ---------- 排行榜 ----------
def topn(df, n):
    return df.assign(absIR=df["IR"].abs()).sort_values("absIR", ascending=False).head(n)

leader = topn(all_df, 30).copy()

# ---------- 图表 ----------
def fig_to_b64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110, bbox_inches="tight")
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode("ascii")

charts = {}

# 1) 各家族因子数 & 有效因子数
fig, ax = plt.subplots(figsize=(9.2, 4.4))
f = fams
tot = [stats[x]["n"] for x in f]
eff = [stats[x]["eff"] for x in f]
x = np.arange(len(f))
ax.bar(x, tot, color="#cbd5e1", label="因子总数")
ax.bar(x, eff, color="#2563eb", label="有效因子(|IR|>0.3)")
ax.set_xticks(x); ax.set_xticklabels([SHORT[s] for s in f], rotation=35, ha="right")
ax.set_ylabel("因子数量")
ax.set_title("各因子族规模与有效因子数")
for i, v in enumerate(eff):
    ax.text(i, v + 2, str(v), ha="center", fontsize=8)
ax.legend()
charts["scale"] = fig_to_b64(fig)

# 2) 平均 |IR|
fig, ax = plt.subplots(figsize=(9.2, 4.4))
m = [stats[s]["mean_absIR"] for s in f]
ax.bar(x, m, color=PALETTE[:len(f)])
ax.axhline(0.3, color="#dc2626", ls="--", lw=1, label="有效性阈值 0.3")
ax.set_xticks(x); ax.set_xticklabels([SHORT[s] for s in f], rotation=35, ha="right")
ax.set_ylabel("平均 |IR|")
ax.set_title("各因子族平均信息比率(|IR|)")
ax.legend()
charts["meanir"] = fig_to_b64(fig)

# 3) IR 分布直方图
fig, ax = plt.subplots(figsize=(8.2, 4.2))
ax.hist(all_df["IR"].dropna(), bins=60, color="#2563eb", alpha=0.8)
ax.axvline(0.3, color="#dc2626", ls="--", lw=1.2, label="IR=0.3")
ax.axvline(-0.3, color="#dc2626", ls="--", lw=1.2, label="IR=-0.3")
ax.axvline(0, color="#475569", lw=1)
ax.set_xlabel("IR (信息比率)")
ax.set_ylabel("因子数量")
ax.set_title("全部因子 IR 分布")
ax.legend()
charts["irhist"] = fig_to_b64(fig)

# 4) Top20 因子 |IR| 横向条
top20 = topn(all_df, 20).iloc[::-1]
fig, ax = plt.subplots(figsize=(8.6, 6.0))
labels = [f"{r.name} [{SHORT[r.family]}]" for _, r in top20.iterrows()]
vals = top20["IR"].values
colors = ["#dc2626" if v < 0 else "#16a34a" for v in vals]
ax.barh(range(len(top20)), vals, color=colors)
ax.set_yticks(range(len(top20))); ax.set_yticklabels(labels, fontsize=8)
ax.set_xlabel("IR")
ax.set_title("Top 20 因子 by |IR| (红=负向, 绿=正向)")
ax.axvline(0, color="#475569", lw=1)
charts["top20"] = fig_to_b64(fig)

# 5) IC vs IR 散点
fig, ax = plt.subplots(figsize=(8.2, 5.6))
for i, fam in enumerate(fams):
    d = all_df[all_df.family == fam]
    ax.scatter(d["IC"], d["IR"], s=10, alpha=0.6, color=PALETTE[i], label=SHORT[fam])
ax.axhline(0.3, color="#dc2626", ls="--", lw=1)
ax.axhline(-0.3, color="#dc2626", ls="--", lw=1)
ax.axvline(0, color="#475569", lw=0.8)
ax.set_xlabel("IC (秩相关)")
ax.set_ylabel("IR (信息比率)")
ax.set_title("IC - IR 关系（按因子族着色）")
ax.legend(fontsize=8, markerscale=2)
charts["scatter"] = fig_to_b64(fig)

# 6) time_potential 分布
fig, ax = plt.subplots(figsize=(8.2, 4.2))
tp = all_df["time_potential"].dropna()
ax.hist(tp, bins=50, color="#7c3aed", alpha=0.8)
ax.axvline(1.0, color="#dc2626", ls="--", lw=1.2, label="稳定性基准 1.0")
ax.set_xlabel("time_potential")
ax.set_ylabel("因子数量")
ax.set_title("time_potential 分布（越接近1越稳定）")
ax.legend()
charts["tp"] = fig_to_b64(fig)

# ---------- 工具函数 ----------
def img_tag(b64, cap=""):
    s = f'<img class="chart" src="data:image/png;base64,{b64}" alt="{cap}"/>'
    if cap:
        s += f'<div class="cap">{cap}</div>'
    return s

def esc(s):
    return html.escape(str(s))

def fmt(x, nd=4):
    if pd.isna(x):
        return "—"
    return f"{x:.{nd}f}"

# ---------- 表构建 ----------
def summary_table():
    rows = ""
    for fam in fams:
        s = stats[fam]
        rows += (f"<tr><td>{esc(fam)}</td><td>{s['n']}</td><td>{s['eff']}</td>"
                 f"<td>{s['strong']}</td><td>{fmt(s['mean_absIR'])}</td>"
                 f"<td>{fmt(s['mean_IC'])}</td><td>{fmt(s['mean_tp'])}</td>"
                 f"<td>{esc(s['top_name'])}</td></tr>")
    g = grand
    rows += (f"<tr class='grand'><td><b>合计</b></td><td><b>{g['n']}</b></td>"
             f"<td><b>{g['eff']}</b></td><td><b>{g['strong']}</b></td>"
             f"<td><b>{fmt(g['mean_absIR'])}</b></td><td>{fmt(g['mean_IC'])}</td>"
             f"<td>{fmt(g['mean_tp'])}</td><td>—</td></tr>")
    return rows

def leaderboard_table():
    rows = ""
    for i, (_, r) in enumerate(leader.iterrows(), 1):
        t10 = fmt(r["top10%_IR"]); b10 = fmt(r["bottom10%_IR"])
        code = esc(r["code"]).replace("\n", "<br/>")
        rows += (f"<tr><td>{i}</td><td>{esc(r['name'])}</td><td>{esc(r['short'])}</td>"
                 f"<td>{fmt(r['IC'])}</td><td>{fmt(r['IR'])}</td>"
                 f"<td>{fmt(r['time_potential'])}</td><td>{t10}</td><td>{b10}</td>"
                 f"<td><details><summary>查看代码</summary><code>{code}</code></details></td></tr>")
    return rows

def family_detail_table():
    out = ""
    for fam in fams:
        d = topn(all_df[all_df.family == fam], 10)
        out += f"<h4>{esc(fam)} — Top 10 by |IR|</h4><table><thead><tr>"\
               f"<th>因子名</th><th>IC</th><th>IR</th><th>time_potential</th>"\
               f"<th>top10%_IR</th><th>bottom10%_IR</th></tr></thead><tbody>"
        for _, r in d.iterrows():
            out += (f"<tr><td>{esc(r['name'])}</td><td>{fmt(r['IC'])}</td><td>{fmt(r['IR'])}</td>"
                    f"<td>{fmt(r['time_potential'])}</td><td>{fmt(r['top10%_IR'])}</td>"
                    f"<td>{fmt(r['bottom10%_IR'])}</td></tr>")
        out += "</tbody></table>"
    return out

# ---------- HTML ----------
CSS = """
* { box-sizing: border-box; }
body { font-family: -apple-system, "Segoe UI", "Microsoft YaHei", sans-serif;
  margin: 0; background: #f5f7fa; color: #1f2937; line-height: 1.6; }
.wrap { max-width: 1080px; margin: 0 auto; padding: 24px 28px 60px; }
.disclaimer { background: #fff7ed; border: 1px solid #fdba74; border-left: 6px solid #ea580c;
  border-radius: 8px; padding: 16px 20px; margin-bottom: 24px; }
.disclaimer h2 { margin: 0 0 6px; color: #c2410c; font-size: 17px; }
.disclaimer p { margin: 4px 0; font-size: 13.5px; color: #7c2d12; }
h1 { font-size: 26px; margin: 0 0 4px; }
.sub { color: #6b7280; font-size: 13px; margin-bottom: 18px; }
.card { background: #fff; border: 1px solid #e5e7eb; border-radius: 10px;
  padding: 18px 22px; margin: 18px 0; box-shadow: 0 1px 2px rgba(0,0,0,.04); }
.card h2 { margin: 0 0 14px; font-size: 19px; border-bottom: 2px solid #2563eb;
  padding-bottom: 8px; display: inline-block; }
.kpis { display: flex; flex-wrap: wrap; gap: 14px; margin: 6px 0 14px; }
.kpi { flex: 1; min-width: 130px; background: #eff6ff; border: 1px solid #bfdbfe;
  border-radius: 8px; padding: 12px 14px; text-align: center; }
.kpi .v { font-size: 24px; font-weight: 700; color: #1d4ed8; }
.kpi .l { font-size: 12px; color: #475569; margin-top: 2px; }
table { width: 100%; border-collapse: collapse; font-size: 12.5px; margin-top: 8px; }
th, td { border: 1px solid #e5e7eb; padding: 6px 8px; text-align: center; }
thead th { background: #f1f5f9; color: #0f172a; position: sticky; top: 0; }
tbody tr:nth-child(even) { background: #fafafa; }
tr.grand td { background: #eef2ff; }
.chart { width: 100%; max-width: 860px; display: block; margin: 8px auto; border: 1px solid #e5e7eb; border-radius: 6px; }
.cap { text-align: center; font-size: 12px; color: #6b7280; margin-bottom: 12px; }
code { display: block; white-space: pre-wrap; word-break: break-all; font-size: 11px;
  background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 4px; padding: 8px; color: #334155; }
details summary { cursor: pointer; color: #2563eb; font-size: 12px; }
.note { font-size: 13px; color: #374151; }
.note li { margin: 5px 0; }
"""

html_doc = f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>股票因子分析报告</title><style>{CSS}</style></head><body><div class="wrap">

<div class="disclaimer">
  <h2>⚠️ 重要提示</h2>
  <p>本报告内容基于 <b>skillhub『股票因子』技能</b> 获取的初始数据（各因子族 IC / IR / time_potential 等评估指标），
  由 <b>WorkBuddy 自动分析</b> 生成，<b>仅供参考，不构成任何投资建议</b>。</p>
  <p>因子历史表现不代表未来收益；市场有风险，投资需谨慎。据此操作，盈亏自负。</p>
</div>

<h1>股票因子分析报告</h1>
<div class="sub">数据来源：stock-factor 技能 output/*.xlsx（自动汇总 {len(fams)} 个因子族）｜ 生成工具：WorkBuddy 自动分析 ｜
样本区间：{esc(date0)} ~ {esc(date1)} ｜ 股票池：全市场约 {sc_med:.0f} 只</div>

<div class="card">
  <h2>一、分析总览</h2>
  <div class="kpis">
    <div class="kpi"><div class="v">{grand['n']}</div><div class="l">纳入因子总数</div></div>
    <div class="kpi"><div class="v" style="color:#16a34a">{grand['eff']}</div><div class="l">有效因子 (|IR|&gt;0.3)</div></div>
    <div class="kpi"><div class="v" style="color:#dc2626">{grand['strong']}</div><div class="l">强有效因子 (|IR|&gt;0.5)</div></div>
    <div class="kpi"><div class="v">{fmt(grand['mean_absIR'])}</div><div class="l">平均 |IR|</div></div>
    <div class="kpi"><div class="v">{fmt(grand['mean_IC'])}</div><div class="l">平均 IC</div></div>
  </div>
  <p class="note">本次共分析 <b>{grand['n']}</b> 个因子，覆盖 <b>{len(fams)}</b> 个因子族。按 |IR|&gt;0.3 口径，
  有效因子 <b>{grand['eff']}</b> 个（占比 {grand['eff']/grand['n']*100:.1f}%），
  其中强有效（|IR|&gt;0.5）<b>{grand['strong']}</b> 个。IC 的正负代表因子方向：
  正=因子值越大未来收益越高，负=相反。</p>
  <table><thead><tr><th>因子族</th><th>因子数</th><th>有效数</th><th>强有效</th>
  <th>平均|IR|</th><th>平均IC</th><th>平均time_potential</th><th>领头牛因子</th></tr></thead>
  <tbody>{summary_table()}</tbody></table>
  {img_tag(charts['scale'], "各因子族规模与有效因子数")}
  {img_tag(charts['meanir'], "各因子族平均信息比率")}
</div>

<div class="card">
  <h2>二、因子有效性分布</h2>
  <p class="note">IR（信息比率）= IC均值 / IC标准差，|IR|&gt;0.3 通常视为有效。
  下图显示全部 {grand['n']} 个因子的 IR 分布：大量因子集中在 0 附近（预测力弱），
  长尾部分布在 ±0.3 之外的是具备选股信号的候选因子。</p>
  {img_tag(charts['irhist'], "全部因子 IR 分布（红色虚线为 ±0.3 阈值）")}
  {img_tag(charts['tp'], "time_potential 分布（越接近1越稳定）")}
</div>

<div class="card">
  <h2>三、IC - IR 关系（跨因子族）</h2>
  <p class="note">横轴为 IC（因子值与未来收益的秩相关），纵轴为 IR。
  点越靠上/下且离 0 越远，因子信号越稳定有效。不同颜色代表不同因子族，可直观比较各族整体表现。</p>
  {img_tag(charts['scatter'], "IC-IR 散点（按因子族着色）")}
</div>

<div class="card">
  <h2>四、有效因子排行榜（Top 30 by |IR|）</h2>
  <p class="note">下表为全部因子中 |IR| 最高的 30 个，按 |IR| 降序。
  top10%_IR / bottom10%_IR 反映因子在头/尾极端档位的区分度（一头显著正、另一头显著负 = 多空信号可靠）。</p>
  <table><thead><tr><th>#</th><th>因子名</th><th>族</th><th>IC</th><th>IR</th>
  <th>time_potential</th><th>top10%_IR</th><th>bottom10%_IR</th><th>代码</th></tr></thead>
  <tbody>{leaderboard_table()}</tbody></table>
  {img_tag(charts['top20'], "Top 20 因子 |IR|（红=负向因子，绿=正向因子）")}
</div>

<div class="card">
  <h2>五、各因子族明细（Top 10 by |IR|）</h2>
  {family_detail_table()}
</div>

<div class="card">
  <h2>六、数据健康度与注意事项</h2>
  <ul class="note">
    <li><b>样本覆盖：</b>股票池中位数约 {sc_med:.0f} 只（最少 {sc_min:.0f} 只），样本区间 {esc(date0)} ~ {esc(date1)}，
    评估用未来 {int(all_df['feature_days'].mode().iloc[0])} 日收益。</li>
    <li><b>time_potential 口径：</b>= daily_IC.MA5.STD / daily_IC.STD，越接近 1 代表近期信号与长期一致、越稳定；
    极端值可能意味着因子近期失效或样本异常。</li>
    <li><b>头尾档位可能缺失：</b>部分因子值大量重复（常数因子或大量同值），排序后极端档位无合适样本，
    其 top10%_* / bottom10%_* 为空（显示为 —），属数据特性非代码错误。</li>
    <li><b>常数因子：</b>个别因子（如 CLOSE0 类）IC 异常属正常，已在初筛中跳过。</li>
    <li><b>本报告边界：</b>当前为「因子清单 + 初筛」，尚未做精选、去冗余、因子合成与策略回测。
    下列指标仅供进一步研究的候选参考。</li>
  </ul>
</div>

<div class="card">
  <h2>七、后续建议（可结合 QuantAll 全A解析）</h2>
  <ul class="note">
    <li>在 |IR|&gt;0.3 候选基础上<b>精选</b>有效因子并评级；</li>
    <li>用 <b>batch_factor_corr</b> 做因子间<b>去冗余</b>（|IC|&gt;0.8 视为冗余），降低多重共线性；</li>
    <li>对精选因子做<b>正交 / 合成</b>，构造复合选股信号；</li>
    <li>接入 <b>strategy_backtest</b> 做回测验证，确认实盘可行性；</li>
    <li>随时间<b>更新 IC</b> 做版本管理，监控因子衰减。</li>
  </ul>
  <p class="note">提示：QuantAll（全A解析）MCP 已就绪，上述步骤可直接在其上调用对应工具完成。</p>
</div>

<div class="sub" style="text-align:center;margin-top:30px">
  本报告由 WorkBuddy 基于 stock-factor 技能初始数据自动生成 · 仅供参考 · 不构成投资建议
</div>
</div></body></html>"""

out_path = os.path.join(SCRIPT_DIR, "因子分析报告.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html_doc)
print(f"[done] report written -> {out_path} ({len(html_doc)/1024:.1f} KB)")
