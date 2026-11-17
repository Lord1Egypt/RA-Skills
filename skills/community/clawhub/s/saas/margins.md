# Margins — Cost to Serve, COGS and the Per-Tenant Number

Scope: what it costs to deliver the product, per account and per unit, and what to do when that number breaks the plan. The company-level P&L and cash model is `cfo`; the price is `pricing`.

**Before any margin statement**, read `## Plans` in `~/Clawic/data/saas/memory.md` (or `plans.md`) for what each plan includes, `## Revenue` for the realized revenue per period, and `config.yaml` for `gross_margin_floor_pct`. A margin quoted without the plan it belongs to is an average that describes no customer.

## What Belongs in SaaS COGS

`gross margin = (revenue − COGS) ÷ revenue`. The argument is always about what goes in COGS, and the answer is: everything required to deliver the service to a paying customer today.

| In COGS | Not in COGS |
|---|---|
| Hosting, compute, storage, bandwidth for production | Development environments, CI, internal tooling |
| Model inference and third-party API calls made on customer requests | Engineering salaries building new features |
| Payment processing fees | Sales, marketing, G&A |
| Customer support and technical support staff | Product management, design |
| Customer success where it is required to keep the service working | Customer success where it is an upsell motion |
| Third-party licences resold or embedded per customer | Company-wide software licences |
| Data transfer to customers, CDN | Corporate IT |

Classic software lands at 75-85% gross margin. Products where a per-request model call or a heavy third-party API sits in the critical path routinely land at 50-65%, and that is a real business — it is only a problem when the price was set as if the margin were 80%.

Payment fees are the most commonly forgotten line, and on low-ACV self-serve books with a fixed per-transaction component they are material: many small monthly charges pay the fixed component many times, which is one of the quieter arguments for annual billing.

## Allocating Cost Per Tenant

Averages hide the account that is eating the tier. The allocation ladder, cheapest first:

1. **Direct attribution.** Every metered request already carries `account_id` (`metering.md`); attach the cost driver — model, tokens, compute seconds, egress bytes — in the same event. This is exact and it is the only method that survives a dispute.
2. **Resource tagging.** Per-tenant infrastructure (dedicated databases, queues, buckets) tagged with the tenant. Works in silo and bridge tenancy (`multitenancy.md`).
3. **Proportional allocation.** Shared infrastructure divided by a driver that correlates with consumption — requests, storage, active seats. State the driver; "divided by account count" is not an allocation, it is a rounding.
4. **Fixed overhead.** What genuinely cannot be attributed, spread and labelled as such. If it exceeds a modest share of COGS, the attribution work is not finished.

Output: cost per account per month, and cost per unit of the value metric. Both, because the first finds the outlier account and the second prices the next plan.

## The Distribution Is the Finding

Cost per account is heavily skewed in almost every SaaS. Report the median, the p90 and the maximum, never the mean alone.

- The p90/median ratio measures how exposed the pricing is to heavy accounts. A wide ratio on a flat-priced plan means a small number of customers consume the margin of the many.
- **Compute margin per account, then sort ascending.** The negative-margin tail is usually a handful of accounts on legacy plans, unlimited grandfathered terms, or a single pathological integration.
- A negative-margin account is one of four things: mispriced plan, abusive usage, a bug in your product retrying forever, or a customer using it for something you did not design for. The remedies differ completely, so diagnose before acting.
- Support cost per account belongs in this analysis. An account generating a ticket a week can be margin-negative on an otherwise healthy plan (`support.md`).

## Per-Request Model Cost

Where inference dominates COGS, margin becomes a runtime property rather than an accounting one.

- **Cost ceiling per request and per account, enforced in code.** A retry loop against a paid model is an unbounded cost incident with no revenue attached.
- **Route by required quality**: a cheaper or smaller model for the routine path, the expensive one where it changes the outcome. Most of the volume is usually routine, and the mix — not the unit price — is the lever.
- **Cache aggressively** on identical or near-identical inputs. In many workloads a meaningful share of requests repeat, and a cache hit is a full-margin request.
- **Bound the context.** Cost scales with input size; sending a whole document where a section suffices multiplies the bill silently.
- **Vendor price changes flow straight into gross margin.** Anything priced as if the current model price were permanent needs a review trigger — put it in `## Due` — and a contract that lets you change the fair-use ceiling.
- **Never resell raw provider units at their list price.** Either mark up meaningfully or, better, price on the customer's outcome and keep the cost model private (`metering.md`).

## When Margin Falls Below the Floor

Below `gross_margin_floor_pct`, in this order:

1. **Find the driver.** Which plan, which accounts, which meter. A blended figure never has an action attached to it.
2. **Fix the technical cost** first if there is obvious slack: caching, model routing, storage tiering, egress via CDN, right-sizing. This is the only remedy with no customer impact.
3. **Fence the usage.** A fair-use ceiling plus overage converts the tail from a margin problem into revenue (`packaging.md`, `metering.md`).
4. **Reprice.** New customers first, existing at renewal with notice (`plan-changes.md`, `pricing`).
5. **Deliberately accept it** — with a written reason and a review date — where the plan is a loss leader that reliably converts. Undocumented, this becomes the permanent state.

Never respond by growing volume. Selling more of a negative-margin plan enlarges the loss precisely in proportion to the success.

## Margin by Segment

Segment margin usually differs more than segment revenue does, and it inverts the picture of who the best customers are.

| Segment | Typical pressure |
|---|---|
| Self-serve SMB | Payment fees on small amounts, high support-ticket rate per dollar, high churn amortizing onboarding cost over a short life |
| Mid-market | Usually the best margin: enough revenue to absorb support, not enough demands to require dedicated infrastructure |
| Enterprise | Dedicated infrastructure or residency, named CSM, security reviews, custom SLAs, procurement time — often lower gross margin, offset by retention and expansion |
| Free tier | Pure COGS; the correct treatment is CAC, not margin (`trials.md`) |

Report margin by segment quarterly. The common discovery is that the smallest customers are the least profitable per dollar, which is a packaging argument rather than a reason to abandon them.

**After any margin analysis**, write the period's gross margin and the per-account distribution — median, p90, worst — to `## Revenue` with its as-of date, and add a `## Due` row for the next review. A cost-reduction that worked, or a decision to accept a plan below the floor, belongs in `artifacts/<kebab-name>.md` with its reasoning, its numbers and its `## Boxes` line (`memory-template.md`): the same infrastructure saving is otherwise rediscovered every year.
