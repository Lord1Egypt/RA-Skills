---
name: rest-best-practices
description: Deep REST workflow—resource modeling, HTTP methods and safety, status codes, errors, pagination, caching, versioning, and idempotency. Use when designing HTTP APIs or reviewing controllers and gateways.
---

# REST Best Practices (Deep Workflow)

REST is **HTTP semantics** used consistently: **resources** as nouns, **methods** with meaning, **predictable** errors, and **cacheable** reads where safe.

## When to Offer This Workflow

**Trigger conditions:**

- Designing public or partner HTTP APIs
- Inconsistent verbs (GET with side effects); wrong status codes
- CDN/caching surprises; client retry storms on POST

**Initial offer:**

Use **six stages**: (1) resource model, (2) methods & safety, (3) status & errors, (4) pagination & filtering, (5) caching & conditional requests, (6) versioning & evolution). Confirm JSON conventions and authentication model.

---

## Stage 1: Resource Model

**Goal:** Clear collection vs item resources; relationships via sub-paths or hypermedia links (HATEOAS optional).

**Exit condition:** Table or diagram of resources, identifiers, and canonical URLs.

---

## Stage 2: Methods & Safety

**Goal:** GET/HEAD safe and idempotent; POST for creation or non-idempotent actions; PUT replaces; PATCH partial; DELETE removes.

### Anti-patterns

- Non-idempotent GET; overloaded POST for everything without documented patterns

---

## Stage 3: Status & Errors

**Goal:** Correct 4xx vs 5xx; consistent error body (e.g., RFC 7807 Problem Details) with stable `type` codes and optional `instance` for support.

---

## Stage 4: Pagination & Filtering

**Goal:** Cursor pagination for large lists; document sort/filter query params; cap page sizes.

---

## Stage 5: Caching & Conditional Requests

**Goal:** ETag/Last-Modified for cacheable GET; Cache-Control directives; validate with intermediaries (CDN) when used.

---

## Stage 6: Versioning & Evolution

**Goal:** URL prefix or header versioning; deprecation policy; **Idempotency-Key** on POST when clients retry.

---

## Final Review Checklist

- [ ] Resource model clear and consistent
- [ ] HTTP methods match semantics; GET is safe
- [ ] Status codes and errors consistent
- [ ] Pagination and filtering documented
- [ ] Caching headers where appropriate
- [ ] Versioning and idempotency strategy

## Tips for Effective Guidance

- Not everything is CRUD—model commands as sub-resources or task resources explicitly.
- Pair with **openapi-spec** for contract-first workflows.

## Handling Deviations

- Internal APIs still benefit from the same discipline—future consumers are often external.
