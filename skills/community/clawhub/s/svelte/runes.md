# Runes — State, Derived, Effects, Props

**Contents**: [$state](#state) · [$derived](#derived) · [$effect](#effect) · [$props and $bindable](#props-and-bindable) · [$inspect and debugging state](#inspect-and-debugging-state) · [Loops and Their Causes](#loops-and-their-causes) · [Async Reactivity](#async-reactivity)

The whole reactivity system in one page. Runes work in `.svelte` files and in `.svelte.js` / `.svelte.ts` modules — nowhere else (`rune_outside_svelte`).

## $state

```js
let count = $state(0);              // primitive: reassign
let todos = $state([{ done: false }]);  // deep proxy: mutate freely
todos[0].done = true;               // triggers
todos.push({ done: false });        // triggers
```

- Proxying is **lazy and recursive** for plain objects and arrays: nested objects become proxies the first time you read them.
- **Not proxied**: class instances, `Map`, `Set`, `Date`, `URL`, `URLSearchParams`, DOM nodes, anything with a custom prototype. For the built-ins use `svelte/reactivity`: `SvelteMap`, `SvelteSet`, `SvelteDate`, `SvelteURL`, `SvelteURLSearchParams`.
- **In classes**, put `$state` on the field: `class Cart { items = $state([]); get total() { … } }`. Getters recompute on read; the instance itself stays a normal object, so `instanceof` keeps working.
- `$state.raw(value)` — no proxy, reactive only on reassignment. Use for arrays of thousands of rows, parsed blobs, and anything you always replace whole. Mutating a raw value silently does nothing.
- `$state.snapshot(value)` — a plain deep clone. Required whenever a value leaves Svelte: `structuredClone`, `postMessage`, IndexedDB, chart/map/editor libraries, `JSON.stringify` of proxies you want to log.
- Reassigning a whole object is fine and cheap: `settings = { ...settings, theme }`.

## $derived

```js
let doubled = $derived(count * 2);
let filtered = $derived.by(() => {
  return rows.filter(r => r.owner === user.id);   // multi-statement form
});
```

- **Lazy and memoized**: the expression runs on read, and only if a dependency changed. A `$derived` nobody reads costs nothing.
- Must be **pure**. Writing state inside a derived raises `state_unsafe_mutation`; reading its own value raises `derived_references_self`.
- Chains are fine and stay glitch-free: `a → b → c` recomputes in dependency order, once per change.
- A derived is the correct answer to "I need to keep X in sync with Y". If you reached for `$effect` to assign a variable, that variable is a derived (SKILL.md rule 2).
- Deriving from a prop is normal: `let sorted = $derived([...items].sort(cmp))` — do not copy props into `$state` unless the local value is meant to diverge from the parent.

## $effect

```js
$effect(() => {
  const id = setInterval(tick, delay);   // `delay` is a dependency
  return () => clearInterval(id);        // cleanup: before rerun and on destroy
});
```

- Runs **after** the DOM updates, batched in a microtask; `$effect.pre` runs before the update (the `beforeUpdate` replacement, for things like scroll-position measurement).
- **Never runs during SSR.** That is why it is also the browser-API guard (SKILL.md rule 9).
- Dependencies = state read **synchronously** while the body runs. Reads after `await`, inside `setTimeout`, or in `.then()` are invisible (SKILL.md rule 3).
- `untrack(() => …)` reads without subscribing — the escape hatch when an effect legitimately needs a current value it must not react to.
- Outside a component (tests, module init) an effect needs an owner: `const stop = $effect.root(() => { $effect(…) })`, and you call `stop()` yourself.
- `$effect.tracking()` reports whether the current code runs inside a reactive context — useful when writing shared utilities.

Legitimate effects: canvas drawing, `IntersectionObserver`, focus management, persistence to `localStorage`, analytics, syncing a third-party widget. Illegitimate: computing a value, validating a form, transforming props.

## $props and $bindable

```svelte
<script>
  let { title, count = 0, onsave, children, ...rest } = $props();
</script>
```

- Destructuring is the canonical form and stays reactive — the compiler rewrites each read. Renaming (`class: className`) and rest props both work.
- Props are **read-only** by default. Mutating an object a parent passed produces `ownership_invalid_mutation` in dev; the data flows back either through a callback prop (`onsave(value)`) or an explicit binding.
- Two-way binding is opt-in on the child: `let { value = $bindable('') } = $props()`, then the parent writes `<Input bind:value={query} />`. The default in `$bindable(x)` applies only when the parent passes nothing.
- `$props.id()` returns a per-instance unique string — the right way to wire `<label for>`/`aria-describedby` without a global counter that breaks under SSR.
- Callback props replace `createEventDispatcher`: the parent passes `onsave={fn}`, the child calls `onsave?.(payload)`. Typed, tree-shakeable, no bubbling to reason about.

## $inspect and debugging state

- `$inspect(a, b)` logs on every change, dev only, stripped from production builds.
- `$inspect(x).with((type, x) => { if (type === 'update') debugger })` — break exactly on the change you care about.
- `$inspect.trace()` as the first statement of an effect or derived prints which dependency caused the rerun; the fastest way to find why an effect fires more than expected.
- `console.log(stateObject)` prints a `Proxy`; log `$state.snapshot(stateObject)` instead.

## Loops and Their Causes

`effect_update_depth_exceeded` means an update cycle re-triggered itself past the framework's iteration limit. Ordered by frequency:

1. Effect assigns state it also reads → make it a `$derived`.
2. Two effects write each other's dependencies → collapse into one derived, or gate one with `untrack`.
3. Effect writes an object it reads by identity (`obj.x = obj.x + 1` on a proxied object read in the same effect) → read via `untrack`, or move the write to the event that caused it.
4. Effect calls a function that touches state during a derived's recomputation → move the call into an event handler.

## Async Reactivity

Fetching per state change is an effect job, and it races:

```js
let data = $state(null);
$effect(() => {
  const controller = new AbortController();
  const url = `/api/items/${id}`;                     // read the dependency first
  fetch(url, { signal: controller.signal })
    .then(r => r.json())
    .then(json => { data = json; });
  return () => controller.abort();                     // cleanup cancels the stale request
});
```

Without the abort, responses can land out of order and the older one wins. In SvelteKit, prefer a load function for anything tied to the URL — the framework already handles ordering and cancellation.

`svelte >=5.36` with the `experimental.async` compiler option allows `await` directly in components and derived values, with `<svelte:boundary>` supplying a `pending` snippet and `$effect.pending()` reporting in-flight work. Experimental: recommend it only when `experimental_features` is true (SKILL.md Configuration); otherwise mention it exists and write the effect-plus-abort form above.
