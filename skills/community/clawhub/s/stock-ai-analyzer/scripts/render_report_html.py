#!/usr/bin/env python3
"""Render an a-stock-analyzer Markdown report as a self-contained HTML page.

Markdown→HTML rendering, CSS theming and text-preservation validation come
from the shared ``html_report`` package (synced into ``scripts/_shared/``).
This file owns only the analyzer-specific bits: evidence loading, the chart
payload extraction (PE/PB/PS valuation bands + financial trends), and the
JS that draws those charts.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

SCRIPT_ROOT = Path(__file__).resolve().parent
_BUNDLED_SHARED = SCRIPT_ROOT / "_shared"
_DEV_SHARED = SCRIPT_ROOT.parents[2] / "shared"
sys.path.insert(0, str(_BUNDLED_SHARED if _BUNDLED_SHARED.exists() else _DEV_SHARED))

from html_report import ChartHook, HtmlReportBuilder, list_themes  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render a Markdown stock report to static HTML.")
    parser.add_argument("--input", "-i", required=True, help="Markdown report path, e.g. reports/report_600519.md.")
    parser.add_argument("--output", "-o", default=None, help="HTML output path. Defaults to input path with .html suffix.")
    parser.add_argument("--evidence", default=None, help="Evidence JSON path. Defaults to sibling evidence_<code>.json when input is report_<code>.md.")
    parser.add_argument("--title", default=None, help="HTML document title.")
    parser.add_argument("--theme", default="default", choices=list_themes(), help="HTML style theme. default = Claude-UI; print = monochrome serif, A4-friendly.")
    parser.add_argument("--no-validate", action="store_true", help="Skip Markdown text preservation validation entirely.")
    parser.add_argument("--strict", action="store_true", help="Abort on text-preservation mismatch instead of warning. Off by default so content changes never break HTML generation.")
    return parser


# --------------------------------------------------------------------------- #
# Evidence loading + chart payload extraction (analyzer-specific)
# --------------------------------------------------------------------------- #
def default_evidence_path(input_path: Path) -> Optional[Path]:
    match = re.match(r"^report_(.+)$", input_path.stem)
    if not match:
        return None
    candidate = input_path.with_name(f"evidence_{match.group(1)}.json")
    return candidate if candidate.exists() else None


def load_evidence(path: Optional[Path]) -> dict:
    if path is None or not path.exists():
        return {"metadata": {"missing": True, "source": str(path) if path is not None else ""}, "datasets": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def _dataset(evidence: dict, name: str) -> Any:
    entry = (evidence.get("datasets") or {}).get(name)
    if isinstance(entry, dict):
        if entry.get("ok") is False:
            return None
        return entry.get("data", entry)
    return entry


def _to_number(value: Any) -> Optional[float]:
    try:
        num = float(value)
    except (TypeError, ValueError):
        return None
    return num if num == num else None  # drop NaN


def _resolve_name(evidence: dict, ts_code: str) -> Optional[str]:
    company = _dataset(evidence, "company")
    if isinstance(company, dict):
        for key in ("name", "com_name"):
            if company.get(key):
                return str(company[key])
    return None


def extract_chart_payload(evidence: dict, source_path: Optional[Path]) -> Dict[str, Any]:
    """Pull the chart datasets from evidence into a compact, JS-ready payload."""
    band_data = _dataset(evidence, "valuation-band")
    bands = (band_data or {}).get("bands") if isinstance(band_data, dict) else {}
    val_series = (band_data or {}).get("series") if isinstance(band_data, dict) else []
    val_series = val_series if isinstance(val_series, list) else []
    ts_code = (band_data or {}).get("ts_code") if isinstance(band_data, dict) else None

    # Financial trends: merge income (revenue / 归母净利) with financial (ROE / margins / yoy) by end_date.
    income = _dataset(evidence, "income")
    income = income if isinstance(income, list) else []
    financial = _dataset(evidence, "financial")
    financial = financial if isinstance(financial, list) else []
    fin_by_end = {str(r.get("end_date")): r for r in financial if isinstance(r, dict) and r.get("end_date")}
    trends_by_end: Dict[str, dict] = {}
    for row in income:
        if not isinstance(row, dict) or not row.get("end_date"):
            continue
        end_date = str(row["end_date"])
        fin = fin_by_end.get(end_date, {})
        trends_by_end[end_date] = {
            "end_date": end_date,
            "revenue": _to_number(row.get("revenue") or row.get("total_revenue")),
            "n_income": _to_number(row.get("n_income_attr_p")),
            "tr_yoy": _to_number(fin.get("tr_yoy") or fin.get("or_yoy")),
            "netprofit_yoy": _to_number(fin.get("netprofit_yoy")),
            "roe": _to_number(fin.get("roe") or fin.get("roe_waa")),
            "grossprofit_margin": _to_number(fin.get("grossprofit_margin")),
            "netprofit_margin": _to_number(fin.get("netprofit_margin")),
        }
    trends = sorted(trends_by_end.values(), key=lambda r: r["end_date"])[-8:]

    return {
        "metadata": {
            "source": str(source_path) if source_path is not None else "",
            "missing": bool((evidence.get("metadata") or {}).get("missing")),
            "ts_code": ts_code,
            "name": _resolve_name(evidence, ts_code or ""),
            "latest_trade_date": (band_data or {}).get("latest_trade_date") if isinstance(band_data, dict) else None,
        },
        "valuation_bands": bands if isinstance(bands, dict) else {},
        "valuation_series": val_series,
        "financial_trends": trends,
    }


# --------------------------------------------------------------------------- #
# UI decoration: promote "核心判断" section into a hero summary card.
# --------------------------------------------------------------------------- #
PILL_RULES_JS = r"""
(function () {
  const root = document.getElementById("report-body");
  if (!root) return;
  const pillRules = [
    { re: /^(成长股|成熟龙头|红利价值)$/, cls: "pill" },
    { re: /^(强连接|核心标的)$/, cls: "pill neg" },
    { re: /^(弱连接|边缘受益)$/, cls: "pill warn" },
    { re: /^(无连接|脱离主线)$/, cls: "pill" },
    { re: /^(深度低估|合理偏低)$/, cls: "pill pos" },
    { re: /^(偏高|透支|极度乐观)$/, cls: "pill neg" },
    { re: /^(合理|合理定价)$/, cls: "pill" },
    { re: /^(强|高)$/, cls: "pill neg" },
    { re: /^(中)$/, cls: "pill warn" },
    { re: /^(弱|低)$/, cls: "pill pos" },
    { re: /^(基准|乐观|压力|Bull|Bear|Base)$/, cls: "pill violet" }
  ];
  root.querySelectorAll("td").forEach(td => {
    const trimmed = td.textContent.trim();
    if (!trimmed || td.children.length > 0) return;
    for (const rule of pillRules) {
      if (rule.re.test(trimmed)) {
        td.innerHTML = `<span class="${rule.cls}">${trimmed}</span>`;
        return;
      }
    }
  });
})();
"""


SUMMARY_HERO_JS = r"""
(function () {
  const root = document.getElementById("report-body");
  if (!root) return;
  const summaryH = Array.from(root.querySelectorAll("h2, h3")).find(h => h.textContent.trim().startsWith("核心判断"));
  if (!summaryH) return;
  const card = document.createElement("aside");
  card.className = "summary-card";
  const label = document.createElement("div");
  label.className = "summary-label";
  label.textContent = summaryH.textContent.trim();
  card.appendChild(label);
  const stopTags = summaryH.tagName === "H2" ? /^H[12]$/ : /^H[123]$/;
  const collected = [];
  let cur = summaryH.nextElementSibling;
  while (cur && !stopTags.test(cur.tagName)) {
    const next = cur.nextElementSibling;
    const txt = cur.textContent.trim();
    if ((cur.tagName === "P" || cur.tagName === "UL") && txt && !/^-{3,}$/.test(txt)) {
      cur.classList.add("summary-body");
      collected.push(cur);
    } else {
      cur.remove();
    }
    cur = next;
  }
  collected.forEach(node => card.appendChild(node));
  summaryH.replaceWith(card);
  collected.forEach(p => {
    p.innerHTML = p.innerHTML.replace(/([+\-])(\d+(?:\.\d+)?)(%|pct|倍|x|分位)/g,
      (_, sign, num, unit) => `<span class="${sign === "+" ? "num-pos" : "num-neg"}">${sign}${num}${unit}</span>`);
  });
})();
"""


# --------------------------------------------------------------------------- #
# Chart drawing JS: valuation bands + financial trends.
# Runs inside builder-supplied IIFE; reads its slice from __payload.
# --------------------------------------------------------------------------- #
STOCK_CHARTS_JS = r"""
const charts = __payload || {};
const root = document.getElementById("report-body");
if (!root) return;
const NS = "http://www.w3.org/2000/svg";

