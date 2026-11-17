"""将 result-* 渲染为单文件自包含 HTML（只读；仅 quality verdict=pass 表）。"""
from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

# 与 domain.catalogs 标签对齐的兜底（避免循环 import）
_GROUP_LABELS: dict[str, str] = {
    "A_key_financials": "主要会计数据",
    "B_statements": "三大报表",
    "C_segments": "主营与分部",
    "D_mda": "MD&A",
    "E_holders": "股东与股本",
    "F_dividend": "股东回报",
    "G_governance": "治理与人员",
    "H_matters": "重要事项",
    "I_audit": "审计与政策",
    "X_fossil_energy": "化石能源",
    "X_consumer": "消费零售",
    "X_bank": "银行",
    "X_insurance": "保险",
    "Z_generic": "未定型候选",
    "audit": "审核",
}

_STMT_BASES = ("balance_sheet", "income_stmt", "cashflow_stmt")
_STMT_LABELS = {
    "balance_sheet": "资产负债表",
    "income_stmt": "利润表",
    "cashflow_stmt": "现金流量表",
}

_MAX_ROWS = 200  # 单表嵌入上限，防超大 related_txn 撑爆 HTML


def _table_base_id(tid: str) -> str:
    tid = str(tid or "")
    if "_p" in tid:
        return tid.split("_p", 1)[0]
    if tid.startswith("generic_merged_"):
        # generic_merged_power_generation_p033_p034 → power_generation-ish keep id
        return tid
    return tid


def _group_label(group: str | None) -> str:
    g = group or "Z_generic"
    if g in _GROUP_LABELS:
        return _GROUP_LABELS[g]
    if g.startswith("X_") and g in _GROUP_LABELS:
        return _GROUP_LABELS[g]
    return g.replace("_", " ")


def _pass_ids(quality: dict) -> set[str]:
    return {
        str(t.get("id"))
        for t in (quality.get("tables") or [])
        if (t.get("verdict") or "") == "pass" and t.get("id")
    }


def _slim_row(row: dict) -> dict:
    src = row.get("source") if isinstance(row.get("source"), dict) else {}
    out: dict[str, Any] = {}
    for k, v in row.items():
        if k == "source":
            continue
        out[k] = v
    out["_page"] = src.get("page")
    out["_quote"] = src.get("quote") or ""
    out["_table"] = src.get("table")
    return out


