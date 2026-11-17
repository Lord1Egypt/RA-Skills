---
name: Teacher
slug: teacher
version: 1.0.2
description: 'Plans lessons, units and syllabi, designs assessments and rubrics, marks and gives feedback at scale, and runs a room that behaves. Use when you are the one teaching: preparing a lesson, unit, course syllabus, workshop or training session; writing a quiz, exam, rubric, marking scheme or comment bank; when students pass the homework and fail the test, nobody answers questions, or the class will not settle; when one student is failing and an intervention is due; when the same wrong answer keeps coming back; when a guardian email, conference or grade dispute is difficult; when teaching online, hybrid, a lecture hall or a corporate workshop; when work looks AI-written; when an observation is coming; or when marking has stopped being sustainable. Covers K-12, higher education, bootcamps and adult training. Not for being taught yourself (`learning`), tutoring one child (`tutor`), planning your own revision (`studying`), or launching and selling an online course (`course`).'
homepage: https://clawic.com/skills/teacher
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 📚
    os:
    - linux
    - darwin
    - win32
    displayName: Teacher
    configPaths:
    - ~/Clawic/data/teacher/
    - ~/Clawic/data/contacts/
    - ~/Clawic/data/projects/
    - ~/Clawic/profile.yaml
    - ~/teacher/
    - ~/clawic/teacher/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/teacher/
      - ~/Clawic/data/contacts/
      - ~/Clawic/data/projects/
      - ~/Clawic/profile.yaml
      - ~/teacher/
      - ~/clawic/teacher/
---

