#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把评分结果 JSON 渲染为 HTML 投资价值报告（单文件、离线可用、深色金融风）

用法:
    python build_report.py --result result.json --output report.html
    python build_report.py --result result.json --output report.html --css ../assets/report.css

图表全部用内联 SVG 绘制，不依赖任何 CDN 或外部资源。
"""

import argparse
import base64
import html
import json
import math
import sys
from pathlib import Path

DIM_NAME = {"Q": "基本面", "G": "成长性", "V": "估值",
            "F": "资金面", "T": "技术面", "N": "消息面"}
DIM_ORDER = ["Q", "G", "V", "F", "T", "N"]

GRADE_CLASS = {"A+": "ap", "A": "a", "B+": "bp", "B": "b", "C": "c", "D": "d"}
ALLOC_COLORS = ["#58a6ff", "#f85149", "#ffa657", "#a371f7", "#56d364",
                "#39c5cf", "#e3b341", "#db61a2"]


def esc(s):
    return html.escape(str(s)) if s is not None else ""


def score_color(v):
    if v is None:
        return "#8b949e"
    if v >= 80:
        return "#ff6b6b"
    if v >= 70:
        return "#ffa657"
    if v >= 60:
        return "#58a6ff"
    if v >= 50:
        return "#8b949e"
    if v >= 40:
        return "#56d364"
    return "#2ea043"


def fmt(v, suffix="", digits=2):
    if v is None:
        return "—"
    if isinstance(v, (int, float)):
        return f"{v:.{digits}f}{suffix}" if isinstance(v, float) else f"{v}{suffix}"
    return f"{v}{suffix}"


def pct_cls(v):
    if v is None:
        return "flat"
    return "up" if v > 0 else ("down" if v < 0 else "flat")


# ---------------------------------------------------------------- 图表

def radar_svg(dims, size=210):
    """六维雷达图，返回 SVG 字符串"""
    if any(dims.get(k) is None for k in DIM_ORDER):
        return '<div class="empty">部分维度数据不足<br>暂不绘制完整雷达图</div>'
    cx = cy = size / 2
    R = size / 2 - 34
    n = len(DIM_ORDER)
    pts = []

    def pt(i, r):
        ang = -math.pi / 2 + i * 2 * math.pi / n
        return cx + r * math.cos(ang), cy + r * math.sin(ang)

    out = [f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}" '
           f'xmlns="http://www.w3.org/2000/svg">']

    # 网格
    for level in (0.25, 0.5, 0.75, 1.0):
        ring = [pt(i, R * level) for i in range(n)]
        poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in ring)
        op = 0.9 if level == 1.0 else 0.4
        out.append(f'<polygon points="{poly}" fill="none" stroke="#30363d" '
                   f'stroke-width="1" opacity="{op}"/>')
    # 轴线
    for i in range(n):
        x, y = pt(i, R)
        out.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" '
                   f'stroke="#30363d" stroke-width="1"/>')

    # 数据多边形
    vals = [max(0.0, min(100.0, float(dims.get(k, 0)))) / 100.0 for k in DIM_ORDER]
    poly_pts = [pt(i, R * vals[i]) for i in range(n)]
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in poly_pts)
    color = score_color(sum(float(dims.get(k, 0)) for k in DIM_ORDER) / n)
    out.append(f'<polygon points="{poly}" fill="{color}" fill-opacity="0.22" '
               f'stroke="{color}" stroke-width="1.8" stroke-linejoin="round"/>')
    for x, y in poly_pts:
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="{color}"/>')

    # 标签
    for i, key in enumerate(DIM_ORDER):
        lx, ly = pt(i, R + 17)
        anchor = "middle"
        if lx > cx + 4:
            anchor = "start"
        elif lx < cx - 4:
            anchor = "end"
        out.append(f'<text x="{lx:.1f}" y="{ly + 4:.1f}" text-anchor="{anchor}" '
                   f'fill="#8b949e" font-size="10.5" '
                   f'font-family="-apple-system,PingFang SC,Microsoft YaHei,sans-serif">'
                   f'{DIM_NAME[key]}</text>')
    out.append("</svg>")
    return "".join(out)


def temp_color(v):
    if v >= 80:
        return "#f85149"
    if v >= 65:
        return "#ffa657"
    if v >= 40:
        return "#58a6ff"
    if v >= 25:
        return "#56d364"
    return "#2ea043"


def gauge_svg(temp, width=168, height=118):
    """半圆仪表盘：大盘温度。数值与刻度内联进 SVG，避免绝对定位错位。"""
    if temp is None:
        return '<div class="empty">市场数据不足<br>暂不计算温度</div>'
    cx, cy, r = width / 2, height - 24, 62
    t = max(0.0, min(100.0, float(temp)))
    c = temp_color(t)
    out = [f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
           f'xmlns="http://www.w3.org/2000/svg">']

    def arc_pt(v, rr=r):
        ang = math.pi * (1 - v / 100.0)
        return cx + rr * math.cos(ang), cy - rr * math.sin(ang)

    x0, y0 = arc_pt(0)
    x1, y1 = arc_pt(100)
    # 底轨（从最左 0 到最右 100 的上半圆）
    out.append(f'<path d="M {x0:.1f} {y0:.1f} A {r} {r} 0 0 1 {x1:.1f} {y1:.1f}" '
               f'fill="none" stroke="#30363d" stroke-width="9" stroke-linecap="round"/>')
    # 数值弧（半圆最大 180°，large-arc-flag 恒为 0，不能按 temp>50 翻转）
    if t > 0:
        xv, yv = arc_pt(t)
        out.append(f'<path d="M {x0:.1f} {y0:.1f} A {r} {r} 0 0 1 {xv:.1f} {yv:.1f}" '
                   f'fill="none" stroke="{c}" stroke-width="9" stroke-linecap="round"/>')
        out.append(f'<circle cx="{xv:.1f}" cy="{yv:.1f}" r="4.5" fill="{c}" '
                   f'stroke="#0d1117" stroke-width="2"/>')
    # 量程刻度：左 0，右 100
    lx0, ly0 = arc_pt(0, r + 11)
    lx1, ly1 = arc_pt(100, r + 11)
    out.append(f'<text x="{lx0 + 2:.1f}" y="{ly0 + 4:.1f}" text-anchor="start" '
               f'fill="#6e7681" font-size="10" '
               f'font-family="-apple-system,PingFang SC,Microsoft YaHei,sans-serif">0</text>')
    out.append(f'<text x="{lx1 - 2:.1f}" y="{ly1 + 4:.1f}" text-anchor="end" '
               f'fill="#6e7681" font-size="10" '
               f'font-family="-apple-system,PingFang SC,Microsoft YaHei,sans-serif">100</text>')
    # 中央数值
    out.append(f'<text x="{cx}" y="{cy - 5:.1f}" text-anchor="middle" fill="{c}" '
               f'font-size="30" font-weight="700" '
               f'font-family="-apple-system,PingFang SC,Microsoft YaHei,sans-serif">{t:.0f}</text>')
    out.append(f'<text x="{cx}" y="{cy + 19:.1f}" text-anchor="middle" fill="#8b949e" '
               f'font-size="11" '
               f'font-family="-apple-system,PingFang SC,Microsoft YaHei,sans-serif">市场温度</text>')
    out.append("</svg>")
    return "".join(out)


def alloc_svg(segments, width=760, height=30):
    """横向堆叠条形图：资产配置占比"""
    total = sum(v for _, v in segments) or 1.0
    out = [f'<svg viewBox="0 0 {width} {height}" width="100%" height="{height}" '
           f'preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">']
    x = 0.0
    for i, (label, val) in enumerate(segments):
        w = val / total * width
        color = ALLOC_COLORS[i % len(ALLOC_COLORS)]
        out.append(f'<rect x="{x:.2f}" y="0" width="{w:.2f}" height="{height}" '
                   f'fill="{color}"/>')
        if w > 46:
            out.append(f'<text x="{x + w / 2:.1f}" y="{height / 2 + 4:.1f}" '
                       f'text-anchor="middle" fill="#fff" font-size="11.5" '
                       f'font-weight="600" '
                       f'font-family="-apple-system,PingFang SC,sans-serif">'
                       f'{esc(label)} {val:.1f}%</text>')
        x += w
    out.append("</svg>")
    return "".join(out)


# ---------------------------------------------------------------- 片段

def render_valuation(s):
    v = s.get('valuation', {})
    values = ''.join(f'<div>{label}<b>{fmt(v.get(key))}</b></div>' for label, key in
                     [('保守公允价值', 'fair_value_bear'), ('基准公允价值', 'fair_value_base'), ('乐观公允价值', 'fair_value_bull')])
    ref = s.get('reference_prices', {})
    refs = (f'<div class="report-sub">独立参考：技术压力位 {fmt(ref.get("technical_resistance"))} · '
            f'券商目标价 {fmt(ref.get("consensus_target"))} '
            f'{esc(ref.get("consensus_horizon", ""))}（均不参与公允价值计算）</div>')
    assumptions = ''.join(f'<li><b>{esc(k)}</b>：{esc(val)}</li>' for k, val in v.get('assumptions', {}).items())
    sources = ''.join(f'<li>{esc(x)}</li>' for x in v.get('sources', []))
    inputs = esc(json.dumps(v.get('scenario_inputs', {}), ensure_ascii=False, indent=2))
    audit = esc(json.dumps(s.get('sources', {}), ensure_ascii=False, indent=2))
    missing = ''.join(f'<li>{esc(k)}：{esc(", ".join(d.get("missing", []))) or "无"}</li>' for k, d in s.get('data_quality', {}).items())
    imputed = ''.join(f'<li>{esc(k)}：按总体期望分插补 {esc(", ".join(d.get("imputed", [])))}（第三方来源缺失，非公司表现差）</li>'
                      for k, d in s.get('data_quality', {}).items() if d.get('imputed'))
    neutral = ''.join(f'<li>{esc(k)}：{esc(", ".join(d.get("neutral", [])))} 缺失，按中性默认分兜底计价'
                      f'（真实覆盖率 {d.get("coverage", 0):.0f}%，兜底不提高覆盖率）</li>'
                      for k, d in s.get('data_quality', {}).items() if d.get('neutral'))
    notes = ''.join(f'<li>{esc(n)}</li>' for n in s.get('notes', []))
    div = s.get('dividend')
    dividend = ''
    if div:
        if div.get('enabled'):
            dividend = (f'<li>股息子项已启用：利差 {fmt(div.get("spread_pct"), "pp", 2)} 计入估值维度，'
                        f'盈利覆盖 {fmt(div.get("coverage"), "×", 2)} 计入基本面维度，不重复计分</li>')
        else:
            dividend = '<li>股息子项未启用（缺有效无风险利率或现金分红），不进分母，不影响本次评分</li>'
    return (f'<div class="valuation-panel"><div class="report-sub">方法 {esc(v.get("method"))} · '
            f'估值日 {esc(v.get("valuation_as_of"))} · 当前公允价值，非未来12个月目标价</div>'
            f'<div class="sc-prices">{values}</div>{refs}'
            f'<details><summary>查看情景假设与输入来源</summary><ul>{assumptions}</ul>'
            f'<pre>{inputs}</pre><ul>{sources}</ul></details>'
            f'<details><summary>查看数据缺口与审计记录</summary><ul>{missing}{imputed}{neutral}{dividend}{notes}</ul><pre>{audit}</pre></details></div>')


def render_stock_card(s):
    dims = s["dims"]
    wts = s.get("weights", {})
    gcls = GRADE_CLASS.get(s["grade"], "b")
    total = s["total"]

    dims_html = "".join(
        f'<div class="dim-row">'
        f'<span class="dim-name">{DIM_NAME[k]}</span>'
        f'<span class="dim-bar"><i style="width:{max(0, min(100, dims.get(k) or 0)):.0f}%;'
        f'background:{score_color(dims.get(k, 0))}"></i></span>'
        f'<span class="dim-val">{fmt(dims.get(k), digits=0)}</span>'
        f'<span class="dim-w">{s.get("data_quality", {}).get(k, {}).get("coverage", 0):.0f}%</span>'
        f'</div>' for k in DIM_ORDER)

    upside = s.get("upside_pct")
    badge_hold = ('<span class="badge badge-hold">持仓</span>'
                  if s.get("holding") else
                  '<span class="badge badge-watch">自选</span>')

    div = s.get('dividend')
    if div and div.get('enabled'):
        div_html = (f'<div>股息率<b>{fmt(div.get("yield_pct"), "%", 2)}</b></div>'
                    f'<div>股息利差<b>{fmt(div.get("spread_pct"), "pp", 2)}'
                    f'（{fmt(div.get("spread_score"), digits=0)}分）</b></div>'
                    f'<div>盈利覆盖<b>{fmt(div.get("coverage"), "×", 2)}'
                    f'（{fmt(div.get("coverage_score"), digits=0)}分）</b></div>')
    elif div:
        div_html = (f'<div>股息率<b>{fmt(div.get("yield_pct"), "%", 2)}</b></div>'
                    f'<div>股息子项<b>未启用</b></div>')
    else:
        div_html = ''

    prices = (
        f'<div>现价<b>{fmt(s.get("price"))}</b></div>'
        f'<div>成本价<b>{fmt(s.get("cost_price"))}</b></div>'
        f'<div>基准公允价值<b>{fmt(s.get("target_price"))}</b></div>'
        f'<div>上行空间<b class="{pct_cls(upside)}">'
        f'{"—" if upside is None else f"{upside:+.1f}%"}</b></div>'
        f'<div>技术支撑参考<b>{fmt(s.get("stop_loss"))}</b></div>'
        f'<div>安全边际<b>{fmt(s.get("margin_of_safety_pct"), "%", 1)}</b></div>'
        f'<div>交易环境分<b>{fmt(s.get("trading_score"), digits=1)}</b></div>'
        f'{div_html}'
    )

    pnl = s.get("pnl_pct")
    pnl_html = (f'<div>持仓盈亏<b class="{pct_cls(pnl)}">'
                f'{"—" if pnl is None else f"{pnl:+.2f}%"}</b></div>'
                if s.get("holding") else "")

    def box(cls, title, items):
        if not items:
            return ""
        lis = "".join(f"<li>{esc(i)}</li>" for i in items)
        return (f'<div class="point-box {cls}"><h4>{title}</h4>'
                f'<ul>{lis}</ul></div>')

    points = (
        box("box-key", "关键信息", s.get("key_points"))
        + box("box-risk", "风险与问题", s.get("risks"))
        + box("box-flag", "红线提示", s.get("red_flags"))
        + box("box-risk", "评级数据门槛", s.get("rating_blockers"))
    )
    points_html = f'<div class="points">{points}</div>' if points else ""

    tgt_note = s.get("target_note") or ""
    note_html = (f'<div style="margin-top:10px;font-size:11.5px;color:#6e7681">'
                 f'{esc(tgt_note)}</div>' if tgt_note else "")

    return f"""
