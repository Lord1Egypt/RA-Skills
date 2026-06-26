---
name: REST API
slug: rest-api
version: 1.0.0
homepage: https://clawic.com/skills/rest-api
description: Build production-ready REST APIs with contract-first design, secure auth, robust testing, and deployment runbooks.
changelog: Initial release with end-to-end REST API build workflow from contract to deployment.
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## Setup

On first use, read `setup.md` for integration behavior and memory initialization.

## When to Use

Use this skill when the user wants to design, implement, secure, test, and ship a REST API from scratch or harden an existing API for production.

This skill covers contract-first design, endpoint conventions, authentication and authorization, persistence strategy, test plans, observability, and release checklists.

## Architecture

Working memory lives in `~/rest-api/`. See `memory-template.md` for structure and status behavior.

```
~/rest-api/
├── memory.md                     # HOT: active API project context
├── contracts/                    # WARM: OpenAPI specs and compatibility notes
├── decisions/                    # WARM: ADR-style technical decisions
├── tests/                        # WARM: test plans and quality gates
├── operations/                   # WARM: runbooks and incident notes
└── archive/                      # COLD: closed projects and old versions
```

## Quick Reference

Load only what is needed for the current API task.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory schema | `memory-template.md` |
| Contract-first design | `api-contract.md` |
| Endpoint conventions and errors | `endpoint-design.md` |
| Auth and API security controls | `auth-and-security.md` |
| Data model and migrations | `persistence-and-migrations.md` |
| Test strategy and telemetry | `testing-and-observability.md` |
| Pre-release readiness gate | `deployment-checklist.md` |

## Core Rules

### 1. Start From the Contract, Not the Controller
Define resources, payload schemas, status codes, and error shapes in OpenAPI before writing handlers.

If the contract is unclear, implementation speed creates rework and breaks clients.

### 2. Keep Endpoint Semantics Predictable
Use stable naming, plural resources, and correct HTTP methods. Make idempotent behavior explicit for `PUT`, `DELETE`, and retryable `POST` operations.

Predictable semantics reduce client bugs and support safer retries.

### 3. Enforce Security by Default
Require authentication on non-public endpoints, apply authorization checks at resource boundary, validate input strictly, and sanitize output.

Never rely on frontend validation as a security control.

### 4. Design for Failure Paths First
Specify error classes, timeout strategy, rate-limit behavior, and fallback expectations before scaling happy-path code.

APIs fail in production at edges, not in demos.

### 5. Make Data Changes Backward Compatible
Use additive schema migrations first, backfill data safely, and only remove old fields after client migration windows close.

Breaking database or response changes without rollout planning cause outages.

### 6. Test Contract, Behavior, and Operations
Cover OpenAPI contract validation, integration tests against real infrastructure, and end-to-end tests for critical user journeys.

Unit tests alone do not prove API reliability.

### 7. Ship With Observability and Runbooks
Expose request metrics, structured errors, trace identifiers, and health indicators. Document recovery steps for known failure modes.

If an API cannot be observed, it cannot be operated safely.

## Common Traps

- Building endpoints before defining response and error contracts -> incompatible clients and patchwork fixes.
- Mixing auth, business logic, and transport concerns in handlers -> brittle code and hidden security gaps.
- Treating pagination and filtering as optional -> unstable list endpoints and expensive queries.
- Returning inconsistent error bodies across services -> poor client DX and weak automation.
- Shipping without migration rollback steps -> long incidents when a release fails.

## Security & Privacy

**Data that leaves your machine:**
- None by default.

**Data that stays local:**
- API project context and decisions under `~/rest-api/`.

**This skill does NOT:**
- Call undeclared external endpoints by default.
- Store secrets automatically.
- Modify infrastructure without explicit user instruction.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `backend` - System design and backend architecture decisions.
- `auth` - Authentication, session strategy, and credential safety.
- `http` - HTTP protocol details and request-response behavior.
- `api` - Third-party API integration references.

## Feedback

- If useful: `clawhub star rest-api`
- Stay updated: `clawhub sync`
