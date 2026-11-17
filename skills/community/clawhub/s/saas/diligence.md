# ARR Quality — Surviving Diligence

Scope: what an investor, acquirer or lender deducts from a claimed number, and how to be ready before they ask. The fundraise process, valuation and term sheets are `cfo` and `ceo`; the definitions themselves are `revenue.md`.

**Before preparing any diligence material**, read `## Definitions`, `## Revenue`, `## Accounts` and `## Commitments` in `~/Clawic/data/saas/memory.md` (or the files `## Boxes` points to). Diligence is a consistency test as much as a performance test: a number that has been defined three different ways over two years is a finding regardless of how good it is.

## What Gets Deducted

A quality-of-earnings review restates ARR downward for anything that is not recurring, not committed, or not real. The restated figure becomes the one everyone uses, so it is worth producing it yourself first.

| Deduction | Why it goes | How it is found |
|---|---|---|
| Professional services, onboarding, training | Not recurring | Revenue by SKU against the contract |
| Hardware, resold licences, pass-through | Not your revenue, and it destroys the margin story | Gross margin by revenue line |
| Uncommitted usage above the floor | Not committed | Contract commitments compared against billed usage |
| One-off or perpetual-licence deals annualized | Not recurring | Contract term versus how it was counted |
| Related-party and founder-connected revenue | Not arm's length | Customer list against the cap table and directorships |
| Customers already churning or in dispute | Not durable | Support escalations, notice letters, receivables ageing |
| Free, comped and internal accounts counted as customers | Not revenue | Billing records against the customer count |
| Non-collectible receivables | Not cash | Ageing beyond terms, dunning status (`dunning.md`) |
| Multi-year contract value reported as annual | TCV is not ARR | Contract terms |
| Discounts and credits netted inconsistently | Overstates realized revenue | Realized ARPA against list |

## The Consistency Test

More deals are damaged by inconsistency than by weak numbers.

- **Every number in the deck, the model, the data room and the reporting history must tie.** They will be diffed. A discrepancy that is innocent still costs a week and a chunk of credibility.
- **Definitions must not have moved silently.** Where one did, disclose it with the date and the reason, and show both series. `## Definitions` with dated changes is exactly the artefact that turns a finding into a footnote (`revenue.md`).
- **Churn is not restated to look better.** A cohort table computed one way in the board pack and another way in the data room is the worst possible discovery.
- **Cash must reconcile to revenue.** Annual prepay makes cash and revenue diverge legitimately; deferred revenue is what explains it, and being unable to explain it reads as something worse than it is (`revenue.md`).

## The Data Room, Assembled in Advance

| Section | Contents |
|---|---|
| Revenue | Monthly movement bridge by month for as far back as it exists, customer-level MRR history, cohort retention, ARR bridge to the P&L |
| Customers | Account list with plan, ARR, start date, renewal date, term, churn date where applicable; concentration analysis |
| Contracts | Executed MSAs, order forms, DPAs, SLAs, and every non-standard term from `## Commitments` |
| Product / technical | Architecture summary, tenancy model, uptime history and incidents (`incidents/<year>.md`), roadmap |
| Security and compliance | SOC 2 or ISO report, penetration test summary, subprocessor list, security answer bank (`compliance.md`) |
| Metrics | The definitions register, CAC and payback derivation, gross margin build with COGS composition (`margins.md`) |
| Legal / people | Cap table, IP assignments, key employee agreements, open litigation |

Assemble it continuously rather than in a scramble. Most of it is already produced by the monthly close (`reporting.md`); the difference between a two-week diligence and a two-month one is whether it was kept.

## Concentration and Durability

- **Revenue concentration**: the share of ARR in the largest customer and the top handful. A single customer above roughly 10-20% of ARR becomes a discussion; above a third it becomes a valuation adjustment or an escrow.
- **Contract durability**: how much of ARR sits under contracts with more than twelve months remaining, versus month-to-month. Two businesses with identical ARR and different weighted contract length are not worth the same.
- **Logo concentration by segment and geography** matters for the same reason. A book that is 80% one industry inherits that industry's cycle.
- **Renewal cliff**: the share of ARR renewing in the next two quarters, and the health of those accounts (`renewals.md`). A large cliff among red-health accounts is the finding an acquirer will price.
- **Founder dependency**: deals closed personally by a founder, or accounts retained by a personal relationship. Documented, repeatable process is the mitigation (`sales-motion.md`).

## The Commitments Ledger Is the Sleeper Issue

Buyers read every contract. What surfaces, reliably:

- **MFN clauses** that constrain future pricing across the whole book.
- **Uncapped or high liability caps** accepted in early deals nobody remembers (`enterprise.md`).
- **Perpetual discounts and grandfathered plans** with no end date, which reduce realized ARPA permanently.
- **Feature commitments with dates** — a roadmap promise inside a contract is a liability, not a plan.
- **Data residency and isolation promises** that constrain the architecture and any future consolidation (`multitenancy.md`).
- **Assignment clauses** requiring customer consent on a change of control. A handful of these turns an acquisition into a customer-by-customer negotiation.

`## Commitments` maintained continuously, with a value and an expiry per row, is what makes this a one-day exercise instead of a three-week contract review with surprises in it (SKILL.md Rule 7).

## Preparing Well Before the Process

- **Restate your own ARR first**, strictly, and present that number. Presenting a strict number and being unable to be reduced is a far stronger position than defending a generous one.
- **Fix the definitions a year out.** A definition changed during a process looks like manipulation; changed a year before, it is hygiene.
- **Clean the customer list**: comped, internal, test and long-dead accounts removed from every count.
- **Close the reporting gaps.** Missing months in the movement history cannot be reconstructed later, and their absence is assumed to be unfavourable.
- **Age the receivables** and resolve the collectible ones. Old receivables read as either weak collections or unhappy customers.
- **Have the security and compliance pack ready** — for a strategic acquirer this is a gate, not a formality (`compliance.md`).

**After any diligence preparation or restatement**, write the restated basis and what was excluded from it to `## Definitions` with the date, ensure `## Commitments` is complete with values and expiries, and record the exercise itself — the restated numbers, the deductions taken, the concentration analysis — in `artifacts/<kebab-name>.md` with its `## Boxes` line (`memory-template.md`). Track the process as a programme in the shared `~/Clawic/data/projects/<project>.md`. Every future round or offer starts from that file rather than from a blank page.
