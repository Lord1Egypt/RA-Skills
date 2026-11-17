#!/usr/bin/env python3
"""Septic hydraulic load balancer.

Computes a septic system's daily/short-window hydraulic budget (tank working
volume + drainfield design flow) and audits or reschedules a household's water
plan. Pure stdlib.

Model sources:
- Classic sizing: ~150 gal/bedroom/day design flow (many state codes).
- Tank equalization: single-hour slugs < ~15% of working volume protect the
  field from solids carryover.
- Fixture flows: EPA WaterSense / DOE appliance data ranges.
"""
import argparse
import json

GAL_PER_BEDROOM_DAY = 150.0
WORKING_FRACTION = 0.80          # tank working volume vs total (scum/sludge reserve)
HOURLY_CAP_FRAC = 0.15           # max gal in any single hour vs working volume

WASHERS = {   # gal per load
    "top": 40.0, "front": 15.0, "he-top": 18.0,
}
DISHWASHER_GAL = 8.0
SHOWER_GPM = 2.1
BATH_GAL = 35.0
TOILET_GAL = {"new": 1.6, "old": 3.5}
SOFTENER_REGEN_GAL = 60.0


def base_daily(persons: int, toilets: str, flushes_pp: int = 5,
               faucet_min_pp: int = 8, faucet_gpm: float = 1.5):
    """Baseline indoor use without laundry/dish machines."""
    d = {}
    d["toilets"] = persons * flushes_pp * TOILET_GAL[toilets]
    d["faucets"] = persons * faucet_min_pp * faucet_gpm
    return d


