# Translation Memory, XLIFF, and Fuzzy Matches

A translation memory is a database of source-target segment pairs from past work. It decides what a job costs, how consistent it is, and — when it is dirty — which mistakes get reproduced forever.

**Contents:** [Match Tiers](#match-tiers) · [Reading an Analysis](#reading-an-analysis) · [The Fuzzy Floor](#the-fuzzy-floor) · [Segmentation Decides Everything](#segmentation-decides-everything) · [XLIFF and the Round Trip](#xliff-and-the-round-trip) · [TMX and Moving Between Tools](#tmx-and-moving-between-tools) · [Alignment](#alignment) · [Maintenance](#maintenance) · [When TM Hurts](#when-tm-hurts) · [Concordance](#concordance) · [Confidentiality](#confidentiality) · [What To Write Down](#what-to-write-down)

**Before quoting or starting a job for a returning client**, read `## Environment` in `~/Clawic/data/translate/memory.md` for where their memory lives and what it is worth, and the pair's glossary. Leverage is the difference between a quote that wins and one that loses (`jobs.md`).

## Match Tiers

| Tier | Meaning | Typical share of the word rate |
|---|---|---|
| Context / ICE (often shown as 101% or 102%) | A 100% match whose preceding and following segments also match — the surrounding text is identical too | 0-10% |
| 100% | Segment text identical, context unknown | 20-30% |
| 95-99% | One or two words or a number differ | 30-40% |
| 85-94% | A short phrase differs | 50-60% |
| 75-84% | Substantially different, same skeleton | 60-80% |
| Below 75% (no match) | Treated as new | 100% |
| Repetitions | Segment repeats inside this job, translated once | 20-30% |

The percentages are the common vendor grid, not a standard: they are negotiated per client and per tool, and the grid must be agreed **before** the analysis is run, or the same file supports two very different invoices.

## Reading an Analysis

Weighted word count = Σ (words in each band × that band's share). Worked example on a 10,000-word job with the grid above at its midpoints:

| Band | Words | Share | Weighted |
|---|---|---|---|
| ICE | 1,000 | 5% | 50 |
| 100% | 2,000 | 25% | 500 |
| 95-99% | 800 | 35% | 280 |
| 85-94% | 1,200 | 55% | 660 |
| 75-84% | 500 | 70% | 350 |
| New | 3,500 | 100% | 3,500 |
| Repetitions | 1,000 | 25% | 250 |
| **Total** | **10,000** | — | **5,590** |

The job is quoted and scheduled as 5,590 words, not 10,000 — but the *reading* time is still 10,000 words, which is why throughput on a high-leverage file is lower per weighted word than on a new one (`jobs.md`). Say that when a client expects the delivery time to scale with the invoice.

## The Fuzzy Floor

Below about 75% similarity, reading the match, deciding what to keep and editing around it costs more than translating the segment fresh, and it leaves the source's structure embedded in the target. That is why 75% is the conventional cut-off and why tools stop showing matches there.

The same reasoning applies inside the bands: a 78% match on a two-sentence segment is often worth discarding. The decision rule is the same one used for machine output — if you are rewriting more than roughly a third of it, start clean (`machine-translation.md`).

Watch the **numbers-only difference**: a 99% match differing only in a figure is the most dangerous tier, because the eye accepts the sentence and misses the digit. Tools flag these as auto-substitutable; verify the substitution rather than trusting it.

## Segmentation Decides Everything

- A TM matches segments, and segments are produced by segmentation rules (SRX is the interchange format for them). Change the rules and yesterday's 100% matches become 0% matches — the memory is intact and worthless.
- Default rules break at sentence-final punctuation with an exception list for abbreviations (`Dr.`, `e.g.`, `Inc.`). A missing exception splits one sentence into two segments and destroys the match for that sentence forever.
- Keep segmentation rules with the memory, and use the same rules for analysis and for translation, or the analysis is fiction.
- **Never merge or split segments casually** during translation: it changes what gets stored. Where a target genuinely needs a different sentence structure, most tools support merging within a paragraph — use that mechanism rather than moving text between segments.
- Sentence-level segmentation is the default; paragraph-level increases quality and destroys leverage. Pick per content type, not per job.

## XLIFF and the Round Trip

- XLIFF is the container that carries source, target, state and inline markup between a filter and a translation tool. The workflow lives in the **state** attribute: `new` → `translated` → `reviewed` → `final` (1.2 uses `needs-translation`, `translated`, `signed-off` among others).
- Inline tags (`<g>`, `<x/>`, `<ph>`, `<bpt>/<ept>`) represent formatting from the original file. They are placeholders (`software-strings.md`): count and nesting must survive, position may move.
- The round trip is the point: translate the XLIFF, convert back with the same filter and the same settings that produced it. A different filter version can fail to reassemble the original file.
- `translate="no"` and locked segments must be respected by the tool and by the human; unlocking to "fix" something is how a code fragment gets translated.
- Validate the XLIFF before returning it. A malformed file is the single most common cause of a delivery being bounced back on the deadline.

## TMX and Moving Between Tools

- TMX is the interchange format for the memory itself: segment pairs plus metadata (creation date, creator, and custom properties).
- Expect **metadata loss** between tools: context keys, some inline tag representations, and tool-specific attributes are the usual casualties. Export, import into the target tool, and check a handful of segments before decommissioning the old memory.
- Import with a **penalty on segments from another source** where the tool supports it, so an imported segment never outranks one your own reviewed work produced.
- Encoding is UTF-8 and the language codes inside are BCP 47 — a TMX with `es` where the memory is `es-419` will silently fail to match in a tool that is strict about codes (`locales.md`).

## Alignment

Creating a memory from legacy bilingual documents by pairing their segments. Worth doing when there is a large, well-translated, still-accurate corpus.

- Alignment errors are the classic way to poison a memory: one skipped segment shifts everything after it, and the result is confident, plausible, wrong matches for years.
- Review the alignment before importing, especially around headings, tables, footnotes and any place the target restructured.
- Do not align content that no longer reflects the product or the terminology; an aligned memory of the old term reintroduces it at every fuzzy match (`terminology.md`).
- Mark aligned segments in the metadata so a later cleanup can tell them from reviewed work.

## Maintenance

Left alone, a memory decays: terminology changes, products change, and bad segments propagate.

| Task | Trigger | What it does |
|---|---|---|
| Deduplicate | Periodic | Multiple targets for one source force a choice at every match |
| Retire outdated segments | After a term change or a product change | Otherwise the old term returns as a fuzzy match forever (`terminology.md`) |
| Separate by client and domain | Always | Never mix clients in one memory — terminology conflicts, and it is usually a confidentiality breach |
| Tag origin | On import | Human-reviewed, machine-translated, aligned, imported — so a later cleanup can act on it |
| Never store unreviewed MT as if it were human work | Always | It is the single fastest way to make a memory untrustworthy (`machine-translation.md`) |
| Penalize age | Periodic | A segment from four years ago deserves a read, not silent reuse |

A cleanup pass is a `## Due` row, not an intention.

## When TM Hurts

- **Creative content**: reusing a headline because it matched 100% is how a campaign ends up with last year's line (`transcreation.md`).
- **Content that must be re-thought**: a legal clause reused from a different contract may be wrong for this one, however identical the wording (`legal-medical.md`).
- **Short segments**: a memory full of one-word segments produces high leverage figures and no real saving, because the work was never in typing the word.
- **Over-leveraged prose**: text assembled from matched segments reads as assembled. Where a document must flow, budget a full read-through even at high leverage.

## Concordance

The most underused feature: a full-text search across the memory for a phrase, showing every past source-target pair containing it. It answers "how did we translate this last time" in seconds, catches terminology drift the glossary does not cover, and is the fastest way to onboard onto a client's existing voice. Use it before inventing a rendering for anything that sounds like it has appeared before.

## What To Write Down

- **Where the memory lives, which tool owns it, the agreed match grid, and the segmentation rules** go in `## Environment` in `~/Clawic/data/translate/memory.md`. All four change what a job costs, and all four are re-derived painfully when undocumented.
- The **analysis of a large job** — bands, weighted count, agreed grid — is an `artifacts/analysis-<job>.md` when there is any chance of a dispute about the invoice, with its `## Boxes` line in the same turn.
- Leverage actually achieved goes in the delivery row (`deliveries/<year>.md`), because it is the number that makes the next quote accurate.
- A cleanup or alignment review that the user agrees to repeat becomes a row in **`## Due`** (`memory-template.md`).
