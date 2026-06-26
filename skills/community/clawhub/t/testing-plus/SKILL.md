---
name: testing-plus
description: "Enhanced testing with framework-specific templates, CI/CD integration, mutation testing, and performance testing. Covers unit, integration, E2E, and security testing."
metadata:
  author: opencode
  version: 2.0
  tags: testing, ci-cd, mutation-testing, performance, security
  compatibility: opencode
  license: MIT
---

# Testing Plus

Enhanced testing with framework templates, CI/CD integration, and advanced testing strategies.

## Features

- **Framework Templates**: Ready-to-use templates for Jest, Vitest, pytest, Go testing
- **CI/CD Integration**: GitHub Actions, GitLab CI, Jenkins pipelines
- **Mutation Testing**: Verify test quality with Stryker, mutmut
- **Performance Testing**: Load testing, stress testing, benchmarks
- **Security Testing**: OWASP, dependency scanning, SAST

## Quick Reference

| Test Type | Tool | Purpose |
|-----------|------|---------|
| Unit | Jest, Vitest, pytest | Individual functions |
| Integration | Supertest, Testcontainers | Module boundaries |
| E2E | Playwright, Cypress | Full user workflows |
| Mutation | Stryker, mutmut | Test quality verification |
| Performance | k6, Artillery | Load testing |
| Security | OWASP ZAP, Snyk | Vulnerability detection |

## Testing Pyramid

| Level | Ratio | Speed | Cost | Confidence |
|-------|-------|-------|------|------------|
| **Unit** | ~70% | ms | Low | Low |
| **Integration** | ~20% | seconds | Medium | Medium |
| **E2E** | ~10% | minutes | High | High |

## Framework Templates

### Jest (JavaScript/TypeScript)

```typescript
// jest.config.js
export default {
  preset: 'ts-jest',
  testEnvironment: 'node',
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};
```

```typescript
// src/utils.test.ts
import { calculateTotal } from './utils';

describe('calculateTotal', () => {
  it('should calculate total with tax', () => {
    const items = [{ price: 10, qty: 2 }, { price: 5, qty: 1 }];
    const taxRate = 0.08;
    expect(calculateTotal(items, taxRate)).toBe(27.0);
  });

  it('should handle empty items', () => {
    expect(calculateTotal([], 0.08)).toBe(0);
  });
});
```

### Vitest (JavaScript/TypeScript)

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
    },
  },
});
```

```typescript
// src/utils.test.ts
import { describe, it, expect } from 'vitest';
import { calculateTotal } from './utils';

describe('calculateTotal', () => {
  it('should calculate total with tax', () => {
    const items = [{ price: 10, qty: 2 }, { price: 5, qty: 1 }];
    expect(calculateTotal(items, 0.08)).toBe(27.0);
  });
});
```

### pytest (Python)

```python
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --cov=src --cov-report=term-missing
```

```python
# tests/test_utils.py
import pytest
from src.utils import calculate_total

def test_calculate_total_with_tax():
    items = [{"price": 10, "qty": 2}, {"price": 5, "qty": 1}]
    assert calculate_total(items, 0.08) == 27.0

def test_calculate_total_empty():
    assert calculate_total([], 0.08) == 0

@pytest.mark.parametrize("items,tax_rate,expected", [
    ([{"price": 10, "qty": 1}], 0.1, 11.0),
    ([{"price": 20, "qty": 2}], 0.05, 42.0),
])
def test_calculate_total_parametrized(items, tax_rate, expected):
    assert calculate_total(items, tax_rate) == expected
```

### Go Testing

```go
// utils_test.go
package utils

import "testing"

func TestCalculateTotal(t *testing.T) {
    tests := []struct {
        name     string
        items    []Item
        taxRate  float64
        expected float64
    }{
        {
            name:     "with tax",
            items:    []Item{{Price: 10, Qty: 2}, {Price: 5, Qty: 1}},
            taxRate:  0.08,
            expected: 27.0,
        },
        {
            name:     "empty items",
            items:    []Item{},
            taxRate:  0.08,
            expected: 0,
        },
    }

    for _, tc := range tests {
        t.Run(tc.name, func(t *testing.T) {
            got := CalculateTotal(tc.items, tc.taxRate)
            if got != tc.expected {
                t.Errorf("CalculateTotal() = %f, want %f", got, tc.expected)
            }
        })
    }
}
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Run tests
        run: npm test
        
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info
```

### GitLab CI

```yaml
# .gitlab-ci.yml
test:
  image: node:20
  stage: test
  script:
    - npm ci
    - npm test
  coverage: '/Lines\s*:\s*(\d+\.?\d*)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
```

## Mutation Testing

### Stryker (JavaScript/TypeScript)

```bash
# Install
npm install --save-dev @stryker-mutator/core @stryker-mutator/jest-runner

# Run
npx stryker run
```

```json
// stryker.conf.json
{
  "$schema": "https://raw.githubusercontent.com/stryker-mutator/stryker/master/packages/core/schema/stryker-core.json",
  "packageManager": "npm",
  "reporters": ["html", "clear-text", "progress"],
  "testRunner": "jest",
  "jestProjectFile": "jest.config.ts",
  "mutate": ["src/**/*.ts", "!src/**/*.test.ts"],
  "thresholds": {
    "high": 80,
    "low": 60,
    "break": 50
  }
}
```

### mutmut (Python)

```bash
# Install
pip install mutmut

# Run
mutmut run

# View results
mutmut results
mutmut html
```

## Performance Testing

### k6 (Load Testing)

```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },
    { duration: '1m', target: 20 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get('https://api.example.com/users');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
```

### Artillery

```yaml
# load-test.yml
config:
  target: "https://api.example.com"
  phases:
    - duration: 60
      arrivalRate: 10
    - duration: 120
      arrivalRate: 50
    - duration: 60
      arrivalRate: 10

scenarios:
  - name: "Get users"
    flow:
      - get:
          url: "/users"
          expect:
            - statusCode: 200
            - contentType: json
```

## Security Testing

### OWASP ZAP

```bash
# Docker scan
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t https://example.com \
  -r report.html
```

### Dependency Scanning

```bash
# npm audit
npm audit
npm audit fix

# Snyk
npx snyk test
npx snyk monitor
```

## Test Quality Checklist

- [ ] **Deterministic** - Same input produces same result
- [ ] **Isolated** - No shared mutable state
- [ ] **Fast** - Unit: < 10ms, Integration: < 1s, E2E: < 30s
- [ ] **Readable** - Test name describes scenario
- [ ] **Maintainable** - Change one behavior, change one test
- [ ] **Focused** - One logical assertion per test

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Testing implementation | Tests break on refactor | Test behavior |
| Flaky tests | Non-deterministic failures | Remove time/order dependencies |
| Overmocking | Tests nothing real | Only mock boundaries |
| No tests for bugs | Regression reappears | Add regression tests |

## Best Practices

1. **Test behavior** - Not implementation details
2. **Use parameterized tests** - For multiple inputs
3. **Mock at boundaries** - External APIs, DB, filesystem
4. **Name tests descriptively** - Scenario + expected result
5. **Run tests in CI** - On every push
6. **Monitor coverage** - But don't chase 100%
7. **Delete skipped tests** - Or fix them
8. **Use mutation testing** - Verify test quality
