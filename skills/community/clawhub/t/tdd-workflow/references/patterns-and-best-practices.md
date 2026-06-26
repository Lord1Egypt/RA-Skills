# TDD Patterns and Best Practices

## Test Types

### Unit Tests

- Individual functions and utilities
- Component logic
- Pure functions
- Helpers and utilities

### Integration Tests

- API endpoints
- Database operations
- Service interactions
- External API calls

### E2E Tests

- Critical user flows
- Complete workflows
- Browser automation
- UI interactions

## Common Testing Patterns

### Unit Test (Jest/Vitest)

```typescript
describe('Button Component', () => {
  it('renders with correct text', () => {
    expect(component).toBeDefined()
  })

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn()
    // Test interaction
    expect(handleClick).toHaveBeenCalled()
  })
})
```

### API Integration Test

```typescript
describe('GET /api/resource', () => {
  it('returns resource successfully', async () => {
    const response = await fetch('/api/resource')
    expect(response.status).toBe(200)
  })

  it('validates parameters', async () => {
    const response = await fetch('/api/resource?invalid=param')
    expect(response.status).toBe(400)
  })
})
```

### E2E Test (Playwright)

```typescript
test('user can complete flow', async ({ page }) => {
  await page.goto('/')
  await page.click('button')
  await expect(page.locator('text=Success')).toBeVisible()
})
```

## Best Practices

1. **Tests first** - Always TDD
2. **One assertion per test** - Focus on single behavior
3. **Descriptive names** - Explain what's tested
4. **Mock dependencies** - Isolate unit tests
5. **Test edge cases** - Null, undefined, empty, boundaries
6. **Test error paths** - Not just happy paths
7. **Keep tests fast** - Unit tests < 50ms each
8. **Clean up after tests** - No side effects
9. **Check coverage** - 80%+ target
10. **No skipped tests** - Review why tests are marked skip or pending

## Common Mistakes to Avoid

### ❌ Testing Implementation Details

```typescript
expect(component.state.count).toBe(5)
```

### ✅ Testing User-Visible Behavior

```typescript
expect(screen.getByText('Count: 5')).toBeInTheDocument()
```

### ❌ Brittle Selectors

```typescript
await page.click('.css-class-xyz')
```

### ✅ Semantic Selectors

```typescript
await page.click('[data-testid="submit-button"]')
```

### ❌ Tests That Depend on Each Other

```typescript
test('creates user', () => { /* ... */ })
test('updates same user', () => { /* depends on previous */ })
```

### ✅ Independent Tests

```typescript
beforeEach(() => {
  user = createTestUser()  // Fresh setup each test
})
```

## Mocking Examples

### Supabase Client Mock

```typescript
jest.mock('@/lib/supabase', () => ({
  supabase: {
    from: jest.fn(() => ({
      select: jest.fn(() => ({
        eq: jest.fn(() => Promise.resolve({
          data: [{ id: 1, name: 'Test' }],
          error: null
        }))
      }))
    }))
  }
}))
```

### Redis Mock

```typescript
jest.mock('@/lib/redis', () => ({
  searchByVector: jest.fn(() => Promise.resolve([
    { id: 'key-1', score: 0.95 }
  ])),
  set: jest.fn(() => Promise.resolve('OK')),
  get: jest.fn(() => Promise.resolve('value'))
}))
```

### OpenAI/Embedding API Mock

```typescript
jest.mock('@/lib/openai', () => ({
  generateEmbedding: jest.fn(() => Promise.resolve(
    new Array(1536).fill(0.1)  // 1536-dim vector
  ))
}))
```

### Database Integration Mock

```typescript
// Mock entire database module
jest.mock('@/lib/db', () => ({
  query: jest.fn(async (sql) => ({
    rows: [{ id: 1, data: 'test' }],
    rowCount: 1
  })),
  transaction: jest.fn(async (fn) => fn())
}))
```

## Success Metrics

- 80%+ code coverage achieved
- All tests passing (green)
- No skipped or disabled tests
- Fast test execution (< 30s for unit tests)
- E2E tests cover critical user flows
- Tests catch bugs before production
