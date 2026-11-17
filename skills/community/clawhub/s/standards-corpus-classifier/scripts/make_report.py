# -*- coding: utf-8 -*-
"""
标准语料分类可视化 HTML 报告生成器（自包含 / 离线可用）。

读取 classify_standards.py 产出的 standards_categorized.csv，
生成含统计卡片、领域分布条形图、年份分布图、级别/类型占比，
以及可展开领域明细的 HTML 报告（无外部 CDN 依赖，可直接双击打开）。

用法:
    python make_report.py <CSV> --title "北京市地方标准(DB11)" --out report.html
依赖: 仅标准库 (csv / argparse / pathlib / datetime / collections)
"""
import csv, sys, argparse
from collections import Counter
from pathlib import Path
from datetime import datetime

PALETTE = ["#2f6df0", "#16a34a", "#d97706", "#dc2626", "#7c3aed", "#0891b2",
           "#db2777", "#65a30d", "#ea580c", "#0d9488", "#9333ea", "#ca8a04",
           "#2563eb", "#059669", "#e11d48", "#4f46e5", "#0e7490", "#b45309",
           "#475569", "#0ea5e9"]

COLS = ["领域", "级别", "归属", "标准类型", "年份", "标准号", "名称", "子文件夹"]


def pct(n, d):
    return (100.0 * n / d) if d else 0.0


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def color_for(i):
    return PALETTE[i % len(PALETTE)]


def domain_bars(by_domain):
    items = by_domain.most_common()
    maxn = items[0][1] if items else 1
    out = []
    for i, (dom, n) in enumerate(items):
        w = pct(n, maxn)
        c = color_for(i)
        out.append(
            f'<div class="bar-row">'
            f'<div class="bar-label" title="{esc(dom)}">{esc(dom)}</div>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{w:.2f}%;background:{c}"></div>'
            f'<span class="bar-val">{n}</span></div>'
            f'</div>'
        )
    return "\n".join(out)


def year_bars(by_year):
    years = sorted(by_year.keys())
    maxn = max(by_year.values()) if by_year else 1
    out = []
    for y in years:
        n = by_year[y]
        h = pct(n, maxn)
        out.append(
            f'<div class="ycol">'
            f'<div class="yval">{n}</div>'
            f'<div class="ytrack"><div class="yfill" style="height:{h:.2f}%;background:#2f6df0"></div></div>'
            f'<div class="ylabel">{esc(y)}</div>'
            f'</div>'
        )
    return "\n".join(out)


def mini_bars(counter, total):
    items = counter.most_common()
    maxn = items[0][1] if items else 1
    out = []
    for i, (k, n) in enumerate(items):
        w = pct(n, maxn)
        c = color_for(i)
        out.append(
            f'<div class="mbar-row">'
            f'<div class="mbar-label">{esc(k)}</div>'
            f'<div class="mbar-track"><div class="mbar-fill" style="width:{w:.2f}%;background:{c}"></div></div>'
            f'<div class="mbar-val">{n} ({pct(n,total):.1f}%)</div>'
            f'</div>'
        )
    return "\n".join(out)


def accordion(by_domain, rows_by_domain):
    out = []
    for i, (dom, n) in enumerate(by_domain.most_common()):
        rows = rows_by_domain[dom]
        c = color_for(i)
        rows.sort(key=lambda r: r.get("标准号", ""))
        body = ['<table class="dtab"><thead><tr>'
                '<th>标准号</th><th>名称</th><th>类型</th><th>年份</th></tr></thead><tbody>']
        for r in rows:
            body.append(
                f'<tr><td class="mono">{esc(r.get("标准号",""))}</td>'
                f'<td>{esc(r.get("名称",""))}</td>'
                f'<td>{esc(r.get("标准类型",""))}</td>'
                f'<td>{esc(r.get("年份",""))}</td></tr>'
            )
        body.append('</tbody></table>')
        out.append(
            f'<details class="acc">'
            f'<summary><span class="dot" style="background:{c}"></span>'
            f'{esc(dom)} <span class="acc-n">({n})</span></summary>'
            f'<div class="acc-body">{"".join(body)}</div>'
            f'</details>'
        )
    return "\n".join(out)


