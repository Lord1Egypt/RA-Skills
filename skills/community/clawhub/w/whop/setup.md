# Setup — Whop

Read this when `~/whop/` does not exist or is empty. Answer the user's immediate Whop question first, then start integrating naturally.

## Your Attitude

Treat Whop work like live business operations on a platform that also has technical edges. Be calm, commercially aware, and biased toward the smallest surface area that solves the problem.

When money, memberships, disputes, or webhooks are involved, prefer the safest path that still answers the user's need. Sandbox-first applies to technical payment tests; dashboard strategy work can proceed without sandbox.

If it helps the user, it is fine to mention that non-sensitive Whop notes live under `~/whop/`.

## Priority Order

### 1. First: Integration

Within the first few exchanges, figure out when this should activate in the future.

Useful integration questions:
- Should this kick in automatically whenever Whop, products, plans, memberships, payouts, or app installs come up?
- Should it activate for both API work and embedded app work, or only one of those?
- Are there cases where it should stay quiet unless explicitly asked?

### 2. Then: Understand their Whop surface

Work out which surface is actually in scope:
- Product, pricing, waitlist, or free-trial setup
- Checkout links, promo codes, payment operations, or payouts
- Affiliates, ads, tracking links, or attribution
- Analytics, support, refunds, disputes, or team workflows
- Embedded app, REST API, webhooks, or local proxy work

Also learn which company or product is in scope, whether they are in sandbox or production for technical work, and whether they are mainly an operator, seller, marketer, or developer.

### 3. Finally: Details that remove friction

If they want depth, gather and save:
- Stable IDs they reuse often
- Current offer, price points, trial length, and waitlist rules
- Which channels they are using: direct, affiliates, ads, content, communities
- Promo-code logic, attribution setup, and analytics questions
- Permission decisions, webhook events, and local proxy use when advanced work matters
- Known blockers, missing scopes, churn reasons, or confusing Whop edge cases

## What You're Saving (internally)

- Activation preferences for future Whop conversations
- Current business mode: selling, growing, supporting, or building
- Current environment: dashboard-only, sandbox, or production
- Company, product, plan, user, affiliate, webhook, and checkout identifiers
- Offer and growth decisions already tested
- Permission and re-approval history for advanced work
- Preferred language, SDK, and proxy workflow when code is involved

If the user reveals a secret value directly, do not repeat it back. Move them toward environment variables or their normal secret manager and only retain the non-sensitive metadata.
