#!/usr/bin/env python3
"""Slow Cooker Converter — rewrite recipes across appliance modes.

Stdlib only, offline.

Commands:
  time        --from MODE --minutes N --to MODE      time mapping
  convert     --from MODE --to MODE --recipe TEXT    recipe rewrite + timeline
  capacity    --servings N --cooker Q                fill verdict (Q in liters)
  ingredients --to MODE                             problem-ingredient triage
"""
import argparse
import re
import sys

MODES = ["stovetop", "oven", "slow-low", "slow-high", "pressure", "rice-program", "sauta"]  # 'sauta' = saute w/o accent

DISPLAY = {"sauta": "sauté", "slow-low": "slow LOW", "slow-high": "slow HIGH",
           "rice-program": "rice program", "pressure": "pressure HP"}

# (from, to) -> (min_minutes, max_minutes) converted, or callable note
TIME_MAP = {
    ("stovetop", "slow-low"): lambda m: (m * 6, m * 8),
    ("stovetop", "slow-high"): lambda m: (m * 3, m * 4),
    ("stovetop", "pressure"): lambda m: (max(3, round(m / 6)), max(4, round(m / 6) + 3)),
    ("oven", "slow-low"): lambda m: (round(m * 3), round(m * 3.5)),
    ("oven", "slow-high"): lambda m: (round(m * 1.5), round(m * 2)),
    ("oven", "pressure"): lambda m: (round(m / 6), round(m / 5)),
    ("slow-low", "slow-high"): lambda m: (round(m / 2), round(m / 2)),
    ("slow-high", "slow-low"): lambda m: (m * 2, m * 2),
    ("slow-low", "stovetop"): lambda m: (round(m / 4), round(m / 3)),
    ("slow-high", "stovetop"): lambda m: (round(m / 2), round(m / 2)),
    ("slow-low", "pressure"): lambda m: (round(m / 14), round(m / 10)),
    ("slow-high", "pressure"): lambda m: (round(m / 7), round(m / 5)),
    ("pressure", "slow-low"): lambda m: (m * 10, m * 14),
    ("pressure", "slow-high"): lambda m: (m * 5, m * 7),
    ("stovetop", "rice-program"): lambda m: (3, 4),
    ("oven", "rice-program"): lambda m: (3, 4),
}

LIQUID = {  # target mode -> (factor, note)
    "slow-low": (0.75, "slow pot loses ~nothing to evaporation"),
    "slow-high": (0.75, "slow pot loses ~nothing to evaporation"),
    "pressure": (0.5, "sealed pot: zero evaporation"),
    "stovetop": (1.0, ""),
    "oven": (1.0, ""),
}

LATE_RULES = [
    # (regex, target_modes, instruction)
    (r"\b(milk|cream|sour cream|yogurt|half.and.half|single cream)\b",
     {"slow-low", "slow-high"},
     "DAIRY: add in the LAST 30-60 min (never hour 0 — curdles/breaks). "
     "Longer window needed? use evaporated milk or coconut cream."),
    (r"\b(milk|cream|sour cream|yogurt|half.and.half|single cream)\b",
     {"pressure"},
     "DAIRY: NEVER under pressure — stir in after release, finish on sauté 2-3 min."),
    (r"\b(pasta|macaroni|noodles|spaghetti|linguine|orzo)\b",
     {"slow-low", "slow-high"},
     "PASTA: cook separately OR add in the last 20-30 min LOW-equiv."),
    (r"\b(pasta|macaroni|noodles)\b",
     {"pressure"},
     "PASTA under pressure: 4-6 min, half-fill max (foams)."),
    (r"\b(basil|cilantro|coriander leaf|parsley|dill|chive)\b",
     {"slow-low", "slow-high", "pressure"},
     "TENDER HERBS: stir in at serve, not at start."),
    (r"\b(flour|cornstarch|corn flour|roux)\b",
     {"slow-low", "slow-high"},
     "THICKENER: dust sinks/lumps — cold-water slurry at the END, or sauté-reduce."),
    (r"\b(flour|cornstarch)\b",
     {"pressure"},
     "THICKENER: grits under pressure — thicken AFTER release on sauté."),
    (r"\b(wine|beer|brandy|whisky|whiskey|sherry|vermouth)\b",
     {"slow-low", "slow-high", "pressure"},
     "ALCOHOL: reduce by half first (sauté/microwave) — raw booze never boils off "
     "in sealed/slow pots. Under pressure also cut amount ~1/3."),
    (r"\b(rice)\b",
     {"slow-low", "slow-high"},
     "RICE in slow pot: long cycle turns grains to paste — pressure rice program "
     "or cook apart (or last 2 h LOW with +25% liquid)."),
    (r"\b(zucchini|courgette|peas|spinach|corn)\b",
     {"slow-low", "slow-high"},
     "FAST VEG: last 30 min or they vanish."),
    (r"\b(zucchini|courgette|peas|spinach)\b",
     {"pressure"},
     "FAST VEG under pressure: 0 min — add at release."),
    (r"\b(shrimp|prawns|salmon|white fish|tilapia|cod|scallops)\b",
     {"pressure"},
     "DELICATE FISH/SHELLFISH: 0 min HP — add at release, sauté 2-3 min."),
]

