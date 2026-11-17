---
name: seasonal-allergy-radar
description: Use when pollen ruins your springs (or you're moving/traveling and want to know what you're walking into) — correlates your daily symptom scores with regional pollen calendars (tree/grass/weed by month for your climate), computes your personal trigger lag and severity curve, forecasts the next 2 weeks of your symptoms from the calendar, and builds a pre-medication plan (antihistamine start before season, not after symptoms).
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [allergy, pollen, hay-fever, seasonal-allergies, health-tracking, antihistamines]
---

# Seasonal Allergy Radar

## Overview

Hay fever suffers through the same 6-week misery every year, then repeats
it — because nothing connects three facts they already have: **when their
symptoms spike**, **what pollinates when in their region**, and **that
antihistamines work best started 1–2 weeks BEFORE the season**.

This skill connects them:

1. **Symptom log** — 10-second daily entries: overall score 0–5 + affected
   systems (eyes/nose/lungs/skin). No app account, no cloud — a JSON file.
2. **Regional pollen calendar** — month-by-month tree/grass/weed risk for
   your climate zone (temperate-Northern, Mediterranean, continental,
   subtropical, coastal-low-pollen). Curaated from aerobiology network
   patterns (see references).
3. **Correlation engine** — aligns your log against the calendar, tests
   lags 0–7 days, and reports which pollen class(s) your symptoms track
   with correlation coefficient + your personal onset/peak.
4. **14-day personal forecast** — calendar × your fitted severity curve →
   expected symptom score per day, with "start/step-up medication" flags.
5. **Pre-medication planner** — antihistamine start dates (season minus
   10–14 days), nasal steroid ramp (they need days-weeks to peak effect),
   ophthalmologist-grade eye-drop timing, and an allergist-visit brief
   from your data.

## When to Use

- "Every April I'm wrecked — is it tree or grass?" → correlation + calendar
- Planning a move or a trip during your allergy season
- "When should I start my antihistamine this year?" → pre-med plan
- Deciding if OTC management is enough or symptoms warrant an allergist
- Multi-year: "is it getting worse?" → season-over-season severity trend

**Don't use for:** asthma management, food allergy, anaphylaxis history,
or substituting an allergist's testing (skin prick/IgE) — this is a
pattern instrument, not a diagnostic one. Red-flag symptoms (wheezing,
chest tightness) → doctor, not a log.

## Quick Start

```bash
# 1. Print a month of blank log entries (paper or notes-app friendly)
python3 scripts/allergy.py log init --from 2027-03-01 --days 31 --out my_log.json

# 2. Record a day (takes 10 seconds)
python3 scripts/allergy.py log add --log my_log.json --date 2027-03-14 \
    --score 4 --eyes --nose

# 3. What's in the air this month where I live?
python3 scripts/allergy.py calendar --zone temperate-northern

# 4. Correlate my log against the calendar (which pollen is me?)
python3 scripts/allergy.py correlate --log my_log.json --zone temperate-northern

# 5. My personal 14-day forecast + med flags
python3 scripts/allergy.py forecast --log my_log.json --zone temperate-northern \
    --from 2027-04-01

# 6. Pre-medication plan for my main season
python3 scripts/allergy.py plan --zone temperate-northern --target tree \
    --year 2027 --antihistamine cetirizine --nasal-steroid fluticasone
```

## Symptom Log Format

One JSON file, one entry per day:
```json
[
  {"date": "2027-03-14", "score": 4, "systems": ["eyes", "nose"], "note": "driving with windows open"}
]
```
- `score` 0 (nothing) to 5 (incapacitating)
- `systems` any of `eyes nose lungs skin`
- Best data: log EVERY day through the season, even good days —
  correlation needs the zeros as much as the spikes.

## Pollen Calendar Zones

| Zone | Tree season | Grass season | Weed season |
|---|---|---|---|
| temperate-northern | Feb–May (birch/oak peak Apr) | May–Jul (peak Jun) | Jul–Sep (ragweed Aug–Sep) |
| mediterranean | Jan–May (cypress! olive Apr–Jun) | Apr–Jun | Jun–Sep |
| continental | Apr–Jun (birch May) | Jun–Jul | Jul–Sep (mugwort) |
| subtropical | near-year-round trees | Mar–Oct ( Bermuda ) | Jul–Nov |
| coastal-low | low overall; some grass May–Aug | | |

(Calendars are 3-week windows around these peaks; script holds the month-level table.)

## How Correlation Works

For each pollen class (tree/grass/weed):
1. Build the calendar's daily risk curve for your zone (0–3 scale).
2. For lag L in 0–7 days: Pearson r between your score(t) and pollen(t−L).
3. Best |r| wins; report r, lag, your days-worst percentile, inferred onset
   and peak dates from your own entries.
4. If no class clears |r| ≥ 0.35, verdict = "no clear pollen driver —
   consider dust-mold-indoor factors or an allergist."

The lag matters clinically: symptoms can trail pollen by 1–3 days (priming
effect), and antihistamines taken after onset fight a losing battle —
receptor saturation works best pre-exposure.

## Common Pitfalls

1. **Logging only bad days.** Correlation needs baseline zeros; a log of
   only flare days correlates with everything.
2. **Starting meds when symptoms start.** Second-generation antihistamines
   reach steady effect in 1–3 days but work best on unstained mast cells;
   nasal steroids need 1–2 weeks to plateau. The `plan` command back-dates
   starts from the season onset accordingly.
3. **Wind vs insect pollinated.** Showy flowers are rarely your problem;
   birch/grass/ragweed are wind-pollinated and produced in millions of
   grains per day. The calendar is built from wind-pollinators.
4. **Rain resets.** Pollen drops during rain, spikes after (fragrance +
   burst grasses). A single rainy week can look like "cure" — it's weather,
   not tolerance.
5. **Cross-reactivity confusions.** Birch-apple, mugwort-celery oral
   allergy syndrome: your "sudden fruit allergy" each April may be the
   tree pollen priming your mouth. Correlate before eliminating foods.

## Verification Checklist

- [ ] Log has ≥ 21 days with honest zeros included
- [ ] Zone matches actual climate (not vacation spots in the log period)
- [ ] Correlation |r| ≥ 0.35 before trusting any trigger verdict
- [ ] Med start dates back-dated before calendar onset
- [ ] Red-flag symptoms (wheezing/chest) routed to a doctor, not the log

## One-Shot Recipes

**"What am I allergic to?" (one season of data):**
```bash
python3 scripts/allergy.py log init --from 2027-03-01 --days 90 --out s.json
# ...log daily...
python3 scripts/allergy.py correlate --log s.json --zone temperate-northern
```

**This year's pre-med calendar (birch-sensitive):**
```bash
plan --zone temperate-northern --target tree --year 2027 \
     --antihistamine cetirizine --nasal-steroid fluticasone
```

**Trip planning — "April in Lyon vs Lisbon":**
```bash
calendar --zone mediterranean
forecast --log my_log.json --zone mediterranean --from 2027-04-05
```
