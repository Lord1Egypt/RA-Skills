#!/usr/bin/env python3
"""Roof leak emergency response — triage, source tracing, tarp, insurance, drying.

Subcommands:
  triage      First-15-minutes decision tree (electrical, flow class, bulge)
  find        Source-tracing protocol (stain reading, attic trace, hose test)
  tarp        DIY tarp GO/STOP cutoffs + anchoring rules
  insurance   Evidence-first protocol + shot list + call script
  dry         24-48h mold clock: open vs dry vs replace decisions

Stdlib only. Offline. Safety-first: when in doubt, OFF the roof.
"""
import argparse
import json
from datetime import date, timedelta

PITCH_STOP = 6  # /12 — above this, no DIY roof walking


def cmd_triage(a):
    print("TRIAGE — first 15 minutes, in order")
    steps = []
    if a.fixture in ("yes", "y"):
        steps.append((
            "0-3 min", "ELECTRICAL: breaker OFF for the circuit feeding the room",
            "wet fixture + curiosity = shock; water follows wiring through joist bays"))
        steps.append((
            "0-3 min", "Do NOT touch or test the wet fixture/fan/switch until the breaker is off and verified with a lamp",
            "treat the wet zone as live — fixtures pool water in the canopy"))
    steps.append((
        "3-5 min", f"CONTAIN: bucket under the drip + towels + plastic sheet on the floor",
        "stop the spreading damage; every liter caught is a liter not in the flooring"))
    if a.bulge in ("yes", "y"):
        steps.append((
            "5-10 min", "RELEASE THE BULGE deliberately: screwdriver at the LOWEST point, bucket under it, you to the side",
            "a bulge is pooled water; it WILL let go — on your terms or its own"))
    if a.flow in ("stream", "pouring"):
        steps.append((
            "immediately", "HIGH FLOW: this is a professional-now event — emergency roofer call while you contain; move furniture OUT of the room",
            "stream/pouring means open decking or a failed flashing — no DIY fixes that size at night"))
    steps.append((
        "10-15 min", "PHOTOGRAPH everything BEFORE further mitigation (see insurance)",
        "the scene erases its own evidence as you fix it"))
    for when, what, why in steps:
        print(f"[{when}] {what}")
        print(f"        WHY: {why}")
    print()
    print(f"STRUCTURAL: ceiling sagging >5cm or cracking sounds -> clear the room")
    print("and stay out. Collapse-class, not DIY-class.")
    verdict = "CONTAIN + TRACE" if a.flow in ("drip",) else "CONTAIN + PROFESSIONAL NOW"
    print(f"VERDICT: {verdict}")
    return {"steps": len(steps), "verdict": verdict}


SUSPECTS = [
    ("Chimney / dormer / wall flashing", "any roof penetration at a vertical wall", 0.30),
    ("Valley (two roof planes meet)", "stain near an inside corner of the house", 0.20),
    ("Plumbing stack / vent collar", "bath/kitchen wet, often ring-stains after rain", 0.15),
    ("Missing/damaged shingle tabs", "visible from ground after wind/hail", 0.12),
    ("Skylight (frame/curb flashing)", "stain concentrates around the opening", 0.10),
    ("Nail backs / fastener pattern", "damp attic with drips at nail points, cold season", 0.05),
    ("Ice dam at eave", "winter, stain near exterior wall top, freeze-thaw", 0.08),
]


