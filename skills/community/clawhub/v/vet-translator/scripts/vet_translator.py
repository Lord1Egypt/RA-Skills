#!/usr/bin/env python3
"""
vet-translator — decode vet notes and lab panels into plain language.

Subcommands: explain | labs | trend | ckd | demo

Educational interpretation only — not a diagnosis. Confirm with a veterinarian.
"""
import argparse
import re
import sys

# ── Veterinary shorthand glossary ───────────────────────────────────────────
ABBREVIATIONS = {
    "hx": ("history", "what the patient came in with / past medical background"),
    "s/p": ("status post", "has already had this procedure in the past"),
    "ovh": ("ovariohysterectomy (spay)", "uterus and ovaries surgically removed"),
    "mc": ("male castrated", "male, neutered"),
    "mn": ("male neutered", "male, neutered"),
    "fs": ("female spayed", "female, spayed"),
    "bar": ("bright, alert, responsive", "acting normally — good sign"),
    "qar": ("quiet, alert, responsive", "slightly subdued but aware"),
    "mm": ("mucous membranes (gums)", "gum color/moisture shows hydration and circulation"),
    "bcs": ("body condition score", "1-9 fatness scale; 4-5 is ideal"),
    "wnl": ("within normal limits", "nothing abnormal found"),
    "nsf": ("no significant findings", "nothing important found"),
    "r/o": ("rule out", "the vet is considering this as a possible diagnosis"),
    "dx": ("diagnosis", "what the vet concluded"),
    "ddx": ("differential diagnoses", "the list of possible causes being considered"),
    "sx": ("surgery", "surgical procedure"),
    "tx": ("treatment", "therapy given or planned"),
    "rx": ("prescription", "medication prescribed"),
    "px": ("prognosis", "expected outcome"),
    "npo": ("nothing by mouth", "no food or water for a period"),
    "prn": ("as needed", "give only when symptoms appear"),
    "bid": ("twice daily", "morning and evening"),
    "tid": ("three times daily", "three doses a day"),
    "sid": ("once daily", "one dose a day"),
    "qid": ("four times daily", "four doses a day"),
    "q4h": ("every 4 hours", "dosing interval"),
    "q8h": ("every 8 hours", "dosing interval"),
    "q12h": ("every 12 hours", "dosing interval"),
    "wks": ("weeks", "time period"),
    "wk": ("week", "time period"),
    "au": ("both ears", "problem present in both ears"),
    "ad": ("right ear", "auris dextra"),
    "as": ("left ear", "auris sinistra"),
    "od": ("right eye", "oculus dexter"),
    "os": ("left eye", "oculus sinister"),
    "ou": ("both eyes", "oculi uterque"),
    "v/d": ("vomiting and diarrhea", "classic GI sign pair"),
    "an": ("anorexia (not eating)", "loss of appetite — veterinary sense, not the human eating disorder"),
    "ckd": ("chronic kidney disease", "long-term kidney function loss, staged by IRIS"),
    "crf": ("chronic renal failure", "older term for CKD"),
    "dm": ("diabetes mellitus", "sugar diabetes"),
    "ibd": ("inflammatory bowel disease", "chronic GI inflammation"),
    "utd": ("up to date", "vaccines current"),
    "felv": ("feline leukemia virus", "contagious cat retrovirus"),
    "fiv": ("feline immunodeficiency virus", "cat immunodeficiency retrovirus"),
    "pkd": ("polycystic kidney disease", "inherited kidney cysts — Persians and relatives"),
    "pe": ("physical exam", "hands-on checkup"),
    "rads": ("radiographs (X-rays)", "imaging"),
    "usg": ("urine specific gravity", "urine concentration; dilute urine + kidney markers is a CKD pattern"),
    "upc": ("urine protein:creatinine ratio", "kidney protein leakage"),
    "sb": ("small bowel", "diarrhea pattern (small intestine origin)"),
    "lb": ("large bowel", "diarrhea pattern with mucus/fresh blood, straining"),
    "wt": ("weight", "body weight"),
    "mcg": ("microgram", "0.001 mg — dose unit"),
    "cbc": ("complete blood count", "red cells, white cells, platelets"),
    "chem": ("chemistry panel", "organ-function blood tests"),
    "po": ("by mouth", "oral route"),
    "sq": ("subcutaneous (under skin)", "injection route; also at-home fluid therapy"),
    "sc": ("subcutaneous (under skin)", "injection route"),
    "iv": ("intravenous", "into a vein"),
    "im": ("intramuscular", "into a muscle"),
    "bp": ("blood pressure", "hypertension complicates CKD, especially in cats"),
    "ecg": ("electrocardiogram", "heart rhythm tracing"),
    "echo": ("echocardiogram", "heart ultrasound"),
    "mets": ("metastases", "cancer spread"),
    "otitis": ("ear inflammation/infection", "common in floppy-eared dogs"),
    "pyoderma": ("bacterial skin infection", "skin disease"),
    "atopy": ("environmental allergy", "itchy skin from pollens etc."),
    "flutd": ("feline lower urinary tract disease", "urinary trouble in cats"),
    "cysto": ("cystocentesis", "urine drawn from the bladder with a needle"),
    "hyperthyroid": ("overactive thyroid", "common older-cat disease: weight loss + big appetite"),
    "hypothyroid": ("underactive thyroid", "common middle-aged-dog disease: weight gain + lethargy"),
    "recheck": ("recheck appointment", "repeat exam/tests to see direction"),
    "ausr": ("aural (ear) — right", "right ear"),
    "glucometer": ("blood glucose meter", "home glucose monitoring"),
    "curbside": ("curbside drop-off", "staff takes the pet inside without the owner"),
}

