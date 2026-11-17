---
name: Studying
slug: studying
version: 1.0.4
changelog: "Display name shown correctly"
description: Plans study schedules and runs study sessions with retrieval practice, spaced review, and exam countdown protocols. Use when a student prepares for an exam, midterm, final, or certification, asks how to study, revise, memorize, or cram, says they studied hard but forgot everything, failed or blanked on a practice test, cannot focus or keeps procrastinating, or is juggling several courses before test week. Covers technique choice, weekly planning, note-taking, problem practice, essay prep, and test-day strategy, and persists what works for this student across sessions. Not for producing flashcard decks or practice tests themselves.
homepage: https://clawic.com/skills/studying
metadata:
  clawdbot:
    emoji: "📖"
    displayName: Studying
    configPaths:
    - ~/Clawic/data/studying/
---

User preferences and session history persist in `~/Clawic/data/studying/` (see `setup.md` on first use, `memory-template.md` for the file format). If you have data at an old location (`~/studying/` or `~/clawic/studying/`), move it to `~/Clawic/data/studying/`.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/studying/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| education_level | high-school \| university \| grad \| professional-cert | university | Calibrates examples and countdown templates; professional-cert routes long-horizon planning through `certifications.md` |
| block_length | number (minutes, 25-90) | 50 | Default session size in Session Protocol and the weekly grids in `scheduling.md`, until session logs establish this student's own degradation point (Session Protocol 5) |
| daily_review_cap | number (minutes) | 30 | Ceiling for daily flashcard review load; `memorization.md` stops new cards when the queue projects past it |
| study_days_per_week | number (2-7) | 6 | Scales the weekly grid and how many spaced sessions fit before an exam (`scheduling.md`) |

Preference areas to record as the user reveals them:

- **techniques** — methods proven or failed for this student (mind maps for conceptual courses, no group study); overrides the defaults in `techniques.md`
- **schedule** — best time of day, cadence, break style; shapes slot placement in `scheduling.md`
- **materials** — format preferences (video-first, past-paper-driven, worked examples); shapes the new-material pass
- **environment** — music vs silence, location, solo vs group; applied to the blocks in `focus.md`
- **exams** — the lead time this student actually starts, practice-test appetite; calibrates when `exam-countdown.md` fires

## When To Use

- A user has an exam, test, certification, or final on a date and needs a plan to get there
- A user asks how to learn, memorize, revise, or cram specific material (chapter, deck, problem set, lecture)
- A user reports "I studied hard but forgot everything", failed a practice test, or scores have plateaued
- Building a weekly revision schedule across multiple courses, or fitting cert study around a job
- Focus problems inside study work: procrastination, distraction, burnout mid-plan
- Mode: advise — this skill coaches a human student. Not for doing the assignment itself (`homework`), designing flashcards (`flashcards`, `anki`), or generating practice tests (`exam`)

## Quick Reference

| Situation | Play |
|---|---|
| Exam 4+ weeks out | Successive relearning: learn to criterion now, relearn in 3+ spaced sessions, gap = 10-20% of days remaining (→ Core Rule 2) |
| Exam in 5-7 days | One full timed past paper or self-test day 1 to locate gaps; spend remaining days on missed items only, 1-day gaps |
| Exam in <48h, little studied | Cram triage: one past paper for the gap map, retrieval-only on the highest-yield slice, sleep kept (→ `exam-countdown.md`) |
| Exam tomorrow | Retrieval-only sprint on highest-yield gaps, stop new material, protect a full night of sleep (→ Core Rule 6) |
| Fact-heavy material (vocab, anatomy, dates, law) | Flashcards with successive relearning; cap new cards so daily reviews stay under `daily_review_cap` (→ `memorization.md`) |
| Verbatim material (formulas, quotes, scripts) | First-letter cues plus flawless-recitation criterion (→ `memorization.md`) |
| Problem-based material (math, physics, coding) | Worked examples → faded practice → 2-3 correct solo solves, then interleave (→ `problem-subjects.md`) |
| Conceptual material (theories, mechanisms) | Closed-book explanation: write the concept from memory, mark every gap, check source, repeat next session |
| Essay exam course | Timed outline-from-memory practice on predicted questions (→ `essays-and-reading.md`) |
| Professional cert while working | Blueprint-weighted plan hung on a booked exam date (→ `certifications.md`) |
| Student says "it feels easy now" | Fluency illusion until proven: schedule a delayed self-test 1-2 days out before trusting it |
| Student failed a practice test | Diagnose per question: never-encoded vs forgot vs misapplied vs out-of-time (→ Diagnosing Misses) |
| Can't start, keeps procrastinating | Shrink the entry: first action = answer yesterday's missed questions, not "study chapter 3" (→ `focus.md`) |
| Blanking or panicking in tests | Two-pass pacing plus park-and-return (→ `test-day.md`); recurring panic → Red Flags |
| Multiple courses competing | Allocate time by (exam weight × current weakness), not by comfort; weakest-highest-stakes course gets the first fresh hour |
| Anything else | Default loop: 10 min recall of last session, new material with self-generated questions, close with a 5-question self-test |