const svgEl = (name, attrs) => {
  const el = document.createElementNS(NS, name);
  Object.entries(attrs || {}).forEach(([k, v]) => el.setAttribute(k, v));
  return el;
};
const svgText = (x, y, text, anchor, color, size) => {
  const el = svgEl("text", { x, y, "text-anchor": anchor || "start", fill: color || "var(--ink-4)", "font-size": size || 11 });
  el.textContent = text;
  return el;
};
const fmtDate = v => String(v || "").replace(/^(\d{4})(\d{2})(\d{2})$/, "$1-$2-$3");
const fmtNum = (v, d) => Number.isFinite(v) ? v.toFixed(d == null ? (Math.abs(v) >= 100 ? 1 : Math.abs(v) >= 10 ? 2 : 2) : d) : "—";
const fmtYi = v => Number.isFinite(v) ? (v / 1e8).toFixed(2) + "亿" : "—";
const findHeading = (texts) => {
  const list = Array.from(root.querySelectorAll("h2, h3, h4"));
  for (const t of texts) { const h = list.find(e => e.textContent.includes(t)); if (h) return h; }
  return null;
};
const insertAfterBlock = (heading, node) => { heading.after(node); };
const mkCard = (cls, title, subtitle) => {
  const card = document.createElement("article");
  card.className = cls;
  if (title) { const t = document.createElement("div"); t.className = "chart-title"; t.textContent = title; card.appendChild(t); }
  if (subtitle) { const s = document.createElement("div"); s.className = "chart-subtitle"; s.textContent = subtitle; card.appendChild(s); }
  return card;
};
const mkLegend = (items) => {
  const legend = document.createElement("div");
  legend.className = "legend";
  items.forEach(([label, color]) => {
    const span = document.createElement("span");
    span.style.setProperty("--legend-color", color);
    span.textContent = label;
    legend.appendChild(span);
  });
  return legend;
};
const mkTooltip = (card) => {
  const tip = document.createElement("div");
  tip.style.cssText = "position:absolute;background:rgba(15,23,42,0.92);color:#f1f5f9;padding:8px 12px;border-radius:8px;font-size:12px;line-height:1.5;pointer-events:none;opacity:0;transition:opacity .15s ease;z-index:100;white-space:nowrap;box-shadow:0 4px 12px rgba(0,0,0,0.2);";
  card.style.position = "relative";
  card.appendChild(tip);
  return tip;
};
const moveTip = (tip, card, e) => {
  const r = card.getBoundingClientRect();
  tip.style.left = Math.min(e.clientX - r.left + 12, r.width - tip.offsetWidth - 8) + "px";
  tip.style.top = Math.max(8, e.clientY - r.top - tip.offsetHeight - 12) + "px";
};

