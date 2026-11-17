#!/usr/bin/env python3
"""Window AC sizer: room load estimate, oversize/short-cycle check, season cost.

Commands:
  size   --length FT --width FT --ceiling FT --sun shaded|average|sunny|west
          --insulation good|average|poor|very-poor [--occupants N] [--kitchen yes]
          [--climate hot|mild] [--btu-list 5000,6000,...]
  check  same flags + --unit-btu N   (is the existing unit oversized?)
  cost   --btu N --ceer N --price $/kWh --hours H --days D
All factors printed so any line can be argued with.
"""
import argparse

BTU_PER_SQFT = 20.0
CEILING_PCT_PER_FT = 0.05
SUN_FACTOR = {"shaded": 0.90, "average": 1.00, "sunny": 1.10, "west": 1.15}
INSULATION_FACTOR = {"good": 0.90, "average": 1.00, "poor": 1.15, "very-poor": 1.25}
CLIMATE_FACTOR = {"mild": 0.90, "average": 1.00, "hot": 1.10}
BTU_PER_EXTRA_OCCUPANT = 600
KITCHEN_ADD = 4000
OVERSIZE_CEILING = 1.15
SHELF_SIZES = [5000, 6000, 8000, 10000, 12000, 15000, 18000, 24000]


def load_stack(a) -> dict:
    area = a.length * a.width
    base = area * BTU_PER_SQFT
    stack = [("base", f"{area:.0f} sqft x {BTU_PER_SQFT:.0f}", base)]
    if a.ceiling != 8.0:
        adj = base * (a.ceiling - 8.0) * CEILING_PCT_PER_FT
        base += adj
        stack.append(("ceiling", f"{a.ceiling} ft (+5%/ft over 8)", adj))
    sun_f = SUN_FACTOR[a.sun]
    stack.append(("sun", f"{a.sun} (x{sun_f:.2f})", base * (sun_f - 1.0)))
    base *= sun_f
    ins_f = INSULATION_FACTOR[a.insulation]
    stack.append(("insulation", f"{a.insulation} (x{ins_f:.2f})",
                  base * (ins_f - 1.0)))
    base *= ins_f
    cli_f = CLIMATE_FACTOR[a.climate]
    stack.append(("climate", f"{a.climate} (x{cli_f:.2f})", base * (cli_f - 1.0)))
    base *= cli_f
    occ_add = max(0, a.occupants - 2) * BTU_PER_EXTRA_OCCUPANT
    if occ_add:
        stack.append(("occupants", f"{a.occupants} people (+600 ea over 2)", occ_add))
    base += occ_add
    if a.kitchen:
        stack.append(("kitchen", "cooking adjacency (+4,000)", KITCHEN_ADD))
        base += KITCHEN_ADD
    return {"area": area, "stack": stack, "load": base}


def nearest_sizes(load: float) -> list:
    return sorted(SHELF_SIZES, key=lambda s: abs(s - load))[:3]


def cmd_size(a) -> None:
    m = load_stack(a)
    print(f"Room: {a.length}x{a.width} ft, {a.ceiling} ft ceiling "
          f"({m['area']:.0f} sqft)")
    for name, why, delta in m["stack"]:
        print(f"  {name:<12} {why:<34} {delta:+9,.0f} BTU/h")
    load = m["load"]
    band_hi = load * OVERSIZE_CEILING
    print(f"\nCALCULATED LOAD: ~{load:,.0f} BTU/h")
    print(f"Recommended band: {load:,.0f} - {band_hi:,.0f} BTU/h")
    n1, n2, n3 = nearest_sizes(load)
    over = n1 / load
    if over <= OVERSIZE_CEILING:
        print(f"Nearest shelf size {n1:,} BTU = {(over-1)*100:+.0f}% vs load -> "
              f"BUY {n1:,} (within +15% doctrine).")
    elif n1 / load <= 1.5:
        print(f"Nearest shelf size {n1:,} BTU = +{(over-1)*100:.0f}% over -> "
              f"acceptable, but prefer an INVERTER model that modulates down "
              f"(dehumidifies at part load); fixed-speed will short-cycle on "
              f"mild days.")
    else:
        print(f"Smallest sane size {n1:,} BTU is +{(over-1)*100:.0f}% over load. "
              f"Options: (a) inverter unit at {n1:,} that turns down, "
              f"(b) accept mild-day clamminess, (c) portable dual-hose SACC-rated "
              f"smaller. Do NOT buy {n2:,}/{n3:,}.")
    print("\nElectrical: <=8k BTU -> 115V outlet; 10-12k often 230V or dedicated "
          "15-20A. Check before ordering.")


