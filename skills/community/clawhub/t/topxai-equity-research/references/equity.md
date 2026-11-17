# Equity Deep-Dive Research Flow

> Read `references/framework.md` first. This file covers **order and actions** only. The way of thinking lives in the framework.
> Applies to report type `equity`. The report series identifier is the ticker (for example `PLTR`).

**Why equity needs two passes.** A stock is the end of the chain. A company's profit is whatever is left after L1-L3 have
passed value down the chain. So run **two passes**. First go top-down and place the company in the chain: what entitles it
to this share of the profit. Then go bottom-up and test its own ability to deliver: can it actually collect that share.
Doing only the second step produces a restatement of the earnings release, not research.

Notation used below: **[Cause]**, **[Process]**, **[Outcome]** are the cause / process / outcome classes from the framework.
**[Fixed]**, **[Probabilistic]**, **[Unknown]** are the certainty tiers. Evidence grades are [A]-[D]. E1-E5 are the
mispricing evidence types in `references/judgment.md` section 2.

---

## Step 0 · Scoping and coordinates

**Must answer**
- Why this company, and why now? Is valuation at an extreme, has governance changed, or is its position in the chain moving?
- Its coordinates on L0-L4: the stage of the economy it sits in, its industry's position on the S-curve, its link in the chain,
  and its current valuation percentile.
- **A one-sentence hypothesis**: where do you expect the market to be wrong? If you cannot write it, do not start. Keep reading first.

**Output**: a one-page scoping memo with the hypothesis, the three most important questions to verify, and an assessment of data availability.

Warning: later evidence will overturn the hypothesis. That is normal and healthy. **When it does, change the hypothesis, never the evidence.**
Keep the trail "initial hypothesis → evidence → revised conclusion" in the final report. The trail itself is a source of credibility.

---

## Step 1 · Business model decomposition

**Must answer**
1. What does it actually sell? The common error is to mistake the delivery form for the business model: is it selling a software
   licence, or a continuing operating result?
2. Who buys it? Which **budget line** does the customer pay from (capital expenditure, operating expense, a dedicated project
   budget)? That decides how cyclical the demand is.
3. How does it get paid: one-time, subscription, revenue share, or a mix? How far apart are the **pace of revenue recognition**
   and the pace of cash coming in?
4. Unit economics: for one customer, one order or one machine, what is revenue minus direct cost minus acquisition cost?
   How long is the payback period?
5. Where do economies of scale come from (marginal cost, network effects, a data flywheel, channel reuse), and
   **have they already shown up in gross margin**?

**Output**: a one-page business-model diagram, a unit-economics table, and the chain "whose budget ultimately pays for this business".

Warning: the business model a company describes often disagrees with its actual revenue mix. **Trust the segment disclosure, not
the management narrative.** If the segment definitions have changed, restate the history on one basis before comparing.

---

## Step 2 · Ownership, governance and control

**Must answer**
- Ownership structure and the degree of **voting-power** separation (dual or multiple share classes, voting trusts, concert
  parties). Work out how much voting power the controller holds for how much economic interest.
- The **conditions under which control persists**: sunset clauses on dual-class stock, conversion triggers, ownership
  thresholds. Under what conditions would control loosen?
- Board composition and independence. Key-person risk (how dependent is the company on its founder).
- **Insider trading** over the last 12 months. Separate scheduled sales (Rule 10b5-1 plans) from discretionary trades. The
  second kind carries far more information.
- Related-party transactions and any channel for value to leak to insiders.
- Management incentives: what are the performance metrics? Pay tied to revenue growth versus pay tied to free cash flow
  produces entirely different companies.

**Data sources**: DEF 14A (proxy statement: governance and compensation), Form 4 (insider transactions), 13F / 13D / 13G
(institutional holdings and activist stakes), and the related-party and risk-factor sections of the 10-K.

**Output**: an ownership look-through diagram, a voting-power calculation table, and an insider-trading timeline.

Warning: the "beneficial ownership" table in a proxy statement includes options and convertible securities. Its basis differs from
shares outstanding, so **the figures cannot be added together directly**. Any inferred holding must be labelled as inferred and
checked against Form 4 first.

