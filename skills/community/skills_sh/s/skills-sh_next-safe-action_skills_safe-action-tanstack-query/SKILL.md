---
name: safe-action-tanstack-query
description: Use when integrating next-safe-action with TanStack Query (React Query) -- mutationOptions(), useMutation, ActionMutationError error handling, type guards, optimistic updates via query cache, query invalidation after mutations
---

# next-safe-action TanStack Query Adapter

## Install

```bash
npm install @next-safe-action/adapter-tanstack-query @tanstack/react-query
```

## Import

```ts
import {
  mutationOptions,
  ActionMutationError,
  isActionMutationError,
  hasServerError,
  hasValidationErrors,
} from "@next-safe-action/adapter-tanstack-query";
```

## Quick Start

```tsx
"use client";

import { useMutation } from "@tanstack/react-query";
import { mutationOptions } from "@next-safe-action/adapter-tanstack-query";
import { createUser } from "@/app/actions";

export function CreateUserForm() {
  const { mutate, isPending, isError, error, data } = useMutation(
    mutationOptions(createUser, {
      onSuccess: (data) => {
        toast.success(`Created ${data.name}`);
      },
    })
  );

  return (
    <form onSubmit={(e) => {
      e.preventDefault();
      const fd = new FormData(e.currentTarget);
      mutate({ name: fd.get("name") as string, email: fd.get("email") as string });
    }}>
      <input name="name" required />
      <input name="email" type="email" required />
      <button type="submit" disabled={isPending}>
        {isPending ? "Creating..." : "Create User"}
      </button>
      {isError && <p className="text-red-500">{error.message}</p>}
      {data && <p>Created: {data.name}</p>}
    </form>
  );
}
```

## How It Works

`mutationOptions()` creates a complete `UseMutationOptions` object that bridges next-safe-action's result envelope to TanStack Query's error model:

1. **Calls the safe action** with input provided to `mutate()` / `mutateAsync()`
2. **Inspects the result envelope** for `serverError` or `validationErrors`
3. **Throws `ActionMutationError`** if either is present (a client-side error class, `instanceof` works)
4. **Returns `data`** directly as TanStack Query's `TData` on success
5. **Handles navigation errors** (`redirect()`, `notFound()`, etc.) by composing `throwOnError` to always re-throw them during React's render phase

## When to Use Which

| Scenario | Recommendation |
|---|---|
| New Next.js project without TanStack Query | Built-in hooks |
| Simple form submissions and button actions | Built-in hooks |
| Instant optimistic UI via React's `useOptimistic` | Built-in hooks (`useOptimisticAction`) |
| Zero additional dependencies | Built-in hooks |
| Already using TanStack Query for data fetching | Adapter |
| Already using tRPC + TanStack Query | Adapter |
| Need automatic retries with backoff | Adapter |
| Need to invalidate client query cache after mutations | Adapter |
| Want TanStack Query DevTools for mutations | Adapter |
| Need offline mutation persistence | Adapter |

## Feature Comparison

| Feature | Built-in hooks | Adapter |
|---|---|---|
| React Transitions | Yes, actions run inside `startTransition` | No |
| Optimistic updates | `useOptimisticAction` via React's `useOptimistic` | Manual via `onMutate` + query cache |
| Automatic retries | No | Yes, `retry` option with backoff |
| Server cache invalidation | Yes, `revalidatePath()` / `revalidateTag()` | Yes, same Next.js APIs |
| Client query cache invalidation | No (not applicable) | Yes, `queryClient.invalidateQueries()` |
| DevTools | No | Yes, TanStack Query DevTools |
| Error model | Result envelope (`result.serverError`, `result.validationErrors`) | Thrown `ActionMutationError` with type guards |
| Offline mutation persistence | No | Yes, paused mutations via `dehydrate`/`hydrate` |
| Async execution | `executeAsync()` returns `Promise<Result>` | `mutateAsync()` returns `Promise<Data>` |
| Status tracking | `status` string + shorthand booleans | Boolean flags (`isPending`, `isError`, `isSuccess`) |
| Extra dependencies | None (React only) | `@tanstack/react-query` |

**General guidance:** Prefer built-in hooks for most Next.js apps. They require no extra dependencies and integrate with React's concurrent rendering. Prefer the adapter when TanStack Query is already part of your stack, especially for cache invalidation, retries, DevTools, and offline support.

## Why Mutations Only

This adapter provides only `mutationOptions()`. There is **no** `queryOptions()`, by design:

- Server Actions use `POST` only, not suitable for `GET`-based queries
- Server Actions are queued per client, creating request waterfalls
- `POST` requests bypass browser cache, `ETag`, and conditional requests
- No stable resource identity for TanStack Query deduplication

For data fetching: use Server Components (server-side), Route Handlers + `useQuery` (client-side), or tRPC (full-stack type-safe).

## Entry Points

| Entry point | Exports | Environment |
|---|---|---|
| `@next-safe-action/adapter-tanstack-query` | `mutationOptions`, `ActionMutationError`, `isActionMutationError`, `hasServerError`, `hasValidationErrors`, types | Client |

## Important Constraints

**Only works with non-throwing actions.** Do NOT use `throwValidationErrors: true` or `throwServerError: true` with actions passed to `mutationOptions()`. The adapter inspects the result envelope for errors. If errors are thrown instead of returned, the adapter cannot extract structured error data, and you lose type-safe error handling. TypeScript enforces this via `NonThrowingActionConstraint`.

## Supporting Docs

- [Mutation patterns, error handling, and optimistic updates](./mutation-patterns.md)

## Anti-Patterns

```ts
// BAD: Using throwValidationErrors with adapter — errors bypass the result envelope
const client = createSafeActionClient({ throwValidationErrors: true });
const action = client.inputSchema(schema).action(async ({ parsedInput }) => { ... });
mutationOptions(action); // TypeScript error! NonThrowingActionConstraint not met

// BAD: Using mutationOptions for data fetching — server actions are POST-only
const { data } = useQuery(mutationOptions(fetchUsers)); // Wrong! Use Route Handler + useQuery

// BAD: Manually calling the action inside mutationFn
useMutation({
  mutationFn: async (input) => {
    const result = await myAction(input); // Loses error bridging, navigation handling
    return result.data;
  },
});

// GOOD: Let mutationOptions handle the bridging
useMutation(mutationOptions(myAction));
```
