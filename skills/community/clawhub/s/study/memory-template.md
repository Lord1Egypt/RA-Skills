# Working File Templates — Study

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — Configuration table keys and preference areas alike | `~/Clawic/data/study/config.yaml` | Key by key, read-modify-write |
| Courses, topic states, decks, marks, materials, technique verdicts, due dates, box index | `~/Clawic/data/study/memory.md` | Rewritten in place; stays small |
| Every missed question with its cause | `~/Clawic/data/study/errors.md` | Its own file from the first entry — one practice paper adds 15 rows |
| Study blocks: what was retrieved, how long, how it went | `~/Clawic/data/study/session-log/<year>-<month>.md` | Append-only, cut by month |
| Things produced that get re-read — formula sheet, summary one-pager, essay skeleton, past-paper frequency table, memory-palace layout, lab checklist, a timetable that held, an exam post-mortem, a thesis outline | `~/Clawic/data/study/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| Professors, tutors, TAs, study partners | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, every skill's contacts in one file |
| A thesis, capstone, or graded group project | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project, from the first |
| A proctored exam appointment that has a confirmation code | `~/Clawic/data/bookings/<year>.md` (**shared**) | One row per booking, by date |
| **Anything durable this table does not name** | `~/Clawic/data/study/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

Deciding where something unnamed goes, in this order: (1) would another skill want to read it — a person, a project, a booking, a health fact? Then it belongs in the shared box, not here. (2) Is it a text read whole when its subject comes up — a procedure, a sheet, a plan, a decision with its reasoning? Then `artifacts/`, its own file from the first one. (3) Is it one more row of something that accumulates? Then a section of `memory.md` until the split threshold.

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A course was added, or its exam date, weights, hurdles or format became known | `## Courses` |
| A topic moved state — `seen`, `recalled once`, `relearned ×n`, `exam-ready` (SKILL.md Rule 3) | `## Topics` |
| A study block ran | A row in `session-log/<year>-<month>.md` |
| Anything was missed — a question, a card, a step in a procedure | A row in `errors.md`, with its cause (SKILL.md Rule 6) |
| A mark came back, or a target was recomputed | `## Results` |
| A deck was created, split, suspended, or retired | `## Decks` |
| A leech was triaged — rewritten, split, suspended or deleted | `### Leech Log`, under `## Decks` |
| A source was adopted, finished, or abandoned as useless | `## Materials` |
| A technique visibly worked or visibly failed for this student | `## What Works`, with the date and what it was tried on |
| A recurring failure has a name now — blanking, sign errors, running out of time | `## Pain Points`; the second occurrence earns a drill in `artifacts/` |
| A formula sheet, summary, outline, frequency table or post-mortem was produced | `artifacts/` |
| A professor, tutor, TA or study partner was named | `contacts.md` (shared) |
| A thesis, capstone or graded group project started or moved | `projects/<project>.md` (shared) |
| A proctored exam was booked, moved, or sat | `bookings/<year>.md` (shared) |
| A review cadence, weekly review, or simulation was scheduled or run | `## Due` |
| The user declared a preference | Its key in `config.yaml` |

## Start flat, split only when it hurts

Everything except artifacts, the error log, the session log and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/study/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Three exceptions are born as their own file whatever their size: **artifacts** (read whole, only when their subject comes up), the **session log** (a dated stream that would swamp anything it shared a file with), and **`errors.md`** (one practice paper produces fifteen rows in a sitting, so it crosses the threshold on day one and is read by topic rather than by date).

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. A pasted portal page, deck export, exam registration email or shared drive link is where they arrive: strip each value **before** writing and leave its pointer in place, in this shape: `<kind>:<locator>`.

`keychain:university-portal` · `env:ANKI_SYNC_KEY` · `1password:School/Portal` · `bitwarden:School/LMS` · `file:~/.ssh/id_ed25519` · `profile:campus-vpn`

