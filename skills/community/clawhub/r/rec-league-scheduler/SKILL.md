---
name: rec-league-scheduler
description: "Use when you run (or coach in) a recreational sports league, club ladder, or weekly game group of 4-32 players and the schedule has become the job — who plays whom, who sits out, who's subbing for whom, is it fair. Round-robin fixture generation (single or double, bye handling for odd counts), absentee-aware rotation (the absent don't consume court time), fair-play audit (games and byes per player within ±1), player availability registry with match-day call-ups, standings table with head-to-head tiebreakers, and a printable match-day sheet. Replaces the spreadsheet-and-group-chat chaos that kills volunteer-run leagues."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [sports, scheduling, round-robin, league, tournament, rotation, fixtures, club]
---

# Rec League Scheduler — Fixtures, Rotation & Fairness for Volunteer Leagues

## Overview

Volunteer-run rec leagues — badminton club, squash ladder, padel group,
chess club, football 7s, curling, darts league — all die the same death: the
schedule becomes a second job for one unpaid person, and the group chat
becomes the database. Typical symptoms:

- "Who hasn't played each other yet?" — nobody knows.
- Two players have had 5 byes while others had zero, and there's a quiet mutiny.
- Absentees still occupy slots, so real attendance produces thin rounds and 3-court halls with 2 courts used.
- Standings live in a photo of a whiteboard from three weeks ago.

This skill is the volunteer's scheduling brain:

1. **Fixture generation** — round-robin (single/double) via the circle
   method; odd counts get a rotating bye; court/slot assignment included.
   Everyone plays everyone, in the minimum number of rounds.
2. **Absence-aware rotation** — mark who's absent on match day; the rotation
   re-flows so present players fill courts and byes fall to those with the
   fewest. Absences never consume playing time.
3. **Fair-play audit** — games played and byes per player, flagging any
   spread wider than ±1, plus pair-coverage (how many times each pair has
   met) so rivalries don't repeat while strangers never meet.
4. **Availability registry** — RSVP per date; call-up list for short rounds.
5. **Standings** — points, game difference, head-to-head tiebreaker, printed
   table.
6. **Match-day sheet** — one printable page: courts, slots, fixtures,
   score blanks, the byes, the next date.

## When to Use

- You run a rec sports group of 4-32 players on a weekly (or multi-week) basis
- A club ladder or internal league needs a fair fixture list, not ad-hoc pairings
- Attendance varies week to week (5 one week, 11 the next) and rotation fairness is fraying
- You want standings that survive longer than a whiteboard photo
- Don't use for: knockout/tournament brackets with elimination (different
  structure — though `fixtures` seeds groups), leagues needing external
  governing-body rule compliance, or scheduling across many teams with
  venues/referees (that's full league-management software territory).

## How It Works

1. `player add "Alex"` — build the roster (skill level 1-5 optional, used
   only for balanced court assignment notes).
2. `fixtures --courts 3 --double` — circle-method round-robin: each round
   lists courts and the bye; `--double` plays home-and-away.
3. `absent "Sam" --date 2026-10-03` — registry of who's out when.
4. `night --date 2026-10-03 --present 9 --courts 3` — tonight's actual
   rotation: present players re-flowed into courts, byes to the players with
   the fewest so far; prints the match-day sheet.
5. `result "Alex" 21 15 "Sam"` — record scores; `standings` builds the
   table (points, diff, head-to-head).
6. `audit` — the fairness report: games and byes per player (±1 target),
   pair coverage matrix summary.

## Commands

```bash
# Roster
python3 scripts/league.py player add "Alex" --level 4
python3 scripts/league.py player add "Sam" --level 3
python3 scripts/league.py player add "Kim" --level 4
python3 scripts/league.py player add "Jo" --level 2
python3 scripts/league.py player add "Mel" --level 3

# Full season fixture list (5 players → bye each round)
python3 scripts/league.py fixtures --courts 2
# Round 1: [Alex vs Mel] court1, [Sam vs Kim] court2, bye: Jo ...

# Match night with real attendance
python3 scripts/league.py absent "Sam" --date 2026-10-03
python3 scripts/league.py night --date 2026-10-03 --present 4 --courts 2

# Results & standings
python3 scripts/league.py result "Alex" 21 15 "Mel"
python3 scripts/league.py result "Sam" 21 19 "Kim"
python3 scripts/league.py standings

# Fairness check
python3 scripts/league.py audit
```

State: `league.json` in cwd (or `--db`). Local, exportable, no accounts.

## The Circle Method (what `fixtures` implements)

N players in a circle; fix player 1, rotate the rest; each rotation yields
N/2 pairings (or (N-1)/2 + a bye when odd). After N-1 rotations every pair
has met exactly once. It's the same construction used in professional
league scheduling — minimal rounds, perfect coverage, zero repeats.

## Fair-Play Rules (what `audit` enforces)

| Metric | Target | Why |
|---|---|---|
| Games per player | within ±1 of mean | court time is the product |
| Byes per player | within ±1 of mean | nobody is perpetually benched |
| Pair meetings | 0 or 1 in single round-robin | variety beats rivalry |
| Consecutive byes | never 2 in a row | the unforgivable sin |

## Common Pitfalls

1. **Scheduling absent players.** A fixture list is a plan, not a contract.
   `night` re-flows who actually came; byes go to the least-benched.
2. **Odd counts without bye accounting.** 9 players on 4 courts = 1 bye by
   arithmetic, not by choice. Unmanaged, the same nice person volunteers to
   sit every week. The rotation distributes it.
3. **Letting standings drive pairings.** "Top two should play" every week
   starves the bottom of the ladder and kills casual leagues. Fixture order
   is round-robin; standings are a report, not a scheduler.
4. **Recording results from memory on Thursday.** Score blanks on the match-
   day sheet exist because by Thursday nobody remembers 21-15 vs 21-18.
5. **No shows → empty court, wasted hall fees.** The call-up list (players
   who said "text me if short") fills rounds in seconds.
6. **Skill-blind court assignment.** Optional levels let you note "court 1 =
   the bloodbath, court 2 = the fun court" instead of discovering it by
   injured feelings in week 3.

## Verification Checklist

- [ ] `fixtures` circle method: N-1 rounds (N even), N rounds (N odd), each pair exactly once (`--double` twice)
- [ ] Bye rotation spreads byes evenly; nobody bye'd twice in a row
- [ ] `night` excludes absent players, fills courts from present, assigns byes by fewest-byes
- [ ] `standings` sorts by points → game difference → head-to-head
- [ ] `audit` flags games/bye spread >1 and duplicate pair meetings
- [ ] Match-day sheet printable as plain text (one page)

## References

- `references/round-robin-math.md` — circle method proof sketch, bye
  distribution for odd N, rotation re-flow algorithm, standings tiebreaker order
