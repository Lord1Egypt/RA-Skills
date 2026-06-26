---
name: react-patterns
description: Deep React patterns workflow—component boundaries, composition, hooks rules, effects and data fetching, performance (memo, lists, suspense), testing, and accessibility. Use when structuring React apps, reviewing component design, or debugging re-renders.
---

# React Patterns (Deep Workflow)

Healthy React codebases emphasize **clear data flow**, **minimal effects**, and **predictable** rendering. Prefer **composition** over inheritance; treat **effects** as synchronization, not “do something after render” for everything.

## When to Offer This Workflow

**Trigger conditions:**

- Prop drilling vs context vs external stores; confusion on **server components** (Next) vs client
- **useEffect** spaghetti; stale closures; double-fetch
- Re-render performance; large lists; hydration issues

**Initial offer:**

Use **six stages**: (1) structure & boundaries, (2) state & data sources, (3) hooks discipline, (4) effects & events, (5) performance, (6) testing & a11y). Confirm **React** version and **framework** (plain CRA, Vite, Next App Router).

---

## Stage 1: Structure & Boundaries

**Goal:** **Colocate** state; split **presentational** vs **container** only when it clarifies—not by default.

### Practices

- **Compound components** for flexible APIs; avoid mega-props objects
- In Next App Router: default to Server Components; add `use client` at leaves

---

## Stage 2: State & Data Sources

**Goal:** **Local** state for UI; **server** state via React Query/SWR/Apollo as appropriate; avoid duplicating server entities in global stores without sync rules.

---

## Stage 3: Hooks Discipline

**Goal:** **Rules of Hooks** satisfied; custom hooks encapsulate reusable stateful logic with clear inputs/outputs.

### Practices

- Name hooks `useThing`; return stable APIs (objects memoized when needed)

---

## Stage 4: Effects & Events

**Goal:** Prefer **event handlers** for user-driven work; **useEffect** for sync with external systems (subscriptions, non-React widgets).

### Practices

- **Cleanup** subscriptions; **abort** fetches; list **effect** dependencies honestly
- Strict Mode double-invoke in dev—write effects idempotent

---

## Stage 5: Performance

**Goal:** Measure before `memo`; **virtualize** long lists; **code-split** routes.

### Practices

- `useCallback`/`useMemo` when profiling shows benefit—not by default
- **Concurrent** features and **Suspense** boundaries where supported

---

## Stage 6: Testing & Accessibility

**Goal:** **React Testing Library** user-centric queries; **focus** management and **labels** for forms.

---

## Final Review Checklist

- [ ] Component boundaries match data ownership
- [ ] Server vs client state strategy clear
- [ ] Hooks and effects used appropriately
- [ ] Performance optimizations evidence-based
- [ ] Tests and a11y basics covered for critical flows

## Tips for Effective Guidance

- **Derive** state when possible instead of storing redundant pieces.
- **URL** as state for shareable UI state when appropriate.
- Point to **state-management** skill for Redux/Zustand-scale decisions.

## Handling Deviations

- **Legacy class components:** same principles; hooks migration incremental.
