#!/usr/bin/env python3
"""Smoke/CO alarm decoder and home auditor: chirp patterns, age audit,
NFPA-72 coverage, placement anti-patterns, CO event script."""
import argparse
import json
from datetime import date

PATTERNS = [
    (["1 beep every minute", "single beep", "one beep", "chirp every minute", "chirp every 30"],
     "LOW BATTERY",
     ["Replace the battery now (9V/AA), or the whole unit if sealed-10-year",
      "If it chirps again WITH a fresh battery -> END-OF-LIFE, replace unit"]),
    (["3 quick beeps", "three beeps", "3 beeps repeating", "4 quick beeps", "four beeps"],
     "SMOKE ALARM PATTERN",
     ["TREAT AS FIRE: evacuate everyone, close doors behind you, meet outside",
      "Feel doors with the back of your hand before opening; use other exit if hot",
      "Call emergency services from outside; never re-enter for belongings"]),
    (["carbon monoxide", "carbon", "monoxide", "co alarm", "4 beeps then pause", "5 beeps kidde", "warning carbon monoxide"],
     "CARBON MONOXIDE PATTERN",
     ["Evacuate to fresh air immediately; open windows/doors on the way out if quick",
      "CO symptoms: headache, nausea, dizziness, confusion — anyone symptomatic needs medical eval",
      "Call fire/gas utility to inspect the source; do not re-enter until cleared and ventilated"]),
    (["5 chirps every minute", "3 chirps every minute", "fault"],
     "UNIT FAULT / END-OF-LIFE",
     ["Check manufacture date on the back label",
      "Past 10 years (smoke) or label EOL (CO): replace the unit, not the battery",
      "If new unit faults: return under warranty (most carry 5-10y)"]),
    (["same time every night", "chirps at night only"],
     "TEMPERATURE-DIP + MARGINAL BATTERY",
     ["Night cooling drops battery voltage below threshold; replace battery",
      "If sealed unit does this in a cold hallway <4C regularly, it's aging — plan replacement"]),
]

PLACEMENT = {
    "kitchen": ("KEEP OUT of the kitchen and >=10 ft from cooking appliances",
                ["Smoke+steam = false alarms -> people rip batteries out",
                 "Photoelectric 10-20 ft away in the hall is the pattern",
                 "Never above the stove or inside the kitchen doorway"]),
    "bedroom": ("REQUIRED in every bedroom",
                ["Closed doors both delay smoke AND muffle hallway units",
                 "Combo smoke units; heat detectors not needed here"]),
    "hallway": ("Outside each separate sleeping area, plus each floor incl. basement",
                ["This is the unit that wakes parents when the kitchen burns",
                 "Wall mount: top edge 4-12 in below the ceiling"]),
    "living": ("Per-floor general coverage; living room + stairwell tops on multi-story",
               ["Stairwell top: smoke rises the stairwell like a chimney — early trigger",
                "Avoid within 4 in of corners (dead air) and ceiling apex"]),
    "garage": ("NEVER a smoke alarm in the garage; HEAT detector only",
               ["Car exhaust + dust = instant nuisance chirping",
                "Attached garage: put the smoke/CO just INSIDE the connecting door instead"]),
    "attic": ("HEAT detector only (if anything), rated for ambient temps",
              ["Attics exceed smoke alarm temp ratings seasonally",
               "Dust kills ionization chambers fast"]),
    "basement": ("Required: near the stairs, not in the furnace dead-air pocket",
                 ["Within 10 ft of furnace/water heater tends to nuisance-chirp on startup",
                  "CO combo unit recommended here for fuel appliances"]),
    "bathroom": ("NOT in bathrooms: steam false-alarms any smoke sensor",
                 ["Put it in the hall outside the bathroom instead"]),
    "ceiling": ("Center of ceiling ideal; avoid supply-air diffusers and fan blades",
                ["AC supply 'airwalls' a sensor — smoke bypasses it",
                 "Ceiling fans mix and delay stratification near the unit"]),
    "co": ("CO: near sleeping areas + near fuel appliances; height barely matters",
           ["CO density ~ air: mixes evenly, so 'low mounting' is a myth",
            "One near each sleeping area so it WAKES you; one within 10-15 ft of furnace room"]),
}

CO_SCRIPT = """CARBON MONOXIDE EVENT — DO NOW
1. Move everyone to fresh air. Count heads.
2. If anyone has headache/nausea/confusion: emergency medical care now.
3. Open doors/windows on your way out (if it takes <10 seconds).
4. Do NOT ventilate-then-reenter to 'check': CO is invisible and
   re-accumulates from the still-running source.
5. Call the fire department / gas utility to find the source.
6. After the event: have the appliance (furnace/boiler/heater/generator/
   blocked flue/running car) inspected BEFORE running it again.
7. Headspace: CO binds hemoglobin ~200x tighter than oxygen; symptoms
   returning indoors means the source is still active. Stay out.
"""


