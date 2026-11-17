#!/usr/bin/env python3
"""Sump Pump Outage Planner — hours-to-critical from pit geometry + measured
inflow, backup option ranking, battery runtime, sizing checks, triage card.
Pure stdlib.

Examples:
    python3 sump_outage.py --pit-diameter 18 --usable-rise-in 14 \
        --off-minutes 8 --on-off-gap-in 6 --storm-mult 3
    python3 sump_outage.py --pit-diameter 18 --usable-rise-in 14 \
        --off-minutes 5 --on-off-gap-in 6 --battery-ah 75 --target-hours 8
    python3 sump_outage.py --triage
"""
import argparse
import json
import math

GAL_PER_CUIN = 1 / 231.0


def gal_per_inch(diameter_in):
    return math.pi * (diameter_in / 2.0) ** 2 * GAL_PER_CUIN


def main():
    ap = argparse.ArgumentParser(description="Sump pump outage clock & backup planner")
    ap.add_argument("--pit-diameter", type=float, default=18)
    ap.add_argument("--usable-rise-in", type=float, default=12,
                    help="resting water level to lowest escape point")
    ap.add_argument("--off-minutes", type=float, default=None,
                    help="measured pump-off period during normal cycling")
    ap.add_argument("--on-off-gap-in", type=float, default=6,
                    help="vertical distance between on and off levels")
    ap.add_argument("--storm-mult", type=float, default=3.0,
                    help="rainy-night inflow multiplier (2-4 typical)")
    ap.add_argument("--inflow-gph", type=float, default=None,
                    help="known inflow, overrides off-period calc")
    ap.add_argument("--battery-ah", type=float, default=None)
    ap.add_argument("--backup-gph", type=float, default=None,
                    help="backup pump rated gph at 10ft head")
    ap.add_argument("--municipal-water", action="store_true",
                    help="city water available (enables water-powered option)")
    ap.add_argument("--target-hours", type=float, default=8)
    ap.add_argument("--triage", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if a.triage:
        print("=" * 64)
        print("2AM SUMP TRIAGE CARD")
        print("=" * 64)
        print("PUMP SILENT:")
        print("  1. Breaker + GFCI test/reset (free, do first)")
        print("  2. Outlet has power? (plug something else)")
        print("  3. Lift float by hand: runs = stuck float ($15 fix)")
        print("  4. GFCI won't reset = ground fault: cord to another")
        print("     circuit as stopgap, replace pump")
        print("PUMP RUNS, WATER RISING:")
        print("  1. Discharge blocked/frozen? Check valve failed (short-cycle)?")
        print("  2. Impeller worn if old and 'weak' — replace pump")
        print("  3. Air lock: clear the weep hole")
        print("  4. Inflow > capacity: second pump time")
        print("PUMP NEVER STOPS:")
        print("  1. Stuck-on float / tangled tether")
        print("  2. Failed check valve (pumping in circles)")
        print("  3. Real inflow beyond capacity: downspouts/grading first")
        print("POWER OUT, NO BACKUP:")
        print("  2-person bucket brigade ~30 gal/10 min. Run the clock below")
        print("  before deciding to bail vs ride it out.")
        print("=" * 64)
        return

    gpi = gal_per_inch(a.pit_diameter)
    usable_gal = a.usable_rise_in * gpi

    if a.inflow_gph is not None:
        base_gph = a.inflow_gph
    elif a.off_minutes:
        gap_gal = a.on_off_gap_in * gpi
        base_gph = gap_gal / a.off_minutes * 60.0
    else:
        base_gph = None

    out = {"gal_per_inch": round(gpi, 2), "usable_gallons": round(usable_gal, 1)}
    if base_gph is None:
        print("Need --off-minutes or --inflow-gph to compute inflow.")
        print(f"Pit geometry only: {gpi:.2f} gal/inch, {usable_gal:.1f} gal usable rise.")
        return

    storm_gph = base_gph * a.storm_mult
    hours = usable_gal / storm_gph if storm_gph > 0 else float("inf")
    out.update({"baseline_gph": round(base_gph), "storm_gph": round(storm_gph),
                "hours_to_critical": round(hours, 2)})

    if hours > 12:
        band = "CALM — a full night of margin; alarm still recommended"
    elif hours > 4:
        band = "BACKUP ESSENTIAL — battery or generator covers most outages"
    elif hours > 1:
        band = "HIGH RISK — dual pumps + high-water alarm, generator plan"
    elif hours > 0.5:
        band = "MINUTES, NOT HOURS — bailing is pointless; backup pump + alarm mandatory"
    else:
        band = "SPRING, NOT A PIT — drainage remediation before any pump shopping"
    out["verdict"] = band

    # backup sizing check
    sizing = None
    if a.backup_gph:
        need = storm_gph * 2
        ok = a.backup_gph >= need
        sizing = {"need_gph": round(need), "rated": a.backup_gph,
                  "verdict": "ADEQUATE (>= 2x storm inflow)" if ok else
                  f"UNDERSIZED — slows the flood only; need >= {need:.0f} gph"}
        out["sizing"] = sizing

    # battery runtime
    battery = None
    if a.battery_ah:
        # 12V backup pump: ~10A when running (conservative incl. losses);
        # duty from storm inflow vs typical 1500gph backup delivery
        delivery_gph = a.backup_gph or 1500.0
        duty = min(1.0, storm_gph / delivery_gph)
        avg_amps = 10.0 * duty
        runtime_h = a.battery_ah * 0.5 / avg_amps  # 50% DoD limit
        covers = runtime_h >= a.target_hours
        battery = {"ah": a.battery_ah, "duty_cycle_pct": round(duty * 100),
                   "runtime_hours": round(runtime_h, 1),
                   "target_hours": a.target_hours,
                   "verdict": (f"COVERS a {a.target_hours:.0f}h outage"
                               if covers else
                               f"FALLS SHORT of {a.target_hours:.0f}h — bigger bank or generator")}
        out["battery"] = battery

    # option ranking
    opts = []
    if battery:
        opts.append((battery["runtime_hours"], f"Battery backup {a.battery_ah:.0f}Ah",
                     f"~{battery['runtime_hours']:.0f} h at storm inflow; replace battery every 3-4 yr"))
    opts.append((24.0, "Portable generator + inlet",
                 "fuel-limited days; runs the main pump at full capacity; CO rules apply"))
    if a.municipal_water:
        opts.append((float("inf"), "Water-powered backup",
                     "unlimited while city pressure holds (~40+ PSI); NOT for wells"))
    else:
        opts.append((0.0, "Water-powered backup",
                     "NOT APPLICABLE — no municipal water detected (well system)"))
    opts.sort(key=lambda t: -t[0])
    out["options"] = [{"protection_h": ("unlimited" if h == float("inf") else round(h)),
                       "name": n, "notes": s} for h, n, s in opts]

    if a.json:
        print(json.dumps(out, indent=2))
        return

    print("=" * 64)
    print("SUMP PUMP OUTAGE CLOCK")
    print("=" * 64)
    print(f"Pit: {a.pit_diameter:.0f} in diameter -> {gpi:.2f} gal/inch")
    print(f"Usable rise: {a.usable_rise_in:.0f} in -> {usable_gal:.1f} gal before trouble")
    src = "measured off-period" if a.off_minutes else "given inflow"
    print(f"Baseline inflow ({src}): {base_gph:.0f} gph")
    print(f"Storm case (x{a.storm_mult:.0f}): {storm_gph:.0f} gph")
    print()
    if hours >= 1:
        print(f"HOURS TO CRITICAL: {hours:.1f} h")
    else:
        print(f"TIME TO CRITICAL: {hours*60:.0f} MINUTES")
    print(f"VERDICT: {band}")
    print()
    if sizing:
        print(f"BACKUP SIZING: {sizing['verdict']} (need {sizing['need_gph']} gph, "
              f"rated {sizing['rated']} gph)")
    if battery:
        print(f"BATTERY: {battery['runtime_hours']} h at {battery['duty_cycle_pct']}% duty "
              f"-> {battery['verdict']}")
    print("BACKUP OPTIONS (ranked by protection hours):")
    for h, n, s in opts:
        hs = "unlimited" if h == float("inf") else f"~{h:.0f} h"
        print(f"  {hs:>10}  {n}: {s}")
    print()
    print("Write the clock on the pit lid. Test backup quarterly (unplug main).")
    print("=" * 64)


if __name__ == "__main__":
    main()
