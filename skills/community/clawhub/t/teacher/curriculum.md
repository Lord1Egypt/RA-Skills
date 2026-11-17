# Curriculum — Course, Syllabus, and the Order of Things

A course is a sequence of dependencies with a budget of contact hours. Most course design failures are arithmetic: more objectives than hours, or an order that teaches a skill before the one it rests on.

**Contents:** [Start From the Hours](#start-from-the-hours) · [Scope: What Gets Cut](#scope-what-gets-cut) · [Sequence: Dependency Before Topic](#sequence-dependency-before-topic) · [Spiralling and Interleaving](#spiralling-and-interleaving) · [Aligning to a Specification](#aligning-to-a-specification) · [The Syllabus as a Contract](#the-syllabus-as-a-contract) · [Assessment Calendar](#assessment-calendar) · [Textbooks and Adopted Resources](#textbooks-and-adopted-resources) · [Inheriting Someone Else's Course](#inheriting-someone-elses-course) · [Coverage Audits](#coverage-audits)

**Before designing or revising a course**, read `## Teaching Context` and `## Environment` in `~/Clawic/data/teacher/memory.md` (timetable shape, term structure, room constraints) and any existing scheme in `artifacts/`. A course rebuilt from scratch when a working scheme exists is the most expensive avoidable job in teaching.

## Start From the Hours

Compute the real budget before writing a single objective:

`teaching hours = weeks × lessons_per_week × session_length_min ÷ 60 − losses`

Losses are not a rounding error. Subtract, honestly: assessment sittings, feedback and reteach lessons, exam-board practicals, trips, assemblies, snow and strike days, the fortnight lost to school events. **A realistic loss figure is 15-20% of nominal contact time**; a scheme built on nominal hours finishes the last unit in the week of the exam, with no practice.

- Reserve one lesson in six for reteach and consolidation (`planning.md`) before allocating any content.
- The remainder is the actual budget. Every objective added after this point removes another one.

## Scope: What Gets Cut

Rank every candidate objective on two axes and cut from the bottom-left:

| | Load-bearing for later work | Not load-bearing |
|---|---|---|
| **Assessed** | Teach to mastery, revisit three times | Teach once, practise, retrieve before the exam |
| **Not assessed** | Teach to mastery anyway — it is a prerequisite | Enrichment: teach only from the slack |

- **The prerequisite test beats the interest test.** A charming topic that nothing depends on is the correct thing to cut first, and the hardest.
- **Depth beats coverage where the two conflict**, because unmastered coverage is not coverage: a topic taught at 40% mastery must be retaught, so it costs twice and appears once.
- Where a specification mandates content you consider low-value, teach it — but at the level the specification assesses it, not at the level you would prefer.

## Sequence: Dependency Before Topic

1. List every objective on its own line.
2. For each, name what a student must already be able to do. That is one edge of the dependency graph.
3. Sort so that no objective appears before its prerequisites. Where the graph allows several valid orders, choose the one that puts the hardest, most load-bearing material earliest in the year — the time to reteach it exists in November and does not exist in May.
4. Anything with more than two unmet dependencies at its position is misplaced, whatever the textbook does.

Common sequencing errors: teaching notation before the concept it notates; teaching analysis before the students can do the procedure fluently; teaching the exception before the rule; teaching a synthesis task in week two "to motivate", which mainly demonstrates to novices that they cannot do it.

## Spiralling and Interleaving

- **Spiral** means each topic returns at a higher cognitive level, not that it is repeated. Plan the return explicitly: first pass application, second pass analysis, third pass under exam conditions.
- **Interleave** across units in the retrieval starter, not by fragmenting instruction. Instruction is blocked; practice is interleaved. Confusing the two produces a course that never teaches anything to fluency.
- Spacing gap is derived from the terminal assessment date: 10-20% of the retention interval (SKILL.md Rule 5). A June exam and a September topic means that topic returns roughly monthly — nine planned returns, each 5 minutes of a starter, is 45 minutes total and is the cheapest exam preparation that exists.

## Aligning to a Specification

Where `standards` is set (an exam-board specification, state standards, a professional competency framework, an accreditation matrix):

- **Map objectives to codes in both directions.** Objective → code proves nothing is unassessed effort; code → objective proves nothing is uncovered. The second direction is the one that gets skipped and the one that fails an audit.
- **Read the assessment objectives, not just the content list.** A specification that weights 40% to application means teaching-to-recall fails at 40% of the marks regardless of coverage.
- **Command words are content.** "Evaluate", "justify", "compare", "state" have fixed meanings in a specification and predictable mark schemes; students lose marks for answering the wrong verb far more often than for not knowing the material.
- Record the mapping as an artifact, not as a mental model: `artifacts/coverage-<course>.md` with a row per code, its lesson, and its assessment.

## The Syllabus as a Contract

A syllabus that answers these in writing prevents most disputes later (`parents.md`, `higher-ed.md`):

| Section | What it must state |
|---|---|
| What the course is for | The terminal capability, in the students' language |
| Sequence | Units, order, and roughly when each falls |
| Assessment | Every graded item, its weight, its form, and the date |
| Grading | The scale (`grade_scale`), how components combine, what rounding happens |
| Late and missed work | The rule, the penalty, the extension route — written before the first request |
| Resubmission and retakes | Whether they exist and their ceiling |
| AI and collaboration | What is permitted per assignment type (`ai_policy`, `integrity.md`) |
| Accessibility | How adjustments are arranged and by when |
| Contact | Channel, response window, office or support hours |

- Write the late-work and AI clauses per assignment type, not as one blanket rule: "AI permitted for brainstorming, prohibited in the submitted draft, disclosed in a one-line statement" is enforceable; "use AI responsibly" is not.
- The syllabus is an artifact and is reused annually: it belongs in `artifacts/`, with the year's changes noted at the top.

## Assessment Calendar

- **Stagger across classes.** Four classes handing in the same week is the arithmetic in SKILL.md Rule 8 detonating on one weekend. Offset by at least a week per class.
- **Check the whole-school calendar** before setting anything: students sitting three subjects' coursework in the same fortnight produce worse work in all three and the blame lands on whoever set last.
- Every assessment date gets a marking-return date derived from `grading_turnaround_days`, and both go in `## Due`.

## Textbooks and Adopted Resources

- A textbook is a resource, not a scheme. Map its chapters onto your sequence and expect gaps in both directions.
- Check what the book's exercises actually practise: many drill the worked-example type only, which produces students who cannot recognise a problem out of context. Add interleaved and unfamiliar-context items yourself.
- Where a department scheme is in force, deviate visibly and in writing rather than quietly — a colleague teaching the parallel class needs to know what your students did and did not see.

## Inheriting Someone Else's Course

Do these in order, in the first fortnight:

1. Get the terminal assessment and last year's results distribution. Everything else is context.
2. Get the scheme, and diff it against what students actually saw — ask the students, they know.
3. Run a prerequisite check on the two most load-bearing prior objectives. This is the single highest-value hour of the handover.
4. Change one thing at a time. A wholesale rewrite mid-course removes the only structure the students have.
5. Record what you found in `## Pacing` and `## Teaching Context`; next year's version starts from it.

## Coverage Audits

Run at each `report_cycle` and at half-term, as a `## Due` row:

- Codes or objectives taught vs planned to date, as a count and a percentage.
- Objectives taught but never retrieved since — these fail the delayed test and read as "we never did this".
- Objectives assessed at a lower cognitive level than the specification demands.
- Slack lessons remaining vs weeks remaining: if slack is exhausted before the halfway point, the scope was wrong and something must be cut now while cutting is still cheap.

**When a scheme of work, syllabus, coverage map or sequencing decision is produced**, write it to `~/Clawic/data/teacher/artifacts/<kebab-name>.md` with the date and the hours budget it assumes, and add its `## Boxes` line to `memory.md` in the same turn (`memory-template.md`). **When a coverage audit runs**, update its `## Due` row and put what was cut or carried in `## Pacing` in the class file. **When the redesign is a multi-week job with milestones**, it is a project: `~/Clawic/data/projects/<project>.md`, with the artifacts referenced by name.
