# PMA-Web Runtime And Data

## Table of Contents

- [State Boundaries](#state-boundaries)
- [Query Client](#query-client)
- [HTTP Client](#http-client)
- [i18n](#i18n)
- [Vite Configuration](#vite-configuration)
- [Backend Integration In Dev (via nsl)](#backend-integration-in-dev-via-nsl)
- [Shared Packages](#shared-packages)


## State Boundaries

- TanStack Query owns request lifecycle, caching, retries, and invalidation.
- Zustand is for UI-only interaction state.
- Do not mirror server data into Zustand without a clear reason.

## Query Client

Use a shared query client module with stable defaults:

```typescript
import { QueryClient } from "@tanstack/react-query";

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60_000,
      retry: 1,
    },
  },
});
```

Tune defaults per product; do not scatter ad hoc query config across unrelated components.

## HTTP Client

- Centralize fetch logic in `shared/lib/http.ts`.
- Use `/api` as the default base path unless the repo already standardizes differently.
- Normalize error handling, headers, and JSON parsing in one place.
- Keep feature `api.ts` files thin wrappers around shared transport.

## i18n

Use only when the product needs multiple locales.

Recommended stack:

- `react-i18next`
- `i18next-http-backend`
- `i18next-browser-languagedetector`

Rules:

- keep locale files under `public/locales/{{lng}}/{{ns}}.json`
- initialize in `app/i18n.ts`
- mount through `I18nextProvider`
- set fallback language based on the product's primary language
- use detection order such as `localStorage -> navigator`

## Vite Configuration

Use Vite 8 defaults that match the repo layout:

```typescript
import tailwindcss from "@tailwindcss/vite";
import { tanstackRouter } from "@tanstack/router-plugin/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [
    // tanstackRouter MUST be listed before react() — incorrect order causes
    // silent failures in route generation and code splitting.
    tanstackRouter({
      target: "react",
      routesDirectory: "src/app/routes",
      autoCodeSplitting: true,
    }),
    react(),
    tailwindcss(),
  ],
  resolve: { tsconfigPaths: true },
  server: {
    host: "0.0.0.0",
    // allowedHosts: see "Choosing server.allowedHosts" below.
  },
});
```

Recommended rules:

- enable `resolve.tsconfigPaths: true`
- import `tanstackRouter` (lowercase) from `@tanstack/router-plugin/vite` and place it **before** `react()` in the `plugins` array; the previously-exported `TanStackRouterVite` symbol still works but is deprecated
- pass `target: "react"` and `routesDirectory: "src/app/routes"`; enable `autoCodeSplitting: true` unless you have a reason not to
- keep server host on `0.0.0.0`
- do **not** add `@hono/vite-dev-server`, `server.proxy`, or backend-aware plugins to Vite config — backend integration happens at the nsl layer, not inside Vite

### Choosing `server.allowedHosts`

The right value depends on which nsl domains forward traffic to Vite. nsl can route both private (`*.localhost`) and public (e.g. `*.a.fr.ds.cc`) hostnames; the `Host` header Vite receives reflects whichever the user typed.

| nsl deployment | What reaches Vite | Recommended `server.allowedHosts` |
|---|---|---|
| Local only — proxy listens on `*.localhost` | `Host: <name>.localhost` | omit (Vite allows `.localhost` by default) |
| nsl exposes a public dev domain (e.g. `a.fr.ds.cc`) | `Host: <name>.a.fr.ds.cc` | `[".a.fr.ds.cc"]` — leading dot allows the domain and all subdomains |
| Multiple public dev domains, or hostnames not known up front | varies | `true`, with the caveats below |

`allowedHosts: true` is the simplest setting that covers every nsl domain configuration without maintenance, and it is the right call when:

- the dev server is fronted by trusted infrastructure (nsl + your team's network)
- public dev hostnames change often or are dynamic
- you do not want each developer to edit Vite config when adding a new domain

The tradeoff per [Vite GHSA-vg6x-rcgg-rjx6](https://github.com/vitejs/vite/security/advisories/GHSA-vg6x-rcgg-rjx6) is that any browser tricked by a DNS-rebinding attack into resolving an attacker-controlled hostname to your dev server's IP can read source and proxied content. Mitigations:

- prefer the explicit-list option whenever the public dev domain is stable (it is the most common case)
- never enable `allowedHosts: true` on a Vite dev server reachable from the open internet (if your dev environment is internet-exposed at all, scope it to a known domain list)
- treat any `allowedHosts` value other than the default and an explicit allowlist as a deliberate, project-specific decision documented in the proposal

## Backend Integration In Dev (via nsl)

The full nsl protocol — install, mental model, registration patterns, `--strip` semantics, `NSL_PORT` placeholder, fallback — lives in `/pma references/dev-environment.md`. This section only covers the **frontend-specific** angle.

### Frontend dev script

```bash
bunx nsl run vite
```

`nsl run` exports the allocated port as `PORT`; Vite reads `PORT` natively, so no `--port` flag is needed. This registers `<name>.localhost` → frontend.

### Frontend HTTP client implications

- Keep the HTTP client base URL as `/api` (relative). Same-origin under nsl means there is nothing to configure differently between dev and prod.
- Do not bake `localhost:<port>` URLs into the client.
- Do not add CORS workarounds for dev — same-origin avoids the problem entirely.

### Vite config implications

- `server.allowedHosts` follows the nsl deployment shape — see the *Choosing `server.allowedHosts`* table in the *Vite Configuration* section above. Default-omitted for local-only `.localhost`; explicit list (`[".your-public-domain"]`) for stable public dev domains; `true` for dynamic / unknown public hostnames with the documented tradeoff.
- Do **not** add `@hono/vite-dev-server` or any `server.proxy` block in committed Vite config. Backend integration happens at the nsl layer.

### Fallback

If the dev environment cannot run nsl, use the `dev:bare` script from `baseline.md` (plain `bunx --bun vite`). See `/pma references/dev-environment.md` for the full fallback caveats.

## Shared Packages

Only relevant in the Monorepo layout (see `baseline.md`). Use `packages/shared` for:

- API response types
- shared enums and value objects
- constants reused by multiple apps

Keep shared packages dependency-light and prefer `import type` on the consuming side.

In the Single App layout, the equivalent code lives in `src/shared/` and there is no cross-package boundary to manage.
