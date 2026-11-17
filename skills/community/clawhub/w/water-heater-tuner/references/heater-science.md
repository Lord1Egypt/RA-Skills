# Water Heater Tuner — Reference

## The three-body problem of one dial

A tank water heater setpoint simultaneously controls:

1. **Scald risk at the tap** — burn injury is exponential in temperature
2. **Legionella risk in the tank** — bacterial growth is exponential in the
   20–45°C band and dies on a clock above 50°C
3. **Standby energy loss** — proportional to (tank − ambient)

These pull in opposite directions: safety-at-tap wants low, sanitation wants
high, cost wants low. The resolution is almost always **store hot, deliver
warm**: storage ≥ 60°C + anti-scald (mixing/thermostatic) valve delivering
≤ 49°C at the tap. Where no valve exists, the trade must be made explicitly —
which is what the `setpoint` verdict does.

## Scald: the burn-time table

Moritz & Henriques (1947) full-thickness burn thresholds (adult skin), the
basis for CPSC/UL/plumbing-code guidance:

| Water temp | Time to full-thickness burn (adult) |
|------------|--------------------------------------|
| 49°C / 120°F | ~10 minutes |
| 52°C / 125°F | ~90 seconds |
| 55°C / 131°F | ~17 seconds |
| 60°C / 140°F | ~3 seconds |
| 68°C / 154°F | ~0.5 seconds |
| 82°C / 180°F | ~instantaneous |

Children and elderly skin burns in roughly **a quarter** of the adult time,
and both groups have slower withdrawal reflexes. CPSC/codes (e.g. ASSE 1070)
target **≤ 49°C (120°F) delivery** for fixtures in homes with young children
or elders; many jurisdictions (e.g., following WHO) treat 50°C as the
practical scald boundary for the general adult population.

Practical scald arithmetic used by the tool:
- Child in household (age < 5) or elder (age > 75): delivery cap 49°C.
- Adults only: 50–52°C delivery is acceptable, still cautious.
- Delivery ≈ setpoint − pipe losses (1–3°C depending on run length/insulation;
  far taps lose more).

## Legionella: the sanitation clock

WHO "Legionella and the prevention of legionellosis" growth/kill profile:

- Multiplies 20–45°C (optimum ~37°C)
- < 20°C: dormant (no kill, no growth)
- 50°C: dies over many hours (weak disinfection)
- **60°C: ~32 minutes** for meaningful log reduction
- ≥ 70°C: seconds–minutes

Implications baked into the tool:
- Tank stored ≥ 60°C self-sanitizes continuously — the classic strategy.
- Stored 50–55°C: partial suppression; weekly thermal purge recommended.
- Stored < 50°C: the tank and dead-leg pipes are habitat; require the
  pasteurization protocol (heat 60°C+, hold 30+ min, flush EVERY outlet —
  hot taps, showers, and any rarely-used fixture — for 5 min at full hot).
- Stagnation is the amplifier: vacations, vacancies, low-use dead legs, and
  water softeners idle periods all raise risk independent of setpoint.

The disease is rare but severe (Legionnaires' pneumonia, ~10% case fatality
in community-acquired cases, higher in hospitals/immunocompromised). Homes
with immunocompromised residents should not store below 60°C, full stop.

## Energy: what a degree costs

Standby loss ≈ UA × (T_tank − T_ambient), so savings from lowering setpoint:

- Rule of thumb: **3–5% of water-heating energy per 10°F (5.6°C)** reduction
  (DOE-ish guidance; older under-insulated tanks trend to the high end).
- Bigger effect for: cold install locations (garage/basement), old tanks
  (less insulation), low-use households (standby is a bigger fraction).
- Smaller effect for: new high-insulation tanks, conditioned-space installs,
  high-use households.
- US household water heating ≈ 14–18% of home energy (DOE/EIA); the tool
  multiplies your fraction by the percentage to get $ per year.
- Companions the tool prices: tank blanket (older electric tanks, ~$20-40,
  5-10% on old units), pipe insulation on the first 2 m hot-side (~2-4%),
  heat-pump replacement (2-3× efficiency, climate-sensitive), drain-sediment
  flush annually (efficiency maintenance, esp. hard water).

## Recovery: the morning-shower math

First-hour rating (FHR) ≈ how much usable hot water (mixed to shower temp)
the tank delivers in the first hour. Typical 40-gal gas: FHR 60-70 gal;
electric: 45-55 gal (gas burners 30-40 kBtu/h vs electric elements 4.5 kW
× 2 ≈ but electric tanks often have smaller effective recovery).

Tool model (per fuel type):
- usable = tank_volume × (T_tank − T_shower) / (T_shower − T_inlet)
  (mixing arithmetic: a 40 gal tank at 60°C shower-mixed at 40°C with 10°C
  inlet yields ~80 gal of shower-temp water — the "hot water multiplier")
- consecutive-shower spacing: recovery power refills the multiplier while
  you wait; the tool reports minutes-between-showers to never run cold.

Winter matters: inlet drops 5-10°C and shrinks the multiplier ~15-25%.
That's why "fine in summer, cold by February" happens.

## Vacation / absence protocols

- ≤ 1 week: leave as-is (or vacation mode if the heater has one). Energy
  saved by going lower is a couple of kWh — not worth the return-flush.
- 1–4 weeks: vacation setting (≈ 7-10°C below normal) if available; else
  leave normal on GAS (pilot-only savings are small); on ELECTRIC you can
  switch off at the breaker — but plan the return protocol.
- > 4 weeks / property vacancy: full off + drain for freeze risk zones;
  otherwise off + return protocol.
- **Return protocol** (any off/low period > 1 week): restore setpoint, heat
  to ≥ 60°C, hold 30+ min, then run every hot outlet 5 min (carefully —
  it's scalding now: no kids, no elders, mind the hose-bib if plumbed hot).
  Healthy adults may simply flush 5 min; immunocompromised households run
  the full protocol.

## Field-measurement notes

- Measure at the NEAREST tap for scald (run 30 s, cup + thermometer) and
  the FARTHEST tap for legionella/logic.
- Heater dials are marketing: verify, then mark with a paint pen.
- After adjusting, re-measure 6-12 h later (tank thermal mass lags).
- Sediment (gas tanks, hard water): rumbling/popcorn sounds = flush 15 min
  via drain valve; restores burner efficiency and quiet.

## Verdict logic summary (what `setpoint` decides)

1. Immunocompromised resident? → storage ≥ 60°C mandatory + mixing valve 49°C.
2. Child <5 or elder >75, valve available? → store 60°C, deliver 49°C.
3. Child/elder, no valve? → setpoint 49-50°C + weekly pasteurize protocol
   (accepted trade: sanitation managed by protocol rather than storage temp).
4. Adults only, no valve? → 55-60°C storage is the pragmatic band
   (scald time at 55°C ≈ 17 s adult; manageable with care, still sanitizing-ish);
   50-52°C with pasteurize protocol acceptable in low-risk households.
5. Every verdict prints: the WHY (which constraint bound), the tap temps to
   verify, and the paired protocol if storage < 60°C.