def _load_table(result_dir: Path, file_rel: str) -> dict | None:
    path = result_dir / file_rel
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def build_html_payload(result_dir: Path, *, cache_id: str = "") -> dict[str, Any]:
    """从 result 目录组装前端 payload（仅 pass 表）。"""
    result_dir = Path(result_dir)
    manifest = json.loads((result_dir / "manifest.json").read_text(encoding="utf-8"))
    quality = {}
    if (result_dir / "quality.json").is_file():
        quality = json.loads((result_dir / "quality.json").read_text(encoding="utf-8"))
    review = {}
    if (result_dir / "review.json").is_file():
        review = json.loads((result_dir / "review.json").read_text(encoding="utf-8"))
    gaps = []
    if (result_dir / "gaps.json").is_file():
        gaps = json.loads((result_dir / "gaps.json").read_text(encoding="utf-8")) or []

    pass_ids = _pass_ids(quality)
    catalog_tables = (manifest.get("catalog") or {}).get("tables") or []
    findings_by_id: dict[str, list] = {}
    for f in quality.get("python_findings") or []:
        tid = str(f.get("id") or "")
        findings_by_id.setdefault(tid, []).append({
            "verdict": f.get("verdict"),
            "reason": f.get("reason"),
            "detail": f.get("detail"),
        })

    tables_out: dict[str, Any] = {}
    nav_buckets: dict[str, list[str]] = {}

    for ent in catalog_tables:
        tid = str(ent.get("id") or "")
        if tid not in pass_ids:
            continue
        file_rel = ent.get("file") or f"tables/{tid}.json"
        obj = _load_table(result_dir, file_rel)
        if not obj:
            continue
        cols = (obj.get("schema") or {}).get("columns") or []
        columns = [{"key": c.get("key"), "label": c.get("label") or c.get("key")} for c in cols]
        rows_raw = obj.get("rows") or []
        truncated = len(rows_raw) > _MAX_ROWS
        rows = [_slim_row(r) for r in rows_raw[:_MAX_ROWS] if isinstance(r, dict)]
        group = str(obj.get("group") or ent.get("group") or "Z_generic")
        tables_out[tid] = {
            "id": tid,
            "title": obj.get("title") or tid,
            "description": obj.get("description") or "",
            "group": group,
            "group_label": _group_label(group),
            "base": _table_base_id(tid),
            "variant": obj.get("variant") or ent.get("variant") or "",
            "unit_default": obj.get("unit_default") or "",
            "columns": columns,
            "rows": rows,
            "row_count": obj.get("row_count") or len(rows_raw),
            "truncated": truncated,
            "provenance": obj.get("provenance") or {},
            "findings": findings_by_id.get(tid) or [],
        }
        nav_buckets.setdefault(group, []).append(tid)

    # 导航：coverage 顺序优先，其余追加
    coverage = list(manifest.get("coverage_groups") or [])
    group_order = list(dict.fromkeys([*coverage, *nav_buckets.keys(), "audit"]))
    nav = []
    for g in group_order:
        if g == "audit":
            nav.append({"group": "audit", "label": "审核与缺口", "table_ids": []})
            continue
        ids = nav_buckets.get(g) or []
        if not ids:
            continue
        nav.append({"group": g, "label": _group_label(g), "table_ids": ids})

    statements: dict[str, list[str]] = {b: [] for b in _STMT_BASES}
    for tid, t in tables_out.items():
        base = t.get("base") or ""
        if base in statements:
            statements[base].append(tid)
        elif any(tid == b or tid.startswith(b + "_") for b in _STMT_BASES):
            for b in _STMT_BASES:
                if tid == b or tid.startswith(b + "_"):
                    statements[b].append(tid)
                    break

    source = manifest.get("source") or {}
    profile = review.get("document_profile") or {}
    return {
        "meta": {
            "cache_id": cache_id or manifest.get("cache_id") or result_dir.parent.name,
            "result": result_dir.name,
            "source": {
                "title": source.get("title") or "",
                "symbol": source.get("symbol") or "",
                "report_date": source.get("report_date") or "",
                "filing_kind": source.get("filing_kind") or profile.get("filing_kind") or "",
                "industry": source.get("industry_hint") or profile.get("industry") or "",
            },
            "profile": {
                "market": profile.get("market"),
                "accounting": profile.get("accounting"),
                "industry": profile.get("industry"),
                "industry_confidence": profile.get("industry_confidence"),
                "filing_kind": profile.get("filing_kind"),
            },
            "quality_status": quality.get("status") or "missing",
            "review_status": review.get("status") or "missing",
            "pass_table_count": len(tables_out),
            "catalog_table_count": len(catalog_tables),
        },
        "nav": nav,
        "statements": {
            "bases": [{"id": b, "label": _STMT_LABELS[b], "table_ids": statements[b]} for b in _STMT_BASES],
        },
        "tables": tables_out,
        "gaps": [
            {
                "id": g.get("id"),
                "group": g.get("group"),
                "status": g.get("status"),
                "reason": g.get("reason"),
                "quote": g.get("quote"),
                "page": g.get("page"),
            }
            for g in gaps if isinstance(g, dict)
        ],
        "review": {
            "hard_failures": review.get("hard_failures") or [],
            "warnings": review.get("warnings") or [],
        },
        "findings": quality.get("python_findings") or [],
        "stmt_labels": _STMT_LABELS,
    }


def render_html_document(payload: dict[str, Any]) -> str:
    """把 payload 嵌入自包含 HTML。"""
    payload_json = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    # 防止 </script> 打断
    payload_json = payload_json.replace("<", "\\u003c").replace(">", "\\u003e")
    title = (payload.get("meta") or {}).get("source", {}).get("title") or "财报提取"
    return _HTML_TEMPLATE.replace("__PAGE_TITLE__", html.escape(title)).replace(
        "__PAYLOAD_JSON__", payload_json
    )


def write_html_report(
    result_dir: Path,
    *,
    cache_id: str = "",
    out_path: Path | None = None,
) -> Path:
    result_dir = Path(result_dir)
    payload = build_html_payload(result_dir, cache_id=cache_id)
    doc = render_html_document(payload)
    dest = Path(out_path) if out_path else result_dir / "report.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(doc, encoding="utf-8")
    return dest


