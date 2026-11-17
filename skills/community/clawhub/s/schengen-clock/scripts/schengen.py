#!/usr/bin/env python3
"""Schengen Clock — rolling 90/180-day presence tracker and trip planner.

Computes exact presence under the Schengen short-stay rule: at most 90 days of
presence in any 180-day window. Entry and exit days both count as presence days.
100% offline; registry stays in schengen.json (or --db).

INFORMATIONAL TOOL. Border authorities apply the rule to your specific passport,
visa, and history. When in doubt, ask the consulate — do not risk an overstay.
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

DB = Path("schengen.json")
WINDOW = 180          # days in rolling window
CAP = 90              # max presence days per window

NON_SCHENGEN_EU = {
    "IE": "Ireland", "GB": "United Kingdom", "CY": "Cyprus",
}


def d(s):
    return dt.date.fromisoformat(s) if s else None


def today():
    return dt.date.today()


def load(db=None):
    p = Path(db) if db else DB
    if p.exists():
        try:
            data = json.loads(p.read_text())
            data.setdefault("stays", [])
            return data
        except Exception:
            return {"stays": []}
    return {"stays": []}


def save(data, db=None):
    p = Path(db) if db else DB
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    return p


def overlap_days(entry, exit_, on_date):
    """Presence days within [entry, exit_] inclusive, counted on a given date.

    A stay's presence on `on_date`: full stay if entirely in the past/today,
    elapsed part if ongoing, zero if in the future.
    """
    entry, exit_ = d(entry), d(exit_)
    effective_exit = min(exit_, on_date)
    if effective_exit < entry:
        return 0
    return (effective_exit - entry).days + 1


def presence_in_window(stays, window_end):
    """Presence days inside the 180-day window ENDING on window_end (inclusive).

    Days of the stay that fall before window_start don't count; days inside do.
    """
    wstart = window_end - dt.timedelta(days=WINDOW - 1)
    total = 0
    detail = []
    for s in stays:
        e, x = d(s["entry"]), d(s["exit"])
        lo = max(e, wstart)
        hi = min(x, window_end)
        n = (hi - lo).days + 1 if hi >= lo else 0
        if n > 0:
            total += n
            detail.append((s, n))
    return total, wstart, detail


def audit(stays, on_date, extra_stay=None):
    """Return (used, remaining, violating) for the window ending on_date."""
    sts = list(stays) + ([extra_stay] if extra_stay else [])
    used, wstart, detail = presence_in_window(sts, on_date)
    remaining = CAP - used
    return used, remaining, wstart, detail


# ---------------------------------------------------------------- stay CRUD
def cmd_stay(a):
    data = load(a.db)
    if a.action == "add":
        if not a.country or len(a.country) != 2 or not a.country.isalpha():
            print("[!] --country must be a 2-letter code, e.g. IT, FR, ES")
            return 1
        c = a.country.upper()
        if c in NON_SCHENGEN_EU:
            print(f"[!] {c} ({NON_SCHENGEN_EU[c]}) is NOT in Schengen — presence there does not count.")
        e, x = d(a.entry), d(a.exit_)
        if not e or not x or x < e:
            print("[!] Need --entry and --exit (ISO dates), exit >= entry")
            return 1
        if (x - e).days + 1 > 366:
            print("[!] Stays over a year suggest a residence-permit situation — this tool is for short stays.")
            return 1
        data["stays"].append({"entry": a.entry, "exit": a.exit_, "country": c})
        data["stays"].sort(key=lambda s: s["entry"])
        save(data, a.db)
        n = (x - e).days + 1
        print(f"added {a.entry} → {a.exit_} ({c}): {n} presence days")
        return 0
    # list
    data = load(a.db)
    if not data["stays"]:
        print("No stays recorded. Add one: schengen.py stay add --entry 2026-05-10 --exit 2026-06-02 --country IT")
        return 0
    print(f"{'entry':12}{'exit':12}{'days':>5}  country")
    for s in data["stays"]:
        n = (d(s["exit"]) - d(s["entry"])).days + 1
        print(f"{s['entry']:12}{s['exit']:12}{n:>5}  {s['country']}")
    total_all = sum((d(s['exit']) - d(s['entry'])).days + 1 for s in data["stays"])
    print(f"\ntotal recorded: {len(data['stays'])} stays, {total_all} presence days (all time)")
    return 0


def cmd_rm(a):
    data = load(a.db)
    before = len(data["stays"])
    data["stays"] = [s for s in data["stays"] if not (
        s["entry"] == a.entry and (a.exit_ is None or s["exit"] == a.exit_))]
    save(data, a.db)
    print(f"removed {before - len(data['stays'])} stay(s)")
    return 0


# ---------------------------------------------------------------- status
def cmd_status(a):
    data = load(a.db)
    on = d(a.on) or today()
    used, remaining, wstart, detail = audit(data["stays"], on)
    print(f"Schengen 90/180 status as of {on}")
    print(f"window: {wstart} … {on} (180 days)\n")
    print(f"presence used : {used} days")
    print(f"remaining     : {max(0, remaining)} days")
    print()
    if detail:
        print("inside window:")
        for s, n in detail:
            print(f"  {s['entry']} → {s['exit']} ({s['country']}): {n} days")
    else:
        print("no presence inside the current window — full 90 days available")
    if remaining < 0:
        print(f"\n[!!] OVERSTAY: {used} days in a 180-day window exceeds the {CAP}-day cap by {-remaining}.")
        print("     Stop accumulating presence; consult the consulate before future travel.")
    elif remaining == 0:
        print("\n[!] Allowance exhausted: you must be outside Schengen tomorrow to stay legal,")
        print("    and old days only free up as the window slides. Check 'maxstay' before re-entering.")
    else:
        # when does the next day free up?
        nxt = on
        for _ in range(400):
            nxt += dt.timedelta(days=1)
            u, r, _, _ = audit(data["stays"], nxt)
            if r > remaining:
                print(f"\nnext allowance increase: {nxt} (+{r - remaining} days as old days slide out)")
                break
    return 0 if remaining >= 0 else 2


# ---------------------------------------------------------------- maxstay
def cmd_maxstay(a):
    data = load(a.db)
    entry = d(a.entry)
    if not entry:
        print("[!] --entry YYYY-MM-DD required")
        return 1
    # longest stay: day-by-day, find last day where every window containing
    # the stay keeps presence <= CAP
    best_exit, cur = None, entry
    for _ in range(400):
        trial = cur + dt.timedelta(days=1)
        # simulate stay entry..trial; check every window end from entry to trial
        ok = True
        we = entry
        while we <= trial:
            used, _, _, _ = audit(data["stays"], we, extra_stay={"entry": iso(entry), "exit": iso(trial)})
            if used > CAP:
                ok = False
                break
            we += dt.timedelta(days=1)
        if not ok:
            break
        best_exit = trial
        cur = trial
    if best_exit is None:
        used, remaining, wstart, _ = audit(data["stays"], entry)
        print(f"Entering {entry}: presence already at/over cap in window ending {entry}.")
        print(f"used {used} / {CAP}. Entry likely refused — wait until allowance frees up.")
        return 2
    days = (best_exit - entry).days + 1
    print(f"Entering {entry}: longest legal stay = {days} days")
    print(f"latest exit date: {best_exit} (exit-day presence counts; leaving later = overstay)")
    # allowance snapshot on entry date
    used, remaining, _, _ = audit(data["stays"], entry)
    print(f"on entry date, window ending {entry}: {used} used / {CAP} cap")
    if days == 90:
        print("(90-day max: no prior presence constrains this stay)")
    return 0


def iso(date):
    return date.isoformat()


# ---------------------------------------------------------------- plan
def cmd_plan(a):
    data = load(a.db)
    e, x = d(a.entry), d(a.exit_)
    if not e or not x or x < e:
        print("[!] need --entry and --exit (ISO), exit >= entry")
        return 1
    trip_days = (x - e).days + 1
    trip = {"entry": iso(e), "exit": iso(x), "country": (a.country or "??").upper()}
    # check every window end from e to x
    worst_used, worst_end = -1, None
    we = e
    while we <= x:
        used, remaining, wstart, _ = audit(data["stays"], we, extra_stay=trip)
        if used > worst_used:
            worst_used, worst_end = used, we
        we += dt.timedelta(days=1)
    verdict = "ALLOWED" if worst_used <= CAP else "TOO-LONG"
    margin = CAP - worst_used
    print(f"Trip {a.entry} → {a.exit_} ({trip_days} days, {trip['country']})")
    print(f"tightest window ends {worst_end}: {worst_used}/90 used" + (f" (over by {-margin})" if margin < 0 else f", margin {margin} days"))
    if verdict == "ALLOWED":
        # future allowance after this trip, 30 days after exit
        fut = x + dt.timedelta(days=30)
        u, r, _, _ = audit(data["stays"], fut, extra_stay=trip)
        print(f"\nVERDICT: ALLOWED")
        print(f"30 days after exit ({fut}): {max(0, r)} days will be free in that window")
        if margin <= 5:
            print("[!] thin margin — any date error or delayed flight risks an overstay. Build buffer.")
        return 0
    # too long: find max feasible exit
    print(f"\nVERDICT: TOO-LONG by {-margin} days")
    print("Options:")
    print(f"  a) shorten the trip (see: schengen.py maxstay --entry {a.entry})")
    print(f"  b) push entry earlier is useless; push exit later only after old days slide out")
    # find first exit date that works
    xx = e
    while xx <= x + dt.timedelta(days=200):
        t2 = {"entry": iso(e), "exit": iso(xx), "country": trip["country"]}
        ok = True
        we = e
        while we <= xx:
            used, _, _, _ = audit(data["stays"], we, extra_stay=t2)
            if used > CAP:
                ok = False
                break
            we += dt.timedelta(days=1)
        if ok:
            print(f"  c) latest feasible exit with this entry: {xx} ({(xx - e).days + 1} days)")
            break
        xx += dt.timedelta(days=1)
    return 2


# ---------------------------------------------------------------- traps
def cmd_traps(a):
    data = load(a.db)
    stays = sorted(data["stays"], key=lambda s: s["entry"])
    found = 0
    print("Classic-trap scan\n" + "-" * 40)
    # 1. cumulative rolling presence right after each exit (heavy usage)
    for i, s in enumerate(stays):
        end = d(s["exit"])
        used, remaining, _, _ = audit(stays, end)
        if used > CAP:
            found += 1
            print(f"[OVERSTAY] at exit {s['exit']}: {used}/90 in the window ending that day —")
            print(f"           history exceeds the cap by {used - CAP}; expect scrutiny at next entry")
        elif used >= 85:
            found += 1
            print(f"[HIGH USAGE] at exit {s['exit']}: {used}/90 used in window —")
            print(f"             re-entry before old days expire will be constrained")
    # 2. back-to-back long stays
    for i in range(len(stays) - 1):
        gap = (d(stays[i + 1]["entry"]) - d(stays[i]["exit"])).days
        len1 = (d(stays[i]["exit"]) - d(stays[i]["entry"])).days + 1
        len2 = (d(stays[i + 1]["exit"]) - d(stays[i + 1]["entry"])).days + 1
        if gap <= 10 and len1 >= 60 and len2 >= 40:
            found += 1
            print(f"[BACK-TO-BACK] {stays[i]['entry']}→{stays[i]['exit']} ({len1}d) then")
            print(f"              {stays[i+1]['entry']}→{stays[i+1]['exit']} ({len2}d) after only {gap}d gap")
            print(f"              second stay is capped by the rolling window — verify with 'plan'")
    # 3. margin on planned future stays
    for s in stays:
        if d(s["exit"]) >= today():
            e, x = d(s["entry"]), d(s["exit"])
            we, worst = e, -1
            while we <= x:
                used, _, _, _ = audit(stays, we, extra_stay=s)
                worst = max(worst, used)
                we += dt.timedelta(days=1)
            if 85 <= worst <= 90:
                found += 1
                print(f"[THIN MARGIN] planned stay {s['entry']}→{s['exit']} peaks at {worst}/90")
                print(f"              <5 days of slack; any extension = overstay risk")
            elif worst > 90:
                found += 1
                print(f"[OVER CAP] planned stay {s['entry']}→{s['exit']} reaches {worst}/90 — ILLEGAL as planned")
    # 4. presence total in last 365 days
    used, _, _, _ = audit(stays, today())
    if used > 150:
        found += 1
        print(f"[YEAR HEAVY] {used} presence days in current window — pattern looks like de-facto residence;")
    if found == 0:
        print("no classic traps detected in the current registry")
    else:
        print(f"\n{found} flag(s). Overstay penalties: fines, removal, entry bans of 1+ year.")
    return 0


# ---------------------------------------------------------------- letter
def cmd_letter(a):
    data = load(a.db)
    e, x = d(a.entry), d(a.exit_)
    if not e or not x:
        print("[!] --entry and --exit required (planned trip)")
        return 1
    trip = {"entry": iso(e), "exit": iso(x), "country": "XX"}
    used, remaining, wstart, _ = audit(data["stays"], e, extra_stay=trip)
    days = (x - e).days + 1
    print("=" * 62)
    print("SCHENGEN SHORT-STAY ALLOWANCE STATEMENT")
    print(f"(generated {today()} — informational, for border interview support)")
    print("=" * 62)
    print(f"Planned presence: {e} → {x} ({days} days)")
    print(f"Allowance check on entry-date window ({wstart} … {e}):")
    print(f"  days used including this trip: {used} / 90")
    print(f"  {'WITHIN the 90/180 rule' if used <= CAP else 'EXCEEDS the rule — DO NOT travel as planned'}")
    print("\nPresence history (last 180 days from entry):")
    wstart_full = e - dt.timedelta(days=WINDOW - 1)
    shown = 0
    for s in sorted(data["stays"], key=lambda s: s["entry"]):
        lo = max(d(s["entry"]), wstart_full)
        hi = min(d(s["exit"]), e)
        if hi >= lo:
            n = (hi - lo).days + 1
            print(f"  {s['entry']} → {s['exit']} ({s['country']}): {n} days in window")
            shown += 1
    if not shown:
        print("  (none)")
    print("\nNote to the officer: rolling-window math above follows the EU")
    print("short-stay counting rules (entry and exit days both count).")
    print("=" * 62)
    return 0 if used <= CAP else 2


# ----------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", default=None)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("stay", help="add/list stays")
    p.add_argument("action", nargs="?", default="list", choices=["add", "list"])
    p.add_argument("--entry", default=None)
    p.add_argument("--exit", dest="exit_", default=None)
    p.add_argument("--country", default=None)
    p.set_defaults(fn=cmd_stay)

    p = sub.add_parser("rm", help="remove a stay by entry date")
    p.add_argument("--entry", required=True)
    p.add_argument("--exit", dest="exit_", default=None)
    p.set_defaults(fn=cmd_rm)

    p = sub.add_parser("status", help="presence + allowance in the current window")
    p.add_argument("--on", default=None, help="date (default today)")
    p.set_defaults(fn=cmd_status)

    p = sub.add_parser("maxstay", help="longest legal stay for a given entry date")
    p.add_argument("--entry", required=True)
    p.set_defaults(fn=cmd_maxstay)

    p = sub.add_parser("plan", help="check a proposed trip against every window")
    p.add_argument("--entry", required=True)
    p.add_argument("--exit", dest="exit_", required=True)
    p.add_argument("--country", default=None)
    p.set_defaults(fn=cmd_plan)

    p = sub.add_parser("traps", help="scan registry for classic overstay traps")
    p.set_defaults(fn=cmd_traps)

    p = sub.add_parser("letter", help="border-interview allowance statement")
    p.add_argument("--entry", required=True)
    p.add_argument("--exit", dest="exit_", required=True)
    p.set_defaults(fn=cmd_letter)

    a = ap.parse_args()
    sys.exit(a.fn(a) or 0)


if __name__ == "__main__":
    main()
