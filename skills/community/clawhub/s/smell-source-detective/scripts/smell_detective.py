#!/usr/bin/env python3
"""Smell Source Detective — rank probable sources of a household smell.

Stdlib only. Offline. Data lives in SMELL_DB below.

Commands:
  diagnose --smell TYPE [--location LOC] [--timing T]   ranked hypotheses
  danger   --smell TYPE                                 act-now screening
  localize --hypothesis "..."                           no-tools protocol
  kill     --source "..."                               elimination protocol
  log      --note "..." | --stats                       episode log
"""
import argparse
import json
import pathlib
import sys

LOG_PATH = pathlib.Path(__file__).resolve().parent.parent / "smell-log.json"

# --- Knowledge base -------------------------------------------------------
# base = general base rate; locations = affinity set; timings = trigger tags
HYPOTHESES = {
    "dry p-trap": dict(
        base=0.60, locations={"bathroom", "basement", "kitchen", "laundry", "garage", "whole-house"},
        timings={"mornings", "after-vacation", "seasonal", "constant"},
        smells={"sewage", "rotten eggs"},
        check="Pour 2 L water into every drain unused >2 weeks (floor drain, guest bath). "
              "Re-sniff in 10 min. Smell fades = trap was dry.",
        fix="Refill trap; add 1 tbsp mineral oil on top of the water to slow evaporation. "
            "Check floor drains monthly in heating season.",
    ),
    "garbage disposal film": dict(
        base=0.55, locations={"kitchen"},
        timings={"constant", "mornings", "when-appliance-runs"},
        smells={"sour", "rotten meat", "sewage"},
        check="Ice + citrus flush, then lift the rubber splash guard and smell its underside.",
        fix="Scrape with ice/citrus; baking-soda+vinegar foam 15 min; wash splash guard. "
            "Enzymatic cleaner weekly if recurring.",
    ),
    "dirty hvac filter": dict(
        base=0.50, locations={"whole-house", "hallway", "bedroom"},
        timings={"when-furnace-runs", "seasonal", "constant"},
        smells={"dusty", "wet dog", "burnt"},
        check="Check the filter date sticker; hold it to the light — no light passing = overdue.",
        fix="Replace filter; mark the date. If smell persists after replace, inspect blower/ducts.",
    ),
    "pet urine in pad": dict(
        base=0.45, locations={"bedroom", "hallway", "living-room", "whole-house"},
        timings={"constant", "worse-when-hot", "after-rain"},
        smells={"urine", "ammonia"},
        check="Blacklight at night — dried salts fluoresce. Focus on carpet edges and near doors.",
        fix="Enzymatic cleaner SATURATED (not misted), covered 12-24 h to stay wet, then extracted. "
            "Repeat failures: seal subfloor with shellac-based blocker.",
    ),
    "dead animal in wall": dict(
        base=0.30, locations={"whole-house", "hallway", "bedroom", "kitchen", "basement", "garage"},
        timings={"sudden-onset"},
        smells={"rotten meat"},
        check="Sudden onset, no household change; flies at one wall/box after day 4; "
              "smell peaks day 3-5, declines by day 10-14.",
        fix="Activated-carbon gel in room; seal electrical-box holes connecting rooms to the void; "
            "ventilate. Wait the desiccation clock — wall cutting is last resort (see reference).",
    ),
    "toilet wax ring failure": dict(
        base=0.25, locations={"bathroom"},
        timings={"constant", "mornings", "when-appliance-runs"},
        smells={"sewage", "rotten eggs"},
        check="Rock the toilet gently (play = ring gone); sniff at base while flushing.",
        fix="Pull and reset toilet with new wax ring (~$5 + 1 h DIY).",
    ),
    "mold cavity": dict(
        base=0.25, locations={"bedroom", "bathroom", "basement", "whole-house", "hallway"},
        timings={"after-rain", "seasonal", "constant", "worse-when-hot"},
        smells={"musty"},
        check="Sniff at outlet/switch boxes on the suspect wall (cavities connect). Look for "
              "moisture staining; moisture meter if available.",
        fix="Find and stop the moisture first. <=1 m2 hard surface: detergent wash + 48 h dry. "
            "Bigger / inside wall / HVAC / recurring: professional remediation.",
    ),
    "electrical overheating": dict(
        base=0.06, locations={"kitchen", "hallway", "whole-house", "bedroom", "garage", "bathroom"},
        timings={"constant", "sudden-onset", "when-appliance-runs"},
        smells={"fish"},
        check="STRONGER AT a fixture, lamp, dimmer, or breaker panel?",
        fix="DANGER path: unplug/switch off if safely reachable; panel off if hardwired; "
            "electrician before reuse. Fish smell = overheated wire insulation.",
    ),
    "sewer vent blockage": dict(
        base=0.10, locations={"bathroom", "whole-house"},
        timings={"mornings", "when-appliance-runs", "after-rain"},
        smells={"sewage", "rotten eggs"},
        check="Gurgling when other fixtures drain; smell strongest in the top-floor bath "
              "(vent runs up from there); check roof vent for leaves/nest.",
        fix="Clear the roof vent by hand/hose. Recurring: vent re-route or AAV (check local code).",
    ),
    "natural gas fitting": dict(
        base=0.05, locations={"kitchen", "basement", "garage", "whole-house"},
        timings={"constant", "mornings"},
        smells={"gas", "rotten eggs", "skunk"},
        check="Do NOT test fittings. If you smell gas additive strongly indoors: leave.",
        fix="DANGER path: no switches, no phone indoors, open windows on the way out, "
            "call the gas emergency line from OUTSIDE.",
    ),
    "cfl or led driver failing": dict(
        base=0.08, locations={"kitchen", "hallway", "bedroom", "bathroom", "garage"},
        timings={"constant", "when-appliance-runs"},
        smells={"fish", "burnt"},
        check="Swap the nearest CFL/bulb out for a day — smell follows the bulb?",
        fix="Replace the bulb/driver. If not the bulb, treat as electrical (danger path).",
    ),
    "refrigerator drip pan": dict(
        base=0.12, locations={"kitchen"},
        timings={"constant", "worse-when-hot"},
        smells={"sour", "rotten meat", "wet dog"},
        check="Pull the base grille; slide out the drip pan (behind/beneath).",
        fix="Wash pan with baking soda solution; check the defrost drain tube for blockage.",
    ),
    "washer gasket biofilm": dict(
        base=0.15, locations={"laundry", "kitchen", "garage"},
        timings={"constant", "when-appliance-runs", "worse-when-hot"},
        smells={"musty", "wet dog", "sour"},
        check="Pull back the door gasket fold; sniff inside the drum seal and detergent drawer.",
        fix="Gasket scrub + washer-cleaner hot cycle; leave door ajar; monthly maintenance cycle.",
    ),
    "stored product off-gassing": dict(
        base=0.12, locations={"garage", "basement", "hallway", "whole-house"},
        timings={"constant", "worse-when-hot", "sudden-onset"},
        smells={"paint", "sweet", "chemical"},
        check="Shelf audit: paint/solvent cans, cleaning jugs — lid failure? Adjacent-unit "
              "renovation (smell through shared wall)?",
        fix="Relid/seal, ventilate, dispose via hazmat channel when done. Off-gassing furniture: "
            "heat + ventilate cycles.",
    ),
    "antifreeze or hvac leak": dict(
        base=0.05, locations={"basement", "garage", "hallway", "whole-house"},
        timings={"when-furnace-runs", "constant", "sudden-onset"},
        smells={"sweet", "chemical"},
        check="Colored wetness/powder residue near furnace, radiators, or car in garage?",
        fix="HVAC tech (refrigerant/coil) or car service. Sweet smell + pets: act fast — "
            "ethylene glycol is attractive and lethal to animals.",
    ),
    "trash or bin residue": dict(
        base=0.35, locations={"kitchen", "garage", "hallway"},
        timings={"mornings", "worse-when-hot", "constant"},
        smells={"rotten meat", "sour"},
        check="Bin out, liner replaced, under-bin floor wiped — smell gone in 24 h?",
        fix="Wash bin with detergent + baking soda; dry fully before new liner.",
    ),
}

