# Metering — Usage Billing, Overage, Credits and Commitments

Scope: counting what gets billed and turning it into a defensible invoice. Enforcing plan limits is `entitlements.md`; the cost side of usage is `margins.md`; writing the payment integration is `billing`.

**Before designing or changing a meter**, read `## Plans` in `~/Clawic/data/saas/memory.md` (or `plans.md`) for the current value metric and included allowances, and `## Commitments` for any customer with a negotiated rate or floor.

## The Meter Is a Ledger, Not a Counter

A counter that increments is unauditable: when a customer disputes an invoice — and with usage billing they will — the only acceptable answer is an itemized list they can reconcile against their own logs.

```
usage_event: { id, account_id, meter, quantity, unit, occurred_at, recorded_at, idempotency_key, metadata }
```

- **Idempotency key per event, deduplicated at write.** Retries are guaranteed — client retries, queue redelivery, replays after an incident — and a double-billed customer costs more trust than the revenue is worth.
- **Store `occurred_at` and `recorded_at` separately.** Late-arriving events are normal; the difference between them is what decides whether an event lands in the closed period or the next one.
- **Raw events are the source of truth; aggregates are a cache.** Aggregate for dashboards and invoices, but keep the events long enough to rebuild any invoice in the dispute window — a year is the practical floor, and longer if the contract says so.
- **Never meter from application logs.** Logs are sampled, rotated and lossy. Metering is a first-class write path with the same reliability requirements as the write it measures.
- **Cap per-account ingestion.** A customer bug that emits a million events a second is your infrastructure bill and your invoice-dispute call.

## Choosing the Aggregation

| Aggregation | Bills for | Right when |
|---|---|---|
| Sum | Total quantity in the period | Events, tokens, jobs, GB transferred |
| Max | Peak in the period | Provisioned capacity, concurrent users |
| Last value | Value at period end | Storage, seats, records |
| Unique count | Distinct entities seen | Monthly active users, tracked contacts |
| Time-weighted average | Quantity × duration | Storage held for part of the month, running instances |

Storage billed with `last value` versus `time-weighted average` differs by the whole shape of the month for a customer who uploads on the 28th. Pick one, publish it, and never change it silently — a change of aggregation is a price change (`plan-changes.md`).

## Cutoff and Late Events

Define the closing rule and put it in `## Definitions`:

- **Grace for late arrivals**: events with `occurred_at` in the closed period but `recorded_at` after the cutoff are accepted for a bounded window — commonly a day or two — then billed in the next period as a clearly labelled adjustment line.
- **Never restate a sent invoice.** Corrections go on the next invoice as an adjustment with the reason. A reissued invoice breaks the customer's own accounting reconciliation.
- **Time zone is the customer's contracted one**, stated on the invoice. Metering in UTC and invoicing in local time misplaces every event at the month boundary.

## Commitments, Drawdown and Overage

The structure most enterprise usage contracts converge on: a committed amount, paid up front or in instalments, drawn down by usage, with overage billed at a stated rate.

- **Drawdown order**: expiring credits first, then promotional credits, then the paid commitment, then overage. Publish the order — a customer who watches promotional credit expire unused while their paid balance is drawn will assume it was deliberate.
- **Overage rate above the commitment rate**, typically by a meaningful multiple, because the commitment is what bought the discount. Same rate for overage means the commitment bought nothing and nobody will commit again.
- **Rollover**: unused commitment expiring at period end is standard and resented. A capped rollover — a fraction of the commitment, valid one period — buys goodwill at limited cost and makes renewal easier (`renewals.md`).
- **True-forward, not true-up, on the renewal**: a customer who exceeded their commitment all year renews at the higher level rather than receiving a retroactive bill. It is the same money, arriving without an argument.
- **Only the committed floor is ARR.** Overage above it is revenue, not recurring revenue, and reporting it inside ARR is the first thing diligence strips out (`revenue.md`, `diligence.md`).

## Making the Bill Predictable

Unpredictability, not price, is what kills usage-based models inside the customer's organization — the buyer has to defend a number they cannot forecast.

- **Live usage in the product**, not only on the invoice: current period consumption, projected end-of-period total, and the point at which the next charge starts.
- **Customer-set budget alerts** at their own thresholds, plus a default at the point where the bill exceeds the last one by a meaningful margin.
- **Optional hard cap.** Some buyers need a spend ceiling more than they need continuity; offering it wins deals and prevents the worst kind of invoice dispute. Make the consequence of hitting it explicit.
- **Anomaly detection on your side**: a 10× jump against the account's own trailing average is either a customer bug or your bug, and reaching out before the invoice does converts a dispute into goodwill.
- **Invoice line items in the customer's language** — "12,400 workflow runs" — not internal meter names.

## Credits and Disputes

- Issue credits as a balance against future invoices rather than as refunds where the contract allows: it preserves cash and recognized revenue, and it retains the customer relationship.
- Every credit gets a reason code and lands in the revenue record — SLA breach (`incidents/<year>.md`), goodwill, billing error, or negotiated. Credits with no reason code make gross margin unexplainable at close.
- A billing error found on your side is disclosed and credited before the customer notices. The alternative is discovered eventually, and then it is a trust problem across the whole book.
- Set a dispute window in the terms — commonly a bounded number of days after invoice — and keep raw events at least that long plus a margin.

## AI and Per-Request Cost

Where per-request model cost dominates, metering is not just billing — it is the margin control (`margins.md`).

- Meter the unit the customer understands (a document processed, a workflow run) while recording the underlying cost driver (tokens, model, latency tier) in `metadata`. Billing on raw tokens exports your vendor's pricing model to your customer and re-prices your product every time the vendor changes.
- Keep a published conversion if you sell credits: opaque credit systems generate constant tickets and read as a way to hide a price increase.
- Set a per-account and per-request cost ceiling in code. An unbounded retry loop against a paid model is a cost incident with no revenue attached.
- Re-check the realized margin per meter monthly, and treat a meter below `gross_margin_floor_pct` as a pricing problem (SKILL.md Rule 6).

**After designing or changing a meter, an aggregation, a rate or a commitment structure**, write the change to `## Plans`, any negotiated rate or floor to `## Commitments`, and the design itself — aggregation, cutoff rule, drawdown order, the numbers behind the rate — to `artifacts/<kebab-name>.md` with its `## Boxes` line, in the same turn (`memory-template.md`). Every future invoice dispute is settled by reading that file.
