---
name: sleep-shift-survivor
description: "Use when you work nights, rotating shifts, or on-call and your body has no idea when to sleep — generates shift-specific sleep schedules from circadian science: forward-rotation adaptation plans (phase delay is easier than advance), anchor-sleep windows for rapidly rotating schedules, strategic caffeine cutoffs timed to shift end not start, light/dark exposure choreography (bright light during night shifts, dark commute home, blackout sleep), clock-shift transition plans for switching between day and night blocks, drowsy-drive risk warnings on post-shift commutes, and shift-work disorder screening flags — because 20 percent of the workforce does shift work and gets told to just sleep more."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [shift-work, sleep, circadian, night-shift, health, scheduling]
---

# Sleep Shift Survivor — Circadian Planner for Shift Workers

## Overview

~20% of workers in industrialized countries do shift work; nurses, drivers, factory, security, IT on-call, hospitality. Shift work disorder is real (excessive sleepiness + insomnia, ~10-30% prevalence among night workers), the health risks are documented (metabolic, cardiovascular), and the standard advice — "keep a regular schedule" — is useless to someone whose shift *rotates*.

Circadian science actually has usable answers, and this skill operationalizes them:

1. **Forward rotation preference** — delaying sleep (later) is physiologically easier than advancing (earlier); rotations should go day → evening → night, and transition plans are built on delaying.
2. **Anchor sleep** — when shifts rotate too fast to adapt, keep a *common anchor window* (e.g. 04:00–08:00) that's sleep-time in EVERY shift block; the circadian clock gets one stable signal, nap blocks flex around it.
3. **Strategic caffeine** — caffeine has a ~5-6h half-life; timing it to shift *start* guarantees it's still active at attempted sleep. Cutoffs are computed per shift end + buffer.
4. **Light choreography** — bright light during night work (shifts the clock later), dark sunglasses on the morning commute home (prevents morning light from snapping the clock back), blackout conditions for day sleep.
5. **Drowsy-drive defense** — the post-night-shift morning commute is among the highest-risk driving windows there is; the planner flags it with concrete countermeasures and a "don't drive" threshold.

## When to Use

- **Permanent night shift** — build a stable inverted schedule with anchor sleep
- **Rotating shifts** (day/evening/night, fast or slow rotation) — transition plans between blocks + anchor window
- **On-call / pager duty** — fragmented sleep strategy: anchor + strategic naps + post-call recovery
- **Clock-change blocks** — switching from a run of days to a run of nights (or back)
- **Post-shift morning commutes** — drowsy-drive risk assessment
- **Screening** — persistent excessive sleepiness/insomnia for ≥3 months on shift work → shift-work-disorder flags (informational; a doctor diagnoses)
- Don't use for: jet lag (different mechanics — phase-shifting travel), regular day-work sleep complaints, or diagnosed sleep disorders without medical care.

## How It Works

1. **Define your schedule** — `schedule add` with a rotation pattern (e.g. `2D 2E 2N 4off` — 2 days, 2 evenings, 2 nights, 4 off) and shift times.
2. **Generate the plan** — `plan --from 2026-10-01 --days 28` produces the dated schedule: sleep windows per day (anchor-aware), naps, caffeine cutoff times, light/dark instructions per block.
3. **Transitions** — when a day-block follows a night-block (or vice versa), the plan inserts a clock-shift transition sequence (delay-by-2h steps, or a 24h+ hard reset for long breaks).
4. **Commute risk** — every night-shift morning is flagged; `commute` prints the countermeasure card for a specific shift end.
5. **Log & screen** — `log` records actual sleep per day; `screen` checks shift-work-disorder flag criteria from the log; `report` summarizes sleep debt, anchor compliance, and schedule friction.

## Commands

```bash
# Define a rotation: 2 days, 2 evenings, 2 nights, 4 off
python3 scripts/shift_sleep.py schedule add "hospital" --pattern 2D,2E,2N,4off \
    --day 07:00-15:00 --evening 15:00-23:00 --night 23:00-07:00
python3 scripts/shift_sleep.py schedules

# The dated plan (sleep windows, naps, caffeine cutoffs, light instructions)
python3 scripts/shift_sleep.py plan hospital --from 2026-10-01 --days 14

# Commute risk for a night shift ending 07:00
python3 scripts/shift_sleep.py commute --night-ends 07:00

# Log real sleep & screen
python3 scripts/shift_sleep.py log hospital --date 2026-10-03 --slept "08:30-14:00" --quality 3
python3 scripts/shift_sleep.py screen hospital
python3 scripts/shift_sleep.py report hospital
```

Storage: `shift_sleep.json` in cwd. 100% local. Informational planning, not medical advice — persistent symptoms → occupational health or sleep medicine.

## Plan Elements (what each day shows)

| Element | Rule of thumb |
|---|---|
| Anchor sleep | fixed window (default 04:00–08:00) present in EVERY block when rotation is fast |
| Main sleep | longest window aligned to block: nights → morning-after sleep; days → night sleep |
| Strategic nap | 90 min (one full cycle) or 20 min (avoid slow-wave wake) before first night shift |
| Caffeine cutoff | shift end + 6h (half-life out of sleep attempt); flagged on every day |
| Bright light | during night shifts (first half); avoid in last 2h before day-sleep attempt |
| Dark commute | sunglasses on morning commute home post-nights |
| Transition days | between blocks: delay sleep 2h/day forward; long break → 24h+ reset |

## Common Pitfalls

1. **Trying to advance (sleep earlier).** Phase-advancing fights the clock; the plan always delays forward (day→evening→night direction), even if that means one short night before a day block.
2. **No anchor in fast rotations.** Adapting fully to each 2-day block is impossible; anchor sleep + naps beats zig-zagging. If your rotation is slow (≥1 week per block), adapt per block instead.
3. **Caffeine at shift start.** The 5-6h half-life means a 23:00 coffee is still ~50% active at 05:00. Cutoff = shift end + buffer, and the plan says the time out loud.
4. **Morning light after nights.** Sunlight on the commute home resets the clock to day mode — the exact opposite of adaptation. Sunglasses sound trivial; they are not.
5. **Driving home after a bad night.** Microsleep risk after a short-sleep night shift is comparable to legally-impaired driving. If sleep < 4h or a microsleep episode occurred: nap before driving or get a ride. The `commute` card makes the threshold explicit.
6. **Sleeping in on recovery days.** After nights end, a hard 24h+ reset (one very long awake stretch into a normal night) beats drifting 2h/day for a week — the plan inserts it when the break is long enough.

## Verification Checklist

- [ ] Schedule pattern + shift times entered and listed correctly
- [ ] Plan generated for the next 14+ days, dates aligned with the actual roster
- [ ] Anchor window present across all blocks (fast rotation) or per-block adaptation chosen (slow rotation)
- [ ] Caffeine cutoff times visible on every day; actually followed
- [ ] Night-shift mornings have the commute card (sunglasses, drive-risk threshold)
- [ ] Transition sequences present between differing blocks
- [ ] Sleep logged for at least 2 weeks; `screen` checked for SWD flags
- [ ] Persistent symptoms → occupational health referral (this tool plans; it doesn't diagnose)
