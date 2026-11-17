# -*- coding: utf-8 -*-
"""
多策略 HTML 报告渲染（make_report_html.py v3）
读取 full_attribution_result.json（run_full_attribution.py 产出）+ A 部分基础数据 JSON
→ 生成自包含 HTML。策略名/指标全部从数据驱动，A/B 结构 + 免责声明。
用法：python make_report_html.py [策略名 golden_cross|reversal|macd]
"""
import json, html, sys

BASE = r"C:/Users/CMF/.workbuddy/skills/stock-deep-backtest/scripts"
strat = sys.argv[1] if len(sys.argv) > 1 else "golden_cross"

# 优先读策略专属结果文件，否则读默认
import os
res_file = f"{BASE}/full_attribution_result_{strat}.json"
if not os.path.exists(res_file):
    res_file = f"{BASE}/full_attribution_result.json"
D = json.load(open(res_file, encoding="utf-8"))
M = D["meta"]
# A 部分基础数据（每策略独立文件，由 AI 提前用 MCP 采集）
try:
    A = json.load(open(f"{BASE}/base_{strat}.json", encoding="utf-8"))
except FileNotFoundError:
    A = {"summary": {}, "timeline": {}, "detail": {}, "quarters": {}}

def pct(x, sign=False, d=2):
    s = f"{x*100:+.2f}" if sign else f"{x*100:.2f}"
    return s + "%"

# ============ 单因子表 ============
cs_rows = ""
for i, r in enumerate(D["single_cs"], 1):
    cls = "pos" if r["cs_improve"] > 0 else "neg"
    gl = r["gl_improve"] * 100
    cs = r["cs_improve"] * 100
    glcls = "pos" if gl > 0 else "neg"
    diff = abs(gl - cs)
    warn = ' <span class="tag warn">时段虚增</span>' if diff > 0.5 else ""
    cs_rows += f"""<tr>
      <td class="muted">{i}</td><td><b>{html.escape(r['name'])}</b></td>
      <td>{r['IR']:+.2f}</td>
      <td class="{cls}">{pct(r['cs_best'])}</td>
      <td class="{cls}">{cs:+.2f}pp</td>
      <td class="{glcls}">{gl:+.2f}pp</td>
      <td>{r['time_share_mean']*100:.1f}% / {r['time_share_max']*100:.1f}%</td>
      <td class="muted">{r['n']:,}</td>{warn}</tr>"""

pair_rows = ""
for i, p in enumerate(D["pairs"], 1):
    cls = "pos" if p["improve"] > 0 else "neg"
    pair_rows += f"""<tr><td class="muted">{i}</td><td><b>{html.escape(p['fA'])}</b> ∩ <b>{html.escape(p['fB'])}</b></td>
      <td class="{cls}">{p['improve']*100:+.2f}pp</td><td class="muted">{p['n']:,}</td></tr>"""

greedy_rows = ""
prev = 0
for g in D["greedy"]:
    d = g["cum_improve"] - prev
    prev = g["cum_improve"]
    greedy_rows += f"""<tr><td class="muted">{g['step']}</td><td><b>{html.escape(g['factor'])}</b></td>
      <td class="pos">+{d*100:.2f}pp</td><td class="pos"><b>{g['cum_improve']*100:+.2f}pp</b></td></tr>"""

qs = D["quarter_share"]
qmax = max(qs.values()) if qs else 1
qbar = ""
for q, v in qs.items():
    w = v / qmax * 100
    qbar += f"""<div class="qrow"><span class="qlab">{q}</span><div class="qbar"><div class="qfill" style="width:{w:.0f}%"></div></div><span class="qval">{v*100:.1f}%</span></div>"""

final_imp = D["greedy"][-1]["cum_improve"] if D["greedy"] else 0

# ============ A 部分 ============
def kv_table(d):
    if not d:
        return "<tr><td class='k'>（未采集）</td><td>—</td></tr>"
    return "".join(f"<tr><td class='k'>{html.escape(str(k))}</td><td>{html.escape(str(v))}</td></tr>" for k, v in d.items())

