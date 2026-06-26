# PMA-Bun Data And Testing

## Database Default: Drizzle Plus SQLite

Prefer this for:

- single-instance services
- internal tools with local state
- local-first tools
- CLIs
- small internal APIs

Rules:

- keep schema in `src/db/schema.ts`
- keep DB initialization and migration wiring in `src/db/index.ts`
- keep generated migrations under the API package, for example `apps/api/drizzle/`
- use WAL mode when appropriate
- commit generated SQL migrations
- choose one driver story and document it clearly

## Driver Guidance

Default extracted pattern:

- use Drizzle for schema and query composition
- use a SQLite-capable client that still works with the repository's encryption or deployment needs
- expose a single `createDb()` path that configures pragmas, schema binding, and migration execution

When compiled binaries are part of delivery:

- support a filesystem migration path during source-mode execution
- support embedded migration fallback for compiled mode
- keep temporary extraction details inside the DB bootstrap layer

## PostgreSQL Alternative

Use PostgreSQL when the service needs:

- multi-instance writes
- richer concurrent access patterns
- shared database infrastructure
- more advanced query characteristics than the default SQLite setup supports

Keep the swap explicit in docs, scripts, and CI.

## Repository Pattern

- repositories own persistence details
- services own business logic
- route handlers coordinate transport only
- keep DB-specific types from leaking through the application without intent
- if a module stays small, a combined `*.service.ts` file is acceptable; do not force extra layers without payoff

## Testing

Use:

- unit tests close to modules with `*.test.ts`
- integration tests under `tests/integration/`
- Playwright only when browser-level coverage is required
- API package tests should run directly under Bun unless another runner is already justified

Rules:

- prefer real dependencies over fragile mocks when feasible
- restore mocks after each test
- keep tests independent
- run coverage in CI and target roughly 80 percent or higher
- keep migration and schema behavior under test when database bootstrap changes

## Test Boundaries

- validate route input and error translation at the edge
- test repositories against real schema behavior where practical
- test service logic without coupling everything to HTTP transport
- test startup helpers when they encode non-trivial behavior such as lock recovery, path detection, or migration fallback
