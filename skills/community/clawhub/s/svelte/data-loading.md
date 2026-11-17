# Load Functions, Invalidation, and Streaming

**Contents**: [Universal vs Server Load](#universal-vs-server-load) · [Serialization Across the Wire](#serialization-across-the-wire) · [The `fetch` You Are Given](#the-fetch-you-are-given) · [When a Load Reruns](#when-a-load-reruns) · [Waterfalls and `await parent()`](#waterfalls-and-await-parent) · [Streaming](#streaming) · [Page Options](#page-options) · [Cookies and Headers](#cookies-and-headers) · [Load Checklist](#load-checklist)

## Universal vs Server Load

| | `+page.js` (universal) | `+page.server.js` (server) |
|---|---|---|
| Runs | Server on first render, browser on client navigation | Server always |
| Can read | Public env, `fetch`, `params`, `url`, parent data | Everything: db, private env, `cookies`, `locals`, `request` |
| Return value | Anything, including class instances and functions | Must survive devalue serialization |
| Ships to the browser | Yes, the code does | No |
| Use for | Wrapping a public API, returning a component constructor, client-only caching | Anything with secrets, a database, or per-user data |

Both can exist for the same route; the server load runs first and its result is available to the universal load via `data`.

```js
// +page.server.js
export const load = async ({ params, locals, depends }) => {
  depends('app:post');                       // a custom invalidation key
  const post = await db.getPost(params.slug);
  if (!post) error(404);
  return { post, user: locals.user };
};
```

## Serialization Across the Wire

Server load output is serialized with devalue, which is strictly better than JSON but not unlimited:

- **Survives**: `Date`, `Map`, `Set`, `RegExp`, `BigInt`, `undefined`, `NaN`/`Infinity`, repeated references, cycles.
- **Does not survive**: functions, class instances (they arrive as plain objects), symbols, DOM nodes, database cursors.
- Custom types cross the boundary through the `transport` hook in `hooks.js` — `encode`/`decode` pairs for your Decimal, ObjectId, or domain class. Without it, a Prisma `Decimal` silently becomes `{}`.
- Everything you return is embedded in the HTML payload. Returning a 4 MB row set makes a 4 MB document — select the columns the page renders.

## The `fetch` You Are Given

`event.fetch` (destructure `{ fetch }`) is not the global one:

- Relative URLs resolve against the app, so `fetch('/api/x')` works during SSR.
- Same-origin requests inherit the incoming `cookie` and `authorization` headers.
- Responses fetched during SSR are **inlined into the HTML** and reused during hydration instead of being requested a second time.
- Internal `+server.js` routes are called directly without an HTTP round trip.
- `handleFetch` in `hooks.server.js` lets you rewrite the URL or attach credentials for a specific backend.

## When a Load Reruns

A load reruns when **any** of these is true (SKILL.md rule 7):

1. A `params` property it read changed.
2. A property of `url` it read changed — tracking is per-property, so reading `url.searchParams.get('page')` reacts to `?page` only.
3. `invalidate('app:post')` fired for a key it registered with `depends()`.
4. `invalidate(url)` fired for a URL it fetched with `event.fetch`.
5. It called `await parent()` and the parent reran.
6. `invalidateAll()` fired, or a form action completed under `use:enhance` (which invalidates all by default).

Consequences worth internalizing:

- Reading `url.pathname` in a layout load makes it rerun on **every** navigation. Read only what you need.
- `untrack(() => url.searchParams.get('debug'))` opts a read out of the dependency set.
- Reruns are not remounts: the page component keeps its state; only `data` changes.
- A load that must rerun on a timer belongs in an effect with `invalidate()`, not in a `setInterval` that mutates local state.

## Waterfalls and `await parent()`

```js
// ✗ serializes the two round trips
export const load = async ({ parent, fetch }) => {
  const { user } = await parent();
  const orders = await fetch(`/api/orders/${user.id}`).then(r => r.json());
  return { orders };
};

// ✓ only await the parent for what genuinely depends on it
export const load = async ({ parent, fetch }) => {
  const settingsPromise = fetch('/api/settings').then(r => r.json());
  const { user } = await parent();
  return { settings: settingsPromise, orders: fetchOrders(user.id) };
};
```

Loads at the same level run in parallel. `await parent()` is the only thing that serializes them, so call it as late as possible — and never just to read something you could read from `locals` directly on the server.

## Streaming

```js
export const load = ({ params }) => ({
  post: await db.getPost(params.slug),      // awaited: blocks the response
  comments: db.getComments(params.slug)     // promise: streams in later
});
```

- Only **server** loads stream; a promise returned from a universal load is not awaited for you.
- Render with `{#await data.comments}` and give it a real skeleton — the whole point is that the shell paints first.
- Rejected streamed promises need a `{:catch}` or they surface as an unhandled rejection; attach the handling in the component.
- Streaming needs a runtime that supports it: it degrades to a fully buffered response behind some proxies and on platforms that buffer function output, and it does nothing for clients with JavaScript disabled.
- Do not stream the primary content of an indexable page — crawlers and social-preview fetchers read what arrived in the initial HTML.

## Page Options

Declared in `+page.js` / `+layout.js` (and `+page.server.js` for the server-side ones):

| Option | Effect |
|---|---|
| `export const prerender = true` | Build-time HTML; the route must not depend on the request. `'auto'` prerenders but keeps it in the SSR manifest |
| `export const ssr = false` | Skip server render — the page is a client-only shell; `load` still runs in the browser |
| `export const csr = false` | Ship no JavaScript for this route: no hydration, no client navigation, forms still work |
| `export const trailingSlash = 'always' \| 'never' \| 'ignore'` | Canonical URL shape; affects prerendered filenames |
| `export const config = { … }` | Adapter-specific deployment config (runtime, region, memory) |
| `export const entries = () => [{ slug: 'a' }]` | Which dynamic routes to prerender when the crawler cannot find them |

`ssr = false` in the root layout turns the app into an SPA; that is a deliberate architecture choice, not a workaround for a "window is not defined" error.

## Cookies and Headers

- `cookies.get/set/delete` are available in server load, actions, endpoints, and hooks. `path` is required on `set` and `delete` (`@sveltejs/kit >=2`).
- Set cookies before returning; after the response starts streaming it is too late.
- `setHeaders({ 'cache-control': … })` shapes the response for the page, once per header — it cannot set cookies (use `cookies`), and it is ignored during prerendering.
- A load that reads `cookies` or `request.headers` makes the route uncacheable at the CDN by definition; that is usually correct, but check before wondering why the CDN hit rate is zero.

## Load Checklist

- Secrets and database access only in `+page.server.js` / `+layout.server.js`
- Return only the fields rendered; no whole ORM rows
- `await parent()` called as late as possible, or not at all
- Slow secondary data streamed with a skeleton, primary data awaited
- `depends()` keys defined for anything invalidated by a mutation
- No `url`/`params` reads in a layout load beyond what it actually uses
