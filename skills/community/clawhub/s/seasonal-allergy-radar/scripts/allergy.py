#!/usr/bin/env python3
"""allergy.py — personal pollen radar: symptom log, zone calendars,
lag-correlation trigger finder, 14-day forecast, pre-medication planner.

Subcommands:
  log init/add/show  symptom log management
  calendar           month-level pollen risk for a climate zone
  correlate          match your log against the calendar (lag search)
  forecast           your personal 14-day symptom forecast
  plan               pre-medication start dates for a target season

Stdlib only. Not a medical device; see references/pollen-science.md.
"""
import argparse
import datetime as dt
import json
import math
import sys
from pathlib import Path

# ---------------------------------------------------------------- zones

# month -> (tree, grass, weed) risk 0-3
ZONES = {
    "temperate-northern": {
        1: (0, 0, 0), 2: (2, 0, 0), 3: (2, 0, 0),
        4: (3, 1, 0), 5: (3, 2, 0), 6: (1, 3, 1),
        7: (0, 2, 2), 8: (0, 1, 3), 9: (0, 0, 2), 10: (0, 0, 0),
        11: (0, 0, 0), 12: (0, 0, 0),
    },
    "mediterranean": {
        1: (2, 0, 0), 2: (3, 0, 0), 3: (2, 1, 0),
        4: (3, 2, 0), 5: (3, 3, 1), 6: (2, 2, 2),
        7: (0, 1, 2), 8: (0, 0, 2), 9: (0, 0, 2),
        10: (0, 0, 0), 11: (0, 0, 0), 12: (1, 0, 0),
    },
    "continental": {
        1: (0, 0, 0), 2: (0, 0, 0), 3: (1, 0, 0),
        4: (2, 0, 0), 5: (3, 1, 0), 6: (1, 3, 1),
        7: (0, 2, 3), 8: (0, 1, 2), 9: (0, 0, 1),
        10: (0, 0, 0), 11: (0, 0, 0), 12: (0, 0, 0),
    },
    "subtropical": {
        1: (2, 1, 0), 2: (3, 1, 0), 3: (3, 2, 0),
        4: (2, 3, 0), 5: (1, 3, 1), 6: (1, 3, 2),
        7: (0, 2, 2), 8: (0, 2, 3), 9: (0, 2, 2),
        10: (0, 1, 1), 11: (1, 0, 0), 12: (2, 0, 0),
    },
    "coastal-low": {
        1: (0, 0, 0), 2: (0, 0, 0), 3: (1, 0, 0),
        4: (1, 1, 0), 5: (1, 2, 0), 6: (0, 2, 1),
        7: (0, 2, 1), 8: (0, 1, 1), 9: (0, 0, 0),
        10: (0, 0, 0), 11: (0, 0, 0), 12: (0, 0, 0),
    },
}
CLASSES = ["tree", "grass", "weed"]

# ---------------------------------------------------------------- helpers

def parse_date(s):
    return dt.date.fromisoformat(s)


def month_curve(zone, cls):
    idx = CLASSES.index(cls)
    return {m: ZONES[zone][m][idx] for m in range(1, 13)}


def daily_risk(zone, cls, day):
    """Smooth interpolation between month midpoints -> 0..3 risk."""
    mc = month_curve(zone, cls)
    mids = [15, 45, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349]  # ~mid-month ordinals
    doy = day.timetuple().tm_yday
    # find bracketing anchors on a cyclic year (offset -365 for wrap)
    best_prev = None
    for m in range(1, 13):
        for off in (-365, 0, 365):
            a = mids[m - 1] + off
            if a <= doy and (best_prev is None or a > best_prev[0]):
                best_prev = (a, mc[m])
    if best_prev is None:  # before Jan 15: prev anchor is Dec 15 of prior year
        best_prev = (mids[11] - 365, mc[12])
    p_a, p_v = best_prev
    # next anchor: first midpoint strictly after doy
    nxt = None
    for m in range(1, 13):
        for off in (-365, 0, 365):
            a = mids[m - 1] + off
            if a > doy and (nxt is None or a < nxt[0]):
                nxt = (a, mc[m])
    n_a, n_v = nxt
    span = n_a - p_a
    if span <= 0:
        return p_v
    frac = max(0.0, min(1.0, (doy - p_a) / span))
    return p_v + (n_v - p_v) * frac


def load_log(path):
    data = json.loads(Path(path).read_text())
    return {parse_date(e["date"]): e for e in data}


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if dx == 0 or dy == 0:
        return 0.0
    return num / (dx * dy)


# ---------------------------------------------------------------- log cmds

def cmd_log_init(args):
    start = parse_date(args.from_)
    entries = []
    for i in range(args.days):
        d = start + dt.timedelta(days=i)
        entries.append({"date": d.isoformat(), "score": None,
                        "systems": [], "note": ""})
    Path(args.out).write_text(json.dumps(entries, indent=2) + "\n")
    print("Log skeleton: %d days from %s -> %s" % (args.days, start, args.out))
    print("Fill score 0-5 + systems each evening BEFORE rescue meds.")
    return 0


