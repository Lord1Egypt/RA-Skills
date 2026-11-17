#!/usr/bin/env python3
"""Run Pace Architect — training paces, predictions, plans from one race time.

Stdlib-only. Subcommands:
  zones    training pace zones from a reference race performance
  predict  Riegel equivalent performances across distances
  plan     goal feasibility verdict + phase structure for a training block
  ramp     10%-rule weekly mileage ramp with cutback weeks
  splits   even-split table for a goal time and distance
"""
import argparse
import math
import re
import sys

RIEGEL = 1.06

DISTANCES = [
    ("1500m", 1.5, "1500 m"),
    ("1mile", 1.609344, "Mile"),
    ("5k", 5.0, "5K"),
    ("10k", 10.0, "10K"),
    ("15k", 15.0, "15K"),
    ("10mi", 16.09344, "10 miles"),
    ("hm", 21.0975, "Half marathon"),
    ("25k", 25.0, "25K"),
    ("30k", 30.0, "30K"),
    ("marathon", 42.195, "Marathon"),
]
DKEY = {k: km for k, km, _ in DISTANCES}
DLABEL = {k: lab for k, km, lab in DISTANCES}


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(2)


def parse_time(s, long_course=False):
    """'22:30' -> 1350.0 ; '3:15:00' -> 11700.0 ; '1350' -> 1350.0

    With long_course=True (expected time > ~40 min: 15K+), a two-segment
    time with first segment < 10 ('1:45') is read as H:MM — nobody runs a
    half marathon in 1 min 45 s, but everyone writes 1h45m as '1:45'.
    """
    s = s.strip()
    parts = s.split(":")
    if not all(p.strip() and re.fullmatch(r"[\d.]+", p) for p in parts):
        die(f"bad time {s!r} (use MM:SS or H:MM:SS)")
    if long_course and len(parts) == 2 and int(float(parts[0])) < 10:
        parts = [parts[0], parts[1], "0"]
    secs = 0.0
    for p in parts:
        secs = secs * 60 + float(p)
    return secs


