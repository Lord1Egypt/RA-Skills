# Quality Bar

This file is the acceptance standard for a research desk. It turns "good research" into checks you can run. Each
item says how to check it; none is a slogan. **When a draft is complete, go through every item. A report that fails
any item is not released.**

The production line has seven gates. Finish each gate before starting the next. Do not run them in parallel to save
time, because later gates depend on the earlier ones being settled.

**1 Three-dimensional exploration -> 2 Data accounting -> 3 Writing -> 4 Chart design -> 5 Presentation and output
-> 6 Rating, outlook and decision chapter -> 7 Adversarial audit**

This file is organised by gate.

---

## Gate 1. Three-dimensional exploration

When you analyse a company, analyse every link of it, so that the company stands clear and whole in view. This is
a three-dimensional task, not a single line of enquiry. A dimension left out means the work is not deep research.

The subject is **the company as a whole plus its position in its industry**. You need both coordinates. For each
item below, decide whether the information is obtainable, and record the decision.

Since 1.1.0 this checklist is the standard for the **notes**, not the report's table of contents: one line per dimension
goes into the full-coverage appendix (finding, whether it affects the claim, source), and the body keeps what serves the
claim (`pipeline/03-writing.md`, "The report form"). Beyond the checklist, look for **new facts** in primary records
outside the SEC statements and in the company's own earlier words (`investigative.md` sections 2 and 3).

### A. Inside the company (the vertical cut)

| Dimension | Question that must be answered | Primary source |
|---|---|---|
| **Ownership look-through** | Top 20 holders, insider holdings, dual-class or special voting rights, passive versus active institutional share, pledges and lock-ups | DEF 14A, 13F / 13D / 13G, Forms 3/4/5 |
| **Board and management** | Background, tenure, pay structure (which metrics it is tied to), trade-by-trade breakdown of insider buying and selling over the last 12 months (separate transaction codes S/M/F/G) | DEF 14A, Form 4 raw XML |
| **Workforce and productivity** | Headcount series, mix of R&D / sales / production where available, revenue per employee and gross profit per employee series, layoffs and expansion moves | 10-K Item 1; label third-party profile data [C] |
| **Revenue composition** | Three cuts: segment x region x customer type. Intersegment sales (gross versus net basis). Concentration of the top N customers | 10-K / 10-Q segment notes, customer-concentration disclosure |
| **Capital structure and funding** | Whose money is being spent: operating cash flow, equity issuance, debt (rate, tenor, covenants) or leases. Net debt series. Dilution series | Cash flow statement, debt note, statement of equity |
| **Return on capital invested** | How much capital it takes to earn one dollar: ROIC series, **incremental ROIC** (change in NOPAT divided by change in invested capital), where capex goes by category | Computed by you; derivation goes in the derivations appendix |
| **Orders and delivery** | Backlog, book-to-bill, RPO (as defined by the standard), delivery lead-time series, implied profit in backlog (backlog x segment margin) | 8-K earnings release, 10-Q RPO note |
| **Operating efficiency over many periods** | Days of inventory, receivables and payables, and the cash conversion cycle, **quarter by quarter from the earliest available period to today**, not two points | Computed by you; pull the full series from XBRL companyfacts |

### B. Industry and the outside world (the horizontal cut)

| Dimension | Question that must be answered | Source |
|---|---|---|
| **Full supply-chain dependency** | Key upstream suppliers (any single point of failure?), purchasing concentration, exposure to raw-material and component prices; the industry and capex cycle of downstream customers | 10-K supplier disclosure, cross-reads of counterparties' filings |
| **Market share and occupancy** | What the share is, whose definition it is, which way it is trending; who is second and third | Institutional estimates [C] plus your own calculation from each company's revenue |
| **Industry-weighted growth** | Revenue growth of each peer; **revenue-weight** them into an industry growth rate and compare with the company. "Outgrew the industry by N points" is worth more than "grew X%" | Computed from each company's 10-K / 10-Q |
| **Competitor mirror** | At least 2 peers on one common basis (gross margin, operating margin, ROIC, growth, valuation); calendarise where fiscal years differ | Counterparties' primary filings |
| **Positioning and leverage** | Crowding and leverage in this name: short-interest series, open interest and skew in options, exposure to leveraged ETFs and structured products where relevant, passive index ownership. **Normal fundamentals with excessive leverage can still deleverage** (a crowded large-cap can fall sharply and recover in a V). Every name has a different leverage profile, so judge name by name | FINRA short data, option chain, ETF holdings |
| **Regulation and geopolitics** | Export controls, subsidies, litigation, investigations, with the quantified revenue exposure | Item 1A of the filing plus primary government documents |

