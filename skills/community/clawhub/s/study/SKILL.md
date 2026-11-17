---
name: Study
slug: study
version: 1.0.3
description: 'Runs a student''s whole term: course load, weekly plan, lectures, notes, retrieval practice, coursework deadlines, grades, and exams. Use when a syllabus, reading list, or semester has to become a weekly schedule; when an exam, midterm, final, viva, or professional certification sits on a date; when revision is not sticking, rereading has replaced recall, or a topic will not stay in memory; when review intervals, decks, or a past-paper plan need designing; when assignments, problem sets, lab reports, essays, or a thesis stack up against deadlines; when several courses compete for the same hours; when procrastination, cramming, or a missed week has to be recovered; when a bad mark needs a post-mortem; or when the question is what to study first and for how long. Covers note systems, study groups, tutors, open-book and adaptive tests, and exam-day tactics. Not for teaching a concept on the spot (`learning`), self-teaching with no course or exam (`learn`), or authoring decks (`anki`).'
homepage: https://clawic.com/skills/study
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 📚
    os:
    - linux
    - darwin
    - win32
    displayName: Study
    configPaths:
    - ~/Clawic/data/study/
    - ~/Clawic/data/contacts/
    - ~/Clawic/data/projects/
    - ~/Clawic/data/bookings/
    - ~/Clawic/profile.yaml
  openclaw:
    requires:
      config:
      - ~/Clawic/data/study/
      - ~/Clawic/data/contacts/
      - ~/Clawic/data/projects/
      - ~/Clawic/data/bookings/
      - ~/Clawic/profile.yaml
---

