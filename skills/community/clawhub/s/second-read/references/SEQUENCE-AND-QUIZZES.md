# Reading-order understanding checks and thread highlighting

## What to model

Extract the ordered list of blocks in the **reader's actual path**, not the author's private outline. Every block may participate in an argument thread (claim/evidence/example/counterargument/implication). When one block contains several threads, record explicit span offsets in richer clients; the bundled demo uses paragraph-level primary threads. Related passages share a stable color **and a visible text label**. Color is an aid, never proof that the relationship is correct.

Detect sequence friction:
- **Unintroduced claim:** the conclusion precedes its required context.
- **Orphan example:** a vivid case lacks an interpretable general point when the genre requires one.
- **Unillustrated abstraction:** the claim is too general for the intended audience to test mentally.
- **Separated dependency:** proof or qualifications appear far from the claim they support.
- **Meaning switch:** terms, referents, voice or level of certainty shift midway.
- **Premature commitment:** the opening implies a stronger policy, product or offer than the body supports.

Suggest *specific text operations*, not abstract notes such as “improve flow.” A move must state what relocates and where; a bridge must supply actual text; a clarification must give its revised wording. Explain how this changes the reading sequence.

## Quiz design

Add a question only when the answer changes an editing decision. Place it immediately **after the passage being tested**. Sequence questions in the same order as their source positions. A useful question asks what the reader can legitimately infer **so far**, not after seeing later evidence.

For each question provide:
- `after_block_id`: exact position in original reading order.
- `prompt`: e.g., "At this point, are you promising an immediate citywide change or proposing a pilot?"
- `choices`: two to four legitimate interpretations, no caricatures.
- `reading_id`: one evidence-grounded plausible cold reading, **not the author's required answer**.
- `suggestion_id`: a specific proposed wording/structural change if divergence matters.
- `why`: cite text and distinguish context provided later.

If the author chooses a different interpretation, say **“That differs from a plausible first reading at this point”**. Highlight the linked thread and affected passage, show the actual proposal, and invite accept/reject. Do not call it a wrong answer or grade the writer. If different readings are intentional, the author can reject the edit. For quizzes testing unsupported factual implications, clarify what is observed versus inferred.

## When the interactive editor is unavailable (ordinary chat)

Keep the existing proposed edits, explanations and revision format. Change **only how relevant sequence questions appear**:

- Label the annotated excerpt(s) **Questions to yourself after reading this once**. Do not use the words "quiz", "test", "wrong", or a score for the writer.
- Place **each question immediately after its exact original sentence or paragraph**, preserving the text's actual reading order. Use a paragraph ID/heading and an **unchanged, verbatim quote**. If the draft is short, the full original with inline annotations is acceptable; for a long draft, show only anchored excerpts in reading order rather than republishing the whole document.
- Ask what a new reader has understood **by that point**, why a particular example is there, or which premise the next claim depends upon. If another passage supplies the missing context, cite its paragraph ID rather than moving the question to the end.
- Include a question **only if it could change a specific proposed edit**; prefer one or two, maximum three. Do not force a question into clear writing. Do not require answers as a prerequisite for showing the edit proposals.
- A question is an editorial annotation, **never part of the author's prose** or the revised/exported version. Maintain legible text labels even if argument threads are described with colors.

Example of placement (hypothetical):

> **P1, original:** "Every city should make night buses free starting next month."
>
> **Questions to yourself after reading this once — after P1:** At this point, have you asked the reader to support an immediate fare change, or a trial that might lead to one?

> **P3, original:** "A six-month pilot could help us find out."
>
> **Questions to yourself after reading this once — after P3:** Does the reader now know whether the pilot will improve reliability or merely measure the problem?

Link both questions to the relevant existing editing proposals. Do not add an answer key or claim that the author's intention is known unless their supplied context establishes it.

## Sample

Source order:
1. “Everyone should get free night buses tomorrow.” [proposal, purple]
2. “Picture a nurse waiting an hour after a night shift.” [example, teal]
3. “We should test reliability on two routes for six months.” [test/verification, amber]

Ask after block 1: “What have you asked the reader to support at this point?” The cold reading is immediate universal free fares. The author brief says limited reliability trial. Proposed replacement: “The city should test night-bus reliability on two routes before changing fares.” This example is hypothetical; the nurse is an illustration, not measured evidence.
