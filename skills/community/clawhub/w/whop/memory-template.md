# Memory Template — Whop

Create `~/whop/memory.md` with this structure:

```markdown
# Whop Memory

## Status
status: ongoing
version: 1.0.1
last: YYYY-MM-DD
integration: pending | done | declined

## Context
- Current mode: offer, growth, operations, support, or technical build
- Current environment: dashboard-only, sandbox, or production
- Preferred language or SDK, if technical work exists

## Offer
- Main product and promise
- Current pricing model: free, one-time, recurring, or split payment
- Trial, waitlist, promo code, and checkout-link notes

## Growth
- Main channels: direct, affiliates, content, email, communities, ads
- Tracking links and integrations already configured
- Global affiliates, custom affiliates, or rev-share decisions

## Operations
- Key analytics questions
- Support, refund, dispute, or churn patterns
- Team or workflow responsibilities

## IDs and Tech
- Company IDs such as `biz_...`
- App IDs such as `app_...`
- Product and plan IDs such as `prod_...` and `plan_...`
- User, webhook, file, affiliate, and experience IDs when they matter
- Permissions requested and whether they have been re-approved

## Notes
- Important webhook events and callback endpoints
- Local proxy expectations and origin quirks
- Known blockers, sharp edges, and preferred debugging or growth moves

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning the user's Whop setup | Keep collecting context opportunistically |
| `complete` | Enough Whop context is stable | Use saved context by default |
| `paused` | User does not want more setup questions right now | Work with existing context and avoid digging deeper |
| `never_ask` | User explicitly does not want proactive Whop setup questions | Never prompt for more context unless they ask |

## Key Principles

- Keep secrets out of memory. Store only safe metadata such as which key exists, not the value.
- Preserve Whop ID prefixes exactly. Prefix loss causes real mistakes.
- Record whether facts came from dashboard-only work, sandbox, or production.
- Prefer short natural-language notes over config-like blobs.