**Data.** At the start of every session, read `~/Clawic/data/study/config.yaml` (what the user declared) and `~/Clawic/data/study/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — the index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Read `~/Clawic/data/study/errors.md` before planning any session, review, or exam sprint: what this student got wrong is the curriculum (Rule 6). If none of it exists, work from defaults and say nothing about it.

**Write before the session ends** whenever it produced something durable: a course, its exam date or its assessment weights; a topic that moved between `seen`, `recalled once`, `relearned`, `exam-ready`; a study block and what was retrieved in it; every miss and its cause; a mark and what it did to the running grade; a deck created or triaged; a source read or abandoned; a technique that worked or failed for this student; or something they will re-read — a formula sheet, a summary one-pager, an essay skeleton, a past-paper frequency table, a revision timetable that actually held, an exam post-mortem. `memory-template.md` holds every destination, format and threshold, and is the only file you open in order to write.

**People, projects and booked exams go to shared boxes**, not here: professors, tutors, TAs and study partners to `~/Clawic/data/contacts/contacts.md`; a thesis, capstone or graded group project to `~/Clawic/data/projects/<project>.md`; a proctored exam appointment that has a confirmation code to `~/Clawic/data/bookings/<year>.md`. Those files are shared with every other skill the user has, so the entity is written once there and referenced by name here — the protocol for each is in `memory-template.md`.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a file you create, not in text the user pastes in to be saved. Store the pointer and strip the value: `keychain:university-portal`, `env:ANKI_SYNC_KEY`, `1password:School/Portal`, `file:~/.ssh/id_ed25519`. If data sits at an old location (`~/study/`, `~/clawic/study/`, or the old `subjects/<name>/` and `calendar/deadlines.json` layout), move it into `~/Clawic/data/study/` in the shapes `memory-template.md` describes.

Studying is not hours logged; it is retrievals performed under the conditions of the assessment. Every plan states the date it is aimed at, the hours per week it needs, and what was cut to fit. Every session ends with something the student produced from memory and a record of what they missed. Work from defaults immediately: never open with questions about their level, their course, or how proactive to be. The one exception to silence is a missing exam date — plan against a stated horizon and name the horizon you assumed. That is a statement, not a question. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: locale, timezone) → the Configuration table default.

## When To Use

- Turning a syllabus, reading list, or a term with several courses into a weekly plan that fits the hours that exist
- Preparing for a dated assessment: exam, midterm, final, viva, practical, open-book paper, professional certification
- Revision that is not working: forgetting what was studied, rereading without recall, plateaued practice scores, blanking under time
- Running the study block itself — retrieval practice, spaced review, problem sets, decks, reading, note systems
- Coursework under deadline pressure: assignments, problem sets, lab reports, essays, group work, a thesis
- Recovery: procrastination, a missed week, a failed paper, burnout mid-term, a mark that needs a post-mortem
- Mode: advise and act-as coach — this skill plans, quizzes, drills and critiques; it never writes the work that gets submitted (Rule 8). Not for teaching a concept on the spot (`learning`), self-teaching with no course or exam (`learn`), or authoring and repairing decks (`anki`)

## Quick Reference

| Situation | Play | Depth |
|-----------|------|-------|
| A syllabus, several courses, no plan | Backwards from each date: hours needed, hours available, what gets cut (Rule 4) | `planning.md` |
| "I studied for hours and remember nothing" | Hours were reading, not retrieval — convert the next block to closed-book recall | `retrieval.md` |
| "When should I review this?" | Gap ≈ 10-20% of the time to the exam; expand ×2-2.5 on success, reset on a lapse (Rule 2) | `spacing.md` |
| Review queue exploded, days skipped | Debt formula and triage; cap new items until the backlog clears | `spacing.md` |
| Fact-heavy material: vocab, anatomy, dates, statutes | Atomic cards, one fact per card, cloze for context-bound facts | `flashcards.md` |
| Dense textbook or paper that will not go in | Question-first pass, then closed-book recall per section — never highlight-first | `reading.md` |
| Lectures: live, recorded, or a backlog of them | Capture skeleton live, retrieve within 24h, playback speed ceiling | `lectures.md` |
| Notes exist but are never reused | Notes are an index and a question bank, not a transcript | `notes.md` |
| Math, physics, coding: problems keep breaking | Worked example → faded steps → solo solve ×2-3 → interleave | `subjects.md` |
| Conceptual course: theories, mechanisms, models | Closed-book explanation, then compare against the source and mark the gaps | `subjects.md` |
| Essay or writing-based exam course | Timed outlines from memory on predicted questions; build reusable argument blocks | `subjects.md` |
| Language course | Comprehensible input plus production practice; cards only for arbitrary pairings | `subjects.md` |
| Exam in 4+ weeks, or 5 days, or tomorrow | Horizon protocol per remaining time, ending in cram triage that protects sleep | `exams.md` |
| Past papers: how many, how to use, when | Frequency table first, then timed simulation, then error analysis | `exams.md` |
| In the exam: pacing, guessing, blanking, open-book | Marks-per-minute (Rule 7), guess threshold, park-and-return, indexed materials | `exams.md` |
| Certification, licensing, or standardized test while working | Blueprint weights, question banks, scaled scores, adaptive tests, retake rules | `certifications.md` |
| Assignment, lab report, or thesis due | Deliverable-first plan, marking rubric read before writing, integrity boundary | `coursework.md` |
| Which assessment deserves the next hour | Weight × gap ÷ hours (→ Deadlines And Grade Math) | `coursework.md` |
| Cannot start, keeps drifting, burned out | Shrink the entry action; recover the streak; escalation signals | `motivation.md` |
| Study group, tutor, office hours, teaching a peer | Rules that make a group a retrieval session instead of a co-working room | `groups.md` |
| Session length, environment, breaks, what to do when stuck | Block structure, stuck ladder, and the consolidation window | `sessions.md` |
| Anything else about studying | Ask what the assessment looks like, then make the next 20 minutes practice in that format (Rule 5) | — |

Coverage map: `planning.md` term and week plans · `sessions.md` the block itself · `retrieval.md` recall practice · `spacing.md` review scheduling and debt · `flashcards.md` card writing and deck upkeep · `reading.md` textbooks and papers · `lectures.md` live and recorded classes · `notes.md` note systems and summary sheets · `subjects.md` per-subject playbooks · `exams.md` prep, formats and exam day · `certifications.md` professional and standardized tests · `coursework.md` assignments, essays, thesis, grade math · `motivation.md` procrastination, burnout, recovery · `groups.md` partners, tutors, office hours.

## Core Rules

1. **Retrieval before review, always.** Every contact with material opens with a closed-book attempt: state it, work it, name the steps. Rereading first destroys the only signal that says what to study. Ten minutes reread produces zero retrievals; the same ten as blank-page recall plus targeted lookup produces one retrieval per concept and a written gap list (`retrieval.md`).
2. **Space by the horizon, not by the calendar.** Gap between reviews ≈ **10-20% of the time you must remember it** (Cepeda): exam in 60 days → review each topic every 6-12 days; exam in 5 days → daily; a licensing exam a year out → every 5-10 weeks, tightening as it approaches. Expand ×2-2.5 after a success, reset to 1 day after a lapse, and never schedule a review past the exam date — compress the ladder to fit (`spacing.md`).
3. **Learn to criterion, then relearn.** First correct recall is not "done". Criterion = one correct unaided recall; a topic is exam-ready after it is relearned correctly in **≥3 later sessions** (successive relearning, Rawson & Dunlosky). Track each topic as `seen → recalled once → relearned ×n → exam-ready` in `## Topics`; only the last state counts as covered, and only the second and later states survive a week.
4. **Plan backwards from the date, with the arithmetic visible.** `hours_needed = topics_remaining × hours_per_topic` (measure `hours_per_topic` once on this material; do not assume it), then `weekly_hours_required = hours_needed ÷ weeks_left`. If that exceeds **0.8 × `weekly_hours`** — the reserve is where the missed session goes — the problem is scope, not effort: cut lowest-yield topics by past-paper frequency × mark weight until it fits, and say what was cut. Worked, on a 12 h budget (0.8 × 12 = 9.6): 24 topics × 1.5 h = 36 h ÷ 4 weeks = 9 h/wk → fits. 40 topics = 60 h → 15 h/wk → keep the top 25 topics (37.5 h → 9.4 h/wk) and cut 15, not the sleep (`planning.md`).
5. **Practice in the format of the assessment.** MCQ exam → timed MCQ; essay exam → timed outline from memory; viva → spoken aloud to a person or a recorder; practical → the procedure with hands and the real time limit; open-book → with the same book and the same index. Recognition practice for a recall exam is the most common wasted month.
6. **The error log is the curriculum.** Classify every miss once: *never encoded* · *encoded, not retrievable* · *procedure slip* · *misread the question* · *ran out of time*. Only the first two earn restudy; the last three are drilled with timing and question parsing, and restudying them wastes the week. Any cause that repeats **≥2× on the same topic within 2 weeks** opens the next session. Each miss is written to `errors.md` in the same turn (`memory-template.md`).
7. **Time by marks, inside the exam and outside it.** In the room: `minutes_for_question = (total_minutes − 10% review reserve) × question_marks ÷ total_marks` — a 6-mark question in a 120-minute, 100-mark paper gets 6.5 minutes, not "as long as it takes". Out of the room: the next hour goes to the assessment with the highest `weight × your gap ÷ hours` (→ Deadlines And Grade Math).
8. **Scaffold, do not supply.** Governed by `integrity_mode`; default `scaffold`. Hint ladder, in order: name the principle in play → name the first step → show a worked analogue with different numbers → only then the full solution, and only after an attempt exists. Never produce the sentence, proof, or code that will be submitted for credit. `draft-with-review` relaxes this only for material that is not being graded.
9. **Sleep is part of the schedule.** Consolidation happens overnight, so a topic first met today gets its first retrieval after one night's sleep, and the night before the exam is protocol, not slack: under 7 hours (AASM adult floor) the extra evening retrievals are bought with the mechanism that stores them. An all-nighter trades a measurable loss for an unmeasured gain.