drawValuationBands();
drawFinancialTrends();

function drawValuationBands() {
  const series = charts.valuation_series || [];
  const bands = charts.valuation_bands || {};
  if (series.length < 2) return;
  const heading = findHeading(["估值快照与历史分位", "估值快照", "历史分位", "估值模式"]);
  if (!heading) return;

  const specs = [
    { key: "pe_ttm", title: "PE-TTM 估值带" },
    { key: "pb", title: "PB 估值带" },
    { key: "ps_ttm", title: "PS-TTM 估值带" }
  ];
  const grid = document.createElement("div");
  grid.className = "chart-grid";
  specs.forEach(spec => {
    const card = buildBandTimeCard(spec.key, spec.title);
    if (card) grid.appendChild(card);
  });
  if (grid.children.length) insertAfterBlock(heading, grid);

  function buildBandTimeCard(key, title) {
    const pts = series
      .map((r, i) => ({ i, date: String(r.trade_date || ""), v: Number(r[key]) }))
      .filter(p => Number.isFinite(p.v) && p.v > 0);
    if (pts.length < 2) return null;
    const band = bands[key] || {};
    const windows = band.windows || {};
    const wkey = ["5y", "3y", "1y"].find(k => windows[k] && windows[k].sample_size);
    const win = wkey ? windows[wkey] : null;
    const current = Number.isFinite(Number(band.current)) ? Number(band.current) : pts[pts.length - 1].v;
    const pctText = win && Number.isFinite(win.current_percentile) ? ` · 分位 ${win.current_percentile.toFixed(0)}%` : "";
    const metricName = title.split(" ")[0];
    const card = mkCard("chart-card", title, `当前 ${fmtNum(current)}${pctText}`);
    const tip = mkTooltip(card);

    const W = 480, H = 220, pad = { l: 38, r: 40, t: 12, b: 28 };
    const usableW = W - pad.l - pad.r, usableH = H - pad.t - pad.b;
    const svg = svgEl("svg", { viewBox: `0 0 ${W} ${H}`, role: "img" });

    const levels = win ? [win.min, win.p25, win.median, win.p75, win.max].filter(Number.isFinite) : [];
    const vals = pts.map(p => p.v).concat(levels);
    let lo = Math.min(...vals), hi = Math.max(...vals);
    if (lo === hi) { lo -= 1; hi += 1; }
    const sp = hi - lo; lo -= sp * 0.06; hi += sp * 0.06;
    const n = pts.length;
    const x = i => pad.l + (n <= 1 ? usableW / 2 : i / (n - 1) * usableW);
    const y = v => pad.t + (hi - v) / (hi - lo) * usableH;

    if (win && Number.isFinite(win.p25) && Number.isFinite(win.p75)) {
      svg.appendChild(svgEl("rect", { x: pad.l, y: y(win.p75).toFixed(2), width: usableW, height: Math.max(1, y(win.p25) - y(win.p75)).toFixed(2), class: "band-box" }));
    }
    const bandLines = win ? [
      ["max", win.max, "var(--neg)"],
      ["P75", win.p75, "var(--ink-4)"],
      ["中位", win.median, "var(--ink-3)"],
      ["P25", win.p25, "var(--ink-4)"],
      ["min", win.min, "var(--pos)"]
    ].filter(l => Number.isFinite(l[1])) : [];
    bandLines.forEach(item => {
      const v = item[1], color = item[2];
      svg.appendChild(svgEl("line", { x1: pad.l, x2: W - pad.r, y1: y(v).toFixed(2), y2: y(v).toFixed(2), stroke: color, "stroke-width": 1, "stroke-dasharray": "3 3", opacity: 0.65 }));
      svg.appendChild(svgText(W - pad.r + 3, y(v) + 3, fmtNum(v), "start", color, 9));
    });

    const d = pts.map((p, i) => `${i === 0 ? "M" : "L"} ${x(i).toFixed(2)} ${y(p.v).toFixed(2)}`).join(" ");
    svg.appendChild(svgEl("path", { d, class: "series-line", style: "stroke: var(--accent)" }));
    const last = pts[pts.length - 1];
    svg.appendChild(svgEl("circle", { cx: x(n - 1).toFixed(2), cy: y(last.v).toFixed(2), r: 3.5, fill: "var(--orange)", stroke: "#fff", "stroke-width": 1.5 }));

    const ticks = 4;
    for (let t = 0; t <= ticks; t++) {
      const idx = Math.round(t / ticks * (n - 1));
      svg.appendChild(svgText(x(idx), H - pad.b + 14, fmtDate(pts[idx].date).slice(0, 7), "middle", "var(--ink-4)", 9));
    }
    svg.appendChild(svgEl("line", { x1: pad.l, x2: W - pad.r, y1: pad.t + usableH, y2: pad.t + usableH, class: "axis" }));

    const cursor = svgEl("line", { x1: 0, x2: 0, y1: pad.t, y2: pad.t + usableH, stroke: "var(--ink-4)", "stroke-width": 1, opacity: 0 });
    svg.appendChild(cursor);
    const hit = svgEl("rect", { x: pad.l, y: pad.t, width: usableW, height: usableH, fill: "transparent", style: "cursor:crosshair" });
    hit.addEventListener("mousemove", e => {
      const r = svg.getBoundingClientRect();
      const px = (e.clientX - r.left) / r.width * W;
      let idx = Math.round((px - pad.l) / usableW * (n - 1));
      idx = Math.max(0, Math.min(n - 1, idx));
      const p = pts[idx];
      cursor.setAttribute("x1", x(idx)); cursor.setAttribute("x2", x(idx)); cursor.setAttribute("opacity", "1");
      tip.innerHTML = `<div style="color:#94a3b8;font-size:11px;margin-bottom:2px;">${fmtDate(p.date)}</div><div>${metricName}: ${fmtNum(p.v)}</div>`;
      tip.style.opacity = "1";
      moveTip(tip, card, e);
    });
    hit.addEventListener("mouseleave", () => { cursor.setAttribute("opacity", "0"); tip.style.opacity = "0"; });
    svg.appendChild(hit);

    card.appendChild(svg);
    card.appendChild(mkLegend([[(wkey ? wkey.toUpperCase() : "") + "分位带", "var(--accent-soft)"], ["估值", "var(--accent)"], ["当前", "var(--orange)"]]));
    return card;
  }
}

