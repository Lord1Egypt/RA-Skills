---
name: roof-leak-emergency-response
description: Use while water is actively dripping from the ceiling — runs the source-tracing protocol (the drip is RARELY under the hole: 3-6 m of run happens; attic-first triangulation from above beats ceiling-staring), the damage-containment sequence (contain water BEFORE opening the bulge — gravity dictates which), electrical hazard triage (fixture + switch off at breaker before anything under a wet ceiling), the tarp-tie-down protocol with the ladder/steepness/night cutoffs for DIY vs professional, an insurance evidence protocol that photographs BEFORE emergency mitigation, and the drying plan that decides whether that drywall is saved or mold-food.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [roof, leak, water-damage, emergency, attic, tarp, insurance, mold-prevention]
---

# Roof Leak Emergency Response

Water coming through a ceiling is a 3-hour problem with a 3-month tail.
The first hour decides most of it: where the water is actually getting
in (the drip point is rarely under the entry — roofs and ceiling voids
route water sideways meters from the hole), whether electricity is in
play, and what gets photographed before mitigation erases the evidence
insurance wants. Then the tail: wet drywall and insulation that isn't
dried within 24–48h becomes mold remediation at 5–10× the cost.

## When to Use

- Water actively dripping / ceiling bulging / brown stain spreading
- After a storm: check the attic even if the ceiling looks dry
- Water around a light fixture or ceiling fan (electrical class —
  different first moves)
- Deciding: tarp it myself tonight vs roofer tomorrow vs emergency call
- After containment: what dries, what gets opened, what insurer needs
- Renters: the notice + documentation sequence that protects the
  deposit and forces the repair

**Don't use for:** burst pipes inside walls (different failure — shut
the water main, see water-shutoff-map patterns); roof COLLAPSE sounds
(structural — evacuate the room, call emergency services line);
standing water near the electrical panel (electrician/utility first).

## The Method

1. **`triage`** — the first-15-minutes decision tree: electrical
   involvement (fixture/fan/any outlet wet → breaker off FIRST, and do
   not touch the fixture), water volume class (drip vs stream vs
   pouring), structural sag (bulge = contained water weight — poke it
   INTO a bucket, never let it choose its own moment), night/steepness
   cutoffs for going up.
2. **`find`** — source tracing: the ceiling-stain rules (wet-edge = 
   active, ring edges = old episodes), attic-entry protocol (from
   BELOW the deck, follow the wet rafters/sheathing uphill — water
   travels on the underside of decking before it drops), the usual
   suspects map (flashing at chimney/valley/vent, nail backs, missing
   shingle tabs, ice dams in season, plumbing-stack collars), and the
   hose-test method for tomorrow if tonight is guesses.
3. **`tarp`** — DIY emergency cover: when (rain ongoing, accessible
   from INSIDE the attic space can be safer than roof-walking), the
   2-ft overlap + downhill-under course rules, anchoring (never nail
   into the wet roof — board/strap weights; furring strips on edges),
   ladder steepness/height cutoffs, and the STOP list (wet roof, night,
   steep pitch >6/12, two stories, alone).
4. **`insurance`** — evidence-first protocol: the photo/video shot
   list (wide → room → stain → attic path → exterior suspect), the
   mitigation-vs-permanent-repair distinction (insurers expect you to
   MITIGATE — tarps and drying are claim-relevant, full replacement
   repairs before adjuster = trouble), receipts for everything, the
  first-notice call script, and the difference between sudden-damage
   (covered) vs wear/tear/maintenance (usually not).
5. **`dry`** — the 24–48h mold clock: moisture mapping (cheap pin meter
   or the screwdriver-poke test), what's salvageable (drywall that
   dries fast and stays structurally sound vs insulation that NEVER
   keeps its R-value wet), when to open the ceiling (wet insulation
   above drywall = open it, it's a mold incubator), fan+dehumidifier
   math, and the smell/humidity red flags that mean call remediation.

Run `python3 scripts/roof_leak_response.py <cmd> --help`.

## Judgment Rules

- **Water first, ceiling second.** Contain the drip (bucket + towels +
  plastic sheet) BEFORE investigating the bulge. A sagging bulge is
  gallons of stored water: poke at the LOWEST point with a screwdriver,
  bucket ready, controlled release beats ceiling choosing.
- **Breaker before bucket** if any fixture/outlet is wet or the leak is
  within ~1 m of one. Water follows wiring through joist bays.
- **The drip point is a starting coordinate, not the answer.** Roofs
  shed water into valleys and flashing gaps meters away; inside, water
  runs the underside of sheathing and tops of joists before dropping.
  Attic triangulation from above beats ceiling-staring every time.
- **Photograph before you mitigate.** The insurer's adjuster wants to
  see the active path; a perfectly tarped, dried scene reads as "minor"
  to someone who wasn't there. Evidence THEN mitigation, always.
- **Tarps are for keeping rain OUT, not for looking tidy.** Overlap
  like shingles (upper course OVER lower), extend past the suspect
  area, weight the edges. A badly anchored tarp in wind becomes a sail
  and enlarges the damage.
- **Wet insulation is done.** Fiberglass batts lose R-value and hold
  water against the drywall; cellulose compacts and molds fast. Wet =
  remove and replace, not dry and hope.
- **The mold clock is 24–48h.** After that, the question isn't whether
  to call remediation, it's how much of the wall opens.

## Common Pitfalls

1. Staring at the ceiling stain while the attic (where the answer is)
   stays unvisited.
2. Popping a bulging ceiling without a bucket under the lowest point —
   gallons release at once and it's NOT where you stood.
3. Touching a wet light fixture "to see if it still works."
4. Nailing a tarp through the shingles — every nail hole is a new leak;
   use furring/board anchoring at edges only.
5. Walking a wet, mossy, or steep roof at night — falls kill more
   people than roof leaks bankrupt people. Emergency roofer exists.
6. Drying the room but leaving wet attic insulation above — mold farm
   with a fresh-painted lid.
7. Repairing permanently before the adjuster sees it — coverage fight
   you created yourself.
8. Renters not putting the leak in WRITING to the landlord day-of —
   the paper trail is what makes the repair and the deposit protection
   enforceable.

## Verification Checklist

- [ ] Power off to affected circuit if any fixture nearby (breaker,
      verified with a lamp)
- [ ] Drip contained; bulge released into a bucket at the low point
- [ ] Attic inspected: wet path marked (chalk), suspect entry
      photographed from the underside
- [ ] Exterior photographed; tarp only if inside safe-cutoffs, else
      emergency roofer called and documented
- [ ] Evidence pack: wide/room/stain/attic/exterior photos + video,
      timestamps on
- [ ] Insurer (or landlord) called; claim/reference number recorded;
      mitigation-vs-repair distinction understood
- [ ] Wet insulation removed and bagged; ceiling opened over wet areas
      if insulation was wet
- [ ] Fans + dehumidifier running; moisture readings logged daily
      until two consecutive dry days
- [ ] No musty smell, humidity normal, readings stable → then (and only
      then) close the ceiling

## One-Shot Recipe

Storm night, water dripping near a ceiling light, bulge growing:

```bash
python3 scripts/roof_leak_response.py triage --fixture yes --flow drip
python3 scripts/roof_leak_response.py find --attic accessible
python3 scripts/roof_leak_response.py tarp --pitch 7 --rain yes --dark yes
python3 scripts/roof_leak_response.py insurance --country us
python3 scripts/roof_leak_response.py dry --wet-insulation yes
```

Breaker off → bucket under the low point → attic flashlight hunt →
photo everything → emergency roofer if the tarp STOP-list fires →
dehumidifier tonight.
