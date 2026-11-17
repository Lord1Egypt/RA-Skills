# Exams: Preparation, Formats, and the Room

The exam is the only assessment where preparation and performance are separate skills. Most lost marks in a well-prepared student are performance losses.

**Contents:** [Horizon Protocols](#horizon-protocols) · [Past Papers](#past-papers) · [The Frequency Table](#the-frequency-table) · [Simulation](#simulation) · [Marks and Minutes](#marks-and-minutes) · [Multiple Choice](#multiple-choice) · [Long Answer and Essay Exams](#long-answer-and-essay-exams) · [Oral Exams and Vivas](#oral-exams-and-vivas) · [Open-Book and Take-Home](#open-book-and-take-home) · [The Last 48 Hours](#the-last-48-hours) · [In the Room](#in-the-room) · [Blanking](#blanking) · [After the Exam](#after-the-exam)

**Before any exam-preparation session**, read `## Courses` for the format, weights and hurdles, `## Topics` for coverage state, and `errors.md` for the live gaps. Preparation that ignores the error log re-covers what is already known.

## Horizon Protocols

| Time left | Protocol |
|---|---|
| 6+ weeks | Full ladder: topics to criterion, ≥3 spaced relearnings each, one past paper early for the frequency table (Rule 3) |
| 3-6 weeks | Coverage first at criterion, one timed paper per fortnight, error log driving the sequence |
| 1-2 weeks | Timed papers twice a week; between them, only the missed items. New material only for high-frequency uncovered topics |
| 5-7 days | Day 1: full timed paper, unscored, to map gaps. Days 2-6: retrieval on missed items at 1-day gaps. Day 7: light |
| 48 hours | Cram triage: one paper for the gap map, retrieval-only on the top slice by frequency × marks, sleep protected (`spacing.md`) |
| Tomorrow | Retrieval only on highest-yield gaps, no new material, stop early, sleep 7+ (SKILL.md Rule 9) |

The protocol is chosen by time remaining and never by how prepared the student feels — the feeling is systematically wrong in both directions (`retrieval.md`, fluency illusion).

## Past Papers

Past papers are the highest-information source in the entire domain and they are systematically hoarded.

- **First paper in the first week of preparation**, unscored, open-book if necessary. It is a map, not a verdict, and treating it as a verdict is why it gets postponed.
- **Three uses, in order**: build the frequency table → diagnose gaps → simulate under time. Skipping to simulation wastes the diagnostic value.
- **Never mark your own paper generously.** Use the published mark scheme; where none exists, mark against the rubric criteria and be harsh — a generous mark is a lie you act on for a fortnight.
- Five years of papers is usually enough for a stable pattern; more adds little unless the course is unchanged for a decade.
- **Check whether the examiner or syllabus changed.** A frequency table from a previous examiner predicts the previous examiner. Where they changed, weight the most recent two years far higher and say so.
- Where papers do not exist: sample questions from the textbook matched to the exam's format, the professor's published quizzes, and questions generated from the syllabus's own learning outcomes — the outcomes are the blueprint.

## The Frequency Table

Built once per course, from all available papers, and kept in `artifacts/`:

| Topic | Papers it appeared in | Average marks when it appears | Last seen | Covered? |
|---|---|---|---|---|

- **Sort by average marks × appearance rate.** That product, not the syllabus order, decides the study sequence and the cut list (`planning.md`).
- Note **which topics appear together** — pairings are examiner habits and predict the shape of the long questions.
- Note **which never appear**: the syllabus routinely lists material that has not been examined in five years. Cutting it is a decision made with evidence, not a gamble.
- Recheck the table against this year's course announcements before trusting it (above).

## Simulation

The purpose is not scoring; it is discovering the performance losses that preparation cannot show.

- **Full length, full time, no notes, no phone, one sitting.** Half-simulations do not surface the failure that happens at minute 95.
- **Same time of day as the exam**, at least once.
- **Handwritten if the exam is handwritten.** Hand fatigue and writing speed are real constraints that typing hides entirely.
- Mark it, classify every miss by cause (SKILL.md Rule 6), and **write the causes into `errors.md`** — the distribution across `never encoded / not retrievable / procedure slip / misread / out of time` decides what the remaining weeks are for.
- A simulation showing 60% of losses under `out of time` means the remaining preparation is fluency and pacing, not content. This is the single most common misdiagnosis in exam preparation.

## Marks and Minutes

```
minutes_for_question = (total_minutes − 10% review reserve) × question_marks ÷ total_marks
```

A 6-mark question in a 120-minute, 100-mark paper gets `108 × 6/100` ≈ **6.5 minutes**. Write the per-section budget on the paper in the first minute of the exam.

- **The reserve is not optional**: the last 10% catches misread questions and unanswered parts, both of which are cheap marks.
- **Marks awarded fall off steeply within a question.** The first half of the marks on a question takes a quarter of the time; the last mark can take longer than an entire unattempted question. Move on at the budget and return with the reserve.
- **An unattempted question scores zero, always.** The most expensive habit in any timed exam is perfectionism on question 2.
- Where marks per question are not published, divide by question count and adjust once inside the paper.

## Multiple Choice

- **Answer before reading the options** where the format allows. Reading them first turns recall into recognition and makes distractors persuasive.
- **Eliminate actively**, marking why each option is wrong. The reason is what protects against the well-designed distractor.
- **Guessing, with the arithmetic**: on `n` options with a wrong-answer penalty `p`, a random guess has expected value `1/n − p(n−1)/n`. Break-even is `p = 1/(n−1)` — the standard negative-marking scheme. Under that scheme, random guessing is neutral and **eliminating even one option makes guessing positive-expected-value**. With no penalty, never leave a blank, ever.
- **"First instinct" is not a rule.** Changing answers is net positive on average; what is negative is changing on vague unease rather than on a recalled reason. Change when you can name what you missed.
- **Absolute qualifiers** (always, never, all) are more often false; hedged options are more often true — a weak signal, used only when genuinely stuck, never over a reason.
- **All questions are usually worth the same**, so the time budget is flat and the hard question is worth exactly as much as the easy one. Two passes: everything answerable on sight, then the flagged ones.
- Check answer-sheet alignment every ten questions on paper forms. A one-row shift is a catastrophic and entirely preventable failure.

## Long Answer and Essay Exams

- **Underline the command word and the constraint** before writing. "Evaluate" and "describe" have different mark schemes, and answering the wrong one caps the mark regardless of quality.
- **Outline for 10% of the question's time.** Five minutes of structure on a 45-minute essay reliably outperforms five extra minutes of prose.
- **Front-load the answer**: the thesis and the structure in the first lines. Markers under volume reward a visible argument.
- **Signpost with the mark scheme's language** where you know it — headings and explicit criteria make marks easy to award.
- **A partial answer to every question beats a perfect answer to two of three.** If time runs out, submit the outline in bullet points: structured bullets routinely earn most of the content marks.
- Legible handwriting is worth marks that no amount of preparation recovers.

## Oral Exams and Vivas

- **Practise aloud, to a person or a recorder.** Silent rehearsal does not train the retrieval-under-speech that a viva tests (`groups.md`).
- **A pause before answering is normal and reads as considered.** Filling silence is what produces the answer you did not mean.
- **Prepare for the follow-up, not the question**: examiners probe until they find the boundary. Knowing where your own understanding ends, and saying so cleanly, scores better than bluffing.
- "I do not know, but I would work it out this way" is a scoring answer in most rubrics; a confident invention is a failing one.
- For a thesis defence, know your **limitations section better than your results** — that is where the questions live (`coursework.md`).

## Open-Book and Take-Home

- **Open-book is a speed test against your index** (`notes.md`). Time spent hunting is time not spent answering.
- **Practise twice with exactly the permitted materials, timed.** The first practice reveals the notes are in the wrong order.
- **Take-home exams are graded harder** because resources were available: originality, precision and referencing carry the marks that recall carried before.
- Read the permitted-materials rules exactly, and the collaboration and AI rules with them. Getting this wrong is an integrity case, not a bad mark (`coursework.md`, `integrity_mode`).

## The Last 48 Hours

- **No new material.** Anything first met now will not be retrievable under pressure and displaces review of things that would have been.
- **One light retrieval pass** over the high-frequency topics, using the summary sheets built from memory (`notes.md`).
- **Logistics settled the day before**: venue, time, ID, permitted calculator, spare pens, travel time with a margin. A booked proctored exam's details are in the shared `bookings/<year>.md` (`certifications.md`).
- **Sleep is the intervention**, not the concession (Rule 9). Below 7 hours the exam is taken with degraded retrieval.
- Eat as normal; caffeine as normal. Exam day is not the day to change a variable.

## In the Room

1. **First 60 seconds**: read the instructions, count the questions, write the per-question minute budget on the paper.
2. **Answer the easiest question first** to establish momentum, unless the format forbids it.
3. **Park and return**: a question that stalls for more than a quarter of its budget gets marked and left. The answer very often arrives while working on another question.
4. **Watch the clock at fixed checkpoints** — a third and two-thirds through — not continuously.
5. **Use the reserve**: unanswered parts, misread commands, sign errors, unit errors, and the question you skipped.
6. **Never leave early.** There is no prize, and the review reserve is where cheap marks live.

## Blanking

- Blanking is a state, not a knowledge failure, and it passes. **Park the question, answer an easy one, and come back** — retrieval usually returns within minutes.
- **Write anything related**: a definition, a formula, a diagram. Partial output re-primes the network and often earns partial marks.
- **Slow the breathing deliberately** — a longer out-breath than in-breath, for four or five cycles.
- **Reappraise the arousal**: the physical state of alarm and the state of readiness are the same state, and interpreting it as readiness measurably outperforms trying to calm down (Jamieson).
- **Ten minutes of expressive writing before the exam** — writing out the worry itself — reduces the performance cost of exam anxiety (Ramirez & Beilock). It is one of the few interventions with a direct study.
- Recurring blanking despite preparation is a pattern to record in `## Pain Points`, and if it is severe or generalized, it is a referral, not a technique (`motivation.md`).

## After the Exam

- **Write the raw observations within the hour**, into `artifacts/post-mortem-<course>.md`: which topics appeared, what surprised you, where time ran out, which prepared answers went unused. Memory of an exam decays within a day and this is the input to the next frequency table.
- **Do not run the post-mortem before the next exam** in a season. Close the file and come back after (`planning.md`).
- The post-mortem is an artifact: mark, cause distribution from `errors.md`, what the plan got wrong, and what changes next time (`memory-template.md`).
- **Do not re-litigate answers with classmates afterwards.** It changes nothing and reliably damages the next exam in the season.

**After every paper, simulation and real exam**, write each miss to `errors.md` with its cause, the mark to `## Results` with its weight and the recomputed target, and the observations to `artifacts/post-mortem-<course>.md` with its `## Boxes` line. Update the frequency table artifact with this year's paper — that is what makes next term's cut list evidence rather than guesswork (`memory-template.md`).
