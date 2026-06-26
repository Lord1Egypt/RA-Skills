# SurrealKit -- Schema Sync, Rollouts, Seeds, and Declarative Tests

SurrealKit is a schema management tool for SurrealDB applications. It treats
`.surql` files as the desired state, reconciles disposable databases directly,
and uses rollout manifests for reviewed staged changes on shared or production
databases.

Tracked upstream snapshot: **v0.7.0** (`8b83dd867338`, 2026-06-11). v0.7.0 adds
library/embedded sync surfaces, improved typegen, template variables, and MODULE
tracking in schema state. The v0.6.x line added library-lock fixes, comment
stripping, `DROP … IF EXISTS` for namespace/database removal, and `DEFINE`
coverage for `BUCKET`, `SEQUENCE`, and `CONFIG`.

> **Packaging note**: the active upstream README now documents four install
> paths: `cargo binstall surrealkit`, `cargo install surrealkit`, prebuilt
> GitHub release archives with `.sha256` files, and a GHCR Docker image
> (`ghcr.io/surrealdb/surrealkit:latest`). Prefer exact release tags in CI and
> production; use `latest` only for disposable local or preview workflows.

---

## Installation

```bash
cargo binstall surrealkit
cargo install surrealkit
docker pull ghcr.io/surrealdb/surrealkit:latest
```

## Project Layout

```text
database/
  schema/       # desired-state .surql definitions
  rollouts/     # planned rollout manifests (.toml)
  snapshots/    # local catalog/schema snapshots
  seeds/        # seed files
  tests/
    config.toml
    suites/*.toml
```

Initialize the scaffold:

```bash
surrealkit init
```

## Environment Variables

SurrealKit reads connection values from CLI args first, then system env vars,
then `.env`, then defaults. Current names are `SURREALDB_*` with older
`DATABASE_*` names as fallbacks:

- `SURREALDB_HOST` (fallback: `DATABASE_HOST`)
- `SURREALDB_NAME` (fallback: `DATABASE_NAME`)
- `SURREALDB_NAMESPACE` (fallback: `DATABASE_NAMESPACE`)
- `SURREALDB_USER` (fallback: `DATABASE_USER`)
- `SURREALDB_PASSWORD` (fallback: `DATABASE_PASSWORD`)
- `SURREALDB_AUTH_LEVEL` (fallback: `DATABASE_AUTH_LEVEL`; accepted values:
  `root`, `namespace` / `ns`, `database` / `db`)

## Operating Modes

### Sync

Use `sync` when the database can match local files immediately.

```bash
surrealkit sync
surrealkit sync --watch
```

Behavior:

- Applies changed definitions from `database/schema`
- Removes SurrealKit-managed objects deleted from desired state
- Best for local, preview, CI, and other disposable databases

For shared databases, destructive prune requires an explicit override:

```bash
surrealkit sync --allow-shared-prune
```

### Template Variables

v0.6.2 added template variables for schema, seed, and rollout SQL. Use
`${VAR_NAME}` tokens in `.surql` files and bind them at runtime:

```surql
DEFINE TABLE ${schema_prefix}_users SCHEMAFULL;
DEFINE ROLE ${writer_role} PERMISSIONS FULL;
```

Resolution priority:

| Source | Example |
|--------|---------|
| CLI `--var KEY=VALUE` | `surrealkit sync --var schema_prefix=acme` |
| Env var `SURREALKIT_VAR_<KEY>` | `SURREALKIT_VAR_SCHEMA_PREFIX=acme surrealkit sync` |
| `[variables]` in `surrealkit.toml` | `schema_prefix = "acme"` |

Variable names are case-insensitive. Use variables for environment-specific
identifiers or values; keep structural schema differences visible in the
reviewed `.surql` files.

### Rollouts

Use rollouts for shared or production databases where changes need review,
staging, rollback, or operator-controlled cutover.

```bash
surrealkit rollout baseline
surrealkit rollout plan --name add_customer_indexes
surrealkit rollout start 20260302153045__add_customer_indexes
surrealkit rollout complete 20260302153045__add_customer_indexes
surrealkit rollout rollback 20260302153045__add_customer_indexes
surrealkit rollout lint 20260302153045__add_customer_indexes
surrealkit rollout status
```

Workflow:

1. Author desired state in `database/schema/*.surql`
2. Baseline the shared database once
3. Generate a rollout manifest
4. Start the non-destructive expansion phase
5. Cut application traffic/code over
6. Complete the contract/destructive phase
7. Roll back if the rollout is still in-flight and the cutover fails

Generated manifests are stored in `database/rollouts/*.toml`.

## Seeding

Run seed data explicitly:

```bash
surrealkit seed
```

Use seeds for deterministic local fixtures, smoke datasets, and test setup. Do
not rely on seeds as a substitute for rollout-managed schema changes.

## Declarative Testing

Run declarative suites:

```bash
surrealkit test
surrealkit test --json-out test-results.json
```

Suite files live under `database/tests/suites/*.toml`.

Supported case kinds:

- `sql_expect`
- `permissions_matrix`
- `schema_metadata`
- `schema_behavior`
- `api_request`

Useful flags:

- `--suite <glob>`
- `--case <glob>`
- `--tag <tag>` (repeatable)
- `--fail-fast`
- `--parallel <N>`
- `--json-out <path>`
- `--no-setup`
- `--no-sync`
- `--no-seed`
- `--base-url <url>`
- `--timeout-ms <ms>`
- `--keep-db`

By default, suites run in isolated ephemeral namespace/database pairs and fail
CI on any test failure.

## Decision Guidance

- Use `sync` for disposable environments where desired-state deletion is safe.
- Use `rollout` for shared or production databases, especially when dropping or
  renaming fields, indexes, access definitions, or tables.
- Use `--var` / `SURREALKIT_VAR_*` only for environment-specific identifiers or
  values. Don't hide schema shape changes behind opaque variables.
- Use `seed` for fixtures and example data, not schema evolution.
- Use `test` to validate permissions, schema invariants, and API behavior in CI
  before rollout completion.

## Common Patterns

### Local Development Loop

```bash
surrealkit sync --watch
surrealkit seed
surrealkit test --tag smoke
```

### Shared Environment Change

```bash
surrealkit rollout plan --name add_order_indexes
surrealkit rollout lint 20260410120000__add_order_indexes
surrealkit rollout start 20260410120000__add_order_indexes
# deploy app cutover
surrealkit rollout complete 20260410120000__add_order_indexes
```

### CI Validation

```bash
surrealkit sync
surrealkit seed
surrealkit test --fail-fast --json-out artifacts/surrealkit-tests.json
```

### Docker / Compose CI

The upstream image is distroless and exits after the command completes, so it
fits "apply schema then run tests" pipelines:

```yaml
services:
  surrealdb:
    image: surrealdb/surrealdb:latest
    command: start --user root --pass root memory
    healthcheck:
      test: ["CMD", "/surreal", "is-ready"]
      interval: 1s
      timeout: 5s
      retries: 30

  surrealkit:
    image: ghcr.io/surrealdb/surrealkit:latest
    depends_on:
      surrealdb:
        condition: service_healthy
    volumes:
      - ./database:/database:ro
    command:
      - --host=http://surrealdb:8000
      - --ns=my_ns
      - --db=my_db
      - --user=root
      - --pass=root
      - sync
```