DANGER = {
    "gas": (
        "GAS — ACT NOW (rotten-egg additive)\n"
        "  1. Do NOT flip switches, use the phone indoors, or light anything.\n"
        "  2. Open windows/doors on your way out.\n"
        "  3. Call the gas emergency line FROM OUTSIDE (US 811-local line or 911;\n"
        "     EU 112; UK 0800 111 999 National Gas Emergency).\n"
        "  4. Stay out until cleared. Never sniff-test fittings."
    ),
    "fish": (
        "FISH SMELL = overheating plastic/electrical (amines from wire insulation).\n"
        "  Recognized precursor to electrical fires. Not a food smell until proven.\n"
        "  1. Identify nearest fixture/lamp/dimmer/breaker — is it stronger there?\n"
        "  2. Unplug suspect device if safely reachable; hardwired → off at panel.\n"
        "  3. Electrician before reuse. Do not 'keep an eye on it'."
    ),
    "sewage": (
        "SEWAGE — danger only if WATER is also appearing at the lowest fixture.\n"
        "  Odor alone → run diagnose (dry trap etc.). Odor + water backing up:\n"
        "  1. Stop running water; every gallon returns.\n"
        "  2. Check cleanout: standing water = downstream blockage.\n"
        "  3. Plumber now; street-side main = city responsibility (often free)."
    ),
    "burnt": (
        "BURNT/SMOKE — find a source within minutes or treat as fire risk.\n"
        "  1. HVAC running? Filter/duct dust burns off first heat of season (harmless,\n"
        "     once). Persistent when blower runs = motor — service.\n"
        "  2. Trapped plastic on a hot element (dryer/toaster/baseboard)? Kill power, cool.\n"
        "  3. Unexplained + lingering: treat as electrical, panel-off, electrician."
    ),
    "rotten meat": (
        "DEAD ANIMAL — usually a 1-2 week nuisance, not an emergency.\n"
        "  Urgent ONLY for: large animal in chimney/crawl (liquids, flies day 4-8),\n"
        "  smell near sleeping areas of infant/ill person, or liquids staining a wall.\n"
        "  Otherwise: carbon gel, seal box holes, ventilate, wait the clock (see kill)."
    ),
}

