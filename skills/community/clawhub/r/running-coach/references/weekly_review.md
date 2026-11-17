# Weekly Review / Week Settlement

How to close out a training week, and how to reconcile it with the week that follows. Load this when the user shares a weekly activity summary (Garmin / Strava weekly view, training-calendar screenshot) or asks to "record this week".

This is the follow-on to **Route B (Weekly Planning)**: the plan was a hypothesis, the week's data is the result, and the *next* week's plan is only valid if it inherits the result.

---

## Step 1 — Extract the week, not just the runs

From the weekly screenshot, pull:

- **Volume:** total distance, run count, days off
- **Distribution:** per-run distance + avg pace + avg HR
- **Non-run load:** strength sessions, cross-training, ball sports, massage — these consume recovery budget but never appear in running mileage
- **Adherence pattern:** which days matched the prescription, which did not, and *in which direction*

Do not reduce the week to a single number. "56 km" is meaningless without knowing whether the excess came from the quality sessions or from the easy days — the two have opposite implications.

## Step 2 — Separate intensity discipline from dose discipline

These fail independently and must be judged separately:

| Discipline | Question | Failure signature | Severity |
|---|---|---|---|
| **Intensity** | Did the hard days stay hard and the easy days stay easy? | Easy-day HR crept into Z3; or a quality session was run too fast to complete | High — corrupts the stimulus |
| **Dose** | Did the volume stay inside the plan's envelope? | Easy days overshooting by 50–100%; an easy long run becoming a marathon-pace run | Medium — recoverable if intensity held |

The combination matters:

- **Intensity held, dose overshot** → the week was harder than designed but not misdirected. Accept the fitness, flag the recovery debt. Usually the *better* failure mode.
- **Dose held, intensity drifted** → looks compliant on paper, produces no adaptation. The *worse* failure mode, because it is invisible.
- **Both overshot** → interrupt: make the next week a genuine down week, not a nominal one.

Never report dose compliance without also reporting intensity compliance. A week can be "+12% volume" and still be a well-executed week.

## Step 3 — Re-derive the pace bands before judging adherence

**The most common false alarm:** a session looks like a deviation ("easy long run was run much too fast") when the real cause is that the plan's pace band was stale.

Check every reported "overshoot" against the user's *measured* recent pace at the prescribed HR:

- If they repeatedly hit HR well below the band's target at a much faster pace, the band is wrong — the band, not the athlete, is out of date.
- Re-derive the easy band from observed pace-at-HR over several runs, then write it back to the profile. Do this whenever ≥3 easy runs in a fortnight show the same mismatch.
- Only after the band is corrected can you judge whether a session was genuinely too hard.

This is a Hard Rule 11 case (`Paces from calibration`): the calibration source includes the athlete's own recent easy running, not only races and time trials.

## Step 4 — Resolve contradictions between "planned" and "executed"

When a session was rewritten on the fly (easy long run → marathon-pace long run), decide explicitly which version stands:

1. **Was the executed version better or worse for the goal?** Grade it against the goal race's demands, not against the plan document.
2. **What did it consume?** A rewritten session that delivered a real stimulus still spends the recovery that was budgeted for the following week.
3. **Do not do both.** If the executed session already delivered the next week's key stimulus, the next week's version of that session is now redundant — remove or downgrade it rather than stacking.

Rule: **when a week front-loads a stimulus, the following week's plan must be edited, not just observed.** A plan left un-revised while the body has already absorbed its main session is worse than no plan.

## Step 5 — Re-baseline the increment

Weekly progression is judged against the **most recent actual week**, not against the last planned week.

- If actual > planned, the next week's increment shrinks automatically. An oversized week can legitimately *restore* compliance — a target that looked like a +30% jump against plan may be only +7% against reality.
- If actual < planned, the next week's target must not be calculated from the plan; it must come from the actual, or the jump arrives all at once.
- State which baseline you used, so the number is auditable.

Corollary: an accidental over-volume week is not a disaster — it raises the floor. The real cost is the lost recovery, which must be repaid at the *start* of the next week (full rest or very short easy runs for the first 1–2 days), not spread invisibly across it.

## Step 6 — Close the week and open the next one in one pass

A settlement that stops at "here is what happened" leaves the plan system inconsistent. Always complete all four:

1. **Session-level:** log only sessions that carry an independent reviewable signal (key workouts, long runs, quality, races) — easy runs and cross-training belong in the weekly summary, not as standalone entries.
2. **Week-level:** actual volume, run count, status → completed; the week's biggest gain, biggest problem, one adjustment for next week, health note.
3. **Next-week-level:** if the settlement changed anything about next week (volume, the long run's structure, number of quality sessions), edit next week's plan *now*. Leaving a contradiction between two weeks' pages is a data-integrity failure.
4. **Profile-level:** write back anything that changed a *parameter* rather than a *plan* — re-derived pace bands, confirmed capability ceilings, revised phase roadmap.

## Step 7 — Verdict template

Keep the weekly verdict to three lines:

```
1. Did intensity hold? Did dose hold? (name the failure that occurred)
2. Which single session produced the week's most valuable signal, and what did it prove?
3. What does this change about next week — volume baseline, key session, or recovery debt?
```

Then the recovery instruction for the next 48 h, which is the only part of the review with a deadline.