# ── Lab reference ranges: marker -> species -> (low, high, unit, meaning, why)
LABS = {
    "CREA": {
        "dog": (0.5, 1.8, "mg/dL", "creatinine — muscle metabolism waste filtered by kidneys",
                "main kidney function marker; IRIS staging anchor"),
        "cat": (0.8, 2.4, "mg/dL", "creatinine — kidney-filtered waste",
                "main kidney function marker; IRIS staging anchor"),
        "quirks": "Greyhounds and other sighthounds normally run 1.5-2.1; healthy sled dogs similar. Persian cats: consider PKD.",
    },
    "SDMA": {
        "dog": (0, 14, "ug/dL", "symmetric dimethylarginine — newer kidney function marker",
                "rises earlier than creatinine; sensitive early-kidney signal"),
        "cat": (0, 14, "ug/dL", "symmetric dimethylarginine",
                "rises earlier than creatinine in cats"),
    },
    "BUN": {
        "dog": (16, 36, "mg/dL", "blood urea nitrogen — protein metabolism waste",
                "kidney + hydration + diet marker; less specific than CREA/SDMA"),
        "cat": (16, 36, "mg/dL", "blood urea nitrogen",
                "kidney + hydration marker; rises with GI bleeding and high-protein meals too"),
    },
    "ALT": {
        "dog": (10, 100, "U/L", "alanine aminotransferase — liver cell enzyme",
                "leaks when liver cells are damaged"),
        "cat": (10, 100, "U/L", "alanine aminotransferase",
                "liver cell damage marker in cats"),
    },
    "ALP": {
        "dog": (23, 212, "U/L", "alkaline phosphatase — bile duct / bone enzyme",
                "cholestasis marker; also bone growth (young dogs) and steroid effect"),
        "cat": (9, 80, "U/L", "alkaline phosphatase",
                "in cats even mild elevations matter more — short ALP half-life"),
    },
    "GLU": {
        "dog": (70, 143, "mg/dL", "glucose",
                "high = diabetes or stress; low = insulinoma/starvation/xylitol"),
        "cat": (71, 148, "mg/dL", "glucose",
                "stress hyperglycemia is common in cats — one high reading does not equal diabetes"),
    },
    "TP": {
        "dog": (5.2, 8.2, "g/dL", "total protein", "hydration + immune + liver protein status"),
        "cat": (5.7, 8.9, "g/dL", "total protein", "dehydration and chronic inflammation raise it"),
    },
    "ALB": {
        "dog": (2.3, 4.0, "g/dL", "albumin — liver-made protein",
                "low = liver, kidney loss, GI loss, or malnutrition"),
        "cat": (2.4, 4.0, "g/dL", "albumin", "chronic illness marker when low"),
    },
    "WBC": {
        "dog": (5.0, 16.0, "x10^3/uL", "white blood cell count",
                "infection/inflammation high; some viral or marrow disease low"),
        "cat": (3.5, 16.0, "x10^3/uL", "white blood cell count", "infection/inflammation marker"),
    },
    "HCT": {
        "dog": (37, 61, "%", "hematocrit — red blood cell fraction",
                "anemia when low; dehydration when high"),
        "cat": (26, 48, "%", "hematocrit",
                "anemia marker; GI bleed, kidney disease (low EPO), fleas"),
    },
    "PLT": {
        "dog": (170, 400, "x10^3/uL", "platelets — clotting cells",
                "low = clotting risk; immune destruction, tick disease, DIC"),
        "cat": (175, 500, "x10^3/uL", "platelets", "low = clotting risk"),
        "quirks": "Greyhounds normally run 80-120+; do not panic at 110 in a sighthound.",
    },
    "T4": {
        "cat": (0.8, 4.7, "ug/dL", "thyroxine — thyroid hormone",
                "HIGH in feline hyperthyroidism; LOW fits canine hypothyroidism"),
        "dog": (0.8, 4.7, "ug/dL", "thyroxine",
                "low = hypothyroidism (weight gain, lethargy, poor coat)"),
        "quirks": "Cats: stress and non-thyroid illness distort T4 both ways; confirm with free T4/TSH.",
    },
    "USG": {
        "dog": (1.015, 1.045, "sg", "urine specific gravity — concentration",
                "kidneys' ability to concentrate urine; CKD makes urine dilute"),
        "cat": (1.015, 1.060, "sg", "urine specific gravity",
                "cats concentrate better than dogs; dilute + kidney markers = CKD pattern"),
    },
    "UPC": {
        "dog": (0.0, 0.5, "ratio", "urine protein:creatinine",
                "kidney protein leakage; >0.5 dogs / >0.4 cats = proteinuric"),
        "cat": (0.0, 0.4, "ratio", "urine protein:creatinine",
                "proteinuria speeds CKD progression; a treatment target"),
    },
    "PHOS": {
        "dog": (2.1, 9.0, "mg/dL", "phosphorus",
                "rises in CKD as kidneys fail to excrete"),
        "cat": (2.4, 8.2, "mg/dL", "phosphorus",
                "CKD progression marker; controlling phosphate extends life in CKD cats"),
    },
    "CA": {
        "dog": (8.9, 11.4, "mg/dL", "calcium", "bone, parathyroid, kidney, some cancers affect it"),
        "cat": (8.2, 10.8, "mg/dL", "calcium", "high calcium in cats: think lymphoma, parathyroid"),
    },
}