<div class="stock-card">
  <div class="sc-head">
    <div>
      <div class="sc-name">{esc(s.get('name'))} {badge_hold}</div>
      <div class="sc-meta">{esc(s.get('code'))} · {esc(s.get('industry') or '未分类')}
        · 模型档位 {esc(s.get('profile'))} · 权重版本 {esc(s.get('weights_version', 'legacy'))}<br>
        价值权重 Q/G/V：{fmt(wts.get('Q'), digits=2)} / {fmt(wts.get('G'), digits=2)} / {fmt(wts.get('V'), digits=2)}</div>
    </div>
    <div class="sc-score">
      <b style="color:{score_color(total)}">{fmt(total, digits=1)}</b>
      <span>/ 100</span>
      <div style="margin-top:5px">
        <span class="badge badge-{gcls}">{esc(s['grade'])} {esc(s['action'])}</span>
      </div>
      <div style="font-size:11px;color:#6e7681;margin-top:5px">
        单票上限 {fmt(s.get('position_cap'), '%')}</div>
    </div>
  </div>
  <div class="sc-body">
    <div class="sc-radar">{radar_svg(dims)}</div>
    <div class="sc-dims"><div class="report-sub">右列为有效数据覆盖率；资金/技术/消息不计入价值总分</div>{dims_html}</div>
  </div>
  <div class="sc-prices">{prices}{pnl_html}</div>
  {note_html}
  {render_valuation(s)}
  {points_html}
