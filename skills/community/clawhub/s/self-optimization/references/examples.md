# Self-Optimization Examples

Concrete examples showing how to capture signal, link recurrence, promote stable rules, and extract reusable skills.

## Learning: User Correction

````markdown
## [LRN-20260401-001] correction

**Logged**: 2026-04-01T09:20:00Z
**Priority**: high
**Status**: pending
**Area**: tests

### Summary
Fixture scope should follow existing repo conventions, not default assumptions

### Details
The initial change used function-scoped fixtures everywhere. The user clarified
that this repo intentionally uses module-scoped fixtures for database-heavy test
setup to reduce suite runtime and setup churn.

### Suggested Action
Before creating new fixtures, inspect existing test infrastructure and match the
dominant scope unless there is a strong reason not to.

### Metadata
- Source: user_feedback
- Related Files: tests/conftest.py
- Tags: pytest, fixtures, conventions

---
````

## Learning: Recurring Pattern With Dedupe

````markdown
## [LRN-20260401-002] best_practice

**Logged**: 2026-04-01T10:10:00Z
**Priority**: high
**Status**: pending
**Area**: backend

### Summary
API schema changes must trigger client regeneration before type checks

### Details
The first fix updated the OpenAPI schema but skipped client regeneration. This
caused downstream type failures and stale client methods in a second task the
same week.

### Suggested Action
Whenever API contract files change, regenerate the client before running type
checks or tests that depend on generated types.

### Metadata
- Source: debugging
- Related Files: openapi.yaml, src/client/generated.ts
- Tags: api, codegen, types
- Pattern-Key: api.codegen.regenerate-after-schema-change
- Recurrence-Count: 2
- First-Seen: 2026-03-27
- Last-Seen: 2026-04-01
- See Also: ERR-20260327-004, LRN-20260328-003

---
````

## Learning: Promoted To Repo Guidance

````markdown
## [LRN-20260401-003] best_practice

**Logged**: 2026-04-01T11:00:00Z
**Priority**: high
**Status**: promoted
**Area**: backend

### Summary
Payment handlers must echo request correlation IDs in all responses

### Details
Tracing breaks if handlers drop the `X-Correlation-ID` header. This issue
surfaced across multiple endpoints and affected debugging for downstream teams.

### Suggested Action
Treat correlation-ID passthrough as a required response concern for all payment
handlers and middleware.

### Metadata
- Source: debugging
- Related Files: src/middleware/correlation.ts, src/routes/payments.ts
- Tags: tracing, observability, api
- Pattern-Key: api.correlation-id.passthrough
- Recurrence-Count: 3
- First-Seen: 2026-03-20
- Last-Seen: 2026-04-01

### Resolution
- **Resolved**: 2026-04-01T11:15:00Z
- **Commit/PR**: docs only
- **Notes**: Promoted to `CLAUDE.md` and `AGENTS.md` as a prevention rule

---
````

## Error: Non-Obvious Failure

````markdown
## [ERR-20260401-001] docker_build

**Logged**: 2026-04-01T08:45:00Z
**Priority**: high
**Status**: pending
**Area**: infra

### Summary
Docker build fails on Apple Silicon because the selected base image has no ARM variant

### Error
```text
error: failed to solve: python:3.11-slim: no match for platform linux/arm64
```

### Context
- Command: `docker build -t myapp .`
- Environment: Apple Silicon host
- Dockerfile base image: `python:3.11-slim`

### Suggested Fix
Use `--platform linux/amd64` for the build or choose an ARM-compatible base image.

### Metadata
- Reproducible: yes
- Related Files: Dockerfile
- See Also: LRN-20260401-004

---
````

## Error: Repeated Incident Worth Promotion

````markdown
## [ERR-20260401-002] payment_timeout

**Logged**: 2026-04-01T12:40:00Z
**Priority**: critical
**Status**: pending
**Area**: backend

### Summary
Checkout flow times out against the payment provider during peak traffic

### Error
```text
TimeoutError: POST https://payments.example.com/charge exceeded 30000ms
```

### Context
- Endpoint: `POST /api/checkout`
- Observed during lunch and evening traffic spikes
- Current retry strategy: none

### Suggested Fix
Add retries with backoff and introduce a circuit breaker to avoid cascading failures.

### Metadata
- Reproducible: yes
- Related Files: src/services/payment.ts
- See Also: ERR-20260326-002, ERR-20260329-001

---
````

## Feature Request: Missing Capability

````markdown
## [FEAT-20260401-001] export_to_csv

**Logged**: 2026-04-01T13:05:00Z
**Priority**: medium
**Status**: pending
**Area**: backend

### Requested Capability
Export analysis results as CSV

### User Context
The user shares weekly results with non-technical stakeholders and currently
reformats command output by hand.

### Complexity Estimate
simple

### Suggested Implementation
Add an `--output csv` mode alongside the existing structured output formats.

### Metadata
- Frequency: recurring
- Related Features: analyze, export

---
````

## Feature Request: Resolved And Promoted

````markdown
## [FEAT-20260401-002] dark_mode

**Logged**: 2026-04-01T14:10:00Z
**Priority**: low
**Status**: resolved
**Area**: frontend

### Requested Capability
Dashboard dark mode

### User Context
Users work late and find the bright theme fatiguing.

### Complexity Estimate
medium

### Suggested Implementation
Use CSS variables, add a user toggle, and support system theme detection.

### Metadata
- Frequency: recurring
- Related Features: settings, theming

### Resolution
- **Resolved**: 2026-04-08T17:30:00Z
- **Commit/PR**: #142
- **Notes**: Implemented and summarized into frontend theming guidance

---
````

## Learning: Promoted To Skill

````markdown
## [LRN-20260401-004] best_practice

**Logged**: 2026-04-01T15:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/docker-platform-fixes
**Area**: infra

### Summary
Container builds on Apple Silicon need an explicit platform strategy

### Details
Multiple build failures traced back to hidden platform assumptions in base
images and local developer machines. The fix pattern is stable and reusable.

### Suggested Action
Document a default build strategy and extract a reusable skill so future
sessions can apply the same fix quickly.

### Metadata
- Source: debugging
- Related Files: Dockerfile, docker-compose.yml
- Tags: docker, arm64, build
- Pattern-Key: docker.platform.strategy
- Recurrence-Count: 3
- First-Seen: 2026-03-21
- Last-Seen: 2026-04-01
- See Also: ERR-20260401-001, ERR-20260321-003

### Resolution
- **Resolved**: 2026-04-01T15:20:00Z
- **Commit/PR**: docs only
- **Notes**: Extracted to `skills/docker-platform-fixes`

---
````

## What Good Entries Have In Common

- The summary is a prevention rule, not just a diary note.
- The details explain why the lesson matters.
- Metadata makes recurrence detectable.
- Repeated issues point toward promotion, not endless duplicate logging.
- Broad stable fixes graduate into reusable skills.
