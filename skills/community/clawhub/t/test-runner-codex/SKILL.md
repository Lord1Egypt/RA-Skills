---
name: test-runner
description: Write and run tests across languages and frameworks.
---

# Test Runner

## Core workflow

1. Detect the language, package manager, and existing test framework before changing anything.
2. Prefer the project's current test stack over introducing a new one.
3. Run the smallest relevant test scope first, then widen coverage after the failure is understood.
4. When fixing bugs, start with a failing test, make the smallest code change that passes, then refactor.
5. After changes, run the narrow test again and then a broader suite if the local workflow supports it.

## Framework selection

Use the existing framework when one is already configured. If the project has no test stack, prefer:

| Language | Unit tests | Integration | End-to-end |
| --- | --- | --- | --- |
| TypeScript / JavaScript | Vitest | Supertest | Playwright |
| Python | pytest | pytest + httpx | Playwright |
| Swift | XCTest | XCTest | XCUITest |

## Command guide

### Vitest

```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom
npx vitest
npx vitest run
npx vitest --coverage
```

Use this baseline config when a project needs one:

```typescript
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './tests/setup.ts',
  },
})
```

### Jest

```bash
npm install -D jest @types/jest ts-jest
npx jest
npx jest --watch
npx jest --coverage
npx jest path/to/test
```

### pytest

```bash
uv pip install pytest pytest-cov pytest-asyncio httpx
pytest
pytest -v
pytest -x
pytest --cov=app
pytest tests/test_api.py -k "test_login"
pytest --tb=short
```

### XCTest

```bash
swift test
swift test --filter MyTests
swift test --parallel
```

### Playwright

```bash
npm install -D @playwright/test
npx playwright install
npx playwright test
npx playwright test --headed
npx playwright test --debug
npx playwright test --project=chromium
npx playwright show-report
```

## Red-green-refactor

1. Red: write a failing test for the behavior you need.
2. Green: implement the smallest change that makes it pass.
3. Refactor: clean up without changing behavior.

## Test patterns

### Arrange, act, assert

```typescript
test('calculates total with tax', () => {
  const cart = new Cart([{ price: 100, qty: 2 }])

  const total = cart.totalWithTax(0.08)

  expect(total).toBe(216)
})
```

### Async tests

```typescript
test('fetches user data', async () => {
  const user = await getUser('123')
  expect(user.name).toBe('Colt')
})
```

### Mocking with Vitest

```typescript
import { vi } from 'vitest'

const mockFetch = vi.fn().mockResolvedValue({
  json: () => Promise.resolve({ id: 1, name: 'Test' }),
})

vi.stubGlobal('fetch', mockFetch)
```

### API tests in Python

```python
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_get_users():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/users")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

### React component tests

```typescript
import { fireEvent, render, screen } from '@testing-library/react'
import { Button } from './Button'

test('calls onClick when clicked', () => {
  const handleClick = vi.fn()
  render(<Button onClick={handleClick}>Click me</Button>)
  fireEvent.click(screen.getByText('Click me'))
  expect(handleClick).toHaveBeenCalledOnce()
})
```

## Coverage commands

```bash
# JavaScript / TypeScript
npx vitest --coverage
npx jest --coverage

# Python
pytest --cov=app --cov-report=html
pytest --cov=app --cov-report=term
pytest --cov=app --cov-fail-under=80
```

## What to test

Always test:

- Public APIs and exported functions
- Edge cases such as empty input, null, and boundary values
- Error handling such as invalid input or network failures
- Business logic such as calculations and state transitions

Usually skip:

- Private implementation details
- Framework internals
- Trivial getters and setters
- Third-party library behavior
