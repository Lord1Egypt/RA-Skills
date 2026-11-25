# Frost Physics Behind the Windshield Frost Forecaster

## 1. Why glass freezes when air doesn't
Any surface facing the sky radiates longwave energy to space (Stefan–Boltzmann,
ε≈0.92–0.95 for glass). At night, with no solar input, the surface's radiative
loss exceeds what it gains from the surrounding air — so the surface settles
**below air temperature**. This "radiative depression" is the whole game:

- **Clear sky**: effective sky temperature is 30–60 °C colder than the air →
  strong net loss → depression up to 5–8 °C on ideal surfaces.
- **Clouds**: water vapor and cloud droplets radiate back at near-air
  temperature; overcast nearly zeroes the depression. Cloud fraction c cuts
  it roughly by factor (1 − 0.85·c).
- **Wind**: the chilled surface film is constantly re-mixed with warmer air.
  Empirically depression scales ~1/(1 + v/1.5) for wind speed v in m/s
  (calm v<0.5 m/s keeps full depression; v≈6 m/s leaves almost none).
- **Humidity**: condensation releases latent heat, slightly damping how far
  below the dew point the surface can sink — a secondary effect we ignore,
  but the dew point itself is decisive for *whether ice appears*.

Combined working formula (calibrated to typical published surface-depression
ranges; it is a planning model, not a numerical weather model):

```
ΔT_radiative = (1 − 0.85·c) · 5.5 °C · 1/(1 + v/1.5)      (c = cloud fraction 0–1)
T_glass_min  = T_air_min − ΔT_radiative
```

Examples: clear calm (c=0, v=0.5): ΔT≈4.2°C; overcast windy (c=1): ΔT≈0;
clear + 4 m/s wind: ΔT≈1.5 °C.

## 2. Frost vs dew — the two-condition test
Ice on glass arrives by two paths:
1. **Deposition**: vapor → ice directly when surface < 0 °C **and** surface
   < dew point (frost grows feathery crystals, mostly at the edges/rubber
   first where cooling is fastest).
2. **Dew-then-freeze**: liquid condenses when surface < dew point above 0 °C,
   then air later falls below zero and the beads freeze into glaze (harder
   to scrape than feathery frost).

Verdict logic implemented:
```
if T_glass_min <= 0 and T_glass_min <= T_dew  -> FROST
elif T_glass_min <= -4                        -> HARD FROST (even modest dew -> thick glaze)
elif T_glass_min <= T_dew (but > 0)           -> DEW only (wipers handle it)
else                                          -> NO FROST, dry glass
```
Note bone-dry air (Tdew far below glass temp) can leave a "cold but clean"
windshield — no moisture, no ice. This is the most common missed factor in
folk forecasts.

## 3. Parked-car warm mass (duration curve)
A car just parked carries engine/cabin heat. Empirically glass runs ~+2 °C
above equilibrium for the first hour or two, decaying exponentially
(τ≈40 min). So a 90-minute cinema parking on a marginal night may not frost
while 8 h overnight will. The script prints glass temp at hours 1..N with
this offset decayed, crossing frost threshold at hour k when applicable.

Windshields also frost *inside* when cabin moisture is high and the glass
chills (parked breath/wet mats) — mention in tactics: crack windows to
flush humidity before parking on frost nights.

## 4. Frost classes and morning tactics
| Class | Glass min | What you'll find | Morning action |
|---|---|---|---|
| NONE | > 0 °C or dry | clean or dew beads | wipers if dew; done |
| LIGHT | −2…0 °C | thin white film, edges first | defrost 3–5 min + scraper pass; 2:1 water:IPA spray works |
| FROST | −4…−2 °C | full crystalline cover | cover tonight; 10 min defrost + scraper; lift wipers |
| HARD | ≤ −4 °C | thick glaze, wipers frozen in | engine + full defrost 10–15 min; NEVER hot water (thermal-shock cracks); de-icer or 50:50 IPA pour-along-edge; start 15 min earlier |

De-icer chemistry quick table:
- 2:1 water:isopropyl alcohol (≥70%) melts thin ice to ~−10 °C and lowers
  refreeze point — cheap, windshield-safe.
- Commercial de-icers add glycol ethers for lower temp; salt brine corrodes
  trim/chrome — avoid on cars.
- **Hot water: never.** ΔT>50 °C on cold tempered glass = crack risk,
  and it refreezes on wipers/seals within minutes.

## 5. Cover tactics
- Verdict FROST/HARD ⇒ covering pays: frost shield, towel, cardboard, or
  tarp over the glass (weighed). Morning: peel, shake, done — saves 5–10 min.
- Cover BEFORE dew falls (evening), on dry glass — a cover put on wet glass
  can freeze to it.
- Alternatives: park facing east (morning sun pre-heats glass), under a tree
  or carport (blocks sky view → kills depression), lift wiper arms.

## 6. Same physics, other targets
- House windows frost on the *inside* when indoor humidity is high and
  night radiative cooling chills the inner pane (single glazing) — the fix is
  humidity + air movement, not "warmer outside".
- Solar panels / roof / foliage: same formula, and why fruit growers spray
  water all night (latent heat release holds surface at 0 °C).
- EV range note: an iced windshield morning ≈ −10 °C morning; precondition
  while plugged in.

## 7. Model limits
- Single-layer steady-state estimate; real nights have evolving cloud/wind —
  use the *forecast minimum* period's average wind/cloud.
- ε and view factor vary (carport! tree!) — see §5 workarounds.
- Dew point drifts; use the evening value, err toward the more humid.