In a text, the pointer goes where the value was: `portal password: <keychain:university-portal>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: course codes and names, module and unit numbers, exam dates and times, room and venue names, assessment weights, marks and grades, topic and chapter names, deck and note names, textbook titles and ISBNs, professor and tutor names, test-centre names, exam confirmation codes, student cohort and year.

**Secrets, strip them**: portal and LMS passwords, SRS sync keys and API tokens, exam-proctor login codes and one-time passcodes, library and VPN credentials, shared-drive links that grant access by URL, the student's national ID or full ID-document number, payment card details for exam fees, anything from an exam paper under embargo.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [errors.md](#errorsmd) · [session-log/](#session-log) · [artifacts/](#artifacts) · [shared contacts](#shared-contacts) · [shared projects](#shared-projects) · [shared bookings](#shared-bookings) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/study/` if it does not exist.

```yaml
level: undergraduate
weekly_hours: 14
session_minutes: 50
break_minutes: 10
daily_review_cap: 25
srs_app: anki
integrity_mode: scaffold
grading_scale: uk-class
interleaving: on
review_day: Sunday

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
platform:
  institution_rules: "AI permitted for study, prohibited in submitted text"
  deadline_timezone: Europe/Madrid
work_order:
  best_hours: "07:00-10:00"
  hardest_first: true
constraints:
  accommodation: "25% extra time, granted for all written exams"
  unavailable: "Tue and Thu 14:00-20:00, work shift"
cadence:
  review_time: "08:00"
  past_paper_simulation: fortnightly
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Study Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Missed questions and their causes (58) → `errors.md`; read before planning any session, review or exam sprint
- Study blocks, July 2026 → `session-log/2026-07.md`; read when checking load, streaks or where the hours went
- Stats formula sheet → `artifacts/formula-sheet-stats.md`; read before any stats problem set or exam
- Past-paper frequency, Stats 2021-2025 → `artifacts/past-papers-stats.md`; read when choosing what to cut
- Pharmacology post-mortem (failed resit) → `artifacts/post-mortem-pharm.md`; read before planning pharmacology again

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Spaced review queue | day | 2026-07-25 | 2026-07-26 |
| Weekly review: plan vs actual, re-rank by weight × gap | week, Sunday | 2026-07-19 | 2026-07-26 |
| Timed past paper, one course | fortnight | 2026-07-12 | 2026-07-26 |
| Deck leech sweep | month | 2026-07-01 | 2026-08-01 |

## Courses
| Course | Code | Format | Exam date | Weight of exam | Hurdles | Notes |
|---|---|---|---|---|---|---|
| Statistics | STA201 | 3h written, 60% MCQ + 40% long | 2026-09-08 | 70% | must pass exam to pass course | calculator allowed, no formula sheet given |
| Pharmacology | PHA310 | MCQ, negative marking 1/3 | 2026-09-15 | 100% | — | resit; first attempt 41% |
| Research methods | RES200 | coursework only | — | 0% | lab attendance 80% | dissertation feeds this |

## Topics
| Topic | Course | State | Last retrieved | Next review | Source |
|---|---|---|---|---|---|
| Hypothesis testing | STA201 | relearned ×2 | 2026-07-24 | 2026-08-01 | ch. 8 + 2023 paper Q3 |
| Bayes / conditional | STA201 | recalled once | 2026-07-22 | 2026-07-27 | ch. 6 |
| Beta blockers | PHA310 | seen | — | 2026-07-27 | lecture 11 |
| ANOVA | STA201 | exam-ready | 2026-07-20 | 2026-08-10 | ch. 11 |

## Decks
| Deck | App | Cards | New/day | Reviews/day | Last triage | Notes |
|---|---|---|---|---|---|---|
| PHA310::drug-class | anki | 420 | 15 | ~150 | 2026-07-01 | 9 leeches suspended, all mechanism cards |
| STA201::definitions | anki | 90 | 5 | ~40 | 2026-06-20 | formulas removed — derivable, practiced as problems |

### Leech Log
| Date | Deck | Card | Why it failed | What replaced it |
|------|------|------|---------------|------------------|
| 2026-07-01 | PHA310::drug-class | "Mechanism of carvedilol?" | compound — three receptor actions in one answer | three atomic cards, one per receptor |
| 2026-07-01 | PHA310::drug-class | "Which beta blocker is cardioselective?" | ambiguous front, four defensible answers | discriminator card: metoprolol vs propranolol |

## Results
| Assessment | Course | Date | Mark | Weight | Running | Notes |
|---|---|---|---|---|---|---|
| Midterm | STA201 | 2026-05-12 | 64% | 20% | — | lost 11 marks to time, not knowledge |
| Lab report 2 | RES200 | 2026-06-02 | 71% | 15% | — | rubric criterion 3 was the gap |

Target 65% overall in STA201: needs 65.3% average on the remaining 80%.

## Materials
| Source | Course | Type | Coverage | Status | Verdict |
|---|---|---|---|---|---|
| Freedman, Statistics 4e | STA201 | textbook | ch. 1-14 = whole syllabus | primary | worked examples are the best part |
| Lecture recordings | STA201 | video | all | secondary | watch at 1.5×, skeleton notes only |
| Katzung summary tables | PHA310 | reference | drug classes | primary | table format matches the exam's asks |
| Random YouTube course | PHA310 | video | partial | abandoned | 2026-06: three hours, no retrievals, dropped |

## What Works
| Tried | On | Verdict | Date |
|---|---|---|---|
| Blank-page recall before rereading | STA201 chapters | works — gap list every time | 2026-06-14 |
| Mind maps as the study act | PHA310 | failed twice; useful only as an end-of-topic index | 2026-05-30 |
| 90-minute blocks | problem sets | works for problems, not for reading | 2026-07-05 |

## Pain Points
Runs out of time on long-answer questions: 2026-05 midterm and both 2024 past papers. Cause is fluency, not knowledge (see `errors.md`).
Blanks on the first question of any timed paper; recovers by question 3. Park-and-return now built into the protocol.

## How They Work
Works Tue/Thu, studies mornings. Wants the question, not the explanation. Will not use paper cards. Reads rubrics only when told to.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Every recurring thing this skill schedules belongs here, and the cadences come from `cadence` in `config.yaml` when the user has declared them.
- **`## Courses`**: `Hurdles` is the field that decides plans — a minimum component mark or an attendance floor outranks every weight (SKILL.md, Deadlines And Grade Math). `Format` records what the assessment physically is, because Rule 5 practices in that format.
- **`## Topics`**: `State` is one of `seen`, `recalled once`, `relearned ×n`, `exam-ready` (Rule 3), never a percentage. `Next review` comes from the Rule 2 gap and never falls after the exam date. A topic with `Last retrieved` older than its `Next review` is overdue and gets said out loud.
- **`## Results`**: marks carry their scale (`64%`, `2:1`, `3.4/4`), because `grading_scale` can change and a bare number stops meaning anything. Recompute the target line whenever a mark lands; keep one target line per course, overwritten, never a second.
- **`## Decks`**: `Reviews/day` is the observed steady state, not the setting. Deck content lives in the SRS app — this table is the registry, and duplicating cards here is how the two go out of sync. `### Leech Log` sits under it and takes one row per triaged leech (`flashcards.md`); without it the same card is rescued and re-broken every term. Both move together when the section splits, and the log becomes `## Leech Log` in `decks.md`.
- **`## Materials`**: an abandoned source keeps its row with the verdict and the date. Deleting it is how the same useless video gets recommended again in October.
- **`## What Works`**: technique verdicts with the date and what they were tried on. This is the section that stops a student re-trying the same failed method every term; it outranks the defaults in `SKILL.md` for this student.
- These headings are exactly the ones `courses.md`, `topics.md`, `results.md`, `materials.md` and `decks.md` get when their sections outgrow this file, so each split stays a copy-paste.

