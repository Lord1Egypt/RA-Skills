# CI Test Integration

## GitHub Actions

### Basic (Node.js)

```yaml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm test
```

### Multi-language Matrix

```yaml
jobs:
  test:
    strategy:
      matrix:
        python-version: ['3.11', '3.12', '3.13']
    steps:
      - run: pip install -r requirements-dev.txt
      - run: pytest --cov --cov-report=xml
      - uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
```

### Caching

- Node.js: `setup-node` with `cache: 'npm'`
- Python: cache `~/.cache/pip` by requirements hash
- Go: cache `~/go/pkg/mod` by go.sum hash
- Rust: cache `~/.cargo` by Cargo.lock hash

### Test Sharding (Large Suites)

```bash
# Jest/Vitest — CI auto-parallelizes
npx vitest --shard=1/3

# pytest-split
pip install pytest-split
pytest --splits 3 --group 1
```

## GitLab CI

```yaml
test:
  script:
    - pip install -r requirements-dev.txt
    - pytest --junitxml=report.xml
  artifacts:
    reports:
      junit: report.xml
```

## Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: unit-tests
        name: Run unit tests
        entry: pytest tests/unit -x --tb=short
        language: system
        pass_filenames: false
        stages: [pre-commit]
```

**Constraint**: Only fast tests in pre-commit (unit tests). Integration/E2E in CI.

## Flaky Test Handling

### Detection

A test is flaky if it passes and fails on the same code without changes. Tools: `pytest-rerunfailures`, `jest.retryTimes`.

### Handling Pipeline

1. **Quarantine**: Move flaky test to separate suite
2. **Diagnose**: Find the root cause (timing? ordering? shared state?)
3. **Fix**: Address the root cause
4. **Promote**: Return to main suite once stable
5. **Gate**: Set a flaky test cap — exceed it, block merge

### Common Causes

| Cause | Fix |
|-------|-----|
| Fixed `setTimeout` or sleep | Wait for specific condition (`waitFor`, `wait_for_selector`) |
| Shared state between tests | Independent setup and teardown per test |
| External service timing | Mock or use testcontainers |
| Test execution order dependency | Randomize order (`--shuffle`) |
| Timezone/locale differences | Fix timezone in test setup |

## Coverage

### Coverage Is a Signal, Not a KPI

Coverage shows what is NOT tested, not what IS correctly tested. 100% coverage with no assertions equals zero safety.

### Recommended Thresholds

| Layer | Threshold | Notes |
|-------|-----------|-------|
| Critical business paths | 100% | Payments, auth, data mutation |
| Core domain logic | 80%+ | Business rules |
| Utility/helper functions | 60%+ | Higher if complex logic |
| Config/glue code | 10%+ | Usually no unit test needed |
| Overall | Risk-calibrated | Don't set arbitrary numbers |

### Integration

```yaml
# Codecov
- uses: codecov/codecov-action@v4
  with:
    files: ./coverage/coverage.xml
    fail_ci_if_error: false  # Don't block CI on coverage failure
```
