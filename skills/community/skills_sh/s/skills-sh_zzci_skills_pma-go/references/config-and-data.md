# PMA-Go Config And Data

## Configuration Layering

Load config in this order:

```text
defaults -> config file -> environment variables -> CLI flags
```

Rules:

- keep config structs explicit
- validate after load
- map env vars predictably
- keep config-file format aligned with the repository convention
- never read process env directly inside domain logic

## koanf Guidance

- keep loading centralized in `internal/config`
- separate loading, validation, and defaulting concerns
- document required env vars and defaults

## Database Default: sqlc Plus pgx

Prefer this when:

- SQL is part of the product logic
- compile-time query safety matters
- the team wants direct control over SQL

Rules:

- store queries under `db/queries`
- keep generated code isolated
- manage connection pools centrally
- pass `context.Context` through all DB calls

## Migration Guidance

- use goose by default
- commit migrations
- avoid silent schema drift
- ensure CI or local verification can apply migrations reproducibly

## GORM Alternative

Use GORM when:

- CRUD speed matters more than SQL transparency
- the schema is simple enough that ORM conventions help more than they hurt

If selected, keep the choice explicit and do not mix ad hoc sqlc and ORM patterns without a clear boundary.

## Repository Boundaries

- handlers manage transport
- services manage business rules
- repositories manage persistence
- keep DB-specific errors translated before they leak into unrelated layers
