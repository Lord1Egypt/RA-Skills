# Assessment — Tests, Rubrics, and Items That Measure Something

A summative assessment makes a claim about what a student can do. The claim is only as good as the blueprint behind it, and most classroom papers have none.

**Contents:** [Blueprint First](#blueprint-first) · [Choosing the Form](#choosing-the-form) · [Writing Items](#writing-items) · [Constructed Response and Essays](#constructed-response-and-essays) · [Performance Tasks and Projects](#performance-tasks-and-projects) · [Rubrics](#rubrics) · [Validity, Reliability, Fairness](#validity-reliability-fairness) · [Item Analysis After the Sitting](#item-analysis-after-the-sitting) · [Accessibility and Access Arrangements](#accessibility-and-access-arrangements) · [Reusing and Retiring Items](#reusing-and-retiring-items)

**Before writing a paper on a topic already tested**, read `~/Clawic/data/teacher/assessments/<year>.md`: which items discriminated, which were too easy to be worth marking, and which distractor exposed the misconception worth testing again.

## Blueprint First

A blueprint is a table of content × cognitive level, with marks allocated in proportion to teaching time and to the weighting the course claims.

| Topic | Recall | Apply | Analyse/Evaluate | Marks | % of teaching time |
|---|---|---|---|---|---|
| Bonding | 4 | 8 | 4 | 16 | 27% |
| Moles | 2 | 10 | 6 | 18 | 30% |
| Rates | 3 | 6 | 3 | 12 | 20% |
| Practical skills | 0 | 6 | 8 | 14 | 23% |

- **Build the table before writing a single question.** Written question-first, a paper drifts toward whatever is easiest to write, which is recall of the most recent topic.
- **Marks proportional to teaching time**, within a few points. A topic that took a third of the term and carries 8% of the marks tells students their time was wasted, and they are right.
- **Cognitive level must match how it was taught** (`planning.md`). Teaching worked examples and testing unseen transfer measures aptitude, not the course.
- Where `standards` is set, add a column for the specification code and check that assessment-objective weightings match the specification's own.
- Save the blueprint in `artifacts/` — it is the reusable part; questions can be rewritten around it each year.

## Choosing the Form

| Form | Measures well | Fails at | Marking cost per script |
|---|---|---|---|
| MCQ / short answer | Breadth of recall and application, misconception detection | Reasoning, communication, method | ~1 min, or zero if self-marked |
| Structured question with parts | Method, staged reasoning | Synthesis, original structure | 3-6 min |
| Essay | Argument, selection, integration | Reliability without moderation; breadth | 8-20 min |
| Practical / performance | Procedure and judgement in real conditions | Consistency across sessions | High, and live |
| Project or portfolio | Sustained work, integration | Provenance — who actually did it (`integrity.md`) | Very high |
| Oral / viva | Depth and authenticity; fastest way to verify authorship | Coverage, scheduling at scale | 3-8 min, live |

Choose by what the claim needs, then check the total against the marking budget (SKILL.md Rule 8) *before* setting it. An essay for four classes of 28 at 12 minutes each is 22 hours. That decision is made when the paper is designed, not the weekend it arrives.

## Writing Items

- **The stem asks the whole question.** A student should know what to do without reading the options.
- **Three options** (Rodriguez 2005): the key plus two distractors that are real errors. A fourth option is usually filler, and filler teaches students to eliminate by style rather than by knowledge.
- **Every distractor traceable to a misconception** from `## Misconceptions`; that is what turns a mark into a diagnosis.
- Avoid: negatives in the stem, "all/none of the above", clueing between items, options that differ in length or grammatical parallelism, and context that adds reading load without adding to the construct.
- **Vary the surface, hold the structure.** Items that all look like the taught example measure recognition of the example.
- Command words are content: use the same verbs the course and the specification use, with the same meanings (`curriculum.md`).
- Order easiest-first within a section. Early failure changes performance on later items for reasons unrelated to knowledge.
- Say the mark allocation next to each part. Students calibrate effort to marks, and unmarked expectations produce three-word answers to five-mark questions.

## Constructed Response and Essays

- Write the mark scheme at the same time as the question, not after collecting scripts. If you cannot write it, the question is ambiguous.
- **Point-based or level-based, not both.** Point-based (this content earns this mark) suits structured recall; level-based descriptors suit extended argument. Mixing them produces double-counting arguments in moderation.
- Give the criteria to students in advance, with a marked exemplar. Secret criteria measure guessing the teacher.
- Where possible, mark question-by-question across all scripts rather than script-by-script: it holds the standard steadier and is faster (`grading.md`).

## Performance Tasks and Projects

- Assess the process, not only the product: checkpoints, a plan, a draft, a log. Checkpoints are also the strongest authorship evidence you will have (`integrity.md`).
- Split the grade: the individual component must be individually assessable, even on a group product (`engagement.md`).
- Constrain the brief enough to be comparable and open enough to be worth doing. Unconstrained projects are unmarkable and reward the students with the most support at home.
- Publish the rubric with the brief, and mark one exemplar with the class before they start.

## Rubrics

- **Four levels by default.** An even number removes the safe middle; three collapses to pass/fail; six invents distinctions markers cannot hold apart. Where `grade_scale` mandates a shape, map the four onto it rather than inventing levels per assignment.
- **Descriptors state observable features, not amounts of quality.** "Cites two sources and explains how each supports the claim" is markable; "good use of sources" is not. The word "appropriate" in a descriptor means the criterion has not been written yet.
- One criterion per row, and criteria that can vary independently. If two rows always score the same, they are one row.
- **Analytic** (criterion by criterion) for feedback and for teaching; **holistic** for speed at scale and for high-agreement judgement calls. Choose deliberately: analytic marking is roughly twice the time and produces feedback students can act on.
- **Norm before marking**: pick 3-5 anchor scripts spanning the range, mark them alone, then agree the boundaries — with a colleague where possible, against last year's anchors where not. Re-check yourself against the anchors every 20 scripts (`grading.md`).
- Weight the rows explicitly. Unweighted rubrics are averaged without comment, which gives presentation the same weight as reasoning.
- A normed rubric is an artifact: it is reused, so it lives in `artifacts/` with the anchor scripts named.

## Validity, Reliability, Fairness

- **Validity is about the claim**: does this measure the objective, or does it measure reading speed, prior background, typing, or home support? The most common invalidity in classroom testing is reading load unrelated to the construct.
- **Reliability is about consistency**: would the same student score the same tomorrow, and would a colleague give the same mark? Classroom tests conventionally aim for an internal-consistency coefficient (KR-20 or alpha) of ≥0.70, and ≥0.80 for anything high-stakes. Short tests are unreliable by construction: **10 items is a snapshot, not a measurement**.
- **Single-marker essay grading is the least reliable common practice in schools.** Mitigations, in order of effect: level descriptors with anchors, marking question-by-question, blind marking, a second marker on boundary scripts, comparative judgement for large batches.
- **Fairness**: contexts that assume specific cultural or economic experience, names and scenarios that exclude, and time limits that measure processing speed when speed is not the construct.
- Timed conditions test fluency. If fluency is not the objective, the time limit is a confound.

## Item Analysis After the Sitting

Two numbers per item, computed once, worth an hour a year:

- **Difficulty `p`** = proportion of students who got it right. Items in the 0.4-0.8 band carry most of the discriminating information; `p` above 0.9 or below 0.2 tells you almost nothing about differences between students, though a very easy opener has a legitimate role.
- **Discrimination `D`** = (proportion correct in the top 27% of scorers) − (proportion correct in the bottom 27%). Ebel's conventional bands: **D ≥ 0.40 excellent · 0.30-0.39 good · 0.20-0.29 marginal, needs editing · < 0.20 revise · negative = broken or mis-keyed**, and a negative D on a reused item means strong students are being penalised for knowing more.
- Read the distractors too: an option chosen by 40% of the class names the reteach for next lesson.
- **Where the whole class fails an item, suspect the teaching or the item, in that order — not the students.** An item at p=0.15 that was taught properly is usually ambiguous.

Record both numbers, the distribution, and what gets retaught in `assessments/<year>.md`.

## Accessibility and Access Arrangements

- Apply every arrangement in the class file by default: extra time as a percentage, separate room, reader, scribe, coloured overlay or paper, enlarged print, assistive software (SKILL.md Rule 9).
- Design out the need where possible: clean layout, sans-serif at adequate size, no reliance on colour alone, plain language in the stem, one question per block.
- Extra time is applied to the whole paper, not to the questions the teacher thinks are hard.
- Never announce an arrangement publicly, and never make a student ask for it in front of peers (`differentiation.md`).

## Reusing and Retiring Items

- An item's statistics belong to the item, not the paper: keep the bank in `## Item Analysis` in `~/Clawic/data/teacher/assessments/<year>.md` — the item, its topic, `p`, `D`, and the year it ran — for every item you intend to reuse (`checking.md`).
- Retire an item once it has circulated. Assume any paper sent home exists online.
- Rotate contexts rather than rewriting structure: the same construct in a new setting keeps the statistics roughly valid and defeats memorisation of answers.

**After any assessment is set and marked**, write the row in `~/Clawic/data/teacher/assessments/<year>.md`: date, class, what, max, mean, median, how many below pass, and the blueprint it came from — then the `## Item Analysis` rows for anything you intend to reuse, and the `## Retaught` row when the reteach happens. **When a blueprint, rubric, mark scheme or exemplar set is produced**, it goes to `~/Clawic/data/teacher/artifacts/<kebab-name>.md` with its `## Boxes` line in `memory.md`, in the same turn (`memory-template.md`) — these are the artifacts most reused across years.