def cmd_chirp(a):
    q = a.pattern.lower()
    for kws, meaning, actions in PATTERNS:
        if any(k in q for k in kws):
            print(f"Pattern: {a.pattern}")
            print(f"Meaning: {meaning}")
            print("Action:")
            for i, s in enumerate(actions, 1):
                print(f"  {i}. {s}")
            print()
            print("Brand variance: First Alert CO = 4 beeps + voice; Kidde CO = 4 beeps")
            print("repeating, Kidde EOL = 5 chirps/min. Confirm on the back label.")
            return
    print(f"Pattern '{a.pattern}' not recognized.")
    print("Describe precisely: beeps per burst, seconds between bursts, time of day.")
    print("Back label of the unit lists its exact chirp table + manufacture date.")


def cmd_audit(a):
    with open(a.units) as f:
        units = json.load(f)
    today = date.today()
    rows = []
    for u in units:
        y, m = map(int, u["installed"].split("-"))
        age = (today.year - y) + (today.month - m) / 12.0
        kind = u.get("kind", "smoke")
        limit = 7 if kind == "co" else 10
        if kind == "combo":
            limit = min(10, 7)  # CO cell dies first
        left = limit - age
        rows.append((left, u, age, limit))
    rows.sort(key=lambda r: r[0])
    print(f"Audit of {len(units)} units (today {today}):")
    print()
    for left, u, age, limit in rows:
        name = u.get("id", "?")
        status = ("EXPIRED" if left <= 0 else
                  f"{left:.0f}y left" if left > 1 else
                  f"{left*12:.0f} months left")
        flag = " <<< REPLACE" if left <= 0 else (" << plan soon" if left < 2 else "")
        print(f"  {name:<12} {u['kind']:<6} installed {u['installed']}  "
              f"age {age:.1f}y / limit {limit}y  {status}{flag}")
    print()
    expired = [u.get("id") for l, u, _, _ in rows if l <= 0]
    if expired:
        print(f"Replace immediately (oldest-risk): {', '.join(expired)}")
    print("Rule: smoke=10y, CO=7y (label governs), combo=CO cell first.")
    print("Sealed units chirping with no battery door = whole-unit replace.")


def cmd_coverage(a):
    b, f = a.bedrooms, a.floors
    print(f"House: {b} bedrooms, {f} floors")
    print()
    print("NFPA-72-style minimum coverage:")
    print(f"  1 smoke in EACH bedroom                    : {b}")
    print(f"  1 outside each sleeping area (hallway)     : 1 per sleeping wing")
    print(f"  1 per floor incl. basement                 : {f + (1 if a.basement else 0)}")
    print(f"  Interconnected (hardwire or wireless)      : strongly recommended")
    print()
    print(f"  => Total smoke units: ~{b + f + (1 if a.basement else 0)}")
    print()
    print("Add CO (combo or separate):")
    print("  - outside each sleeping area (wake-you-up position)")
    print("  - near fuel appliances / attached garage door")
    print("  - check jurisdiction: many require CO on each floor w/ bedrooms")
    print()
    print("Upgrades: sealed 10-y lithium (no battery swaps), escape-light")
    print("models, strobe/shaker for hearing-impaired household members.")


def cmd_placement(a):
    room = a.room.lower()
    for key, (rule, notes) in PLACEMENT.items():
        if key in room or room in key:
            print(f"Room/zone: {a.room}")
            print(f"Rule: {rule}")
            print("Why / how:")
            for n in notes:
                print(f"  - {n}")
            return
    print(f"No specific rule for '{a.room}' — general rules:")
    print("  - ceiling center ideal; wall mount 4-12 in below ceiling")
    print("  - never within 4 in of a corner (dead air)")
    print("  - away from supply diffusers, fans, ducts")


def cmd_co(a):
    print(CO_SCRIPT)


def main():
    p = argparse.ArgumentParser(description="Smoke/CO alarm decoder and auditor.")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("chirp"); s.add_argument("--pattern", required=True); s.set_defaults(f=cmd_chirp)
    s = sub.add_parser("audit"); s.add_argument("--units", required=True); s.set_defaults(f=cmd_audit)
    s = sub.add_parser("coverage"); s.add_argument("--bedrooms", type=int, required=True)
    s.add_argument("--floors", type=int, required=True); s.add_argument("--basement", action="store_true"); s.set_defaults(f=cmd_coverage)
    s = sub.add_parser("placement"); s.add_argument("--room", required=True); s.set_defaults(f=cmd_placement)
    s = sub.add_parser("co"); s.set_defaults(f=cmd_co)
    a = p.parse_args(); a.f(a)


if __name__ == "__main__":
    main()
