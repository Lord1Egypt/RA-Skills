# Observability and performance

Use for a new service, endpoint, job or dependency, a logging or alerting change, an SLO, or a latency, throughput or load target. Timeouts, retries, idempotency and overload belong to [contracts and failure handling](api-design.md).

## Instrument the new path

In the same change, add the telemetry that answers an operator's questions: is it working, for whom is it failing, since when, and which dependency is slow?

- Write structured log events with a stable event name, level, service, version and the current trace ID. Log an error once, where it is handled, with its cause.
- Log identifiers rather than personal data. Never log passwords, tokens, session IDs, keys, connection strings or full request bodies, and neutralize line breaks in user-supplied text. A test can assert that a known secret never reaches captured logs.
- Propagate trace context across HTTP calls and queue messages, following W3C Trace Context and the OpenTelemetry semantic conventions where the project uses them.
- Record latency as a histogram so percentiles can be computed. Keep metric labels bounded: route templates, not raw URLs or user IDs.
- Record security events such as sign-in failures, permission changes and administrative actions, with actor, action, target, outcome and time.

## Alert on symptoms

Page only for urgent, user-visible symptoms that someone can act on now, such as an error rate or latency outside its objective. Internal causes like high CPU belong on dashboards or tickets. Each alert needs a note on what to check first.

## SLO basics

A service level indicator is a ratio of good events to all events, for example requests served successfully within 300 ms. Choose a few that users feel: availability, latency, correctness or freshness. Set the objective below 100 percent; the remainder is an error budget, with an agreed response for when it runs out. Alert on how fast the budget is burning rather than on single bad minutes.

## Baseline and target before optimizing

Set the target first, as a percentile at a stated load: "p95 under 300 ms at 200 requests per second". Measure with production-like data and profile to see where the time goes. Report p50, p95 and p99, not averages. Change one thing, measure again the same way, and keep the change only if the numbers improved.

Usual causes are N+1 queries, missing indexes, unbounded result sets, chatty remote calls, exhausted connection pools and lock contention. A cache needs an explicit lifetime and invalidation rule. For web pages, the Core Web Vitals thresholds apply at the 75th percentile of real visits.

## Prove it works

Trigger the failure path in a test or staging environment and confirm that the log event, the trace with its error status, the metric and any alert appear. Back every performance claim with before and after numbers.

## Sources

- [Google SRE book: monitoring distributed systems](https://sre.google/sre-book/monitoring-distributed-systems/)
- [Google SRE workbook: alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)
- [W3C Trace Context](https://www.w3.org/TR/trace-context/)
- [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/)
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- [Web Vitals](https://web.dev/articles/vitals)
