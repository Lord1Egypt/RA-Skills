# Entry Examples

Concrete examples of well-formatted engineering entries with all fields.

## Learning: Architecture Debt (Monolith Coupling)

```markdown
## [LRN-20250210-001] architecture_debt

**Logged**: 2025-02-10T09:30:00Z
**Priority**: high
**Status**: pending
**Area**: design

### Summary
Tight coupling between OrderService and InventoryService in the monolith prevents independent deployment

### Details
OrderService directly imports InventoryService to check stock before placing orders.
InventoryService imports OrderService to update order status after stock reservation.
This circular dependency means both services must be deployed together, making the
planned microservice extraction impossible without a significant refactor. Found during
the sprint planning for the inventory service extraction milestone.

### Suggested Action
Introduce an event-driven pattern: OrderService publishes OrderPlaced events,
InventoryService subscribes and publishes StockReserved events. Use an in-process
event bus now (e.g., MediatR or EventEmitter) to decouple without infrastructure changes.
Extract to message broker (RabbitMQ/SQS) during microservice migration.

### Metadata
- Source: investigation
- Category: architecture_debt
- Related Files: src/services/OrderService.ts, src/services/InventoryService.ts
- Tags: coupling, circular-dependency, microservices, event-driven
- Pattern-Key: arch.circular_dependency
- Recurrence-Count: 1
- First-Seen: 2025-02-10

---
```

## Learning: Testing Gap (Payment Flow)

```markdown
## [LRN-20250212-002] testing_gap

**Logged**: 2025-02-12T14:15:00Z
**Priority**: high
**Status**: pending
**Area**: code_review

### Summary
Integration tests missing for the entire payment processing flow — only unit tests with mocked Stripe client

### Details
Code review for PR #287 revealed that payment processing has 94% unit test coverage
but zero integration tests. All Stripe API calls are mocked. When Stripe changed their
error response format in API version 2024-12-18, our error handling silently failed.
The customer-facing error was "Unknown error" instead of the specific decline reason.
This went unnoticed for 3 days until a customer complaint.

### Suggested Action
1. Add integration test suite using Stripe test mode API keys
2. Pin Stripe API version in client config and test against it
3. Add contract test: verify error response schema matches our parser
4. Run integration tests nightly (too slow for every PR)

### Metadata
- Source: code_review
- Category: testing_gap
- Related Files: src/services/PaymentService.ts, tests/unit/payment.test.ts
- Tags: stripe, integration-tests, payment, api-contract
- See Also: ENG-20250209-001

---
```

## Learning: Performance Regression (N+1 Query)

```markdown
## [LRN-20250215-003] performance_regression

**Logged**: 2025-02-15T11:00:00Z
**Priority**: high
**Status**: resolved
**Area**: implementation

### Summary
N+1 query in user listing endpoint — 1 query for users + 1 query per user for their organization

### Details
The GET /api/users endpoint was taking 3.2s for 200 users. APM trace showed 201 database
queries: one SELECT for the user list, then one SELECT per user to fetch their org name
for display. The ORM (Prisma) lazy-loads relations by default. Adding `include: { organization: true }`
to the query reduced it to 1 query with a JOIN, bringing response time to 45ms.

### Suggested Action
Audit all list endpoints for lazy-loaded relations. Add a lint rule or code review
checklist item: "list endpoints must eager-load displayed relations."

### Metadata
- Source: monitoring
- Category: performance_regression
- Related Files: src/routes/users.ts, src/models/user.ts
- Tags: n-plus-one, prisma, query-optimization, orm
- Pattern-Key: perf.n_plus_one
- Recurrence-Count: 3
- First-Seen: 2025-01-20
- Last-Seen: 2025-02-15

### Resolution
- **Resolved**: 2025-02-15T12:30:00Z
- **Commit/PR**: #312
- **Root Cause**: Prisma lazy-loading default on relation fields
- **Notes**: Added `include` clause. Opened follow-up ticket to audit other list endpoints.

---
```

## Engineering Issue: Build Failure (Node Version Mismatch)

```markdown
## [ENG-20250218-A1B] build_failure

**Logged**: 2025-02-18T08:45:00Z
**Priority**: high
**Status**: resolved
**Area**: ci_cd

### Summary
CI build fails on GitHub Actions — node-gyp compilation error due to Node 22 vs project requiring Node 20 LTS

### Error
```
npm ERR! code 1
npm ERR! path /home/runner/work/app/node_modules/bcrypt
npm ERR! command failed
npm ERR! gyp ERR! build error
npm ERR! gyp ERR! stack Error: `make` failed with exit code: 2
npm ERR! node-pre-gyp ERR! build error
```

### Context
- GitHub Actions runner: ubuntu-latest
- Node version on runner: 22.1.0
- Project .nvmrc: 20.11.1
- Trigger: Dependabot PR updated actions/setup-node from v3 to v4
- The setup-node v4 action defaults to the runner's node if .nvmrc is not explicitly referenced

### Impact
All PRs blocked from merging. Main branch CI red for 2 hours.

### Suggested Fix
Pin Node version in CI workflow: `node-version-file: '.nvmrc'` in setup-node config.
Add engines field to package.json: `"engines": { "node": ">=20 <21" }`.

### Metadata
- Reproducible: yes
- Environment: ci
- Related Files: .github/workflows/ci.yml, .nvmrc, package.json
- See Also: ENG-20250115-C3D

### Resolution
- **Resolved**: 2025-02-18T10:15:00Z
- **Commit/PR**: #318
- **Root Cause**: setup-node v4 ignores .nvmrc unless explicitly configured with node-version-file
- **Notes**: Also added engines field to package.json as a second safeguard

---
```

