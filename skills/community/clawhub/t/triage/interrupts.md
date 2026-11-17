# Interrupting — When and How to Switch Tasks

Triage assigns the level; this file is the switch itself. A wrong switch turns one incident into two: the new fire plus the half-done work you dropped.

## The Interrupt Decision

- Only P0 interrupts mid-task by default (`interrupt_floor` in config raises P1 to interrupt-grade for users who want it). Everything else waits for a boundary — see the level responses in SKILL.md.
- The real comparison: damage accumulating on the new item vs. switch cost + risk to the paused work. When the new damage is per-minute (the P0 test), the switch always wins. When it is per-day, it never does.
- An interrupt request that fails the P0 test gets a position, not a switch: "Queued next — I finish the current unit first (~N min)."

## Switch Cost Is Paid Twice

- Returning to interrupted work takes ≈23 minutes on average to reach prior depth (Mark, UC Irvine interruption studies) — and you pay a second recovery when you switch back. Two casual interrupts can erase an hour.
- The paused work carries risk too: state held only in your head evaporates. That is why the parking protocol below is mandatory, not polite.

## Safe Stopping Points (best → worst)

1. **Completed unit** — the work is in a done, verified state. Switch freely.
2. **Consistent checkpoint** — tests green, document section complete, transaction closed. Switch after the check passes.
3. **Parked mid-flight** — state written down via the protocol below. Acceptable for P0 only.
4. **Mid-edit, nothing recorded** — never. Thirty seconds to reach state 3 is always affordable; a half-applied change is its own incident (SKILL.md Queue Discipline).

## The Parking Protocol (before every mid-task switch)

Write a resume note — three lines, kept with the task:

1. Where I stopped (file/section/step, exact).
2. The next concrete action I was about to take.
3. Open question or fragile state (what will bite me if I forget it).

Then preserve WIP in the medium's native way (draft saved, changes stashed or committed as WIP, browser state noted) and announce: "Pausing X for the P0 — resume note saved."

## Resume Protocol

- Read the note before touching anything.
- Re-verify state — re-run the last check that was green. The world may have moved while you were away (someone else edited, the deploy landed, the user replied).
- If the pause exceeded a day, re-triage the parked task itself: its slack changed while it sat.

## Stacked P0s

- A second P0 during a P0: never leave the first half-handled to chase the second. Park the first at a checkpoint (protocol above) or escalate sequencing to the user — two "drop everything" cannot both be true (SKILL.md Quick Reference).
- Compare damage rates when forced to choose: revenue-per-minute beats reputation-per-day; active data loss beats both.

## The Two-Minute Exception

At a natural boundary — never mid-task — a request that genuinely takes under ~2 minutes (Allen's GTD two-minute rule) is cheaper to do than to queue, classify, and re-load later. Cap: one per boundary. A chain of "quick ones" is a queue bypass wearing a disguise; the third quick favor in a row gets queued and the pattern gets named.

## Self-Interruption

- Checking the queue is itself an interrupt — batch queue checks at work-unit boundaries instead of polling.
- Only paging-grade sources may push through focus time (signals.md, Source Defaults); everything else accumulates for the next boundary or sweep (batch.md).
