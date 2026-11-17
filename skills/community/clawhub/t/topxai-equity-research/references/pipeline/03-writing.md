# 3. Writing (ordered by the argument, not by topic)

> This is steps 3 and 3.5 of the pipeline in `SKILL.md`. Previous step: `02-research.md`. Next step: `04-audit.md`.
> Since 1.1.0 reports use the form below. Where it comes from and the method behind it: `references/investigative.md`.

**Source-file convention.** `research/<report-id>/parts/pNN-<chapter>.md` (primary language) and `parts/<lang>-pNN.md`
(second-language edition, if any) are the **only sources**. The assembled files (`<lang>.md`) are generated and **must never
be edited by hand**. To change a number, change the part and re-assemble. Front matter is written only at the start of
`p01`. Assemble with a small script of your own: concatenate the parts in filename order with a blank line between parts
(otherwise a heading directly after a table gets absorbed into the table), and resolve label placeholders such as
`[[t:label]]` and `[[f:label]]` into table and figure numbers, so inserting a table does not mean renumbering by hand.
Exhibit images live in `research/<report-id>/exhibits/` and are referenced by relative path.

## The report form

After the title page and the summary, a reader should be able to say in one sentence what we claim, what it is worth per
share, and which facts carry it. Every section of the body argues for that sentence. A company deep dive:

| Part | What it holds | Notes |
|---|---|---|
| Title page | Title = the claim, with the per-share impact; a one-line subtitle; a thesis paragraph (claim, per-share impact, the two strongest new facts); rating box; the three basis dates | Thesis at most 90 words; subtitle at most two numbers |
| Summary | A short report in its own right, 3-6 pages: the claim, then one short section per new fact (heading = conclusion, one exhibit each), then how the money works (value bridge and the per-share outcomes), what the company says, and the rating with the three-horizon outlook table and transition box (once in the whole report, here) | A reader who stops after the summary still has the conclusion |
| Part 1 Evidence | Sections whose headings are claims, in the order of the argument. Each: the conclusion sentence, the original text and exhibit, the reasoning, and which input of the value bridge the fact changes, by how much | New facts are developed here; old versus new statements, statement timelines, budget against promise (`investigative.md` section 3) |
| Part 2 Valuation | Value bridge, then up to three outcomes per share (one sentence of trigger each), probability weighting and its basis, market-implied pricing, rating and settlement terms | Two valuation paths and the price ladder still apply; detailed sensitivities go to Appendix D; one timing convention for all scenarios |
| Part 3 The company's account and the opposing case | Management's statements on the points in dispute, taken apart one by one; the opposing side's first three arguments from the debate answered one by one; misreadings; risks ordered by observability | `investigative.md` section 5; each answer lands on a number |
| Part 4 Tracking and settlement | Falsifiable conditions, catalyst calendar, ledger entries; the five decision items of `quality-bar.md` in tables here | What to track over different holding periods |
| Appendix A | The company's statements over time (by year, original text and source) | |
| Appendix B | Exhibits that did not fit in the body | |
| Appendix C | Full-coverage table: one row per dimension of `quality-bar.md` section 1 (finding, whether it affects the claim, source) | The breadth of the research lives here, not spread across the body |
| Appendix D | Derivations and calculations (formula, inputs, intermediate values, result, sensitivity; the target-date cash ledger) | |
| Appendices E-G | Glossary and definitions / sources and known limitations (with the standing entries) / disclosures (from `assets/disclaimer.md`, verbatim), audit revision log and version | |

The 1.0 structure ordered sixteen chapters by topic (financial quality, capital structure, governance, peers, market ...).
Most of each topic chapter had nothing to do with the claim, and readers could not find the point. Research every dimension
as before; put the findings in Appendix C, and write the parts that bear on the claim into the matching section of Part 1.
**Industry and macro reports** use the same skeleton (claim, evidence, valuation or scenarios, opposing case, tracking);
the inner structure of each link of the chain is in `references/industry.md` Step 8 and `references/macro.md`.

