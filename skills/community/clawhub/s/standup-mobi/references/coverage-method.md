# Absence Coverage — The Full Method

## Why coverage fails

Teams discover duty-by-duty what an absent member did, **during** the
absence, at the worst possible moment. Three structural causes:

1. **Duties are invisible.** Standup mentions outcomes, not the recurring
   work behind them. Nobody lists "renews the SSL cert every 60 days"
   until it expires.
2. **Coverage is assigned by availability, not load.** The most reliable
   person silently absorbs everything — then burns out or becomes the next
   single point of failure.
3. **Tribal knowledge has no extraction protocol.** "Knowledge transfer"
   gets booked as one meeting that everyone assumes someone else will
   document.

## Duty inventory from observable traces

When the absentee can't help, rebuild their duty list from:

- **Calendar** (recurring meetings they run vs. attend — running matters)
- **Standup notes** (their "yesterday" entries across 2+ weeks)
- **Systems** (cron jobs, scheduled reports, invoice runs, on-call rota)
- **Inboxes/lists** (tickets auto-assigned to them, approval queues)
- **Ask the neighbors** ("what do you ping Alex for?") — one question,
  asked of 3 teammates, surfaces 80% of duties

Tag each duty: cadence (daily/weekly/monthly), skill, minutes, risk if
skipped, tribal (no runbook?).

## The coverage solver

Formally: assign duties to people maximizing coverage subject to
capacity constraints. Practical version used here:

1. Sort duties by `risk_weight × minutes` descending — high-risk
   long-running duties get first claim on attention.
2. For each duty, choose among eligible people (skill match) the one with
   **most remaining capacity** — load-balancing, not hero-assignment.
3. Hard cap: if an assignment pushes a person past
   `1.5 × average_added_load`, flag UNCOVERED instead. A visible hole in
   the plan beats an invisible overload in a person.

The 1.5× cap is a heuristic, not physics — but it makes the "reliable
person absorbs everything" failure mode impossible to hide.

## Tribal knowledge extraction

A 15-minute structured interview beats a wiki page nobody writes. The 12
questions in SKILL.md are ordered to move from inventory (1–3) to failure
modes (4–6) to support network (7) to runbook seed (8) to triage (9–11)
to unknown-unknowns (12).

Rules of thumb:
- Record it (with permission) — transcription is cheaper than attention.
- The output is a **one-page runbook per duty**, written by the
  interviewer, corrected by the absentee. Never assign the absentee
  homework; they're the source, not the scribe.
- Questions 9 (what's skippable) and 12 (what should I have asked) are
  consistently the highest-yield.

## The graded ramp

Coverage fails when a substitute is handed a task at full difficulty on
day one. The ramp:

| Day | Level | Substitute does | Stop-and-ask trigger |
|---|---|---|---|
| 1 | watch | observes absentee/recordings, reads runbook | any step not in the runbook |
| 2 | shadow | does it alongside the absentee | any divergence from runbook |
| 3 | assist | does it, absentee reviews before "done" | output looks different from usual |
| 4 | solo | does it alone, documents deviations | anything the runbook marks STOP |
| 5 | audit | absentee (or lead) reviews the week's deviations | — |

For sudden absences the ramp compresses: watch = reading + the person who
usually receives the duty's output, shadow/assist merge into "first run
with a buddy on chat", solo from day 2–3 with an explicit stop-list.

## Checklist design

The substitute's one-pager groups by cadence, not by project — because
the substitute's day is organized by time, not by the absentee's mental
model. Each line: duty, when (day/time), minutes, first step, stop-and-ask
trigger, contact.

Paper beats apps here: it survives laptop swaps, works at 08:55 before a
09:00 duty, and can be taped next to a monitor.

## Metrics that matter

- Coverage ratio: owned duties / total duties (target 100%, holes explicit)
- Tribal ratio: tribal duties / total (target → 0 over time; every
  extraction session should convert at least one)
- Load spread: max added load / average added load (target ≤ 1.5)

Re-run `solve` after any team change — coverage is a snapshot that rots.