### C. When the data are not disclosed

When a company **stops disclosing** or **never discloses** a key metric, "not disclosed" is not an acceptable
finding on its own. Do three things:

1. **Why.** What management said about it on the call and whether analysts pressed. Whether the CFO or auditor changed. Whether you checked SEC comment letters (EDGAR CORRESP / UPLOAD).
2. **Who questioned it.** Whether any sell-side report, financial press or shareholder letter challenged it, and how the stock reacted to the change in disclosure.
3. **A substitute basis.** Use a figure the standard forces out (RPO), counterparty disclosures, or a supply-chain back-calculation, and state the error range of the estimate.

Put the result of all three steps in the body, not in a footnote. A change in disclosure behaviour is itself a
signal and deserves its own section.

---

## Gate 2. Data accounting

The numbers you publish should be numbers you have organised and computed. A raw number from a source does not
tell you whether the company has made it look better than it is.

1. **No decorative metrics.** A closing price, a market capitalisation or a bare "total revenue" figure, anything that can be said in one sentence, does not get a headline-metric slot. The test is: **has this number been processed by us (compared, put in a series, decomposed or back-solved)? If not, it is decoration.**
2. **Every headline metric needs three things**: the current value, the change over several periods (a curve, or at least three time points), and a reference basis (industry-weighted, peer median or its own history).
3. **Window-dressing checklist** (go through every item; write any anomaly into the body):
   - Accruals diverging from cash: the gap series between net income and operating cash flow.
   - A sudden change in DSO or inventory days (channel stuffing, an early trace of weakening demand).
   - A change in expense-capitalisation policy (capitalisation rate of R&D, software, contract costs).
   - A change in depreciation life (servers moved from 4 to 6 years creates profit from nothing).
   - "Non-recurring" items that recur every year.
   - Segment reorganisation (redrawing segments so weak businesses sit inside strong ones).
   - Buybacks flattering EPS (net income flat, EPS up; split out the share-count contribution).
   - The non-GAAP bridge: list every GAAP-to-adjusted item, and the SBC-to-revenue series.
   - Related-party transactions and VIE or off-balance-sheet arrangements.
4. **Derivations go in the derivations appendix (Appendix D).** Every number you compute yourself (incremental ROIC, calendarised comparisons, implied profit in backlog, weighted industry growth) is shown there step by step: formula, then inputs (with sources), then intermediate values, then the result, then the sensitivity. If a number comes from a derivation, the report must show the professional reasoning at the end.
5. **Cross-checking is a procedure, not a slogan.** Key numbers need two independent sources. Recompute each self-computed number by a different route (for example, a calendarised annual value against the value the annual report states directly; the two must agree).

---

## Gate 3. Writing

Headlines and prose should read like professional research, not like a podcast or a methods lecture.

1. **Headline formula: conclusion plus number, as a declarative sentence.** A research headline states the conclusion directly. Examples below use placeholders for the numbers.
   - Good: "Backlog disclosure discontinued: ten straight quarters reported, none in the last two."
   - Good: "Regional organic growth of -X%, fully masked by the consolidated figure."
   - Bad: "And then they both disappeared." (suspense narrative, sounds like a podcast)
   - Bad: "What this finding can and cannot support." (meta-discussion, sounds like a methods lecture)
   - Bad: any headline phrased as a question, and any headline that starts "We found ...".
2. **Banned words and sentence patterns** (they apply to the body as well):
   - Meta-discussion: "it is worth noting", "interestingly", "it should be pointed out", "let us look at".
   - Empty turns: "however, things are not so simple".
   - Self-reference: "this report believes" strung together (at most once per chapter; state judgments as declarative sentences).
   - Addressing the reader: "you may ask", "the reader needs to understand".
   - Explainer tone: "simply put", "think of it as".