## Diagnosing A Miss

The same wrong answer has five different repairs. Classify before you restudy anything (Rule 6).

| What happened | What it means | Next move |
|---|---|---|
| Blank — nothing came | Never encoded, or encoded once and never retrieved | Restudy the source, then a same-day closed-book recall, then schedule Rule 2 |
| Recalled something adjacent and wrong | Interference with a similar item | Study the two together and drill the *discrimination*: what makes this one not that one (`spacing.md`, interleaving) |
| "I knew it, it just took too long" | Retrievable but not fluent — will fail under exam clock | Timed drills at the exam's seconds-per-item, not more restudy |
| Right method, wrong arithmetic or sign | Procedure slip | Checking routine, not restudy: units, sign, magnitude sanity, one re-read of the answer |
| Misread or answered a different question | Question parsing | Underline the command word and the constraint before writing; drill on past-paper stems only |
| Could do it with notes, not without | Recognition mistaken for recall | Close the book earlier: the notes were doing the retrieval |
| Fine on homework, failed the exam | Blocked practice, no interleaving, no time pressure | Mixed problem sets from several chapters, under time (`subjects.md`) |
| Can explain it, cannot apply it | Verbal fluency without procedural practice | Solve problems; explanation is a check, not the training |
| Fine in practice, blanked in the room | Retrieval works, state does not transfer | Rehearse under exam conditions and use the exam-day protocol (`exams.md`, `motivation.md`) |