# importance weights for sorting findings
WEIGHTS = {"SDMA": 3, "CREA": 3, "T4": 3, "PHOS": 2, "BUN": 2, "UPC": 2, "ALB": 2, "USG": 2}

# IRIS CKD staging creatinine thresholds (mg/dL)
IRIS = {
    "cat": {"STAGE1": (0.0, 1.6), "STAGE2": (1.6, 2.8), "STAGE3": (2.8, 5.0), "STAGE4": (5.0, 999.0)},
    "dog": {"STAGE1": (0.0, 1.4), "STAGE2": (1.4, 2.0), "STAGE3": (2.0, 5.0), "STAGE4": (5.0, 999.0)},
}

SIGHTHOUNDS = {"greyhound", "saluki", "whippet", "borzoi", "afghan hound", "italian greyhound", "deerhound"}


def evaluate_marker(marker, value, species, breed=None):
    m = LABS.get(marker.upper())
    if not m:
        return None
    spec = m.get(species)
    if not spec:
        return None
    low, high, unit, meaning, why = spec
    # Breed-adjusted ranges for sighthounds (from LABS quirks)
    breed_adjusted = False
    if breed and breed.lower() in SIGHTHOUNDS:
        if marker.upper() == "CREA":
            low, high = 0.8, 2.1
            breed_adjusted = True
        elif marker.upper() == "PLT":
            low, high = 80, 400
            breed_adjusted = True
    verdict = "NORMAL"
    if value < low:
        verdict = "LOW"
    elif value > high:
        verdict = "HIGH"
    if breed and breed.lower() in SIGHTHOUNDS and m.get("quirks"):
        if marker.upper() == "CREA" and 1.5 <= value <= 2.1 and verdict == "HIGH":
            verdict = "NORMAL (breed-adjusted)"
        if marker.upper() == "PLT" and 80 <= value < low:
            verdict = "NORMAL (breed-adjusted)"
    if breed_adjusted and verdict == "NORMAL":
        verdict = "NORMAL (breed-adjusted)"
    rng = high - low if high > low else 1.0
    if verdict == "NORMAL" and (high - value) <= rng * 0.10:
        verdict = "BORDERLINE-HIGH"
    elif verdict == "NORMAL" and (value - low) <= rng * 0.10:
        verdict = "BORDERLINE-LOW"
    return {
        "marker": marker.upper(), "value": value, "unit": unit,
        "ref": f"{low}-{high}", "verdict": verdict, "meaning": meaning, "why": why,
        "quirks": m.get("quirks", ""),
        "weight": WEIGHTS.get(marker.upper(), 1),
    }