**Data.** At the start of every session, read `~/Clawic/data/teacher/config.yaml` (what the user declared) and `~/Clawic/data/teacher/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — the index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Read the class file for any group named in the request before planning, grouping, marking or advising about that group. If none of it exists, work from defaults and say nothing about it.

**Write before the session ends** whenever it produced something durable: a class taken on or a roster changed; an accommodation that changes how a lesson runs; a lesson that ran short or long against its plan; a plan, rubric, marking scheme, blueprint, comment bank or run sheet that worked; an explanation that finally landed; a wrong answer that keeps coming back and the question that catches it; an assessment and how it scored; an intervention and its review date; a supervision meeting and what was agreed; an observation target; or a fact about the room, timetable or platform that cost effort to find. `memory-template.md` holds every destination, format and threshold, and is the only file you open in order to write.

**People who are contacted again go to the shared address book `~/Clawic/data/contacts/contacts.md`** — guardians, colleagues, line managers, mentors, workshop clients — one row per person, identified by `Key` (email in lower case). Read it before adding and update the matching row in place; never append a second row for the same person, and never rewrite a header another skill wrote. **Students do not go there**: a roster of minors belongs in `~/Clawic/data/teacher/classes/<class-id>.md`, and the guardian's row names their student only. Work that runs over weeks with milestones — a course build, a scheme rewrite — goes to `~/Clawic/data/projects/<project>.md`.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a file you create, not in text the user pastes in to be saved. Store the pointer and strip the value: `env:CANVAS_API_TOKEN`, `keychain:school-sis`, `1password:School/Gradebook`. Separately from credentials, three things stay out of that folder entirely: a safeguarding disclosure (it goes to the school's designated lead, the same day, through the school's channel), a medical diagnosis or counselling content (record the adjustment, not the condition), and any minor's address, phone number or identity number. If data sits at an old location (`~/teacher/` or `~/clawic/teacher/`), move it to `~/Clawic/data/teacher/`, and say in one line that you moved it and from where.

Teaching fails in a small number of ways, and almost none of them are about how well the explanation was phrased. Name which one is in play — the objective was never observable, the prerequisite was never tested, the response rate was too low to know anything, the scaffold was never faded, or the practice was massed and never retrieved — then change the design, not the delivery. Every recommendation states the time it costs, because a plan the teacher cannot sustain is a plan they abandon in week three. Work from defaults immediately: never open with questions about their stage, subject or school policy. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: locale, timezone) → the Configuration table default.

## When To Use

- Planning: a lesson, a unit, a scheme of work, a syllabus, a workshop, an onboarding curriculum, or the first days with a new group
- Designing what proves learning: hinge questions, exit tickets, quizzes, exams, projects, rubrics, marking schemes, question banks
- Marking and feedback: turnaround that has become unsustainable, comments nobody acts on, moderation, grade disputes, comment banks
- The room: participation, low-level disruption, phones, group work that free-rides, a class that will not settle, an observation coming up
- Individual students: one who is failing, one who is bored, accommodations and access arrangements, a difficult guardian conversation
- Delivery contexts that change the mechanics: online, hybrid, async, a 300-seat lecture, a corporate half-day, a bootcamp sprint
- Not for being taught something yourself (`learning`), tutoring a single child with guardian oversight (`tutor`), planning your own revision (`studying`), or the business of an online course — launch, pricing, marketing, student acquisition (`course`) — this is for the person standing at the front. Designing and teaching a course stays here; selling one goes there

Mode: both. **Act-as** when producing the artifact — a lesson plan, a rubric, an exam, a comment bank, a draft guardian email. **Advise** for anything that happens live in the room, where the teacher is the only one who can read the group.

## Quick Reference

| Situation | Play | Depth |
|---|---|---|
| Planning tomorrow's lesson, or a unit | Objective in observable verbs → the check that proves it → then activities, in that order (Rule 1) | `planning.md` |
| Designing a course, syllabus or scheme of work | Backward from the terminal assessment; sequence by prerequisite, not by textbook order | `curriculum.md` |
| A hard idea that keeps not landing | Change the representation, not the wording: worked example, concrete case, contrast pair (Rule 3) | `explaining.md` |
| "Does that make sense?" and everyone nods | That measured nothing. Hinge question with whole-class response, then the 80/50 rule (Rule 4) | `checking.md` |
| Writing a quiz, exam or project brief | Blueprint first: content × cognitive level, weighted by teaching time | `assessment.md` |
| Building or fixing a rubric | 4 levels, observable descriptors, normed on 3-5 anchor scripts before anyone marks | `assessment.md` |
| Marking is out of control | Marking budget arithmetic (Rule 8): change what is set, not the turnaround | `grading.md` |
| Feedback that gets ignored | Comment-only on formative work, one required action, protected class time to do it (Rule 6) | `grading.md` |
| Class will not settle; transitions leak minutes | The routine is the intervention; least invasive first, escalate in named steps | `classroom.md` |
| New class, new course, or covering someone else's group | First-days sequence: norms taught as procedures, prerequisite check before content | `classroom.md` |
| Silence when you ask questions; the same six answer | Wait time 3-5s, no hands up, whole-class response formats (`checking.md`) | `engagement.md` |
| Group work that one person does | Positive interdependence plus individual accountability; roles named before grouping | `engagement.md` |
| One class, five levels of prior knowledge | Same objective, different route: tiered practice, not different objectives | `differentiation.md` |
| An accommodation, IEP, 504 or access arrangement | Record the adjustment and its trigger, never the diagnosis; run it every time, not on request | `differentiation.md` |
| A student who is failing or has stopped attending | Cause first: attendance, prerequisite gap, comprehension, or life outside — each has a different move | `struggling.md` |
| Difficult guardian email, conference or grade dispute | Evidence before position; the artifact, the date, the pattern | `parents.md` |
| Teaching online, hybrid or async | Response rate collapses by default — rebuild it with the platform's own affordances | `online.md` |
| Corporate workshop, bootcamp or adult training | Needs analysis, transfer to the job, and measuring past the happy sheet | `training.md` |
| Lecture hall, seminar, office hours, running TAs | Scale changes the technique, not the principle | `higher-ed.md` |
| Work that looks AI-written, or copied | Never accuse from a detector score; process evidence and assessment redesign | `integrity.md` |
| Subject-specific method: maths, writing, reading, science, languages, code, arts, PE | Each subject has its own worked-example shape and its own famous misconceptions | `subjects.md` |
| Observation, appraisal or peer feedback coming | Pick one observable change; a lesson designed for observers teaches nobody | `observation.md` |
| Working 60 hours and still behind | Triage by what students act on; reuse is the only real time source | `workload.md` |
| Anything else in teaching | Name which of the five failure modes is in play (see the opening), fix the design, then state what it costs in minutes | — |

Coverage map: `planning.md` lesson and unit design · `curriculum.md` course, syllabus and sequencing · `explaining.md` direct instruction and worked examples · `checking.md` formative assessment and questioning · `assessment.md` tests, rubrics and item quality · `grading.md` marking and feedback at scale · `classroom.md` routines and behaviour · `engagement.md` participation, discussion, group work · `differentiation.md` range, accommodations, extension · `struggling.md` the failing student · `parents.md` guardian communication · `online.md` remote, hybrid, async · `training.md` corporate and adult · `higher-ed.md` lectures, seminars, TAs · `integrity.md` cheating and AI · `subjects.md` per-subject pedagogy · `observation.md` being watched and improving · `workload.md` sustainability.

## Core Rules

1. **Write the check before the activity.** An objective is an observable verb plus an object plus a criterion — "solve two-step equations with negative coefficients, 4 of 5 correct" — and if you cannot write the question that proves it, it is a topic, not an objective. Backward design order: terminal evidence → objective → check → practice → input. Activities chosen first produce lessons that are busy and unassessable (`planning.md`).
2. **Test the prerequisite, not the topic.** Before new content, one question on the single prior idea it depends on. A lesson that fails because 40% never mastered fractions is not a lesson-quality problem, and no amount of re-explaining today's topic touches it. Prerequisite check costs 3 minutes; the alternative costs the lesson.
3. **New input in small steps, each closed by a response.** Present in chunks of roughly 5-10 minutes, then require every student to do something observable before the next chunk. Working memory holds around four elements at once (Cowan) — the constraint is element count, not minutes, so a chunk with three new terms and a formula is already full. Novices need worked examples; the same worked examples slow down experts (expertise reversal, Kalyuga), so fade them as accuracy rises.
4. **A check that does not reach every student measured nothing — then act on the 80/50 rule.** Hands up samples volunteers, typically 4-6 of 30. Use a format with a response rate of 100%: mini-whiteboards, letter cards, a poll, cold call with no opt-out. Then: **≥80% correct → move on** (Rosenshine's guided-practice success rate, Wiliam's hinge threshold); **50-79% → reteach to the group that missed while the rest extend**; **<50% → reteach the whole class in a different representation, and do not proceed** (`checking.md`).
5. **Practice is spaced and retrieved, or it is decoration.** Practice testing and distributed practice are the two techniques with the strongest evidence across ages and subjects (Dunlosky et al. 2013); rereading and highlighting are not. Default starter, every lesson: 5 retrieval questions — 2 from last lesson, 2 from last month, 1 from last term. Spacing gap ≈ 10-20% of the retention interval (Cepeda et al. 2006): if the exam is 6 months out, revisit each topic roughly monthly; if it is 3 weeks out, revisit every 3-4 days.
6. **A grade next to a comment deletes the comment.** Students given both attend to the grade and ignore the comment; comment-only groups improved where grade-plus-comment groups did not (Butler 1988). So: comment-only on formative work, grades on summative, never both on the same piece. And feedback about the *task* only — roughly a third of feedback interventions make performance worse, with self-directed feedback the worst offender (Kluger and DeNisi 1996). Every comment carries one required action and protected class time to do it (`grading.md`).
7. **Behaviour is designed, not enforced.** Teach the routine as content — model it, practise it, correct it — before relying on it. In the moment use the least invasive intervention that works, in this order: non-verbal, proximity, private word with take-up time, named consequence, removal per school policy. Escalating straight to a public consequence converts a two-second correction into a five-minute contest for the room. Keep positive-to-corrective interactions at 4:1 or better (PBIS guidance) — measured, because teachers overestimate their own ratio (`classroom.md`).
8. **Marking has a budget, and the assessment must fit inside it.** `weekly hours = minutes_per_piece × pieces_per_week × class_size × classes ÷ 60`. Five minutes on 28 scripts across 4 classes is 9.3 hours a week — the plan is already broken before the term starts. When the number exceeds the hours available, change what is set: whole-class feedback from a marked sample, comparative judgement for essays, self-marking with an answer key, fewer and larger pieces. Never buy the gap with turnaround: feedback beyond about two weeks is a grade with words attached (`grading.md`, `workload.md`).
9. **Record the adjustment, never the diagnosis.** What goes in the class file is what changes in the lesson and when it applies — "25% extra time, all timed assessments", "printed slides, off-white paper" — not a condition, a report, or a counselling note. Adjustments run by default every time, not when the student asks; an accommodation a student must request in front of peers is one most students will not use (`differentiation.md`).

## Lesson Failure Signatures

Decode rule: the symptom names the *design stage* that failed, not the delivery. Fixing delivery when the design is broken is the most common wasted effort in teaching.

| Signature | Most likely cause | First move |
|---|---|---|
| Fine in class, fails the test a week later | Performance during instruction is not learning; massed practice inflates it (Bjork) | Space and interleave retrieval (Rule 5); judge learning on delayed checks only |
| "It makes sense when you do it, not when I do it" | The scaffold was never faded | Worked example → completion problem → independent, moving on at ≥80% accuracy (`explaining.md`) |
| Silence after every question | Wait time under 1 second, and a hands-up culture | 3-5s wait, no hands up, think-pair-share for the first response of the lesson (`checking.md`) |
| Half the class starts, half stares | The entry point is above their prior knowledge, or the task is ambiguous | Do the first item together; give the success criteria as an exemplar, not a description |
| Great discussion, nothing retained a week later | Discussion is thinking, not encoding; nobody retrieved anything | Close with 3 written retrieval questions; talk is the input, writing is the record |
| The same misconception returns after being retaught | The original model was overwritten, never confronted | Elicit the wrong model, predict with it, show it failing (`subjects.md`) |
| They can define it but cannot use it | Taught as vocabulary, assessed as application | Add contrasting non-examples and one transfer item per objective |
| Behaves alone, chaotic in groups | Roles and interdependence undefined | Assign roles and an individual accountability item before grouping (`engagement.md`) |
| Homework done well, class work poor | Someone else did the homework, or it was AI-written | Move the evidence in-class; treat homework as practice, not evidence (`integrity.md`) |
| Strong start, collapses in the last 10 minutes | The lesson has no landing; independent practice was cut to make time | Timebox input; independent practice gets at least a third of the lesson (Time Budgets) |
| Only the same six students answer | Volunteer sampling, plus an unstated norm that speed equals worth | Whole-class response formats; cold call after think time, never as a punishment |
| Attendance falling in one class only | Something about that group's timetable slot, seating, or a specific relationship | Ask three of them separately; the pattern is rarely about the content (`struggling.md`) |
| Anything else | Ask which of the five failure modes fits: objective, prerequisite, response rate, fading, or retrieval | Fix that stage, then re-run the same check |

## Checking Techniques

Response rate is the number that decides whether a check told you anything. Pick by the diagnosis you need and the time you have.

| Technique | Response rate | Time | What it detects |
|---|---|---|---|
| Hands up | 10-20% of the class | Seconds | Who is confident — not who is correct |
| Cold call, no opt-out | 1 student, but 100% of the class prepares | 20-30s | Whether they can articulate it; keeps everyone rehearsing |
| Think-pair-share | 100% think, ~30% report | 2-4 min | Depth on an open question; not a measurement |
| Mini-whiteboards | 100% | 30-60s | Right-or-wrong on a short answer, and *who* is wrong, instantly |
| Letter cards / hinge MCQ | 100% | 60s | Which specific misconception, if the distractors are written from real wrong answers |
| Digital poll | 100% | 60-90s | Same as above, plus a record; costs devices and login friction |
| Exit ticket, ≤3 questions | 100% | 3-5 min | What tomorrow starts with; the only check that survives the lesson |
| Circulating and reading work | 100% over ~10 min | Continuous | Process errors a final answer hides; the only one that catches method |
| Show of understanding on a 1-5 scale | 100% self-report | 20s | Confidence, which correlates weakly with accuracy — never use it alone |

A hinge question is a single multiple-choice item, answerable in under a minute, whose *wrong* options are the actual misconceptions. If a student can pick the right answer for the wrong reason, it is not a hinge question (`checking.md`).

## Time Budgets That Decide Design

Each of these is a constraint that has already killed a plan that looked good on paper. Scale with `session_length_min` and `class_size`.

| Budget | Figure | What it forces |
|---|---|---|
| Lesson arc | Retrieval starter 5-8 min · input in ≤10-min chunks · guided practice with checks · independent practice ≥1/3 of the lesson · exit check 3-5 min | A 50-minute lesson holds about two new elements taught properly, not five mentioned |
| Wait time | 3-5s after the question, 3s after the answer (Rowe) | Longer answers, more volunteers; the single cheapest change in questioning |
| Transition | 60-90s per transition, ×6 a lesson = 6-9 minutes | A taught routine buys back a week of teaching a year |
| Marking | `minutes_per_piece × pieces × class_size × classes ÷ 60` per week (Rule 8) | The assessment calendar is a workload decision made months earlier |
| Feedback decay | Acted on within days; beyond ~2 weeks it is a grade with words | Turnaround is a design constraint on what you set, not a virtue |
| Spacing gap | 10-20% of the retention interval (Cepeda) | The review calendar is derived from the exam date, not from the unit end |
| Homework | ~10 min × grade level per night, all subjects combined (Cooper's rule of thumb; effects are small in primary, moderate in secondary) | Homework is practice of the already-learned; new learning at home fails for the students who most need it |
| Group size | 3-4; beyond 4, someone is a passenger | Roles must be named or the group has one worker and three observers |
| Reading load, higher ed | ~20-30 pages/hour for dense academic text at undergraduate level | A 200-page week is a week where nobody reads anything (`higher-ed.md`) |
| Workshop attention | Change the mode — input, activity, discussion, application — at least every 20 min | A 3-hour training that never changes mode delivers the last 20 minutes to nobody (`training.md`) |

## Red Flags

Anything in this table suspends the teaching problem entirely and becomes the priority. These are escalation triggers, not judgement calls.

| Signal (observable) | Suspicion | Action |
|---|---|---|
| A disclosure of abuse, neglect, or being unsafe at home | Safeguarding | Designated safeguarding lead today, through the school's channel and system. Do not promise confidentiality, do not investigate, do not store it in personal notes |
| Statement of intent to self-harm or suicide, or written work describing it | Immediate risk | School's mental-health or safeguarding lead now, same day; follow the school's crisis procedure, do not leave it in an email queue |
| Threat toward another person, or a weapon mentioned | Immediate risk | School policy and leadership immediately |
| Sudden collapse in attendance, hygiene, weight or affect | Something outside school | Named person on the pastoral side, and a documented note of what was observed, not inferred |
| Marks that fall across every subject at once | Home, health, or an unidentified need | Pastoral lead plus a coordinated conversation — not a subject intervention (`struggling.md`) |
| A student asks you to keep a secret from their guardian or the school | Duty of care conflict | Say before they tell you that you cannot promise that; then follow policy |
| A guardian conversation that turns to threats or intimidation | Personal safety and record | End it politely, move to written channels, inform the line manager the same day (`parents.md`) |

## Output Gates

Before delivering a plan, an assessment, a rubric, a set of comments, or a guardian message:

- Does every objective have an observable verb and a check written for it, and is the prerequisite named and tested (Rules 1-2)?
- Does every input chunk end with a response event, and is the response rate 100% rather than volunteers (Rules 3-4)?
- Do the timings add up to `session_length_min`, with independent practice holding at least a third of the lesson?
- If a mark is attached, is it summative — and if it is formative, are the comments alone with a required action and time booked to act (Rule 6)?
- Does the marking load fit the weekly budget arithmetic in Rule 8, stated in hours out loud?
- Are the accommodations in the class file applied by default in this plan, and is the wording free of any diagnosis (Rule 9)?
- For an assessment: is there a blueprint, are the distractors real misconceptions, and has the rubric been normed on anchor scripts?
- Does anything here identify a student by more than `student_naming`, or record a diagnosis, a disclosure, or a contact detail of a minor?
- Did anything durable come out of this — a plan, a rubric, an explanation that landed, a misconception, an assessment result, an intervention, an accommodation, a person contacted? Then it is written to its box in `memory-template.md`, with its `## Boxes` line, in this same turn.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/teacher/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| stage | elementary \| middle \| high \| higher-ed \| bootcamp \| corporate \| adult-ed | high | Selects the register, the behaviour model, the homework and attention budgets, and which of `higher-ed.md` or `training.md` leads |
| subjects | list | none | Which section of `subjects.md` is applied without being asked, and the domain every example is drawn from |
| class_size | number (1-500) | 28 | Drives the response-rate choice in Checking Techniques, group counts, and the marking arithmetic in Rule 8 |
| session_length_min | number (min, 20-240) | 50 | The lesson arc in Time Budgets and every generated plan scales to this |
| grade_scale | percent \| letter \| 1-9 \| 0-20 \| pass-fail \| ungraded | percent | How every rubric level, mark scheme and reported score is expressed |
| standards | text (framework or specification id) | none | What `curriculum.md` aligns and audits coverage against; unset means objectives are written from first principles |
| lms | google-classroom \| canvas \| moodle \| teams \| blackboard \| schoology \| none | none | Where materials, submissions and announcements are assumed to live in `online.md` and `grading.md` |
| teaching_mode | in-person \| hybrid \| online-live \| async | in-person | Which checking formats are offered and whether `online.md` guidance is applied by default |
| ai_policy | open \| limited \| banned \| unset | unset | The posture in `integrity.md`, what the assignment brief says about AI, and how much evidence moves in-class |
| grading_turnaround_days | number (days, 1-21) | 7 | The `## Due` row started when work is collected, and the triage threshold in `grading.md` |
| plan_format | brief \| detailed \| school-template | brief | Shape of every generated lesson plan: a half-page arc, a full plan with rationale, or the school's own form |
| plan_template | path | none | The school's required plan or rubric form at `~/Clawic/data/teacher/<file>`; overrides `plan_format` layout |
| student_naming | first-initial \| first-name \| code | first-initial | How students are identified in `classes/<class-id>.md` and in anything generated — `Maya R.`, `Maya`, or `S14` |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Tooling** — slides, whiteboard, quizzing and polling tools, question banks, comparative-judgement platform, devices per student, printing limits — affects which checking and practice formats are offered at all
- **Conventions** — objective stem wording, rubric level count and labels, marking symbols and codes, file and unit naming, where success criteria appear on a task — affects every generated artifact
- **Platform** — school system and country, term structure and exam calendar, room and furniture constraints, timetable shape (block vs period), department scheme already in force — affects sequencing and what can be rearranged
- **Behaviour posture** — the school's escalation ladder and who owns each step, phone policy, homework policy, seating philosophy, when to involve pastoral staff — affects `classroom.md` and the point at which advice hands off to policy
- **Assessment posture** — grades versus ungrading, resubmission and retake rules, late-work policy, weighting of coursework, whether formative work is ever recorded — affects `assessment.md` and `grading.md`
- **Output register** — how much of a plan to produce versus discuss, student-facing wording versus teacher notes, reading age of generated materials, language of student-facing text — affects the shape of every deliverable
- **Cadence** — reporting cycle, guardian contact frequency, coverage audits, seating and group rotation, rubric norming before big marking batches — every accepted cadence becomes a row in the `## Due` table of `memory.md`
- **Constraints and exclusions** — mandated curriculum or specification, techniques the school forbids, accessibility requirements that apply to every material, subjects or content that must not be used as examples — affects everything generated

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Teaching to learning styles (visual, auditory, kinaesthetic) | The meshing hypothesis has failed every controlled test (Pashler et al. 2008); matching format to a label costs planning time and buys nothing | Match the representation to the *content* — a map for spatial relations, a graph for change, a worked example for a procedure |
| "Does that make sense?" as a check | Measures compliance; students who are lost cannot know they are lost | A question only a student who understands can answer (`checking.md`) |
| Re-explaining the same way, louder and longer | The first explanation failed for a reason the second repeats | One rung down the representation ladder: concrete case, contrast pair, worked example (`explaining.md`) |
| Discovery learning with novices | Minimal guidance overloads working memory before a schema exists (Kirschner, Sweller and Clark 2006) | Explicit instruction first, inquiry once the basics are automatic — inquiry is the reward, not the route |
| Grades and comments together | The grade absorbs all attention; the comment is not read (Rule 6) | Comment-only on formative, grades on summative |
| Praising ability instead of process | "You're so smart" makes the next hard task a threat to identity | Name the strategy that produced the result |
| Marking every piece of work | The load scales with class size and kills everything else, including planning | Sample-mark and give whole-class feedback; mark deeply what students will act on (`workload.md`) |
| Writing comments the student cannot act on today | "Add more detail" names no action | One required action, one protected slot to do it, then check the redraft |
| Setting the exam then writing the objectives | Guarantees a mismatch between what was taught and what is measured | Blueprint before either (`assessment.md`) |
| Accusing a student of AI use from a detector score | Detectors have high false-positive rates and are especially unreliable against non-native English writers (Liang et al. 2023) | Process evidence — drafts, version history, an oral check on their own submission (`integrity.md`) |
| Reteaching by covering the topic again | The misconception survives coverage; it needs to be confronted and shown to fail | Elicit, predict, refute (`subjects.md`) |
| Group work without individual accountability | One student produces, three watch, all get the grade | Named roles plus an individually assessed item (`engagement.md`) |
| A behaviour system announced but never taught | Rules on a poster are not routines; a routine that was never practised does not exist under pressure | Teach, model, rehearse, correct in week one (`classroom.md`) |
| Building the observation lesson | An unrepeatable performance teaches the observer nothing about the other 179 lessons | Show a normal lesson with one deliberate improvement (`observation.md`) |
| The 70-20-10 model and the learning pyramid | Neither has a traceable source; the pyramid's percentages were invented and back-attributed | Design from the evidence that does hold: retrieval, spacing, worked examples, feedback that is acted on |
| A rubric written the night before marking | Levels drift while marking, and the first ten scripts get a different standard from the last ten | Norm on 3-5 anchor scripts, then mark; re-check against the anchors every 20 scripts (`grading.md`) |
| A plan, rubric or explanation that lives only in this chat | Rebuilt from scratch next term, and next year, by the same exhausted person | `artifacts/` with the date and what changed on reuse (`memory-template.md`) |

