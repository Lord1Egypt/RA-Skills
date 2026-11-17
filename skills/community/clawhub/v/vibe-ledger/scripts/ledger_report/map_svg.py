"""Diagram A: where the data goes. Three fixed lanes (browser | your server |
storage & outside services) so the layout is the same every time. Edge labels
live in the gaps between lanes and are drawn last, so no box ever hides them."""
from __future__ import annotations

from ledger_report.bits import h, hf
from ledger_report.i18n import t

LANES = ("browser", "server", "storage")
MAX_NODES = 12
WIDTH, LANE_W = 960, 230
LANE_X = (15, 365, 715)
GAP_W = LANE_X[1] - LANE_X[0] - LANE_W  # 120 px between lanes, where edge labels go
NODE_H, GAP, TOP = 66, 18, 62
LABEL_UNITS = 16  # display width of one edge-label line (≈ 8 CJK characters)


def _risky(m: dict) -> set:
    ids = set()
    for e in m["edges"]:
        if e.get("risk"):
            ids.update((e["from"], e["to"]))
    return ids


def select_nodes(m: dict) -> tuple[list, list]:
    risky = _risky(m)
    ranked = sorted(m["nodes"], key=lambda n: (n["id"] not in risky, not n.get("paid"), -len(n.get("evidence", []))))
    return ranked[:MAX_NODES], ranked[MAX_NODES:]


def _code_ref(node: dict, evidence: dict) -> str:
    for eid in node.get("evidence", []):
        e = evidence.get(eid, {})
        if e.get("ok") and e.get("kind") in ("code", "probe") and e.get("path"):
            return f"{e['path']}:{e.get('line', '')}"
    return ""


def _edge(a: tuple, b: tuple, e: dict, detour_y: float | None = None) -> tuple[str, str]:
    """(path markup, label markup) for one edge between node positions a and b.
    An edge that skips the middle lane dips to `detour_y` (below that lane's boxes)
    so it never seems to start from a box it only passes behind."""
    (ax, ay), (bx, by) = a, b
    la, lb = LANE_X.index(ax), LANE_X.index(bx)
    y1, y2 = ay + NODE_H / 2, by + NODE_H / 2
    if la == lb:
        side = 1 if la < len(LANES) - 1 else -1  # loop into the gap that exists
        x1 = x2 = ax + LANE_W if side > 0 else ax
        d = f"M{x1},{y1:.1f} C{x1 + 46 * side},{y1:.1f} {x2 + 46 * side},{y2:.1f} {x2},{y2:.1f}"
        mx, my = x1 + (GAP_W / 2) * side, (y1 + y2) / 2
    else:
        forward = la < lb
        x1, x2 = (ax + LANE_W, bx) if forward else (ax, bx + LANE_W)
        if abs(la - lb) > 1 and detour_y is not None:
            xm = LANE_X[1] + LANE_W / 2
            d = (f"M{x1},{y1:.1f} C{x1 + 50:.1f},{y1:.1f} {xm - 90:.1f},{detour_y:.1f} {xm:.1f},{detour_y:.1f} "
                 f"S{x2 - 50:.1f},{y2:.1f} {x2},{y2:.1f}")
        else:
            dx = (x2 - x1) / 2
            d = f"M{x1},{y1:.1f} C{x1 + dx:.1f},{y1:.1f} {x2 - dx:.1f},{y2:.1f} {x2},{y2:.1f}"
        # label in the gap next to the target lane, so it never lands on a box in a skipped lane
        mx = x2 - GAP_W / 2 if forward else x2 + GAP_W / 2
        my = y2 if abs(la - lb) > 1 else (y1 + y2) / 2
    risk = bool(e.get("risk"))
    carries = e.get("carries") or ""
    full = f"⚠ {carries} — {e['risk']}" if risk and carries else (f"⚠ {e['risk']}" if risk else carries)
    marker = "arrow-map-risk" if risk else "arrow-map"
    path = f'<path class="edge{" risk" if risk else ""}" d="{d}" marker-end="url(#{marker})"/>'
    lines = []
    if carries:
        lines.append(("edge-label", carries))
    if risk:
        lines.append(("edge-label risk", "⚠ " + e["risk"]))
    top = my - 8 - 16 * (len(lines) - 1)  # every line sits above the edge, never on it
    texts = "".join(f'<text class="{cls}" x="{mx:.1f}" y="{top + 16 * i:.1f}" text-anchor="middle">{hf(txt, LABEL_UNITS)}</text>'
                    for i, (cls, txt) in enumerate(lines))
    label = f'<g class="edge-text"><title>{h(full)}</title>{texts}</g>' if lines else ""
    return path, label


