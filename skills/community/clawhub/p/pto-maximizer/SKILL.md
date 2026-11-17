---
name: pto-maximizer
description: "Use when planning vacation days for the year: turns N PTO days into the maximum number of long weekends and extended breaks by bridging public holidays, warns about holiday blackout windows, balances consumption across quarters, and exports the full year plan with ICS calendar events."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [pto, vacation, holidays, long-weekends, calendar, work-life, planning]
---

# PTO Maximizer

## Overview

Most workers use vacation days reactively — a day here, a sick-ish Friday
there — and discover in November they're sitting on 6 unused days and a
use-it-or-lose-it deadline. The alternative is arithmetic: **public holidays
fall on fixed weekdays; a single PTO day adjacent to one buys a 4-day
weekend; two days around one can buy a 9-day break.**

The leverage points:

1. **Holiday bridges** — Mon holidays: take Tue–Fri? No: take **Fri (before
   a Mon holiday) or Tue (after)** for a 4-day weekend with 1 PTO day.
   Thu holidays (Thanksgiving-style): Fri is 1 day → 4-day weekend.
2. **Weekend stitching** — Sat+Sun on both ends converts 4 PTO days into a
   9-day arc (Sat … Sun) without anyone noticing you "took a week and a half."
3. **Quarter balancing** — spreading PTO across quarters avoids both the
   burnout stack (none until Q4) and the manager panic (all in Q3).
4. **Blackout awareness** — many employers freeze PTO in peak windows
   (retail Q4, finance quarter-close, tax season). The plan flags them.

The script computes, for a given country/year and PTO budget, the best-value
bridges: every placement of PTO days adjacent to holidays and weekends,
ranked by **days-off per PTO-day spent** (efficiency), with an efficiency
filter so you don't burn 5 days on a mediocre arc.

## When to Use

- Start of year / new job: building the annual PTO calendar
- "I have N days left and it's already [month]" — rescue planning
- Deciding whether to bridge a specific holiday (is it worth it this year?)
- Coordinating two calendars (partners) so overlapping weeks match
- Deciding when NOT to take off (blackout windows)

**Don't use for:** employer-specific policy math (accrual rates, carryover
caps, negative balances — read your handbook; the script takes a fixed
budget), or school-calendar coordination beyond US/UK/EU generic spring
breaks.

## The Bridge Math

The four canonical 1-day bridges (efficiency 4.0 — the best in the game):

| Holiday weekday | PTO placement | PTO days | Consecutive days off |
|---|---|---|---|
| Monday | Fri before | 1 | 4 (Fri–Mon) |
| Tuesday | Mon after | 1 | 4 (Sat–Tue) |
| Thursday | Fri after | 1 | 4 (Thu–Sun) |
| Friday | Mon before | 1 | 4 (Fri–Mon) |

Bigger shapes:

| Shape | PTO days | Consecutive off | Efficiency |
|---|---|---|---|
| Wed holiday: Tue or Thu | 1 | 2 (midweek pair) | 2.0 — bridge-poor |
| Fri–Mon bracket around a weekend holiday | 2 | 5–6 | 2.5–3.0 |
| Full week Mon–Fri | 5 | 9 (Sat–Sun arc) | 1.8 |
| Two adjacent holidays (e.g., Thu+Fri): Mon–Wed before | 3 | 10 (Sat–Mon) | 3.3 |

**Efficiency** = consecutive days off ÷ PTO days spent. Rules of thumb:

- Wed holidays are bridge-poor: 1 day buys only a 2-day midweek pair (2.0).
- Always check whether the observed holiday **shifts** (US: Sat→Fri, Sun→Mon
  observance; UK: bank-holiday substitution; Easter moves annually). The
  script applies these rules.

## Using the Script

```bash
# US worker with 15 PTO days, current year
python3 scripts/pto_planner.py --country US --year 2026 --budget 15

# UK, 25 days, avoid school-holiday price spikes flag (blackout = Aug peak)
python3 scripts/pto_planner.py --country UK --year 2026 --budget 25

# Only bridges worth >= 3.0 efficiency, JSON for further processing
python3 scripts/pto_planner.py --country US --year 2026 --budget 10 --min-eff 3.0 --json

# Reserve 5 days for a summer week; plan the rest as bridges
python3 scripts/pto_planner.py --country US --year 2026 --budget 15 --reserve-summer 5

# Export the chosen plan to calendar
python3 scripts/pto_planner.py --country US --year 2026 --budget 15 --ics pto_2026.ics
```

## The Plan It Produces

1. All public holidays for the country/year (with weekday + shift rules applied)
2. Every candidate bridge: PTO dates, consecutive off-days, efficiency
3. A greedy annual plan: pick highest-efficiency non-overlapping bridges until
   the budget runs out, with quarter-balancing preference
4. Blackout warnings where relevant (country-generic: US retail Q4 freeze,
   UK school summer peak pricing, EU August shutdowns = great for time off,
   terrible for deals)
5. ICS export of PTO days + resulting long weekends

## Common Pitfalls

1. **Forgetting observance shifts.** July 4 on Saturday is observed Friday
   July 3 (US federal); a bridge planned around "July 4 Monday" is fiction.
   The script applies US/UK shift rules.
2. **Bridging into blackout.** A perfect Thanksgiving bridge is worthless if
   the retail employer freezes November PTO. Set your real blackouts.
3. **Ignoring carryover caps.** US average cap ~5 days; plan to land under
   the cap by December, not at it.
4. **Spending everything on efficiency.** A 4.0-efficiency February bridge is
   not a vacation; the math optimizes days, you still need one actual week
   off. Use --reserve-summer for a real break.
5. **Team-calendar collisions.** Two senior people bridging the same holiday
   = manager vetoes both. Check the team calendar before committing.

## Verification Checklist

- [ ] Country + year correct (Easter/shift-dependent holidays move)
- [ ] Budget = actual remaining PTO (minus already-booked days)
- [ ] Blackout windows set to your employer's reality
- [ ] Quarter balance acceptable (no quarter > ~40% of budget unless intended)
- [ ] ICS imported and PTO days visible in the work calendar
