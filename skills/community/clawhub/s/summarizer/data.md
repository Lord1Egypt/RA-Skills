# Numbers, Tables, and Reports Made of Data

Scope: earnings reports and filings, financial statements, dashboards, analytics exports, survey results, benchmark runs, spreadsheets, and any source where the payload is figures rather than prose.

**Before summarizing a recurring report**, read `## Sources` in `~/Clawic/data/summarizer/memory.md` (or `sources.md` per the `## Boxes` index) for the previous period's figures, and `glossary.md` for this user's metric definitions — a number without its prior period is a fact, not information, and a metric named differently than last month reads as a change that did not happen.

**Contents:** [The Rule That Governs Everything Here](#the-rule-that-governs-everything-here) · [What a Number Needs](#what-a-number-needs) · [Comparison Is the Content](#comparison-is-the-content) · [Reading a Table](#reading-a-table) · [Financial Reports](#financial-reports) · [Dashboards and Analytics](#dashboards-and-analytics) · [Surveys](#surveys) · [Benchmarks](#benchmarks) · [Charts With No Underlying Data](#charts-with-no-underlying-data) · [Output Shape](#output-shape)

## The Rule That Governs Everything Here

**Copy figures; never derive them.** Any percentage, growth rate, average, total, or ratio that the source did not print is a number you invented, and it will be read as the source's. If a derivation is genuinely needed, it appears outside the summary, labelled as a calculation, with its inputs shown.

The three derivations that look harmless and are not:
- **Summing a column** that the source did not total — subtotals frequently exclude rows, and eliminations are invisible.
- **Computing growth** between two numbers with different scopes ("revenue" in one row, "revenue excluding discontinued operations" in the other).
- **Averaging percentages** — an average of rates is not the rate of the total unless the denominators are equal.

## What a Number Needs

A bare figure in a summary is unusable. Five attachments, all copied from the source:

| Attachment | Example | Failure if dropped |
|---|---|---|
| Unit and currency | `4.2M EUR`, not `4.2M` | The reader assumes their own currency |
| Period | `Q2 2026`, `trailing 12 months`, `as of 30 June` | A month-to-date figure gets compared to a closed month |
| Scope | `EMEA only`, `excluding one-off items` | The number is right and the comparison is wrong |
| Basis | `GAAP`, `constant currency`, `annualized`, `estimate` | An adjusted figure reads as reported |
| Direction and comparator | `up 12% vs Q1`, `vs 3.9M in Q2 2025` | A number with no baseline supports any narrative |

Rounding: keep the source's precision. If the source says 26.4% and the target length forces shortening, write `26%` and say the figures are rounded — never `about 30%`, which is a different number wearing a hedge.

## Comparison Is the Content

A data summary that lists current values has restated the report. The reader wants what changed, by how much, and whether that is unusual.

- **Every headline figure ships with one comparison**: prior period, prior year, or plan. Prior year controls for seasonality; prior period catches turns; plan catches expectation gaps. Say which one you used.
- **Percentage point vs percent.** A conversion rate moving 4% → 5% rose **1 percentage point** and **25 percent**. Both are true, they differ by 25×, and the source's own wording decides which one you copy.
- **Magnitude before rate.** "Support tickets up 300%" from 2 to 8 is noise; state the absolute values whenever the base is small. Rule of thumb: below ~30 events, give the counts and let the rate be secondary.
- **Mix effects.** A total can rise while every segment falls, if the segment weights moved. When segment data is present, check whether the headline change survives the mix — and if it does not, that is the finding.
- **Name the biggest mover, not the biggest number.** The largest line item is usually the same one as last period.

## Reading a Table

1. **Read the header and the footnotes first.** Footnotes carry the scope, the restatements, and the basis change that make the table mean something different from what it looks like.
2. **Find the total and check it against the rows** — not to publish a derived figure, but because a mismatch means the table excludes something the summary must name.
3. **Scan for the largest deltas**, not the largest values.
4. **Look for blanks and dashes** — a missing cell is often the story ("not disclosed this quarter").
5. **Check for a units row** and for magnitudes stated once in the header ("all figures in thousands"), which is the classic 1000× error.
6. **Never reproduce a wide table in a summary.** Take the two or three rows that moved; a pasted table is not a summary.

## Financial Reports

| Layer | What it is | Where the summary looks |
|---|---|---|
| Headline release | The issuer's summary of itself | Orientation only; every figure is chosen |
| Income statement | Revenue through net income | Revenue mix and margin direction, not just the top line |
| Balance sheet | Position at a date | Cash, debt maturities, receivables trend |
| Cash flow | Cash actually moved | Operating cash flow versus net income — a persistent gap is the finding |
| Guidance | Forward statements | Changes in guidance, and any change in the language around it |
| Footnotes | Where accounting choices live | Restatements, one-offs, segment redefinitions, contingencies |
| MD&A / commentary | Management narrative | The explanations given for the numbers, attributed as management's |

- **Adjusted figures are attributed, always.** "Adjusted EBITDA" is a company-defined metric; the summary says whose definition it is and, when the source states it, what was adjusted out.
- **Non-recurring items that recur** every quarter are recurring; if the source shows three consecutive quarters of "one-off" charges, the summary can note the count without judging it.
- **Segment redefinition breaks comparability.** When segments were re-cut, prior-period comparisons in the summary carry a note.
- Forward-looking statements keep their modal: "expects", "targets", "guides to" — never "will".

## Dashboards and Analytics

- **Metric definitions are local.** "Active user" varies by product and sometimes by dashboard. Pull the definition into `glossary.md` on first encounter and use the user's own wording thereafter.
- **Date range and timezone** are part of every number pulled from a dashboard; a "yesterday" panel is timezone-dependent and two panels can disagree for that reason alone.
- **Sampling and thresholds**: many analytics tools sample above a volume and silently switch. If the source shows a sampling indicator, it goes in the summary.
- **Attribution windows** change reported conversions without anything changing in reality. A window change is a bigger story than the number.
- Alerts and anomalies: report the anomaly with its threshold, not just the value — "3,400 errors, threshold 500" is actionable, "3,400 errors" is not.

## Surveys

- **N and response rate**, first line, always. A 12% response rate makes every percentage a statement about respondents, not about the population.
- **Question wording** is copied verbatim for any headline result; the wording produced the answer.
- **Denominators shift per question** when respondents skip. "68% agreed" on a question answered by a third of respondents is 68% of that third.
- **Scale points**: "top-2-box" versus "agree" are different figures; state which.
- Free-text responses are a `threads.md` job: theme them, count them, and quote sparingly with counts (`3 of 40 mentioned pricing`).

## Benchmarks

- **The configuration is the result.** Hardware, version, dataset, concurrency, warm-up, and whether the run was repeated. A benchmark number without its configuration cannot be compared to anything.
- **Distribution over mean.** p50/p95/p99 where the source gives them; a mean latency hides the tail that users actually feel.
- **Who ran it.** Vendor-run benchmarks are attributed (SKILL.md Rule 4).
- **Variance across runs**: a single run is an anecdote; if the source reports run-to-run variance, it survives compression.

## Charts With No Underlying Data

When the source is an image or a chart without a data table:

- Read values as approximate and say so — "roughly 40%, read from the chart".
- Check the axis: truncated y-axes make small changes look dramatic; log scales make large ones look small. If the axis is truncated or logarithmic, the summary says so.
- Never state a precise figure that was estimated from pixels.
- Missing periods on a time axis are a finding.

## Output Shape

```
<Report name> — <period>, <basis>. Source: <issuer/system>, as of <date>.

Headline: <figure with unit, currency, period> — <direction vs named comparator>
Movers: <2-3 biggest changes, each with absolute and relative>
Against plan/prior: <the comparison that matters here>
Definitions in play: <any metric whose definition changed or is non-standard>
Not disclosed: <figures a reader would expect and did not get>
Omitted: <lines not covered>
```

**After summarizing a data source**, register it in `## Sources` in `~/Clawic/data/summarizer/memory.md` with its period and basis so the next edition has a baseline; write the figure block to `summaries/<report>-<period>.md` when `store_summaries: full`; add every non-standard metric definition to `glossary.md` in the same turn — this is the box that prevents the same metric being summarized two different ways in two months; and if the report belongs to a recurring cadence, add its row to `## Due`. Formats and thresholds: `memory-template.md`.