def parse_results(text):
    markers_re = "|".join(re.escape(k) for k in LABS)
    found = []
    for m in re.finditer(rf"({markers_re})\s*[:=]?\s*([0-9]+(?:\.[0-9]+)?)", text, re.IGNORECASE):
        found.append({"marker": m.group(1).upper(), "value": float(m.group(2))})
    return found


def trend_analysis(marker, series, species=None):
    vals = [v for _, v in series]
    m = LABS.get(marker.upper())
    ref = (m[species][0], m[species][1]) if m and species else None
    deltas = [round(vals[i] - vals[i - 1], 2) for i in range(1, len(vals))]
    up = all(d > 0 for d in deltas)
    down = all(d < 0 for d in deltas)
    direction = "rising" if up else "falling" if down else "fluctuating"
    total_change = round(vals[-1] - vals[0], 2)
    pct = round(100.0 * (vals[-1] - vals[0]) / vals[0], 1) if vals[0] else None
    in_range_now = bool(ref and ref[0] <= vals[-1] <= ref[1])
    drift = False
    if ref and vals[0] >= ref[0] and len(vals) >= 2:
        drift = abs(vals[-1] - vals[0]) / max(vals[0], 1e-6) >= 0.25
    interp = f"{marker.upper()} moving {direction}: {vals[0]} -> {vals[-1]}"
    if pct is not None:
        interp += f" ({pct:+.1f}%)"
    interp += ". "
    if drift and in_range_now:
        interp += ("Still inside reference range, but a sustained >=25% drift deserves a vet "
                   "conversation — early disease hides inside 'normal'.")
    elif not in_range_now:
        interp += "Outside reference range at the latest point — discuss with your vet."
    else:
        interp += "No significant drift."
    return {"marker": marker.upper(), "series": series, "direction": direction,
            "deltas": deltas, "total_change": total_change, "pct_change": pct,
            "last_in_range": in_range_now, "drift_alert": drift,
            "interpretation": interp}


def iris_stage(species, crea, sdma=None, upc=None, bp=None):
    thresholds = IRIS[species]
    stage = "STAGE4"
    for name in ("STAGE1", "STAGE2", "STAGE3", "STAGE4"):
        lo, hi = thresholds[name]
        if lo <= crea < hi:
            stage = name
            break
    substages = []
    if upc is not None:
        cut = 0.4 if species == "cat" else 0.5
        substages.append(("proteinuria", "proteinuric" if upc > cut else "non-proteinuric"))
    if bp is not None:
        if bp < 140:
            sub = "normotensive"
        elif bp < 160:
            sub = "borderline hypertensive"
        elif bp < 180:
            sub = "hypertensive"
        else:
            sub = "severe hypertensive"
        substages.append(("blood pressure", sub))
    return {"stage": stage, "substages": substages}


def parse_series(text):
    out = []
    for part in text.split(","):
        part = part.strip()
        if not part:
            continue
        if ":" in part:
            label, val = part.split(":", 1)
            out.append((label.strip(), float(val)))
        else:
            out.append(("", float(part)))
    return out


FLAGS = {"LOW": "v", "HIGH": "^", "NORMAL": "ok", "BORDERLINE-HIGH": "~",
         "BORDERLINE-LOW": "~", "NORMAL (breed-adjusted)": "ok"}


