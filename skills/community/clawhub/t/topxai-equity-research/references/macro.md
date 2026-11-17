# Macroeconomic Research Flow

> Read `references/quality-bar.md` (the entry bar: read it before starting, and go through its landing checklist before
> publishing) and `references/framework.md` first.
> Applies to report types `macro`, `advisory` and `quarterly`.

Notation: **[Cause]**, **[Process]**, **[Outcome]** are the cause / process / outcome classes from the framework.
**[Fixed]**, **[Probabilistic]**, **[Unknown]** are the certainty tiers. E1-E5 are the mispricing evidence types in
`references/judgment.md` section 2.

**Macro reports slide into empty talk more easily than any other kind**, because macro sits furthest from prices and closest to
grand narrative. The only defence is to hold to two rules:

1. **Do not forecast aggregates. Describe constraints and reaction functions.**
   "Next year's GDP growth is X%" is neither reliable nor tradable. What has value is this:
   "Under condition A, policy must turn, because constraint B has been reached; the observable signal of the turn is C."
2. **Every conclusion must land on "who is forced to do what".**
   Macro transmission works through the **forced behaviour of specific actors**: the central bank is forced by inflation, the
   treasury by debt, firms by profit, households by cash flow, fund managers by drawdown. Find the "forced" and you find the turning point.

---

## Step 0 · Structural positioning: place the economy in L0 first

A macro report must open with the **slow variables**. Otherwise everything after it is noise.

**Must answer** (one group at a time, numbered as in the framework, L0-1 to L0-5)
1. **L0-1 Productivity**: the trend in total factor productivity, the position on the technology S-curve, and the rate at which the
   unit cost of energy and compute is falling. How big can the pie grow?
2. **L0-2 Relations of production and distribution**: labour share, corporate profits as a share of GDP, the direction of the tax
   and transfer system. Where is the long-run centre of the profit margin? Is the current high margin held up by a technical
   barrier, or by a distribution pattern that is only temporarily favourable (the latter mean-reverts)?
3. **L0-3 Institutional order**: trade rules, the settlement system, capital controls, technology controls.
4. **L0-4 Demographic cycle and collective experience**:
   - Structural layer: age structure, dependency ratio, household formation rate, the turning point of labour supply.
   - **Experience layer (a distinctive part of this framework; do not omit it)**: have today's dominant market participants and
     policy-makers **lived through a comparable cycle**?
     If the answer is "no": expectations adjust more slowly, policy involves more trial and error, volatility is larger, the
     "this time is different" narrative has more of a market, and confirmation of the turning point lags markedly.
     If the answer is "yes": reactions are faster, overreaction is more likely, and the policy toolbox is used more decisively.
     This item directly sets the **speed parameter of the turn** in the scenario tree later.
5. **L0-5 Stage positioning**:
   - **Development stage**: industrialising / urbanising / post-industrial / ageing. Each has a different growth engine and bottleneck.
   - **Debt cycle position**: leverage by sector (government / corporate / household / financial) and its direction of change;
     the **duration and currency structure** of the debt (a high share of short-term debt means refinancing risk; a high share of
     foreign-currency debt means the exchange rate is itself solvency risk); and the interest-coverage multiple (interest
     expense against income). This is the hard constraint on "how long can it hold".
   - **Historical analogies** (stagflation, balance-sheet recession, a particular tightening cycle, and so on): if you use one,
     you must give **three failure conditions** at the same time, and each must meet the three requirements of framework L0-5:
     observable (points to specific public data or an event), structural (a difference in mechanism, not in magnitude), and
     explicit (says which part of the analogy no longer applies: the duration, the amplitude or the way it cleared). An analogy
     that cannot meet this goes only into a background chapter, marked "background reference only". It may not enter the
     conclusion chapter (red line 3 in `references/framework.md` section 6).

**Output**: an L0 positioning card (one paragraph of conclusion for each of the five groups, numbered as in the framework), a
table of sector leverage and interest coverage, a judgment on collective experience and what it implies for reaction speed, and
a historical-analogy table (with the three failure conditions; write "not used" if no analogy is used).

---

## Step 1 · Capital and liquidity (L1): the fastest variables

