# Backend Testing

Testing strategies, frameworks, tools, and CI/CD testing.

## Testing Pyramid

### 70-20-10 Rule
- **70% Unit Tests** - Fast, isolated, test individual functions
- **20% Integration Tests** - Test component interactions
- **10% E2E Tests** - Test full user flows

### Unit Tests
- Test individual functions/methods
- Mock external dependencies
- Fast execution (<1ms per test)
- High coverage target (80%+)

### Integration Tests
- Test database interactions
- Test API endpoints
- Test service integrations
- Use test databases

### E2E Tests
- Test complete workflows
- Use staging environment
- Slower execution
- Lower coverage (critical paths)

## Testing Frameworks

### Node.js/TypeScript
- **Vitest** - Fast, Vite-based, 50% faster than Jest
- **Jest** - Popular, feature-rich
- **Mocha** - Flexible, minimal

### Python
- **pytest** - Popular, fixtures, plugins
- **unittest** - Standard library
- **Hypothesis** - Property-based testing

### Go
- **testing** - Standard library
- **testify** - Assertions and mocks

## Test Structure

### AAA Pattern
- **Arrange** - Set up test data
- **Act** - Execute code under test
- **Assert** - Verify results

### Example
```python
def test_user_creation():
    # Arrange
    user_data = {"name": "Test User", "email": "test@example.com"}
    
    # Act
    user = create_user(user_data)
    
    # Assert
    assert user.id is not None
    assert user.name == "Test User"
```

## Database Testing

### Strategies
- Use test database (separate from production)
- Transactions that rollback
- Fixtures for test data
- Migrations for schema setup

### Best Practices
- Clean up after tests
- Use factories for test data
- Test migrations separately
- Verify data constraints

## API Testing

### Tools
- **Postman** - Manual testing
- **REST Client** - HTTP requests
- **Supertest** (Node.js) - API testing
- **httpx** (Python) - HTTP client for testing

### Test Cases
- Status codes
- Response structure
- Error handling
- Authentication/authorization
- Rate limiting

## Contract Testing

### Purpose
- Verify API contracts between services
- Prevent breaking changes
- Consumer-driven contracts

### Tools
- **Pact** - Consumer-driven contracts
- **Spring Cloud Contract** - Contract testing
- **OpenAPI** - Schema validation

## CI/CD Testing

### Pipeline Stages
1. Lint and format checks
2. Unit tests
3. Integration tests
4. Build artifacts
5. E2E tests (staging)
6. Deploy to production

### Best Practices
- Run fast tests first
- Parallel test execution
- Cache dependencies
- Fail fast on errors
- Test migrations before deployment

## Performance Testing

### Types
- **Load Testing** - Normal expected load
- **Stress Testing** - Beyond normal capacity
- **Spike Testing** - Sudden load increases
- **Endurance Testing** - Sustained load

### Tools
- **k6** - Load testing
- **Artillery** - Performance testing
- **Apache JMeter** - Load testing

## Test Coverage

### Metrics
- Line coverage
- Branch coverage
- Function coverage
- Statement coverage

### Targets
- 80%+ for unit tests
- 60%+ for integration tests
- Critical paths for E2E tests
