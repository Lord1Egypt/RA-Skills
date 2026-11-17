# 1. Kickoff: choose the topic and set the terms

> This is step 1 of the pipeline in `SKILL.md`. Next step: `02-research.md`.

- **Type**: `equity` (single company), `industry` (value chain), `macro` (macro or strategy), `quarterly` (quarterly report).
- **Series key** (`report_series`): the ticker for a company (for example `IREN`), a kebab-case topic for a thematic series
  (for example `ai-value-chain`). Every later update of the series reuses the key, and the ledger, the watch file and the
  update chain all hang off it. Decide the boundary of the series now.
- **Report directory**: `research/<report-id>/`, where `<report-id>` is the series key plus a date, such as
  `report-<ticker>-deep-dive-<yyyy-mm>`.
- **Compare candidates** when there are three or more (use `assets/templates/kickoff.md`). Score each candidate 1-10 through
  four lenses: evidence density and verifiability; difference from existing coverage; whether a tradable judgment can be
  made; reader demand and discoverability. **If evidence density or tradable judgment is 4 or lower, the candidate is out.**
  Above that bar, decide on the whole picture and write down "why not the other candidates".
- **Liquidity threshold**: market cap of at least $2 billion and 20-day average daily turnover of at least $20 million. A
  reader cannot act on a report about a stock below the bar. The user may waive it by naming the company.
- **Read the settlement record first**: the last 30 lines of `research/lessons.md` and `research/patterns.md`. In the
  candidate comparison, count how many open ratings share the new candidate's factor exposure. Several underweights on the
  same high-beta theme will all flip in one rally, and the scoreboard then measures one market move. This is one input to
  the choice. It never changes the rule that a rating follows the evidence.
- **Claim and new-facts gate** (`investigative.md` sections 1 and 2). Write three things before anything else, or do not
  start: (1) one falsifiable claim with a per-share impact (a rough figure is fine; state the basis); (2) the value bridge,
  the mechanism that turns facts into money; (3) at least three new facts, each with its text and location (page, section or
  table), why the market missed it, and which input of the bridge it changes. In the candidate comparison, score
  "difference from existing coverage" on the number and weight of new facts. A topic that only re-computes filed numbers
  is not started, however dense its evidence. Add one line on how management is likely to answer the claim, and research
  the facts that answer depends on.
- **The kickoff brief** is `research/<report-id>/notes-00-kickoff.md`. It holds: the verdict and reasons; the data basis
  date at three layers (hard rule 3 in `SKILL.md`); the rating benchmark (default: S&P 500 total return, or a more
  investable index when `judgment.md` section 4 supports one); hard constraints on form (do not repeat the previous
  report's framework); research discipline (the four sentences in `references/agents.md`); and the data plan. The
  initiation memo of Step 0 in `references/equity.md` follows it.

## Deciding not to publish is also an output

A user once asked for an update to an existing report. Three primary-source checks (SEC EDGAR, transaction-level government
contract data, and official investor-relations and trade-press sources) found no 8-Ks in the window. New government
obligations were a rounding error against company guidance. A forced Delta update could only restate what had been published
days earlier. The right call was **do not update**.

Write the reasoning and the restart triggers into the kickoff brief and hand it to the user. That is a deliverable. Before
starting any report, ask one question: does this period contain anything new to write?
