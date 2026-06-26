# PMA-Bun Runtime

## Table of Contents

- [Formatting And TypeScript](#formatting-and-typescript)
- [Scripts](#scripts)
- [Error Handling](#error-handling)
- [Configuration](#configuration)
- [ROOT_DIR And Compiled Mode](#rootdir-and-compiled-mode)
- [Bootstrap Split](#bootstrap-split)
- [HTTP Server With OpenAPIHono](#http-server-with-openapihono)
- [Middleware Stack](#middleware-stack)
- [Dev URL Routing (via nsl)](#dev-url-routing-via-nsl)
- [Logging](#logging)
- [API Documentation](#api-documentation)
- [PID Lock And Singleton Safety](#pid-lock-and-singleton-safety)
- [Single-Binary Delivery](#single-binary-delivery)


## Formatting And TypeScript

- Use `@antfu/eslint-config`.
- Ignore generated artifacts such as `drizzle/**` and route trees when appropriate.
- Keep TypeScript in strict mode with `noUncheckedIndexedAccess`.
- Prefer `verbatimModuleSyntax`, `exactOptionalPropertyTypes`, and `import type` discipline.
- Keep path aliases aligned with `tsconfig.json`; do not invent aliases that CI does not resolve.

## Scripts

Baseline scripts should usually include:

- `dev`
- `lint`
- `typecheck`
- `build`
- `test`
- `test:coverage`
- `db:generate`
- `start`

Keep script names predictable across repositories.

## Error Handling

- Use an `AppError` hierarchy with HTTP status mapping.
- Convert internal errors to safe API responses at the edge.
- Never leak stack traces or internal DB details to clients.

## Configuration

- Load environment variables once.
- Validate them with Zod at startup.
- Inject validated config into app services; do not call `Bun.env` from domain logic.
- Keep `.env.example` complete and non-secret.
- Resolve file paths relative to a centralized root helper instead of scattering path joins across modules.

## ROOT_DIR And Compiled Mode

When the project supports compiled binaries:

- centralize root-directory detection in one module
- support explicit env override such as `ROOT_DIR`
- handle both source-tree and compiled-binary execution paths
- keep asset and migration lookup logic out of business modules

## Bootstrap Split

Recommended shape:

- `app.ts` bootstraps config, logging, db wiring, and returns the `fetch` handler
- `index.ts` owns `Bun.serve()` and graceful shutdown — reads `PORT` from the env (which `nsl run` injects in dev) and binds to it
- `root.ts` resolves runtime root paths
- `pid-lock.ts` prevents duplicate listeners when the service should be singleton-like
- `dev.ts` is **optional**. Add it only if dev startup truly diverges from prod (e.g. seeding fixtures, attaching dev-only middleware). Frontend integration is handled by nsl outside the process — `dev.ts` should not exist solely to mount Vite.

Rules:

- keep startup side effects centralized
- keep mutable runtime state out of business modules unless the design explicitly requires it
- separate dev-only bootstrap from production startup *only when there is real divergence*

## HTTP Server With OpenAPIHono

Recommended shape:

- `app.ts` builds the OpenAPIHono app graph
- `index.ts` handles startup and shutdown
- `modules/docs` serves OpenAPI JSON and Scalar UI
- `modules/health` exposes a health endpoint
- domain routes stay in their own modules

Rules:

- keep route handlers thin
- validate input with Zod
- map domain errors centrally
- return a consistent response envelope where the product expects it
- use graceful shutdown for signals

## Middleware Stack

Default API middleware ordering should be explicit:

1. request ID
2. secure headers
3. CORS
4. dependency injection onto context
5. request logging
6. CSRF or other browser-facing state protections
7. business routes
8. centralized error handler

Keep security middleware close to the edge, not inside individual feature handlers.

## Dev URL Routing (via nsl)

The full nsl protocol lives in `/pma references/dev-environment.md`. This section only covers the **Bun-specific** angle.

### Bun dev script

```bash
bunx nsl run -n <name>:/api -s -- bun --watch src/index.ts
```

- `Bun.serve()` reads `PORT` natively, so the API binds to the port nsl allocates without any extra wiring.
- `-s` (`--strip`) drops the `/api` prefix before forwarding, so route handlers stay mounted at their domain paths (`/users`, `/orders`, …) and remain unaware of the public mount point.

### Bun-specific anti-patterns

- Do **not** mount Vite into the Bun process (no `@hono/vite-dev-server`, no Vite middleware in `dev.ts`).
- Do **not** import the API package from the frontend for middleware mounting — frontend and backend run as independent processes.
- Production bootstrap stays untouched: `index.ts` reads `PORT` and serves embedded SPA assets normally; nothing in production depends on nsl.

## Logging

- use consola for human-readable development logs
- use pino for structured operational logs
- redact secrets
- attach correlation IDs when the service needs request tracing
- flush structured logs on controlled shutdown when using file destinations

## API Documentation

- prefer OpenAPI generation from route schemas
- serve interactive docs at `/docs`
- keep docs generation aligned with actual validation schemas

## PID Lock And Singleton Safety

When the service uses local files, embedded SQLite, or singleton integrations:

- keep PID lock logic in one module
- record enough metadata to detect stale locks
- probe carefully before taking over an existing lock
- never scatter duplicate-listener protection across startup code

## Single-Binary Delivery

When using `bun build --compile`:

- replace stub modules for embedded assets and migrations during build
- keep compiled-only logic isolated
- document any feature gaps versus source-mode execution
