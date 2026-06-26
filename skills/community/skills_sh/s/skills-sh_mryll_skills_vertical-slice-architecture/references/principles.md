# VSA Core Principles

## The Fundamental Rule

**Minimize coupling between slices. Maximize coupling within a slice.**

A "slice" is the complete vertical cut through the application for a single use case — from the entry point (HTTP handler, CLI command, event consumer) down to data access. Everything that use case needs lives together.

## What VSA Is NOT

- NOT "no architecture" — it's a different axis of organization
- NOT incompatible with DDD — domain logic can live inside slices or in shared domain objects
- NOT a rejection of all abstractions — only of premature/forced abstractions

## Key Principles

### 1. Organize by Feature, Not by Layer

```
BAD (layered):                    GOOD (sliced):
controllers/                      features/
  OrderController                   create-order/
  ProductController                   handler, request, response, validator
services/                           get-order/
  OrderService                        handler, request, response
  ProductService                    list-products/
repositories/                         handler, request, response
  OrderRepository
  ProductRepository
```

### 2. Each Slice is Autonomous

- Owns its request/response types
- Defines its own dependency interfaces
- Chooses its own data access strategy
- Can evolve independently of other slices

### 3. Single Entry Point per Feature

Every feature exposes ONE setup/registration function that:
- Receives the router/framework handle and all required dependencies (as interfaces)
- Registers its own routes/commands/event subscriptions
- Wires its internal handler to the dependencies

This is the ONLY public API of a feature. Internal types (handler struct, helpers) stay unexported/private.

### 4. Start Simple, Refactor When Needed

Begin each slice as a simple handler (Transaction Script). Only extract patterns when code smells emerge:
- Duplicate logic across 3+ slices → extract to shared helper or domain object
- Complex business rules → push into domain entities
- Cross-cutting concerns → middleware or interceptors

### 5. No Premature Abstractions

Do NOT create:
- A generic `Repository<T>` interface "just in case"
- A `BaseHandler` with shared logic for 2 handlers
- A `ServiceLayer` that just delegates to the data access

DO create shared code when:
- Genuine duplication emerges across multiple slices (the "3+ slices" heuristic is guidance, not a hard rule — use judgment)
- The shared code represents a real domain concept
- Cross-cutting concerns need consistent behavior (auth, logging, metrics)

### 6. Cross-Cutting Concerns Live in Platform/Infrastructure

Middleware, interceptors, and shared infrastructure go in a separate `platform/` or `infrastructure/` package:
- Authentication/authorization middleware
- Request logging and metrics
- Error handling and response formatting
- Database connection management
- Circuit breakers, retries
- Idempotency middleware, operation queues, event notifications (pg-notify, outbox pattern)

### 7. Dependencies Flow Inward

The composition root (main/startup) creates infrastructure and passes it DOWN to features.
Features never reach out to global state or service locators.

```
main.go / Program.cs / Application.java
  └── creates infrastructure (DB, HTTP clients, config)
       └── passes to each feature's Setup/Register function
            └── feature wires its handler internally
```

### 8. CQRS is Natural

VSA naturally separates commands (mutations) from queries (reads):
- Commands: create-order/, update-user/, delete-product/
- Queries: get-order/, list-products/, search-users/

Each can use different data access strategies (ORM for writes, raw SQL for reads).

## When to Use VSA

**Good fit:**
- Feature-rich APIs with many distinct use cases
- Teams working on separate features in parallel
- Systems where use cases vary significantly in complexity
- Microservices or modular monoliths

**Less ideal:**
- Extremely CRUD-heavy apps with uniform operations
- Very small apps with <5 features
- Teams unfamiliar with refactoring patterns

## Shared Domain Models

When multiple slices operate on the same domain entity (e.g., `Order`):
1. **Prefer slice-local definitions first** — each slice defines only the fields it needs
2. **Extract to `features/{domain}/model`** when a shared type genuinely represents a domain concept used across slices
3. **Never put domain types in `platform/`** — platform is for infrastructure, not business concepts

## Dependencies: Interfaces vs Concrete Types

- **Prefer interfaces** for external dependencies (DB, HTTP clients, message queues) to enable mock injection in tests
- **Concrete types are acceptable** when using real infrastructure in tests (e.g., testcontainers) or for simple internal helpers with no test substitution need
- This is a recommendation, not a hard rule — pragmatism over dogma

## Pragmatic Exceptions

- **Feature-local typed clients**: A feature may construct a typed client from an injected URL/config (e.g., `projects.New(projectsAdminURL)`). This is acceptable encapsulation — the config value still flows from the composition root.
- **Platform importing feature types**: Ideally platform never imports from features. When unavoidable (e.g., adapter needs response types for bulk operations), treat it as a known tradeoff and document it.

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Fix |
|---|---|---|
| God handler | Single handler grows to 500+ lines | Extract domain logic, split into sub-steps |
| Shared service layer | Defeats the purpose of slices | Let each slice own its logic |
| Cross-slice imports | Creates hidden coupling | Extract to shared domain or platform |
| Premature DRY | Abstractions before real duplication | Wait for genuine duplication to emerge |
| Feature-flag inside slice | Slices should be one use case | Create separate slices per variant |
| Platform imports features | Reverse dependency direction | Move shared types to domain or accept as documented tradeoff |
