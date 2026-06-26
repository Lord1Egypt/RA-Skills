---
name: test-design
description: >
  Test design and strategy skill for comprehensive testing.
  Use when: designing test cases, planning testing strategy, writing unit/integration/e2e tests,
  or improving test coverage.
  Triggers: test design, test strategy, unit test, integration test, e2e test, TDD,
  test coverage, test plan, test case design.
  Provides: testing pyramid guidance, test case templates, test categorization,
  mocking strategies, and test execution frameworks.
---

# Test Design Skill

A structured approach to designing tests that give confidence without excessive maintenance burden.

## Core Philosophy

**Test behavior, not implementation.** Tests that couple to internal implementation details become fragile and refactor-resistant. Aim to test what the code does, not how it does it.

**The best test is the one that fails when something breaks, and passes when everything works.** Perfect coverage means nothing if tests don't catch real bugs.

## Testing Pyramid

```
        ┌─────────┐
        │   E2E   │  ← Few, slow, high confidence
       ┌┴─────────┴┐
       │ Integration│ ← Some, medium speed
      ┌┴───────────┴┐
      │    Unit     │ ← Many, fast, granular
      └─────────────┘
```

**Unit tests** form the base — fast, isolated, cover individual functions.
**Integration tests** verify components work together.
**E2E tests** validate complete user journeys.

## Test Case Design

### Arrange-Act-Assert (AAA) Pattern

```python
def test_withdraw_amount_exceeds_balance():
    # Arrange
    account = Account(balance=Decimal("100.00"))
    
    # Act
    result = account.withdraw(Decimal("150.00"))
    
    # Assert
    assert result.is_failed()
    assert account.balance == Decimal("100.00")  # unchanged
```

### Given-When-Then (GWT) Pattern

```gherkin
Feature: Account Withdrawal

  Scenario: Withdrawal amount exceeds balance
    Given an account with balance $100
    When I withdraw $150
    Then the withdrawal is rejected
    And the balance remains $100
```

## Test Categories

### 🔴 Happy Path Tests
- Verify the main success scenario works
- At least one per feature/function

### 🟡 Edge Case Tests
- Boundary values (0, -1, max integer)
- Empty/null inputs
- Rare but possible conditions

### 🟡 Error Case Tests
- Invalid inputs
- Missing dependencies
- Permission denied scenarios

### 🟢 Edge/Extreme Cases
- Very large inputs
- Very small inputs
- Unicode/special characters
- Concurrent access

## Test Doubles (Mocks/Stubs/Fakes)

| Type | Purpose | Use When |
|------|---------|----------|
| **Dummy** | Fill parameter lists | Never actually used |
| **Stub** | Provide predetermined responses | Test requires specific data |
| **Spy** | Record how something was called | Verify interactions |
| **Mock** | Pre-programmed expectations | Verify behavior + interactions |
| **Fake** | Working implementation (simplified) | Real impl too slow/complex |

**Rule:** Prefer real objects over mocks when practical. Mocks hide integration problems.

## Test Naming Convention

```
test_<unit>_<scenario>_<expected_result>
```

Examples:
- `test_user_create_with_valid_input_succeeds`
- `test_user_create_with_duplicate_email_fails`
- `test_order_cancel_after_shipment_refunds_full_amount`

## Coverage Targets

| Layer | Target | Purpose |
|-------|--------|---------|
| Unit | 70-80% | Core business logic |
| Integration | 40-60% | Key flows work together |
| E2E | Critical paths only | User journeys |

**Note:** Coverage is a guide, not a goal. 100% coverage with shallow tests is worse than 70% with meaningful assertions.

## Test Execution

### Unit Tests
Run frequently during development (every save).
```bash
# Go
go test ./...

# Python
pytest tests/unit/ -v

# TypeScript
npm test -- --coverage
```

### Integration Tests
Run before PR, after unit tests pass.
```bash
# Start dependencies
docker-compose up -d

# Run integration suite
pytest tests/integration/ -v
```

### E2E Tests
Run on CI against deployed environment.
```bash
# CI/CD pipeline
npm run test:e2e -- --specs=critical-paths
```

## Test Data Management

### Strategies
1. **Factories/Fixtures** — Create test data on demand
2. **Seeded Data** — Deterministic test datasets
3. **Randomized Data** — Fuzz testing with random inputs
4. **Snapshot Testing** — Verify serializable outputs

### Best Practices
- Tests should be independent (no shared state)
- Each test should clean up after itself
- Use meaningful data, not magic values
- Avoid test interdependencies

## File Structure

```
test-design/
├── SKILL.md
└── references/
    ├── test-case-templates.md
    ├── testing-pyramid.md
    ├── mocking-strategies.md
    ├── test-naming-conventions.md
    └── per-type/
        ├── unit-test-guide.md
        ├── integration-test-guide.md
        └── e2e-test-guide.md
```