# --------------------------------------------------------------------------
# HTML template (editorial finance; system fonts only)
# --------------------------------------------------------------------------

_HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>__PAGE_TITLE__ · 提取阅览</title>
<style>
:root {
  --ink: #1a1a1a;
  --muted: #5c5a56;
  --paper: #f7f4ef;
  --paper-2: #efeae2;
  --line: #d9d2c6;
  --accent: #2f5d50;
  --accent-soft: rgba(47, 93, 80, 0.12);
  --danger: #8b3a2f;
  --warn: #8a6a2f;
  --ok: #2f5d50;
  --drawer-w: min(420px, 92vw);
  --side-w: 220px;
  --serif: "Songti SC", "Noto Serif SC", "Source Han Serif SC", Georgia, "Times New Roman", serif;
  --sans: "PingFang SC", "Hiragino Sans GB", "Noto Sans SC", "Helvetica Neue", Arial, sans-serif;
  --mono: ui-monospace, "SF Mono", Menlo, Consolas, "Courier New", monospace;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: var(--sans);
  font-size: 14px;
  line-height: 1.55;
}
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
.hero {
  padding: 2.25rem 2rem 1.5rem;
  border-bottom: 1px solid var(--line);
  background: linear-gradient(180deg, #faf8f4 0%, var(--paper) 100%);
}
.hero-brand {
  font-family: var(--serif);
  font-size: clamp(1.6rem, 3vw, 2.15rem);
  font-weight: 600;
  letter-spacing: 0.02em;
  margin: 0 0 0.4rem;
  max-width: 48rem;
}
.hero-sub {
  color: var(--muted);
  margin: 0 0 1rem;
  font-size: 0.95rem;
}
.badges { display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center; }
.badge {
  display: inline-flex; align-items: center; gap: 0.35rem;
  padding: 0.2rem 0.65rem;
  border: 1px solid var(--line);
  border-radius: 999px;
  font-size: 0.75rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  background: #fff;
}
.badge.ok { border-color: var(--accent); color: var(--ok); background: var(--accent-soft); }
.badge.fail { border-color: var(--danger); color: var(--danger); background: rgba(139,58,47,0.08); }
.badge.miss { color: var(--muted); }
.layout {
  display: grid;
  grid-template-columns: var(--side-w) minmax(0, 1fr);
  min-height: calc(100vh - 8rem);
}
.side {
  position: sticky; top: 0; align-self: start;
  height: 100vh; overflow: auto;
  padding: 1.25rem 1rem 3rem;
  border-right: 1px solid var(--line);
  background: var(--paper-2);
}
.side h2 {
  font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.08em;
  color: var(--muted); font-weight: 600; margin: 0 0 0.75rem;
}
#nav-search {
  width: 100%; padding: 0.45rem 0.6rem; margin-bottom: 1rem;
  border: 1px solid var(--line); border-radius: 4px;
  background: #fff; font: inherit; color: var(--ink);
}
#nav-search:focus { outline: 2px solid var(--accent-soft); border-color: var(--accent); }
.nav-group { margin-bottom: 1rem; }
.nav-group-label {
  font-size: 0.72rem; color: var(--muted); margin-bottom: 0.35rem;
  letter-spacing: 0.04em;
}
.nav-link {
  display: block; padding: 0.28rem 0.45rem; margin: 0.1rem 0;
  border-radius: 3px; color: var(--ink); cursor: pointer;
  font-size: 0.85rem; border-left: 2px solid transparent;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.nav-link:hover { background: rgba(0,0,0,0.04); }
.nav-link.active {
  border-left-color: var(--accent);
  background: var(--accent-soft);
  color: var(--accent);
  font-weight: 560;
}
.main { padding: 1.5rem 2rem 4rem; max-width: 920px; }
.section { margin-bottom: 2.5rem; scroll-margin-top: 1rem; }
.section h2 {
  font-family: var(--serif);
  font-size: 1.35rem; font-weight: 600;
  margin: 0 0 0.35rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px solid var(--line);
}
.section .hint { color: var(--muted); font-size: 0.85rem; margin: 0 0 1rem; }
.tabs { display: flex; flex-wrap: wrap; gap: 0.35rem; margin: 0.75rem 0 1rem; }
.tab {
  border: 1px solid var(--line); background: #fff; color: var(--ink);
  padding: 0.35rem 0.75rem; border-radius: 3px; cursor: pointer; font: inherit;
}
.tab.active { border-color: var(--accent); background: var(--accent-soft); color: var(--accent); }
.subtabs { display: flex; flex-wrap: wrap; gap: 0.3rem; margin-bottom: 0.75rem; }
.subtab {
  border: none; background: transparent; color: var(--muted);
  padding: 0.2rem 0.5rem; cursor: pointer; font: inherit; font-size: 0.82rem;
  border-bottom: 2px solid transparent;
}
.subtab.active { color: var(--accent); border-bottom-color: var(--accent); }
.table-wrap {
  overflow: auto; max-height: min(70vh, 640px);
  border: 1px solid var(--line); background: #fff;
  animation: fadeIn 0.18s ease;
}
@keyframes fadeIn { from { opacity: 0.4; } to { opacity: 1; } }
table.data {
  width: 100%; border-collapse: collapse; font-variant-numeric: tabular-nums;
  font-family: var(--mono); font-size: 0.78rem;
}
table.data th, table.data td {
  padding: 0.4rem 0.55rem; border-bottom: 1px solid var(--line);
  text-align: left; vertical-align: top;
}
table.data th {
  position: sticky; top: 0; background: var(--paper-2);
  font-family: var(--sans); font-weight: 560; font-size: 0.72rem;
  color: var(--muted); z-index: 1;
}
table.data tbody tr { cursor: pointer; transition: background 0.12s; }
table.data tbody tr:nth-child(even) { background: rgba(247,244,239,0.55); }
table.data tbody tr:hover { background: var(--accent-soft); }
table.data tbody tr.degraded { box-shadow: inset 3px 0 0 var(--warn); }
table.data .page-tag {
  font-family: var(--sans); font-size: 0.68rem; color: var(--accent);
  margin-left: 0.35rem; white-space: nowrap;
}
.flag-warn {
  display: inline-block; margin-left: 0.35rem;
  color: var(--warn); font-size: 0.7rem; font-family: var(--sans);
}
.gap-list { display: flex; flex-direction: column; gap: 0.5rem; }
.gap-item {
  border: 1px solid var(--line); background: #fff; padding: 0.65rem 0.85rem;
  border-radius: 3px;
}
.gap-item summary { cursor: pointer; list-style: none; display: flex; gap: 0.5rem; align-items: baseline; flex-wrap: wrap; }
.gap-item summary::-webkit-details-marker { display: none; }
.status-pill {
  font-size: 0.68rem; padding: 0.1rem 0.45rem; border-radius: 3px;
  border: 1px solid var(--line); text-transform: uppercase; letter-spacing: 0.04em;
}
.status-pill.found { color: var(--ok); border-color: var(--accent); background: var(--accent-soft); }
.status-pill.pending, .status-pill.required { color: var(--warn); border-color: var(--warn); }
.status-pill.not_disclosed, .status-pill.not_applicable, .status-pill.not_found { color: var(--muted); }
.gap-quote {
  margin-top: 0.5rem; padding: 0.5rem 0.65rem;
  background: var(--paper-2); border-left: 2px solid var(--accent);
  font-size: 0.85rem; color: var(--ink);
}
.findings { margin-top: 1.25rem; }
.finding {
  padding: 0.45rem 0.65rem; border-left: 3px solid var(--warn);
  background: rgba(138,106,47,0.06); margin-bottom: 0.4rem; font-size: 0.85rem;
}
.footer {
  margin-top: 3rem; padding-top: 1rem; border-top: 1px solid var(--line);
  color: var(--muted); font-size: 0.8rem;
}
.drawer-backdrop {
  position: fixed; inset: 0; background: rgba(26,26,26,0.28);
  opacity: 0; pointer-events: none; transition: opacity 0.2s;
  z-index: 40;
}
.drawer-backdrop.open { opacity: 1; pointer-events: auto; }
.drawer {
  position: fixed; top: 0; right: 0; width: var(--drawer-w); height: 100%;
  background: #fff; border-left: 1px solid var(--line);
  transform: translateX(100%); transition: transform 0.2s ease;
  z-index: 50; padding: 1.25rem 1.35rem 2rem; overflow: auto;
  box-shadow: -8px 0 24px rgba(0,0,0,0.06);
}
.drawer.open { transform: translateX(0); }
.drawer h3 { font-family: var(--serif); margin: 0 0 0.75rem; font-size: 1.15rem; }
.drawer dl { margin: 0; }
.drawer dt { font-size: 0.7rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; margin-top: 0.85rem; }
.drawer dd { margin: 0.25rem 0 0; font-family: var(--mono); font-size: 0.82rem; white-space: pre-wrap; word-break: break-word; }
.drawer .close {
  position: absolute; top: 0.85rem; right: 0.85rem;
  border: none; background: transparent; font-size: 1.25rem; cursor: pointer; color: var(--muted);
}
.drawer .copy-btn {
  margin-top: 1rem; border: 1px solid var(--line); background: var(--paper);
  padding: 0.35rem 0.75rem; cursor: pointer; font: inherit; border-radius: 3px;
}
.empty { color: var(--muted); padding: 1rem 0; font-size: 0.9rem; }
@media print {
  .side, .drawer, .drawer-backdrop, #nav-search, .tabs, .subtabs { display: none !important; }
  .layout { display: block; }
  .main { max-width: none; padding: 0; }
  .table-wrap { max-height: none; overflow: visible; }
  .hero { padding: 0 0 1rem; }
}
@media (max-width: 860px) {
  .layout { grid-template-columns: 1fr; }
  .side { position: relative; height: auto; border-right: none; border-bottom: 1px solid var(--line); }
}
</style>
</head>
<body>
<header class="hero" id="hero">
  <h1 class="hero-brand" id="hero-title"></h1>
  <p class="hero-sub" id="hero-sub"></p>
  <div class="badges" id="hero-badges"></div>
</header>
<div class="layout">
  <aside class="side" id="side">
    <h2>目录 <kbd style="font-weight:400;opacity:.6">/</kbd></h2>
    <input id="nav-search" type="search" placeholder="搜索表…" autocomplete="off"/>
    <nav id="nav"></nav>
  </aside>
  <main class="main" id="main">
    <section class="section" id="sec-statements">
      <h2>三大报表</h2>
      <p class="hint">仅展示 quality=pass 的表。点击行查看溯源 quote 与页码。</p>
      <div class="tabs" id="stmt-tabs"></div>
      <div class="subtabs" id="stmt-subtabs"></div>
      <div id="stmt-panel"></div>
    </section>
    <section class="section" id="sec-other">
      <h2>经营与其它表</h2>
      <p class="hint">分部、产销、股东、治理等 pass 表。</p>
      <div id="other-panel"></div>
    </section>
    <section class="section" id="sec-audit">
      <h2>审核与缺口</h2>
      <p class="hint">gaps 终态与 QA findings；只读，不在此改数。</p>
      <div id="audit-hard"></div>
      <div class="gap-list" id="gap-list"></div>
      <div class="findings" id="findings"></div>
    </section>
    <footer class="footer" id="footer"></footer>
  </main>
</div>
<div class="drawer-backdrop" id="backdrop"></div>
<aside class="drawer" id="drawer" aria-hidden="true">
  <button class="close" id="drawer-close" aria-label="关闭">×</button>
  <h3>溯源</h3>
  <dl id="drawer-body"></dl>
  <button class="copy-btn" id="drawer-copy">复制 quote</button>
</aside>
<script type="application/json" id="payload">__PAYLOAD_JSON__</script>
<script>
(function () {
  const payload = JSON.parse(document.getElementById("payload").textContent);
  const meta = payload.meta || {};
  const tables = payload.tables || {};
  const nav = payload.nav || [];
  const statements = (payload.statements && payload.statements.bases) || [];
  let activeStmt = null;
  let activeTableId = null;
  let drawerQuote = "";

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function badge(label, status) {
    const cls = status === "pass" ? "ok" : (status === "fail" ? "fail" : "miss");
    return `<span class="badge ${cls}">${esc(label)} · ${esc(status)}</span>`;
  }

  function renderHero() {
    const src = meta.source || {};
    document.getElementById("hero-title").textContent = src.title || "财报提取阅览";
    const bits = [
      src.symbol && `代码 ${src.symbol}`,
      src.report_date && `报告期 ${src.report_date}`,
      src.filing_kind && src.filing_kind,
      src.industry && `行业 ${src.industry}`,
      `${meta.pass_table_count || 0} 张 pass 表`,
    ].filter(Boolean);
    document.getElementById("hero-sub").textContent = bits.join(" · ");
    document.getElementById("hero-badges").innerHTML =
      badge("quality", meta.quality_status) + badge("review", meta.review_status);
    document.getElementById("footer").textContent =
      `数据来源：${src.title || "—"}（报告期 ${src.report_date || "—"}；PDF 页码见正文角标；cache ${meta.cache_id || "—"}；result ${meta.result || "—"}）`;
  }

  function renderNav(filter) {
    const q = (filter || "").trim().toLowerCase();
    const el = document.getElementById("nav");
    let html = "";
    nav.forEach(g => {
      if (g.group === "audit") {
        html += `<div class="nav-group" data-group="audit">
          <div class="nav-group-label">${esc(g.label)}</div>
          <div class="nav-link" data-jump="sec-audit">审核与缺口</div>
        </div>`;
        return;
      }
      const ids = (g.table_ids || []).filter(id => {
        if (!q) return true;
        const t = tables[id] || {};
        return (id + " " + (t.title || "")).toLowerCase().includes(q);
      });
      if (!ids.length && q) return;
      html += `<div class="nav-group" data-group="${esc(g.group)}">
        <div class="nav-group-label">${esc(g.label)}</div>`;
      ids.forEach(id => {
        const t = tables[id] || {};
        html += `<div class="nav-link" data-table="${esc(id)}" title="${esc(t.title || id)}">${esc(t.title || id)}</div>`;
      });
      html += `</div>`;
    });
    el.innerHTML = html || `<div class="empty">无匹配</div>`;
  }

  function openDrawer(row) {
    drawerQuote = row._quote || "";
    const body = document.getElementById("drawer-body");
    body.innerHTML = `
      <dt>科目 / 行</dt><dd>${esc(row.item || "—")}</dd>
      <dt>页码</dt><dd>${esc(row._page != null ? "p" + row._page : "—")}</dd>
      <dt>表索引</dt><dd>${esc(row._table != null ? row._table : "—")}</dd>
      <dt>Quote</dt><dd>${esc(row._quote || "（无 quote）")}</dd>`;
    document.getElementById("drawer").classList.add("open");
    document.getElementById("backdrop").classList.add("open");
    document.getElementById("drawer").setAttribute("aria-hidden", "false");
  }

  function closeDrawer() {
    document.getElementById("drawer").classList.remove("open");
    document.getElementById("backdrop").classList.remove("open");
    document.getElementById("drawer").setAttribute("aria-hidden", "true");
  }

  function renderTable(tid, mountId) {
    const t = tables[tid];
    const mount = document.getElementById(mountId);
    if (!t) {
      mount.innerHTML = `<div class="empty">无表 ${esc(tid)}</div>`;
      return;
    }
    const cols = t.columns || [];
    const degraded = (t.findings || []).some(f => f.verdict === "degraded");
    let head = "<tr>" + cols.map(c => `<th>${esc(c.label || c.key)}</th>`).join("") + "<th>页</th></tr>";
    let body = (t.rows || []).map(r => {
      const cells = cols.map(c => {
        const key = c.key;
        let val = r[key];
        if (key === "item" || key === cols[0].key) {
          return `<td>${esc(val)}${degraded ? '<span class="flag-warn">⚠ 需复核</span>' : ""}</td>`;
        }
        return `<td>${esc(val)}</td>`;
      }).join("");
      const page = r._page != null ? `<span class="page-tag">p${esc(r._page)}</span>` : "";
      return `<tr class="${degraded ? "degraded" : ""}" data-row="${encodeURIComponent(JSON.stringify(r))}">${cells}<td>${page}</td></tr>`;
    }).join("");
    const trunc = t.truncated ? `<p class="hint">已截断至前 ${t.rows.length} / ${t.row_count} 行</p>` : "";
    const varTag = t.variant && t.variant !== "primary"
      ? `<span class="badge miss" style="font-size:11px;margin-left:8px">${esc(t.variant)}</span>` : "";
    const titleHtml = `<h3 class="panel-title" style="margin:0 0 6px">${esc(t.title || tid)}${varTag}</h3>`;
    const findHtml = (t.findings || []).map(f =>
      `<div class="finding">⚠ ${esc(f.reason || "")} — ${esc(f.detail || "")}${f.adjudicated ? `（已仲裁：${esc(f.adjudicated)}）` : ""}</div>`
    ).join("");
    mount.innerHTML = `${titleHtml}${trunc}<div class="table-wrap"><table class="data"><thead>${head}</thead><tbody>${body}</tbody></table></div>${findHtml}`;
    mount.querySelectorAll("tbody tr").forEach(tr => {
      tr.addEventListener("click", () => {
        try { openDrawer(JSON.parse(decodeURIComponent(tr.getAttribute("data-row")))); } catch (e) {}
      });
    });
    activeTableId = tid;
    document.querySelectorAll(".nav-link").forEach(a => {
      a.classList.toggle("active", a.getAttribute("data-table") === tid);
    });
  }

  function renderStmtTabs() {
    const tabs = document.getElementById("stmt-tabs");
    tabs.innerHTML = statements.map(s => {
      const n = (s.table_ids || []).length;
      const dis = n ? "" : " disabled style=\"opacity:.4\"";
      return `<button class="tab" data-stmt="${esc(s.id)}"${dis}>${esc(s.label)} (${n})</button>`;
    }).join("");
    const first = statements.find(s => (s.table_ids || []).length);
    if (first) selectStmt(first.id);
    else document.getElementById("stmt-panel").innerHTML = `<div class="empty">无 pass 三表</div>`;
  }

  function selectStmt(base) {
    activeStmt = base;
    try { sessionStorage.setItem("wm-html-stmt", base); } catch (e) {}
    document.querySelectorAll("#stmt-tabs .tab").forEach(b => {
      b.classList.toggle("active", b.getAttribute("data-stmt") === base);
    });
    const spec = statements.find(s => s.id === base);
    const ids = (spec && spec.table_ids) || [];
    const sub = document.getElementById("stmt-subtabs");
    sub.innerHTML = ids.map((id, i) => {
      const t = tables[id] || {};
      const label = t.title || id;
      return `<button class="subtab${i === 0 ? " active" : ""}" data-tid="${esc(id)}">${esc(label)}</button>`;
    }).join("");
    if (ids[0]) renderTable(ids[0], "stmt-panel");
  }

  function renderOther() {
    const stmtIds = new Set();
    statements.forEach(s => (s.table_ids || []).forEach(id => stmtIds.add(id)));
    const otherIds = Object.keys(tables).filter(id => !stmtIds.has(id));
    const mount = document.getElementById("other-panel");
    if (!otherIds.length) {
      mount.innerHTML = `<div class="empty">无其它 pass 表</div>`;
      return;
    }
    let html = `<div class="tabs" id="other-tabs">` +
      otherIds.map((id, i) => {
        const t = tables[id];
        return `<button class="tab${i === 0 ? " active" : ""}" data-tid="${esc(id)}">${esc(t.title || id)}</button>`;
      }).join("") + `</div><div id="other-table"></div>`;
    mount.innerHTML = html;
    renderTable(otherIds[0], "other-table");
    mount.querySelectorAll(".tab").forEach(b => {
      b.addEventListener("click", () => {
        mount.querySelectorAll(".tab").forEach(x => x.classList.remove("active"));
        b.classList.add("active");
        renderTable(b.getAttribute("data-tid"), "other-table");
      });
    });
  }

  function renderAudit() {
    const rev = payload.review || {};
    const hard = rev.hard_failures || [];
    const hardEl = document.getElementById("audit-hard");
    if (hard.length) {
      hardEl.innerHTML = hard.map(h =>
        `<div class="finding" style="border-left-color:var(--danger)">硬挂 · ${esc(h.id || "")} — ${esc(h.reason || "")}
        ${(h.items || []).length ? "（" + esc((h.items || []).join(", ")) + "）" : ""}</div>`
      ).join("");
    } else {
      hardEl.innerHTML = `<div class="empty">无 hard_failures</div>`;
    }
    const gaps = payload.gaps || [];
    document.getElementById("gap-list").innerHTML = gaps.map(g => {
      const st = g.status || "pending";
      const openable = g.quote ? "" : "";
      return `<details class="gap-item" ${g.quote ? "" : ""}>
        <summary>
          <span class="status-pill ${esc(st)}">${esc(st)}</span>
          <strong>${esc(g.id || "")}</strong>
          <span style="color:var(--muted);font-size:.85rem">${esc(g.reason || "")}</span>
          ${g.page != null ? `<span class="page-tag">p${esc(g.page)}</span>` : ""}
        </summary>
        ${g.quote ? `<div class="gap-quote">${esc(g.quote)}</div>` : (st === "pending" || st === "required" ? `<div class="empty">待 text_scan / auto-heal</div>` : "")}
      </details>`;
    }).join("") || `<div class="empty">无 gaps</div>`;
    const findings = payload.findings || [];
    document.getElementById("findings").innerHTML = findings.length
      ? `<h3 style="font-family:var(--serif);font-size:1.05rem">QA findings</h3>` +
        findings.map(f => `<div class="finding">${esc(f.id)} · ${esc(f.verdict)} · ${esc(f.reason)} — ${esc(f.detail || "")}</div>`).join("")
      : "";
  }

  // events
  document.getElementById("stmt-tabs").addEventListener("click", e => {
    const b = e.target.closest(".tab");
    if (b && b.getAttribute("data-stmt")) selectStmt(b.getAttribute("data-stmt"));
  });
  document.getElementById("stmt-subtabs").addEventListener("click", e => {
    const b = e.target.closest(".subtab");
    if (!b) return;
    document.querySelectorAll("#stmt-subtabs .subtab").forEach(x => x.classList.remove("active"));
    b.classList.add("active");
    renderTable(b.getAttribute("data-tid"), "stmt-panel");
  });
  document.getElementById("nav").addEventListener("click", e => {
    const jump = e.target.closest("[data-jump]");
    if (jump) {
      document.getElementById(jump.getAttribute("data-jump")).scrollIntoView({ behavior: "smooth" });
      return;
    }
    const a = e.target.closest("[data-table]");
    if (!a) return;
    const tid = a.getAttribute("data-table");
    const t = tables[tid];
    if (!t) return;
    const base = t.base;
    if (["balance_sheet", "income_stmt", "cashflow_stmt"].includes(base) ||
        ["balance_sheet", "income_stmt", "cashflow_stmt"].some(b => tid === b || tid.startsWith(b + "_"))) {
      let b = base;
      if (!["balance_sheet", "income_stmt", "cashflow_stmt"].includes(b)) {
        b = ["balance_sheet", "income_stmt", "cashflow_stmt"].find(x => tid === x || tid.startsWith(x + "_"));
      }
      selectStmt(b);
      document.querySelectorAll("#stmt-subtabs .subtab").forEach(x => {
        const on = x.getAttribute("data-tid") === tid;
        x.classList.toggle("active", on);
      });
      renderTable(tid, "stmt-panel");
      document.getElementById("sec-statements").scrollIntoView({ behavior: "smooth" });
    } else {
      document.getElementById("sec-other").scrollIntoView({ behavior: "smooth" });
      const tab = document.querySelector(`#other-tabs .tab[data-tid="${CSS.escape(tid)}"]`);
      if (tab) tab.click();
      else renderTable(tid, "other-table");
    }
  });
  document.getElementById("nav-search").addEventListener("input", e => renderNav(e.target.value));
  document.getElementById("backdrop").addEventListener("click", closeDrawer);
  document.getElementById("drawer-close").addEventListener("click", closeDrawer);
  document.getElementById("drawer-copy").addEventListener("click", () => {
    if (drawerQuote) navigator.clipboard.writeText(drawerQuote).catch(() => {});
  });
  document.addEventListener("keydown", e => {
    if (e.key === "/" && document.activeElement.tagName !== "INPUT") {
      e.preventDefault();
      document.getElementById("nav-search").focus();
    }
    if (e.key === "Escape") closeDrawer();
  });

  renderHero();
  renderNav("");
  renderStmtTabs();
  try {
    const saved = sessionStorage.getItem("wm-html-stmt");
    if (saved && statements.some(s => s.id === saved && (s.table_ids || []).length)) selectStmt(saved);
  } catch (e) {}
  renderOther();
  renderAudit();
})();
</script>
</body>
</html>
"""