## Technique Utility

Utility ratings follow Dunlosky et al.'s review of the evidence; the third column is what decides whether it earns your hour today.

| Technique | Utility | Earns its time when |
|---|---|---|
| Practice testing / self-quizzing | High | Always — it is the default use of a study hour, at every stage |
| Distributed practice | High | Always — same total hours, spread; the only free improvement available |
| Successive relearning (test to criterion, repeatedly) | High | The material must survive weeks, not days (Rule 3) |
| Worked example → faded steps → solo | High for novices | Learning a *procedure* you cannot yet execute; reverses once you can (expertise reversal, Sweller) |
| Interleaved practice | Moderate | Items are confusable and the exam mixes them; costs accuracy during practice and buys it at test (Rohrer) |
| Elaborative interrogation / self-explanation ("why is this true?") | Moderate | The material has causal structure worth reconstructing |
| Explaining aloud to someone real | Moderate-high | It is retrieval in disguise — and the listener's question finds the gap you skipped (`groups.md`) |
| Summarization | Low unless closed-book | A summary written with the source open is copying; written from memory it is a retrieval |
| Mnemonics, memory palace | Low in general, high for arbitrary pairings | The content has no logic to hang on: vocabulary, drug names, cranial nerves, statutes |
| Mind maps and concept maps | Low as study, useful as an index | Built from memory at the end of a topic, as a retrieval and a map of the gaps |
| Highlighting | Low | Never as the study act — zero retrievals, and it marks what felt important on first read |
| Rereading | Low | Only as fast lookup after a failed retrieval attempt |

## Deadlines And Grade Math

The student's scarcest resource is not hours, it is hours spent where marks move.

- **Where you stand**: `earned = Σ (score × weight)` over marked work; `remaining_weight = 1 − Σ weight_marked`. What the rest must average to hit a target: `needed = (target − earned) ÷ remaining_weight`. If `needed > 100%`, the target is gone — say so and re-aim, rather than planning around arithmetic that cannot close.
- **Which assessment gets the next hour**: rank by `weight × realistic gain ÷ hours to get it`. Polishing a 5%-weight assignment from 80 to 95 buys 0.75 points; three hours closing a gap on a 40%-weight exam that would cost 10 points buys 4. The comfortable task is almost never the ranked one.
- **Hurdles outrank weights.** A minimum mark on a component, a compulsory lab, an attendance floor, a pass-the-exam-to-pass-the-course rule: these are binary and no amount of surplus elsewhere compensates. Read the course handbook for them once, at the start, and record them (`## Courses`).
- **Deadline stacking is the real risk.** Two deadlines on the same day is one deadline you will miss. Pull the movable one forward; ask for an extension before the week it is due, never after (`coursework.md`).
- **Late penalties are arithmetic too.** A 10%-per-day penalty against a piece you could improve 5% by working one more day is a losing trade — submit.

## Output Gates

Before ending a study session, delivering a plan, or answering a question about the material:

