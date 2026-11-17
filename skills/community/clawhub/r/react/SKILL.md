---
name: React
slug: react
version: 1.0.7
description: >-
  Builds, debugs, and reviews React apps: components, hooks, state, Server Components, forms, performance, testing.
  Use when writing or refactoring components, choosing state management (useState, Context, Zustand, TanStack Query, Redux),
  when a component rerenders too often, loops infinitely ("too many re-renders"), shows stale or not-updating state, fails
  with a hydration mismatch or hook-order error, when an effect fires twice or fetches race, when typing lags or long lists
  scroll slowly, when adopting React 19, Server Actions, or the React Compiler, when testing components with Testing Library,
  typing props in TypeScript, or reviewing AI-generated React code. Not for React Native (mobile) or Next.js routing and
  deployment — use react-native or nextjs.
homepage: https://clawic.com/skills/react
changelog: "Display name shown correctly"
metadata:
  clawdbot:
    emoji: ⚛️
    displayName: React
    requires:
      bins:
      - node
    configPaths:
    - ~/Clawic/data/react/
---

User preferences and memory live in `~/Clawic/data/react/` (see `setup.md` on first use, `memory-template.md` for the file format). If you have data at an old location (`~/react/` or `~/clawic/react/`), move it to `~/Clawic/data/react/`.

## When To Use

- Building React components, features, or app architecture
- Choosing or wiring state (useState, Context, Zustand, TanStack Query)
- Working with React 19: Server Components, use(), Actions, React Compiler
- Debugging rerenders, infinite loops, stale closures, hydration errors, racing fetches
- Testing components, typing props, migrating legacy React code
- Reviewing AI-generated React for the failure patterns listed here
- Not for routing/deployment specifics (nextjs skill) or mobile (react-native skill)

## Quick Reference