</div>"""


def render_delta_table(deltas):
    if not deltas:
        return '<div class="empty">首次运行，暂无历史评分可对比</div>'
    rows = []
    for d in deltas:
        if d.get("new"):
            rows.append(
                f'<tr><td class="name-cell">{esc(d["name"])}</td>'
                f'<td colspan="4" class="flat">本次新增标的，无历史基准</td></tr>')
            continue
        if d.get("comparable") is False:
            rows.append(f'<tr><td>{esc(d["name"])}</td><td colspan="4">{esc(d.get("reason"))}</td></tr>')
            continue
        dv = d["total_delta"]
        cls = pct_cls(dv)
        dims = " ".join(
            f'<span style="color:{pct_cls(x["delta"])};margin-right:9px">'
            f'{x["dim"]}{x["delta"]:+.0f}</span>' for x in d.get("top_dims", []))
        hint = (f'<span style="color:#f85149">{esc(d["action_hint"])}</span>'
                if d.get("action_hint") else "")
        if 'weight_effect' in d:
            hint += (f'<div class="report-sub">数据影响 {fmt(d.get("data_effect"))} · '
                     f'调权影响 {fmt(d.get("weight_effect"))} · 风险/舍入 {fmt(d.get("risk_and_rounding_effect"))}<br>'
                     f'{esc(d.get("weights_version_change"))}</div>')
        rows.append(
            f'<tr><td class="name-cell">{esc(d["name"])}</td>'
            f'<td class="num">{d["prev_total"]}</td>'
            f'<td class="num {cls}">{dv:+.1f}</td>'
            f'<td>{esc(d["trend"])}</td>'
            f'<td>{esc(d["grade_change"])} {dims} {hint}</td></tr>')
    return (f'<table><thead><tr><th>标的</th><th class="num">上次</th>'
            f'<th class="num">Δ</th><th>趋势</th><th>主要归因</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table>')


def render_alloc(alloc, stocks):
    if alloc.get("status") == "blocked":
        reasons = ''.join(f'<li>{esc(w)}</li>' for w in alloc.get('warnings', []))
        return f'<div class="card"><b>暂不生成配置权重</b><ul class="blocked-reasons">{reasons}</ul></div>'
    targets = alloc.get("targets", {})
    name_of = {s["code"]: s.get("name") for s in stocks}
    cash = alloc.get("cash_pct", 0)

    segs = [(name_of.get(c, c), v) for c, v in targets.items()]
    if cash > 0.05:
        segs.append(("现金", cash))
    if alloc.get('other_assets_pct', 0) > 0:
        segs.append(('其他资产', alloc['other_assets_pct']))

    legend = "".join(
        f'<span><i class="dot" style="background:{ALLOC_COLORS[i % len(ALLOC_COLORS)]}"></i>'
        f'{esc(l)} {v:.1f}%</span>'
        for i, (l, v) in enumerate(segs))

    actions = alloc.get("actions", [])
    arows = []
    for a in actions:
        cls = {"加仓": "up", "减仓": "down", "维持": "flat"}.get(a["action"], "flat")
        dv = "—" if a["delta"] is None else f'{a["delta"]:+.1f}pct'
        arows.append(
            f'<tr><td class="name-cell">{esc(a["name"])}</td>'
            f'<td class="num">{fmt(a.get("current"), "%", 1)}</td>'
            f'<td class="num">{a["target"]}%</td>'
            f'<td class="num {cls}">{dv}</td>'
            f'<td class="{cls}">{esc(a["action"])}</td></tr>')

    warn_html = ""
    if alloc.get("warnings"):
        lis = "".join(f"<li>{esc(w)}</li>" for w in alloc["warnings"])
        warn_html = (f'<div class="notice"><b>配置约束提示</b><ul>{lis}</ul></div>')

    watch = alloc.get("watch_only") or []
    watch_html = ""
    if watch:
        items = " · ".join(f'{esc(x["name"])}（{fmt(x["total"], digits=1)} / {esc(x["grade"])}）'
                           for x in watch)
        watch_html = (f'<div class="notice" style="background:rgba(88,166,255,.08);'
                      f'border-color:rgba(88,166,255,.25)">'
                      f'<b style="color:#58a6ff">自选未持仓</b>：{items}'
                      f'<div style="margin-top:5px;font-size:11.5px;color:#8b949e">'
                      f'以上为自选池中尚未建仓的标的，未计入配置权重。</div></div>')

    return f"""
