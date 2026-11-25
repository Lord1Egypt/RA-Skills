#!/usr/bin/env python3
"""Smoker Pitmaster Planner — low-and-slow BBQ timeline + probe ETA.

Subcommands:
  plan   Back-plan a full cook timeline from serve time.
  probe  Mid-cook: fit heating rate from a live reading, forecast ETA.

stdlib only.
"""
import argparse
import json
import math
import sys
from datetime import datetime, timedelta

# --- meat database ---------------------------------------------------------
# k_ref: Newton heating coeff (1/h) at pit 110C, for m_ref kg
# stall: stall hours per kg in the 65-75C band (0 = thin cut, no real stall)
# pull_quality / safety: degC
MEATS = {
    "brisket":        dict(label="Beef brisket (packer)", m_ref=6.5, k_ref=0.1040,
                           stall=0.90, pull_quality=94, safety=71, rest_h=2.5),
    "pork_shoulder":  dict(label="Pork shoulder / butt",  m_ref=4.5, k_ref=0.1900,
                           stall=0.85, pull_quality=93, safety=63, rest_h=1.5),
    "spare_ribs":     dict(label="Spare / St-Louis ribs", m_ref=2.5, k_ref=0.2900,
                           stall=0.25, pull_quality=90, safety=63, rest_h=0.75),
    "baby_back_ribs": dict(label="Baby back ribs",        m_ref=1.4, k_ref=0.3450,
                           stall=0.15, pull_quality=88, safety=63, rest_h=0.5),
    "whole_chicken":  dict(label="Whole chicken (spatchcock ok)", m_ref=2.0, k_ref=0.3000,
                           stall=0.05, pull_quality=78, safety=74, rest_h=0.4),
    "turkey":         dict(label="Whole turkey",          m_ref=7.0, k_ref=0.1600,
                           stall=0.15, pull_quality=76, safety=74, rest_h=0.75),
    "tri_tip":        dict(label="Beef tri-tip",          m_ref=1.5, k_ref=0.2400,
                           stall=0.05, pull_quality=56, safety=63, rest_h=0.5),
    "pork_belly":     dict(label="Pork belly burnt ends", m_ref=2.0, k_ref=0.4000,
                           stall=0.50, pull_quality=92, safety=63, rest_h=0.5),
}

COOKERS = {  # charcoal/lump kg per hour at 110-120C
    "kettle": dict(rate=0.75, fuel="briquettes"),
    "offset": dict(rate=1.10, fuel="lump charcoal"),
    "kamado": dict(rate=0.40, fuel="lump charcoal"),
    "pellet": dict(rate=0.70, fuel="wood pellets"),
}

STALL_LO, STALL_HI = 65.0, 75.0
T0_DEFAULT = 5.0  # fridge temp degC


def newton_time(k, t_pit, t0, target):
    """Hours for Newton heating from t0 to target."""
    frac = (t_pit - target) / (t_pit - t0)
    if frac <= 0:
        return 0.0
    return -math.log(frac) / k


def cook_hours(meat, mass, pit, wrap):
    """Two-segment model: (pre-stall climb, stall, post-stall climb).

    Pre-stall: Newton to 65C with k scaled by mass.
    Stall: stall_h_per_kg * mass, cut 65% if wrapped.
    Post-stall: Newton 75C -> pull with k boosted if wrapped.
    Returns (hours, detail dict).
    """
    m = MEATS[meat]
    k_pre = m["k_ref"] * (m["m_ref"] / mass) ** (1.0 / 3.0)
    k_post = k_pre * (1.6 if wrap else 1.0)
    t_pre = newton_time(k_pre, pit, T0_DEFAULT, min(STALL_LO, m["pull_quality"]))
    stall = m["stall"] * mass * (0.35 if wrap else 1.0)
    t_post = 0.0
    if m["pull_quality"] > STALL_HI:
        t_post = newton_time(k_post, pit, STALL_HI, m["pull_quality"])
    # thin/no-stall meats: if pull target below stall band, pre covered it all
    if m["pull_quality"] <= STALL_LO:
        stall = 0.0
    total = t_pre + stall + t_post
    return total, dict(k_pre=k_pre, t_pre=t_pre, stall=stall, k_post=k_post, t_post=t_post)


