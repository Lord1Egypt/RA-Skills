---
name: Svelte
slug: svelte
version: 1.0.2
description: >-
  Builds, debugs, and reviews Svelte and SvelteKit apps: runes, stores, snippets, load functions, form actions, adapters.
  Use when the UI does not update after a state change, an effect loops forever
  ("effect_update_depth_exceeded"), props or bindings stop reacting, a Map or class field is not
  tracked, state leaks between users on the server, "window is not defined" breaks the build,
  markup mismatches on hydration, data stays stale after a mutation, a form action does nothing or
  returns 403, scoped CSS is pruned as an unused selector, transitions never fire, or a Node,
  Vercel, Cloudflare, or static adapter build fails. Also for migrating Svelte 4 to Svelte 5 runes,
  converting export let to $props, $: to $derived, createEventDispatcher to callback props, slots
  to snippets and on:click to onclick, typing props and route data in TypeScript,
  testing components with Vitest or Playwright, and cutting bundle size and rerender cost.
  Not for Vue or Nuxt, React, or plain browser JavaScript semantics.
homepage: https://clawic.com/skills/svelte
changelog: "Display name shown correctly"
metadata:
  clawdbot:
    emoji: 🔥
    requires:
      bins:
      - node
    os:
    - linux
    - darwin
    - win32
    displayName: Svelte
    configPaths:
    - ~/Clawic/data/svelte/
---

User preferences and memory live in `~/Clawic/data/svelte/` (see `setup.md` on first use, `memory-template.md` for the file format). If you have data at an old location (`~/svelte/` or `~/clawic/svelte/`), move it to `~/Clawic/data/svelte/`.

## When To Use

- Writing or reviewing Svelte components, `.svelte.js` state modules, or SvelteKit routes
- Reactivity failures: UI not updating, effect loops, bindings that stop propagating, stale derived values
- SvelteKit request-layer work: load functions, invalidation, form actions, hooks, `+server.js` endpoints
- Server-only failures: hydration mismatch, `window is not defined`, state shared between requests, adapter build errors
- Migrating a Svelte 4 codebase to Svelte 5 runes, or maintaining a mixed legacy/runes codebase
- Not for Vue or Nuxt (`vue`, `nuxt`), React (`react`), or language-level JavaScript semantics (`javascript`)

## Quick Reference

| Situation | Play |
|-----------|------|
| UI does not update after a change | Is the variable `$state`? Destructured? A `Map`/`Set`/class instance? → Reactivity Model table, then `debug.md` |
| `effect_update_depth_exceeded` | An effect writes state it also reads — convert to `$derived`, or `untrack()` the read (rule 2) |
| Value computed from other state | `$derived` / `$derived.by`; never `$effect` + assignment (rule 2) |
| Deep dive on `$state`, `$derived`, `$effect`, `$props` | `runes.md` |
| Shared state across files, context, legacy stores | `stores.md` |
| Snippets, bindings, callback props, attachments, wrapping an imperative library | `components.md` |
| Scoped CSS not applying, unused-selector warning, transitions, motion | `styling.md` |
| Typing props, snippets, route data, `app.d.ts` | `typescript.md` |
| Symptom-first debugging and the error-code catalog | `debug.md` |
| Svelte 4 → 5: `export let`, `$:`, slots, `on:click`, `new Component()` | `migration.md` |
| Routes, layouts, groups, param matchers, navigation, shallow routing | `routing.md` |
| `load`, `invalidate`, streaming, `depends`, serialization | `data-loading.md` |
| Form actions, `use:enhance`, validation, uploads, remote functions | `forms.md` |
| `window is not defined`, hydration mismatch, per-request state, env vars | `ssr.md` |
| Login, sessions, cookies, route guards, roles, CSRF, XSS, CSP, leaked secrets | `security.md` |
| Bundle size, slow lists, rerender cost, preloading | `performance.md` |
| Vitest, component tests, mocking `$app/*`, Playwright, `svelte-check` | `testing.md` |
| Adapters, prerendering, CSP, service workers, self-hosting | `deployment.md` |
| Packaging components for npm, custom elements, library API design | `library.md` |
| Anything else | Apply Core Rules; reproduce in a single component with no props before blaming the framework |

## Core Rules