def fmt_time(secs):
    secs = int(round(secs))
    h, rem = divmod(secs, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def parse_race(spec):
    """'5k=22:30' -> ('5k', 5.0, 1350.0)"""
    if "=" not in spec:
        die(f"race spec {spec!r} must look like 5k=22:30")
    key, t = spec.split("=", 1)
    key = key.strip().lower().replace(" ", "")
    if key not in DKEY:
        die(f"unknown distance {key!r}; choose from {', '.join(DKEY)}")
    tsec = parse_time(t, long_course=DKEY[key] >= 15.0)
    if tsec <= 0:
        die("time must be positive")
    return key, DKEY[key], tsec


def riegel(t1, d1, d2):
    return t1 * (d2 / d1) ** RIEGEL


def pace_per_km(seconds, km):
    return seconds / km


def fmt_pace(sec_per_km, unit="km"):
    if unit == "mi":
        spm = sec_per_km * 1.609344
        label = "/mi"
    else:
        spm = sec_per_km
        label = "/km"
    return f"{mcm(spm)}{label}"


def mcm(spm):
    """seconds-per-unit -> 'M:SS' (carries 60s into the minute)."""
    m = int(spm // 60)
    s = int(round(spm % 60))
    if s == 60:
        m, s = m + 1, 0
    return f"{m}:{s:02d}"


def fmt_pace_range(lo, hi, unit="km"):
    return f"{fmt_pace(lo, unit)}–{fmt_pace(hi, unit)}"


# ---------------------------------------------------------------- zones
def solve_60min_pace(ref_km, ref_sec):
    """Binary-search the distance D whose Riegel-predicted time is 3600 s."""
    lo, hi = 1.0, 60.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if riegel(ref_sec, ref_km, mid) < 3600:
            lo = mid
        else:
            hi = mid
    d60 = (lo + hi) / 2
    return 3600.0 / d60  # sec per km


def cmd_zones(args):
    key, d1, t1 = parse_race(args.race)
    mar_pace = pace_per_km(riegel(t1, d1, DKEY["marathon"]), DKEY["marathon"])
    easy_lo = mar_pace + 45
    easy_hi = mar_pace + 75
    long_lo, long_hi = easy_lo + (easy_hi - easy_lo) / 2, easy_hi
    thr = solve_60min_pace(d1, t1)
    itv = pace_per_km(riegel(t1, d1, 3.0), 3.0)
    rep = pace_per_km(riegel(t1, d1, 1.5), 1.5)

    u = args.unit
    print(f"Reference performance: {DLABEL[key]} in {fmt_time(t1)} "
          f"({fmt_pace(pace_per_km(t1, d1))})")
    print()
    print(f"{'Zone':<12} {'Pace':<20} Basis")
    print("-" * 58)
    print(f"{'Easy':<12} {fmt_pace_range(easy_lo, easy_hi, u):<20} marathon pace +45–75 s/km")
    print(f"{'Long run':<12} {fmt_pace_range(long_lo, long_hi, u):<20} upper half of easy")
    print(f"{'Marathon':<12} {fmt_pace(mar_pace, u):<20} Riegel @ 42.195 km")
    print(f"{'Threshold':<12} {fmt_pace(thr, u):<20} your 60-minute pace (solved)")
    print(f"{'Interval':<12} {fmt_pace(itv, u):<20} ~3K race effort (VO2max)")
    print(f"{'Repetition':<12} {fmt_pace(rep, u):<20} ~1500 m race effort")
    print()
    print("Weekly shape: ~80% of volume easy, <=2 hard sessions, strides 2x/wk.")


# ---------------------------------------------------------------- predict
def cmd_predict(args):
    key, d1, t1 = parse_race(args.race)
    targets = [t.strip().lower() for t in (args.to or "").split(",") if t.strip()]
    for t in targets:
        if t not in DKEY:
            die(f"unknown distance {t!r}")
    rows = [(k, km, lab) for k, km, lab in DISTANCES
            if not targets or k in targets]
    print(f"From: {DLABEL[key]} in {fmt_time(t1)}")
    print()
    print(f"{'Distance':<15} {'Predicted':<10} Pace")
    print("-" * 40)
    for k, km, lab in rows:
        if k == key and not targets:
            continue
        t = riegel(t1, d1, km)
        print(f"{lab:<15} {fmt_time(t):<10} {fmt_pace(pace_per_km(t, km))}")
    print()
    print("Riegel exponent 1.06; assumes even pace, road terrain, adequate")
    print("training for the target distance.")


# ---------------------------------------------------------------- plan
def feasibility(current, goal, weeks, trained=None):
    req = (current - goal) / current
    blocks = max(weeks / 10.0, 0.5)  # normalize to a 10-week block
    per_block = req / blocks
    if trained is None:
        trained = req <= 0.03 * blocks  # assume trained if modest ask
    band = 0.03 if trained else 0.08
    if per_block <= 0.01:
        verdict = "LIKELY"
    elif per_block <= band:
        verdict = "LIKELY" if trained else "LIKELY (novice headroom)"
    elif per_block <= 2 * band:
        verdict = "AGGRESSIVE"
    else:
        verdict = "UNREALISTIC"
    return req, per_block, verdict, trained


def cmd_plan(args):
    ckey, cd, ct = parse_race(args.race)
    gkey, gd, gt = parse_race(args.goal)
    if gkey != ckey:
        die("plan expects the same distance for --race and --goal")
    req, per_block, verdict, trained = feasibility(ct, gt, args.weeks)
    pct = req * 100
    print(f"Goal: {DLABEL[gkey]} {fmt_time(ct)} -> {fmt_time(gt)} "
          f"in {args.weeks} weeks")
    print(f"Required improvement: {pct:.1f}% total "
          f"(~{per_block*100:.1f}% per 10-wk block)")
    print(f"Verdict: {verdict}")
    print()
    if verdict == "UNREALISTIC":
        print("Split into two blocks with an intermediate race; or relax the")
        print("goal. Large single-block jumps are the classic injury path.")
        print()
    elif verdict == "AGGRESSIVE":
        print("Extend to 10-12 weeks if possible; keep easy days genuinely")
        print("easy so the hard days can count.")
        print()

    n = args.weeks
    base = max(1, int(round(n * 0.5)))
    rest = n - base
    build = max(1, int(round(rest * 0.6))) if rest >= 2 else max(1, rest)
    peak = max(0, rest - build - 1)
    phases = [("BASE", base, "volume +, strides 2x/wk, long run extends"),
              ("BUILD", build, "VO2max intervals + threshold, race-pace in long runs"),
              ("PEAK", max(peak, 0) or 0, "race-specific sharpening, volume starts dropping")]
    if n >= 3:
        phases.append(("TAPER", 1, "-30-40% volume, keep intensity touches"))
    print(f"{'Weeks':<8} {'Phase':<7} Focus")
    print("-" * 56)
    w = 1
    for name, weeks_n, focus in phases:
        if weeks_n <= 0:
            continue
        rng = f"W{w}" if weeks_n == 1 else f"W{w}-{w+weeks_n-1}"
        print(f"{rng:<8} {name:<7} {focus}")
        w += weeks_n
    print()
    print(f"Paces for this block (from {fmt_time(ct)} {DLABEL[ckey]}):")
    print(f"  easy {fmt_pace_range(*easy_from(ct, cd))}, "
          f"threshold {fmt_pace(solve_60min_pace(cd, ct))}")


def easy_from(t1, d1):
    mar = pace_per_km(riegel(t1, d1, DKEY["marathon"]), DKEY["marathon"])
    return (mar + 45, mar + 75)


# ---------------------------------------------------------------- ramp
def cmd_ramp(args):
    cur, tgt = args.current, args.target
    if cur <= 0 or tgt <= 0:
        die("mileage must be positive")
    week, miles, weeks = 0, float(cur), []
    while miles < tgt - 1e-9 and week < 104:
        week += 1
        if week % 4 == 0:
            miles = max(miles * 0.8, cur)
            tag = "cutback -20%"
        else:
            cap = miles * 1.10
            miles = min(cap, tgt)
            tag = ""
        weeks.append((week, round(miles, 1), tag))
    print(f"Mileage ramp: {cur} -> {tgt} {args.unit}/week "
          f"(max +10%/wk, -20% every 4th week)")
    print()
    print(f"{'Week':<6} {'Volume':<8} Note")
    print("-" * 30)
    for w, m, t in weeks:
        print(f"W{w:<5} {m:<8} {t}")
    print()
    print(f"Reaches target in {len(weeks)} week(s). Hold intensity flat while")
    print("volume climbs; add quality only after 2-3 stable weeks.")


# ---------------------------------------------------------------- splits
def cmd_splits(args):
    key = args.race.strip().lower()
    if key not in DKEY:
        die(f"unknown distance {key!r}")
    km = DKEY[key]
    goal = parse_time(args.goal, long_course=km >= 15.0)
    pk = goal / km
    pm = goal / (km / 1.609344)
    print(f"{DLABEL[key]} goal {fmt_time(goal)} — even-split table")
    print()
    print(f"Pace: {fmt_pace(pk)}  |  {fmt_pace(pm, 'mi')}")
    print()
    marks_km = [i for i in range(1, int(km) + 1)]
    print(f"{'km':<6} {'elapsed':<9} {'split':<7}")
    print("-" * 24)
    for i in marks_km:
        print(f"{i:<6} {fmt_time(pk*i):<9} {fmt_pace(pk)}")
    frac = km - int(km)
    if frac > 1e-6:
        print(f"{km:<6.2f} {fmt_time(goal):<9} final {frac*1000:.0f} m "
              f"@ {fmt_pace(pk)}")
    # a few mile marks
    mile_km = 1.609344
    mi = 1
    print()
    print("Mile marks: ", end="")
    while mi * mile_km < km:
        el = pk * mi * mile_km
        print(f"{fmt_time(el)}@mi{mi}", end="  ")
        mi += 1
    print()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("zones", help="training paces from a race performance")
    p.add_argument("--race", required=True, help="e.g. 5k=22:30")
    p.add_argument("--unit", choices=["km", "mi"], default="km")
    p.set_defaults(fn=cmd_zones)

    p = sub.add_parser("predict", help="equivalent performances")
    p.add_argument("--race", required=True, help="e.g. 10k=48:00")
    p.add_argument("--to", default="", help="comma list: hm,marathon,10k...")
    p.set_defaults(fn=cmd_predict)

    p = sub.add_parser("plan", help="goal feasibility + phase structure")
    p.add_argument("--race", required=True, help="current, e.g. 5k=22:30")
    p.add_argument("--goal", required=True, help="goal, same distance")
    p.add_argument("--weeks", type=int, default=8)
    p.set_defaults(fn=cmd_plan)

    p = sub.add_parser("ramp", help="10%%-rule mileage ramp")
    p.add_argument("--current", type=float, required=True)
    p.add_argument("--target", type=float, required=True)
    p.add_argument("--unit", default="km")
    p.set_defaults(fn=cmd_ramp)

    p = sub.add_parser("splits", help="even-split table for a goal time")
    p.add_argument("--race", required=True, help="5k|10k|hm|marathon|...")
    p.add_argument("--goal", required=True, help="e.g. 1:45 or 3:30:00")
    p.set_defaults(fn=cmd_splits)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