def fuel(kg_h, hours, cooker):
    used = kg_h * hours
    return used, used * 1.25  # reserve


def fmt_hm(hours):
    h = int(hours)
    m = round((hours - h) * 60)
    if m == 60:
        h, m = h + 1, 0
    return f"{h}h{m:02d}m"


def cmd_plan(a):
    mass = a.weight_kg if a.weight_kg else (a.weight_lb * 0.4536)
    pit = a.pit_c if a.pit_c is not None else (a.pit_f - 32) * 5 / 9
    m = MEATS[a.meat]
    if m["pull_quality"] < m["safety"]:
        # tri-tip style: rare target below safety floor -> warn loudly
        print(f"!! {a.meat}: quality pull {m['pull_quality']}C is BELOW the whole-cut "
              f"safety context; whole-muscle beef is sear-then-rare legal, ground is not.")
    hours, det = cook_hours(a.meat, mass, pit, a.wrap)
    planned = hours * a.uncertainty
    rest = m["rest_h"] * (1.5 if a.long_rest else 1.0)
    ck = COOKERS[a.cooker]
    fuel_used, fuel_res = fuel(ck["rate"], planned, a.cooker)

    serve = datetime.fromisoformat(a.serve)
    serve_dt = serve - timedelta(hours=rest)          # pull by
    put_on = serve_dt - timedelta(hours=planned)      # start by

    print("=" * 64)
    print(f"{m['label']}  {mass:.1f} kg  @  {pit:.0f} C pit  "
          f"({'wrapped' if a.wrap else 'no wrap'})")
    print("=" * 64)
    print(f"Serve time            : {serve:%a %Y-%m-%d %H:%M}")
    print(f"Rest window           : {fmt_hm(rest)}  (cooler, towels)")
    print(f"Pull internal temp    : {m['pull_quality']} C quality / "
          f"{m['safety']} C safety floor")
    print(f"Cook time (model)     : {fmt_hm(hours)}")
    print(f"Cook time (planned)   : {fmt_hm(planned)}  (x{a.uncertainty} uncertainty)")
    print(f"  pre-stall climb     : {fmt_hm(det['t_pre'])} to {STALL_LO:.0f} C "
          f"(k={det['k_pre']:.3f}/h)")
    print(f"  STALL {STALL_LO:.0f}-{STALL_HI:.0f} C : {fmt_hm(det['stall'])} "
          f"{'(wrapped, cut ~65%)' if a.wrap else '(NORMAL - do not open lid)'}")
    if det["t_post"] > 0:
        print(f"  post-stall climb    : {fmt_hm(det['t_post'])} to pull")
    print(f"PUT ON BY             : {put_on:%a %Y-%m-%d %H:%M}")
    print(f"Pull by               : {serve_dt:%a %Y-%m-%d %H:%M}")
    slack = (serve_dt - put_on).total_seconds() / 3600 - hours
    print(f"Schedule slack        : {fmt_hm(max(slack, 0))} absorbed by uncertainty factor")
    print(f"Fuel ({ck['fuel']:<14}): {fuel_used:.1f} kg cook + reserve = {fuel_res:.1f} kg "
          f"({a.cooker} @ {ck['rate']} kg/h)")
    print("-" * 64)
    print("Doctrine: finish EARLY and hold (rest up to 2-4h for big cuts).")
    print("Running late? Raise pit 10-15C and wrap - do NOT serve under-temp.")
    if m["stall"] > 0.5 and not a.wrap:
        print("Stall advice: 65-75C plateau is evaporation, not failure;")
        print("  options = power through (best bark) / wrap (fastest) / +10C pit.")
    return 0


