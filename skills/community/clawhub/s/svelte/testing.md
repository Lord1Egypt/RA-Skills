# Testing Svelte and SvelteKit

**Contents**: [Setup](#setup) · [Testing Runes](#testing-runes) · [Component Tests](#component-tests) · [Mocking the SvelteKit Environment](#mocking-the-sveltekit-environment) · [Testing Load Functions and Actions](#testing-load-functions-and-actions) · [End-to-End](#end-to-end) · [Static Checks in CI](#static-checks-in-ci) · [What to Test, in Priority Order](#what-to-test-in-priority-order)

Four layers, cheapest first: plain functions, runes in isolation, components, end-to-end. Most Svelte bugs that reach production are boundary bugs (load, actions, SSR), which is why the middle two layers are worth less here than in a client-only framework and the outer two are worth more.

## Setup

```bash
npx sv add vitest       # wires vitest + the Svelte plugin into an existing project
```

- Component tests run either in a real browser (`vitest-browser-svelte`, Playwright-driven, the current default from `sv create`) or in jsdom with `@testing-library/svelte`. Browser mode gives real layout, focus, and pointer behavior; jsdom is faster and enough for logic-heavy components.
- Split the Vitest config into two projects — a `client` project for `*.svelte.test.ts` and a `server` project for `*.test.ts` — so server code is not loaded into a browser environment.
- **File naming matters**: a test that uses runes at the top level must live in a `.svelte.test.ts` / `.svelte.js` file, otherwise the compiler never processes it and you get `rune_outside_svelte`.

## Testing Runes

```ts
// counter.svelte.test.ts
import { flushSync } from 'svelte';
import { Counter } from './counter.svelte.js';

test('increments', () => {
  const c = new Counter();
  c.increment();
  expect(c.count).toBe(1);        // derived/state read synchronously: no flush needed
});

test('effect fires', () => {
  const cleanup = $effect.root(() => {
    let doubled = $derived(c.count * 2);
    $effect(() => log.push(doubled));
  });
  c.increment();
  flushSync();                     // effects are batched; force them now
  cleanup();                       // $effect.root owns the teardown
});
```

- Effects need an owner outside a component: `$effect.root` returns the cleanup, and forgetting to call it leaks between tests.
- `flushSync()` applies pending updates synchronously; `await tick()` is the async equivalent inside components.
- State classes in `.svelte.js` modules are the easiest thing in the codebase to test — that is an argument for putting logic there rather than in components.

## Component Tests

```ts
import { render } from 'vitest-browser-svelte';   // or '@testing-library/svelte'
import { expect, test, vi } from 'vitest';
import Button from './Button.svelte';

test('calls onclick with the payload', async () => {
  const onclick = vi.fn();
  const screen = render(Button, { label: 'Save', onclick });
  await screen.getByRole('button', { name: 'Save' }).click();
  expect(onclick).toHaveBeenCalledOnce();
});
```

- Props are passed as a plain object; to change them mid-test pass a `$state` object and mutate it, or use the returned `rerender`.
- Query by role and accessible name, not by class — the query doubles as an accessibility assertion.
- Snippets as props: pass `createRawSnippet` output, or wrap the component in a small test-only `.svelte` harness, which is usually clearer.
- Two-way bindings and slots are the components most worth a harness component; everything else can be driven from props.

## Mocking the SvelteKit Environment

```ts
vi.mock('$app/state', () => ({
  page: { url: new URL('http://localhost/blog/hello'), params: { slug: 'hello' }, data: {} },
  navigating: null
}));

vi.mock('$app/navigation', () => ({ goto: vi.fn(), invalidateAll: vi.fn() }));
vi.mock('$app/environment', () => ({ browser: true, dev: true, building: false }));
vi.mock('$env/static/private', () => ({ DATABASE_URL: 'postgres://test' }));
```

`$app/state` exports plain values (`@sveltejs/kit >=2.12`), so mocking it is a plain object; the older `$app/stores` exports stores, so its mock needs `subscribe`. Mixing the two mocks in one suite is a common source of "page is not a store".

## Testing Load Functions and Actions

They are ordinary async functions — call them directly with a hand-built event, no framework needed:

```ts
const result = await load({
  params: { slug: 'hello' },
  locals: { user: { id: 1 } },
  fetch: vi.fn().mockResolvedValue(new Response('{}')),
  depends: vi.fn(),
  parent: async () => ({ settings: {} })
} as any);

expect(result.post.title).toBe('Hello');
```

- Actions: build a `Request` with a real `FormData` body and assert on the returned `fail()` payload or the thrown redirect (`isRedirect(e)` / `isHttpError(e)`).
- `error()` and `redirect()` throw, so assert with `expect(...).rejects` and inspect `e.status`.
- This layer catches authorization bugs cheaply — one test per action asserting that an anonymous `locals` gets a redirect or a 403.

## End-to-End

```ts
// e2e/checkout.test.ts
import { expect, test } from '@playwright/test';

test('checkout without JavaScript', async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false });
  const page = await context.newPage();
  await page.goto('/cart');
  await page.getByRole('button', { name: 'Checkout' }).click();
  await expect(page.getByText('Order confirmed')).toBeVisible();
});
```

- Run e2e against the **preview** server (`npm run build && npm run preview`), which is what the default Playwright config does: `dev` renders everything dynamically and hides prerender, cache, and adapter bugs.
- The `javaScriptEnabled: false` test above is the cheapest possible guard on progressive enhancement, and it fails loudly the day someone replaces a form action with a client fetch.
- Cover per user role: an e2e that logs in as a second user and asserts it cannot see the first one's data catches the module-state leak that unit tests never will.
- Seed data through an API or a fixture script, not through the UI, and reset between runs.

## Static Checks in CI

| Command | Gate |
|---|---|
| `npx svelte-check --threshold error` | Type errors in `.svelte` files, which `tsc` cannot see; the threshold is `check_threshold` (SKILL.md Configuration) |
| `npx vitest run --coverage` | Unit and component tests |
| `npx playwright test` | Preview-server e2e |
| `npm run build` | Server-only imports leaking to the client, missing env vars, prerender failures |

`npm run build` is a test. SvelteKit turns whole classes of boundary mistake into build errors on purpose — a server-only import reaching client code, a missing `$env/static` variable, a dynamic route marked `prerender`, an unresolvable link in a prerendered page — and none of them can fail any other way, so a CI job that never builds ships every one of them.

## What to Test, in Priority Order

1. Actions and server loads: authorization, validation, failure payloads
2. Progressive enhancement of the critical flow, JavaScript disabled
3. State classes and derivations in `.svelte.js` modules
4. Components with real interaction logic (forms, editors, custom widgets)
5. Presentational components — only where a regression would be visible and expensive