| Status | Meaning |
|-------|---------|
| `ongoing` | Still learning their courses, level and habits |
| `complete` | Know their term, their formats and what works for them |

## errors.md

The most valuable file this skill produces, and the one it reads before planning anything (SKILL.md Rule 6). One row per miss, classified once.

```markdown
# Missed Questions

| Date | Course | Topic | Source | What was missed | Cause | Retried | Result |
|------|--------|-------|--------|-----------------|-------|---------|--------|
| 2026-07-24 | STA201 | hypothesis testing | 2023 paper Q3 | picked one-tailed for a two-tailed prompt | misread | 2026-07-26 | correct |
| 2026-07-24 | STA201 | CI for proportions | 2023 paper Q7 | blank | never encoded | — | — |
| 2026-07-22 | PHA310 | beta blockers | deck | recalled the alpha-blocker mechanism | interference | 2026-07-25 | correct |
```

- **`Cause` is one of five**, never a free-text apology: `never encoded` · `not retrievable` · `procedure slip` · `misread` · `out of time`. Interference is recorded as `not retrievable` with the confused item named in `What was missed` — the pair is the thing to drill.
- Only `never encoded` and `not retrievable` earn restudy. The other three earn drills: timing, checking routine, question parsing.
- **`Retried` and `Result` are the point of the file.** A miss with no retry date is an open loop; a topic with two same-cause rows inside two weeks opens the next session (Rule 6).
- **Scale cut**: one file while there are ≤60 rows. Past that, one file per course at `~/Clawic/data/study/errors/<course>.md` with the same columns, and `errors.md` becomes the index (`Course | Rows | Open loops | → file`). If you arrive and the folder already looks like that, follow it.
- Never delete a resolved row inside the current term: the pattern across a term is what names the pain point.

