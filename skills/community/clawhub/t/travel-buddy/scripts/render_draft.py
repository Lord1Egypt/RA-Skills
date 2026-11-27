#!/usr/bin/env python3
"""The first page the traveller sees: a rough plan to decide on, in about ten minutes.

Usage: python render_draft.py <draft.json> [--workspace PATH] [--overwrite]

WHY THIS EXISTS
---------------
Measured on four runs, the first page reached the traveller 25 to 54 minutes after the start,
before any fact-check; the checkpoint before design was a chat message. Someone who only wants to
know whether a trip is worth it (what it costs, how to get there, where to stay) waited for a
day-by-day plan with opening hours they had not asked for yet. This page is what feasibility
ends in: how to get there with real fares, one or two areas to stay with real nightly prices, a
labelled estimate for daily spend, a one-line-per-day outline, and the questions the full plan
needs answered. It is also the single consolidated checkpoint (references/research-budget.md):
design and verification start only after the traveller answers it.

WHAT IT CHECKS
--------------
It refuses to render a price without a source and a check date (daily spend may instead be a
labelled estimate), dates that do not make a trip, and a draft with no questions. The all-in
range is computed here from the parts, never typed in, so the headline cannot disagree with the
cards under it. The page says at the top that it is a draft and not fact-checked.

The draft file is templates/trip-draft.json. With --workspace it saves the page to
<workspace>/html/draft-<start>-<destination>.html and the draft beside the plans.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plan_flags import is_search_url  # noqa: E402
from travel_workspace import DEFAULT_WORKSPACE  # noqa: E402

DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

WORDS = {
    "en": {
        "banner": "Draft to decide on. Not fact-checked yet: book nothing from this page.",
        "all_in": "About {amount} per person, all in",
        "parts": "Getting there {a} · stay {b} · daily spend {c}",
        "getting_there": "Getting there", "stay": "Where to stay", "outline": "Rough outline",
        "entry": "Entry", "decide": "To build the full plan, answer these",
        "per_person": "per person", "per_night": "per room per night", "checked": "checked",
        "estimate": "estimate", "search": "Search {source} (pick from the results)",
        "open": "Open on {source}", "daily": "Daily spend (food, local transport, entry fees)",
        "nights": "{n} nights", "travellers": "{n} traveller(s)",
        "stops": {0: "non-stop", 1: "1 stop"}, "stops_n": "{n} stops",
        "next": "Next: once these are answered, the full plan adds the day-by-day route, opening "
                "hours, reservations and a fact-check.",
    },
    "zh": {
        "banner": "草稿，用来做决定。还没有核查，请不要直接按这一页下单。",
        "all_in": "人均全部花费约 {amount}",
        "parts": "交通 {a} · 住宿 {b} · 每日开销 {c}",
        "getting_there": "怎么去", "stay": "住在哪一带", "outline": "大致安排",
        "entry": "入境", "decide": "回答这几个问题，就开始做完整计划",
        "per_person": "人均", "per_night": "每间每晚", "checked": "核对于",
        "estimate": "估算", "search": "在 {source} 搜索（需在结果里挑选）",
        "open": "在 {source} 打开", "daily": "每日开销（吃饭、市内交通、门票）",
        "nights": "{n} 晚", "travellers": "{n} 人",
        "stops": {0: "直飞", 1: "1 次中转"}, "stops_n": "{n} 次中转",
        "next": "下一步：回答这些问题后，完整计划会加上每天的路线、营业时间、预约和核查。",
    },
}


def _num(value: object) -> float | None:
    return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def validate(draft: dict) -> list[str]:
    errors = []
    for key in ("destination", "origin", "start_date", "end_date", "currency"):
        if not str(draft.get(key) or "").strip():
            errors.append(f"{key} is required")
    start, end = str(draft.get("start_date") or ""), str(draft.get("end_date") or "")
    if DATE.match(start) and DATE.match(end):
        if dt.date.fromisoformat(end) <= dt.date.fromisoformat(start):
            errors.append("end_date must be after start_date")
    else:
        errors.append("start_date and end_date must be YYYY-MM-DD")
    if not isinstance(draft.get("travellers"), int) or draft["travellers"] < 1:
        errors.append("travellers must be a whole number of at least 1")
    if not isinstance(draft.get("rooms", 1), int) or draft.get("rooms", 1) < 1:
        errors.append("rooms must be a whole number of at least 1")

    def priced(item: dict, where: str, fields: tuple[str, ...]) -> None:
        if any(_num(item.get(f)) is None for f in fields):
            errors.append(f"{where}: {' and '.join(fields)} must be numbers")
        if not str(item.get("source") or "").strip() or not DATE.match(str(item.get("checked_at") or "")):
            errors.append(f"{where}: a price needs its source and checked_at (YYYY-MM-DD); "
                          "a figure nobody looked up does not go on the page")
        url = item.get("url")
        if url is not None and not str(url).startswith("https://"):
            errors.append(f"{where}: url must be HTTPS")

    for kind, fields in (("getting_there", ("per_person_low", "per_person_high")),
                         ("stay_areas", ("nightly_low", "nightly_high"))):
        items = draft.get(kind)
        if not isinstance(items, list) or not items or not all(isinstance(i, dict) for i in items):
            errors.append(f"{kind} needs at least one option")
            continue
        for n, item in enumerate(items):
            priced(item, f"{kind}[{n}]", fields)
            if not str(item.get("label") or item.get("name") or "").strip():
                errors.append(f"{kind}[{n}] needs a label/name")
    spend = draft.get("daily_spend")
    if not isinstance(spend, dict) or _num(spend.get("per_person_low")) is None or _num(spend.get("per_person_high")) is None:
        errors.append("daily_spend needs per_person_low and per_person_high")
    elif spend.get("basis") != "estimate":
        priced(spend, "daily_spend", ("per_person_low", "per_person_high"))
    if not isinstance(draft.get("outline"), list) or not draft["outline"]:
        errors.append("outline needs one line per day")
    decisions = draft.get("decisions")
    if not isinstance(decisions, list) or not [d for d in decisions if str(d).strip()]:
        errors.append("decisions is the checkpoint: list every question the full plan needs answered")
    return errors


def cost_range(draft: dict) -> dict[str, tuple[float, float]]:
    """Per-person low/high for each part and the total."""
    nights = (dt.date.fromisoformat(draft["end_date"]) - dt.date.fromisoformat(draft["start_date"])).days
    people, rooms = draft["travellers"], draft.get("rooms", 1)
    there = draft["getting_there"]
    stay = draft["stay_areas"]
    spend = draft["daily_spend"]
    parts = {
        "getting_there": (min(t["per_person_low"] for t in there), max(t["per_person_high"] for t in there)),
        "stay": (min(s["nightly_low"] for s in stay) * nights * rooms / people,
                 max(s["nightly_high"] for s in stay) * nights * rooms / people),
        "daily": (spend["per_person_low"] * (nights + 1), spend["per_person_high"] * (nights + 1)),
    }
    parts["total"] = (sum(v[0] for v in parts.values()), sum(v[1] for v in parts.values()))
    return parts


def _money(currency: str, low: float, high: float) -> str:
    return f"{currency} {low:,.0f}" + (f"–{high:,.0f}" if round(high) != round(low) else "")


def render(draft: dict) -> str:
    lang = "zh" if str(draft.get("language") or "zh").startswith("zh") else "en"
    w = WORDS[lang]
    e = lambda v: html.escape(str(v if v is not None else ""))  # noqa: E731
    cur = draft["currency"]
    parts = cost_range(draft)
    nights = (dt.date.fromisoformat(draft["end_date"]) - dt.date.fromisoformat(draft["start_date"])).days

    def link(item: dict) -> str:
        url, source = item.get("url"), item.get("source")
        if not url:
            return ""
        label = (w["search"] if is_search_url(url) else w["open"]).format(source=source)
        return f'<a class="btn" href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(label)}</a>'

    def stops(n: object) -> str:
        if not isinstance(n, int):
            return ""
        return w["stops"].get(n) or w["stops_n"].format(n=n)

    there = "".join(
        f'<article class="card"><strong>{e(t.get("label"))}</strong>'
        f'<p>{e(t.get("outbound"))}{" · " + e(t.get("return")) if t.get("return") else ""} {e(stops(t.get("stops")))}</p>'
        f'<p class="big">{e(_money(cur, t["per_person_low"], t["per_person_high"]))} <span class="meta">{w["per_person"]}</span></p>'
        f'<p class="meta">{e(t.get("source"))} · {w["checked"]} {e(t.get("checked_at"))}</p>{link(t)}</article>'
        for t in draft["getting_there"])
    stay = "".join(
        f'<article class="card"><strong>{e(s.get("name"))}</strong><p>{e(s.get("why"))}</p>'
        f'<p class="big">{e(_money(cur, s["nightly_low"], s["nightly_high"]))} <span class="meta">{w["per_night"]}</span></p>'
        f'<p class="meta">{e(s.get("source"))} · {w["checked"]} {e(s.get("checked_at"))}</p>{link(s)}</article>'
        for s in draft["stay_areas"])
    spend = draft["daily_spend"]
    spend_meta = (w["estimate"] if spend.get("basis") == "estimate"
                  else f'{e(spend.get("source"))} · {w["checked"]} {e(spend.get("checked_at"))}')
    entry = draft.get("entry") if isinstance(draft.get("entry"), dict) else {}
    entry_block = (f'<section><h2>{w["entry"]}</h2><p>{e(entry.get("note"))}</p></section>'
                   if entry.get("note") else "")
    total = parts["total"]
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(draft.get("title") or draft["destination"])}</title>
<style>body{{margin:0;background:#f7f9fc;color:#162235;font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif}}main{{max-width:880px;margin:auto;padding:24px 16px 48px}}h1{{font-size:clamp(1.8rem,5vw,2.8rem);line-height:1.1;margin:8px 0}}section{{background:#fff;border:1px solid #d9e2ec;border-radius:14px;padding:18px;margin:16px 0}}.banner{{background:#fff5df;border-left:4px solid #8a4b08;color:#8a4b08;font-weight:700;padding:12px 14px;border-radius:0 10px 10px 0}}.total{{font-size:1.7rem;font-weight:800;margin:4px 0}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}}.card{{border:1px solid #d9e2ec;border-radius:12px;padding:12px}}.big{{font-size:1.25rem;font-weight:800;margin:6px 0}}.meta{{color:#5d6b7c;font-size:.9rem;font-weight:400}}.btn{{display:inline-block;margin-top:6px;padding:8px 12px;border-radius:9px;background:#0b6e69;color:#fff;text-decoration:none;font-weight:700}}ol li,ul li{{margin:6px 0}}</style></head>
<body><main data-trip-draft><p class="banner">{w["banner"]}</p>
<h1>{e(draft.get("title") or draft["destination"])}</h1>
<p>{e(draft["origin"])} → {e(draft["destination"])} · {e(draft["start_date"])} – {e(draft["end_date"])} · {w["nights"].format(n=nights)} · {w["travellers"].format(n=draft["travellers"])}</p>
<section><p class="total">{e(w["all_in"].format(amount=_money(cur, *total)))}</p>
<p class="meta">{e(w["parts"].format(a=_money(cur, *parts["getting_there"]), b=_money(cur, *parts["stay"]), c=_money(cur, *parts["daily"])))}</p></section>
<section><h2>{w["decide"]}</h2><ol>{"".join(f"<li>{e(d)}</li>" for d in draft["decisions"] if str(d).strip())}</ol><p class="meta">{w["next"]}</p></section>
<section><h2>{w["getting_there"]}</h2><div class="grid">{there}</div></section>
<section><h2>{w["stay"]}</h2><div class="grid">{stay}</div></section>
<section><h2>{w["daily"]}</h2><p class="big">{e(_money(cur, spend["per_person_low"], spend["per_person_high"]))} <span class="meta">{w["per_person"]} · {spend_meta}</span></p><p class="meta">{e(spend.get("note"))}</p></section>
<section><h2>{w["outline"]}</h2><ol>{"".join(f"<li>{e(line)}</li>" for line in draft["outline"])}</ol></section>
{entry_block}</main></body></html>'''


def safe_name(text: str) -> str:
    cleaned = "".join("-" if c in '/\\:*?"<>|（）()，, ' or c.isspace() else c for c in text)
    return re.sub(r"-{2,}", "-", cleaned).strip("-. ") or "trip"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("draft")
    parser.add_argument("--workspace", default=str(DEFAULT_WORKSPACE))
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args(argv)
    draft = json.loads(Path(args.draft).read_text(encoding="utf-8"))
    errors = validate(draft) if isinstance(draft, dict) else ["the draft must be a JSON object"]
    if errors:
        print("DRAFT REFUSED\n" + "\n".join(f"- {err}" for err in errors), file=sys.stderr)
        return 1
    workspace = Path(args.workspace).expanduser()
    name = f"draft-{draft['start_date']}-{safe_name(str(draft['destination']))}"
    page, copy = workspace / "html" / f"{name}.html", workspace / "plans" / f"{name}.json"
    if page.exists() and not args.overwrite:
        print(f"ERROR: {page} exists; pass --overwrite to replace it", file=sys.stderr)
        return 1
    page.parent.mkdir(parents=True, exist_ok=True)
    copy.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(render(draft), encoding="utf-8")
    copy.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    parts = cost_range(draft)
    print(f"ALL IN: {_money(draft['currency'], *parts['total'])} per person "
          f"(getting there {_money(draft['currency'], *parts['getting_there'])}, stay "
          f"{_money(draft['currency'], *parts['stay'])}, daily {_money(draft['currency'], *parts['daily'])})")
    for question in draft["decisions"]:
        print(f"ASK: {question}")
    print(f"Draft JSON: {copy}\nDraft HTML: {page}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
