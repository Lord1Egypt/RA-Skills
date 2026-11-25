# Windshield Frost Forecaster

**It's +2 °C outside. Morning: frozen windshield.** On a clear, calm night
glass radiates heat to the sky and drops 4–8 °C *below* air temperature —
so frost forms while every thermometer says "above freezing". Meanwhile a
windy overcast night at −1 °C can leave the glass merely wet. Whether you
scrape ice tomorrow is physics, not luck: dew point × cloud × wind.

```
python3 scripts/frost.py --tmin 2 --tdew 0 --wind 0.5 --cloud 10
# Radiative depression: 3.8°C -> glass minimum -1.8°C
# VERDICT: FROST  -> cover tonight, lift wipers

python3 scripts/frost.py --tmin 2 --tdew 0 --wind 6 --cloud 100
# VERDICT: NONE   -> sleep in
```

## The real-world problem
- Every driver in a temperate climate loses 5–15 minutes on surprise frost
  mornings — often exactly the mornings with the least slack (school run,
  commute). Worse, improvisations cause real damage: hot water cracks
  windshields, frozen-on wipers tear their rubber, salt brine corrodes trim.
- Folk rules ("below 3 °C = ice") fail in both directions because they ignore
  the two decisive factors: **sky view** (clear vs cloudy) and **wind**
  (mixing kills the chilled film) — plus **moisture** (dry air = cold but
  clean glass).
- Deciding *whether to cover the glass tonight* is a 30-second evening
  decision that saves a 10-minute morning. This tool makes it with numbers.

## What it does
- Computes radiative depression `(1 − 0.85·cloud)·5.5°C·1/(1+v/1.5)` → glass
  minimum temperature for the night
- Verdict classes: NONE / DEW / FROST / HARD FROST with the two-condition
  test (glass ≤ 0 °C **and** moisture available at dew point)
- Parked-car duration curve: hour-by-hour glass temp including engine
  warm-mass decay — "will it frost during a 3 h cinema parking?"
- Morning tactics per class: defrost times, 2:1 water:IPA de-icer, the
  never-hot-water rule, wiper-lifting, cover-before-dew timing
- Same physics applies to house windows (inside pane frosting), solar
  panels, roof — see references

## What's inside
- `SKILL.md` — triggers, steps, pitfalls, verification checklist
- `references/frost-physics.md` — derivation, frost-vs-dew paths, class
  table, de-icer chemistry, cover tactics, model limits
- `scripts/frost.py` — pure stdlib; `--rh` fallback (Magnus dew point),
  `--hours` curve, `--json`; tested on 4 canonical cases

MIT © Denis Voronin
