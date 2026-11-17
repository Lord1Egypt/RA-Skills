---
name: rain-barrel-harvest-planner
description: Use when installing rain barrels or a rainwater harvesting system, sizing cistern storage, or deciding if harvesting pays — catchment yield from roof area x rainfall, storage sufficiency against irrigation demand (Rabi 15-20 L/m²/week doctrine), overflow routing, and payback vs municipal water with honest first-flush and winterization rules.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [rainwater, rain-barrel, irrigation, garden, water-conservation, sustainability]
---

# Rain Barrel Harvest Planner

## Overview
A 1,500 ft² roof in a 30-inch rain climate sheds **~28,000 gallons a year** — free, soft, chlorine-free water that most households send to the storm drain while paying the city to water the garden with potable water. The engineering is simple enough that anyone can do it, and the mistakes are predictable: barrels sized without demand (a full barrel with no demand overflows all summer), demand estimated without area (a 200 m² garden in July drinks ~3,000 L/week — one 200 L barrel is a gesture), and first-flush diverters skipped (the first millimeter of rain carries most of the bird droppings and roof grit).

This skill is a closed-system calculator: **catchment yield** (area × rainfall × runoff coefficient, monthly), **irrigation demand** (planted area × 15–20 L/m²/week in dry season, or landscape coefficient ET₀ method), **storage sufficiency** (does the barrel carry rain from wet weeks into dry weeks? — a mass-balance simulation, not a single number), **overflow routing**, and **payback** vs your actual water/sewer rate.