def plan_day(laundry_loads=0, washer="top", dishwasher_runs=0, showers=0,
             shower_min=8, baths=0, persons=2, toilets="new", softener_regen=False):
    """Return (total_gal, hourly list of 24 slots, breakdown)."""
    br = base_daily(persons, toilets)
    total = sum(br.values())
    hours = [0.0] * 24

    # spread baseline across waking hours 7am-10pm (16 h)
    per_h = total / 16
    for h in range(7, 23):
        hours[h] += per_h

    # laundry: each load = wash+rinse over ~1h, back-to-back
    lp = WASHERS[washer] * laundry_loads
    total += lp
    for i in range(laundry_loads):
        hours[9 + i] += WASHERS[washer]  # start ~9am default

    dw = DISHWASHER_GAL * dishwasher_runs
    total += dw
    for i in range(dishwasher_runs):
        hours[20 + i] += DISHWASHER_GAL  # after dinner

    sh = SHOWER_GPM * shower_min * showers
    total += sh
    for i in range(showers):
        hours[6 + i // 2] += SHOWER_GPM * shower_min  # staggered pairs

    tb = BATH_GAL * baths
    total += tb
    for i in range(baths):
        hours[19] += BATH_GAL

    if softener_regen:
        total += SOFTENER_REGEN_GAL
        hours[2] += SOFTENER_REGEN_GAL

    return total, hours, {"baseline(toilets+faucets)": round(sum(br.values()), 1),
                          "laundry": round(lp, 1), "dishwasher": round(dw, 1),
                          "showers": round(sh, 1), "baths": round(tb, 1),
                          "softener": SOFTENER_REGEN_GAL if softener_regen else 0}


def budget(tank_gal, bedrooms):
    field_cap = GAL_PER_BEDROOM_DAY * bedrooms
    working = tank_gal * WORKING_FRACTION
    tank_cap = working / 3.0        # conservative: field should see <= 1/3 working vol/day as sustained flow
    return min(field_cap, tank_cap), field_cap, working


def verdict_and_plan(tank_gal, bedrooms, laundry_loads, washer, persons,
                     toilets="new", softener=False, showers=None, shower_min=8):
    daily_cap, field_cap, working = budget(tank_gal, bedrooms)
    hourly_cap = working * HOURLY_CAP_FRAC
    if showers is None:
        showers = persons

    total, hours, br = plan_day(laundry_loads, washer, 1, showers, shower_min,
                                0, persons, toilets, softener)
    peak_h = max(hours)
    breaches = []
    if total > daily_cap:
        breaches.append(f"day total {total:.0f} gal > daily budget {daily_cap:.0f} gal "
                        f"(field capacity {field_cap:.0f} gal/day)")
    if peak_h > hourly_cap:
        breaches.append(f"peak hour {peak_h:.0f} gal > hourly surge cap {hourly_cap:.0f} gal "
                        f"(solids-carryover protection)")

    # --- redistribution solver: laundry spread across days ---
    loads_ok = max(0, int((daily_cap - (total - WASHERS[washer] * laundry_loads)) // WASHERS[washer]))
    if laundry_loads > 0 and (breaches or laundry_loads > loads_ok):
        per_day = 1 if washer == "top" else 2
        days = []
        remaining = laundry_loads
        while remaining > 0:
            take = min(per_day, remaining)
            days.append(take)
            remaining -= take
        plan = {("today" if i == 0 else f"day+{i}"): f"{n} load(s)" for i, n in enumerate(days)}
        # fix today's load count to the first planned day
        safe_today = days[0] if days else laundry_loads
    else:
        plan = {}
        safe_today = laundry_loads

    band = "OK" if not breaches else "OVERLOADED"

    advice = []
    if washer == "top":
        advice.append("top-loader uses ~2.5x the water of a front-loader: switching is the single biggest lever")
    if softener:
        advice.append("move softener regeneration to a low-use morning, never same-day as laundry catch-up")
    if showers and shower_min >= 12:
        advice.append("long showers stack: keep 30+ min between consecutive showers on guest days")
    if total > daily_cap:
        advice.append(f"cut ~{total - daily_cap:.0f} gal/day or spread use; sustained over-budget flow saturates the field")
    advice.append("pump the tank on sludge depth (~every 3 yr typical), not on 'looks full'")

    return {
        "verdict": band,
        "daily_budget_gal": round(daily_cap),
        "day_total_gal": round(total),
        "hourly_surge_cap_gal": round(hourly_cap),
        "peak_hour_gal": round(peak_h),
        "breakdown": br,
        "breaches": breaches,
        "laundry_safe_today": safe_today,
        "redistribution_plan": plan,
        "advice": advice,
    }


def main():
    p = argparse.ArgumentParser(description="Septic hydraulic load balancer")
    p.add_argument("--demo", action="store_true")
    p.add_argument("--tank-gal", type=float, default=1000.0, help="septic tank capacity")
    p.add_argument("--bedrooms", type=int, default=3, help="bedrooms the field was sized for")
    p.add_argument("--laundry-loads", type=int, default=0)
    p.add_argument("--washer", choices=sorted(WASHERS), default="top")
    p.add_argument("--persons", type=int, default=2)
    p.add_argument("--toilets", choices=sorted(TOILET_GAL), default="new")
    p.add_argument("--softener", action="store_true", help="water softener regenerates today")
    p.add_argument("--showers", type=int, help="showers today (default = persons + guests... just persons)")
    p.add_argument("--shower-min", type=float, default=8)
    p.add_argument("--guests", type=int, default=0, help="extra persons today")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    if a.demo:
        r = verdict_and_plan(1000, 3, laundry_loads=6, washer="top", persons=4,
                             softener=True, showers=6, shower_min=10)
    else:
        persons = a.persons + a.guests
        showers = a.showers if a.showers is not None else persons
        r = verdict_and_plan(a.tank_gal, a.bedrooms, a.laundry_loads, a.washer,
                             persons, a.toilets, a.softener, showers, a.shower_min)

    if a.json:
        print(json.dumps(r, indent=2)); return

    print(f"VERDICT: {r['verdict']}")
    print(f"Daily budget: {r['daily_budget_gal']} gal | today's plan: {r['day_total_gal']} gal")
    print(f"Hourly surge cap: {r['hourly_surge_cap_gal']} gal | peak hour: {r['peak_hour_gal']} gal")
    for b in r["breaches"]:
        print(f"  ! {b}")
    if r["breakdown"]:
        print("Breakdown (gal): " + ", ".join(f"{k}={v}" for k, v in r["breakdown"].items()))
    if r["redistribution_plan"]:
        print(f"Laundry: do {r['laundry_safe_today']} load(s) today, then -> " +
              "; ".join(f"{d}: {n}" for d, n in r["redistribution_plan"].items()))
    for s in r["advice"]:
        print(f"  - {s}")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        pass
