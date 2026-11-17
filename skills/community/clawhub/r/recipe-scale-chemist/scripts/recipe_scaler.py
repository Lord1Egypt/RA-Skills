#!/usr/bin/env python3
"""
Recipe Scale Chemist — non-linear recipe scaling, pan conversion, time fixes.

Usage:
  recipe_scaler.py --demo
  recipe_scaler.py --recipe file.json --factor 3
  recipe_scaler.py --recipe file.json --servings 4:12
  recipe_scaler.py --pan-from 9x13x2 --pan-to 9rx9rx1.5 --time 32

Recipe JSON: {"title": str, "servings": int, "bake_minutes": num?,
              "ingredients": [{"name": str, "qty": num, "unit": str}...]}
"""
import argparse
import json
import math
import re
import sys

# (regex, class label, exponent p, why)
RULES = [
    (r"\b(kosher|sea|table)?\s*salt\b|fleur de sel", "salt", 0.80,
     "salt perception is sub-linear; oversalted food is unrecoverable"),
    (r"cayenne|chili flakes?|chilli|red pepper flake|habanero|jalapeno|\
jalape|sriracha|hot sauce|chipotle|harissa|sambal|gochujang|black pepper\b",
     "chili/heat", 0.75,
     "capsaicin stacks fast; the classic doubled-recipe disaster"),
    (r"\bspice|cumin|paprika|cinnamon|oregano|thyme|rosemary|basil(?! leave)|\
curry|turmeric|garlic powder|onion powder|saffron|nutmeg|allspice|coriander \
seed|cloves?|cardamom|garam|five.sppe|chile powder|chilli powder",
     "dried spice", 0.80,
     "aroma compounds overwhelm balance at high concentration"),
    (r"fresh (basil|cilantro|coriander|parsley|dill|mint|oregano|thyme)|\
cilantro|parsley leaves|dill weed|mint leaves|basil leaves",
     "fresh herb", 0.85, "milder than dried, still sub-linear"),
    (r"vanilla", "vanilla", 0.90, "aromatic; excess is noticeable"),
    (r"baking (powder|soda)|bicarbonate|cream of tartar|active dry yeast|\
instant yeast|fresh yeast|sourdough starter",
     "leavening", 0.90,
     "excess leavening = metallic/soapy taste and collapse risk"),
    (r"\bwine(?! vinegar)|bourbon|\brum\b|vodka|\bbeer\b|liqueur|brandy|\
vermouth|sherry|whiskey|whisky|tequila|marsala|madeira",
     "alcohol", 0.90, "reduction is non-linear; over-extracts tannins"),
    (r"\boil\b|olive oil|vegetable oil|canola|sesame oil|butter|margarine|\
\blard\b|shortening|ghee|duck fat|bacon fat",
     "fat", 0.95, "nearly linear; greasiness appears at excess"),
]
DEFAULT_CLASS = ("bulk (flour/sugar/meat/veg/liquid)", 1.00,
                 "bulk physics — scales linearly")


def classify(name: str):
    low = name.lower()
    for pattern, label, p, why in RULES:
        if re.search(pattern, low):
            return label, p, why
    return DEFAULT_CLASS


def fmt_qty(q: float) -> str:
    """Trim floats to something a cook can measure."""
    if q >= 10:
        return f"{q:.0f}"
    if q >= 1:
        s = f"{q:.1f}".rstrip("0").rstrip(".")
        return s
    s = f"{q:.2f}".rstrip("0").rstrip(".")
    return s if s else "0"


