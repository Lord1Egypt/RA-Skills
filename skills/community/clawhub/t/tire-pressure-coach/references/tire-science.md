# Tire Pressure Coach — Reference

## Why pressure matters (the stakes)

- NHTSA estimates ~11,000 tire-related crashes annually in the US; under-
  inflation is the leading tire factor in blowouts.
- The contact patch — the entire interface between car and road — is roughly
  a postcard per tire. Its shape is set by pressure.
- Under-inflation: outer-edge wear, higher rolling resistance (fuel penalty
  measurable from ~2 psi low), heat buildup (blowout mechanism), sloppy
  steering, longer stops.
- Over-inflation: center wear, smaller patch, harsher ride, more vulnerable
  sidewalls to pothole damage, degraded wet grip.
- ESC/ABS calibration assumes roughly placard pressure; wildly off pressure
  subtly changes how the safety systems intervene.

## Cold pressure: the reference state

"Cold" = tire at ambient thermal equilibrium: parked ≥3 hours OR driven
less than ~1 mile. Manufacturers specify cold pressures because warm
readings are a moving target.

### The gas physics

Gauge pressure reads relative to atmosphere; the tire's absolute pressure
scales with absolute temperature:

    P2 = P1 × (T2 + 273.15) / (T1 + 273.15)     (approximately, fixed volume)

Rules of thumb that fall out (for ~30-35 psi tires):
- **1 psi per 10°F (≈5.5°C)** of temperature change
- 0.7 psi per 100 m of altitude (gauge only — absolute is unchanged)
- A tire that heats from driving: +2 to +6 psi is normal highway behavior,
  more in summer or with load

### Filling warm (the gas station problem)

You checked cold this morning (30.5), drove to the station, and now the
tire reads 33 hot. Filling "to 33" guarantees a morning pressure of ~30.5 —
you fixed nothing. Two correct approaches:
1. Fill to `placard + (hot − cold_now)` — you need this morning's readings.
2. Fill to placard + ~3 psi (typical warm delta), re-check cold next
   morning, top off precisely.

The script's `check --hot` implements #2 and prints the exact fill-to.

## Placard logic

The placard (door jamb / fuel flap / manual) lists: size, load index, and
cold pressures — sometimes two sets (normal vs full-load/high-speed).
- The **sidewall max** (e.g. "MAX LOAD 615 kg AT 44 psi") is a capability
  ceiling tied to load rating — never a setting.
- Full-load / towing: use the high-load numbers; if only one set is given,
  +2..4 psi on the rear axle is the common manufacturer guidance (check the
  manual — some explicitly forbid deviation).
- "PSI all around the same" is wrong for many RWD and performance cars
  (typical split like 35F/38R or 33F/30R).

## Seasonal rhythm

- Autumn→winter: a 20°C drop costs ~2-3 psi. October is when TPMS lights
  fleet-wide come on — it's physics, not coincidence.
- Spring: pressures rise; bleed back to placard (over-pressure from ambient
  warming is usually small but check).
- Mountain trips: gauge reads ~2 psi high at 1500 m relative to sea level;
  don't bleed at the summit — the tire's absolute pressure didn't change.

## Tread depth

| Depth | Meaning |
|-------|---------|
| 8 mm | new (typical summer/all-season) |
| ~8-10 mm | new winter tire |
| 4 mm | wet-grip performance cliff — aquaplaning risk rises steeply below this |
| 3 mm | practical minimum for winter tires (compound+sipes need depth) |
| 1.6 mm | legal minimum in US(most states)/EU/UK — inspection pass, NOT safety |
| < 1.6 mm | illegal; catastrophic wet performance |

Wet braking from 80 km/h can be tens of percent longer at 1.6 mm vs 4 mm
(ADAC/EU label testing consistently shows large deltas in the last meters
of tread life). Advice: plan replacement at 4 mm (summers) / 4-5 mm
(winters), not at the legal limit.

Quick field tests:
- US quarter: insert head-down into grooves; if the top of Washington's
  head is fully visible → ≈4/32" (≈3.2 mm) → start shopping.
- US penny: Lincoln's whole head visible → ≈2/32" (1.6 mm) → replace NOW.
- EU: a €1 coin's outer band ≈ measuring reference; better to use a cheap
  calibrated gauge (~the price of a coffee).

Wear patterns:
- both edges worn, center fine → chronic under-inflation
- center worn → chronic over-inflation
- one edge (inner OR outer) → alignment (camber)
- feathered/cupped → alignment or worn shocks
- flat spots → brake lock/ABS issue or parking brake left on
- sidewall bubbles → replace immediately (structural)

## TPMS decode

- US direct TPMS triggers at **25% below placard** cold — i.e., placard 32 →
  warning at ~24. That's already deep into under-inflation territory: the
  light is a fire alarm, not a smoke detector. Monthly manual checks beat it.
- Indirect TPMS (ABS-wheel-speed based) also under-detects slow leaks and
  needs a relearn after rotation.
- Solid light = pressure; flashing-then-solid = TPMS system fault (sensor
  battery dead is the common cause after 5-7 years / ~10-year batteries).

## Monthly check protocol (5 minutes)

1. Same morning window each month (consistency beats precision).
2. Cold tires; gauge (digital, ±1 psi).
3. All four + spare (spacesaver: typically 60 psi — checked never, needed
   always).
4. Log per-tire values. A tire losing >2 psi/month vs its axle-mate's <0.5
   has a slow leak: nail, valve, or bead — get it looked at this week.
5. Season transitions: expect and pre-correct the ±2 psi ambient swing.

## Script math summary

- temp correction: `P_cold_at_T2 = P_set × (T2+273)/(T1+273)` via absolute
  pressures, reported in gauge with 1-decimal psi
- altitude: `gauge_delta ≈ 0.0145 psi/m × Δm` (sign: gauge rises with
  altitude relative to fill point)
- verdicts: |measured − target| ≤ 1.0 psi → OK; below → ADD to target;
  above by >1.5 → BLEED; side-to-side gap on axle >2 → leak/alignment flag
- tread verdicts: ≥4 safe; 3-4 caution (replace before wet season; winter:
  now); 1.6-3 urgent; <1.6 replace immediately + legal warning
