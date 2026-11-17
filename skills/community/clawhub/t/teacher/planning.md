# Planning — A Lesson and a Unit That Hold Up

A plan is a sequence of evidence, not a sequence of activities. The test of a plan is whether, at four fixed moments, you can say what every student can now do.

**Contents:** [Backward Design in Five Steps](#backward-design-in-five-steps) · [Writing an Objective That Can Be Checked](#writing-an-objective-that-can-be-checked) · [The Prerequisite Check](#the-prerequisite-check) · [The Lesson Arc](#the-lesson-arc) · [Unit Design](#unit-design) · [Selecting Practice](#selecting-practice) · [Planning for the Group You Have](#planning-for-the-group-you-have) · [What a Plan Must Contain](#what-a-plan-must-contain) · [Replanning Mid-Lesson](#replanning-mid-lesson) · [Planning Faster](#planning-faster)

**Before planning for a named group**, read that group's `~/Clawic/data/teacher/classes/<class-id>.md`: the accommodations that must run by default, the pacing already carried from earlier weeks, and the groupings that do not work. Read `## Explanations That Landed` and `## Misconceptions` in `memory.md` for the topic — the representation that worked last year and the wrong answer that always appears are the two most expensive things to rediscover.

## Backward Design in Five Steps

Order matters; each step is only answerable once the one above is fixed (Wiggins and McTighe).

1. **Terminal evidence.** What will students produce at the end of the unit that could not be produced without understanding? Name the artifact: the paper question, the write-up, the working demo, the performance.
2. **Objectives.** Decompose that artifact into observable capabilities, one per lesson or two per lesson at most (Rule 3: element count, not minutes, is the ceiling).
3. **The check.** For each objective, write the exact question or task that separates a student who has it from one who does not. If two students with different understanding both pass it, it is a weak check.
4. **Practice.** What must be done repeatedly, with feedback, to get from novice to that check. This is where most of the lesson time goes and where most plans allocate least.
5. **Input.** Only now decide what you will say, show and model, and in what order. Input is the smallest part of the plan and the part teachers over-plan.

Planning in the opposite direction — activity first — produces lessons that are enjoyable, busy and unassessable, and it is the single most common structural flaw in a plan brought for review.

## Writing an Objective That Can Be Checked

Form: **observable verb + object + condition or criterion**.

| Weak | Why | Rewritten |
|---|---|---|
| Understand photosynthesis | "Understand" is unobservable — it names no evidence | Explain, using a labelled diagram, where the carbon in a plant's mass comes from |
| Learn about the French Revolution | A topic, not a capability | Rank three causes of the 1789 revolt by evidence, defending the top one in a paragraph |
| Be able to code loops | No criterion, so no pass mark exists | Write a `for` loop that sums a list, correcting an off-by-one error in a given example |
| Appreciate the poem | Nothing separates appreciation from silence | Identify two devices in an unseen stanza and state the effect of each |

- **Cognitive level is a choice, not decoration.** Bloom's revised levels (remember, understand, apply, analyse, evaluate, create) and SOLO (one idea, several ideas, related, extended) both exist to make you state the level before you assess it. Teach and test at the same level: teaching worked examples and testing transfer is the most common alignment failure.
- **One objective, one check.** Two objectives sharing a check means one of them is untested.
- Where `standards` is set, the objective quotes the specification wording and adds the criterion the specification omits (`curriculum.md`).

## The Prerequisite Check

Every objective depends on something already learned. Name the single most load-bearing prior idea and test it in the first five minutes (SKILL.md Rule 2).

- Format: one or two questions in the retrieval starter, whole-class response so the result is a count, not an impression.
- Decision, using the same 80/50 thresholds as every other check: ≥80% have it → proceed as planned; 50-79% → reteach the prerequisite in five minutes with a worked example and cut one item of today's content; <50% → today's lesson becomes the prerequisite lesson. The last case feels like failure and prevents a wasted week.
- Plan the fallback before the lesson, not during it. A plan without a "if the prerequisite check fails" line is a plan that will be improvised in front of thirty people.

## The Lesson Arc

Scales with `session_length_min`; the proportions hold, the minutes move. Shown for 50 minutes.

| Phase | Minutes | Purpose | Non-negotiable |
|---|---|---|---|
| Retrieval starter | 5-8 | Spaced practice plus prerequisite check | Written, on the board before entry, 2-2-1 mix (SKILL.md Rule 5) |
| Review of the starter | 3 | Correct the misconception before it is built on | Answers given aloud, not just collected in |
| Input chunk 1 | ≤10 | New element with a worked example | Ends with a whole-class response event |
| Guided practice | 8-10 | They do it, you circulate and read | Circulating means reading work, not policing |
| Input chunk 2 (optional) | ≤10 | Second element, only if chunk 1 passed at ≥80% | Cut it without regret when the check said 50-79% |
| Independent practice | ≥1/3 of the lesson | The only phase where learning is actually built | Protected — it is the first thing that gets eaten and the last that should |
| Exit check | 3-5 | What tomorrow starts with | ≤3 questions, collected, read the same day |

- **Independent practice under a third of the lesson is the reliable signature of a lesson that will not stick.** If the input took 25 of 50 minutes, the plan had too many elements.
- Timings in a plan are predictions; write the actual next to them afterwards, in `## Pacing` in that class file. Three lessons of that data is enough to see the size of your own habitual error — almost always over-estimating how much fits in a period — and the correction is to cut a phase, never to hurry the practice.

## Unit Design

- **Sequence by prerequisite, not by textbook order.** Draw the dependency graph for the unit's objectives; anything with two unmet dependencies is being taught too early. The textbook's order is optimised for printing, not for learning.
- **Interleave from the second unit onward.** Blocked practice looks better in the lesson and performs worse on a delayed test (Bjork). Every unit's starter draws on the previous two units.
- **Build in slack: one lesson in six with no new content.** It becomes reteach time when a hinge question comes back at 50-79%, and consolidation when it does not. A unit planned at 100% capacity is a unit that finishes three lessons late and lands the last objective with no practice.
- **Front-load the assessment.** Write the end-of-unit assessment before lesson one, and show students the form of it in the first week. Teaching toward a paper written afterwards is how coverage and assessment drift apart.
- **Name the misconception you expect.** Every unit has one or two famous wrong models (`subjects.md`); plan the lesson that confronts them rather than hoping they do not appear.

## Selecting Practice

| Practice type | Use when | Beware |
|---|---|---|
| Worked example | The procedure is new and the schema does not exist | Stops paying once accuracy is ≥80% (expertise reversal) |
| Completion problem | Between worked example and independent | Remove one step at a time, always the last step first |
| Minimally different pairs | The distinction is the point (`its`/`it's`, ionic/covalent) | Pairs must differ in exactly one feature |
| Interleaved set | Students can execute each type but cannot tell them apart | Feels harder and scores worse in the lesson; that is the mechanism |
| Retrieval quiz | Anything that must survive a week | Low stakes or no stakes, or it becomes a test |
| Extended task or project | Integration of several mastered objectives | Never as first exposure — it hides who cannot do the components |

## Planning for the Group You Have

- Apply the `## Needs` table from the class file to the plan itself: the printed copy, the extra time, the vocabulary pre-teach are part of the plan, not adjustments made at the door (SKILL.md Rule 9).
- Check `## Dynamics` before deciding groupings and seating.
- Check `## Pacing` before assuming the previous lesson happened as planned. Carried content is the most common reason a good lesson lands badly.

## What a Plan Must Contain

Under `plan_format: brief`, this is half a page; under `detailed`, each line expands; under `school-template`, these facts go into the school's form at `plan_template`.

1. Objective in observable form, with its criterion
2. The prerequisite and the question that tests it, plus the fallback if it fails
3. The check for each objective, written out verbatim
4. Timings by phase, summing to `session_length_min`
5. The worked example, written out — not "model the method"
6. The independent practice set, with the extension and the scaffolded route
7. The accommodations from the class file, named
8. The exit check, ≤3 questions
9. Materials and anything that must be prepared before the room fills

## Replanning Mid-Lesson

Three decisions, made from the check result, not the clock:

- **Check at 50-79%**: cut the next input chunk, reteach to the group that missed while the rest extend. The lesson finishes one objective short; that is the correct outcome.
- **Check at <50%**: stop the plan. Re-present in a different representation and re-check. Continuing produces a class where 60% cannot follow anything that comes next.
- **Check at ≥80% and 20 minutes left**: move to the extension task already in the plan, not to a new topic introduced without a check.

## Planning Faster

- Plan the unit once, the lessons in batches, and adapt from the artifact — never from a blank page. The single largest source of teacher time is the plan that already worked (`workload.md`).
- Steal structure, never wording: another teacher's worked example rarely matches your students' prior knowledge, but their sequence usually holds.
- Timebox: a lesson plan that takes longer than the lesson is unsustainable at four lessons a day. Under `plan_format: brief`, aim for a plan that takes 15-20 minutes when the unit already exists.

**When a lesson or unit plan actually worked**, write it to `~/Clawic/data/teacher/artifacts/<kebab-name>.md` with the timings that held, the part that ran late, and the misconception that appeared, then add its `## Boxes` line to `memory.md` in the same turn (`memory-template.md`). **When the lesson ran ahead or behind**, add the row to `## Pacing` in that group's class file with what was cut or carried — that is the field the next plan reads first.