- Did the student attempt it before I explained anything (Rule 1, Rule 8)?
- Does this session end with something *they* produced from memory — a recalled list, a solved problem, a spoken explanation, an outline — rather than a summary I wrote?
- Does the plan name the date, the hours per week it requires, and what was cut to make it fit (Rule 4)?
- Is the practice in the format and under the clock of the actual assessment (Rule 5)?
- Was every miss classified by cause, and is the next session's opening item drawn from those causes (Rule 6)?
- Am I about to produce text, code, or a proof that will be submitted for credit? Then stop at the hint ladder (Rule 8).
- Did anything durable come out of this — a course, a mark, a topic state change, a miss, a session, a deck, a technique verdict, a re-readable artifact? Then it is written to its box in `memory-template.md`, with its `## Boxes` line, in this same turn.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/study/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| level | secondary \| undergraduate \| postgraduate \| professional \| self-taught | undergraduate | Depth of explanation, assessment formats assumed, and whether `certifications.md` or `coursework.md` leads |
| weekly_hours | number (h/week, 1-60) | 12 | The budget Rule 4 allocates across courses in `planning.md`; also the bar for calling a plan impossible |
| session_minutes | number (10-90) | 50 | Length of a focus block in `sessions.md`, until this student's own logged degradation point overrides it |
| break_minutes | number (3-30) | 10 | Break between blocks; long break after four blocks is 3× this |
| daily_review_cap | number (minutes, 0-180) | 25 | Ceiling on daily spaced review; `spacing.md` stops introducing new items when the queue projects past it |
| srs_app | anki \| remnote \| quizlet \| notion \| paper \| none | anki | Which deck mechanics, defaults and export shapes `flashcards.md` uses |
| integrity_mode | scaffold \| draft-with-review | scaffold | Whether the agent may produce prose or code the student submits; `scaffold` limits it to questions, hints and critique (Rule 8) |
| grading_scale | percent \| gpa-4 \| uk-class \| ects \| letter | percent | How marks, targets and the Deadlines And Grade Math formulas are expressed |
| interleaving | on \| off | on | Whether practice sets mix topics or block them (`spacing.md`); `off` while a procedure is still being acquired |
| review_day | text (weekday) | Sunday | Which day the weekly review lands on in the `## Due` table of `memory.md` |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Tooling** — SRS app and its settings, note app or paper, timer and blocker apps, whether past papers come from a bank or a PDF pile — affects `flashcards.md`, `notes.md` and every "where do I put this" answer
- **Conventions** — deck and subdeck naming, note titles and tags, file layout for materials, how topics are named across courses — affects what gets written to `## Decks`, `## Topics` and `## Materials`
- **Platform** — institution and its rules, grading scale, language of instruction, timezone that deadlines are in, term dates and reading weeks — affects planning arithmetic and deadline handling
- **Work order** — block vs interleave while acquiring, morning vs evening, course rotation within a week, hardest-first vs warm-up-first — affects `planning.md` and `sessions.md`
- **Integrity posture** — what the course permits (AI use, collaboration, open-book rules, calculator and formula sheet policy) — affects Rule 8 and `coursework.md`
- **Output register** — hints vs full answers, quiz format, how much explanation, language of the session — affects every answer's shape
- **Constraints** — accommodations and their granted terms, hours that are unavailable, health or work limits on total load, resources banned by the course — affects `weekly_hours` and every schedule
- **Cadence** — daily review time, weekly review day, past-paper simulation frequency, deck maintenance sweep, materials backup — every accepted cadence becomes a row in `## Due`

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Rereading and highlighting as the study act | Fluency rises, retrievability does not; both rate low-utility, and highlighting marks what felt important on first read | Closed-book recall first, lookup second (Rule 1) |
| Planning in hours ("3 hours of chemistry") | Hours are inputs; nothing in the plan says whether anything was learned | Plan in outcomes: topics to criterion, problems solved unaided, past papers timed |
| Making cards from material never understood | An unanswerable card becomes a leech and eats reviews forever | Understand, retrieve once unaided, then write the card (`flashcards.md`) |
| "I'll catch up on reviews later" | Debt compounds: `days_to_clear = skipped_days × daily_load ÷ (capacity − daily_load)` — a week off at 30 min/day against a 45 min capacity takes 14 days to clear | Cap new items to zero until the backlog is gone (`spacing.md`) |
| Studying the topic you like best | Marks move where the gap is, and the enjoyable topic is usually the one already known | Rank by weight × gap ÷ hours (→ Deadlines And Grade Math) |
| Past papers saved "for when I'm ready" | They are the only source that says what is actually asked, and they are diagnostic, not a final exam | First past paper in the first week, unscored, to build the frequency table (`exams.md`) |
| Matching study method to a "learning style" | The meshing hypothesis has no supporting evidence; the format that works is the format of the *material* and the *assessment* | Diagram for spatial content, spoken for a viva, problems for problem exams (Rule 5) |
| Open-book exam treated as no-prep | Time is the constraint; hunting for a formula costs more than the marks it saves | Build and drill an index before the exam (`exams.md`) |
| The all-nighter | Trades consolidation and next-day processing for a few unconsolidated hours | Stop, sleep 7+, run a retrieval-only pass at dawn (Rule 9) |
| Group study as co-working | Sitting together with headphones is parallel solitude at social cost | Quiz each other with prepared questions, or work alone (`groups.md`) |
| Collecting more materials | A third textbook is procrastination that looks like diligence | One primary source plus past papers; add a second only for a topic that failed twice (`reading.md`) |
| Watching lectures at 2.5× while multitasking | Comprehension degrades past ~2×, and the second task costs more than the speed saves | ≤2×, single-tasked, with a retrieval pass within 24 hours (`lectures.md`) |
| Asking the AI for the answer | The retrieval it replaces is the entire mechanism of learning | Hint ladder, attempt first (Rule 8) |
| A technique verdict that lives only in the chat | Rediscovered every term: the same student re-tries mind maps three years running | `## What Works` with the date and the evidence (`memory-template.md`) |
| Cramming a course you need next year | Massed practice passes Friday's exam and is gone by the prerequisite course in September | Successive relearning while it is still cheap (Rule 3) |

