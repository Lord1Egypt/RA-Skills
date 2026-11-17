#!/usr/bin/env python3
# DEPENDENCIES: Python stdlib only (>= 3.8).
"""Render an application observe report from structured JSON.

The skill collects per-layer findings and emits one JSON blob; this script
scores it, validates it, and renders the final report so the model does not
hand-format long output token-by-token.

Scoring covers four health dimensions — application, ECS, RDS (only when the
app has one), and availability — combined into a weighted 0-100 health score
with an A/B/C/D grade. Cost is shown separately with the actual billed amount
and an optional optimization note; it never affects the health score.

Usage:
    python3 render_report.py --schema
    python3 render_report.py --validate --input data.json
    python3 render_report.py --input data.json --format md   --output report.md
    python3 render_report.py --input data.json --format html --output report.html
    cat data.json | python3 render_report.py --format md

All prices are USD (international site). Cost shows the actual bill only; there
is no estimate field.
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from typing import Any

STATES = ("healthy", "degraded", "unavailable", "unknown")
CURRENCY = "USD"

DIMENSIONS = ("application", "ecs", "rds", "availability")

WEIGHTS_WITH_RDS = {"application": 35, "ecs": 30, "rds": 25, "availability": 10}
WEIGHTS_NO_RDS = {"application": 45, "ecs": 45, "availability": 10}

SCHEMA_DOC = """
{
  "meta": {
    "generated_at": "2026-08-26 16:20 UTC+8",
    "app": "shop-api",
    "region": "ap-southeast-1",
    "region_label": "Singapore",
    "window": "1h",
    "topology": "ecs" | "ecs+rds",
    "data_source": "cloudmonitor" | "fallback"
  },
  "recent_action": null | {
    "time": "2026-09-09 11:20 UTC+8",
    "action": "restart shop-api",
    "verification": "recovered"
  },
  "layers": {
    "application": {
      "state": "healthy" | "degraded" | "unavailable" | "unknown",
      "score": 32, "max_score": 35,
      "evidence": "reachable, response 186 ms; app and Nginx healthy",
      "metrics": [
        {"name": "Reachability", "value": "200 OK", "threshold": "2xx/3xx", "trend": "stable"},
        {"name": "Response time", "value": "186 ms", "threshold": "<800 ms warn", "trend": "stable"},
        {"name": "Error rate", "value": "0.2%", "threshold": "<1% warn", "trend": "flat"}
      ],
      "detail": "one paragraph of plain-language analysis for this layer",
      "reason": "only when state is unknown: why it could not be determined"
    },
    "ecs": {
      "state": "healthy", "score": 27, "max_score": 30,
      "evidence": "1h avg CPU 31%, memory 44%, disk 15%",
      "metrics": [
        {"name": "CPU", "value": "31%", "threshold": "80/95", "trend": "stable"},
        {"name": "Memory", "value": "44%", "threshold": "80/95", "trend": "stable"},
        {"name": "Disk usage", "value": "15%", "threshold": "80/90", "trend": "flat"},
        {"name": "Disk IO", "value": "236 IOPS", "threshold": "vs 2280 limit", "trend": "low"},
        {"name": "Network out", "value": "0.24 Mbps", "threshold": "vs 100 Mbps", "trend": "low"}
      ],
      "detail": "..."
    },
    "rds": null | {
      "state": "degraded", "score": 18, "max_score": 25,
      "evidence": "active connections rose 12 -> 38; watch the pool",
      "metrics": [
        {"name": "Connections", "value": "38", "threshold": "vs 200 max", "trend": "rising"},
        {"name": "Slow SQL", "value": "3 / 1h", "threshold": "<10 warn", "trend": "up"},
        {"name": "Space usage", "value": "22%", "threshold": "80/90", "trend": "flat"},
        {"name": "Row-lock waits", "value": "0", "threshold": "0 ideal", "trend": "flat"}
      ],
      "detail": "..."
    },
    "availability": {
      "state": "healthy", "score": 10, "max_score": 10,
      "evidence": "ECS Running; RDS Running; EIP InUse; SG 80/443 open; no recent system events",
      "metrics": [
        {"name": "ECS status", "value": "Running", "threshold": "Running", "trend": "stable"},
        {"name": "RDS status", "value": "Running", "threshold": "Running", "trend": "stable"},
        {"name": "EIP status", "value": "InUse", "threshold": "InUse", "trend": "stable"},
        {"name": "Exposure", "value": "80/443 only", "threshold": "no 22/3306 to 0.0.0.0/0", "trend": "stable"}
      ],
      "detail": "..."
    }
  },
  "assessment": {
    "health_score": 87,
    "grade": "B", "grade_label": "Good",
    "one_liner": "App healthy; watch the RDS connection trend",
    "narrative": "one or two paragraphs summarizing the whole app's health",
    "previous": null | {"health_score": 72, "grade": "C"},
    "anomalies": [
      {"level": "warn" | "crit", "title": "RDS connections rising", "message": "...", "anchor": "rds"}
    ]
  },
  "cost": null | {
    "state": "healthy" | "unknown",
    "cycle": "2026-08",
    "currency": "USD",
    "total": 12.40,
    "breakdown": [
      {"product": "ecs", "amount": 7.80},
      {"product": "rds", "amount": 4.60}
    ],
    "evaluation": "utilization-based note, e.g. CPU steady at 31% — right-sized",
    "suggestion": "optional optimization idea; never an estimate of spend",
    "reason": "only when state is unknown: e.g. no actual bill for this cycle yet"
  },
  "recommendations": {
    "immediate": ["..."],
    "short_term": ["..."],
    "long_term": ["..."]
  },
  "unknowns": ["item + why it could not be determined", "..."],
  "next_step": "optional: offer qwencloud-operate when a real fault is found"
}

