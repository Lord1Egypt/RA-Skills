# Plan: Unsupported Partner Gate

**Date:** 2026-02-25
**Status:** Concept. Needs design.

---

## The Idea

When a user's AI agent tries to pay on a store or x402 gate that isn't in the AI CASH partner network, don't just fail. Show a gate:

> "This seller isn't an AI CASH partner yet. Would you like us to reach out to them?"

If the user says yes, we capture:
- The seller's domain/URL
- The product the user was trying to buy
- The user's contact (optional, for follow-up)

Then we reach out to the seller with a warm lead: "A real customer tried to buy from you through AI CASH and couldn't. Here's how to join."

## Why This Matters

- Every failed purchase becomes a **lead generation event**
- The user is already motivated ... they wanted to buy
- The seller gets inbound demand, not a cold pitch
- Network grows organically from actual purchase intent
- We learn which sellers/sites users want most (prioritize outreach)

## Design Questions

1. **Where does the gate live?** In the CLI response? In the worker? Both?
2. **What does "reach out" mean?** Automated email? Form submission? Manual outreach queue?
3. **Do we collect the user's email?** Or just log the request anonymously?
4. **How do we store interest?** KV? Database? Simple log?
5. **What's the UX for the agent?** Does it say "I'll let them know" or does it give the user a link to share with the seller?
6. **Rate limiting?** Don't spam a seller with 100 requests for the same domain.
7. **Privacy:** Do we tell the seller who the user is? Or just "someone tried to buy X"?

## Possible Flows

### Flow A: Automated (v1)
```
1. Agent hits unsupported domain
2. Worker returns: { status: "unsupported-partner", domain: "example.com" }
3. CLI shows: "This store isn't an AI CASH partner yet. Want us to reach out?"
4. User says yes
5. CLI calls: POST /partner/request { domain, productUrl }
6. Worker logs to KV: partner-request:example.com (count, last request, product URLs)
7. When count hits threshold, we manually review and reach out
```

### Flow B: User-Driven
```
1. Same as above, but instead of us reaching out...
2. CLI gives user a shareable link: "Send this to the store owner"
3. Link goes to a landing page: "A customer wants to buy from you with AI CASH. Here's how to join."
4. Lower effort for us, but depends on user following through
```

### Flow C: Hybrid
- Log all requests automatically (Flow A)
- Also give user the shareable link (Flow B)
- We reach out when we see demand patterns, user can accelerate it

## Agent-Readable Partner Application Skill

The partner pages (PARTNERS-402.md, PARTNERS-STRIPE.md) should double as agent-readable skills. Same pattern as CASH.md's "Teach Your AI How To Pay."

On the 402 partner page:

> **Want to apply?** Point your agent to this URL. It will read the requirements, check your setup, and walk you through the application.

The agent reads the page, understands:
- What AI CASH is
- What's required (working 402 gate, supported chain, etc.)
- How to apply (submit domain, payment gate URL, expected volume)
- What tier they'd start at

Then it walks the seller through the process interactively. The application gets submitted to us via API (`POST /partner/apply`).

Same thing for Stripe partners: agent reads PARTNERS-STRIPE.md, checks their Shopify/Stripe setup, walks them through Connect OAuth.

**This means the partner pages need to move to wipcomputer.com** so they're proper URLs agents can fetch, not just GitHub markdown. GitHub works but a clean URL like `wipcomputer.com/partners/402` or `wipcomputer.com/partners/stripe` is better for agents and humans.

## Implementation Notes

- New worker routes: `POST /partner/request`, `POST /partner/apply`
- KV key: `partner-request:{domain}` with count, timestamps, product URLs
- KV key: `partner-application:{domain}` with application data
- Dashboard/report for reviewing top-requested domains
- Partner pages need to move to wipcomputer.com (TODO)
- Partner pages need to be structured as agent-readable skills (like SKILL.md)
- Could integrate with partner onboarding flow once that exists
