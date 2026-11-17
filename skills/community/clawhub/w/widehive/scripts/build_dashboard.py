#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WideHive dashboard generator - turn merged.json into an interactive,
self-contained HTML dashboard (search / sort / drill-down / numeric charts).

Usage:
  python build_dashboard.py --merged <run_dir>/merged.json [--out dashboard.html] [--title "..."]

No external dependencies, no CDN, double-click to open. Vanilla JS only.
"""
import argparse
import html
import json
from datetime import datetime, timezone
from pathlib import Path


def display(v):
    if v is None:
        return ""
    if isinstance(v, (dict, list)):
        return json.dumps(v, ensure_ascii=False)
    return str(v)


def is_number(v):
    if isinstance(v, bool):
        return False
    if isinstance(v, (int, float)):
        return True
    if isinstance(v, str):
        try:
            float(v.replace(",", ""))
            return True
        except ValueError:
            return False
    return False


def num(v):
    return float(v) if not isinstance(v, (int, float)) else float(v)


def esc(s):
    return html.escape(str(s), quote=True)


def bar_chart(rows, field, accent="#0e7490"):
    pts = [(r["target"], num(r["raw"].get(field)))
           for r in rows if is_number(r["raw"].get(field))]
    if len(pts) < 2:
        return None
    pts = sorted(pts, key=lambda x: x[1], reverse=True)[:12]
    w, bh, gap, label_w = 860, 26, 14, 190
    h = len(pts) * (bh + gap) + 40
    vmax = max(v for _, v in pts) or 1
    bars = []
    y = 30
    for name, v in pts:
        bw = max(4, int((w - label_w - 80) * v / vmax))
        bars.append(
            f'<text x="{label_w - 10}" y="{y + bh / 2 + 4}" text-anchor="end" '
            f'class="lbl">{esc(name)}</text>'
            f'<rect x="{label_w}" y="{y}" width="{bw}" height="{bh}" fill="{accent}" opacity="0.85"/>'
            f'<text x="{label_w + bw + 8}" y="{y + bh / 2 + 4}" class="val">{v:g}</text>')
        y += bh + gap
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img">'
            f'<style>.lbl{{font:11.5px "Segoe UI",sans-serif;fill:#5b636e}}'
            f'.val{{font:11px Consolas,monospace;fill:#17191e}}</style>{"".join(bars)}</svg>')


def main():
    ap = argparse.ArgumentParser(description="WideHive dashboard generator")
    ap.add_argument("--merged", required=True, help="path to merged.json")
    ap.add_argument("--out", default=None, help="output html (default alongside merged.json)")
    ap.add_argument("--title", default=None)
    args = ap.parse_args()

    merged_path = Path(args.merged)
    data = json.loads(merged_path.read_text(encoding="utf-8"))
    fields = data.get("fields", [])
    scenario = data.get("scenario", "custom")
    title = args.title or f"WideHive Dashboard — {scenario}"
    out = Path(args.out) if args.out else merged_path.parent / "dashboard.html"

    rows = []
    total_sources = 0
    for rec in data.get("records", []):
        fd = rec.get("fields") if isinstance(rec.get("fields"), dict) else {}
        cells = {f: display(fd.get(f)) for f in fields}
        raw = {f: fd.get(f) for f in fields}
        sources = rec.get("sources") or []
        total_sources += len(sources)
        rows.append({"target": rec.get("target", ""), "cells": cells,
                     "raw": raw, "sources": sources})

    charts = []
    for f in fields:
        non_empty = sum(1 for r in rows if r["raw"].get(f) not in (None, ""))
        numeric = sum(1 for r in rows if is_number(r["raw"].get(f)))
        if non_empty >= 2 and numeric / non_empty >= 0.6:
            svg = bar_chart(rows, f)
            if svg:
                charts.append((f, svg))
        if len(charts) >= 2:
            break

    payload = json.dumps({"fields": fields, "rows": rows},
                         ensure_ascii=False, default=str).replace("</", "<\\/")

    chart_html = ""
    for f, svg in charts:
        chart_html += f"<h3>{esc(f)}</h3><div class='chart'>{svg}</div>"

    doc = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<style>
  :root{--bg:#f4f5f6;--paper:#fcfcfd;--ink:#17191e;--muted:#5b636e;--faint:#8a919c;
    --line:#dde1e6;--line-strong:#c6ccd3;--accent:#0e7490;--accent-deep:#0a5870;--wash:#eef6f8;
    --sans:"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;--mono:Consolas,"Cascadia Code",monospace;}
  *{margin:0;padding:0;box-sizing:border-box;}
  body{background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:14.5px;line-height:1.6;}
  .wrap{max-width:1180px;margin:0 auto;background:var(--paper);border-left:1px solid var(--line);
    border-right:1px solid var(--line);min-height:100vh;padding:0 48px 72px;}
  .kick{display:flex;justify-content:space-between;border-bottom:1px solid var(--ink);
    padding:40px 0 10px;font-family:var(--mono);font-size:11px;letter-spacing:.12em;
    text-transform:uppercase;color:var(--accent-deep);font-weight:600;}
  h1{font-size:30px;font-weight:600;letter-spacing:-.02em;margin:24px 0 20px;}
  .metrics{display:grid;grid-template-columns:repeat(4,1fr);border:1px solid var(--line-strong);margin:0 0 28px;}
  .metric{padding:14px 16px;border-right:1px solid var(--line);}
  .metric:last-child{border-right:none;}
  .metric .k{font-family:var(--mono);font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:var(--faint);}
  .metric .v{font-size:20px;font-weight:600;margin-top:4px;}
  .controls{display:flex;gap:12px;align-items:center;margin:0 0 12px;}
  #q{flex:0 0 320px;padding:8px 12px;border:1px solid var(--line-strong);font:13px var(--sans);
    background:#fff;color:var(--ink);outline:none;}
  #q:focus{border-color:var(--accent);}
  .count{font-family:var(--mono);font-size:11px;color:var(--faint);}
  table{border-collapse:collapse;width:100%;font-size:13px;}
  th{background:#f1f3f5;text-align:left;font-weight:600;font-size:11.5px;color:var(--muted);
    border-bottom:1px solid var(--ink);padding:8px 10px;cursor:pointer;user-select:none;white-space:nowrap;}
  th:hover{color:var(--accent-deep);}
  td{border-bottom:1px solid var(--line);padding:8px 10px;vertical-align:top;}
  tbody tr:hover{background:var(--wash);cursor:pointer;}
  td.tgt{font-weight:600;white-space:nowrap;}
  td.cell{max-width:340px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
  td.cell.num{font-family:var(--mono);font-size:12.5px;}
  #detail{display:none;margin-top:24px;border:1px solid var(--line-strong);padding:20px 24px;background:#fdfdfe;}
  #detail h3{font-size:16px;margin-bottom:10px;}
  #detail dl{display:grid;grid-template-columns:180px 1fr;gap:6px 16px;font-size:13px;}
  #detail dt{color:var(--muted);font-family:var(--mono);font-size:11.5px;padding-top:2px;}
  #detail dd{word-break:break-word;}
  #detail .src{margin-top:14px;padding-top:10px;border-top:1px solid var(--line);}
  #detail .src a{color:var(--accent-deep);font-size:12.5px;display:block;margin-bottom:3px;}
  #detail .close{float:right;border:1px solid var(--line-strong);background:none;padding:2px 10px;
    font:11px var(--mono);color:var(--muted);cursor:pointer;}
  h3{font-size:15px;margin:28px 0 10px;}
  .chart{border:1px solid var(--line);padding:10px;background:#fdfdfe;}
  .chart svg{width:100%;height:auto;}
  footer{margin-top:48px;padding-top:14px;border-top:1px solid var(--line);font-family:var(--mono);
    font-size:10.5px;color:var(--faint);display:flex;justify-content:space-between;}
</style>
</head>
<body>
<div class="wrap">
  <div class="kick"><span>WideHive Dashboard · __SCENARIO__</span><span>__GEN__</span></div>
  <h1>__TITLE__</h1>
  <div class="metrics">
    <div class="metric"><div class="k">Objects</div><div class="v">__NOBJ__</div></div>
    <div class="metric"><div class="k">Fields</div><div class="v">__NF__</div></div>
    <div class="metric"><div class="k">Sources cited</div><div class="v">__NSRC__</div></div>
    <div class="metric"><div class="k">Data date</div><div class="v">__LATEST__</div></div>
  </div>
  <h3>Explore</h3>
  <div class="controls">
    <input id="q" type="search" placeholder="Search objects & fields…" oninput="render()">
    <span class="count" id="cnt"></span>
  </div>
  <table id="tbl"><thead id="thead"></thead><tbody id="tbody"></tbody></table>
  <div id="detail"></div>
  <h3>Distribution</h3>
  __CHARTS__
  <footer><span>generated by WideHive build_dashboard.py · zero LLM</span><span>__SRC__</span></footer>
</div>
<script>
const DATA = __DATA__;
const F = DATA.fields;
let sortKey = null, sortDir = 1, selected = null;
const NUM = f => { const vs = DATA.rows.map(r => r.raw[f]).filter(v => v !== null && v !== "" && v !== undefined);
  return vs.length > 0 && vs.every(v => !isNaN(parseFloat(v))); };
function disp(v){ return (v === null || v === undefined || v === "") ? "—" : v; }
function render(){
  const q = document.getElementById("q").value.toLowerCase();
  let rows = DATA.rows.map((r,i)=>({r,i}));
  if(q) rows = rows.filter(({r}) => (r.target + " " + Object.values(r.cells).join(" "))
    .toLowerCase().includes(q));
  if(sortKey){
    const numeric = NUM(sortKey);
    rows.sort((a,b)=>{
      let x = a.r.raw[sortKey], y = b.r.raw[sortKey];
      if(x === null || x === undefined || x === "") return 1;
      if(y === null || y === undefined || y === "") return -1;
      if(numeric){ x = parseFloat(x); y = parseFloat(y); return (x-y)*sortDir; }
      return String(x).localeCompare(String(y))*sortDir;
    });
  }
  const tb = document.getElementById("tbody");
  tb.innerHTML = rows.map(({r,i}) =>
    `<tr onclick="showDetail(${i})"><td class="tgt">${esc(r.target)}</td>` +
    F.map(f => `<td class="cell${NUM(f)?" num":""}">${esc(String(disp(r.cells[f])).slice(0,160))}</td>`).join("") +
    `</tr>`).join("");
  document.getElementById("cnt").textContent = rows.length + " / " + DATA.rows.length + " objects";
}
function showDetail(i){
  const r = DATA.rows[i];
  const d = document.getElementById("detail");
  d.style.display = "block";
  d.innerHTML = `<button class="close" onclick="this.parentNode.style.display='none'">close</button>` +
    `<h3>${esc(r.target)}</h3><dl>` +
    F.map(f => `<dt>${esc(f)}</dt><dd>${esc(String(disp(r.cells[f])))}</dd>`).join("") +
    `</dl>` + (r.sources && r.sources.length ?
      `<div class="src"><b style="font-size:12px">Sources</b>` +
      r.sources.map(s => `<a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.title || s.url)}</a>`).join("") +
      `</div>` : "");
  d.scrollIntoView({behavior:"smooth", block:"nearest"});
}
function init(){
  const th = document.getElementById("thead");
  th.innerHTML = `<th data-k="__TARGETKEY__">Object</th>` +
    F.map(f => `<th data-k="${esc(f)}">${esc(f)}${NUM(f)?" ▾":""}</th>`).join("");
  th.querySelectorAll("th").forEach(el => el.onclick = () => {
    const k = el.dataset.k;
    if(sortKey === k) sortDir *= -1; else { sortKey = k; sortDir = 1; }
    render();
  });
  render();
}
init();
</script>
</body>
</html>"""

    latest = max((r.get("fetched_at", "") for rec in data.get("records", [])
                  for r in [rec]), default="")
    doc = (doc.replace("__TITLE__", esc(title))
              .replace("__SCENARIO__", esc(scenario))
              .replace("__GEN__", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
              .replace("__NOBJ__", str(len(rows)))
              .replace("__NF__", str(len(fields)))
              .replace("__NSRC__", str(total_sources))
              .replace("__LATEST__", esc(latest or "—"))
              .replace("__TARGETKEY__", esc("target"))
              .replace("__CHARTS__", chart_html or "<p class='muted'>No numeric field detected for charts.</p>")
              .replace("__SRC__", esc(str(merged_path)))
              .replace("__DATA__", payload))

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    print(json.dumps({"dashboard": str(out), "objects": len(rows),
                      "numeric_charts": [f for f, _ in charts]},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