---

## Step 3 · Position in the industry chain and bargaining power

**Must answer** (the method is detailed in `references/industry.md`; here take only the slice that concerns this company)
- Which segment of the chain is it in? How concentrated is upstream supply, and how concentrated is downstream demand?
- **Which way bargaining power flows.** Read three things together: gross margin, receivable and payable terms, and customer
  prepayments. Together they show who is funding whom. (High gross margin, but upstream demands prepayment and downstream
  stretches payment terms: bargaining power is actually leaking away.)
- Dependence on a single supplier or a single customer, and whether an **irreplaceable chokepoint** is held by someone else.
- Its position on the cost curve relative to peers. The cost leader is the one that survives a downcycle.

**Output**: a chain-slice diagram for this company and a trend table of the three bargaining-power indicators (at least eight quarters).

---

## Step 4 · Financial quality and accounting basis: a strict three-way split

This is the step most likely to go wrong. **Read the financials by cause / process / outcome, not in statement order.**

| Class | Typical line items | How to read them |
|---|---|---|
| **[Cause]** | Backlog, contract liabilities, remaining performance obligations (RPO), price-locked long-term contracts, construction in progress, capital commitments | The **already locked** part of future revenue. The hardest forward-looking information there is |
| **[Process]** | Change in deferred revenue, inventory mix (raw materials / work in progress / finished goods), receivables ageing, divergence of operating cash flow from net income, capacity utilisation, unit cost | How the mechanism is running now. It leads the income statement |
| **[Outcome]** | Revenue, gross profit, net income, EPS, ROE | Already priced. Use only for calibration |

**Must answer**
1. Revenue quality: did growth come from volume, price, acquisitions or a change in definition? **Separate all four.**
2. Earnings quality: the long-run ratio of operating cash flow to net income. Where did the difference go (receivables,
   inventory, capitalisation)?
3. **Accounting traps**: changes in revenue-recognition policy; capitalising versus expensing (R&D, customer acquisition,
   interest); one-off gains and losses; stock-based compensation (is the GAAP to non-GAAP gap being systematically ignored?);
   mismatched fiscal years (align them for cross-company comparison); currency effects (constant currency versus nominal).
4. Balance sheet: the debt maturity schedule ([Fixed]), off-balance-sheet commitments, leases, and goodwill and impairment risk.
5. Share count: the dilution path (options, RSUs, convertibles). Re-check every per-share metric on a **fully diluted** basis.

**Output**: a cause / process / outcome financial table, a cash-flow versus net-income divergence analysis, a fully diluted
share-count table, and a list of accounting-basis notes.

Hard rule: whenever you cite a non-GAAP metric, give the GAAP figure and the composition of the difference next to it.
Giving only the non-GAAP number is sell-side promotion, not research.

---

## Step 5 · Competitive position and moat: ask in a falsifiable way

Do not write "the moat is deep". That cannot be tested. Ask:

1. What is the **specific mechanism** of the moat: switching cost, network effect, cost advantage, intangible asset, or efficient scale?
2. **Is it widening or narrowing?** Which indicator shows it? Examples:
   switching cost → net dollar retention (NDR) and customer churn;
   cost advantage → the trend in the unit-cost gap against peers;
   network effect → whether the marginal cost of acquiring each new user is falling.
3. From which angle are competitors **most likely to break through**? Have they started (hiring, patents, capacity, pricing)?
4. Substitutes: look beyond like-for-like competitors to **substitution of the customer's budget**. The customer may spend this money elsewhere.

**Output**: a moat-mechanism table (mechanism → observable indicator → trend over the last 8 quarters → verdict: widening / stable / narrowing),
plus a tracker of competitor moves.

---

## Step 6 · Reverse-engineering the market price (L4)

**Must answer**
1. The current valuation percentile, against the company's own history and against peers.
2. **Reverse calculation: what does today's price imply?**
   Turn the market capitalisation back into the revenue, free cash flow, market share or margin implied N years out.
   Then ask: **what would the world have to look like for this assumption to hold?**
   This step is often the most forceful passage in the whole report.
