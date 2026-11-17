# Deployment — Adapters, Prerendering, Hosting

**Contents**: [Choosing an Adapter](#choosing-an-adapter) · [Prerendering](#prerendering) · [SPA Mode](#spa-mode) · [Environment Variables at Deploy Time](#environment-variables-at-deploy-time) · [Self-Hosting with adapter-node](#self-hosting-with-adapter-node) · [Serverless and Edge Constraints](#serverless-and-edge-constraints) · [Service Workers and Offline](#service-workers-and-offline) · [Security Headers and CSP](#security-headers-and-csp) · [Pre-Deploy Checklist](#pre-deploy-checklist)

The adapter is the only thing that knows what your host is. Everything else in the app is portable, so choosing wrong is cheap to reverse — choosing without knowing the constraints is not.

## Choosing an Adapter

| Adapter | Output | Pick when | Loses |
|---|---|---|---|
| `adapter-auto` | Detects the CI platform | Prototyping, or a platform it supports | Reproducibility: pin the real adapter before production |
| `adapter-node` | A Node server (`build/index.js`) | Own VM, container, or PaaS; long-lived processes, websockets nearby | You operate the process, TLS, and restarts |
| `adapter-static` | Plain HTML/CSS/JS | Docs, marketing, anything fully prerenderable | Server load, actions, endpoints, dynamic env |
| `adapter-vercel` | Serverless/edge functions | Vercel; ISR and image optimization wanted | Cold starts, body/duration limits |
| `adapter-cloudflare` | Workers/Pages | Global low latency, cheap egress | No Node built-ins by default; bindings via `platform.env` |
| `adapter-netlify` | Netlify Functions/Edge | Netlify | Same serverless limits |

Install and set it explicitly in `svelte.config.js`; `adapter-auto` in a repo deployed to two places is how staging and production end up with different runtimes.

## Prerendering

```js
// +layout.js — prerender everything by default, opt out per route
export const prerender = true;
```

- A route is prerenderable when its HTML does not depend on the request: no `cookies`, no `locals`, no user-specific data, no `url.searchParams` that change the output.
- The crawler starts from the entry points and follows links. A dynamic route nobody links to needs `export const entries = () => [{ slug: 'a' }, …]` (or `prerender.entries` in the config).
- `prerender = 'auto'` renders at build time **and** keeps the route server-renderable — the right setting for pages that are usually static but must handle unknown ids.
- Actions cannot exist on a prerendered route; a form there must post somewhere else.
- Build-time failures are deliberate: an unresolvable link fails the build rather than shipping a 404. `prerender.handleHttpError` narrows that when a link genuinely points outside the app.

## SPA Mode

```js
// svelte.config.js
adapter: adapter({ fallback: '200.html' })
// src/routes/+layout.js
export const ssr = false;
```

Produces a single shell that client-routes everything. Legitimate for an authenticated dashboard where every view needs the client anyway. What you give up: first-paint content, SEO, no-JS forms, and server load functions — which means auth and data access move to endpoints on some other origin or a hybrid deployment.

## Environment Variables at Deploy Time

- `$env/static/*` is inlined at **build** time: the values must exist in the build environment, and changing one requires a rebuild. Missing variables fail the build, which is the desired behavior.
- `$env/dynamic/*` is read at **runtime**: one image, many environments — but unavailable during prerendering, so a prerendered route cannot use it.
- `PUBLIC_`-prefixed values end up in the client bundle. Everything else is server-only and enforced by the build.
- `adapter-node` reads `PORT`, `HOST`, `ORIGIN`, `BODY_SIZE_LIMIT`, and the proxy headers. **`ORIGIN` matters**: behind a reverse proxy, without it (or `PROTOCOL_HEADER`/`HOST_HEADER`) SvelteKit computes the wrong origin and rejects your own form posts with a 403 CSRF error.
- Cloudflare bindings (KV, D1, R2) arrive as `platform.env` in server code, typed through `App.Platform`.

## Self-Hosting with adapter-node

```dockerfile
FROM node:22-slim AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build && npm prune --omit=dev

FROM node:22-slim
WORKDIR /app
ENV NODE_ENV=production
COPY --from=build /app/build ./build
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/package.json ./
EXPOSE 3000
CMD ["node", "build"]
```

- Only `build/`, `node_modules/`, and `package.json` are needed at runtime; source and dev dependencies do not ship.
- Terminate TLS at the proxy, set `ORIGIN=https://example.com`, and forward `X-Forwarded-Proto`/`X-Forwarded-Host` with the matching env vars.
- Static assets in `client/` are immutable and content-hashed — serve them from the CDN or the proxy with a long `max-age`, and let the Node process handle only rendered routes.
- Graceful shutdown: the server listens for `SIGTERM`; do not `SIGKILL` in-flight requests during a deploy.

## Serverless and Edge Constraints

- Cold starts scale with bundle size; a heavy dependency in the root layout is paid on every cold invocation.
- Body size and execution duration are capped per platform: uploads go directly to object storage with a presigned URL, and long jobs go to a queue.
- Edge runtimes are not Node: no `fs`, no native modules, a subset of Node built-ins. A single native dependency decides the runtime for the whole route.
- No local disk you can rely on between requests, and no shared in-memory cache — the module-level cache that works on one VM is per-instance here (and per-request unsafe regardless: SKILL.md rule 4).
- Streaming responses degrade to buffered output on platforms or proxies that do not support them; verify the streamed page in the deployed environment, not locally.

## Service Workers and Offline

```js
// src/service-worker.js — registered automatically in production builds
import { build, files, prerendered, version } from '$service-worker';

const CACHE = `cache-${version}`;                       // version busts on every build
const ASSETS = [...build, ...files, ...prerendered];    // hashed JS/CSS, static/, prerendered HTML
```

- `build` assets are content-hashed and safe to cache forever; `files` (from `static/`) are not hashed, so cache them with a revalidation strategy or they go stale across deploys.
- **Never serve an HTML shell from the cache without a version check.** A cached shell paired with a new deploy's hashed chunks produces 404s on navigation — the classic "site broken until hard refresh".
- Clean old caches in `activate`, keyed by `version`, or storage grows one full build per deploy.
- `updated` from `$app/state` reports when a new version is detected; `updated.check()` polls on demand. Prompt the user and reload rather than swapping code under a running session.
- The service worker is not registered in `dev` by default — test it against `npm run build && npm run preview`, and remember that an old worker survives a deploy until it is replaced.

## Security Headers and CSP

```js
// svelte.config.js
kit: {
  csp: {
    directives: { 'script-src': ['self'] },
    reportOnly: { 'script-src': ['self'], 'report-uri': ['/csp-report'] }
  }
}
```

Configuring CSP through Kit lets it hash or nonce its own inline hydration script. A hand-written CSP header in the `handle` hook without this configuration blocks that script, and the symptom is a page that renders correctly and then never becomes interactive. Add `strict-transport-security`, `x-content-type-options: nosniff`, and a `referrer-policy` in the same hook.

## Pre-Deploy Checklist

- Real adapter pinned in `svelte.config.js`, not `adapter-auto`
- `npm run build && npm run preview` passes locally, and the smoke path is clicked there
- Every `$env/static/*` variable present in the build environment; every `PUBLIC_` value safe to publish
- `ORIGIN` (or the proxy headers) set for `adapter-node`, and a form submission tested through the proxy
- Prerendered routes free of dynamic env and request-dependent data
- Cache-control set deliberately on cacheable pages; uncacheable ones read cookies for a reason
- Error path verified: a real 500 renders `+error.svelte`, and `handleError` logs it somewhere you read