def _notes(overflow: list, unverified: list, lang: str) -> str:
    sep = h(t(lang, "sep"))
    out = ""
    if overflow:
        out += f'<p class="note">{h(t(lang, "other_nodes"))}' + sep.join(hf(n["label"], 40) for n in overflow) + "</p>"
    if unverified:
        out += (f'<p class="note unverified">{h(t(lang, "unverified_nodes"))}'
                + sep.join(hf(n["label"], 40) for n in unverified) + "</p>")
    return out


def render_map(ledger: dict, lang: str) -> str:
    m, ev = ledger["map"], ledger["evidence"]
    shown, overflow = select_nodes(m)
    notes = _notes(overflow, m.get("unverified_nodes", []), lang)
    if not shown:
        return f'<p class="empty">{h(t(lang, "no_map"))}</p>' + notes
    pos, used = {}, {lane: 0 for lane in LANES}
    for n in shown:
        i = used[n["lane"]]
        used[n["lane"]] += 1
        pos[n["id"]] = (LANE_X[LANES.index(n["lane"])], TOP + i * (NODE_H + GAP))
    height = TOP + max(used.values()) * (NODE_H + GAP) + 34
    out = [f'<div class="diagram-wrap"><svg class="diagram map" viewBox="0 0 {WIDTH} {height}" role="img" '
           f'aria-label="{h(t(lang, "sec_map"))}"><defs>'
           '<marker id="arrow-map" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="8" markerHeight="8" orient="auto">'
           '<path class="arrowhead" d="M0,0 L8,4 L0,8 z"/></marker>'
           '<marker id="arrow-map-risk" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="8" markerHeight="8" orient="auto">'
           '<path class="arrowhead risk" d="M0,0 L8,4 L0,8 z"/></marker></defs>']
    own = m.get("lane_labels") or {}
    for i, lane in enumerate(LANES):
        x = LANE_X[i]
        out.append(f'<rect class="lane" x="{x - 6}" y="12" width="{LANE_W + 12}" height="{height - 40}" rx="14"/>')
        out.append(f'<text class="lane-title" x="{x + LANE_W / 2:.1f}" y="40" text-anchor="middle">{h(own.get(lane) or t(lang, "lane_" + lane))}</text>')
    labels = []
    detour = TOP + used["server"] * (NODE_H + GAP) - GAP / 2 + 6 if used["server"] else None
    for e in m["edges"]:
        if e["from"] in pos and e["to"] in pos:
            path, label = _edge(pos[e["from"]], pos[e["to"]], e, detour)
            out.append(path)
            labels.append(label)
    for n in shown:
        x, y = pos[n["id"]]
        out.append(f'<g class="node"><rect x="{x}" y="{y}" width="{LANE_W}" height="{NODE_H}" rx="10"/>'
                   f'<text class="node-label" x="{x + 14}" y="{y + 24}">{hf(n["label"], 26)}</text>')
        holds = ", ".join(n.get("holds", []))
        if holds:
            out.append(f'<text class="node-sub" x="{x + 14}" y="{y + 43}">{hf(holds, 32)}</text>')
        ref = _code_ref(n, ev)
        if ref:
            out.append(f'<text class="node-ref dev-only" x="{x + 14}" y="{y + 59}">{hf(ref, 32)}</text>')
        if n.get("paid"):
            out.append(f'<text class="paid" x="{x + LANE_W - 12}" y="{y + 24}" text-anchor="end">💰</text>')
        out.append("</g>")
    out.extend(labels)
    out.append(f'<text class="legend" x="15" y="{height - 10}">{h(t(lang, "legend_map"))}</text></svg></div>')
    return "".join(out) + notes
