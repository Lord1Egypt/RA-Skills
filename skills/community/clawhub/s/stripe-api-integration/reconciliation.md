# Reconciliation — Payouts, Fees, and Making the Bank Match

**Read `## Volume & Fees` in `~/Clawic/data/stripe-api-integration/memory.md`** (or its box) before answering any money question: a current-month number with no prior months is not an answer, and the effective rate only means something as a series.

**Contents:** [Three Ledgers, Not One](#three-ledgers-not-one) · [The Balance Transaction Is the Unit of Truth](#the-balance-transaction-is-the-unit-of-truth) · [Why the Payout Is Smaller Than Your Charges](#why-the-payout-is-smaller-than-your-charges) · [The Monthly Procedure](#the-monthly-procedure) · [Multi-Currency Settlement](#multi-currency-settlement) · [Payout Timing and Cash Flow](#payout-timing-and-cash-flow) · [A Payout Did Not Arrive](#a-payout-did-not-arrive) · [Feeding an Accounting System](#feeding-an-accounting-system) · [Connect Reconciliation](#connect-reconciliation)

## Three Ledgers, Not One

| Ledger | What it says | When it is right |
|---|---|---|
| Your database | What you believe you sold | Only if every webhook was handled |
| Stripe balance | What Stripe holds and why, net of everything | Always — it is the settlement record |
| Bank account | What arrived | Always, and late |

Reconciliation is proving the three agree. The direction is fixed: the bank confirms the payout, the payout is explained by balance transactions, and the balance transactions are matched to your records — never the reverse, because your database cannot tell you about money it never learned existed.

## The Balance Transaction Is the Unit of Truth

Every movement — charge, refund, dispute withdrawal, dispute reversal, transfer, application fee, payout, adjustment — has a balance transaction carrying `amount`, `fee`, `net`, `currency` and `available_on`.

- **Only here do fees exist.** A charge object shows what the customer paid; the balance transaction shows what you keep. Summing charges and calling it revenue overstates by the entire fee stack.
- `fee_details` breaks the fee into its parts — processing, application fee, tax on the fee where it applies. That is the breakdown that answers "why is our rate 3.3% when the headline says 2.9%".
- `available_on` is when the money becomes payable, and it is what groups transactions into a payout — not `created`.
- The payout object links to its transactions, which is how you go from a single line on the bank statement to the hundreds of movements that produced it.
- For high volume, the Reporting API produces itemized files per payout instead of paging the API; that is the input finance actually wants.

## Why the Payout Is Smaller Than Your Charges

| Deduction | Notes |
|---|---|
| Processing fees | Percentage plus fixed per successful charge; the fixed part dominates small tickets |
| Cross-border and currency conversion | An extra percentage when the card's country or currency differs from yours |
| Refunds | The refunded amount leaves; the original fee generally does not come back |
| Disputes | The amount plus a per-dispute fee, withdrawn on filing and returned only in part if you win |
| Product add-ons | Billing, Tax, Radar for Fraud Teams and similar, billed against the balance |
| Connect transfers and application fees | Money routed to connected accounts never reaches your bank (`connect.md`) |
| Reserves and holds | New or risk-flagged accounts may have a rolling reserve — money earned, not yet payable |
| Payout failures and returns | A failed bank transfer returns to the balance and looks like a missing payout |
| Negative balance carry | A month with more refunds than sales deducts from the next payout |

`effective_rate = total_fees ÷ gross_volume` for the month. Tracking that single number per month is what makes fee drift visible; a change means the customer mix, the method mix or the add-on stack moved.

## The Monthly Procedure

Run it on `reconciliation_day` from `config.yaml`; the `## Due` row carries the date.

1. List payouts for the period with their status and arrival dates.
2. For each payout, pull its balance transactions and sum `net`. The sum equals the payout amount, or something above is missing.
3. Total gross, fees, refunds and dispute movements for the period. Compute the effective rate.
4. Match gross against your own order records by `metadata[order_id]`. Investigate both directions: charges with no order (a flow you did not know about) and orders with no charge (a fulfillment you gave away).
5. Check tax collected against what the tax reports say is owed — collected tax is not revenue (`tax.md`).
6. Check the closing balance, including any reserve, and note whether it moved for a reason.
7. Write the month's row into `## Volume & Fees` with the currency and the `As of` date.

A discrepancy that survives step 4 is an incident, not a rounding issue: it means events were missed or a flow charges outside your system.

## Multi-Currency Settlement

- **Presentment** is what the customer pays in; **settlement** is what your balance holds. Selling in a currency you do not settle in triggers a conversion with a spread, applied at payout.
- Where the account supports holding multiple currency balances, holding what you sell avoids the round trip — at the cost of managing several balances and several payout schedules.
- Book revenue at the rate on the transaction date, not the payout date. The difference between the two is an FX gain or loss, and it belongs in its own accounting line rather than silently inside revenue.
- Never mix currencies in a total. Every stored amount carries its currency (`memory-template.md`), for exactly this reason.

## Payout Timing and Cash Flow

- Standard payouts run on a rolling schedule — money becomes available a couple of business days after settlement in mature markets, longer in others, and the schedule can be set to daily, weekly or monthly.
- The first payout on a new account takes substantially longer, commonly one to two weeks, while the account is reviewed. Plan launch cash flow around that, not around the steady-state schedule.
- Instant payouts cost a percentage of the amount. That is a financing decision with a real rate, not a convenience toggle.
- A manual payout schedule gives control of when money moves and requires someone to actually move it.
- Weekends and bank holidays shift arrival dates; "not arrived" on a Sunday is usually a calendar, not a problem.

## A Payout Did Not Arrive

1. Check the payout's status and its stated arrival date — pending, in transit, paid, or failed.
2. `failed` carries a failure code: closed account, wrong details, rejected by the bank. Fix the bank details and the balance stays yours.
3. Check whether the balance is negative or reserved — with nothing payable there is nothing to pay out.
4. Check for an account-level hold: verification requirements, a restriction, or an ownership change all pause payouts.
5. Confirm the schedule was not changed to manual by someone tidying settings.
6. Only then escalate to Stripe with the payout id (`debug.md`).

## Feeding an Accounting System

- Export per payout, not per charge: the bank statement has one line, and the accounting entry should reconcile to it.
- The minimum useful mapping: gross revenue, refunds as a contra-revenue, fees as an expense, tax collected as a liability, disputes as their own line, payouts as a bank transfer. Netting fees into revenue is the most common error and it understates both revenue and costs.
- Revenue recognition for subscriptions is not cash: a year paid upfront is deferred revenue recognized monthly. Stripe's Revenue Recognition product does this, and it is a paid add-on — the line belongs in `~/Clawic/data/finances/subscriptions.md`.
- Sigma runs SQL over the account's data for analyses the API makes painful; it is also priced, and it is for analysis, never for the request path.

## Connect Reconciliation

- Platform and connected accounts have separate balances and separate payouts. Reconcile them separately, then reconcile the transfers that connect them.
- Application fees are platform revenue and appear as their own balance transactions on the platform side.
- With destination charges, the funds pass through the platform balance; with direct charges they never do — which is why the charge-type decision shows up here as two completely different sets of books (`connect.md`).
- A negative balance on a connected account, from refunds or disputes after payout, is a real receivable. Decide who absorbs it before it happens, not during.

---

**After every reconciliation**, write the month's row into `## Volume & Fees` in `~/Clawic/data/stripe-api-integration/memory.md` — gross, refunds, disputes, fees, net, effective rate, all with currency and the `As of` date — overwriting the row if the month was already recorded, and update the `## Due` row with the date it ran. Establish the payout bank reference and entity in `~/Clawic/data/finances/accounts.md`, and any paid Stripe add-on in `~/Clawic/data/finances/subscriptions.md`, so the numbers a finance skill reads are the same numbers. A procedure that took work to derive is `artifacts/procedure-reconciliation.md` with its `## Boxes` line.
