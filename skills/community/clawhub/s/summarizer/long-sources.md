# Sources Too Long To Read At Once

Scope: books, 300-page reports, full documentation sets, multi-hour transcripts, whole mailboxes — anything where a single pass is impossible, unreliable, or expensive enough to be worth structuring.

**Before starting a long job**, read `## Sources` in `~/Clawic/data/summarizer/memory.md` (or `sources.md`, per the `## Boxes` index): if the source was processed before, its chunk map already exists in `summaries/<source>.md` and re-deriving it is the most expensive avoidable mistake in this skill.

**Contents:** [Decide the Architecture](#decide-the-architecture) · [Chunking](#chunking) · [Map-Reduce](#map-reduce) · [Refine](#refine) · [Hierarchical Maps](#hierarchical-maps) · [Recursion Rot](#recursion-rot) · [Cross-Chunk Arguments](#cross-chunk-arguments) · [Budgeting](#budgeting) · [The Chunk Map Is the Asset](#the-chunk-map-is-the-asset)

## Decide the Architecture

| Source size (words) | Architecture | Why |
|---|---|---|
| <2,000 | One pass, no structure | Chunking a short source only adds seams |
| 2,000-25,000 | One pass, but read the middle deliberately | Fits, yet middle-of-input degradation is already measurable on ranked material |
| 25,000-150,000 | Map-reduce over semantic chunks | Parallel, bounded cost, and the chunk map is reusable |
| >150,000 | Hierarchical: chunk → section → whole | A single reduce step over 200 chunk summaries is itself a long-source problem |
| Any size, high stakes | Map-reduce with spans retained | Every claim keeps a pointer back to its chunk for the faithfulness pass (`verification.md`) |
| Any size, already processed | Load the stored chunk map | Only re-read chunks whose subject the new question touches |

Word count from pages: prose runs ~250-300 words per printed page, ~500 for dense two-column academic layout. A 300-page business book is therefore ~80,000 words — map-reduce territory, not a single read.

## Chunking

- **Split on semantic boundaries, never on a fixed token count.** Chapter, section heading, speaker turn, email message, function, date. A chunk that ends mid-argument produces two summaries that each carry half a claim and neither carries the conclusion.
- **When no boundary exists** (a wall-of-text transcript), fall back to fixed size with **10-15% overlap** so a claim that straddles a seam appears whole in one of the two chunks. Below ~10% the seam loses claims; above ~20% you pay for the same text repeatedly with no additional recall.
- **Size the chunk so the reduce step fits.** Rule: `chunk size ≤ usable context ÷ 4`, because the reduce step must hold many chunk summaries plus the instructions plus the output. Sizing chunks to the maximum makes the merge impossible and forces a second hierarchy level you did not plan for.
- **Carry a header into every chunk**: source title, section title, position ("chunk 7 of 34"), and the document's own date. A chunk summary written without knowing what document it came from generalizes wrongly, every time.
- **Never split a table, a numbered list, or a contract clause.** Structures are read as units; half a table is worse than no table.

## Map-Reduce

The default for long sources. Each chunk is summarized independently, then the chunk summaries are merged.

1. **Map.** One summary per chunk at a fixed ratio — `standard` level per chunk regardless of chunk importance, because importance is not knowable until the merge. Each chunk summary keeps: the chunk's claims with their numbers, the entities introduced, and open threads it did not resolve.
2. **Reduce.** Merge the chunk summaries into the target length. This is where deduplication, ranking, and the point budget (SKILL.md Rule 2) apply — not during the map.
3. **Backfill.** After the merge, any surviving claim whose number or wording is uncertain is checked against its original chunk, not against the chunk summary.

Properties: parallelizable, bounded cost, and independent of chunk order — no position bias. Its one weakness is that no chunk sees any other chunk, so cross-chunk arguments must be recovered deliberately (below).

## Refine

Sequential: summarize chunk 1, then feed that summary plus chunk 2, and so on.

- **Strength**: the running summary carries context forward, so cross-chunk arguments survive naturally. Correct for narrative — a novel, a chronological history, an incident timeline.
- **Failure**: the early chunks get re-compressed at every step and fade, while the last chunk arrives at full fidelity. On ranked or evidential material this produces a summary weighted toward the end of the document for no reason but processing order.
- **Never use refine on**: papers with the findings in the middle, reference documentation, anything the reader will treat as a ranked list.
- Cost is linear and non-parallel: on a 100-chunk source, refine reads roughly twice the text of map-reduce and takes serial time.

## Hierarchical Maps

Above ~150,000 words, one reduce step is itself too long.

```
Level 0: source
Level 1: chunk summaries, standard level, one per semantic chunk  ← the reusable asset
Level 2: section summaries, one per group of ~8-15 level-1 summaries, following the source's own structure
Level 3: the delivered summary, at the requested length
```

- Group level-1 summaries by the source's structure (parts, chapters, months), never by arbitrary count — a section summary spanning two unrelated chapters is a chunk boundary problem again, one level up.
- Every level records what it dropped. Without that, level 3 has no way to answer "was anything about X in there?" except by re-reading level 0.
- Level 1 is written to disk (below). Levels 2 and 3 are outputs.

## Recursion Rot

Each summarization generation loses in the same direction: specifics out, abstractions in. Three generations of a business chapter reliably converge on the genre's platitudes, and every generation reads plausible, which is why nobody catches it.

- **Rule**: the delivered summary is at most one generation from the level it was built on, and the level-1 chunk summaries are always one generation from the source (SKILL.md Rule 5).
- **A shorter version is re-derived, not re-compressed.** Asked for 100 words after delivering 400, go back to level 1 and merge to 100. Compressing your own 400 words produces a summary of your prose style.
- **The one legitimate multi-generation case** is the hierarchy above, where each level is a merge across siblings rather than a re-compression of the same text — and even there, numbers and quotes are pulled from level 1, never re-copied from level 2.

## Cross-Chunk Arguments

Map-reduce's blind spot, and the reason a mechanical long-source summary reads like a table of contents.

| Pattern | How it hides | Recovery |
|---|---|---|
| Thesis in chapter 1, proof in chapter 9 | Chunk 1 records a claim with no support; chunk 9 records evidence for nothing | Reduce step joins claims to orphan evidence by subject before ranking |
| Definition introduced once, used throughout | Later chunks summarize a term they cannot expand | Entity pass: collect first-use definitions in the map, resolve in the reduce, add recurring terms to `glossary.md` |
| A number restated with different scope | Two chunks report "revenue 4.2M" and "revenue 4.2M excluding EMEA" | Numbers carry their qualifier from the map stage; conflicts go to the reduce as conflicts, not as a pick |
| Contradiction between sections | Each chunk is internally consistent | Ask explicitly at the reduce: does any pair of chunk claims disagree? A contradiction inside one source is a finding, not noise |
| Running narrative or argument arc | Chunks report events with no arc | Add a one-line "position in the argument" field to each chunk summary during the map |

## Budgeting

- **Words to tokens**: `tokens ≈ words × 1.3` for English. Compute the source's token cost before choosing an architecture; a 500-page report is not a one-pass job at any price.
- **Map-reduce total reads** ≈ source once + chunk summaries once. **Refine total reads** ≈ source once + the running summary once per chunk, which on many chunks approaches double.
- If a source is going to be queried repeatedly, the level-1 map pays for itself on the second question. If it is a one-off at `brief` length, a single pass over the source with a deliberate middle read is cheaper and better.

## The Chunk Map Is the Asset

The delivered summary is disposable; the level-1 map is not. It is what makes the next question about the same book answerable in seconds instead of a full re-read.

**After processing a long source**, write the level-1 chunk map to `~/Clawic/data/summarizer/summaries/<source-kebab>.md` under `## Chunk Map` (subject to `store_summaries`, and never with intact secrets), register the source in `## Sources` in `memory.md` with its size, architecture used, and chunk count, and add the `## Boxes` line in the same turn. Terms and entities the map resolved go to `glossary.md`. Formats and thresholds: `memory-template.md`.