| Situation | Play |
|----------|------|
| Data comes from an API | TanStack Query — never useState + useEffect fetch (`state.md`) |
| UI state shared across components | Zustand slice, read via selectors only (`state.md`) |
| State used by one component | useState, colocated; lift at the second consumer, not before |
| Rarely-changing globals (theme, locale, auth identity) | Context with memoized value; split state and dispatch contexts |
| Filters, tabs, page number the user could bookmark | URL searchParams, not useState (`state.md`) |
| Form with validation | React Hook Form + Zod (uncontrolled: keystrokes don't rerender); server mutation → useActionState (`forms.md`) |
| Typing lags in a filtered view | useDeferredValue around the value you receive; startTransition around state you set |
| List with thousands of rows | Virtualize (tanstack-virtual) — DOM node count is the cost, not data size |
| Component must reset when identity changes | Change its `key`: `<Profile key={userId} />` — remount beats manual state clearing |
| Multi-step flow / wizard | One discriminated-union status field, not a pile of booleans (`forms.md`) |
| A crash blanks the whole app | react-error-boundary per route and per risky feature |
| Same component commits repeatedly, props unchanged | Profile before touching code (`performance.md`) |
| Infinite loop, stale state, hydration error | Symptom chains in `debug.md` |
| Class components, forwardRef, PropTypes in the codebase | `migration.md` before adding features on top |
| Anything else / unsure | useState colocated, named export; extract when a second consumer appears |

Depth on demand: `debug.md` symptom→cause chains · `state.md` server/client/URL state · `server-components.md` RSC boundaries and Actions · `hooks.md` effect discipline, refs, custom hooks · `performance.md` profiling and fixes in priority order · `forms.md` validation, wizards, uploads · `testing.md` Testing Library, MSW, async · `typescript.md` typing patterns · `accessibility.md` focus, ARIA, keyboard · `migration.md` upgrades and legacy code · `setup.md` scaffolding and recommended stack.

## Core Rules

1. **Server state ≠ client state.** API data lives in TanStack Query (a cache with a lifecycle); UI state in useState/Zustand. Mixing them means hand-rebuilding dedupe, caching, and invalidation — badly.
2. **No effect without an external system.** Derivable from props/state → compute in render: `const total = items.reduce(...)`. Before writing useEffect ask "what outside React am I synchronizing with?" No answer → no effect (`hooks.md` for the full replacement table).
3. **`'use client'` marks a boundary, not a component.** Everything that file imports joins the client bundle. Put it on leaf interactive components; pass Server Components through as `children`.
4. **Stable keys — and keys as a tool.** `key={item.id}` for lists; deliberately changing a key is the sanctioned way to reset component state.
5. **Named exports only.** `export function UserCard` — rename refactors stay safe, imports stay greppable.
6. **Memoize by evidence.** React Compiler on: write no memo/useMemo/useCallback by hand — the compiler bails out on components that break the Rules of React, it doesn't fix them. Compiler off: memoize only after the Profiler shows the same component committing repeatedly with unchanged props.
7. **`strict: true` plus `noUncheckedIndexedAccess`.** With it, `array[0]` is `T | undefined` — the "impossible" runtime crash becomes a compile error.
8. **Split at ~50 lines of JSX or ~300 lines per file** (house default, not dogma): past that, the extraction candidates are already visible in the markup.

## Error Messages Decoded

| Error | Cause | First move |
|-------|-------|-----------|
| "Too many re-renders" | setState called during render, unconditionally | Find the bare `setX(...)` in the body or an `onClick={fn()}` call instead of `onClick={fn}` |
| "Rendered more hooks than during the previous render" | Conditional hook, or early return above a hook | Move every early return below the last hook (Component Rules) |
| "Invalid hook call" | Hook outside a component/custom hook — or two React copies | `npm ls react`; monorepos and linked packages duplicate React silently |
| "Objects are not valid as a React child" | Rendering `{user}` or `{date}` instead of a field | Render primitives: `{user.name}`, `{date.toISOString()}` |
| "Each child in a list should have a unique key" | Missing or duplicate keys | `key={item.id}` (rule 4); duplicates mean the data has duplicate ids — fix the data |
| "Hydration failed" / "Text content does not match" | Server and client rendered different markup | Chain in `debug.md` — Date/random/locale, invalid HTML nesting, browser extensions |
| "Cannot update a component while rendering a different component" | setState on another component during render | Move the setState into an event handler or effect |
| Minified React error #NNN | Production build strips messages | Decode at react.dev/errors/NNN, then reproduce in dev |

## Component Rules

```tsx
export function UserCard({ user, onEdit }: UserCardProps) {
  // 1. Hooks first, unconditional
  const [isOpen, setIsOpen] = useState(false)
  // 2. Derived values in render — never in an effect
  const fullName = `${user.firstName} ${user.lastName}`
  // 3. Handlers
  const handleEdit = () => onEdit(user.id)
  // 4. Early returns AFTER all hooks
  if (!user.isVisible) return null
  // 5. JSX
  return (...)
}
```

Export the props interface (`typescript.md` for variant props, generics, event types). Early returns must come after every hook call — a conditional return above a hook changes hook order between renders and crashes.

## State Management

```
Is it from an API?
├─ YES → TanStack Query (not Redux, not Zustand, not Context)
└─ NO → Should it survive refresh / be shareable? → URL searchParams
    └─ NO → Shared across components?
        ├─ YES → Zustand (changes often) or Context (rarely changes)
        └─ NO → useState
```

Load-bearing defaults (full patterns, pagination, optimistic updates, persistence: `state.md`):

- **TanStack Query >=5**: staleTime defaults to 0 — every mount and window refocus refetches. Set it per resource: staleTime = how stale the user can tolerate that data. Keep gcTime (default 5 min) ≥ staleTime. Query keys come from a key factory, one source of truth.
- **Zustand >=5**: read with selectors — bare `useStore()` rerenders on every store change; selectors returning fresh objects need `useShallow`. One store per concern — a god-store recreates Redux without the devtools.
- **Context**: every value change rerenders every consumer, no selectors. Memoize the value object; split state and dispatch into two contexts so setter-only consumers never rerender.

## React 19

- **Server Components** render on the server, ship zero JS; client components are the interactive leaves. Serialization rules, streaming, and Server Actions: `server-components.md`.
- **`use(promise)`** suspends until resolved and may be called conditionally — the one exception to hook rules. Never create the promise inside a client render (new promise each render suspends forever): create it in the parent or cache it.
- **`ref` is a normal prop** — forwardRef is no longer needed. **`<Context>`** renders as a provider directly. Migration of legacy patterns: `migration.md`.
- **Actions**: `useActionState(action, initial)` returns `[state, formAction, pending]`; `useFormStatus` reads pending from any child of the form — no prop drilling into submit buttons; `useOptimistic` renders the optimistic value and reverts automatically on throw. Worked form example: `forms.md`.

## Performance

Order of operations — measure before touching code (workflow in `performance.md`):

| Priority | Technique | When |
|----------|-----------|------|
| P0 | Route-based code splitting (`lazy` + Suspense) | Always — users pay only for the route they visit |
| P0 | Parallel data loading (`Promise.all`, prefetch) | Any page with 2+ independent fetches — waterfalls dominate load time |
| P1 | Virtualize long lists | Thousands of rows or hundreds of complex rows — profile, DOM nodes are the cost |
| P1 | useDeferredValue / startTransition | Typing or dragging feels janky because a heavy subtree rerenders per keystroke |
| P2 | memo / useMemo by Profiler evidence | Only without React Compiler (→ Core Rule 6) |

## Output Gates

Before emitting a component or review verdict, verify:

- Every list key a stable identity, never the index on reorderable data?
- Every useEffect names an external system; derivable values computed in render?
- `'use client'` only on interactive leaves; no server-only import crossing the boundary?
- Mutations invalidate or update their query keys?
- Interactive elements are native (`button`, `a`, `label`) with accessible names?
- Error path rendered — boundary or explicit error state, not just the happy path?
- New abstraction has a second consumer, or stays concrete?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/react/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| framework | nextjs \| vite \| remix | nextjs | Selects RSC vs SPA guidance: Server Components/Actions sections apply only under an RSC framework; vite switches examples to client-only patterns |
| styling | tailwind \| css-modules \| styled-components | tailwind | Styling used in every component example and scaffold |
| state_library | zustand \| redux-toolkit \| jotai | zustand | Client-state recommendations and store examples in State Management |
| package_manager | npm \| pnpm \| yarn \| bun | npm | Install and script commands in setup and examples |

Preference areas to record as the user reveals them:

- **tooling** — test runner (Vitest/Jest), lint/format stack, monorepo layout — affects `testing.md` examples and scaffold commands
- **conventions** — file naming, folder structure, component patterns beyond the named-export rule — affects generated file layout
- **platform** — SSR requirements, target browsers, deployment target — affects hydration guidance and performance budgets
- **safety posture** — how aggressively to flag legacy patterns and AI mistakes during review (rewrite vs comment) — affects review behavior

Per-project facts (React version, Compiler on/off, stack deviations) belong in `memory.md`, not config — they change per repo, not per user.

## Traps

| Trap | Why it fails | Do instead |
|------|--------------|------------|
| `{count && <X />}` | `0` is falsy but renderable — the page shows a literal 0 | `{count > 0 && <X />}` |
| `key={index}` on lists that reorder/filter | State and DOM stick to the position, not the item — inputs show the wrong values | `key={item.id}` |
| Object/array literal in effect deps | Fresh reference every render → effect fires every render | Depend on primitives, or memoize upstream |
| Mutating state then setState | Same reference — React skips the rerender | New reference: `setArray([...array, item])` |
| Fetch in effect without cancellation | Slow response for the old value overwrites fast response for the new one | `AbortController` in cleanup (below) |
| "My effect runs twice" → deleting StrictMode | Double-mount is dev-only and deliberate: it exposes missing cleanup | Fix the cleanup; keep StrictMode |
| Expecting error boundaries to catch handler/async errors | Boundaries only catch render and lifecycle errors | try/catch in handlers; `onError` in mutations |
| Hydration mismatch | `Date.now()`, `Math.random()`, locale formatting, `typeof window` branches render differently on server vs client | Move to an effect, or `suppressHydrationWarning` on that single element |
| setState during render | Render → setState → render, infinite loop | Compute derived values inline; setState in handlers/effects |
| `useEffect(async () => …)` | Effect must return cleanup or nothing, not a promise | Define an async fn inside and call it |
| Reading state right after setState | State is a snapshot per render — the variable still holds the old value | Use the value you passed, or a functional update; effects react to the next render |

```tsx
// Cancellation — the race-condition fix
useEffect(() => {
  const controller = new AbortController()
  fetch(url, { signal: controller.signal })
    .then((r) => r.json())
    .then(setData)
    .catch((e) => { if (e.name !== 'AbortError') setError(e) })
  return () => controller.abort()
}, [url])
```

## AI Mistakes to Avoid

Patterns generated code gets wrong — check these when reviewing:

| Mistake | Correct pattern |
|---------|-----------------|
| useEffect + useState to derive a value | Compute inline in render (→ Core Rule 2) |
| Fetching in useEffect | TanStack Query, or promise + use() under Suspense |
| Redux/Context for API data | TanStack Query — server state is a cache, not app state |
| Default exports | Named exports (→ Core Rule 5) |
| useCallback/useMemo on everything | Compiler on: none by hand; off: Profiler evidence first (→ Core Rule 6) |
| Generic abstraction on first use (`<DataTable>` for one table) | Write it concrete; abstract at the second real consumer |
| Giant components | Split at ~50 JSX / ~300 file lines (→ Core Rule 8) |
| No error boundaries anywhere | Route level + each risky feature |
| Scattered `any` to silence strict mode | Fix the type; `unknown` + narrowing when truly dynamic (`typescript.md`) |
| `<div onClick>` for interactive elements | Native `button`/`a` — keyboard and focus come free (`accessibility.md`) |
| Testing implementation details (state values, mock call counts) | Test what the user sees: roles, labels, visible output (`testing.md`) |

## Where Experts Disagree

- **Memoize-by-default vs profile-first.** The React Compiler settles it for new code (write none). For pre-compiler codebases: libraries and design systems memoize exports defensively (unknown consumers); apps profile first.
- **RSC-everything vs SPA.** Content and commerce sites win with Server Components (payload, SEO). Dashboard-dense apps behind a login with constant interactivity lose little by staying SPA (Vite) — don't pay the RSC mental tax for zero SEO benefit.
- **Zustand vs Context for shared state.** Context is fine while values change rarely; the crossover is update frequency, not app size. Frequent updates through Context force consumer-tree rerenders that selectors avoid.
- **Feature folders vs type folders.** Type folders (`components/`, `hooks/`) survive only in small apps; beyond a handful of features, colocation by feature keeps change surface local. Default to feature folders (→ setup.md).
- **Form libraries vs platform forms.** A login form needs no library — useActionState + FormData is enough. The crossover is client-side validation complexity and dynamic fields, not form count (`forms.md`).

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/react (install if the user confirms):

- `frontend-design-ultimate` — complete UIs with React + Tailwind
- `typescript` — TypeScript beyond component typing: generics, tsconfig, declaration files
- `nextjs` — Next.js App Router, caching, and deployment
- `testing` — testing strategy beyond components

## Feedback

- If useful, star it: https://clawic.com/skills/react
- Latest version: https://clawic.com/skills/react

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/react.
