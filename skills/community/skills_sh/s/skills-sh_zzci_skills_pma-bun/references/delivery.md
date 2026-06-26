# PMA-Bun Delivery

## Compile Pipeline

When the repository ships a standalone binary:

- build the frontend first when static assets are embedded
- generate asset maps and embedded migration modules as explicit steps
- restore stub files after compilation, including interrupted runs
- keep compile-time file rewriting confined to dedicated scripts
- write checksums or release metadata as part of the build output when distribution needs it

## Hooks And Tooling

- keep lint and typecheck fast enough for frequent local runs
- use post-tool or stop hooks only when the repository already standardizes on them
- avoid hook logic that mutates code unpredictably

## Security Patterns

Review these areas before merge:

- password hashing
- constant-time secret comparison
- rate limiting for public endpoints
- CSRF protection when serving browser-facing state-changing routes
- XSS avoidance by rejecting raw HTML injection paths
- secret redaction in logs
- safe handling of local encryption keys, bootstrap tokens, or lock files when the project uses them

Pre-commit checklist:

- no hardcoded secrets
- all user inputs validated
- SQL injection blocked through parameterized access
- auth and authorization checked
- rate limits applied where needed
- error messages do not leak internals

## Observability

Adopt only when the deployment context needs it.

Recommended shape:

- OpenTelemetry for traces and metrics
- pino logs with request correlation
- health endpoint for liveness
- human-readable local logs for developer workflows when the service is frequently run interactively

## CI Pipeline

Typical jobs:

- lint
- test
- coverage
- build
- compile when the repository distributes binaries

If the project needs security audit or DB bootstrap jobs, keep them explicit and reproducible.

## Docker

When containerizing:

- use reproducible Bun images
- copy only necessary build inputs
- set non-root execution where possible
- keep env injection external to the image
- document whether the container runs source mode or precompiled binary mode

## Workspaces

Only relevant in the *Monorepo* layout (see `baseline.md`).

- keep workspace boundaries explicit
- centralize shared configs
- avoid hidden cross-package imports
- make package exports intentional; the API package should not be imported by the frontend at runtime — dev integration runs through nsl, not via cross-package middleware mounting

## Git Conventions

- use English remote-visible metadata
- use conventional commits
- keep PR summaries short and test plans explicit

## API Review Checklist

Before merge, verify:

- request and response schemas match behavior
- docs match runtime validation
- error mapping is consistent
- auth boundaries are explicit
- migration impact is understood
- compile-time embedded assets and migrations stay in sync with source behavior