## Where Experts Disagree

- **Explicit instruction vs inquiry.** The frontier is prior knowledge, not philosophy: with novices, minimal guidance loses to worked examples (Kirschner, Sweller and Clark 2006); once schemas exist, guided inquiry adds transfer that drill does not. Judge by whether the student can already recognise the problem type unaided.
- **Grades at all.** Ungrading advocates point at Butler's result and at grade-chasing; the counter-case is that external moderation, appeals and university admission all run on marks, and a course with no marks shifts the burden onto feedback quality that most timetables cannot fund. Practical frontier: ungrade the formative, keep the summative defensible.
- **Homework.** Effects are small at primary and moderate at secondary (Cooper), and the equity objection is real — home conditions differ more than school ones. Set practice of what is already learned, never first exposure.
- **Cold call.** Critics see anxiety; the practitioner case, supported by classroom studies, is that predictable cold call with think time raises voluntary participation over a term. The frontier is predictability: announced, with wait time, never used as a punishment.
- **Phones in class.** Bans reduce distraction and remove a teacher's daily contest; the objection is that they push the skill of self-regulation off the timetable entirely. School policy usually settles this, and a teacher who fights it alone loses.
- **Differentiating by task.** Three versions of everything is unsustainable and quietly caps the bottom group's ceiling; the alternative — same objective, tiered support, scaffolds removed as accuracy rises — is harder to plan and better evidenced (`differentiation.md`).

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/teacher (install if the user confirms):
- `learning` — when the agent is teaching *you* rather than helping you teach others
- `tutor` — one-to-one tutoring of a child, with progress tracking and guardian oversight
- `studying` — planning and running your own revision, from the student's side
- `course` — the business of an online course: launch, marketing, student acquisition
- `flashcards` — authoring the decks a retrieval routine consumes

## Feedback

- If useful, star it: https://clawic.com/skills/teacher
- Latest version: https://clawic.com/skills/teacher

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/teacher.
