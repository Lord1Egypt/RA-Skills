---
name: Triage / Task Prioritization
slug: triage
version: 1.0.3
description: >-
  Prioritizes competing tasks into P0-P3 by cost of delay and decides what to do first, what waits, and when to interrupt current work.
  Use when tasks pile up or everything feels urgent, when a request arrives mid-task, when triaging bugs, tickets, alerts, or a backlog
  after time away, when deadlines conflict or slack runs out, or when the user says urgent, ASAP, EOD, drop everything, or no rush.
  Learns the user's real priority rules from their corrections and reorders. Not for effort estimation or roadmap planning.
homepage: https://clawic.com/skills/triage
changelog: "Display name shown correctly"
metadata:
  clawdbot:
    emoji: 🚦
    displayName: "Triage / Task Prioritization"
    configPaths: ["~/Clawic/data/triage/"]
---

Classify incoming work into P0-P3 by cost of delay, route it, and learn the user's real priority rules from their corrections. Learned rules and stated preferences persist in `~/Clawic/data/triage/` (created on first confirmed rule or stated preference; nothing is stored without the user's explicit yes). If you have data at an old location (`~/triage/` or `~/clawic/triage/`), move it to `~/Clawic/data/triage/`.

## When To Use

- Several tasks compete and you must pick an order
- A new request arrives mid-task and you must decide whether to interrupt — and how to switch safely
- A pile needs sorting: an inbox after time away, an ungroomed backlog, a ticket queue
- A bug, ticket, alert, or security report needs a priority, not just an acknowledgment
- The user uses priority language: "urgent", "ASAP", "drop everything", "no rush", "when you have time"
- The user reorders or overrides your queue — that is training data, not just an instruction
- Not for effort estimation or roadmap planning: triage decides *when*, not *how long*

## Quick Reference

