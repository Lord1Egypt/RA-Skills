---
name: smoker-pitmaster-planner
description: Low-and-slow BBQ planner that back-plans the whole cook from serve time. Newton-law heating model per meat class (rate scales with mass^-1/3), evaporative stall prediction with wrap-cut math, fuel budget (briquette/lump burn rates), USDA-safe pull temps with carryover, probe-mode ETA fitting from your live thermometer readings. Solves "when do I put the brisket on for Saturday 6PM dinner".
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [bbq, smoking, brisket, cooking, meal-planning, food-safety]
---

# Smoker Pitmaster Planner

Turns "I want to serve smoked brisket at 6 PM Saturday" into a dated timeline:
put-on time with uncertainty margin, when the stall will hit, wrap decision,
fuel needed, pull temp, rest window — and a probe mode that re-forecasts the
ETA from your live thermometer readings mid-cook.

## When to trigger
- "when do I start the brisket/pork butt/ribs for dinner at X"
- "how long does a 4 kg pork shoulder take at 110 °C"
- "my brisket has been stuck at 70 °C for 3 hours, is that normal?" (stall)
- "how much charcoal do I need for a 14-hour cook"
- "should I wrap or ride out the stall"
- planning any overnight low-and-slow smoke

## How it works

1. **Pick the meat and numbers**: meat class, weight (kg or lb), pit temp
   (°C or °F), serve time. Meat database is embedded: brisket, pork shoulder,
   spare/St-Louis ribs, baby backs, whole chicken, turkey, tri-tip, pork belly.
2. **Run the heating model** (`scripts/smoke_planner.py plan`):
   - Internal temp follows Newton's law: `T(t) = Tpit − (Tpit − T0)·e^(−k·t)`,
     with k per meat class calibrated to pitmaster rules of thumb
     (brisket ≈ 1–1.5 h/lb at 225 °F) and scaled by `(m_ref/m)^(1/3)`
     (thicker masses heat slower).
   - **Stall**: in the 65–75 °C band evaporative cooling plateaus the temp.
     Duration scales with mass; wrapping (Texas crutch) cuts it ~65 % and
     raises post-wrap k (foil = faster).
   - **Pull temp**: quality target (brisket/pork butt probe-tender ~93 °C)
     vs USDA-safe floor (poultry 74 °C, ground/meat 71 °C) — the script
     prints both and never lets quality override safety.
   - **Carryover + rest**: +2–4 °C carryover, then a rest window (1 h minimum,
     2–4 h in a cooler for big cuts — which also *buys schedule slack*).
3. **Fuel budget**: burn rate (kg/h) by cooker class at the chosen pit temp,
   total fuel with a +25 % reserve, water-pan reminder.
4. **Back-plan with margin**: cook time is multiplied by an uncertainty
   factor (default 1.25) for the put-on time; the script tells you your
   slack and what to do if you're early (hold longer) vs late (raise pit temp
   by 10–15 °C — the honest accelerator; "hotter and faster" beats ruin).
5. **Mid-cook** (`probe`): give elapsed time + current internal temp; the
   script fits k from your actual curve and re-forecasts done-time and the
   adjusted serve risk.

## Pitfalls encoded
- **The stall is not a malfunction.** 2–6 h flat at 65–75 °C is evaporative
  cooling; opening the lid "to check" extends it. Power through, wrap, or
  raise temp — but never serve an under-temp brisket out of impatience.
- **Never plan to the minute.** BBQ finishes when it finishes; the rest
  window is your buffer — use a longer rest as slack, not a delay.
- **Food safety floors are non-negotiable**: poultry 74 °C, ground/stuffed
  71 °C; pork quality-pull ~88–93 °C but trichina-safe far lower.
- **Fuel runs out at 4 AM**: budget with reserve; a minion/snake setup
  feeding for the full cook beats re-lighting mid-stall.
- **Thermometer placement**: fat cap vs point center can read 5–8 °C apart;
  probe the thickest part of the flat, not near bone or fat.

## Examples

```bash
# Brisket 6.5 kg at 110 °C, serve Sat 18:00 → timeline + fuel
python3 scripts/smoke_planner.py plan --meat brisket --weight-kg 6.5 \
  --pit-c 110 --serve "2026-11-28 18:00"

# Pork butt 4 kg, wrap planned, Fahrenheit
python3 scripts/smoke_planner.py plan --meat pork_shoulder --weight-lb 8.8 \
  --pit-f 225 --wrap --serve "2026-12-05 17:30"

# Mid-cook: 9.5 h elapsed, internal 71 °C, am I stalling?
python3 scripts/smoke_planner.py probe --meat brisket --pit-c 110 \
  --elapsed-h 9.5 --internal-c 71 --weight-kg 6.5

# Fuel only
python3 scripts/smoke_planner.py plan --meat pork_shoulder --weight-kg 5 \
  --pit-c 120 --serve "2026-12-24 14:00" --cooker offset
```

## Output contract
- dated timeline (put-on → stall window → wrap → pull → rest → serve)
- fuel kg with reserve, water-pan note
- slack analysis (hours of buffer, late/early protocol)
- probe mode: fitted k, ETA, stall status verdict
