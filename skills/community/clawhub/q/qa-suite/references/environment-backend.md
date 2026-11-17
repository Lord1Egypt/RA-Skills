# Backend Test Environment Setup

## Docker-First Environment Strategy

**Primary Recommendation**: Prioritize containerized test environments using Docker Compose or Testcontainers.

- **Isolation & Parity**: Run test databases (PostgreSQL, MySQL), caches (Redis), queues (RabbitMQ, Kafka), and mock services in Docker containers matching production versions.
- **Docker Compose**: Create a dedicated `docker-compose.test.yml` (or `docker-compose.yml` test profile) to spin up services with one command (`docker compose -f docker-compose.test.yml up -d`).
- **Programmatic Control**: Use language-native Testcontainers (`testcontainers-python`, `testcontainers-go`, `testcontainers-node`, `testcontainers-rs`) for automated lifecycle management inside unit/integration test runs.

```yaml
# Example: docker-compose.test.yml
services:
  test-db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: app_test
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_password
    ports:
      - "5433:5432"
  test-redis:
    image: redis:7-alpine
    ports:
      - "6380:6379"
```

---

## Python

```bash
# Core testing tools
pip install pytest pytest-cov pytest-mock

# Database testing (preferred: real DB via testcontainers)
pip install testcontainers

# pyproject.toml configuration
# [tool.pytest.ini_options]
# testpaths = ["tests"]
# addopts = "-v --cov=src --cov-report=term-missing"

# Run
pytest
pytest --cov=src --cov-report=html
```

**Database strategies**:
- Unit tests: SQLite in-memory (fast)
- Integration tests: testcontainers with real PostgreSQL/MySQL (accurate)
- Alternative: Docker Compose test services + transaction rollback

**Environment variables**: Create `.env.test`, load via `pytest-env` or conftest.py.

## Go

```bash
# Standard library testing + convenience
go get github.com/stretchr/testify
go get github.com/testcontainers/testcontainers-go

# Run all
go test ./...
go test -v -race ./...
go test -coverprofile=coverage.out ./...

# Coverage report
go tool cover -html=coverage.out
```

**Test organization**:
- Unit: Same package `_test.go` files
- Integration: `//go:build integration` build tag, run separately in CI
- Table-driven: Standard Go pattern for multiple inputs

**Database**: testcontainers-go with real DB; avoid mock interfaces for database layers.

## Node.js (Backend)

```bash
npm install --save-dev vitest  # Preferred: faster than Jest
npm install --save-dev supertest  # HTTP testing
npm install --save-dev testcontainers  # Database
npm install --save-dev msw  # External API mocking
```

```javascript
// vitest.config.ts
export default defineConfig({
  test: {
    environment: 'node',
    globals: true,
  },
});
```

## Rust

```bash
# Built-in: cargo test

cargo test                    # All tests
cargo test test_name          # Specific test
cargo test -- --nocapture     # Show output

# Unit tests: #[cfg(test)] mod tests {} in src/
# Integration tests: tests/ directory (separate crate)
```

**Database**: `testcontainers-rs` or `sqlx::test` fixture pattern.

## General Patterns

### Transaction Rollback (Fast DB Reset)

```python
@pytest.fixture
def db_session():
    session = create_session()
    session.begin()
    yield session
    session.rollback()  # Clean rollback after each test
```

### Test Environment Parity

- Same database version as production (or minimum supported)
- Same timezone handling
- Explicit, not implicit, environment variables