INGREDIENT_NOTES = {
    "slow-low": [
        "dairy -> last 30-60 min (evaporated milk for longer windows)",
        "pasta -> separate, or last 20-30 min",
        "tender herbs -> at serve; woody herbs at hour 0",
        "thickeners -> cold slurry at end; flour-dust at start lumps",
        "alcohol -> reduce by half before it goes in",
        "frozen meat -> NO (danger zone too long); thaw first",
        "kidney beans etc. -> boil hard 10 min first (toxin), then slow",
        "liquid -> cut ~25% vs stovetop/oven recipe",
        "lid -> no peeks; each look adds 20-30 min on LOW",
    ],
    "slow-high": [
        "same rules as LOW; 1 h HIGH ≈ 2 h LOW",
        "dairy -> last 20-30 min",
        "pasta -> last 15 min",
        "liquid -> cut ~25%",
    ],
    "pressure": [
        "milk products -> NEVER under pressure; finish on sauté after release",
        "alcohol -> reduce first AND cut amount ~1/3",
        "flour thickeners -> after release only",
        "fill -> max 2/3; 1/2 for beans/pasta/oats (foam)",
        "braises -> natural release 10+ min (quick release toughens)",
        "liquid -> cut ~50% vs stovetop",
        "delicate fish -> 0 min HP",
    ],
}


def fmt_hhmm(minutes):
    if minutes >= 60:
        h, m = divmod(round(minutes), 60)
        return f"{h}h" + (f"{m:02d}m" if m else "")
    return f"{round(minutes)}m"


def cmd_time(args):
    if (args.frm, args.to) not in TIME_MAP:
        print(f"no direct map {args.frm} -> {args.to}; try via stovetop")
        return 1
    lo, hi = TIME_MAP[(args.frm, args.to)](args.minutes)
    extra = " + natural release 10-15 min" if args.to == "pressure" else ""
    print(f"{fmt_hhmm(args.minutes)} @ {DISPLAY.get(args.frm, args.frm)}"
          f"  ->  {fmt_hhmm(lo)}-{fmt_hhmm(hi)} @ {DISPLAY.get(args.to, args.to)}{extra}")
    return 0


def cmd_capacity(args):
    # volume classes: soup .6, stew .5, side .3 L per serving
    for cls, per in (("soup/chili", 0.6), ("stew/braise", 0.5), ("side", 0.3)):
        vol = args.servings * per
        frac = vol / args.cooker
        verdict = "OK (half..two-thirds)" if 0.5 <= frac <= 0.67 else (
            "UNDER half — scorch risk in slow pot, scale up or smaller pot" if frac < 0.5
            else "OVER two-thirds — boil-over/pressure headroom risk")
        print(f"{cls:14} {vol:.1f} L of {args.cooker} L ({frac:.0%}) -> {verdict}")
    return 0


def cmd_ingredients(args):
    notes = INGREDIENT_NOTES.get(args.to)
    if not notes:
        print("notes available for: " + ", ".join(INGREDIENT_NOTES))
        return 1
    print(f"TRIAGE for -> {DISPLAY.get(args.to, args.to)}\n")
    for n in notes:
        print(f"  - {n}")
    return 0


def cmd_convert(args):
    recipe = args.recipe
    to = args.to
    print(f"CONVERTED ({DISPLAY.get(args.frm, args.frm)} -> {DISPLAY.get(to, to)}):\n")
    print("  1. (unchanged steps carry over; sear/brown steps keep — flavor base)")
    # time conversion: find "NNN min" or "N.N h" patterns
    found_time = False
    for m in re.finditer(r"(\d+(?:\.\d+)?)\s*(h|hr|hour|min|minute)", recipe, re.I):
        # skip sear/brown/skillet steps — they stay as-is (check current clause only)
        clause_start = max(recipe.rfind(";", 0, m.start()), recipe.rfind(".", 0, m.start()), 0)
        context = recipe[clause_start:m.start()].lower()
        if any(w in context for w in ("brown", "sear", "skillet", "saut")):
            continue
        val = float(m.group(1))
        mins = val * 60 if m.group(2).lower().startswith("h") else val
        if (args.frm, to) in TIME_MAP:
            lo, hi = TIME_MAP[(args.frm, to)](mins)
            found_time = True
            extra = " + NR10-15" if to == "pressure" else ""
            print(f"  2. cook step '{m.group(0)}' -> {fmt_hhmm(lo)}-{fmt_hhmm(hi)}{extra}")
    if not found_time:
        print("  2. (no explicit time found in text — map manually via the time command)")
    # liquid adjustment
    factor, note = LIQUID.get(to, (1.0, ""))
    if factor != 1.0:
        print(f"  3. LIQUID: cut to {factor:.0%} of original — {note}")
    # late rules
    timeline = []
    for pat, modes, msg in LATE_RULES:
        if to in modes and re.search(pat, recipe, re.I):
            timeline.append(msg)
    if timeline:
        print("\n  INSERT-AT TIMELINE / INGREDIENT CHANGES:")
        for msg in timeline:
            print(f"    * {msg}")
    if to in {"slow-low", "slow-high"}:
        print("\n  SERVE: thickness check — slow pot can't reduce; slurry or sauté-reduce.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("time")
    t.add_argument("--from", dest="frm", required=True)
    t.add_argument("--minutes", type=float, required=True)
    t.add_argument("--to", required=True)
    t.set_defaults(func=cmd_time)
    c = sub.add_parser("convert")
    c.add_argument("--from", dest="frm", required=True)
    c.add_argument("--to", required=True)
    c.add_argument("--recipe", required=True)
    c.set_defaults(func=cmd_convert)
    cap = sub.add_parser("capacity")
    cap.add_argument("--servings", type=float, required=True)
    cap.add_argument("--cooker", type=float, required=True, help="cooker size in liters")
    cap.set_defaults(func=cmd_capacity)
    ing = sub.add_parser("ingredients")
    ing.add_argument("--to", required=True)
    ing.set_defaults(func=cmd_ingredients)
    args = ap.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
