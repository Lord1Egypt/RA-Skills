---
title: Fresh QueryClient Per Test
impact: CRITICAL
impactDescription: test isolation
tags: testing, QueryClient, isolation
---

## Fresh QueryClient Per Test

Never share QueryClient between tests.

**Incorrect (shared client):**

```typescript
const queryClient = new QueryClient(); // Shared!

describe('TodoList', () => {
  it('test 1', () => {
    render(<TodoList />, { wrapper: ... });
  });

  it('test 2', () => {
    // Cache pollution from test 1!
    render(<TodoList />, { wrapper: ... });
  });
});
```

**Correct (fresh client per test):**

```typescript
function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
        gcTime: 0,
      },
      mutations: {
        retry: false,
      },
    },
    logger: {
      log: console.log,
      warn: console.warn,
      error: () => {}, // Silence error logs
    },
  });
}

function createWrapper() {
  const queryClient = createTestQueryClient();

  return function Wrapper({ children }: { children: React.ReactNode }) {
    return (
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    );
  };
}

describe('TodoList', () => {
  it('test 1', () => {
    render(<TodoList />, { wrapper: createWrapper() });
  });

  it('test 2', () => {
    render(<TodoList />, { wrapper: createWrapper() }); // Fresh!
  });
});
```
