# Revenue — MRR, ARR, and Making the Numbers Tie

**Contents:** [The Movement Bridge](#the-movement-bridge) · [Bucketing Rules That Decide Everything](#bucketing-rules-that-decide-everything) · [Computing It From Subscription Events](#computing-it-from-subscription-events) · [What Counts as ARR](#what-counts-as-arr) · [Bookings, Billings, Revenue, Cash](#bookings-billings-revenue-cash) · [Deferred Revenue](#deferred-revenue) · [Cohorts and the Retention Curve](#cohorts-and-the-retention-curve) · [Why Two Dashboards Disagree](#why-two-dashboards-disagree)

**Before stating any number**, read `## Definitions` and `## Revenue` in `~/Clawic/data/saas/memory.md` — or `definitions.md` / `mrr-log.md` if the `## Boxes` index points there. A current-month figure with no prior months and no definition is not an answer.

## The Movement Bridge

```
End MRR = Start MRR + New + Expansion + Reactivation − Contraction − Churn
```

**Sign convention, fixed for the whole skill: all six buckets are positive magnitudes.** The identity supplies the signs, so contraction and churn are stored and reported as the size of the loss — `1,200`, never `-1,200`. Worked, from the 2026-06 row of `## Revenue`: `78,400 + 6,100 + 2,900 + 300 − 1,200 − 3,300 = 83,200`. A source that hands you signed buckets (most billing exports do) gets its signs stripped before the row is written, not after the total is computed.

Every dollar of month-over-month delta lands in exactly one bucket. The bridge is not a report — it is the check that the report is real. If it does not close to zero, the gap is the finding, and the total is not published until it does.

| Bucket | Definition | The mistake |
|---|---|---|
| New | First paid subscription of an account that has never paid | Counting a returning account as new inflates both New and Churn |
| Expansion | More MRR from an account that was already paying: seats, tier up, overage that became recurring | Counting a one-off overage spike as expansion, then reporting churn next month |
| Reactivation | An account that had fully churned starts paying again | Frequently merged into New; it hides how much of growth is recycling old logos |
| Contraction | Same account, less MRR: seats down, tier down, discount granted | Recording a downgrade as churn + new destroys both retention numbers |
| Churn | Account goes to zero MRR | Counting the cancellation request date instead of the subscription end date shifts churn a month |

The identity fails, in practice, for four reasons: currency conversion applied at different dates on the two sides, mid-month proration credited but not bucketed, a plan price change applied retroactively, and test or internal accounts included in one query and not the other. Check those four before suspecting the data.

## Bucketing Rules That Decide Everything

Write the chosen rule into `## Definitions` once; the choice matters far less than the consistency.

- **Cancel-then-return inside the same month**: a wash. Do not record churn and reactivation for the same account in the same period — it doubles both retention denominators.
- **Downgrade to a free plan**: churn, because MRR reached zero. Log it as `voluntary` with the reason, and keep the account in `## Accounts` — free users convert at a higher rate than strangers.
- **Trial that never converts**: not churn. It never had MRR. A trial funnel that leaks looks like a churn problem only if trials are counted as customers (`trials.md`).
- **Annual contract, mid-term seat addition**: expansion in the month the seats start billing, at the monthly-equivalent rate — not the full prepaid amount.
- **Annual contract non-renewal**: churn in the month the term ends, not the month notice was given. Notice date belongs in `## Accounts` as a renewal risk, not in the bridge.
- **Usage overage**: expansion only if the account's committed floor rose. Variable overage above an unchanged commit is revenue but not recurring — report it as a separate line (`metering.md`).
- **Currency**: convert at a fixed monthly rate and state it. Converting each transaction at its own spot rate makes NRR move when nothing happened.

## Computing It From Subscription Events

The subscription state at two month-ends, joined on account, produces every bucket:

```sql
WITH m AS (
  SELECT account_id,
         SUM(CASE WHEN month = '2026-06-01' THEN mrr ELSE 0 END) AS prev,
         SUM(CASE WHEN month = '2026-07-01' THEN mrr ELSE 0 END) AS curr
  FROM monthly_account_mrr
  WHERE month IN ('2026-06-01','2026-07-01')
  GROUP BY account_id
)
SELECT
  SUM(CASE WHEN prev = 0 AND curr > 0 AND first_paid_month = '2026-07-01' THEN curr END) AS new_mrr,
  SUM(CASE WHEN prev = 0 AND curr > 0 AND first_paid_month < '2026-07-01' THEN curr END) AS reactivation,
  SUM(CASE WHEN prev > 0 AND curr > prev THEN curr - prev END) AS expansion,
  SUM(CASE WHEN prev > 0 AND curr > 0 AND curr < prev THEN prev - curr END) AS contraction,
  SUM(CASE WHEN prev > 0 AND curr = 0 THEN prev END) AS churn
FROM m LEFT JOIN accounts USING (account_id);
```

`contraction` and `churn` are written `prev - curr` and `prev` so the query returns positive magnitudes: its output plugs straight into the identity above with no sign flipping in between.

Two details that make this correct rather than approximately correct: `monthly_account_mrr` must be normalized monthly recurring value (an annual contract divided by 12, not the invoice), and `first_paid_month` must be stored per account rather than derived from the earliest row in the current query window, or every reactivation older than the window is misread as new.

## What Counts as ARR

Recurring, committed, annualized. The strict test: would this money arrive next year without a new sales decision?

| Include | Exclude |
|---|---|
| Monthly and annual subscription fees | Onboarding, implementation, migration and training fees |
| Committed minimums on a usage contract | Usage above the commitment, unless it has a stable floor reported separately |
| Contracted support or premium-SLA fees | Hardware, resold licences, and pass-through costs |
| Multi-year contracts, at the annualized rate | The full multi-year contract value (that is TCV, a different number) |
| Recurring add-ons | Non-recurring professional services, however profitable |

`ARR = MRR × 12` is correct only when every contract is normalized to monthly first. Annualizing a strong month — or summing annual contract values signed in a year — produces a number that diligence will restate downward, and the restated figure is the one everyone remembers (`diligence.md`).

## Bookings, Billings, Revenue, Cash

Four numbers that are all correct and all different. Confusing them is the most common way a board deck fails to tie to the model.

| Number | What it measures | When it moves |
|---|---|---|
| Bookings | Contract value signed | Signature date, for the whole term |
| Billings | Invoices issued | Invoice date, per billing schedule |
| Revenue | Service delivered, recognized ratably | Every month of the term |
| Cash | Money received | Payment date, minus fees |

A single 24k annual contract signed 1 July, paid up front: bookings 24k in July, billings 24k in July, revenue 2k per month for twelve months, cash ~23.3k in July after processing fees. MRR is 2k. Anyone quoting 24k as July's MRR has just made the next twelve months look like a collapse.

## Deferred Revenue

Cash received for service not yet delivered is a liability. Annual prepay is the cheapest financing a SaaS business has, and the one that most often flatters a dashboard.

- Deferred balance rises with each prepaid contract and unwinds monthly. A quarter of strong annual sales grows cash and deferred revenue together; revenue growth lags.
- The ratio that matters when annual prepay is pushed hard: `deferred balance ÷ monthly revenue` is roughly how many months of already-collected obligation exist. Rising fast means the cash position is borrowed from future months.
- A refund on an annual prepay hits cash immediately and reverses several months of recognized revenue at once — which is why refund policy is a revenue decision, not a support decision (`renewals.md`).

## Cohorts and the Retention Curve

- Group by signup month, track the cohort's total MRR as a percentage of its month-0 MRR. The curve flattening above zero is the whole business: a cohort that stabilizes at 80% has a durable base, one that keeps declining has no floor and LTV is not defined.
- With expansion, a cohort curve can exceed 100% — that is NRR above 100 made visible, and it is the only honest way to show it.
- Choose calendar-month or anniversary cohorts once and record the choice in `## Definitions`. Mixing them makes month-12 retention look ~half a month better or worse depending on signup timing.
- Minimum readable cohort: enough accounts that one departure does not move the line more than a couple of points — below roughly 30 accounts, report the curve with its count next to it and resist drawing conclusions.

## Why Two Dashboards Disagree

Run this list before rebuilding anything.

| Cause | Tell |
|---|---|
| Different churn timing (request date vs term end) | Totals match, monthly attribution is shifted by one month |
| Test, internal or comped accounts included on one side | Constant small offset in every month |
| Discounts applied to list price on one side, realized on the other | Gap scales with discount volume, appears after a big deal |
| Annual contracts counted at invoice value | One side spikes in the signing month |
| Currency converted at different dates | Gap moves with the exchange rate, not with the business |
| Refunds and credits netted in one place only | Gap appears in months following an incident (`incidents/<year>.md`) |
| One side excludes accounts in dunning, the other does not | Gap tracks failed-payment volume (`dunning.md`) |

**After computing any month's movement or a metric**, write the row to `## Revenue` in the same turn with its as-of date, its currency and whether the month is closed, and any definition you had to settle into `## Definitions` with the date it changed (`memory-template.md`). A number recomputed next quarter from a query nobody saved is a new number, not the same one.
