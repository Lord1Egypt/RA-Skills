#!/usr/bin/env python3
"""Used-appliance deal checker: fair price bands + risk grading.

Prices a used appliance with an age-based depreciation curve (steeper in
years 1-2, flattening after), applies condition multipliers, and grades the
category's used-buy risk with failure modes and inspection priorities.

Stdlib only. Data: aggregated repair-frequency/lifespan knowledge from
appliance-repair trade publications and consumer reports class data.
"""
import argparse
import json

# category: (new price band lo, hi, service life yr, risk, killer failures)
CATS = {
    "top-washer":    ((450, 700), 13, "GOOD",
                      ["coupling/clutch wear ($120-180, rarely fatal)"]),
    "front-washer":  ((700, 1100), 10, "RISKY",
                      ["door gasket mold (cleanable/$150)", "drum bearing roar ($400-600, fatal)",
                       "control board ($250-350)"]),
    "electric-range": ((500, 900), 14, "GOOD",
                       ["element ($50-150)", "infinite switch ($90)"]),
    "gas-range":     ((600, 1000), 14, "GOOD",
                      ["igniter ($120)", "regulator/safety valve - pro check before buy"]),
    "fridge-simple": ((600, 900), 13, "GOOD",
                      ["start relay ($100)", "defrost timer ($150)",
                       "compressor ($700+) = walk away"]),
    "fridge-fancy":  ((1400, 2400), 10, "RISKY",
                      ["ice-maker assembly ($300+)", "main board ($300-450)",
                       "sealed-system leaks = total loss"]),
    "dishwasher":    ((400, 700), 10, "FAIR",
                      ["pump/motor ($250-400, often uneconomical)", "door latch/leaks"]),
    "dryer-basic":   ((450, 650), 13, "GOOD",
                      ["belt/rollers ($150)", "heating element ($120)"]),
    "dryer-he":      ((700, 1000), 10, "RISKY",
                      ["control board ($300+)", "sensor array failures"]),
    "tv":            ((400, 1200), 7, "FAIR",
                      ["backlight/panel failure = total loss", "no repair economy at current prices"]),
}

# condition multipliers applied to age-depreciated value
CONDITION = {
    "excellent": 1.00,   # verified working, clean, all features tested
    "good":      0.88,
    "fair":      0.70,   # cosmetic damage, one minor known issue
    "issues":    0.50,   # known fault (price ONLY if fault is cheap-fixable)
    "untested":  0.60,   # cannot verify working: max 60% of age value
}


def age_value(new_price, age_yr, life_yr):
    """Depreciation: 25%/yr years 1-2, then linear to ~15% residual at end of life."""
    if age_yr <= 0:
        return new_price * 0.80          # open-box/like-new
    if age_yr == 1:
        return new_price * 0.65
    if age_yr == 2:
        return new_price * 0.55
    # linear from 0.55 (yr2) to 0.15 (end of life)
    frac = min(age_yr, life_yr) / life_yr
    return new_price * (0.55 - (0.55 - 0.15) * (frac - 2 / life_yr) / max(1e-9, 1 - 2 / life_yr))


def band_for(category, age_yr, condition, new_price=None):
    lo, hi = CATS[category][0]
    life, risk = CATS[category][1], CATS[category][2]
    out = {}
    for np_ in (new_price, ) if new_price else (lo, hi):
        base = age_value(np_, age_yr, life)
        mult = CONDITION[condition]
        out[round(base * mult)] = np_
    return out, life, risk


def check(category, age_yr, asking, condition="good", new_price=None):
    if category not in CATS:
        raise SystemExit(f"unknown category {category}; choose from: {', '.join(CATS)}")
    band, life, risk = band_for(category, age_yr, condition, new_price)
    lo_band, hi_band = min(band), max(band)
    (nlo, nhi), _, killers = CATS[category][0], CATS[category][1], CATS[category][3]

    if asking <= lo_band * 0.7:
        verdict = "SUSPICIOUSLY CHEAP - verify it works before trusting it"
    elif asking <= hi_band:
        verdict = "FAIR DEAL" if risk != "RISKY" else "FAIR PRICE, RISKY CATEGORY - inspection is everything"
    elif asking <= hi_band * 1.2:
        verdict = "OVERPRICED - counter with the fair band"
    else:
        verdict = "SKIP - above fair band; buy refurb/scratch-dent instead"

    inspection = {
        "top-washer": ["high-speed spin: grinding = bearings, walk away",
                        "under-body rust/calcium", "drain filter sludge"],
        "front-washer": ["peel door gasket folds: black mold?",
                          "high-speed spin grind (bearing $400-600)",
                          "ask: door left open between loads?"],
        "electric-range": ["every element full then low (cycling)",
                            "oven holds 200C", "door hinge sag"],
        "gas-range": ["blue flames, no yellow tips", "igniter click -> flame <5s",
                       "sniff at valve; last service date"],
        "fridge-simple": ["paper test on door gaskets", "frost pattern even",
                           "rust at compressor = walk", "24h upright after transport"],
        "fridge-fancy": ["see ice-maker cycle", "error codes on display",
                          "check repair history - these fail serially"],
        "dishwasher": ["rinse cycle: pumps, no errors, no door leak",
                        "pull filter: black sludge = never maintained",
                        "rack tine rust ($80+/rack)"],
        "dryer-basic": ["drum turns + heats in 5 min", "lint at rear connection",
                         "burn smell = element touching drum"],
        "dryer-he": ["all sensor cycles selectable", "error codes",
                      "control board replacement history"],
        "tv": ["full-white + full-dark screens (backlight bands, burn-in)",
                "HDMI test with YOUR device", "ask hours-of-use"],
    }[category]

    return {
        "category": category,
        "risk": risk,
        "typical_life_yr": life,
        "fair_band": [lo_band, hi_band],
        "asking": asking,
        "verdict": verdict,
        "killer_failures": killers,
        "inspection_priority": inspection,
        "notes": [
            "photo the model/serial plate; decode manufacture date from serial",
            "new braided water hoses on any washer install ($20) - never reuse old ones",
            "price the install: gas hookup / 240V / water line / anti-tip bracket",
            "untested machines: max 60% of age value, budget a diagnostic visit",
        ],
    }


def main():
    p = argparse.ArgumentParser(description="Used appliance deal checker")
    p.add_argument("--demo", action="store_true")
    p.add_argument("--category", choices=sorted(CATS))
    p.add_argument("--age-years", type=float)
    p.add_argument("--asking", type=float)
    p.add_argument("--condition", choices=sorted(CONDITION), default="good")
    p.add_argument("--new-price", type=float, help="if you know the new price of this model")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    if a.demo:
        r = check("front-washer", 5, 275, "good", 900)
    elif a.category and a.age_years is not None and a.asking is not None:
        r = check(a.category, a.age_years, a.asking, a.condition, a.new_price)
    else:
        p.error("need --category --age-years --asking (or --demo)")

    if a.json:
        print(json.dumps(r, indent=2)); return
    print(f"{r['category']} | category risk: {r['risk']} | typical life {r['typical_life_yr']} yr")
    print(f"Fair band: ${r['fair_band'][0]} - ${r['fair_band'][1]} | asking ${r['asking']}")
    print(f"VERDICT: {r['verdict']}")
    print("Killer failures:")
    for k in r["killer_failures"]:
        print(f"  x {k}")
    print("Inspection priority (15 min):")
    for s in r["inspection_priority"]:
        print(f"  -> {s}")
    print("Notes:")
    for s in r["notes"]:
        print(f"  - {s}")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        pass
