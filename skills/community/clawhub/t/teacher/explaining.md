# Explaining — Direct Instruction That Survives Contact

An explanation fails for one of four reasons: too many new elements at once, no concrete referent, the wrong representation, or a competing model already in the student's head that was never addressed. Diagnose which before rephrasing anything.

**Contents:** [The Representation Ladder](#the-representation-ladder) · [Worked Examples and Fading](#worked-examples-and-fading) · [Managing Load](#managing-load) · [Analogies That Do Not Backfire](#analogies-that-do-not-backfire) · [Examples, Non-Examples, Contrast Pairs](#examples-non-examples-contrast-pairs) · [Modelling Out Loud](#modelling-out-loud) · [Board, Slides and Handouts](#board-slides-and-handouts) · [Vocabulary](#vocabulary) · [Confronting a Wrong Model](#confronting-a-wrong-model) · [Live Demonstrations and Code-Alongs](#live-demonstrations-and-code-alongs) · [When the Explanation Still Fails](#when-the-explanation-still-fails)

**Before reteaching a topic that already failed once**, read `## Explanations That Landed` and `## Misconceptions` in `~/Clawic/data/teacher/memory.md` for that topic. Re-deriving the analogy that worked last year is a wasted hour; repeating the explanation that failed last week is worse than a wasted hour.

## The Representation Ladder

When an explanation does not land, move **down** one rung, never sideways into more words at the same rung.

| Rung | Form | Use |
|---|---|---|
| 5 | Formal / symbolic | The destination: notation, definition, general rule |
| 4 | Verbal abstraction | "Force equals rate of change of momentum" |
| 3 | Diagram / graph / structured visual | Relations that words serialise badly |
| 2 | Concrete worked case with real numbers | Where most reteaching should start |
| 1 | Physical or lived referent | Objects, the student's own experience, a demonstration |

- Moving down is not dumbing down: the destination is unchanged, the route is shorter. The failure mode is teaching at rung 4 twice and concluding the student cannot learn it.
- Dual coding — spoken words plus a diagram — beats either alone; spoken words plus the *same* words on a slide is worse than either, because the two channels compete (redundancy effect, Sweller).
- Return upward explicitly. A concrete case that is never generalised produces students who can do that example only.

## Worked Examples and Fading

For a novice, studying a worked example produces more learning per minute than attempting the problem (worked example effect, Sweller). The sequence:

1. **Full worked example** — every step shown, the reason for each step said aloud, including the step where you decided *which* method applies. That decision is the step experts skip and novices most need.
2. **Completion problem** — the same problem with the last step removed. Then the last two. Removing from the end preserves the model of where you are going.
3. **Independent** — once accuracy on completion problems is ≥80%.
4. **Interleaved independent** — mixed with other problem types, so recognition is practised, not just execution.

Ratios that work in practice: for a genuinely new procedure, roughly 2 worked examples per 1 attempted problem at the start, inverting within the lesson as accuracy climbs. Keeping worked examples once students are fluent slows them down (expertise reversal, Kalyuga) — the same material helps novices and harms experts, which is why "always model first" is wrong as a blanket rule.

## Managing Load

Working memory holds about four elements at once (Cowan). Everything below buys elements back:

| Technique | What it frees |
|---|---|
| Pre-teach the vocabulary | Words stop consuming slots meant for the concept |
| Give the diagram already labelled | Labelling is a second task competing with the first |
| Split-attention fix: put the text *on* the diagram | Eyes moving between a figure and a caption pay a load tax |
| Remove decorative images, animations, background music | Seductive details reduce retention of the actual content |
| One worked example on screen while they attempt the next | Removes the memory demand of holding the method |
| Automate the sub-skill first | A student computing arithmetic by hand has no capacity for the algebra above it |

The signature of overload: students copying accurately, answering nothing, and asking procedural questions ("do we write the date?"). That is a capacity signal, not a motivation signal.

## Analogies That Do Not Backfire

- **State the mapping and the limit in the same breath.** "Current is like water in a pipe — pressure is voltage, flow rate is current. It breaks where the water can leak out and charge cannot." Unbounded analogies become the misconception you spend next term removing.
- Two weak analogies beat one strong one: comparing where they agree isolates the actual structure.
- The analogy must be more familiar than the target to the *student*, not to you. A budget analogy fails on a fourteen-year-old who has never had one.
- Retire the analogy explicitly once the formal model works. Students who still reason in the analogy at exam time answer questions about pipes.

## Examples, Non-Examples, Contrast Pairs

- Present examples that vary everything except the defining feature, and non-examples that vary only the defining feature. That combination is what makes the boundary visible.
- **Minimally different pairs** are the strongest form: two items differing in exactly one respect, side by side. `3x + 2 = 11` next to `3(x + 2) = 11`; a metaphor next to the same sentence as a simile; a correct and an incorrect commit message.
- Range matters: three examples all from the same context teach the context, not the concept.

## Modelling Out Loud

Think-aloud modelling makes the invisible expert process audible. What to narrate, in order of value:

1. **How you decided what kind of problem this is** — the single most skipped step
2. Where you were unsure, and how you resolved it
3. The check you performed and what would have made you go back
4. The wrong turn you did not take, and why

Read the whole model before writing anything, then write while narrating. A silent model teaches the product; a narrated model teaches the process. Students should be able to name your first question, not just copy your final answer.

## Board, Slides and Handouts

- **The board keeps the trace; slides erase it.** For anything cumulative, work on a surface where the earlier steps stay visible. Slides that advance destroy the very working memory support the student needs.
- One idea per slide, and never read the slide aloud (redundancy effect). If the words must be there, say something different while they read, or say nothing.
- Handouts with gaps outperform both blank note-taking and complete handouts for novices: the gaps direct attention without spending the lesson on transcription.
- Anything worth copying is worth giving. Copying from the board is a legibility exercise; the learning is in the practice you cut to make room for it.

## Vocabulary

- Teach the word, its definition in student language, an example, a non-example, and the false friend it collides with ("volume" in maths versus in music; "significant" in statistics versus in speech).
- Etymology and morphology repay their cost in subjects dense with Greek and Latin roots — a student who knows *photo-*, *-synthesis*, *thermo-*, *-lysis* decodes dozens of unseen terms.
- Require the word in output. A term that students never say or write is one they will not recognise under exam pressure.

## Confronting a Wrong Model

Coverage does not remove a misconception; the old model survives alongside the new one and resurfaces under pressure. The sequence that works:

1. **Elicit** — ask a question whose wrong answer exposes the model, and get a public commitment (whiteboards, poll). Commitment matters: an unstated belief is not revisable.
2. **Predict** — have them predict what the wrong model implies in a case where it clearly fails.
3. **Confront** — run the demonstration, show the data, work the counter-case.
4. **Resolve** — state the correct model and explicitly say what the old one got right and where it stops.
5. **Re-check later** — a delayed check the following week, because the old model returns when the new one is not yet automatic.

A student who is corrected while confident and then re-tested remembers the correction better than one who was unsure (hypercorrection effect, Butterfield and Metcalfe) — high-confidence errors are the most productive ones to catch.

## Live Demonstrations and Code-Alongs

- **Prepare the failure.** A demo that always works teaches nothing about diagnosis; a planned, recoverable failure teaches the debugging move.
- Type or work slower than feels natural, and stop at each decision point to ask for the next step from the class before doing it.
- **Nobody types while you type** in a code-along unless the whole class is at ≥80% on the previous step; otherwise half the room is transcribing and hearing nothing (`subjects.md`).
- Have the finished state available. When a live demo breaks unrecoverably, the lesson continues from the artifact rather than dying.

## When the Explanation Still Fails

Work down this list; stop at the first that fits.

| Check | If yes |
|---|---|
| Is the prerequisite actually in place? | Reteach that instead — today's topic is not the problem (`planning.md`) |
| More than about four new elements? | Split across two lessons; nothing else will help |
| Was it verbal at rung 4-5 only? | Drop to rung 2 with real numbers |
| Is a competing model in play? | Elicit-predict-confront, above |
| Is the vocabulary the barrier? | Pre-teach the five words and re-run the same explanation |
| Was there any student response between input and confusion? | There was no check; you are debugging blind (`checking.md`) |
| Correct in guided practice, wrong alone? | The scaffold was never faded — go back to completion problems |

**When an explanation, analogy or worked example finally lands**, add the row to `## Explanations That Landed` in `~/Clawic/data/teacher/memory.md`: topic, what worked, and why it worked. **When a wrong answer recurs across students or years**, add it to `## Misconceptions` with the question that catches it. Both sections split to `explanations.md` and `misconceptions.md` at the threshold in `memory-template.md`, keeping the same headings. These two lists are the highest-return records this skill keeps: they turn next year's hardest lesson into a ten-minute preparation.
