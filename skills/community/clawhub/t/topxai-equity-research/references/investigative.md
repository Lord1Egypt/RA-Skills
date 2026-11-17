# investigative.md — Building the case: the claim, new facts, and evidence a reader can check

Added in 1.1.0. We read a 54-page investigative report on a listed utility (Muddy Waters on Edison International,
2026-10-13) next to our own company deep dives. The gap was method, not data volume:

| | The investigative report | A typical deep dive written with version 1.0 of this skill |
|---|---|---|
| Length | 54 pages, about 33 in the body | Over 60,000 words in the body alone |
| Conclusion | The title is the claim; the first summary paragraph gives the per-share impact | A subtitle with five numbers; a thesis paragraph with two dozen |
| New facts | An admission buried in a regulatory filing years earlier; a budget line cut to zero in rate-case workpapers; a failed safety step recorded in an incident report; distances measured on satellite imagery | Re-computing figures already filed in the 10-Q and XBRL |
| Sources | 159 footnotes, each to a section, page or table, with a date and URL | Almost no links; thousands of inline [A]-[D] tags |
| Exhibits | 19, mostly screenshots of the company's own documents with a red box | None from primary documents; only our own charts |
| Internal codes in the text | None | Audit and model codes the reader cannot decode |

This file turns what the investigative report does well into rules. Section 8 lists what not to copy.
`scripts/check_report.py` measures the parts that can be counted (the step 3 gate).

---

## 1. Claim first: one sentence and a value bridge

The kickoff produces a **falsifiable claim with a per-share impact**, not "a study of company X". The example report's title
is its claim ("should be liable for ~$20 billion"), and its summary gives the per-share figures for each outcome.

The **value bridge** is the mechanism that turns facts into money. Find the mechanism first, then collect evidence; every
section of evidence must land on one input of the bridge. A finding that lands on no input is news and stays out of the body.

| Mechanism | How a fact becomes per-share value |
|---|---|
| Statutory or contractual caps and their exceptions | Whether the cap applies: a capped liability versus an uncapped one |
| Debt covenants, maturities and cross-defaults | Trigger, acceleration, refinancing cost or dilution |
| Lease and contract terms | Termination rights, credit support, start conditions, then the present value of the receivable |
| Dilution channels | ATM programs, convertibles, warrants, restricted stock, then the share count |
| Regulated rate base | Whether capital spending is allowed into the base, then the allowed return |
| Impairment, reclassification and accounting judgments | The trigger, then equity and earnings |
| Funding gaps in a capital program | The period-by-period cash ledger (`judgment.md` section 5), then new shares or debt |

Every per-share conversion states five things: the share count basis (cover-page count and its date), the tax rate, the
discount rate, the timing convention, and whether the figure is probability-weighted. **All scenarios use one timing
convention.** Recomputing the example report under its own stated assumptions, its lower scenario discounts "year three"
over three periods and its higher scenario over two; on a consistent convention the higher figure comes out about a tenth
lower than printed. Keep one timing function in `calc/model.py` and call it from every scenario.

Show at most three outcomes, each one sentence of trigger plus a per-share value. The 12-month rating is still
probability-weighted and settleable (`judgment.md` section 4); print the outcomes and the weighted value side by side.

## 2. New facts: at least three

A **new fact** is a primary-source fact the market has not absorbed that changes an input of the value bridge. Re-computing
filed numbers does not count. Kickoff gate (step 1): at least three, each with four things written down: the text and its
location (page, section or table); why the market missed it (what kind of document, which page, how long the document is);
which input of the bridge it changes; and by how much. Without three, do not publish, or downgrade to a short note and give
the user the reasons. That is a deliverable (`pipeline/01-kickoff.md`).

Where new facts usually hide (the SEC financial statements are one cell of this table):

| Category | Where to look | What the example report used |
|---|---|---|
| SEC documents beyond the statements | 8-K exhibits (full contracts and credit agreements), S-1 / S-3 / 424B terms, DEF 14A compensation scorecards, Form 4 footnotes, SEC correspondence (CORRESP / UPLOAD), the 10-K exhibit index | The proxy's safety scorecard marked "no deduct"; a target lowered after the event |
| Regulatory dockets | FERC eLibrary, state utility commissions, grid operators' interconnection queues and studies, state environmental permits, FCC, FDA, NRC | Wildfire mitigation plans, rate-case workpapers, data-request responses, incident reports, exercise scripts in Excel |
| Courts and bankruptcy | PACER, CourtListener, state courts, bankruptcy dockets (the company, its customers, counterparties and suppliers) | The company's countersuits |
| Local government | Planning and zoning minutes, building and power permits, tax-abatement agreements, county property-tax records, council meeting video | A city's emergency declaration |
| Procurement and funding | USAspending, SAM.gov, state procurement, municipal bond filings (EMMA) | |
| The company's own earlier words | Past investor decks, earnings calls, responses to regulators, old web pages (Wayback Machine) | Year-by-year statements about a model upgrade, 2019-2026 |
| The physical world and outside data | Satellite imagery and measurements, weather and grid data, dated construction photos, job postings | Span lengths measured on satellite imagery; grid load; weather-station readings |
| Media and social posts | Leads only, graded [B] or [D]; go back to a primary source before using one | News reports of surveillance video |

