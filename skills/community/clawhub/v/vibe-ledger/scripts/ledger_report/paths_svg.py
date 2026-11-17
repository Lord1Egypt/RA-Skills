"""Diagram E (developer view): what happens, step by step, after one action."""
from __future__ import annotations

from ledger_report.bits import h, ht
from ledger_report.i18n import t

BOX_W, BOX_H, GAP, ROW_GAP, PER_ROW = 200, 58, 40, 46, 4


def _ref(step: dict, evidence: dict) -> str:
    e = evidence.get(step.get("evidence"), {})
    if e.get("ok") and e.get("path"):
        return f"{e['path']}:{e.get('line', '')}"
    return ""


def render_paths(ledger: dict, lang: str) -> str:
    if not ledger["paths"]:
        return f'<p class="empty">{h(t(lang, "no_paths"))}</p>'
    ev = ledger["evidence"]
    out = []
    for path in ledger["paths"]:
        steps = path["steps"]
        rows = max(1, (len(steps) + PER_ROW - 1) // PER_ROW)
        width = 20 + PER_ROW * (BOX_W + GAP)
        height = 40 + rows * (BOX_H + ROW_GAP)
        svg = [f'<div class="diagram-wrap"><svg class="diagram paths" viewBox="0 0 {width} {height}" role="img" '
               f'aria-label="{ht(path["action"], 60)}"><defs><marker id="arrow-path" viewBox="0 0 8 8" refX="7" refY="4" '
               'markerWidth="8" markerHeight="8" orient="auto"><path class="arrowhead" d="M0,0 L8,4 L0,8 z"/></marker></defs>',
               f'<text class="path-title" x="10" y="22">{ht(path["action"], 60)}</text>']
        for i, st in enumerate(steps):
            r, c = divmod(i, PER_ROW)
            x, y = 10 + c * (BOX_W + GAP), 36 + r * (BOX_H + ROW_GAP)
            if i + 1 < len(steps):
                if c < PER_ROW - 1:
                    svg.append(f'<path class="flow" d="M{x + BOX_W},{y + BOX_H / 2} L{x + BOX_W + GAP - 4},{y + BOX_H / 2}" '
                               'marker-end="url(#arrow-path)"/>')
                else:
                    ny = y + BOX_H + ROW_GAP
                    svg.append(f'<path class="flow" d="M{x + BOX_W / 2},{y + BOX_H} L{x + BOX_W / 2},{y + BOX_H + ROW_GAP / 2} '
                               f'L{10 + BOX_W / 2},{y + BOX_H + ROW_GAP / 2} L{10 + BOX_W / 2},{ny - 4}" marker-end="url(#arrow-path)"/>')
            cls = "step" + (" warn" if st.get("warning") else "") + (" unverified" if st.get("unverified") else "")
            svg.append(f'<g class="{cls}"><rect x="{x}" y="{y}" width="{BOX_W}" height="{BOX_H}" rx="9"/>'
                       f'<text class="step-label" x="{x + 12}" y="{y + 24}">{ht(st["label"], 24)}</text>')
            ref = _ref(st, ev)
            if ref:
                svg.append(f'<text class="step-ref" x="{x + 12}" y="{y + 44}">{ht(ref, 30)}</text>')
            if st.get("unverified"):
                svg.append(f'<text class="step-unv" x="{x + BOX_W - 10}" y="{y + 16}" text-anchor="end">{h(t(lang, "unverified"))}</text>')
            if st.get("warning"):
                svg.append(f'<text class="step-warn" x="{x + 4}" y="{y + BOX_H + 16}">{ht("⚠ " + st["warning"], 30)}</text>')
            svg.append("</g>")
        svg.append("</svg></div>")
        out.append("".join(svg))
    return "".join(out)