def year_table(by_year, rows_by_year):
    """单个可折叠区块 + 紧凑表格：年份 / 份数 / 主要领域(前3)。默认收起，不占篇幅。"""
    body = []
    for y in sorted(by_year.keys()):
        rows = rows_by_year[y]
        n = len(rows)
        top = Counter(r["领域"] for r in rows).most_common(3)
        top_str = "、".join(f"{esc(d)} {c}" for d, c in top)
        body.append(
            f'<tr><td class="mono">{esc(y)}</td><td>{n}</td>'
            f'<td class="sub">{top_str}</td></tr>'
        )
    return (
        '<details class="acc"><summary>按年份浏览（点击展开明细）</summary>'
        '<div class="acc-body"><table class="dtab"><thead><tr>'
        '<th>年份</th><th>份数</th><th>主要领域（前 3）</th></tr></thead><tbody>'
        + "".join(body) + '</tbody></table></div></details>'
    )


def main():
    ap = argparse.ArgumentParser(description="标准语料可视化 HTML 报告生成器")
    ap.add_argument("csv", help="standards_categorized.csv 路径")
    ap.add_argument("--title", default="标准语料分类报告")
    ap.add_argument("--out", default="report.html")
    args = ap.parse_args()

    rows = []
    with open(args.csv, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    total = len(rows)
    if total == 0:
        sys.exit("CSV 无数据: " + args.csv)

    by_domain = Counter(r["领域"] for r in rows)
    by_year = Counter(r["年份"] for r in rows)
    by_level = Counter(r["级别"] for r in rows)
    by_type = Counter(r["标准类型"] for r in rows)
    by_belong = Counter(r["归属"] for r in rows)

    rows_by_domain = {}
    for r in rows:
        rows_by_domain.setdefault(r["领域"], []).append(r)
    rows_by_year = {}
    for r in rows:
        rows_by_year.setdefault(r["年份"], []).append(r)

    n_dom = len(by_domain)
    years_sorted = sorted(by_year.keys())
    year_span = f"{years_sorted[0]}–{years_sorted[-1]}" if years_sorted else "—"
    main_level = by_level.most_common(1)[0][0] if by_level else "—"
    main_belong = by_belong.most_common(1)[0][0] if by_belong else "—"
    n_rec = by_type.get("推荐性", 0)
    n_mand = by_type.get("强制性", 0)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(args.title)} · 分类可视化报告</title>
