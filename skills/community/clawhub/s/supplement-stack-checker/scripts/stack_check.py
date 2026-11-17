#!/usr/bin/env python3
"""
Supplement Stack Checker — interaction flags, UL dose checks, duplicate
detection, and a timing schedule that separates mineral antagonists.

Products are given as: "Name|ingredient:mg|ingredient:mg"
  - mg units; micrograms written as e.g. vitamin D:25u  (u = µg)
  - omega-3:1000 means 1000 mg EPA+DHA

Usage:
  stack_check.py --demo
  stack_check.py "Multivitamin|zinc:15|vitamin B6:2|vitamin A:800u" \
                 "Calcium+D|calcium:500|vitamin D:25u" "Zinc|zinc:23" \
                 --schedule
  stack_check.py --stack stack.txt --schedule
"""
import argparse
import re
import sys

# canonical name -> (display, UL in same unit as input, unit label)
# UL None = no established adult UL (pragmatic cap used where noted)
ING = {
    "vitamin a":    ("vitamin A (retinol)", 3000, "u"),
    "vitamin b6":   ("vitamin B6", 100, "mg"),
    "vitamin b12":  ("vitamin B12", None, "mg"),
    "folate":       ("folate (folic acid)", 1000, "u"),
    "folic acid":   ("folate (folic acid)", 1000, "u"),
    "niacin":       ("niacin (nicotinic acid)", 35, "mg"),
    "vitamin c":    ("vitamin C", 2000, "mg"),
    "vitamin d":    ("vitamin D", 100, "u"),
    "vitamin d3":   ("vitamin D", 100, "u"),
    "vitamin e":    ("vitamin E", 1000, "mg"),
    "vitamin k":    ("vitamin K", None, "mg"),
    "vitamin k2":   ("vitamin K", None, "mg"),
    "calcium":      ("calcium", 2500, "mg"),
    "iron":         ("iron", 45, "mg"),
    "zinc":         ("zinc", 40, "mg"),
    "magnesium":    ("magnesium (supplemental)", 350, "mg"),
    "selenium":     ("selenium", 400, "u"),
    "iodine":       ("iodine", 1100, "u"),
    "copper":       ("copper", 10000, "u"),
    "omega-3":      ("omega-3 EPA+DHA", 3000, "mg"),
    "fish oil":     ("omega-3 EPA+DHA", 3000, "mg"),
    "epa":          ("omega-3 EPA+DHA", 3000, "mg"),
    "dha":          ("omega-3 EPA+DHA", 3000, "mg"),
    "caffeine":     ("caffeine", 400, "mg"),
    "melatonin":    ("melatonin", 5, "mg"),   # pragmatic cap, no formal UL
    "curcumin":     ("curcumin", None, "mg"),
    "boron":        ("boron", 20, "mg"),
    "potassium":    ("potassium (supplemental)", None, "mg"),
    "st. john's wort": ("St. John's Wort", None, "mg"),
    "st johns wort":   ("St. John's Wort", None, "mg"),
    "5-htp":        ("5-HTP", None, "mg"),
    "ginkgo":       ("ginkgo", None, "mg"),
    "garlic":       ("garlic extract", None, "mg"),
    "red yeast rice": ("red yeast rice", None, "mg"),
    "ginseng":      ("ginseng", None, "mg"),
    "rhodiola":     ("rhodiola", None, "mg"),
    "probiotic":    ("probiotic (CFU)", None, "billion CFU"),
    "ashwagandha":  ("ashwagandha", None, "mg"),
}

# pair rules: (a, b, kind, message)
PAIRS = [
    ("calcium", "iron", "BLOCK",
     "calcium inhibits non-heme iron absorption up to ~50% — separate by 2+ h"),
    ("zinc", "iron", "BLOCK",
     "zinc and iron compete for absorption (>30 mg zinc especially) — separate by 2+ h"),
    ("calcium", "zinc", "BLOCK",
     "high-dose calcium modestly reduces zinc absorption — separate when convenient"),
    ("magnesium", "iron", "BLOCK",
     "magnesium salts can chelate iron — separate when convenient"),
    ("vitamin c", "iron", "ENHANCE",
     "vitamin C raises non-heme iron absorption 2-3x — take TOGETHER"),
    ("vitamin d", "calcium", "ENHANCE",
     "vitamin D improves calcium absorption — take TOGETHER"),
    ("vitamin d", "magnesium", "ENHANCE",
     "magnesium is a cofactor for vitamin D activation — fine together"),
    ("zinc", "copper", "DEPLETE",
     "chronic zinc >40 mg/day induces copper deficiency (months-scale) — ensure copper or cap zinc"),
    ("st. john's wort", "5-htp", "DANGER",
     "serotonin syndrome risk stacking serotonergic agents — prescriber decision"),
    ("fish oil", "ginkgo", "DANGER",
     "additive anticoagulant tendency (fish oil + ginkgo) — relevant before surgery / on blood thinners"),
    ("fish oil", "garlic", "DANGER",
     "additive anticoagulant tendency (fish oil + garlic) — bleeding-risk stacking"),
    ("fish oil", "vitamin e", "DANGER",
     "high-dose vitamin E + omega-3 stacks bleed tendency — keep E below UL"),
    ("ginkgo", "garlic", "DANGER",
     "ginkgo + garlic both antiplatelet — stacking multiplies bleeding risk"),
    ("red yeast rice", "niacin", "DANGER",
     "red yeast rice is statin-active: combining with niacin raises myopathy risk"),
]

