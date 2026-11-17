# From Analysis to Tradable Judgment: the procedure

> Prerequisite: `references/framework.md`. Section 4 of the framework says what to do. This file says **how to do it, what to deliver,
> and how to degrade when the data cannot be had**.
>
> **Why this is a separate file**: error-prevention (evidence grading, definition traps, not reversing cause and outcome) can at best
> guarantee that "every number is right". A report whose numbers are all right but whose conclusion hangs in the air still leaves the reader
> not knowing what to do at what price, how long to hold, or where the thesis breaks. This file is the last step that turns research
> into a product. **Every report must pass through it.**

---

## 1. Consensus reconstruction: know who you differ from first

"Difference from consensus" is where value comes from, but **sell-side consensus is paid data** (see L4 in `references/indicators.md`).
With free data only, degrade in the order below and state in the report which level you used:

| Priority | Method | Availability | How |
|---|---|---|---|
| **1. Implied consensus (recommended default)** | **Back-solve from price** | 100% free | Turn current market cap or EV into implied revenue growth, margin, share, or FCF path. See `references/equity.md` Step 6.2 |
| 2. Public compilation | The consensus table on the company's IR page, or the "street expectations" management cites on the earnings call | Partly available | Name the compiler and the date |
| 3. Event expectations priced by the market | The size of the event move implied by option-chain implied volatility, or the implied earnings move | Free (broker chains) | Gives magnitude only, not direction |
| 4. Wording evidence | The words used in sell-side report titles or media paraphrase ("expects" versus "will") | Scattered | Grade [B] evidence. It can support a point but cannot carry one |

**Hard rule**: if none of 1 to 4 can be obtained, the section must say
"This report did not obtain sell-side consensus; market-implied assumptions stand in for consensus."
**Never use an unsourced "the market generally believes".** That is rhetoric, not consensus.

---

## 2. Mismatch evidence: "which class the market treats it as" needs evidence

Section 1.2 of the framework requires the view to land on a mismatch point (the market treats [Probabilistic] or [Unknown] as [Fixed], or the reverse).
But the **"market's implied verdict" column may not be filled by assertion.** It must meet at least one of the following, with the evidence type marked in the table:

| Evidence type | What to do | Evidence grade |
|---|---|---|
| **E1 Price back-solve** | Compare the implied assumption from a reverse DCF or multiple with the real-world distribution of that variable | [A] |
| **E2 Event study** | The size of the price reaction when comparable news was historically announced (small reaction means the market already treated it as [Fixed]) | [A] |
| **E3 Valuation percentile** | Premium or discount to peers or to own history, attributed to this variable | [B] |
| **E4 Option pricing** | Whether the implied-volatility skew, or the event-day implied move, prices this risk | [A] |
| **E5 Positioning structure** | High passive share means the variable is not actively priced at all; high crowding means it is fully priced | [B] |

**Hard rule**: a mismatch point with no E1-E5 evidence is, by the framework's own rule, **downgraded to "Observation" and may not be a core thesis.**

---

## 3. Catalyst path: an observation point is not a catalyst

These are two different things and must be produced separately:

- A **falsification condition** answers "how do I know I am wrong". It protects the reader.
- A **catalyst** answers "when is the market forced to admit I am right". It decides whether the reader can make money.

Section 4.2 of the framework says the timing gap is the most tradable source of difference, so the timing path must be delivered. **Every report must include this table:**

| Catalyst event | Expected timing (quarter precision) | Why it forces the marginal price-setter to change behaviour | If it does not occur, how long until the judgment lapses |
|---|---|---|---|

**Hard rules**:
- If the core conclusion has **no catalyst within 12 months**, the summary page must say plainly:
  "This judgment is a structural view that needs N years to play out. **It does not suit capital with an evaluation period.**"
- Compress the summary front page to three lines: **the pivotal variable / the nearest catalyst / the price at which the thesis fails**.

---

## 4. Rating and target price: must be settleable

The old wording "Buy > +15%" has no term and no benchmark. It can never be falsified, because one can always say "it is not time yet".
That empties the hard rule "a conclusion must be falsifiable". The settleable wording:

> **Rating = expected relative return over the next 12 months versus a <named benchmark>.**
> Buy > +15% · Overweight +5% to +15% · Neutral −10% to +5% · Underweight < −10%

**This is the annual horizon of the three-horizon outlook in `references/quality-bar.md`, "Rating and outlook".** A rating is not one word. It is a three-horizon outlook:
monthly (1-3 months, driven by the event calendar, settled by event), quarterly (3-6 months, tracking indicator prints, settled by a statement line),
annual (12 months, the wording of this section, settled by relative return against the benchmark). Each horizon gets its own ledger entry
(`--tier monthly`, `quarterly`, `annual`). When an entry falls due, the coverage-watch script flags it (`python3 scripts/desk.py run`), and it is settled on its own basis.
The three horizons form one table, with a "migration conditions" box written in advance and never edited afterwards. The table appears once, in chapter 1.
The conclusion chapter states only the handling rule after a trigger and does not repeat the table
(`references/quality-bar.md`, item 5.3; repeating the three-horizon outlook in three places was a blocker in an earlier report's audit).

- **The benchmark must be stated on the front page**, with the start date and the reason it was chosen. Choose by two tests: **investability**
  (the benchmark itself can be bought: an index or a replicable basket; a basket that contains another subject of the same series does not count)
  and **unrelated exposure** (the benchmark must not carry factors outside the subject's thesis, for example a BTC exposure that comes with a peer basket).
  For a single stock, prefer the industry-chain index or the peer median first. If those fail the two tests, fall back to a broad index.
  For industry-chain and macro reports, use the matching broad index or asset class. **The S&P 500 is not the default.** Re-decide for every report.
- All versions in the same series must use the same benchmark (a track record accumulates by series, and changing the benchmark breaks it).
  If a change is unavoidable, old conclusions are still settled on the old benchmark, and the "settlement of the previous version" chapter says so.
- **Settlement rule**: at expiry (issued date plus horizon), the editor settles each ledger entry as hit or miss
  (`python3 scripts/ledger.py settle <id> hit|miss --evidence '...' --lesson '...'`). Nothing settles automatically.
  If the falsification condition triggers early, settle early. `too_early` is available only before expiry; after expiry it may not be used.
  Unsettled calls show as "pending settlement" in the track record. **Never leave a call silently unsettled**, and never suspend settlement because no updated version has been issued.
- Still state that this is an **analytical judgment, not a buy or sell order**.
- **The target price comes from the value bridge** (since 1.1.0, `investigative.md` section 1). Each of up to three
  outcomes is one sentence of trigger plus a per-share value. Every per-share conversion states the share count basis
  (cover-page count and date), tax rate, discount rate and timing convention, and **all scenarios use one timing
  convention** (one timing function in `calc/model.py`). Otherwise the higher scenario is overstated: recomputing one
  published report under its own assumptions, its higher scenario discounted "year three" over two periods and its lower
  scenario over three, which put the higher figure about a tenth too high.

---

## 5. The decision chapter's four required items: an average cannot size a position

A probability-weighted target price is an average. "+20% target with a −50% tail" and "+20% with a −8% tail" are two completely different trades,
and they have the same weighted target. **The output of Step 7 is not one number. It is the four items below**,
embedded in the decision chapter. The decision chapter's format is the five operating-research items in `references/quality-bar.md`, "Decision chapter"
(scenario-to-action map / entry and invalidation conditions / comparison of ways to express the view / position and risk-budget framework / review cadence).
The four items below appear inside that chapter, and each appears **once only**. The information is unchanged from the earlier "decision four-pack"; only the format changed.

1. **The price in each of the three scenarios** (bull / base / bear), plus the **trigger condition** of each scenario.
2. **Risk-reward ratio** = upside ÷ downside.
3. **The price at which the thesis fails.** A fall to this price means **the thesis is wrong**, not that the stock "got cheaper".
   State which fundamental assumption breaks at that price.
4. **Expected time to realisation.**

The target price itself needs at least **two independent paths** (the estimation discipline in `references/quality-bar.md`).
If the two differ by more than 20%, attribute the difference. Put the derivation in Appendix D.

**The valuation section also needs four mandatory disclosures** (often skipped, yet they are the biggest lever for long-duration assets):
- The make-up of WACC or the discount rate, and **the effect on the target price of ±1%**.
- **Terminal value as a percentage of valuation.** A model with terminal value above 70% is decided mainly by assumptions, not analysis, and must carry a prominent warning.
- **One sentence of basis for each scenario probability.**
- **Funding sources and target-date assets must come from one set of books.** The funding source of a capital commitment (cash on hand, committed drawdowns,
  new debt and equity) and the net debt and share count at the target date must come from the same period-by-period cash ledger.
  The same cash may not serve both as a funding source and as an asset held on the target date. Breaking this rule is a blocker-level error,
  and fixing it can change the rating.

Warning: **no guessed probabilities.** A probability may come from only three sources: (1) historical frequency (the historical occurrence rate of comparable cases, with the sample stated);
(2) market-implied values (back-solved from options or spreads); (3) explicit subjective assignment. For (3), write "subjective assignment, based on ..."
and run a probability ±10pp sensitivity. **Defaulting to 25/50/25 counts as violating the hard rule "do not present a derived value as a measured one".**

**Consistency test (mandatory)**: the probability-weighted result of the three scenarios must be reconciled line by line against the **market-implied expectations** back-solved in section 1.
The one or two lines with the largest gap are this report's view. Put them in the summary.

---

## 6. Evidence strength binds conclusion strength

Evidence grades [A]-[D] that only require "labelling" are not enough. Under the old rule, a "Buy" rating could have a load-bearing chain of all [C]
or even [D], and still comply as long as each was honestly labelled. **The binding rule:**

1. Identify the **load-bearing chain** of each core conclusion: the 3-5 key numbers that hold it up.
2. The load-bearing chain **may not contain [D]**.
3. If it contains [C], run a **±30% sensitivity** on that number and show the conclusion does not flip. If it flips, the conclusion is **downgraded to "Observation"**.
4. On the summary page, mark each core conclusion with an **evidence strength** = the grade of the **weakest link** in its load-bearing chain.

---

## 7. Settlement of the prior report: make "falsifiable" a promise that gets kept

A falsifiable commitment that is never settled is no commitment. **A track record is the strongest evidence a reader can have that the claims were meant seriously,
and the only asset that lets a reader check a publisher with no institutional reputation behind it.**

**When updating an existing report, add a mandatory chapter "Settlement of the previous version":**

| Previous conclusion | What was observed | Verdict | Note |
|---|---|---|---|
| (one row per conclusion) | (facts + source) | Hit / Falsified / Open / Too early | What was corrected this time and why |

**Maintain a cumulative track record at series level**: total conclusions / hit rate / average time to realisation.
How it is done (already implemented, do not rebuild):
- The ledger is `research/ledger.json`, operated with `scripts/ledger.py` (`add`, `settle`, `list`, `stats`).
- Any public display of the track record must show every call, state the method, and carry the line "past performance does not indicate future results".

**Settlement is a manual act, with no automatic settlement** (the settlement rule in section 4), but **discovery is automatic**:
every day `scripts/desk.py run` matches new filings from the coverage list to falsification conditions, computes price conditions and mark-to-market,
and lists overdue calls and outlooks (written to `research/desk/<date>.md`). Every settlement carries a lesson (`--lesson`),
which is appended to `research/lessons.md`. Read that file before starting the next report.
- Before each release (new report or updated version), run `python3 scripts/ledger.py list`. Every entry whose issued date plus horizon has passed and that is still
  pending or too_early is settled as hit or miss in this release. Never suspend settlement because no updated version has been issued.
  Unsettled entries show as "pending settlement" in the track record where readers can see them. Silent non-settlement is cherry-picking.
- Enter the conclusion text verbatim. Never rewrite it afterwards. **Voiding and re-registering must be an auditable mechanism, not deleting a row**:
  keep the original row, mark the outcome void, record the reason and the new id in the note, and show voided rows together with the reason in any public display.
  `python3 scripts/ledger.py void ID --reason '...'` does exactly this: the row stays, its outcome becomes void, and
  the reason is kept; register the corrected call with `ledger.py add`. There is no delete command.

Warning: once a track record is public, it falls under the rules for **performance advertising**. So it must be **shown in full** (no selection),
state the period covered and the method of judging, and always carry "past performance does not indicate future results".

---

## 8. The degrade path for "must answer" items (general rule)

Some of the "must answer" items in the three process files cannot be found with free data at all
(sell-side consensus, unit-economics cohorts, second- and third-tier supplier relationships).
**Forcing an answer to a question that cannot be researched produces only compliant nonsense.** So the rule is uniform:

> Every "must answer" actually means "**you must determine availability, and record the result**".

Three tiers:

| Determination | Action |
|---|---|
| **Available** | Do it properly and cite the source |
| **Partly available** | Make a directional estimate; **mark every derived cell "est."**, and **it may never be an input to the valuation chapter** |
| **Not available** | Do not build the table. Do the available alternative analysis, and write in "Known limitations": "this report did not build X because Y" |

**Standing entries in "Known limitations"** (present in every report, omitted for no case):
- This report has no primary channel research (no management interviews, no expert network, no site visits).
- Part of the positioning structure is invisible: OTC swaps, non-US holdings, derivative direction, dark-pool trades.
- How the report was produced and reviewed, and the publisher's regulatory status: state this exactly as in the template in `assets/disclaimer.md`.
  The body may not carry a different version. The appendix uses the full text of `assets/disclaimer.md`, and the two places may not diverge.

---

## 9. Pre-release final check

Write the final check to `research/<slug>/checks.md`, one result per item: **passed / fixed / n/a**.
"Fixed" and "n/a" must carry one sentence (what was changed and why, or why the item does not apply). A tick with no note counts as unchecked.
The point is that the result can be verified, and afterwards you can trace which item let an error through.

- [ ] Which level of method from section 1 was used for consensus? Is it stated in the report?
- [ ] Does every mismatch point carry E1-E5 evidence? Have those without it been downgraded to "Observation"?
- [ ] Is the catalyst path table complete? Is a conclusion with no catalyst in 12 months marked "structural view" on the summary?
- [ ] Does the annual-horizon rating state the **benchmark (with the reason for choosing it) + start date + 12 months**? Are benchmarks consistent across versions of the series?
- [ ] Do the three-horizon outlook (monthly / quarterly / annual) and the migration-conditions box appear once in chapter 1, and once only in the whole text?
- [ ] Is the decision chapter in the five-item operating-research format, with the four items (three-scenario prices / risk-reward ratio / thesis-failure price / time to realisation) each appearing once inside it?
- [ ] Does the target price have two independent paths, and is any difference above 20% attributed?
- [ ] Are the four valuation disclosures made: WACC sensitivity, terminal-value share, basis for probabilities, and funding sources and target-date assets from one set of books?
- [ ] Has the probability-weighted result been reconciled against market-implied expectations, and the lines that differ written into the summary?
- [ ] Is there no [D] in any core conclusion's load-bearing chain, and has every chain with [C] had the ±30% sensitivity?
- [ ] Does each core conclusion on the summary page carry an evidence strength?
- [ ] (Updated versions) Is the "Settlement of the previous version" chapter written? Have all due entries in the ledger been settled, with none left silently open?
- [ ] Does "Known limitations" contain the three standing entries, with the production-and-review entry matching `assets/disclaimer.md`?
- [ ] Were the `assets/disclaimer.md` template and its conflict-of-interest items used as written, each item stated (including "none")?
- [ ] **no-lookahead**: does the body use no filing made after the filing cut-off and no market data after the reference date? Does the rating's settlement window start from the release-date close?
- [ ] **quote-fresh**: is the market reference date a closed trading day (not an intraday price; before 16:30 US Eastern the same day does not count), and do two sources agree?
- [ ] **earnings-date**: is the next earnings date in the summary? If fewer than 10 trading days lie between release and the next earnings date, does the summary say "the figures in this version may be updated on day X"?
- [ ] **opposite-answered**: when the rating is not Neutral, are the top three points of the opposing side (`debate-*.md`) answered one by one in the body, with any that cannot be answered moved into Known limitations?
- [ ] **desk-registered**: after ledger entries are registered, has the series been added to `research/watch.json`, and does `python3 scripts/desk.py check` return 0?