## Engineering Issue: Dependency CVE (Lodash Prototype Pollution)

```markdown
## [ENG-20250220-B2C] dependency_cve

**Logged**: 2025-02-20T16:00:00Z
**Priority**: critical
**Status**: resolved
**Area**: implementation

### Summary
CVE-2020-8203: lodash prototype pollution vulnerability — used directly in request validation middleware

### Error
```
npm audit
lodash  <4.17.20
Severity: critical
Prototype Pollution - https://github.com/advisories/GHSA-p6mc-m468-83gw
fix available via `npm audit fix --force`
```

### Context
- lodash@4.17.15 pinned in package-lock.json
- Used in src/middleware/validate.ts for deep merge of request defaults
- The vulnerable `_.defaultsDeep()` is called on user-supplied request body
- Exploitable: attacker can inject `__proto__` properties via POST body

### Impact
Critical security vulnerability. Attacker can pollute Object prototype on the server,
potentially escalating to RCE depending on downstream code.

### Suggested Fix
1. Immediate: upgrade lodash to >=4.17.20
2. Medium-term: replace lodash.defaultsDeep with structuredClone + manual merge
3. Long-term: add `npm audit --audit-level=critical` to CI pipeline as a gate

### Metadata
- Reproducible: yes
- Environment: local, ci, staging, production
- Related Files: package.json, package-lock.json, src/middleware/validate.ts

### Resolution
- **Resolved**: 2025-02-20T17:30:00Z
- **Commit/PR**: #325 (emergency patch)
- **Root Cause**: lodash pinned to vulnerable version, no audit gate in CI
- **Notes**: Added `npm audit --audit-level=critical` to CI. Scheduled lodash removal for next sprint.

---
```

## Feature Request: Automated Architecture Fitness Functions

```markdown
## [FEAT-20250222-001] architecture_fitness_functions

**Logged**: 2025-02-22T10:00:00Z
**Priority**: medium
**Status**: pending
**Area**: design

### Requested Capability
Automated architecture fitness functions that run in CI to detect layer violations,
circular dependencies, and forbidden imports between modules

### Engineering Context
We keep finding architecture violations during code review (3 times in the last sprint).
By the time a reviewer catches it, the code is already built on top of the violation.
Automated detection would catch these at PR time, saving review cycles and preventing
tech debt from accumulating.

### Complexity Estimate
medium

### Suggested Implementation
1. Use dependency-cruiser for JavaScript/TypeScript import graph analysis
2. Define rules: no direct imports from `domain/` to `infrastructure/`, no circular deps
3. Add as CI step: `npx depcruise --validate .dependency-cruiser.cjs src/`
4. Configure `.dependency-cruiser.cjs` with forbidden patterns
5. Consider ArchUnit equivalent for backend if using Java/Kotlin

### Metadata
- Frequency: recurring (architecture violations found 3x in last sprint)
- Related Features: CI pipeline, code review checklist

---
```

## Learning: Promoted to ADR

```markdown
## [LRN-20250225-004] architecture_debt

**Logged**: 2025-02-25T09:00:00Z
**Priority**: high
**Status**: promoted
**Promoted**: docs/decisions/ADR-012.md
**Area**: design

### Summary
Database queries from API handlers must go through repository layer — direct ORM calls in route handlers cause untestable, tightly-coupled code

### Details
Found direct Prisma calls in 12 route handlers during a test coverage push. Each handler
was importing PrismaClient directly, making it impossible to mock the database in unit tests
without also mocking the ORM. This also means query logic is scattered across handlers
instead of centralized in repositories.

### Suggested Action
Enforce repository pattern: all database access through repository classes. Add a lint
rule (eslint-plugin-import) to forbid importing PrismaClient outside of `src/repositories/`.

### Metadata
- Source: code_review
- Category: architecture_debt
- Related Files: src/routes/*.ts, src/repositories/
- Tags: repository-pattern, prisma, separation-of-concerns, testability
- See Also: LRN-20250210-001, LRN-20250218-002

---
```

## Learning: Promoted to Skill

```markdown
## [LRN-20250228-005] performance_regression

**Logged**: 2025-02-28T14:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/n-plus-one-detection
**Area**: implementation

### Summary
Systematic approach to detecting and fixing N+1 queries in Prisma/TypeORM applications

### Details
After encountering N+1 queries for the fourth time across different services, developed
a systematic detection approach: enable query logging, load-test list endpoints, count
queries per request, and fix with eager loading or DataLoader pattern.

### Suggested Action
Apply the detection checklist to all list endpoints. Use the extracted skill for future
projects using ORMs with lazy-loading defaults.

### Metadata
- Source: investigation
- Category: performance_regression
- Related Files: src/routes/users.ts, src/routes/orders.ts, src/routes/products.ts
- Tags: n-plus-one, orm, prisma, typeorm, dataloader
- Pattern-Key: perf.n_plus_one
- Recurrence-Count: 4
- First-Seen: 2025-01-20
- Last-Seen: 2025-02-28
- See Also: LRN-20250215-003, LRN-20250120-007, LRN-20250205-002

---
```