def cmd_probe(a):
    mass = a.weight_kg if a.weight_kg else (a.weight_lb * 0.4536)
    pit = a.pit_c if a.pit_c is not None else (a.pit_f - 32) * 5 / 9
    m = MEATS[a.meat]
    t0 = a.start_c if a.start_c else T0_DEFAULT
    frac = (pit - a.internal_c) / (pit - t0)
    if frac <= 0:
        print("Reading at/above pit temp - check probe placement.")
        return 1
    k_fit = -math.log(frac) / a.elapsed_h
    k_norm = m["k_ref"] * (m["m_ref"] / mass) ** (1 / 3)
    remaining = newton_time(k_fit, pit, a.internal_c, m["pull_quality"])
    eta = datetime.now() + timedelta(hours=remaining)

    in_stall = STALL_LO <= a.internal_c <= STALL_HI
    print("=" * 64)
    print(f"PROBE FIT  {m['label']} {mass:.1f} kg @ {pit:.0f} C pit")
    print(f"Elapsed {fmt_hm(a.elapsed_h)}, internal {a.internal_c:.1f} C")
    print(f"Fitted k   : {k_fit:.3f}/h   (class norm {k_norm:.3f}/h)")
    ratio = k_fit / k_norm if k_norm else 0
    if in_stall and ratio < 0.75:
        verdict = "STALLED (normal evaporative stall)"
        rem = max(remaining, 1.5 * mass * m["stall"] * 0.4)
        print(f"VERDICT    : {verdict}")
        print(f"  Plateau zone 65-75C. Expected up to "
              f"{fmt_hm(m['stall'] * mass)} total stall; then it moves.")
        print("  Do: keep lid closed; wrap or +10-15C pit if schedule-tight.")
        eta = datetime.now() + timedelta(hours=rem)
        print(f"ETA to pull: ~{eta:%H:%M} (stall-adjusted {fmt_hm(rem)})")
    elif ratio < 0.6:
        print("VERDICT    : BEHIND (slow but climbing)")
        print(f"  ETA at current rate: {eta:%H:%M} ({fmt_hm(remaining)} left)")
        print("  Do: verify pit temp actually at target; +10-15C if late-risk.")
    else:
        print("VERDICT    : ON TRACK")
        print(f"  ETA to pull: {eta:%H:%M} ({fmt_hm(remaining)} left)")
    print(f"Pull at    : {m['pull_quality']} C (quality) / {m['safety']} C floor")
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("plan")
    pl.add_argument("--meat", required=True, choices=MEATS)
    pl.add_argument("--weight-kg", type=float)
    pl.add_argument("--weight-lb", type=float)
    pl.add_argument("--pit-c", type=float)
    pl.add_argument("--pit-f", type=float)
    pl.add_argument("--serve", required=True, help="ISO datetime, e.g. 2026-11-28T18:00")
    pl.add_argument("--wrap", action="store_true")
    pl.add_argument("--cooker", default="kettle", choices=COOKERS)
    pl.add_argument("--uncertainty", type=float, default=1.25)
    pl.add_argument("--long-rest", action="store_true")
    pl.set_defaults(fn=cmd_plan)

    pr = sub.add_parser("probe")
    pr.add_argument("--meat", required=True, choices=MEATS)
    pr.add_argument("--weight-kg", type=float)
    pr.add_argument("--weight-lb", type=float)
    pr.add_argument("--pit-c", type=float)
    pr.add_argument("--pit-f", type=float)
    pr.add_argument("--elapsed-h", type=float, required=True)
    pr.add_argument("--internal-c", type=float, required=True)
    pr.add_argument("--start-c", type=float)
    pr.set_defaults(fn=cmd_probe)

    a = p.parse_args()
    if (a.weight_kg is None and a.weight_lb is None):
        p.error("give --weight-kg or --weight-lb")
    if (a.pit_c is None and a.pit_f is None):
        p.error("give --pit-c or --pit-f")
    sys.exit(a.fn(a))


if __name__ == "__main__":
    main()
