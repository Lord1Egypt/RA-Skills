---
name: rate-limiting
description: Deep rate limiting workflow—identifying actors and resources, choosing algorithms, distributed vs local limits, client UX (headers, retries), and abuse detection. Use when protecting APIs, gateways, or multi-tenant SaaS workloads.
---

# Rate Limiting (Deep Workflow)

Rate limits balance **fairness**, **availability**, and **abuse prevention**. Design explicitly: **who** is throttled, **what** resource is limited, and how clients should **back off**.

## When to Offer This Workflow

**Trigger conditions:**

- Protecting public APIs, auth endpoints, or expensive operations
- Multi-tenant “noisy neighbor” isolation
- Retry storms after incidents causing cascading 429/502

**Initial offer:**

Use **six stages**: (1) threat & fairness model, (2) dimensions & keys, (3) algorithms & config, (4) distributed enforcement, (5) client protocol & UX, (6) observability & tuning). Confirm enforcement layer (API gateway vs app middleware vs edge).

---

## Stage 1: Threat & Fairness Model

**Goal:** Distinguish legitimate bursts (batch jobs, mobile retries) from abuse; align limits with product tiers and SLAs.

**Exit condition:** Written policy: free vs paid limits, partner caps, burst allowances.

---

## Stage 2: Dimensions & Keys

**Goal:** Choose stable limit keys: authenticated user id > API key > IP (with shared-NAT caveats).

### Practices

- Per-tenant and global limits; separate expensive routes (exports, search)

---

## Stage 3: Algorithms & Config

**Goal:** Token bucket / leaky bucket for smooth bursts; sliding window for strict per-minute caps; consider **concurrency** limits separately from request rate.

---

## Stage 4: Distributed Enforcement

**Goal:** Central store (Redis, etc.) with atomic increments; handle multi-region (sticky routing vs shared counters); mind clock skew.

---

## Stage 5: Client Protocol & UX

**Goal:** Consistent **429** responses with **`Retry-After`**; document exponential backoff + jitter; optional `X-RateLimit-*` headers for transparency.

---

## Stage 6: Observability & Tuning

**Goal:** Metrics on throttles by route and actor class; alerts on abnormal deny spikes (attack vs misconfigured client).

---

## Final Review Checklist

- [ ] Policy matches tiers and fairness goals
- [ ] Limit keys stable and hard to spoof
- [ ] Algorithm matches burst vs sustained semantics
- [ ] Distributed correctness considered
- [ ] Client-facing 429 behavior documented
- [ ] Metrics and tuning loop defined

## Tips for Effective Guidance

- Coordinate with authentication—anonymous IP limits are coarse.
- Don’t throttle health checks in ways that break monitors.
- GraphQL: consider query **cost** / depth limits, not only HTTP count.
- WebSockets: separate connection caps from message rate limits.

## Handling Deviations

- **Edge/CDN:** limits may differ from origin—document both layers.