| Situation | Play |
|-----------|------|
| "Drop everything and X" | Interrupt now, but name what gets paused: "Pausing Y (was P1) — resume after?" |
| Two tasks both claim P0 | Escalate sequencing to the user — two "drop everything" cannot both be true |
| Must interrupt mid-task | Park first: resume note + WIP preserved, then switch (`interrupts.md`) |
| Sounds urgent, but no deadline and no accumulating damage | Cap at P1; one closed question: "Is anyone blocked right now?" |
| Mixed signals ("urgent but no rush") | Ask — the contradiction is the signal; never average to P1.5 |
| Deadline exists but looks far | Compute slack (Core Rules #2); slack under one working day → P1 today |
| Deadline looks fake or negotiable | Find what consumes the output — the real deadline hides behind the stated one (`deadlines.md`) |
| Slack already negative | Negotiate scope → sequence → time, in that order (`deadlines.md`) |
| Bug or ticket arrives | Severity ≠ priority: score severity × reach × trend (`bugs.md`) |
| Pile of unsorted items (post-vacation, backlog) | Two-pass sweep: classify all, then order; newest-first for old piles (`batch.md`) |
| User corrects your priority | Record it; on the 2nd same-direction correction, propose a standing rule (`patterns.md`) |
| Confirmed rule matches a new task | Apply it and cite it: "Deploy issue → P0 (your standing rule)" |
| New fact arrives (deadline revealed, blocker cleared, scope change) | Re-triage the whole queue, not just the new item |
| Else | Run the level tests below top-down; torn between adjacent levels → Core Rules #3 |

Depth on demand: `signals.md` reading urgency language, senders, sources · `patterns.md` learning protocol and memory format · `interrupts.md` switching safely, parking, stacked P0s · `batch.md` sweeps, piles, grooming, overflow · `deadlines.md` slack cases, real vs stated, negotiation · `bugs.md` bug, ticket, SLA, and alert triage.

## Priority Levels

Each level has a boundary test. Run the tests top-down; first yes wins. Test states, not tone.

| Level | Test (yes → this level) | Response | Examples |
|-------|-------------------------|----------|----------|
| P0 | Does damage accumulate every minute this waits? | Interrupt current work now | Production down, active breach, data loss in progress |
| P1 | Is a person or deliverable stalled today? | Next work-unit boundary, same day | Blocked teammate, client waiting, due-today deadline |
| P2 | Dated or clearly valuable, but nobody stalls today? | Scheduled queue, with a date | Reviews, planning, deadlines beyond today |
| P3 | Would anyone notice if this never happened? (barely) | Backlog, batch-processed | Ideas, "someday", minor optimizations |

## Core Rules

1. **Priority = cost of delay, never effort or loudness.** A hard task nobody waits on is P2; a 5-minute unblock for a stalled teammate is P1. Tie-break within a level: highest cost of delay per unit of effort first (WSJF, Reinertsen); when costs look equal, shortest job first.
2. **Deadline urgency is slack, not calendar distance.** Slack = working time until deadline − remaining work, counted in `working_hours` only. Friday deadline + 3 days of work, seen on Wednesday = negative slack = P1 today. A Monday-9am deadline seen Friday afternoon has near-zero slack. Recompute whenever scope grows; edge cases (timezones, dependency chains) in `deadlines.md`.
3. **Misclassification is asymmetric — up is cheap, down is expensive.** A false P0 costs one interruption; a missed P0 costs the whole damage window. Torn between adjacent levels *with* concrete urgency evidence → take the higher. No evidence, just tone → take the lower and label it: "Queued as P2 — say the word if it's blocking."
4. **Ask only at the P0/P1 boundary.** One closed question there beats a wrong guess. At P2/P3 the stakes don't cover the interruption cost — pick, state the assumption, move on.
5. **Learn only through the ladder: observe → propose → confirm.** One correction = record. Two same-direction corrections = propose ("Should deploy issues always be P0?"). Apply automatically only after an explicit yes, and cite the rule when applying it. Never silently internalize — full ladder and decay in `patterns.md`.
6. **P0 is rare by construction.** If over a week more than ~1/3 of items land P0/P1, the bar drifted — re-anchor on the level tests instead of inventing intermediate levels. When everything is urgent, nothing is.
7. **Re-triage on state change, not on a timer.** Triggers: deadline revealed or moved, blocker cleared, scope change, new P0. Each one re-sorts the whole queue; a queue sorted on stale facts is a wrong queue.

## Queue Discipline

- P0 interrupts mid-task (`interrupt_floor` in config can extend this to P1). P1 waits for the current unit of work to finish — dropping a half-done change leaves broken state, which is its own incident. Exception: if current work is P2/P3, switch at the next safe point. Switching mechanics — parking note, resume protocol, stacked P0s: `interrupts.md`.
- Order within a level: confirmed user rules first, then ascending slack, then arrival order.
- Announce changes, not steady state: "New P0 — pausing X. Queue now: [incident, review, docs]." Silent reshuffles destroy the user's trust in the queue; verbosity is `announce_style` in config.
- A dated P2 gets scheduled the moment it enters the queue. A P2 that "ages into" a P0 was a triage failure, not an escalation — log it as a correction against yourself.
- When the queue exceeds capacity, triage becomes explicit rejection — propose drops by name, never silent starvation (`batch.md`, Overflow).

## Output Gates

Before emitting a priority or a reordered queue:

- Is every P0 justified by accumulating damage or a level test — not by tone, caps, or sender seniority?
- Did I check `~/Clawic/data/triage/patterns.md` for a confirmed rule before falling back to defaults?
- Am I auto-applying any rule the user never confirmed? If yes → propose instead.
- If queue order changed, did I say so and name what got bumped?
- If I am about to interrupt current work, does the paused task have a resume note (`interrupts.md`)?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/triage/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| working_hours | text (e.g. "Mon-Fri 09:00-18:00") | Mon-Fri 09:00-18:00 | The hours slack counts (Core Rules #2); changes every deadline-driven level |
| triage_mode | interrupt \| batch | interrupt | batch defers non-P0 classification to scheduled sweeps (`batch.md`); paging-grade sources still push through |
| interrupt_floor | P0 \| P1 | P0 | Lowest level allowed to interrupt mid-task; P1 relaxes the wait-for-boundary rule in Queue Discipline |
| sweep_times | list of times | none | With `triage_mode: batch`: when sweeps run; empty = sweep on request |
| announce_style | full \| minimal | full | full names every bumped item on reorder; minimal reports only the new top of the queue |

Preference areas — customizable dimensions; a stated preference gets recorded in config.yaml and applied:

- **Labels**: reporting scheme (P0-P3, High/Normal/Low, MoSCoW) — affects how levels are announced, never the level tests
- **Risk posture**: tie-break direction when torn without evidence — affects the default-down in Core Rules #3
- **Sources**: which channels count as paging-grade vs digest — overrides rows in `signals.md` Source Defaults
- **Cadence**: grooming day, drift-check day, aging thresholds — affects the weekly routines in `batch.md`
- **Escalation**: whether the P0/P1 question goes to the user or a named delegate — affects Core Rules #4

## Traps

| Trap | Why it fails | Do instead |
|------|--------------|------------|
| Sender rank as urgency | An exec's "someday idea" outranks nothing; rank predicts importance, not cost of delay | Run the level tests; if the user consistently overrides for a sender, learn that as a rule |
| Severity as priority | A crash in a feature nobody uses outranks nothing; impact alone misorders the queue | Score severity × reach × trend (`bugs.md`) |
| Newest-task pull | Recency feels urgent; arrival time is not cost of delay | Slot by test result, re-sort, report the position |
| Doing work mid-triage | Each "quick fix" during a sweep restarts its context; the pile outlives the morning | Classify everything first, then work the ordered queue (`batch.md`) |
| Averaging mixed signals | "Urgent but no rush" averaged to P1.5 satisfies neither reading | Ask — the contradiction is the signal |
| Escalating on repetition | A third mention is frustration, not new urgency | Acknowledge, give queue position and expected start |
| Demoting polite requests | "Whenever you get a chance" from some users means "today" | Check for a date before demoting; calibrate per sender (`signals.md`) |
| Rolling a passed date forward | A silently moved date is a decision hidden from the user | Re-triage the item the day its date passes (`batch.md`) |

## Where Experts Disagree

- **Interrupt-driven vs. batch triage.** Batch (fixed triage passes) wins when true P0s are rare and deep work dominates; interrupt-driven wins for on-call contexts. Pick per user context, tell the user which mode you're running, and record it as `triage_mode`.
- **FIFO vs. WSJF within a level.** FIFO is predictable and reads as fair to requesters who watch the queue; WSJF delivers more value when only outcomes are visible. Perceived fairness is a real cost — choose by who is watching.

## Related Skills

More Clawic skills, get them at https://clawic.com/skills/triage (install if the user confirms):

- `task-list` — maintaining the queue itself once triage has assigned levels
- `incident-response` — when a P0 is a production incident: triage decides the interrupt, that skill runs the handling
- `time-blocking` — protecting focus time that P2/P3 must not interrupt
- `inbox` — processing message streams before items become triaged tasks

## Feedback

- If useful, star it: https://clawic.com/skills/triage
- Latest version: https://clawic.com/skills/triage

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/triage.
