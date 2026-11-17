# Industry-Chain Research Flow

> Read `references/quality-bar.md` (the entry bar: read it before starting, and go through its landing checklist before
> publishing) and `references/framework.md` first.
> Applies to report type `industry`. It also applies to the industry slice of `advisory` and `macro` reports.

Notation: **[Cause]**, **[Process]**, **[Outcome]** are the cause / process / outcome classes from the framework.
**[Fixed]**, **[Probabilistic]**, **[Unknown]** are the certainty tiers. E1-E5 are the mispricing evidence types in
`references/judgment.md` section 2.

**An industry-chain study rests on two assets:**
1. **The [Fixed] part of supply**: capacity under construction and the dates it comes on line. This is the hardest and most
   predictable information in the whole system, because poured concrete cannot be changed. Whoever works out the capacity cycle
   knows one to three years ahead where prices are going.
2. **The location of the bottleneck**: it decides who receives the profit of the whole chain. Money settles where technology is scarce.

Everyone forecasts demand, and very few forecast it well. **Supply, by contrast, can be counted.** That is the structural
reason an industry-chain report can keep producing insight the market does not have.

---

## Step 0 · Boundary definition and chain map

**Must answer**
- Where is the chain's **boundary**? How far up does it go (to which raw material or equipment), and how far down (to which end market)?
  If the boundary is drawn wrongly, the whole value allocation in the report is computed wrongly.
- How many layers and segments are there? For each segment: **representative companies, the technical barrier, and substitutability**.
- Each segment's **share of output value or market value**, and the gap between its share of output and its share of profit.
  The gap is itself a conclusion.

**Output**: a full chain map (layers and segments) and a table of representative companies and shares by segment.

Warning: do not copy an industry report's classification. Classify by **bargaining power and technical barrier**, not by statistical
industry codes. Industry codes lump together links whose bargaining power is entirely different.

---

## Step 1 · Demand side: break it down to the cause

Do not stop at "the industry is worth X and grows at Y% a year". That is an [Outcome]. Keep breaking it down until you reach **driving factors**:

- Whose budget pays for demand (a government programme, corporate capex, corporate operating expense, household consumption)?
  Different budget sources have entirely different cyclicality and interest-rate sensitivity.
- Decompose into quantity × price. What drives quantity? What drives price?
- The penetration curve: where on the S-curve is it now? (Introduction: watch the technology inflection. Growth: watch capacity.
  Maturity: watch share and cost.)
- How **postponable** is demand? Is it rigid or deferrable? Deferrable demand vanishes at once in a downturn and rebounds sharply in recovery.
- Substitution: how much installed base of the previous generation remains? How high is the switching cost?

**Output**: a demand driver tree (broken down to observable [Cause] items), a penetration-curve position, and an assessment of how postponable demand is.

---

## Step 2 · Supply side: the capacity cycle (the centre of this flow)

**Count four tables:**

| Table | Contents | Cause / process / outcome | Fixed / probabilistic / unknown |
|---|---|---|---|
| Existing capacity | Each player's nameplate capacity, effective capacity, current utilisation | [Cause] (nameplate) / [Process] (utilisation) | [Fixed] |
| **Capacity under construction** | Project, size, start-up date, current progress | **[Cause]** | **[Fixed]** |
| Planned capacity | Announced but not started; estimate the probability it goes ahead | [Cause] | [Probabilistic] |
| Exiting capacity | Closures, ageing, forced retirement by regulation | [Process] | [Fixed] / [Probabilistic] |

The two columns correspond to framework question 1 (cause / process / outcome) and question 2 (fixed / probabilistic / unknown).
Do not mix the labels. The load-bearing-chain check (step 2, `references/pipeline/02-research.md`) reads only the
cause / process / outcome column. Mismatch identification (Step 7.5) uses the fixed / probabilistic / unknown column. The labels
are consistent with L3-B in `references/indicators.md`.

**Must answer**
1. Over the next 8-12 quarters, what is the **net new effective capacity** each quarter? Set against demand growth, how large is the shortfall or surplus?
2. How long is the **lag from capital expenditure to capacity release**?
   Warning: **do not use a generic assumption.** The right method is to extract, from the announcements of the last 3-5 completed
   projects in this industry, the actual interval "start-of-construction announcement → start-up announcement → full-rate
   announcement", take the median, and state the sample. Different asset forms differ enormously (heavy-asset plant construction,
   equipment expansion, production-line retrofit), so compute them separately.
3. **The ramp curve.** Start-up is not full production. How long is the yield ramp? How much should effective supply be discounted during it?
4. Supply elasticity: when prices rise, how long before new supply arrives? (The lower the elasticity, the larger the price elasticity.)
5. Exit barriers: can capacity be stopped when it loses money? (Capacity that cannot be stopped means a price war that runs below cash cost.)

**Output**: a quarterly net-new-capacity table (next 8-12 quarters), a supply-demand gap estimate, the lag-extraction sample, and the ramp assumptions.