## Length and density (gates in `scripts/check_report.py`)

- Body without appendices: at most 15,000 English words (30,000 characters for a Chinese edition).
- **One fact per sentence**: two or three numbers per sentence at most; comparisons and detail go into a table or a note.
  Sentences with more than four numbers: at most 5% of all sentences.
- No [A]-[D] tags in body paragraphs; the grade sits at the end of the footnote (a grade column in a table is fine).
  Compound grades such as `[A/C]` are dropped; explain "filed value split by this report" in the note instead.
- No internal codes in the text: judgment numbers (J1 ...), cross-check and gap numbers (X1 ... / G1 ...), mispricing
  evidence codes (E1-E5), model output section numbers, note and model file names. Write what a reader understands
  ("price-implied" rather than "E1"; "see Appendix D, section 3" rather than "§3").

## Sources and footnotes

Every key number and every quotation carries a footnote. Use standard Markdown footnotes: `[^label]` in the text and
`[^label]: source ...` at the end of the chapter. Use short meaningful labels (`10q-cf`, `ppa-l3`), unique within the
chapter. A footnote states five things and ends with the evidence grade:

```
[^10q-cf]: Riot Platforms, Form 10-Q (quarter ended 2026-06-30), Consolidated Statements of Cash Flows, "Proceeds from
    sale of bitcoin", filed 2026-08-10,
    <https://www.sec.gov/Archives/edgar/data/1167419/000110465926093448/riot-20260630x10q.htm> (hereinafter "Q2 2026 10-Q"). [A]
[^ppa-l3]: Q2 2026 10-Q, Note <N> "<note title>", the Level 3 fair value paragraph (use the note number and title in the original). [A]
[^mining-cash]: This report's calculation: mining segment gross profit plus curtailment credits, four quarters summed; formula and inputs in Appendix D, section 2. [C]
[^cf-repeat]: Same as note 3.
```

- Publisher, "document name" (type and period), **location** (page, section, table, note number, Item or slide), date, URL.
- First citation in full with "hereinafter"; later citations use the short name and a location without repeating the URL;
  "same as note N" for an immediate repeat.
- Own calculations say "this report's calculation / estimate", give the formula briefly and point to Appendix D; grade [C].
- An HTML filing has no page numbers: cite the Item, section heading, table or note number. The "PDF page N" that
  `scripts/exhibit.py` prints is the page of a print copy, not of the original.
- Quotations keep the original language; a translated edition puts the original in quotation marks followed by the translation.
- Indent continuation lines four spaces (the Markdown footnote rule), or they fall into the body text.

## Exhibits from primary documents

Every new fact gets at least one screenshot of the company's (or a regulator's or court's) own document with the sentence
boxed in red. A company deep dive carries at least six.

```
**Exhibit 1: Bitcoin sale proceeds sit in investing activities: $732 million in the first half of 2026**

![Riot Q2 2026 10-Q, consolidated statements of cash flows](exhibits/riot-proceeds.png)

Source: Riot Platforms, Form 10-Q (quarter ended 2026-06-30), Consolidated Statements of Cash Flows, filed 2026-08-10.
Red box added by the authors.
```

- Make the image with `python3 scripts/exhibit.py <URL or file> --find "original text" --out research/<report-id>/exhibits/x.png`
  (add `--row` to box a whole table row; HTML filings are printed to PDF through a local Chrome first; sec.gov needs
  `SEC_USER_AGENT`; the script needs `pip install pymupdf`).
- The exhibit title states the conclusion, like a chart title; never "Exhibit 1: cash flow statement".
- The source line gives the page or section and says the red box was added by the authors.
- Place it next to the sentence it proves; put overflow in Appendix B and write "see Exhibit N" in the text.
- Screenshots are only of original documents. Numbers we calculate are drawn as charts (`quality-bar.md` section 4), never
  dressed up as an original.

## Valuation numbers have exactly one source