q_rows = ""
for k, v in A.get("quarters", {}).items():
    cls = "pos" if str(v).startswith("+") else "neg"
    q_rows += f"<tr><td class='muted'>{k}</td><td class='{cls}'>{v}</td></tr>"

# ============ KPI ============
kpi = f"""
<div class="kpi-grid">
  <div class="kpi"><div class="kpi-v">{M['n_stocks']:,}</div><div class="kpi-l">股票数</div></div>
  <div class="kpi"><div class="kpi-v">{M['n_segments']:,}</div><div class="kpi-l">持仓片段</div></div>
  <div class="kpi"><div class="kpi-v">{pct(M['global_ret'])}</div><div class="kpi-l">全局片段收益</div></div>
  <div class="kpi"><div class="kpi-v">{M['win_rate']*100:.1f}%</div><div class="kpi-l">片段胜率</div></div>
  <div class="kpi"><div class="kpi-v">{M['n_factors']}</div><div class="kpi-l">评估因子</div></div>
  <div class="kpi"><div class="kpi-v">{M['agree_frac']*100:.0f}%</div><div class="kpi-l">方向与IR一致</div></div>
</div>"""

HTML = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(M['strategy'])} · 回测归因分析报告</title>
<style>
  :root {{ --bg:#f5f6fa; --card:#fff; --ink:#1a2233; --mut:#8a94a6; --line:#e6e9f0;
           --pos:#d93026; --neg:#0f9d58; --acc:#3b6ef5; --warn:#f5a623; --sec:#6a4bf5; }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ font-family:-apple-system,"Segoe UI","Microsoft YaHei",sans-serif; background:var(--bg); color:var(--ink); line-height:1.6; }}
  .wrap {{ max-width:1060px; margin:0 auto; padding:28px 20px 60px; }}
  header {{ margin-bottom:16px; }}
  h1 {{ font-size:24px; font-weight:700; }}
  .sub {{ color:var(--mut); font-size:13.5px; margin-top:6px; }}
  .disclaimer {{ background:#fff8ec; border:1px solid #f3dfb0; border-left:4px solid var(--warn);
                border-radius:10px; padding:12px 16px; font-size:12.5px; color:#7a5c1e; margin-bottom:22px; }}
  .disclaimer b {{ color:#8a6a00; }}
  .section-head {{ display:flex; align-items:center; gap:10px; margin:28px 0 16px; }}
  .section-head .badge {{ background:var(--sec); color:#fff; font-size:12px; font-weight:700;
                padding:4px 12px; border-radius:16px; }}
  .section-head h2 {{ font-size:19px; }}
  .banner {{ background:linear-gradient(135deg,#3b6ef5,#6a4bf5); color:#fff; border-radius:12px; padding:14px 20px; margin:0 0 20px; font-size:13.5px; }}
  .banner b {{ font-size:15px; }}
  .card {{ background:var(--card); border:1px solid var(--line); border-radius:12px; padding:20px 22px; margin-bottom:20px; }}
  .card h3 {{ font-size:15px; margin-bottom:14px; padding-bottom:10px; border-bottom:1px solid var(--line); }}
  .kpi-grid {{ display:grid; grid-template-columns:repeat(6,1fr); gap:12px; }}
  .kpi {{ background:var(--card); border:1px solid var(--line); border-radius:10px; padding:14px 10px; text-align:center; }}
  .kpi-v {{ font-size:20px; font-weight:700; color:var(--acc); }}
  .kpi-l {{ font-size:12px; color:var(--mut); margin-top:2px; }}
  table {{ width:100%; border-collapse:collapse; font-size:13px; }}
  th,td {{ padding:8px 10px; text-align:right; border-bottom:1px solid var(--line); }}
  th {{ background:#f0f3fa; font-weight:600; font-size:12px; color:var(--mut); }}
  td:first-child, td:nth-child(2), th:first-child, th:nth-child(2) {{ text-align:left; }}
  td.k {{ color:var(--mut); width:40%; }}
  .pos {{ color:var(--pos); font-weight:600; }}
  .neg {{ color:var(--neg); font-weight:600; }}
  .muted {{ color:var(--mut); }}
  .tag {{ font-size:11px; padding:1px 7px; border-radius:10px; margin-left:6px; }}
  .tag.warn {{ background:#fef3e0; color:var(--warn); }}
  .note {{ font-size:12.5px; color:var(--mut); background:#f8f9fc; border-left:3px solid var(--acc); padding:10px 14px; border-radius:0 8px 8px 0; margin-top:12px; }}
  .note b {{ color:var(--ink); }}
  .qrow {{ display:flex; align-items:center; gap:10px; margin:5px 0; font-size:12.5px; }}
  .qlab {{ width:64px; color:var(--mut); }}
  .qbar {{ flex:1; height:16px; background:#eef1f8; border-radius:8px; overflow:hidden; }}
  .qfill {{ height:100%; background:linear-gradient(90deg,#3b6ef5,#6a4bf5); border-radius:8px; }}
  .qval {{ width:56px; text-align:right; font-weight:600; }}
  .concl {{ background:linear-gradient(135deg,#fff,#f0f4ff); border:1px solid #d7e0ff; border-radius:12px; padding:18px 22px; margin-top:4px; }}
  .concl h3 {{ font-size:15px; color:var(--acc); margin-bottom:10px; }}
  .concl ul {{ padding-left:20px; font-size:13.5px; }}
  .concl li {{ margin:6px 0; }}
  .footer {{ text-align:center; color:var(--mut); font-size:12px; margin-top:26px; }}
  @media (max-width:720px) {{ .kpi-grid {{ grid-template-columns:repeat(3,1fr); }} }}
</style></head><body><div class="wrap">

<header>
  <h1>📊 {html.escape(M['strategy'])} · 回测归因分析报告</h1>
  <div class="sub">{M['date_range']} · {M['n_stocks']:,} 只股票 · stock-deep-backtest 技能 · 计算耗时 {M['runtime_s']}s</div>
</header>

<div class="disclaimer">⚠️ <b>免责声明：</b>本报告由 AI 使用 QuantAll（全A解析）量化分析工具生成。分析流程基于脚本自动化与统计推断，难免存在片面性、假设偏差与样本内局限（含停牌处理、参数敏感性、时段效应等未完全覆盖项）。本报告<b>仅供参考，不构成任何投资建议</b>。据此操作，风险自担。</div>

<div class="banner">🎯 <b>核心问题：</b>买入点那一刻的因子值/入场前行情特征，能否筛选出更优质的持仓片段、改善收益？<br>
<span style="opacity:.85">基线：片段平均收益 <b>{pct(M['global_ret'])}</b>（中位 {pct(M['global_med'])}，胜率 {M['win_rate']*100:.1f}%，{M['n_segments']:,} 片段）</span></div>

<!-- ============ A. 基础分析 ============ -->
<div class="section-head"><span class="badge">A</span><h2>基础分析：策略本身表现如何</h2></div>

<div class="card">
  <h3>A1 · summary 成绩单（strategy_backtest · 逐笔截面口径）</h3>
  <table>{kv_table(A.get('summary', {}))}</table>
  <div class="note">📌 逐笔口径：每只股票各自统计后取均值，<b>不是资金连续在场净值</b>（与 A2 差异可能极大，尤其事件驱动策略）。</div>
</div>

<div class="card">
  <h3>A2 · timeline 净值与择时（连续复利口径 · 更接近资金真实体验）</h3>
  <table>{kv_table(A.get('timeline', {}))}</table>
  <table style="margin-top:12px"><tr><th>季度</th><th>年化收益</th></tr>{q_rows}</table>
  <div class="note">📌 <b>双口径对照（D7）</b>：若 A1 逐笔年化与 A2 连续复利年化方向相反 → 收益依赖"何时在场"而非选股 = 假有效红旗（典型：反转/抄底策略只在崩后买入、把资金暴露在坏 regime）。</div>
</div>

<div class="card">
  <h3>A3 · detail 个股横截面归因（D8）</h3>
  <table>{kv_table(A.get('detail', {}))}</table>
  <div class="note">📌 因子暴露：波动率/市值/行业分布对策略收益的解释力（与 B 部分片段筛选结论互证）。</div>
</div>

<!-- ============ B. 因子筛选改善 ============ -->
<div class="section-head"><span class="badge">B</span><h2>因子筛选改善：叠加因子能否提升收益</h2></div>

{kpi}

<div class="card">
  <h3>B1 · 单因子筛选改善（每日截面排名 vs 全局排名 双口径）</h3>
  <table>
    <tr><th>#</th><th>因子</th><th>IR</th><th>最优30%片段收益</th><th>截面排名改善</th><th>全局排名改善</th><th>时间分布(均/最大)</th><th>样本</th></tr>
    {cs_rows}
  </table>
  <div class="note">📌 <b>排名口径：</b>截面排名=按买入日分组 rank（排除大盘干扰，可外推）；全局排名=跨全部买点 rank（含时段效应）。差异大者标"时段虚增"。时间分布均值≈30%、最大≤31% = 时间均匀。</div>
</div>

<div class="card">
  <h3>B2 · 双因子 intersect 组合（各自最优方向前 30% 交集）</h3>
  <table>
    <tr><th>#</th><th>组合</th><th>改善</th><th>样本</th></tr>
    {pair_rows}
  </table>
</div>

<div class="card">
  <h3>B3 · 多因子贪心叠加（逐步追加，前 30% 交集）</h3>
  <table>
    <tr><th>步</th><th>追加因子</th><th>本步增量</th><th>累计改善</th></tr>
    {greedy_rows}
  </table>
  <div class="note">📌 累计改善 <b>+{final_imp*100:.2f}pp</b>（片段收益 {pct(M['global_ret']+final_imp)}）。⚠️ 样本递减 + 贪心样本内选择 → 过拟合风险，需样本外/MCP 引擎验证。</div>
</div>

<div class="card">
  <h3>B4 · 时间分布：买点季度分布（全样本）</h3>
  {qbar}
  <div class="note">📌 时间聚集是市场客观现象：全局排名的改善含时段效应，不适合直接做未来交易参考；但可揭示因子盈利对市场环境的依赖（regime/择时参考）。</div>
</div>

<div class="concl">
  <h3>📝 综合结论</h3>
  <ul>
    <li><b>A（基础）</b>：逐笔 vs 连续复利双口径对照（见 A2 note），判断是否存在"假有效"。</li>
    <li><b>B（改善）</b>：单因子改善 {pct(D['single_cs'][0]['cs_improve'], sign=True) if D['single_cs'] else '—'}（最好）→ 双因子 → 贪心 <b>+{final_imp*100:.2f}pp</b>。</li>
    <li><b>口径警示</b>：全局排名改善含时段效应，不可直接用于未来交易过滤。</li>
    <li><b>风险提示</b>：矩阵算法无法避免停牌（片段中途停牌会被 bfill 拆分）；严谨验证请走全A解析 MCP。</li>
    <li><b>免责</b>：以上分析仅供研究参考，不构成投资建议。</li>
  </ul>
</div>

<div class="footer">stock-deep-backtest 技能 · run_full_attribution.py + make_report_html.py · 生成于 2026-08-28</div>
</div></body></html>"""

OUT = f"{BASE}/full_attribution_report_{strat}.html"
open(OUT, "w", encoding="utf-8").write(HTML)
print(f"[OK] {OUT}  {len(HTML):,} 字符")