def cmd_check(a) -> None:
    m = load_stack(a)
    load = m["load"]
    ratio = a.unit_btu / load
    print(f"Room load: ~{load:,.0f} BTU/h | Unit: {a.unit_btu:,} BTU "
          f"(ratio {ratio:.2f})")
    if ratio > 1.5:
        print("VERDICT: OVERSIZED — classic cold-but-clammy room. Short blasts "
              "cool the air but never condense humidity; compressor short-cycles "
              "(wear + noise). Fix: replace with right-sized/inverter unit, or "
              "add a dehumidifier and run the AC at LOW fan + higher setpoint "
              "for longer runs.")
    elif ratio > OVERSIZE_CEILING:
        print("VERDICT: MILDLY OVERSIZED — acceptable on design days, marginal "
              "on mild ones. Prefer longer runs: raise setpoint 1-2F, use LOW "
              "fan (more latent removal per pass), verify filter is clean.")
    elif ratio >= 0.85:
        print("VERDICT: RIGHT-SIZED — leave it alone. If room feels damp, check "
              "drainage/tilt and fan speed before blaming capacity.")
    else:
        print("VERDICT: UNDERSIZED — runs forever, never cold. Clean filter "
              "first; then sun-control (blinds/west glass film); then re-run "
              "the load math before upsizing.")


def cmd_cost(a) -> None:
    watts = a.btu / a.ceer
    kwh_h = watts / 1000.0
    per_day = kwh_h * a.hours
    season = per_day * a.days
    print(f"{a.btu:,} BTU @ CEER {a.ceer} = {watts:,.0f} W = {kwh_h:.2f} kWh/h")
    print(f"{a.hours} h/day x {a.days} days = {season:,.0f} kWh/season")
    print(f"Cost @ ${a.price:.3f}/kWh: ${per_day*a.price:.2f}/day, "
          f"${season*a.price:,.0f}/season")
    print("Compare: each +1 CEER on a 10k unit saves ~7%/season at same hours.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    def room_args(p):
        p.add_argument("--length", type=float, required=True)
        p.add_argument("--width", type=float, required=True)
        p.add_argument("--ceiling", type=float, default=8.0)
        p.add_argument("--sun", default="average",
                       choices=list(SUN_FACTOR))
        p.add_argument("--insulation", default="average",
                       choices=list(INSULATION_FACTOR))
        p.add_argument("--occupants", type=int, default=2)
        p.add_argument("--kitchen", default="no", choices=["yes", "no"])
        p.add_argument("--climate", default="average",
                       choices=list(CLIMATE_FACTOR))

    p = sub.add_parser("size"); room_args(p); p.set_defaults(func=cmd_size)
    p = sub.add_parser("check"); room_args(p)
    p.add_argument("--unit-btu", type=float, required=True)
    p.set_defaults(func=cmd_check)
    p = sub.add_parser("cost")
    p.add_argument("--btu", type=float, required=True)
    p.add_argument("--ceer", type=float, required=True)
    p.add_argument("--price", type=float, default=0.17)
    p.add_argument("--hours", type=float, default=8.0)
    p.add_argument("--days", type=float, default=120.0)
    p.set_defaults(func=cmd_cost)

    args = ap.parse_args()
    if getattr(args, "kitchen", "no") == "yes":
        args.kitchen = True
    else:
        args.kitchen = False
    args.func(args)


if __name__ == "__main__":
    main()
