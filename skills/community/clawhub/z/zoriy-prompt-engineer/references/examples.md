# Prompt Examples

## QUICK Mode

### Example: Add JWT auth to Express API

```
You are working as ClaudeKit Engineer.
Use Context7 for current JWT library docs and Express middleware patterns.

Goal: Add JWT authentication middleware to an existing Express.js REST API.

Constraints:
- Use environment variables for secrets (no hardcoded values)
- Token expiry configurable via env
- Return standardized error responses

Deliverables:
- auth middleware file
- updated route registrations
- .env.example additions
- brief validation: test protected route returns 401 without token
```

---

## FULL Mode

### Example: Build a REST API with PostgreSQL

```
You are working as ClaudeKit Engineer.
Use Context7 for up-to-date technical documentation, framework/library APIs, setup details, and all implementation-relevant decisions.

Goal:
Build a production-shaped REST API using Node.js + Express + PostgreSQL with proper architecture.

Required Context:
- Stack: Node.js 20+, Express 5, PostgreSQL 15, Prisma ORM
- Auth: JWT (access + refresh tokens)
- Environment: Docker Compose for local dev

Constraints:
- No hardcoded secrets — all config via env vars
- No raw SQL unless Prisma cannot handle it (document why)
- All endpoints must have input validation (zod)
- Error handling must be centralized

Phases:
1. Schema design — entities, relations, indexes
2. Prisma setup — models, migrations, seed
3. API layer — routes, controllers, services (separated concerns)
4. Auth — JWT middleware, refresh flow
5. Validation — zod schemas for all inputs
6. Error handling — global handler, typed errors
7. Docker Compose — app + db + optional pgAdmin

Deliverables:
- Working API with CRUD for at least one resource
- Auth flow (register, login, refresh, logout)
- Docker Compose up produces a running stack
- .env.example with all required variables documented
- README with setup and test instructions

Validation:
- curl examples for each endpoint
- Auth flow demonstrable end-to-end
- All zod validations tested with bad input

Special Rules:
- Architecture-first: define folder structure before writing code
- Config discipline: no magic strings, no hardcoded ports
- Avoid over-engineering: no microservices, no message queues unless explicitly requested
```

---

## MASTER Mode

### Example: Migrate monolith to modular architecture

```
You are working as ClaudeKit Engineer.
Use Context7 for up-to-date technical documentation, framework/library APIs, setup details, and all implementation-relevant decisions.
This is a large-scale refactoring and architectural migration task. Treat it as production-critical work.

Goal:
Migrate a Node.js Express monolith to a modular, domain-driven architecture without breaking existing functionality.

Required Context:
- Existing: single app.js, mixed concerns, no tests
- Target: modules per domain (auth, users, billing, notifications)
- DB: PostgreSQL via raw pg — migrate to Prisma
- CI: GitHub Actions

Constraints:
- Zero breaking changes to public API contract during migration
- Each phase must leave the app in a working, deployable state
- No hardcoded config — audit and extract all
- Test coverage must increase with each phase, not decrease

Phases:
1. AUDIT
   - Map all routes, middleware, DB queries, side effects
   - Identify circular dependencies and shared state
   - Document current API contract (input/output shapes)
   - Output: audit report + migration plan

2. FOUNDATION
   - Set up module folder structure
   - Introduce dependency injection container
   - Configure Prisma alongside existing pg (parallel, not replace)
   - Set up Jest + supertest baseline

3. DOMAIN EXTRACTION (per domain, sequential)
   - Extract auth module: routes → controller → service → repository
   - Migrate auth DB calls to Prisma
   - Extract users module (same pattern)
   - Extract billing module
   - Extract notifications module

4. INTEGRATION
   - Remove legacy pg dependency
   - Wire all modules through DI container
   - Verify API contract unchanged (contract tests)

5. CLEANUP
   - Remove dead code
   - Standardize error handling across all modules
   - Finalize .env.example
   - Update CI pipeline

6. VALIDATION
   - Full integration test suite passes
   - Load test baseline (k6 or autocannon): no regression
   - Docker Compose build + up produces working stack

Deliverables:
- Fully modular codebase, one folder per domain
- Prisma replacing all raw pg usage
- Test suite with >60% coverage
- CI pipeline green
- Migration runbook for production deployment

Validation:
- All original API endpoints return identical responses
- Auth flow works end-to-end
- No hardcoded values remain (grep audit)
- Docker Compose up from clean state works

Special Rules:
- Never break the running app between phases
- Document every non-obvious architectural decision
- If a phase reveals a blocker, surface it immediately with options — do not silently work around it
- Prefer explicit over clever
```

---

## Non-Technical Prompt (no ClaudeKit/Context7 injection)

### Example: Write a product announcement email

```
Goal: Write a short product announcement email for the launch of [Product Name].

Audience: Existing customers, technical background
Tone: Professional but approachable
Length: 150-200 words

Must include:
- What's new (1-2 sentences)
- Why it matters to them
- Clear CTA (link to docs or changelog)

Avoid: Marketing fluff, vague superlatives, passive voice
```