3. **Paragraph discipline.** The first sentence of each paragraph is that paragraph's conclusion (inverted pyramid). One paragraph says one thing. When a number appears, give its comparison in the same sentence (year on year, quarter on quarter, versus peers). A bare number is not a sentence.
4. **Procedure for checking every heading and banned pattern** (run it on the finished draft; send corrections back to the source parts and reassemble):
   - **Headings.** Extract every H1/H2/H3 plus every table title, box title, chart title and chart caption into one list and check each against the formula above. Fix failures on the spot. Adapt the pattern to your markup, for example: `grep -nE '^#{1,3} |^Table [0-9]|"(title|caption)":' report.md`
   - **Banned patterns.** Run a case-insensitive grep and require zero hits: `grep -nEi "it is worth noting|interestingly|it should be (pointed out|noted)|let us look|however, (things are|it is) not so simple|you may ask|the reader (needs|must)|simply put|think of it as" report.md`. Count "this report believes" chapter by chapter: at most one per chapter. Also remove filler, hype and templated phrasing that the grep does not catch.
   - The style audit route in Gate 7 starts from the output of these two steps and reviews false positives. It does not re-read the whole text by eye for banned words.
5. **Use desk vocabulary** ("basis", "exposure", "delivered", "settled", "implied"). Do not use explainer tone.
6. **Sources, sentences and codes** (since 1.1.0; details in `pipeline/03-writing.md`). Every key number and quotation is
   footnoted to a page, section or table with a URL; the grade sits at the end of the note, not in body paragraphs; two or
   three numbers per sentence at most; internal codes (judgment, cross-check, mispricing-evidence and model-section numbers)
   stay out of the text. `python3 scripts/check_report.py <report>.md` exits 0.

---

## Gate 4. Chart design

There are many chart types. Choose the one that best matches the data. Before you draw, answer: **what is this
data's job?**

Hard rules for every chart, whatever the tool: never use a dual axis; draw missing data as missing (a gap, never an
interpolated or zero value); check that the palette is distinguishable in greyscale and under common colour-vision
deficiency. Only draw a chart type your chart tool can render faithfully. Where it cannot, use the alternative in the
table instead of approximating.

| The data's job | Use | Never use |
|---|---|---|
| Evolution over many periods (8 or more) | Line chart, with the key turning points labelled with values | A row of columns (crowded) |
| Joint evolution of two quantities with different units | Stacked panels with a shared time axis | A dual axis (always forbidden) |
| Composition and change in composition | Stacked columns with share labels (put shares in the caption or an accompanying table if the tool labels only totals); stacked columns also work for many periods | A pie chart (forbidden above 3 items) |
| Step-by-step decomposition (growth into contributions) | Waterfall, every step labelled, rounding residual shown openly as its own step | A text list |
| Multi-dimension comparison with peers | A table (exact numbers) or a sorted horizontal bar. For a two-period comparison, use paired bars (x = company, one series per period) or two rows per company | A radar chart (always forbidden) |
| Distribution, range or scenarios | A **price ladder** (below), or a range bar with a current-price anchor | Three circles joined by arrows |
| Transmission mechanism | A flow diagram, with an observation point on every layer and an observability state (ok / broken / blind) | A plain text chain |
| One striking number | The number plus one comparison line, as a single tile or as bold text in the body with the comparison in the same sentence | A chart drawn for one number |
| One-page overview | A dashboard (below) | A static table of numbers; dark blocks |
| Showing what the company said, did or wrote | A screenshot of the original with a red box; title states the conclusion; source gives the page or section and says the box was added (`scripts/exhibit.py`) | Paraphrase; our own chart dressed up as an original |

**Three-scenario price ladder** (use it in place of a loose three-scenario sketch). Specification:
- A vertical price axis, ordered bottom to top: downside price, then current price (a heavy anchor line), then base price, then upside price.
- Beside each price level, three items: the probability (with its basis), the key assumption it implies (for example, next-year revenue and multiple), and the percentage distance to the current price.
- On top, a layer of **market-implied comparison**: where the growth rate or multiple backed out of the current price falls, between which two scenarios. The ladder must let the reader see which scenario the market is currently pricing, not only that you have three numbers.
- Optional overlay: the one-year plus-or-minus 1 sigma range implied by options, set against your scenario range. The mismatch between the two ranges is the view.

**One-page overview = a dashboard.**
- 8-10 **processed** metrics, each with a mini series chart (a small multi-year quarterly curve), the current value and the direction of change.
- Examples: the cash conversion cycle curve from the first available quarter to today, the incremental ROIC series, the series of the company-versus-industry-weighted growth gap, FCF margin and capex intensity in two panels, backlog and implied profit series.
- Use a light, print-style layout, not dark web-style blocks (see Gate 5).

---

## Gate 5. Presentation and output