3. What is the sell-side consensus? How far is your number from it, and on which assumption?
4. Positioning and crowding: change in institutional holdings (13F), passive share, short interest, option open-interest distribution.
5. Who is the marginal price-setter (framework question 3), and what constrains them?

**Output**: a valuation-percentile table, an implied-expectations table, an attribution of the difference from consensus, and the positioning structure.

---

## Step 7 · Scenarios and valuation

- **Three scenarios** (bull / base / bear). For each, write the **conditions that trigger it**, not only a number.
- A probability-weighted target price. Also give a second number on a **fully diluted** basis. With different share-count
  assumptions the conclusion can flip.
- A sensitivity table on key assumptions: which assumption, moved by 10%, flips the conclusion? That is this report's
  **linchpin variable**. It must rank first among the tracking indicators.
- **At least two independent paths to the target price** (valuation discipline in `references/quality-bar.md`). Choose the primary
  path by the stage of the business: for high-growth, unprofitable companies use a revenue multiple plus the reverse calculation;
  for mature cash cows use DCF or EV/EBITDA; for cyclicals use through-the-cycle normalised earnings. Use a second path as a
  cross-check (reverse DCF, layered DCF, comparable multiples or exit multiples). If the two differ by more than 20%, attribute
  the difference. **Put the reason for the method choice and both derivations in Appendix D.**

**Output**: a three-scenario table, a probability-weighted target price (two share-count bases, two paths), a sensitivity table, and the linchpin variable.

Warning: **for rating conventions see `references/judgment.md` section 4.** An annual-horizon rating must state "next 12 months ·
relative to <benchmark> (with the reason for choosing it) · start date". Without that it cannot be falsified, because it can
always be answered with "not yet". Combine the monthly, quarterly and annual outlooks into one table plus a transition-conditions
box, as set out in "Rating and outlook" in `references/quality-bar.md`. This appears once, in chapter 1. Before fixing the
rating, run the bull/bear debate in step 2.5 (`references/pipeline/02-research.md`). When the rating is not neutral, respond in
the body, one by one, to the first three points of the opposing case (`debate-bear.md` or `debate-bull.md`). Register one
ledger entry per horizon (`--tier`); see `references/pipeline/05-publish.md`.

Warning: **the output of this step is not a single target price. It is the four required items of the decision chapter**
(`references/judgment.md` section 5): the three scenario prices, the risk/reward ratio, the **thesis-invalidation price level**,
and the expected time to realisation. These go into chapter 13, the decision chapter, as the five items of operational research
(see "Decision chapter" in `references/quality-bar.md`). Also disclose the effect of WACC ±1%, the terminal-value share, the
basis for each scenario probability, and that the funding source and the end-date assets come from one consistent set of accounts.
Probabilities must not be guessed (red line 7 in `references/framework.md` section 6). The weighted result must be
**reconciled line by line** with the market-implied expectations from Step 6.

---

## Step 8 · Tracking indicators and falsifiability

**Produce four tables. This is the part readers return to most often.**

**Table A · Key tracking indicators**

| Indicator | Nature | Importance | Current value | Bullish threshold | Bearish threshold | Disclosure date | Data source |
|---|---|:--:|---|---|---|---|---|

Rows come from the [Cause] and [Process] items of Step 4, the moat indicators of Step 5, and the linchpin variable of Step 7.
Grade **importance** with ★ / ★★ / ★★★. Allow **at most five ★★★ rows** (this forces ranking), and the linchpin variable must be one of them.

**Table B · Falsification conditions**

| Core conclusion | What, if it happens, falsifies the conclusion | When it can be observed |
|---|---|---|

**Table C · Catalyst path** (`references/judgment.md` section 3; this is a different thing from Table B):

| Catalyst event | Expected timing (quarter) | Why it forces the marginal price-setter to change behaviour | How long past due before it is void |
|---|---|---|---|

If no catalyst can be found within 12 months, the summary page must say so plainly: "structural view, needs N years to play out,
not suited to capital with an evaluation period."

