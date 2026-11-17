# Papers, Studies, and Scientific Claims

Scope: journal articles, preprints, systematic reviews, meta-analyses, clinical trials, technical reports, and white papers. The failure mode here is not omission — it is stating a finding with more certainty, more scope, or more generality than the paper does.

**Before summarizing into an ongoing literature effort**, read the project file at `~/Clawic/data/projects/<project>.md` and `## Sources` in `~/Clawic/data/summarizer/memory.md` (or `sources.md` per the `## Boxes` index): a paper already summarized has a file, and a synthesis that re-reads the same paper twice will contradict itself.

**Contents:** [The Abstract Is Not The Paper](#the-abstract-is-not-the-paper) · [Reading Order](#reading-order) · [The Claim Frame](#the-claim-frame) · [Numbers That Must Survive](#numbers-that-must-survive) · [Study Types and What They Support](#study-types-and-what-they-support) · [Red Flags](#red-flags) · [Systematic Reviews and Meta-Analyses](#systematic-reviews-and-meta-analyses) · [Preprints and Status](#preprints-and-status) · [Output Shapes](#output-shapes)

## The Abstract Is Not The Paper

The abstract is the authors' own summary, optimized for citation, and by convention it omits limitations, negative secondary outcomes, and the gap between what was measured and what is claimed. Summarizing it reproduces the spin with your name on it.

- **The Discussion says what the authors think it means; the Results say what happened.** When they disagree — Results show a non-significant primary outcome, Discussion emphasizes a significant subgroup — that disagreement is the most important thing in the paper and belongs in the summary.
- **Limitations are a section, not a caveat.** Papers that do not have one have hidden it in the Discussion's final paragraph.
- **The title frequently overstates.** "X improves Y" over a study that measured a surrogate marker in 24 people is a headline, not a finding.

## Reading Order

1. **Abstract** — for orientation only: what was studied, in whom, roughly what was found. Two minutes; do not take claims from here.
2. **Figures and tables with their captions** — the actual results, before any prose framing. Most papers can be summarized from figures plus methods.
3. **Methods** — design, population, N, comparison, primary outcome, pre-registration. This is what decides whether the claim is supportable.
4. **Results** — the numbers, especially the ones the abstract did not mention.
5. **Limitations** — the paper's own list of what it cannot conclude.
6. **Discussion** — last, and read as argument rather than as finding.
7. **Funding and conflicts** — one line, always checked, mentioned in the summary when the funder has a stake in the result.

## The Claim Frame

Every finding in the summary carries five slots. A finding missing any of them is not summarized, it is amplified.

| Slot | Example | Failure if dropped |
|---|---|---|
| Claim with its hedge | "was associated with a reduction in" | Becomes "reduces" — correlation upgraded to cause |
| Population | "in 240 adults aged 40-65 with type 2 diabetes" | Becomes a claim about everyone |
| N and design | "randomized, double-blind, 12 weeks" | An 18-person open-label pilot reads like a trial |
| Effect size with its unit and interval | "HbA1c −0.4% (95% CI −0.7 to −0.1)" | "Significant improvement" hides a clinically trivial effect |
| Comparator | "versus placebo" / "versus standard care" | Versus-placebo results read as versus-best-available |

Worked example. Source: "In a 12-week randomized trial of 240 adults with T2D, the intervention was associated with a mean HbA1c reduction of 0.4% (95% CI −0.7 to −0.1) versus placebo; the effect was not significant in the subgroup over 65."
- Wrong: "The intervention lowers HbA1c."
- Right: "12-week RCT, 240 adults with T2D: mean HbA1c 0.4 points lower than placebo (95% CI −0.7 to −0.1); no significant effect in over-65s."

## Numbers That Must Survive

- **Effect size, not just significance.** "p < 0.05" says the effect probably is not zero; it says nothing about whether it matters. A summary carrying p-values but no effect size has kept the least useful number in the paper.
- **Absolute before relative.** "Risk fell 50%" from 2 in 10,000 to 1 in 10,000 is a relative risk reduction of 50% and an absolute reduction of 0.01 percentage points. When the source gives both, both go in; when it gives only relative, say "relative".
- **Confidence intervals travel with their point estimate.** An interval crossing the null is a null result however the abstract phrases it.
- **N per arm, not just total.** 240 total in an unbalanced design can be 200 versus 40.
- **Attrition.** Dropout above ~20% changes what an intention-to-treat result means; if the paper reports it, the summary reports it.
- Never compute a number the paper did not state — no converting to percentages, no pooling arms, no annualizing. Derivation is analysis, and it is labelled as yours if it appears at all.

## Study Types and What They Support

| Design | Supports | Never supports |
|---|---|---|
| Systematic review / meta-analysis of RCTs | The strongest available effect estimate, if the included studies are homogeneous | More than its inputs — garbage in, pooled garbage out |
| Randomized controlled trial | Causal claim within the trial's population and duration | Generalization beyond the enrolled population |
| Prospective cohort | Association over time, plausible temporality | Causation; residual confounding is always available |
| Case-control | Association for rare outcomes | Incidence or risk in the general population |
| Cross-sectional survey | Prevalence at one moment; correlation | Any direction of causality |
| Case series / case report | Existence proof, hypothesis generation | Frequency, effectiveness, or risk |
| Animal or in-vitro study | Mechanism | Any human claim — "in mice" is not an optional qualifier |
| Modeling / simulation | The consequences of the assumptions | Anything the assumptions were not tested against |
| Anything else | State the design in the summary and let the reader weight it | — |

## Red Flags

Signals that the summary must carry forward; they change how a reader should act on the finding. Anything in this table appears in the summary even when the point budget is tight — it is the difference between a compression and a misrepresentation.

| Signal (observable) | Suspicion | Action in the summary |
|---|---|---|
| Primary outcome in the registration differs from the one reported | Outcome switching | State that the reported primary outcome differs from the pre-registered one |
| Effect appears only in subgroups | Post-hoc slicing | Report the primary outcome first, subgroups as exploratory |
| No confidence intervals anywhere | Precision hidden | Say the paper reports significance without effect precision |
| Funder benefits directly from the result | Sponsorship effect | One line naming the funder |
| Surrogate endpoint stands in for the outcome people care about | Extrapolation | Name the surrogate: "reduced LDL", not "prevented heart attacks" |
| N under ~30 per arm | Underpowered; effect estimate unstable | Give N per arm in the first line |
| Preprint, no peer review | Unvetted | "Preprint" travels with every claim |
| Retraction or expression of concern on record | The paper is not usable | Do not summarize it as a finding; report the retraction |

## Systematic Reviews and Meta-Analyses

- **The inclusion criteria are the finding.** A review of 4 studies out of 800 screened is a statement about those 4 and about the 796 exclusions; the summary carries both counts.
- **Heterogeneity** (reported as I², a percentage of variation not due to chance): high heterogeneity means the pooled estimate averages studies that were measuring different things. Report it when the source does.
- **Publication bias** assessments (funnel plot, Egger's test) belong in the summary when the review performed one and it was positive.
- A meta-analysis of observational studies pools associations, not causes, no matter how many participants it totals.

## Preprints and Status

Status is a property of the claim, not a footnote (SKILL.md, What Compression Destroys First).

| Status | Carry as |
|---|---|
| Peer-reviewed, published | Journal and year |
| Preprint | "preprint" attached to the claim, plus the server |
| Conference abstract | "conference abstract" — often never published in full |
| Retracted / corrected | Never summarized as a finding; report the retraction and its date |
| Industry white paper | Named as vendor-published; treat every figure as attributed (SKILL.md Rule 4) |
| Under embargo or confidential draft | Say so; it may not be quotable at all |

## Output Shapes

**Single paper, standard length:**
```
<Title> — <authors, year>, <journal or preprint server>. <design>, n=<N>.
Question: <what it set out to test>
Finding: <claim with hedge, effect size + interval, comparator, population>
Limitations: <the two that most constrain use>
Not shown: <what the design cannot support>
```

**One-line citation form** for a literature list: `<first author> <year>: <design>, n=<N> — <finding with effect size> [<status>]`.

**Literature matrix** across papers (one row per paper: citation, design, N, population, effect, quality note) is a synthesis artifact — build it in `multi-source.md` and store it as an artifact.

**After summarizing a paper**, register it in `## Sources` in `~/Clawic/data/summarizer/memory.md` with its citation, design, and where the full summary lives; write the summary itself to `summaries/<first-author>-<year>.md` when `store_summaries: full`; add domain terms and abbreviations to `glossary.md`; and, if this belongs to a literature review or ongoing research, add the finding line to `~/Clawic/data/projects/<project>.md` and store any matrix at `artifacts/<topic>-matrix.md` with its `## Boxes` line. Formats and thresholds: `memory-template.md`.