**Do this step thoroughly and the report is half done.**

---

## Step 3 · Bottleneck identification: find the neck of the hourglass

Walk along the chain and ask three questions of each segment, marking every **single-point dependency**:

1. How many effective suppliers does this segment have? (1 = single point; 2-3 = oligopoly; more than 5 = competitive.)
2. How long and how costly is it to switch supplier? (Qualification time is the most underestimated barrier.)
3. What limits capacity expansion in this segment (equipment lead times, talent, energy, licences, patents)?

**Output**:
- A **bottleneck list**: which segments are the neck, and what constrains their capacity.
- The **longest single-point dependency chain**: trace from the furthest upstream to the end market and find the path where every
  layer has no second supplier. This is the most fragile path in the industry and also the one with the most pricing power. It
  is usually the most striking chart in the report.
- For each bottleneck, the **release condition and timing** (a new supplier qualified? a new technology route that bypasses it?).

---

## Step 4 · Value allocation: who gets the profit

**Must answer**
1. Compare gross and net margin by segment (align fiscal years and accounting standards) and draw the **profit gap**.
2. What causes the gap: a bottleneck, a brand, or policy protection? Different causes mean entirely different sustainability.
3. **The direction bargaining power is moving.** Use three groups of indicators: receivable and payable terms, customer
   prepayments, and inventory transfer. They show which segment is absorbing the working capital. This reflects changes in
   bargaining power earlier than gross margin does (gross margin is an [Outcome]; payment terms are a [Process]).
4. **Cost pass-through** to the end price: when the upstream raises prices, how long until it reaches the end market, and at what
   pass-through rate? The segment that cannot pass cost on is the one whose profit will be squeezed.

**Output**: a value-allocation chart (gross margin and output share by segment), a trend of the three bargaining-power indicators,
and the cost pass-through path with pass-through rates.

---

## Step 5 · Institutions and geopolitics

An industry-chain report cannot avoid this layer, and it is often the largest variable:

- Export controls, import tariffs, entity lists: which segments and technology nodes are covered, when they take effect, what exemptions apply.
- Technical standards and certification: who controls standard-setting? Which segments change position if a standard changes?
- Subsidies and industrial policy: the **form** of the subsidy (tax, direct grant, procurement, financing) and the phase-out schedule.
  Warning: the date a subsidy phases out is [Fixed], but the demand gap after the phase-out is [Probabilistic]. Say the two separately.
- Environmental, energy-use and safety regulation: will it force a block of capacity out? (This is the strongest exogenous shock to supply.)

**Output**: a timeline of institutional variables and an impact matrix of each rule on each segment (beneficiary / loser / neutral).

---

## Step 6 · Cycle position and historical analogies

1. Where is the industry in the capacity cycle?
   `capacity shortage → price rise → capex expansion → capacity release → price fall → capex contraction → clearing → capacity shortage`
   Locate it using: capex growth, the ratio of capacity under construction to existing capacity, capacity utilisation, and where price sits relative to cash cost.
2. Where is the inventory cycle? (Active restocking / passive restocking / active destocking / passive destocking.)
   Decide it from the relative direction of sales growth and inventory growth.
3. Historical analogies: find 2-3 structurally similar past cycles and give their duration, amplitude and the way they cleared.
   Warning: **give three failure conditions at the same time** (framework L0-5). An analogy without failure conditions may not enter the conclusion chapter.

**Output**: a cycle-position chart (with the current position marked), an inventory-cycle determination, and an analogy table (with failure conditions).

---

## Step 7 · Ranking the links and what it means for allocation

Arrange all links in one table. This is the core deliverable of an industry-chain report:

| Link | Business conditions | Supply-demand gap | Bargaining-power trend | Valuation percentile | Relative rank (12 months · relative to <benchmark>) | Trigger signal |
|---|---|---|---|---|---|---|

- Express **relative rank** as a relative judgment within the industry. It is not a buy or sell instruction.
- A **trigger signal** must be a specific, publicly observable event or threshold (framework 4.3 / 4.4).

**Output**: the link ranking table and a representative name for each link (listed for reference only, not a recommendation).

**Settleable wording** (red line 8 in `references/framework.md` section 6, and `references/judgment.md` section 4): every
relative judgment in the ranking table must be settleable. Write it as the three-horizon outlook in "Rating and outlook" in
`references/quality-bar.md`:
- **Annual horizon**: "next 12 months · <link vehicle> relative to <benchmark> · start date". The link vehicle is the matching
  industry index or a basket of representative stocks (put the constituents and weights in Appendix A). Choose the benchmark by
  the two tests of investability and unrelated exposure in `references/judgment.md` section 4 (for an industry chain, use the
  matching broad index or asset class; the S&P 500 is not the default). State the benchmark, the reason for choosing it and the
  start date on the summary page. Keep the benchmark the same across versions of a series.
