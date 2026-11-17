# TODO: Partner Signup / Application Process

**Date:** 2026-02-25
**Priority:** Needed before launch

---

## Stripe Partners

- [ ] Design application/signup flow for Stripe Connect partners
- [ ] What info do we need? (store URL, Stripe account ID, product categories, expected volume)
- [ ] How do they apply? (form, email, GitHub issue?)
- [ ] Onboarding: Stripe Connect OAuth flow to link their account
- [ ] Tier assignment (Tier 0/1/2) ... manual review or automated?
- [ ] Fee agreement: 90-day free intro, then 2-5% application_fee

## 402 Partners

- [ ] Design application/signup flow for x402 gate operators
- [ ] What info do we need? (domain, payment gate URL, chain, expected volume)
- [ ] How do they apply? (form, email, GitHub issue?)
- [ ] Verification: test their 402 response to confirm it works
- [ ] Tier assignment (Tier 0/1/2) ... manual review or automated?
- [ ] Fee agreement: 90-day free intro, then 2-5% (deducted from pool settlement ... mechanics TBD)

## Partner Pages as Agent-Readable Skills

- [ ] Move PARTNERS-402.md and PARTNERS-STRIPE.md to wipcomputer.com (clean URLs)
- [ ] Structure partner pages so an agent can read them and walk a seller through applying
- [ ] "Point your agent to this URL" ... same pattern as "Teach Your AI How To Pay"
- [ ] Agent reads requirements, checks seller's setup, submits application via `POST /partner/apply`
- [ ] Build `POST /partner/apply` worker route

## Unsupported Partner Gate

- [ ] When agent hits a non-partner store, show: "This seller isn't an AI CASH partner yet. Want us to reach out?"
- [ ] Log requests to KV (`partner-request:{domain}`)
- [ ] Give user a shareable link to send to the store owner
- [ ] Review top-requested domains for manual outreach
- [ ] See full plan: `ai/plans/unsupported-partner-gate--2026-02-25.md`

## Open Questions

- Do we need a partner portal / dashboard?
- Self-serve signup or manual approval for v1?
- Legal: do we need a partner agreement / ToS?