def scale_ingredient(ing: dict, factor: float):
    name, qty, unit = ing["name"], float(ing["qty"]), ing.get("unit", "")
    label, p, why = classify(name)
    scaled = qty * (factor ** p)

    notes = []
    if p != 1.0:
        linear = qty * factor
        notes.append(f"linear would be {fmt_qty(linear)} {unit} "
                     f"(p={p:.2f}: {why})")
    # Whole-egg handling
    if re.search(r"\begg\b", name.lower()) and unit in ("", "count", "large",
                                                        "eggs", "whole"):
        rounded = max(0.5, round(scaled * 2) / 2)
        if abs(rounded - scaled) > 0.01:
            notes.append(f"rounded {fmt_qty(scaled)} -> {fmt_qty(rounded)} "
                         f"eggs (1 egg ~ 50 g / 3 tbsp beaten)")
        scaled = rounded
    return {"name": name, "orig": f"{fmt_qty(qty)} {unit}".strip(),
            "new": f"{fmt_qty(scaled)} {unit}".strip(),
            "class": label, "p": p, "notes": notes}


def scale_recipe(recipe: dict, factor: float) -> str:
    lines = [f"Recipe: {recipe.get('title', 'untitled')}  "
             f"| servings {recipe.get('servings', '?')} -> "
             f"{factor:g}x", "=" * 72,
             f"{'INGREDIENT':<28}{'ORIG':>10}{'SCALED':>10}  CLASS (p)"]
    lines.append("-" * 72)
    warn = []
    for ing in recipe["ingredients"]:
        r = scale_ingredient(ing, factor)
        lines.append(f"{r['name'][:27]:<28}{r['orig']:>10}{r['new']:>10}"
                     f"  {r['class']} (p={r['p']:.2f})")
        for n in r["notes"]:
            lines.append(f"{'':>50}-> {n}")
    if recipe.get("bake_minutes"):
        t = recipe["bake_minutes"]
        lines.append(f"\nBake time {t:g} min: SAME oven temperature; time "
                     f"moves only if pan DEPTH changed (see --pan-*/refs).")
    if abs(factor) >= 2:
        warn.append("Big jump (>=2x): add salt/spice at 80% of the scaled "
                    "amount, taste, then adjust.")
        warn.append("Cool large batches in shallow containers before "
                    "refrigerating (food safety does not scale down).")
    if warn:
        lines.append("\nWARNINGS:")
        lines.extend(f"  ! {w}" for w in warn)
    return "\n".join(lines)


# ---------------- pan geometry ----------------
def parse_pan(spec: str):
    """'9x13x2' -> (w,d,h) inches; '9r' or '9r-1.5' -> round d(,depth)."""
    s = spec.lower()
    if "r" in s:
        parts = [p for p in re.split(r"[rx×\-]", s) if p]
        d = float(parts[0])
        depth = float(parts[1]) if len(parts) > 1 else None
        return ("round", d, depth)
    nums = [float(x) for x in re.split(r"[x×]", s)]
    depth = nums[2] if len(nums) > 2 else None
    return ("rect", (nums[0], nums[1]), depth)


def pan_area(pan) -> float:
    kind, a, _ = pan
    if kind == "round":
        return math.pi * (a / 2) ** 2
    return a[0] * a[1]


def round_to_square_side(d: float) -> float:
    return d * math.sqrt(math.pi / 4)


def pan_report(spec_from: str, spec_to: str, t1: float | None) -> str:
    pf, pt = parse_pan(spec_from), parse_pan(spec_to)
    af, at = pan_area(pf), pan_area(pt)
    out = ["PAN CONVERSION", "=" * 60,
           f"from: {spec_from}  (area {af:.1f} sq in)",
           f"to:   {spec_to}  (area {at:.1f} sq in)",
           f"yield factor = {at / af:.2f}x "
           f"({'scale recipe UP' if at > af else 'scale DOWN' if at < af else 'same'})"]
    if pf[0] == "round":
        out.append(f"hint: {pf[1]:g}\" round ~ square pan of side "
                   f"{round_to_square_side(pf[1]):.1f}\"")
    if pt[0] == "round":
        out.append(f"hint: {pt[1]:g}\" round ~ square pan of side "
                   f"{round_to_square_side(pt[1]):.1f}\"")
    df, dt = pf[2], pt[2]
    if df and dt and t1:
        ratio = dt / df
        t2 = t1 * ratio ** 1.6
        out.append(f"depth {df}\" -> {dt}\" at same temp: bake {t1:g} min -> "
                   f"~{t2:.0f} min  (t x (d2/d1)^1.6)")
        out.append("start checking 10 min early; thermometer targets NEVER "
                   "scale")
    elif df and dt and not t1:
        out.append(f"depth {df}\" -> {dt}\": multiply bake time by "
                   f"(d2/d1)^1.6 = {(dt/df)**1.6:.2f}")
    else:
        out.append("(depth not given for both pans — bake time likely "
                   "unchanged if depths match)")
    if pt[0] == "round" and at / af > 1.0:
        out.append("note: same batter in narrower+taller pan = longer bake, "
                   "lower temp by 25F only if top browns too fast")
    return "\n".join(out)


