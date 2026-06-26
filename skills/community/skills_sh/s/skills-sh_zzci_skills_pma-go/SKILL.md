---
name: pma-go
description: Go implementation guide for PMA-managed service and CLI projects. Covers project layout (cmd/internal), strict linting with golangci-lint v2, database access (sqlc + pgx or GORM), HTTP patterns (stdlib + Chi or Gin), layered config with koanf, structured logging with slog, OpenTelemetry observability, and CI quality gates. Use when implementing, scaffolding, or reviewing a Go service or CLI in a PMA repo.
---

# Go Project Implementation Guide

Use this skill together with `/pma`. `/pma` controls workflow, approval, and task tracking; this guide defines the implementation baseline after approval.

Keep this entry file lean. Load only the reference packs needed for the task.

## Scope

For PMA-managed Go backends, API services, and CLI applications.

Not for embedded targets, library-only modules without binaries, or non-PMA projects.

## Loading Order

1. Always load `references/baseline.md` first.
2. Load `references/config-and-data.md` for config layering, validation, sqlc, pgx, GORM, and migrations.
3. Load `references/http-and-runtime.md` for handlers, middleware, logging, observability, and shutdown.
4. Load `references/delivery.md` for lint, tests, task runners, security review, CI, and Git workflow.

## Quick Routing

- New service or CLI setup: `references/baseline.md`
- koanf config, env mapping, DB access, migrations, repository boundaries: `references/config-and-data.md`
- HTTP server, response envelopes, auth middleware, slog, tracing, shutdown: `references/http-and-runtime.md`
- quality gates, lint, tests, Taskfile, security checklist, CI, PR readiness: `references/delivery.md`

## Reference Packs

- `references/baseline.md`
  Stack defaults, quality gates, layout, conventions, error model, and code quality standards.
- `references/config-and-data.md`
  Config layering with koanf, validation, sqlc plus pgx, GORM alternative, and migration rules.
- `references/http-and-runtime.md`
  Router structure, handler patterns, middleware, logging, observability, and graceful shutdown.
- `references/delivery.md`
  Lint config, testing, task runner expectations, security checks, CI, and Git conventions.

If the repo already diverges from these defaults, make the divergence explicit and apply it consistently across code, docs, and CI.