# --- Scoring ---------------------------------------------------------------

def normalize(tag):
    return tag.strip().lower()


def score_hypotheses(smell, location, timing):
    loc = normalize(location)
    tim = normalize(timing)
    ranked = []
    for name, h in HYPOTHESES.items():
        if smell not in h["smells"]:
            continue
        s = h["base"]
        if loc and loc in h["locations"]:
            s *= 1.6
        elif loc and loc not in h["locations"]:
            s *= 0.35
        if tim:
            if tim in h["timings"]:
                s *= 1.5
            elif tim in {"after rain", "after-rain"} and "after-rain" in h["timings"]:
                s *= 1.5
            elif tim in {"when appliance runs", "when-appliance-runs"} and "when-appliance-runs" in h["timings"]:
                s *= 1.5
            else:
                s *= 0.8
        ranked.append((s, name))
    ranked.sort(reverse=True)
    total = sum(s for s, _ in ranked) or 1.0
    return [(name, s / total) for s, name in ranked]


def cmd_diagnose(args):
    smell = normalize(args.smell)
    ranked = score_hypotheses(smell, args.location, args.timing)
    if not ranked:
        print(f"No hypotheses for smell family '{smell}'. Families: " +
              ", ".join(sorted({x for h in HYPOTHESES.values() for x in h['smells']})))
        return 1
    print(f"SMELL: {smell}" +
          (f" | {args.location}" if args.location else "") +
          (f" | timing: {args.timing}" if args.timing else ""))
    print("Screen danger patterns first if any apply (danger command).\n")
    print("RANKED HYPOTHESES:")
    for i, (name, p) in enumerate(ranked, 1):
        h = HYPOTHESES[name]
        print(f"\n{i}. {name.upper()} ({p:.0%})")
        print(f"   CHECK: {h['check']}")
        print(f"   FIX:   {h['fix']}")
    return 0


def cmd_danger(args):
    key = normalize(args.smell)
    if key in DANGER:
        print(DANGER[key])
        return 0
    print("No special danger protocol for that family. Danger families: " +
          ", ".join(DANGER))
    return 0


LOCALIZE = {
    "dry p-trap": [
        "Pour test every underused drain, lowest fixture first (floor drains).",
        "Re-sniff at 10 min — trap-refill causes fade within minutes.",
        "If no fade: move to wax ring (rock test) then vent (gurgle test).",
    ],
    "mold cavity": [
        "Sniff outlet/switch boxes on the suspect wall — cavities connect through them.",
        "Follow the gradient: strongest box = cavity behind it.",
        "Look for stain/moisture; confirm with meter if available before opening anything.",
    ],
    "dead animal in wall": [
        "Room gradient + fly concentration points at the void (day 4+).",
        "Sniff each electrical box on the suspect wall at ankle and waist height.",
        "Only open the wall if: multi-week smell, wall staining, or repeating fly cycles.",
    ],
    "electrical overheating": [
        "Smell strongest AT which fixture? Swap-test lamps/bulbs one day at a time.",
        "Check dimmer switches and the breaker panel door (sniff at the seam).",
        "Kill power before opening anything. Electrician for anything hardwired.",
    ],
    "washer gasket biofilm": [
        "Fold back the door gasket; smell the interior drum seal and drawer.",
        "Run empty hot cycle with washer cleaner — smell gone after = confirmed.",
    ],
    "refrigerator drip pan": [
        "Pull base grille, slide pan out, smell it. Check defrost drain for blockage.",
    ],
    "default": [
        "Sniff-map the gradient: ankle/waist/ceiling in the strongest room. Write it down.",
        "Fixture elimination: run each suspect fixture, re-sniff at 10 min.",
        "Appliance isolation: smell only when X runs = X's drain/filter/heat path.",
        "Weather correlation: after-rain? Check timing table in references.",
    ],
}


