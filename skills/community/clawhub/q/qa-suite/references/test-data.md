# Test Data Management

## Factory Pattern

Generate test objects with sensible defaults. Override only the fields under test.

**Python (factory_boy)**:
```python
import factory

class UserFactory(factory.Factory):
    class Meta:
        model = User
    name = factory.Faker("name")
    email = factory.Faker("email")
    is_active = True

user = UserFactory(name="Alice")
inactive = UserFactory(is_active=False)
```

**JavaScript/TypeScript**:
```typescript
function createUser(overrides: Partial<User> = {}): User {
  return {
    id: crypto.randomUUID(),
    name: 'Test User',
    email: 'test@example.com',
    isActive: true,
    ...overrides,
  };
}
```

## Fixture Strategies

### Inline — Simplest

```python
def test_create_user():
    user = User(name="Alice", email="alice@example.com")
    result = save(user)
    assert result.id is not None
```

Good for: Simple tests, few tests sharing data.

### Shared — Multiple test reuse

```python
@pytest.fixture
def active_user():
    return UserFactory(is_active=True)

def test_can_login(active_user):
    assert can_login(active_user) is True
```

Good for: Multiple tests needing the same baseline data.

### Transactional — Database tests

```python
@pytest.fixture
def db_session():
    session = create_session()
    session.begin()
    yield session
    session.rollback()  # Auto-cleanup
```

## Seed Data

For integration and E2E tests:

```
tests/
├── fixtures/
│   ├── users.json
│   ├── products.yaml
│   └── seed.sql
```

**Principles**:
- Minimal set (not 10,000 rows pre-seeded)
- Each test file manages its own seed
- Never use production data

## Testcontainers (Recommended)

Real, ephemeral databases for integration tests:

```python
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="module")
def postgres():
    with PostgresContainer("postgres:16") as pg:
        yield pg.get_connection_url()
```

Supports: PostgreSQL, MySQL, MongoDB, Redis, Kafka, Elasticsearch.

## Deterministic Data

Sources of non-determinism to control:
- `datetime.now()` → freeze with `freezegun` (Python), `jest.useFakeTimers()` (JS)
- `random()` → set seed or inject mock
- External APIs → MSW interception or pact contract tests
- File system ordering → explicit sort

## Property-Based Testing

Describe input properties; framework generates test cases:

**Python (hypothesis)**:
```python
from hypothesis import given, strategies as st

@given(st.integers(), st.integers())
def test_add_commutative(a, b):
    assert a + b == b + a
```

**JavaScript (fast-check)**:
```typescript
import fc from 'fast-check';

test('add is commutative', () => {
  fc.assert(fc.property(fc.integer(), fc.integer(), (a, b) => {
    expect(a + b).toBe(b + a);
  }));
});
```

Good for: Math operations, serialization/deserialization, encoding/decoding, sort algorithms.
