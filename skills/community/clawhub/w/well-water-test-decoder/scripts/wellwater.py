#!/usr/bin/env python3
"""Well Water Test Decoder — lab-report decode against EPA MCL/secondary
standards, symptom fingerprinting, test-panel ordering, and treatment
sequencing with price bands + oversell guard. Stdlib only."""
import argparse

# name: (health limit or None, unit, secondary limit or None)
PARAMS = {
    "nitrate":   (10.0, "mg/L", None),
    "arsenic":   (10.0, "µg/L", None),
    "lead":      (15.0, "µg/L", None),
    "iron":      (None, "mg/L", 0.3),
    "manganese": (0.12, "mg/L", 0.05),
    "hardness":  (None, "mg/L", 120.0),
    "ph":        (None, "pH", None),
    "tds":       (None, "mg/L", 500.0),
    "sulfate":   (None, "mg/L", 250.0),
    "chloride":  (None, "mg/L", 250.0),
    "sodium":    (None, "mg/L", None),
}

SYMPTOM_FINGERPRINTS = {
    "blue-green": ("corrosive water (pH<6.5 / low alkalinity) leaching copper",
                   "pH + alkalinity + copper + lead"),
    "brown-red": ("iron >0.3 mg/L (ferrous: clears after standing)",
                  "iron + manganese + pH"),
    "black": ("manganese >0.05 mg/L or iron bacteria",
              "manganese + iron + iron-bacteria slide"),
    "rotten-egg-hot": ("sulfate-reducing bacteria in the water heater: "
                       "magnesium anode reacts with SRB",
                       "no test: swap Mg anode for aluminum-zinc ($30)"),
    "rotten-egg-cold": ("H2S gas / SRB in the well itself",
                        "H2S test + shock chlorination"),
    "musty": ("iron bacteria or surface organics entering the well",
              "coliform + well-cap inspection"),
    "white-scale": ("hardness >120 mg/L", "hardness + TDS"),
    "no-lather": ("hardness binding soap", "hardness"),
    "salty": ("chloride/TDS — road salt, sea proximity, or water softener "
              "backwash issue", "chloride + sodium + TDS"),
    "gi-illness": ("coliform / E. coli / nitrate — send to a LAB, not strips",
                   "bacteria (coliform+E.coli) + nitrate"),
    "metallic": ("iron or low pH corrosion", "iron + pH + copper"),
    "pinhole-leaks": ("aggressive/corrosive water (pH<6.5, low alkalinity, "
                      "high CO2)", "pH + alkalinity + Langelier index"),
}

PANELS = {
    "new-property": ("Full panel + bacteria: coliform/E.coli, nitrate, "
                     "arsenic, lead, iron, manganese, hardness, pH, TDS, "
                     "sulfate, chloride, sodium. $80-150 at state/county "
                     "labs. REQUIRED before closing — results are a "
                     "negotiation item."),
    "annual": ("Coliform + nitrate + (arsenic if ever detected). $30-60. "
               "Coliform is the annual heartbeat test."),
    "symptoms": ("Symptom-driven: see `symptoms` command output for the "
                 "short list; don't pay for the full panel blind."),
    "after-flood": ("Coliform + E.coli + turbidity + any previous hits. "
                    "Shock-chlorinate first, wait 2 weeks, THEN sample; "
                    "run water 15 min before sampling."),
    "infant-home": ("Nitrate + bacteria are the infant-critical pair. "
                    "Nitrate >8 mg/L: use bottled water for formula until "
                    "a certified POU solution is verified."),
}

# treatment sequence price bands (installed, US 2026)
TREATMENTS = {
    "shock": ("shock-chlorination + well-defect fix", 0, 150,
              "coliform/E.coli positive or after flood/well work"),
    "uv": ("UV sterilizer (if bacteria recurring after well fix)",
           800, 1500, "recurring coliform with intact well"),
    "neutralizer": ("calcite/soda-ash pH neutralizer", 800, 1800,
                    "pH < 6.5 — MUST precede softener/iron units"),
    "oxidizer": ("air-injection/greensand oxidizing filter (Fe+Mn)", 900, 2200,
                 "iron >3 ppm or manganese >0.3, or Fe+Mn together"),
    "softener": ("ion-exchange softener sized to grain load", 600, 1500,
                 "hardness >120 mg/L (and iron <=3 ppm only)"),
    "pou-ro": ("point-of-use RO at drinking taps", 200, 600,
               "arsenic/nitrate/lead/TDS at the DRINKING tap only"),
    "poe-ro": ("whole-house RO", 4000, 15000,
               "extreme whole-house TDS/sodium/sulfate ONLY"),
}


def band(low, high):
    return f"${low:,}-${high:,}"


