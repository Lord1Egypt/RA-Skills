# Language and Architecture Risk Checklists

Use only relevant sections for the current stack.

## Cross-Stack Core Checks

- input validation at trust boundaries
- null or optional handling on every data hop
- error propagation without silent swallowing
- idempotency of retries and background jobs
- backward compatibility for APIs and data contracts

## JavaScript and TypeScript

- unsafe `any` paths masking runtime errors
- missing runtime guards on external payloads
- async race conditions in shared mutable state
- unhandled promise rejections and partial failures
- bundling regressions from heavy dependencies

## Python

- mutable default arguments and hidden state leaks
- broad exception catches hiding root causes
- timezone-naive datetime operations
- ORM queries causing N+1 behavior
- serialization mismatches across boundaries

## Java, Kotlin, C#, Go

- transactional boundaries and rollback consistency
- thread safety and shared state contention
- panic or exception propagation to API layer
- resource lifecycle leaks (connections, streams)
- timeout and cancellation handling in I/O calls

## Data and Migration Paths

- destructive migrations without rollback plan
- implicit schema assumptions in old clients
- default values changing business meaning
- indexes missing for new query paths
- dual-write drift during transition windows

## Final Architecture Sanity Check

Before closing review, confirm:
- ownership boundaries are respected
- dependency direction did not regress
- observability exists for changed critical paths
