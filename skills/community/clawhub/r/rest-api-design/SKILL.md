---
name: rest-api-design
description: "REST API design patterns: resource naming, HTTP methods, status codes, pagination, filtering, authentication, rate limiting, versioning, and response formats. Use when designing new endpoints, reviewing API contracts, or planning API strategies. Trigger phrases: API design, endpoint design, REST API, API versioning, schema design. Adapted from everything-claude-code by @affaan-m (MIT)"
metadata: {"clawdbot":{"emoji":"🔌","requires":{"bins":[],"env":[]},"os":["darwin","linux","win32"]}}
---

# API Design Patterns

Design consistent, developer-friendly REST APIs with resource naming, HTTP semantics, and versioning.

## When to Activate

- Designing new API endpoints
- Reviewing existing API contracts
- Adding pagination, filtering, or authentication
- Planning API versioning strategy
- Building public or partner-facing APIs

## Quick Start

1. Use nouns (plural, kebab-case) for resource URLs, not verbs
2. Apply correct HTTP method (GET/POST/PUT/PATCH/DELETE)
3. Return appropriate status codes (200/201/400/401/403/404/429)
4. Use consistent response format (data + metadata + error structure)
5. Implement pagination (cursor-based preferred) and filtering
6. Require authentication and check authorization per resource

## Key Concepts

- **Resource naming** — Plural nouns in kebab-case; use verbs sparingly for actions
- **HTTP semantics** — Each method has idempotency/safety properties; honor them
- **Status codes** — Signal intent precisely (400 for validation, 422 for semantic error)
- **Error format** — Consistent structure with codes, messages, and field details
- **Versioning** — URL path versioning (v1, v2); non-breaking changes don't need new version

## Common Usage

Most frequent patterns:
- CRUD endpoints (GET, POST, PUT, PATCH, DELETE)
- List endpoints with pagination and filtering
- Sub-resources for relationships (users/:id/orders)
- Authentication headers and permission checks
- Rate limiting headers and strategies

## References

- `references/resource-design.md` — URL structure, naming rules, HTTP methods, status codes, response formats
- `references/pagination-filtering-auth.md` — Pagination strategies, filtering, sorting, authentication, rate limiting, versioning, and checklist