1. **One light, print-style layout throughout.** Dark text on a light ground; colour only in charts and small areas of emphasis. **No large dark blocks.** Title-page KPI tiles, the rating box and the conclusion box use a light outline or a light grey fill, not a dark fill with reversed text.
2. **The data basis date is always visible.** Wherever a reader can open the report in parts or on a single page, the report name and the data basis date appear with it (for example in a running header). Do not repeat the disclaimer on every page: point to it once at the front and once in the appendix.
3. **No repeated components.** The same information (rating, scorecard, KPI) appears once in the whole report, in a fixed place. The rating appears on the title page and in the conclusion chapter (the conclusion chapter is the expanded version, not a copy). The overview dashboard comes once, right after the title page. After drafting, grep for key phrases and count their occurrences.
4. **Compact financial layout.** Tight table rows, right-aligned tabular numerals, no blank page between chapters, uniform space before paragraphs. The target is the density of a printed terminal page, not a magazine.
5. **Bilingual versions match cell for cell.** If the report ships in two languages, numbers, table numbers, figure numbers and evidence grades are identical.
6. **Check the output after rendering.** Open the rendered file, not the source. Look for text overflow, clipped tables, missing figures and a page or section that falls apart.

---

## Gate 6. Rating, outlook and decision chapter

### Rating and the three-horizon outlook

A rating is not one word. It is **an outlook at three horizons, plus the evidence and the settlement conditions**.
Each horizon gets its own entry in the ledger (`tier` = monthly / quarterly / annual). The monthly and quarterly
outlooks are shown on the scorecard in full, like the annual one, and when they fall due `scripts/desk.py run`
flags them (see `references/desk.md`).

| Horizon | Content | Source of the evidence |
|---|---|---|
| **Monthly outlook** (1-3 months) | Event-calendar driven: earnings date, product launches, macro releases, the option-expiry structure. Direction plus the trigger conditions | The catalyst path table |
| **Quarterly outlook** (3-6 months) | The pace at which fundamentals are delivered: which tracked indicator prints this quarter and what print counts as a hit | The tracked-indicator table |
| **Annual outlook** (12 months) | Three scenarios, probability-weighted, plus a rating relative to a benchmark (the settleable basis is unchanged) | The valuation chapter |

**Valuation discipline.**
- A target price needs at least **two independent paths** (reverse DCF or DCF, plus a comparable multiple or exit multiple). When the two paths differ by more than 20%, explain where the difference comes from.
- State the basis of each probability: historical frequency, market-implied, or explicitly subjective.
- **The source of funds and the target-date assets must be one set of accounts** (the same rule as section 5 of `references/judgment.md`). The funding source for capital commitments (cash on hand, committed draws, new debt and equity), and the net debt and share count at the target date, must all come from one period-by-period (quarterly or monthly) cash ledger running from the balance-sheet date to the target date. One cash balance cannot be both a source of funds and an asset in hand at the target date. Committed but undrawn facilities enter target-date debt according to the scenario. The price back-solve (E1) and the three scenarios use the same net-debt formula. A violation of this rule can flip a rating (for example from neutral to reduce), so it is a blocking finding.
- All of it goes in the derivations appendix, with the cash ledger listed period by period.

### The decision chapter

The decision chapter is written as **operating research**. Its reader manages money professionally. It is not
written for retail investors. It reorganises these items:

1. **Scenario-to-action mapping table.** For each scenario: what is observed (with thresholds), what it means, and the research action that follows. Write actions in research language ("under this scenario the rating in this report would be raised/lowered to X"). Do not write buy or sell orders.
2. **Entry and invalidation conditions.** At what price or event combination the thesis is worth expressing, and what breach (a price or fundamental threshold) voids the thesis. Both must be observable.
3. **Ways to express the view** (research description, not a recommendation): holding the stock directly, a pair trade against a peer (the logic and risk of long X / short Y), or an option structure (where the convexity comes from and what it costs). State what strength of conviction each suits.
4. **Position-sizing and risk-budget framework.** Tiers of exposure by strength of conviction (evidence grade x catalyst density): core, tactical, watch. State plainly that this is a framework, not an allocation recommendation.
5. **Review rhythm.** Which dates the analyst must come back (earnings dates, catalyst dates) and what is settled at each review.

In the 1.1.0 report form these five items sit in tables in Part 4, "Tracking and settlement"; they are not a chapter of
their own (`pipeline/03-writing.md`).

Compliance is unchanged. Everything is research content, aimed at no particular investor, with no buy or sell
wording. See `assets/disclaimer.md`.

