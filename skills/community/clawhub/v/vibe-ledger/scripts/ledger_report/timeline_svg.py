"""Diagram C: the conversation over time. Four lanes (you said / error /
AI changed / for later) and a 'today' column showing where each item stands."""
from __future__ import annotations

from collections import Counter

from ledger_report.bits import GLYPH, ORDER, h, hf, ht
from ledger_report.i18n import t

LANES = ("you_said", "error", "ai_changed", "deferred")
LANE_OF_TYPE = {"user_requirement": "you_said", "ai_claim": "ai_changed", "deferred": "deferred"}
MAX_ITEMS = 16
X0, TODAY_W, PILL_H, TOP = 130, 270, 24, 58
MAX_WIDTH = 980  # fits the page; longer histories scroll inside their box
PILL_UNITS = 34  # display width of a status pill's text
COMPROMISE_STATUS = {True: "broken", False: "kept", None: "unknown"}


def build_items(ledger: dict) -> tuple[list, list]:
    ev = ledger["evidence"]
    items = []
    for p in ledger["promises"]:
        src = next((ev[i] for i in p["source"] if ev.get(i, {}).get("ok")), None)
        if src is None:
            continue
        lane = LANE_OF_TYPE[p["type"]]
        items.append({"key": p["id"], "status": p["status"], "label": p["plain"], "lane": lane,
                      "events": [(src.get("ts", ""), lane, src.get("quote", ""))], "compromise": False})
    for c in ledger["compromises"]:
        events = []
        err = ev.get(c["error"], {})
        if err.get("ok"):
            events.append((err.get("ts", ""), "error", err.get("quote", "")))
        change = next((ev[i] for i in c["change"] if ev.get(i, {}).get("ok")), None)
        if change:
            events.append((change.get("ts", ""), "ai_changed", change.get("quote", "")))
        if events:
            items.append({"key": c["id"], "status": COMPROMISE_STATUS[c.get("still_present")],
                          "label": c.get("bypassed", ""), "lane": "error", "events": events,
                          "compromise": True, "still": c.get("still_present")})
    items.sort(key=lambda it: (ORDER.index(it["status"]), min(e[0] for e in it["events"])))
    return items[:MAX_ITEMS], items[MAX_ITEMS:]


def _marker(lane: str, x: float, y: float, status: str, quote: str) -> str:
    cls = f"mk s-{status}"
    tip = f"<title>{ht(quote, 160)}</title>"
    if lane == "you_said":
        return f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="7">{tip}</circle>'
    if lane == "error":
        return f'<path class="{cls}" d="M{x:.1f},{y - 8:.1f} L{x + 8:.1f},{y + 6:.1f} L{x - 8:.1f},{y + 6:.1f} Z">{tip}</path>'
    if lane == "ai_changed":
        return f'<rect class="{cls}" x="{x - 6.5:.1f}" y="{y - 6.5:.1f}" width="13" height="13" rx="2">{tip}</rect>'
    return f'<path class="{cls}" d="M{x:.1f},{y - 8:.1f} L{x + 8:.1f},{y:.1f} L{x:.1f},{y + 8:.1f} L{x - 8:.1f},{y:.1f} Z">{tip}</path>'


def _pill_text(it: dict, lang: str) -> str:
    if it["compromise"]:
        word = {True: t(lang, "still_present"), False: t(lang, "fixed"), None: t(lang, "unclear")}[it["still"]]
        return f'{GLYPH[it["status"]]} {t(lang, "compromise")}: {it["label"]} · {word}'
    return f'{GLYPH[it["status"]]} {it["label"]}'


