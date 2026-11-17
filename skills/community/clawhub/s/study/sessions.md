# The Study Block Itself

A session is not a container for hours; it is a sequence with an entry, a retrieval, a struggle, and an exit artifact. Most wasted study is a block that skipped the entry and the exit.

**Contents:** [The Block Shape](#the-block-shape) · [Warm-Up That Is Not Wasted](#warm-up-that-is-not-wasted) · [Block Length and Breaks](#block-length-and-breaks) · [The Stuck Ladder](#the-stuck-ladder) · [Environment and Distraction](#environment-and-distraction) · [Working With the Agent in the Room](#working-with-the-agent-in-the-room) · [The Exit Artifact](#the-exit-artifact) · [The Consolidation Window](#the-consolidation-window) · [Reading the Session Log](#reading-the-session-log)

**Before a block on a course already in flight**, read `## Topics` for its state, `errors.md` for its open loops, and `## What Works` — this student's verdicts on technique outrank the defaults below.

## The Block Shape

Five phases; the first and last are the ones people drop, and they are the ones that make the middle worth anything.

| Phase | Minutes of a 50-minute block | What happens |
|---|---|---|
| Entry | 5 | Closed-book recall of the last session on this course: what were the three things? Missed ones open the block |
| Target | 1 | Name the outcome in one line — "explain the CLT unaided, then two problems solo". Written down, not thought |
| Work | 35 | Retrieval, problems, or reading-with-recall. One topic; switching mid-block costs the reload |
| Exit | 7 | Blank-page recall of what was just covered, then check it against the source and mark every gap |
| Record | 2 | The session row and every miss, written (`memory-template.md`) |

A block that runs out of time drops the Work phase, never the Exit. Forty minutes of study you cannot recall is worth less than twenty-five that you can.

## Warm-Up That Is Not Wasted

The first minutes are the hardest to start and the easiest to waste. The warm-up is itself a retrieval:

- Answer yesterday's missed questions from `errors.md`. It is the lowest-effort entry that exists and it is also the highest-yield item in the block.
- Or re-derive one formula or one definition from memory before opening anything.
- Never: re-reading the last session's notes, reorganizing files, "getting set up". These are the standard forms of not starting (`motivation.md`).

## Block Length and Breaks

- `session_minutes` sets the default (50); `break_minutes` (10) follows it; after four blocks, a long break of about 3× the short one.
- **The right length is measured, not chosen.** Log the minute at which attention visibly went (the log's `Notes` column). Two or three sessions establish this student's degradation point; from then on that number overrides the default and gets recorded under `work_order` in `config.yaml`.
- Short blocks (25) suit avoided tasks and memorization; long blocks (75-90) suit problem sets and writing, where the reload cost after a break is high.
- **A break is a break from the material, not from the screen.** Scrolling during the break carries the same load into the next block; standing, walking, water, and a window do not.
- Interrupting a fixed timer mid-flow is a worse trade than finishing the thought — a timer is a starting device, not a stopping one.

## The Stuck Ladder

Stuck is a state with a protocol, and the protocol is what stops both the doom-loop and the instant lookup.

1. **Two minutes of productive struggle.** The attempt before the answer is what makes the answer stick — looking it up at second zero converts a retrieval into a reading.
2. **Say the blockage precisely**: "I do not know which distribution applies", not "I do not get it". Half of stuckness dissolves at this step.
3. **Retrieve the neighbourhood**: what do I know that is adjacent? Which worked example is closest?
4. **One hint from the ladder** (SKILL.md Rule 8) — the principle, then the first step, then a worked analogue.
5. **Park it and move on** if two more minutes fail. Write it in `errors.md` as an open loop with the precise blockage; a parked problem often resolves on the next session's entry phase, and the ones that do not are the true curriculum.

Never spend more than about 15 minutes of a block on one stuck point. The marginal minute there is worth less than the next topic, and the parked item is now scheduled rather than lost.

## Environment and Distraction

- The measurable intervention is **removing the phone from the room**, not silencing it. Within reach is a different condition from in another room.
- **One tab rule for study, whatever the task**: the material and the notes. A search that opens a browser is a decision that ends the block for many students.
- Music: instrumental or nothing for reading and writing; anything works for mechanical drill. Lyrics compete with verbal material specifically.
- Same place, same time, same opening action is what makes starting cheap. The variable that matters is the ritual, not the desk.
- Context variation helps retention *across* sessions (study in two places, not one), while constancy helps starting. Vary the location between sessions, not within one.

## Working With the Agent in the Room

The default failure is the student watching a competent explanation and mistaking it for learning. The session runs the other way round:

- Quiz first, explain second, always. Ask before telling, even when telling is faster.
- After any explanation, immediately ask for it back in their words. An explanation not repeated back was not received.
- When they answer partially, mark the gap and re-ask rather than completing it for them.
- Time-box the explanations. If a concept has taken three attempts, the block is now a `learning` problem — change the representation (diagram, analogy, worked example) instead of repeating the same words louder.
- Never produce work that will be submitted (Rule 8, `integrity_mode`).

## The Exit Artifact

Every block ends with something the student produced from memory. Options, by material type:

| Material | Exit artifact |
|---|---|
| Conceptual | Blank-page explanation, then a diff against the source with every gap marked |
| Problem-based | Two solo solves with no notes, one of them from a different chapter |
| Fact-heavy | A recall test on the day's items, scored; missed items become tomorrow's entry |
| Reading | Three questions the text answers, written from memory, plus one it does not answer |
| Writing course | An outline from memory to a plausible exam question, timed |

The artifact is the evidence that the block happened. If nothing can be produced, the block was reading — record that plainly in the session log rather than logging the minutes as study.

## The Consolidation Window

- A topic first met today gets its **first retrieval after one night's sleep** (SKILL.md Rule 9). Same-day retrieval also helps, but the overnight one is what moves it from fragile to durable.
- **Study the hardest material before sleep, not the easiest** — the interval to the first sleep is short for evening study, which is exactly the material that benefits.
- A nap after a heavy encoding session is not a break from the protocol; it is part of it.
- Below 7 hours (AASM adult floor), stop adding evening blocks: the extra retrievals are bought with the mechanism that stores them.
- Exercise, food and daylight belong to the schedule for the same reason — but if sleep itself is the broken part, that is its own problem (`sleep`), not something to solve with study technique.

## Reading the Session Log

`session-log/<year>-<month>.md` answers questions no memory can:

- **Planned vs actual blocks** — below 70% for two weeks means the plan is wrong (`planning.md`).
- **Minutes per topic moved to criterion** — this is the real `hours_per_topic`, and it replaces the estimate in every future plan.
- **Blocks with no retrieval named** — if this is most of them, nothing else in the system matters yet.
- **Time of day against outcome** — the evidence that decides `work_order`, rather than a preference the student stated once.

**At the end of every block**, write its row to `session-log/<year>-<month>.md` — date, course, actual minutes, what was *retrieved* (never "read chapter 8"), miss count — and every miss to `errors.md` with its cause. If a topic changed state, update `## Topics` in the same turn. If a technique visibly worked or failed, that is a dated row in `## What Works` (`memory-template.md`).
