# React Query Best Practices

**Version 1.0.0** | **React Query v4**
Based on TkDodo's Blog Series
January 2026

> **Important:** This guide targets **React Query v4**. Some patterns may differ in v5.

> **Note:**
> This document is mainly for agents and LLMs to follow when maintaining,
> generating, or refactoring React Query codebases. Humans may also find
> it useful, but guidance here is optimized for automation and consistency
> by AI-assisted workflows.

---

## Abstract

Comprehensive guide for React Query (TanStack Query) based on TkDodo's authoritative blog series. Contains 24 rules across 7 categories, prioritized by impact from critical (query keys, mutations) to incremental (testing, troubleshooting). Each rule includes detailed explanations, real-world examples comparing incorrect vs. correct implementations, and specific impact metrics to guide automated refactoring and code generation.

---

## Table of Contents

1. [Query Keys & Patterns](#1-query-keys--patterns) — **CRITICAL**
   - 1.1 [Query Keys as Dependencies](#11-query-keys-as-dependencies)
   - 1.2 [Query Key Factory Pattern](#12-query-key-factory-pattern)
   - 1.3 [Select Option for Transformations](#13-select-option-for-transformations)
   - 1.4 [Status Check Order](#14-status-check-order)
   - 1.5 [Tracked Properties](#15-tracked-properties)
   - 1.6 [Placeholder vs Initial Data](#16-placeholder-vs-initial-data)
   - 1.7 [Dependent Queries with Enabled](#17-dependent-queries-with-enabled)
2. [Mutations & Updates](#2-mutations--updates) — **CRITICAL**
   - 2.1 [Prefer mutate() Over mutateAsync()](#21-prefer-mutate-over-mutateasync)
   - 2.2 [Query Invalidation](#22-query-invalidation)
   - 2.3 [Direct Cache Updates](#23-direct-cache-updates)
   - 2.4 [Optimistic Updates](#24-optimistic-updates)
   - 2.5 [Callback Separation Pattern](#25-callback-separation-pattern)
3. [Caching Strategy](#3-caching-strategy) — **HIGH**
   - 3.1 [Setting staleTime](#31-setting-staletime)
   - 3.2 [Refetch Triggers](#32-refetch-triggers)
4. [WebSocket Integration](#4-websocket-integration) — **HIGH**
   - 4.1 [Event-Based Invalidation](#41-event-based-invalidation)
   - 4.2 [Infinite staleTime for WS Data](#42-infinite-staletime-for-ws-data)
   - 4.3 [Reconnection Handling](#43-reconnection-handling)
5. [TypeScript Integration](#5-typescript-integration) — **MEDIUM**
   - 5.1 [Type Inference Strategy](#51-type-inference-strategy)
   - 5.2 [Runtime Validation with Zod](#52-runtime-validation-with-zod)
6. [Testing Patterns](#6-testing-patterns) — **MEDIUM**
   - 6.1 [Fresh QueryClient Per Test](#61-fresh-queryclient-per-test)
   - 6.2 [MSW for Network Mocking](#62-msw-for-network-mocking)
7. [Common Pitfalls](#7-common-pitfalls) — **MEDIUM**
   - 7.1 [Copying Query Data to State](#71-copying-query-data-to-state)
   - 7.2 [Missing Query Key Dependencies](#72-missing-query-key-dependencies)
   - 7.3 [Fetch Not Rejecting on Errors](#73-fetch-not-rejecting-on-errors)
8. [Migration to v5](#8-migration-to-v5) — **HIGH**
   - 8.1 [cacheTime Renamed to gcTime](#81-cachetime-renamed-to-gctime)
   - 8.2 [Query Callbacks Removed](#82-query-callbacks-removed)
   - 8.3 [New Suspense Hooks](#83-new-suspense-hooks)

---

## 1. Query Keys & Patterns

**Impact: CRITICAL**

Query keys are the foundation of React Query. Getting them right ensures proper caching, automatic refetching, and predictable behavior.

### 1.1 Query Keys as Dependencies

**Impact: CRITICAL (prevents cache collisions and stale closures)**

Include ALL variables used in queryFn as part of the queryKey. Query keys work like useEffect dependencies.

**Incorrect: filters not in queryKey**

```typescript
const [filters, setFilters] = useState({ status: 'active' });

useQuery({
  queryKey: ['todos'], // Missing filters!
  queryFn: () => fetchTodos(filters),
});
```

**Correct: all dependencies included**

```typescript
useQuery({
  queryKey: ['todos', filters], // Key changes when filters change
  queryFn: () => fetchTodos(filters),
});
```

Key changes automatically trigger refetches. This is the declarative pattern React Query is built for.

### 1.2 Query Key Factory Pattern

**Impact: HIGH (enables flexible invalidation)**

Use factory functions to generate consistent query keys. Structure: generic to specific.

**Incorrect: inconsistent key strings**

```typescript
// Scattered key definitions
useQuery({ queryKey: ['todos'] });
useQuery({ queryKey: ['todo', id] });
queryClient.invalidateQueries({ queryKey: ['todos'] }); // Might miss some
```

**Correct: centralized key factory**

```typescript
const todoKeys = {
  all: ['todos'] as const,
  lists: () => [...todoKeys.all, 'list'] as const,
  list: (filters: Filters) => [...todoKeys.lists(), filters] as const,
  details: () => [...todoKeys.all, 'detail'] as const,
  detail: (id: number) => [...todoKeys.details(), id] as const,
};

// Usage
useQuery({
  queryKey: todoKeys.detail(todoId),
  queryFn: () => fetchTodo(todoId),
});

// Flexible invalidation
queryClient.invalidateQueries({ queryKey: todoKeys.all });        // All todos
queryClient.invalidateQueries({ queryKey: todoKeys.lists() });    // All lists
queryClient.invalidateQueries({ queryKey: todoKeys.detail(5) });  // Specific todo
```

### 1.3 Select Option for Transformations

**Impact: MEDIUM (enables partial subscriptions)**

Use the `select` option for data transformations. It only runs when data exists and enables render optimizations.

**Incorrect: transform in queryFn or component**

```typescript
// Transform runs on every fetch
useQuery({
  queryKey: ['todos'],
  queryFn: async () => {
    const todos = await fetchTodos();
    return todos.filter(todo => !todo.done); // Runs every time
  },
});

// Or transform in component (no memoization)
const { data } = useQuery({...});
const activeTodos = data?.filter(todo => !todo.done);
```

**Correct: use select option**

```typescript
// Only runs when data exists, enables partial subscriptions
useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  select: (data) => data.filter(todo => !todo.done),
});

// Component only re-renders when count changes
useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  select: (data) => data.length,
});
```

For expensive transforms, stabilize with useCallback:

```typescript
const selectActiveTodos = useCallback(
  (data: Todo[]) => data.filter(todo => !todo.done),
  []
);

useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  select: selectActiveTodos,
});
```

### 1.4 Status Check Order

**Impact: MEDIUM (proper stale-while-revalidate UX)**

Check data availability FIRST, following the stale-while-revalidate philosophy.

**Incorrect: error blocks stale data display**

```typescript
function TodoList() {
  const { data, error, isPending } = useQuery({...});

  if (isPending) return <Loading />;
  if (error) return <Error />;  // Hides stale data on background refetch error
  return <List items={data} />;
}
```

**Correct: show stale data during background errors**

```typescript
function TodoList() {
  const { data, error, isPending } = useQuery({...});

  // Data first - show stale data during background refetch errors
  if (data) {
    return <List items={data} />;
  }

  // Then error (only when no data available)
  if (error) {
    return <Error message={error.message} />;
  }

  // Finally loading (initial load only)
  if (isPending) {
    return <Skeleton />;
  }
}
```

### 1.5 Tracked Properties

**Impact: LOW (reduces unnecessary re-renders)**

React Query tracks which properties you access during render. Only destructure what you need.

**Incorrect: rest spread tracks all fields**

```typescript
// Tracks ALL fields, defeats optimization
const { data, ...rest } = useQuery({...});
```

**Correct: explicit destructuring**

```typescript
// Only tracks data and isError
const { data, isError } = useQuery({...});

// Component won't re-render when isFetching changes
```

### 1.6 Placeholder vs Initial Data

**Impact: MEDIUM (affects caching behavior)**

Know when to use `initialData` (persists to cache) vs `placeholderData` (temporary).

| Aspect | initialData | placeholderData |
|--------|-------------|-----------------|
| Persists to cache | Yes | No |
| Respects staleTime | Yes | No (always refetches) |
| Scope | Cache-level (shared) | Observer-level (per component) |

**initialData: pre-fill from another query's cache**

```typescript
useQuery({
  queryKey: ['todo', todoId],
  queryFn: () => fetchTodo(todoId),
  initialData: () => {
    return queryClient
      .getQueryData(['todos'])
      ?.find(todo => todo.id === todoId);
  },
  initialDataUpdatedAt: () => {
    return queryClient.getQueryState(['todos'])?.dataUpdatedAt;
  },
});
```

**placeholderData: temporary data during fetch**

```typescript
useQuery({
  queryKey: ['todo', todoId],
  queryFn: () => fetchTodo(todoId),
  placeholderData: { id: todoId, title: 'Loading...', done: false },
});

// For smooth pagination transitions
useQuery({
  queryKey: ['todos', page],
  queryFn: () => fetchTodos(page),
  placeholderData: keepPreviousData,
});
```

### 1.7 Dependent Queries with Enabled

**Impact: HIGH (prevents unnecessary fetches)**

Use the `enabled` option to control when queries run.

**Incorrect: query runs with undefined params**

```typescript
const { data: user } = useQuery({...});

// Runs immediately with undefined userId!
const { data: projects } = useQuery({
  queryKey: ['projects', user?.id],
  queryFn: () => fetchProjects(user?.id),
});
```

**Correct: enabled option controls execution**

```typescript
const { data: user } = useQuery({
  queryKey: ['user', userId],
  queryFn: () => fetchUser(userId),
});

const { data: projects } = useQuery({
  queryKey: ['projects', user?.id],
  queryFn: () => fetchProjects(user!.id),
  enabled: !!user?.id, // Only fetch when user is loaded
});
```

**With skipToken (v5.25+):**

```typescript
import { skipToken } from '@tanstack/react-query';

useQuery({
  queryKey: ['user', userId],
  queryFn: userId ? () => fetchUser(userId) : skipToken,
});
```

---

## 2. Mutations & Updates

**Impact: CRITICAL**

Mutations modify server state. Proper patterns ensure data consistency and good UX.

### 2.1 Prefer mutate() Over mutateAsync()

**Impact: HIGH (better error handling)**

Use `mutate()` with callbacks for most cases. Only use `mutateAsync()` for sequential operations.

**Incorrect: unhandled promise rejection**

```typescript
const { mutateAsync } = useMutation({...});

// Easy to forget try/catch
const handleSave = () => {
  mutateAsync(data); // Unhandled rejection if error!
};
```

**Correct: mutate with callbacks**

```typescript
const { mutate } = useMutation({
  mutationFn: updateTodo,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['todos'] });
  },
});

mutate(todoData, {
  onSuccess: () => toast.success('Saved!'),
  onError: (error) => toast.error(error.message),
});
```

**Use mutateAsync only for sequential mutations:**

```typescript
async function handleComplexSave() {
  try {
    const user = await createUserMutation.mutateAsync(userData);
    await createProfileMutation.mutateAsync({
      userId: user.id,
      ...profileData,
    });
    toast.success('User and profile created!');
  } catch (error) {
    toast.error('Failed to create user');
  }
}
```

### 2.2 Query Invalidation

**Impact: CRITICAL (ensures data consistency)**

Invalidate related queries after mutations to trigger refetches.

**Incorrect: manual refetch or no sync**

```typescript
const { mutate } = useMutation({
  mutationFn: updateTodo,
  onSuccess: () => {
    // Manual refetch - doesn't work well with multiple components
    refetch();
  },
});
```

**Correct: invalidate queries**

```typescript
const mutation = useMutation({
  mutationFn: updateTodo,
  onSuccess: () => {
    // Marks queries as stale, triggers refetch for active ones
    queryClient.invalidateQueries({ queryKey: ['todos'] });
  },
});
```

**Await invalidation to keep button disabled:**

```typescript
const mutation = useMutation({
  mutationFn: updateTodo,
  onSuccess: async () => {
    // Keep isPending true until refetch completes
    await queryClient.invalidateQueries({ queryKey: ['todos'] });
  },
});

<Button disabled={mutation.isPending}>Save</Button>
```

### 2.3 Direct Cache Updates

**Impact: MEDIUM (instant UI feedback)**

Update cache directly when mutation returns updated data.

```typescript
const mutation = useMutation({
  mutationFn: updateTodo,
  onSuccess: (updatedTodo) => {
    // Update specific item in list
    queryClient.setQueryData(['todos'], (old: Todo[]) =>
      old.map(todo =>
        todo.id === updatedTodo.id ? updatedTodo : todo
      )
    );

    // Also update detail cache
    queryClient.setQueryData(
      ['todos', updatedTodo.id],
      updatedTodo
    );
  },
});
```

### 2.4 Optimistic Updates

**Impact: HIGH (instant perceived performance)**

Show success immediately, rollback on failure.

```typescript
const mutation = useMutation({
  mutationFn: updateTodo,

  onMutate: async (newTodo) => {
    // Cancel outgoing refetches
    await queryClient.cancelQueries({ queryKey: ['todos', newTodo.id] });

    // Snapshot previous value
    const previousTodo = queryClient.getQueryData(['todos', newTodo.id]);

    // Optimistically update
    queryClient.setQueryData(['todos', newTodo.id], newTodo);

    // Return context for rollback
    return { previousTodo };
  },

  onError: (err, newTodo, context) => {
    // Rollback on error
    if (context?.previousTodo) {
      queryClient.setQueryData(
        ['todos', newTodo.id],
        context.previousTodo
      );
    }
  },

  onSettled: () => {
    // Always refetch to ensure consistency
    queryClient.invalidateQueries({ queryKey: ['todos'] });
  },
});
```

**Good candidates for optimistic updates:**
- Toggle actions (like/unlike, done/undone)
- Simple field updates
- High-confidence mutations

**Avoid for:**
- Complex operations that might fail
- Actions requiring server-side validation

### 2.5 Callback Separation Pattern

**Impact: MEDIUM (separation of concerns)**

Place query logic in hook, UI effects in component.

**Custom hook - query-related logic:**

```typescript
export function useUpdateTodo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateTodo,
    onSuccess: (data) => {
      // Query cache updates here
      queryClient.setQueryData(['todos', data.id], data);
      queryClient.invalidateQueries({ queryKey: ['todos', 'list'] });
    },
    onError: (error) => {
      // Logging here
      console.error('Update failed:', error);
    },
  });
}
```

**Component - UI effects:**

```typescript
function TodoEditor() {
  const { mutate } = useUpdateTodo();

  const handleSave = () => {
    mutate(todoData, {
      onSuccess: () => {
        toast.success('Saved!');
        closeModal();
      },
      onError: () => {
        toast.error('Save failed');
      },
    });
  };
}
```

---

## 3. Caching Strategy

**Impact: HIGH**

Proper caching configuration balances freshness with performance.

### 3.1 Setting staleTime

**Impact: HIGH (reduces unnecessary refetches)**

Set appropriate `staleTime` based on how often your data changes.

**Recommended defaults:**

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 2, // 2 minutes
      gcTime: 1000 * 60 * 5,    // 5 minutes (formerly cacheTime)
      retry: 3,
    },
  },
});
```

**Per-query overrides:**

```typescript
// Frequently changing data
useQuery({
  queryKey: ['notifications'],
  queryFn: fetchNotifications,
  staleTime: 1000 * 30, // 30 seconds
});

// Rarely changing data
useQuery({
  queryKey: ['config'],
  queryFn: fetchConfig,
  staleTime: 1000 * 60 * 30, // 30 minutes
});

// WebSocket-managed data
useQuery({
  queryKey: ['automations', id],
  queryFn: () => fetchAutomation(id),
  staleTime: Infinity, // Manual invalidation via WebSocket
});
```

### 3.2 Refetch Triggers

**Impact: HIGH (data freshness)**

Keep refetch triggers enabled in production. They're features, not bugs.

**Incorrect: over-disabling**

```typescript
useQuery({
  queryKey: ['user'],
  queryFn: fetchUser,
  refetchOnMount: false,
  refetchOnWindowFocus: false,
  refetchOnReconnect: false,
  staleTime: Infinity,
});
// Data never updates automatically!
```

**Correct: appropriate configuration**

```typescript
// Most queries: keep defaults
useQuery({
  queryKey: ['user'],
  queryFn: fetchUser,
  staleTime: 1000 * 60 * 5, // 5 minutes
  // refetchOnWindowFocus: true (default)
  // refetchOnMount: true (default)
});

// Only disable for truly static or WebSocket-managed data
useQuery({
  queryKey: ['automations', id],
  queryFn: () => fetchAutomation(id),
  staleTime: Infinity,
  refetchOnWindowFocus: false, // WebSocket handles this
});
```

---

## 4. WebSocket Integration

**Impact: HIGH**

Real-time data synchronization patterns for WebSocket-driven updates.

### 4.1 Event-Based Invalidation

**Impact: HIGH (simple, predictable)**

Push lightweight events from backend, not full data objects.

```typescript
// Backend sends events like:
// { "entity": ["automations", "list"] }
// { "entity": ["automations", "detail"], "id": "abc123" }

function useWebSocketSync() {
  const queryClient = useQueryClient();

  useEffect(() => {
    const socket = connectWebSocket();

    socket.on('invalidate', (event) => {
      queryClient.invalidateQueries({
        queryKey: event.entity,
      });
    });

    return () => socket.disconnect();
  }, [queryClient]);
}
```

**Example pattern (entity-specific WebSocket handler):**

```typescript
const handleMessage = useCallback((message: WebSocketMessage) => {
  switch (message.type) {
    case 'AUTOMATION_UPDATED':
      queryClient.invalidateQueries({
        queryKey: ['automations', message.automationId],
      });
      break;

    case 'AUTOMATION_STATUS_CHANGED':
      // Direct cache update for frequent status changes
      queryClient.setQueryData(
        ['automations', message.automationId],
        (old) => old ? { ...old, status: message.status } : old
      );
      break;

    case 'AUTOMATION_LIST_CHANGED':
      queryClient.invalidateQueries({
        queryKey: ['automations', 'list'],
      });
      break;
  }
}, [queryClient]);
```

### 4.2 Infinite staleTime for WS Data

**Impact: HIGH (prevents redundant fetches)**

When WebSocket handles updates, disable automatic refetching.

```typescript
// Queries updated via WebSocket
useQuery({
  queryKey: ['automations', automationId],
  queryFn: () => fetchAutomation(automationId),
  staleTime: Infinity, // Manual invalidation via WebSocket
  refetchOnWindowFocus: false,
});
```

### 4.3 Reconnection Handling

**Impact: MEDIUM (ensures consistency after disconnect)**

Invalidate stale queries when WebSocket reconnects.

```typescript
function useWebSocketWithReconnect() {
  const queryClient = useQueryClient();
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const socket = connectWebSocket();

    socket.on('connect', () => {
      setIsConnected(true);
      // Refresh stale data after reconnection
      queryClient.invalidateQueries({
        predicate: (query) => query.state.isInvalidated,
      });
    });

    socket.on('disconnect', () => {
      setIsConnected(false);
    });

    return () => socket.disconnect();
  }, [queryClient]);

  return isConnected;
}
```

**Fallback to polling when disconnected:**

```typescript
const { data } = useQuery({
  queryKey: ['automations', id],
  queryFn: () => fetchAutomation(id),
  staleTime: isWebSocketConnected ? Infinity : 0,
  refetchInterval: isWebSocketConnected ? false : 5000,
});
```

---

## 5. TypeScript Integration

**Impact: MEDIUM**

Let TypeScript infer types rather than explicitly specifying generics.

### 5.1 Type Inference Strategy

**Impact: MEDIUM (cleaner code, fewer errors)**

Type the queryFn, not the hook.

**Incorrect: explicit generics**

```typescript
// Unnecessary and error-prone
const { data } = useQuery<Todo[], Error>({
  queryKey: ['todos'],
  queryFn: fetchTodos,
});
```

**Correct: type the function**

```typescript
// Type flows automatically
async function fetchTodos(): Promise<Todo[]> {
  const response = await fetch('/api/todos');
  return response.json();
}

const { data } = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
});
// data is Todo[] | undefined
```

**With select, inference still works:**

```typescript
const { data } = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  select: (todos) => todos.length,
});
// data is number | undefined
```

### 5.2 Runtime Validation with Zod

**Impact: HIGH (catches API contract violations)**

Replace type assertions with runtime validation.

```typescript
import { z } from 'zod';

const todoSchema = z.object({
  id: z.number(),
  title: z.string(),
  done: z.boolean(),
  createdAt: z.string().transform(s => new Date(s)),
});

const todosSchema = z.array(todoSchema);

type Todo = z.infer<typeof todoSchema>;

async function fetchTodos(): Promise<Todo[]> {
  const response = await fetch('/api/todos');
  const data = await response.json();
  return todosSchema.parse(data); // Runtime validation
}
```

**Benefits:**
- Catches data shape mismatches at runtime
- Failed validation triggers error state
- Single source of truth for types

---

## 6. Testing Patterns

**Impact: MEDIUM**

Proper test setup ensures reliable, isolated tests.

### 6.1 Fresh QueryClient Per Test

**Impact: CRITICAL (test isolation)**

Never share QueryClient between tests.

**Incorrect: shared client**

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

**Correct: fresh client per test**

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

### 6.2 MSW for Network Mocking

**Impact: HIGH (single source of truth)**

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

---

## 7. Common Pitfalls

**Impact: MEDIUM**

Avoid these common mistakes that break React Query's guarantees.

### 7.1 Copying Query Data to State

**Impact: HIGH (breaks single source of truth)**

Never copy query results to local state.

**Incorrect: duplicated state**

```typescript
const { data } = useQuery({ queryKey: ['user'], queryFn: fetchUser });
const [user, setUser] = useState(data);

useEffect(() => {
  if (data) setUser(data);
}, [data]);
// Breaks background updates, creates sync bugs
```

**Correct: use query data directly**

```typescript
const { data: user } = useQuery({
  queryKey: ['user'],
  queryFn: fetchUser,
});

// For derived state, use select
const { data: userName } = useQuery({
  queryKey: ['user'],
  queryFn: fetchUser,
  select: (user) => user.name,
});
```

### 7.2 Missing Query Key Dependencies

**Impact: CRITICAL (causes cache collisions)**

Always include all queryFn parameters in the query key.

**Incorrect: filters not in key**

```typescript
const [filters, setFilters] = useState({ status: 'active' });

useQuery({
  queryKey: ['todos'], // Missing filters!
  queryFn: () => fetchTodos(filters),
});
// Cache collision between different filter states
```

**Correct: include all dependencies**

```typescript
useQuery({
  queryKey: ['todos', filters],
  queryFn: () => fetchTodos(filters),
});
```

### 7.3 Fetch Not Rejecting on Errors

**Impact: HIGH (silent failures)**

The fetch API doesn't reject on HTTP errors.

**Incorrect: 404 treated as success**

```typescript
const { data, error } = useQuery({
  queryKey: ['user'],
  queryFn: () => fetch('/api/user').then(res => res.json()),
});
// error is always null even on 404!
```

**Correct: check response.ok**

```typescript
const { data, error } = useQuery({
  queryKey: ['user'],
  queryFn: async () => {
    const res = await fetch('/api/user');
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    return res.json();
  },
});
```

**Or use axios (rejects automatically):**

```typescript
const { data, error } = useQuery({
  queryKey: ['user'],
  queryFn: () => axios.get('/api/user').then(res => res.data),
});
```

---

## 8. Migration to v5

**Impact: HIGH**

When upgrading from React Query v4 to v5, these are the key breaking changes to address.

### 8.1 cacheTime Renamed to gcTime

**Impact: HIGH (breaking change, find-replace required)**

In v5, `cacheTime` was renamed to `gcTime` to better reflect its purpose: it controls when unused/inactive cache entries are garbage collected.

**v4 (before):**

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      cacheTime: 1000 * 60 * 5, // 5 minutes
    },
  },
});

useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  cacheTime: 1000 * 60 * 10, // 10 minutes
});
```

**v5 (after):**

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      gcTime: 1000 * 60 * 5, // 5 minutes
    },
  },
});

useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  gcTime: 1000 * 60 * 10, // 10 minutes
});
```

**Migration:** Find and replace all occurrences of `cacheTime` with `gcTime`.

### 8.2 Query Callbacks Removed

**Impact: HIGH (breaking change, refactor required)**

In v5, the `onSuccess`, `onError`, and `onSettled` callbacks were removed from `useQuery`. Use `useEffect` or handle in the component instead.

**Why removed:** These callbacks had subtle timing issues and didn't play well with React's concurrent features.

**v4 (before):**

```typescript
useQuery({
  queryKey: ['user', userId],
  queryFn: () => fetchUser(userId),
  onSuccess: (data) => {
    console.log('User loaded:', data);
    analytics.track('user_loaded');
  },
  onError: (error) => {
    toast.error(error.message);
  },
});
```

**v5 (after):**

```typescript
const { data, error } = useQuery({
  queryKey: ['user', userId],
  queryFn: () => fetchUser(userId),
});

useEffect(() => {
  if (data) {
    console.log('User loaded:', data);
    analytics.track('user_loaded');
  }
}, [data]);

useEffect(() => {
  if (error) {
    toast.error(error.message);
  }
}, [error]);
```

**Note:** Mutation callbacks (`onSuccess`, `onError`, `onSettled`) are still available on `useMutation`.

### 8.3 New Suspense Hooks

**Impact: HIGH (new API for suspense mode)**

In v5, suspense mode uses dedicated hooks instead of the `suspense` option. This provides better TypeScript inference since data is guaranteed to be defined.

**v4 (before):**

```typescript
const { data } = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  suspense: true,
});

// data is TData | undefined (TypeScript doesn't know suspense guarantees data)
```

**v5 (after):**

```typescript
import { useSuspenseQuery } from '@tanstack/react-query';

const { data } = useSuspenseQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
});

// data is TData (guaranteed by suspense, TypeScript knows this)
```

**Available suspense hooks in v5:**
- `useSuspenseQuery` - Single query with suspense
- `useSuspenseInfiniteQuery` - Infinite query with suspense
- `useSuspenseQueries` - Multiple queries with suspense

---

## Best Practices Summary

### DO

- Include all queryFn parameters in queryKey
- Use `mutate()` with callbacks for most mutations
- Set appropriate `staleTime` for your domain
- Keep `refetchOnWindowFocus` enabled in production
- Use `select` for derived/computed data
- Create fresh `QueryClient` per test
- Use Zod for runtime API validation

### DON'T

- Copy query results to local state
- Use `useEffect` to sync React Query state elsewhere
- Disable refetch triggers without good reason
- Use same keys for `useQuery` and `useInfiniteQuery`
- Forget to handle loading/error states
- Add explicit generics to useQuery/useMutation