def cmd_log_add(args):
    p = Path(args.log)
    entries = json.loads(p.read_text())
    systems = []
    if args.eyes:
        systems.append("eyes")
    if args.nose:
        systems.append("nose")
    if args.lungs:
        systems.append("lungs")
    if args.skin:
        systems.append("skin")
    for e in entries:
        if e["date"] == args.date:
            e.update({"score": args.score, "systems": systems,
                      "note": args.note or ""})
            break
    else:
        entries.append({"date": args.date, "score": args.score,
                        "systems": systems, "note": args.note or ""})
    entries.sort(key=lambda e: e["date"])
    p.write_text(json.dumps(entries, indent=2) + "\n")
    print("Logged %s score=%d systems=%s" % (args.date, args.score,
                                             "+".join(systems) or "-"))
    return 0


def cmd_log_show(args):
    log = load_log(args.log)
    filled = sorted((d, e) for d, e in log.items() if e.get("score") is not None)
    for d, e in filled:
        print("%s  %d  %-16s %s" % (d, e["score"],
              "+".join(e.get("systems", [])) or "-", e.get("note", "")))
    print("(%d/%d days filled)" % (len(filled), len(log)))
    return 0


# ---------------------------------------------------------------- calendar

def cmd_calendar(args):
    print("Zone: %s\n" % args.zone)
    print("%-6s %-6s %-6s %-6s" % ("MONTH", "TREE", "GRASS", "WEED"))
    for m in range(1, 13):
        t, g, w = ZONES[args.zone][m]
        bar = lambda v: ("*" * v) or "-"
        print("%-6d %-6s %-6s %-6s" % (m, bar(t), bar(g), bar(w)))
    print("\n0 none, 1 low, 2 moderate, 3 high; ramps between months.")
    return 0


# ---------------------------------------------------------------- correlate

def cmd_correlate(args):
    log = load_log(args.log)
    days = sorted(d for d, e in log.items() if e.get("score") is not None)
    if len(days) < 14:
        print("Need >=14 logged days (have %d). Log the zeros too." % len(days))
        return 1
    scores = [log[d]["score"] for d in days]

    print("Log: %d days, %s -> %s\n" % (len(days), days[0], days[-1]))
    results = []
    for cls in CLASSES:
        best = (None, -2)
        for lag in range(0, 8):
            pairs = [(log[d]["score"], daily_risk(args.zone, cls, d - dt.timedelta(days=lag)))
                     for d in days]
            r = pearson([p[0] for p in pairs], [p[1] for p in pairs])
            if r is not None and r > best[1]:
                best = (lag, r)
        results.append((cls, best[0], best[1]))
        print("%-6s best lag %s d, r = %+.2f" %
              (cls, best[0] if best[0] is not None else "?", best[1]))

    hit = [(c, l, r) for c, l, r in results if r is not None and r >= 0.35]
    if not hit:
        print("\nNo class clears r>=0.35 — no clear pollen driver.")
        print("Consider mold/humidity, dust-mite, pollution, or an allergist.")
        return 0
    hit.sort(key=lambda t: -t[2])
    c, l, r = hit[0]
    print("\nPrimary trigger: %s (r=%+.2f, lag %s d)" % (c.upper(), r, l))
    for c2, l2, r2 in hit[1:]:
        print("Contributor : %s (r=%+.2f, lag %s d)" % (c2, r2, l2))
    bad = [d for d in days if log[d]["score"] >= 3]
    if bad:
        print("Your worst days: %s ... (%d days >=3/5)" %
              (", ".join(str(x) for x in bad[:5]), len(bad)))
    return 0


# ---------------------------------------------------------------- forecast

def cmd_forecast(args):
    log = load_log(args.log)
    days = sorted(d for d, e in log.items() if e.get("score") is not None)
    if len(days) < 7:
        print("Need >=7 logged days to fit your severity curve (have %d)." % len(days))
        return 1
    start = parse_date(args.from_)

    # calibrate: mean score per calendar-risk level you experienced
    cal = {}
    for d in days:
        risk = (daily_risk(args.zone, "tree", d) + daily_risk(args.zone, "grass", d)
                + daily_risk(args.zone, "weed", d))
        cal.setdefault(round(risk), []).append(log[d]["score"])
    curve = {k: sum(v) / len(v) for k, v in cal.items()}
    kmin, kmax = min(curve), max(curve)

    print("Forecast from %s (zone %s), 14 days:\n" % (start, args.zone))
    flags = []
    for i in range(14):
        d = start + dt.timedelta(days=i)
        risk = (daily_risk(args.zone, "tree", d) + daily_risk(args.zone, "grass", d)
                + daily_risk(args.zone, "weed", d))
        key = min(max(round(risk), kmin), kmax)
        pred = curve.get(key)
        pred_s = "n/a" if pred is None else "%.1f" % pred
        trend = ""
        if pred is not None:
            if pred >= 3 and (i == 0 or True):
                trend = "  <- HIGH risk day, plan meds/indoors"
            elif pred >= 2:
                trend = "  <- moderate"
        print("%s  total-risk %.1f -> expected score %s%s" % (d, risk, pred_s, trend))
        if pred is not None and pred >= 3:
            flags.append(d)
    if flags:
        print("\nHigh-risk days: %s" % ", ".join(str(x) for x in flags))
        print("If not yet medicated: start antihistamine NOW (takes days to steady).")
    else:
        print("\nNo high-risk days in the window — good stretch.")
    return 0


