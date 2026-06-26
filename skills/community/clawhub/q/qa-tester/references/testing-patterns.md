# Testing Patterns

## Test Selection Rules

Choose the lowest layer that can prove the behavior:

- **Unit** if logic can be verified without framework/runtime integration
- **Integration** if contracts between modules, API handlers, DB, or auth are involved
- **E2E** only if true user workflow or browser/runtime integration must be proven

If a bug can be caught by unit or integration, do not default to E2E.

## Unit Test Guidance

Use unit tests for:
- pure functions
- service business rules
- mappers and serializers
- validation helpers
- guards and permission checks

Rules:
- Prefer AAA structure
- Keep one behavior per test
- Mock only external boundaries
- Use parameterized tests for repeated cases
- Make edge cases explicit

## Integration Test Guidance

Use integration tests for:
- route/controller/service/repository flow
- request validation + response contract
- repository and DB interactions
- auth middleware and access control

Rules:
- Assert status code, response body, and side effects
- Use factories or fixtures, not random manual setup everywhere
- Keep DB state isolated and disposable
- Avoid coupling assertions to implementation internals

## Test Data Rules

Prefer:
- factories/builders
- explicit fixtures
- isolated setup per test/suite

Avoid:
- hidden shared state
- mutable global fixtures
- one giant fixture file for everything

## Quality Checklist

Every test should be:
- deterministic
- isolated
- readable
- fast enough for its layer
- focused on behavior
- useful during refactor

## Anti-Patterns

Do not:
- assert on private/internal function calls unless interaction is the behavior
- over-mock internal code
- duplicate the same arrange block across many tests without helper extraction
- chase 100% coverage blindly
- keep flaky tests in CI without fixing root cause