**Table D · What to track for different holding periods** (which three indicators long-term, swing and event-driven holders should each watch).
Compliance: Table D says only **what to watch**, never what to do. Exposure and entry / invalidation conditions are written only in
chapter 13, the decision chapter, following items 2 and 4 of "Decision chapter" in `references/quality-bar.md`. What you give is a
**research framework for exposure tiers (core / tactical / watch)**. It is not aimed at any particular investor and contains no
specific position sizes or trade timing. Use the wording "under this scenario, this report's rating would…" and state explicitly
that it is a framework and not an allocation recommendation.

**Three lines on the first summary page**: the linchpin variable / the nearest catalyst / the thesis-invalidation price level.

---

## Step 9 · Write-up, audit, publish

Chapter plan (16 body chapters and 4 appendices; see `references/pipeline/03-writing.md` for how to write them):
> ① Executive summary and three-horizon outlook (overview dashboard + core judgment + three-horizon outlook table + transition-conditions box)
> → ② Business model and transmission chain
> → ③-⑥ Four company-specific look-through chapters (set by the company's value-realisation chain, for example a contract
> ledger / counterparties and credit support / unit economics of the core asset / the [Cause] layer such as power, site or capacity)
> → ⑦ Financial quality (including a window-dressing checklist) → ⑧ Capital structure and dilution
> → ⑨ Governance and insiders → ⑩ Peer mirror → ⑪ Reverse-engineering the market price → ⑫ Valuation (two paths + three scenarios + price ladder)
> → ⑬ Decision chapter (five items of operational research) → ⑭ Risks (ordered by observability) → ⑮ Misreading-prevention section
> → ⑯ Tracking indicators, falsification conditions and catalyst path
> Appendices: A Terms and definitions / B Source list and known limitations / C Disclaimer and disclosures (the template in
> `assets/disclaimer.md`, verbatim, including the audit revision log) / D Derivations and calculations (every number you computed yourself)

Warning: the relationship networks (capital, cross-appointments, revolving doors between business and government) in
chapters ③-⑥ and ⑨ have no separate step in the nine above, but they are among the most distinctive content of the report.
Fold them into the research. Do the relationship network together with Step 2 (ownership and governance). Do chapters ③-⑥
together with Step 1 (business model) and Step 3 (chain position), breaking them down by contract form, counterparty and asset
to primary filings that can be checked.

After the draft is written, run the **seven-scope adversarial audit** (scope list in `references/pipeline/04-audit.md`). The
seven are scopes, not a number of agents; you may combine them into fewer dispatches, but all seven scopes must be covered. The
first five are fact-checking. Scope 6, tradability, catches "every number is right but the conclusion hangs in the air". Scope 7,
presentation and copy, follows item ⑦ of `references/quality-bar.md`. Run **at least two rounds**. Round one covers all seven
scopes. Round two includes at least the opposing-case review (take the strongest counterparty, change the parameters, recompute,
and try to overturn the rating) and tradability; if there is a translated edition, add translation consistency (cell by cell,
with Appendix C identical to `assets/disclaimer.md`). Pure fact-checking has diminishing returns after two rounds. Publish the
revisions as a three-column table, "original wording → revised wording → nature of change", in Appendix C.

Pre-publication self-check:
1. All **eight components** of framework section 5 are present: mechanism diagram / evidence grading / certainty tiers /
   bull-bear comparison / falsification conditions and observation calendar / known limitations / **misreading-prevention
   section** / **audit revision log**.
2. Work through the **tradability final check** in `references/judgment.md` section 9 item by item, and write the result into
   `checks.md` (passed / fixed / n/a, with a note).
3. Use the `assets/disclaimer.md` template verbatim for the disclaimer and conflicts of interest. Write out all four conflict
   items one by one, including "none".
4. Tick off the landing checklist in `references/quality-bar.md` item by item (all three horizons of outlook present / decision
   chapter in operational-research format / all seven audit scopes run).
5. After publication: register the core judgments, the annual rating and the monthly and quarterly outlooks in the ledger
   (`python3 scripts/ledger.py add … --tier …`, see `references/pipeline/05-publish.md`), add the series to `research/watch.json`
   (`references/pipeline/05-publish.md`), and confirm that `python3 scripts/desk.py check` finds every ledger series covered.
   Later updates follow `references/pipeline/06-updates.md`.
