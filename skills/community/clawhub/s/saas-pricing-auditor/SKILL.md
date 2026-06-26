---
name: saas-pricing-auditor
description: Audit a SaaS pricing page and return a scorecard, specific rewrites, and an A/B test priority queue. Diagnoses tier psychology (3-tier vs 4-tier, where the anchor sits), price points (charm vs round, currency formatting, decoy effect), feature-gating logic (the right and wrong reasons to gate a feature), the freemium-vs-trial decision, value-metric selection (per-seat, per-usage, hybrid, outcome-based), expansion-revenue mechanisms (overages, add-ons, tier upgrades, seat sprawl), monthly/annual toggle defaults, comparison-table clarity, and social-proof placement. Outputs a 1-10 score per dimension with specific rewrites and a ranked test backlog. Use when asked to review a pricing page, redesign tiers, raise prices, fix poor conversion, choose a value metric, decide between freemium and trial, or prep for a pricing repackage.
metadata:
  tags: ["pricing", "saas", "monetization", "conversion-rate-optimization", "packaging", "pricing-strategy", "growth", "revenue"]
---

# SaaS Pricing Auditor

Most SaaS pricing pages were drafted in a tab once and never revisited. They feel reasonable, convert below industry median, and quietly leak 20–40% of potential ARR through bad gating, weak anchoring, and a value metric that punishes power users. This skill audits the page on nine dimensions, scores each one, and ships specific rewrites plus a ranked test backlog.

## Usage

**Basic invocation:**
> Audit my pricing page: [URL or paste]
> Should I be 3-tier or 4-tier?
> Help me pick a value metric — I'm currently per-seat
> Free trial or freemium?
> Repackage from $19/$49/$99 to higher ACV

**With context:**
> B2B SaaS, $40k ARR, single $49/mo tier, no annual
> PLG product, 8% free→paid, want to lift to 12%
> Mid-market sales-led, $25k ACV, comparing to Salesforce
> Vertical SaaS for dental clinics, 3 tiers, low expansion revenue

The auditor returns a scorecard, prioritized rewrites, and the next 3–5 tests to ship.

## The Nine Audit Dimensions

Each dimension scored 1–10 with notes and a fix.

1. **Tier architecture** — number, names, anchor placement
2. **Price points** — charm pricing, round vs odd, currency display
3. **Feature gating logic** — what's gated and why
4. **Free trial vs freemium** — which model, parameters
5. **Value metric** — what you charge per
6. **Expansion-revenue mechanisms** — how revenue grows post-sale
7. **Monthly/annual toggle** — default, discount, framing
8. **Comparison table clarity** — readability, visual weight
9. **Social proof placement** — logos, quotes, numbers, near CTA

The order is the priority order. Architecture errors swallow everything below them — fixing button color while your value metric is wrong is rearranging deck chairs.

## Dimension 1: Tier Architecture

### 3-tier vs 4-tier vs 5-tier

| Count | When it works | When it fails |
|---|---|---|
| 1 tier | Self-serve under $50/mo, dead-simple product | Anything multi-segment |
| 2 tiers | Pure PLG with one upgrade path | Mid-market+ |
| 3 tiers | Default for SMB SaaS — Good/Better/Best | When segments diverge dramatically |
| 4 tiers | When Enterprise needs custom pricing on top of 3 | Otherwise; adds choice paralysis |
| 5+ tiers | Almost never; only with strong segmentation | Most SaaS — analysis paralysis |

**Default recommendation:** 3 tiers + custom Enterprise = 4 visible "options" without overwhelming.

### Anchor tier (the most-read tier)

The center tier in a 3-tier display gets ~60% of visual attention and should:

