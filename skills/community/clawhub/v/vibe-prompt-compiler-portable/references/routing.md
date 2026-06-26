# Portable Routing Guide

Use this guide when one request could fit multiple templates.

## Priority Rules

1. If the request mentions an error, regression, broken behavior, or stack trace, use `bugfix`.
2. If the request asks to improve structure without behavior changes, use `refactor`.
3. If the request is about routes, handlers, validation, auth, or backend behavior, use `api-backend`.
4. If the request centers on create/list/edit/delete around an entity, use `crud-feature`.
5. If the request is about pages, screens, components, forms, or visual structure, use `page-ui`.
6. If the request is about architecture, system boundaries, scaling, tenancy, isolation, queues, caching, or platform design, use `architecture-review`.
7. If the request is about external systems, third-party APIs, webhooks, internal services, SSO, payments, storage, or sync flows, use `integration`.
8. If the request is a greenfield app, MVP, prototype, or tool, use `new-project`.
9. If the request is about chat, summarization, extraction, generation, or LLM/agent features, use `ai-feature`.
10. If the request concerns hosting, env vars, release, Docker, CI/CD, or deployment, use `deployment`.
11. If the request is about scheduled jobs, background workers, agent loops, inbox processors, or recurring task systems, use `automation-workflow`.
12. Otherwise use `general`.

## Tie-Break Rules

When a request overlaps categories, prefer the narrowest risk-bearing type:

- bug symptoms + API surface change -> `bugfix`
- page change + backend wiring -> `crud-feature` if entity workflow is central, otherwise `page-ui`
- "design the system" + implementation later -> `architecture-review`
- external vendor or service handoff is central -> `integration`
- scheduled processing or agent orchestration is central -> `automation-workflow`
- vague platform change without enough specificity -> `general`

## Missing Information Policy

Ask a follow-up question only when one missing fact blocks useful progress. Otherwise compile with explicit assumptions.

## Default Assumptions by Type

### `architecture-review`

- prefer incremental evolution over rewrite
- keep one codebase when possible
- separate control plane from data plane when useful
- call out scaling and operational trade-offs explicitly

### `integration`

- prefer the simplest reliable integration path
- make auth, retries, idempotency, and failure behavior explicit
- separate transport concerns from business logic

### `automation-workflow`

- prefer observable, restartable workflows
- separate synchronous API paths from background execution
- include retries, idempotency, and alerting assumptions

## Confidence Heuristic

If you can state a clear current task in one sentence, do not ask a question first.
If you cannot define the current task without inventing core product behavior, ask one blocking question.
