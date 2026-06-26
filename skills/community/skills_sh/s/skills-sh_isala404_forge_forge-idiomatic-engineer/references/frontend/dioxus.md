# Dioxus Reference

Project signature: `frontend/Cargo.toml` with `dioxus` + a `frontend/src/forge/` dir. See the shared rules in [frontend.md](../frontend.md).

## Generated APIs

For a backend query `get_user(ctx, id: Uuid)`:

| Export | Returns | Use for |
|---|---|---|
| `get_user(client, args)` | `Result<T, E>` | One-shot async. |
| `use_get_user(args)` | `QueryState<T>` | Fetch-once hook. |
| `use_get_user_live(args)` | `SubscriptionState<T>` | SSE-backed live subscription. |

For mutations / jobs / workflows:
- `use_create_user()` → `Mutation<P, T>` handle. `.call(params).await` for manual control, `.fire(params)` / `.fire_with(params, |err| ...)` for fire-and-forget with error routing.
- `use_send_email(args)` → `JobExecutionState<T>`.
- `use_onboard_user(args)` → `WorkflowExecutionState<T>`.

## App Setup

- `ForgeProvider` for unauthenticated apps.
- `ForgeAuthProvider` when you need sessions — manages token storage (localStorage on web, filesystem on native), refresh, and auto-recovery from 401.
- Read state with `use_forge_auth()`.
- Configure a `refresh_token` provider on the client with `.with_refresh_token_provider(|refresh| async { ... })` so 401s trigger a single coalesced refresh + retry.

## Platform Requirements

- **WASM**: native `EventSource`, token passed via `?token=…` query param.
- **Native**: `reqwest-eventsource`, token via `Authorization` header. Configure `reqwest` with `rustls-tls` on non-WASM targets.

## Mutations

```rust
let create = use_create_user();

// Fire-and-forget with global error routing
create.fire(Args { name: "Alice".into() });

// Local error handling
create.fire_with(Args { ... }, |err| tracing::error!(?err));

// Manual await
spawn(async move {
    match create.call(Args { ... }).await {
        Ok(user) => { ... }
        Err(e) => { ... }
    }
});
```

**Never read signals inside `spawn`** — the component may unmount before the future resolves and the read will panic. Clone first.

```rust
// WRONG
spawn(async move { let id = some_signal.read().id; create.call(Args { id }).await; });

// RIGHT
let id = some_signal.read().id;
spawn(async move { create.call(Args { id }).await; });
```

`.fire()` sidesteps this entirely — prefer it unless you need the awaited result.

## Keyed Remount on Auth Change

**Required.** Without it, stores from the previous user bleed into the new session.

```rust
fn AppShell() -> Element {
    let auth_key = use_auth_key();
    rsx! {
        main {
            key: "{auth_key}",
            Router::<Route> {}
        }
    }
}
```

## Optimistic Updates

```rust
let tasks_sub = use_list_tasks_live_signal();
let reorder = use_optimistic(use_reorder_task(), tasks_sub, |tasks, args| {
    // return modified Vec
});
// Read from reorder.data() — the merged server + local state.
reorder.fire(args);
```

Auto-reverts on server error or default 3s TTL.

## Common Failure Cases

### `use_*_live` inside a loop opens N subscriptions

```rust
// WRONG
for id in &ids { let item = use_get_item_live(GetItemArgs { id: *id }); }

// RIGHT
let items = use_list_items_live(ListItemsArgs { ids: ids.clone() });
```

### Reading the wrong source for optimistic state

```rust
// WRONG — unpatched
rsx! { for task in tasks.read().data { ... } }

// RIGHT
rsx! { for task in reorder.data() { ... } }
```

## Hard Constraints

- Never edit `frontend/src/forge/*`.
- Never fetch inside `use_effect` — races and leaks. Use subscription hooks.
- Never use an authenticated `ForgeClient` for token refresh — the server rejects the expired token header. The built-in provider creates an anonymous client for refresh.
- Missing `use_auth_key()` is a data leak, not a visual glitch.
