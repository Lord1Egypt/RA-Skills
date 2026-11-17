# Working File Templates — Teacher

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — Configuration table keys and preference areas alike | `~/Clawic/data/teacher/config.yaml` | Key by key, read-modify-write |
| Teaching context, what works with these groups, environment facts, practice goals, pain points, due dates, box index | `~/Clawic/data/teacher/memory.md` | Rewritten in place; stays small |
| A class or cohort: roster, needs and accommodations, dynamics, seating, pacing against plan | `~/Clawic/data/teacher/classes/<class-id>.md` | Its own file from the first roster — read whole before planning for that group |
| Explanations, analogies and worked examples that landed, by topic | `## Explanations That Landed` in `memory.md`; `~/Clawic/data/teacher/explanations.md` once it outgrows the section | One entry per topic |
| Recurring wrong answers and the question that catches each one | `## Misconceptions` in `memory.md`; `~/Clawic/data/teacher/misconceptions.md` once it outgrows the section | One entry per misconception |
| A project or dissertation supervision meeting: date, supervisee, what was agreed, next milestone | `## Supervisions` in `memory.md`; `~/Clawic/data/teacher/supervisions.md` once it outgrows the section | One dated entry per meeting, grouped by supervisee |
| What was assessed, the score distribution, and item analysis | `~/Clawic/data/teacher/assessments/<year>.md` | Append-only, cut by year |
| Things you produced that get re-read — lesson and unit plans that worked, a syllabus, a rubric, a comment bank, a marking scheme, a routines and behaviour plan, a workshop run sheet, an assessment blueprint, a decision with its reasoning | `~/Clawic/data/teacher/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| Guardians, colleagues, mentors, department heads — adults you contact again | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, every skill in one address book |
| A course build, redesign, or department initiative that runs over weeks | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project |
| **Anything durable this table does not name** | `~/Clawic/data/teacher/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |
| A safeguarding disclosure, or anything a child said about being harmed | Nowhere under `~/Clawic/data/` | Goes to the designated safeguarding lead through the school's channel, today — see Confidential, Not A Credential |

Deciding where something unnamed goes, in this order: (1) would another skill want to read it — a person you contact again, a multi-week project? Then the shared box, not here. (2) Is it a text read whole when its subject comes up — a plan, a rubric, a policy, a decision with its reasoning? Then `artifacts/`, its own file from the first one. (3) Is it one more row of something that accumulates? Then a section of `memory.md` until the split threshold.

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A class or cohort was taken on, or its roster changed | `classes/<class-id>.md` |
| A student's accommodation, access arrangement or support plan became known | The `## Needs` table in that class file — the adjustment, never a diagnosis you are not qualified to make |
| A lesson ran ahead of or behind the plan | `## Pacing` in that class file, with the date and what was cut |
| A lesson, unit, or workshop plan actually worked | `artifacts/`, with the timings that held and the part that did not |
| A syllabus, scope-and-sequence, rubric, marking scheme, comment bank, or blueprint was produced | `artifacts/` |
| An explanation, analogy or worked example finally landed | `## Explanations That Landed` |
| A wrong answer recurred, or a hinge question exposed a shared misconception | `## Misconceptions`, with the question that catches it |
| A supervision or dissertation meeting happened | A dated entry in `## Supervisions`: supervisee, what was agreed, what they will submit, plus the next milestone as a `## Due` row |
| An assessment was set and marked | A row in `assessments/<year>.md`: distribution, the items that failed, what gets retaught |
| An intervention started for a struggling student | That student's line in the class file, plus a review date in `## Due` |
| A guardian, colleague or mentor conversation happened | The person in shared `contacts/contacts.md`; what was agreed in the class file |
| Something about the room, timetable, platform or policy cost effort to find out | `## Environment` |
| An observation, appraisal or peer feedback produced an improvement target | `## Practice Goals`, with its review date in `## Due` |
| A behaviour approach worked or failed with a specific group | `## What Works With This Group` |
| A recurring commitment was scheduled or run — marking turnaround, report cycle, contact cadence, coverage audit, seating rotation | `## Due` |
| The user declared a preference | Its key in `config.yaml` |

## Start flat, split only when it hurts

Everything except class files, artifacts, assessment records and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/teacher/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite. `## Explanations That Landed` and `## Misconceptions` keep their exact headings inside `explanations.md` and `misconceptions.md`.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Class files, artifacts and assessment records are the exception: a roster, a rubric, a run sheet or an exam post-mortem is born as its own file whatever its size, because each is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. A pasted LMS export, gradebook link, integration snippet or configuration file is the densest source of secrets there is: strip each value **before** writing and leave its pointer in place, in this shape: `<kind>:<locator>`.

