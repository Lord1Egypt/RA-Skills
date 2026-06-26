# PMA-Go Baseline

## Table of Contents

- [Scope](#scope)
- [Tech Stack](#tech-stack)
- [Dependency Freshness (Go)](#dependency-freshness-go)
- [Required Quality Gates](#required-quality-gates)
- [Project Layout](#project-layout)
- [Required Conventions](#required-conventions)
- [Error Handling](#error-handling)
- [Code Quality Standards](#code-quality-standards)


## Scope

This pack is for PMA-managed Go backends, API services, and CLI applications.

Goals:

- idiomatic Go
- explicit error handling
- strict linting and formatting
- reproducible builds
- operational and security defaults that are easy to review

## Tech Stack

### Required

| Category | Technology | Notes |
|---|---|---|
| Language | Go 1.26+ | latest stable |
| Format | gofmt and goimports | enforced in CI |
| Lint | golangci-lint v2 | includes revive, govet, errcheck, staticcheck |
| Errors | `fmt.Errorf` with `%w` | use `errors.Is` and `errors.As` |
| Logging | slog | structured logging |
| Modules | Go modules | commit `go.mod` and `go.sum` |
| Validation | go-playground/validator | input validation at boundaries |

### Default

| Category | Technology | Notes |
|---|---|---|
| HTTP server | stdlib `net/http` plus Chi | default router and middleware stack |
| Data access | sqlc plus pgx | compile-time SQL safety |
| Migration | goose | SQL or Go migrations |
| Config | koanf | defaults -> file -> env -> flags |
| CLI | Cobra plus pflag | subcommands and completions |
| Task runner | Task | consistent local automation |
| Hot reload | air | development only |

### Optional

| Category | Technology | When to adopt |
|---|---|---|
| Observability | OpenTelemetry | production tracing and metrics |
| High-perf logging | zerolog | only when measured overhead matters |
| RPC | connect-go plus buf | service-to-service RPC |
| DI | google/wire | large dependency graph |
| Release | GoReleaser | multi-platform release automation |

### Alternative

| Replaces | Technology | Notes |
|---|---|---|
| Chi | Gin | broader middleware ecosystem |
| sqlc plus pgx | GORM | CRUD-heavy internal tools |
| goose | golang-migrate | wider DB support |
| goose | Atlas | declarative schema management |
| koanf | envconfig | env-only services |

## Dependency Freshness (Go)

See `/pma references/workflow.md` *Dependency Freshness* for the cross-stack rule. Go-specific verification:

```bash
# All published versions of a module
go list -m -versions <module>

# Latest version (the trailing token of the line above)
go list -m -versions <module> | awk '{print $NF}'

# Find direct deps with newer minor/patch available
go list -u -m all | grep '\['

# Apply the latest patch within current major (safe default)
go get -u=patch ./...

# Apply latest minor within current major
go get -u ./...
go mod tidy

# Cross-check via pkg.go.dev for breaking-change notes before upgrading a major
```

When pinning to a non-latest version, note the reason in `go.mod` near the `require` block or in `docs/decisions/`:

```go
require (
    // PINNED: <module>@v1 — v2 requires Go 1.27; revisit after toolchain bump
    example.com/<module> v1.8.3
)
```

For major-version upgrades (`v2`, `v3`, …), Go requires updating the import path; treat that as a tracked refactor, not a routine bump.

## Required Quality Gates

Every PMA-Go project should define:

- `goimports -l .`
- `golangci-lint run`
- `go vet ./...`
- `go test ./...`
- `go test -cover ./...`
- `go build ./...`
- `go mod tidy` with no diff
- `gosec ./...`

## Project Layout

Use `cmd/` plus `internal/` for binary projects. Avoid `/pkg`.

```text
cmd/
  server/
  cli/
internal/
  config/
  server/
  handler/
  service/
  repository/
  model/
  middleware/
db/
  queries/
  migrations/
  sqlc.yaml
```

## Required Conventions

| Area | Convention |
|---|---|
| Context | pass `context.Context` first; never store it in structs |
| Interfaces | define them on the consumer side and keep them small |
| Constructors | `NewXxx(deps)` returning concrete types |
| Config | inject config structs; do not read env in business logic |
| Secrets | never log secrets |
| Imports | stdlib, external, internal groups via goimports |
| Testing | table-driven tests by default |

## Error Handling

Use a two-tier model:

- sentinel errors for conditions callers need to branch on
- wrapped errors for context propagation

Translate internal errors to safe HTTP responses at the edge.

## Code Quality Standards

- prefer immutable-style updates when practical
- keep functions under 50 lines when possible
- keep files focused and usually under 800 lines
- avoid deep nesting
- avoid unnecessary interfaces and abstractions