def cmd_find(a):
    print("SOURCE TRACE — the drip point is a coordinate, not the answer")
    print()
    print("STAIN READING")
    for line in (
        "  wet growing edge = ACTIVE; dry brown ring = old episode; many rings = repeating",
        "  soft/spongy drywall = saturated; measure stain diameter for the record",
    ):
        print(line)
    print()
    if a.attic in ("yes", "y", "accessible"):
        print("ATTIC TRACE (preferred — answers live above the ceiling)")
        for line in (
            "  1. Headlamp + phone camera + chalk; mark the ceiling spot from below first",
            "  2. Walk ONLY joists/trusses — wet drywall is not a floor",
            "  3. Follow the wet sheathing UP-hill: darker ply, beads, drips",
            "  4. Chalk the wet zone; photograph WITH the roof feature in frame",
            "  5. Pull a batt: water pools under insulation against the ceiling",
        ):
            print(line)
    else:
        print("ATTIC NOT ACCESSIBLE -> exterior-first: binocular/phone-zoom scan of")
        print("penetrations and valleys from the ground; hose test tomorrow if dry.")
    print()
    print("USUAL SUSPECTS (prior by your geometry)")
    for name, tell, _ in sorted(SUSPECTS, key=lambda s: -s[2]):
        print(f"  {name:<34} tell: {tell}")
    print()
    print("HOSE TEST (tomorrow, dry roof, two people): water LOW on the suspect")
    print("feature 5 min at a time, working up-hill; spotter inside watches. Never alone.")
    return {"suspects": len(SUSPECTS)}


def cmd_tarp(a):
    pitch = a.pitch or 0
    stop = []
    if a.rain in ("yes", "y"):
        stop.append("rain still falling — wet roof is a no-walk surface")
    if a.dark in ("yes", "y"):
        stop.append("dark — night roof work multiplies fall risk")
    if pitch and pitch > PITCH_STOP:
        stop.append(f"pitch {pitch}/12 > {PITCH_STOP}/12 cutoff")
    if a.stories and a.stories >= 2:
        stop.append(f"{a.stories} stories — emergency roofer territory for DIY night work")
    if stop:
        print("TARP DECISION: STOP — do NOT get on this roof now")
        for s in stop:
            print(f"  - {s}")
        print()
        print("INSTEAD (in priority order):")
        for line in (
            "  1. ATTIC routing: plastic sheet draped to funnel water into a bucket",
            "  2. Interior catch station reinforced (bucket + towels + plastic)",
            "  3. Emergency roofer called NOW (storm crews tarp professionally)",
            "  4. If none available tonight: document and contain; reassess at dawn",
        ):
            print(line)
        verdict = "INTERIOR CONTAINMENT"
    else:
        print("TARP DECISION: GO — with the anchor rules")
        for line in (
            "  - Extend 1m+ past damage every direction; ridge-side edge goes UNDER",
            "    the course above (water-shedding overlap, upper OVER lower)",
            "  - Anchor: furring strips along edges + weighted 2x4 over the ridge",
            "  - NEVER nail through shingles — each hole is a new leak",
            "  - Harness/anchor above 6 ft; never work alone; phone in pocket",
            "  - Pooling on the tarp = re-pitch it before it finds the edge",
        ):
            print(line)
        verdict = "DIY TARP OK"
    print()
    print(f"FALL MATH: emergency roofers exist because 'quick night fix' falls are")
    print(f"worse than any water damage. When any STOP fires, that IS the plan.")
    return {"verdict": verdict, "stop_reasons": stop}


def cmd_insurance(a):
    print("INSURANCE / LANDLORD — evidence FIRST, mitigation second, repair LAST")
    print()
    print("PHOTO SHOT LIST (timestamps ON, before touching anything)")
    for i, s in enumerate((
        "wide exterior + storm context (branch, hail-line, gutter)",
        "room wide, then stain close-up with tape measure for scale",
        "30s video of the active drip — narrate the date",
        "attic: wet path, chalk marks, suspect feature in frame",
        "EVERY mitigation step repeated after (tarp placed, batts pulled)",
    ), 1):
        print(f"  {i}. {s}")
    print()
    if a.country == "us":
        print("CALL SCRIPT (insurer first-notice)")
        for line in (
            "  'Sudden water intrusion through the ceiling during [storm/date].",
            "  I have photos/video. I am doing emergency mitigation — tarp and",
            "  drying — and will keep all receipts. I need a claim number and an",
            "  adjuster timeline BEFORE any permanent repairs.'",
        ):
            print(line)
        print()
        print("LINES THAT MATTER")
        for line in (
            "  - 'Sudden' is the coverage trigger word; don't volunteer 'it's been",
            "    dripping for months' before the adjuster classifies",
            "  - Mitigation is REQUIRED and reimbursable (keep receipts)",
            "  - Permanent repair before adjuster = jeopardized claim",
            "  - Wind/hail deductible is often %-of-value (2-5%), not flat $",
        ):
            print(line)
    else:
        print("Non-US: same evidence discipline; check policy excess and the insurer's")
        print("approved-contractor list — using it speeds payment, read the terms.")
    print()
    print("RENTERS: written notice to landlord TODAY (photo of the sent message);")
    print("your renters policy covers belongings + displacement, not the building.")
    return {"shot_list": 5}


