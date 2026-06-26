---
title: MSW for Network Mocking
impact: HIGH
impactDescription: single source of truth
tags: testing, msw, mocking, network
---

## MSW for Network Mocking

Use Mock Service Worker instead of mocking useQuery directly.

```typescript
// src/mocks/handlers.ts
import { rest } from 'msw';

export const handlers = [
  rest.get('/api/todos', (req, res, ctx) => {
    return res(
      ctx.json([
        { id: 1, title: 'Todo 1', done: false },
        { id: 2, title: 'Todo 2', done: true },
      ])
    );
  }),
];

// src/mocks/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);

// src/setupTests.ts
import { server } from './mocks/server';

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

**Testing error states:**

```typescript
it('handles error state', async () => {
  server.use(
    rest.get('/api/todos', (req, res, ctx) => {
      return res(ctx.status(500));
    })
  );

  const { result } = renderHook(() => useTodos(), {
    wrapper: createWrapper(),
  });

  await waitFor(() => {
    expect(result.current.isError).toBe(true);
  });
});
```
