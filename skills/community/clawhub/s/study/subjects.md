# Playbooks by Subject Type

The technique is chosen by what the material *is* and what the assessment *asks*, never by preference. Most subjects are a mix; classify each topic, not the course.

**Contents:** [Classify the Topic First](#classify-the-topic-first) · [Problem Subjects](#problem-subjects) · [Memorization-Heavy Material](#memorization-heavy-material) · [Conceptual and Theory Material](#conceptual-and-theory-material) · [Writing-Based Subjects](#writing-based-subjects) · [Languages](#languages) · [Programming](#programming) · [Lab, Clinical and Practical](#lab-clinical-and-practical) · [Verbatim Material](#verbatim-material)

**Before starting a topic**, read its row in `## Topics` and its history in `errors.md`. The error causes decide the playbook as much as the subject does: `out of time` on a problem subject is a fluency programme, not a restudy programme.

## Classify the Topic First

| The topic is… | Test | Primary practice |
|---|---|---|
| A procedure to execute | "Can I do it, unaided, on a new instance?" | Worked example → faded → solo → interleaved |
| An arbitrary pairing | "Is there any logic connecting these two?" — no | Cards, mnemonics (`flashcards.md`) |
| A structure to reconstruct | "Can I draw the whole thing from memory?" | Free recall, maps from memory |
| An argument to deploy | "Can I defend and attack it in five minutes?" | Timed outlines, argument blocks |
| A physical or clinical skill | "Could I do this with hands, under time?" | Rehearsal against a checklist |
| A discrimination between similars | "Do I mix these two up?" | Interleaved practice on the pair (`spacing.md`) |

A single chapter usually contains three of these. Applying one technique to all of them is the most common cause of "I studied everything and still failed".

## Problem Subjects

Mathematics, physics, engineering, quantitative chemistry, statistics, quantitative economics.

**The acquisition sequence**, in order, and skipping steps is why practice stops working:

1. **Study a worked example actively**: cover the next line, predict it, uncover, compare. A worked example read straight through teaches nothing (Sweller's worked example effect applies to *studied* examples).
2. **Faded practice**: the same problem with the last step removed, then the last two, until nothing is given.
3. **Solo solves**: two to three correct, unaided, from cold, on different instances.
4. **Interleave** with the neighbouring methods once solo solves succeed — this is where selection is learned (`spacing.md`).
5. **Timed**, at the exam's seconds-per-mark, once selection is reliable.

Rules that decide outcomes:

- **Start every problem by naming the method and why**, before any algebra. Most exam losses in problem subjects are selection errors, and the algebra was fine.
- **Attempt for a genuine ten minutes before looking.** Then look at *one line* of the solution, not the whole thing, and continue.
- **Re-solve every problem you got wrong, from blank, within 48 hours.** Reading your own corrected solution is recognition and it is why the same mistake reappears in the exam.
- **Redo old problems from cold rather than doing new ones** when the topic has already been practised: novelty feels productive and mostly retests what already works.
- **Sanity checks are content**: units, sign, limiting cases, order of magnitude. Build the check into the procedure and half of the `procedure slip` category disappears.
- Keep a **problem-solution log** rather than a solutions file: the problem, the approach, why that approach, and where it broke (`notes.md`).

## Memorization-Heavy Material

Anatomy, pharmacology, taxonomy, statute and case names, historical dates, vocabulary, medical terminology.

- **Card only the arbitrary**, atomically (`flashcards.md`). Anything derivable from a principle is practiced as a problem instead.
- **Mnemonics are for arbitrary pairings and orderings only** — where there is no logic to reconstruct from, they are high-value; where there is, they replace understanding with a fragile string.
- **A memory palace works for ordered lists** (cranial nerves, a statute's elements, a process order) and is worth the setup only for lists you will need for years. Record the palace layout in `artifacts/` — its value is entirely in reuse.
- **Study confusable items together**, deliberately, then drill the discriminator. Learning them a week apart guarantees interference at the exam (`spacing.md`).
- **Chunk by structure, not alphabetically**: drug classes by mechanism, bones by region, vocabulary by semantic field. Alphabetical order is an arbitrary index imposed on content that has a real one.
- Volume is the trap: a 900-card deck for one course is a daily tax that consumes the hours the problem-based half of the course needed (`spacing.md`, capacity math).

## Conceptual and Theory Material

Physics concepts, philosophy, economics, psychology, biology mechanisms, theory-heavy computer science.

- **Explain it from memory to a naive listener, out loud** (the Feynman procedure): where the explanation stalls or turns into jargon is exactly the gap. Then study only that gap and re-explain.
- **Analogies are diagnostic and dangerous**: use one, then immediately state where it breaks. An analogy without its boundary produces confident wrong answers on transfer questions.
- **Ask "what would falsify this?"** for every theory. Exam questions about theories are usually about their limits and their competitors, not their statements.
- **Compare theories in a table** — assumptions, predictions, evidence, failure cases. The comparison is the examinable structure; the individual summaries usually are not.
- **Apply it to a new case immediately.** A concept understood only on the textbook's example is bound to that example.
- Self-explanation while reading ("why is this step true?") rates moderate-utility and costs nothing extra (`retrieval.md`).

## Writing-Based Subjects

Literature, history, law, politics, sociology, essay-based sciences.

- **Practice the outline, not the essay.** Ten timed outlines from memory beat one polished essay for exam preparation: the exam skill is selecting and ordering evidence under time.
- **Build reusable argument blocks**: a position, its two strongest supports with sources, and its strongest counter. Most exam questions recombine blocks rather than requiring new material.
- **Read the mark scheme or rubric first**, and mark your own practice against it. Most marks are lost against criteria the student never read (`coursework.md`).
- **Prepare the counter-argument for every position** you would defend — the discriminating marks live there.
- Memorize **evidence, not sentences**: dates, names, quotations short enough to be exact, and case citations. Pre-memorized prose reads as pre-memorized and rarely answers the question asked.
- **Answer the question asked**: underline the command word (evaluate, compare, to what extent) and the constraint, and structure the answer around it. Off-question brilliance scores zero.
- For a viva or oral, practise **aloud to a person or a recorder**, with follow-up questions (`groups.md`).

## Languages

- **Comprehensible input plus forced production**, daily. Neither alone works: input builds recognition, production builds retrieval, and only production transfers to speaking and writing exams.
- **Card only arbitrary pairings** — vocabulary, irregular forms, gendered nouns, collocations. Grammar rules are practised by producing sentences, not by carding the rule statement.
- **Sentence cards beat word cards** for anything context-dependent: a word learned in isolation is unusable in production.
- **Cover the productive direction** where the exam is productive: L1→L2 costs more reviews and is the one the exam asks for.
- **Speaking is a separate skill from everything else** and degrades fastest without practice. If the exam has an oral, schedule it as its own block from week one, not as revision.
- Listening at 1× with a transcript afterwards; slowed audio trains a skill nobody tests (`lectures.md`).

## Programming

- **Write code in a blank file, run it, read the error.** Reading tutorials and following along is recognition; the compiler is the fastest feedback in any subject.
- **Retype worked examples from memory** rather than copying, then diff. The diff is the lesson.
- For exams **written by hand or without a compiler** (still common), practise exactly that way: no autocomplete, no run button, and syntax carded like vocabulary.
- **Debugging is examinable and rarely practised**: take working code, break it deliberately, and diagnose. Also the best preparation for the practical.
- Complexity, data structures and algorithm selection are **conceptual** material — explain from memory and compare, do not card.
- Read error messages as content, and keep the recurring ones with their causes in `errors.md` under `procedure slip`.

## Lab, Clinical and Practical

- **Rehearse the sequence verbally from memory, then perform it against a checklist.** The checklist is the mark scheme and is often published.
- **Know what result would falsify the experiment** before the bench. Practicals are graded on reasoning and safety far more than on the number obtained.
- **Safety-critical steps get their own drill** and are never left to general familiarity.
- **Time each attempt.** Practical exams are usually time-limited, and the untimed rehearsal always feels adequate.
- **OSCE-style clinical stations** are a scripted format: practise the script, the sequence, and the communication marks, which are usually a third of the sheet and the cheapest to earn.
- The procedure checklist that finally worked is an artifact worth keeping (`memory-template.md`).

## Verbatim Material

Formulas to be reproduced exactly, quotations, scripts, statutes, code syntax, musical passages.

- **First-letter cueing**: write the first letter of every word, recite from that, then drop the cue. It is the standard route to verbatim recall and it is fast.
- **Criterion is flawless**, twice, on separate days. Approximate verbatim material scores zero in the contexts that require it.
- Chunk into units of a few words and chain them; whole-passage repetition is slow and fragile.
- Write it out, do not just recite it, where the exam requires writing — the motor act is part of what is being trained.

**When a topic's playbook is chosen and run**, update its `State` in `## Topics` and log the block in `session-log/<year>-<month>.md`. Every miss carries its cause to `errors.md`, and a playbook that visibly worked or failed for this student is a dated row in `## What Works` — the subject-type default is a starting point, and this student's record outranks it (`memory-template.md`).
