---
name: state-management
description: Deep workflow for client (and hybrid) state—modeling domain vs UI state, server cache vs client store, async and consistency, DevTools, persistence, and testing. Use when choosing Redux/Zustand/Recoil/Context, fixing stale UI, or designing data flow in React/Vue/Svelte apps.
---

# State Management (Deep Workflow)

Most “state bugs” are **ownership** and **lifecycle** bugs: who writes, when it syncs, and what happens on failure. Guide users to **explicit models** instead of ad-hoc globals.

## When to Offer This Workflow

**Trigger conditions:**

- Prop drilling pain, inconsistent UI, duplicate sources of truth
- Stale data after mutations; optimistic UI gone wrong
- Choosing a library vs Context vs server-state library (React Query, SWR, Apollo)
- SSR/hydration + client state mismatches

**Initial offer:**

Use **six stages**: (1) inventory state kinds, (2) assign ownership, (3) server vs client boundaries, (4) async & updates, (5) persistence & URLs, (6) testing & DevTools. Confirm **framework** and **data fetching** approach.

---

## Stage 1: Inventory State Kinds

**Goal:** Classify **what** state exists before picking tools.

### Categories

- **Remote/server state**: API responses, pagination, staleness—often **not** Redux-shaped
- **URL state**: filters, tabs, selection when shareable/bookmarkable
- **Session UI state**: modals, toggles, transient form drafts
- **Client-derived**: sorted/filtered views of remote data—**avoid** storing both raw and derived as writable truths
- **Global cross-cutting**: auth user, theme, feature flags—with clear **read-only** vs **mutable** rules

**Exit condition:** Table of **state slices** → **source of truth** → **consumers**.

---

## Stage 2: Assign Ownership

**Goal:** **One writer** per piece of truth (or strict reducer pattern).

### Rules of Thumb

- **Colocate** state where it’s used if not shared—don’t globalize prematurely
- **Lift** only when multiple subtrees need it or prop chains hurt **and** ownership is clear
- **Avoid** copying server entities into multiple stores without sync rules

**Exit condition:** For each slice: **who sets**, **who reads**, **invalidation** story.

---

## Stage 3: Server vs Client Boundaries

**Goal:** Prefer **server-state libraries** for remote data; use **client stores** for true client concerns.

### Guidance

- **React Query / SWR / RTK Query**: caching, dedupe, refetch, background refresh—use for HTTP JSON
- **GraphQL clients**: normalized cache + mutations with **update** policies
- **Redux**: great for **predictable** global client state + middleware—not every fetch response

### Anti-patterns

- Storing **full API JSON** in Redux without normalization when Apollo/Query would fit
- **Double fetch**: SSR then client refetch without coordination—use **hydration** patterns

**Exit condition:** Remote data has **defined cache keys**, **stale time**, and **mutation** flow.

---

## Stage 4: Async & Consistency

**Goal:** **Loading**, **error**, **empty**, and **retry** are first-class; **optimistic** updates are safe or scoped.

### Practices

- **Optimistic UI**: rollback path; idempotent mutations; **server reconciliation**
- **Ordering**: serial vs parallel requests; **race** cancellation (AbortController)
- **Pagination/infinite scroll**: cursor stability; dedupe pages

### Concurrency

- **Last write wins** awareness; versioning or ETags if server supports

**Exit condition:** User-visible **failure modes** handled; no silent stale success.

---

## Stage 5: Persistence & URL

**Goal:** Decide **what survives refresh**, **what is shareable**, and **security**.

### Options

- **URL query** for filters/tabs when users share links
- **localStorage/sessionStorage** for drafts—mind **XSS** risk (sensitive data → not localStorage)
- **IndexedDB** for offline—complexity tax

**Exit condition:** Sensitive data **never** persisted client-side inappropriately.

---

## Stage 6: Testing & DevTools

**Goal:** State logic is **unit-testable**; time-travel/debug when needed.

### Practices

- **Pure reducers** / small hooks for rules
- **Integration tests** for critical flows with **MSW** or mock server
- **DevTools**: Redux/Query panels—ensure team knows how to inspect cache

---

## Final Review Checklist

- [ ] State classified: remote vs UI vs URL vs derived
- [ ] Single owner per truth; invalidation clear
- [ ] Server cache strategy chosen for API data
- [ ] Async/error/empty/optimistic paths specified
- [ ] Persistence/security boundaries respected

## Tips for Effective Guidance

- **Start minimal**: Context + server-state library solves many “Redux-sized” problems.
- Always ask: “**What is the source of truth** after mutation returns?”
- Mention **React Strict Mode** double-invoke when debugging weird effect behavior.

## Handling Deviations

- **Legacy Redux everywhere**: incremental migration—**feature modules** first, remote data to Query next.
- **Non-React**: map patterns to **signals/stores** (Vue Pinia, Svelte stores) with same ownership discipline.