Not used: anonymous expert interviews. The example report quotes three anonymous former employees; a reader cannot verify
them, and this skill has no expert network or the compliance process one needs. Anonymous statements never enter a payload
chain.

## 3. Let the company speak

The strongest evidence is the company's own words failing to line up. Four forms:

1. **Statement comparison table**: what the company said about the same matter to regulators, to investors and to the
   public, and in different years. Quote verbatim; date and source each line.
2. **Year-by-year statement timeline** (an appendix): the company's commitments, budgets and outcomes on the key matter,
   year by year. Laid out like this, "knew and delayed" needs no further argument.
3. **The same sentence, year after year**: place several years of the same passage side by side and mark the words that
   changed.
4. **Budget against promise**: does the thing the company said it would do have money in the budget, the capital plan or
   the headcount?

Keep quotations in the original language. A translated edition puts the original in quotation marks followed by the
translation; the translation must not strengthen or soften the company's wording.

## 4. Get times and places right

- Date key events to the day, and to the minute where it matters; put them in a timeline table.
- Draw a map where one helps (sites, lines, counterparties, interconnection points), and state the base map and the method.
- State how you measured anything you measured, and which way the error runs ("straight-line distance, so conservative").
- Every number carries its date and basis; never compare numbers from different dates in one sentence.

## 5. Take apart the company's account, point by point

List management's public statements on the point in dispute (calls, interviews, releases, responses to regulators). For
each, write four cells: the statement; the fact it depends on; what the documents show; holds / partly holds / does not
hold. This goes in Part 3 of the report, next to the answers to the opposing side of the debate (`pipeline/03-writing.md`).

## 6. How far inference may go

| State of the evidence | How to write it |
|---|---|
| The primary document's own words | State it directly; the footnote points to the exact place |
| Inferred from several primary facts | "We infer", "in our view", and write out each step |
| This report's estimate | "This report estimates"; formula and inputs in Appendix D |
| Not found | "Not disclosed" or "we did not find", and say where you looked |

Draw no legal conclusions: do not write "fraud", "willful" or "illegal". You may write "inconsistent with its 2022
regulatory filing". Make no moral judgments. Hedge in line with the evidence grade: an [A] fact is not hedged; inference is
written as inference.

## 7. How the evidence is shown

- **Footnotes**: every key number and every quotation carries a footnote to the page, section, table or note number, with a
  URL and the evidence grade at the end. Format in `pipeline/03-writing.md`, "Sources and footnotes".
- **Exhibits**: every new fact gets at least one screenshot of the source document with the sentence boxed in red
  (`scripts/exhibit.py`). The exhibit title states the conclusion; the source line gives the page or section and says
  "red box added". Place it next to the sentence it proves; put the overflow in an appendix.
- **One fact per sentence**: two or three numbers at most per sentence; comparisons and detail go into a table or a note.

## 8. What not to copy

- **Short-seller advocacy**: the example report's author held a short position at publication and said it would cover. This
  skill takes no positions and advocates nothing; a rating is a research judgment, settled in public, misses included.
- **Accusatory tone and moral judgment** ("conscious and willful disregard", "callous"). That is advocacy, not research,
  and it conflicts with hard rules 4 and 12.
- **Anonymous interviews as evidence** (section 2).
- **Outcomes without an expectation**: the example report applies no probability weighting, so the reader gets no expected
  value. A settleable rating needs one.
- **Inconsistent conventions between scenarios** (section 1).

## 9. How this fits the rest of the method

- The full-coverage checklist in `quality-bar.md` section 1 still applies, but it is the standard for the **notes**, not the
  table of contents. One line per dimension goes into the full-coverage appendix (finding, whether it affects the claim,
  source); the body keeps only what serves the claim.
- Cause / process / outcome, falsifiability, evidence grades, settleable ratings, the ledger and settlement all stay. The
  evidence grade moves from the body into the footnote.
- The misreading section answers the market's misreadings; section 5 answers the company. Both sit in Part 3.
