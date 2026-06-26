# Testing and Observability

## Test Layers

- Contract tests: validate OpenAPI against server behavior.
- Integration tests: run against real database and dependencies.
- End-to-end tests: verify critical user workflows through API surface.
- Chaos or resilience checks for timeout, retry, and partial failure behavior.

## Minimum Release Gate

Do not deploy unless all are true:

- Critical endpoint integration tests pass.
- Backward compatibility checks pass for current clients.
- Error handling paths are tested, not just success paths.
- Performance budget is within accepted threshold.

## Observability Baseline

Expose metrics for:

- Request count and latency by endpoint and status code.
- Error rate by endpoint and error code.
- Dependency latency and failure rate.
- Saturation signals (queue depth, worker utilization).

## Logging and Tracing

- Use structured logs with `request_id` and `actor_id` when available.
- Avoid logging secrets and sensitive fields.
- Propagate trace context across service boundaries.

## Alerting

- Alert on user-impacting symptoms first (error rate, p95 latency, saturation).
- Add runbook links in alerts for first response speed.
