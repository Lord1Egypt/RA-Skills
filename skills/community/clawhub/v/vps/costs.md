# Costs — Where the Money Actually Goes

Read before any spend question, when a bill moves, and on the review cadence in `## Due`. Ratios below are stable; absolute prices are not — verify on the provider's page before quoting. Thresholds scale with `monthly_budget`.

**Before answering any spend question**, read `## Spend` in `~/Clawic/data/vps/memory.md` (or `spend-log.md` if `## Boxes` points there) and `~/Clawic/data/servers/servers.md`. A current-month number with no prior months is not an answer, and a month-to-date figure compared against a closed month is a wrong answer.

**Contents:** [The Plan Price Is Not the Bill](#the-plan-price-is-not-the-bill) · [Diagnosing a Jump](#diagnosing-a-jump) · [Bandwidth](#bandwidth) · [The Waste Sweep](#the-waste-sweep) · [Commitments and Prepay](#commitments-and-prepay) · [Right-Sizing as a Saving](#right-sizing-as-a-saving) · [When a VPS Stops Being the Cheap Option](#when-a-vps-stops-being-the-cheap-option) · [Non-Payment](#non-payment) · [Review Checklist](#review-checklist)

## The Plan Price Is Not the Bill

Six line items beyond the server, in rough order of how often they surprise people:

| Line item | Shape | Control |
|---|---|---|
| Bandwidth overage | Included allowance then a per-unit rate; allowances differ between providers by more than an order of magnitude | Know the allowance, then move heavy traffic to a CDN or object storage |
| Snapshots | Per GB of **disk size** on most platforms, not of data used, and forever | A retention count, pruned on a cadence |
| Backup add-on | Commonly a flat share of the plan price, around a fifth | Worth it as the fast undo; it never satisfies the offsite leg (`backups.md`) |
| IPv4 addresses | Small monthly charge each, attached or not, at nearly every provider since 2024 | Count them; release on teardown (`networking.md`) |
| Block volumes | Per GB, and they survive the instance | Delete with the server, or knowingly keep |
| Managed extras — databases, load balancers, object storage | Each is its own subscription created alongside the server and destroyed separately | The teardown list (`migration.md`) |

Plus the two that are not on any invoice: **servers nobody owns**, and **your time**. The first is the most common finding of a spend review. The second is why a managed service is sometimes the cheap option.

## Diagnosing a Jump

In order, because each step names a different kind of cause:

1. **Compare against the previous closed month**, not against the month-to-date figure. Half of reported bill jumps are a full month being compared with a partial one.
2. **Read the invoice line items**, not the total. The provider breaks it down; the breakdown names the cause.
3. **Which line moved?** Bandwidth, storage, instances, or add-ons. The four have entirely different investigations.
4. **Map the delta to a date**, and map that date to something that happened: a deploy, a new server, a backup job, a scraper, a public link to a large file.
5. **Check for resources created and forgotten** — a test server from three weeks ago, a volume from a migration, a snapshot series with no retention.
6. **Check the exchange rate** if the account bills in a currency other than the user's. A "jump" of a few percent with no usage change is usually this, and it is not a problem to solve.

## Bandwidth

- Almost always **outbound only**. Inbound is typically free everywhere.
- Allowances may pool across all servers in an account or apply per server. Which one changes the fleet's economics: pooled means small boxes share a large budget, per-server means a single busy box overruns while others idle.
- **Private-network traffic between your own machines is usually free**; the same traffic over public addresses in the same location usually is not. Configuring replication or backups over public addresses between two of your own servers is a silent, recurring charge.
- The usual causes of an unexpected overage: a backup egressing to another region or provider nightly; a large file linked somewhere public; a scraper or a badly behaved crawler; media served directly from the box instead of a CDN; an application making large outbound API calls in a loop.
- Overage is billed on the period total, not on the peak, so a single bad week can consume a month's allowance.
- The structural fix is a CDN in front of static assets, which typically removes the majority of egress for a content-heavy site and also improves latency.

## The Waste Sweep

Run on the cadence in `## Due`. Each row is money already spent for nothing:

| Look for | Why it exists |
|---|---|
| Stopped or powered-off servers | On most providers they still bill for disk and reserved address — "stopped" is not "free" |
| Servers with no owner in the inventory | Created for an experiment, never destroyed. The single most common finding |
| Reserved addresses attached to nothing | A destroyed server leaves its reserved address behind |
| Detached block volumes | Survive the instance they were attached to |
| Snapshots older than the retention policy, or with no policy | Per-GB, forever, and the count only grows |
| The backup add-on on a box that is rebuilt from a file anyway | Paying for undo on a machine with nothing to undo |
| Managed add-ons from a project that ended | Load balancers and managed databases outlive the servers they served |
| Oversized boxes below 20% utilisation for 14 days | `resizing.md` — each step down roughly halves the compute cost |
| Duplicate monitoring or uptime checks pointing at dead hosts | Bill per check, and page someone about a machine that no longer exists |

## Commitments and Prepay

- VPS discounts for annual prepay are typically modest — nothing like the multi-year commitment discounts of the large clouds.
- **Right-size first.** Prepaying an oversized box locks in the waste for a year and removes the incentive to fix it.
- Prepay is a bet that the provider's price will not fall and that you will not want to move. In a market where prices trend down, that bet is weaker than it looks.
- Reasonable rule: commit only for a workload that has been stable for two months and that has no migration in its foreseeable future.
- Watch the auto-renewal date. A yearly plan renewing silently for a project that ended is the most expensive version of the waste sweep.

## Right-Sizing as a Saving

- Fourteen days of metrics minimum, and check for a periodic peak — a monthly batch job invalidates a 14-day average (`resizing.md`).
- Sustained utilisation below roughly 20% with no periodic spike is a candidate for one step down. Steps roughly halve resources and cost.
- Memory is the risky dimension; CPU is usually safe to reduce first.
- A grown disk blocks a downsize on plans that bundle storage. Note it in `## Hosts` so the same suggestion is not made twice.
- Record what a change saved, with currency, in `## Spend` → `### Optimization Log`. Without the log, the same cleanup is rediscovered annually and nobody can say what the last one was worth.

## When a VPS Stops Being the Cheap Option

- **Bandwidth-heavy workloads**: past a certain egress volume, a provider with a large included allowance, or a CDN, dominates. Media hosting on a metered cloud is the classic mistake.
- **Steady, predictable, large compute**: at that scale, dedicated hardware — rented or a bare-metal offering — is frequently cheaper per unit than the equivalent VPS plans, and it removes steal time entirely.
- **Genuinely spiky, low-duty-cycle workloads**: something that runs for one minute an hour costs less on per-invocation pricing than on a box that is idle for 59.
- **Anything needing real high availability**: the second box, the load balancer, and the replicated database mean the comparison against a managed platform gets much closer than the plan pages suggest.
- **Your time**, when the alternative is a managed service and the person maintaining the box is the same person building the product.

## Non-Payment

- A failed payment leads to a suspension warning, then suspension, then deletion, on a provider-specific timetable typically measured in days to a few weeks.
- **Deletion after non-payment takes the snapshots with it.** This is the concrete version of Rule 4: an offsite copy is what survives a billing failure, a card expiry, or a closed account.
- An expired card on an account nobody checks is a real total-loss path. The billing contact should be an address someone reads, and the review cadence should include glancing at the payment method's expiry.

## Review Checklist

| Check | Action |
|---|---|
| This month against the last two closed months | Any line item that moved more than ~20% gets explained |
| Every server in the inventory has an owner and a purpose | Anything unowned is a teardown candidate |
| Bandwidth used against the allowance | Approaching the limit means a CDN, not a bigger plan |
| Snapshot count and total stored size against the retention policy | Prune |
| Reserved addresses and volumes attached to nothing | Release |
| Utilisation of every host over 14 days | Downsize candidates (`resizing.md`) |
| Payment method expiry and billing contact | Prevents the total-loss path above |
| Provider row in the subscriptions box matches the real invoice | Keeps the shared finances box honest |

---

**Write it down.** After every review: the month's row in `## Spend` → `### Monthly` in `~/Clawic/data/vps/memory.md` — provider, amount **with currency**, the `As of` date the number was read, the breakdown splitting plan price from add-ons, and whether it is closed or month-to-date (re-checking the current month overwrites its row, never adds a second). Every saving goes in `### Optimization Log` with its monthly amount and currency. Refresh any host in `~/Clawic/data/servers/servers.md` whose real cost moved more than ~20%, and the provider's total in `~/Clawic/data/finances/subscriptions.md` — one row per provider account, never per host, with the breakdown left in the inventory. Record the review date in `## Due`; a checklist with no last-run date gets skipped for a year and nobody notices. Past ~15 monthly rows, split `## Spend` to `spend-log.md` per `memory-template.md`.
