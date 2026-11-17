#!/usr/bin/env python3
"""Water Heater Tuner — setpoint verdicts balancing scald, legionella, energy.

Commands:
  profile      household + tank facts (ages, size, fuel, location, setpoint)
  setpoint     verdict: storage temp + delivery strategy + why (constraint-bound)
  energy       savings estimate for a setpoint move + upgrade deltas
  recovery     shower multiplier + consecutive-shower spacing math
  pasteurize   thermal disinfection protocol card (low-setpoint / post-stagnation)
  vacation     away plan + return protocol by duration and fuel

Stdlib only. Store: heater_profile.json next to script (--store overrides).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

DEFAULT_STORE = Path(__file__).resolve().parent / "heater_profile.json"

# Moritz & Henriques burn data (adult), C -> seconds to full-thickness burn
SCALD_TABLE = [(49, 600), (52, 90), (55, 17), (60, 3), (68, 0.5), (82, 0.0)]

# share of home energy used by water heating (DOE/EIA-ish central estimate)
WH_ENERGY_SHARE = 0.16
# standby savings per °C of setpoint reduction (fraction of WH energy)
SAVINGS_PER_C = 0.0075  # ~4% per 5.6°C, mid-range of 3-5%/10F
# recovery power by fuel: kW-equivalent into water
RECOVERY_KW = {"gas": 9.5, "electric": 4.5, "heat-pump": 1.8}
SHOWER_FLOW_LPM = 8.0        # modern showerhead ~8 L/min
SHOWER_MIX_C = 40.0          # comfortable shower temp
SHOWER_MIN = 8               # minutes per shower


def load(store: Path) -> dict:
    if not store.exists():
        sys.exit(f"No profile at {store}. Run `profile` first.")
    return json.loads(store.read_text())


def save(store: Path, d: dict) -> None:
    store.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")


def burn_time(c: float, child: bool) -> str:
    secs = None
    for t_c, t_s in SCALD_TABLE:
        if c <= t_c:
            secs = t_s
            break
    if secs is None:
        return "< 1 s"
    if child:
        secs /= 4
    if secs >= 60:
        return f"~{secs/60:.0f} min"
    return f"~{secs:.0f} s"


def users_from_spec(spec: str):
    """'adult,adult,child2' -> list of (kind, age)"""
    out = []
    for tok in spec.split(","):
        tok = tok.strip().lower()
        if tok.startswith("child"):
            age = int("".join(ch for ch in tok[5:] if ch.isdigit()) or 4)
            out.append(("child", age))
        elif tok.startswith("elder"):
            out.append(("elder", 78))
        elif tok.startswith("immuno"):
            out.append(("immunocompromised", 40))
        else:
            out.append(("adult", 35))
    return out


# ------------------------------------------------------------------ profile
def cmd_profile(args) -> None:
    users = users_from_spec(args.users)
    d = {
        "tank_gal": args.tank_gal, "fuel": args.fuel,
        "location": args.location, "setpoint_f": args.setpoint,
        "users": users, "mixing_valve": args.mixing_valve,
        "bill_monthly": args.bill or None, "profiled": date.today().isoformat(),
    }
    save(args.store, d)
    kinds = ", ".join(f"{k}" + (f"({a})" if k == "child" else "") for k, a in users)
    print(f"Profiled: {args.tank_gal} gal {args.fuel} tank in {args.location}, "
          f"setpoint {args.setpoint}°F, users: {kinds}, "
          f"{'with' if args.mixing_valve else 'NO'} mixing valve.")
    print("Verify actual tap temps before acting: nearest tap (scald), "
          "farthest tap (delivery loss) — 30 s run, thermometer.")


# ------------------------------------------------------------------ verdict
def cmd_setpoint(args) -> None:
    d = load(args.store)
    kinds = {k for k, _ in d["users"]}
    immuno = "immunocompromised" in kinds
    child = any(k == "child" and a < 5 for k, a in d["users"])
    elder = "elder" in kinds
    valve = d["mixing_valve"]

    if immuno or (valve and (child or elder)):
        store_c, deliver_c, why = 60, 49, (
            "immunocompromised resident" if immuno else
            "child/elder present + mixing valve available")
        strategy = (f"STORE at {store_c}°C (140°F) — tank self-sanitizes "
                    f"(legionella dies ~32 min at 60°C)\n"
                    f"DELIVER at {deliver_c}°C via anti-scald mixing valve")
    elif (child or elder) and not valve:
        store_c, deliver_c, why = 49, 49, "child/elder present, NO mixing valve"
        strategy = (f"setpoint {store_c}°C (120°F) → scald time "
                    f"{burn_time(49, child)} for a child\n"
                    f"⚠ storage < 60°C → run the weekly pasteurize protocol")
    elif not valve:
        store_c, deliver_c, why = 58, 55, "adults only, no valve — pragmatic band"
        strategy = (f"setpoint ~{store_c}°C ({round(store_c*9/5+32)}°F): adults-only "
                    f"scald time {burn_time(55, False)} at the tap\n"
                    f"storage near-sanitizing; check tap temp actually ≤ 55°C")
    else:
        store_c, deliver_c, why = 55, 50, "adults only with valve"
        strategy = (f"STORE at {store_c}°C, DELIVER {deliver_c}°C via valve "
                    f"(energy-lean, valve handles safety)")
    print(f"VERDICT — bound by: {why}")
    print(strategy)
    print("\nVerify: nearest tap ≤ "
          f"{deliver_c}°C after 30 s run; farthest tap within 2°C of setpoint.")
    if store_c < 60:
        print("Run `pasteurize` — print the weekly thermal-disinfection card.")


# ------------------------------------------------------------------ energy
def cmd_energy(args) -> None:
    d = load(args.store)
    frm = d["setpoint_f"] or 140
    to = args.to
    drop_c = (frm - to) * 5 / 9
    frac = SAVINGS_PER_C * drop_c
    monthly = d.get("bill_monthly")
    print(f"Setpoint move {frm}°F → {to}°F ({drop_c:.1f}°C):")
    print(f"  water-heating energy saved ≈ {frac*100:.1f}%")
    if monthly:
        wh_month = monthly * WH_ENERGY_SHARE
        print(f"  ≈ ${wh_month*frac:.0f}/mo, ${wh_month*frac*12:.0f}/yr "
              f"(assuming ${monthly}/mo total bill, ~16% to water heat)")
    print("\nAdjacent wins:")
    print("  tank blanket on old electric tank: 5-10%")
    print("  insulate first 2m of hot pipe: 2-4%")
    print("  heat-pump heater (climate-dependent): 50-65% of WH cost")
    print("  annual sediment drain (hard water / gas): efficiency maintenance")
    if (d["location"] in ("garage", "basement")):
        print(f"\nTank in {d['location']} (cold space): savings trend to the HIGH "
              "end; pipe insulation pays fast.")


# ------------------------------------------------------------------ recovery
def cmd_recovery(args) -> None:
    d = load(args.store)
    tank_c = ((d["setpoint_f"] or 140) - 32) * 5 / 9
    inlet = args.inlet_c
    # mixing multiplier: how many liters of shower-temp water the tank yields
    usable_l = d["tank_gal"] * 3.785 * (tank_c - SHOWER_MIX_C) / (SHOWER_MIX_C - inlet)
    per_shower = SHOWER_FLOW_LPM * SHOWER_MIN
    n_now = usable_l / per_shower
    kw = RECOVERY_KW[d["fuel"]]
    # reheat time for one shower's worth of energy at shower temp
    dT = SHOWER_MIX_C - inlet
    t_shower_min = per_shower * dT * 4.186 / 60.0 / (kw * 0.98)
    print(f"Tank {d['tank_gal']} gal at {tank_c:.0f}°C, inlet {inlet}°C, "
          f"shower {SHOWER_MIX_C:.0f}°C:")
    print(f"  usable shower-temp water: {usable_l:.0f} L "
          f"(multiplier {usable_l/(d['tank_gal']*3.785):.1f}× tank)")
    print(f"  back-to-back showers on a full tank: {n_now:.1f}")
    print(f"  recovery ({d['fuel']}): ~{t_shower_min:.0f} min of heating per "
          f"{SHOWER_MIN}-min shower → space showers ~{t_shower_min:.0f} min apart")
    if args.showers and args.showers > n_now:
        deficit = args.showers - n_now
        print(f"  ⚠ {args.showers} requested — deficit {deficit:.0f} showers; "
              f"add ~{deficit*t_shower_min:.0f} min spacing or raise setpoint/size")
    print("\nWinter note: inlet at 9°C vs 20°C shrinks usable volume ~"
          f"{(1-(tank_c-SHOWER_MIX_C)/(SHOWER_MIX_C-9)/((tank_c-SHOWER_MIX_C)/(SHOWER_MIX_C-20)))*100:.0f}%.")


# ------------------------------------------------------------------ protocols
def cmd_pasteurize(args) -> None:
    d = load(args.store)
    print("THERMAL DISINFECTION PROTOCOL (legionella)")
    print("Run weekly if storage < 60°C; also after any stagnation > 1 week.\n")
    print(" 1. Raise setpoint to 60°C+ (140°F+). Wait for recovery "
          f"(gas ~45 min, electric ~2 h for a {d['tank_gal']} gal tank).")
    print(" 2. HOLD ≥ 30 min at temperature (60°C ≈ 32 min for a big kill).")
    print(" 3. Flush EVERY hot outlet 5 min at full hot, hottest tap LAST:")
    print("    kitchen, baths, showers, any rarely-used fixture, hose bibs if hot-plumbed.")
    print(" 4. SCALD WARNING: water now burns in seconds at 60°C "
          f"({burn_time(60, any(k=='child' for k,_ in d['users']))} "
          "for your most vulnerable user). No kids, no elders at fixtures.")
    print(" 5. Restore normal setpoint. Log the date.")
    print("\nImmunocompromised household: do NOT operate storage below 60°C "
          "at all — install a mixing valve instead.")


def cmd_vacation(args) -> None:
    d = load(args.store)
    days = args.days
    print(f"Away {days} days — {d['fuel']} tank:")
    if days <= 7:
        print("  Leave as-is (or vacation mode if present). Savings from going "
              "lower are trivial vs the return flush.")
    elif days <= 28:
        if d["fuel"] == "gas":
            print("  Vacation setting if available; otherwise leave normal "
                  "(pilot-only savings are small).")
        else:
            print("  Switch off at the breaker (electric).")
        print("  Return: restore power, heat to 60°C+, hold 30 min, flush all "
              "hot outlets 5 min.")
    else:
        print("  Off at breaker/pilot. Freeze-risk zone: drain the tank.")
        print("  Return: full pasteurize protocol (see `pasteurize`).")
    print("\nReturn rule of thumb: healthy adults flush 5 min hot before "
          "showering; kids/elders/immunocompromised — full protocol.")


# ------------------------------------------------------------------ cli
def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--store", default=str(DEFAULT_STORE))
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("profile")
    sp.add_argument("--tank-gal", type=float, required=True)
    sp.add_argument("--fuel", choices=["gas", "electric", "heat-pump"], required=True)
    sp.add_argument("--location", default="basement",
                    choices=["basement", "garage", "conditioned", "attic", "closet"])
    sp.add_argument("--setpoint", type=float, default=140, help="current °F")
    sp.add_argument("--users", default="adult",
                    help="comma list: adult, child3 (age), elder, immunocompromised")
    sp.add_argument("--mixing-valve", action="store_true",
                    help="anti-scald / thermostatic mixing valve installed")
    sp.add_argument("--bill", type=float, default=None, help="monthly energy bill for $ math")
    sp.set_defaults(fn=cmd_profile)

    sub.add_parser("setpoint").set_defaults(fn=cmd_setpoint)

    sp = sub.add_parser("energy")
    sp.add_argument("--to", type=float, required=True, help="proposed °F")
    sp.add_argument("--bill", type=float, default=None, help="monthly $ bill for $ math")
    sp.set_defaults(fn=cmd_energy)

    sp = sub.add_parser("recovery")
    sp.add_argument("--showers", type=int, default=None)
    sp.add_argument("--inlet-c", type=float, default=15.0, help="cold inlet °C")
    sp.set_defaults(fn=cmd_recovery)

    sub.add_parser("pasteurize").set_defaults(fn=cmd_pasteurize)

    sp = sub.add_parser("vacation")
    sp.add_argument("--days", type=int, required=True)
    sp.set_defaults(fn=cmd_vacation)

    args = p.parse_args()
    args.store = Path(args.store)
    args.fn(args)


if __name__ == "__main__":
    main()
