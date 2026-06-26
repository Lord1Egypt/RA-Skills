# Mutation Patterns

## Basic Mutation

```tsx
"use client";

import { useMutation } from "@tanstack/react-query";
import { mutationOptions } from "@next-safe-action/adapter-tanstack-query";
import { updateProfile } from "@/app/actions";

export function ProfileForm({ user }: { user: User }) {
  const mutation = useMutation(mutationOptions(updateProfile));

  return (
    <form onSubmit={(e) => {
      e.preventDefault();
      const fd = new FormData(e.currentTarget);
      mutation.mutate({
        name: fd.get("name") as string,
        bio: fd.get("bio") as string,
      });
    }}>
      <input name="name" defaultValue={user.name} />
      <textarea name="bio" defaultValue={user.bio ?? ""} />
      <button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? "Saving..." : "Save"}
      </button>
      {mutation.isError && <ErrorDisplay error={mutation.error} />}
      {mutation.isSuccess && <p>Profile updated!</p>}
    </form>
  );
}
```

## Callbacks and Query Invalidation

```tsx
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { mutationOptions } from "@next-safe-action/adapter-tanstack-query";
import { hasServerError, hasValidationErrors } from "@next-safe-action/adapter-tanstack-query";

export function CreatePostButton() {
  const queryClient = useQueryClient();

  const mutation = useMutation(mutationOptions(createPostAction, {
    onSuccess: (data) => {
      toast.success(`Created "${data.title}"`);
      // Invalidate the posts query so the list refetches
      queryClient.invalidateQueries({ queryKey: ["posts"] });
    },
    onError: (error) => {
      if (hasValidationErrors(error)) {
        // error.validationErrors is typed based on your input schema
        toast.error("Please fix the form errors");
      } else if (hasServerError(error)) {
        toast.error(`Server error: ${error.serverError}`);
      }
    },
  }));

  return (
    <button onClick={() => mutation.mutate({ title: "New Post", content: "..." })} disabled={mutation.isPending}>
      Create Post
    </button>
  );
}
```

## Error Handling

### ActionMutationError

When an action returns `serverError` or `validationErrors`, the adapter wraps them in an `ActionMutationError`:

```ts
class ActionMutationError<ServerError, ShapedErrors> extends Error {
  readonly kind: "server" | "validation" | "both";
  readonly serverError?: ServerError;
  readonly validationErrors?: ShapedErrors;
}
```

### Type Guards

Three type guards help narrow the error type:

```tsx
import {
  isActionMutationError,
  hasServerError,
  hasValidationErrors,
} from "@next-safe-action/adapter-tanstack-query";

// ServerError and ShapedErrors types are inferred from your action
function ErrorDisplay({ error }: { error: ActionMutationError<string, Record<string, { _errors?: string[] }>> }) {
  if (hasServerError(error)) {
    // error.serverError is guaranteed non-undefined here
    return <p className="text-red-500">Server error: {error.serverError}</p>;
  }

  if (hasValidationErrors(error)) {
    // error.validationErrors is guaranteed non-undefined here
    return (
      <ul className="text-red-500">
        {Object.entries(error.validationErrors).map(([field, errs]) => (
          <li key={field}>{field}: {(errs as any)?._errors?.[0]}</li>
        ))}
      </ul>
    );
  }

  return <p className="text-red-500">{error.message}</p>;
}
```

### Displaying Errors from Mutation State

```tsx
function MyForm() {
  const mutation = useMutation(mutationOptions(myAction));

  return (
    <form onSubmit={(e) => { e.preventDefault(); mutation.mutate(formData); }}>
      {/* Form fields... */}

      {mutation.isError && (
        <>
          {hasServerError(mutation.error) && (
            <p className="text-red-500">{mutation.error.serverError}</p>
          )}
          {hasValidationErrors(mutation.error) && (
            <p className="text-red-500">
              {mutation.error.validationErrors.email?._errors?.[0]}
            </p>
          )}
        </>
      )}
    </form>
  );
}
```