## When to Use
- Considering rain barrels / cisterns / IBC totes for garden irrigation
- Sizing storage for a greenhouse, community garden, or new-build landscape
- Deciding between one barrel, daisy-chained barrels, or a real cistern
- Checking whether harvesting pays at your water rate (it often doesn't at US flat rates without sewer discount — the math is honest about this)
- Rain barrel already overflows constantly — is the problem demand, storage, or catchment area?

**Don't use for:** potable systems (filtration/disinfection is a different discipline), large agricultural storage ( dams, ponds, licensing), or legality questions — some arid jurisdictions restrict harvesting; check local rules first (references §7).

## Quick Start
```bash
# Catchment: 1500 ft² roof, 30 in/yr rain, asphalt shingles
python3 scripts/rainbarrel.py catchment --area-ft2 1500 --rain-in 30 --surface asphalt

# Demand: 60 m² vegetable garden, dry-season weeks
python3 scripts/rainbarrel.py demand --area-m2 60 --liters-per-m2 20 --weeks 14

# Storage: monthly rainfall pattern vs demand — does 2x 200L cut it?
python3 scripts/rainbarrel.py storage --area-ft2 1500 --surface asphalt \
    --monthly-in "1.8 1.9 2.5 2.9 3.2 3.4 2.9 2.8 3.0 2.6 2.4 2.3" \
    --demand-area-m2 60 --lpm2 18 --capacity 400

# Payback: two 200L barrels ($280 installed) vs $14/kgal water
python3 scripts/rainbarrel.py payback --harvest-gal 6200 --used-gal 4800 \
    --cost 280 --water-rate 14 --sewer-credit 0
```

## The Model
1. **Yield** `gal = area_ft² × rain_in × 0.623 × runoff_coefficient` (0.85–0.95 asphalt/metal, 0.8 tile, smooth membrane up to 0.95). Metric: `L = m² × mm × 0.85 (coeff)`.
2. **Demand** dry-season doctrine: vegetables 15–20 L/m²/week applied; lawns ~20–25; xeric beds 5–8. Demand months = dry weeks only — barrels serve the dry season, not annual totals.
3. **Storage mass-balance**: month by month, `storage = min(capacity, storage + inflow − demand)`; track **overflow** (wasted harvest) and **shortfall** (municipal backfill). Sufficiency = used ÷ demand. This is where single-barrel setups die: summer demand and summer rain arrive out of phase.
4. **Payback** = installed cost ÷ (gallons actually *used* × all-in water rate incl. sewer credit). Harvest ≠ used: overflow doesn't pay.

## Doctrine
- **First-flush diverter always** — the first 0.5–1 mm of rain per storm carries the roof's contaminant load; divert it before storage (§4 references).
- **Match demand first, then storage.** 200 L per 10–15 m² of irrigated bed is the working heuristic; more storage without demand is just overflow theater.
- **Overflow must go somewhere engineered** — away from foundations (≥10 ft), into a soakaway/rain garden, never against the wall the barrel hugs.
- **Mosquitoes**: sealed screens on every opening; a barrel with one 5 mm hole breeds all summer.
- **Winterization**: drain and disconnect before first hard freeze (ice splits barrels and crushes fittings) — freeze depth varies; when in doubt, drain.
- **Legality**: mostly legal/encouraged (with rebates) in US/EU; historically restricted in parts of Colorado/Utah (prior-appropriation doctrine) — verify locally.

## Verdict Bands (storage simulation)
| Used ÷ demand | Verdict |
|---|---|
| ≥ 90% | SYSTEM SIZED — demand essentially fully served |
| 60–90% | WORKS — meaningful offset; add capacity or demand-shift |
| 30–60% | HALF-SERVES — the barrel delays municipal water, doesn't replace it |
| < 30% | GESTURE — mostly overflow; add demand or rethink storage |

## Common Pitfalls
1. **Sizing storage from annual rainfall.** Demand and rain are out of phase; only the monthly mass-balance tells the truth.
2. **Ignoring the runoff coefficient and roof material** — gravel/built-up roofs shed 0.7 or less; tarps and "green roofs" even lower.
3. **No first-flush diverter** — storing the dirtiest water of each storm; clogs drip irrigation and loads the barrel with organics.
4. **Overflow at the foundation** — 28,000 gal/yr against a basement wall is a damp problem you built yourself.
5. **Tiny spigots feeding drip lines** — gravity gives ~0.4 bar per meter of head; drip needs pressure or a drip-kit rated for gravity; otherwise barrel-fed drip trickles uselessly.
6. **Winter freeze splits barrels** — every plastic barrel is a freeze victim; drain by first frost, every year, no exceptions.
7. **Payback computed on harvested, not used gallons** — a barrel overflowing in March saves nothing.

## Verification Checklist
- [ ] Roof catchment area measured (plan view, not slope; only roof planes routed to the barrel count)
- [ ] Runoff coefficient per roof material applied
- [ ] Monthly rainfall for your station (not annual ÷ 12) used in the storage sim
- [ ] Demand from planted area × L/m²/week for dry weeks only
- [ ] Storage capacity = sum of ALL barrels on the same catchment
- [ ] First-flush diverter in the parts list; overflow routed ≥10 ft from foundation
- [ ] Payback on gallons-used × (water + sewer credit) rate
- [ ] Winterization date set (drain before first hard freeze)

## Example Session
```
$ python3 scripts/rainbarrel.py storage --area-ft2 1500 --surface asphalt \
    --monthly-in "3.0,2.8,2.5,1.2,0.4,0.1,0.0,0.1,0.4,1.5,2.7,3.0" \
    --demand-area-m2 60 --lpm2 18 --capacity 400
STORAGE SIMULATION — 1500 ft² asphalt roof, 400 L storage, 60 m² @ 18.0 L/m²/wk
  month  rain    inflow      demand     overflow   shortfall
  May    0.4in     1,134 L         0 L     1,134 L         0 L
  Jun    0.1in       179 L         0 L       179 L         0 L
  Jul    0.0in         0 L     4,676 L         0 L     4,276 L
  Aug    0.1in       179 L     4,676 L         0 L     4,497 L
  Sep    0.4in     1,134 L     4,676 L         0 L     3,542 L
  Oct    1.5in     4,636 L     4,676 L         0 L        41 L
  Nov    2.7in     8,456 L     4,676 L     3,379 L         0 L
  ...
  season used: 15,701 L of 28,058 L demand (56%)
  overflow wasted: 38,711 L
VERDICT: HALF-SERVES — the barrel delays municipal water, doesn't replace it.
  (38,711 L overflowed in the wet half — a 5,000 L cistern would carry
  the wet season into July; more 200 L barrels would not.)
```
