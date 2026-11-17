---
name: stall-solver
description: Use when checking whether a venue's restroom count actually survives a halftime rush, planning fixtures for an event space/coffee-shop/school, or auditing fixture counts against plumbing-code minimums — Erlang-C queue math on toilet demand (arrival rates by venue type, burst-break simulation, IPC fixture tables) plus verdicts (OK / TIGHT / FAIL) and queue-clearing times.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [restrooms, plumbing, queueing, venue, event-planning, erlang, ipc, fixtures]
---

# Stall Solver — Restroom Queue Math

Restroom planning has a hard split personality: plumbing codes size
fixtures for *sustained* occupancy, but the pain people remember is a
*burst* — halftime, intermission, the session break. A venue can be
fully code-compliant and still have a 25-minute women's-room line,
because 40% of 400 attendees hit the toilets in the same 15-minute
window. This skill runs both checks: queueing math on arrivals vs
fixtures, and fixture-count audits against code tables.

## When to Use

- Evaluating a venue (theater, bar, conference hall, school) for an
  event — will the break queue be survivable?
- Planning a cafe/restaurant/office buildout — how many stalls and
  urinals to install
- Reviewing an architect's fixture schedule against expected use
- Diagnosing an existing restroom-line problem (is it fixture count,
  or is it dwell time / layout?)
- All-gender restroom conversions (stalls-only) — how many stalls
  replace a given WC+urinal split

Don't use for: residential bathrooms, portable-toilet logistics for
outdoor festivals (different tables entirely), or ADA clearance/
layout questions (those are geometry, not counts).

## The Model

Three layers, each answering a different question:

1. **Demand rates** — visits/person/hour by venue type (concert 0.45,
   conference 0.35, office 0.25...) and median occupancy per fixture
   (urinal ~35 s, stall ~95 s, sink ~20 s).
2. **Queue math** — M/M/c with Erlang-C expected wait. Sustained mode
   gives steady-state utilization and average wait; event mode takes a
   burst share (default 40% of attendees) over a window (default 15
   min) and reports burst utilization, expected wait, and total
   drain time.
3. **Code minimums** — IPC-style assembly fixture ladder by occupancy
   bucket (water closets per sex, urinals, lavatories), with linear
   scaling beyond the table.

Key asymmetry the math exposes: **urinals are throughput machines**
(3x the turnover of a stall) but only serve half the population;
female/stall demand is where queues actually form. In queue terms,
stalls need more fixtures for the same arrival rate because service
time is 3x longer.

## Workflow

1. Establish the worst case: peak headcount AND the break structure
   (is there a simultaneous break — halftime, intermission, plenary
   gap?).
2. Sustained check:
   ```bash
   python3 scripts/stall_detector.py demand --venue concert \
       --attendees 600 --fixtures 8 --urinals 6
   ```
3. Burst check (the one that matters at halftime):
   ```bash
   python3 scripts/stall_detector.py event --venue sports \
       --attendees 400 --fixtures 6 --urinals 4 \
       --burst-share 0.5 --window-min 15
   ```
   Verdicts per fixture class: OK (ρ<0.8), TIGHT (0.8-1.0),
   FAIL (ρ≥1 — the line grows faster than it drains).
4. Code audit (buildout/permit stage):
   ```bash
   python3 scripts/stall_detector.py audit --venue conference \
       --occupancy 350 --f-wc 8 --m-wc 3 --m-ur 2 --f-lav 6 --m-lav 4
   ```
5. Fix FAILs by, in order of cost-effectiveness: staggering the break
   (free), converting WCs to urinals in men's rooms, adding stalls
   (esp. all-gender), adding a fixture bank at a remote location to
   split arrival streams.

## Reading the numbers

- **Utilization ≥100% in event mode = the queue never clears during
  the window**; the drain-time figure tells you how long the line
  runs after the break ends.
- A 56-minute "avg wait" in a 15-minute window means the math says
  the burst saturates the room — people self-adjust (leave early,
  skip), so read it as "severe," not literal.
- Code-minimum compliance ≠ no lines. The audit is a floor, not a
  comfort guarantee; run the demand/event checks separately.

## Common Pitfalls

1. **Sizing only from code tables.** Tables assume steady use; a
   single 15-minute burst can require 2-3x the sustained fixture load.
2. **Ignoring the female/stall asymmetry.** Same arrival rate, 3x
   service time = ~3x the fixtures needed for the same wait. The
   classic "huge men's room, huge women's line" design error.
3. **Treating all-gender conversion as a pure swap.** Removing
   urinals without adding ~1 stall per 2 urinals lost typically FAILs
   the burst check — urinals were carrying men's throughput.
4. **Forgetting sinks.** Lavatory demand peaks with the restroom exit
   wave; hand-wash occupancy (~20 s) usually clears fine but code
   requires the counts anyway.
5. **Miscounting "fixtures."** A double-lav counts as 2; a WC in a
   stall counts as 1 regardless of stall size; urinals with privacy
   partitions are still urinals for throughput.
6. **Blindly trusting the bundled code table.** Local amendments
   (UPC jurisdictions, city addenda) shift minimums; always verify
   against the adopted edition before permitting.

## Verification Checklist

- [ ] Peak headcount is the real one (fire-marshal occupancy, not RSVP)
- [ ] Break simultaneity assessed (halftime = everyone; staggered
      sessions = lower burst share)
- [ ] Both sustained AND burst checks run
- [ ] Fixture counts match actual architectural counts (not plans
      from an earlier revision)
- [ ] Code table cross-checked against locally adopted plumbing code

## One-Shot Recipe: is the theater's intermission survivable?

```bash
python3 scripts/stall_detector.py event --venue theater \
    --attendees 800 --fixtures 12 --urinals 8 --window-min 20
```
If stalls read TIGHT/FAIL: recommend adding 2-4 all-gender stalls OR
holding the house 5 minutes before intermission ends (staggering the
return wave does nothing — the arrival burst is the problem; lengthen
the intermission instead).
