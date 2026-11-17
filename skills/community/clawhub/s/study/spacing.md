# Spacing, Intervals, and Review Debt

Same total hours, spread out, produce more retention than massed. That is the entire mechanism — everything below is about choosing the gaps and surviving the queue they create.

**Contents:** [Choosing the Gap](#choosing-the-gap) · [The Interval Ladder](#the-interval-ladder) · [Successive Relearning](#successive-relearning) · [Fitting the Ladder Inside the Horizon](#fitting-the-ladder-inside-the-horizon) · [Interleaving](#interleaving) · [Review Debt](#review-debt) · [Capacity Math](#capacity-math) · [Cramming When It Is Genuinely the Right Call](#cramming-when-it-is-genuinely-the-right-call) · [After the Exam](#after-the-exam)

**Before scheduling any review**, read `## Topics` (state, last retrieved, next review) and `## Due` in `~/Clawic/data/study/memory.md`. Overdue items are stated out loud at the start of the session — a statement, not a question.

## Choosing the Gap

**Gap ≈ 10-20% of the retention interval** (Cepeda). The retention interval is the time from now until you must know it — which is the exam date, not the end of term.

| Must know it in | Gap between reviews | Reviews needed |
|---|---|---|
| 5 days | 1 day | 4-5 |
| 2 weeks | 1-3 days | 5-6 |
| 2 months | 6-12 days | 5-8 |
| 6 months | 3-5 weeks | 5-7 |
| 1 year (licensing exam, prerequisite course) | 5-10 weeks, tightening in the last month | 6-10 |

Two consequences students get wrong in opposite directions: reviewing daily for an exam six months out wastes an enormous number of reviews on material that was not going to be forgotten; reviewing weekly for an exam in five days leaves half the material unreviewed at all.

## The Interval Ladder

Per topic or per card, starting from the first successful unaided recall:

```
success  → next_interval = last_interval × 2 to 2.5
lapse    → next_interval = 1 day, and the ladder restarts
ceiling  → next_interval never lands after the exam date
```

- Start at 1 day, then 2-3, 6, 14, 30. Multiply by the smaller factor for material that keeps lapsing, the larger for material that returns instantly.
- **A lapse resets the ladder but not the knowledge**: the second climb is faster than the first, which is why a relapsed topic is cheap and an unstudied one is not.
- Judge success by the unaided attempt, never by "that looked familiar" (`retrieval.md`).
- Where an SRS app owns the schedule, let it: it is doing this arithmetic per card, with the student's own lapse history (`flashcards.md`). Keep this ladder for *topics*, which no app tracks.

## Successive Relearning

The high-utility combination: test to criterion, then relearn on a spaced schedule (Rawson & Dunlosky). Practically:

1. Session 1: study, then retrieve until **one correct unaided recall** (criterion). Stop there — extra reps in the same session buy little.
2. Sessions 2, 3, 4, spaced by the ladder: retrieve to criterion again, from cold.
3. A topic is `exam-ready` after **≥3 relearning sessions** at expanding gaps, and that is the state recorded in `## Topics` (SKILL.md Rule 3).

The failure mode this prevents: a topic studied hard once, marked done in week 2, and gone by the exam — with the student's honest memory being "I studied that a lot".

## Fitting the Ladder Inside the Horizon

When there is not room for a full ladder before the date:

- **Compress, do not skip.** Four reviews at 1-2-4-7 days fit in a fortnight; the same four at 1-3-7-14 do not fit in ten days. Recompute rather than dropping reviews.
- **Front-load the topics with the longest ladders** — the weakest and heaviest ones need to start first because they need the most passes, not because they are more important.
- **Never place the last review more than 2 days before the exam.** The final pass exists to bring the whole set to the surface simultaneously, which is a different job from learning it.
- Topics that cannot fit even a 3-review ladder are candidates for the cut list (`planning.md`), not for a single desperate pass.

## Interleaving

Mixing topics within a practice set improves discrimination — knowing *which* method applies, not just how to run it (Rohrer). Governed by `interleaving`.

- **Block while acquiring, interleave once acquired.** A procedure you cannot yet execute needs consecutive reps; a procedure you can execute needs to be told apart from its neighbours. Switch when solo solves start succeeding, not before.
- Interleave the **confusable**, not the unrelated: three hypothesis tests together, or three drug classes with similar names. Mixing chemistry with medieval history is just switching cost.
- Expect practice accuracy to drop when interleaving starts. That drop is the mechanism, and it is the reason students abandon it — record the exam-side outcome in `## What Works` rather than judging on practice scores.
- Mixed sets are also the honest simulation: an exam paper is maximally interleaved by construction.

## Review Debt

The queue is the only part of the system whose collapse compounds.

```
days_to_clear = skipped_days × daily_load ÷ (capacity − daily_load)
```

A week off at 30 min/day of load, against a 45 min/day capacity, takes `7 × 30 ÷ 15` = **14 days** to clear. Two weeks off takes a month. This is why the daily slot survives illness at reduced size while everything else is dropped (`planning.md`).

Triage for a backlog, in order:

1. **Stop new items entirely** until the queue is clear. Adding while behind is the single decision that turns a backlog into an abandoned system.
2. **Sort by lapse count, not by age.** The oldest item is often the easiest; the item that has lapsed four times is the one that is actually gone.
3. **Cut the deck, not the review**: suspend or delete the low-yield items rather than half-reviewing everything (`flashcards.md`). A queue that is honestly 400 items long is better than 900 items reviewed carelessly.
4. **Reset intervals on anything untouched for more than 3× its interval.** Those items have already been forgotten; treating them as reviews wastes the schedule's arithmetic.

## Capacity Math

Daily review load is not a preference, it is a consequence:

```
daily_reviews ≈ Σ (1 / interval_i)   over every item in the system
```

- A steady stream of new items settles at roughly **10× the daily new-item rate** on typical settings: 20 new cards/day → about 200 reviews/day → at ~6 s/card, roughly 20 minutes. That is the arithmetic behind `daily_review_cap`.
- **Set new items from the review time you can afford**, not the other way round. The queue you create today is paid for daily for months.
- Every item added is a permanent subscription. This is the argument for cards only where content is genuinely arbitrary (`flashcards.md`) — derivable content is cheaper practiced as problems, because problems are not reviewed forever.
- When the projected queue exceeds `daily_review_cap`, stop introductions and say so in one line; it never grows without being named.

## Cramming When It Is Genuinely the Right Call

Massed practice produces test-day performance and rapid loss afterwards. That trade is correct in exactly one situation: a low-stakes assessment on material never needed again, with no prerequisite depending on it. Everywhere else it is a loan against next term.

If the exam is inside 48 hours and little is prepared, the protocol is not "study more":

1. One past paper or self-test first, unscored, to build the gap map. Studying without it spends the remaining hours on what was already known.
2. Rank the gaps by past-paper frequency × marks. Take the top slice only.
3. **Retrieval only** — no reading, no new sources, no note-making. Question, attempt, correct, next.
4. Protect a full night of sleep (SKILL.md Rule 9). The last three hours awake are worth less than the sleep they cost, and they cost the next morning too.
5. Write the post-mortem afterwards into `artifacts/` — the plan that produced the cram is the thing to fix, and it will be forgotten within a week of relief.

## After the Exam

- A course that is a prerequisite for the next one keeps a **maintenance ladder** at monthly-to-quarterly gaps. The alternative is relearning it under time pressure in September.
- A course never needed again: retire its topics and suspend its deck the day after the exam. Carrying dead reviews is the most common reason a working system gets abandoned.
- A professional qualification with recertification has a horizon measured in years; that is a `## Due` row, not a memory (`certifications.md`).

**After any review pass**, update `Last retrieved` and `Next review` in `## Topics`, write each lapse to `errors.md` with cause `not retrievable`, and record the run in `## Due`. When the queue is triaged, the decision and what was suspended goes to `## Decks` with the date (`memory-template.md`) — otherwise the same 300 cards get suspended, restored and re-suspended across three terms.