def cmd_dry(a):
    print("DRYING — the 24-48h mold clock starts NOW")
    print()
    if a.wet_insulation in ("yes", "y"):
        print("WET INSULATION ABOVE THE CEILING -> OPEN IT")
        for line in (
            "  - Fiberglass batts: pull, bag, seal, carry out IN the bags",
            "  - Wet batts never recover R-value; cellulose compacts + molds",
            "  - Drywall over a wet void is an incubator: cut it open over the",
            "    wet zone (this is mitigation, photograph before each cut)",
        ):
            print(line)
    else:
        print("No wet insulation reported: surface-dry protocol — fans + dehumidifier,")
        print("daily readings, but verify the void above is actually dry (meter).")
    print()
    print("EQUIPMENT MATH")
    for line in (
        "  - 1 LGR dehumidifier per ~40 m2 of affected area, room closed",
        "  - Air movers ACROSS wet surfaces (not into open doorways)",
        "  - Target: drywall <=15% moisture, 2 consecutive stable days",
    ):
        print(line)
    print()
    print("DISPOSITION TABLE")
    for item, verdict in (
        ("Fiberglass batt (wet)", "REPLACE"),
        ("Cellulose (wet)", "REPLACE"),
        ("Drywall, structurally sound, dries <48h", "SAVE + stain-block paint"),
        ("Drywall, soft/spongy/crumbled", "REPLACE (cut 30cm past visible damage)"),
        ("Ceiling tile (wet)", "REPLACE"),
        ("Carpet padding (wet)", "REPLACE"),
        ("Framing lumber (wet)", "DRY + meter-verify (usually salvageable)"),
    ):
        print(f"  {item:<38} {verdict}")
    print()
    print("ESCALATE TO REMEDIATION IF: 48h wet elapsed, >1 m2 suspected mold,")
    print("musty smell persists, anyone at home has respiratory issues.")
    print("CLOSE ONLY AFTER: readings stable-dry + smell gone + ENTRY FIXED.")
    return {"clock": "24-48h"}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("triage")
    sp.add_argument("--fixture", default="no", choices=["yes", "no", "y", "n"])
    sp.add_argument("--flow", default="drip", choices=["drip", "stream", "pouring"])
    sp.add_argument("--bulge", default="no", choices=["yes", "no", "y", "n"])
    sp.set_defaults(fn=cmd_triage)

    sp = sub.add_parser("find")
    sp.add_argument("--attic", default="accessible", choices=["yes", "no", "accessible"])
    sp.set_defaults(fn=cmd_find)

    sp = sub.add_parser("tarp")
    sp.add_argument("--pitch", type=int, default=None, help="roof pitch X/12")
    sp.add_argument("--rain", default="no", choices=["yes", "no", "y", "n"])
    sp.add_argument("--dark", default="no", choices=["yes", "no", "y", "n"])
    sp.add_argument("--stories", type=int, default=None)
    sp.set_defaults(fn=cmd_tarp)

    sp = sub.add_parser("insurance")
    sp.add_argument("--country", default="us", choices=["us", "other"])
    sp.set_defaults(fn=cmd_insurance)

    sp = sub.add_parser("dry")
    sp.add_argument("--wet-insulation", default="unknown",
                    choices=["yes", "no", "y", "n", "unknown"])
    sp.set_defaults(fn=cmd_dry)

    a = p.parse_args()
    out = a.fn(a)
    if a.json:
        print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
