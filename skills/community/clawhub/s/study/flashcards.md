# Cards: What to Card, How to Write It, How to Keep the Deck Alive

A card is a permanent daily subscription. The craft is deciding what deserves one and writing it so it can be answered — deck mechanics, scheduler settings, imports and sync belong to the `anki` skill.

**Contents:** [What Deserves a Card](#what-deserves-a-card) · [The Atomicity Rule](#the-atomicity-rule) · [Card Shapes](#card-shapes) · [Writing Rules](#writing-rules) · [Deck Structure](#deck-structure) · [Introducing New Cards](#introducing-new-cards) · [Leeches](#leeches) · [Shared and Pre-Made Decks](#shared-and-pre-made-decks) · [Reviewing Well](#reviewing-well) · [Retiring a Deck](#retiring-a-deck)

**Before creating or triaging any deck**, read `## Decks` in `~/Clawic/data/study/memory.md` for the current card counts and steady-state load, and `errors.md` for which items keep failing — a card that has failed four times is a writing problem, not a memory problem.

## What Deserves a Card

The test is one question: **can this be derived?**

| Content | Card? | Why |
|---|---|---|
| Vocabulary, terminology, drug names, anatomical structures | Yes | Arbitrary pairings, nothing to reconstruct from |
| Dates, statutes, article numbers, named cases | Yes | Same — no logic connects the label to the thing |
| A formula you must produce under time, whose derivation you know | Yes, as a recall card | Fluency is the goal, not understanding |
| A formula whose derivation is the exam content | No | Practise the derivation as a problem |
| A procedure with steps | Only the step *list*, as a cloze | The execution is trained by executing, not by recall |
| A concept, mechanism, or argument | No | Free recall and explanation cover it far better (`retrieval.md`) |
| Anything not yet understood | No | It becomes a leech within a fortnight (Traps) |
| Something appearing in one lecture and never again | No | Frequency check against past papers first (`exams.md`) |

Ten well-chosen cards per topic beat a hundred generated ones. The permanent cost of a card is what makes the selection matter: a 900-card deck at typical settings costs 20-30 minutes a day for months.

## The Atomicity Rule

**One card, one retrieval.** A card asking for three things fails when any one is missing, and the failure teaches nothing about which.

- Bad: "Describe the renin-angiotensin system." — that is a free-recall exercise, not a card.
- Good: "Renin is released by which cells?" · "Angiotensin II acts on which receptor to cause vasoconstriction?" · "ACE converts what to what?"
- The compression test: if the answer needs a comma-separated list of more than about three items, split it or make it a cloze with one blank per card.

Enumerations are the standard exception and the standard trap: a five-item list becomes five cloze cards on the same sentence, not one card with five blanks — otherwise the first two items cue the rest and nothing is being retrieved.

## Card Shapes

| Shape | Best for | Watch out for |
|---|---|---|
| Basic (front → back) | Terminology, definitions, arbitrary facts | Ambiguous fronts that could have several right answers |
| Reversed (both directions) | Vocabulary where production matters | Doubles the review load — only where the reverse direction is genuinely needed |
| Cloze deletion | Facts that need their sentence for context; step lists; statutes | The surrounding sentence giving the answer away |
| Image occlusion | Anatomy, diagrams, maps, circuit layouts, UI screens | Occluding the label but leaving the position obvious |
| Type-in | Spelling, formulas, code syntax, precise notation | Slowing reviews to a crawl; use only where exactness is the point |

## Writing Rules

- **The front must have exactly one right answer.** "What is the treatment?" has many; "First-line treatment for uncomplicated hypertension in a patient under 55, per the current guideline?" has one. Ambiguity produces a card you mark wrong while knowing the material.
- **Add the minimum context that disambiguates**, and keep it on the front: the course, the chapter, the patient type, the language direction.
- **Write in your own words**, from memory, after understanding. Copy-pasted cards fail because the phrasing was never processed.
- **No card whose answer is "it depends"** without the deciding condition in the front.
- **Include the discriminator for confusable pairs**: if two items keep swapping, one card should explicitly ask what distinguishes them (`spacing.md`, interleaving).
- **Cards are made after the first successful unaided recall**, never during the first reading. A card is a maintenance tool, not a learning tool.

## Deck Structure

- **One deck per course**, subdecks by topic only when a topic must be studied in isolation before an assessment. Deeper hierarchies produce a deck nobody reviews as a whole.
- Tag by topic and by source (`ch08`, `past-paper-2023`) — tags survive reorganization and are how you pull a filtered set before a specific exam.
- **Never split a deck by "hard/easy"**: the scheduler already does that, and the split guarantees the hard deck gets skipped.
- Register each deck in `## Decks` with its app, card count, new/day and observed reviews/day. The deck lives in the app; the registry lives here, and duplicating the cards into `memory.md` guarantees the two diverge.

## Introducing New Cards

- `daily_review_cap` decides `new/day`, not the other way round: steady-state reviews land near **10× the new rate** (`spacing.md`). To stay inside 25 minutes at ~6 s/card, that is roughly 250 reviews — so about 25 new cards a day, across all decks combined.
- **Front-load introductions early in a course** so every card gets several spaced reps before the exam. Cards added in the last fortnight are cramming with extra steps.
- When a backlog exists, new cards are zero until it clears. No exceptions — this is the decision that decides whether the deck survives the term.
- Do not introduce cards for a topic still at state `seen`. Understand, retrieve once unaided, then card it.

## Leeches

A card that keeps lapsing — Anki's default threshold is 8 lapses, at which it tags and suspends the card. That default is well-chosen: eight failures is decisive evidence.

Diagnose before rescuing, in this order:

1. **Is the card ambiguous?** Multiple defensible answers is the most common cause. Rewrite the front.
2. **Is it a compound?** Split into atoms.
3. **Was the material ever understood?** Suspend the card, study the concept, then rewrite it.
4. **Is it interference with a sibling card?** Make a discriminator card that asks for the difference explicitly, and study the pair together.
5. **Is it worth knowing at all?** Delete it. A deleted low-yield leech is a win, not a defeat — check against past-paper frequency first.

Run a leech sweep monthly (`## Due`) and write each verdict to `### Leech Log`, under `## Decks` in `memory.md`: date, deck, card, why it failed, what replaced it. Without the log the same card is rescued and re-broken every term.

## Shared and Pre-Made Decks

- Pre-made decks are **not free**: they carry someone else's phrasing, scope and errors, and the cards were never processed by the person reviewing them.
- They are defensible for large standardized bodies of arbitrary content (medical licensing, language frequency lists) where the community deck is better curated than anything one student would build.
- Always: filter to the syllabus before starting, and delete out-of-scope subdecks on day one rather than suspending them "for later".
- Never for conceptual courses, and never as a substitute for having read the material.
- Auditing a shared deck's first 50 cards for errors takes twenty minutes and prevents memorizing something wrong for a term.

## Reviewing Well

- **Answer out loud or in writing before revealing.** Flipping to check whether you "knew it" is recognition, and it is the way a deck stops working (`retrieval.md`).
- Grade honestly: hesitation is a fail. A deck graded generously reports success while retention falls.
- **Same time every day**, sized by `daily_review_cap`. The queue collapses on irregularity, not on volume.
- Do not review the same card twice in a sitting to "make it stick" — that is massing inside a spaced system.
- Dead time (commute, queues) is for reviews, never for new cards.

## Retiring a Deck

The day after an exam for a course never needed again: suspend the whole deck, record the date in `## Decks`, and take the daily minutes back. For a prerequisite course, keep it at a long interval instead — it is far cheaper than relearning next September (`spacing.md`).

**Whenever a deck is created, split, suspended or triaged**, update its row in `## Decks` — cards, new/day, observed reviews/day, last triage date. Leech verdicts go to `### Leech Log` under it, and every lapse that reveals a knowledge gap (not a writing problem) goes to `errors.md` with cause `not retrievable` (`memory-template.md`).