`env:CANVAS_API_TOKEN` · `keychain:school-sis` · `1password:School/Gradebook` · `bitwarden:Work/LMS` · `vault:secret/school/lms` · `file:~/.config/lms/token`

In a text, the pointer goes where the value was: `api_token: <env:CANVAS_API_TOKEN>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: course and section codes, class ids, room numbers, period and timetable slots, standard and objective codes, rubric criteria, assignment names and due dates, score distributions, item numbers, LMS course URLs, textbook and edition names, exam board specification codes.

**Secrets, strip them**: LMS, SIS and gradebook passwords or API tokens, shared staff logins, proctoring and exam-portal credentials, question-bank licence keys, the answer key of a live exam, unpublished exam papers, and any student or guardian password.

### Confidential, not a credential

Some things are not secrets and still do not belong in a plain text folder on a laptop. Hold this line separately from the pointer rule:

- **A disclosure of harm — abuse, neglect, self-harm, a threat — is never written here.** It goes to the school's designated safeguarding lead through the school's channel, the same day, in the school's system. Reporting duties in most jurisdictions are personal and non-delegable, and a copy in a private file is both a data-protection breach and a reason a case is later thrown out.
- **Medical diagnoses, protected characteristics, immigration status, family circumstances and counselling content** stay out. What belongs in the class file is the *adjustment* and its trigger: "extra time 25%, exam access arrangement on file", "seat away from the window, sound sensitivity", not the condition behind it.
- **Identify students by `student_naming`** (default `first-initial`: `Maya R.`). Never a full home address, phone number, national or student identity number, date of birth, or photograph.
- If the user pastes a roster export carrying those fields, drop the columns before writing and say in one line which ones you dropped.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [classes/](#classes) · [artifacts/](#artifacts) · [assessments/](#assessments) · [shared contacts](#shared-contacts) · [shared projects](#shared-projects) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/teacher/` if it does not exist.

```yaml
stage: high
subjects: [chemistry, physics]
class_size: 28
session_length_min: 50
grade_scale: 1-9
standards: AQA GCSE Chemistry 8462
lms: google-classroom
teaching_mode: in-person
ai_policy: limited
grading_turnaround_days: 7
plan_format: school-template
plan_template: lesson-plan-template.md
student_naming: first-initial

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
conventions:
  rubric_levels: 4
  objective_stem: "Students will be able to…"
constraints:
  no_homework_policy: true
  phones: collected-at-door
cadence:
  report_cycle: half-term
  guardian_contact: fortnightly-for-at-risk
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Teacher Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Year 10 Chemistry, 29 students → `classes/y10-chem.md`; read before planning or marking anything for that group
- Year 12 Physics, 18 students → `classes/y12-phys.md`; read before planning or marking anything for that group
- Bonding unit plan that held its timings → `artifacts/unit-bonding-y10.md`; read when reteaching or rebuilding that unit
- Practical-write-up rubric, 4 levels, normed → `artifacts/rubric-practical-writeup.md`; read before marking any practical write-up
- Assessments and item analysis 2026 → `assessments/2026.md`; read before setting a paper on a topic already tested

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Return Y10 mocks | within 7 days of sitting | 2026-06-19 | 2026-06-26 |
| Guardian contact, at-risk list | fortnight | 2026-07-10 | 2026-07-24 |
| Standards coverage audit vs scheme of work | half-term | 2026-05-29 | 2026-07-17 |
| Seating and group rotation | half-term | 2026-05-29 | 2026-07-17 |
| Observation improvement target review | 6 weeks | 2026-06-15 | 2026-07-27 |

## Teaching Context
State school, England. Four classes, 22 contact periods a week, 50-minute lessons, one shared lab.

## Environment
Lab benches fixed in rows of four — no circle discussion without moving to R12. Projector loses HDMI after standby; arrive early. Google Classroom is the only channel guardians read.

## What Works With This Group
Y10 Chem: mini-whiteboards get 100% response; hands-up gets four volunteers out of 29. Starter must be on the board before they enter or the first five minutes are lost.

## Explanations That Landed
| Topic | What worked | Why it worked |
|---|---|---|
| Ionic vs covalent | Transfer versus sharing, drawn as two hands passing a coin, then holding one together | Makes the electron count visible before any dot-and-cross diagram |

## Misconceptions
| Topic | The wrong answer | Catch it with |
|---|---|---|
| Conservation of mass | "Mass is lost when a candle burns" | Sealed-flask hinge question with a distractor that says mass decreases |

## Practice Goals
Observation 2026-06-15: questioning reaches the same six students. Target: whole-class response in every check for four weeks. Review 2026-07-27.

## Pain Points
March: 11 hours of marking in one week after setting full essays for four classes in the same fortnight. Assessment calendar now staggered.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next term:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Every recurring thing this skill schedules belongs here, including the marking turnaround clock started by `grading_turnaround_days`.
- **`## What Works With This Group`** is per group and stays short: the technique, the group, the observed effect. A technique that worked with one class and failed with another is two entries, not a contradiction.
- **`## Supervisions`** exists only for whoever supervises projects, dissertations or theses. One dated line per meeting, newest last, never edited afterwards — `2026-03-04 · Maya R. · agreed: method chapter by 03-25, pilot data reviewed, two drafts remaining` — with the milestone date going in `## Due`. Write it the same day: if supervision is ever disputed, this dated sequence is the whole evidence base, and a line written three weeks later is worth much less than one written that afternoon.
- **`## Explanations That Landed`**, **`## Misconceptions`** and **`## Supervisions`** are the sections that grow fastest; they keep these exact headings when they split out.