def render_timeline(ledger: dict, lang: str, has_transcripts: bool) -> str:
    if not has_transcripts:
        return f'<p class="empty">{h(t(lang, "no_transcripts_timeline"))}</p>'
    items, overflow = build_items(ledger)
    if not items:
        return f'<p class="empty">{h(t(lang, "no_timeline_items"))}</p>'
    events = sorted((ts, lane, k, quote) for k, it in enumerate(items) for ts, lane, quote in it["events"])
    step = max(28.0, min(90.0, (MAX_WIDTH - X0 - 40 - TODAY_W) / len(events)))
    x_today = X0 + len(events) * step + 40
    width = int(x_today + TODAY_W)
    per_lane = Counter(it["lane"] for it in items)
    lane_h = {lane: max(52, per_lane[lane] * (PILL_H + 6) + 16) for lane in LANES}
    lane_y, y = {}, TOP
    for lane in LANES:
        lane_y[lane] = y
        y += lane_h[lane]
    height = y + 16
    mid = {lane: lane_y[lane] + (lane_h[lane] - 4) / 2 for lane in LANES}
    out = [f'<div class="scroll-x"><svg class="diagram timeline" viewBox="0 0 {width} {height}" width="{width}" '
           f'height="{height}" role="img" aria-label="{h(t(lang, "sec_timeline"))}">']
    for lane in LANES:
        out.append(f'<rect class="tl-band" x="0" y="{lane_y[lane]}" width="{width}" height="{lane_h[lane] - 4}" rx="8"/>')
        out.append(f'<text class="tl-lane" x="12" y="{mid[lane] + 5:.1f}">{h(t(lang, "lane_" + lane))}</text>')
    out.append(f'<rect class="tl-today" x="{x_today - 14:.1f}" y="{TOP - 30}" width="{TODAY_W - 2}" '
               f'height="{height - TOP + 26}" rx="10"/>')
    out.append(f'<text class="tl-date today" x="{x_today:.1f}" y="{TOP - 12}">{h(t(lang, "today"))}</text>')
    positions: dict[int, list] = {}
    last_day, last_label = None, -99
    for idx, (ts, lane, k, quote) in enumerate(events):
        x = X0 + idx * step + step / 2
        day = ts[5:10]
        tick = day if day and day != last_day else (ts[11:16] if idx - last_label >= 3 and len(ts) >= 16 else "")
        if tick:
            out.append(f'<text class="tl-date" x="{x:.1f}" y="{TOP - 12}" text-anchor="middle">{h(tick)}</text>')
            last_day, last_label = day, idx
        positions.setdefault(k, []).append((x, mid[lane], lane, quote))
    used, pill_y = Counter(), {}
    for k, it in enumerate(items):
        pill_y[k] = lane_y[it["lane"]] + 8 + used[it["lane"]] * (PILL_H + 6)
        used[it["lane"]] += 1
    for k, it in enumerate(items):
        pts = positions[k]
        for (x1, y1, _, _), (x2, y2, _, _) in zip(pts, pts[1:]):
            out.append(f'<path class="tl-link s-{it["status"]}" d="M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}"/>')
        x, yv = pts[-1][0], pts[-1][1]
        py = pill_y[k] + PILL_H / 2
        out.append(f'<path class="arc s-{it["status"]}" d="M{x:.1f},{yv:.1f} C{x + 60:.1f},{yv:.1f} '
                   f'{x_today - 70:.1f},{py:.1f} {x_today - 8:.1f},{py:.1f}"/>')
    for k, it in enumerate(items):
        for x, yv, lane, quote in positions[k]:
            out.append(_marker(lane, x, yv, it["status"], quote))
        out.append(f'<g class="tl-pill s-{it["status"]}"><rect x="{x_today - 6:.1f}" y="{pill_y[k]}" '
                   f'width="{TODAY_W - 22}" height="{PILL_H}" rx="12"/>'
                   f'<text x="{x_today + 6:.1f}" y="{pill_y[k] + 16}">{hf(_pill_text(it, lang), PILL_UNITS)}</text></g>')
    out.append("</svg></div>")
    if overflow:
        out.append(f'<p class="note">{h(t(lang, "more_items", n=len(overflow)))}</p>')
    return "".join(out)
