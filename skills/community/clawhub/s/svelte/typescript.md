# TypeScript in Svelte and SvelteKit

`<script lang="ts">` is type-checked by `svelte-check`, not by `tsc` — `.svelte` files are invisible to a plain `tsc --noEmit`. CI runs both.

## Typing Props

```svelte
<script lang="ts">
  import type { Snippet } from 'svelte';

  interface Props {
    title: string;
    count?: number;
    variant?: 'primary' | 'ghost';
    onsave?: (value: string) => void;
    children?: Snippet;
    row?: Snippet<[item: Item]>;          // snippet with arguments
  }

  let { title, count = 0, variant = 'primary', onsave, children, row }: Props = $props();
</script>
```

- Type the destructuring, not the rune: `let { … }: Props = $props()`.
- Bindable props: `let { value = $bindable('') }: { value?: string } = $props()` — the type is the value's type; bindability is not part of it.
- Extending element attributes for a wrapper component:
  `interface Props extends HTMLButtonAttributes { loading?: boolean }` from `svelte/elements` (`HTMLInputAttributes`, `HTMLAnchorAttributes`, and the rest live there).
- Generic components: `<script lang="ts" generics="T extends { id: string }">` puts `T` in scope for the whole component, so `items: T[]` and `row: Snippet<[T]>` stay linked.
- `ComponentProps<typeof Button>` extracts a component's props for wrappers and tests; `Component` is the type of a component value (Svelte 5 components are functions, not classes — `SvelteComponent` is the legacy type).

## Typing State

- `let user = $state<User | null>(null)` — the type argument goes on the rune when inference has nothing to work with.
- `$state` on a class field infers from the initializer; annotate the field when it starts empty: `items: Item[] = $state([])`.
- `$derived` infers; annotate only to force a wider type.
- `$props.id()` returns `string`; `$bindable()` returns the prop type.

## SvelteKit's Generated Types

```ts
// src/routes/blog/[slug]/+page.server.ts
import type { PageServerLoad, Actions } from './$types';

export const load: PageServerLoad = async ({ params, locals }) => {
  return { post: await db.post(params.slug) };   // params.slug is typed from the folder name
};

export const actions: Actions = { … };
```

- `./$types` is generated per route by `svelte-kit sync` (run automatically by `dev` and `build`; run `npx svelte-kit sync` by hand after a fresh clone or when the editor shows "Cannot find module './$types'").
- Available per route: `PageLoad`, `PageServerLoad`, `LayoutLoad`, `LayoutServerLoad`, `Actions`, `RequestHandler`, `EntryGenerator`, plus `PageProps` and `LayoutProps` (`@sveltejs/kit >=2.16`).
- In `+page.svelte`: `let { data, form }: PageProps = $props()` — `data` is the merged type of every load feeding the route, so a field added in a layout load appears in the page automatically. Below `@sveltejs/kit >=2.16` those two types are not generated: write `let { data, form }: { data: PageData; form: ActionData } = $props()` importing both from `./$types`.
- Route params come from the directory structure; a rest param is `string`, an optional param is `string | undefined`.

## `app.d.ts` — the Four Global Slots

```ts
declare global {
  namespace App {
    interface Locals { user: User | null }          // set in hooks, read in server load/actions
    interface PageData { flash?: string }           // fields present on many pages
    interface Error { code?: string }               // shape of the object in +error.svelte
    interface Platform { env: { KV: KVNamespace } } // adapter-provided runtime bindings
  }
}
export {};
```

Filling `Locals` is what makes `event.locals.user` typed everywhere; leaving it empty is why so many codebases cast in every load function.

## Module and Asset Declarations

- `$env/static/private` and `$env/static/public` are typed from your `.env` files after `svelte-kit sync` — a missing variable is a build-time type error, which is the point.
- Untyped imports (`.svg?raw`, `.md`, worker files) need a `declare module '*.svg?raw'` block in `src/app.d.ts` or a dedicated `.d.ts`.
- `.svelte.ts` modules are type-checked like normal TypeScript; runes inside them are recognized by the Svelte language tools, not by `tsc`.

## Checking and CI

| Command | Catches |
|---|---|
| `npx svelte-check --tsconfig ./tsconfig.json` | Type errors, a11y and unused-CSS warnings inside `.svelte` |
| `npx svelte-check --threshold error --output human` | CI gate that ignores warnings but fails on errors (`check_threshold` in the SKILL.md Configuration table) |
| `npx tsc --noEmit` | `.ts` files only — not a substitute |
| `npx svelte-kit sync` | Regenerates `./$types` when the editor disagrees with reality |

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| `export let x: string` alongside runes | Mixing modes in one file | `let { x }: Props = $props()` |
| Casting `data as MyType` in `+page.svelte` | Hides a real mismatch between load and page | Fix the load return type; `PageProps` follows |
| Typing a component as `SvelteComponent` | Svelte 5 components are functions | `Component` or `ComponentProps<typeof X>` |
| `any` on `event.locals` | `App.Locals` was never filled | Declare it once in `app.d.ts` |
| Trusting `tsc` alone in CI | `.svelte` files are not type-checked by it | Add `svelte-check` to the same job |
| Annotating a `$derived` with a narrower type | Silently masks a widened source | Fix the source state's type |

For type-system depth beyond these Svelte-specific bindings — generics, narrowing, declaration files — the `typescript` skill in SKILL.md Related Skills is the deeper reference.
