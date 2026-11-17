# Shared State — Modules, Context, and Stores

Three mechanisms, three jobs. Picking wrong is how state ends up shared between users or lost on navigation.

| Need | Mechanism |
|---|---|
| App-wide client state (theme, cart, editor) | `$state` in a `.svelte.js` module |
| Per-request or per-subtree state (session, form config, tenant) | `setContext` / `getContext` |
| Push-based external source (socket, geolocation, SDK) | A store, or `createSubscriber` |
| Interop with a library that expects `subscribe` | Store, or `toStore()` over runes |
| Anything read during SSR that differs per user | Context — never a module variable |

## State in a `.svelte.js` Module

Runes work in `.svelte.js` / `.svelte.ts` files, and the export rule catches everyone once:

```js
// ✗ counter.svelte.js — importers see the value at import time
export let count = $state(0);

// ✓ export the container, not the binding
export const counter = $state({ count: 0 });

// ✓ or a class — the idiomatic form
export class Counter {
  count = $state(0);
  increment = () => this.count++;
}

// ✓ or getters when you want a read-only surface
let internal = $state(0);
export const total = { get value() { return internal; } };
```

Consumers write `counter.count++`. No `$` prefix, no subscription, works in plain functions.

**This module is a singleton per process.** In the browser that means per tab — correct. On the server it means per Node process, shared by every concurrent request (SKILL.md rule 4). Module state is safe only for values that are identical for all users: static config, a memoized parse of a bundled file. Anything user-derived goes in context.

## Context

```svelte
<script>
  import { setContext } from 'svelte';
  let { data } = $props();
  const session = $state({ user: data.user });
  setContext('session', session);   // reactive object: children see updates
</script>
```

- `setContext`/`getContext` must be called **synchronously during component initialization** — not in an event handler, not after an `await` (`lifecycle_outside_component`).
- Context is keyed by any value; a `Symbol` or an exported constant avoids collisions across libraries.
- Pass a `$state` object (or a class instance) to keep reactivity; passing a primitive snapshots it.
- Wrap it: export `setSession(data)` / `getSession()` from one module so the key and the type live in one place.
- Context is inherited by the component subtree only — it does not reach load functions, actions, or `+server.js`. Server-side per-request state belongs in `event.locals`.

## Stores (still supported, still useful)

```js
import { writable, readable, derived, get } from 'svelte/store';

export const ticks = readable(0, (set) => {
  const id = setInterval(() => set(Date.now()), 1000);
  return () => clearInterval(id);   // runs when the last subscriber leaves
});
```

- `$ticks` in a component auto-subscribes and auto-unsubscribes on destroy. Manual `store.subscribe()` returns an unsubscribe function you must call — in a component, from `onDestroy`; that leak is invisible until a list of 500 rows mounts and unmounts.
- `get(store)` reads once without subscribing: fine in an event handler, wrong inside markup (no reactivity).
- `derived([a, b], ([$a, $b]) => …)` for combining; the callback's optional `set`/`update` argument plus a returned cleanup covers async derivations.
- A store is any object with a correctly shaped `subscribe`; `store_invalid_shape` means the value you `$`-prefixed is not one — usually a runes object that needs no prefix at all.
- Bridges: `fromStore(store)` gives `.current` readable by runes; `toStore(() => value, v => …)` exposes runes state to store consumers. Use them instead of rewriting a working store layer during a migration.

`createSubscriber` (from `svelte/reactivity`) is the modern way to wrap an external event source in something rune-readable: it starts the subscription on first read inside an effect and tears it down when nothing reads it any more.

## Persisting State

```js
// prefs.svelte.js
export const prefs = $state({ theme: 'system' });

export function loadPrefs() {           // call from an $effect or onMount
  Object.assign(prefs, JSON.parse(localStorage.getItem('prefs') ?? '{}'));
}
export function savePrefs() {           // call from an $effect that reads prefs
  localStorage.setItem('prefs', JSON.stringify($state.snapshot(prefs)));
}
```

Read and write from a component effect, never at module scope: module bodies run during SSR where `localStorage` does not exist. Snapshot before stringifying so the proxy does not leak into the JSON path.

## Choosing, With the Failure Modes

| Choice | Fails when |
|---|---|
| Module `$state` for user session | SSR: request B renders request A's user |
| Context for global theme | Component outside the provider subtree gets `undefined` |
| Store for a value only one component uses | Ceremony with no benefit — plain `$state` in the component |
| Prop drilling through five layers | Refactor to context at the layer that owns the concept |
| `get(store)` inside markup | Renders once, never updates |