- Be marked "Most popular" with a colored border
- Contain the features the median customer needs (so they don't have to upgrade for table stakes)
- Be priced at the sweet spot of your contribution-margin curve
- Hide enough power-user features to leave room for the top tier

**Anchor errors to flag:**

- "Most popular" badge on the cheapest tier (signals to prospects that paying more is rare)
- "Most popular" badge on the most expensive tier (read as upsell theater)
- No badge at all (you're letting the visitor pick blind)

### Tier names

Names that work: *Starter, Pro, Business, Enterprise* / *Free, Plus, Pro, Scale* / *Solo, Team, Company*

Names that don't: *Bronze, Silver, Gold* (cliché, no signal); *Basic* (sounds like punishment); *Premium* (vague); *Tier 1, 2, 3* (reads as internal ops).

The middle tier name should imply *"this is the right answer for normal businesses"* — that's why "Pro" and "Business" outperform "Standard" and "Plus."

## Dimension 2: Price Points

### Charm pricing (.99) vs round vs odd

| Format | Where it works | Why |
|---|---|---|
| $19 | Self-serve, low end | Reads cheap and confident |
| $19.99 | Consumer / very low end | Squeezes loss-aversion bias |
| $29 / $49 / $99 | SMB SaaS sweet spot | Round = serious; odd = approachable |
| $49 | Common anchor SMB | The "tax floor" perception break |
| $50 | Slightly worse than $49 | Round numbers are processed as estimates |
| $499 / $999 | Mid-market | Charm pricing in 3-digit range still moves the needle |
| $1,000+ | Enterprise | Round numbers; charm pricing reads cheap |
| Custom / Talk to sales | Above ~$30k ACV | Forces qualification |

**The decoy effect:** when tier B is meaningfully better than A and *almost* the same price as C, B captures most volume. Common pattern:

- Tier A: $19/mo — 5 seats, basic features
- Tier B: $49/mo — 25 seats, full feature set ← decoy-driven anchor
- Tier C: $99/mo — unlimited seats, integrations

Tier B is the trap. Make sure the *delta* from A to B is large enough that A looks bad-value, and the delta from B to C is small enough that C looks like overkill for most.

### Currency display

- Always show currency symbol explicitly (`$49`, not `49`)
- Show "/month" or "/mo" with every price; never assume the period is obvious
- For per-seat pricing, show "per user/mo" — never just "/mo" (creates sticker-shock at checkout)
- For annual: show monthly-equivalent ("$49/mo, billed annually") — annual lump sum scares small buyers

## Dimension 3: Feature Gating Logic

The hardest pricing decision. Wrong gating either leaves money on the table (everyone gets the upgrade feature for free) or kills conversion (must-have features hidden behind enterprise tier).

### Good reasons to gate

- **Power-user-only features** — API, SSO, audit logs, custom roles. Most users don't need them; those who do pay for them.
- **High variable cost** — features that cost you per-use (AI calls, transactional emails over a threshold)
- **Compliance/security** — SOC 2 reports, BAA, custom DLP. Buyer of these is enterprise; gate accordingly.
- **Volume scaling** — seats, projects, storage. Linear cost = linear gate.

### Bad reasons to gate

- **It feels premium** — gating UI polish (dark mode, custom themes) annoys people without driving upgrades
- **Competitor does it** — they may be wrong; copying gates copies their conversion ceiling too
- **You spent engineering time on it** — sunk-cost fallacy; gate value not effort
- **Table-stakes features** — gating CSV export, basic search, or 2FA punishes everyone and signals greed

### The gating decision tree

```
Is the feature's marginal cost > $0?  → Gate by usage (overage or tier)
Is it a power-user / admin feature?    → Gate to higher tier
Is it a compliance/security feature?    → Gate to enterprise
Is it consumed in a measurable unit?    → Use as the value metric (don't gate; meter)
Otherwise                                → Don't gate; ship to all tiers
```

**Specific anti-patterns to flag in audits:**

- SSO behind enterprise-only when the rest of the product is $99/mo (the "SSO tax" — well-known pricing sin)
- API access at the highest tier only (cuts off integrations that drive expansion)
- Hard caps on seats with no overage path (forces a contract negotiation for +1 user; high friction)
- Feature counts as the differentiator instead of usage (drives feature-comparison fatigue)

## Dimension 4: Free Trial vs Freemium

### Decision matrix

| Factor | Freemium wins | Free trial wins |
|---|---|---|
| Time-to-value | Long (days/weeks) | Short (minutes) |
| Network effects | Strong | Weak |
| Marginal user cost | Near zero | Non-trivial |
| Buyer is end-user | Yes | Mixed |
| Sales motion | Pure PLG | PLG + sales-assist |
| Aha moment requires data | Yes (real workspace) | No (demo data fine) |

### Freemium parameters that work

- Free tier should solve a *real, narrow* problem completely — not a crippled version of the paid product
- Limits should hit at the moment users stop being hobbyists (number of projects, seats, integrations)
- Convert at the *aha moment*, not at month boundary
- Expect 2–5% free-to-paid conversion as median; 5–10% is excellent

### Free trial parameters that work

- 14 days is the default; 7 days for simple products; 30 days only for complex products with onboarding
- Require credit card if conversion intent is high; don't if you're top-of-funnel
- Trial-to-paid conversion: 15–25% no-CC, 40–60% with-CC
- Reverse trial (full features for N days, then downgrade to free) increasingly common; works for engagement-led products

### Anti-patterns

- Trial that requires CC + auto-charges silently (= chargeback magnet, bad reputation)
- Freemium with no path to paid (the "free forever" trap)
- 30-day free trial on a $19/mo product (you've given away ~10% of annual revenue per signup)

## Dimension 5: Value Metric

The single highest-leverage decision in pricing. Get it right, expansion revenue is automatic; get it wrong, you cap your account growth at "reset the contract."

### The value metric test

A good value metric:

1. **Scales with customer value** — when they get more out of the product, the metric grows
2. **Is predictable to the buyer** — they can estimate their bill before signing
3. **Aligns incentives** — your growth doesn't punish their adoption
4. **Has expansion built in** — accounts naturally grow on the metric

### Common metrics, ranked

| Metric | Pros | Cons | Best for |
|---|---|---|---|
| Per-seat | Predictable, SaaS-default | Caps at team size; punishes adoption | Collaboration, internal-tool SaaS |
| Per-usage (events, API calls, runs) | Scales with value, unbounded | Unpredictable bills, sticker shock | Infrastructure, AI, analytics |
| Per-record (contacts, customers) | Clear ROI mapping | Customers prune to save money | CRM, marketing |
| Per-revenue | Truly aligned | Hard to verify, requires trust | Payments, embedded fintech |
| Flat tiers | Predictable | Zero expansion mechanism | Very early or very low ACV |
| Hybrid (seats + usage) | Captures both | Complex to explain | PLG with team sprawl + power-use |
| Outcome-based | Maximally aligned | Hard to attribute, slow sales | Performance marketing, AI agents |

### How to choose

- If usage *causes* customer value (calls made, jobs run, data ingested) → meter it
- If a team is the unit of value → seats
- If a power-user does 10x what a casual user does → hybrid (seats + usage)
- If your customer is a small business and predictability matters → flat tier with usage caps

**Repackaging from per-seat to hybrid** is the most common 2025–2026 move; AI features have value-per-call that breaks pure-seat models.

## Dimension 6: Expansion-Revenue Mechanisms

Net revenue retention >110% is the difference between a 4x and a 10x business. The pricing page is where you build the mechanism.

### The four levers

1. **Overages** — soft caps with metered overages (e.g., "10k API calls included; $0.001/call after"). Best when usage is variable.
2. **Add-ons** — separately priced modules (extra storage, premium support, additional brands). Best when there are clear segments.
3. **Tier upgrades** — natural progression as the customer grows. Requires tier deltas to feel earned.
4. **Seat/license sprawl** — auto-add seats when invited, with admin approval. The most reliable expansion mechanism for collab tools.

### Expansion audit checklist

- Does any tier have a hard cap with no overage path? (= contract friction)
- Are there add-ons visible on the pricing page? (= optional, non-disruptive expansion)
- Does the metric grow naturally with customer success?
- Is there a clear upgrade trigger (UI nudge when nearing a limit)?
- Does annual billing kill expansion? (Quarterly true-ups solve this for usage-based.)

## Dimension 7: Monthly/Annual Toggle

### Default state

Default the toggle to **annual** if your business depends on annual cash. Defaulting to monthly is leaving 20–30% of contract value on the table for buyers who would have taken annual if it were the default option.

### Discount sizing

- 10% off annual: too small to motivate
- 15–20% off annual: industry standard, works
- 25%+ off annual: strong signal; use when cash flow matters
- 2 months free (≈17%): same as 17% but feels more concrete

### Framing

- "$49/mo, billed annually" reads as $49/month
- "$588/year" reads as a big number
- Always show monthly-equivalent next to the annual price
- Show the savings explicitly: "Save $118/yr"

## Dimension 8: Comparison Table

### Common errors

- Every feature row checked for every tier (no actual differentiation visible)
- Cryptic "✓" / "—" / "Limited" with no explanation
- Long feature lists (>20 rows) that no visitor reads
- Hiding meaningful limits in tooltips
- Putting the cheapest tier on the left (visitors read left-to-right; anchor on the right)

### What works

- 8–15 rows max; group into sections
- Use numbers, not just checks ("5 projects", "Unlimited", not "✓")
- Bold the differentiating features per tier
- Sticky headers on long tables
- Mobile collapse: each tier as its own card

## Dimension 9: Social Proof Placement

Where it goes determines whether it converts.

| Placement | Effect |
|---|---|
| Hero (above tiers) | Brand legitimacy; helps prospects believe pricing |
| Just below CTAs | Closes the deal; place the strongest quote here |
| Inside enterprise tier | Reinforces the "real companies pay this" cue |
| Footer-only | Wasted; nobody scrolls there before deciding |

### Types ranked

1. **Logos** of recognizable customers — fastest credibility
2. **Numerical proof** ("Used by 12,000 teams", "$2B processed", "ROI 4.2x")
3. **Specific quotes with title and company** — beats generic testimonials by 3–5x
4. **Case study link near tier** — for sales-led mid-market

## Scoring Rubric

Score 1–10 per dimension:

- **1–3**: actively harmful or missing
- **4–6**: present but unoptimized
- **7–8**: solid; minor improvements
- **9–10**: best-in-class; nothing to fix

A typical SMB SaaS audit lands around 5.5 average. Above 7.5 average = strong page. Below 4.5 average = repackaging project, not a CRO project.

## A/B Test Priority Queue

Tests ranked by typical lift × ease of implementation:

1. **Default annual toggle** — 5–15% ARR lift; one CSS change
2. **Add "Most popular" badge to anchor tier** — 5–10% mix shift to anchor; trivial
3. **Reorder tiers (anchor in middle, expensive on right)** — 3–8% conversion; layout change
4. **Move SSO out of enterprise-only** — 5–15% conversion lift on mid-tier; pricing change
5. **Add usage overage instead of hard cap** — 10–20% NRR lift; product+billing work
6. **Replace "Talk to sales" on enterprise with starting price** — increases qualified inbound; one-line change
7. **Replace generic testimonial with named-company quote near CTAs** — 3–7% conversion
8. **Switch to charm pricing on the anchor tier** — 1–4% conversion; trivial

## Output Format

The auditor returns:

1. **Scorecard** — 1–10 on all nine dimensions with one-line rationale per
2. **Top three architecture issues** — the highest-leverage problems first
3. **Specific rewrites** — exact tier names, prices, headlines, feature names to change
4. **Value-metric recommendation** — current metric, recommended metric, migration path
5. **Test backlog** — ranked queue of 5–10 A/B tests with hypothesis and lift estimate
6. **Repackaging plan (if needed)** — when fixes can't be done via tests; phased rollout
7. **Quick-wins list** — changes that can ship today without a meeting
