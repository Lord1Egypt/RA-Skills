---
name: subscription-renewal-health
description: Monitor recurring-billing and subscription business health — pool volatility, churn, and payment failure — then output dunning and retention email series grounded in compensation psychology. Use when churn rate is rising, failed renewal charges or card declines spike, MRR or active subscriber count swings, dunning workflows break, or the user wants win-back and "sorry + make-good" sequences for subscribers. Automate structured reporting plus email scripts (not generic blasts). Do NOT use for one-off transactional receipts with no subscription context, or pure pricing math with no churn or payment-failure angle.
compatibility:
  required: []
---

# Subscription renewal health monitor

You combine **subscription pool signals** → **payment failure tracking** → **retention emails with compensation psychology** so operators see health clearly and recover revenue without sounding punitive.

## When to lean in

- **Churn rate** up vs prior period.
- **Failed charges** (expired card, insufficient funds, authentication) frequent.
- **Volatility** in active subs or MRR without clear acquisition story.

## Core workflow

1. **Pool snapshot** — Active subs, new, churned, net movement; optional cohort window.
2. **Payment failure lens** — Failure reasons if known; retry policy; dunning stage gaps.
3. **Retention + compensation scripts** — Email (or SMS) series using **compensation psychology**: fairness, reciprocity, certainty of fix, optional small tangible make-good when policy allows.

## Gather context

1. Platform (Stripe Billing, Recharge, Shopify Subscriptions, etc.).
2. Churn definition (voluntary cancel vs involuntary fail).
3. Current dunning steps and retry count.
4. What compensation is allowed (free month, skip box, % off next cycle).

Read `references/subscription_playbook.md` for dunning stages and compensation framing.

## Mandatory outputs (full run)

### A) Health table

| Signal | Current | Prior / target | Note |
|--------|---------|----------------|------|
| Active subscribers | … | … | … |
| Churn rate | … | … | voluntary vs involuntary |
| Failed payment rate | … | … | … |
| Recovered after dunning | … | … | if known |

Placeholders OK; state what to export from billing tool.

### B) Payment failure tracking (structured)

| Failure type | Share (if known) | Retry / fix | Owner |
|--------------|------------------|-------------|--------|
| Card expired | … | Update card link | Dunning email 1 |
| Insufficient funds | … | Retry schedule | … |
| Authentication | … | 3DS / new PM | … |

### C) Retention email series — compensation psychology

Deliver a **3+ message** sequence (dunning + optional voluntary churn win-back). Each message must include:

- **Subject line A/B**
- **Body skeleton** (short)
- **Compensation psychology label** (e.g. reciprocity — small gift after fix; fairness — acknowledge failure; certainty — "we've extended your access until X")

**Psychology angles to use (at least two across the series)**

- **Fairness** — acknowledge failed charge or bad experience without blame.
- **Reciprocity** — modest make-good after they update payment (credit, extra week, free add-on).
- **Loss aversion** — what they keep by fixing (access, member price) vs neutral tone.
- **Certainty** — single clear CTA; "one click to update card."

Avoid manipulative guilt; stay compliant with subscription and email law (easy unsubscribe on marketing; transactional dunning separate per policy).

## When NOT to use

- Single order shipping email only.
- Churn analysis with no actionable comms or failure tracking ask (still OK to give health table only if user insists).

## Split with other skills

- **LTV win-back** — one-time purchasers; this skill is **recurring billing + dunning**.
- **Payment funnel** — one-time checkout; this skill is **renewal attempts**.
