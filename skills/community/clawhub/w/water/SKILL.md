---
name: Water Tracker
slug: water
version: 1.0.4
description: >-
  Tracks daily water intake from casual mentions and sets hydration targets
  from weight, exercise, heat, and health context. Use when the user logs a
  drink ("had a glass", "finished my bottle"), asks how much water they should
  drink or whether they drink enough, reports thirst, dark urine, dry mouth,
  cramps, or a headache that could be dehydration, plans fluid or electrolyte
  replacement for workouts, races, sauna, hiking, flights, or hot weather, or
  needs rehydration guidance during fever, vomiting, diarrhea, or a hangover,
  or asks whether tap, bottled, filtered, mineral, or sparkling water is safe
  or better. Not for meal or calorie logging.
homepage: https://clawic.com/skills/water
changelog: "Full coverage pass: deeper guides, situation-named files, and per-user configuration"
metadata:
  clawdbot:
    emoji: "💧"
    displayName: Water Tracker
    configPaths:
    - ~/Clawic/data/water/
---

Hydration tracking and advice from conversational mentions. All persistent data lives in `~/Clawic/data/water/` — `log.md` (daily entries), `memory.md` (learned containers, baseline, patterns), `config.yaml` (declared preferences); this skill reads and writes only that folder. Health context stays local: nothing is uploaded, shared, or sent anywhere, and no credentials or identifiers are stored. If you have data at an old location (`~/water/` or `~/clawic/water/`), move it to `~/Clawic/data/water/`. First use: read `setup.md`; file formats in `memory-template.md`.

## When To Use

- User mentions drinking anything ("had water with lunch", "finished my bottle") and wants intake tracked
- User asks how much water they should drink, or whether they drink enough
- User reports thirst, dark urine, headache, cramps, or fatigue and hydration is a plausible factor
- User plans or logs exercise, sauna, a flight, altitude, or hot weather — or is sick (fever, vomiting, diarrhea, hangover) — and asks what or how much to drink
- Mode: act-as tracker (log without commentary) plus advise (targets and adjustments) when asked
- Not for meal or calorie logging (route to calories) and not for diagnosing illness (see Red Flags)

## Quick Reference

| Situation | Play |
|---|---|
| Drink mentioned, no size given | Log the default size for that container (Logging Defaults), flag as estimated; parsing edge cases → logging.md |
| First mention of a personal container ("my bottle") | Ask its size once, store in memory.md, never ask again |
| "How much should I drink?" | 30-35 ml x body weight in kg per day (Rule 1); weight unknown → 1600 ml (women) / 2000 ml (men) |
| Exercise or sports session mentioned | Add 500-1000 ml per sweaty hour to today's target; regular trainers → sweat-rate test in exercise.md |
| Session over 90 min, or heavy sweating | Sodium matters as much as volume → electrolytes.md |
| Hot day (above 30 C), sauna, sun labor | Raise today's target 250-500 ml without announcing it; heat, cold, acclimatization → environment.md |
| Flight or altitude above 2500 m | Dry-air losses the user won't feel → environment.md |
| Headache or fatigue mentioned | Check today's log first; only if intake is below half of target by mid-afternoon, suggest water once |
| Fever, vomiting, or diarrhea | Oral rehydration solution, not plain water → illness.md; run Red Flags first |
| Hangover mentioned | Real but modest deficit; rebound protocol → illness.md |
| Pregnancy, kidney stones, heart or kidney disease, diuretics | Target changes or formulas suspend → conditions.md |
| Active fasting window | Water, black coffee, and plain tea do not break a fast; fasts over 24 h need electrolytes (→ fasting skill) |
| Tap vs bottled, filter choice, travel water safety | Taste and context, not fear; certifications, boil rules, lead → quality.md |
| User asks for trends or opted into summaries | Weekly summary format → habits.md |
| Any other hydration mention (default) | Log without comment with timestamp and estimated ml; no comment, no reminder, no target talk |

Depth on demand: `logging.md` mention→ml parsing, calibration, day boundaries · `exercise.md` sweat rate, endurance, hyponatremia · `environment.md` heat, cold, altitude, flights · `illness.md` fever, GI losses, hangover, kids and elderly · `electrolytes.md` sodium, ORS, sports drinks · `conditions.md` stones, pregnancy, fluid restriction, medications · `habits.md` pattern detection, summaries, habit design · `quality.md` tap, bottled, filters, travel safety · `setup.md` first run · `memory-template.md` file formats.

## Core Rules