def cmd_decode(a):
    print("DECODING WELL WATER REPORT")
    health_hits, aesthetic_hits, notes = [], [], []

    if a.coliform and a.coliform.lower() not in ("absent", "negative", "0"):
        print("  coliform PRESENT — surface intrusion or well defect.")
        print("    E.coli too? -> DO NOT DRINK; health dept now.")
        print("    Fix: shock-chlorinate + find entry point (cap, casing,")
        print("    grading), then retest. Do not simply filter.")
        health_hits.append("coliform")
    elif a.coliform:
        print("  coliform ABSENT — good. Recheck annually.")

    for key, (mcl, unit, secondary) in PARAMS.items():
        val = getattr(a, key, None)
        if val is None:
            continue
        if key == "ph":
            if val < 6.5:
                print(f"  pH {val} — BELOW RANGE: corrosive water; blue-green")
                print("    stains, leaches lead/copper. Neutralizer first.")
                aesthetic_hits.append(("pH low (corrosive)", "neutralizer"))
            elif val > 8.5:
                print(f"  pH {val} — ABOVE RANGE: scaling, bitter taste;")
                print("    check with health provider if >9.")
                aesthetic_hits.append(("pH high (scaling)", "acid injection"))
            else:
                print(f"  pH {val} — in range (6.5-8.5).")
            continue
        if mcl and val > mcl:
            print(f"  {key} {val} {unit} — OVER HEALTH LIMIT ({mcl}):")
            if key == "nitrate":
                print("    infants <6mo: use bottled water NOW; identify")
                print("    source (septic, farm, feedlot within 100 ft?).")
            elif key == "arsenic":
                print("    chronic carcinogen; POU RO at drinking taps,")
                print("    whole-house if >50 µg/L. Retest to confirm.")
            elif key == "lead":
                print("    usually plumbing + corrosive water: fix pH,")
                print("    replace lead service/solder; flush taps before")
                print("    drinking; POU RO certified for lead.")
            elif key == "manganese":
                print("    above health advisory (children: neuro effects)")
                print("    AND above secondary — oxidizing filter.")
            health_hits.append(key)
            continue
        if secondary and val > secondary:
            mult = val / secondary
            line = f"  {key} {val} {unit} — {mult:.0f}x SECONDARY LIMIT"
            if key == "hardness":
                line += ": HARD"
                print(line)
                print("    scale, soap waste, appliance wear. Not a health")
                print("    issue. Fix: softener (after iron/pH handling).")
                aesthetic_hits.append(("hardness", "softener"))
            elif key == "iron":
                print(line + ": red-brown stains, metallic taste.")
                if val > 3:
                    print("    >3 ppm: oxidizing filter, NOT softener-only")
                    print("    (resin fouls).")
                    aesthetic_hits.append(("iron high", "oxidizer"))
                else:
                    print("    <=3 ppm: softener removes incidentally.")
                    aesthetic_hits.append(("iron low", "softener"))
            elif key == "manganese":
                print(line + ": black stains. Greensand/air filter treats")
                print("    Fe+Mn together.")
                aesthetic_hits.append(("manganese", "oxidizer"))
            else:
                print(line + ".")
                aesthetic_hits.append((key, "filter class per reference"))
            continue
        print(f"  {key} {val} {unit} — fine "
              f"({'< ' + str(mcl) + ' ' + unit if mcl else 'under secondary'})")

    print()
    if health_hits:
        print(f"HEALTH ACTIONS FIRST: {', '.join(health_hits)} — resolve")
        print("these before any aesthetic equipment purchases.")
    else:
        print("No health-limit exceedances in provided parameters.")
    seq = []
    if any("corrosive" in h[0] for h in aesthetic_hits):
        seq.append(("neutralizer", "pH first — protects pipes + downstream resin"))
    if any(h[1] == "oxidizer" for h in aesthetic_hits):
        seq.append(("oxidizer", "iron/manganese before softener"))
    if any(h[0] == "hardness" for h in aesthetic_hits):
        seq.append(("softener", "after iron handled — resin protected"))
    if seq:
        print("\nTREATMENT SEQUENCE (order matters):")
        for i, (t, why) in enumerate(seq, 1):
            name, lo, hi, _ = TREATMENTS[t]
            print(f"  {i}) {name} {band(lo, hi)} — {why}")
        lo = sum(TREATMENTS[t][1] for t, _ in seq)
        hi = sum(TREATMENTS[t][2] for t, _ in seq)
        print(f"  realistic installed total: {band(lo, hi)}")
    print("\nOVERSELL GUARD: whole-house RO is justified ONLY by whole-house")
    print("  TDS/sodium/sulfate extremes. If your issues are hardness/iron/")
    print("  pH/bacteria, the train above does it for a fraction of")
    print(f"  {band(*TREATMENTS['poe-ro'][1:3])}.")


