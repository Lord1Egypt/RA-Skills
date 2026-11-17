# Sales Motion — Choosing It by Arithmetic, Not Ambition

Scope: which go-to-market motion the ACV supports, when to switch, and how self-serve and sales coexist. Acquisition channels are `growth`; qualifying and running an individual deal is `b2b`; the price is `pricing`.

**Before proposing a motion change**, read `## Accounts` in `~/Clawic/data/saas/memory.md` (or `accounts.md`) for the actual ACV distribution and `## Revenue` for CAC payback — the motion follows the numbers already in the book, not the segment the company wishes it sold to.

## The Quota-Capacity Calculation

A motion is affordable when a quota-carrying rep can close enough deals to cover a multiple of their own cost.

```
quota          ≈ 4-5 × fully loaded rep cost
deals needed   = quota ÷ ACV
capacity       ≈ 30-60 closes per rep per year, depending on cycle length and complexity
```

Worked: a rep at 200k fully loaded carries roughly a 1M quota. At a 25k ACV that is 40 deals a year — inside capacity, so a sales motion works. At 5k ACV it is 200 deals a year, which no rep sustains, so the motion must be self-serve or the price must move. At 100k ACV it is 10 deals, comfortable, and the constraint becomes pipeline rather than capacity.

Run this before hiring the first rep, and run it again whenever ACV shifts by a large fraction. Most failed first sales hires are an arithmetic error, not a hiring error.

## Motion by ACV Band

| ACV | Motion | Human touch | Cycle | CAC payback to expect |
|---|---|---|---|---|
| Under ~1k | Pure self-serve | None; product and docs only | Minutes to days | Weeks, or the model does not work |
| 1-5k | Self-serve with assisted onboarding | Reactive help, no quota carrier | Days to weeks | Under a year |
| 5-25k | Sales-assist / inside sales | Demo, trial guidance, invoicing | Weeks to a quarter | Under a year, SMB expectation |
| 25-100k | Inside sales with a security review stage | Named rep, solutions help | One to two quarters | 12-18 months |
| 100k+ | Field / enterprise | Rep, solutions engineer, exec sponsor, procurement | Two to four quarters | 18-24 months |

The bands move with cycle length, not with preference. A 15k product with a six-month security review costs more to sell than a 40k product bought on a card, and it should be priced or packaged accordingly (`enterprise.md`).

## Self-Serve and Sales Together

Most SaaS businesses end up hybrid, and the hybrid fails on the boundary rather than on either side.

- **The self-serve path is never removed.** Forcing every buyer through a demo kills the segment that would have bought at 2am, and that segment is often the source of the champions who later buy the enterprise contract.
- **Define the hand-off by a signal, not by an inbound form**: seats above a threshold, usage above a tier ceiling, a corporate domain with multiple signups, a security-questionnaire request, or a plan-limit event on an account with company-scale traffic (`expansion.md`).
- **The rep's first contact must add something the product could not** — a configuration, a migration plan, a procurement path. A rep who reads back the pricing page reduces conversion below the no-rep baseline.
- **Never let sales-touch accounts get a worse deal than the self-serve price.** A published price that the sales team routinely undercuts trains the entire market to ask for a rep.
- **Compensation must not punish self-serve conversions** in a rep's territory, or reps will intercept accounts that were converting fine on their own.

## Founder-Led Sales, and When It Ends

- Founders should run sales until the motion is repeatable: the same qualification criteria, the same objections, the same close reasons, several times over. Dozens of closed deals is the commonly used marker, and the underlying test is whether the process can be written down.
- **Write it down before hiring**: ICP definition, qualification criteria, the demo narrative, the objection responses, the pricing and discount rules, the close sequence. A rep hired without this reconstructs it badly over two quarters, at full cost.
- **Hire two, not one.** With one rep, an underperformance is unattributable — the rep, the product, the market, the leads. Two gives a comparison.
- Ramp is real: a new rep at a moderate cycle length typically produces little in the first quarter and reaches full productivity around two to three cycles in. Model the cost of that ramp before hiring, not after.

## Discount Discipline

- **Ceiling first**: `discount_ceiling_pct` is what any rep may offer without approval, and one named person approves anything beyond it. A ceiling that everyone routinely exceeds is not a ceiling, it is a lower price list.
- **Trade, never give.** Longer term, annual prepay, a case study, a reference call, a shorter payment window, a broader initial deployment. A concession given for nothing sets the price of every renewal (`renewals.md`).
- **Measure realized ARPA against list monthly.** Discount drift is invisible deal by deal and obvious in the aggregate; a widening gap while list price holds is a price cut nobody decided (SKILL.md, Where Revenue Leaks).
- **Never discount to fix a value problem.** A buyer who does not believe the value will churn at the discounted price too, having cost the same to acquire.
- **End-of-quarter discounting teaches the market to wait.** Buyers share this information with each other far more than sellers expect.

## Pipeline Arithmetic

- **Coverage**: pipeline needed ≈ target ÷ win rate. A 30% win rate against a 1M quarter needs roughly 3.3M of qualified pipeline, and "qualified" must mean a written criterion, not a feeling.
- **Cycle length sets the lead time**: pipeline for next quarter is created this quarter. A team that starts generating pipeline at the start of the quarter it needs to close is one full cycle behind permanently.
- **Track stage conversion, not just totals.** A win-rate collapse in the security-review stage is an `enterprise.md` problem; one in the first-call stage is a targeting problem (`growth`).
- **Loss reasons, coded, from a fixed list**, exactly as churn reasons are. Free-text loss reasons aggregate to nothing.

## Switching Motions

The two directions have different failure modes.

**Self-serve → sales-assist** is triggered by inbound requests for invoicing, security review, or contracts; by a growing share of ACV coming from a small number of accounts; or by an entry-tier population that is obviously undersized for its usage. The risk is degrading the self-serve path in the process.

**Sales-led → self-serve (product-led)** is triggered by CAC payback drifting long and a product that no longer needs a human to demonstrate. It takes longer than teams expect: signup, onboarding, billing, entitlements and support deflection all have to exist before the first unassisted customer converts (`trials.md`, `entitlements.md`), and the sales team must be compensated in a way that does not make them fight it.

**After any motion decision**, write it to `artifacts/<kebab-name>.md` with the ACV distribution, quota arithmetic and CAC payback that justified it, plus its `## Boxes` line; record the discount ceiling and approval path in `config.yaml`; and log any perpetual discount or non-standard commercial term granted to a specific customer in `## Commitments` with its expiry (`memory-template.md`).
