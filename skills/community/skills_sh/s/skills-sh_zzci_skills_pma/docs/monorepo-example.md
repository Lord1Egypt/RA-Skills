# Monorepo Example: Bun Workspaces + nsl

A concrete walkthrough of when to reach for a Bun monorepo, how to lay it out, and how the apps inside it tie together at dev time via `@nsio/nsl`. Pair this with the *Monorepo* sections in `pma-bun` and `pma-web`, and the protocol reference in [`references/dev-environment.md`](../references/dev-environment.md).

## Table of Contents

- [When to use this layout](#when-to-use-this-layout)
- [Example: `acme` - main app + admin + worker + shared types](#example-acme---main-app--admin--worker--shared-types)

## When to use this layout

A monorepo is justified when **at least one** of these is true:

- two or more deployable apps live in the same repo (e.g. main API + admin API + worker, or main SPA + admin SPA)
- one or more `packages/*` are genuinely shared by multiple consumers (e.g. shared types, shared design tokens, shared client SDK)
- shared TS / lint / drizzle / vite config must be reused across apps

A single API plus a single SPA is **not** justification. That is the *API + Sibling SPA* layout from `pma-bun` (the SPA lives as a plain `web/` directory, no workspace).

## Example: `acme` — main app + admin + worker + shared types

A realistic shape: a customer-facing app (SPA + API), a separate internal admin (SPA + same API), and a background worker. They share generated API types.

### Layout

```text
acme/
  package.json                       # workspaces root
  bun.lock
  tsconfig.base.json
  apps/
    api/                             # pma-bun
      package.json
      tsconfig.json
      drizzle.config.ts
      src/
        app.ts
        index.ts
        config.ts
        modules/
          health/
          users/
          orders/
        shared/
      drizzle/
    worker/                          # pma-bun, no HTTP exposure
      package.json
      src/
        index.ts
        jobs/
    web/                             # pma-web, single-app layout under apps/web
      package.json
      vite.config.ts
      components.json
      src/
        main.tsx
        index.css
        app/
        features/
        shared/
      public/
    admin/                           # pma-web, single-app layout under apps/admin
      package.json
      vite.config.ts
      components.json
      src/
      public/
  packages/
    api-types/                       # generated/owned shared types
      package.json
      src/
        index.ts
    config/
      tsconfig/
        base.json
        react.json
  scripts/
    compile.ts                       # production single-binary build, when applicable
```

### Root `package.json`

```json
{
  "name": "acme",
  "private": true,
  "workspaces": ["apps/*", "packages/*"],
  "scripts": {
    "lint": "eslint apps/ packages/ --ext .ts,.tsx",
    "typecheck": "bun run --filter '*' typecheck",
    "test": "bun run --filter '*' test",
    "build": "bun run --filter '*' build",
    "check": "bun run lint && bun run typecheck && bun run test && bun run build"
  },
  "devDependencies": {
    "@nsio/nsl": "^0.1.4",
    "typescript": "^5.9.0"
  }
}
```

There is **no** root `dev` script. Each app is launched independently (see below) and tied together by nsl.

### Per-app dev scripts

Each app's `package.json` carries its own `dev` script that registers with nsl. Names are chosen so the URLs read naturally.

`apps/api/package.json`:

```json
{
  "name": "@acme/api",
  "scripts": {
    "dev": "bunx nsl run -n acme:/api -s -- bun --watch src/index.ts",
    "dev:bare": "bun --watch src/index.ts"
  }
}
```

`apps/worker/package.json` — no nsl, the worker has no HTTP surface:

```json
{
  "name": "@acme/worker",
  "scripts": {
    "dev": "bun --watch src/index.ts"
  }
}
```

`apps/web/package.json`:

```json
{
  "name": "@acme/web",
  "scripts": {
    "dev": "bunx nsl run -n acme vite",
    "dev:bare": "bunx --bun vite"
  }
}
```

`apps/admin/package.json` — separate host so the admin and the customer app coexist without colliding:

```json
{
  "name": "@acme/admin",
  "scripts": {
    "dev": "bunx nsl run -n acme-admin vite",
    "dev:bare": "bunx --bun vite"
  }
}
```

### URL map

After running each app's `dev`:

```text
http://acme.localhost:3355           -> apps/web
http://acme.localhost:3355/api       -> apps/api          (/api stripped before forwarding)
http://acme-admin.localhost:3355     -> apps/admin
http://acme-admin.localhost:3355/api -> apps/api          (admin reuses the same API host? see below)
```

If the admin should hit the same API as the main app, point the admin's HTTP client at `http://acme.localhost:3355/api` directly. If the admin needs its own API surface mounted under `acme-admin`, register a second route for the same API process:

```bash
bunx nsl route acme-admin:/api 8787 --strip
```

### Starting everything

Each app runs in its own tmux session (per `references/delivery.md` conventions). Do **not** multiplex unrelated apps in a single session.

```bash
# from the repo root, one tmux session per app
SESSION_PREFIX=$(basename "$PWD" | tr '.' '-')-$(echo -n "$PWD" | md5sum | cut -c1-6)

tmux new-session -d -s ${SESSION_PREFIX}-api    /bin/bash
tmux send-keys      -t ${SESSION_PREFIX}-api    'bun run --filter @acme/api dev' Enter

tmux new-session -d -s ${SESSION_PREFIX}-worker /bin/bash
tmux send-keys      -t ${SESSION_PREFIX}-worker 'bun run --filter @acme/worker dev' Enter

tmux new-session -d -s ${SESSION_PREFIX}-web    /bin/bash
tmux send-keys      -t ${SESSION_PREFIX}-web    'bun run --filter @acme/web dev' Enter

tmux new-session -d -s ${SESSION_PREFIX}-admin  /bin/bash
tmux send-keys      -t ${SESSION_PREFIX}-admin  'bun run --filter @acme/admin dev' Enter
```

Verify with `bunx nsl list`. Stop one app by sending `C-c` to its session; stop everything by killing the matching sessions.

### Shared packages

`packages/api-types` is the canonical place for generated API response types and shared enums. Apps depend on it via `workspace:*`:

```json
{
  "dependencies": {
    "@acme/api-types": "workspace:*"
  }
}
```

Keep `packages/*` dependency-light. Prefer `import type` on the consumer side. Do **not** put runtime logic into shared packages unless multiple consumers truly need it.

### Anti-patterns specific to monorepos

- Do not add a root `dev` script that fans out to every app. Apps start independently; sequencing them in one process makes lifecycle management worse, not better.
- Do not import the API package from the frontend at runtime. Dev integration runs through nsl, not via cross-package middleware mounting. Shared types are fine; shared handlers are not.
- Do not collapse two apps into one `apps/*` directory because they happen to share code. Promote the shared code to `packages/*` instead.
- Do not skip `workspace:*`. Always pin internal deps to the workspace, never to a published version.

### Production

In production the apps deploy independently (or as a single binary that embeds one or more SPA outputs — see `pma-bun` *delivery*). nsl is a **dev-only** tool; nothing in production should depend on it.