## session-log/

One file per month, append-only. This is where "am I actually doing the hours" gets answered without anyone estimating.

```markdown
# Study Sessions — 2026-07

| Date | Course | Minutes | What was retrieved (not read) | Misses | Notes |
|------|--------|---------|-------------------------------|--------|-------|
| 2026-07-24 | STA201 | 95 | 2023 paper, timed, sections A-B | 6 → errors.md | ran 12 min over on Q3 |
| 2026-07-25 | PHA310 | 30 | deck review, 148 cards | 4 → errors.md | queue back under cap |
```

- **`What was retrieved` never says "read chapter 8".** If the row cannot name a retrieval, the block was reading, and saying so plainly is the point of the log.
- Minutes are actual, not planned. The gap between `weekly_hours` and the monthly total is the input to the next weekly review.
- Roll up nothing into `memory.md`. The weekly review reads this file; `memory.md` keeps only its `## Boxes` line.

## artifacts/

One file per thing, at `~/Clawic/data/study/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **formula or fact sheet**, **summary one-pager for a topic**, **essay or answer skeleton**, **past-paper frequency table**, **memory-palace or mnemonic set**, **lab or procedure checklist**, **a revision timetable that actually held**, **an exam post-mortem**, **a thesis outline**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Formula sheet — Statistics
*Read before any stats problem set or exam. Built from memory 2026-07-20, checked against ch. 6-11.*

...formulas, each with the one condition that decides whether it applies...
```

```markdown
# Past-paper frequency — Stats 2021-2025
*Read when deciding what to cut from the plan. Built 2026-07-18 from five papers.*

| Topic | Appeared | Average marks | Last seen |
...
Cut list this term, in order, and why.
```

```markdown
# Post-mortem — Pharmacology, 41%
*Read before planning pharmacology again. Written 2026-06-30.*

What the marks actually went on: ...
Cause distribution from errors.md: never encoded 4, out of time 11.
What changes: timed drills at 55 s/question from week 1; cards written after understanding, not before.
```

A sheet or skeleton is built **by the student from memory** and then checked against the source (Rule 8) — an artifact you wrote for them is a handout, and handouts do not get retrieved.

If the artifact belongs to a tracked project (a thesis chapter plan, a capstone decision), its one-line summary also goes in the shared `~/Clawic/data/projects/<project>.md`, with the full text staying here and referenced by name.

## Shared contacts

Lives at `~/Clawic/data/contacts/contacts.md` and is shared with every other skill that knows a person — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Contacts

