# Rain Barrel Harvest Planner

A 1,500 ft² roof in a 30-inch rain climate sheds **~28,000 gallons a year** — free, soft, chlorine-free water — while the household below pays the city to irrigate with potable water. Rain harvesting is simple engineering with predictable failure modes: barrels sized without demand (overflow theater), demand estimated without area (one 200 L barrel against a July garden drinking 3,000 L/week), no first-flush diverter (storing the dirtiest water of every storm), and overflow dumped at the foundation.

This skill is a closed-system calculator with four commands:

1. **Catchment** — roof area × rainfall × runoff coefficient; per-storm and annual yield.
2. **Demand** — planted area × L/m²/week doctrine bands (vegetables 15–20, lawns 20–25, xeric 5–8), dry-season weeks only.
3. **Storage simulation** — monthly mass-balance: inflow, demand, overflow, shortfall; the used/demand fraction names the verdict (SYSTEM SIZED / WORKS / HALF-SERVES / GESTURE) and diagnoses whether your constraint is storage or demand.
4. **Payback** — on gallons *used* (not harvested) × water + sewer-credit rate; honest verdicts where flat US water rates make barrels a slow pay.

Plus doctrine: first-flush sizing (0.5–1 mm per storm), gravity-head physics (0.1 bar/m — standard drip won't run), mosquito screening, winterization (ice splits barrels), overflow routing ≥10 ft from foundations, and legality notes.

## Real problem it solves
Garden irrigation is 30–60% of summer household water use in much of the US/EU, and half of installed rain barrels don't deliver because component sizing ignored the demand/storage phase mismatch. The planner turns "should I get a barrel?" into a 5-minute numbers exercise: what the roof yields, what the garden drinks, what storage bridges the gap, and whether it pays at your rates — with the overflow number telling you when the right move is more beds, not more barrels.

## Quick start
```bash
python3 scripts/rainbarrel.py catchment --area-ft2 1500 --rain-in 30 --surface asphalt
python3 scripts/rainbarrel.py demand --area-m2 60 --liters-per-m2 20 --weeks 14
python3 scripts/rainbarrel.py storage --area-ft2 1500 --surface asphalt \
    --monthly-in "1.8 1.9 2.5 2.9 3.2 3.4 2.9 2.8 3.0 2.6 2.4 2.3" \
    --demand-area-m2 60 --lpm2 18 --capacity 400
python3 scripts/rainbarrel.py payback --used-gal 4800 --cost 280 --water-rate 14
```

## Contents
- `SKILL.md` — model, verdict bands, doctrine, pitfalls, example simulation
- `references/harvest-reference.md` — demand tables, first-flush, plumbing physics, economics, legality, troubleshooting
- `scripts/rainbarrel.py` — stdlib-only CLI (catchment / demand / storage / payback)
