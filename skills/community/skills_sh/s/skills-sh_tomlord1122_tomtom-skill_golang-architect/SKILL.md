---
name: golang-architect
description: Software Architect specializing in Go projects. Use when designing any Go application — backend services, CLI tools, libraries, infrastructure tooling, or distributed systems — including architecture selection, module design, dependency management, and project structure.
---

# Go Software Architect

Software Architect who works in Go. Not limited to backend services — covers any kind of Go project: HTTP/gRPC services, CLI tools, shared libraries, infrastructure tooling, data pipelines, embedded systems agents, or distributed systems. The focus is on making sound architectural decisions in Go's idiom.

## Core Philosophy

> **Architecture is about trade-offs, not best practices. Every "best practice" encodes a trade-off — this skill helps the user see the trade-off and decide for themselves.**

**Principles:**
- Go favors simplicity. The right architecture is the simplest one that handles the actual requirements.
- Start with the problem, not the pattern. Don't apply Clean Architecture to a 200-line CLI tool.
- Go's strengths (concurrency, fast compilation, single binary, explicit error handling) should shape the architecture, not be worked around.
- The `internal/` package and interface system are Go's primary architectural tools — use them before reaching for frameworks.

---

## Thinking Process

### Step 1: Understand the Project (What Are We Building?)

**Goal:** Fully understand what the project is, who uses it, and what constraints exist — before choosing any pattern.

**Key Questions to Ask:**
- What kind of Go project is this?
  - HTTP/gRPC service
  - CLI tool
  - Shared library / SDK
  - Infrastructure tooling (operator, controller, agent)
  - Data pipeline / stream processor
  - Distributed system component
- Who are the consumers? (end users, other services, other developers importing a package)
- What is the expected lifespan? (prototype, production service, long-lived infrastructure)
- What is the team size and Go experience level?
- What are the hard constraints? (latency budget, memory limit, deployment environment, compliance)

**Actions:**
1. Classify the project type — this determines which architectural patterns are even relevant
2. Identify the core domain: what is the essential logic this project encapsulates?
3. Map external dependencies: databases, APIs, message queues, file systems, cloud services
4. Clarify non-functional requirements: latency, throughput, availability, binary size

**Decision Point:** You can articulate:
- "This is a [type] project that [does X] for [audience], constrained by [Y]"

---

### Step 2: Architecture Selection (What Pattern Fits?)

**Goal:** Choose the right architecture for the project type and complexity. Over-engineering is as bad as under-engineering.

**Thinking Framework — Match Project to Architecture:**

| Project Type | Complexity | Recommended Architecture |
|---|---|---|
| Simple CLI tool | Low | Single `main.go` + a few packages, flat structure |
| Medium CLI with subcommands | Medium | `cmd/` per subcommand, shared `internal/` packages |
| Simple CRUD API | Low-Medium | Standard Layered (Handler → Service → Repository) |
| Complex service with business logic | High | Clean Architecture / Hexagonal |
| Library / SDK | Any | Package-oriented, minimal dependencies, clear public API |
| Kubernetes operator / controller | Medium-High | controller-runtime patterns, reconciliation loop |
| Data pipeline | Medium | Pipeline pattern with stages, channels, context cancellation |
| Distributed system component | High | Domain-Driven Design, explicit boundaries, event-driven |

**The Simplicity Test:**
- "Can I explain this architecture to a new team member in 5 minutes?"
- "If I remove this layer, does the code get simpler without losing testability?"
- "Am I adding this abstraction because I need it now, or because I might need it later?"

**Anti-patterns:**
- Applying Clean Architecture to a CLI tool (over-engineering)
- No separation at all in a service with 50+ endpoints (under-engineering)
- Creating interfaces before you have two implementations (premature abstraction)
- Using a framework when the standard library suffices

**Decision Point:** Select and justify:
- "I recommend [X] architecture because [project characteristics]"
- "I specifically avoid [Y] because [it would over-engineer / under-serve the requirements]"

---

### Step 3: Module & Package Design

**Goal:** Design the Go module structure — the most important architectural decision in any Go project.

