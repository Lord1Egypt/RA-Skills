# Migrating Svelte 4 to Svelte 5

Svelte 5 runs Svelte 4 syntax. Nothing forces a rewrite: mode is **per file**, so a codebase can be half-migrated for months. Migrate a file when you touch it, and convert leaf components before their parents.

## Run the Codemod First

```bash
npx sv migrate svelte-5
```

It rewrites the mechanical cases: `export let` → `$props()`, `$:` → `$derived`/`$effect`, `on:x` → `onx`, `createEventDispatcher` → callback props, slots → snippets, component instantiation → `mount()`. Review the diff — the cases it deliberately leaves alone are exactly the ones listed below.

## The Translation Table

| Svelte 4 | Svelte 5 | Watch for |
|---|---|---|
| `export let title` | `let { title } = $props()` | Required props are no longer implied; add defaults deliberately |
| `export let value = 0` + parent binds | `let { value = $bindable(0) } = $props()` | Bindings are opt-in now; a missed `$bindable` breaks the parent |
| `let count = 0` | `let count = $state(0)` | A plain `let` becomes non-reactive |
| `$: doubled = count * 2` | `let doubled = $derived(count * 2)` | Only assignments convert cleanly |
| `$: { sideEffect(count) }` | `$effect(() => sideEffect(count))` | Effects run after DOM update; `$:` ran before |
| `$: if (x) …` | `$effect(() => { if (x) … })` | Or restructure as a derived condition |
| `beforeUpdate` | `$effect.pre` | Different timing granularity — per dependency, not per render |
| `afterUpdate` | `$effect` | Same |
| `on:click={fn}` | `onclick={fn}` | No colon |
| `on:click\|preventDefault` | Handler calls `e.preventDefault()` | Modifiers are gone |
| `on:custom` from a child | `oncustom` callback prop | No bubbling; the child calls the function |
| `createEventDispatcher()` | Callback props | `dispatch('save', d)` → `onsave?.(d)` |
| `<slot />` | `{@render children?.()}` | `children` is a normal prop |
| `<slot name="row" {item} />` | `{@render row?.(item)}` + `{#snippet row(item)}` | Snippet arguments replace slot props |
| `$$slots.footer` | `if (footer)` | Snippet props are just values |
| `$$props` / `$$restProps` | `let { ...rest } = $props()` | Explicit rest |
| `<svelte:component this={C} />` | `<C />` | Variable must be capitalized |
| `<svelte:self />` | Import the file by name | Self-import is legal |
| `new Component({ target })` | `mount(Component, { target })` | Also `hydrate()` and `unmount()` |
| `component.$set(props)` | `$state` object passed as props | Mutate the object you passed |
| `component.$on('x', fn)` | Pass `onx` in props | Or `events` option of `mount` |
| `component.$destroy()` | `unmount(instance)` | Returns a promise when outros are pending |
| `svelte:options accessors` | Exported functions or `$bindable` | Accessors are legacy-only |
| `tweened` / `spring` stores | `new Tween()` / `new Spring()` | `.current` to read, `.target` to set |
| Transitions global by default | Local by default | Add `\|global` where an ancestor toggle should animate |

## What the Codemod Cannot Decide

- **`$:` that both computes and side-effects.** `$: { total = sum(items); localStorage.setItem(…) }` splits into a `$derived` and an `$effect`. Copying it wholesale into one `$effect` recreates the loop problem the runes were designed to remove.
- **`$:` ordering tricks.** Svelte 4 topologically sorted reactive statements and reran them per render pass; code that relied on a statement running after another in the same tick needs restructuring into explicit derivations.
- **Stores used as component-local state.** `const x = writable(0)` inside a component is just `let x = $state(0)`. Stores that cross files can stay stores — nothing breaks (see the shared-state guidance in the SKILL.md router).
- **Props mutated by the child.** Svelte 4 tolerated it; Svelte 5 warns (`ownership_invalid_mutation`) because it is a data-flow bug. Convert to `$bindable` or a callback.
- **Deep reactivity that used to require reassignment.** `arr = arr` after a push is now unnecessary but harmless; leave it or clean it, do not chase it.
- **`bind:` chains through several layers.** Every layer must declare `$bindable`; two-way bindings three levels deep are usually the wrong design — pass a callback or lift the state.

## Mixed-Mode Rules

- One mode per file: a file that uses any rune must not use `export let`, `$:`, `$$props`, or `<slot>`.
- A runes component can render a legacy component and vice versa; props and content cross the boundary normally. The exception is slot/snippet shape: a legacy child needs `<slot>` content, a runes child needs a snippet.
- Legacy stores work unchanged in runes components; `$store` still auto-subscribes.
- Pin an ambiguous file with `<svelte:options runes={true} />` — useful for a component with no state where the mode is otherwise undetectable.
- Third-party components compiled for Svelte 4 keep working; check the library's peer range before assuming.

## SvelteKit Upgrades Along the Way

| Old | New |
|---|---|
| `import { page } from '$app/stores'` + `$page` | `import { page } from '$app/state'` + `page` (`@sveltejs/kit >=2.12`) |
| `throw redirect(303, '/')` | `redirect(303, '/')` (`@sveltejs/kit >=2` throws internally) |
| `throw error(404)` | `error(404)` |
| `cookies.set(name, value)` | `cookies.set(name, value, { path: '/' })` — path is now required |
| `npm create svelte@latest` | `npx sv create` |
| `use:action` with `update`/`destroy` | `{@attach fn}` returning a cleanup (`svelte >=5.29`) |

## Migration Order That Avoids Rework

1. Upgrade dependencies and get the app running unchanged on Svelte 5 — legacy mode is fully supported, so this step should be boring.
2. Run `npx svelte-check` and fix deprecation warnings that have mechanical fixes.
3. Convert **leaf** components (no children, no bindings) — pure `$props`/`$state` translations.
4. Convert components with slots into snippets, updating every caller in the same commit; slot-to-snippet is the only change that breaks the interface between two files at once.
5. Convert stateful containers and stores last, when you can see which state is genuinely shared.
6. Delete `$:`-era workarounds: manual `arr = arr` reassignments, `tick()` calls that existed to sequence reactive statements, store-in-component ceremony.
