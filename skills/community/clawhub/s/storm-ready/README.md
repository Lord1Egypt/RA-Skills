# Storm Ready — Household Preparedness Audit & Planner

**The problem.** Emergency-preparedness advice is generic and unordered:
"keep 72 hours of supplies" is 5× undersized for a Gulf Coast hurricane,
irrelevant for a tornado (where everything depends on 13 minutes of
warning), and aimed at the wrong resource for an ice storm (where indoor
cold, not supplies, is the killer). Real households get a storm warning,
google a 200-item PDF, and do none of it.

**What this is.** A regional, household-specific preparedness planner:

- **8 hazard profiles** (gulf/atlantic hurricane, tornado, ice storm,
  atmospheric river, wildfire WUI, blizzard, generic) encoding what each
  *actually* demands — day-counts, items, and phases.
- **A gap audit** against your marked inventory: ✓ have / ~ partial /
  ✗ missing, sorted by phase and P0/P1/P2 priority, ending with a
  numbered list of life-safety gaps to fix first.
- **Real sizing math for YOUR household**: 4 people + a 60-lb dog → 63
  gallons of water with container breakdowns; people × days × 2,000 kcal
  food baskets you rotate through your pantry; power loads with duty
  cycles, compressor surge (×3.5), and runtime for your battery bank.
- **Phase-by-phase countdown** from T-72h (fill tubs, fuel, RX fills)
  through T-12h (safe room) and during-storm rules (CO, flood depth,
  fridge discipline) to recovery (photo before cleanup, insurance,
  disaster assistance).
- **The rules that keep killing people**, stated where you'll see them:
  generators outdoors ≥20 ft, 6 in of moving water takes a car, tape on
  windows does nothing.

## Quick start

```bash
python3 scripts/storm_ready.py regions                     # pick your profile
python3 scripts/storm_ready.py profile --region hurricane-gulf \
    --people 4 --pets "dog:60,cat:10"                      # your household
python3 scripts/storm_ready.py audit                       # gap analysis
python3 scripts/storm_ready.py profile --mark-have radio first-aid
python3 scripts/storm_ready.py water                       # gallons + storage
python3 scripts/storm_ready.py power --loads fridge,cpap --battery-wh 2000
python3 scripts/storm_ready.py timeline --region hurricane-gulf
python3 scripts/storm_ready.py example                     # full demo
```

## Tests

```bash
python3 scripts/test_storm_ready.py    # 35 assertions, pure stdlib
```

## Guidance basis

FEMA/Ready.gov conventions (1 gal/person/day, 72-hour baseline), gulf-
coast county standards (14-day hurricane supply), NOAA/NWS safety rules
(Turn Around Don't Drown, CO generator safety), and after-action report
patterns (helmets in tornado country, shoes post-windstorm, photo-before-
cleanup). `references/region-playbooks.md` explains the reasoning.

**Not a substitute for official warnings.** Follow your national weather
service and local emergency management; this tool organizes your
preparation, it doesn't replace evacuation orders.

MIT License — see LICENSE. Pure Python stdlib, no network calls.