def explain_text(text):
    decoded = []
    # split on whitespace and punctuation EXCEPT within known shorthand that
    # contains punctuation (r/o, s/p, v/d, q4h...) — check both the raw token
    # and punctuation-stripped forms against the glossary
    raw_tokens = re.split(r"[\s,;()]+", text)
    for tok in raw_tokens:
        tok = tok.strip().rstrip(".")
        if not tok:
            continue
        candidates = [tok, tok.lower()]
        # also try splitting on / and . to catch "r/o:" style trailing bits
        for t in candidates:
            if t in ABBREVIATIONS:
                exp, why = ABBREVIATIONS[t]
                if exp:
                    decoded.append((tok, exp, why))
                break
    return decoded


def cmd_explain(args):
    species = (args.species or "dog").lower()
    decoded = explain_text(args.text)
    results = parse_results(args.text)
    evals = [e for e in (evaluate_marker(r["marker"], r["value"], species, args.breed)
                         for r in results) if e]
    evals.sort(key=lambda e: (-e["weight"], e["marker"]))
    print("PLAIN-LANGUAGE DECODE")
    print("=" * 60)
    if decoded:
        print("Terms explained:")
        for orig, exp, why in decoded[:40]:
            print(f"  {orig:<14} -> {exp}. ({why})")
    else:
        print("No known shorthand terms found.")
    print()
    if evals:
        print("Embedded lab results (importance order):")
        for e in evals:
            print(f"  [{FLAGS.get(e['verdict'], '-')}] {e['marker']:<6} {e['value']:g} {e['unit']:<9} ref {e['ref']:<11} {e['verdict']}")
            print(f"        what: {e['meaning']}")
            if e["verdict"] != "NORMAL":
                print(f"        why:  {e['why']}")
            if e["quirks"] and (args.breed or "").lower() in SIGHTHOUNDS:
                print(f"        breed: {e['quirks']}")
    print()
    print("Educational interpretation, not a diagnosis. Confirm with your veterinarian.")
    return 0


def cmd_labs(args):
    species = args.species.lower()
    results = parse_results(args.results)
    if not results:
        print("No recognizable results. Use e.g. --results 'CREA 2.8, BUN 38'.")
        return 1
    evals = [e for e in (evaluate_marker(r["marker"], r["value"], species, args.breed)
                         for r in results) if e]
    if not evals:
        print("Recognized markers but no species table. Known markers:")
        print(", ".join(sorted(LABS)))
        return 1
    evals.sort(key=lambda e: (-e["weight"], e["marker"]))
    title = f"LAB EVALUATION — {species}"
    if args.breed:
        title += f" ({args.breed})"
    print(title)
    print("=" * 60)
    concerns = 0
    for e in evals:
        print(f"  [{FLAGS.get(e['verdict'], '-')}] {e['marker']:<6} {e['value']:g} {e['unit']:<9} ref {e['ref']:<11} {e['verdict']}")
        if e["verdict"] not in ("NORMAL", "NORMAL (breed-adjusted)"):
            concerns += 1
            print(f"        {e['why']}")
    print()
    if concerns == 0:
        tail = " and breed" if args.breed else ""
        print(f"All evaluated markers normal for this species{tail}.")
    else:
        print(f"{concerns} marker(s) outside reference range — discuss with your vet.")
    print("Educational interpretation only — not a diagnosis. Confirm with your veterinarian.")
    return 0


def cmd_trend(args):
    series = parse_series(args.series)
    if len(series) < 2:
        print("Need >= 2 points. Format: '2024-01:10,2024-07:14'.")
        return 1
    t = trend_analysis(args.marker, series, (args.species or "").lower() or None)
    print(f"TREND — {t['marker']} ({args.species or 'species not set'})")
    print("=" * 60)
    for label, val in series:
        print(f"  {label:<12} {val:g}")
    print()
    print(f"  direction:     {t['direction']}")
    tail = f" ({t['pct_change']:+.1f}%)" if t["pct_change"] is not None else ""
    print(f"  total change:  {t['total_change']:+g}{tail}")
    print(f"  last in range: {'yes' if t['last_in_range'] else 'no'}")
    if t["drift_alert"]:
        print("  ! DRIFT ALERT: sustained >=25% move — early disease hides inside 'normal'.")
    print()
    print(t["interpretation"])
    print("Educational interpretation only — confirm with your veterinarian.")
    return 0


