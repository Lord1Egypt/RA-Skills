# Smoker Pitmaster Planner

**Problem.** Low-and-slow BBQ is measured in half-days, crosses a multi-hour
temperature stall, and still has to land on a dinner time. Home pitmasters
start too late, panic during the stall, run out of charcoal at 4 AM, and
confuse quality pull-temps between species (chicken is not brisket).

**What it does.** A physics-grounded planning instrument:

- **Newton-law heating model** per meat class, rate scaled by `mass^(-1/3)`,
  calibrated to pitmaster rules of thumb (brisket ≈ 1.5 h/lb @ 225 °F).
- **Stall prediction** (evaporative plateau 65–75 °C) with wrap-cut math:
  the Texas crutch shortens the stall ~65 % and boosts post-wrap heating.
- **Back-planning from serve time**: put-on time with a 1.25× uncertainty
  factor, rest window as schedule buffer, carryover noted.
- **Fuel budget** by cooker class (kettle / offset / kamado / pellet) with a
  +25 % reserve — so the 4 AM burnout doesn't happen.
- **Probe mode**: feed your live thermometer reading; it fits the actual
  heating rate from your curve and re-forecasts the ETA, with a
  STALLED / BEHIND / ON TRACK verdict and the right response for each.

**Why broadly useful.** Tens of millions of households smoke meat; brisket
is the #1 showpiece cook and the #1 ruined one. Every BBQ forum thread is
some version of "help, when do I start / it's stuck at 160 °F". This skill
answers both with numbers instead of folklore.

**Example.**

```bash
python3 scripts/smoke_planner.py plan --meat brisket --weight-kg 6.5 \
  --pit-c 110 --serve 2026-11-28T18:00
# -> PUT ON BY Fri 13:47, stall window ~6h, ~9.4 kg charcoal w/ reserve

python3 scripts/smoke_planner.py probe --meat brisket --pit-c 110 \
  --elapsed-h 9.5 --internal-c 71 --weight-kg 6.5
# -> VERDICT: STALLED (normal) - do not open the lid
```

Not medical/legal advice; USDA poultry floor (74 °C) is always printed and
never overridden. MIT license.
