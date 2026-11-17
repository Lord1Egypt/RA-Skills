# State Management

**Sources:**
- https://v2.tauri.app/develop/state-management/
- https://github.com/tauri-apps/tauri-docs/blob/v2/src/content/docs/develop/state-management.mdx
- https://docs.rs/tauri/latest/tauri/trait.Manager.html
- https://v2.tauri.app/develop/calling-rust/ (state access from commands)

Tauri's state system lets you register any `Send + Sync + 'static` Rust value once and retrieve it from any command, any thread with an `AppHandle`, and any lifecycle hook — without manually threading it through function signatures.

## Basic pattern

```rust
use std::sync::Mutex;
use tauri::{Builder, Manager};

#[derive(Default)]
struct AppState {
    counter: u32,
}

pub fn run() {
    Builder::default()
        .setup(|app| {
            app.manage(Mutex::new(AppState::default()));
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![increment])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

#[tauri::command]
fn increment(state: tauri::State<'_, Mutex<AppState>>) -> u32 {
    let mut state = state.lock().unwrap();
    state.counter += 1;
    state.counter
}
```

- `app.manage(value)` registers `value` under its concrete type. You can `manage()` as many distinct types as you want; each is retrieved independently.
- `tauri::State<'_, T>` in a command signature is auto-injected by Tauri — it is **not** passed from the frontend and should not appear in the JS `invoke()` call's argument object.
- **You do not need to wrap the managed value in `Arc` yourself** for `State` to be usable across threads/commands — Tauri's state container already handles shared ownership internally. Wrapping in `Arc<Mutex<T>>` on top is redundant unless you're independently sharing a clone of the *inner* `Arc` outside of Tauri's state system (e.g. handing a clone to a spawned background task that runs detached from any command).
- What you generally **do** need is interior mutability, since managed state is otherwise immutable through the shared reference: `Mutex<T>` or `RwLock<T>` for sync code, `tokio::sync::Mutex<T>` if you need to hold the guard across an `.await` point (a `std::sync::Mutex` guard is not `Send` across await points and won't compile in that position).

## Multiple state types

```rust
struct Storage { store: Mutex<HashMap<u64, String>> }
struct DbConnection { db: Mutex<Option<Connection>> }

tauri::Builder::default()
    .manage(Storage { store: Default::default() })
    .manage(DbConnection { db: Default::default() })
    .invoke_handler(tauri::generate_handler![connect, storage_insert])
    .run(tauri::generate_context!())
    .expect("error while running tauri application");

#[tauri::command]
fn connect(connection: tauri::State<'_, DbConnection>) {
    *connection.db.lock().unwrap() = Some(Connection {});
}

#[tauri::command]
fn storage_insert(key: u64, value: String, storage: tauri::State<'_, Storage>) {
    storage.store.lock().unwrap().insert(key, value);
}
```

Mutations happen through interior mutability on the managed struct's fields (`Mutex`/`RwLock`/`AtomicX`), not by reassigning the whole managed value — `state()`/`State<T>` gives you a shared reference, never `&mut T`.

## Accessing state outside a command (e.g. from `setup`, a spawned thread, an event handler)

```rust
.setup(|app| {
    app.manage(Mutex::new(AppState::default()));
    let state: tauri::State<Mutex<AppState>> = app.state();
    // ...
    Ok(())
})
```

From inside a spawned thread that only has an `AppHandle` (not an `App`/`Window` with a convenient lifetime), retrieve state the same way — `AppHandle` also implements `Manager`:

```rust
let handle = app.handle().clone(); // AppHandles are cheap to clone
std::thread::spawn(move || {
    let state = handle.state::<Mutex<AppState>>();
    let mut s = state.lock().unwrap();
    s.counter += 1;
});
```

If `State<'_, T>`'s lifetime bound doesn't fit where you need to move it (e.g. into a thread closure with `'static`), move an `AppHandle` into the closure instead and call `.state::<T>()` inside it, as above — this sidesteps the lifetime issue entirely.

## Panics vs `try_state`

- `app.state::<T>()` / `State<T>` extraction **panics** if `T` was never `manage()`d. This is a programmer error class (forgot to call `.manage()`), not a runtime condition — let it panic in development so you catch the wiring bug immediately.
- Use `app.try_state::<T>()` (returns `Option<State<T>>`) only where "may or may not have been managed yet" is a genuine runtime possibility (e.g. optional plugin state, conditionally-initialized subsystems), not as a substitute for correctly wiring `.manage()` at startup.

## Sync vs async lock choice — decision guide

| Situation | Use |
|---|---|
| Command is sync `fn`, lock held briefly, no `.await` while holding it | `std::sync::Mutex<T>` (cheapest, no runtime dependency) |
| Command is `async fn` but never `.await`s while the guard is alive (lock, mutate, drop before any await) | `std::sync::Mutex<T>` is still fine |
| Command is `async fn` and needs to `.await` something (e.g. a DB call) **while holding the lock** | `tokio::sync::Mutex<T>` (or restructure to drop the guard before awaiting — usually the better fix) |
| Many concurrent readers, occasional writer | `std::sync::RwLock<T>` (or `tokio::sync::RwLock` under the same await-holding rule) |
| Simple counters/flags | `std::sync::atomic::{AtomicU32, AtomicBool, ...}` — avoids lock overhead entirely |

Default to `std::sync::Mutex` and only reach for the `tokio` variants when the compiler actually forces you to (a `MutexGuard` held across `.await` fails to compile because it isn't `Send`) — this keeps the common case simple and avoids the (real, if usually small) overhead of async-aware locking everywhere.

## Unmanaging state

There's no built-in "unmanage" API. If you genuinely need to drop/replace managed state at runtime, wrap it so the *content* can be swapped out: `Mutex<Option<T>>`, and use `Option::take()` to remove it. Don't try to fight the framework here — this is the documented workaround, not a hack.

## Frontend-mirrored state (cross-window sync)

State managed in Rust is invisible to the frontend unless you explicitly expose it — either via a `get_state` command the frontend polls/calls on mount, or by having Rust `emit` a state-changed event (see `references/ipc-commands.md`) whenever it mutates, with every window listening and updating its own local store (Zustand/Redux/Pinia/whatever). There is no automatic two-way binding; design the sync direction deliberately:

- **Rust is source of truth** (most common for anything that must survive window creation/destruction, e.g. app settings, DB connections): frontend sends action → command mutates state → command (or the mutation itself) emits a state-changed event to all windows → each window's local store updates from the payload.
- **Frontend is source of truth, Rust just persists it**: simpler, but means Rust-side commands can't rely on reading current UI state without an explicit round-trip.

Pick one direction per piece of state and be consistent — mixing "sometimes Rust pushes, sometimes frontend polls" for the same value is a common source of stale-UI bugs across multiple windows.
