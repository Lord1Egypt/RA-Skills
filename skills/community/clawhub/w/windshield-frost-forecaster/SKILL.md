---
name: windshield-frost-forecaster
description: "Use on cold evenings to predict whether frost will form on your car windshield or home windows tonight: dew-point + radiative-cooling physics (clear sky, wind, humidity), parking-duration verdicts for uncovered vs covered, morning scrape-time penalty, and cover/defrost tactics by frost class."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [frost, windshield, ice-scraping, radiative-cooling, dew-point, winter, car-care]
---

# Windshield Frost Forecaster

## Overview
On a calm, clear autumn night a car windshield can drop **5–8 °C below air
temperature** and frost even when the air never reaches 0 °C — because glass
radiates heat to a cold sky and wind cannot stir the thin boundary layer
right at the surface. Conversely, a cloudy or windy night at −1 °C air may
leave the glass completely wet-but-liquid. Whether you wake up to a frozen
windshield is predictable from four numbers: **air temp minimum, dew point,
wind, cloud cover**.

This skill computes, for tonight's forecast:

- **Radiative depression**: how far glass falls below air temp (sky-clearness
  × wind formula), giving glass-minimum temperature
- **Frost verdict**: NO FROST / FROST / HARD FROST (glaze risk) by comparing
  glass minimum vs dew point and 0 °C
- **Dew vs frost discrimination**: condensation that forms above 0 °C (beads
  of water, easy wipers) vs below (ice needing a scraper)
- **Parking-duration curves**: glass temperature over 1–12 h parked outside —
  short errand vs overnight
- **Cover verdict**: is a frost shield / towel / tarp worth it tonight (it is
  whenever FROST), plus morning tactics per frost class (defrost times,
  never-pour-hot-water warning, alcohol-mix de-icer ratios)

## When to Use
- Evening before a cold night: "Will I need to scrape tomorrow at 06:30?"
- Deciding to park in the open vs under a carport / cover the glass
- "It's +2 °C — can frost really form?" (yes — this skill explains when)
- Garage-vs-driveway tradeoffs during a cold snap; ev-camera/roof frost for
  home windows and solar panels uses the same physics
- **Don't use for:** road-ice warnings for driving (black ice on pavement is
  a different surface-energy problem), or aviation icing.

## Steps
1. Get tonight's numbers (any weather app): overnight min air temp, dew point
   (or RH → the script converts), mean wind speed, cloud cover %.
   ```bash
   python3 scripts/frost.py --tmin 1 --tdew -1 --wind 2 --cloud 30
   python3 scripts/frost.py --tmin 1 --tdew -1 --wind 2 --cloud 30 --rh 90 --hours 8
   ```
2. Read the verdict block: glass-min temp, frost class, why (one-line physics).
3. Read the parking table if you're parked outdoors for limited hours (glass
   reaches frost threshold at hour N or never).
4. Act on the tactics: cover tonight / scraper time budget in the morning /
   de-icer mix if HARD FROST.

## The Model (summary — full derivation in references/frost-physics.md)
- Glass minimum ≈ air min − ΔT_radiative, where
  `ΔT = (1 − 0.85·cloud_fraction) × 5.5 °C × wind_factor`,
  `wind_factor = 1/(1 + wind_ms/1.5)` (calm air lets the film cool; wind
  mixes warm air back).
- Frost forms iff glass_min ≤ 0 °C **and** glass_min ≤ dew point (deposition
  path: vapor → ice directly, or dew that then freezes).
- HARD FROST when glass_min ≤ −4 °C (thick crystalline glaze, scraper
  mandatory, defrost 10+ min).
- Vehicle heat mass: engine/warm cabin adds ~+2 °C to glass for the first
  1–2 h after parking — the duration curve starts elevated, then decays.

## Output
Verdict block + hourly glass-temperature table for parked car + morning
tactics per class + cover advice. `--json` for machine use.

## Common Pitfalls
1. **"Air is +2 °C, no frost possible."** Wrong on clear calm nights: glass
   radiates below air by 5+ °C; the classic surprise freeze.
2. **Wind check ignored.** A 6 m/s night wind can erase frost risk at −2 °C
   air by keeping the boundary mixed; the formula handles it.
3. **Dew point ignored.** Glass below 0 °C but air bone-dry (Tdew −12 °C)
   → little ice: no moisture to deposit. Both conditions must hold.
4. **Hot water on a frozen windshield** — thermal shock cracks glass. Lukewarm
   ≤30 °C at most, or proper de-icer; tactics block states this.
5. **Wiper blades frozen to glass**: free them before switching on (tears the
   rubber); lift wipers when FROST verdict is issued.
6. **Covering after dew has already fallen** traps water against the glass
  and can freeze the cover ON. Cover in the evening, dry glass.

## Verification Checklist
- [ ] Both frost conditions evaluated (glass ≤ 0 °C AND moisture available)
- [ ] Wind and cloud both fed in — a verdict computed with defaults silently assumes calm/clear
- [ ] Duration table shows the crossing hour when verdict is borderline
- [ ] Morning tactics match the frost class, not generic advice
- [ ] No recommendation of hot water anywhere in output