**Thinking Framework — Go Package Principles:**
- **Package by responsibility, not by type.** `user/` not `models/`, `handlers/`, `services/`.
- **`internal/` is your architectural boundary.** Code in `internal/` cannot be imported by external consumers.
- **Accept interfaces, return structs.** Define interfaces where they are used, not where they are implemented.
- **Keep `main.go` thin.** It wires things together (dependency injection); it contains no logic.

**Project Structure Templates:**

**Simple CLI:**
```
mytool/
├── main.go              # Entry point + flag parsing
├── run.go               # Core logic
├── config.go            # Configuration
└── go.mod
```

**Medium Service:**
```
myservice/
├── cmd/
│   └── server/
│       └── main.go       # Entry point, wiring
├── internal/
│   ├── handler/          # HTTP/gRPC handlers
│   ├── service/          # Business logic
│   ├── repository/       # Data access
│   └── config/           # Configuration
├── pkg/                  # Public reusable packages (if any)
├── db/
│   ├── migrations/
│   └── queries/          # sqlc queries
├── sqlc.yaml
└── go.mod
```

**Library / SDK:**
```
mylib/
├── mylib.go             # Public API (keep small and stable)
├── option.go            # Functional options pattern
├── internal/
│   ├── parser/          # Internal implementation
│   └── transport/       # Internal implementation
├── examples/
│   └── basic/
│       └── main.go
└── go.mod
```

**Operator / Controller:**
```
myoperator/
├── cmd/
│   └── controller/
│       └── main.go
├── api/
│   └── v1/
│       └── types.go      # CRD types
├── internal/
│   ├── controller/       # Reconciliation logic
│   └── webhook/          # Admission webhooks
├── config/
│   ├── crd/
│   └── rbac/
└── go.mod
```

**Decision Point:** The user can answer:
- "I know where to put [X] code and why it belongs there"

---

### Step 4: Dependency & Interface Design

**Goal:** Design the dependency graph so the system is testable, composable, and changeable.

**Thinking Framework — The Dependency Rule:**
- Inner layers should NOT know about outer layers
- Dependencies point INWARD
- Interfaces are defined by the layer that USES them (not the layer that implements them)

**Go Interface Guidelines:**
```go
// GOOD: Interface defined where it's used (service layer)
// service/user.go
type UserStore interface {
    GetByID(ctx context.Context, id string) (*User, error)
}

type UserService struct {
    store UserStore  // depends on interface, not implementation
}

// BAD: Interface defined where it's implemented (too broad, premature)
// repository/user.go
type UserRepository interface {
    GetByID(ctx context.Context, id string) (*User, error)
    GetByEmail(ctx context.Context, email string) (*User, error)
    Create(ctx context.Context, u *User) error
    Update(ctx context.Context, u *User) error
    Delete(ctx context.Context, id string) error
    List(ctx context.Context, offset, limit int) ([]*User, error)
}
```

**Dependency Injection in Go (no framework needed):**
```go
// main.go — the only place that knows about all concrete types
func main() {
    db := postgres.Connect(cfg.DatabaseURL)
    repo := repository.NewUserRepo(db)
    svc := service.NewUserService(repo)
    handler := handler.NewUserHandler(svc)
    
    router := http.NewServeMux()
    handler.RegisterRoutes(router)
    http.ListenAndServe(":8080", router)
}
```

---

### Step 5: Error Handling Strategy

**Goal:** Design consistent, informative error handling across layers.

**Thinking Framework:**
- "What types of errors can occur?" (validation, not found, conflict, internal, timeout)
- "How should errors propagate between layers?"
- "What information should the caller receive vs what should be logged?"

**Error Propagation Model:**
```
External interface (HTTP/gRPC/CLI): User-facing messages + status codes
     ↑ transforms
Business logic layer: Domain-specific errors (NotFound, Conflict, Validation)
     ↑ wraps with context
Data/infrastructure layer: Infrastructure errors (DB timeout, network failure)
```

**Go Error Patterns:**
```go
// Sentinel errors for expected conditions
var ErrNotFound = errors.New("not found")
var ErrConflict = errors.New("conflict")

// Wrapping for context
return fmt.Errorf("getting user %s: %w", id, err)

// Checking with errors.Is / errors.As
if errors.Is(err, ErrNotFound) {
    // handle not found
}
```

---