function drawFinancialTrends() {
  const rows = (charts.financial_trends || []).filter(r => r.end_date);
  if (rows.length < 2) return;
  const heading = findHeading(["成长性与财务质量诊断", "成长性与财务质量", "财务质量诊断", "成长性诊断"]);
  if (!heading) return;

  const labels = rows.map(r => String(r.end_date).replace(/^(\d{4})(\d{2})(\d{2})$/, "$1/$2"));
  const grid = document.createElement("div");
  grid.className = "chart-grid";
  const configs = [
    { title: "营收 / 归母净利 (亿元)", type: "bars", fmt: fmtYi, fields: [
      { key: "revenue", label: "营收", color: "var(--blue)", div: 1e8 },
      { key: "n_income", label: "归母净利", color: "var(--orange)", div: 1e8 } ]},
    { title: "同比增速 (%)", type: "line", fmt: v => fmtNum(v) + "%", fields: [
      { key: "tr_yoy", label: "营收YoY", color: "var(--blue)" },
      { key: "netprofit_yoy", label: "归母YoY", color: "var(--orange)" } ]},
    { title: "盈利能力 (%)", type: "line", fmt: v => fmtNum(v) + "%", fields: [
      { key: "roe", label: "ROE", color: "var(--violet)" },
      { key: "grossprofit_margin", label: "毛利率", color: "var(--pos)" },
      { key: "netprofit_margin", label: "净利率", color: "var(--cyan)" } ]}
  ];
  configs.forEach(cfg => {
    const hasData = cfg.fields.some(f => rows.some(r => Number.isFinite(r[f.key])));
    if (hasData) grid.appendChild(buildTrendCard(cfg, rows, labels));
  });
  if (grid.children.length) insertAfterBlock(heading, grid);

  function buildTrendCard(cfg, rows, labels) {
    const card = mkCard("chart-card", cfg.title, `${labels[0]} – ${labels[labels.length - 1]}`);
    const tip = mkTooltip(card);
    const W = 480, H = 210, pad = { l: 40, r: 14, t: 14, b: 30 };
    const usableW = W - pad.l - pad.r, usableH = H - pad.t - pad.b;
    const svg = svgEl("svg", { viewBox: `0 0 ${W} ${H}`, role: "img" });
    const series = cfg.fields.map(f => ({
      field: f,
      pts: rows.map((r, i) => ({ i, date: labels[i], v: Number.isFinite(r[f.key]) ? r[f.key] / (f.div || 1) : null })).filter(p => Number.isFinite(p.v))
    })).filter(s => s.pts.length);
    if (!series.length) { svg.appendChild(svgText(W / 2, H / 2, "暂无数据", "middle")); card.appendChild(svg); return card; }
    const vals = series.flatMap(s => s.pts.map(p => p.v));
    let lo = Math.min(...vals, 0), hi = Math.max(...vals, 0);
    if (lo === hi) { lo -= 1; hi += 1; }
    const sp = hi - lo; lo -= sp * 0.08; hi += sp * 0.08;
    const n = rows.length;
    const x = i => pad.l + (n <= 1 ? usableW / 2 : (i + 0.5) / n * usableW);
    const y = v => pad.t + (hi - v) / (hi - lo) * usableH;
    for (let i = 0; i <= 4; i++) {
      const gy = pad.t + usableH * i / 4;
      svg.appendChild(svgEl("line", { x1: pad.l, x2: W - pad.r, y1: gy, y2: gy, class: "grid-line" }));
    }
    const y0 = y(0);
    if (y0 >= pad.t && y0 <= pad.t + usableH) svg.appendChild(svgEl("line", { x1: pad.l, x2: W - pad.r, y1: y0, y2: y0, class: "axis" }));

    if (cfg.type === "bars") {
      const groupW = usableW / n, bw = Math.min(18, groupW / (series.length + 0.6));
      series.forEach((s, si) => {
        s.pts.forEach(p => {
          const cx = pad.l + (p.i + 0.5) / n * usableW + (si - (series.length - 1) / 2) * bw;
          const py = y(p.v), barY = p.v >= 0 ? py : y0;
          svg.appendChild(svgEl("rect", { x: (cx - bw / 2).toFixed(2), y: barY.toFixed(2), width: bw.toFixed(2), height: Math.max(1, Math.abs(py - y0)).toFixed(2), fill: s.field.color, rx: 2, opacity: 0.85 }));
        });
      });
    } else {
      series.forEach(s => {
        const d = s.pts.map((p, i) => `${i === 0 ? "M" : "L"} ${x(p.i).toFixed(2)} ${y(p.v).toFixed(2)}`).join(" ");
        svg.appendChild(svgEl("path", { d, class: "series-line", style: `stroke:${s.field.color}` }));
        s.pts.forEach(p => svg.appendChild(svgEl("circle", { cx: x(p.i).toFixed(2), cy: y(p.v).toFixed(2), r: 3, fill: s.field.color, stroke: "#fff", "stroke-width": 1.5 })));
      });
    }

    rows.forEach((r, i) => {
      svg.appendChild(svgText(x(i), H - pad.b + 14, labels[i], "middle", "var(--ink-4)", 9.5));
      const hit = svgEl("rect", { x: (pad.l + i / n * usableW).toFixed(2), y: pad.t, width: (usableW / n).toFixed(2), height: usableH, fill: "transparent", style: "cursor:pointer" });
      hit.addEventListener("mouseenter", () => {
        tip.innerHTML = `<div style="color:#94a3b8;font-size:11px;margin-bottom:2px;">${labels[i]}</div>` +
          cfg.fields.map(f => {
            const raw = r[f.key];
            if (!Number.isFinite(raw)) return "";
            return `<div>${f.label}: ${cfg.fmt(raw)}</div>`;
          }).join("");
        tip.style.opacity = "1";
      });
      hit.addEventListener("mousemove", e => moveTip(tip, card, e));
      hit.addEventListener("mouseleave", () => { tip.style.opacity = "0"; });
      svg.appendChild(hit);
    });
    svg.appendChild(svgText(4, pad.t + 4, cfg.fmt(hi)));
    svg.appendChild(svgText(4, pad.t + usableH, cfg.fmt(lo)));
    card.appendChild(svg);
    card.appendChild(mkLegend(cfg.fields.map(f => [f.label, f.color])));
    return card;
  }
}
"""


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else input_path.with_suffix(".html")
    evidence_path = Path(args.evidence) if args.evidence else default_evidence_path(input_path)
    markdown_text = input_path.read_text(encoding="utf-8")
    title = args.title or input_path.stem
    evidence = load_evidence(evidence_path)
    charts = extract_chart_payload(evidence, evidence_path)
    meta = charts.get("metadata") or {}
    sub_bits = [bit for bit in [meta.get("name"), meta.get("ts_code")] if bit]
    header_sub = " · ".join(sub_bits) if sub_bits else ""
    latest = str(meta.get("latest_trade_date") or "")
    meta_text = header_sub + (" · " + latest if (latest and header_sub) else latest)

    builder = HtmlReportBuilder(title=title, theme=args.theme, meta_text=meta_text)
    builder.add_ui_decoration(PILL_RULES_JS)
    builder.add_ui_decoration(SUMMARY_HERO_JS)
    builder.add_chart_hook(ChartHook(name="stock-charts", payload=charts, js=STOCK_CHARTS_JS))

    validation_warning: Optional[str] = None
    try:
        html_text = builder.render(markdown_text, validate=not args.no_validate)
    except RuntimeError as exc:
        if args.strict or args.no_validate:
            raise
        # Content/format are decoupled: a preservation mismatch is reported as a
        # warning but never blocks HTML output (run with --strict to hard-fail).
        validation_warning = str(exc)
        print(f"warning: {exc}", file=sys.stderr)
        html_text = builder.render(markdown_text, validate=False)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_text, encoding="utf-8")
    print(json.dumps({
        "input": str(input_path),
        "output": str(output_path),
        "evidence": str(evidence_path) if evidence_path is not None else None,
        "theme": args.theme,
        "valuation_series_points": len(charts.get("valuation_series") or []),
        "valuation_bands": sorted((charts.get("valuation_bands") or {}).keys()),
        "financial_periods": len(charts.get("financial_trends") or []),
        "validation_warning": validation_warning,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
