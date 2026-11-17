#!/usr/bin/env python3
"""Coverage watch: new SEC filings matched to open falsifiers, price triggers, mark-to-market, calls coming due.
No model calls; it only fetches and compares. Run it by hand (or on your own scheduler).

    python3 scripts/desk.py run [--days 3] [--prices prices.csv]   # writes research/desk/<date>.md and prints it
    python3 scripts/desk.py check                                  # every series in the ledger has a watch entry

Inputs
    research/watch.json    coverage list: per series a rating (ledger call id, start date and price, benchmark),
                           price triggers written in the report, and outlook events with due dates
                           (format: assets/templates/watch-entry.json)
    research/ledger.json   calls (scripts/ledger.py)
    --prices CSV           optional daily closes you supply: columns date,ticker,close (ISO dates). Include the
                           benchmark tickers named in watch.json. Without it, price sections are skipped.
Environment: SEC_USER_AGENT (see scripts/sec.py). Network: sec.gov / data.sec.gov only.

Sections of the run file
    1. New filings      per covered company; lists open ledger calls whose falsifier names that filing type.
                        Routine 8-Ks (items 5.05, 5.07, exhibits only) are not matched. When a falsifier names an
                        item ("8-K Item 1.01"), the filing's items must match.
    2. Price triggers   below a level / N consecutive closes above a level / a (beta-adjusted) ratio vs benchmark.
    3. Mark-to-market   absolute, benchmark and relative return since the start date, and which rating band today's
                        price falls in. This is tracking, not settlement: settle on the report's own terms.
    4. Due              outlook events past due or due within 14 days; core/annual calls due within 30 days.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("sec", HERE / "sec.py")
sec = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sec)

BANDS = [("buy", 15, None), ("overweight", 5, 15), ("neutral", -10, 5), ("underweight", None, -10)]
FORM_KEYS = {"8-K": ["8-K"], "10-Q": ["10-Q"], "10-K": ["10-K"], "DEF 14A": ["DEF 14A", "proxy"],
             "4": ["Form 4", "open-market purchase", "open-market buy"], "424B5": ["424B5", "ATM"],
             "S-3": ["S-3", "ATM"], "S-3ASR": ["S-3", "ATM"]}
ROUTINE_8K = {"5.05", "5.07", "9.01"}


def mentions(text: str, form: str, items: str = "") -> bool:
    text = text or ""
    if not any(k.lower() in text.lower() for k in FORM_KEYS.get(form, [form])):
        return False
    if form != "8-K":
        return True
    got = {i.strip() for i in (items or "").split(",") if i.strip()}
    if got and got <= ROUTINE_8K:
        return False
    named = set(re.findall(r"Item\s*(\d\.\d\d)", text)) | set(re.findall(r"/\s*(\d\.\d\d)", text))
    return not named or not got or bool(named & got)


def band_of(rel_pct: float) -> str:
    for name, lo, hi in BANDS:
        if (lo is None or rel_pct > lo) and (hi is None or rel_pct <= hi):
            return name
    return "?"


def run_length(flags: list) -> tuple:
    tail = best = cur = 0
    for f in flags:
        cur = cur + 1 if f else 0
        best = max(best, cur)
    for f in reversed(flags):
        if not f:
            break
        tail += 1
    return tail, best


def load_prices(path: str | None) -> dict:
    if not path:
        return {}
    px: dict = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            px.setdefault(row["ticker"].upper(), {})[row["date"]] = float(row["close"])
    return {t: dict(sorted(v.items())) for t, v in px.items()}


def add_months(d: dt.date, n: int) -> dt.date:
    y, m = divmod(d.month - 1 + n, 12)
    for day in (d.day, 30, 29, 28):
        try:
            return dt.date(d.year + y, m + 1, day)
        except ValueError:
            continue
    raise ValueError(d)


def prices_section(key, s, px, out, alerts, errors):
    r = s.get("rating")
    if not r:
        return
    tk, start = s["ticker"].upper(), r["start"]
    syms = [tk, *[b.upper() for b in r["benchmark"]]]
    if any(x not in px for x in syms):
        errors.append(f"{key}: price CSV lacks {[x for x in syms if x not in px]}")
        return
    base = {tk: r.get("start_price") or px[tk].get(start)}
    base.update({b.upper(): (v or px[b.upper()].get(start)) for b, v in r["benchmark"].items()})
    if any(v is None for v in base.values()):
        errors.append(f"{key}: no close on start date {start}")
        return
    bench_days = set.intersection(*(set(px[b.upper()]) for b in r["benchmark"]))
    bench = {d: sum(px[b.upper()][d] / base[b.upper()] for b in r["benchmark"]) / len(r["benchmark"]) for d in bench_days}
    days = sorted(d for d in px[tk] if d in bench and d >= start)
    if not days:
        errors.append(f"{key}: no common closes after {start}")
        return
    last, stock = days[-1], px[tk]
    rs, rb = stock[last] / base[tk] - 1, bench[last] - 1
    rel = (1 + rs) / (1 + rb) - 1 if r.get("method") == "ratio" else rs - rb
    b = band_of(rel * 100)
    out["marks"].append(f"| {key} | #{r['call']} | {r['label']} | {start} {base[tk]:.2f} | {last} {stock[last]:.2f} | "
                        f"{rs:+.1%} | {rb:+.1%} | {rel:+.1%} | {b}{'' if b == r['label'] else ' (differs)'} |")
    for t in s.get("triggers", []):
        k = t["kind"]
        if k == "below":
            hits = [d for d in days if stock[d] < t["level"]]
            crossed, dist = bool(hits), stock[last] / t["level"] - 1
            txt = f"below {t['level']}: last {stock[last]:.2f} ({dist:+.1%})" + (f", **crossed** first on {hits[0]}" if hits else "")
        elif k == "consec_above":
            tail, best = run_length([stock[d] > t["level"] for d in days])
            crossed, dist = best >= t["days"], stock[last] / t["level"] - 1
            txt = f"{t['days']} closes above {t['level']}: last {stock[last]:.2f} ({dist:+.1%}), run {tail}, longest {best}" + (" **crossed**" if crossed else "")
        elif k == "ratio_consec":
            ratio = {d: (stock[d] / base[tk]) / (bench[d] ** t.get("beta", 1)) for d in days}
            hi, lo = t.get("hi"), t.get("lo")
            tail, best = run_length([(hi is not None and ratio[d] >= hi) or (lo is not None and ratio[d] <= lo) for d in days])
            crossed, dist = best >= t["days"], None
            txt = f"ratio {t['days']} days outside {lo}–{hi}: now {ratio[last]:.3f}, run {tail}, longest {best}" + (" **crossed**" if crossed else "")
        else:
            errors.append(f"{key}: unknown trigger kind {k}")
            continue
        out["triggers"].append(f"- {key} #{t['call']} {txt}. {t.get('note', '')}")
        if crossed:
            alerts.append(f"{key} #{t['call']} price condition crossed: settle per the report's terms")
        elif dist is not None and abs(dist) <= 0.05:
            alerts.append(f"{key} #{t['call']} within {dist:+.1%} of its price condition")


def cmd_run(a) -> int:
    watch = json.loads(Path(a.watch).read_text(encoding="utf-8"))
    ledger = json.loads(Path(a.ledger).read_text(encoding="utf-8")) if Path(a.ledger).exists() else {"calls": []}
    calls = ledger["calls"]
    pending = [c for c in calls if c["outcome"] == "pending"]
    outcome = {c["id"]: c["outcome"] for c in calls}
    today = dt.date.today()
    since = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=a.days)
    px = load_prices(a.prices)
    out = {"filings": [], "triggers": [], "marks": [], "due": []}
    alerts, errors = [], []

    for key, s in watch["series"].items():
        try:
            rows = sec.recent(sec.cik_of(s["ticker"]), since, None)
        except SystemExit as e:
            errors.append(f"{key}: {e}")
            continue
        for f in rows:
            items = f" Item {f['items']}" if f["items"] else ""
            out["filings"].append(f"- {key} {f['form']}{items} ({f['filed']}) <{f['url']}>")
            hits = [c for c in pending if c["series"] == s["ticker"].upper() and mentions(c["falsifier"], f["form"], f["items"])]
            evs = [e for e in s.get("events", []) if outcome.get(e.get("call")) not in ("hit", "miss")
                   and mentions(e["what"], f["form"], f["items"])]
            if hits:
                out["filings"].append("  - check ledger: " + ", ".join(f"#{c['id']}" for c in hits)
                                      + " (falsifier names this filing type; read it and settle early if triggered)")
                alerts.append(f"{key} {f['form']}{items} {f['filed']} touches " + ", ".join(f"#{c['id']}" for c in hits))
            if evs:
                out["filings"].append("  - check outlook: " + ", ".join(f"{e['tier']} (due {e['due']})" for e in evs))
        if px:
            prices_section(key, s, px, out, alerts, errors)
        for e in s.get("events", []):
            if outcome.get(e.get("call")) in ("hit", "miss"):
                continue
            dd = dt.date.fromisoformat(e["due"])
            if dd <= today:
                out["due"].append(f"- **overdue** {key} {e['tier']} outlook (#{e.get('call', '?')}) due {e['due']}: {e['what']} ({e['source']})")
                alerts.append(f"{key} {e['tier']} outlook due {e['due']} is unsettled")
            elif dd <= today + dt.timedelta(days=14):
                out["due"].append(f"- {key} {e['tier']} outlook due {e['due']}: {e['what']}")
    for c in pending:
        if c.get("tier") in ("monthly", "quarterly"):
            continue
        dd = add_months(dt.date.fromisoformat(c["issued_at"]), int(c["horizon_months"]))
        if dd <= today + dt.timedelta(days=30):
            out["due"].append(f"- {'**overdue**' if dd <= today else 'due soon'} #{c['id']} {c['series']} {dd}: {c['claim'][:70]}")

    md = [f"# Coverage watch {today}", "", f"Filings since {since:%Y-%m-%d %H:%M} UTC. Prices: {a.prices or 'not supplied'}.", ""]
    md += ["## Alerts", ""] + ([f"- {x}" for x in alerts] or ["- none"]) + [""]
    md += ["## 1. New filings", ""] + (out["filings"] or ["- none"]) + [""]
    if px:
        md += ["## 2. Price triggers", ""] + (out["triggers"] or ["- none"]) + [""]
        md += ["## 3. Mark-to-market (tracking, not settlement)", "",
               "| Series | Call | Rating | Start | Last | Abs | Bench | Rel | Band today |", "|---|---|---|---|---|---|---|---|---|",
               *out["marks"], ""]
    md += ["## 4. Due", ""] + (out["due"] or ["- none"]) + [""]
    if errors:
        md += ["## Data errors", ""] + [f"- {e}" for e in errors] + [""]
    text = "\n".join(md)
    run_dir = Path(a.out)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / f"{today}.md").write_text(text, encoding="utf-8")
    print(text)
    print(f"written: {run_dir / f'{today}.md'}")
    return 0


def cmd_check(a) -> int:
    watch = json.loads(Path(a.watch).read_text(encoding="utf-8"))
    ledger = json.loads(Path(a.ledger).read_text(encoding="utf-8")) if Path(a.ledger).exists() else {"calls": []}
    covered = {s["ticker"].upper() for s in watch["series"].values()}
    missing = sorted({c["series"] for c in ledger["calls"] if c["outcome"] == "pending"} - covered)
    for m in missing:
        print(f"  missing watch entry for {m}")
    print(f"{len(covered)} series watched; {len(missing)} ledger series not covered")
    return 1 if missing else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["run", "check"])
    ap.add_argument("--days", type=int, default=3)
    ap.add_argument("--prices")
    ap.add_argument("--watch", default=os.environ.get("RESEARCH_WATCH", "research/watch.json"))
    ap.add_argument("--ledger", default=os.environ.get("RESEARCH_LEDGER", "research/ledger.json"))
    ap.add_argument("--out", default="research/desk")
    a = ap.parse_args()
    return cmd_run(a) if a.cmd == "run" else cmd_check(a)


if __name__ == "__main__":
    sys.exit(main())
