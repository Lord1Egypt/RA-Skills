# House Style — Consistency Across a Body of Work

Scope: the decisions that are neither right nor wrong but must be the same every time. One piece can survive inconsistency; a publication, a product, or a year of newsletters cannot.

**Before writing in any recurring context**, read its `~/Clawic/data/writing/style-sheets/<context>.md`. If the context has no sheet and it will recur, the first decision made in it starts one — created in the same turn, with its `## Boxes` line in `memory.md` (`memory-template.md`).

## Style Is Not Correctness

Calling a house-style preference an error is the fastest way to lose authority over the real errors. Three categories, and only one of them is negotiable:

| Category | Examples | Who decides |
|---|---|---|
| **Error** | Subject-verb disagreement, a misspelled name, a wrong number, a broken link | Nobody — it gets fixed |
| **Convention** | Oxford comma, US vs UK spelling, heading case, numerals under ten, spaced or unspaced em-dashes | The style sheet |
| **Voice** | Contractions, humour, sentence length, first vs second person | The writer, unless a client's sheet overrides (`voice.md`) |

`spelling` in `config.yaml` sets the dialect default. A client sheet outranks it inside that client's work.

## What Goes in a Style Sheet

The test for inclusion: **would two competent writers decide this differently?** If yes, it belongs. If it is simply correct, it does not — a sheet full of grammar rules is a sheet nobody reads.

- **Mechanics**: dialect and spelling variant, Oxford comma, quotation marks and where punctuation sits relative to them, em-dash style, ellipsis, capitalisation of headings and job titles, numerals vs words, date and time format, currency format.
- **Terminology**: the preferred term for every recurring concept, with the rejected alternatives listed. `customer` not `user`; `sign in` not `log in`; the product name in full, never abbreviated.
- **Names**: how the company, its products and its features are written, including capitalisation and whether "the" precedes them.
- **Banned**: words, claims, competitor mentions, superlatives that legal will not defend.
- **Structure**: required sections and their order, subhead cadence, length caps, mandatory blocks (disclaimer, byline, CTA).
- **Register**: person, formality, contractions, humour tolerance, emoji.
- **Process**: who reviews, what they always change, how long it takes, and where the piece is published.
- **Open questions**: decisions not yet made, with the date they were raised. This section is what prevents the same question being re-asked every quarter.

Everything gets a decision, not a discussion. One line each.

## Dialect Differences That Actually Bite

Beyond `-ize`/`-ise` and `color`/`colour`, the ones that cause real errors:

| Area | US | UK |
|---|---|---|
| Punctuation with quotes | Commas and periods inside the quotation marks | Outside, unless part of the quoted text |
| Quotation marks | Double outer, single inner | Either convention, applied consistently |
| Dates | Month-day-year; `7/4` is July 4 | Day-month-year; `7/4` is 4 July |
| Collective nouns | Singular verb ("the team is") | Often plural ("the team are") |
| Past participles | `learned`, `spelled` | `learnt`, `spelt` both acceptable |
| `-yse` verbs | `analyze`, `paralyze` | `analyse`, `paralyse` — the Oxford `-ize` convention does not reach them, so a blanket `-ise`→`-ize` replace breaks these and only these |
| Abbreviated titles | `Mr.`, `Dr.`, `St.` with the period | `Mr`, `Dr`, `St` without — the period marks a truncation, and these end in the word's last letter |

The date format is the one that causes actual damage. In any document crossing dialects, write the month as a word: `4 July 2026` or `July 4, 2026` is unambiguous, `7/4/26` is not.

## Terminology Discipline

- **One thing, one name, every time.** Elegant variation is a style failure and a comprehension failure: the reader assumes a renamed thing is a new thing (`clarity.md`).
- Record the term *and* the rejected alternatives. Without the rejected list, the next writer picks a synonym in good faith.
- Capitalisation of a product or feature is a decision that must be made once and enforced, because inconsistent capitalisation of a proper noun looks like carelessness rather than style.
- Words that mean something specific in the field and something loose in general use — `significant`, `optimize`, `real-time`, `secure` — get an explicit ruling on which sense the sheet permits.
- Acronyms: expand on first use per piece, not per publication. A reader arriving from search has not read the previous piece.

## Keeping the Sheet Alive

- One line per decision, with the date. The date is what settles "we changed that, didn't we".
- Add a rule the moment a decision is made — not at the end of the piece, when it is already forgotten.
- A rule that has been broken twice without anyone objecting is not a rule; delete it or enforce it.
- Never grow a sheet past what someone will actually read before writing. Past roughly two pages, split by document type rather than adding sections, and note the split in both files.
- Review before a new writer joins the context, and after any rebrand or product rename.

## Consistency Checks Before Publishing

Run these against the sheet — they are the failures that survive every other pass because each instance looks correct alone:

- Product and feature names, character for character, including capitalisation.
- One spelling variant throughout — mixed dialects inside one document is the most common consistency error and it is invisible while reading.
- Heading case consistent at every level.
- Numerals handled the same way throughout (the boundary is usually ten, but the sheet decides).
- Date format identical everywhere, including in captions and image alt text.
- Terminology: search for each rejected alternative in the sheet's list.
- Serial commas: present or absent, not both.
- Link text style consistent — either descriptive phrases or bare URLs, never a mix.

## When There Is No Sheet and No Time

Default to a published guide rather than inventing one, and say which: AP for news and press writing, Chicago for long-form and books, the platform's own guide for product writing, the client's existing published pieces for anything ghostwritten. Then record the choice as the first line of the new `style-sheets/<context>.md` — the choice of guide is itself the decision that stops being re-made.

**Every style decision made in a recurring context is written to `style-sheets/<context>.md` in the same turn it is made**, with its date, and the sheet's `## Boxes` line added to `memory.md` if the file is new. A decision that stays in the chat is re-litigated on the next piece, which is the exact cost this file exists to prevent (`memory-template.md`).
