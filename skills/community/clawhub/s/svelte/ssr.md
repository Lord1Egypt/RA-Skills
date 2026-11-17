# SSR, Hydration, and Server Safety

**Contents**: [What Runs Where](#what-runs-where) · [Browser-Only Code](#browser-only-code) · [Hydration Mismatches](#hydration-mismatches) · [Per-Request Isolation](#per-request-isolation) · [Server-Only Modules](#server-only-modules) · [Environment Variables](#environment-variables) · [Response Shaping](#response-shaping) · [SSR Checklist](#ssr-checklist)

Every SvelteKit page runs twice by default: once on the server producing HTML, once in the browser producing the live app. Almost every "works in dev, breaks in production" bug is a difference between those two passes.

## What Runs Where

| Phase | Runs on server | Runs in browser |
|---|---|---|
| Module top-level code | Yes | Yes |
| Component `<script>` body | Yes (once per request) | Yes (on hydration) |
| `load` (universal) | Yes | Yes (on navigation) |
| `load` (server) | Yes | No |
| `$effect`, `$effect.pre` | **No** | Yes |
| `onMount`, `onDestroy` | **No** | Yes |
| Attachments and actions | No | Yes |
| `<svelte:window>` / `<svelte:document>` bindings | No | Yes |

`$effect` never running on the server is the guard, not a limitation (SKILL.md rule 9).

## Browser-Only Code

```js
import { browser } from '$app/environment';

// module scope in a shared file
if (browser) { … }

// a library that touches document on import
$effect(() => {
  let instance;
  import('heavy-editor').then(({ Editor }) => { instance = new Editor(node); });
  return () => instance?.destroy();
});
```

- `browser`, `dev`, `building`, and `version` come from `$app/environment`. `building` is true during prerendering — use it to skip work that needs a live backend.
- A component that cannot render server-side at all: wrap it in `{#if browser}`, or set `export const ssr = false` for the route if the whole page is client-only.
- Never "fix" an SSR crash with `typeof window !== 'undefined'` sprinkled through render logic: the branch that runs on the server is the one that produced the HTML, and if it differs from the client branch you have traded a crash for a hydration mismatch.

## Hydration Mismatches

The client's first render must produce the same DOM the server sent. Causes, in the order they actually occur:

1. **Time and randomness in render** — `new Date()`, `Math.random()`, `crypto.randomUUID()`. Compute on the server and pass through load, or render a placeholder and fill it in an effect.
2. **Locale and timezone** — `toLocaleString()` on a server in UTC versus a browser in Madrid. Format from an explicit locale/timezone, or format client-side after mount.
3. **Reading browser storage during init** — theme from `localStorage`, feature flags from a cookie the server did not see. Read the cookie server-side and pass it down; that is also what removes the theme flash.
4. **Invalid HTML** — `<div>` inside `<p>`, `<a>` inside `<a>`, a `<div>` inside `<table>` without `<tbody>`. The browser repairs the markup while parsing, so the client tree differs from the server tree before Svelte does anything.
5. **Browser extensions** injecting nodes — verify in a clean profile before hunting further.
6. **Non-deterministic ordering** — iterating an object whose key order differs, or a `Set` built from a `Map` on one side only. Sort explicitly.

`$props.id()` exists precisely so generated ids match across the two passes; a module-level counter does not.

## Per-Request Isolation

This is the one SSR bug with a security impact:

```js
// ✗ lib/session.svelte.js — one value for the whole Node process
export const session = $state({ user: null });

// ✓ hooks.server.js
export const handle = async ({ event, resolve }) => {
  event.locals.user = await getUser(event.cookies.get('sid'));
  return resolve(event);
};
// then: server load returns { user: locals.user }, components read it from data or context
```

- Module-level state, module-level caches, and singletons created at import time are shared by every concurrent request in the process.
- Safe at module scope: immutable config, compiled regexes, a database connection pool (the pool is shared on purpose), a memoized parse of a bundled asset.
- Unsafe: current user, request id, per-tenant configuration, a "current" anything.
- Test for it the cheap way: log in as two users in two browsers and reload both repeatedly against a production build.

## Server-Only Modules

- `$lib/server/**` and any `*.server.js` file cannot be imported from client-reachable code — the build fails with an explicit error naming the import chain. Put database clients, API keys, and admin logic there and the guarantee is structural rather than a code-review habit.
- `$env/static/private` and `$env/dynamic/private` are equally protected; importing them into a component is a build error.
- The chain matters: a shared `utils.js` that imports one server-only helper poisons everything importing `utils.js`. Split the module.

## Environment Variables

| Module | Read at | Available where |
|---|---|---|
| `$env/static/private` | Build time, inlined | Server code only |
| `$env/static/public` | Build time, inlined | Anywhere; requires the `PUBLIC_` prefix |
| `$env/dynamic/private` | Runtime, from the platform | Server code only, and **not** during prerendering |
| `$env/dynamic/public` | Runtime | Anywhere; `PUBLIC_` prefix |

- Static env is a compile-time constant: it enables dead-code elimination and fails the build when a variable is missing, which is why it is the default choice.
- Dynamic env is what lets one built image run in staging and production; it is unavailable while prerendering, so a prerendered route reading it breaks at build.
- Anything with a `PUBLIC_` prefix is in the JavaScript bundle. There is no such thing as a semi-public key here.

## Response Shaping

- `transformPageChunk` in the `handle` hook rewrites the HTML stream — the standard place for `%lang%` substitution and injecting a nonce.
- `filterSerializedResponseHeaders` controls which headers of SSR `fetch` responses reach the client payload; the default is none, which surprises people expecting `content-range`.
- `preload` in `resolve` decides which fonts, JS, and CSS get `<link rel=preload>` — trimming it is a real first-paint lever on font-heavy pages.
- CSP is configured in `svelte.config.js` (`kit.csp`), which makes Kit add hashes or nonces to its own inline scripts. Hand-writing a CSP header in the `handle` hook without that config blocks the hydration script and produces a page that renders and then does nothing.

## SSR Checklist

- No `window`, `document`, `localStorage`, or `navigator` outside `$effect`/`onMount`/`browser`
- No user-derived state at module scope in any file the server imports
- Dates and numbers formatted with an explicit locale, or after mount
- Secrets only in `$lib/server`, `*.server.js`, or `$env/*/private`
- Prerendered routes free of `$env/dynamic/*`
- Verified against `npm run build && npm run preview`, not only `npm run dev`
