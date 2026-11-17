# Report contract, citations, and failure handling

Load this reference in the final reporting step.

## Output contract

1. **Audit frame** — page, screen, or task flow; type; goal; users; traffic source when relevant;
   data; viewport.
2. **Verdict** — two sentences: biggest conversion cost and first fix.
3. **Findings table** — fewer than 15 rows; group minor issues.

   | # | Criterion ID | Finding | Evidence on page | Score | Exposure | Severity | Effort | Source |
   |---|---|---|---|---|---|---|---|---|

4. **Top three fixes** — change, expected effect, ROI range, and assumptions.
5. **What passed** — elements the redesign should preserve.
6. **Not assessed** — unobserved items and how to check them.
7. **Observations outside the criteria** — optional, explicitly uncited and excluded from ranking.
8. **Sources** — full entries from `ATTRIBUTION.md` for every cited source.

## Citation and reuse rules

- Cite every sourced finding as author, year, and chapter, for example
  `(Loveday & Niehaus 2008, ch. 8)`.
- Paraphrase. Do not reproduce source passages, checklists, tables, figures, or worked examples.
- If a direct quote is unavoidable, use at most one per report and keep it below 15 words.
- Treat white-paper statistics as secondary citations: `(Nielsen 1997, as cited in Marcus 2004)`.
  Retain intermediary sources when present, for example `(Spool / UIE 1998, as cited in Nielsen
  1998, as cited in Marcus 2004)`.
- Never present an old case figure as a current benchmark. Load `source-limitations.md` and give
  its year.
- Always end the report with full source references.

## Failure handling

| Situation | Action |
|---|---|
| No success goal | Stop and ask for the one conversion or task outcome that counts. |
| Whole-site or whole-product request | Ask for funnel or task data, then audit the page or flow with the largest loss. |
| No value data | Audit qualitatively and name the missing revenue or cost inputs. |
| Guaranteed uplift requested | Decline; give a range and assumptions. |
| Brand or legal constraint conflicts with a criterion | Record the constraint with the finding. |
| Copy rewrite requested | Finish the audit, then hand off to a content-design workflow. |
| Source statistic looks implausible | Give the original study and year; do not generalize it. |

## Final checklist

- [ ] Every ranked finding has a criterion ID, page evidence, and source.
- [ ] Uncited observations are labelled and excluded from ranking.
- [ ] No source text is reproduced; at most one quote below 15 words.
- [ ] Every statistic names the original study and year.
- [ ] Estimates are ranges with assumptions, annual value, and payback period.
- [ ] Unobserved items are listed under “Not assessed”, not scored.
- [ ] The report ends with full source references.
