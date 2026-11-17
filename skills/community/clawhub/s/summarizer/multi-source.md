# Several Sources, One Account

Scope: N documents on one subject — competing news coverage, a set of papers, three vendor proposals, a stack of customer interviews, several reports on the same market. The output is one account that preserves disagreement instead of averaging it away.

The boundary with the `synthesize` skill is the deliverable, and it is the same line as SKILL.md Rule 9: here the product is **shorter than the inputs and contains no claim the sources did not make** — every line traces to a source and a disagreement is reported, not resolved. When the user wants the conclusion drawn across the sources — a recommendation, a resolved contradiction, a coverage verdict of their own — that is insight generation and belongs to `synthesize`; if it ships from here, it ships labelled as judgment, outside the summary.

**Before starting a synthesis**, read `## Sources` in `~/Clawic/data/summarizer/memory.md` (or `sources.md` per the `## Boxes` index) for sources already processed and their summaries, and the project file at `~/Clawic/data/projects/<project>.md` if the synthesis belongs to one. Re-reading a source you already summarized is how two halves of one synthesis end up contradicting each other.

**Contents:** [Summarize Each Source First](#summarize-each-source-first) · [The Coverage Matrix](#the-coverage-matrix) · [Handling Disagreement](#handling-disagreement) · [Source Independence](#source-independence) · [Weighting](#weighting) · [Deduplication](#deduplication) · [Comparing Options](#comparing-options) · [Citation Density](#citation-density) · [Output Shapes](#output-shapes)

## Summarize Each Source First

Never synthesize by reading everything at once and writing an impression. The pipeline is fixed:

1. **Per-source summary** at `standard` level, each one carrying claims with their numbers, the source's date, and its status (peer-reviewed, vendor, anonymous).
2. **Matrix** — claims as rows, sources as columns (below).
3. **Synthesis** — written from the matrix, not from the sources.

Skipping step 2 produces a synthesis that reflects reading order: whatever you read first frames everything after it, and whatever you read last is freshest. The matrix is what makes the output independent of the order you happened to open the files in.

## The Coverage Matrix

Rows are claims or dimensions; columns are sources. Cells are the source's position, with its number.

```
| Claim / dimension | Source A (2026, RCT) | Source B (2025, vendor) | Source C (2026, cohort) |
|---|---|---|---|
| Effect on latency | −40 ms (CI −55 to −25) | "up to 60% faster" | not measured |
| Cost at 1M requests | 120 USD/mo | not stated | 180 USD/mo |
| Failure mode under load | queue backs up | not addressed | queue backs up |
```

The matrix makes three things visible that prose hides:

- **Empty cells are findings.** A dimension every source ignores is a gap in the literature or in the vendor market, and it is often the most useful line in the synthesis.
- **Single-source claims** are visible as such — one column filled, the rest empty. These are reported with attribution and never as consensus.
- **Real disagreement** separates from apparent disagreement caused by different units, periods, or populations. Normalize the cells' units before concluding that two sources conflict; most conflicts dissolve here.

Store the matrix as an artifact when it took real effort to build (below) — it is the reusable asset, the synthesis is the disposable output.

## Handling Disagreement

Averaging is the failure. "Estimates range from 12% to 47%" is a finding; "roughly 30%" is a fabrication that no source supports.

| Situation | Do |
|---|---|
| Two credible sources, different numbers | Report the range, name who holds each end, and give the reason if the sources give one (different population, period, or method) |
| Difference explained by method | Say so — "the RCT finds no effect; the observational study finds one, consistent with confounding" is the whole answer |
| One source is newer and supersedes | Report the newer, note the older and its date; a superseded figure is still cited elsewhere and the reader needs to recognize it |
| One source is an interested party | Report both, attributed; do not resolve on authority alone |
| Sources disagree on a fact, not an estimate | Report the disagreement as unresolved; a fact both cannot hold is a signal about at least one of them |
| Only one source addresses it | Attribute it explicitly and note that it is uncorroborated |
| Sources agree | Say how many, and check independence before calling it corroboration |
| Anything else | Report both positions with their sources and state that the disagreement is unresolved; never pick on tone or fluency |

## Source Independence

Agreement between sources is only evidence if the sources are independent. In practice they frequently are not.

- **Citation chains**: three articles reporting one original study are one source. Trace claims back to the first appearance before counting agreement.
- **Shared data**: two analyses of the same dataset agree by construction.
- **Wire copy**: many outlets publish the same agency story with a new headline.
- **Vendor-funded studies** across a market often share a methodology consultant.
- The counting rule: `independent sources`, not `documents`. Say the number, and say it as documents when independence cannot be established: "reported by 6 outlets, all tracing to one Reuters story".

## Weighting

Rank sources before writing, and state the ranking's basis once.

| Dimension | Higher weight |
|---|---|
| Directness | Primary document or original data over reporting about it |
| Method | Design that supports the claim being made (`research.md`) |
| Recency | Newer, in domains that move; irrelevant in domains that do not — say which case applies |
| Independence | No stake in the result |
| Specificity | Sources that state numbers, scope, and method over those that assert |
| Reproducibility | Data, code, or methodology available |

Never weight by prominence, by how confidently a source writes, or by how well the claim fits the rest of the synthesis.

## Deduplication

- **Claim-level dedup, not document-level.** Two documents overlapping 80% still contribute one distinct claim each.
- **Normalize before comparing**: units, currency, time period, population. "4.2M EUR in FY25" and "$4.6M in calendar 2025" may be the same fact.
- **Near-identical wording across sources** signals copying, not corroboration — flag it rather than counting it twice.
- Keep one canonical statement per claim and attach every supporting source to it, so the synthesis reads once and cites many.

## Comparing Options

Vendor proposals, tool evaluations, and approach comparisons are the applied case of the matrix.

- **Dimensions come from the reader's decision, not from the vendors' feature lists.** A matrix built from vendor materials reproduces whichever vendor wrote the best marketing.
- **"Not stated" and "not supported" are different cells** and the difference decides purchases.
- **Price needs its basis**: per seat, per unit, minimum commitment, and what is excluded (`legal.md` for the contract-side reading).
- **Rank on the two or three dimensions that would change the decision**; a fifteen-row matrix scored equally makes every option look similar.
- If the user wants a recommendation rather than a comparison, that is a decision document — `brief`.

## Citation Density

- **Every claim in the synthesis carries its source**, by short key (`[A]`, `[Smith 2026]`) matching the source table at the bottom. A synthesis without per-claim attribution cannot be checked and will not be trusted.
- **Consensus claims cite the count, not every source**: "all four sources [A-D]".
- **Never cite a source for a claim it does not make** — the most common synthesis error, produced by a citation drifting one sentence during editing. The faithfulness pass in `verification.md` checks citations as well as claims.

## Output Shapes

**Synthesis:**
```
<Question the synthesis answers> — <N> sources (<M> independent), <date range>.

Settled: <claims all or most sources support> [refs]
Contested: <claim> — <range or positions>, held by <who>, differing because <reason if known> [refs]
Single-source: <claim> [ref] — uncorroborated
Gaps: <dimensions no source addresses>
Sources: <key — citation, date, type, stake>
```

**Option comparison** delivers the matrix itself plus three lines: the dimension that separates the options, the one that surprised, and what is missing from every option.

**After a synthesis**, write the coverage matrix to `~/Clawic/data/summarizer/artifacts/<topic>-matrix.md` from the first one — it is a long text read whole when the topic returns — and add its `## Boxes` line with a read condition in the same turn. Register every source processed in `## Sources` in `memory.md` with its independence note, so the next pass does not double-count; write the synthesis to `summaries/<topic>-synthesis.md` when `store_summaries: full`; add domain terms to `glossary.md`; and if this is ongoing research or an evaluation, record the conclusion and its date in `~/Clawic/data/projects/<project>.md`. Formats and thresholds: `memory-template.md`.