## Optimistic Updates

Use TanStack Query's `onMutate` to optimistically update the query cache:

```tsx
const queryClient = useQueryClient();

const mutation = useMutation(mutationOptions(toggleTodoAction, {
  onMutate: async (input) => {
    // Cancel outgoing queries to prevent overwriting our optimistic update
    await queryClient.cancelQueries({ queryKey: ["todos"] });

    // Snapshot current state for rollback
    const previous = queryClient.getQueryData<Todo[]>(["todos"]);

    // Optimistically update the cache
    queryClient.setQueryData<Todo[]>(["todos"], (old) =>
      old?.map((t) => t.id === input.id ? { ...t, done: !t.done } : t)
    );

    return { previous };
  },
  onError: (_error, _input, context) => {
    // Rollback on error
    if (context?.previous) {
      queryClient.setQueryData(["todos"], context.previous);
    }
  },
  onSettled: () => {
    // Always refetch to ensure consistency
    queryClient.invalidateQueries({ queryKey: ["todos"] });
  },
}));
```

**Contrast with built-in hooks:** `useOptimisticAction` uses React's `useOptimistic` for automatic rollback. The TanStack Query approach gives you more control (manual cache manipulation) but requires more boilerplate. Choose based on whether you're already using TanStack Query for data fetching.

## Retry Logic

```tsx
const mutation = useMutation(mutationOptions(submitOrder, {
  retry: (failureCount, error) => {
    // Don't retry validation errors — they'll fail again
    if (hasValidationErrors(error)) return false;
    // Retry server errors up to 3 times
    return failureCount < 3;
  },
}));
```

Navigation errors (`redirect`, `notFound`, etc.) are never retried. The adapter composes `retry` to automatically skip them.

## mutateAsync for Sequential Flows

```tsx
const createUser = useMutation(mutationOptions(createUserAction));
const assignRole = useMutation(mutationOptions(assignRoleAction));

const handleSubmit = async () => {
  try {
    const user = await createUser.mutateAsync({ name, email });
    await assignRole.mutateAsync({ userId: user.id, role: "admin" });
    toast.success("User created and role assigned");
  } catch (error) {
    if (isActionMutationError(error)) {
      if (hasServerError(error)) {
        toast.error(error.serverError);
      }
    }
  }
};
```

## Navigation Errors

Navigation errors (`redirect()`, `notFound()`, `forbidden()`, `unauthorized()`) are handled automatically:

- The adapter composes `throwOnError` to always re-throw navigation errors during React's render phase
- The adapter composes `retry` to never retry navigation errors
- No configuration needed: just call `redirect()` or `notFound()` in your server action, and Next.js handles the rest

## Bound Arguments

```tsx
import { useMutation } from "@tanstack/react-query";
import { mutationOptions } from "@next-safe-action/adapter-tanstack-query";
import { updatePost } from "@/app/actions";

export function EditPostForm({ postId }: { postId: string }) {
  // Bind the postId argument
  const boundAction = updatePost.bind(null, postId);

  const mutation = useMutation(mutationOptions(boundAction, {
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["posts", postId] });
    },
  }));

  return (
    <form onSubmit={(e) => {
      e.preventDefault();
      mutation.mutate({ title: "Updated Title", content: "..." });
    }}>
      {/* Form fields */}
    </form>
  );
}
```

## Type Utilities

```ts
import type { InferMutationOptions, InferActionMutationError } from "@next-safe-action/adapter-tanstack-query";
import type { createUserAction } from "@/app/actions";

// Infer the full mutation options type from an action
type CreateUserMutationOpts = InferMutationOptions<typeof createUserAction>;

// Infer the error type for a given action
type CreateUserError = InferActionMutationError<typeof createUserAction>;
// CreateUserError = ActionMutationError<string, { name?: { _errors: string[] }, ... }>
```
