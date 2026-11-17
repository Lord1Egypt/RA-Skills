#!/usr/bin/env python3
"""Rain Barrel Harvest Planner — catchment yield, irrigation demand,
storage mass-balance simulation, overflow routing and payback.
Stdlib only."""
import argparse

RUNOFF = {  # runoff coefficients by roof surface
    "asphalt": 0.90, "metal": 0.95, "tile": 0.80,
    "membrane": 0.95, "gravel": 0.70, "thatch": 0.60, "green": 0.40,
}

GAL_PER_FT2_IN = 0.623  # gallons per ft² per inch of rain


def gallons(area_ft2, rain_in, coeff):
    return area_ft2 * rain_in * GAL_PER_FT2_IN * coeff


def liters(area_ft2, rain_in, coeff):
    return gallons(area_ft2, rain_in, coeff) * 3.785


def cmd_catchment(a):
    coeff = RUNOFF[a.surface]
    annual_gal = gallons(a.area_ft2, a.rain_in, coeff)
    annual_l = annual_gal * 3.785
    print(f"CATCHMENT YIELD — {a.area_ft2:.0f} ft² {a.surface} roof, "
          f"{a.rain_in:.1f} in/yr (coeff {coeff})")
    print(f"  annual harvestable: {annual_gal:,.0f} gal "
          f"({annual_l:,.0f} L)")
    print(f"  per 1 in storm:     {gallons(a.area_ft2, 1, coeff):,.0f} gal")
    if a.first_flush_mm is not None:
        # first-flush waste: mm over catchment area
        area_m2 = a.area_ft2 * 0.092903
        waste_l = area_m2 * a.first_flush_mm
        print(f"  first-flush diverter ({a.first_flush_mm} mm): "
              f"discards {waste_l:,.0f} L per storm — negligible annually,")
        print(f"  essential for water quality (bird droppings + grit).")
    print(f"  rule of thumb: every 1,000 ft² of roof yields ~"
          f"{gallons(1000, a.rain_in, coeff):,.0f} gal/yr in your climate.")


def cmd_demand(a):
    weekly = a.area_m2 * a.liters_per_m2
    season = weekly * a.weeks
    print(f"IRRIGATION DEMAND — {a.area_m2:.0f} m² planted area, "
          f"{a.liters_per_m2} L/m²/week, {a.weeks} dry-season weeks")
    print(f"  weekly demand:   {weekly:,.0f} L/wk")
    print(f"  season demand:   {season:,.0f} L")
    print(f"  per single 200 L barrel: {200 / weekly * 100:.0f}% of one week")
    if weekly > 1000:
        print("  -> >1,000 L/wk: single-barrel systems are a gesture here;")
        print("     plan daisy-chains or a cistern (see storage command).")
    print(f"  doctrine bands: vegetables 15-20 L/m²/wk, lawns 20-25,")
    print(f"  xeric/native beds 5-8. New plantings the first summer: 1.5x.")


