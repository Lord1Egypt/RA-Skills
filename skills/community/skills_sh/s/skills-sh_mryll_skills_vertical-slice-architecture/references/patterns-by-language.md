# VSA Patterns by Language/Framework

This reference provides concrete VSA patterns for different languages. The principles are universal; only the idioms change.

## Table of Contents

- [Go (Gin, Chi, stdlib)](#go)
- [.NET / C# (ASP.NET Core)](#net--c-aspnet-core)
- [Java / Kotlin (Spring Boot)](#java--kotlin-spring-boot)
- [TypeScript / Node.js (Express, Fastify, NestJS)](#typescript--nodejs-express-fastify-nestjs)
- [Python (FastAPI, Flask)](#python-fastapi-flask)
- [Universal Structure](#universal-structure)

---

## Go

### Directory Structure

```
internal/
  features/
    {domain}/
      {operation}/
        handler.go          # Handler struct + Setup function
        handler_test.go     # Tests co-located
        request.go          # Request type (optional, if complex)
        response.go         # Response type (optional, if complex)
        internal/           # Feature-private dependencies
          client.go         # e.g., external service client
  platform/
    httpx/                  # Shared HTTP middleware
    observability/          # Metrics, tracing
    errors/                 # Error classification
main.go                    # Composition root
```

### Single Entry Point Pattern

```go
package create

type Repository interface {
    Create(ctx context.Context, item Item) error
}

type handler struct {
    repo Repository
}

// Setup is the ONLY exported function. Receives router + dependencies.
func Setup(r gin.IRoutes, repo Repository) {
    h := handler{repo: repo}
    r.POST("/items", h.handle)
}

func (h handler) handle(c *gin.Context) {
    // validate → execute → respond
}
```

### Composition Root (main.go)

```go
func main() {
    db := postgres.NewPool(cfg.DatabaseURL)
    engine := gin.New()
    api := engine.Group("/api/v1")

    // Each feature registers itself
    create.Setup(api, db)
    list.Setup(api, db)
    getbyid.Setup(api, db)
    delete.Setup(api, db)
}
```

### Key Go Idioms
- Handler struct is **unexported** (`handler`, not `Handler`)
- Repository interface defined **inside the slice**, not in a shared package
- Entry point name varies by convention: `Setup()`, `RegisterRoute()`, etc. — the role matters, not the name
- Entry point receives an interface (`gin.IRoutes`), not a concrete type (`*gin.Engine`)
- Prefer interfaces for external deps (enables mock injection). Concrete types acceptable when testing with real infra (testcontainers)
- Feature-private code goes in `internal/` subdirectory (Go enforces visibility)
- Use `context.Context` for cancellation propagation

---

## .NET / C# (ASP.NET Core)

### Directory Structure

```
Features/
  Orders/
    CreateOrder/
      CreateOrderEndpoint.cs      # Minimal API endpoint
      CreateOrderCommand.cs       # Request + handler (MediatR)
      CreateOrderValidator.cs     # FluentValidation
      CreateOrderResponse.cs
    GetOrder/
      GetOrderEndpoint.cs
      GetOrderQuery.cs
      GetOrderResponse.cs
Infrastructure/
  Persistence/
  Middleware/
Program.cs                        # Composition root
```

### With MediatR (Command/Query pattern)

```csharp
// CreateOrderCommand.cs
public record CreateOrderCommand(string Product, int Qty) : IRequest<OrderResponse>;

public class CreateOrderHandler : IRequestHandler<CreateOrderCommand, OrderResponse>
{
    private readonly AppDbContext _db;
    public CreateOrderHandler(AppDbContext db) => _db = db;

    public async Task<OrderResponse> Handle(CreateOrderCommand cmd, CancellationToken ct)
    {
        var order = new Order(cmd.Product, cmd.Qty);
        _db.Orders.Add(order);
        await _db.SaveChangesAsync(ct);
        return new OrderResponse(order.Id);
    }
}

// CreateOrderEndpoint.cs
public static class CreateOrderEndpoint
{
    public static void Map(IEndpointRouteBuilder app) =>
        app.MapPost("/orders", async (CreateOrderCommand cmd, ISender sender) =>
            Results.Created($"/orders/{(await sender.Send(cmd)).Id}", null));
}
```

### Without MediatR (Minimal API direct)

```csharp
public static class CreateOrderEndpoint
{
    public static void Map(IEndpointRouteBuilder app) =>
        app.MapPost("/orders", Handle);

    private static async Task<IResult> Handle(
        CreateOrderRequest req, AppDbContext db, CancellationToken ct)
    {
        var order = new Order(req.Product, req.Qty);
        db.Orders.Add(order);
        await db.SaveChangesAsync(ct);
        return Results.Created($"/orders/{order.Id}", null);
    }
}
```

### Composition Root (Program.cs)

```csharp
var app = builder.Build();
CreateOrderEndpoint.Map(app);
GetOrderEndpoint.Map(app);
ListOrdersEndpoint.Map(app);
```

### Key .NET Idioms
- MediatR is popular but NOT required — Minimal APIs work fine without it
- FluentValidation for request validation inside the slice
- Each endpoint class has a static `Map()` method (single entry point)
- `IEndpointRouteBuilder` is the interface (not `WebApplication`)
- Dependencies are resolved via the DI container (not passed as `Map()` parameters) — this is the standard .NET mechanism, unlike Go/TS/Python which use explicit params

---

## Java / Kotlin (Spring Boot)

### Directory Structure

```
features/
  order/
    createorder/
      CreateOrderController.java    # REST endpoint
      CreateOrderRequest.java       # Request DTO
      CreateOrderResponse.java      # Response DTO
      CreateOrderHandler.java       # Business logic
      OrderRepository.java          # Slice-specific repository interface
    getorder/
      GetOrderController.java
      GetOrderResponse.java
platform/
  config/
  middleware/
  exceptions/
Application.java
```

### Slice Implementation

```java
// CreateOrderHandler.java
@Component
public class CreateOrderHandler {
    private final JdbcTemplate jdbc;

    public CreateOrderHandler(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    public CreateOrderResponse handle(CreateOrderRequest req) {
        // validate → persist → return response
    }
}

// CreateOrderController.java
@RestController
@RequestMapping("/api/v1/orders")
public class CreateOrderController {
    private final CreateOrderHandler handler;

    public CreateOrderController(CreateOrderHandler handler) {
        this.handler = handler;
    }

    @PostMapping
    public ResponseEntity<CreateOrderResponse> create(@Valid @RequestBody CreateOrderRequest req) {
        return ResponseEntity.status(201).body(handler.handle(req));
    }
}
```

### Key Java/Kotlin Idioms
- Spring's component scan auto-discovers controllers — this IS the entry point mechanism (no explicit `Setup()` function needed)
- The `@RestController` class itself is the entry point; its package is the slice boundary
- Each feature package is self-contained
- Handler + Controller separation within the slice (optional — can merge for simple cases)
- `@Valid` with Jakarta Bean Validation for request validation
- Dependencies injected via constructor (Spring DI), not as function parameters

---

## TypeScript / Node.js (Express, Fastify, NestJS)

### Directory Structure

```
features/
  orders/
    create-order/
      create-order.handler.ts     # Business logic
      create-order.route.ts       # Route registration
      create-order.schema.ts      # Zod/Joi validation
      create-order.types.ts       # Request/Response types
    get-order/
      get-order.handler.ts
      get-order.route.ts
platform/
  middleware/
  database/
app.ts                            # Composition root
```

### Single Entry Point (Express)

```typescript
// create-order.route.ts
import { Router } from 'express';
import { createOrderHandler } from './create-order.handler';

export function setup(router: Router, db: Database): void {
  router.post('/orders', async (req, res) => {
    const result = await createOrderHandler(db, req.body);
    res.status(201).json(result);
  });
}
```

### Composition Root

```typescript
// app.ts
import * as createOrder from './features/orders/create-order/create-order.route';
import * as getOrder from './features/orders/get-order/get-order.route';

const router = express.Router();
const db = new Database(config.dbUrl);

createOrder.setup(router, db);
getOrder.setup(router, db);
app.use('/api/v1', router);
```

---

## Python (FastAPI, Flask)

### Directory Structure

```
features/
  orders/
    create_order/
      __init__.py
      handler.py          # Business logic
      router.py           # Route setup
      schemas.py          # Pydantic models
    get_order/
      __init__.py
      handler.py
      router.py
      schemas.py
platform/
  database.py
  middleware.py
main.py
```

### Single Entry Point (FastAPI)

```python
# create_order/router.py
from fastapi import APIRouter, Depends
from .handler import create_order_handler
from .schemas import CreateOrderRequest, CreateOrderResponse

def setup(router: APIRouter, get_db=Depends()) -> None:
    @router.post("/orders", response_model=CreateOrderResponse, status_code=201)
    async def create_order(req: CreateOrderRequest, db=Depends(get_db)):
        return await create_order_handler(db, req)
```

### Alternative: Explicit Dependency Passing

```python
# Simpler approach without Depends() — db passed directly from composition root
def setup(router: APIRouter, db: Database) -> None:
    @router.post("/orders", response_model=CreateOrderResponse, status_code=201)
    async def create_order(req: CreateOrderRequest):
        return await create_order_handler(db, req)
```

### Key Python Idioms
- FastAPI's `Depends()` is the idiomatic DI mechanism — use it for DB sessions, auth, etc.
- Explicit param passing (closure pattern) also works for simpler cases
- Pydantic models for request/response validation (built into FastAPI)
- Each feature package has `__init__.py`, `handler.py`, `router.py`, `schemas.py`

---

## Universal Structure

Regardless of language, every VSA project follows this skeleton:

```
{project-root}/
  {features-dir}/           # "features/", "internal/features/", "Features/"
    {domain}/               # "orders/", "users/", "kvs/"
      {operation}/          # "create/", "list/", "delete/"
        handler             # Entry point + orchestration
        request/response    # DTOs (can be inline for simple cases)
        validator           # Input validation (optional)
        test                # Co-located tests
        internal/           # Feature-private helpers (optional)
  {platform-dir}/           # "platform/", "Infrastructure/", "platform/"
    middleware/
    database/
    observability/
  {composition-root}        # main.go, Program.cs, app.ts, main.py
```

### Beyond HTTP: Event Consumer Slices

VSA is not limited to HTTP endpoints. Event consumers (message queues, Kafka, SQS, etc.) follow the same pattern — the entry point registers a subscription instead of a route:

```go
// features/orders/process_payment/handler.go
package processpayment

func Setup(consumer messaging.Consumer, db *pgxpool.Pool, payments PaymentClient) {
    h := handler{db: db, payments: payments}
    consumer.Subscribe("orders.created", h.handle)
}
```

The same principle applies to CLI commands, cron jobs, and gRPC services — each use case is a self-contained slice with a single entry point.
