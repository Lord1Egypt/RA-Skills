#!/usr/bin/env python3
"""Render a daily-market-sense Markdown report as a self-contained HTML page.

Markdown→HTML rendering, CSS theming and text-preservation validation come
from the shared ``html_report`` package. This file owns only the
market-sense-specific bits: loading market_data.json / evidence_*.json,
extracting the index K-line + stock K-line + market-trend payloads, and the
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
SKILL_ROOT = SCRIPT_ROOT.parent
DEFAULT_MARKET_DATA = SKILL_ROOT / "reference" / "market_data.json"
INDEX_KLINE_DISPLAY_DAYS = 120

_BUNDLED_SHARED = SCRIPT_ROOT / "_shared"
_DEV_SHARED = SCRIPT_ROOT.parents[2] / "shared"
sys.path.insert(0, str(_BUNDLED_SHARED if _BUNDLED_SHARED.exists() else _DEV_SHARED))

from html_report import ChartHook, HtmlReportBuilder, list_themes  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render a Markdown daily market report to static HTML.")
    parser.add_argument("--input", "-i", required=True, help="Markdown report path, e.g. reports/report_YYYYMMDD.md.")
    parser.add_argument("--output", "-o", default=None, help="HTML output path. Defaults to input path with .html suffix.")
    parser.add_argument("--market-data", default=str(DEFAULT_MARKET_DATA), help="Derived market_data.json path.")
    parser.add_argument("--evidence", default=None, help="Evidence JSON path. Defaults to sibling evidence_YYYYMMDD_utf8.json when input is report_YYYYMMDD.md.")
    parser.add_argument("--title", default=None, help="HTML document title.")
    parser.add_argument("--theme", default="default", choices=list_themes(), help="HTML style theme. default = Claude-UI; print = monochrome serif, A4-friendly.")
    parser.add_argument("--no-validate", action="store_true", help="Skip Markdown text preservation validation.")
    return parser


# --------------------------------------------------------------------------- #
# Data loading (market-sense-specific)
# --------------------------------------------------------------------------- #
def load_market_data(path: Path) -> dict:
    if not path.exists():
        return {
            "metadata": {"missing": True, "source": str(path)},
            "columns": [],
            "records": [],
            "series": {},
            "quality": {"records_available": 0, "has_120_records": False},
        }
    return json.loads(path.read_text(encoding="utf-8"))


def default_evidence_path(input_path: Path) -> Optional[Path]:
    match = re.match(r"^report_(\d{8})$", input_path.stem)
    if not match:
        return None
    return input_path.with_name(f"evidence_{match.group(1)}_utf8.json")


def load_evidence(path: Optional[Path]) -> dict:
    if path is None or not path.exists():
        return {
            "metadata": {"missing": True, "source": str(path) if path is not None else ""},
            "market_trend": {"indices": {}},
        }
    return json.loads(path.read_text(encoding="utf-8"))


def extract_index_kline_payload(evidence: dict, source_path: Optional[Path]) -> Dict[str, Any]:
    indices = ((evidence.get("market_trend") or {}).get("indices") or {})
    payload: Dict[str, Any] = {
        "metadata": {
            "source": str(source_path) if source_path is not None else "",
            "missing": bool((evidence.get("metadata") or {}).get("missing")),
        },
        "indices": {},
    }
    for key in ("shanghai", "chinext"):
        item = indices.get(key) or {}
        records = item.get("kline_records") if isinstance(item, dict) else []
        if isinstance(records, list):
            records = records[-INDEX_KLINE_DISPLAY_DAYS:]
        else:
            records = []
        payload["indices"][key] = {
            "available": bool(item.get("available")) and bool(records),
            "name": item.get("name"),
            "ts_code": item.get("ts_code"),
            "trade_date": item.get("trade_date"),
            "kline_days": item.get("kline_days"),
            "kline_days_requested": item.get("kline_days_requested"),
            "records": records,
        }
    return payload


def extract_stock_kline_payload(evidence: dict, source_path: Optional[Path]) -> Dict[str, Any]:
    raw = evidence.get("stock_kline_records") or {}
    by_ts_code = raw.get("by_ts_code") if isinstance(raw, dict) else {}
    name_to_ts_code = raw.get("name_to_ts_code") if isinstance(raw, dict) else {}
    payload: Dict[str, Any] = {
        "metadata": {
            "source": str(source_path) if source_path is not None else "",
            "missing": bool((evidence.get("metadata") or {}).get("missing")),
            "kline_days_requested": (raw.get("metadata") or {}).get("kline_days_requested") if isinstance(raw, dict) else None,
            "price_adjustment": (raw.get("metadata") or {}).get("price_adjustment") if isinstance(raw, dict) else None,
        },
        "by_ts_code": {},
        "name_to_ts_code": name_to_ts_code if isinstance(name_to_ts_code, dict) else {},
    }
    if not isinstance(by_ts_code, dict):
        return payload
    for ts_code, item in by_ts_code.items():
        if not isinstance(item, dict):
            continue
        records = item.get("records")
        if isinstance(records, list):
            records = records[-INDEX_KLINE_DISPLAY_DAYS:]
        else:
            records = []
        payload["by_ts_code"][str(ts_code)] = {
            "available": bool(item.get("available")) and bool(records),
            "name": item.get("name"),
            "ts_code": item.get("ts_code") or ts_code,
            "trade_date": item.get("trade_date"),
            "price_adjustment": item.get("price_adjustment") or payload["metadata"].get("price_adjustment"),
            "kline_days": item.get("kline_days"),
            "kline_days_requested": item.get("kline_days_requested"),
            "records": records,
        }
    return payload


# --------------------------------------------------------------------------- #
# Skill-specific UI decoration: pill rules + "一句话盘面判断" hero card.
# --------------------------------------------------------------------------- #
PILL_RULES_JS = r"""
(function () {
  const root = document.getElementById("report-body");
  if (!root) return;
  const pillRules = [
    { re: /^高位强势股退潮$/, cls: "pill neg" },
    { re: /^流动性杀跌$/, cls: "pill warn" },
    { re: /^主线内部分歧$/, cls: "pill warn" },
    { re: /^高位趋势$/, cls: "pill" },
    { re: /^高$/, cls: "pill neg" },
    { re: /^中$/, cls: "pill warn" },
    { re: /^低$/, cls: "pill pos" },
    { re: /^领导股$/, cls: "pill" },
    { re: /^弹性股$/, cls: "pill violet" },
    { re: /^启动型$|^持续换手型$|^分歧型$/, cls: "pill" },
    { re: /^[ABC]$/, cls: "pill" }
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
  const summaryH3 = Array.from(root.querySelectorAll("h2,h3")).find(h => h.textContent.trim().startsWith("一句话盘面判断"));
  if (!summaryH3) return;

  const card = document.createElement("aside");
  card.className = "summary-card";
  const label = document.createElement("div");
  label.className = "summary-label";
  label.textContent = summaryH3.textContent.trim();
  card.appendChild(label);

  const collected = [];
  let cur = summaryH3.nextElementSibling;
  while (cur && !/^H[1-6]$/.test(cur.tagName)) {
    const next = cur.nextElementSibling;
    const txt = cur.textContent.trim();
    if (txt && /^[^\dA-Za-z\u4e00-\u9fff]*\d+\./.test(txt)) break;
    if (collected.length >= 3) break;
    if (cur.tagName === "P" && txt && !/^-{3,}$/.test(txt)) {
      cur.classList.add("summary-body");
      collected.push(cur);
    } else {
      cur.remove();
    }
    cur = next;
  }
  collected.forEach(node => card.appendChild(node));
  summaryH3.replaceWith(card);

  collected.forEach(p => {
    let h = p.innerHTML.replace(
      /([+\-])(\d+(?:\.\d+)?)(%|pct|倍)/g,
      (_, sign, num, unit) => {
        const cls = sign === "+" ? "num-pos" : "num-neg";
        return `<span class="${cls}">${sign}${num}${unit}</span>`;
      }
    );
    h = h.replace(/(上证|创业板|半导体设备与材料|电力能源)/g, '<span class="kw">$1</span>');
    p.innerHTML = h;
  });
})();
"""


# --------------------------------------------------------------------------- #
# Chart drawing: index K-lines + stock-table K-lines.
# Reads its payload slice from __payload (set by builder per hook).
# --------------------------------------------------------------------------- #
KLINE_CHARTS_JS = r"""
const payload = __payload.index || {};
const stockPayload = __payload.stocks || {};
const klineDisplayDays = __payload.display_days || 120;
const indices = payload.indices || {};
const stockByCode = stockPayload.by_ts_code || {};
const stockNameIndex = stockPayload.name_to_ts_code || {};
const reportBody = document.getElementById("report-body");
if (!reportBody) return;

const indexConfigs = [
  { key: "shanghai", anchorTexts: ["上证指数趋势判断", "上证指数趋势"], fallbackTitle: "上证指数" },
  { key: "chinext", anchorTexts: ["创业板趋势判断", "创业板指数趋势判断", "创业板指数趋势"], fallbackTitle: "创业板指数" }
];
const stockSectionConfigs = [
  { headingText: "3.3", gridLabel: "module3-leaders" },
  { headingText: "5.1", gridLabel: "module5-capacity-up" },
  { headingText: "5.2", gridLabel: "module5-star-breakout" },
  { headingText: "5.3", gridLabel: "module5-early-limit" }
];

insertIndexKlines();
insertStockTableKlines();

function insertIndexKlines() {
  const prepared = indexConfigs.map(config => {
    const indexData = indices[config.key] || {};
    const rows = normalizeRows(indexData.records).slice(-klineDisplayDays);
    return rows.length ? { ...config, indexData, rows } : null;
  }).filter(Boolean);
  if (!prepared.length) return;

  const anchor = findInsertionAnchor(indexConfigs[0].anchorTexts) || findInsertionAnchor(indexConfigs.flatMap(c => c.anchorTexts));
  if (!anchor) return;

  const grid = document.createElement("div");
  grid.className = "kline-grid";
  prepared.forEach(item => {
    grid.appendChild(buildKlineCard(item.rows, item.indexData, item.fallbackTitle));
  });
  if (anchor.insert === "after") {
    anchor.element.after(grid);
  } else {
    anchor.element.before(grid);
  }
}

function insertStockTableKlines() {
  stockSectionConfigs.forEach(config => {
    const heading = findHeading(config.headingText);
    if (!heading) return;
    const tableWrap = findNextTableWrap(heading);
    if (!tableWrap || tableWrap.dataset.stockKlinesInserted === "1") return;

    const names = extractStockNames(tableWrap);
    const prepared = names.map(name => {
      const stockData = findStockData(name);
      if (!stockData) return null;
      const rows = normalizeRows(stockData.records).slice(-klineDisplayDays);
      return rows.length ? { rows, stockData: { ...stockData, name }, fallbackTitle: name } : null;
    }).filter(Boolean);
    if (!prepared.length) return;

    const grid = document.createElement("div");
    grid.className = `stock-kline-grid stock-kline-grid-${config.gridLabel}`;
    prepared.forEach(item => {
      grid.appendChild(buildKlineCard(item.rows, item.stockData, item.fallbackTitle));
    });
    tableWrap.after(grid);
    tableWrap.dataset.stockKlinesInserted = "1";
  });
}

function findInsertionAnchor(texts) {
  const anchors = reportBody.querySelectorAll("p, h3, h4");
  for (const text of texts) {
    for (const element of anchors) {
      if (!element.textContent.includes(text)) continue;
      const tag = element.tagName.toLowerCase();
      return { element, insert: tag === "h3" || tag === "h4" ? "after" : "before" };
    }
  }
  return null;
}

function findHeading(text) {
  return Array.from(reportBody.querySelectorAll("h3, h4")).find(e => e.textContent.includes(text));
}

function findNextTableWrap(heading) {
  let current = heading.nextElementSibling;
  while (current) {
    if (current.classList && current.classList.contains("table-wrap")) return current;
    if (/^H[234]$/.test(current.tagName || "")) return null;
    current = current.nextElementSibling;
  }
  return null;
}

function extractStockNames(tableWrap) {
  const headers = Array.from(tableWrap.querySelectorAll("thead th")).map(c => normalizeStockName(c.textContent));
  const stockIndex = headers.indexOf("股票");
  if (stockIndex < 0) return [];
  return Array.from(tableWrap.querySelectorAll("tbody tr"))
    .map(row => row.children[stockIndex] ? normalizeStockName(row.children[stockIndex].textContent) : "")
    .filter(Boolean);
}

function findStockData(name) {
  const normalized = normalizeStockName(name);
  const tsCode = stockNameIndex[name] || stockNameIndex[normalized];
  if (!tsCode) return null;
  return stockByCode[tsCode] || null;
}

function normalizeStockName(value) { return String(value || "").replace(/\s+/g, "").trim(); }

function normalizeRows(records) {
  return (Array.isArray(records) ? records : [])
    .map(row => ({
      trade_date: String(row.trade_date || ""),
      open: toNumber(row.open),
      high: toNumber(row.high),
      low: toNumber(row.low),
      close: toNumber(row.close),
      pct_chg: toNumber(row.pct_chg),
      amount: toNumber(row.amount),
      vol: toNumber(row.vol)
    }))
    .filter(row => row.trade_date && [row.open, row.high, row.low, row.close].every(Number.isFinite))
    .sort((a, b) => a.trade_date.localeCompare(b.trade_date));
}

function buildKlineCard(rows, indexData, fallbackTitle) {
  const card = document.createElement("article");
  card.className = "kline-card";
  card.style.position = "relative";

  const title = document.createElement("div");
  title.className = "chart-title";
  title.textContent = `${indexData.name || fallbackTitle} ${klineDisplayDays}日K线`;
  const subtitle = document.createElement("div");
  subtitle.className = "chart-subtitle";
  const first = rows[0];
  const last = rows[rows.length - 1];
  const requested = Number(indexData.kline_days_requested) || klineDisplayDays;
  subtitle.textContent = `${formatDate(first.trade_date)} 至 ${formatDate(last.trade_date)} · ${rows.length}/${requested} 个交易日`;
  card.appendChild(title);
  card.appendChild(subtitle);
  card.appendChild(drawKline(rows, card));

  const legend = document.createElement("div");
  legend.className = "legend";
  [
    ["K线", "var(--neg)"],
    ["MA20", "var(--blue)"],
    ["MA60", "var(--orange)"],
    ["成交金额", "rgba(100,116,139,0.55)"]
  ].forEach(([label, color]) => {
    const span = document.createElement("span");
    span.style.setProperty("--legend-color", color);
    span.textContent = label;
    legend.appendChild(span);
  });
  card.appendChild(legend);
  return card;
}

function drawKline(rows, card) {
  const enriched = rows.map((row, idx) => ({
    ...row, idx,
    ma20: rollingAverage(rows, idx, 20),
    ma60: rollingAverage(rows, idx, 60)
  }));
  const width = 560;
  const height = 340;
  const pad = { left: 48, right: 14, top: 12, bottom: 24 };
  const usableW = width - pad.left - pad.right;
  const amountPanelH = 64;
  const panelGap = 16;
  const priceH = height - pad.top - pad.bottom - amountPanelH - panelGap;
  const amountTop = pad.top + priceH + panelGap;
  const amountBottom = amountTop + amountPanelH;
  const svg = svgEl("svg", { viewBox: `0 0 ${width} ${height}`, role: "img" });

  const allPrices = enriched.flatMap(row => [row.high, row.low, row.ma20, row.ma60]).filter(Number.isFinite);
  let min = Math.min(...allPrices);
  let max = Math.max(...allPrices);
  if (min === max) { min -= 1; max += 1; }
  const span = max - min;
  min -= span * 0.05;
  max += span * 0.05;

  const x = idx => pad.left + (enriched.length <= 1 ? usableW / 2 : idx / (enriched.length - 1) * usableW);
  const y = price => pad.top + (max - price) / (max - min) * priceH;
  const candleWidth = Math.max(2, Math.min(8, usableW / Math.max(enriched.length, 1) * 0.62));
  const amounts = enriched.map(row => row.amount).filter(value => Number.isFinite(value) && value > 0);
  const maxAmount = amounts.length ? Math.max(...amounts) : 1;
  const amountY = value => amountBottom - (value / maxAmount) * amountPanelH;

  for (let i = 0; i <= 4; i += 1) {
    const gy = pad.top + priceH * i / 4;
    svg.appendChild(svgEl("line", { x1: pad.left, x2: width - pad.right, y1: gy, y2: gy, class: "grid-line" }));
  }
  svg.appendChild(svgEl("line", { x1: pad.left, x2: width - pad.right, y1: pad.top + priceH, y2: pad.top + priceH, class: "axis" }));
  svg.appendChild(svgEl("line", { x1: pad.left, x2: width - pad.right, y1: amountBottom, y2: amountBottom, class: "axis" }));
  svg.appendChild(svgEl("line", { x1: pad.left, x2: width - pad.right, y1: amountTop, y2: amountTop, class: "grid-line", opacity: 0.55 }));

  const tooltip = document.createElement("div");
  tooltip.style.cssText = "position:absolute;background:rgba(15,23,42,0.92);color:#f1f5f9;padding:8px 12px;border-radius:8px;font-size:12px;line-height:1.5;pointer-events:none;opacity:0;transition:opacity 0.15s ease;z-index:100;white-space:nowrap;box-shadow:0 4px 12px rgba(0,0,0,0.2);";
  card.appendChild(tooltip);

  enriched.forEach(row => {
    const px = x(row.idx);
    const up = row.close >= row.open;
    const cls = up ? "kline-candle-up" : "kline-candle-down";
    if (Number.isFinite(row.amount) && row.amount > 0) {
      const barTop = amountY(row.amount);
      const amountCls = up ? "amount-bar-up" : "amount-bar-down";
      svg.appendChild(svgEl("rect", {
        x: (px - candleWidth / 2).toFixed(2),
        y: barTop.toFixed(2),
        width: candleWidth.toFixed(2),
        height: Math.max(1, amountBottom - barTop).toFixed(2),
        class: `amount-bar ${amountCls}`,
        rx: 1
      }));
    }
    const bodyTop = y(Math.max(row.open, row.close));
    const bodyBottom = y(Math.min(row.open, row.close));
    const bodyHeight = Math.max(1, bodyBottom - bodyTop);
    svg.appendChild(svgEl("line", {
      x1: px.toFixed(2), x2: px.toFixed(2),
      y1: y(row.high).toFixed(2), y2: y(row.low).toFixed(2),
      class: `kline-wick ${cls}`
    }));
    svg.appendChild(svgEl("rect", {
      x: (px - candleWidth / 2).toFixed(2),
      y: bodyTop.toFixed(2),
      width: candleWidth.toFixed(2),
      height: bodyHeight.toFixed(2),
      class: cls, rx: 1, opacity: 0.88
    }));
    const hit = svgEl("rect", {
      x: (px - Math.max(candleWidth, 4) / 2).toFixed(2),
      y: pad.top,
      width: Math.max(candleWidth, 4).toFixed(2),
      height: amountBottom - pad.top,
      fill: "transparent", stroke: "none",
      style: "cursor:pointer"
    });
    hit.addEventListener("mouseenter", () => {
      tooltip.innerHTML = [
        `<div style="color:#94a3b8;font-size:11px;margin-bottom:2px;">${formatDate(row.trade_date)}</div>`,
        `<div>开: ${formatNumber(row.open)} 高: ${formatNumber(row.high)}</div>`,
        `<div>低: ${formatNumber(row.low)} 收: ${formatNumber(row.close)}</div>`,
        `<div>涨跌幅: ${formatPercent(row.pct_chg)} · 成交额: ${formatAmount(row.amount)}</div>`
      ].join("");
      tooltip.style.opacity = "1";
    });
    hit.addEventListener("mousemove", event => {
      const r = card.getBoundingClientRect();
      tooltip.style.left = `${Math.min(event.clientX - r.left + 12, r.width - tooltip.offsetWidth - 8)}px`;
      tooltip.style.top = `${Math.max(8, event.clientY - r.top - tooltip.offsetHeight - 12)}px`;
    });
    hit.addEventListener("mouseleave", () => { tooltip.style.opacity = "0"; });
    svg.appendChild(hit);
  });

  drawMaLine(enriched, "ma20", "var(--blue)");
  drawMaLine(enriched, "ma60", "var(--orange)");

  svg.appendChild(svgText(4, pad.top + 4, formatNumber(max), "start", "var(--text-tertiary)"));
  svg.appendChild(svgText(4, pad.top + priceH, formatNumber(min), "start", "var(--text-tertiary)"));
  svg.appendChild(svgText(4, amountTop + 12, "成交金额", "start", "var(--text-tertiary)"));
  svg.appendChild(svgText(4, amountTop + 28, formatAmount(maxAmount), "start", "var(--text-tertiary)"));
  return svg;

  function drawMaLine(items, key, color) {
    const points = items.filter(row => Number.isFinite(row[key]));
    if (!points.length) return;
    const d = points.map((row, idx) => `${idx === 0 ? "M" : "L"} ${x(row.idx).toFixed(2)} ${y(row[key]).toFixed(2)}`).join(" ");
    svg.appendChild(svgEl("path", { d, class: "ma-line", style: `stroke: ${color}` }));
  }
}

function rollingAverage(rows, idx, windowSize) {
  if (idx + 1 < windowSize) return null;
  const slice = rows.slice(idx - windowSize + 1, idx + 1).map(row => row.close).filter(Number.isFinite);
  if (slice.length !== windowSize) return null;
  return slice.reduce((sum, value) => sum + value, 0) / windowSize;
}
function toNumber(value) { const n = Number(value); return Number.isFinite(n) ? n : null; }
function svgEl(name, attrs) {
  const el = document.createElementNS("http://www.w3.org/2000/svg", name);
  Object.entries(attrs || {}).forEach(([k, v]) => el.setAttribute(k, v));
  return el;
}
function svgText(x, y, text, anchor, color) {
  const el = svgEl("text", { x, y, "text-anchor": anchor, fill: color, "font-size": "11" });
  el.textContent = text;
  return el;
}
function formatDate(value) { return String(value || "").replace(/^(\d{4})(\d{2})(\d{2})$/, "$1-$2-$3"); }
function formatNumber(value) {
  if (!Number.isFinite(value)) return "—";
  const abs = Math.abs(value);
  const digits = abs >= 1000 ? 1 : abs >= 100 ? 2 : 3;
  return value.toFixed(digits);
}
function formatPercent(value) {
  if (!Number.isFinite(value)) return "—";
  const sign = value > 0 ? "+" : "";
  return `${sign}${value.toFixed(2)}%`;
}
function formatAmount(value) {
  if (!Number.isFinite(value)) return "—";
  return `${(value / 100000).toFixed(2)}亿`;
}
"""


# --------------------------------------------------------------------------- #
# Market-trend mini-chart panel driven by market_data.json.
# --------------------------------------------------------------------------- #
MARKET_TRENDS_JS = r"""
const data = __payload || {};
const records = Array.isArray(data.records) ? data.records.filter(r => r && r.trade_date).slice(-90) : [];
if (!records.length) return;

const reportBody = document.getElementById("report-body");
const headings = reportBody.querySelectorAll("h3");
let targetHeading = null;
for (const h of headings) {
  if (h.textContent.includes("1.1") && h.textContent.includes("情绪趋势")) { targetHeading = h; break; }
}

const chartSection = document.createElement("div");
chartSection.className = "chart-grid";
chartSection.style.marginTop = "18px";

const charts = [
  { title: "成交额趋势", fields: [{ key: "成交额", color: "var(--blue)", scale: 1e9, unit: "万亿" }] },
  { title: "活跃度 / 情绪值", fields: [{ key: "活跃度", color: "var(--orange)" }, { key: "情绪值", color: "var(--purple)" }] },
  { title: "融资净买入", type: "bar", fields: [{ key: "融资净买入", color: "var(--green)", scale: 1e8, unit: "亿" }] },
  { title: "上涨 vs 下跌家数", fields: [{ key: "上涨", color: "var(--red)" }, { key: "下跌", color: "var(--green)" }] },
  { title: "涨停 vs 跌停家数", fields: [{ key: "涨停", color: "var(--red)" }, { key: "跌停", color: "var(--green)" }] },
];

charts.forEach(config => {
  const card = document.createElement("article");
  card.className = "chart-card";
  const title = document.createElement("div");
  title.className = "chart-title";
  title.textContent = config.title;
  const subtitle = document.createElement("div");
  subtitle.className = "chart-subtitle";
  card.appendChild(title);
  const drawable = drawChart(records, config, card, subtitle);
  card.appendChild(drawable);
  const legend = document.createElement("div");
  legend.className = "legend";
  config.fields.forEach(field => {
    const span = document.createElement("span");
    span.style.setProperty("--legend-color", field.color);
    span.textContent = field.key;
    legend.appendChild(span);
  });
  card.appendChild(legend);
  chartSection.appendChild(card);
});

if (targetHeading) {
  let insertAfter = targetHeading;
  let sibling = targetHeading.nextElementSibling;
  while (sibling) {
    if (sibling.tagName === "H3" || sibling.tagName === "H2") break;
    insertAfter = sibling;
    sibling = sibling.nextElementSibling;
  }
  insertAfter.after(chartSection);
} else {
  reportBody.appendChild(chartSection);
}

function drawChart(rows, config, card, subtitle) {
  const width = 480;
  const height = 200;
  const pad = { left: 42, right: 16, top: 14, bottom: 28 };
  const usableW = width - pad.left - pad.right;
  const usableH = height - pad.top - pad.bottom;
  const svg = svgEl("svg", { viewBox: `0 0 ${width} ${height}`, role: "img" });
  const series = config.fields.map(field => {
    const points = rows.map((row, idx) => {
      const raw = row[field.key];
      const value = typeof raw === "number" ? raw / (field.scale || 1) : null;
      return { idx, date: row.trade_date, value };
    }).filter(p => Number.isFinite(p.value));
    return { field, points };
  }).filter(item => item.points.length);
  if (!series.length) {
    svg.appendChild(svgText(width / 2, height / 2, "暂无数据", "middle", "var(--text-tertiary)"));
    subtitle.textContent = "该列暂无可绘制数值";
    return svg;
  }
  const allValues = series.flatMap(item => item.points.map(p => p.value));
  let min = Math.min(...allValues);
  let max = Math.max(...allValues);
  if (min === max) { min -= 1; max += 1; }
  const span = max - min;
  min -= span * 0.08;
  max += span * 0.08;
  const x = idx => pad.left + (rows.length <= 1 ? usableW / 2 : idx / (rows.length - 1) * usableW);
  const y = value => pad.top + (max - value) / (max - min) * usableH;
  for (let i = 0; i <= 4; i += 1) {
    const gy = pad.top + usableH * i / 4;
    svg.appendChild(svgEl("line", { x1: pad.left, x2: width - pad.right, y1: gy, y2: gy, class: "grid-line" }));
  }
  svg.appendChild(svgEl("line", { x1: pad.left, x2: width - pad.right, y1: height - pad.bottom, y2: height - pad.bottom, class: "axis" }));

  const tooltip = document.createElement("div");
  tooltip.style.cssText = "position:absolute;background:rgba(15,23,42,0.92);color:#f1f5f9;padding:8px 12px;border-radius:8px;font-size:12px;line-height:1.5;pointer-events:none;opacity:0;transition:opacity 0.15s ease;z-index:100;white-space:nowrap;box-shadow:0 4px 12px rgba(0,0,0,0.2);";
  card.style.position = "relative";
  card.appendChild(tooltip);

  const isBar = config.type === "bar";
  const barWidth = isBar ? Math.max(2, usableW / rows.length * 0.55) : 0;
  const y0 = y(0);

  series.forEach(item => {
    if (isBar) {
      item.points.forEach(p => {
        const px = x(p.idx);
        const py = y(p.value);
        const barH = Math.abs(py - y0);
        const barY = p.value >= 0 ? py : y0;
        const barColor = p.value >= 0 ? "var(--red)" : "var(--green)";
        const rect = svgEl("rect", {
          x: (px - barWidth / 2).toFixed(2),
          y: barY.toFixed(2),
          width: barWidth.toFixed(2),
          height: Math.max(1, barH).toFixed(2),
          fill: barColor, rx: 2, opacity: 0.85
        });
        svg.appendChild(rect);
        const hit = svgEl("rect", {
          x: (px - barWidth / 2).toFixed(2),
          y: Math.min(py, y0).toFixed(2),
          width: barWidth.toFixed(2),
          height: Math.max(1, barH).toFixed(2),
          fill: "transparent", stroke: "none",
          style: "cursor:pointer"
        });
        hit.addEventListener("mouseenter", () => {
          rect.setAttribute("opacity", "1");
          tooltip.innerHTML = `<div style="color:#94a3b8;font-size:11px;margin-bottom:2px;">${formatDate(p.date)}</div><div style="font-weight:600;">${item.field.key}: ${formatValue(p.value, item.field.unit)}</div>`;
          tooltip.style.opacity = "1";
        });
        hit.addEventListener("mousemove", e => {
          const r = card.getBoundingClientRect();
          tooltip.style.left = `${Math.min(e.clientX - r.left + 12, r.width - tooltip.offsetWidth - 8)}px`;
          tooltip.style.top = `${Math.max(8, e.clientY - r.top - tooltip.offsetHeight - 12)}px`;
        });
        hit.addEventListener("mouseleave", () => {
          rect.setAttribute("opacity", "0.85");
          tooltip.style.opacity = "0";
        });
        svg.appendChild(hit);
      });
    } else {
      const d = item.points.map((p, i) => `${i === 0 ? "M" : "L"} ${x(p.idx).toFixed(2)} ${y(p.value).toFixed(2)}`).join(" ");
      svg.appendChild(svgEl("path", { d, class: "series-line", style: `stroke: ${item.field.color}` }));
      item.points.forEach(p => {
        svg.appendChild(svgEl("circle", {
          cx: x(p.idx).toFixed(2), cy: y(p.value).toFixed(2),
          r: 3.5, fill: item.field.color, stroke: "#ffffff", "stroke-width": 1.5
        }));
        const hit = svgEl("circle", {
          cx: x(p.idx).toFixed(2), cy: y(p.value).toFixed(2),
          r: 10, fill: "transparent", stroke: "none",
          style: "cursor:pointer"
        });
        hit.addEventListener("mouseenter", () => {
          tooltip.innerHTML = `<div style="color:#94a3b8;font-size:11px;margin-bottom:2px;">${formatDate(p.date)}</div><div style="font-weight:600;">${item.field.key}: ${formatValue(p.value, item.field.unit)}</div>`;
          tooltip.style.opacity = "1";
        });
        hit.addEventListener("mousemove", e => {
          const r = card.getBoundingClientRect();
          tooltip.style.left = `${Math.min(e.clientX - r.left + 12, r.width - tooltip.offsetWidth - 8)}px`;
          tooltip.style.top = `${Math.max(8, e.clientY - r.top - tooltip.offsetHeight - 12)}px`;
        });
        hit.addEventListener("mouseleave", () => { tooltip.style.opacity = "0"; });
        svg.appendChild(hit);
      });
    }
  });
  svg.appendChild(svgText(4, pad.top + 4, formatValue(max, config.fields[0].unit), "start", "var(--text-tertiary)"));
  svg.appendChild(svgText(4, height - pad.bottom, formatValue(min, config.fields[0].unit), "start", "var(--text-tertiary)"));
  return svg;
}

function svgEl(name, attrs) {
  const el = document.createElementNS("http://www.w3.org/2000/svg", name);
  Object.entries(attrs || {}).forEach(([k, v]) => el.setAttribute(k, v));
  return el;
}
function svgText(x, y, text, anchor, color) {
  const el = svgEl("text", { x, y, "text-anchor": anchor, fill: color, "font-size": "11" });
  el.textContent = text;
  return el;
}
function formatDate(value) { return String(value || "").replace(/^(\d{4})(\d{2})(\d{2})$/, "$1-$2-$3"); }
function formatValue(value, unit) {
  if (!Number.isFinite(value)) return "—";
  const abs = Math.abs(value);
  const digits = abs >= 100 ? 0 : abs >= 10 ? 1 : 2;
  return `${value.toFixed(digits)}${unit || ""}`;
}
"""


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else input_path.with_suffix(".html")
    market_data_path = Path(args.market_data)
    evidence_path = Path(args.evidence) if args.evidence else default_evidence_path(input_path)
    markdown_text = input_path.read_text(encoding="utf-8")
    title = args.title or input_path.stem
    market_data = load_market_data(market_data_path)
    evidence = load_evidence(evidence_path)
    index_kline_data = extract_index_kline_payload(evidence, evidence_path)
    stock_kline_data = extract_stock_kline_payload(evidence, evidence_path)

    builder = HtmlReportBuilder(title=title, theme=args.theme)
    builder.add_ui_decoration(PILL_RULES_JS)
    builder.add_ui_decoration(SUMMARY_HERO_JS)
    builder.add_chart_hook(ChartHook(
        name="klines",
        payload={
            "index": index_kline_data,
            "stocks": stock_kline_data,
            "display_days": INDEX_KLINE_DISPLAY_DAYS,
        },
        js=KLINE_CHARTS_JS,
    ))
    builder.add_chart_hook(ChartHook(name="market-trends", payload=market_data, js=MARKET_TRENDS_JS))

    html_text = builder.render(markdown_text, validate=not args.no_validate)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_text, encoding="utf-8")
    print(json.dumps({
        "input": str(input_path),
        "output": str(output_path),
        "theme": args.theme,
        "market_data": str(market_data_path),
        "evidence": str(evidence_path) if evidence_path is not None else None,
        "index_kline_records": {
            key: len((value or {}).get("records") or [])
            for key, value in (index_kline_data.get("indices") or {}).items()
        },
        "stock_kline_records": len(stock_kline_data.get("by_ts_code") or {}),
        "records_available": (market_data.get("quality") or {}).get("records_available", 0),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
