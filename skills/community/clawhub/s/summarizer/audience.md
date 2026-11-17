# Writing for a Specific Reader

Scope: the same material, cut for a different reader. Audience changes what is deleted first and what vocabulary survives — never what is added (SKILL.md Rule 9).

**Before writing for a named person**, read `## Audiences` in `~/Clawic/data/summarizer/memory.md` for their length ceiling, jargon tolerance, and standing requests, and `~/Clawic/data/contacts/contacts.md` for who they are and their preferred channel. A stored audience profile is the difference between a first draft that lands and three rounds of "shorter".

**Contents:** [Deletion Order](#deletion-order) · [The Audience Table](#the-audience-table) · [Jargon Budget](#jargon-budget) · [Executive Cuts](#executive-cuts) · [Technical Cuts](#technical-cuts) · [Non-Expert Cuts](#non-expert-cuts) · [Fan-Out: One Extract, Three Summaries](#fan-out-one-extract-three-summaries) · [Register and Voice](#register-and-voice) · [Storing an Audience](#storing-an-audience)

## Deletion Order

Every audience has an implicit ranking of what it will forgive losing. Write the ranking down before cutting, and cut from the bottom.

| Audience | Deleted first | Deleted last |
|---|---|---|
| Executive | Method, mechanism, caveats about process, names of tools | Money, dates, risk, the decision required |
| Technical | Business framing, market context, motivational language | Mechanism, constraints, failure modes, exact versions and numbers |
| Operator / on-call | Analysis and background | The action, its order, and what breaks |
| Academic | Practical implications, cost | Method, N, limitations, prior work |
| Legal / compliance | Performance and cost detail | Obligations, dates, liability, jurisdiction |
| Customer / user | Internal reasoning, roadmap politics | What changes for them, when, what they must do |
| Investor | Implementation detail | Numbers, growth basis, risk, comparison to plan |
| General public | Jargon, quantitative nuance, institutional detail | The concrete consequence for a person |
| Child or beginner | Everything abstract | One concrete image and one true sentence |
| Unknown | — | Write the `general` cut and name the assumption in the header |

## The Audience Table

| Audience | Length default | Vocabulary | Structure | Opens with |
|---|---|---|---|---|
| Executive | brief; never more than one screen | Business terms; every technical term earns its place or goes | Conclusion first, then three supports | The decision or the number |
| Technical | standard | Domain terms unexpanded; precision over accessibility | Problem, mechanism, constraints, tradeoff | What changed or what breaks |
| Operator | brief, imperative | Commands and component names | Ordered steps | The action |
| Academic | abstract, ~250 words, fixed slots | Field vocabulary | Background, method, results, conclusion | The question |
| Legal | standard, defensive | Defined terms exactly as defined | Obligations, dates, exposures | The deadline |
| Customer | brief, plain | Their words, not the product's internal names | What changed, what to do | The change and its date |
| Investor | brief with a numbers block | Financial terms with their basis | Headline, drivers, risks | The number and its comparator |
| General | standard, plain | Everyday words; expand every acronym once | Concrete before abstract | The consequence |
| Beginner | brief | One new term at a time, defined on use | Analogy, then the real thing | Why they should care |
| Anything else | `default_length` from the Configuration table | Neutral | Conclusion first | The single most important fact |

## Jargon Budget

Set a number before writing: how many unexplained domain terms this reader tolerates in this length.

- **Executive brief, 80 words**: budget 1-2 terms. Every additional term costs a sentence of explanation the length cannot afford, so the term goes instead.
- **Technical standard, 250 words**: unlimited within the domain; expanding known terms wastes the reader's time and signals you do not know who you are writing for.
- **General audience**: expand each acronym once on first use, then use it; expanding it every time is padding.
- **The substitution test**: replacing a term with a plain-language phrase must not change the claim. When it does — a legal defined term, a metric with a specific definition, a drug name — the term stays and gets a short gloss. Terms with a required exact form belong in `glossary.md`.
- Jargon is not only vocabulary: internal project names, ticket numbers, and org acronyms are jargon to anyone outside the team and are the ones most often left in by accident.

## Executive Cuts

The most-requested audience and the easiest to get wrong.

- **Conclusion in the first sentence.** BLUF: bottom line up front. If the reader stops after one line, they must still have the answer. The Minto pyramid is the same discipline: answer first, then the supporting arguments, then the data.
- **Every number carries its comparator** — against plan, against last period, against the alternative. A bare figure invites the question you were summarizing to prevent.
- **Name the decision required and its deadline**, or say explicitly that none is required. An executive summary with no ask is read as a status update and skimmed.
- **Three supports, maximum**, per the point budget (SKILL.md Rule 2). A fourth is a signal you have not decided what matters.
- **Hedge the claim, not the recommendation** — "the vendor's uptime figure is unaudited; recommend the 90-day exit clause" carries the uncertainty exactly where it belongs.
- **Caveats go in one line at the end**, never distributed through the text. Distributed hedging reads as a report that concluded nothing.

## Technical Cuts

- **Precision beats accessibility.** Exact versions, exact error strings, exact thresholds. A technical reader can look up a term; they cannot recover a number you rounded.
- **Constraints and failure modes are the content.** What breaks, at what limit, and what was not tested.
- **Tradeoffs stay explicit**: what was given up, not just what was chosen.
- **Cut business framing entirely** unless it constrains the technical decision (a deadline, a budget, a compliance regime does).
- Code, config, and commands are referenced by name and location, not reproduced, unless the exact text is the point.

## Non-Expert Cuts

- **Concrete before abstract.** A number a person can picture ("about the annual electricity use of 400 homes") lands where a raw figure does not — but the raw figure stays too, and the comparison is labelled as a comparison.
- **One idea per sentence**, and short sentences. This is the only audience where sentence length is a genuine constraint rather than a style preference.
- **Analogies are yours, not the source's** — label them, and never let an analogy carry a claim the source did not make.
- **Answer "why should I care" in the first line**, because there is no professional obligation to keep reading.
- Do not simplify a number into vagueness: "1 in 10,000" is more comprehensible than "a very small chance", not less.

## Fan-Out: One Extract, Three Summaries

When the same material must serve several audiences, do not write three summaries from the source and do not rewrite one into another (SKILL.md Rule 5).

1. **One extract pass** over the source: every load-bearing claim with its numbers, attribution, and hedges — audience-neutral, longer than any deliverable.
2. **Cut each audience's version from the extract**, applying that audience's deletion order.
3. **Check consistency**: the same fact must not appear with different numbers or different certainty across versions. This is the failure that gets noticed, because the recipients talk to each other.

The extract is worth storing when the fan-out will repeat (a launch, a board cycle, an incident) — it goes to `artifacts/`.

## Register and Voice

- **Default register** is neutral, third person, present tense for findings and past tense for events. Deviations come from `style_file` or a stated preference, never from the source's own tone.
- **Never inherit the source's voice.** A marketing document summarized in marketing language has not been summarized; an angry email summarized angrily is a fidelity failure of a different kind (`threads.md`).
- **The user's house style wins** over every default here: banned words, required sections, sentence-length rules, whether contractions are allowed. It lives in the file `style_file` points to.
- Emoji and section markers follow `markers`; they are a channel and taste decision, not an audience one.

## Storing an Audience

The person belongs in the shared box; their reading preferences belong here. Never duplicate the person.

**After writing for a named recipient**, put the person in `~/Clawic/data/contacts/contacts.md` — one row, keyed by lowercase email → handle → `<kebab-name>`, updated in place if they already exist and never duplicated — and record what is summarizer-specific in `## Audiences` in `~/Clawic/data/summarizer/memory.md`: their contact key, length ceiling, jargon tolerance, what they always ask for, and what they always cut. If they asked for a specific shape twice, store it as `templates/<audience>.md` with its `## Boxes` line. Reusable extract passes go to `artifacts/<topic>-extract.md`. Formats, columns, and the full shared-box protocol: `memory-template.md`.