1. **Reactivity comes from `$state`, not from assignment.** In runes mode a bare `let count = 0` never re-renders no matter how you assign it — the compiler emits `non_reactive_update`. `let count = $state(0)` then `count++` or `obj.items.push(x)` both work: `$state` on a plain object or array is a deep proxy.
2. **`$derived` for values, `$effect` for the outside world.** Decision rule: if the new value is a pure function of other state → `$derived`; if it touches the DOM, network, storage, or a non-Svelte library → `$effect`. An effect that assigns state costs an extra render pass and is the direct cause of `effect_update_depth_exceeded`.
3. **Effects track only synchronous reads.** Dependencies are collected while the effect body runs to its first `await`; anything read after an `await`, in a `setTimeout`, or in a `.then()` is invisible to the tracker and the effect will not rerun. Read your dependencies at the top, then await.
4. **Module-level state on the server belongs to every user at once.** A `let user = $state(null)` exported from a `.svelte.js` module is one value per Node process, not per request — request A writes it, request B renders it. Per-request data goes in `event.locals` (server) and `setContext`/props (components).
5. **Key every `{#each}` whose items can move.** `{#each rows as row (row.id)}`. Unkeyed, Svelte maps DOM to array index: delete row 0 and the input, focus, and component state of index 0 stay attached to what is now a different row. This is a correctness bug, not an optimization.
6. **Secrets and the database live behind `+page.server.js`.** Universal `+page.js` runs in the browser too, so anything it imports ships. Server load output crosses the wire through devalue serialization: `Date`, `Map`, `Set`, `BigInt`, and cycles survive; class instances and functions do not (register them with the `transport` hook).
7. **A load function reruns only for what it read.** Rerun happens when: a `params` or `url` property it accessed changes, OR an `invalidate(key)` matches something it `depends()` on or a URL it fetched, OR a parent it `await parent()`-ed reran, OR `invalidateAll()` fired. After any mutation outside `use:enhance`, call `invalidateAll()` yourself or the page keeps serving the old data.
8. **Mutations go through form actions, not fetch handlers.** `<form method="POST" action="?/save">` works with JavaScript disabled and on the first paint; `use:enhance` upgrades the same form to a fetch with no reload and reinvalidates data on success. Reach for a `+server.js` endpoint only for non-form clients: webhooks, third parties, file streaming.
9. **Guard browser APIs by phase, not by try/catch.** `$effect` and `onMount` never run during SSR — that is the guard. Module scope and load functions run on the server, so `window`, `document`, `localStorage`, and `IntersectionObserver` there need `import { browser } from '$app/environment'` or a dynamic `import()`.

## Reactivity Model

What is tracked, and what silently is not:

| Declaration | Reactive on | Rule |
|---|---|---|
| `let x = $state(0)` | reassignment | Primitives: assign to update |
| `let o = $state({a: {b: 1}})` | reassignment + deep mutation | Plain objects/arrays become recursive proxies; `o.a.b = 2` and `arr.push()` both work |
| `$state.raw(bigList)` | reassignment only | No proxy: cheaper for large data you replace wholesale |
| `new Map()`, `Set`, `Date`, `URL` inside `$state` | nothing | Not proxied — use `SvelteMap`, `SvelteSet`, `SvelteDate`, `SvelteURL` from `svelte/reactivity` |
| Class field `count = $state(0)` | reassignment | Methods and `get` accessors stay reactive; the instance itself is not a proxy |
| `let { a, b = 1 } = $props()` | parent updates | Destructuring props IS reactive in runes mode — the compiler rewrites the reads |
| `const { a } = someStateObject` | nothing | Destructuring state reads the value once; keep the object, or wrap in `$derived` |
| Exported `let x = $state(0)` from a module | not across the import | Importers get a snapshot binding — export an object, a class instance, or a getter |
| `let x = 0` in a runes file | nothing | Compiler warning `non_reactive_update` |

Passing state to a non-Svelte library (`structuredClone`, IndexedDB, `postMessage`, charting libs) hands it a `Proxy`; send `$state.snapshot(x)` instead.

## Version Gates

- `svelte >=5` — runes, snippets, `onclick` event attributes, `mount()`/`unmount()`; `$:`, `export let`, slots, and `new Component()` only work in legacy mode
- `svelte >=5.3` — `<svelte:boundary>` with `failed` snippet and `onerror`
- `svelte >=5.29` — attachments (`{@attach fn}`) supersede actions (`use:fn`); actions still work
- `svelte >=5.36` — experimental `await` inside components and `$effect.pending()`, behind the `experimental.async` compiler option
- `@sveltejs/kit >=2` — `error()` and `redirect()` throw internally: call them, never `throw` them; `cookies.set` requires an explicit `path`
- `@sveltejs/kit >=2.12` — `$app/state` (`page`, `navigating`, `updated`) replaces the `$app/stores` subscriptions; `page.url`, not `$page.url`
- `@sveltejs/kit >=2.16` — `PageProps` and `LayoutProps` in `./$types`; below it, type `$props()` with `{ data: PageData; form: ActionData }`
- `@sveltejs/kit >=2.27` — remote functions (`query`, `form`, `command`) in `.remote.js`, behind `experimental.remoteFunctions`

