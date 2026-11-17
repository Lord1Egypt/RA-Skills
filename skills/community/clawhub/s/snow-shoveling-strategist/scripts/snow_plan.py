#!/usr/bin/env python3
"""Snow shoveling strategist — load math, tool/placement plan, pacing, ice-melt.

Subcommands:
  plan  Area x depth x density -> tonnage, tool verdict, layer timing,
        placement plan, order of operations
  pace  Age/fitness/risk -> work/rest cycles + cardiac red flags
  salt  Pavement temp + surface -> melter choice, rate, warnings

Stdlib only. Offline. This is effort planning, not medical advice —
chest pain means stop and call emergency services.
"""
import argparse
import json
from datetime import datetime

SNOW = {
    "powder": (75, "falls apart when squeezed, squeaks underfoot"),
    "average": (150, "packs loosely, common storm snow"),
    "wet": (350, "packs into a ball, heavy, near 0C"),
    "ice-crust": (250, "snow over / mixed with frozen crust"),
}

DENSITY_NOTE = "kg/m3 (water equivalent: 1 cm rain ~ 10 cm powder)"


def parse_hhmm(s):
    return datetime.strptime(s, "%H:%M")


def cmd_plan(a):
    w, h = [float(x) for x in a.area.lower().split("x")]
    area_m2 = w * h
    dens, snote = SNOW[a.snow]
    volume_m3 = area_m2 * (a.depth / 100.0)
    total_kg = volume_m3 * dens
    shovel_load_l = 5.0  # typical heaping shovel
    load_kg = shovel_load_l / 1000 * dens
    full_loads = total_kg / load_kg

    # tool verdict
    if a.depth < 8 and a.snow in ("powder", "average"):
        tool = "PUSHER/scoop only — push, don't lift"
        layers = 1
    elif a.depth <= 15:
        tool = "24-28in shovel: push to a stack line, then throw"
        layers = 1
    else:
        tool = (f"DEPTH {a.depth}cm: shovel in LAYERS — skim {10 if a.snow == 'wet' else 15}cm "
                "passes (or snowblower). Full-depth lifts of heavy snow are the back/heart killer.")
        layers = -(-a.depth // (10 if a.snow == "wet" else 15))

    # timing: single pass vs layered clears
    try:
        ends = parse_hhmm(a.ends)
        now = parse_hhmm(a.now)
        hours_left = (ends - now).total_seconds() / 3600.0
        if hours_left < 0:
            hours_left += 24
    except (TypeError, ValueError):
        hours_left = None
    timing = []
    if hours_left is not None and a.depth >= 15:
        if hours_left >= 1.5:
            timing.append(f"Storm ends in {hours_left:.1f}h and {a.depth}cm is deep: "
                          "clear NOW at current depth, again at the end — two light clears "
                          "beat one 5-tonne clear.")
        else:
            timing.append(f"Only {hours_left:.1f}h to storm end: wait it out, clear once "
                          f"(in {layers} layers).")
    elif hours_left is not None:
        timing.append(f"{hours_left:.1f}h to storm end, {a.depth}cm: one clear after it ends is fine.")

    per_layer_tonnes = total_kg / layers / 1000

    return {
        "load": {
            "area_m2": area_m2,
            "snow": f"{a.snow} ({snote}), density {dens} {DENSITY_NOTE}",
            "total_kg": round(total_kg),
            "total_tonnes": round(total_kg / 1000, 1),
            "shovel_loads_equivalent": round(full_loads),
            "kg_per_5L_shovel_load": round(load_kg, 1),
        },
        "tool": tool,
        "layers": layers,
        "per_clearing_pass_tonnes": round(per_layer_tonnes, 2),
        "timing": timing or [f"{a.depth}cm: clear when convenient; layers={layers}"],
        "placement": [
            "Stack line: pick the DOWNWIND long edge; push everything there first.",
            "Throw past the stack line's far edge — snow landing short = re-handled snow.",
            "Never throw onto: the path you'll clear next, the car, the mailbox approach, "
            "drainage paths (melt needs somewhere to go).",
            "Leave 30+ cm of snow storage width along edges: tomorrow's storm adds to it.",
            "Driveway apron (city plow ridge) LAST — the plow comes after you clear.",
        ],
        "order_of_operations": [
            "1. Exit path first (door -> car -> street) so life works mid-job.",
            "2. Main surface in layers/pushes toward the stack line.",
            "3. Car: clear roof BEFORE pulling it into the cleared zone (roof snow "
            "onto cleared pavement = re-work + hazard for others).",
            "4. Apron/plow ridge last, layered — it's the densest wet snow of the day.",
            "5. Ice-melt the surface AFTER clearing (see salt) — salt through 20cm of "
            "snow does nothing but pollute the melt.",
        ],
    }


def cmd_pace(a):
    max_hr = 208 - 0.7 * a.age  # Tanaka formula
    effort_cap = {"low": 0.5, "moderate": 0.65, "high": 0.75}[a.fitness]
    if a.risk_factors >= 1:
        effort_cap = min(effort_cap, 0.55)
    target_hr = max_hr * effort_cap
    work_min, rest_min = (3, 2) if effort_cap >= 0.6 else (2, 2)

    out = {
        "age": a.age,
        "estimated_max_hr": round(max_hr),
        "effort_cap_pct_mhr": f"{effort_cap:.0%}",
        "target_hr_during_work": round(target_hr),
        "cycle": f"{work_min} min work / {rest_min} min rest — timer on, every cycle",
        "talk_test": "You should be able to speak a full sentence while working. If not, you're over cap.",
    }
    risk = []
    if a.age >= 45:
        risk.append("45+: cold-air shoveling is a documented cardiac trigger — the cap above is real, not cautionary.")
    if a.risk_factors >= 1:
        risk.append(f"{a.risk_factors} cardiac risk factor(s): cap tightened to 55% MHR; consider a snowblower, "
                    "a neighborhood teen, or waiting for the city.")
    if a.alone:
        risk.append("Alone: phone IN POCKET (not inside), location shared, check-in time set with someone.")
    risk.append("Warm up 5 min indoors (march, arm swings); dress in layers; scarf over mouth warms intake air; "
                "no big meal or coffee immediately before.")
    out["risk_notes"] = risk
    out["stop_now_call_emergency"] = [
        "chest pressure, tightness, or pain — even mild, even 'probably nothing'",
        "pain spreading to jaw, neck, shoulder, or left arm",
        "unusual shortness of breath / can't finish a sentence",
        "light-headedness, cold sweat, nausea",
        "skipping/racing palpitations that don't settle in 30s of rest",
        "women + diabetics: sudden extreme fatigue, back pain, 'feeling off' count too",
    ]
    out["back_rules"] = [
        "hands 30-45cm apart on the shaft; load close to your body",
        "lift with legs/hips, back neutral — never bend + twist under load",
        "walk the snow to the stack; don't throw it if you can push or carry it",
        "wet snow: HALF-fill the shovel (the math above says a full load is 2 kg)",
    ]
    return out


MELTERS = {
    "rock-salt": {"min_temp": -9, "rate_g_m2": 30, "note": "NaCl: cheap, works to -9C pavement"},
    "calcium-chloride": {"min_temp": -25, "rate_g_m2": 25, "note": "CaCl2: exothermic, fastest, works to -25C; can irritate paws"},
    "magnesium-chloride": {"min_temp": -15, "rate_g_m2": 25, "note": "MgCl2: gentler on concrete/pets, to -15C"},
    "calcium-magnesium-acetate": {"min_temp": -5, "rate_g_m2": 30, "note": "CMA: kindest to concrete/environment, weak in deep cold"},
    "sand": {"min_temp": -99, "rate_g_m2": 100, "note": "traction only, no melting — the answer below -25C or on questionable surfaces"},
}


def cmd_salt(a):
    t = a.pavement_temp
    surf = a.surface
    ok = {k: v for k, v in MELTERS.items() if t >= v["min_temp"]}
    if not ok:
        choice = "sand"
        why = f"Pavement {t}C is below every melter's working range — traction only."
    else:
        # surface-driven choice among those that work
        if surf == "new-concrete":
            choice = "magnesium-chloride" if "magnesium-chloride" in ok else "sand"
            why = ("Concrete <1yr: chlorides (esp. rock salt) attack the curing surface "
                   "and cause spalling; MgCl2 at low rate is the compromise, sand is safest.")
        elif surf == "brick" or surf == "flagstone":
            choice = "calcium-magnesium-acetate" if "calcium-magnesium-acetate" in ok else "sand"
            why = "Mortared/soft stone: freeze-thaw + chloride pushes mortar apart; CMA or sand."
        elif a.pets:
            choice = "magnesium-chloride" if "magnesium-chloride" in ok else "sand"
            why = "Pets: MgCl2 labeled pet-safer; CaCl2 burns paws; wipe paws after walks regardless."
        else:
            choice = "calcium-chloride" if t < -9 else "rock-salt"
            why = f"Pavement {t}C: {choice} works to {MELTERS[choice]['min_temp']}C at the lowest cost-per-melt."
    m = MELTERS[choice]
    rate = m["rate_g_m2"]
    out = {
        "pavement_temp_c": t,
        "surface": surf,
        "melter_choice": choice,
        "why": why,
        "properties": m,
        "application_rate": f"{rate} g/m2 (~1 cup per 10 m2). More is NOT faster — it's "
                            "burnt lawns, tracked-in residue, and pitted concrete.",
        "strategy": [
            "Clear bulk snow FIRST; melters are for the bonded layer/thin events, not 20cm dumps.",
            "Pre-treat (thin frost/glaze events only): apply before the event, prevent the bond.",
            "Post-storm: apply to the cleared surface; melt needs sun/traffic assist below -10C.",
            "Black ice on slopes: treat and re-route walking, don't trust the melt.",
        ],
        "never": [
            "New concrete <1 year: no chlorides (spalling)",
            "Brick/flagstone mortar joints: no rock salt (freeze-thaw burst)",
            "Aluminum surfaces: chlorides corrode",
            "Any melter into storm drains 'to help' — it doesn't",
        ],
    }
    if a.pets:
        out["pet_notes"] = "Wipe paws after walks; keep antifreeze FAR away (sweet, deadly). " \
                           "Store melters sealed and dry."
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("plan")
    sp.add_argument("--area", required=True, help="WxH meters, e.g. 6x9")
    sp.add_argument("--depth", type=float, required=True, help="cm")
    sp.add_argument("--snow", default="average", choices=sorted(SNOW))
    sp.add_argument("--ends", help="storm end HH:MM")
    sp.add_argument("--now", help="current time HH:MM")
    sp.set_defaults(fn=cmd_plan)

    sp = sub.add_parser("pace")
    sp.add_argument("--age", type=int, required=True)
    sp.add_argument("--fitness", default="moderate", choices=["low", "moderate", "high"])
    sp.add_argument("--risk-factors", type=int, default=0,
                    help="smoking, hypertension, diabetes, high cholesterol, family history, sedentary")
    sp.add_argument("--alone", action="store_true")
    sp.set_defaults(fn=cmd_pace)

    sp = sub.add_parser("salt")
    sp.add_argument("--pavement-temp", type=float, required=True, help="C — pavement, not air")
    sp.add_argument("--surface", default="asphalt", choices=["asphalt", "concrete-3yr", "new-concrete", "brick", "flagstone"])
    sp.add_argument("--pets", action="store_true")
    sp.set_defaults(fn=cmd_salt)

    args = ap.parse_args()
    print(json.dumps(args.fn(args), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