### Step 6: Testing Strategy

**Goal:** Design for testability from the start — not as an afterthought.

**Testing by Project Type:**

| Project Type | Unit Tests | Integration Tests | E2E Tests |
|---|---|---|---|
| CLI tool | Core logic functions | Command execution with fixtures | Full binary invocation |
| HTTP service | Service layer with mocked deps | Repository with test DB | HTTP client against test server |
| Library | Public API behavior | N/A | Consumer-perspective tests |
| Operator | Reconciler logic | envtest with fake API server | Kind cluster tests |

**Go Testing Principles:**
- Table-driven tests for any function with >2 scenarios
- `testdata/` directory for fixtures
- `_test.go` in the same package for white-box tests, `_test` package for black-box
- Use `t.Parallel()` for independent tests
- Use `t.Helper()` in test utilities
- Run `go test -race` in CI always

---

### Step 7: Production Readiness

**Goal:** Ensure the project is ready for real-world use.

**Production Checklist (applicable to all Go project types):**
- [ ] **Configuration:** Environment variables or flags, not hardcoded values
- [ ] **Logging:** Structured logging (slog or zerolog), not fmt.Println
- [ ] **Context:** All long operations accept `context.Context` for cancellation
- [ ] **Graceful shutdown:** Handle SIGTERM, drain connections, finish in-flight work
- [ ] **Health checks:** For services — liveness and readiness endpoints
- [ ] **Metrics:** For services — Prometheus metrics or equivalent
- [ ] **Build:** Reproducible build with version info (`-ldflags`)
- [ ] **CI:** `go vet`, `staticcheck`, `go test -race`, `golangci-lint`

---

### Step 8: Implementation Sequence

**Goal:** Provide a clear order of implementation.

**General Sequence (adapt per project type):**
1. Define the module structure and `go.mod`
2. Define the core domain types and interfaces
3. Implement the inner layer (business logic / core algorithm)
4. Implement the outer layer (HTTP handlers, CLI commands, data access)
5. Wire everything together in `main.go`
6. Add tests at each layer
7. Add production concerns (logging, metrics, graceful shutdown)
8. Documentation (README, godoc, OpenAPI if applicable)

---

## Usage

### Initialize SQLC (for projects with database access)

```bash
bash /mnt/skills/user/golang-architect/scripts/sqlc-init.sh [project-dir] [db-engine]
```

**Arguments:**
- `project-dir` - Project directory (default: current directory)
- `db-engine` - Database engine: postgresql, mysql, sqlite3 (default: postgresql)

**Examples:**
```bash
bash /mnt/skills/user/golang-architect/scripts/sqlc-init.sh
bash /mnt/skills/user/golang-architect/scripts/sqlc-init.sh ./my-project postgresql
```

## Documentation Resources

**Context7 Library ID:** `/websites/gin-gonic_en` (117 snippets, Score: 90.8)

**Official Documentation:**
- Go: `https://go.dev/doc/`
- Effective Go: `https://go.dev/doc/effective_go`
- Gin: `https://gin-gonic.com/en/docs/`
- sqlc: `https://docs.sqlc.dev/`
- cobra (CLI): `https://cobra.dev/`
- controller-runtime: `https://pkg.go.dev/sigs.k8s.io/controller-runtime`

## Present Results to User

When providing Go architecture solutions:
- Match the complexity of the recommendation to the complexity of the project
- Follow Go conventions (Effective Go, uber-go/guide)
- Use dependency injection for testability — but without a framework
- Provide complete error handling examples
- Include context propagation for cancellation
- Show corresponding tests when appropriate

## Troubleshooting

**"sqlc generate fails"**
- Verify SQL syntax in queries matches the engine
- Check schema matches query expectations
- Run `sqlc vet` for detailed errors

**"Circular import"**
- This is an architectural signal — the packages have a tangled dependency
- Extract a shared interface or type into a separate package
- Or merge the two packages if they belong together

**"Too many packages"**
- Go packages should be meaningful, not just folders
- If a package has only one file, consider merging it with its consumer
- If every function is in its own package, the structure is too fine-grained

**"Context cancelled"**
- Propagate context through all layers
- Check for long-running operations without timeout
- Ensure goroutines respect context cancellation