`research/<report-id>/calc/model.py`. All inputs sit at the top, each marked [A] for a filed value or [C] for an assumption.
Run `python3 calc/model.py > calc/model-vN-output.txt`. Valuation numbers in the body and in Appendix D come **only from
that output file**. Never calculate them by hand. All scenarios discount through one timing function in the model
("year three" means the same number of periods everywhere; `investigative.md` section 1).

**Required components**: the eight items in `framework.md` section 5 are mandatory. Where they sit in this form: mechanism
diagram (Part 2, value bridge) / evidence grading (end of each footnote) / certainty layering (summary core-judgment table) /
bull-bear comparison (Part 3) / falsifiability and observation calendar (Part 4) / known limitations (Appendix F) /
misreading section (Part 3) / audit revision log (Appendix G).

## Gate

```bash
python3 scripts/check_report.py research/<report-id>/<lang>.md     # form gate, exit code 0
```

What the gate cannot count, the first-round appearance lane and verifiability lane check by hand (`04-audit.md`).

## 3.5 The tradable-judgment pass (before the draft is final)

Finishing the analysis is not the same as finishing the report. Go through `references/judgment.md` section by section:
consensus reconstruction (with its degrade path) -> mispricing evidence (five kinds) -> **catalyst path table** -> rating
basis (12 months, benchmark and start date) -> the four decision items (three-scenario prices, risk/reward ratio,
**invalidation price**, time to realisation) -> evidence-strength binding -> the bear's three arguments answered one by one
(step 2.5). The results go into the summary, Part 2 and Part 4 of the form above; the procedure's codes (E1-E5 and so on)
stay in the notes and the audit.

**This pass is what separates the report from commentary.** Without it, the report ends up with every number right,
every definition clear, and a reader who does not know what to do.

## Writing style

Write plainly. The audience is a professional reader scanning for the decision. Remove filler, hype and templated phrasing.
Make each heading a declarative conclusion that carries a number, and put the conclusion in the first sentence of each
paragraph. Write inference as inference ("we infer"), state primary facts directly, draw no legal conclusions and make no
moral judgments (`investigative.md` section 6). The three failure modes that appear most in research text:

- **Triplets**: three short sentences or items that share the same opening words. Cut to the one that carries the number.
- **Abstract nominal stacking**: "the implementation of the optimisation of ...". Use a verb and an object.
- **Closing flourishes**: a last sentence that lifts the paragraph to "the industry" or "the era". End when the claim ends.

The appearance-and-copy lane of the first-round audit checks the same list (`quality-bar.md` section 3, item 4).

## When several agents write chapters

Create `research/<report-id>/WRITING-CONTRACT.md` first (template: `assets/templates/writing-contract.md`). Its core rules:
numbers come only from `data-*.json` and `notes-*.md`; superseded values may appear only as a correction; an unresolved
conflict is written as `⟦OPEN: conflict N⟧` and no writer picks a version; no one smooths over an upstream contradiction;
no pipeline traces in the text; no buy or sell wording.

Run `scripts/check_report.py` on each chapter as well as on the assembled draft (footnotes, sentence density and internal
codes can be checked chapter by chapter). A gate that raises false alarms gets ignored; tune it to zero false alarms before
you let it block anyone.

## Pitfalls (collected from past work)

- **Numbers come only from the derivation file.** A second-round audit found an operating-basis figure off by nearly an
  order of magnitude: the number in a memo was wrong, and copying from the memo around the derivation file is a violation.
  The same round caught "contributes two thirds", which was really a weight; by contribution the share was far higher.
- **For every judgment sentence, ask whose debt this number subtracts.** A claim that the contracted portion "leaves no
  equity" had charged the construction cost of a later phase to the contracted portion's net debt. The attribution was
  wrong, and the opposing-side review caught it. The same accounting rule for cash is in `judgment.md` section 5.
- **Topic chapters bury the claim.** A 1.0-form deep dive ran past 60,000 words in the body, with two dozen numbers in its
  thesis paragraph and nearly half of its sentences carrying over four numbers; readers could not restate the
  conclusion. Ordered by the argument, the topic findings moved to Appendix C.
