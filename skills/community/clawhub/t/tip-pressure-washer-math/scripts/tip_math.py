#!/usr/bin/env python3
"""tip_math.py — pressure-washer nozzle, orifice, dilution and surface-planning math.

Subcommands
-----------
  units    PSI x GPM cleaning-units rating for a machine (or a comparison pair).
  orifice  Nozzle number -> GPM at a given PSI, with pump-feed verification.
  dilute   Mix-tank math for a dilution ratio (e.g. 1:9 into a 5 gal tank).
  plan     Surface type -> PSI band, tip size, standoff distance, pre-treat.

Stdlib only. Exit codes: 0 = success, 2 = bad input / usage error.
"""

import argparse
import math
import sys

EXIT_OK = 0
EXIT_ERR = 2

# Industry convention: a nozzle's size number equals its flow in GPM at 4000 PSI.
REF_PSI = 4000.0

ORIFICE_SIZES = [2.0 + 0.5 * i for i in range(13)]  # 2.0 .. 8.0 step 0.5

TABLE_PSIS = [1000, 2000, 2500, 3000, 3500, 4000]

# (surface, psi_min, psi_max, tip_deg, dist_in, dist_cm, pre_treat, dwell, notes)
SURFACES = {
    "concrete": {
        "band": (2500, 4000),
        "tip": "25-40 deg fan; turbo/rotary for stubborn stains",
        "distance": "4-8 in (10-20 cm) for stains; 12 in (30 cm) for rinse passes",
        "pre_treat": "Alkaline degreaser or concrete cleaner, 1:5 to 1:10, dwell 5-10 min",
        "notes": "Untreated concrete tolerates high PSI; avoid etching lines by keeping "
                 "the fan consistent and never running a 0-deg tip on it.",
    },
    "wood": {
        "band": (500, 1500),
        "tip": "40-45 deg fan, wide pattern",
        "distance": "12-18 in (30-45 cm), constant sweep",
        "pre_treat": "Sodium percarbonate (deck cleaner) 1:4 to 1:8, dwell 10-15 min",
        "notes": "Softwoods (pine, cedar) live at the low end; 1500+ PSI furs and gouges "
                 "grain. Let the chemical do the work, not the pressure.",
    },
    "vinyl": {
        "band": (1300, 1800),
        "tip": "25-40 deg fan",
        "distance": "12-18 in (30-45 cm), spray with the overlap, never uphill into laps",
        "pre_treat": "House-wash surfactant (soft-wash style) 1:9 to 1:15, dwell 5-10 min",
        "notes": "Soft washing is the goal: low PSI, longer dwell, rinse top-down. "
                 "High PSI drives water behind the siding.",
    },
    "car": {
        "band": (1000, 1900),
        "tip": "40 deg fan or foam cannon",
        "distance": "12-24 in (30-60 cm), never closer than a hand-width",
        "pre_treat": "Snow foam / pH-neutral shampoo 1:9 to 1:20 via foam cannon",
        "notes": "Never use a 0/15-deg tip. PSI over ~1900 risks clear-cout damage and "
                 "stripping wax; foam + contact wash beats blast.",
    },
}

TURBO_FACTOR = 1.25  # rotary/turbo nozzle concentrates impact; derate ceilings 20-25%
OVERFLOW_FACTOR = 1.05  # orifice flow more than 5% over rated flow = warning


def pos_float(value, label):
    try:
        f = float(value)
    except (TypeError, ValueError):
        raise SystemExit(
            _err(f"{label} must be a number, got {value!r}"))
    if not math.isfinite(f) or f <= 0:
        raise SystemExit(
            _err(f"{label} must be a positive finite number, got {value!r}"))
    return f


