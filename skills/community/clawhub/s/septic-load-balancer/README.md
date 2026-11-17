# Septic Load Balancer

**Your septic tank can take the volume. Your drainfield can't take the schedule.**

About 20% of US homes (and most rural homes worldwide) run on septic. The system has a fixed daily processing budget — and the classic household pattern of "laundry marathon Sunday + everyone showers before guests arrive" blows straight through it. The result reads as mysterious slow drains and a soggy lawn, and repeated often enough becomes a $10k–40k drainfield replacement. The fix is almost never less water; it's **the same water, spread out**.

## What this skill does

- **Budget computation** from tank size + bedrooms the field was sized for (design-flow model, with the tank working-volume constraint — whichever binds first).
- **Day-plan audit**: laundry loads × washer type, showers, dishwasher, softener regen, guests → daily total vs budget, peak hour vs solids-carryover surge cap.
- **Redistribution solver**: converts "6 loads Sunday" into a safe day-by-day laundry plan.
- **Overload-vs-clog triage table**: all-fixtures-slow = spacing problem; one fixture = plumbing; alarm/stoppage = pump, call now.
- **Levers ranked**: front-loader switch (2.5×), softener regen timing, shower staggering, the leaky-toilet silent killer.

## Quick start

```bash
# Demo: 4 people, 6 top-load loads, softener regen, 6 showers -> overloaded, rescheduled
python3 scripts/septic_balancer.py --demo

# Your system: 1000-gal tank, 3-bedroom field, 2 front-load loads, couple
python3 scripts/septic_balancer.py --tank-gal 1000 --bedrooms 3 \
    --laundry-loads 2 --washer front --persons 2
```

## Why it matters

- Drainfield replacement is among the most expensive single-family repair outside the foundation; spacing water use is free.
- The failure is cumulative and invisible: bio-mat clogging gives no warning until slow drains, then soggy lawn, then backup.
- Guest weekends and laundry catch-up days are exactly when systems take their worst hits — and exactly when this tool earns its keep.

## What's inside

```
SKILL.md                        triggers, budget model, scheduling doctrine, pitfalls
references/septic-hydraulics.md sizing tables, symptom triage, field-killers ranked
scripts/septic_balancer.py      audit + redistribution engine (stdlib-only, offline)
```

## Scope & honesty

Budget numbers are classic design-flow estimates; actual field capacity varies with soil type and condition. If drains are slow for days on end or sewage surfaces: stop water use and call a septic professional — this tool schedules prevention, not remediation.
