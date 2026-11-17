# Scheduling — Spacing Math and the Weekly Plan

The plan is arithmetic first, calendar second: gaps from Rule 2, session counts from Rule 3, then slots placed where this student's logs say they perform.

## Gap Arithmetic (Rule 2 worked)

| Days to exam | Gap (10-20%) | Spaced sessions that fit |
|---|---|---|
| 7 | 1 day | 5-6 |
| 14 | 1-3 days | 4-7 |
| 30 | 3-6 days | 5-8 |
| 60 | 6-12 days | 5-9 |
| 120+ | drifts toward 5-10% (6-12 days) | weekly cadence → `certifications.md` |

- Sessions per topic ≈ days remaining ÷ chosen gap. If that yields fewer than 3 relearning sessions for a fact-heavy topic, shorten the gap below the formula rather than dropping sessions — the Rule 3 floor beats the Rule 2 optimum.
- When unsure between two gaps, take the longer (Rule 2's tiebreak).

## Building the Week

1. Anchor fixed blocks first: classes, work, commute, meals, sleep. Sleep is load-bearing (Rule 6), not the flex space.
2. Place `study_days_per_week` days of slots sized `block_length` at the times memory.md marks as this student's best. No data yet: keep whatever time they already study at, and log hit rates by time of day for two weeks — the log picks the slot, not folklore.
3. First fresh slot of the day goes to the weakest highest-stakes course (SKILL.md Quick Reference).
4. One topic per slot; two courses back-to-back beats two hours of one course — spacing between topics is free interleaving.
5. Leave at least one empty slot per week as overflow. A plan that needs perfection to work is already broken.

## Multi-Course Allocation

share(course) ∝ exam_weight × current_weakness, where weakness = (100 − latest practice score).

Worked example: Course A is 50% of the grade at 60% mastery → 50×40 = 2000. Course B is 30% at 85% → 30×15 = 450. Course C is 20% at 70% → 20×30 = 600. Total 3050 → A gets ~66% of hours, B ~15%, C ~20%.

- Re-run the formula after every practice test — allocations rot as scores move.
- Comfort-drift check: if actual logged hours beat the formula for the course the student likes, the schedule is being renegotiated by mood; restore the ordering next week, don't punish the past one.

## Maintenance Mode

- A topic above 90% two sessions running drops to maintenance: one retrieval pass per week until the exam (same threshold as Session Protocol 4 and the T-2-weeks re-plan).
- Maintenance items ride along at the start of other slots — they never justify their own block.

## When the Plan Breaks

- Missed one session: do not double tomorrow. Re-space the remaining gaps with the Rule 2 formula from today; the gap widens slightly and the plan survives.
- Behind for a week or more: cut topics by ascending syllabus weight — never cut the retrieval share or sleep. A plan covering 70% of topics at criterion beats 100% seen once (Rule 1).
- New fixed obligation: shrink the number of blocks, not their quality; re-anchor the week from step 1.
- Chronic slippage (third re-plan in a month): the problem is entry or volume, not the calendar → `troubleshooting.md`, "Always behind the plan".
