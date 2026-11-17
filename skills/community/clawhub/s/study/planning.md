# Planning a Term, a Week, and a Recovery

A study plan is an arithmetic claim: these topics, in these hours, by this date. Most plans fail because the claim was never checked — not because the student was lazy.

**Contents:** [Syllabus Intake](#syllabus-intake) · [The Hour Budget](#the-hour-budget) · [Backwards From the Date](#backwards-from-the-date) · [Splitting Hours Across Courses](#splitting-hours-across-courses) · [The Weekly Grid](#the-weekly-grid) · [The Weekly Review](#the-weekly-review) · [Exam Season With Several Dates](#exam-season-with-several-dates) · [When the Plan Breaks](#when-the-plan-breaks) · [Studying Around a Job](#studying-around-a-job)

**Before building or revising any plan**, read `## Courses`, `## Topics` and `## Due` in `~/Clawic/data/study/memory.md`, plus `errors.md` — a plan that ignores what this student keeps getting wrong is a syllabus, not a plan.

## Syllabus Intake

Ten minutes at the start of a course buys the whole term. Extract, in this order, and record in `## Courses`:

1. **The dated assessments** and their weights. Anything without a date gets an assumed date and the assumption said out loud.
2. **The format of each one** — MCQ, long answer, oral, practical, open-book, take-home. This is what Rule 5 practices against; getting it wrong wastes the entire preparation.
3. **The hurdles**: minimum component marks, attendance floors, must-pass exams, compulsory labs. Binary, and they outrank every weight.
4. **The topic list**, from the syllabus rather than the textbook's table of contents — the two differ, and the syllabus is what is examined.
5. **What is permitted in the room**: calculator, formula sheet, notes, dictionary, AI. Each one changes what is worth memorizing.
6. **Where past papers live**, and whether the examiner changed this year.

A syllabus with 34 topics and no dates is the normal starting state. Give it dates before doing anything else, even invented ones — an undated plan cannot be checked.

## The Hour Budget

- **Measure, do not assume, `hours_per_topic`.** Take the first two topics of a course to criterion (one unaided recall) and time them. Most students' real number is 1.5-3× their guess, and the guess is what makes plans collapse in week 6.
- **Available hours are what is left after the fixed grid**: classes, commute, work, sleep at 7+, meals. Write the fixed grid first; the residue is the honest budget, and it is usually far below the stated `weekly_hours`.
- **Plan to 80% of the budget.** A plan that consumes every available hour fails on the first sick day, and the failure is read as personal weakness rather than as arithmetic. The reserve is not slack — it is where the missed session goes.
- **Reserve the last 20% of the timeline** for simulation and error repair, with no new material in it. A plan whose last day is also the day the last topic is first seen has no capacity to fix what the simulation finds.

## Backwards From the Date

```
hours_needed          = topics_remaining × hours_per_topic
weekly_hours_required = hours_needed ÷ weeks_left
```

If `weekly_hours_required > 0.8 × weekly_hours`, the plan does not fit and the answer is scope, not effort.

**Worked**: Stats, 24 remaining topics at 1.5 h = 36 h, 4 weeks left → 9 h/wk against a 12 h budget (0.8 × 12 = 9.6) → fits, with room for the review queue.
**Worked, failing**: Pharmacology, 40 topics at 1.5 h = 60 h, 4 weeks → 15 h/wk against the same budget → over. Cut by `past-paper frequency × mark weight` until the number lands under 9.6: keeping the top 25 topics gives 37.5 h → 9.4 h/wk. Say which 15 were cut and what the exposure is — "these 15 topics are uncovered; across five past papers they were worth ~6 marks a paper."

Cutting is the skill. Refusing to cut produces a plan that covers everything at a depth that retains nothing, which scores worse than a plan that abandons the tail on purpose.

## Splitting Hours Across Courses

Equal division is the default mistake. Rank the next block by `weight × gap ÷ hours to close it` (SKILL.md, Deadlines And Grade Math), with three overrides:

- **Hurdles first.** A must-pass component at risk takes the hours regardless of weight arithmetic.
- **The earliest date first when two are within a week of each other** — a topic learned for Monday's exam is still there on Friday, but not the reverse.
- **The weakest-and-heaviest course gets the first fresh hour of the day**, not the last tired one. Comfort ordering is what leaves the hardest course studied only when exhausted.

Rotate courses within a week rather than blocking one course per week: a course untouched for nine days needs relearning before it can progress, and that relearning is the cost that the weekly rotation avoids.

## The Weekly Grid

1. **Anchors** — classes, work, commitments, sleep window, one non-negotiable rest block.
2. **Fixed daily review slot** at the same time, sized by `daily_review_cap`. Same time every day is what stops the queue exploding (`spacing.md`).
3. **Deep blocks** at `session_minutes`, placed in the best hours declared under `work_order`, each labelled with a course *and an outcome* — "STA201: hypothesis testing to criterion", never "STA201: study".
4. **One weekly simulation slot** once inside 6 weeks of an exam: a timed past paper or a timed section.
5. **Two floating catch-up blocks** left unassigned; they absorb overruns. Unused, they become rest — never quietly refilled with more topics.

A weekly plan that names an outcome per block is checkable on Sunday. One that names hours is not.

## The Weekly Review

Fifteen minutes, on `review_day`, and it is the mechanism that keeps everything else honest:

| Check | Action |
|---|---|
| Blocks planned vs blocks done (`session-log/<year>-<month>.md`) | Below 70% for two weeks → the budget is wrong, not the student; re-cut scope |
| Topics that moved state this week (`## Topics`) | Zero moved with hours logged → the hours were reading, not retrieval (Rule 1) |
| Open loops in `errors.md` — misses with no retry date | Schedule them into next week's first blocks |
| Overdue reviews | Triage before adding anything new (`spacing.md`) |
| Weight × gap ranking | Re-rank; last week's priority is often not this week's |
| Deadlines inside 14 days | Pull movable work forward; ask for extensions now, not in the last week |

Write the review's outcome as the next week's plan, then update `## Due` with the run date. A review with no last-run date gets skipped for a month and nobody notices.

## Exam Season With Several Dates

Place the **final relearn pass for each exam in the 48 hours before it**, working backwards from the last exam to the first, then fill the remaining days forward with the earlier exams' build-up. That ordering is what resolves the classic clash where two exams three days apart both want the day before.

- An exam on day 1 of the season gets its build-up in the weeks before the season, not during it. There is no time inside the season.
- Between two exams 24 hours apart, the second exam's session is retrieval-only on its highest-yield gaps — new material between exams is never retained and costs the sleep that the second exam needs.
- Do not schedule the post-mortem of exam A before exam B. Write the raw observations, close it, and run the post-mortem after the season (`artifacts/`).

## When the Plan Breaks

- **A missed session** goes into a floating catch-up block. Two missed in a week means the grid was wrong: rebuild it against the honest budget.
- **A missed week** is not redistributed across the remaining weeks — that is how a plan becomes impossible and gets abandoned entirely. Cut scope by the same fraction of time lost: one week lost of four remaining = cut the lowest-yield quarter.
- **A course added mid-term** (a resit, an elective) takes its hours from cuts, never from sleep or from the reserve.
- **Illness or a crisis**: hold the daily review slot at whatever size is possible and drop everything else. The review queue is the only part whose collapse compounds (`spacing.md`); topics simply wait.
- **The plan was never followed at all**: this is a starting problem, not a planning problem (`motivation.md`). Rebuilding the same plan smaller is the fix; rebuilding it more detailed is not.

## Studying Around a Job

- Budget on **weekly** rather than daily hours, and place the load on the two days that actually exist. Daily targets fail on the first shift that runs late and take the streak with them.
- Protect one full block a week over five fragments: reading and problem work have a reload cost that 25-minute gaps never repay.
- Commute and dead time carry the review queue and audio, never new material (`lectures.md`).
- A professional certification hung on a booked date is planned the same way, with the blueprint replacing the syllabus (`certifications.md`).
- Where the employer funds it, the deadline and the money are usually tied to a booked exam date — that booking is a row in the shared `bookings/<year>.md` (`memory-template.md`).

**When a plan is agreed**, write the courses and their dates, weights, formats and hurdles to `## Courses`, the topic list to `## Topics` with state `seen`, and the review cadences to `## Due`. If the timetable survived a full week, it is worth keeping as `artifacts/<kebab-name>.md` with its `## Boxes` line — the plan that held is the one to rebuild from next term, and the one that did not is evidence for `## What Works` (`memory-template.md`).