| Status | Meaning |
|-------|---------|
| `ongoing` | Still learning their groups, timetable and constraints |
| `complete` | Groups, constraints and marking rhythm are known |

## classes/

One file per class, cohort or section, at `~/Clawic/data/teacher/classes/<class-id>.md`, created the first time there is a roster. `<class-id>` is what the teacher calls the group in speech, in kebab case: `y10-chem`, `cs101-fall26`, `onboarding-cohort-7`. Never a date-based name — the same group is taught for a year.

```markdown
# Year 10 Chemistry — 29 students
*Read before planning, grouping or marking anything for this group. Started 2025-09-03.*

## Roster
| Student | Strength | Watch | Grouping note |
|---|---|---|---|
| Maya R. | Fast on calculation | Skips units under time pressure | Pairs well with Tom B.; not with Alex D. |

## Needs
| Student | Adjustment | Trigger / when it applies | On file |
|---|---|---|---|
| Sam K. | 25% extra time, separate room | All timed assessments | Yes, access arrangement |
| Iris P. | Printed copy of slides, off-white paper | Every lesson | Yes |

## Dynamics
Two off-task pairs when seated together. Whole class settles on a written starter, not a verbal one.

## Seating
Current plan and the reason for it, with the date it was last rotated.

## Pacing
| Week | Planned | Actually taught | Cut or carried |
|---|---|---|---|
| 12 | Bonding 1-3 | Bonding 1-2 | Metallic bonding carried to week 13 |

## Interventions
| Student | Concern | Started | What was tried | Review |
|---|---|---|---|---|
| Alex D. | 14 of 60 sessions missed | 2026-05-06 | Seat change, guardian call, catch-up sheet weekly | 2026-07-24 |
```

- **`## Needs` records the adjustment, never the diagnosis.** "Extra time 25%, access arrangement on file" — not the condition, not the report text, not counselling content.
- Identify students by `student_naming`; the default is first name plus last initial.
- **Retirement is part of the record.** When a class ends, add `status: finished — <date>` at the top and keep the file: next year's version of the same course is planned from it. Delete the roster and needs tables at that point and keep pacing, dynamics and what worked — the students have left, the course has not.
- A guardian who is contacted more than once is a person: they go in shared `contacts/contacts.md`, and here only their student's name links them.

## artifacts/

One file per thing, at `~/Clawic/data/teacher/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **lesson plan**, **unit plan**, **syllabus or scheme of work**, **rubric**, **marking scheme**, **comment bank**, **assessment blueprint**, **routines and behaviour plan**, **workshop run sheet**, **decision with its reasoning**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Rubric — practical write-up (4 levels)
*Read before marking any practical write-up, and before setting one. Normed on 5 anchor scripts 2026-03-04.*

Criteria, level descriptors, and the anchor script that defines each boundary...
```

```markdown
# Unit plan — bonding, Year 10, 9 lessons
*Read when reteaching or rebuilding this unit. Timings verified in delivery 2026-02.*

Objectives with their hinge questions · lesson sequence · prerequisites tested in lesson 0 ·
where it ran late (lesson 4, dot-and-cross took a full period) · the practice set that worked ·
the misconception that appears every year and the question that catches it.
```

```markdown
# Decision — no summative grades on drafts
*Read before designing any writing assessment. 2026-04-11.*

Decision: drafts get comment-only, grades appear on the final piece.
Because: grade plus comment suppresses attention to the comment (Butler 1988), observed twice here.
Rejected: grade with hidden comment reveal — the LMS shows the grade first anyway.
Cost: one extra marking pass per piece, absorbed by cutting the mid-unit quiz.
```

A plan or rubric that was reused is worth more than one that was written well: when an artifact is reused, add one line saying when and what changed. That line is what makes next year's version a five-minute edit.

If the work is tracked as a multi-week project — a new course, a redesign, an accreditation cycle — the decision summary also belongs in shared `~/Clawic/data/projects/<project>.md`, with the full artifact staying here and referenced by name.