DEMO_CHILI = {
    "title": "Hearty beef chili", "servings": 4,
    "ingredients": [
        {"name": "ground beef", "qty": 500, "unit": "g"},
        {"name": "kidney beans", "qty": 800, "unit": "g"},
        {"name": "crushed tomatoes", "qty": 796, "unit": "mL"},
        {"name": "kosher salt", "qty": 1.5, "unit": "tsp"},
        {"name": "cayenne pepper", "qty": 0.25, "unit": "tsp"},
        {"name": "ground cumin", "qty": 2, "unit": "tsp"},
        {"name": "smoked paprika", "qty": 1, "unit": "Tbsp"},
        {"name": "fresh cilantro", "qty": 0.25, "unit": "cup"},
        {"name": "olive oil", "qty": 2, "unit": "Tbsp"},
        {"name": "red wine", "qty": 120, "unit": "mL"},
    ],
}

DEMO_COOKIES = {
    "title": "Chocolate chip cookies", "servings": 24,
    "bake_minutes": 11,
    "ingredients": [
        {"name": "all-purpose flour", "qty": 2.25, "unit": "cups"},
        {"name": "butter", "qty": 1, "unit": "cup"},
        {"name": "brown sugar", "qty": 0.75, "unit": "cup"},
        {"name": "granulated sugar", "qty": 0.75, "unit": "cup"},
        {"name": "large egg", "qty": 2, "unit": "count"},
        {"name": "vanilla extract", "qty": 2, "unit": "tsp"},
        {"name": "baking soda", "qty": 1, "unit": "tsp"},
        {"name": "kosher salt", "qty": 1, "unit": "tsp"},
        {"name": "chocolate chips", "qty": 2, "unit": "cups"},
    ],
}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--recipe")
    ap.add_argument("--factor", type=float)
    ap.add_argument("--servings", help="FROM:TO e.g. 4:12")
    ap.add_argument("--pan-from")
    ap.add_argument("--pan-to")
    ap.add_argument("--time", type=float, help="bake time for depth math")
    args = ap.parse_args(argv)

    if args.demo:
        print(scale_recipe(DEMO_CHILI, 3.0))
        print()
        print(scale_recipe(DEMO_COOKIES, 0.5))
        print()
        print(pan_report("9x13x2", "9r-1.5", 32))
        print()
        print("ROAST: 2 kg -> 5 kg brisket: time x (5/2)^(2/3) = "
              f"{(5/2)**(2/3):.2f} (same temp, same internal pull temp)")
        return 0
    if args.pan_from and args.pan_to:
        print(pan_report(args.pan_from, args.pan_to, args.time))
        return 0
    if args.recipe:
        with open(args.recipe) as f:
            recipe = json.load(f)
        if args.servings:
            frm, to = (float(x) for x in args.servings.split(":"))
            factor = to / frm
        elif args.factor:
            factor = args.factor
        else:
            ap.error("need --factor or --servings FROM:TO")
        print(scale_recipe(recipe, factor))
        return 0
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