| Name | Key | Role | Preferred channel | Context | Last contact | File |
|------|-----|------|-------------------|---------|--------------|------|
| Ana Ruiz | a.ruiz@uni.example | STA201 lecturer | email | office hours Wed 15:00; sets the exam | 2026-07-10 | — |
| Marco Feld | marco-feld | study partner, PHA310 | messaging | quizzes drug classes, reliable | 2026-07-24 | — |
```

- **Identity is `Key`**, and it is a column of the row, never implicit: email in lowercase, else a handle, else `<kebab-name>` plus a stable disambiguator (`ana-ruiz-sta201`). Read the file before adding and search for the key. If it is there, **update that row in place** — never append a second row for the same person.
- **Only your own rows.** A row written by another skill is updated only in the fields you own (`Context`, `Last contact`); never rewrite someone else's `Role` or delete their row.
- **Leaving is part of the record.** When a tutor or partner stops being one, update `Role` and `Context` with the date rather than deleting the person — the same name comes back next term.
- **Scale cut**: one row per person while there are ≤15, or until one person no longer fits a row. Past that, one file per person at `~/Clawic/data/contacts/<name>.md` and `contacts.md` becomes the index with the `File` pointer. If the folder already looks like that, follow it — do not start a parallel `contacts.md`.
- **Foreign columns win.** If `contacts.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- Never a password, a portal login, or a home address here. Channel type, not credentials.

## Shared projects

Lives at `~/Clawic/data/projects/<project>.md`, one file per project from the first, shared with every other skill that tracks work.

```markdown
# Dissertation — sleep and recall in shift workers
status: active
owner: me
supervisor: Ana Ruiz (see contacts)
due: 2027-04-30

## Goal
One sentence.

## Milestones
| What | Due | Status |
|---|---|---|
| Ethics submission | 2026-09-15 | done 2026-09-02 |
| Data collection | 2026-12-01 | in progress |

## Decisions
2026-07-20 — within-subject design, rejected between-subject: n available is 22.
```

- **Identity is the file name** (kebab slug of the project). Read the folder before creating: a project the user already tracks gets updated, never duplicated under a second name.
- **Closing is `status: done | cancelled — <date>` inside the file, never deletion** — the record of what was delivered is the reason the box exists. Past ~20 closed projects, move them to `projects/archive/<project>.md` without renaming.
- The supervisor, client or teammates go in `contacts.md` and are referenced here **by name only**. Duplicating the person is how two skills end up disagreeing about who they are.
- Study-specific detail (topic states, misses, reading) stays in the study box; this file carries the goal, the milestones and the decisions.

## Shared bookings

Lives at `~/Clawic/data/bookings/<year>.md` and holds anything with a date and a confirmation code, from any skill. Only booked, proctored exam appointments belong here from this skill — an exam date printed on a syllabus is a `## Courses` field, not a booking.

```markdown
# Bookings — 2026

| Date | Type | Locator | Provider | Details | Status | Cost |
|------|------|---------|----------|---------|--------|------|
| 2026-09-15 09:00 | exam | 7XK2M4 | Pearson VUE, Madrid Norte | PHA310 resit, 3h, ID required | confirmed | 220 EUR |
```

- **Identity is the locator.** Read the file before adding; if the locator is there, update the row in place.
- **A cancelled or rescheduled booking keeps its row** with `status: cancelled` or `rescheduled → <new locator>` and the refund if there was one. A booking history that only shows what happened cannot answer "did we get that money back".
- **Amounts carry their currency in the value** (`220 EUR`), because rows from travel and other skills are in other currencies and someone will add the column up. An estimate carries the date it was estimated.
- **Scale cut**: past ~60 rows in one year, split by quarter into `bookings/<year>-q<n>.md` and leave `<year>.md` as the index (`Date | Type | Locator | → file`).
- **Foreign columns win**: match the header that is already there and add anything missing as a trailing note.
- The confirmation code is not a secret and stays; the account password used to book it is, and never appears.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`courses.md` — `## Courses`, one `## <term>` heading above it once more than one term is tracked. This is the file that answers "what am I actually enrolled in and what does each one need" without opening a portal.

`topics.md` — `## Topics`, grouped by `## <course>` when more than one course is in flight. The file grows fastest of all of them: a single syllabus is 20-40 rows, so expect this split in the first fortnight.

`results.md` — `## Results` plus the running-target line per course. Keeping the whole term's marks together is what makes the Deadlines And Grade Math arithmetic reliable instead of remembered.

`materials.md` — `## Materials`, including the abandoned rows with their verdicts.

`decks.md` — `## Decks`, plus `## Leech Log` — the same table that lived as `### Leech Log` under `## Decks`, promoted one level and keeping its five columns (date, deck, card, why it failed, what replaced it). The leech log is the reason this file exists: a card that has failed eight times is a card written wrong, and the fix is a rewrite, not another review.
