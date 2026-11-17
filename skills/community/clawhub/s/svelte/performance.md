# Performance — Rendering Cost, Payload, Perceived Speed

Svelte has no virtual DOM: an update touches the nodes bound to the value that changed. So component-level "memoization" is not a thing here, and the wins come from four places — reactivity shape, list handling, payload size, and navigation strategy.

## Reactivity Cost

- **`$derived` is lazy and memoized**: an expensive derived nobody renders costs nothing, and a rendered one recomputes at most once per change. Deriving is nearly always cheaper than an effect that assigns, which forces a second update pass.
- **Deep proxies cost per property access.** For a 10k-row table you only ever replace wholesale, `$state.raw` removes the proxying entirely; keep `$state` for the small object holding the selection and filters.
- **Narrow the reactive surface.** A single `$state` object read by twenty components means twenty subscriptions to one identity; splitting hot fields into their own state (or deriving them) keeps unrelated updates from waking everything.
- **Effects are the expensive rune** — they run after every dependency change, in a batch, and their cleanup runs too. An effect that reads a whole object subscribes to every property of it; read only the fields you need, or `untrack` the rest.
- Measure before restructuring: `$inspect.trace()` names the dependency that fired, and Chrome's Performance panel shows whether time is in your handlers or in layout.

## Lists

- **Key them** (SKILL.md rule 5). Beyond correctness, an unkeyed list re-patches every row's contents on reorder; a keyed one moves nodes.
- `animate:flip` only works on keyed lists, and it animates transforms — cheap. Animating `top`/`height` per row is not.
- Render windows, not thousands of rows: paginate server-side, or use a virtual list. The cost of 5,000 rows is DOM nodes and layout, which no framework optimizes away.
- Filtering: `let visible = $derived(rows.filter(…))` recomputes once per change; the same filter inline in the template recomputes per render of that block.
- `{#each}` over a derived slice plus `{@const}` inside the block beats recomputing per-row values in three attribute expressions.

## Payload

- SvelteKit **code-splits per route automatically**. A heavy dependency imported by the root layout is in every route's critical path — that is the first thing to check when the initial bundle is large.
- `await import('chart-lib')` inside an effect or an event handler defers a heavy widget until it is needed; pair with a skeleton so the layout does not shift.
- Load data is embedded in the HTML: returning entire ORM rows inflates the document and the hydration cost. Select the columns you render.
- `@sveltejs/enhanced-img` (Vite plugin) generates responsive `srcset` and modern formats at build time for local images; for remote images set explicit `width`/`height` and `loading="lazy"` on everything below the fold.
- Inspect with `npx vite-bundle-visualizer` (or the build output's chunk list) before optimizing by intuition.
- `csr = false` on a genuinely static route ships zero JavaScript for it — the largest possible saving, available on marketing and documentation pages.

## Navigation and Perceived Speed

- Preloading on hover is on by default in the standard template (`data-sveltekit-preload-data="hover"`); it starts the load function while the pointer travels, which typically removes the entire perceived wait for a link click.
- `data-sveltekit-preload-code="viewport"` fetches the JavaScript for links as they scroll into view without running their loads — the cheaper half, for link-dense pages.
- Stream slow secondary data so the shell paints immediately, and give `{#await}` a skeleton with the same dimensions as the result to avoid layout shift.
- Long tasks in `$effect` block the frame like any other JS: chunk them, or move them to a worker (`?worker` import in Vite).
- View Transitions: `onNavigate(() => document.startViewTransition?.(…))` — one hook, and it degrades silently where unsupported.

## Server-Side

- Prerender everything that does not depend on the request: it turns a per-request render into a static file, which no runtime optimization can beat.
- `setHeaders({ 'cache-control': 'public, max-age=60' })` on a load makes a CDN serve the page; reading `cookies` in the same load makes it uncacheable, so decide which one you want.
- The SSR render itself is synchronous string building — the time is almost always in your `await`s. Parallelize them (`Promise.all`) and avoid `await parent()` waterfalls.
- Watch for N+1 queries inside `{#each}`-shaped data: fetch the join once in the load rather than per row.

## Measurement Order

1. Build and preview (`npm run build && npm run preview`) — dev-server numbers are meaningless.
2. Lighthouse or a field-data tool for LCP/INP/CLS: they tell you whether the problem is payload, server time, or interaction.
3. Server time high → load functions (waterfalls, N+1, uncached upstream).
4. Payload high → route-level chunks, root-layout imports, load data size.
5. Interaction lag → effects, unkeyed lists, per-frame `tick` transitions.
6. Layout shift → images without dimensions, skeletons of the wrong size, fonts without `font-display`.

## Performance Traps

| Trap | Cost |
|---|---|
| `$state` over a large parsed dataset | Proxy allocation and per-access overhead — use `$state.raw` |
| Effect that assigns state | An extra update pass per change, and a loop risk |
| Unkeyed `{#each}` | Full content re-patch on reorder, plus state bugs |
| Heavy import in the root layout | Present in every route's critical path |
| Returning full DB rows from load | Bigger HTML, slower hydration, leaked columns |
| `tick`-based custom transitions on lists | JavaScript per frame per node |
| Fetching your own endpoint from a load | An extra network hop that SSR did not need |
| Disabling preloading globally to "save bandwidth" | Trades a measurable interaction win for a hypothetical one |
