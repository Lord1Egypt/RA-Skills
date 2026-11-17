# Form: literature-review

**Register:** `academic`

A form file supplies slots. Only the voice may fill them. Every quoted phrase in this file is under Tells, and every one of them is a phrase to avoid.

A synthesis of what a body of work establishes, disagrees about, and has not tried. The test is the same one `forms/essay.md` applies and it is stricter here: if the sections could be reordered without loss, this is an annotated bibliography with prose connectives, not a review.

Three shapes, and the differences are real rather than stylistic. A **narrative** review argues a reading of a field. A **systematic** review answers one question against a pre-registered protocol, and its method is the contribution. A **scoping** review maps what exists and deliberately does not synthesize. Say which at the top, because a reader judges the rest against that claim.

## Slots

- **Title.** The question or the field, with the review type in it where the venue expects one.
- **Abstract.** `forms/abstract.md` applies. For a systematic review it carries the protocol registration.
- **Introduction.** Why this synthesis, now. What changed, or what the field keeps disagreeing about.
- **Method.** For a systematic or scoping review this is where the rigor lives: databases, date range, search strings, inclusion and exclusion criteria, screening process, how disagreements were resolved, and how many records survived each stage. A flow diagram is expected. For a narrative review it is shorter and it is still stated, because a review with no stated selection is a review whose selection cannot be argued with.
- **Body.** Organized by theme, by mechanism, by method, or by chronology, and the choice is a claim about the field. Chronological is the weakest and the most common, because it is the one that requires no thesis.
- **Synthesis.** Where the sources are put against each other rather than beside each other. This is the slot that makes it a review.
- **Gaps.** What has not been done, specifically enough that somebody could do it.
- **Limitations.** Of the review, not of the field. Search dates, languages, publication bias, what a database does not index.
- **References.** A citation style applies, and reviews carry the most references of any form here. `references/citations/` has the four.

## Bands

| Purpose | Band |
|---|---|
| A review section inside a paper | 800 to 2,000 words |
| A standalone narrative review | 4,000 to 10,000 words |
| A systematic review | as long as the protocol requires, and the appendices carry the search strings |

## Tells

Phrases and shapes named here are the ones to avoid. Nothing in this file is a phrase to use.

- "Smith (2019) found X. Jones (2020) found Y. Brown (2021) found Z." Three sentences with no relation between them is a bibliography.
- "Several studies have examined" with no statement of what they concluded.
- "The literature is divided" without saying along which line.
- "A growing body of research suggests" as a substitute for counting.
- A section per decade, where the decades have no argument between them.
- A systematic review with no stated search string, which cannot be reproduced and therefore is not one.
- A gaps section that names a gap the review's own selection created.
- Citing a review for a primary finding, which passes the claim along without anybody checking it.
- Every source treated as equally weighted, so a preprint and a replicated trial carry the same force.

## What the mechanical layer sees here

The `academic` register applies, and `docs/academic-corpus/README.md` has how it was calibrated.

One thing this form does that no other form here does: it names other people constantly. `verify.py` lists named entities and never fails on them, for the reason `references/false-positives.md` gives about every crude signal, so an edit to a review is not checked for dropped authors. Nothing mechanical is watching that, which means you are.

`vague-attribution` is the finding to expect and it is a P0 fingerprint, so it fires at full strength here as it does everywhere. In a review the phrases it catches are usually attached to a citation, and they are also usually the sentence where a specific finding should have been stated instead. Read each hit rather than dismissing the class: this is the form where `studies show` most often means the author did not want to commit to which studies.

Trigram repetition and low burstiness are skipped in this register, which matters more here than in a research paper. A review repeats construct names across dozens of sources by necessity, and renaming them for variety is the one thing that would make it unreadable.
