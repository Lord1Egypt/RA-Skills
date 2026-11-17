# Terminology — Glossaries, DNT, and Consistency

Consistency is the cheapest quality signal in translation and the most visible when it is missing. A reader who meets two words for one concept concludes they are two concepts; a reviewer who meets three concludes nobody is in charge.

**Contents:** [What Counts as a Term](#what-counts-as-a-term) · [One Entry per Concept](#one-entry-per-concept) · [Extracting the Candidate List](#extracting-the-candidate-list) · [Deciding a Term](#deciding-a-term) · [Do Not Translate](#do-not-translate) · [Forbidden Renderings](#forbidden-renderings) · [Glossary Versus Style Guide](#glossary-versus-style-guide) · [Enforcing It](#enforcing-it) · [Changing a Term After Launch](#changing-a-term-after-launch) · [Anti-Patterns](#anti-patterns) · [What To Write Down](#what-to-write-down)

**This is the file whose whole output is a box.** Read the pair's glossary — `## Glossary` in `~/Clawic/data/translate/memory.md`, or the file `## Boxes` names — before translating anything, and write every decision back in the same session. A term decided in a chat and not written down is a term that will be re-decided differently.

## What Counts as a Term

Include: domain concepts the product or field owns · UI labels and the verbs of core actions (`share`, `archive`, `sync`) · feature and plan names · recurring compound phrases (`two-factor authentication`) · units, roles and object types that appear in many strings · anything a reviewer has already argued about once.

Exclude: ordinary vocabulary with no domain meaning · one-off words · full sentences (those belong in translation memory, `translation-memory.md`) · anything whose translation is forced by grammar rather than chosen.

A glossary of 100-300 entries for a product is a working tool. Past roughly 500, nobody consults it and the enforcement checks drown in false positives — which is a signal to split by domain, not to stop adding.

## One Entry per Concept

An entry describes a **concept**, not a string. `sign in`, `log in` and `sign-in` are one concept with one target and three source variants; recording them as three entries is how the target ends up with three renderings.

Minimum viable entry, which is what the box stores: source term · part of speech · target · why (context or the reason for the choice) · date decided. Add when they exist, inside the same `Context / why` cell: status (approved, pending, forbidden), domain or product area, the person who approved it, and one example sentence.

**Part of speech is not optional.** `sync` the verb and `sync` the noun take different targets in most languages, and a single row for both produces a sentence with a noun where a verb belongs. Two rows, both correct.

## Extracting the Candidate List

Do this before translating, not during:

1. **Frequency plus specificity.** A word that appears many times and is not ordinary vocabulary is a candidate. A useful working threshold for a product corpus is five or more occurrences, plus everything appearing in a heading, a menu label, or a button.
2. **Structural positions**: UI labels, error message subjects, table column headers, API resource names surfaced to users, plan and feature names. These carry disproportionate weight because users see them repeatedly.
3. **Multi-word units matter more than single words.** Two- and three-word phrases are where inconsistency hides, because each word looks fine alone.
4. **Ask what already exists.** The client usually has a term list, a brand guide, or a competitor analysis somewhere; and a previous translation is itself a source of terms (`translation-memory.md`).
5. **Validate before translating.** Send the source-language candidate list for confirmation first — it is a five-minute task for the client and it prevents translating the wrong concept precisely.

## Deciding a Term

- Evidence beats intuition: what the target market's own literature, competitors and standards bodies use. Search the term in the target language restricted to the market before inventing one.
- **English is sometimes the right target.** Many fields keep English terms in other languages; forcing a translation reads as amateur to a practitioner. The evidence decides, not a policy.
- Who approves depends on what the term is: an in-market reviewer for register and naturalness, the product owner for feature names, legal for anything that is a claim (`legal-medical.md`). Write the approver into the term's `Context / why` cell (`approved by Ana, in-market`) and the date in `Set on`, in `## Glossary` or the pair's glossary file.
- When a term genuinely has no target equivalent, the options are a borrowing, a calque, a descriptive phrase, or a coined term — with the source in brackets on first use. Pick one, record it as a glossary row with the reason, and never alternate.
- A term decided under time pressure gets `status: pending` and a note. Pending is honest; silently guessing is not.

## Do Not Translate

The generic list lives in `SKILL.md`; this box holds the user's own: brand and product names, trademarks with their required treatment (capitalization, ® placement, whether they take an article or a plural), third-party product names, legal entity names, code-like identifiers the team keeps in English, and error codes.

Two details that get missed: a trademark cannot be inflected or declined in most style guides, which constrains sentences in Slavic and Finnic languages — rewrite around it; and a brand that *is* translated in one market (a registered local form) is a DNT exception that must be recorded per locale, not globally.

## Forbidden Renderings

The rejected candidates, with the accepted form and the reason. This is the highest-value part of the glossary and the part most often missing.

Without it: the same wrong word is proposed every release by whoever is translating that week, rejected by the same reviewer, and the cycle repeats with no memory. With it, the rejection is a lookup.

Sources of rows: reviewer corrections, client complaints, an in-market reader's "nobody says that", and any term whose rendering was changed after launch.

## Glossary Versus Style Guide

| Glossary | Style guide |
|---|---|
| Individual terms and their targets | Rules that apply to all text |
| Concept-level decisions | Register, punctuation, capitalization, number style, voice |
| Checked mechanically at delivery | Judged by a reviewer |
| One per language pair | One per locale (`styles/<locale>.md`) |

Keeping them separate is what makes each usable: a style rule buried in a glossary comment is never applied, and a term list inside a style document cannot be checked automatically.

## Enforcing It

- **At delivery, not at review.** A glossary check is a mechanical pass over the target: for every source segment containing a glossary term, confirm the target contains the approved rendering. Most CAT and QA tools do this; without one, a scripted search over the deliverable finds most of it.
- **Match on lemmas, not strings.** Inflected languages will not contain the dictionary form: the check must accept `espacios de trabajo` for `espacio de trabajo`, or it produces so many false positives that the team turns it off — which is how enforcement dies.
- **Check both directions.** One source term rendered two ways is the obvious failure. One target word used for two different source terms is the subtler one, and it merges two concepts in the reader's mind.
- Where a term legitimately must differ from the glossary in a specific context, that is a new entry with the context recorded, not an exception nobody can see.
- Glossary compliance is a scored category in a quality review, and terminology errors are usually the largest single category in a first delivery (`quality.md`).

## Changing a Term After Launch

A term change is a project, not an edit:

1. Decide the **scope**: retroactive across everything, or from now on. Mixed usage is worse than either, so the decision has to be explicit.
2. Find every occurrence — shipped product strings, documentation, help center, marketing pages, subtitles, previous releases, and the translation memory itself. A TM left unfixed reintroduces the old term as a fuzzy match forever.
3. Update the glossary row with the new target and the date, and move the old rendering to `### Forbidden Renderings` so the search history stays findable.
4. Tell the humans: a term users already know is a change they will notice (`games.md` for the community case).

## Anti-Patterns

| Anti-pattern | Why it fails |
|---|---|
| Dumping every noun in the source into the glossary | The check becomes noise, the list becomes unmaintainable, and translators stop reading it |
| One entry per source string instead of per concept | Guarantees synonyms of the source get different targets |
| No part of speech | Verbs get noun renderings and the sentences read as machine output |
| A glossary that contradicts the shipped product | The documentation says one thing and the button says another; the product wins, so fix the glossary or fix the product |
| Term list living in the CAT tool only | It cannot express forbidden renderings or the reason for the choice, and it dies with the platform subscription |
| Adding terms at the end of a project | The end of a project is when it is skipped; add them in the session where they were decided |

## What To Write Down

Everything here, and immediately (`memory-template.md`):

- Each decided term → a row in **`## Glossary`** in `~/Clawic/data/translate/memory.md`, or in `glossaries/<src>-<tgt>.md` once it has split. Source, part of speech, target, why, date.
- Each brand, trademark, or code-like item → **`### Do Not Translate`**.
- Each rejected rendering → **`### Forbidden Renderings`**, with the accepted form and the reason.
- The split is automatic: a second language pair, or ~15 entries, moves the section to `glossaries/<src>-<tgt>.md` with the same three headings promoted one level, its `## Boxes` line written in the same turn, and the section deleted from `memory.md`.
- A periodic consolidation across pairs — merging duplicates, resolving contradictions, retiring dead terms — is a row in **`## Due`**; quarterly is a reasonable default for an active product.
