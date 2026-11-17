# Contracts and failure handling

Use for an API, remote call, queue or cache whose failure affects callers or stored state.

## Preserve the contract

Find existing consumers and the behavior they rely on: response shape, defaults, ordering, error semantics and duplicate handling. An additive change can still break a strict consumer. Keep compatibility, provide a transition or obtain an explicit decision to break it.

For pagination, choose stable ordering with a tie-breaker. Check empty, first/last and invalid pages; concurrent inserts should not silently duplicate or lose records under the promised semantics. Do not replace a response array with an envelope without handling existing clients. A cursor is not authorization: recheck the caller and scope on each page.

When concurrent edits could overwrite valid work, use the contract's revision/conditional-write mechanism, such as an ETag with `If-Match`. Test stale revisions and define conflict handling.

## Bound work and retries

Set timeouts and an overall deadline, including retries. A read-inactivity timeout may restart after each chunk and therefore does not bound total duration. Propagate cancellation. Retry only failures that can plausibly recover, with bounded attempts, backoff and jitter; respect `Retry-After` and the service's quota window. Authentication errors need corrected credentials, not repeated requests.

A write may have succeeded before the client timed out. For payments, jobs or other side effects, use a provider-supported idempotency key or an equivalent atomic deduplication mechanism. Reuse the same key for the same operation and reject a conflicting payload. Check the outcome before retrying an ambiguous result. Avoid multiplying retries across client, SDK and job layers.

For queues, verify duplicate and out-of-order delivery, partial failure and exhausted retries. Bound concurrency and backlog; define backpressure, rejection or a safe degraded mode under overload. Do not acknowledge work before its required effects are durable.

A database commit followed by event publication has a crash gap. When both must be reliable, use a transactional outbox or an equivalent atomic handoff, with idempotent consumers. Test a crash after commit but before publication and recovery without losing the event.

## Protect state and diagnostics

- Bind authorization and cache keys to the relevant identity/tenant. Include any input that changes the result, and define invalidation when permissions or data change.
- Verify webhook signatures over the required original payload, check replay constraints and deduplicate events before applying effects.
- Return stable, safe errors. Keep internal details and credentials out of responses and logs.
- Add only the telemetry needed to detect this failure: useful status, duration, correlation and bounded-cardinality dimensions. An alert should identify a user-visible problem and a useful response; [observability and performance](observability-and-performance.md) has more.

Verify the changed boundary with realistic failures. Report whether the evidence used a stub, local integration or live service.

## Sources

- [HTTP semantics, RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html)
- [Transactional outbox](https://microservices.io/patterns/data/transactional-outbox.html)
- [Google SRE: handling overload](https://sre.google/sre-book/handling-overload/)
- [Google SRE: monitoring distributed systems](https://sre.google/sre-book/monitoring-distributed-systems/)