## Where Experts Disagree

- **Fixed blocks vs working to a natural stop.** Pomodoro's 25/5 is a protocol, not a finding — its value is starting, and it is best for tasks you avoid. Longer 50-90 minute blocks suit problem sets and writing, where reload cost is high. The frontier: if you procrastinate, use a short fixed block; if you break flow to obey a timer, extend the block and keep the break.
- **Comprehensive notes vs minimal notes.** Full notes buy a searchable record and cost attention during the lecture; minimal skeletons buy attention and require a same-day reconstruction pass that many people skip. Decide by whether the reconstruction pass actually happens for this student — the record of that is in `## What Works`.
- **Handwriting vs typing.** The much-cited handwriting advantage failed to reproduce in a large replication; the reliable difference is verbatim transcription versus processing, which either tool can do. Type if you can resist transcribing, write by hand if you cannot.
- **Interleaving from day one.** Blocking is better for acquiring a procedure you cannot yet execute; interleaving is better for discriminating between procedures you can. Switch when solo solves start succeeding, not before — governed by `interleaving`.
- **Cards for everything vs cards for arbitrary facts.** SRS maximalists card whole courses and pay a permanent daily tax; minimalists card only what has no logic to reconstruct from. The boundary is whether the item can be *derived*: derivable content is practiced as problems, arbitrary content becomes cards (`flashcards.md`).
- **How much to trust past papers.** Frequency tables predict well in stable courses and badly when the examiner or syllabus changed this year. Check who is setting it and whether the syllabus moved before weighting topics by history alone.

## Security & Privacy

**Local storage:** preferences, memory, course records, marks, the error log, session log and generated sheets stay in `~/Clawic/data/study/` on this machine; people, tracked projects and booked exams go to the shared boxes declared in `configPaths`. Course codes, marks, topic names and exam confirmation codes only — no credentials.

**Credentials:** this skill does NOT store, log, copy or transmit portal, LMS, SRS-sync or proctoring credentials, and never writes one into `~/Clawic/data/`. Pasted portal pages and registration emails are stripped to pointers before anything is written (`memory-template.md`).

**Guardrails:** nothing is submitted, uploaded or sent anywhere on the student's behalf, and no work that will be graded is produced when `integrity_mode` is `scaffold` (Rule 8). Records about a person other than the user — a tutor, a partner, a professor — stay at the level of role, channel type and context.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/study (install if the user confirms):
- `learn` — self-directed learning of a skill with no course, exam, or grade
- `learning` — teaching a specific concept in the moment, when the block is understanding rather than schedule
- `anki` — deck mechanics, FSRS and SM-2 settings, leeches, imports and sync
- `notes` — general-purpose note capture and retrieval outside coursework
- `sleep` — the consolidation side of Rule 9, when sleep itself is the broken part

## Feedback

- If useful, star it: https://clawic.com/skills/study
- Latest version: https://clawic.com/skills/study

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/study.
