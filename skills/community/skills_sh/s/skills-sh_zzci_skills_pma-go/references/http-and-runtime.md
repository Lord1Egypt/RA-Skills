# PMA-Go HTTP And Runtime

## HTTP Server

Default stack:

- stdlib `net/http`
- Chi router

Rules:

- centralize router construction in `internal/server`
- register middleware explicitly
- keep route registration readable

## Handler Pattern

- handlers should parse input, call services, and write responses
- move business rules out of handlers
- validate input before calling deeper layers
- keep response mapping consistent

## API Response Envelope

Use a response envelope only when the product already standardizes on it. Do not wrap everything by reflex.

## Middleware

Common middleware concerns:

- request logging
- panic recovery
- auth and authorization
- request IDs and correlation
- timeouts where appropriate

## Logging

- use slog for structured logs
- keep attribute names stable
- redact secrets and sensitive identifiers when needed
- attach request context fields consistently

## Observability

Adopt OpenTelemetry when deployment context requires it.

Focus areas:

- tracer and meter setup
- HTTP instrumentation
- DB instrumentation
- health and readiness endpoints
- trace correlation in logs

## Graceful Shutdown

- handle `SIGINT` and `SIGTERM`
- stop accepting new work before process exit
- let in-flight requests drain within a timeout
- close DB pools and telemetry exporters cleanly
