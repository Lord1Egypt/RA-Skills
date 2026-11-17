# Integration Test Execution

## Prerequisites
- Confirm test environment is ready (Docker/Testcontainers from Step 5 environment setup)
- If not ready, STOP and run environment setup first
- Verify external dependencies are accessible (DB, Redis, message queue, external APIs)

## Test Organization
- File structure: `tests/integration/test_{module_name}.{ext}`
- One test file per service/module boundary
- Separate from unit tests (different directory or build tag)
- Each test file documents which external dependencies it needs

## Test Writing Rules
1. Use REAL external services (via Testcontainers or Docker Compose), NOT mocks
   - Mocks hide real integration bugs (SQL syntax errors, connection handling, serialization)
   - Exception: external third-party APIs that cost money or are rate-limited → use MSW/WireMock
2. Each external dependency gets at minimum:
   - 1 happy path test (correct data flow end-to-end)
   - 1 failure path test (dependency down, timeout, invalid response)
   - 1 data integrity test (transaction rollback, concurrent writes if applicable)
3. Every test MUST be independent — setup its own data, clean up after itself
   - Preferred: transaction rollback pattern
   - Alternative: truncate tables in teardown
4. Test data uses Factory pattern (see references/test-data.md)
5. Environment variables via `.env.test` — NEVER hardcode connection strings

## Execution Loop
1. Read the module under test — understand its external dependencies and data flow
2. Write test file with setup (Testcontainers/fixtures) and teardown
3. Write test cases following the rules above
4. Run tests: provide the exact command for the project's language
5. If tests fail:
   - Read the failure output carefully
   - Determine: is it a test bug or a production code bug?
   - If test bug → fix the test
   - If production code bug → report it (do NOT silently fix production code)
6. All tests pass → report results

## Language-Specific Templates

### Python (pytest + testcontainers)
```python
import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from myapp.models import Base
from myapp.services import UserService

@pytest.fixture(scope="module")
def postgres_container():
    with PostgresContainer("postgres:15-alpine") as postgres:
        yield postgres

@pytest.fixture(scope="module")
def engine(postgres_container):
    engine = create_engine(postgres_container.get_connection_url())
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

def test_create_user_success(db_session):
    service = UserService(db_session)
    user = service.create_user("test@example.com", "password123")
    assert user.id is not None
    assert user.email == "test@example.com"

def test_create_user_duplicate_email_fails(db_session):
    service = UserService(db_session)
    service.create_user("test@example.com", "password123")
    with pytest.raises(Exception, match="duplicate key value"):
        service.create_user("test@example.com", "password456")

def test_get_user_db_connection_lost(postgres_container, engine):
    # Simulate DB failure
    postgres_container.stop()
    Session = sessionmaker(bind=engine)
    session = Session()
    service = UserService(session)
    
    with pytest.raises(Exception):
        service.get_user(1)
```

### Go (testcontainers-go)
```go
//go:build integration
package integration

import (
	"context"
	"testing"
	"github.com/testcontainers/testcontainers-go"
	"github.com/testcontainers/testcontainers-go/wait"
)

var dbURL string

func TestMain(m *testing.M) {
	ctx := context.Background()
	req := testcontainers.ContainerRequest{
		Image:        "postgres:15-alpine",
		ExposedPorts: []string{"5432/tcp"},
		Env:          map[string]string{"POSTGRES_PASSWORD": "password"},
		WaitingFor:   wait.ForListeningPort("5432/tcp"),
	}
	
	postgresC, err := testcontainers.GenericContainer(ctx, testcontainers.GenericContainerRequest{
		ContainerRequest: req,
		Started:          true,
	})
	if err != nil {
		panic(err)
	}
	defer postgresC.Terminate(ctx)
	
	// Setup DB connection and run tests
	m.Run()
}

func TestUserService(t *testing.T) {
	tests := []struct{
		name    string
		email   string
		wantErr bool
	}{
		{"happy path", "test@example.com", false},
		{"duplicate email", "test@example.com", true},
	}
	
	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			// Execute test cases here with fresh transactions
		})
	}
}
```

### Node.js (vitest + testcontainers)
```typescript
import { beforeAll, afterAll, beforeEach, describe, it, expect } from 'vitest';
import { PostgreSqlContainer, StartedPostgreSqlContainer } from '@testcontainers/postgresql';
import { Client } from 'pg';
import { UserRepository } from '../src/UserRepository';

describe('UserRepository Integration', () => {
  let container: StartedPostgreSqlContainer;
  let client: Client;
  let repo: UserRepository;

  beforeAll(async () => {
    container = await new PostgreSqlContainer().start();
    client = new Client({ connectionString: container.getConnectionUri() });
    await client.connect();
    // Run schema migrations here
  });

  afterAll(async () => {
    await client.end();
    await container.stop();
  });

  beforeEach(async () => {
    await client.query('BEGIN');
    repo = new UserRepository(client);
    
    return async () => {
      await client.query('ROLLBACK');
    };
  });

  it('creates user successfully', async () => {
    const user = await repo.create('test@example.com');
    expect(user.id).toBeDefined();
  });
  
  it('fails on duplicate email', async () => {
    await repo.create('test@example.com');
    await expect(repo.create('test@example.com')).rejects.toThrow();
  });
});
```

### Rust (testcontainers-rs)
```rust
#[cfg(test)]
mod tests {
    use testcontainers::{clients, images::postgres};
    
    #[tokio::test]
    async fn test_database_interaction() {
        let docker = clients::Cli::default();
        let pg = docker.run(postgres::Postgres::default());
        let port = pg.get_host_port_ipv4(5432);
        
        let conn_string = format!("postgres://postgres:postgres@127.0.0.1:{}/postgres", port);
        // Connect to the DB using conn_string and perform integration tests
    }
}
```

## Result Report Format

After execution, output:
```
### Integration Test Results
- Test file: {path}
- Command: {run command}
- Result: {N} passed / {N} failed / {N} skipped
- External dependencies tested: {list with status}
- Failed tests: {table if any: name, error, category}
```

## Gotchas

| Mistake | Consequence | Rule |
|---------|-------------|------|
| Mocking the DB in integration tests | Defeats the purpose of integration tests, hiding real-world DB interaction bugs (e.g., SQL syntax errors) | Use REAL external services (e.g., Testcontainers). |
| Shared state between tests | Flaky tests that pass or fail unpredictably depending on execution order | Tests MUST be independent; setup data per test and clean up after. |
| Forgetting to set timezone in test DB | Timestamp mismatches and logic errors when deployed across regions | Always explicitly set timezones in DB and app configuration. |
| Not testing connection pool exhaustion | Application crashes under load in production | Include tests that simulate concurrent access or connection drops. |
| Using production data | Privacy violations, data leaks, and unpredictable test states | Use test factories or seed scripts to generate mock data. |
| Not testing migration compatibility | Deployments break because schema changes conflict with running code | Run migrations against the test database before executing tests. |
