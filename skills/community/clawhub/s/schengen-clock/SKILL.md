---
name: schengen-clock
description: "Use when you travel (or plan travel) to Europe on a non-EU passport and must respect the Schengen 90/180 rule — a rolling window where any 180-day stretch allows at most 90 days of presence. Parses passport stamps / stay history, computes presence per rolling window, finds the current maximum allowed stay on any entry date, projects forward (can I add this trip?), flags the classic overstay traps (5-day overstay from poor counting, back-to-back long stays, the day-of-entry-counts rule), and generates a border-interview-ready itinerary letter. For tourists/visitors — doesn't handle residence permits, long-stay visas, or working-holiday schemes."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [schengen, visa-free, 90-180-rule, travel-planning, overstay, border-control]
---

# Schengen Clock — Rolling 90/180 Rule Tracker

## Overview

The Schengen 90/180 rule is simple to state and brutal to apply: **in any 180-day
window (rolling backwards from today, or from any entry date), you may be present
at most 90 days** — visa-free or on a short-stay visa. The rolling part is what
destroys people:

- Days don't "reset" when you leave for a weekend. The window slides every day.
- The 180-day window counts **backwards from each day of presence**, so a long
  stay from 7 months ago can still bite you today.
- Day of entry counts as day 1 of presence; day of exit also counts. Counting
  errors of 3–5 days are the most common cause of **accidental overstays** —
  which now mean entry bans (1+ years), not just a stern lecture at the border.

This skill turns stay history into certainty:

1. **Stay registry** — record entry/exit dates (+ country). Both dates count as
   presence days (that's the rule).
2. **Rolling-window audit** — for any date, compute presence in the trailing
   180 days and remaining allowance.
3. **Max-stay forecast** — "if I enter on Oct 12, what is the longest I can
   stay?" — computed exactly, with the date allowance runs out.
4. **Trip planner** — "can I add Nov 1–Dec 12?" → verdict + adjusted allowance
   + which old stays are still "burning" inside the window.
5. **Overstay traps** — pattern-scan the registry for the classic mistakes.
6. **Border letter** — a dated itinerary + allowance statement to hand the
   border officer who asks "how long are you staying?"

All data in one local `schengen.json`. Travel history is nobody's cloud data.

## When to Use

- You hold a non-EU passport with visa-free Schengen access (US, UK, UA, GE, AM, RS, MK, BA, MD, and ~50 more) and make multiple Europe trips per year
- You live partly in Europe on tourist stamps and need to know your exact runway
- You're planning trips and want to know: enter date X → max stay, or add trip Y → allowed?
- You over stayed once and need to understand your current standing before booking
- Border interview prep — printable allowance statement
- Don't use for: residence permits / national long-stay visas (D-visas) with
  separate rules, working-holiday schemes, or non-Schengen European microstates
  and Ireland/UK/Cyprus/Bulgaria/Romania (until they join — Romania and
  Bulgaria joined Schengen air/sea March 2024, land borders March 2025).

## How It Works

1. `stay add --entry 2026-05-10 --exit 2026-06-02 --country IT` — record past/
   future stays. Both dates count as presence days (day of entry AND day of exit
   both count — this is the official counting).
2. `status --on 2026-10-01` — presence in the 180-day window ending that date,
   remaining allowance, burn-down of which stays are inside the window.
3. `maxstay --entry 2026-10-12` — exact answer: if you enter Oct 12, the
   longest legal stay is N days, allowance exhausted on date D.
4. `plan --entry 2026-11-01 --exit 2026-12-12` — verdict ALLOWED / TOO-LONG /
   EXACT-FIT with details; shows what the trip does to future allowance.
5. `traps` — pattern-scan the registry for the classic mistakes.
6. `letter --entry 2026-10-12 --exit 2026-11-20` — border-interview one-pager.

## Commands

```bash
# Record stays (past trips from passport stamps)
python3 scripts/schengen.py stay add --entry 2026-03-05 --exit 2026-03-18 --country FR
python3 scripts/schengen.py stay add --entry 2026-05-10 --exit 2026-06-02 --country IT   # 24 days
python3 scripts/schengen.py stay add --entry 2026-07-01 --exit 2026-08-30 --country ES   # 61 days
python3 scripts/sengen.py stay list                       # (typo-guarded anyway)

# Where do I stand today / on a date?
python3 scripts/schengen.py status                        # as of today
python3 scripts/schengen.py status --on 2026-10-01        # 43 used / 47 left in window

# If I enter on a date, how long can I stay?
python3 scripts/schengen.py maxstay --entry 2026-10-12
# → longest legal stay 47 days, must exit by 2026-11-27 (or earlier if rules change)

# Can I add this trip?
python3 scripts/schengen.py plan --entry 2026-11-01 --exit 2026-12-12
# → TOO-LONG: trip is 42 days, only 29 available in window ending 2026-12-12

# Classic-trap scan
python3 scripts/schengen.py traps

# Border letter
python3 scripts/schengen.py letter --entry 2026-10-12 --exit 2026-11-20
```

Storage: `schengen.json` in cwd (or `--db`). Fully offline.

## The Counting Rules (as implemented)

| Rule | Implementation |
|---|---|
| Window | any 180-day period; for "status today", the 180 days ending today |
| Presence day | calendar day inside Schengen, **entry day and exit day both count** |
| Cap | 90 presence days per any 180-day window |
| Exit deadline | last day you may be present; overstay = presence on day 91+ |
| Overstay consequences | flags, fines, entry bans (typically 1–3 years), annulled visas |

## Common Pitfalls

1. **Counting the exit day as free.** Exit day counts as presence. A "90-day"
   trip entered on day 1 must exit on day 90, not day 91.
2. **Thinking a weekend out resets the clock.** The window rolls; only days
   *outside* stop accumulating. A 2-day hop to London saves you exactly 2 days.
3. **Back-to-back long stays.** 90 days in, out for a week, 90 days back in —
   the second stay trips the cap almost immediately because the first stay is
   still inside the rolling window. `traps` flags this pattern.
4. **Ignoring future-dated stays.** The planner simulates the registry *as if*
   the trip happened; booked-but-not-taken trips count in projections.
5. **Microstate confusion.** San Marino, Monaco, Vatican have no border checks
   — time there is Schengen time. UK, Ireland, Cyprus are NOT Schengen.
6. **Assuming the rule is 180 days per year.** It is not. It's 90 per any
   rolling 180. A calendar-year mental model overestimates allowance.
7. **Trusting airport "you're fine" over the math.** Airline check of ten uses
   the same rolling math; border police always do. Trust `status`, not vibes.
8. **Overstaying "just 3 days".** Post-2017 enforcement: fines, removal, and
   entry bans that outlast the trip's value. A 3-day overstay can cost a 1-year ban.

## Verification Checklist

- [ ] Presence math: entry and exit days both counted, inclusive
- [ ] Rolling window: `status` uses the 180 days ending on the query date
- [ ] `maxstay` searches day-by-day for the true maximum (not an approximation)
- [ ] `plan` simulates the trip added to the registry and re-audits every window
- [ ] `traps` detects: back-to-back long stays, thin-margin (<5 days) plans,
      stays ending inside the next 180 days, cumulative-year heavy usage
- [ ] `letter` output is dated, shows trips + allowance math, printable
- [ ] No network calls — registry never leaves the machine

## References

- `references/rule-explained.md` — the 90/180 mechanics worked examples, border
  interview tactics, overstay consequences by severity, FAQ
