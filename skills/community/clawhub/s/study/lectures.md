# Lectures: Live, Recorded, and Backlogged

A lecture is the lowest-retention hour in a student's week and the one most often treated as the study itself. Its value is the map, the emphasis and the examiner's own phrasing — extracting those is a different job from being present.

**Contents:** [Before the Lecture](#before-the-lecture) · [During: Capture, Not Transcription](#during-capture-not-transcription) · [The 24-Hour Pass](#the-24-hour-pass) · [Recorded Lectures](#recorded-lectures) · [Playback Speed](#playback-speed) · [A Backlog of Recordings](#a-backlog-of-recordings) · [Reading the Examiner](#reading-the-examiner) · [Seminars, Labs and Problem Classes](#seminars-labs-and-problem-classes) · [When the Lecture Is Bad](#when-the-lecture-is-bad)

**Before a lecture in a course already tracked**, read the topic's row in `## Topics`: arriving with the previous lecture's content retrieved is what makes the new one comprehensible rather than a stream of unfamiliar terms.

## Before the Lecture

Ten minutes of preparation changes what the hour is worth:

- **Skim the slides or the corresponding chapter headings** and write three questions you expect answered. Attention has something to look for.
- **Retrieve last week's lecture in two minutes**, from memory. Lecture n+1 assumes lecture n; without the retrieval the first fifteen minutes are lost decoding vocabulary.
- Note the one thing that was confusing last time — it is the question to ask, and it is usually confusing to half the room.

## During: Capture, Not Transcription

The decision is where attention goes: a verbatim transcript costs the processing that makes the content usable, and processing without any record loses the specifics. Capture a skeleton:

- **Structure over sentences**: headings, the order of the argument, the transitions ("this is why X fails, which is why we need Y"). The order is content — it is usually the order of the exam question.
- **Verbatim only for**: definitions the lecturer emphasized, formulas with their conditions, worked example steps, and anything said twice.
- **Mark, do not solve, the gaps**: `?` for what was not understood, `!` for what was flagged as examinable. Two symbols, used consistently.
- **Copy worked examples completely**, including the steps that seem obvious in the room and will not be in three days.
- Leave space on the page. The 24-hour pass writes into it.

Type if you can resist transcribing; write by hand if you cannot. The reliable difference is transcription versus processing, not the tool (SKILL.md, Where Experts Disagree).

## The 24-Hour Pass

The step that converts a lecture into something learned, and the step almost universally skipped. Fifteen minutes, ideally after one night's sleep (Rule 9):

1. **Closed book, blank page**: what was the lecture about, in structure? Three to seven points.
2. Open the skeleton and fill what is missing, in a different colour. The difference between the two is what did not land.
3. Resolve every `?` — from the textbook, the slides, or a question to the lecturer. Unresolved gaps compound: lecture 8 is incomprehensible because lecture 5's `?` was never closed.
4. Convert the content into questions for the question bank, and cards only for the genuinely arbitrary items (`flashcards.md`).
5. Update the topic to state `seen` or `recalled once` in `## Topics` and schedule its first review (`spacing.md`).

A course where this pass happens weekly needs no revision period in the usual sense — revision becomes review of things already learned once.

## Recorded Lectures

Recordings invite the two worst study behaviours — passivity and infinite postponement — and remove the two constraints that made the live hour work.

- **Watch to a schedule, in the week the lecture belongs to.** A recording watched three weeks late has already broken the next three lectures.
- **Pause and predict**: before the lecturer answers their own question, answer it. Before the next step of a derivation, write it. This is the only thing that makes a recording better than a live lecture.
- **Never watch while doing something else.** The second task costs more than the speed saves, and the illusion of coverage is total.
- Rewinding to re-hear a sentence is cheap and correct; re-watching a whole lecture is not — the second watch is recognition (`retrieval.md`).
- Transcripts, where available, turn the recording into a searchable reference for the lookup mode of reading (`reading.md`).

## Playback Speed

Comprehension holds to roughly **2×** on recorded lecture material and degrades beyond it; 2.5× costs more than it saves. Practical rules:

- Start at 1.5× for familiar material, 1× for a first pass on anything with notation or derivations.
- Speed is not the saving; **skipping is**. Watching only the segments the slides say you need, at 1×, beats the whole thing at 2×.
- Watching twice at 2× is worse than watching once at 1× with a retrieval pass afterwards — the second watch adds recognition, the retrieval adds learning.
- If speed is being used to clear a backlog, that is a scheduling problem to fix rather than a comprehension budget to spend (below).

## A Backlog of Recordings

Twelve unwatched lectures is not twelve hours of work; it is a scope decision.

1. **Do not start at lecture 1.** Start at the most recent, so the live course becomes comprehensible again immediately.
2. **Triage the rest against past papers**: which of those topics is actually examined, and how heavily (`exams.md`)?
3. For the surviving ones, watch **slides plus the sections marked in the syllabus**, not the full recording. Then run the 24-hour pass.
4. Take the rest to zero explicitly and record the cut in `## Materials` with a reason. An unwatched backlog that nobody has cancelled generates guilt for the rest of term and no learning.
5. If several courses are backlogged simultaneously, the weekly grid was wrong (`planning.md`), and watching faster will not repair it.

## Reading the Examiner

Where the lecturer writes the exam, the lecture is primary source material about the exam:

- **Repetition is the strongest signal**: anything said twice, or appearing in two lectures, is examinable. Mark it.
- "You should know this", "this is a classic exam question", and any worked example done on the board are explicit tells.
- The lecturer's **phrasing and notation** are what the mark scheme uses. Where the textbook and the lecturer differ, answer in the lecturer's terms.
- Their research interests bias the long-answer questions in most courses.
- Cross-check the signals against the past-paper frequency table before reweighting the plan — emphasis in the room and frequency in the papers usually agree, and where they disagree the papers win unless the examiner changed (`exams.md`).

## Seminars, Labs and Problem Classes

- **Small-group classes are retrieval opportunities disguised as teaching.** Answer before the tutor does, even if only in your head; volunteering an answer that turns out wrong is the cheapest feedback available all term.
- Arrive having attempted the problem set. A problem class attended without an attempt is a demonstration, and demonstrations are recognition.
- **Labs**: read the protocol before arriving and know what result would falsify the experiment. The report is graded on the reasoning, and the reasoning is decided at the bench (`coursework.md`).
- Office hours have their own protocol — bring the attempt and the specific blockage (`groups.md`).

## When the Lecture Is Bad

Some lectures are genuinely not worth the hour, and pretending otherwise costs a term.

- **Test it honestly**: run the 24-hour pass twice. If the pass consistently produces nothing the slides did not already contain, the lecture is redundant for this student.
- Substitute the textbook, the slides plus the reading, or a well-regarded recorded course — then run the same pass on that instead. The pass is the invariant, not the source.
- **Attendance requirements are hurdles** and outrank this analysis entirely (`planning.md`).
- Record the verdict in `## Materials` with its date so the decision is not re-litigated every fortnight.

**After every lecture and its 24-hour pass**, update the topic's state and next review in `## Topics`, write unresolved gaps to `errors.md` with cause `never encoded`, and log the block in `session-log/<year>-<month>.md`. Where the reconstruction produced something durable — a clean derivation, a summary one-pager, the examiner's emphasis list for a course — it becomes `artifacts/<kebab-name>.md` with its `## Boxes` line (`memory-template.md`).
