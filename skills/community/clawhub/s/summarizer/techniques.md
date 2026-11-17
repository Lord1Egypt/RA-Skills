# Choosing the Method

Scope: how the summary gets produced — extractive, abstractive, or hybrid; single pass or staged; with or without a critique loop. Architecture for oversized inputs is `long-sources.md`; checking the result is `verification.md`.

**Before deriving a method, a prompt shape, or a slot list**, check `templates/` through the `## Boxes` index in `~/Clawic/data/summarizer/memory.md`: a stored template exists for any job the user has run twice, and re-deriving one produces a second shape for the same job, which is what makes a repeating deliverable stop being comparable.

**Contents:** [Extractive, Abstractive, Hybrid](#extractive-abstractive-hybrid) · [Method by Stakes](#method-by-stakes) · [The Staged Pass](#the-staged-pass) · [Instruction Patterns](#instruction-patterns) · [Few-Shot](#few-shot) · [Role Framing](#role-framing) · [Self-Critique](#self-critique) · [Query-Focused Summaries](#query-focused-summaries) · [What Not To Do](#what-not-to-do)

## Extractive, Abstractive, Hybrid

`default_mode` sets the default; the source and the stakes override it.

| Mode | What it does | Strength | Failure |
|---|---|---|---|
| Extractive | Selects sentences from the source, unchanged | Cannot fabricate; every claim is verbatim and checkable | Reads badly; a sentence torn from its context can mislead while being word-perfect; cannot compress below the granularity of a sentence |
| Abstractive | Rewrites in new language | Compresses far tighter; can merge and rank; reads as prose | Can fabricate, and fabricates fluently |
| Hybrid | Extract the load-bearing spans first, then rewrite with only those spans in view | Keeps the fidelity anchor and the readability; the extract doubles as the fan-out source (`audience.md`) | Two stages, so it costs more |

Hybrid is the default here because the extract stage is exactly what the faithfulness pass needs later: a list of spans that every summary sentence can point back to.

**The extract stage is not a summary.** It is a longer-than-the-deliverable list of the claims that carry the source, each with its numbers, hedges, attribution, and location. Compression happens in the rewrite, not in the extraction — extracting selectively is how the coverage failure gets baked in before you start writing.

## Method by Stakes

| Situation | Mode | Why |
|---|---|---|
| Legal, medical, financial, regulatory | Extractive or hybrid with spans attached | The reader must be able to check every claim against the document |
| Anything published under the user's name | Hybrid, plus both verification passes | The reputational cost of a fabricated detail is asymmetric |
| Quotable material (press, court, board) | Extractive for the quotes, abstractive for the frame | Quotes are never paraphrased (`media.md`) |
| Internal, low-stakes, disposable | Abstractive, single pass | Verification cost exceeds the value |
| Recurring series | Whatever the template fixed | Consistency across editions beats per-edition optimization (`recurring.md`) |
| Source in another language | Hybrid, with the original wording kept for anything quoted | Translation plus compression compounds two lossy steps |
| Very long source | Hybrid per chunk, abstractive at the merge | Extraction preserves the numbers through the chunk boundary |
| Anything else | `default_mode` | — |

## The Staged Pass

For anything above a `brief`, separate the stages. Doing extraction, ranking, and writing simultaneously is what produces a summary that follows the source's structure instead of the reader's need.

1. **Orient** — structure only: headings, first lines, length, date, genre. Decides the reading strategy (SKILL.md, Where The Payload Lives).
2. **Extract** — the load-bearing claims with their numbers, hedges, and attribution. No compression yet.
3. **Rank** — by consequence to the named reader, not by the source's emphasis. Apply the point budget: `target words ÷ 25`.
4. **Write** — from the extract only, at the target length.
5. **Verify** — faithfulness then coverage (`verification.md`).

Where each stage fails: skipping orient produces the wrong reading order for the genre; skipping extract produces a summary of the parts you happened to remember; skipping rank produces a table of contents; skipping verify produces the errors this skill exists to prevent.

## Instruction Patterns

When the job is being specified — for yourself, for a batch, or for a repeated pipeline — the specification carries five things. Anything missing gets defaulted, usually wrongly.

| Element | Specify as | Default if omitted |
|---|---|---|
| Length | An absolute number of words, not "short" | Whatever the writer feels; always wrong twice |
| Reader | Who and what they will do next | A generic reader, which produces a generic summary |
| Must-keep | The classes that cannot be cut in this domain | Nothing protected; the qualifiers go first |
| Shape | The slots, in order (`formats.md`) | The source's structure |
| Omission policy | Whether to state what was cut | Silence |

Two patterns that earn their cost:

- **Constrained rewrite**: give the target length, the reader, and the protected classes, and require the output to end with the omission line. The omission requirement alone improves ranking, because it forces the cuts to be explicit rather than accidental.
- **Slot filling**: give the fixed slots and require every one to be filled or marked "not stated in the source". This is what makes a series comparable and what surfaces gaps instead of hiding them.

## Few-Shot

- **Use examples when the shape is unusual or must match a series**, not for ordinary summarization — the shape is the thing examples transmit reliably.
- **Two or three examples, same genre, same length band.** Examples from a different genre transfer their structure to the wrong content.
- **Examples teach shape and register; they also teach length.** An example longer than your target will pull the output long.
- The durable form of a good example is a stored template (`formats.md`), not an example re-pasted each time.

## Role Framing

Framing the writer as a domain reader ("write this as the on-call engineer would need it") changes vocabulary, deletion order, and what counts as important. It does not change what is true.

- It is a shortcut for the audience deletion order in `audience.md`, useful when that order is obvious from the role and tedious to spell out.
- **It must never license invention.** A role frame that produces domain claims the source did not contain is the frame doing the work instead of the source.
- Prefer naming the deletion order explicitly when the stakes are high; roles are compact but imprecise.

## Self-Critique

A second pass over your own summary, with the source available and a rubric.

- **With a rubric and the source, it works**: it finds omissions, unsupported claims, and length overruns reliably.
- **Without them, it does not**: "improve this summary" produces a longer summary with more hedging, every time.
- **The productive rubric is the Output Gates** in `SKILL.md`, run as questions rather than as a checklist read.
- **One critique pass.** A second pass starts rewriting prose rather than fixing claims, and rewriting prose is how a verified summary drifts back out of fidelity.
- Critique is not re-summarization: it edits the existing text against the source, and never regenerates from the summary (SKILL.md Rule 5).

## Query-Focused Summaries

When the user has a question rather than a request to summarize ("what does this say about pricing?"), the job changes shape.

- **The question sets the ranking**, and everything not relevant to it is cut regardless of how central it is to the source.
- **Say what the source covers that the question did not ask about**, in one line — otherwise the user believes the document is about their question.
- **"The source does not address this" is a complete and valuable answer.** Producing a plausible answer from adjacent material is the characteristic failure here, and it is worse than in ordinary summarization because the user asked precisely because they could not find it.
- Long sources: run the query against the chunk map rather than re-reading (`long-sources.md`).

## What Not To Do

| Approach | Why it fails |
|---|---|
| Reading and writing at the same time | Produces the source's structure with fewer words |
| Compressing your own draft to hit a length | One generation further from the source each time (SKILL.md Rule 5) |
| Asking for "the key points" with no count | Returns whatever number is habitual, usually five, regardless of the source |
| Optimizing for a similarity metric | Rewards copying the reference's wording (`verification.md`) |
| Chunking a source that fits | Adds seams and cross-chunk losses for no benefit |
| A role frame instead of a reader | Produces the register without the deletion order |
| Summarizing before knowing the target length | The commonest cause of a second round trip |

**When a method, prompt shape, or slot list works for a job that will repeat**, store it as `~/Clawic/data/summarizer/templates/<job>.md` with a one-line note of when to use it, and add its `## Boxes` line in the same turn; record a stated method preference (extractive for contracts, always-verify for published work) as a key in `config.yaml`. Formats and thresholds: `memory-template.md`.