- **Monthly horizon** = an event calendar and triggers (the catalyst path table of Step 7.5). **Quarterly horizon** = which
  tracked indicator prints this quarter, and what print counts as a hit. Combine the three into the three-horizon outlook table
  in chapter 1. It appears once in the whole text.
- After publication, register each call in the ledger as set out in `references/pipeline/05-publish.md`. Register every core
  judgment, and **one entry per horizon** for the three-horizon outlook (annual `--tier annual`, quarterly `--tier quarterly`,
  monthly `--tier monthly`; the outlook cell supplies the claim text, and the falsifier is "date + settlement"):
  `python3 scripts/ledger.py add --report ID --series CHAIN --claim '…' --falsifier '…' --horizon 12 --benchmark '<benchmark>' --issued YYYY-MM-DD --tier annual`
  (always single-quote the arguments: a double-quoted shell argument swallows a `$` followed by digits; see `05-publish.md`).
  After registering, add one entry for this series to `research/watch.json` (the due dates and ledger IDs of the monthly and
  quarterly horizons). `python3 scripts/desk.py run` reminds you when they fall due.

---

## Step 7.5 · Consensus, mispricing and catalysts (this step cannot be skipped)

An industry-chain report passes the first three gates of `references/judgment.md` as well. The only change is that the object
is a link instead of a single stock:

1. **Consensus**: what is the market's uniform narrative on this chain? Reconstruct it from **the leading stock's valuation
   percentile and the capacity / price assumptions it implies** (the price reverse-calculation, item 1 in `references/judgment.md`
   section 1, free and the default).
2. **Mispricing**: which link's [Probabilistic] is the market treating as [Fixed]?
   Typical cases: treating planned capacity as certain supply, treating policy subsidy as permanent, treating the current price spread as the long-run mean.
   Give E1-E5 evidence for each mispricing point (`references/judgment.md` section 2). If you cannot, downgrade it to "watch".
3. **Catalysts**: which events in the next 12 months will force the market to reprice? (Capacity start-up announcements, leader
   guidance, price crossing the cost line, regulation effective dates, inflection in trade-association data.)

**Output**: a consensus reconstruction, a mispricing table (with evidence types), and a catalyst path table.

---

## Step 8 · Scenarios, tracking and write-up

- **Three scenarios**, each stating its **discriminating signs** (so readers can tell for themselves which path has been taken).
  Warning: probabilities must not be guessed. Accept only one of three sources: historical frequency (state the sample), market-implied
  (futures curves, spreads reverse-calculated), or explicit subjective assignment (state the basis and run a ±10 percentage-point
  sensitivity). See `references/judgment.md` section 5.
- **Observation calendar**: capacity start-up announcements, trade-association monthly data, customs import/export, price indices,
  leader earnings guidance. For each, the disclosure date and what to look for.
- **Chapter plan**: set the chapter order by the topic (the outputs of Step 0-7.5 each become a chapter or are merged). There is
  no fixed chapter count. Use the structure only as a guide; do not reproduce an old fixed layout. These components **must be
  placed** (governed by `references/pipeline/03-writing.md` and `references/quality-bar.md`):

| Component | Where it goes | Basis |
|---|---|---|
| Overview dashboard | Inside chapter 1 (summary), after the cover page, once in the whole text. 8-10 processed chain-level indicators (quarterly net new capacity, supply-demand gap, the three bargaining-power indicators, concentration at the neck, and so on), each with a mini series, as a dashboard chart block | `quality-bar.md` item ④ "one-page overview", item ⑤-3 |
| Core judgment + three-horizon outlook table + transition-conditions box | Chapter 1, once in the whole text. Monthly = event calendar and triggers; quarterly = the tracked indicator that prints this quarter; annual = relative judgment on the link + benchmark + start date (the settleable wording in Step 7) | `quality-bar.md` "Rating and outlook"; `judgment.md` section 4 |
| Decision chapter (five items of operational research) | After the link ranking, before risks: scenario-to-action map / entry and invalidation conditions / comparison of ways to express the view / position and risk-budget framework / review cadence. The four required items of `judgment.md` section 5 appear in the chapter, once each (at chain level, do not give single-stock target prices; express price levels in terms of the link vehicle) | `quality-bar.md` "Decision chapter"; `judgment.md` section 5 |
| Misreading-prevention section | After risks, before tracking indicators | Framework section 5, component 7 |
| Audit revision log | Appendix C, three columns: "original wording → revised wording → nature of change" | Framework section 5, component 8; step 4 (`references/pipeline/04-audit.md`) |
| Appendix D, derivations and calculations | After Appendix C: quarterly net new capacity, supply-demand gap, median of the lag sample, cost pass-through rate, chain-level valuation cross-checks, and every other number you computed yourself | `quality-bar.md` item ②-4 |

The **fixed internal structure of each link chapter** (it keeps the rhythm of the whole report consistent):
> primary-source anchor figures → core judgment box → definition-notes box → vendor comparison table → data gaps that remain for this link

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