## Where Code Runs

| File | Runs | Can hold secrets | Shipped to browser |
|---|---|---|---|
| `+page.svelte`, `+layout.svelte` | SSR render, then client | No | Yes |
| `+page.js` (universal load) | Server on first load, client on navigation | No | Yes |
| `+page.server.js` (server load, actions) | Server only | Yes | No |
| `+server.js` (endpoint) | Server only | Yes | No |
| `hooks.server.js` | Server, every request | Yes | No |
| `hooks.client.js` | Browser only | No | Yes |
| `$lib/server/**`, `*.server.js` | Server only | Yes | Import from client code = build error |

Order per request: `handle` hook → server loads (`+layout.server.js`, then `+page.server.js`) → universal loads → render. Loads at the same level run in parallel unless one calls `await parent()`, which serializes it behind the parent.

## Error Codes

| Code or message | Meaning | First move |
|---|---|---|
| `state_unsafe_mutation` | State written while a derived or the template was computing it | Move the write into an event handler or `$effect` |
| `effect_update_depth_exceeded` | An effect writes state that it (or a chained effect) reads | Convert to `$derived`; if the read is genuinely one-way, wrap it in `untrack()` |
| `hydration_mismatch` | Server HTML differs from the first client render | Remove `Date.now()`/`Math.random()`/`window` from render; check invalid nesting (`<div>` inside `<p>`) |
| `rune_outside_svelte` | A rune used in a `.js`/`.ts` file | Rename the file to `.svelte.js` / `.svelte.ts` |
| `lifecycle_outside_component` | `onMount`, `setContext`, or `getContext` called after an `await` or inside a callback | Call synchronously during component initialization |
| `derived_references_self` | A `$derived` reads its own value | Compute from source state, or keep the accumulator in `$state` |
| `each_key_duplicate` | Two items produced the same key | Key by a unique id; never by index or by a repeated value |
| `bind_invalid_export` / binding error | `bind:` to a prop the child did not declare bindable | `let { value = $bindable() } = $props()` |
| `ownership_invalid_mutation` (dev warning) | A child mutated an object owned by its parent | `$bindable()` or a callback prop |
| `css_unused_selector` (warning) | Selector matches nothing in this component's own markup | `:global(...)`, or move the rule into the child component |
| `403` on a form POST | Kit's CSRF origin check rejected a cross-origin submission | Submit same-origin, or set `csrf.checkOrigin` deliberately |
| `Cannot import $lib/server/... into client-side code` | A server-only module reached a client bundle | Import it in `+page.server.js` and pass the result through load |

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/svelte/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| syntax_mode | runes \| legacy \| mixed | runes | Selects the syntax of every generated component (`$state`/`$props` vs `let`/`export let`) and whether migration advice is offered at all |
| kit_project | bool | true | When false, drops routing, load, actions, and adapter guidance and treats the app as Svelte + Vite with client-side routing |
| deployment_adapter | auto \| node \| static \| vercel \| cloudflare \| netlify | auto | Drives the deploy checklist, which env-var mechanism is valid, and whether prerender/SPA fallback is required |
| package_manager | npm \| pnpm \| yarn \| bun | npm | Sets the command syntax in install, `sv add`, build, and test instructions |
| styling | scoped-css \| tailwind \| unocss \| css-modules | scoped-css | Shapes generated markup and which scoped-CSS caveats apply |
| typescript | bool | true | Emits `<script lang="ts">`, typed `$props()`, and `./$types` imports; false switches to JSDoc annotations |
| experimental_features | bool | false | When false, remote functions, `experimental.async`/`$effect.pending()`, and attachments-over-actions are mentioned as available but never the recommended form; when true they are written by default |
| check_threshold | error \| warning | error | The `svelte-check --threshold` value in every CI recipe, and whether a warning-level finding blocks the work |

Preference areas to record as the user reveals them:

- **conventions** — component and route file naming, folder layout, `$lib` structure, barrel files
- **stack** — form validation library, ORM or data client, auth approach, i18n, component library
- **progressive enhancement** — whether the app must work with JavaScript disabled; decides form-action vs client-fetch mutations
- **accessibility posture** — treat compiler a11y warnings as errors, or advisory
- **testing strategy** — component tests in browser mode vs jsdom, and the unit/e2e split
- **risk posture** — appetite for experimental and just-released APIs beyond `experimental_features`, upgrade cadence, and whether to propose a migration on a codebase that currently works
- **budgets** — bundle-size and first-load targets, coverage floor, and any perf number the project gates on beyond `check_threshold`
- **output format** — explanation depth (fix only vs walkthrough), full files vs diffs, comment density in generated code
- **proactivity** — how eagerly to flag reactivity, boundary, and bundle issues versus answering only what was asked