# timing preferences: slot -> reason
NIGHT = {"magnesium": "relaxant mineral forms; sleep-friendly",
         "melatonin": "1-2 h before bed"}
MORNING_EMPTY = {"iron": "empty-ish stomach + away from coffee/tea/calcium"}
WITH_FAT = {"vitamin a": "fat-soluble", "vitamin d": "fat-soluble",
            "vitamin e": "fat-soluble", "vitamin k": "fat-soluble",
            "vitamin k2": "fat-soluble", "omega-3": "fat improves absorption",
            "fish oil": "fat improves absorption", "curcumin": "fat + piperine"}
BEFORE_14 = {"caffeine": "sleep interference", "ginseng": "stimulating adaptogen",
             "rhodiola": "can disturb sleep", "vitamin b6": "vivid dreams/activating for some",
             "b complex": "activating"}


def canon(name: str) -> str:
    n = name.lower().strip()
    if n in ING:
        return n
    for k in ING:
        if k in n or n in k:
            return k
    return n


def parse_product(spec: str):
    """'Name|ing:qty|ing:qty' -> (name, [(ing, qty, unit)])"""
    parts = [p.strip() for p in spec.split("|") if p.strip()]
    if not parts:
        return None
    name = parts[0]
    ings = []
    for p in parts[1:]:
        m = re.match(r"^(.+?):\s*([\d.]+)\s*(u|ug|mcg|mg|g|iu)?$", p, re.I)
        if not m:
            continue
        iname, val, unit = m.group(1), float(m.group(2)), (m.group(3) or "").lower()
        if unit in ("ug", "mcg"):
            unit = "u"
        if unit == "iu":
            # convert IU per ingredient class
            c = canon(iname)
            if "vitamin d" in c:
                val /= 40.0; unit = "u"
            elif "vitamin a" in c:
                val *= 0.3; unit = "u"
        elif unit == "g":
            val *= 1000; unit = "mg"
        ings.append((iname, val, unit))
    return (name, ings)


