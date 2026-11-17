---
name: septic-load-balancer
description: Use when a home has a septic system and you need to schedule laundry/dishwasher/showers without drowning the drainfield, plan water use during heavy days (guests, laundry catch-up), or interpret slow drains/gurgling as hydraulic overload vs clog.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [septic, drainfield, water-management, laundry, home-maintenance]
---

# Septic Load Balancer

## Overview

A septic system is a biological reactor with a fixed daily processing budget. The tank can hold a lot; the **drainfield can only absorb so much effluent per day**. When a household stacks laundry (50 gal/load top-loader), long showers, and dishwashing into one Sunday, the drainfield saturates: slow drains, gurgling, soggy lawn over the field, and — repeated often enough — progressive bio-mat clogging that costs $10k–40k to replace.

The fix isn't using less water overall. It's **spreading the same gallons across days and hours** so the drainfield never sees a surge. This skill computes your system's hydraulic budget from tank size and (estimated) field capacity, audits a day's plan against it, and schedules heavy water use into safe slots.

## When to Use

- You own/rent a septic home and want a weekly laundry/dishwasher schedule.
- Guests arriving, holidays, laundry catch-up days, hot-tub drains, pool backwash.
- Slow drains or gurgling fixtures and you want to distinguish **hydraulic overload** (fix = spacing) from a clog/pump failure (fix = service call).
- Buying a house with septic: sanity-check system size vs household.
- After a pump-out: restart guidance and what to change so it doesn't recur.

Don't use for: sewage backing up into the basement (call a septic pro now), aerobic-unit control-panel alarms (different beast), or CAFO/commercial grease systems.

## How It Works

1. **Size the budget.** Typical residential: tank 750–1500 gal; drainfield absorption ~ sized to bedrooms at ~150 gal/bedroom/day design flow (older systems less). The daily budget = min(tank working volume ÷ 3, field design flow). Working with both gives honesty margins.
2. **Log a water inventory.** Fixtures and habits: showers (2.1 gpm × minutes), top-load washer 30–50 gal vs front-loader 12–20, dishwasher 4–10, toilets (1.6 vs 3.5 gal flush), faucets, softener regeneration (can backwash 40–100 gal!).
3. **Compute day + hour curves.** The script totals the day, flags the daily budget breach, and models the **hourly surge** (the tank equalizes; the field is what matters on a 2–4 h horizon).
4. **Schedule.** Spread laundry across the week (≤1 heavy load/day), move dishwasher to off-hours, sequence guests' showers 30+ min apart.
5. **Overload triage.** Symptom table: overload = all fixtures slow together, worse at day's end, lawn soggy over field; clog = one fixture; pump failure = alarm or total stoppage.

## Data & Physics

**Design flow:** ~150 gal/bedroom/day is the classic sizing figure; a 3-bedroom field is nominally sized for 450 gal/day. A water-softener regeneration mid-morning can dump 60+ gal in an hour — a hidden surge the field never "planned" for.

**Tank equalization:** the tank buffers short surges; trouble comes from (a) daily total above field capacity for days in a row, and (b) large single-hour slugs that push solids out (suspended solids carryover accelerates bio-mat clogging). Rule of thumb: **keep any single hour under ~15% of the tank working volume** and the daily total under field capacity.

**Garbage disposal:** adds solids load; tank needs pumping ~2× as often.

**Laundry lint:** non-degradable fibers mat the field; use a lint filter on older washers, prefer front-loaders.

## Worked Examples

`python3 scripts/septic_balancer.py --demo` — a household doing 6 top-loader loads every Sunday + guests showering: breaches both the daily budget and the hourly surge cap → rescheduled across Tue/Thu/Sat with slot assignments.

`python3 scripts/septic_balancer.py --tank-gal 1000 --bedrooms 3 --laundry-loads 6 --washer top --showers 6 --shower-min 10 --guests 2` → verdict with a day-by-day redistribution.

## Common Pitfalls

1. **"Big tank = invincible."** The tank is a buffer; the field is the bottleneck. You can drown a healthy field with a 1500-gal tank.
2. **Sunday laundry marathon.** 6 top-load loads = 200–300 gal in 5 hours. The single most common self-inflicted overload.
3. **Water softener on a timer, regenerating at 2 AM... into a field that's already saturated from evening use.** Move regeneration to low-use mornings and space it from laundry day.
4. **Consecutive-guest showers.** Three 15-minute showers back-to-back = ~95 gal in 45 min. Space them 30 min.
5. **Reading a clog as overload (or vice versa).** All-fixtures-slow-together + soggy field = overload. One slow sink = local clog. Total stoppage/alarm = pump/tee failure → service call.
6. **Hot tub / pool backwash drained to the septic.** Never. Bypass to a permitted surface discharge or haul.
7. **Ignoring the lint problem.** Front-loaders halve both water AND lint; a $15 lint trap saves field life on old machines.
8. **Pumping the tank "because it was full."** Tanks are supposed to be full (that's the working volume). Pump on sludge/scum depth (measure yearly, ~every 3 yr typical), not on "looks full."

## Verification Checklist

- [ ] Tank size and bedroom count entered (from pump-out receipt or county records)
- [ ] A real week of water habits inventoried honestly (include softener!)
- [ ] Daily totals vs budget checked for every day of the plan
- [ ] Hourly surge cap checked on the busiest day
- [ ] Laundry redistributed so no day exceeds the verdict's allowance
- [ ] Overload symptoms (if any) triaged: spacing fix vs service call