def _err(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    return EXIT_ERR


def die(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(EXIT_ERR)


# ---------------------------------------------------------------- orifice math

def flow_at(size, psi):
    """GPM through a given orifice size at PSI (size = GPM @ 4000 PSI)."""
    return size * math.sqrt(psi / REF_PSI)


def size_for(gpm, psi):
    """Nozzle size number that passes GPM at PSI."""
    return gpm * math.sqrt(REF_PSI / psi)


def nearest_size(exact):
    """Snap an exact size to the nearest half-point in the 2.0-8.0 table."""
    snapped = round(exact * 2) / 2.0
    return min(max(snapped, ORIFICE_SIZES[0]), ORIFICE_SIZES[-1])


# ------------------------------------------------------------------ formatting

def g(x, nd=2):
    """Trim trailing zeros: 3.50 -> '3.5', 2.60 -> '2.6'."""
    return f"{x:.{nd}f}".rstrip("0").rstrip(".")


def header(title):
    print("=" * 62)
    print(f"  {title}")
    print("=" * 62)


# ------------------------------------------------------------------- subcommands

def cmd_units(args):
    psi = pos_float(args.psi, "--psi")
    gpm = pos_float(args.gpm, "--gpm")
    cu = psi * gpm
    if cu < 5000:
        cls = "light-duty (electric handhelds)"
    elif cu < 8000:
        cls = "residential gas / pro-electric"
    elif cu < 16000:
        cls = "professional"
    else:
        cls = "heavy-duty / skid rig"

    header(f"CLEANING UNITS: {g(psi, 0)} PSI x {g(gpm)} GPM")
    print(f"  Cleaning units (CU) = PSI x GPM = {cu:,.0f}")
    print(f"  Class: {cls}")
    print(f"  Rule of thumb: 1 GPM cuts rinse time more than 1000 extra PSI;")
    print(f"  flow is time, pressure is impact.")

    if args.compare:
        cpsi_s, cgpm_s = args.compare
        cpsi = pos_float(cpsi_s, "compare psi")
        cgpm = pos_float(cgpm_s, "compare gpm")
        ccu = cpsi * cgpm
        pct = (cu - ccu) / ccu * 100.0
        header(f"VS {g(cpsi, 0)} PSI x {g(cgpm)} GPM")
        print(f"  Machine A CU: {cu:,.0f}   Machine B CU: {ccu:,.0f}")
        print(f"  A is {abs(pct):.1f}% {'more' if pct >= 0 else 'less'} capable overall")
    return EXIT_OK


def print_orifice_table():
    hdr = "| Size | " + " | ".join(f"{p:>5}" for p in TABLE_PSIS) + " |"
    print(hdr)
    print("|" + "-" * (len(hdr) - 2) + "|")
    for s in ORIFICE_SIZES:
        cells = " | ".join(f"{flow_at(s, p):5.2f}" for p in TABLE_PSIS)
        print(f"| {s:>4.1f} | {cells} |")
    print("\n  (size number = GPM at 4000 PSI; flow scales with sqrt(psi/4000))")


def cmd_orifice(args):
    if args.list:
        print_orifice_table()
        return EXIT_OK

    if args.size is None or args.psi is None:
        die("orifice requires --size and --psi (or --list for the table)")

    size = pos_float(args.size, "--size")
    psi = pos_float(args.psi, "--psi")
    if not 0.5 <= size <= 10.0:
        die("--size outside the common nozzle range 0.5-10")

    flow = flow_at(size, psi)
    eff_psi = psi

    header(f"ORIFICE {g(size)} AT {g(psi, 0)} PSI")
    print(f"  Flow: {flow:.2f} GPM at {psi:.0f} PSI")
    rec_gpm = flow_at(nearest_size(size), psi)
    print(f"  Nearest catalog size {g(nearest_size(size))} -> {rec_gpm:.2f} GPM here")
    print(f"  Cleaning units at nozzle: {psi * flow:,.0f} CU")

    if args.rated_gpm:
        rated = pos_float(args.rated_gpm, "--rated-gpm")
        ratio = flow / rated
        print(f"  Pump rated flow: {rated:.2f} GPM  (demand ratio {ratio:.2f}x)")
        if flow > OVERFLOW_FACTOR * rated:
            print()
            print("  WARNING: orifice demand exceeds pump capability!")
            print(f"  This tip wants {flow:.2f} GPM but the pump is rated {rated:.2f} GPM")
            print(f"  ({ratio:.2f}x rated, threshold {OVERFLOW_FACTOR}x). The pump will")
            print(f"  dead-head, pressure will sag below {psi:.0f} PSI, and the unloader")
            print(f"  will cycle (chatter). Fit a smaller tip: try size "
                  f"{g(nearest_size(size_for(rated, psi)))} for {rated:.2f} GPM at "
                  f"{psi:.0f} PSI.")
        elif ratio < 0.9:
            print(f"  OK: pump easily feeds this tip ({ratio:.2f}x rated).")
            print(f"  Note: tip is small for this pump; expect higher than {psi:.0f} PSI")
            print(f"  at the gun unless the unloader regulates. Size for full flow:"
                  f" {g(size_for(rated, psi))}")
        else:
            print(f"  OK: pump can feed this tip ({ratio:.2f}x rated, within tolerance).")

    if args.turbo:
        print(f"  Turbo/rotary: effective impact ~{eff_psi * TURBO_FACTOR:.0f} PSI-equiv;")
        print(f"  derate surface PSI ceilings by 20-25% when using a turbo nozzle.")
    return EXIT_OK


def cmd_dilute(args):
    try:
        chem_s, water_s = (args.ratio or "").split(":")
        chem = float(chem_s)
        water = float(water_s)
    except (ValueError, AttributeError):
        raise SystemExit(
            _err(f"--ratio must look like 1:9 (chemical:water), got {args.ratio!r}"))
    if chem <= 0 or water < 0:
        die("ratio parts must be positive")
    tank = pos_float(args.tank_gal, "--tank-gal")

    parts = chem + water
    chem_gal = tank * chem / parts
    water_gal = tank * water / parts
    strength = 1.0 / parts  # fraction of concentrate in final mix

    header(f"DILUTION {g(chem)}:{g(water)} INTO {g(tank)} GAL")
    print(f"  Chemical (concentrate): {chem_gal:.3f} gal  "
          f"({chem_gal * 128:.1f} fl oz, {chem_gal * 3785:.0f} ml)")
    print(f"  Water:                  {water_gal:.3f} gal  "
          f"({water_gal * 128:.1f} fl oz)")
    print(f"  Total mix:              {chem_gal + water_gal:.3f} gal")
    print(f"  Final strength: {strength * 100:.1f}% concentrate "
          f"(1 part concentrate : {parts:.10g} parts mix)")
    if args.upstream:
        print("  NOTE: upstream (before-pump) injection - chemical must be rated")
        print("  safe for pump seals/valves; flush with clean water after use.")
    else:
        print("  Assumes downstream injection (10:1 typical draw at the injector).")
    if strength > 0.2:
        print("  CAUTION: mix is >20% concentrate - verify against the product label.")
    return EXIT_OK


def cmd_plan(args):
    surface_raw = args.surface or ""
    surface = surface_raw.lower().strip()
    aliases = {"driveway": "concrete", "patio": "concrete", "deck": "wood",
               "fence": "wood", "siding": "vinyl", "house": "vinyl",
               "auto": "car", "vehicle": "car", "truck": "car"}
    surface = aliases.get(surface, surface)
    if surface not in SURFACES:
        raise SystemExit(
            _err(f"unknown surface {surface_raw!r}; choose from: "
                 + ", ".join(sorted(SURFACES))))
    spec = SURFACES[surface]
    lo, hi = spec["band"]

    machine_psi = pos_float(args.psi, "--psi") if args.psi else None
    machine_gpm = pos_float(args.gpm, "--gpm") if args.gpm else None
    turbo = args.turbo

    header(f"PLAN: {surface.upper()}  (PSI band {lo}-{hi})")
    print(f"  Tip:       {spec['tip']}")
    print(f"  Distance:  {spec['distance']}")
    print(f"  Pre-treat: {spec['pre_treat']}")
    print(f"  Notes:     {spec['notes']}")

    if machine_psi:
        eff = machine_psi * (TURBO_FACTOR if turbo else 1.0)
        label = f" (turbo-derated: {eff:.0f} effective)" if turbo else ""
        print()
        print(f"  Machine: {machine_psi:.0f} PSI{label} vs ceiling {hi} PSI")
        if eff > hi:
            print(f"  WARNING: effective PSI {eff:.0f} EXCEEDS the {surface} ceiling "
                  f"of {hi} PSI.")
            print(f"  Back off to {hi / (TURBO_FACTOR if turbo else 1.0):.0f} PSI"
                  f"{' machine PSI with turbo' if turbo else ''}, widen standoff to "
                  f"18+ in, or switch to a wider fan tip.")
        elif eff < lo and not turbo:
            print(f"  Below the {lo} PSI floor: rely on dwell time and pre-treat;")
            print(f"  cleaning will be slower but safe.")
        else:
            print(f"  OK: within the safe band for {surface}.")

    if machine_gpm and machine_psi:
        exact = size_for(machine_gpm, machine_psi)
        fit = nearest_size(exact)
        print(f"  Correct tip for {machine_gpm:.2f} GPM @ {machine_psi:.0f} PSI: "
              f"size {g(fit)} (exact {exact:.2f})")
        print(f"  That tip flows {flow_at(fit, machine_psi):.2f} GPM here.")
        print(f"  Cleaning units: {machine_psi * machine_gpm:,.0f} CU")
    elif machine_gpm:
        exact = size_for(machine_gpm, 3000)
        print(f"  Tip near size {g(nearest_size(exact))} (sized at a 3000 PSI reference)")
    return EXIT_OK


# ------------------------------------------------------------------------ main

def build_parser():
    p = argparse.ArgumentParser(
        prog="tip_math.py",
        description="Pressure-washer tip / orifice / dilution / surface math.")
    sub = p.add_subparsers(dest="cmd", required=True)

    u = sub.add_parser("units", help="PSI x GPM cleaning units")
    u.add_argument("--psi", required=True)
    u.add_argument("--gpm", required=True)
    u.add_argument("--compare", nargs=2, metavar=("PSI", "GPM"),
                   help="second machine to compare against")
    u.set_defaults(func=cmd_units)

    o = sub.add_parser("orifice", help="nozzle size -> GPM at PSI + pump check")
    o.add_argument("--size", help="nozzle size number, e.g. 4.0 (=GPM @ 4000 PSI)")
    o.add_argument("--psi", help="operating pressure")
    o.add_argument("--rated-gpm", help="pump rated flow, enables feed check")
    o.add_argument("--turbo", action="store_true",
                   help="show turbo/rotary derating note")
    o.add_argument("--list", action="store_true", help="print the orifice table")
    o.set_defaults(func=cmd_orifice)

    d = sub.add_parser("dilute", help="mix-tank math for a dilution ratio")
    d.add_argument("--ratio", required=True, help="chemical:water, e.g. 1:9")
    d.add_argument("--tank-gal", required=True, help="final mix volume in gallons")
    d.add_argument("--upstream", action="store_true",
                   help="chemical injected before the pump")
    d.set_defaults(func=cmd_dilute)

    pl = sub.add_parser("plan", help="surface type -> safe operating plan")
    pl.add_argument("surface", help="concrete | wood | vinyl | car")
    pl.add_argument("--psi", help="your machine's rated PSI")
    pl.add_argument("--gpm", help="your machine's rated GPM")
    pl.add_argument("--turbo", action="store_true",
                    help="apply 25% turbo-nozzle effective-PSI derate")
    pl.set_defaults(func=cmd_plan)
    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
