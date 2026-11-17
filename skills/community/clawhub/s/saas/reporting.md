# Reporting — The Close, the Set, and the Board Pack

Scope: producing the numbers on a cadence, in a form that survives being read next quarter. The definitions and the movement bridge are `revenue.md`; the company financial model, forecast and fundraise narrative are `cfo`.

**Before any reporting run**, read `## Definitions` and `## Revenue` in `~/Clawic/data/saas/memory.md` (or `definitions.md` / `mrr-log.md`) and check `## Due` against today's date. A reporting pack whose definitions differ from last month's is not a comparison, and the difference is invisible to everyone reading it.

## The Monthly Close

A close is a procedure, not a query. Run it in this order; each step depends on the previous one.

| Step | What | Why the order matters |
|---|---|---|
| 1 | Freeze the period: no more events accepted into it after the cutoff (`metering.md`) | Everything after this assumes a stable dataset |
| 2 | Reconcile subscriptions against the billing provider: active, past due, cancelled, paused | Product state and billing state drift; the gap is the finding |
| 3 | Resolve accounts still in dunning — recovered, suspended, churned (`dunning.md`) | Their classification changes both churn buckets |
| 4 | Compute the movement bridge and confirm it closes | The total is not publishable until it does (SKILL.md Rule 2) |
| 5 | Compute the metric set from the bridge | Metrics computed independently of the bridge will disagree with it |
| 6 | Allocate COGS and compute gross margin (`margins.md`) | Needed before CAC payback, which is margin-adjusted |
| 7 | Write the row: numbers, currency, as-of date, closed flag | The record is the deliverable, not the chart |
| 8 | Write the one-paragraph narrative: what moved, why, what it implies | A number with no explanation is re-explained differently by each reader |

Close within the first working week if the data allows it. A number produced three weeks after month end informs nothing, because the decision it should have driven has already been made.

## The Standing Set

Same metrics, same definitions, same order, every period. Consistency is worth more than completeness: a set that changes shape cannot be trended, and trend is the entire purpose.

| Always | Monthly or quarterly | Only when relevant |
|---|---|---|
| MRR / ARR and the movement bridge | NRR and GRR | Segment splits (by plan, size, geography, cohort) |
| New, expansion, reactivation, contraction, churn | Gross margin | Magic number and quick ratio |
| Logo and revenue churn, split voluntary / involuntary | CAC and CAC payback | Burn multiple and rule of 40 |
| Customer count by plan | Cohort retention curve | Per-meter margin (`metering.md`) |
| Cash and runway (from `cfo`) | Rule of 40 where growth and margin are both meaningful | Pipeline and win rate where a sales motion exists |

Two rules that prevent most arguments: **a month-to-date number is never compared against a closed month**, and **every number carries its currency and its as-of date** (SKILL.md Rule 1).

## Reading the Set

The value is in the combinations, not the individual numbers.

| Pattern | Reading |
|---|---|
| Growth strong, NRR under 100% | Growth is bought entirely with new logos; CAC efficiency decides how long that lasts (`expansion.md`) |
| NRR strong, new logos weak | The product works and the top of funnel does not — a `growth` problem, not a retention one |
| GRR strong, NRR flat | Nothing leaks, nothing expands: a packaging problem, because the fences give no reason to grow (`packaging.md`) |
| Logo churn high, revenue churn low | The small end leaves; often fine, and sometimes an argument to raise the entry price (`pricing`) |
| Revenue churn high, logo churn low | A few large accounts are shrinking — the most dangerous shape, because the count looks healthy |
| CAC payback lengthening, win rate flat | Price or mix moved, not sales performance |
| Gross margin falling while revenue grows | Cost to serve scales with usage and the price does not (`margins.md`) |
| Burn multiple rising while growth holds | Growth is being bought at a worsening rate; the rate, not the growth, is the finding |

## The Board or Investor Pack

Fifteen slides that answer four questions: where are we, what changed, what did we learn, what do we need. The full narrative, forecast and ask are `cfo`; what belongs here is the SaaS operating content.

- **Open with the headline set** — ARR, growth, NRR, burn multiple, runway — against last period and against the plan. Every subsequent slide explains one of those.
- **Show the bridge**, not just the total. A board that sees new, expansion, contraction and churn separately asks better questions and stops requesting a breakdown every meeting.
- **Same slide order every time.** Reordering to flatter a bad month is noticed, and it costs credibility that takes several good months to rebuild.
- **State the definition of anything unusual on the slide itself**, especially ARR treatment of usage revenue (`revenue.md`).
- **One slide of what did not work** and what was learned. Its absence is read as either nothing was tried or nothing is being disclosed.
- **Pre-wire the bad news** before the meeting. A board that learns of a miss in the room spends the meeting on the surprise rather than on the response.
- Restatements are disclosed as restatements, with the old and new numbers side by side and the reason. A silently changed historical figure is the fastest way to lose the room.

## Instrumentation Behind the Numbers

The output is only as good as the event data underneath it, and the failures are always the same handful.

- **One source of truth per metric.** When the product, the billing provider and the warehouse each compute MRR, three numbers exist and every meeting starts with reconciliation (`revenue.md`).
- **Events named and versioned**, with a schema. Renaming an event breaks every historical comparison silently.
- **Account id on every event**, always resolvable to a paying account. Metrics that cannot be joined to revenue cannot answer any commercial question.
- **Exclude internal, test and comped accounts consistently** — in every query, defined once. This is the single most common cause of two dashboards disagreeing.
- **Backfill discipline**: a corrected historical figure is noted with its date and reason in `## Definitions`, never overwritten silently.

## Cadence

| Cadence | Work |
|---|---|
| Weekly | New, churn, trials started and converted, failed payments in flight; a short list, five minutes, no pack |
| Monthly | Full close, movement bridge, metric set, gross margin, narrative, board or investor update |
| Quarterly | Cohort curves, segment margin, health-score validation, discount and realized-ARPA review, packaging check |
| Annually | Pricing and packaging review, benchmark comparison, definition audit, tax and compliance registrations (`compliance.md`) |

Every one of these is a row in `## Due` with its last-run date. A cadence with no recorded last run is skipped for two quarters, and the first person to notice is usually an investor.

**After every close or pack**, write the period's row to `## Revenue` with all buckets, the metric set, its currency, its as-of date and whether the month is closed; update `## Due` with the run date; and record any definition that had to be settled in `## Definitions` with the date it changed (`memory-template.md`). A board narrative structure worth reusing — the shape, not the numbers — belongs in `artifacts/<kebab-name>.md` with its `## Boxes` line.