Depth on demand: `techniques.md` what works, when, and what to retire · `scheduling.md` spacing math and weekly plans · `exam-countdown.md` horizon protocols and cram triage · `memorization.md` fact-heavy and verbatim tracks · `problem-subjects.md` math, physics, code · `essays-and-reading.md` reading, notes, essay prep · `focus.md` procrastination, environment, burnout · `test-day.md` pacing, MCQ, blanking · `certifications.md` studying alongside a job · `troubleshooting.md` symptom→cause chains.

## Core Rules

1. Retrieval beats re-exposure: at least 50% of any session is closed-book recall (self-test, blank-page dump, problem solving). Check: if the session log shows pages read but zero questions answered, the session failed. One week out, tested material is recalled at roughly 1.5x the rate of restudied material (Roediger and Karpicke).
2. Spacing formula: review gap = 10-20% of time until the test (Cepeda). Exam in 30 days: gaps of 3-6 days. Exam in 10 days: gaps of 1-2 days. For multi-month horizons the optimal ratio drifts down toward 5-10%; when unsure, choose the longer gap because too-long beats too-short at test time.
3. Successive relearning protocol (Rawson and Dunlosky): first session, practice each item until 3 correct recalls; every later session, until 1 correct recall; minimum 3 relearning sessions before the exam. Dropping an item after one correct answer is the single most common scheduling error.
4. Interleave only after acquisition: block a new problem type until 2-3 correct unassisted solves, then mix types so the student must pick the method, not just execute it. In Rohrer's math studies interleaved practice roughly doubled delayed-test scores versus blocked practice while feeling worse during practice.
5. Judge learning only after a delay: confidence rated immediately after studying is inflated by short-term fluency (Bjork's desirable difficulties). Rate an item "known" only if recalled cold at the start of a later session.
6. Sleep is part of the schedule: memory consolidation happens during sleep, so the night before the exam is study material too. If the plan requires trading sleep for new content within 24h of the exam, the plan is wrong; cut lowest-weight topics instead.
7. Low-utility techniques are pre-processing only: rereading, highlighting, and summarizing rate low-utility in Dunlosky's technique review. Allowed for exactly one pass whose sole output is a question list to feed retrieval practice.

## Session Protocol

1. Open with recall, not review: 5-10 min writing everything remembered from last session, blank page, book closed. Then check and mark gaps.
2. New material pass: for every section, generate 2-5 test questions (definition, why, applied case) and log them; questions are the session's durable artifact, highlights are not.
3. Close the loop: answer today's new questions plus all questions missed last session, cold. Anything missed twice gets flagged for the next session's opening.
4. Log one line to memory.md: date, topic, minutes, retrieval hit rate (correct / attempted). Hit rate below 60% next session means gaps are too long or items too big: split items or halve the gap. Above 90% two sessions running means gaps are too short: lengthen toward the Rule 2 ceiling.
5. Session length: start from `block_length`; stop when retrieval accuracy visibly degrades within the session, not at a fixed timer; log the duration where that happened and treat it as this student's default block length.

## Exam Countdown

Full horizon protocols, multi-exam weeks, and the cram triage live in `exam-countdown.md`. The core schedule:

- T-4 weeks: inventory all topics, weight by syllabus points; build spaced slots per Rule 2; start successive relearning on fact-heavy topics first because they need the most sessions.
- T-2 weeks: first full-length timed practice test under exam conditions (same time limit, no notes, same allowed tools). Score it, then re-plan: topics below ~70% get double slots, topics above 90% drop to maintenance (one retrieval pass per week).
- T-1 week: second timed test; practice the exam's actual format (essay outlines in essay courses, problem sets in problem courses). Format-mismatched practice inflates confidence without transferring.
- T-1 day: retrieval-only, no new topics, half-length day, full night of sleep. Prepare logistics (location, materials, ID) the evening before, not the morning of.
- Post-exam, 10 min: log to memory.md what the exam actually tested versus what the plan predicted; this calibrates the next countdown.

## Diagnosing Misses

For each miss on a self-test or practice exam, classify before fixing:

- Never encoded (no memory of ever seeing it): coverage hole; add to new-material queue, not to review queue.
- Encoded but forgot (recognized the answer instantly on reveal): spacing failure; shorten gap for that item and re-enter relearning at 3 correct recalls.
- Knew it, misapplied it (right fact, wrong method or wrong question read): practice-format failure; fix with mixed timed sets, not more flashcards.
- Ran out of time: pacing failure; all further practice tests get a per-question time budget = total minutes / question count, enforced.

Session-level, plan-level, and motivation failures: `troubleshooting.md`.

## Preference Memory

Persist in `~/Clawic/data/studying/memory.md` (format in `memory-template.md`, loading behavior in `setup.md`): Techniques, Schedule, Materials, Session Log, Exams, Never. Promote an observation to confirmed after 2+ consistent signals; confirmed entries override this skill's defaults except Core Rules 1, 2, and 6, which are non-negotiable floors. Declared preferences live in `config.yaml`; an observation never overwrites a declared preference without the student's confirmation.

## Output Gates

Before emitting a study plan or session design, verify:

- Retrieval share at least 50% of every session (Rule 1)?
- Every review gap inside the Rule 2 band for its exam distance?
- Fact-heavy topics scheduled for 3+ relearning sessions before the exam (Rule 3)?
- Full night of sleep intact every night, including the last (Rule 6)?
- At least one exam-condition practice test on the calendar (T-2 weeks)?
- Plan survives one missed session (re-space rule in `scheduling.md`), or does it require perfection?
- Values pulled from config.yaml and memory.md where they exist, not defaults the student already overrode?

## Red Flags

| Signal (observable) | Suspicion | Action |
|---|---|---|
| Second consecutive night under ~4h sleep to study | Sleep deprivation degrading the memory being built | Stop the plan, sleep first; replan with cut topics |
| Escalating stimulant use (doubling caffeine, borrowed prescription drugs) | Dependence or dangerous dosing | Do not optimize around it; flag it and route to a clinician |
| Panic symptoms during study or exams (racing heart, blanking, nausea) | Anxiety condition beyond technique fixes | Suggest campus counseling or a clinician; keep sessions short meanwhile |
| Skipped meals across multiple days to extend study time | Disordered eating pattern | Rebuild schedule around fixed meals; persistent pattern goes to a clinician |

Anything in this table suspends the protocols above: route to a clinician or counselor before resuming optimization.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Rereading until it "feels familiar" | Familiarity is recognition, not recall; it evaporates at the exam | Convert every reread urge into a closed-book question attempt |
| Massing all review into the final 48h | Cramming survives days, not the follow-on course or cumulative final | Rule 2 spacing; final 48h is retrieval-only maintenance |
| Reading worked solutions and nodding along | Recognizing a solution is not generating one | Cover the solution, re-derive solo; count only unassisted solves |
| Making flashcards or notes all session | Production feels like progress but contains zero retrieval | Cap creation at 30% of session; the rest is answering |
| Watching lecture videos at 2x as a "session" | Passive input at any speed encodes weakly and tests nothing | Counts as the one Rule 7 pass; output must be a question list |
| Studying the favorite subject first while fresh | Comfort allocation; the weak high-stakes course gets tired hours | Weakness × weight ordering from Quick Reference |
| Trusting confidence right after studying | Immediate judgments of learning are inflated by fluency | Only delayed cold recall marks an item known (Rule 5) |
| All-nighter before the exam | Loses the consolidation night and degrades exam-day retrieval | Cut topics, keep the sleep (Rule 6) |
| Untimed, open-note practice tests | Trains a different task than the exam | Exam conditions from the first practice test onward |

## Where Experts Disagree

- **Longhand vs laptop notes.** The original finding favored longhand for conceptual learning; direct replications have been mixed. The stable boundary: transcription is the failure mode on either medium — capture sparsely and process into questions within a day (`essays-and-reading.md`).
- **Pomodoro vs long blocks.** Timers beat blocks for aversive starts; blocks beat timers once engaged in problem sets or essays. Default: `block_length` with degradation-point stopping; pomodoro as the entry device for procrastination (`focus.md`).
- **Music while studying.** Lyrics compete with verbal encoding; instrumental is tolerable for routine problem practice, silence wins for reading and memorization. Treat the student's proven preference in memory.md as data that beats the default.
- **Group study.** Works as solo-solve-then-compare with explained disagreements; fails as shared rereading. The boundary is whether every member retrieves before the group talks (`techniques.md`).

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/studying (install if the user confirms):
- `exam` — generate the practice tests and timed simulations this skill schedules
- `flashcards` / `anki` — card design and deck mechanics for the fact-heavy tracks
- `spaced-repetition` — deeper scheduling theory when tuning gaps beyond Rule 2
- `learning` — curiosity-driven learning with no exam or deadline attached
- `homework` — doing the assignment itself rather than preparing for a test

## Feedback

- If useful, star it: https://clawic.com/skills/studying
- Latest version: https://clawic.com/skills/studying

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/studying.