def cmd_symptoms(a):
    seen = set()
    print("SYMPTOM FINGERPRINT")
    for attr in ("stains", "odor", "taste", "corrosion", "health", "other"):
        val = getattr(a, attr)
        if not val:
            continue
        for s in [v.strip().lower() for v in val.split(",")]:
            key = s if s in SYMPTOM_FINGERPRINTS else None
            if key is None:
                aliases = {"pipes": "pinhole-leaks", "leaks": "pinhole-leaks",
                           "hot-only": "rotten-egg-hot",
                           "rotten-egg": "rotten-egg-cold",
                           "sick": "gi-illness", "diarrhea": "gi-illness",
                           "scale": "white-scale", "soap": "no-lather"}
                key = aliases.get(s)
            if key and key not in seen:
                seen.add(key)
                cause, test = SYMPTOM_FINGERPRINTS[key]
                print(f"  '{s}' -> {cause}")
                print(f"           test: {test}")
            elif key is None:
                print(f"  '{s}' -> not recognized; closest fingerprints: "
                      f"{', '.join(list(SYMPTOM_FINGERPRINTS)[:6])}...")
    if not seen:
        print("  no recognized symptoms given. Common ones: blue-green /")
        print("  brown-red / black stains, rotten-egg (hot vs cold!),")
        print("  white-scale, no-lather, pinhole-leaks, gi-illness, salty.")
    print("\nORDER A LAB PANEL from county/state lab — not a free treatment-")
    print("company strip test.")


def cmd_panel(a):
    text = PANELS[a.context]
    print(f"TEST PANEL — context: {a.context}")
    print(f"  {text}")
    print("\n  sampling rules: run water 2-3 min; sample cold tap; sterile")
    print("  bottle for bacteria (lab-provided); ship same day or refrigerate;")
    print("  NEVER sample within 2 weeks of shock-chlorination.")


def cmd_treat(a):
    print("TREATMENT SANITY-CHECK")
    if a.ph is not None and a.ph < 6.5:
        print(f"  pH {a.ph} < 6.5 -> NEUTRALIZER {band(*TREATMENTS['neutralizer'][1:3])}")
        print("     must be FIRST in the train (protects pipes and resin).")
    if a.iron is not None:
        if a.iron > 3:
            print(f"  iron {a.iron} mg/L > 3 -> OXIDIZING FILTER "
                  f"{band(*TREATMENTS['oxidizer'][1:3])}")
            print("     softener-only here = resin fouled within months.")
        elif a.iron > 0.3:
            print(f"  iron {a.iron} mg/L (0.3-3) -> softener handles "
                  "incidentally; no separate unit needed.")
    if a.manganese is not None and a.manganese > 0.3:
        print(f"  manganese {a.manganese} -> oxidizing filter (same unit as "
              "iron if both present).")
    if a.hardness is not None and a.hardness > 120:
        print(f"  hardness {a.hardness} mg/L -> SOFTENER "
              f"{band(*TREATMENTS['softener'][1:3])}, sized to grain load "
              "(see water-softener-sizer doctrine).")
    if a.nitrate is not None and a.nitrate > 8:
        print(f"  nitrate {a.nitrate} near/at MCL -> POU RO "
              f"{band(*TREATMENTS['pou-ro'][1:3])} at drinking tap; infants: "
              "bottled water until verified.")
    if a.arsenic is not None and a.arsenic > 10:
        print(f"  arsenic {a.arsenic} µg/L > MCL -> POU RO certified for As "
              f"{band(*TREATMENTS['pou-ro'][1:3])}; whole-house media if "
              ">50 µg/L. RETEST to confirm before buying.")
    print("\n  guards: bacteria first, pH second, iron third, hardness last.")
    print("  whole-house RO only for extreme whole-house TDS/sodium/sulfate.")
    print("  get itemized quotes; cross-check against bands above.")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("decode", help="decode lab report values")
    for k in PARAMS:
        d.add_argument(f"--{k}", type=float, default=None)
    d.add_argument("--coliform", default=None,
                   help="'absent'/'negative'/'0' or 'present'")
    d.set_defaults(fn=cmd_decode)

    s = sub.add_parser("symptoms", help="symptom fingerprint")
    s.add_argument("--stains", help="e.g. blue-green,brown-red,black")
    s.add_argument("--odor", help="e.g. rotten-egg,rotten-egg-hot,musty")
    s.add_argument("--taste", help="e.g. metallic,salty")
    s.add_argument("--corrosion", help="e.g. pipes,pinhole-leaks")
    s.add_argument("--health", help="e.g. gi-illness,diarrhea")
    s.add_argument("--other")
    s.set_defaults(fn=cmd_symptoms)

    s = sub.add_parser("panel", help="which lab panel to order")
    s.add_argument("--context", choices=sorted(PANELS), default="annual")
    s.set_defaults(fn=cmd_panel)

    t = sub.add_parser("treat", help="treatment sequencing check")
    for k in ("ph", "iron", "manganese", "hardness", "nitrate", "arsenic"):
        t.add_argument(f"--{k}", type=float, default=None)
    t.set_defaults(fn=cmd_treat)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