<div class="card">
  <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;
              margin-bottom:14px">
    <div style="font-size:13px;color:#8b949e">
      用户政策约束后的权益预算 <b style="color:#e6edf3">{alloc.get('requested_equity_pct')}%</b>
    </div>
    <div style="font-size:13px;color:#8b949e">
      权益参考配置 <b style="color:#e6edf3">{alloc.get('equity_pct', 0):.1f}%</b>
      · 现金 <b style="color:#e6edf3">{cash}%</b>
      · 其他资产 <b>{alloc.get('other_assets_pct', 0)}%</b>
    </div>
  </div>
  <div class="alloc-chart" style="height:auto;background:none">
    {alloc_svg(segs)}
  </div>
  <div class="alloc-legend" style="margin-bottom:16px">{legend}</div>
  <table><thead><tr><th>标的</th><th class="num">当前权重</th>
    <th class="num">目标权重</th><th class="num">调整</th><th>动作</th></tr></thead>
    <tbody>{"".join(arows)}</tbody></table>
  <div style="font-size:11.5px;color:#6e7681;margin-top:9px">
    当前与目标权重均以总资产为分母；差额仅供复核，不是买卖指令。</div>
  {warn_html}
  {watch_html}
</div>"""


# ---------------------------------------------------------------- 主渲染

def render(result, css):
    mk = result.get("market", {})
    stocks = result.get("stocks", [])
    alloc = result.get("allocation", {})
    date = result.get("date") or "未提供分析日期"
    temp = mk.get("temperature", 0)
    icon_path = Path(__file__).resolve().parent.parent / 'assets' / 'icon.png'
    logo = ('<img class="report-logo" alt="价值分析图标" src="data:image/png;base64,'
            + base64.b64encode(icon_path.read_bytes()).decode('ascii') + '">') if icon_path.exists() else ''
    demo_notice = '<div class="notice"><b>合成测试数据，仅用于验证功能；不是实际持仓或市场分析。</b></div>' if result.get('synthetic') else ''
    if result.get('weight_warnings'):
        demo_notice += '<div class="notice">' + '；'.join(esc(x) for x in result['weight_warnings']) + '</div>'

    cards = "".join(render_stock_card(s) for s in stocks)

    # 评分总览表
    rows = []
    for s in stocks:
        gcls = GRADE_CLASS.get(s["grade"], "b")
        pnl = s.get("pnl_pct")
        rows.append(
            f'<tr>'
            f'<td><div class="name-cell">{esc(s["name"])}</div>'
            f'<div class="code-cell">{esc(s["code"])}</div></td>'
            f'<td><div class="score-cell">'
            f'<span class="score-bar"><i style="width:{s["total"] or 0:.0f}%;'
            f'background:{score_color(s["total"])}"></i></span>'
            f'<span class="score-val" style="color:{score_color(s["total"])}">'
            f'{fmt(s["total"], digits=1)}</span></div></td>'
            f'<td><span class="badge badge-{gcls}">{esc(s["grade"])}</span></td>'
            f'<td>{esc(s["action"])}</td>'
            f'<td class="num">{fmt(s.get("price"))}</td>'
            f'<td class="num">{fmt(s.get("target_price"))}</td>'
            f'<td class="num {pct_cls(s.get("upside_pct"))}">'
            f'{"—" if s.get("upside_pct") is None else f"{s['upside_pct']:+.1f}%"}</td>'
            f'<td class="num">{fmt(s.get("stop_loss"))}</td>'
            f'<td class="num {pct_cls(pnl)}">'
            f'{"—" if pnl is None else f"{pnl:+.2f}%"}</td>'
            f'</tr>')

    overview = (f'<table><thead><tr><th>标的</th><th style="min-width:130px">投资价值评分</th>'
                f'<th>评级</th><th>建议</th><th class="num">现价</th>'
                f'<th class="num">基准公允价值</th><th class="num">空间</th>'
                f'<th class="num">支撑参考</th><th class="num">持仓盈亏</th>'
                f'</tr></thead><tbody>{"".join(rows)}</tbody></table>')

    mk_comment = mk.get("comment", "")
    mk_notes = mk.get("notes") or []
    mk_cov = mk.get("coverage")
    mk_scope = (f'可用 {len(mk.get("used") or [])} 项 · 覆盖率 {mk_cov:.0f}%'
                if mk_cov is not None else '未提供')
    notes_html = ""
    if mk_notes:
        notes_html = ("<div style='margin-top:9px;font-size:11.5px;color:#6e7681'>"
                      + "；".join(esc(n) for n in mk_notes) + "</div>")

    deltas = result.get("deltas")
    delta_sec = ""
    if deltas is not None:
        delta_sec = (f'<section><div class="sec-title">评分变化追踪'
                     f'<span class="hint">对比上一快照</span></div>'
                     f'<div class="card">{render_delta_table(deltas)}</div></section>')

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>自选与持仓投资价值评分报告 · {esc(date)}</title>
<style>{css}</style>
</head>
<body>
<div class="wrap">
  {demo_notice}

  <div class="report-head">
    <div>
      <div class="report-title">{logo}<span>自选与持仓投资价值评分报告</span></div>
      <div class="report-sub">
        覆盖 {len(stocks)} 只标的 · 价值评分与交易环境分开 · 基本面情景估值
      </div>
    </div>
    <div class="head-meta">
      数据日期：{esc(date)}<br>
      生成时间：{esc(result.get('_generated', ''))}<br>
      评分模型：{esc(result.get('model_version', '旧版'))}
    </div>
  </div>

  <section>
    <div class="sec-title">大盘研判<span class="hint">描述市场环境，不自动决定仓位</span></div>
    <div class="card">
      <div class="temp-row">
        <div class="temp-gauge">
          {gauge_svg(temp)}
        </div>
        <div class="temp-info">
          <div class="temp-state">{esc(mk.get('state'))}市场
            <span style="font-size:13px;color:#8b949e;font-weight:400">
              · {esc(mk.get('tone'))}</span></div>
          <div class="temp-desc">{esc(mk_comment)}</div>
          <div class="temp-metrics">
            <div>权益预算<b>由用户风险政策确定</b></div>
            <div>现金缓冲<b>至少 5%，并满足资金需求</b></div>
            <div>配置基调<b style="font-size:13px">{esc(mk.get('tone'))}</b></div>
            <div>温度口径<b style="font-size:13px">{esc(mk_scope)}</b></div>
          </div>
          {notes_html}
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="sec-title">评分总览<span class="hint">0–100 分，质量/成长/估值加权；NR 为暂不评级</span></div>
    <div class="card">{overview}</div>
  </section>

  {delta_sec}

  <section>
    <div class="sec-title">个股详情<span class="hint">雷达图为六维得分</span></div>
    {cards}
  </section>

  <section>
    <div class="sec-title">资产配置建议
      <span class="hint">单票/行业上限约束下的目标权重</span></div>
    {render_alloc(alloc, stocks)}
  </section>

  <div class="report-foot">
    <div>数据来源：以各标的展开后的来源与审计记录为准。
      数据日期与分析日可能不同；财报实际值与经营预测假设分开标注。</div>
    <div>价值分使用质量/成长/估值的行业相对权重并归一化；资金/技术/消息独立形成交易环境分。
      缺失项不赠送中性分，覆盖率低于70%不出维度分。参数尚未完成历史收益校准。</div>
    <div class="disclaimer">
      <b>风险提示：</b>{esc(result.get('disclaimer', ''))}
      本报告的评分、公允价值、技术参考位与配置参考均由量化模型基于公开数据生成，
      存在数据延迟与模型局限，<b>不构成任何投资建议，不承诺收益</b>。
      投资有风险，入市需谨慎，请独立判断并自行承担投资决策后果。
    </div>
  </div>

</div>
</body>
</html>"""


def main():
    ap = argparse.ArgumentParser(description="生成 HTML 投资价值评分报告")
    ap.add_argument("--result", required=True, help="评分结果 JSON")
    ap.add_argument("--output", required=True, help="输出 HTML 路径")
    ap.add_argument("--css", default=None, help="样式表路径，默认 ../assets/report.css")
    args = ap.parse_args()

    result = json.loads(Path(args.result).read_text(encoding="utf-8"))
    css_path = Path(args.css) if args.css else \
        Path(__file__).resolve().parent.parent / "assets" / "report.css"
    css = css_path.read_text(encoding="utf-8")

    from datetime import datetime
    result["_generated"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    Path(args.output).write_text(render(result, css), encoding="utf-8")
    print(f"[OK] 报告已生成: {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
