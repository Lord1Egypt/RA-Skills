# VSA Testing Strategy

## Core Testing Principle

The primary test for each feature exercises it **end-to-end through its single entry point**:
1. Calls the feature's Setup/Register/Map function with real or test infrastructure
2. Sends an HTTP request (or invokes the handler directly)
3. Verifies **outcomes**: database state, API calls made, responses returned

This is a **feature integration test** that exercises the full slice. Unit tests for complex domain logic and platform/adapter contract tests are also encouraged where they add value.

> **Note**: All code snippets below are illustrative — adapt them to your project's conventions and framework versions.

## Table of Contents

- [Go](#go)
- [.NET / C#](#net--c)
- [Java / Kotlin](#java--kotlin-spring-boot)
- [TypeScript / Node.js](#typescript--nodejs)
- [Python](#python-fastapi)
- [Universal Patterns](#universal-patterns)
- [Platform / Adapter Tests](#platform--adapter-tests)

---

## Go

### Libraries
- **testcontainers-go**: Real database/service containers for integration tests
- **testify**: Assertions (`assert`, `require`) and mock verification (`mock.Mock`)
- **net/http/httptest**: HTTP test server from stdlib

### Pattern: Integration Test with Testcontainers

```go
// create/handler_test.go
package create_test

import (
    "context"
    "net/http"
    "net/http/httptest"
    "testing"

    "github.com/gin-gonic/gin"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
    "github.com/testcontainers/testcontainers-go/modules/postgres"
)

func TestCreateItem(t *testing.T) {
    // 1. Start real infrastructure
    ctx := context.Background()
    pgContainer, err := postgres.Run(ctx, "postgres:16-alpine",
        postgres.WithDatabase("testdb"),
    )
    require.NoError(t, err)
    t.Cleanup(func() { pgContainer.Terminate(ctx) })

    db := connectToDB(t, pgContainer)

    // 2. Setup feature via its single entry point
    engine := gin.New()
    create.Setup(engine.Group("/api/v1"), db)

    // 3. Send request
    w := httptest.NewRecorder()
    req := httptest.NewRequest("POST", "/api/v1/items", toJSON(CreateRequest{Name: "test"}))
    engine.ServeHTTP(w, req)

    // 4. Verify outcomes
    assert.Equal(t, http.StatusCreated, w.Code)

    // Verify DB state
    var count int
    err = db.QueryRow(ctx, "SELECT count(*) FROM items WHERE name = $1", "test").Scan(&count)
    require.NoError(t, err)
    assert.Equal(t, 1, count)
}
```

### Pattern: Mock Verification for External Dependencies

```go
func TestCreateOrder_CallsPaymentAPI(t *testing.T) {
    // Mock external dependency
    paymentMock := new(MockPaymentClient)
    paymentMock.On("Charge", mock.Anything, mock.MatchedBy(func(amt int) bool {
        return amt == 1000
    })).Return(nil)

    engine := gin.New()
    createorder.Setup(engine.Group("/api/v1"), db, paymentMock)

    w := httptest.NewRecorder()
    req := httptest.NewRequest("POST", "/api/v1/orders", toJSON(orderReq))
    engine.ServeHTTP(w, req)

    assert.Equal(t, http.StatusCreated, w.Code)

    // Verify the external API was called correctly
    paymentMock.AssertCalled(t, "Charge", mock.Anything, 1000)
    paymentMock.AssertNumberOfCalls(t, "Charge", 1)
}
```

### Key Go Testing Idioms
- Test file lives next to handler: `handler.go` + `handler_test.go`
- Package: `_test` suffix for black-box testing (`create_test`, not `create`)
- Use `t.Cleanup()` for testcontainer teardown
- Use `require` for fatal checks, `assert` for non-fatal
- Mock interfaces defined in the slice, not in a shared mock package

---

## .NET / C#

### Libraries
- **Testcontainers.NET**: Real database containers
- **WebApplicationFactory**: In-memory test server (Microsoft.AspNetCore.Mvc.Testing)
- **NSubstitute** or **Moq**: Mock verification
- **FluentAssertions**: Expressive assertions
- **Respawn**: Database cleanup between tests

### Pattern: Integration Test with WebApplicationFactory

```csharp
public class CreateOrderTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;
    private readonly AppDbContext _db;

    public CreateOrderTests(WebApplicationFactory<Program> factory)
    {
        // Replace DB with testcontainer
        _client = factory.WithWebHostBuilder(builder =>
        {
            builder.ConfigureServices(services =>
            {
                services.RemoveAll<DbContextOptions<AppDbContext>>();
                services.AddDbContext<AppDbContext>(opts =>
                    opts.UseNpgsql(TestContainerConnectionString));
            });
        }).CreateClient();

        _db = GetDbContext();
    }

    [Fact]
    public async Task CreateOrder_PersistsToDatabase()
    {
        // Send request through the full pipeline
        var response = await _client.PostAsJsonAsync("/orders",
            new { Product = "Widget", Qty = 5 });

        // Verify HTTP response
        response.StatusCode.Should().Be(HttpStatusCode.Created);

        // Verify DB state
        var order = await _db.Orders.FirstOrDefaultAsync(o => o.Product == "Widget");
        order.Should().NotBeNull();
        order!.Qty.Should().Be(5);
    }
}
```

### Pattern: Mock Verification

```csharp
[Fact]
public async Task CreateOrder_CallsPaymentService()
{
    var paymentMock = Substitute.For<IPaymentService>();

    var client = _factory.WithWebHostBuilder(builder =>
    {
        builder.ConfigureServices(services =>
        {
            services.AddSingleton(paymentMock);
        });
    }).CreateClient();

    await client.PostAsJsonAsync("/orders", new { Product = "Widget", Qty = 5 });

    // Verify external call
    await paymentMock.Received(1).ChargeAsync(Arg.Is<int>(a => a == 500));
}
```

---

## Java / Kotlin (Spring Boot)

### Libraries
- **Testcontainers**: Real database/service containers
- **Spring Boot Test**: `@SpringBootTest` + `TestRestTemplate`/`WebTestClient`
- **Mockito**: Mock verification (`verify`, `when`)
- **AssertJ**: Fluent assertions

### Pattern: Integration Test

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Testcontainers
class CreateOrderTest {

    @Container
    static PostgreSQLContainer<?> pg = new PostgreSQLContainer<>("postgres:16-alpine");

    @DynamicPropertySource
    static void dbProps(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", pg::getJdbcUrl);
        registry.add("spring.datasource.username", pg::getUsername);
        registry.add("spring.datasource.password", pg::getPassword);
    }

    @Autowired TestRestTemplate rest;
    @Autowired JdbcTemplate jdbc;

    @Test
    void createOrder_persistsToDatabase() {
        var req = new CreateOrderRequest("Widget", 5);

        var response = rest.postForEntity("/api/v1/orders", req, OrderResponse.class);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);

        var count = jdbc.queryForObject(
            "SELECT count(*) FROM orders WHERE product = ?", Integer.class, "Widget");
        assertThat(count).isEqualTo(1);
    }
}
```

### Mock Verification

```java
@SpringBootTest
class CreateOrderTest {

    @MockBean PaymentClient paymentClient;

    @Test
    void createOrder_callsPaymentAPI() {
        when(paymentClient.charge(anyInt())).thenReturn(PaymentResult.ok());

        rest.postForEntity("/api/v1/orders", req, OrderResponse.class);

        verify(paymentClient, times(1)).charge(eq(500));
    }
}
```

---

## TypeScript / Node.js

### Libraries
- **testcontainers** (npm): Real containers
- **supertest**: HTTP assertions
- **jest** or **vitest**: Test runner + mocking
- **jest.fn() / vi.fn()**: Mock verification

### Pattern: Integration Test

```typescript
import { GenericContainer, StartedTestContainer } from 'testcontainers';
import request from 'supertest';
import { createApp } from '../app';

describe('POST /api/v1/orders', () => {
  let container: StartedTestContainer;
  let app: Express;
  let db: Database;

  beforeAll(async () => {
    container = await new GenericContainer('postgres:16-alpine')
      .withExposedPorts(5432)
      .start();

    db = await connectDB(container.getConnectionUri());
    app = createApp(db);
  });

  afterAll(() => container.stop());

  it('persists order to database', async () => {
    const res = await request(app)
      .post('/api/v1/orders')
      .send({ product: 'Widget', qty: 5 });

    expect(res.status).toBe(201);

    const rows = await db.query('SELECT * FROM orders WHERE product = $1', ['Widget']);
    expect(rows).toHaveLength(1);
  });
});
```

### Mock Verification

```typescript
it('calls payment API', async () => {
  const paymentMock = { charge: vi.fn().mockResolvedValue({ ok: true }) };
  const app = createApp(db, paymentMock);

  await request(app).post('/api/v1/orders').send(orderReq);

  expect(paymentMock.charge).toHaveBeenCalledWith(500);
  expect(paymentMock.charge).toHaveBeenCalledTimes(1);
});
```

---

## Python (FastAPI)

### Libraries
- **testcontainers-python**: Real containers
- **httpx** + **pytest**: Async test client
- **unittest.mock** / **pytest-mock**: Mock verification

### Pattern: Integration Test

```python
import pytest
from testcontainers.postgres import PostgresContainer
from httpx import AsyncClient, ASGITransport
from app import create_app

@pytest.fixture(scope="module")
def pg():
    with PostgresContainer("postgres:16-alpine") as pg:
        yield pg

@pytest.fixture
def db(pg):
    return connect(pg.get_connection_url())

@pytest.fixture
def app(db):
    return create_app(db)

@pytest.mark.asyncio
async def test_create_order_persists(app, db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.post("/api/v1/orders", json={"product": "Widget", "qty": 5})

    assert res.status_code == 201

    # Verify DB
    row = db.execute("SELECT * FROM orders WHERE product = %s", ("Widget",)).fetchone()
    assert row is not None
```

---

## Universal Patterns

### What to Test Per Feature

| Aspect | How | Example |
|--------|-----|---------|
| **Happy path** | Full request → verify response + DB state | POST creates record, returns 201 |
| **Validation errors** | Invalid input → verify 400 + no side effects | Missing field returns 400, DB unchanged |
| **Not found** | Missing resource → verify 404 | GET nonexistent ID returns 404 |
| **External API calls** | Mock dependency → verify calls | Payment API called with correct amount |
| **Error handling** | Simulate failure → verify graceful degradation | DB timeout returns 503, no partial state |
| **Idempotency** | Repeat same request → verify same outcome | Duplicate POST returns same result |

### Test Naming Convention

Name tests by behavior, not implementation:
```
GOOD: TestCreateOrder_PersistsToDatabase
GOOD: TestCreateOrder_Returns400_WhenProductEmpty
GOOD: TestCreateOrder_CallsPaymentAPI_WithCorrectAmount

BAD:  TestHandler
BAD:  TestCreateOrderHandler_Handle
BAD:  TestPost
```

### Shared Test Fixtures

For infrastructure setup shared across features, create a test helper:

```
testutil/           # or testfixtures/, testinfra/
  database.go       # Start testcontainer, return connection
  httptest.go       # Create test engine with middleware
```

Keep feature-specific test setup inside the feature's test file.

---

## Platform / Adapter Tests

Beyond feature integration tests, platform components benefit from their own contract tests:

### What to Test in Platform

| Component | What to Verify | Example |
|-----------|---------------|---------|
| **Idempotency middleware** | Duplicate requests return same result, no side effects | POST same idempotency key twice → 200, single DB row |
| **Operation queue** | Jobs enqueue, execute, retry on failure | Enqueue job → verify execution, simulate failure → verify retry |
| **Circuit breaker** | Opens after N failures, half-opens after timeout | Fail N requests → verify open, wait → verify half-open |
| **Auth middleware** | Valid token passes, invalid/expired rejects | Valid JWT → 200, expired → 401, missing → 401 |
| **Error handler** | Maps domain errors to HTTP status codes | NotFound → 404, ValidationError → 400, unknown → 500 |

These tests live in `platform/{component}/{component}_test` and use the same testcontainers/test-server approach as feature tests.