**Must answer**
- **Central bank**: the direction and speed of its balance sheet, the policy-rate path, and changes in forward-guidance wording
  (compare word for word against the previous meeting's minutes).
- **Credit creation**: bank lending, net corporate bond financing, non-bank and shadow channels.
  Warning: the central bank adding liquidity is not credit expansion. **The monetary base is a [Process]; credit creation is the
  link that actually reaches the real economy.** When the two diverge (liquidity added but credit not expanding), transmission is
  blocked at the banks or on the demand side, and you must look specifically for the blockage.
- **Risk appetite**: credit spreads (investment grade and high yield), volatility, leverage, IPO and M&A activity.
- **Cross-border**: direction of capital flows, exchange rates and rate differentials, changes in reserves.
- **Term structure**: the shape of the yield curve and the term premium. This is the market's pricing of the future policy path
  and can be used directly to reverse-engineer market consensus (framework 4.1).

**Output**: a liquidity dashboard (5-7 indicators, each labelled [Cause] / [Process] / [Outcome]), a table comparing central-bank
wording meeting by meeting, and a judgment on where credit transmission is blocked.

---

## Step 2 · Breaking down aggregate demand (L2)

Break down each of the four sectors to its **driving factors**. Do not stop at growth rates:

| Sector | Break down to |
|---|---|
| Consumption | Income growth × employment × propensity to consume. Separate durables from non-durables (the former is rate-sensitive, postponable demand) |
| Investment | Corporate capex (look at profits and capacity utilisation) / property (starts, sales, inventory clearance) / infrastructure (fiscal quota and project delivery) |
| Exports | External demand strength × share × price. Separate volume from price |
| Government | Deficit ratio, special-bond quota and actual drawdown progress (the quota is [Fixed]; the drawdown progress is [Process]) |

**Must answer**: which sector is the current **marginal variable**? That is, who contributes most of the change in the aggregate.
The marginal variable decides where policy should push, and where observation should focus.

**Output**: a contribution breakdown across the four sectors, the identified marginal variable, and a list of leading indicators for each sector.

---

## Step 3 · Aggregate supply and prices

- **Supply side**: labour supply (participation rate, migration, retirement), capital stock, energy and commodities, the state of supply chains.
- **Inflation structure**: break it into four blocks and read each separately: goods / services / housing (rent) / energy and food.
  Their drivers and policy sensitivities are entirely different.
  Warning: looking only at headline CPI leads to a completely wrong policy judgment. Services and rent are far stickier than goods.
- The **output gap**, and evidence for a wage-price spiral (wage growth against productivity growth).

**Output**: a four-way inflation decomposition table (the trend and drivers of each), a list of supply constraints, and an assessment of the evidence for a wage-price spiral.

---

## Step 4 · The policy reaction function: turning macro into something tradable

**This is the most valuable section of a macro report.** Do not predict policy. Describe "under what conditions policy must move".

For each major policy actor (central bank / treasury / regulator), write:

| Actor | Objective function | Hard constraints | Conditions that trigger a turn | Observable signals | Tools and lags |
|---|---|---|---|---|---|

- **Objective function**: the official wording plus the actual priority (the two often differ; point to the evidence).
- **Hard constraints**: the inflation ceiling, the employment floor, the exchange-rate floor, the ability to service debt, financial stability.
- **Trigger conditions**: quantify as far as you can ("core inflation below X% for two consecutive quarters", "unemployment rate breaks through Y%").
- **Lags**: from decision to implementation to effect on the real economy, how long does each take?

**Output**: a policy reaction-function table (one row per actor) and, for each trigger condition, how far the economy is from it today.

Warning: **you must calibrate against history, or the numbers in the "trigger conditions" column are made up.**
There is a mandatory subsection, "Back-test". List the actor's last 3-5 real turns. For each, fill in: where the variable stood
at the time / whether your function would have signalled / how much earlier or later the actual turn came. Disclose the cases
the function cannot explain and give the reason for each exception.

For policy actors with **no public rule** (for example some emerging-market central banks), do not force a reaction function on
them. Write a "constraint list + historical behaviour pattern" instead, and say explicitly that this is not a reaction function.
For **committee-based** actors, add a column "who is the median vote, and how has their public stance drifted". The person to be
persuaded is the median vote, not the chair.

---

## Step 5 · Market participants and positioning (L4)

To turn a macro view into a return, you have to know **who is on the other side**:

- Positions and constraints of the main fund types: pensions and insurers (long-duration liabilities, constrained by regulation),
  mutual funds (redemption pressure), hedge funds (leverage and stop-losses), sovereign funds, retail, passive index funds.
- What is the **crowded trade** now? (The direction with the strongest consensus is often the most fragile.)
- **Who will be forced to act?** (Hitting risk limits, index rebalancing, duration gaps, margin calls.) Forced action is the
  strongest short-term price driver, and its timing can often be foreseen.

**Output**: an assessment of positioning and crowding, and a "forced action" list (actor / trigger condition / order of magnitude).

---

## Step 6 · Certainty tiers and mispricing identification

Sort all the key variables above into [Fixed] / [Probabilistic] / [Unknown] (framework 1.2). Then do the most important step:

> **For each one, mark which class the market currently treats it as.**

| Variable | My determination | The market's currently implied determination | Evidence type (E1-E5) | Mispricing | Trading implication |
|---|---|---|---|---|---|

Fill the column "the market's currently implied determination" with evidence under `references/judgment.md` section 2. **It may
not be filled by assertion.** Mark the evidence type on every row:
- **E1 Price reverse-calculation**: the policy path reverse-calculated from fed funds futures and the OIS curve, breakeven
  inflation and real rates, term premium (sources in `references/indicators.md` L1);
- **E2 Event study**: the historical price reaction on the release days of the same data or on meeting days (a small reaction
  means the market already treated it as [Fixed]);
- **E3 Valuation percentile**: the percentile of an asset class against its own history (credit spreads, equity risk premium,
  term premium), attributed to this variable;
- **E4 Option pricing**: implied volatility and skew in rate and FX options, and whether event-day implied moves price this risk;
- **E5 Positioning structure**: CFTC positioning reports and crowding, the share of passive money (the positioning assessment of Step 5).

A mispricing point with no evidence of any type from E1-E5 is **downgraded to "watch" and may not enter the core conclusions**.

Mispricing is where a report's view comes from. **No mispricing means no view.** In that case, honestly writing "current pricing
is reasonable, no significant mispricing" is worth far more than forcing a view, and it builds credibility over the long run.

---

## Step 7 · The scenario tree

- A main scenario plus 2-3 secondary scenarios. Give each a **probability** and **discriminating signs** (how far along the path
  you must be to know it is this one).
  Warning: probabilities must not be guessed. Accept only one of three sources: historical frequency (state the sample: the
  historical incidence of comparable cycles), market-implied (policy-path probabilities reverse-calculated from fed funds
  futures, OIS and breakeven inflation), or explicit subjective assignment (state the basis and run a ±10 percentage-point
  sensitivity). See `references/judgment.md` section 5. Applying a default 25/50/25 split violates red line 7 in
  `references/framework.md` section 6.
- Under each scenario: policy path / performance of each sector / **asset-class implications** (equities / bonds / FX / commodities).
- Warning: scenarios are not "good, middling, bad" in new words. Different scenarios must differ in **structural mechanism**,
  that is, in the causal path, and not merely in the amplitude of one path.

**Output**: a scenario tree (with probabilities and their sources, discriminating signs, and asset implications).

**Settleable wording** (red line 8 in `references/framework.md` section 6, and `references/judgment.md` section 4): write the
core macro judgments as the three-horizon outlook in "Rating and outlook" in `references/quality-bar.md`:
- **Annual horizon**: relative judgments on asset classes, written as "next 12 months · <asset> relative to <benchmark> · start
  date". Choose the benchmark by the two tests of investability and unrelated exposure in `references/judgment.md` section 4
  (for macro use the matching broad index or asset class; the S&P 500 is not the default). State the benchmark, the reason for
  choosing it and the start date on the summary page. Keep the benchmark the same across versions of a series.
- **Monthly horizon** = an event calendar and triggers (the catalyst path and observation calendar of Step 8). **Quarterly
  horizon** = which data prints this quarter, and what print counts as a hit. Combine the three into the three-horizon outlook
  table in chapter 1. It appears once in the whole text.
- After publication, register each call in the ledger as set out in `references/pipeline/05-publish.md`. Register every core
  judgment, and **one entry per horizon** for the three-horizon outlook (annual `--tier annual`, quarterly `--tier quarterly`,
  monthly `--tier monthly`; the outlook cell supplies the claim text, and the falsifier is "date + settlement"):
  `python3 scripts/ledger.py add --report ID --series THEME --claim '…' --falsifier '…' --horizon 12 --benchmark '<benchmark>' --issued YYYY-MM-DD --tier annual`
  (always single-quote the arguments: a double-quoted shell argument swallows a `$` followed by digits; see `05-publish.md`).
  After registering, add one entry for this series to `research/watch.json` (the due dates and ledger IDs of the monthly and
  quarterly horizons). `python3 scripts/desk.py run` reminds you when they fall due.

---

## Step 8 · Observation calendar and write-up

**Catalyst path** (`references/judgment.md` section 3): which events will force the market to reprice, when they are expected,
and how long past due before they are void. This is a different thing from the observation calendar below. One governs "when it
gets acknowledged", the other "when it counts as wrong".

**Observation calendar** (the most practical page of a macro report):

| Date | Data / event | What to look at | Which judgment it tests | Falsification threshold |
|---|---|---|---|---|

Order it by the actual release schedule for the next 1-2 quarters. Include: central-bank meetings, key data releases, fiscal
announcements, major auctions and maturities, and the political calendar.

**Suggested chapter plan** (the order can be adjusted to the topic):
> Summary and core conclusions → Methodology and data definitions → L0 structural positioning → Liquidity and credit → Aggregate demand →
> Aggregate supply and inflation → Policy reaction function (with back-test) → Market participants and positioning →
> Certainty tiers and mispricing (with evidence types) → Scenario tree → Operating framework (decision chapter) → Risks →
> Misreading-prevention section → Catalyst path and observation calendar →
> Appendices: A Terms and definitions / B Source list and known limitations / C Disclaimer and disclosures + audit revision log / D Derivations and calculations

The order can change, but these components **must be placed** (governed by `references/pipeline/03-writing.md` and `references/quality-bar.md`):

| Component | Where it goes | Basis |
|---|---|---|
| Overview dashboard | Inside chapter 1 (summary), after the cover page, once in the whole text. 8-10 processed indicators (liquidity, credit transmission, the four-way inflation decomposition, each policy actor's distance from its trigger condition, and so on), each with a mini series, as a dashboard chart block | `quality-bar.md` item ④ "one-page overview", item ⑤-3 |
| Core judgment + three-horizon outlook table + transition-conditions box | Chapter 1, once in the whole text. Monthly = event calendar and triggers; quarterly = the data that prints this quarter; annual = relative asset-class judgment + benchmark + start date (the settleable wording in Step 7) | `quality-bar.md` "Rating and outlook"; `judgment.md` section 4 |
| Decision chapter (five items of operational research) | After the scenario tree, before risks: scenario-to-action map / entry and invalidation conditions / comparison of ways to express the view / position and risk-budget framework / review cadence. The four required items of `judgment.md` section 5 appear in the chapter, once each (express price levels in terms of the asset class being judged) | `quality-bar.md` "Decision chapter"; `judgment.md` section 5 |
| Misreading-prevention section | After risks, before the observation calendar | Framework section 5, component 7 |
| Audit revision log | Appendix C, three columns: "original wording → revised wording → nature of change" | Framework section 5, component 8; step 4 (`references/pipeline/04-audit.md`) |
| Appendix D, derivations and calculations | After Appendix C: the reaction-function back-test, the market-implied reverse calculations of the policy path and inflation, the basis for scenario probabilities, and every other number you computed yourself | `quality-bar.md` item ②-4 |

- Before fixing the core judgment and the annual horizon, run a bull/bear debate as set out in step 2.5
  (`references/pipeline/02-research.md`), with `research-bull` and `research-bear` reading only the research notes. When the
  annual horizon is not neutral, respond in the body, one by one, to the first three points of the opposing case.
- After the draft, run the adversarial audit in `references/pipeline/04-audit.md`: **two rounds, four to five scopes, including
  the opposing case and (if you publish a translated edition) translation consistency**. Round one (the first draft) runs four
  scopes, one of which is scope 7, presentation and copy, per `quality-bar.md` item ⑦ (title formulas, chart types, dark blocks
  and repeated components, decorative indicators). Round two (v2, after the translated edition is synced) runs five scopes,
  including the opposing-case `skeptic` (take the opposite side of the core judgment, change only the parameters, keep the
  formulas, and recompute) and, if there is a translated edition, `consistency`. Publish the revisions as a three-column table,
  "original wording → revised wording → nature of change", in Appendix C.
- Pre-publication self-check: (1) go through the landing checklist in `quality-bar.md` item by item; (2) the eight components of
  framework section 5 (including the misreading-prevention section and the audit revision log); (3) the tradability final check
  in `references/judgment.md` section 9, with the result written to `checks.md` (passed / fixed / n/a, with a note).
- Use the template in `assets/disclaimer.md` verbatim for the disclaimer and conflicts of interest.
- Publishing, ledger registration and watch registration follow `references/pipeline/05-publish.md`. Later updates follow `references/pipeline/06-updates.md`.

---

## Three macro-specific traps

1. **Narrative standing in for mechanism.** Grand narratives ("great-power rivalry", "paradigm shift") are satisfying to read but
   cannot be falsified. Every narrative must land on a specific actor's specific constraint, or be deleted.
2. **Definition traps.** Seasonally adjusted versus unadjusted, year-on-year versus annualised month-on-month, nominal versus
   real, and statistical definitions changed midway. State the basis of every macro figure, and align it before comparing across periods.
3. **Mistaking policy intent for policy effect.** Announcing a policy is the start of an [Outcome], not its end. Track the
   [Process] indicators of **implementation progress** (quota utilisation, project start rate, funds-arrival rate). The
   announcement alone is not a conclusion.