---

## Gate 7. Adversarial audit

The audit is Step 4 of the flow (`references/pipeline/04-audit.md`): **two rounds, four to five routes per round,
including a skeptic and a bilingual-consistency check**. Each route's goal is to find errors, not to confirm
that the draft passes.

There are seven audit **scopes**. A scope is not a count of agents.

| Scope | Where it runs |
|---|---|
| Financials and valuation | Round 1, merged into the first three routes |
| Ownership and governance | Round 1, merged into the first three routes |
| Contracts and business | Round 1, merged into the first three routes |
| Industry chain and competition | Round 1, merged into the first three routes |
| Summary and risks | Round 1, merged into the first three routes |
| Tradability | Round 1, merged into the first three routes |
| **Presentation and prose** | Round 1, its own route |

Round 2 has five routes: skeptic (the bear case), tradability, financials, bilingual consistency, and a style
re-check. It audits only v2 and the passages that were revised.

**The presentation and prose route** simulates a demanding editor:
- Check every heading against the Gate 3 formula. First run the heading-extraction grep and the banned-pattern grep from Gate 3 step 4, then review by hand.
- Check every chart against the Gate 4 type-matching table.
- Look through every section for white space, heavy blocks and repeated components, and check the basis-date placement under Gate 5.
- For every headline metric ask: has this number been processed? Does it have a series? Does it have a comparison?
- Output a list of challenges in the same format as every other route (`audit-vN-style.md`), and dispose of each item.

Every route writes `audit-vN-<route>.md`. Each item gives location, original text, the problem, the evidence, the
severity and the fix. The editor resolves every item, and revisions are recorded in the revision log in Appendix C
(original wording, revised wording, nature of the change).

---

## Release checklist

Run this last, before release. All items apply in full to a single-stock report. In an industry-chain or macro
report, items that hold only for a single company apply on the matching basis: replace the A/B coverage lists in
Gate 1 with the "must answer" availability decisions in each step of `references/industry.md` or
`references/macro.md`; run the window-dressing checklist and the target-date cash ledger only for the core
companies the report looks into. Record in the self-check what you substituted.

- [ ] The title is the claim, with a per-share impact; thesis paragraph and subtitle within their limits; a reader can restate the claim after the summary (`check_report.py`).
- [ ] At least three new facts, each with a section in Part 1, an exhibit, and a landing point on the value bridge (`investigative.md` sections 1 and 2).
- [ ] Part 3 takes management's public statements apart one by one; Appendix A holds the company's statements over time.
- [ ] `check_report.py` exits 0 for every edition (length, footnotes, exhibits, sentence density, internal codes); the verifiability lane opened 30 footnotes and found every one at its stated location.
- [ ] Gate 1, every dimension in A and B: answered, or judged unobtainable and written into Known limitations; findings collected in the full-coverage appendix.
- [ ] Every undisclosed metric has been through the three steps (why / who questioned it / substitute basis).
- [ ] Zero decorative metrics: each headline metric has processing, a series and a comparison.
- [ ] The derivations appendix holds the derivation of every self-computed number, including the period-by-period target-date cash ledger (source of funds and target-date assets on one set of accounts).
- [ ] The window-dressing checklist has been completed item by item.
- [ ] Every heading, caption and table note has been checked against the headline formula; the banned-pattern grep returns zero hits (Gate 3, step 4).
- [ ] Every chart has been compared with the type-matching table. The three scenarios use a price ladder (for an industry chain or macro report with no single price vehicle, use a range bar with a current-price anchor). The overview is a dashboard.
- [ ] Light layout; the data basis date is visible; no per-page disclaimer; no repeated components.
- [ ] The three-horizon outlook is complete (monthly, quarterly, annual). The decision chapter is in operating-research format.
- [ ] The bull/bear debate was run before the rating was set (`debate-bull.md` and `debate-bear.md` are in the report folder). Where the rating is not neutral, the bear side's first three points are answered one by one in the body.
- [ ] After release, the ledger is complete: the core calls, the annual rating, and the monthly and quarterly outlooks (`scripts/ledger.py add ... --tier`). `research/watch.json` includes the series, and `python3 scripts/desk.py check` returns 0.
- [ ] Both audit rounds are done (round 1: five routes including presentation and prose, and verifiability; round 2: includes the skeptic and bilingual consistency; all seven scopes had a reviewer), and the revisions are in the Appendix C revision log (original wording, revised wording, nature of the change).
