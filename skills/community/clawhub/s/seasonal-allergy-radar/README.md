# Seasonal Allergy Radar

**Stop discovering your allergy season by sneezing through it.** Correlates
your daily symptom scores with month-level pollen calendars for your
climate zone, identifies which pollen class actually drives YOUR symptoms
(with lag — priming is real), forecasts the next two weeks, and tells you
when to start medication (before the season, when it actually works).

## The real-world problem

10–30% of adults have allergic rhinitis. Most manage it reactively: symptoms
start, then they medicate — weeks behind, because antihistamines and nasal
steroids work best started 1–2 weeks BEFORE exposure. Nobody connects three
things they already have: their symptom pattern, their region's pollen
calendar, and medication lead times.

## What it does

- **Symptom log** — 10-second daily JSON entries (score 0–5 + systems);
  zeros matter as much as spikes
- **Zone calendars** — month-level tree/grass/weed risk for 5 climate
  zones (temperate, Mediterranean, continental, subtropical, coastal-low)
- **Trigger correlation** — Pearson r between your log and each pollen
  class's daily risk curve, lag-searched 0–7 days; reports your primary
  trigger, contributors, and worst days
- **Personal 14-day forecast** — your logged severity calibrated against
  upcoming calendar risk, with HIGH-risk day flags
- **Pre-medication planner** — back-dated antihistamine/nasal-steroid
  start dates from your target season onset; immunotherapy referral
  threshold from your own data

## Quick start

```bash
python3 scripts/allergy.py log init --from 2027-03-01 --days 90 --out my.json
python3 scripts/allergy.py log add --log my.json --date 2027-04-14 --score 4 --eyes --nose
python3 scripts/allergy.py correlate --log my.json --zone temperate-northern
python3 scripts/allergy.py forecast --log my.json --zone temperate-northern --from 2027-05-01
python3 scripts/allergy.py plan --zone temperate-northern --target tree --year 2027
```

Stdlib-only Python 3. Not a medical device — red-flag symptoms (wheezing,
chest tightness) go to a doctor, not a log.

## License

MIT © 2026 Denis Voronin
