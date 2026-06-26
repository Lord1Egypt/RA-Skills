# Testing Pyramid

## Concept

The testing pyramid suggests having many fast, focused unit tests at the base, fewer integration tests in the middle, and even fewer slow, end-to-end tests at the top.

```
        /\
       /  \
      / E2E\         Slow, Expensive, High Confidence
     /______\
    /        \
   /Integration\    Medium Speed, Medium Cost
  /____________\
 /              \
/    Unit        \   Fast, Cheap, Granular
/________________\

Many        Few
```

## Layer Definitions

### Unit Tests

**Speed:** Milliseconds
**Cost:** Very low
**Scope:** Single function/class
**Dependencies:** Mocked

**When to write:**
- Core business logic
- Complex algorithms
- Edge cases
- Error handling

**When to skip:**
- Trivial getters/setters
- Generated code
- UI bindings

### Integration Tests

**Speed:** Seconds
**Cost:** Medium
**Scope:** Multiple components
**Dependencies:** Real (or close to real)

**When to write:**
- Database interactions
- API integrations
- Message queue operations
- External service calls

**When to skip:**
- Unit-tested paths
- Simple transformations
- Already covered scenarios

### E2E Tests

**Speed:** Minutes
**Cost:** High
**Scope:** Complete user journeys
**Dependencies:** Full system

**When to write:**
- Critical user flows
- Payment/checkout
- Login/authentication
- Core product features

**When to skip:**
- Rare edge cases
- Internal workflows
- Developer tooling

## Practical Adaptation

Not every team should follow the pyramid strictly. Consider:

| Context | Pyramid Emphasis |
|---------|------------------|
| New project | Start with unit tests |
| Legacy code | Add integration tests first |
| High-risk domain (finance) | More E2E |
| Microservices | Contract tests + E2E |
| Data pipelines | Integration + validation |

## Anti-Patterns

### Inverted Pyramid
```
   Many E2E
   Few Unit
```
Problem: Slow, brittle, expensive to maintain

### Ice Cream Cone
```
   Many E2E
   Many Integration  
   Few Unit
```
Problem: Over-reliance on slow tests

### Single Layer
```
   Only Unit
```
Problem: Doesn't catch integration issues

## Test Execution Strategy

### On Every Commit (CI)
- Unit tests only
- Must complete in < 5 minutes

### On Every PR
- Unit tests
- Integration tests
- Lint + type check

### Nightly/Weekly
- Full E2E suite
- Performance tests
- Security scans

## Coverage Guidelines

| Layer | Target | Minimum |
|-------|--------|---------|
| Unit | 70-80% | 50% |
| Integration | 40-60% | 30% |
| E2E | Critical paths | - |
