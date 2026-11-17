# Debugging — Symptom to Cause

Work symptom-first. Each chain is ordered by how often the cause turns out to be the culprit, and every step is a check you can run in under a minute.

## The Universal First Three

1. **Which mode is this file in?** A file is runes mode if it uses any rune, legacy mode otherwise. `$:` in a runes file does nothing useful; `$state` in a legacy file is a compile error. `<svelte:options runes={true} />` settles it explicitly.
2. **Read the compiler output.** `non_reactive_update`, `css_unused_selector`, `state_referenced_locally`, and the a11y warnings each name the bug directly. Warnings scroll past in the dev server; run `npx svelte-check` to see them all at once.
3. **`$inspect(value)`** on the suspect state, then `$inspect.trace()` as the first line of the effect or derived that misbehaves — it prints which dependency triggered the run. Both are dev-only and stripped from production builds.

## UI Does Not Update

1. Is the variable `$state`? A bare `let` in runes mode never rerenders — the compiler already warned `non_reactive_update`.
2. Was it destructured? `const { rows } = data` captures the value. Keep the object (`data.rows`) or wrap it in `$derived`.
3. Is the mutated thing proxyable? `Map`, `Set`, `Date`, `URL`, and class instances are not — use the `svelte/reactivity` equivalents, or reassign the whole value.
4. Is it `$state.raw`? Then only reassignment counts; the mutation you just made was a no-op.
5. Did it cross a module boundary? `export let x = $state(0)` gives importers a dead binding — export an object, class, or getter.
6. Is it a prop the parent never changes? Log the value in the parent; a stale prop is a parent bug, and mutating it in the child raises `ownership_invalid_mutation`.
7. Is the update inside an untracked region — after an `await` in an effect, in a `setTimeout`, in a `.then()`? The write still lands; the rerun does not fire because the read was never registered.
8. Is the value rendered through `{@html}` or drawn by a third-party library? Svelte does not own that DOM: re-render it yourself in an effect keyed on the state.

## Effect Runs Forever (`effect_update_depth_exceeded`)

1. Does the effect assign state it also reads? That is the bug in most cases — the value is a `$derived`.
2. Two effects updating each other's inputs: collapse to one derived, or `untrack()` the read that must not subscribe.
3. Object identity: assigning a fresh object every run (`config = { ...config }`) invalidates every dependent, including the effect itself.
4. A function called from the effect writes state as a side effect — follow the call, not just the effect body.
5. Genuine one-way sync (persistence, analytics): read the dependencies you want to track, `untrack` everything else, and confirm with `$inspect.trace()`.

## Props Or Bindings Stopped Working

| Symptom | Cause | Fix |
|---|---|---|
| Child ignores parent updates | Prop copied into `$state` at init | Use the prop directly, or `$derived` |
| `bind:` throws or does nothing | Prop not declared `$bindable()` | `let { value = $bindable() } = $props()` |
| Dev warning about mutating a prop | Child mutates an object the parent owns | Callback prop, or `$bindable` |
| Spread props do not reach the element | Rest not spread, or a named prop shadows it | `let { class: cls, ...rest } = $props()` then `{...rest}` |
| `bind:this` is `null` | Read during render | Read in `$effect`/`onMount` |
| Snippet renders nothing | Called without optional chaining, or shadowed by a same-named prop | `{@render row?.(item)}`, rename the prop |

## Server-Only Failures

- **`window is not defined` / `document is not defined`** — module-scope browser access. Move it into `$effect`/`onMount`, or guard with `browser` from `$app/environment`; for a library that touches the DOM on import, `await import('lib')` inside the effect.
- **Hydration mismatch** — the server rendered different HTML than the client's first pass. Sources, in order: `Date`/`Math.random`/`crypto.randomUUID` in render; locale or timezone formatting; reading `localStorage` for an initial value; invalid HTML nesting the browser silently repairs (`<div>` inside `<p>`, `<a>` inside `<a>`, stray whitespace in `<table>`); a browser extension injecting nodes.
- **Data from one user shown to another** — module-level state on the server (SKILL.md rule 4). Grep for `$state` at module scope in `.svelte.js` files, and for module-level caches keyed by nothing.
- **Works in `dev`, fails in `build`** — dev is unbundled and lenient: a server-only import that dev tolerated now fails the client bundle, and `$env/dynamic/*` is unavailable during prerendering.

## Data Is Stale After a Mutation

1. Did anything invalidate? `use:enhance` invalidates on success by default; a hand-rolled `fetch` does not — call `invalidateAll()` or `invalidate(key)`.
2. Does the load depend on what you invalidated? A load only reruns for URLs it fetched, `depends()` keys it registered, params it read, or an awaited parent that reran.
3. Custom `use:enhance` callback: returning your own handler replaces the default behavior — you must call `update()` or `applyAction(result)` yourself.
4. Reading `data` into `$state` in the component: it froze at first render. Read `data.x` directly, or `$derived`.
5. Browser back/forward shows old data: client navigation reuses the data captured for that history entry. If the page must always be fresh, call `invalidateAll()` from `afterNavigate`.

## Form Action Does Nothing

| Check | Detail |
|---|---|
| `method="POST"` present | A GET form navigates and silently ignores the action |
| Action name matches | `action="?/save"` must match the key in `export const actions` |
| Default plus named actions | Cannot coexist — a form posting to a default action while named ones exist errors |
| 403 response | Kit's CSRF origin check: the submission came from another origin |
| Fields have `name` attributes | `formData.get('email')` returns `null` without them |
| File upload empty | Missing `enctype="multipart/form-data"` |
| Nothing in `form` prop | Action returned nothing, or returned via `error()` instead of `fail()` |
| Redirect swallowed | `redirect()` called inside a `try` whose `catch` handles it |

## Styles Not Applying

1. Compiler said `css_unused_selector`: the selector matches no element in this component's markup.
2. Target is inside a child component or `{@html}` output → `:global()`, a `class` prop, or CSS custom properties.
3. Specificity: the scoping class raises specificity, so a global rule you expected to win may lose.
4. Transition never plays: the directive sits on a wrapper that is never added or removed, or an ancestor block toggles and the transition is local by default in Svelte 5 (`|global`).

## Build and Tooling Errors

| Message | Meaning |
|---|---|
| `rune_outside_svelte` | Runes used in `.js`/`.ts` — rename to `.svelte.js` |
| `Cannot find module './$types'` | Run `npx svelte-kit sync` |
| `Cannot import $lib/server/... into client-side code` | Import chain reaches a client bundle; move it behind a server load |
| `500` only after `build` | Adapter or env difference: check `$env/dynamic` usage and prerender settings |
| `store_invalid_shape` | `$`-prefixed something that is not a store — runes state needs no prefix |
| `lifecycle_outside_component` | `onMount`/`getContext` called asynchronously or outside init |

## When You Are Truly Stuck

Rebuild the failure in isolation: one component, `$state` inline, no props, no load. If it reproduces, the bug is in the reactivity model above. If it does not, add back one layer at a time — props, then load data, then SSR (`npm run build && npm run preview`) — and the layer that breaks it names the file to open next from the SKILL.md router.