def cmd_ckd(args):
    species = args.species.lower()
    s = iris_stage(species, args.crea, args.sdma, args.upc, args.bp)
    print(f"IRIS CKD STAGING — {species}, creatinine {args.crea} mg/dL")
    print("=" * 60)
    print(f"  Stage: {s['stage']}")
    lo, hi = IRIS[species][s["stage"]]
    print(f"  ({s['stage']} covers creatinine {lo}-{hi} mg/dL for {species})")
    if args.sdma is not None:
        note = "supports kidney involvement" if args.sdma > 14 else "not elevated"
        print(f"  SDMA {args.sdma}: {note}")
    for label, verdict in s["substages"]:
        print(f"  {label}: {verdict}")
    print()
    print("  What the stage means:")
    print("    STAGE1 — kidney damage present, function preserved (creatinine normal).")
    print("    STAGE2 — mild functional loss (the 'silent' stage most cats are caught in).")
    print("    STAGE3 — moderate loss; diet and phosphate control matter most here.")
    print("    STAGE4 — severe loss; referral-level care usually discussed.")
    print()
    print("  Questions for your vet:")
    qs = [
        "Should we recheck creatinine + SDMA in 2-4 weeks to confirm staging (stable vs acute)?",
        "Is a kidney-support (phosphate-restricted) diet indicated at this stage?",
        "Would you check urine protein (UPC) and blood pressure if not already done?",
    ]
    if s["stage"] in ("STAGE3", "STAGE4"):
        qs.append("Are potassium and phosphorus being monitored? Should we discuss phosphate binders?")
    if args.bp is not None and args.bp >= 160:
        qs.append("Blood pressure is elevated — should we start BP medication?")
    for q in qs:
        print(f"    - {q}")
    print()
    print("Educational interpretation using published IRIS guidelines — not a diagnosis.")
    return 0


def cmd_demo(args):
    print("=== DEMO 1: cat discharge note with labs ===")
    cmd_explain(argparse.Namespace(
        text=("Barney, 12y MC cat. Hx weight loss. BCS 5/9. CBC WNL. "
              "Chem: BUN 38, CREA 2.8, SDMA 28, ALT 92. USG 1.014. r/o CKD; recheck in 4 wks."),
        species="cat", breed=None))
    print()
    print("=== DEMO 2: greyhound panel — breed quirk demo ===")
    cmd_labs(argparse.Namespace(
        results="CREA 1.7 mg/dL, PLT 118, ALP 210", species="dog", breed="greyhound"))
    print()
    print("=== DEMO 3: SDMA drift across a year ===")
    cmd_trend(argparse.Namespace(
        marker="SDMA", species="cat",
        series="2024-01:10,2024-07:14,2025-01:19,2025-07:26"))
    print()
    print("=== DEMO 4: IRIS staging ===")
    cmd_ckd(argparse.Namespace(species="cat", crea=2.8, sdma=28, upc=0.4, bp=150))


def main():
    p = argparse.ArgumentParser(description="vet-translator: decode vet notes and lab panels")
    sub = p.add_subparsers(dest="cmd")
    e = sub.add_parser("explain", help="translate a narrative vet note")
    e.add_argument("--text", required=True)
    e.add_argument("--species", help="cat or dog (default dog)")
    e.add_argument("--breed", help="e.g. greyhound — enables breed-aware ranges")
    l = sub.add_parser("labs", help="evaluate a results list")
    l.add_argument("--results", required=True, help="'CREA 2.8, BUN 38'")
    l.add_argument("--species", required=True, choices=["cat", "dog"])
    l.add_argument("--breed")
    t = sub.add_parser("trend", help="one marker across visits")
    t.add_argument("--marker", required=True)
    t.add_argument("--species")
    t.add_argument("--series", required=True, help="'2024-01:10,2024-07:14'")
    c = sub.add_parser("ckd", help="IRIS CKD staging")
    c.add_argument("--species", required=True, choices=["cat", "dog"])
    c.add_argument("--crea", required=True, type=float)
    c.add_argument("--sdma", type=float)
    c.add_argument("--upc", type=float)
    c.add_argument("--bp", type=float)
    sub.add_parser("demo", help="run built-in scenarios")
    args = p.parse_args()
    if args.cmd == "explain":
        return cmd_explain(args)
    if args.cmd == "labs":
        return cmd_labs(args)
    if args.cmd == "trend":
        return cmd_trend(args)
    if args.cmd == "ckd":
        return cmd_ckd(args)
    if args.cmd == "demo":
        return cmd_demo(args)
    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
