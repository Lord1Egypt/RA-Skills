# SvelteKit Routing and Navigation

**Contents**: [Route Files](#route-files) · [Parameters](#parameters) · [Layout Structure](#layout-structure) · [Navigation](#navigation) · [Shallow Routing](#shallow-routing) · [Errors and Redirects](#errors-and-redirects) · [Endpoints](#endpoints-serverjs) · [Hooks](#hooks) · [Routing Checklist](#routing-checklist)

Routing is the filesystem. Every rule below is a consequence of that.

## Route Files

| File | Role |
|---|---|
| `+page.svelte` | The page component |
| `+page.js` | Universal load, page options (`prerender`, `ssr`, `csr`) |
| `+page.server.js` | Server load, form `actions` |
| `+layout.svelte` | Wraps this directory and everything under it; renders `{@render children()}` |
| `+layout.js` / `+layout.server.js` | Load and options inherited by descendants |
| `+error.svelte` | Error UI for this level and below |
| `+server.js` | HTTP endpoint (`GET`, `POST`, …) — no page at this path |

`src/routes/blog/[slug]/+page.svelte` serves `/blog/hello`. Files that do not start with `+` are colocatable helpers, never routes.

## Parameters

| Pattern | Matches | Notes |
|---|---|---|
| `[slug]` | one segment | `params.slug` is `string` |
| `[[lang]]` | zero or one segment | Optional params cannot be the only segment of a required parent |
| `[...rest]` | zero or more segments | `params.rest` is a `/`-joined string; also how you build a custom 404 |
| `[id=integer]` | segment matching a matcher | Matcher lives in `src/params/integer.js`, exports `match(value)` |
| `[x]-[y]` | one segment, split | Multiple params inside a segment are allowed |

Route specificity is resolved by the framework: static segments beat dynamic, matched dynamic beats unmatched, rest params come last. When two routes could both match, add a matcher rather than reordering files — order is not something you control.

## Layout Structure

- `(group)` directories organize routes without adding a URL segment: `(app)/dashboard` serves `/dashboard`. Use them to give a set of routes a different layout — the classic marketing/app split.
- `+page@.svelte` resets to the **root** layout; `+page@(app).svelte` resets to the layout of the named group. This is the escape hatch for a full-screen editor inside an app shell.
- Layouts nest top-down and every layout's load result is merged into `data` for the page.
- Layouts do not re-render on navigation within their subtree — component state in a layout survives route changes, which is exactly why persistent players and sidebars go there.

## Navigation

```js
import { goto, invalidate, invalidateAll, preloadData, pushState } from '$app/navigation';
import { page, navigating } from '$app/state';   // @sveltejs/kit >=2.12
```

- Plain `<a href>` is client-side routed automatically. `goto()` is for programmatic navigation only — never in a component body, never as an anchor replacement.
- `page.url`, `page.params`, `page.route.id`, `page.status`, `page.form`, `page.data` — plain reactive values, no `$` prefix. `navigating.to` is non-null during a navigation: the source for a top progress bar.
- Link options as data attributes, on the link or any ancestor: `data-sveltekit-preload-data="hover|tap|off"` (the default template sets `hover` on `<body>`), `data-sveltekit-preload-code`, `data-sveltekit-reload` (force a full document request), `data-sveltekit-noscroll`, `data-sveltekit-replacestate`.
- Guards: `beforeNavigate(({ cancel }) => …)` blocks (unsaved-changes prompts); `onNavigate` runs between navigations and is where the View Transitions API hooks in; `afterNavigate` runs after.
- `goto(url, { invalidateAll: true, replaceState, noScroll, keepFocus })` — the options are the reason to prefer it over `location.assign`.

## Shallow Routing

```js
import { pushState } from '$app/navigation';

function openPhoto(href) {
  pushState(href, { photo: href });     // adds a history entry, no navigation
}
```

`page.state.photo` then drives a modal, and the back button closes it. Pair with `preloadData(href)` so the underlying route's data is ready if the user reloads or shares the URL. The rule that keeps this honest: the route must also work as a full page load, because history state is gone after a refresh.

## Errors and Redirects

```js
import { error, redirect, isHttpError, isRedirect } from '@sveltejs/kit';

if (!post) error(404, { message: 'Not found', code: 'POST_MISSING' });
if (!locals.user) redirect(303, `/login?next=${encodeURIComponent(url.pathname)}`);
```

- In `@sveltejs/kit >=2` these throw internally: call them, never `throw` them, and call them **outside** any `try` whose `catch` would swallow the control flow (`isHttpError`/`isRedirect` let a catch rethrow correctly).
- `error()` renders the nearest `+error.svelte` **above** the failing load — an error in `+page.server.js` renders the layout's error page inside the layout; an error in `+layout.server.js` at the same level cannot be caught by that layout's own error page and bubbles up.
- The shape of the object is `App.Error`; unexpected exceptions are sanitized to a generic 500 and passed to the `handleError` hook, which is where logging belongs.
- The root fallback is `src/error.html` (plain HTML, no components) — it renders when the layout itself failed.
- 303 for post-redirect-get, 307/308 to preserve the method, 301/302 only for permanent/temporary content moves.

## Endpoints (`+server.js`)

```js
import { json, error } from '@sveltejs/kit';

export async function GET({ url, setHeaders }) {
  setHeaders({ 'cache-control': 'public, max-age=60' });
  return json({ ok: true });
}
```

- `+page.svelte` and `+server.js` **can coexist** in the same directory; Kit disambiguates by content negotiation. `GET`, `POST`, and `HEAD` are treated as page requests when the request's `accept` header prioritises `text/html`, and are handled by `+server.js` otherwise; `PUT`, `PATCH`, `DELETE`, and `OPTIONS` always go to `+server.js`. Kit adds `Vary: Accept` to the response so a cache never serves the JSON to a browser. Keep the dual route when one URL genuinely serves a page and an API; do not refactor it away.
- `GET` returning HTML/text uses `new Response(body, { headers })`; `json()` is the shortcut for JSON.
- `OPTIONS` and CORS are yours to implement; SvelteKit does not add CORS headers.
- Endpoints are for third parties, webhooks, downloads, and streaming. Your own pages should use load functions and form actions instead of fetching their own endpoints (SKILL.md Traps).

## Hooks

| Hook | File | Job |
|---|---|---|
| `handle` | `hooks.server.js` | Every request: auth into `event.locals`, headers, `resolve(event, { transformPageChunk })` |
| `handleFetch` | `hooks.server.js` | Rewrite or authenticate `fetch` calls made inside load |
| `handleError` | both | Log unexpected errors, shape the client-visible message |
| `reroute` | `hooks.js` | Map an incoming URL to a different route without a redirect (i18n prefixes, vanity URLs) |
| `init` | both | One-time async setup before the first request |

`sequence()` from `@sveltejs/kit/hooks` composes multiple `handle` functions in order; each one's `resolve` wraps the next.

## Routing Checklist

- Dynamic segments validated by a matcher or by the load function, never trusted raw
- Group layouts used instead of duplicated wrapper markup
- Every `redirect()` and `error()` outside a `try`
- `+error.svelte` at the level that can actually render (root fallback for layout failures)
- Preload strategy set once on `<body>`, overridden per link only where it costs money
- Shallow-routed modals still resolvable as a full page load