def cmd_localize(args):
    key = normalize(args.hypothesis)
    steps = LOCALIZE.get(key, LOCALIZE["default"])
    print(f"LOCALIZATION — {key}\n")
    for i, step in enumerate(steps, 1):
        print(f"  {i}. {step}")
    return 0


def cmd_kill(args):
    key = normalize(args.source)
    fixes = {
        "dry p-trap": "Refill + 1 tbsp mineral oil. Monthly winter check for floor drains.",
        "garbage disposal film": "Ice+citrus scrape, soda/vinegar foam 15 min, wash splash guard.",
        "mold": "Stop moisture first. <=1 m2 hard surface: detergent wash + 48 h dry (not bleach-only). "
                ">1 m2 / in-wall / HVAC / recurring: professional remediation.",
        "dead animal in wall": "Carbon gel + seal box holes + ventilate; wait day 10-14. "
                               "Cut wall only if multi-week, staining, or repeat fly cycles.",
        "pet urine in pad": "Enzymatic SATURATED + covered 12-24 h, extract. Seal subfloor on repeat failure.",
        "washer gasket biofilm": "Gasket scrub + cleaner hot cycle; door ajar after loads.",
        "electrical overheating": "Power off, electrician. Do not reuse fixture until checked.",
    }
    if key in fixes:
        print(f"KILL PROTOCOL — {key}\n  {fixes[key]}")
    else:
        h = HYPOTHESES.get(key)
        if h:
            print(f"KILL PROTOCOL — {key}\n  {h['fix']}")
        else:
            print("Unknown source. Known: " + ", ".join(sorted(HYPOTHESES)) +
                  ", " + ", ".join(sorted(fixes)))
    return 0


def cmd_log(args):
    if args.stats:
        if not LOG_PATH.exists():
            print("No episodes logged yet.")
            return 0
        episodes = json.loads(LOG_PATH.read_text())
        print(f"{len(episodes)} episodes logged:")
        for e in episodes:
            print(f"  {e['date']}  {e['note']}")
        # crude pattern hints
        lows = [e for e in episodes if "away" in e["note"].lower() or "vacation" in e["note"].lower()]
        rains = [e for e in episodes if "rain" in e["note"].lower()]
        if len(lows) >= 2 and len(lows) >= len(episodes) * 0.5:
            print("\nPATTERN: majority of episodes follow low water use → dry-trap hypothesis strengthened.")
        if len(rains) >= 2 and len(rains) >= len(episodes) * 0.5:
            print("\nPATTERN: majority are rain-linked → vent/moisture path hypothesis strengthened.")
        return 0
    if not args.note:
        print("Provide --note \"...\" or --stats")
        return 1
    episodes = json.loads(LOG_PATH.read_text()) if LOG_PATH.exists() else []
    import datetime
    episodes.append({"date": datetime.date.today().isoformat(), "note": args.note})
    LOG_PATH.write_text(json.dumps(episodes, indent=2, ensure_ascii=False))
    n = len(episodes)
    hint = " — pattern review useful at 5+ entries" if n < 5 else f" — {n} entries: review patterns now"
    print(f"logged episode #{n}{hint}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("diagnose")
    d.add_argument("--smell", required=True)
    d.add_argument("--location")
    d.add_argument("--timing")
    d.set_defaults(func=cmd_diagnose)
    dg = sub.add_parser("danger")
    dg.add_argument("--smell", required=True)
    dg.set_defaults(func=cmd_danger)
    lo = sub.add_parser("localize")
    lo.add_argument("--hypothesis", required=True)
    lo.set_defaults(func=cmd_localize)
    k = sub.add_parser("kill")
    k.add_argument("--source", required=True)
    k.set_defaults(func=cmd_kill)
    lg = sub.add_parser("log")
    lg.add_argument("--note")
    lg.add_argument("--stats", action="store_true")
    lg.set_defaults(func=cmd_log)
    args = ap.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