## Output Gates

Before emitting a component or route, verify:

- Every mutable value declared with `$state`; no bare `let` expected to rerender?
- Every computed value a `$derived`, with `$effect` reserved for DOM, network, storage, or third-party libraries?
- Every `{#each}` over reorderable data keyed by a stable id?
- No secret, database client, or `$env/static/private` import reachable from `+page.svelte` or `+page.js`?
- Mutations expressed as a form action that still works with JavaScript disabled?
- Browser APIs only inside `$effect`/`onMount` or behind a `browser` check?
- Per-request data in `event.locals` or context — never a module-level variable?
- One syntax mode per file: no `export let` or `$:` in a file that uses runes?

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| `$effect` used to compute derived state | Extra render pass and a loop the moment the effect reads what it writes | `$derived` / `$derived.by` |
| Destructuring a `$state` object, then mutating the copy | The destructured constants captured values, not the proxy | Keep the object and read `o.a`; `$derived` for a stable view |
| `let count = $state(0)` exported from a `.svelte.js` module | Importers bind to the value at import time | Export a class instance or `{ get count() {...} }` |
| Per-user data in a server module variable | One value per process, shared by all concurrent requests | `event.locals` in hooks, `setContext` in components |
| `throw redirect(...)` / `throw error(...)` inside a `try` | Kit 2 helpers throw internally; your `catch` swallows the control flow | Call them after the try/catch block |
| Fetching your own `+server.js` from a server load | An extra HTTP hop, lost types, cookie forwarding you now own | Call the function or database directly in server load |
| `{@html userInput}` | XSS, and component-scoped styles do not apply to injected markup | Sanitize server-side; style with `:global` |
| Passing `$state` straight to a chart or map library | The library receives a `Proxy` and its identity checks fail | `$state.snapshot(value)` |
| `await` early in an `$effect`, then reading state | Reads after the await are untracked; the effect never reruns | Read every dependency synchronously first |
| `on:click` or `createEventDispatcher` in a runes component | Legacy syntax; the runes compiler rejects or deprecates it | `onclick={...}` and callback props |
| `<svelte:component this={C}>` in runes mode | Deprecated: components are already dynamic values | Capitalized variable: `<C />` |
| `bind:value` to a prop the child never declared bindable | Bindings are opt-in in runes mode | `let { value = $bindable() } = $props()` |
| `document` or `window` at module scope | Module bodies execute during SSR | Move into `$effect`/`onMount`, or guard with `browser` |
| Unkeyed `{#each}` around inputs or stateful children | DOM nodes are reused by index | Key by id (rule 5) |

## Where Experts Disagree

- **Runes vs stores for shared state.** Default: a class or object with `$state` fields in a `.svelte.js` module — plain values, no `$` prefix, works outside components. Stores remain the right shape for push-based external sources (sockets, geolocation, third-party subscriptions) and for anything consuming the `subscribe` contract; `fromStore`/`toStore` bridge the two rather than forcing a rewrite.
- **How much `$effect` is acceptable.** The framework position is that effects are a last resort for synchronizing with systems outside Svelte; the pragmatic position accepts effects for analytics, logging, and persistence. Both agree on the hard line: an effect that assigns state which feeds back into its own dependencies is a bug, not a style choice.
- **SSR by default vs SPA.** Prerendering or SSR wins for public, indexable, first-paint-sensitive pages. `adapter-static` with `ssr = false` is a legitimate choice for an internal dashboard behind auth where every view needs the client anyway — the deciding factors are SEO, first paint, and no-JS support, not fashion.
- **Validation libraries in form actions.** Hand-rolled checks are fine for one to three fields. Once you need repopulating on failure, nested data, arrays, or multi-step wizards, a schema library plus a form helper stops the per-field boilerplate from drifting out of sync with the server.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/svelte (install if the user confirms):
- `typescript` — type-system depth beyond the Svelte-specific typings
- `vite` — dev server, plugins, and build configuration under SvelteKit
- `playwright` — end-to-end testing of the running app
- `tailwindcss` — utility styling inside Svelte components
- `nodejs` — running and hardening the `adapter-node` server

## Feedback

- If useful, star it: https://clawic.com/skills/svelte
- Latest version: https://clawic.com/skills/svelte

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/svelte.
