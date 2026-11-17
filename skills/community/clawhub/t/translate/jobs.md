# Running a Job — Scoping, Briefing, Vendors, Handoff

The commissioning side of translation: what to count, how long it takes, what to send with the file, and who does the work. Most failed translation projects failed here, before a word was translated.

**Contents:** [Counting the Work](#counting-the-work) · [Throughput and Deadlines](#throughput-and-deadlines) · [Splitting Across Translators](#splitting-across-translators) · [The Brief](#the-brief) · [The Handoff Package](#the-handoff-package) · [Query Management](#query-management) · [Choosing a Translator or Agency](#choosing-a-translator-or-agency) · [Rates and What They Cover](#rates-and-what-they-cover) · [Scope Changes](#scope-changes) · [Acceptance](#acceptance) · [Red Flags in an Incoming Job](#red-flags-in-an-incoming-job) · [What To Write Down](#what-to-write-down)

**Before quoting for a returning client**, read `deliveries/<year>.md` and `## Environment` in `~/Clawic/data/translate/memory.md` if `## Boxes` names them: what the last comparable job actually took and what leverage their memory gave is the only reliable input to an estimate.

## Counting the Work

- **Source word count is the default basis**, because it is knowable before the work starts. Target-based counting exists and it makes the invoice unpredictable — the target of the same file differs by 30% between German and Japanese (`SKILL.md` Rule 5).
- Local conventions differ and are not wrong: German-speaking markets often price by standard line (a line of 55 characters including spaces), Japanese by source character, and some markets by 1,000 words. Establish the unit before the number.
- **Count what is actually there**: hidden text, headers and footers, footnotes, speaker notes, alt text, text in images, embedded spreadsheets (`documents.md`). Text in images is quoted separately because it needs the design source.
- Apply the memory analysis to get the weighted count (`translation-memory.md`); quote both the raw and the weighted figure so the client sees the leverage they are being given.
- Non-word content has its own units: subtitles by runtime, voice-over by recorded minute, DTP by page, review by hour, transcreation by project.
- A minimum charge exists for a reason — a 40-word job carries the same overhead as a 400-word one.

## Throughput and Deadlines

Planning figures for a professional working in a familiar domain. Calibrate them against `deliveries/<year>.md` for the actual people involved; treat them as a starting point, never as a promise:

| Task | Per working day |
|---|---|
| Translation, from scratch | 2,000-3,000 words |
| Full post-editing of good machine output | 4,000-7,000 words |
| Bilingual revision | 800-1,200 words per hour |
| Final proofreading of a clean target | Substantially faster than revision; measure it, since it depends entirely on quality |
| Subtitle translation from an existing template | Tens of minutes of runtime, dropping sharply if spotting is included |

Deadline formula: `translation days = weighted words ÷ daily throughput`, then add revision, then DTP or engineering, then a buffer for queries and rework. A worked example: 12,000 weighted words at 2,500/day is 5 days of translation; revision of 12,000 raw words at 1,000/hour is about 1.5 days; DTP a day; buffer a day. Quote 8-9 working days, not 5.

Two corrections that matter:

- **High leverage cuts the invoice more than the calendar.** Someone still reads all 12,000 words even if 5,000 of them are matches (`translation-memory.md`).
- **Rush work is a quality decision, not a price decision.** Beyond about 120% of a translator's normal daily throughput, the job must be split, and splitting costs consistency.

## Splitting Across Translators

Sometimes unavoidable. What makes it survivable:

- **Glossary first, before anyone starts.** With two translators and no glossary, the same term arrives in two forms, guaranteed (`terminology.md`).
- **One reviser harmonizes the whole file.** Never split the revision too, or the inconsistencies survive.
- Split by **section boundary**, not by interleaving: a translator who has the whole chapter can be consistent inside it.
- Share the memory live if the tooling allows it, so the second translator sees the first's segments.
- Budget extra revision time. The harmonization pass is real work and is the thing that gets cut when the schedule slips.

## The Brief

Send this with every job. It takes ten minutes and it prevents the two most expensive outcomes — the wrong register and the wrong terminology, both of which are found after delivery.

1. **Target locale**, not language: `pt-BR`, `es-419`, `zh-Hant-TW`.
2. **Audience and purpose**: who reads it and what they do next.
3. **Register**: formal or informal address, and any brand voice notes (`locales.md`).
4. **Glossary and do-not-translate list** (`terminology.md`).
5. **Style guide** for the locale, or the reference that stands in for one.
6. **Reference material**: previous translations, the live product, screenshots, the source document's context.
7. **Constraints**: character limits, reading speed, layout, file format.
8. **Deliverable and deadline**: exact format, exact date, and the time zone.
9. **Who answers questions**, and by when.
10. **What is out of scope**: images, DTP, review, certification.

Creative work needs the additional brief in `transcreation.md`; regulated work needs the requirements in `legal-medical.md` established before anyone quotes.

## The Handoff Package

| Item | Why it matters |
|---|---|
| Editable source files, final | A PDF or a non-final file doubles the cost silently (`documents.md`) |
| Glossary and DNT list | The single highest-leverage attachment |
| Style guide or reference translations | Defines "correct" before the argument |
| Translation memory | Consistency plus leverage (`translation-memory.md`) |
| Screenshots or product access | Removes the biggest cause of context errors (`software-strings.md`) |
| Character limits per string, where they exist | Prevents overflow found three weeks later |
| A named contact for queries | Without one, the translator guesses |

## Query Management

- Keep **one query log** for the job in `artifacts/queries-<job>.md`, born as its own file with its `## Boxes` line: segment reference, question, answer, date, who answered. Not a thread, not a chat.
- **Batch queries** rather than sending them one at a time — one interruption a day, not fifteen.
- The answer goes into the glossary or the style guide in the same session, or it is answered again next month (`terminology.md`).
- A translator who asks good questions early is doing the job correctly. A job with zero queries on ambiguous source is a job where the ambiguity was guessed.
- Unanswered by the deadline: translate for the most likely reading, mark it in a translator's note, and deliver on time (`SKILL.md` Rule 2).

## Choosing a Translator or Agency

- **Native in the target, working into their own language**, and living in or closely connected to the target market. Both halves matter: language competence and current usage.
- **Subject expertise beats general excellence** for legal, medical, technical and financial content. A brilliant literary translator is the wrong choice for an IFU.
- **Test with a paid sample**, the same 250-300 words for every candidate, reviewed blind by someone who is not choosing. An unpaid test attracts the wrong candidates and an unblinded review measures the reviewer's expectations.
- Ask what they need from you. A candidate who asks about audience, register, glossary and reference material is showing you the process; one who only asks for the file is showing you theirs.
- For regulated work, check the specific credential the receiving authority requires, not a general certification (`legal-medical.md`).
- For agencies, ask who actually translates, whether it is the same person next time, and whether revision by a second linguist is included or an upsell.

## Rates and What They Cover

- Establish the unit (word, line, character, hour, minute, page), the currency, the leverage grid, the minimum charge, and what is included: revision, DTP, one round of amendments, project management.
- Hourly is correct for review, transcreation, DTP, query-heavy work and anything unquantifiable in words. Per-word pricing on creative work misprices it in both directions.
- Rush surcharges and weekend work are normal and should be stated up front, not discovered.
- Payment terms, purchase order requirements and the invoicing entity are part of the agreement; for a freelancer, so is the currency conversion cost.
- Record what this client or vendor actually pays, with the currency, in the contacts row — never a bank detail (`memory-template.md`).

## Scope Changes

- **Source changes mid-project are a re-quote, not a favor.** Keep a change log with dates and word deltas in `artifacts/scope-changes-<job>.md`, or as decision lines in the shared `projects/<project>.md` when the user tracks the effort there; a project with rolling source edits costs more than one with a freeze, and the client needs to see why.
- A string freeze before translation is the single most effective process improvement available on a software project (`software-strings.md`).
- Additional locales added mid-project multiply every downstream step, including query answering and review.
- Format changes (now we also need PDF, now it must fit the old layout) are new work.

## Acceptance

- Acceptance criteria are agreed in the brief, using the typology and threshold in `quality.md`. Without them, "we do not like it" is unfalsifiable and unbillable.
- Distinguish **rework** (defects against the brief, fixed at no cost) from **new work** (preference changes, source changes, added scope), and say which each item is in the reply that returns the feedback. Sorting a mixed list weeks later is unwinnable.
- Feedback from the client's in-market reviewer is gold and must be routed into the glossary and style boxes, not applied only to this file (`quality.md`).
- Close every job by writing the delivery row — the count, the leverage, the reviewer, the issues found. That row is what makes the next quote accurate instead of hopeful.

## Red Flags in an Incoming Job

| Signal | Why it costs |
|---|---|
| PDF only, no editable source | Rebuilding the document is a separate project (`documents.md`) |
| "It's just a small file" with no context or brief | Small files with no context generate the most queries per word |
| Deadline set before the source is final | Every source edit re-triggers translation, review and layout |
| No named reviewer, but "we'll have someone check it" | An unbriefed internal reviewer produces preferential rewrites and disputes (`quality.md`) |
| Certification mentioned casually | The requirement is jurisdictional and may make the timeline impossible (`legal-medical.md`) |
| "Just machine translate it and clean it up" | Full post-editing priced as light post-editing (`machine-translation.md`) |
| A target locale nobody on the team can read | Budget for an in-market reviewer, or accept unverifiable delivery |

## What To Write Down

- Every delivered job is a row in **`deliveries/<year>.md`**: date, pair, content type, word count, tool, reviewer, issues, project. This is the file that makes estimates real.
- The client's standing requirements — brief contents, glossary, style guide, delivery format, acceptance criteria — are an **`artifacts/brief-<client>.md`**, born as its own file with its `## Boxes` line.
- The running job records are **`artifacts/queries-<job>.md`** (the query log) and **`artifacts/scope-changes-<job>.md`** (dates and word deltas), each born as its own file with its `## Boxes` line and read condition, in the same turn. An answered query whose decision is a term also becomes a glossary row (`terminology.md`).
- Translators, revisers, agencies and in-market reviewers are rows in the shared **contacts** box, with their pair, specialization and rate note (currency included).
- A localization effort the user tracks as work in progress is a shared **project** file, with the milestones and the decisions; keep the linguistic detail in this skill's boxes and leave a pointer there.
- What a CAT tool, MT plan or retainer costs is a row in the shared **subscriptions** box, with the currency inside the value (`memory-template.md`).
