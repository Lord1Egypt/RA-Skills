---
name: ssr-ssg
description: Deep workflow for SSR, SSG, ISR, and hybrid rendering—choosing modes per route, data freshness, caching, streaming, hydration, SEO, and operational trade-offs (Next.js, Nuxt, Remix, etc.). Use when tuning web apps for performance, correctness, and crawlability.
---

# SSR / SSG / Hybrid Rendering (Deep Workflow)

Rendering is an **architecture decision**, not a framework toggle. Guide users to map **freshness**, **personalization**, **cost**, and **complexity** per route—avoid “SSR everything” or “static everything” by default.

## When to Offer This Workflow

**Trigger conditions:**

- Choosing rendering strategy for marketing vs app shell vs dashboards
- SEO + auth + dynamic data conflicts
- Slow TTFB, stale content, or expensive server work per request
- Hydration bugs, double data fetch, or client/server environment mismatch

**Initial offer:**

Use **six stages**: (1) route & data classification, (2) choose rendering mode(s), (3) data loading & cache layers, (4) streaming & partial SSR, (5) hydration & client boundaries, (6) validate (SEO, perf, ops). Confirm **framework** and **hosting** (Node server, serverless, edge).

---

## Stage 1: Route & Data Classification

**Goal:** Each **route** has clear **freshness**, **auth**, and **personalization** needs.

### Dimensions

- **Public vs authenticated**: can HTML be shared or per-user?
- **Update frequency**: static marketing, hourly blog, real-time inventory
- **Source of truth**: CMS, DB, API with rate limits, edge KV

### Output

A **matrix**: route pattern → public/private → max staleness acceptable → personalization level.

**Exit condition:** No ambiguous “dynamic page” without stating **what changes** and **how often**.

---

## Stage 2: Choose Rendering Mode(s)

**Goal:** Pick **SSG**, **SSR**, **ISR/ondemand revalidate**, **CSR with SSR shell**, or **edge**—per route.

### Heuristics

- **SSG / prerender**: stable content, best TTFB/CDN cache, great SEO—watch **rebuild/revalidate** story
- **SSR**: must reflect **request-time** data (A/B, geo, auth gating) or **strict freshness**
- **Client-heavy**: acceptable for **post-auth** app surfaces if SEO not needed
- **Hybrid**: static shell + client islands; or **static generation** with **server components** for parts (framework-specific)

### Trade-offs

- SSR **cost** and **latency** vs SSG **staleness**
- **Edge** rendering: geography and limits (CPU, Node APIs)

**Exit condition:** Documented **per-route** strategy with **rationale**.

---

## Stage 3: Data Loading & Cache Layers

**Goal:** **One coherent story** for where data is fetched and how it is cached (CDN, full-page, data cache, edge).

### Practices

- **Cache-Control** / surrogate keys / tag-based invalidation—align with framework primitives (e.g., `revalidate`, `fetch` cache)
- **Deduplicate** requests between server and client where frameworks allow
- **Avoid** accidental **private data in shared cache**—vary by cookie/auth correctly or disable cache

### Stale-While-Revalidate

- Great for **mostly fresh**—document **user-visible staleness** acceptance

**Exit condition:** Data flow diagram: origin → edge → browser; **invalidation** owner identified.

---

## Stage 4: Streaming & Partial SSR

**Goal:** Improve **perceived performance** with **suspense/streaming** where supported.

### Guidance

- Defer **slow** fragments; show **skeletons** with accessible semantics
- **Ordering**: ensure critical **LCP** resources not blocked by deferred junk
- **Headers**: understand **chunked** response implications for intermediaries

**Exit condition:** Slow dependencies **isolated**; UX fallbacks defined.

---

## Stage 5: Hydration & Client Boundaries

**Goal:** **Correct** interactive UI without **double work** or **mismatches**.

### Checklist

- **Server/client** component or module boundaries (framework-specific)
- **useEffect** vs server fetch duplication—**waterfalls**
- **Environment**: no `window` on server; no **secret** APIs in client bundles
- **Hydration mismatch**: locale, random IDs, time—**suppress** or **serialize state**

**Exit condition:** Known **interactive islands** listed; mismatch risks mitigated.

---

## Stage 6: Validate (SEO, Performance, Ops)

**Goal:** Rendering choices **show up** correctly in search, metrics, and logs.

### SEO

- **View source** / rendered HTML for critical content; **meta** and **canonical** per mode
- **Auth**: soft paywalls—decide what crawlers see ethically and technically

### Performance

- **TTFB** vs **FCP/LCP**; **server time** vs **edge cache hit**
- **RUM** segmented by route and cache hit

### Ops

- **Cold starts** on serverless SSR; **concurrency** limits; **regional** failover

---

## Final Review Checklist

- [ ] Per-route rendering choice documented with freshness/personalization
- [ ] Caching and invalidation story is explicit and safe for auth
- [ ] Streaming/skeletons don’t harm LCP or a11y
- [ ] Hydration and env boundaries verified
- [ ] SEO and RUM validation for top templates

## Tips for Effective Guidance

- Name **staleness** in seconds/minutes—“real-time” is rarely real-time.
- When user uses **Next.js**, tie advice to **App Router** vs **Pages** semantics explicitly if known.
- Warn: **edge** ≠ full Node—**API surface** differs.

## Handling Deviations

- **SPA-only**: focus on **meta** for landing routes and **prerender** for marketing if added later.
- **No server**: SSG + client or **external** prerender service—be honest about limits.