# ---------------------------------------------------------------- plan

MEDS = {
    "antihistamine": ("start season minus 10-14 days; daily through season",
                      ["cetirizine", "loratadine", "fexofenadine"]),
    "nasal-steroid": ("start season minus 14 days; peak effect needs 1-2 weeks",
                      ["fluticasone", "mometasone", "budesonide"]),
    "eye-drops": ("PRN + before high-pollen outings",
                  ["ketotifen"]),
}

SEASON_ONSET = {  # zone -> class -> (month, day) typical onset
    "temperate-northern": {"tree": (2, 15), "grass": (5, 10), "weed": (7, 25)},
    "mediterranean": {"tree": (1, 5), "grass": (4, 10), "weed": (6, 10)},
    "continental": {"tree": (4, 1), "grass": (6, 1), "weed": (7, 10)},
    "subtropical": {"tree": (1, 1), "grass": (3, 15), "weed": (7, 1)},
    "coastal-low": {"tree": (3, 15), "grass": (5, 1), "weed": (7, 1)},
}


def cmd_plan(args):
    onset = SEASON_ONSET[args.zone][args.target]
    on = dt.date(args.year, onset[0], onset[1])
    print("Pre-medication plan — %s %s, zone %s, season onset ~%s\n"
          % (args.target.upper(), args.year, args.zone, on))
    ah = MEDS["antihistamine"]
    print("1. %s (%s): start %s" %
          (args.antihistamine.title(), ah[1][0], on - dt.timedelta(days=10)))
    ns = MEDS["nasal-steroid"]
    print("2. %s (%s): start %s" %
          (args.nasal_steroid.title(), "nasal spray", on - dt.timedelta(days=14)))
    print("3. Ketotifen eye drops: keep on hand; use before outings from %s" % on)
    print("4. Reassess at season end; if >=2 seasons of scores >=3 lasting >=6 weeks,")
    print("   discuss immunotherapy with an allergist (bring your log).")
    print("\nNot medical advice — confirm choices with pharmacist/doctor.")
    return 0


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="Personal pollen radar.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    lg = sub.add_parser("log", help="symptom log")
    lsub = lg.add_subparsers(dest="logcmd", required=True)
    li = lsub.add_parser("init")
    li.add_argument("--from", dest="from_", required=True)
    li.add_argument("--days", type=int, default=30)
    li.add_argument("--out", required=True)
    li.set_defaults(func=cmd_log_init)
    la = lsub.add_parser("add")
    la.add_argument("--log", required=True)
    la.add_argument("--date", required=True)
    la.add_argument("--score", type=int, required=True, choices=range(0, 6))
    la.add_argument("--eyes", action="store_true")
    la.add_argument("--nose", action="store_true")
    la.add_argument("--lungs", action="store_true")
    la.add_argument("--skin", action="store_true")
    la.add_argument("--note", default="")
    la.set_defaults(func=cmd_log_add)
    ls = lsub.add_parser("show")
    ls.add_argument("--log", required=True)
    ls.set_defaults(func=cmd_log_show)

    cal = sub.add_parser("calendar", help="zone pollen calendar")
    cal.add_argument("--zone", required=True, choices=list(ZONES))
    cal.set_defaults(func=cmd_calendar)

    co = sub.add_parser("correlate", help="find your trigger class")
    co.add_argument("--log", required=True)
    co.add_argument("--zone", required=True, choices=list(ZONES))
    co.set_defaults(func=cmd_correlate)

    fc = sub.add_parser("forecast", help="personal 14-day forecast")
    fc.add_argument("--log", required=True)
    fc.add_argument("--zone", required=True, choices=list(ZONES))
    fc.add_argument("--from", dest="from_", required=True)
    fc.set_defaults(func=cmd_forecast)

    pl = sub.add_parser("plan", help="pre-medication start dates")
    pl.add_argument("--zone", required=True, choices=list(ZONES))
    pl.add_argument("--target", required=True, choices=CLASSES)
    your_year = pl.add_argument("--year", type=int, required=True)
    pl.add_argument("--antihistamine", default="cetirizine")
    pl.add_argument("--nasal-steroid", dest="nasal_steroid", default="fluticasone")
    pl.set_defaults(func=cmd_plan)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
