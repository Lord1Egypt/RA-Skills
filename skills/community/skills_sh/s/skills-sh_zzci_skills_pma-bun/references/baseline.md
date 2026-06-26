# PMA-Bun Baseline

## Table of Contents

- [Scope](#scope)
- [Tech Stack](#tech-stack)
- [Dependency Freshness (Bun)](#dependency-freshness-bun)
- [Required Quality Gates](#required-quality-gates)
- [Project Layout](#project-layout)
- [Required Conventions](#required-conventions)
- [Code Quality Standards](#code-quality-standards)
- [Baseline Scripts](#baseline-scripts)
- [Implementation Workflow](#implementation-workflow)


## Scope

Use this pack for PMA-managed Bun backends, API services, and Bun-based full-stack monorepos.

Goals:

- Bun-native runtime and workspace conventions
- strict TypeScript with zero `any`
- explicit module and bootstrap boundaries
- reproducible builds with lockfile and predictable scripts
- operational and security conventions that are easy to review

## Tech Stack

### Required

| Category | Technology | Notes |
|---|---|---|
| Runtime | Bun 1.2+ | latest stable |
| Language | TypeScript 5.9+ | strict mode, `noUncheckedIndexedAccess` |
| Package manager | bun | commit `bun.lock` |
| Lint / format | ESLint + @antfu/eslint-config | no Prettier |
| Validation | Zod 3 | API-boundary validation |
| Errors | typed error classes | `AppError` hierarchy at transport boundaries |
| Test | bun:test | built-in runner |

### Default

| Category | Technology | Notes |
|---|---|---|
| HTTP server | OpenAPIHono | from `@hono/zod-openapi` |
| API docs | `@scalar/hono-api-reference` | serve docs at `/docs` |
| Data access | Drizzle ORM + drizzle-kit | schema-as-code |
| Database | SQLite | default for local-first internal services |
| Driver | libSQL client + Drizzle | supports file DB plus encryption features when needed |
| Config | environment variables + Zod | validate at startup |
| Logging | consola + pino | console plus structured file output |
| Hot reload | `bun --watch src/index.ts` | restarts on source change; backend runs as its own process |
| Dev URL routing | `@nsio/nsl` | named `.localhost` routes for API (and sibling SPA when same repo). Protocol details: `/pma references/dev-environment.md`. |

### Optional

| Category | Technology | When to adopt |
|---|---|---|
| Observability | OpenTelemetry | production tracing and metrics |
| Queue | BullMQ | background jobs |
| Cache | Redis | shared cache |
| CLI | Commander.js | richer command surface |
| E2E test | Playwright | browser-level flows |
| Process lock | PID lock file | prevent duplicate listeners |
| Single binary | `bun build --compile` | embed assets and migrations |

### Alternative

| Replaces | Technology | Notes |
|---|---|---|
| OpenAPIHono | plain Hono | lighter when OpenAPI generation is unnecessary |
| OpenAPIHono | Elysia | Bun-native alternative |
| SQLite | PostgreSQL via `postgres` or managed libSQL | multi-instance writes or shared DB needs |
| Drizzle ORM | Prisma | heavier but broader ORM feature set |
| consola + pino | pino only | headless services |
| ESLint | Biome | faster, smaller ecosystem |

## Dependency Freshness (Bun)

See `/pma references/workflow.md` *Dependency Freshness* for the cross-stack rule. Bun-specific verification:

```bash
# Latest stable version on npm
bun pm view <pkg> version

# Find outdated packages in the current project
bun outdated

# For deeper upgrade planning (peer-dep aware)
npx npm-check-updates --target latest
npx npm-check-updates -u --target minor   # safer bump
```

When pinning to a non-latest version, note the reason in `package.json` near the entry or in `docs/decisions/`:

```jsonc
{
  "dependencies": {
    // PINNED: <pkg>@3.x — 4.x requires Bun 1.3; revisit after runtime bump
    "<pkg>": "^3.8.0"
  }
}
```

Library docs check: when adopting or upgrading Hono, Drizzle, Zod, or any other core dep, fetch current docs via Context7 (`mcp__plugin_context7_context7__query-docs`). Hono v4 and Drizzle's APIs evolve faster than training-data recall.

## Required Quality Gates

Every PMA-Bun project should expose:

- `bun run lint`
- `bun run typecheck`
- `bun run build`
- `bun test`
- `bun test --coverage` or package-local coverage equivalent
- security review for auth, secrets, outbound HTTP, and config changes

For monorepos, also expose a root `check` command that sequences the main gates.

## Project Layout

Pick exactly one of the three layouts and stay with it. Default to **Single API**; promote only when the trigger conditions are met.

### Single API (default)

For an API-only service or an internal tool. No workspaces, one `package.json` at the project root.

```text
package.json
tsconfig.json
drizzle.config.ts
src/
  app.ts
  index.ts
  config.ts
  root.ts
  pid-lock.ts
  db/
    index.ts
    schema.ts
    embedded-migrations.ts
  modules/
    health/
    docs/
    <domain>/
  shared/
    lib/
    middleware/
    static-assets.ts
drizzle/
scripts/
  compile.ts
```

A `dev.ts` is **not** required by default. Add one only if the dev startup truly needs different wiring than `index.ts` (e.g. seeding test fixtures, attaching dev-only middleware). Frontend integration is handled at the nsl layer, not via a Vite middleware bridge in `dev.ts`.

### API + Sibling SPA (same repo, no workspace)

When the project ships a SPA in the same repo. Keep the SPA as a plain sibling directory (`web/`); do **not** introduce Bun workspaces just to host it. Dev runs as two independent processes, glued by nsl (see `pma-web`).

```text
package.json                # API project (this skill)
src/
drizzle/
web/                        # SPA project (pma-web, single-app layout)
  package.json
  vite.config.ts
  src/
scripts/
  compile.ts
```

Production single-binary mode: the compile script builds the SPA first and embeds the `web/dist` output into the API binary (see `delivery.md`).

### Monorepo (only when justified)

Use Bun workspaces only when one or more of these are true:

- two or more deployable apps live in the same repo (e.g. API + worker + admin SPA)
- one or more `packages/*` are genuinely shared by multiple consumers
- shared TS / lint / drizzle config must be reused across apps

A single API plus a single SPA is **not** a sufficient reason — that case is *API + Sibling SPA*.

```text
package.json
apps/
  api/
    package.json
    tsconfig.json
    drizzle.config.ts
    src/
      app.ts
      index.ts
      config.ts
      root.ts
      pid-lock.ts
      db/
      modules/
      shared/
    drizzle/
  web/
    package.json
    vite.config.ts
packages/
  config/
  shared/
scripts/
  compile.ts
```

## Required Conventions

| Area | Convention |
|---|---|
| Workspace layout | only in *Monorepo*: `apps/*` for runnable apps, `packages/*` for shared config and code |
| Project layout | `src/modules/` for domain modules, `src/shared/` for cross-cutting concerns |
| Module structure | co-locate routes, service, types, and tests; keep transport thin |
| Bootstrap split | `app.ts` builds the app, `index.ts` runs startup; add `dev.ts` only when dev wiring genuinely diverges from prod |
| Dev URL routing | invoke the backend through `bunx nsl run` so the API binds to `<name>.localhost:3355/api`; never embed Vite into the backend process |
| Errors | never throw raw strings |
| Validation | Zod at boundaries |
| Config | never read `Bun.env` directly in business logic |
| Database | parameterized queries only |
| Logging | no `console.log` in production paths |
| Imports | prefer `import type` for type-only imports |
| Aliases | use `@/*` only when it maps to the real `src/` tree |

## Code Quality Standards

- prefer immutable updates
- keep functions under 50 lines when possible
- keep files focused and usually under 800 lines
- avoid deep nesting
- avoid hardcoded values when config or constants fit better
- no `any` in application code

## Baseline Scripts

For a *Single API* or the API project in the *API + Sibling SPA* layout:

```json
{
  "scripts": {
    "dev": "bunx nsl run -n <name>:/api -s -- bun --watch src/index.ts",
    "dev:bare": "bun --watch src/index.ts",
    "build": "bun build src/index.ts --outdir dist --target bun --minify",
    "start": "bun dist/index.js",
    "lint": "eslint .",
    "typecheck": "tsc --noEmit",
    "test": "bun test",
    "test:coverage": "bun test --coverage",
    "db:generate": "drizzle-kit generate"
  },
  "devDependencies": {
    "@nsio/nsl": "^0.1.4"
  }
}
```

Notes:

- `<name>` matches the project's nsl host. In *API + Sibling SPA*, use the SPA's project name so the API mounts at `<name>.localhost:3355/api`. In *Single API*, drop `:/api` and `-s` and just expose the API at `<name>.localhost:3355`.
- `Bun.serve()` reads `PORT` natively, which `nsl run` exports automatically — no extra flags.
- `dev:bare` keeps a plain `bun --watch` invocation around for CI smoke tests, container builds, or environments where the nsl daemon cannot run.
- For protocol details (`--strip`, `NSL_PORT`, registration patterns, fallback), see `/pma references/dev-environment.md`. For multi-app workspace setup, see `/pma docs/monorepo-example.md`.

For the *Monorepo* layout, add a root `package.json` that fans out to per-app scripts:

```json
{
  "scripts": {
    "lint": "eslint apps/ packages/ --ext .ts,.tsx",
    "typecheck": "bun run --filter '*' typecheck",
    "test": "bun run --filter '*' test",
    "build": "bun run --filter '*' build",
    "check": "bun run lint && bun run typecheck && bun run test && bun run build"
  }
}
```

Run each app's `dev` script from inside the app directory (or via `bun run --filter <app> dev`) — there is no longer a single root `dev` because each app is launched independently and tied together by nsl.

## Implementation Workflow

Within approved implementation work:

1. Research and reuse existing libraries first.
2. Plan interfaces and failure modes before coding.
3. Keep module boundaries explicit before adding new routes or services.
4. Run review passes focused on correctness, security, and missing tests.