def check(products, schedule=False):
    out, flags = [], []
    totals = {}   # canon -> (display, amount, unit, [products])
    for pname, ings in products:
        for iname, val, unit in ings:
            c = canon(iname)
            disp, ul, ulunit = ING.get(c, (iname, None, unit or "mg"))
            # unit unify: assume stack input mg unless 'u'
            amt_unit = unit if unit in ("u", "mg") else "mg"
            t = totals.setdefault(c, [disp, 0.0, amt_unit, ul, ulunit, set()])
            if amt_unit != t[2]:
                t = totals[c] = [disp, totals[c][1], "MIXED", ul, ulunit,
                                 totals[c][5]]
            t[1] += val
            t[5].add(pname)

    out.append("DAILY TOTALS (summed across products)")
    out.append("=" * 64)
    for c, (disp, amt, unit, ul, ulunit, srcs) in sorted(totals.items()):
        line = f"  {disp:<30} {amt:>9,.0f} {unit:<3}"
        if ul is not None and unit == ulunit:
            pct = amt / ul
            line += f" vs UL {ul:,} {ulunit}  ({pct:.0%})"
            if pct > 1.0:
                flags.append(("UL", f"{disp}: {amt:,.0f} {unit} EXCEEDS adult "
                                    f"UL {ul:,} {ulunit} — cut back or drop a "
                                    f"product ({', '.join(sorted(srcs))})"))
            elif pct >= 0.8:
                flags.append(("HIGH", f"{disp}: {amt:,.0f} {unit} at "
                                      f"{pct:.0%} of UL — near ceiling, mind "
                                      f"dietary sources"))
        elif len(srcs) > 1:
            line += f"  (from {len(srcs)} products)"
        out.append(line)

    # pair interactions
    out.append("")
    out.append("INTERACTIONS")
    out.append("-" * 64)
    keys = list(totals.keys())
    pair_found = False
    # chronic zinc->copper depletion even without copper in the stack
    if "zinc" in totals and "copper" not in totals:
        zamt = totals["zinc"][1]
        if zamt >= 30:
            out.append(f"  [CHRONIC    ] zinc {zamt:,.0f} mg/day without copper")
            out.append("               months-scale zinc at/above ~30 mg "
                       "depletes copper — add 1-2 mg copper or cycle zinc")
            flags.append(("CHRONIC", f"zinc {zamt:,.0f} mg/day with no copper "
                                     "in stack: chronic depletion risk"))
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            for pa, pb, kind, msg in PAIRS:
                if {canon(pa), canon(pb)} == {a, b}:
                    pair_found = True
                    tag = {"BLOCK": "SEPARATE", "ENHANCE": "COMBINE",
                           "DEPLETE": "CHRONIC", "DANGER": "ASK-DOCTOR"}[kind]
                    out.append(f"  [{tag:<10}] {totals[a][0]} + {totals[b][0]}")
                    out.append(f"               {msg}")
                    if kind == "BLOCK":
                        flags.append(("BLOCK", f"{totals[a][0]} + "
                                               f"{totals[b][0]}: separate by "
                                               "2+ h (scheduler below does "
                                               "this)"))
                    if kind == "DANGER":
                        flags.append(("DANGER", f"{totals[a][0]} + "
                                                f"{totals[b][0]}: {msg}"))
    if not pair_found:
        out.append("  no known pair interactions among these ingredients")

    # duplicates
    dups = {c: v for c, v in totals.items() if len(v[5]) > 1}
    if dups:
        out.append("")
        out.append("DUPLICATE SOURCES")
        out.append("-" * 64)
        for c, v in dups.items():
            out.append(f"  {v[0]} from {len(v[5])} products: "
                       f"{', '.join(sorted(v[5]))}")

    # schedule
    if schedule:
        out.append("")
        out.append("SUGGESTED TIMING (2-hour rule applied)")
        out.append("-" * 64)
        slots = {"breakfast": [], "lunch": [], "dinner": [], "evening": []}
        iron_amt = totals.get("iron", [None, 0])[1]
        for c, (disp, amt, unit, *_rest) in totals.items():
            placed = False
            for ing, why in NIGHT.items():
                if canon(ing) == c:
                    slots["evening"].append(f"{disp} ({why})"); placed = True
            if not placed:
                for ing, why in MORNING_EMPTY.items():
                    if canon(ing) == c:
                        slots["breakfast"].append(
                            f"{disp} ({why}; with vitamin C if in stack)")
                        placed = True
            if not placed:
                for ing in ("calcium",):
                    if canon(ing) == c:
                        slots["lunch"].append(f"{disp} (2+ h after iron "
                                              "breakfast; with meal)"); placed = True
            if not placed:
                for ing, why in WITH_FAT.items():
                    if canon(ing) == c:
                        slots["dinner"].append(f"{disp} (largest meal: "
                                               f"{why})"); placed = True
            if not placed:
                for ing, why in BEFORE_14.items():
                    if canon(ing) == c:
                        slots["breakfast"].append(f"{disp} ({why}; before "
                                                  "14:00)"); placed = True
            if not placed:
                if canon("zinc") == c and iron_amt > 0:
                    slots["dinner"].append(f"{disp} (away from morning iron)")
                    placed = True
            if not placed:
                slots["breakfast"].append(disp)
        for slot in ("breakfast", "lunch", "dinner", "evening"):
            out.append(f"  {slot:<11}: " + ("; ".join(slots[slot]) or "-"))

    out.append("")
    out.append("FLAGS")
    out.append("-" * 64)
    if flags:
        for kind, msg in flags:
            out.append(f"  ! [{kind}] {msg}")
    else:
        out.append("  none — doses within ULs, no danger pairs, no blocks")
    out.append("")
    out.append("Educational check from public nutrition references "
               "(NIH-ODS level). Not medical advice — confirm supplement/"
               "drug decisions with a pharmacist or physician.")
    return "\n".join(out)


DEMO = [
    "OneADay 50+|vitamin A:600u|vitamin B6:3|zinc:15|calcium:200|"
    "selenium:105u|vitamin D:20u",
    "Cal-Mag PM|calcium:500|magnesium:250",
    "Gentle Iron AM|iron:18|vitamin C:90",
    "Cold-Eeze lozenge|zinc:23",
    "Omega-3 1200|fish oil:1000|vitamin E:15",
    "Mood Support|st. john's wort:300|5-htp:100",
]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("products", nargs="*", help='"Name|ing:mg|ing:mg"')
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--stack", help="file: one product per line")
    ap.add_argument("--schedule", action="store_true")
    args = ap.parse_args(argv)

    if args.demo:
        print("DEMO — blog-assembled stack (6 products)\n" + "~" * 60)
        products = [p for p in (parse_product(s) for s in DEMO) if p]
        print(check(products, schedule=True))
        return 0
    specs = list(args.products)
    if args.stack:
        specs += [ln.strip() for ln in open(args.stack)
                  if ln.strip() and not ln.startswith("#")]
    if not specs:
        ap.print_help()
        return 1
    products = [p for p in (parse_product(s) for s in specs) if p]
    bad = len(specs) - len(products)
    if bad:
        print(f"(skipped {bad} unparseable line(s))")
    print(check(products, schedule=args.schedule))
    return 0


if __name__ == "__main__":
    sys.exit(main())