1. Daily fluid target = 30-35 ml x body weight in kg. Worked example: 70 kg → 2100-2450 ml. Weight unknown → default 1600 ml (women) / 2000 ml (men), the ~80% drinking-fluid share of EFSA adequate total-water intake (2.0 L women / 2.5 L men, food water included). Never quote 3.7 L or 2.7 L as a drinking target: those NAM figures are total water including the 20-30% that comes from food.
2. Count all non-alcoholic drinks at 100%: coffee, tea, milk, soup, sparkling water. Up to 400 mg caffeine per day produces no net fluid loss in habitual drinkers (Armstrong). Alcohol counts as 0 ml.
3. Estimate first, ask later. Use the Logging Defaults table, flag the entry as estimated, and only ask when the ambiguity changes the day total by more than 20% ("bottle" could be 500 or 1000 ml → ask; "a glass" → just log 250).
4. Judge status by urine, not by totals hit. Pale straw = on target regardless of ml logged; dark (5 or above on the 8-level Armstrong chart) at midday = deficit, drink 500 ml now; completely colorless at every void = overshooting, ease off. First morning urine is always dark and proves nothing.
5. Thirst is a lagging signal: it appears at roughly 1-2% body mass already lost, and measurable performance drop starts near 2% (ACSM). For planned long efforts, schedule intake instead of waiting for thirst. Adults over 65 have blunted thirst: schedule for them by default.
6. Cap intake rate at about 1 L per hour sustained; the gut absorbs little more, and plain water beyond sweat losses dilutes sodium. Body weight GAIN during exercise = overdrinking, stop fluids (exercise hyponatremia hit 13% of Boston Marathon finishers in the Almond study).
7. History of kidney stones changes the target: drink enough to produce at least 2.5 L urine per day (AUA), which means roughly 3 L intake. This overrides Rule 1 upward.

## Logging Defaults

Default sizes when the user does not specify (store personal overrides in memory.md after one calibration; parsing rules in logging.md):

| Container | Default |
|---|---|
| Glass, cup of water | 250 ml |
| Large glass, tumbler | 400 ml |
| Mug (tea, coffee) | 300 ml |
| Can | 330 ml |
| Small bottle | 500 ml |
| Sports bottle | 750 ml |
| Large bottle | 1000 ml |
| Bowl of soup, glass of milk or juice | 250 ml |
| "Some water", "a sip" | 100 ml |
| Restaurant glass with refills | 250 ml per mention; count refills only if stated |

Reporting default: silent logging, summary only when asked or per the `reporting` variable. Never send missed-glass reminders; nagging is the main reason users abandon hydration tracking (habits.md for what works instead).

## Target Adjustments

Stack on top of the Rule 1 baseline; conditions.md restrictions override everything.

| Context | Adjustment | Depth |
|---|---|---|
| Exercise | +500-1000 ml per sweaty hour, during and after | exercise.md |
| Heat above 30 C or direct sun | +250-500 ml per day of exposure | environment.md |
| Hard labor in heat | Sweat runs 1-2 L per hour — treat as exercise, not weather | exercise.md |
| Flight | +250 ml per hour in the air (estimate; 10-20% cabin humidity) | environment.md |
| Altitude above 2500 m | Losses rise; drink for losses, urine color governs | environment.md |
| Pregnancy | +300 ml per day (EFSA) | conditions.md |
| Breastfeeding | +700 ml per day (EFSA) | conditions.md |
| Fever, vomiting, diarrhea | Volume alone is wrong — losses include electrolytes | illness.md |
| Kidney stone history | At least 2.5 L urine per day (AUA), roughly 3 L intake (Rule 7) | conditions.md |

## Red Flags

| Signal (observable) | Suspicion | Action |
|---|---|---|
| No urination for 8+ h despite drinking, dizziness on standing, very dry mouth | Severe dehydration | Same-day clinician; emergency care if confusion or fainting |
| Headache, nausea, bloating, or confusion during or after a long endurance event with heavy drinking | Exercise-associated hyponatremia | Emergency care; do NOT give more water |
| Confusion or collapse in heat, skin hot with sweating stopped | Heat stroke | Emergency care; active cooling; sips only if fully alert |
| Extreme thirst plus urinating far more than usual, persisting over a week | Diabetes (mellitus or insipidus) | Clinician within days, mention both symptoms |
| Dark urine with yellowed skin or eyes, or flank pain | Liver or kidney problem, not simple dehydration | Clinician; urgent if pain is severe |
| Vomiting or diarrhea beyond 24 h in a child or elderly person, or fluids not staying down | Dehydration risk in a vulnerable person | Same-day care; oral rehydration solution meanwhile |
| User has heart failure, kidney disease, cirrhosis, or takes lithium or diuretics, and asks to raise intake | Fluid restriction may apply; formulas here are unsafe | Clinician sets the target; suspend Rules 1-7 |

Anything in this table suspends the protocols above: route to a clinician.

## Output Gates

Before replying to any hydration-related message, verify:

- Drink mention → entry appended to log.md before anything else; reply is a one-line acknowledgment at most, no unsolicited advice?
- Any target quoted → computed from stored weight or the sex defaults (Rule 1), never a flat 2 L or "8 glasses"?
- About to suggest drinking more → today's log checked AND no Red Flags row matches?
- About to ask a question → answer not already in memory.md, and it is either the one-time container calibration or a decision the defaults cannot resolve?
- Any number given → traceable to a rule or table in this skill, not improvised?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/water/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| units | metric \| imperial | metric | Displays logs and targets in ml or fl oz (conversion in logging.md); storage stays in ml |
| weight_kg | number (30-200 kg) | none | Enables the Rule 1 target; absent → 1600 ml (women) / 2000 ml (men) defaults |
| daily_target_ml | number (ml) | computed from Rule 1 | User- or clinician-set override; Target Adjustments still stack unless conditions.md suspends them |
| reporting | silent \| daily \| weekly | silent | When intake summaries are volunteered (format in habits.md) |
| climate | temperate \| hot | temperate | hot applies the +250-500 ml heat adjustment as standing baseline instead of per-day judgment |

Preference areas — customizable dimensions; a stated preference gets recorded in config.yaml and applied:

- **Beverages** — drinks the user wants excluded or counted differently ("don't count soda") — modifies Rule 2 at log time
- **Containers** — personal container sizes; learned once via calibration, stored in memory.md, never re-asked
- **Schedule** — fasting windows, pre-bed cutoff, front-loading — shapes when suggestions land (habits.md)
- **Activity** — training days and sport — pre-applies the exercise adjustment on those days (exercise.md)
- **Medical context** — declared conditions or clinician-set numbers — override Rule 1 per conditions.md; never inferred from symptoms
- **Tone** — summary verbosity, encouragement vs bare numbers — affects habits.md summaries only

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Pushing "8 glasses" or a flat 2 L on everyone | The famous figures are total-water averages that include food water; a 55 kg and a 95 kg user differ by over a liter | Weight formula (Rule 1) plus Target Adjustments |
| Counting only plain water | Coffee, tea, milk, and soup hydrate at effectively 100%; excluding them undercounts by 30-50% for many users | Log all non-alcoholic fluids (Rule 2) |
| Asking container size on every log | Each question adds friction; users stop reporting within days | Calibrate once, store in memory, reuse forever |
| Double-logging a re-mentioned drink | "Finished my bottle" after earlier sips from the same fill inflates the day | Check log.md for an open partial first; log the remainder (logging.md) |
| Answering every headache with "drink more water" | Post-race headache with heavy drinking can be hyponatremia; more water is the wrong direction | Check the day's log and context first (Quick Reference row) |
| Reading dark first-morning urine as dehydration | Overnight concentration is normal physiology | Judge from a midday sample (Rule 4) |
| Reading sauna or hot-yoga scale loss as fat loss | The loss is water; it returns with rehydration | Say so, then apply the replacement rule (exercise.md) |
| Letting the user chug the day's deficit at night | Exceeds the 1 L per hour absorption cap (Rule 6) and wrecks sleep with nocturia | Close the day as-is; front-load tomorrow (habits.md) |
| Sending reminder pings for missed intake | Nagging converts a passive habit into a chore; abandonment follows | Silent logging; surface trends per `reporting` or on request |
| Applying the standard formula to users with heart or kidney conditions | These conditions can require fluid restriction; the formula can cause harm | Red Flags last row: clinician sets the number (conditions.md) |

## Where Experts Disagree

- **Drink to thirst vs programmed drinking.** The exercise-hyponatremia consensus (Hew-Butler) pushes drink-to-thirst for endurance events because overdrinking kills and underdrinking rarely does; ACSM programs intake for hard efforts in heat where thirst lags real losses. Boundary: fast, hot, or over-4-h efforts and adults over 65 → schedule it; recreational sessions → thirst plus the sweat-rate test (exercise.md).
- **Water as a weight-loss or skin tool.** Pre-meal water (about 500 ml) showed a modest weight-loss effect in one dieting RCT (Dennis); skin-appearance claims lack evidence. Offer the pre-meal trick when asked; never promise skin or metabolism effects.
- **Is plain water the best rehydrator?** For everyday life, yes. After heavy one-shot losses, drinks with sodium and nutrients are retained measurably longer (Maughan's beverage hydration index — details in electrolytes.md); the boundary is losses, not preference.

## Related Skills

More Clawic skills, get them at https://clawic.com/skills/water (install if the user confirms):

- `fasting` — eating-window rules and electrolyte protocol for fasts over 24 h
- `calories` — meal and drink logging when the user tracks food, not just fluids
- `running` — race-day fueling and pacing where fluid plans meet training plans
- `gym` — workout logging that feeds the exercise adjustment automatically

## Feedback

- If useful, star it: https://clawic.com/skills/water
- Latest version: https://clawic.com/skills/water

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/water.
