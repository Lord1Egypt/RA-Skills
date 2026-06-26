# SvelteKit Reference

Project signature: `frontend/package.json` with Svelte + a `frontend/src/lib/forge/` dir. See the shared rules in [frontend.md](../frontend.md).

## Generated APIs

For a backend query `list_todos`:

| Export | File | Returns | Use for |
|---|---|---|---|
| `listTodos()` | `api.ts` | `Promise<T[]>` | One-shot RPC. |
| `listTodosStore$()` | `api.ts` | `SubscriptionStore<T[]>` | Classic Svelte store (use `$` in markup, call `unsubscribe()`). |
| `listTodos$()` | `reactive.svelte.ts` | `ReactiveQuery<T[]>` | **Svelte 5 runes.** Auto-cleanup. Preferred. |

For mutations:

| Export | File | Returns | Use for |
|---|---|---|---|
| `createTodo(args)` | `api.ts` | `Promise<T>` | Manual one-shot call. |
| `createTodo$()` | `reactive.svelte.ts` | `ReactiveMutation<Args, T>` | Runes mutation with `{ mutate, pending, error }` state. |

For jobs / workflows / uploads:
- `trackExportUsers(args)` returns `JobStore<T>` — stream `status`, `progress`, `output`.
- `trackOnboardUser(args)` returns `WorkflowStore<T>`.
- `Upload` / `File` / `Blob` → the generated `call()` switches to `multipart/form-data`.

## Using Svelte 5 Runes

Top-level call in a component is safe — the helper registers an `$effect` root and closes the SSE subscription on unmount. No manual `unsubscribe()`.

```svelte
<script>
  import { listTodos$ } from '$lib/forge';
  const todos = listTodos$();
</script>

{#if todos.loading}<p>Loading…</p>
{:else if todos.error}<p>{todos.error.message}</p>
{:else}
  {#each todos.data ?? [] as todo}<p>{todo.title}</p>{/each}
{/if}
```

**Caveat**: the auto-cleanup only works inside a reactive scope (component setup, `$effect`, `$derived.by`). Calling `listTodos$()` from a module, a timer callback, or a one-shot function leaks the subscription — use `listTodosStore$()` and call `unsubscribe()` explicitly.

### Reactive Mutations

The `$()` form on a mutation (e.g. `createTodo$()`) returns a runes-backed handle.

```svelte
<script>
  import { createTodo$ } from '$lib/forge';
  const create = createTodo$();

  async function submit(title) {
    try { await create.mutate({ title }); }
    catch (e) { /* create.error already has it; handler runs onMutationError */ }
  }
</script>

<button disabled={create.pending} onclick={() => submit('New task')}>Add</button>
{#if create.error}<p class="err">{create.error.message}</p>{/if}
```

`ReactiveMutation<TArgs, TResult>` surface: `{ mutate(args): Promise<TResult>; pending: boolean; error: ForgeError | null }`. Never hand-roll a wrapper around the generated `Store$` / runes helpers — doing so reintroduces the lifecycle bugs the runes form fixes.

## App Setup

- Wrap the app in `ForgeProvider` in `+layout.svelte`. Pass `getToken` and `onMutationError`.
- Set `export const ssr = false;` in `+layout.ts`. SSE, `EventSource`, and `localStorage` aren't available server-side.

## Authentication and Session Management

Generated helper with a global `auth` object.

- `auth.setAuth(access, refresh, user)` — persist tokens and call `getForgeClient()?.reconnect()` so SSE re-subscribes under the new principal.
- `auth.clearAuth()` — clear storage and reconnect (anonymous).
- `auth.startRefreshLoop(url)` — rotates tokens before expiry; the client retries once on 401 after successful refresh (concurrent 401s coalesce on a single refresh).
- Never write to `localStorage` directly for auth. Bypassing `setAuth` / `clearAuth` leaves SSE on the old identity and serves stale or wrong data.

## Mutations — Two Idioms

```typescript
// 1. fireMutation: global error routing, no state
import { fireMutation } from '@forge-rs/svelte';
import { createTodo } from '$lib/forge';
fireMutation(createTodo, { title: 'New task' });

// 2. createTodo$(): runes-backed, local pending + error
const create = createTodo$();
await create.mutate({ title: 'New task' });
```

Use `$()` form when the UI needs per-button pending / error state. Use `fireMutation` for fire-and-forget actions where a global toast is enough.

## Optimistic Mutations

```typescript
const todos = listTodosStore$();
const reorder = createOptimisticMutation(reorderTask, todos, (data, args) =>
  data.map(t => t.id === args.id ? { ...t, ...args } : t)
);
// Read from reorder.data for UI. Patch auto-reverts on error or 3s TTL.
reorder.fire({ id, status: 'done' });
```

## Common Failure Cases

### Subscription inside `$derived` leaks

```svelte
<!-- WRONG — new subscription every time id changes -->
<script>
  const item = $derived(getItemStore$({ id: currentId }));
</script>

<!-- RIGHT — manage lifecycle via $effect -->
<script>
  let item = $state(null);
  let unsub;
  $effect(() => {
    unsub?.();
    const store = getItemStore$({ id: currentId });
    unsub = store.subscribe(v => { item = v; });
    return () => unsub?.();
  });
</script>
```

### Manual `localStorage` writes break SSE reconnect

```svelte
<!-- WRONG -->
<script>
  async function login(email, password) {
    const r = await signIn({ email, password });
    localStorage.setItem('token', r.access_token);  // bypasses auth store, SSE keeps the old identity
  }
</script>

<!-- RIGHT -->
<script>
  import { auth } from '$lib/forge/auth.svelte';
  async function login(email, password) {
    const r = await signIn({ email, password });
    auth.setAuth(r.access_token, r.refresh_token, r.user);
  }
</script>
```

### Swallowed mutation errors

```typescript
// WRONG — errors disappear
createTodo({ title });

// RIGHT — routes to onMutationError
fireMutation(createTodo, { title });

// Also RIGHT — local handling
try { await createTodo({ title }); } catch (e) { showToast(e.message); }
```

### Missing `ssr = false` crashes hydration

```typescript
// frontend/src/routes/+layout.ts
export const ssr = false;
```

## Hard Constraints

- Never edit `$lib/forge/*`.
- Never create a store inside `$derived` — use `$effect` with explicit cleanup.
- Never poll a reactive query — SSE handles updates.
- Always handle mutation errors (global `onMutationError` or local try/catch).