## assessments/

```markdown
# Assessments — 2026

| Date | Class | What | Max | Mean | Median | Below pass | Blueprint |
|------|-------|------|-----|------|--------|-----------|-----------|
| 2026-06-19 | y10-chem | Mock paper 1 | 60 | 38 | 40 | 6 of 29 | artifacts/blueprint-y10-p1.md |

## Item Analysis
| Date | Item | Topic | p (proportion correct) | D (discrimination) | Verdict |
|------|------|-------|------------------------|--------------------|---------|
| 2026-06-19 | Q7 | Moles from mass | 0.31 | 0.11 | Reteach: distractor B matched a real misconception, and the item does not discriminate |
| 2026-06-19 | Q12 | Ionic bonding | 0.92 | 0.05 | Too easy — keep as a warm-up, drop from the next paper |

## Retaught
| Date | Topic | Trigger | Result on recheck |
|------|-------|---------|-------------------|
| 2026-06-26 | Moles from mass | Q7 at p=0.31 | Recheck p=0.74 |
```

- One row per assessment, one block per year. Scores are aggregates; a per-student mark belongs in the school's gradebook, which is the system of record, not here.
- `p` and `D` are defined in `assessment.md`; record them for any item you intend to reuse, because reusing an item with negative `D` puts a broken question back in front of students.
- Corporate and workshop evaluations use the same file: the Kirkpatrick level measured, when, and the number.

## Shared contacts

Lives at `~/Clawic/data/contacts/contacts.md` and is shared with every other skill that deals with people — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Contacts

| Name | Key | Role | Preferred channel | Context | Last contact | File |
|------|-----|------|-------------------|---------|--------------|------|
| Dana Reyes | dana.reyes@example.org | Guardian of Maya R. | email | Prefers written summaries; works nights | 2026-06-12 | — |
| Priya Nair | priya.nair@example.org | Head of science, line manager | in person | Runs the observation cycle | 2026-06-15 | — |
```

- **Identity is `Key`**: the email address in lower case, else a handle, else `<kebab-name>` plus a stable disambiguator. The key is a column of the row, never implicit and never delegated to a per-person file. `Preferred channel` is the *type* of channel, not the address, so it cannot serve as a key.
- **Read the file before adding.** If the key is already there, update that row in place; only its absence justifies a new row. Update and retire your own rows; never rewrite a row another skill wrote.
- **Scale cut**: one row per person while there are ≤15. Past that, one file per person at `~/Clawic/data/contacts/<name>.md` with the same fields, and `contacts.md` becomes the index carrying the `File` pointer. If the folder already looks like that when you arrive, follow it — never start a parallel `contacts.md`.
- **Foreign columns win.** If `contacts.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- **Who goes in**: adults you will contact again — guardians, colleagues, line managers, mentors, external examiners, workshop clients. **Who does not**: students. A roster of thirty minors would swamp a shared address book and puts children's data in a file every other skill reads; students live in their class file, and the guardian's row names the student by the same `student_naming` form.
- Retirement: when a guardian relationship ends with the school year, delete the row and note the date in `memory.md`. An address book that only grows stops being one.
- No phone numbers or addresses of minors, ever. Contact references are pointers, never credentials.

## Shared projects

Lives at `~/Clawic/data/projects/<project>.md`, one file per project, shared with every planning and delivery skill.

```markdown
# Project — GCSE chemistry scheme rewrite
status: active
owner: us
objective: Rebuild the two-year scheme against the 2026 specification
milestones:
- 2026-08-20 unit map approved
- 2026-09-30 first term's resources built
decisions:
- Practical write-up rubric shared across the department (artifacts/rubric-practical-writeup.md)
```

- Identity is the project name, which is the file name. Read before creating: a project already there gets updated, never duplicated.
- Retirement is `status: done | cancelled — <date>` inside the file; never delete it, it is the record of what was delivered. Past roughly 20 closed projects, move them to `projects/archive/<project>.md` without renaming.
- Use it only for work that runs over weeks and has milestones. A single lesson, a single exam, a single unit is an artifact here, not a project.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`explanations.md` — `## Explanations That Landed`, one row per topic. This file is the reason a second attempt at a hard topic takes ten minutes instead of an hour, and it is the single most reused thing a teacher accumulates.

`misconceptions.md` — `## Misconceptions`, one row per misconception with the question that catches it. Grouped by topic once it passes ~30 rows, so it can be read before planning rather than after marking.

`supervisions.md` — `## Supervisions`, one dated entry per meeting, grouped under a `### <supervisee>` sub-heading once more than one project runs at a time. Read the supervisee's entries before their next meeting: the first question is always what was agreed last time.