<style>
:root{{--bg:#f5f7fb;--card:#ffffff;--ink:#1f2937;--sub:#6b7280;--line:#e5e7eb;--accent:#2f6df0;}}
*{{box-sizing:border-box;}}
body{{margin:0;background:var(--bg);color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
  line-height:1.55;}}
.wrap{{max-width:1120px;margin:0 auto;padding:28px 20px 60px;}}
header h1{{margin:0 0 4px;font-size:24px;}}
header .sub{{color:var(--sub);font-size:14px;}}
.cards{{display:flex;flex-wrap:wrap;gap:14px;margin:22px 0;}}
.card{{flex:1 1 160px;background:var(--card);border:1px solid var(--line);border-radius:12px;
  padding:16px 18px;box-shadow:0 1px 3px rgba(0,0,0,.04);}}
.card .k{{color:var(--sub);font-size:13px;}}
.card .v{{font-size:26px;font-weight:700;margin-top:4px;}}
.card .x{{font-size:12px;color:var(--sub);margin-top:2px;}}
section{{background:var(--card);border:1px solid var(--line);border-radius:12px;
  padding:20px 22px;margin:18px 0;box-shadow:0 1px 3px rgba(0,0,0,.04);}}
section h2{{margin:0 0 16px;font-size:17px;}}
.bar-row{{display:flex;align-items:center;gap:10px;margin:7px 0;}}
.bar-label{{width:170px;flex:none;text-align:right;font-size:13px;color:var(--ink);
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}}
.bar-track{{position:relative;flex:1;background:#eef1f6;border-radius:6px;height:22px;}}
.bar-fill{{height:100%;border-radius:6px;min-width:2px;}}
.bar-val{{position:absolute;right:8px;top:0;line-height:22px;font-size:12px;font-weight:600;color:#1f2937;}}
.ychart{{display:flex;align-items:flex-end;gap:6px;height:230px;overflow-x:auto;padding-bottom:4px;}}
.ycol{{display:flex;flex-direction:column;align-items:center;flex:1 1 auto;min-width:34px;}}
.yval{{font-size:11px;color:var(--sub);height:16px;}}
.ytrack{{width:24px;flex:1;display:flex;align-items:flex-end;background:#eef1f6;border-radius:5px 5px 0 0;}}
.yfill{{width:100%;border-radius:5px 5px 0 0;min-height:2px;}}
.ylabel{{font-size:11px;color:var(--sub);margin-top:4px;}}
.two{{display:flex;gap:20px;flex-wrap:wrap;}}
.two>div{{flex:1 1 300px;}}
.mbar-row{{display:flex;align-items:center;gap:10px;margin:6px 0;}}
.mbar-label{{width:120px;flex:none;font-size:13px;text-align:right;}}
.mbar-track{{flex:1;background:#eef1f6;border-radius:6px;height:18px;}}
.mbar-fill{{height:100%;border-radius:6px;min-width:2px;}}
.mbar-val{{width:130px;flex:none;font-size:12px;color:var(--sub);}}
.acc{{border:1px solid var(--line);border-radius:10px;margin:8px 0;overflow:hidden;background:#fcfdff;}}
.acc summary{{cursor:pointer;padding:12px 16px;font-weight:600;font-size:14px;list-style:none;}}
.acc summary::-webkit-details-marker{{display:none;}}
.acc summary .dot{{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:8px;vertical-align:middle;}}
.acc-n{{color:var(--sub);font-weight:400;margin-left:6px;}}
.acc-body{{padding:0 16px 14px;}}
.dtab{{width:100%;border-collapse:collapse;font-size:13px;}}
.dtab th,.dtab td{{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line);}}
.dtab th{{color:var(--sub);font-weight:600;position:sticky;top:0;background:#fcfdff;}}
.dtab .mono{{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;white-space:nowrap;}}
footer{{color:var(--sub);font-size:12px;margin-top:24px;line-height:1.7;}}
.pill{{display:inline-block;background:#eef2ff;color:#2f6df0;border-radius:999px;padding:2px 10px;font-size:12px;margin-right:6px;}}
</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>{esc(args.title)} · 分类可视化报告</h1>
  <div class="sub">生成时间：{now} ｜ 数据源：standards_categorized.csv（由 standards-corpus-classifier 技能产出）</div>
</header>

<div class="cards">
  <div class="card"><div class="k">标准总数</div><div class="v">{total}</div><div class="x">份 PDF</div></div>
  <div class="card"><div class="k">领域数</div><div class="v">{n_dom}</div><div class="x">个分类</div></div>
  <div class="card"><div class="k">年份跨度</div><div class="v" style="font-size:20px">{year_span}</div><div class="x">{len(years_sorted)} 个年份</div></div>
  <div class="card"><div class="k">主要级别</div><div class="v" style="font-size:20px">{esc(main_level)}</div><div class="x">归属：{esc(main_belong)}</div></div>
  <div class="card"><div class="k">强制 / 推荐</div><div class="v" style="font-size:20px">{n_mand} / {n_rec}</div><div class="x">占比 {pct(n_mand,total):.0f}% / {pct(n_rec,total):.0f}%</div></div>
</div>

<section>
  <h2>领域分布</h2>
  {domain_bars(by_domain)}
</section>

<section>
  <h2>年份分布</h2>
  <div class="ychart">{year_bars(by_year)}</div>
</section>

<section>
  <h2>按年份浏览</h2>
  {year_table(by_year, rows_by_year)}
</section>

<section>
  <div class="two">
    <div>
      <h2>级别占比</h2>
      {mini_bars(by_level, total)}
    </div>
    <div>
      <h2>归属占比</h2>
      {mini_bars(by_belong, total)}
    </div>
  </div>
</section>

<section>
  <h2>领域明细（点击展开）</h2>
  {accordion(by_domain, rows_by_domain)}
</section>

<footer>
  <p><span class="pill">流程</span>下载标准 PDF → 按文件名关键词自动归类至 <code>pdfs/01_领域/</code> 子文件夹 → 生成 <code>standards_categorized.csv</code> → 渲染本可视化报告。</p>
  <p>分类基于文件名中的「标准代号前缀（级别/归属）」与「标准名称关键词（领域）」自动归并，未逐份审读全文；跨领域标准按首位命中落类。引擎：standards-corpus-classifier 技能。</p>
</footer>
</div>
</body>
</html>"""

    out_path = Path(args.out)
    out_path.write_text(html, encoding="utf-8")
    print(f"报告已生成: {out_path} （{total} 条，{n_dom} 领域，{year_span}）")


if __name__ == "__main__":
    main()
