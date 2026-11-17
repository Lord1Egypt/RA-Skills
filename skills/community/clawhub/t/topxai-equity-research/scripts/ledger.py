#!/usr/bin/env python3
"""Call ledger: register every research call, settle it when it comes due, keep one lesson per settlement.

    python3 scripts/ledger.py add --report ID --series TICKER --claim '...' --falsifier '...' \
        --horizon 12 --benchmark 'S&P 500 total return' --issued 2026-10-06 [--tier annual|quarterly|monthly]
    python3 scripts/ledger.py settle CALL_ID hit|miss|too_early --evidence '...' --lesson '...' [--by REPORT_ID]
    python3 scripts/ledger.py void CALL_ID --reason '...'
    python3 scripts/ledger.py list [--series TICKER] [--due DAYS]
    python3 scripts/ledger.py stats

Files (override with --ledger or env RESEARCH_LEDGER):
    research/ledger.json   the calls
    research/lessons.md    one line per settlement, newest first

Rules the tool enforces, and why:
- Append-only. There is no edit or delete command: a call that can be rewritten after the fact cannot be trusted.
  A registration typo is fixed by `void` plus a new call; the voided row stays visible with its reason.
- Every settlement needs evidence and a lesson. The lesson is what the next report reads at kickoff.
- `too_early` is allowed only before the call is due (issued + horizon). After that, settle hit or miss.
- Register every core call, the annual rating and the monthly and quarterly outlooks. A public track record that
  shows only some calls is selective performance advertising; show all of them, the method, and
  "past performance does not indicate future results".
Use single quotes around text that contains `$`; double quotes let the shell eat `$12` silently.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

TIERS = ("annual", "quarterly", "monthly")
OUTCOMES = ("hit", "miss", "too_early")


def ledger_path(a) -> Path:
    return Path(a.ledger or os.environ.get("RESEARCH_LEDGER", "research/ledger.json"))


def load(p: Path) -> dict:
    if not p.exists():
        return {"version": 1, "calls": []}
    return json.loads(p.read_text(encoding="utf-8"))


def save(p: Path, d: dict) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    tmp.replace(p)


def add_months(d: dt.date, n: int) -> dt.date:
    y, m = divmod(d.month - 1 + n, 12)
    for day in (d.day, 30, 29, 28):
        try:
            return dt.date(d.year + y, m + 1, day)
        except ValueError:
            continue
    raise ValueError(d)


def due_date(c: dict) -> dt.date:
    return add_months(dt.date.fromisoformat(c["issued_at"]), int(c["horizon_months"]))


def find(d: dict, cid: int) -> dict:
    for c in d["calls"]:
        if c["id"] == cid:
            return c
    raise SystemExit(f"call #{cid} not found")


def cmd_add(a, d) -> str:
    if a.tier and a.tier not in TIERS:
        raise SystemExit(f"--tier must be one of {TIERS}")
    dt.date.fromisoformat(a.issued)
    for c in d["calls"]:
        if c["report"] == a.report and c["claim"] == a.claim:
            return f"already registered as #{c['id']} (same report, identical claim)"
    cid = max((c["id"] for c in d["calls"]), default=0) + 1
    d["calls"].append({"id": cid, "report": a.report, "series": a.series.upper(), "tier": a.tier,
                       "claim": a.claim, "falsifier": a.falsifier, "horizon_months": a.horizon,
                       "benchmark": a.benchmark, "issued_at": a.issued, "outcome": "pending",
                       "settled_at": None, "evidence": None, "settled_by": None, "note": None,
                       "registered_at": dt.date.today().isoformat()})
    return f"registered #{cid} ({a.tier or 'core'}) due {due_date(d['calls'][-1])}"


def add_lesson(path: Path, line: str) -> None:
    head = ("# Settlement lessons\n\nOne line per settled call, newest first. Read the latest 30 before starting a report.\n\n")
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else head.rstrip("\n").splitlines()
    at = next((i for i, l in enumerate(lines) if l.startswith("- ")), len(lines))
    lines.insert(at, line)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def cmd_settle(a, d, p: Path) -> str:
    c = find(d, a.call_id)
    if c["outcome"] in ("hit", "miss", "void"):
        raise SystemExit(f"#{c['id']} is already {c['outcome']}")
    today = dt.date.today()
    if a.outcome == "too_early" and today >= due_date(c):
        raise SystemExit(f"#{c['id']} came due on {due_date(c)}; settle it hit or miss")
    c.update({"outcome": a.outcome, "evidence": a.evidence, "settled_by": a.by,
              "settled_at": today.isoformat() if a.outcome != "too_early" else None})
    add_lesson(p.with_name("lessons.md"), f"- {today} · #{c['id']} {c['series']} {a.outcome} · {a.lesson}")
    return f"#{c['id']} → {a.outcome}; lesson added to {p.with_name('lessons.md')}"


def cmd_void(a, d) -> str:
    c = find(d, a.call_id)
    if c["outcome"] == "void":
        raise SystemExit(f"#{c['id']} is already void")
    c.update({"outcome": "void", "note": a.reason, "settled_at": dt.date.today().isoformat()})
    return f"#{c['id']} voided (kept in the ledger with its reason)"


def cmd_list(a, d) -> None:
    today = dt.date.today()
    rows = [c for c in d["calls"] if not a.series or c["series"] == a.series.upper()]
    if a.due is not None:
        rows = [c for c in rows if c["outcome"] in ("pending", "too_early") and due_date(c) <= today + dt.timedelta(days=a.due)]
    for c in sorted(rows, key=lambda c: (c["issued_at"], c["id"])):
        flag = {"hit": "✓", "miss": "✗", "void": "∅"}.get(c["outcome"], "·")
        overdue = " OVERDUE" if c["outcome"] in ("pending", "too_early") and due_date(c) <= today else ""
        print(f"{flag} #{c['id']:<4} {c['series']:<6} {(c['tier'] or 'core'):<9} due {due_date(c)}{overdue}  {c['claim'][:80]}")
    print(f"{len(rows)} calls")


def cmd_stats(d) -> None:
    def line(label, cs):
        hit = sum(c["outcome"] == "hit" for c in cs); miss = sum(c["outcome"] == "miss" for c in cs)
        rate = f"{hit / (hit + miss):.0%}" if hit + miss else "—"
        print(f"{label:<14} total {len(cs):<4} settled {hit + miss:<4} hit {hit:<4} miss {miss:<4} hit rate {rate}")
    line("all", d["calls"])
    for t in TIERS + (None,):
        cs = [c for c in d["calls"] if c["tier"] == t]
        if cs:
            line(t or "core", cs)
    for s in sorted({c["series"] for c in d["calls"]}):
        line(s, [c for c in d["calls"] if c["series"] == s])
    print("Hit rate = hits / (hits + misses); open and void calls are excluded from the denominator. "
          "Past performance does not indicate future results.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ledger")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("add")
    for f in ("--report", "--series", "--claim", "--falsifier", "--benchmark", "--issued"):
        s.add_argument(f, required=True)
    s.add_argument("--horizon", type=int, required=True); s.add_argument("--tier")
    s = sub.add_parser("settle"); s.add_argument("call_id", type=int); s.add_argument("outcome", choices=OUTCOMES)
    s.add_argument("--evidence", required=True); s.add_argument("--lesson", required=True); s.add_argument("--by")
    s = sub.add_parser("void"); s.add_argument("call_id", type=int); s.add_argument("--reason", required=True)
    s = sub.add_parser("list"); s.add_argument("--series"); s.add_argument("--due", type=int)
    sub.add_parser("stats")
    a = ap.parse_args()
    p = ledger_path(a)
    d = load(p)
    if a.cmd == "list":
        cmd_list(a, d); return 0
    if a.cmd == "stats":
        cmd_stats(d); return 0
    msg = {"add": lambda: cmd_add(a, d), "settle": lambda: cmd_settle(a, d, p), "void": lambda: cmd_void(a, d)}[a.cmd]()
    save(p, d)
    print(msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