def cmd_storage(a):
    coeff = RUNOFF[a.surface]
    rains = [float(x) for x in a.monthly_in.split(",")]
    if len(rains) < 6:
        raise SystemExit("need >=6 monthly rainfall values")
    storage = 0.0
    used = 0.0
    overflow = 0.0
    shortfall = 0.0
    demand_m = a.demand_area_m2 * a.lpm2 * 4.33  # weekly -> month
    print(f"STORAGE SIMULATION — {a.area_ft2:.0f} ft² {a.surface} roof, "
          f"{a.capacity:.0f} L storage, {a.demand_area_m2:.0f} m² @ "
          f"{a.lpm2} L/m²/wk")
    print(f"  (demand months assumed = {'all' if a.all_months else 'dry-half'} "
          f"of the year)")
    names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    # demand applied to second half of list (dry season) unless --all-months
    demand_flags = ([True] * len(rains) if a.all_months else
                    [False] * (len(rains) // 2) + [True] * (len(rains) - len(rains) // 2))
    print("  month  rain    inflow      demand     overflow   shortfall")
    for i, rain in enumerate(rains):
        inflow = liters(a.area_ft2, rain, coeff)
        dem = demand_m if demand_flags[i] else 0.0
        # first-flush deduction per raining month (~1 mm)
        inflow = max(0.0, inflow - a.area_ft2 * 0.092903 * 1.0)
        take = min(storage + inflow, dem)
        storage = storage + inflow - take
        ov = 0.0
        if storage > a.capacity:
            ov = storage - a.capacity
            storage = a.capacity
        short = dem - take
        overflow += ov
        shortfall += short
        used += take
        print(f"  {names[i % 12]:<5} {rain:4.1f}in {inflow:9,.0f} L "
              f"{dem:9,.0f} L {ov:9,.0f} L {short:9,.0f} L")
    total_demand = sum(demand_m for f, demand_m in
                       zip(demand_flags, [demand_m] * len(rains)) if f)
    frac = used / total_demand if total_demand else 1.0
    print(f"\n  season used: {used:,.0f} L of {total_demand:,.0f} L demand "
          f"({frac:.0%})")
    print(f"  overflow wasted: {overflow:,.0f} L")
    if frac >= 0.9:
        v = "SYSTEM SIZED — demand essentially fully served."
    elif frac >= 0.6:
        v = ("WORKS — meaningful offset. If overflow is large, the")
        v += " constraint is DEMAND: irrigate more area or add beds."
    elif frac >= 0.3:
        v = ("HALF-SERVES — the barrel delays municipal water, doesn't")
        v += " replace it. Add capacity, or accept a partial system."
    else:
        v = ("GESTURE — mostly overflow or empty. Storage and demand are")
        v += " mismatched; rerun with different capacity/demand."
    print(f"VERDICT: {v}")
    if overflow > 3 * used and used > 0:
        print(f"  ({overflow:,.0f} L overflowed vs {used:,.0f} L used —")
        print(f"   this roof could serve far more demand; consider")
        print(f"   expanding irrigated area before buying storage.)")


def cmd_payback(a):
    value_per_gal = (a.water_rate + a.sewer_credit) / 1000.0
    annual_value = a.used_gal * value_per_gal
    print(f"PAYBACK — {a.used_gal:,.0f} gal used/yr @ "
          f"${a.water_rate:.2f}/kgal water + ${a.sewer_credit:.2f}/kgal credit")
    print(f"  annual value: ${annual_value:,.0f}/yr")
    if annual_value <= 0:
        print("  no water cost — payback undefined (harvest for ecology,")
        print("  soft water, or outage resilience instead).")
        return
    pb = a.cost / annual_value
    print(f"  payback on ${a.cost:,.0f}: {pb:.1f} yr")
    if pb <= 5:
        print("  VERDICT: PAYS — clear win at your rates.")
    elif pb <= 12:
        print("  VERDICT: SLOW — justify on resilience/soft-water grounds")
        print("  too; check utility rebates (often $50-100/barrel).")
    else:
        print("  VERDICT: DOESN'T PAY ECONOMICALLY — common at flat US")
        print("  water rates; the case is chlorine-free soft water,")
        print("  stormwater reduction, and drought resilience.")
    print(f"  note: harvest != used; only USED gallons pay. Sewer credit")
    print(f"  (where meters allow) is often the difference that flips this.")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("catchment", help="roof yield")
    s.add_argument("--area-ft2", type=float, required=True)
    s.add_argument("--rain-in", type=float, required=True)
    s.add_argument("--surface", choices=sorted(RUNOFF), default="asphalt")
    s.add_argument("--first-flush-mm", type=float, default=None)
    s.set_defaults(fn=cmd_catchment)

    s = sub.add_parser("demand", help="irrigation demand")
    s.add_argument("--area-m2", type=float, required=True)
    s.add_argument("--liters-per-m2", type=float, default=18)
    s.add_argument("--weeks", type=int, default=14)
    s.set_defaults(fn=cmd_demand)

    s = sub.add_parser("storage", help="monthly mass-balance simulation")
    s.add_argument("--area-ft2", type=float, required=True)
    s.add_argument("--surface", choices=sorted(RUNOFF), default="asphalt")
    s.add_argument("--monthly-in", required=True,
                   help="comma-separated monthly rainfall inches")
    s.add_argument("--demand-area-m2", type=float, required=True)
    s.add_argument("--lpm2", type=float, default=18)
    s.add_argument("--capacity", type=float, required=True,
                   help="total storage liters")
    s.add_argument("--all-months", action="store_true",
                   help="apply demand every month (greenhouse etc.)")
    s.set_defaults(fn=cmd_storage)

    s = sub.add_parser("payback", help="economics")
    s.add_argument("--harvest-gal", type=float, default=0)
    s.add_argument("--used-gal", type=float, required=True)
    s.add_argument("--cost", type=float, required=True)
    s.add_argument("--water-rate", type=float, default=12.0,
                   help="$ per 1000 gal")
    s.add_argument("--sewer-credit", type=float, default=0.0)
    s.set_defaults(fn=cmd_payback)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
