# Retrieval Practice

Testing is not measurement of learning; it is the event that produces it (Roediger & Karpicke). Every technique in this file is a way of forcing an unaided attempt before the material is available again.

**Contents:** [The Four Retrieval Formats](#the-four-retrieval-formats) · [Writing Questions Worth Answering](#writing-questions-worth-answering) · [Blank-Page Recall](#blank-page-recall) · [Feedback: What and When](#feedback-what-and-when) · [Desirable Difficulties](#desirable-difficulties) · [The Fluency Illusion](#the-fluency-illusion) · [Free Recall for Big Structures](#free-recall-for-big-structures) · [Retrieval for Skills, Not Facts](#retrieval-for-skills-not-facts) · [Common Failures](#common-failures)

**Before a retrieval session on a topic already touched**, read its row in `## Topics` and its open loops in `errors.md`: the questions this student already failed are better retrieval items than any new ones.

## The Four Retrieval Formats

Ordered by difficulty; harder means better retention, and unanswerable means wasted.

| Format | Cue given | Use when |
|---|---|---|
| Free recall | Topic name only — "everything about renal clearance" | End of a topic, or entry phase of a session; reveals structure and holes at once |
| Cued recall | A question or a prompt — "what does a low p-value license you to say?" | The normal working format; most exam questions live here |
| Recognition | Options presented | Only when the exam itself is recognition, and even then paired with cued recall first |
| Generation | Produce the answer *and* the question — "write the exam question this paragraph answers" | Deep processing on reading, and the best way to build a question bank (`notes.md`) |

Move up the ladder as the topic strengthens: recognition passes long before free recall does, which is exactly why recognition practice overstates readiness.

## Writing Questions Worth Answering

A question is worth answering if a wrong answer is *informative*. Three tests:

- **One retrieval per question.** "Explain the whole chapter" is a session, not a question. "What are the three assumptions of a t-test, and which one fails with paired data?" is a question.
- **Not answerable from the wording.** "Is the CLT important?" retrieves nothing. Strip words that give away the answer.
- **Asked the way it will be asked.** Convert past-paper stems into practice questions verbatim before inventing your own — the phrasing of the exam is itself content (`exams.md`).

Question sources, in descending value: past papers → the student's own generated questions → end-of-chapter problems → questions written by anyone else. The student generating them is a retrieval on its own.

## Blank-Page Recall

The highest-yield ten minutes available and the cheapest to run.

1. Close everything. Write the topic name at the top.
2. Write everything recallable: definitions, steps, formulas, relationships, one worked example, and the boundaries — where it does not apply.
3. Stop when nothing more comes, wait 30 more seconds, then stop for real. The last items are the fragile ones.
4. Open the source and mark up in a second colour: **missing**, **wrong**, **vague**. Only the *wrong* ones are urgent; missing is normal on the first pass.
5. The marked page is the next session's entry list. Every wrong or vague item becomes a row in `errors.md` with its cause.

Run it after reading a chapter, at the end of every block, and before every exam. Its value is the diff, not the page.

## Feedback: What and When

- **Feedback is mandatory.** Retrieval without feedback lets a confidently wrong answer consolidate — the one case where testing actively harms.
- **Delay it slightly** rather than showing the answer instantly: finishing the set, then checking, beats item-by-item reveal. The delay forces commitment and prevents copying the answer forward.
- **Correct answer plus the reason**, not just right/wrong. A miss with no explanation gets re-missed on the same grounds.
- **A wrong answer given confidently is the most valuable item in the set** — the hypercorrection to it is durable, provided the correction actually happens.
- Self-marking against a rubric or a mark scheme is a second retrieval and is how essay and long-answer practice gets feedback at all (`subjects.md`).

## Desirable Difficulties

Conditions that slow practice and improve retention (Bjork). Each feels worse and tests better:

| Difficulty | What it costs | What it buys |
|---|---|---|
| Spacing instead of massing | Practice accuracy looks worse | Durable retention (`spacing.md`) |
| Interleaving instead of blocking | Slower, more errors during practice | Discrimination between confusable procedures |
| Generation instead of reading | Effort, and being wrong | Stronger encoding of the generated item |
| Varying the conditions | Feels inconsistent | Retrieval that transfers to a different room and a different phrasing |
| Testing instead of restudying | Feels like it is not "learning" | The largest single effect available |

The trap they share: **the technique that feels most productive is generally the one producing the least durable learning**. Fluency during practice is not evidence, which is why `## What Works` records outcomes rather than impressions.

## The Fluency Illusion

Recognition, familiarity and having just read something all produce the sensation of knowing. Three tests that break the illusion:

- **Close the book earlier than feels reasonable.** If the notes are open, the notes are doing the retrieval.
- **Delay before judging.** Judge readiness on a test taken at least a day later, never at the end of the study session.
- **Change the surface.** Ask it in the past paper's wording, in a different order, with different numbers. Fluency is tied to the surface form; knowledge is not.

"It feels easy now" is a prediction, and it is scheduled for verification, not believed.

## Free Recall for Big Structures

For material whose difficulty is organization rather than fact count — a legal framework, a metabolic pathway, a historical period, a codebase's architecture:

- Recall the **skeleton first**: what are the top-level parts, and in what order? Then descend one level per pass.
- Draw the map from memory, then diff against the source. The drawing is a retrieval; a map copied from the book is not (`notes.md`).
- Rebuild it from a different entry point each time — from the end of the pathway backwards, from the exception to the rule — because a structure recallable from only one starting cue fails on an exam question that enters elsewhere.

## Retrieval for Skills, Not Facts

Procedures are retrieved by executing them, and the format changes accordingly:

- **Maths and physics**: solve unaided, no worked example in sight. Reading a solution and following it is recognition (`subjects.md`).
- **Code**: write it in a blank file, run it, and let the error message be the feedback. Reading a tutorial is not practice.
- **Language**: produce a sentence before checking it; passive review of a vocabulary list is recognition, and speaking is the hardest and most transferable retrieval.
- **Clinical and practical**: verbalize the sequence from memory, then perform it against a checklist. The checklist is the mark scheme.

## Common Failures

| Failure | Why it happens | Fix |
|---|---|---|
| Reading the question and thinking "I know this", then moving on | Recognition satisfies the sense of knowing | Say or write the answer fully — a retrieval not produced did not happen |
| Testing only on the material just studied | Everything is still in working memory | Test on the *previous* session's material at the start of this one |
| Practising only the questions that get answered correctly | Comfort, and a scoring habit | Sort the set by miss history; the failed items are the set |
| Giving up when the first attempt is blank | Blank feels like proof of failure | Blank on a first attempt is the normal starting state, and the attempt still improves the subsequent study |
| Retrieval only from cards | Cards are cued recall of atomic items | Add free recall and problems — an exam asks neither in card form (`flashcards.md`) |

**After a retrieval session**, write every miss to `errors.md` with its cause (SKILL.md Rule 6) and update the topic's `State` and `Last retrieved` in `## Topics`. A generated question bank that will be reused belongs in `artifacts/<kebab-name>.md` with its `## Boxes` line — questions written once and lost are the most commonly re-created artifact in this domain (`memory-template.md`).