Notes:
- Every layer state MUST be one of: healthy, degraded, unavailable, unknown.
- health_score is the SUM of the per-layer score values; grade must match it
  (>=90 A / >=75 B / >=60 C / <60 D). RDS is scored only when the app has one;
  otherwise its weight is redistributed to application and ECS.
- Cost carries the ACTUAL billed amount only. There is no estimate field; never
  invent one. Cost never contributes to health_score.
- When cost has no bill yet, set state "unknown" with a reason and omit total/breakdown.
- data_source: "cloudmonitor" when CloudMonitor agent trend metrics (memory in particular) are
  available; "fallback" when the agent is missing/failing and a metric drops to a read-only
  Cloud Assistant snapshot, whose evidence must note "point-in-time, no trend"; metrics obtainable
  by neither path are marked unknown.
- previous: optional. When a prior observe result exists, set the last health_score/grade; the
  report title then shows the score change.
"""


def _state_ok(s: Any) -> bool:
    return isinstance(s, str) and s in STATES


def _grade_for(score: Any) -> str:
    if not isinstance(score, (int, float)):
        return "?"
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 60:
        return "C"
    return "D"


def _delta_text(assessment: dict) -> str:
    prev = assessment.get("previous")
    if not isinstance(prev, dict):
        return ""
    ps = prev.get("health_score")
    cur = assessment.get("health_score")
    if not isinstance(ps, (int, float)) or not isinstance(cur, (int, float)):
        return ""
    pg = (prev.get("grade") or _grade_for(ps)).upper()
    cg = (assessment.get("grade") or _grade_for(cur)).upper()
    return f" (was {pg} {ps} → {cg} {cur})"


def validate(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["[root] top-level JSON must be an object"]

    layers = data.get("layers")
    has_rds = False
    if not isinstance(layers, dict):
        errors.append("[required] layers{} is missing")
        layers = {}
    else:
        for name in ("application", "ecs", "availability"):
            layer = layers.get(name)
            if not isinstance(layer, dict):
                errors.append(f"[required] layers.{name} is missing")
                continue
            if not _state_ok(layer.get("state")):
                errors.append(f"[enum] layers.{name}.state must be one of {STATES}")
            if layer.get("state") == "unknown" and not (layer.get("reason") or "").strip():
                errors.append(f"[rule] layers.{name} is unknown but has no reason")
            if not isinstance(layer.get("score"), (int, float)):
                errors.append(f"[required] layers.{name}.score must be a number")
        rds = layers.get("rds")
        if rds is not None:
            has_rds = True
            if not isinstance(rds, dict) or not _state_ok(rds.get("state")):
                errors.append(f"[enum] layers.rds.state must be one of {STATES}")
            elif not isinstance(rds.get("score"), (int, float)):
                errors.append("[required] layers.rds.score must be a number")

    assessment = data.get("assessment")
    if not isinstance(assessment, dict):
        errors.append("[required] assessment{} is missing")
    else:
        for key in ("health_score", "grade", "grade_label", "one_liner", "narrative"):
            v = assessment.get(key)
            if v is None or (isinstance(v, str) and not v.strip()):
                errors.append(f"[required] assessment.{key} must not be empty")

        score = assessment.get("health_score")
        grade = assessment.get("grade")
        if isinstance(score, (int, float)) and isinstance(grade, str):
            expected = _grade_for(score)
            if grade.upper() != expected:
                errors.append(
                    f"[logic] grade={grade} does not match health_score={score}; "
                    f"expected {expected} (>=90 A / >=75 B / >=60 C / <60 D)"
                )

        if isinstance(score, (int, float)) and isinstance(layers, dict):
            names = ("application", "ecs", "rds", "availability") if has_rds \
                else ("application", "ecs", "availability")
            total = 0
            ok = True
            for name in names:
                s = (layers.get(name) or {}).get("score")
                if isinstance(s, (int, float)):
                    total += s
                else:
                    ok = False
            if ok and abs(total - score) > 0.5:
                errors.append(
                    f"[logic] health_score={score} must equal the sum of layer scores ({total})"
                )

        one_liner = (assessment.get("one_liner") or "").strip().lower()
        if isinstance(score, (int, float)) and score < 60 and one_liner:
            for kw in ("all normal", "everything is fine", "no issues", "running normally", "healthy"):
                if kw in one_liner:
                    errors.append(
                        f"[logic] health_score={score} is below 60 but one_liner suggests a normal status"
                    )
                    break

    cost = data.get("cost")
    if cost is not None:
        if not isinstance(cost, dict):
            errors.append("[type] cost must be an object or null")
        else:
            st = cost.get("state")
            if st not in ("healthy", "unknown"):
                errors.append("[enum] cost.state must be healthy or unknown")
            blob = json.dumps(cost, ensure_ascii=False).lower()
            if "estimate" in blob or "预估" in blob:
                errors.append("[rule] cost must be the ACTUAL billed amount only; no estimate")
            if st == "unknown":
                if not (cost.get("reason") or "").strip():
                    errors.append("[rule] cost is unknown but has no reason")
            else:
                if not isinstance(cost.get("total"), (int, float)):
                    errors.append("[required] cost.total must be a number when state is healthy")
                cur = cost.get("currency")
                if cur and cur != CURRENCY:
                    errors.append(f"[rule] cost.currency should be {CURRENCY} on this site")
    return errors


_BADGE = {
    "healthy": "🟢 healthy",
    "degraded": "🟡 degraded",
    "unavailable": "🔴 unavailable",
    "unknown": "⚪ unknown",
}
_GRADE_ICON = {"A": "🟢", "B": "🟡", "C": "🟠", "D": "🔴"}
_LAYER_LABEL = {"application": "Application", "ecs": "ECS", "rds": "RDS",
                "availability": "Availability"}


def _money(amount: Any, currency: str = CURRENCY) -> str:
    sym = "$" if currency == "USD" else "¥"
    try:
        return f"{sym}{float(amount):.2f}"
    except (TypeError, ValueError):
        return "N/A"


def _ordered_layers(layers: dict):
    for name in ("application", "ecs", "rds", "availability"):
        layer = layers.get(name)
        if isinstance(layer, dict):
            yield name, layer


def render_md(data: dict) -> str:
    meta = data.get("meta", {}) or {}
    layers = data.get("layers", {}) or {}
    assessment = data.get("assessment", {}) or {}
    cost = data.get("cost")
    rec = data.get("recommendations", {}) or {}
    out: list[str] = []

    grade = (assessment.get("grade") or "?").upper()
    icon = _GRADE_ICON.get(grade, "")
    out.append(f"# Observe Report — {meta.get('app', 'application')}")
    out.append("")
    delta = _delta_text(assessment)
    out.append(f"{icon} **{assessment.get('health_score', '?')} / 100** · "
               f"{grade} {assessment.get('grade_label', '')}{delta} · "
               f"{assessment.get('one_liner', '')}".strip())
    out.append("")
    if assessment.get("narrative"):
        out.append(assessment["narrative"])
        out.append("")

    out.append("## Scores by dimension")
    out.append("")
    out.append("| Dimension | Grade | Score | State | Evidence |")
    out.append("|---|---|---|---|---|")
    for name, layer in _ordered_layers(layers):
        st = layer.get("state", "unknown")
        out.append(
            f"| {_LAYER_LABEL.get(name, name)} "
            f"| {_BADGE.get(st, st).split(' ')[0]} "
            f"| {layer.get('score', '?')}/{layer.get('max_score', '?')} "
            f"| {st} | {(layer.get('evidence') or layer.get('reason') or '').replace('|', '/')} |"
        )
    out.append("")

    anomalies = assessment.get("anomalies") or []
    if anomalies:
        out.append("## Anomalies")
        for a in anomalies:
            mark = "🔴" if a.get("level") == "crit" else "🟠"
            anchor = a.get("anchor")
            title = a.get("title", "")
            title = f"[{title}](#{anchor})" if anchor else f"**{title}**"
            out.append(f"- {mark} {title}: {a.get('message', '')}")
        out.append("")

    for name, layer in _ordered_layers(layers):
        out.append(f'<a id="{name}"></a>')
        out.append("")
        out.append(f"## {_LAYER_LABEL.get(name, name)}")
        st = layer.get("state", "unknown")
        out.append(f"{_BADGE.get(st, st)} · {layer.get('score', '?')}/{layer.get('max_score', '?')}")
        metrics = layer.get("metrics") or []
        if metrics:
            out.append("")
            out.append("| Metric | Value | Threshold | Trend |")
            out.append("|---|---|---|---|")
            for m in metrics:
                out.append(f"| {m.get('name', '')} | {m.get('value', '')} | "
                           f"{m.get('threshold', '')} | {m.get('trend', '')} |")
        if layer.get("detail"):
            out.append("")
            out.append(layer["detail"])
        out.append("")

    if isinstance(cost, dict):
        out.append("## Cost (actual billed)")
        if cost.get("state") == "unknown":
            out.append(f"- {_BADGE['unknown']} — {cost.get('reason', 'no actual bill yet')}")
        else:
            cur = cost.get("currency", CURRENCY)
            out.append(f"- Cycle {cost.get('cycle', '')}: **{_money(cost.get('total'), cur)}** {cur}")
            for row in cost.get("breakdown", []) or []:
                out.append(f"  - {row.get('product', '?')}: {_money(row.get('amount'), cur)}")
        if cost.get("evaluation"):
            out.append(f"- Evaluation: {cost['evaluation']}")
        if cost.get("suggestion"):
            out.append(f"- Suggestion: {cost['suggestion']}")
        out.append("")

    buckets = [("immediate", "Immediate"), ("short_term", "Short-term"), ("long_term", "Long-term")]
    if any(rec.get(k) for k, _ in buckets):
        out.append("## Recommendations")
        for key, label in buckets:
            items = rec.get(key) or []
            if items:
                out.append(f"**{label}**")
                out += [f"- {i}" for i in items]
        out.append("")

    unknowns = data.get("unknowns") or []
    if unknowns:
        out.append("## Unknown / not determined")
        out += [f"- {u}" for u in unknowns]
        out.append("")

    ra = data.get("recent_action")
    if isinstance(ra, dict) and ra.get("action"):
        v = f" ({ra['verification']})" if ra.get("verification") else ""
        out.append(f"> Last operate: {ra.get('time', '')} {ra['action']}{v}")
        out.append("")

    if data.get("next_step"):
        out.append(f"> Next step: {data['next_step']}")
        out.append("")

    ctx = " · ".join(str(x) for x in (
        meta.get("region_label") or meta.get("region"),
        f"window {meta.get('window')}" if meta.get("window") else None,
        f"source {meta.get('data_source')}" if meta.get("data_source") else None,
        meta.get("generated_at"),
    ) if x)
    if ctx:
        out.append(f"_Data as of: {ctx}_")
    return "\n".join(out).rstrip() + "\n"


def _esc(s: Any) -> str:
    return html.escape(str(s), quote=False)


_COLOR = {"healthy": "#00b894", "degraded": "#e17055",
          "unavailable": "#d63031", "unknown": "#636e72"}

CSS = """
  :root { --bg:#f5f6fa; --card:#fff; --text:#2d3436; --muted:#636e72; --border:#dfe6e9;
          --green:#00b894; --green-bg:#e6faf3; --orange:#e17055; --red:#d63031; --accent:#6c5ce7; }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family:-apple-system,"PingFang SC","Microsoft YaHei",Segoe UI,Roboto,sans-serif;
         background:var(--bg); color:var(--text); line-height:1.6; padding:24px 16px; }
  .container { max-width:960px; margin:0 auto; }
  .header { background:linear-gradient(135deg,#6c5ce7,#a29bfe); color:#fff; text-align:center;
            padding:36px 24px; border-radius:12px 12px 0 0; }
  .header h1 { font-size:24px; font-weight:700; margin-bottom:10px; }
  .header .score { font-size:40px; font-weight:800; }
  .header .meta { font-size:13px; opacity:.9; display:flex; gap:20px; justify-content:center;
                  flex-wrap:wrap; margin-top:10px; }
  .card { background:var(--card); border:1px solid var(--border); border-radius:12px;
          padding:24px 28px; margin-bottom:18px; }
  .card:first-of-type { border-radius:0 0 12px 12px; }
  .section-title { font-size:17px; font-weight:700; margin-bottom:14px; padding-bottom:8px;
                   border-bottom:2px solid var(--accent); display:flex; align-items:center; gap:8px; }
  table { width:100%; border-collapse:collapse; margin:10px 0; font-size:14px; }
  th,td { padding:9px 12px; border:1px solid var(--border); text-align:left; }
  th { background:#f8f9fa; font-weight:600; color:var(--muted); }
  .ta-c { text-align:center; }
  .rating { display:inline-block; padding:2px 10px; border-radius:10px; font-size:12px; font-weight:700; }
  .rating-a { background:var(--green-bg); color:#00a376; }
  .rating-b { background:#fff8e1; color:#f39c12; }
  .rating-c { background:#fff3e0; color:#e17055; }
  .rating-d { background:#ffeaea; color:#d63031; }
  .badge { display:inline-block; padding:2px 8px; border-radius:10px; color:#fff; font-size:12px; }
  .highlight { border-left:3px solid var(--green); background:#f0faf6; padding:11px 15px;
               border-radius:0 8px 8px 0; margin:10px 0; font-size:14px; }
  .highlight.warn { background:#fff8e1; border-color:var(--orange); }
  .highlight.crit { background:#ffeaea; border-color:var(--red); }
  .note { color:var(--muted); font-size:13px; margin:6px 0; }
  ul { padding-left:20px; } li { margin:4px 0; font-size:14px; }
  .footer { text-align:center; color:var(--muted); font-size:12px; padding:18px 0; }
"""


def _grade_letter(g: str) -> str:
    return (g or "a").lower()


def _badge_html(st: str) -> str:
    return f'<span class="badge" style="background:{_COLOR.get(st, "#636e72")}">{_esc(st)}</span>'


def _metric_table(metrics: list) -> str:
    if not metrics:
        return ""
    rows = "".join(
        f'<tr><td>{_esc(m.get("name", ""))}</td>'
        f'<td class="ta-c">{_esc(m.get("value", ""))}</td>'
        f'<td class="ta-c">{_esc(m.get("threshold", ""))}</td>'
        f'<td class="ta-c">{_esc(m.get("trend", ""))}</td></tr>'
        for m in metrics
    )
    return ("<table><tr><th>Metric</th><th class='ta-c'>Value</th>"
            "<th class='ta-c'>Threshold</th><th class='ta-c'>Trend</th></tr>"
            f"{rows}</table>")


def render_header(meta: dict, assessment: dict) -> str:
    grade = (assessment.get("grade") or "?").upper()
    icon = _GRADE_ICON.get(grade, "")
    delta = _delta_text(assessment)
    delta_html = f'<div class="meta"><span>{_esc(delta.strip())}</span></div>' if delta else ""
    return f"""
<div class="header">
  <h1>{icon} Observe Report — {_esc(meta.get('app', 'application'))}</h1>
  <div class="score">{_esc(assessment.get('health_score', '?'))} <span style="font-size:18px">/ 100</span>
    &nbsp;<span class="rating rating-{_grade_letter(grade)}">{grade} · {_esc(assessment.get('grade_label', ''))}</span></div>
  {delta_html}
  <div class="meta">
    <span>{_esc(assessment.get('one_liner', ''))}</span>
  </div>
</div>
"""


def render_overview(layers: dict, assessment: dict) -> str:
    rows = []
    for name, layer in _ordered_layers(layers):
        st = layer.get("state", "unknown")
        rows.append(
            f'<tr><td>{_LAYER_LABEL.get(name, name)}</td>'
            f'<td class="ta-c">{_badge_html(st)}</td>'
            f'<td class="ta-c">{_esc(layer.get("score", "?"))}/{_esc(layer.get("max_score", "?"))}</td>'
            f'<td>{_esc(layer.get("evidence") or layer.get("reason") or "")}</td></tr>'
        )
    anomalies = ""
    for a in assessment.get("anomalies", []) or []:
        lvl = a.get("level", "warn")
        mark = "🔴" if lvl == "crit" else "🟠"
        anchor = a.get("anchor", "")
        link = f' &rarr; <a href="#{_esc(anchor)}">see section</a>' if anchor else ""
        anomalies += (f'<div class="highlight {lvl}">{mark} <b>{_esc(a.get("title", ""))}</b>: '
                      f'{_esc(a.get("message", ""))}{link}</div>')
    if not anomalies:
        anomalies = '<div class="highlight">✅ <b>No anomalies</b> — all layers within healthy thresholds.</div>'
    narrative = f'<p>{_esc(assessment.get("narrative", ""))}</p>' if assessment.get("narrative") else ""
    return f"""
<div class="card">
  <div class="section-title">📊 Overview</div>
  {narrative}
  <table>
    <tr><th>Dimension</th><th class="ta-c">State</th><th class="ta-c">Score</th><th>Evidence</th></tr>
    {''.join(rows)}
  </table>
  <p class="note">Grade legend: 🟢 A (&ge;90) · 🟡 B (&ge;75) · 🟠 C (&ge;60) · 🔴 D (&lt;60). Cost is shown separately and does not affect the score.</p>
  {anomalies}
</div>
"""


_LAYER_ICON = {"application": "🌐", "ecs": "🖥️", "rds": "🗄️", "availability": "✅"}


def render_layer_card(name: str, layer: dict) -> str:
    st = layer.get("state", "unknown")
    detail = f'<p>{_esc(layer.get("detail", ""))}</p>' if layer.get("detail") else ""
    return f"""
<div class="card" id="{name}">
  <div class="section-title">{_LAYER_ICON.get(name, '')} {_LAYER_LABEL.get(name, name)}
    &nbsp;{_badge_html(st)}
    &nbsp;<span class="note">{_esc(layer.get('score', '?'))}/{_esc(layer.get('max_score', '?'))}</span></div>
  <p>{_esc(layer.get('evidence') or layer.get('reason') or '')}</p>
  {_metric_table(layer.get('metrics') or [])}
  {detail}
</div>
"""


def render_cost_card(cost: dict) -> str:
    if cost.get("state") == "unknown":
        body = f'<p>{_badge_html("unknown")} {_esc(cost.get("reason", "no actual bill yet"))}</p>'
    else:
        cur = cost.get("currency", CURRENCY)
        items = "".join(
            f"<li>{_esc(r.get('product', '?'))}: {_esc(_money(r.get('amount'), cur))}</li>"
            for r in (cost.get("breakdown") or [])
        )
        body = (f"<p>Cycle {_esc(cost.get('cycle', ''))}: "
                f"<strong>{_esc(_money(cost.get('total'), cur))}</strong> {_esc(cur)}</p>"
                f"<ul>{items}</ul>")
    rows = ""
    if cost.get("evaluation"):
        rows += f"<tr><td style='width:140px'><b>Evaluation</b></td><td>{_esc(cost['evaluation'])}</td></tr>"
    if cost.get("suggestion"):
        rows += f"<tr><td><b>Suggestion</b></td><td>{_esc(cost['suggestion'])}</td></tr>"
    table = f"<table>{rows}</table>" if rows else ""
    return f"""
<div class="card" id="cost">
  <div class="section-title">💰 Cost (actual billed)</div>
  {body}
  {table}
  <p class="note">Actual billed amount only; never an estimate. Cost does not affect the health score.</p>
</div>
"""


def render_reco_card(rec: dict) -> str:
    def _ul(items):
        if not items:
            return '<p class="note">None.</p>'
        return "<ul>" + "".join(f"<li>{_esc(i)}</li>" for i in items) + "</ul>"
    return f"""
<div class="card">
  <div class="section-title">💡 Recommendations</div>
  <h4>⚡ Immediate</h4>{_ul(rec.get('immediate') or [])}
  <h4 style="margin-top:10px">📅 Short-term</h4>{_ul(rec.get('short_term') or [])}
  <h4 style="margin-top:10px">🔭 Long-term</h4>{_ul(rec.get('long_term') or [])}
</div>
"""


def render_footer(meta: dict, next_step: str, recent_action: dict | None = None) -> str:
    ns = f'<p>Next step: {_esc(next_step)}</p>' if next_step else ""
    ra = ""
    if isinstance(recent_action, dict) and recent_action.get("action"):
        v = f" ({recent_action['verification']})" if recent_action.get("verification") else ""
        ra = f"<p>Last operate: {_esc(recent_action.get('time', ''))} {_esc(recent_action['action'])}{_esc(v)}</p>"
    return f"""
<div class="footer">
  {ns}
  {ra}
  <p>Region {_esc(meta.get('region_label') or meta.get('region', 'N/A'))} · window {_esc(meta.get('window', 'N/A'))} · source {_esc(meta.get('data_source', 'N/A'))} · {_esc(meta.get('generated_at', ''))}</p>
</div>
"""


def render_html(data: dict) -> str:
    meta = data.get("meta", {}) or {}
    layers = data.get("layers", {}) or {}
    assessment = data.get("assessment", {}) or {}
    cost = data.get("cost")
    rec = data.get("recommendations", {}) or {}

    cards = [render_header(meta, assessment), '<div class="container">',
             render_overview(layers, assessment)]
    for name, layer in _ordered_layers(layers):
        cards.append(render_layer_card(name, layer))
    if isinstance(cost, dict):
        cards.append(render_cost_card(cost))
    if any(rec.get(k) for k in ("immediate", "short_term", "long_term")):
        cards.append(render_reco_card(rec))
    unknowns = data.get("unknowns") or []
    if unknowns:
        lis = "".join(f"<li>{_esc(u)}</li>" for u in unknowns)
        cards.append(f'<div class="card"><div class="section-title">❓ Unknown / not determined</div><ul>{lis}</ul></div>')
    cards.append(render_footer(meta, data.get("next_step", ""), data.get("recent_action")))
    cards.append("</div>")

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Observe Report — {_esc(meta.get('app', 'application'))}</title>
<style>{CSS}</style></head><body>
{''.join(cards)}
</body></html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Render an observe report from JSON.")
    parser.add_argument("--input", "-i", help="Path to JSON input; defaults to stdin.")
    parser.add_argument("--output", "-o", help="Path to write output; required unless --schema/--validate.")
    parser.add_argument("--format", "-f", choices=("md", "html"), default="md",
                        help="Output format (default: md).")
    parser.add_argument("--schema", action="store_true", help="Print the JSON schema and exit.")
    parser.add_argument("--validate", action="store_true",
                        help="Validate the input JSON without rendering.")
    args = parser.parse_args()

    if args.schema:
        print(SCHEMA_DOC)
        return 0

    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    if args.validate:
        errs = validate(data)
        if errs:
            print("✗ JSON validation failed:", file=sys.stderr)
            for e in errs:
                print(f"  - {e}", file=sys.stderr)
            return 1
        print("✓ JSON validation passed", file=sys.stderr)
        return 0

    if not args.output:
        parser.error("--output is required unless using --schema or --validate")

    errs = validate(data)
    if errs:
        print("⚠ pre-render validation issues (fix per SKILL Report section):", file=sys.stderr)
        for e in errs:
            print(f"  - {e}", file=sys.stderr)

    text = render_html(data) if args.format == "html" else render_md(data)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"✓ {args.format} report written to: {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
