# IPC: Commands, Events, and Channels

**Sources:**
- https://v2.tauri.app/concept/inter-process-communication/
- https://v2.tauri.app/develop/calling-rust/
- https://v2.tauri.app/develop/calling-frontend/
- https://docs.rs/tauri/latest/tauri/ipc/struct.Channel.html
- https://github.com/tauri-apps/tauri-docs/blob/v2/src/content/docs/concept/Inter-Process%20Communication/index.mdx

Tauri IPC has three distinct patterns. Pick the right one — most bugs come from using events where a command (or channel) was the right tool.

| Pattern | Direction | Shape | Use for |
|---|---|---|---|
| **Command** (`invoke`) | Frontend → Core, request/response | One call, one typed return (or error) | "Do X and give me the result" — the vast majority of interactions |
| **Event** (`emit`/`listen`) | Either direction, fire-and-forget | Named, unstructured broadcast | Lifecycle notifications, state-change pushes, one-to-many broadcast |
| **Channel** | Core → Frontend, streaming | Ordered stream of messages tied to one call | Progress updates, chunked/large data transfer, log tailing |

## Commands

A command is a plain Rust function annotated `#[tauri::command]`, registered via `tauri::generate_handler![...]`, and called from the frontend with `invoke()`.

```rust
// src-tauri/src/lib.rs
#[tauri::command]
fn greet(name: String) -> String {
    format!("Hello, {name}!")
}

#[tauri::command]
async fn save_file(path: String, contents: String) -> Result<(), String> {
    std::fs::write(&path, contents).map_err(|e| e.to_string())
}

pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet, save_file])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

```ts
// frontend
import { invoke } from "@tauri-apps/api/core";

const greeting = await invoke<string>("greet", { name: "Anjasta" });
await invoke("save_file", { path: "/tmp/out.txt", contents: "hi" });
```

Rules:
- Every parameter must implement `serde::Deserialize`; every return type must implement `serde::Serialize`. Tauri rejects the IPC call outright (before your function body runs) if arg names/types/counts don't line up with what the frontend sent — this is a real validation layer, not just documentation.
- Argument names are **camelCase on the JS side by default** even if the Rust parameter is `snake_case` (Tauri renames via serde). `save_file(path, contents)` in Rust is called as `invoke("save_file", { path, contents })` — matches here because both are already single words, but e.g. Rust `file_name: String` becomes JS `fileName`.
- Prefer `Result<T, E>` returns over panicking. A command that panics currently aborts the whole process in some configurations — always return `Result` for anything fallible, and implement `serde::Serialize` for your error type (or map to `String`).
- Use `async fn` for anything that does I/O, talks to another process, or **creates a window** (see SKILL.md rule 7 — sync window creation inside a command handler can deadlock on Windows/WebView2).

### Accessing app/window/state from a command

Commands can request special parameters by type — Tauri injects them, they don't need to be passed from JS:

```rust
use tauri::{AppHandle, State, Window};

#[tauri::command]
async fn do_thing(app: AppHandle, window: Window, state: State<'_, AppState>) -> Result<(), String> {
    // app: talk to the whole application (create windows, access resources)
    // window: the WebviewWindow that invoked this command
    // state: your managed state — see references/state-management.md
    Ok(())
}
```

## Events

Events are named, JSON-payload broadcasts. Either side can emit; either side can listen.

```rust
// Rust: emit to all windows
app.emit("progress", 42)?;

// Rust: emit to one window only
app.emit_to("main", "progress", 42)?;
```

```ts
// Frontend: listen
import { listen } from "@tauri-apps/api/event";

const unlisten = await listen<number>("progress", (event) => {
  console.log(event.payload); // 42
});
// call unlisten() when the component unmounts to avoid leaks
```

```ts
// Frontend: emit (e.g. window-to-window)
import { emit } from "@tauri-apps/api/event";
await emit("frontend-ready", { ok: true });
```

Global vs window-specific events: global events are app-wide lifecycle notifications; window events (resize, move, close-requested, focus) are scoped to one window and are what you get via `window.onCloseRequested(...)` etc. Prefer explicit named custom events for your own app logic over overloading window events.

**Always call the returned `unlisten` function** on component teardown — listeners otherwise accumulate across remounts (a very common React/Vue useEffect-cleanup miss).

## Channels — the v2 way to stream data

Added in Tauri v2 specifically to replace "emit hundreds of small events" for progress bars, log tails, and chunked downloads. A `Channel` is created per-call on the frontend, passed into the command like a normal argument, and the backend sends ordered messages through it.

```rust
use tauri::ipc::Channel;

#[derive(Clone, serde::Serialize)]
#[serde(tag = "event", content = "data")]
enum DownloadEvent {
    Started { content_length: u64 },
    Progress { chunk_length: usize },
    Finished,
}

#[tauri::command]
async fn download(url: String, on_event: Channel<DownloadEvent>) -> Result<(), String> {
    on_event.send(DownloadEvent::Started { content_length: 1000 }).unwrap();
    // ... stream chunks, calling on_event.send(DownloadEvent::Progress{..}) ...
    on_event.send(DownloadEvent::Finished).unwrap();
    Ok(())
}
```

```ts
import { invoke, Channel } from "@tauri-apps/api/core";

const onEvent = new Channel<DownloadEvent>();
onEvent.onmessage = (message) => {
  console.log(message); // tagged enum, matches Rust shape
};
await invoke("download", { url: "https://example.com/file", onEvent });
```

Use channels instead of events whenever the data is: (a) high-frequency, (b) tied to one specific call rather than global, or (c) must preserve strict ordering. This is also what plugin authors use for streaming plugin APIs (e.g. upload progress) — see `references/plugins-sidecar.md`.

## Frontend without a bundler (`window.__TAURI__`)

A loading page or `frontendDist` served plain HTML with no ESM imports must use the global:

```html
<script>
  const { core, event } = window.__TAURI__;
  await core.invoke("retry_launch");
  const unlisten = await event.listen("launch-error", ({ payload }) => { ... });
</script>
```

This **only works if `"app": {"withGlobalTauri": true}` is set in `tauri.conf.json`** — it's `false` by default in v2 (unlike v1). If `window.__TAURI__` is `undefined` in the webview console, check this first.

## Debugging checklist when `invoke()` "does nothing" or rejects

1. Is the command registered in `tauri::generate_handler![...]`? (No compile-time enforcement that it's wired up.)
2. Does the calling window's capability file grant permission for this command? → `references/security-capabilities.md`.
3. Do the JS argument names match the expected (camelCase) Rust parameter names exactly?
4. Is a `Result<T, E>` being returned as `Err` and swallowed on the frontend because the `.catch()`/`try` wasn't checked?
5. If called from a plain HTML page: is `withGlobalTauri` on, and are you using `window.__TAURI__.core.invoke` not `window.__TAURI__.invoke`?
