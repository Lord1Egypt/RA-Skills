# Quality — Review, Scoring, and Acceptance

"Is this translation good?" is answerable only against a typology, a weighting and a threshold agreed in advance. Everything else is two people's taste, which is how review turns into an argument nobody can win.

**Contents:** [The Roles](#the-roles) · [Self-Review When You Are Alone](#self-review-when-you-are-alone) · [Error Typology](#error-typology) · [Severity and Scoring](#severity-and-scoring) · [Sampling](#sampling) · [Automated Checks](#automated-checks) · [Back-Translation](#back-translation) · [Reviewing Someone Else's Work](#reviewing-someone-elses-work) · [Disputes](#disputes) · [The LQA Report](#the-lqa-report) · [Closing the Loop](#closing-the-loop) · [What To Write Down](#what-to-write-down)

**Before reviewing anything for a returning client**, read the pair's glossary, `styles/<locale>.md`, and any previous `artifacts/lqa-*.md` that `## Boxes` names. A finding that was already accepted as a preference is not a finding.

## The Roles

`review_stage` selects how many of these run. They are different jobs and conflating them is why review is expensive and shallow at the same time.

| Role | Reads | Looks for |
|---|---|---|
| Translation | Source | — |
| Revision (bilingual) | Source and target side by side | Accuracy: mistranslation, omission, addition, terminology |
| Review (monolingual, domain expert) | Target only | Does this work for its purpose and audience in this field |
| Proofreading | Target only, final layout | Typos, punctuation, spacing, hyphenation, layout defects |
| Sign-off | The finished artifact | Acceptance criteria met; nothing structural left |

The profession's baseline (ISO 17100) is translation plus revision by a **second person**; post-editing has its own standard (ISO 18587, `machine-translation.md`). Anything less is a reduced service and should be named as one in the quote, not discovered by the client.

## Self-Review When You Are Alone

The substitute Rule 9 permits, in this order. Skipping the delay is what makes self-review worthless — you cannot see your own text until you have stopped holding the source in your head.

1. **Wait.** Hours if possible, overnight for anything long.
2. **Monolingual read of the target, source hidden.** Mark everything that stumbles. Fluency defects are invisible while the source is in view, because the source explains them.
3. **Bilingual verification pass**, but not a re-read — a targeted check of the risk categories: negations, numbers, dates, names, obligations, quantities, conditions, and anything the client called out.
4. **Numbers-only pass.** Read only the figures, in order, against the source. It finds what prose reading cannot (`legal-medical.md`).
5. **Mechanical checks** (below), then the Output Gates in `SKILL.md`.
6. **Read aloud** for anything that will be spoken or is short and prominent — a headline, a slogan, a subtitle line.

## Error Typology

The dimensions of the MQM tradition, which nearly every scorecard descends from. Classify every finding into exactly one, or the counts mean nothing.

| Dimension | Includes |
|---|---|
| Accuracy | Mistranslation, omission, addition, untranslated text, over- or under-translation |
| Fluency | Grammar, spelling, punctuation, agreement, awkward or unidiomatic phrasing, inconsistency |
| Terminology | Wrong term, glossary violation, inconsistent term use |
| Locale conventions | Number, date, currency, address, phone and unit formats (`numbers-and-names.md`) |
| Style | Register, voice, brand guideline violations |
| Design and markup | Broken tags and placeholders, truncation, encoding, layout defects |
| Audience appropriateness | Correct but wrong for this reader — reading level, cultural fit, legal suitability |

**Preferential changes are not errors** and get their own bucket. Keeping them separate is what makes a score defensible.

## Severity and Scoring

Weights vary by scorecard: the LISA-derived grid is minor 1, major 5, critical 10, while many MQM scorecards weight critical at 25. **Fix the weights in the brief before scoring**, because a threshold means nothing without them.

- **Minor**: noticeable, does not mislead — a clumsy phrase, a missing comma.
- **Major**: changes meaning, breaks a function, or would embarrass the client publicly.
- **Critical**: causes harm, legal exposure, or safety risk — a wrong dose, an inverted obligation, a reversed negation. One critical fails the delivery regardless of the score.

Formula: `score = 100 − (total penalty points × 100 ÷ word count)`.

Worked example: 1,100 words reviewed, 6 minor (6) + 1 major (5) + 3 minor (3) = 14 points. `100 − (14 × 100 ÷ 1100) = 98.7`. With a pass threshold of 98, this passes — and the terminology cluster inside it still generates glossary rows, because a passing score is not the same as nothing to fix.

Set the threshold per content type, not globally: publishable marketing tolerates less than internal documentation. A commonly used bar for publishable content is roughly one penalty point per 100 words, which is a score of 99.

## Sampling

- Full review for anything regulated, short, or highly visible.
- For large volumes, review a **sample of 1,000-2,000 words, or 10-20% of the job**, whichever is larger, then extrapolate.
- Choose the sample **risk-weighted, not randomly alone**: the first pages (where a translator finds the voice), headings and UI labels, the numbers-heavy sections, and one random block to keep it honest.
- A failed sample does not get patched. It fails the batch, and the batch is reworked and re-sampled — patching the reviewed part and shipping the rest is how a known-bad file reaches production.

## Automated Checks

Run before human review so the human is not spending attention on machine-findable defects. Any CAT or QA tool does these; without one, a script over the deliverable covers most:

| Check | Catches |
|---|---|
| Placeholder and tag parity | Crashes and broken markup (`software-strings.md`) |
| Number and date consistency between source and target | Transposed digits, dropped figures |
| Glossary compliance, lemma-aware | Terminology drift (`terminology.md`) |
| Same source segment, different targets | Inconsistency across a large file |
| Same target for different sources | Two concepts merged into one word |
| Untranslated or copied-source segments | Skipped work |
| Forbidden renderings | Rejected terms reappearing |
| Length limits per string | UI overflow (`software-strings.md`) |
| Double spaces, missing or doubled punctuation, spacing before punctuation | Locale typography (`locales.md`) |
| Spell check with the **target locale's** dictionary | The wrong dictionary passes everything and flags everything |

## Back-Translation

Translating the target back into the source, by a translator who has not seen the original. Used as verification in clinical and regulated work (`legal-medical.md`), and as a communication device in transcreation (`transcreation.md`) — the two uses are not interchangeable.

- **It detects**: omission, addition, inverted meaning, mistranslated numbers and negations.
- **It does not detect**: fluency, register, terminology fit, or naturalness — a stilted target can back-translate perfectly.
- **It produces false alarms** wherever the target legitimately restructured. That is what the **reconciliation** step is for: the two translators and a moderator compare the back-translation to the source, and each divergence is either a real defect or a documented, justified choice.
- Never back-translate with the same person, and never with a machine when the purpose is verification — a machine will regenerate the source's structure from the target and hide the very omissions being hunted.

## Reviewing Someone Else's Work

- **Change errors, not preferences.** Preferential rewriting is the most common dispute in this profession, and it is the reviewer's failure, not the translator's. If the sentence is correct, clear and on-brand, leave it.
- Every change gets a category from the typology above and, where it is not self-evident, one line of evidence: a glossary row, a style rule, a dictionary or corpus citation.
- Use tracked changes or a comparable diff, always. A silently rewritten file cannot be learned from, and it cannot be argued with.
- Review against the brief and the glossary, not against the translation you would have written.
- Separate the deliverable from the feedback: the client gets a clean file, the translator gets the annotated one.
- When the file is genuinely below standard, say so early and stop, rather than rewriting it as a review. A rewrite billed as a review destroys both the schedule and the relationship.

## Disputes

- Evidence first: the glossary, the style guide, the brief, a corpus of the target market, an authority. "It sounds better" is not evidence, in either direction.
- Distinguish an error from a preference explicitly, in writing, per item. Most disputes shrink to two or three real items once this is done.
- Unresolved after that, an independent third linguist arbitrates against the same typology, and both parties accept the categories before seeing the verdict.
- The outcome is written down as a glossary row or a style rule so the same argument cannot recur.

## The LQA Report

Short, numeric, and actionable:

- Scope: what was reviewed, sample size, total word count.
- The weights and the pass threshold used.
- The score, with the arithmetic visible.
- Errors grouped by dimension, with severity, the segment reference, the source, the target and the correction.
- Preferential changes listed separately, marked as such.
- Root causes, where there is a pattern: no glossary, no context in the file, a source defect, an MT engine artifact.
- Actions taken and actions requested, each with an owner.

## Closing the Loop

A review that only fixes the file is half a review. Every finding routes somewhere permanent: a terminology error becomes a glossary row and, if a rendering was rejected, a forbidden rendering; a register finding becomes a line in `styles/<locale>.md`; a markup or placeholder defect becomes an environment fact or a source-side bug report; a recurring accuracy defect becomes a note in the brief for the next job. Findings that do not route anywhere reappear at the same rate next time.

## What To Write Down

- The **LQA report** is an `artifacts/lqa-<scope>.md`, born as its own file, with its `## Boxes` line and a read condition naming the surface it covers (`memory-template.md`).
- **Reviewer corrections go into the glossary in the same session** — terms to `## Terms`, rejected renderings to `### Forbidden Renderings` with the accepted form.
- A defect that reached a reader is a one-line entry in **`## Pain Points`** with its cause. That line is what makes the next session check the right thing first.
- The reviewer is a row in the shared **contacts** box, with what they are trusted to judge; the score and the issue count go in the delivery row in `deliveries/<year>.md`.
