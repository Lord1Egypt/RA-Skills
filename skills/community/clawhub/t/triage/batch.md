# Batch Triage — Sweeps, Piles, and Backlog Grooming

One item at a time is the default mode; this file is for the pile — an inbox after a weekend, a backlog nobody groomed, `triage_mode: batch` users who collect everything for scheduled passes.

## When Batch Mode Wins

- True P0s are rare and deep work dominates → sweeps at fixed times (`sweep_times` in config) beat per-arrival triage; classification itself stops interrupting.
- Paging-grade sources still push through in batch mode — they bypass the sweep by definition (signals.md, Source Defaults). Batch mode batches classification, never emergencies.

## The Two-Pass Sweep

**Pass 1 — classify only.** ≤15 seconds per item: run the level tests (SKILL.md, Priority Levels), assign, move on. No replying, no fixing, no research. An item you cannot classify in 15 seconds gets P2 plus a noted question — the question is a task; answering it mid-sweep is not.

**Pass 2 — order within levels.** Confirmed user rules first, then ascending slack, then arrival (SKILL.md, Queue Discipline). Only now may two-minute items be executed (interrupts.md, The Two-Minute Exception) — at the end, capped, never during Pass 1.

Doing the work mid-sweep is the classic failure: each "quick fix" restarts the sweep's context and the pile outlives the morning. Classify everything, then work the queue.

## The Post-Absence Pile

Scan **newest → oldest** — the reverse of arrival order, and the reason: newer messages resolve, supersede, or answer older ones. Triage oldest-first and you process corpses.

1. First pass newest→oldest: mark items that are superseded, self-resolved, or answered downstream. Collapse threads to their latest state.
2. Items that expired unanswered (the meeting happened, the deadline passed): close with a one-line acknowledgment — do not triage a corpse into the live queue.
3. What survives enters the normal two-pass sweep.

## Duplicates and Repeats

- Link duplicates to one canonical item; N requests for the same thing is measured reach — it raises the canonical item's priority instead of cluttering the queue (bugs.md applies the same rule to tickets).
- A repeat from the same person is frustration, not new urgency (signals.md, Anti-Patterns) — answer with queue position.

## Recurring Items

Triage each occurrence by the cost of skipping THIS one, not by the task's standing importance. A weekly report due during an incident skips; a monthly backup check does not — its skip cost compounds silently. When an occurrence is skipped twice in a row, question the recurrence itself with the user.

## Backlog Grooming (weekly)

- **Dated P2 whose date passed** → re-triage it now; never silently roll the date forward. A rolled date is a decision hidden from the user.
- **P3 untouched ~90 days** → propose kill-or-commit: delete it or give it a date. A backlog that only grows is not a queue, it is a graveyard with notifications.
- **Item bumped 3 times** → the level is wrong, not the schedule. Surface it: promote with a date, or kill. Three deferrals is evidence, and evidence goes to the user (patterns.md ladder if they correct you).
- **Important-but-never-urgent work** (health of the system, learning, maintenance): its cost of delay never spikes, so pure urgency starves it forever. Give it a date at intake — a dated P2 manufactures the slack pressure that urgency never will.
- Run drift detection in the same pass (patterns.md, Drift Detection).

## Overflow — When Demand Exceeds Capacity

Triage's original medical meaning includes a third category: those who will NOT be treated. When the queue exceeds capacity, honest triage becomes explicit rejection:

- Compute it: if the P0-P2 queue's total work exceeds available working hours before the earliest deadlines, something must move — scope, dates, or the list itself.
- Propose the cut to the user by name: "These three don't fit before Friday — drop, delegate, or move which?" Never resolve overflow by silent starvation of the bottom of the queue.
- Deadline-side negotiation moves live in deadlines.md (Negotiating When Slack Is Negative).

## Sweep Output

End every sweep with a snapshot the user can veto at a glance: count per level, the top 3 by name, anything killed or closed, and any proposal awaiting their yes.
