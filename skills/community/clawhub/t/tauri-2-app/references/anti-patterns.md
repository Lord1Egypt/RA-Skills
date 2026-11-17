# Anti-patterns

Each anti-pattern below was observed in a real Tauri 2 codebase. The "Why it's bad" explains the failure mode; "Fix" shows what to do instead.

## Committed `.backup` / `.orig` / `.temp` files

**Symptom:** Files like `src-tauri/src/lib.rs.backup`, `platform/macos.rs.orig`, `lib.rs.temp` checked into git.

**Why it's bad:** They're either WIP code paths that compile and silently win on some branch, or merge-conflict artefacts that obscure history. Either way they confuse `grep`, break `cargo build` with duplicate-definition errors, and leak unfinished implementations.

**Fix:** Add `*.backup`, `*.orig`, `*.temp`, `*.rej` to `.gitignore`. Delete every existing one. Use a VCS branch for WIP, not a sibling file.

## Plaintext API keys in `settings.json`

**Symptom:** `"openaiApiKey": "sk-proj-..."` in `settings.json`.

**Why it's bad:** Any process that can read the app's data directory (malware, backup-syncing services, a developer's grep) gets the key. App data directories are not encrypted on disk by default on any major OS.

**Fix:** Encrypt at rest. AES-256-GCM ciphertext + Argon2id-derived key + machine-bound salt. Store `EncryptedApiKey { ciphertext, nonce, salt }`. Auto-migrate legacy plaintext keys on load (log a warning, encrypt, save).

## Tokens in `localStorage` / `sessionStorage`

**Symptom:** Frontend stores auth tokens via `localStorage.setItem("token", ...)`.

**Why it's bad:** Any XSS-equivalent path in the WebView reads them. Tauri's WebView is sandboxed from arbitrary websites, but extension content scripts, embedded WebViews, or future bundled JS dependencies can still touch `localStorage`.

**Fix:** Store secrets in Rust-side encrypted storage. Frontend asks the backend for tokens only when needed (e.g. for an outbound request). Better: have the backend make the outbound request and return the result.

## `cfg!(target_os = "...")` in command bodies

**Symptom:**

```rust
#[tauri::command]
pub fn open_settings(path: &str) -> Result<(), String> {
    if cfg!(target_os = "macos") {
        std::process::Command::new("open").arg(path).spawn()...
    } else if cfg!(target_os = "windows") {
        std::process::Command::new("explorer").arg(path).spawn()...
    } else {
        std::process::Command::new("xdg-open").arg(path).spawn()...
    }
}
```

**Why it's bad:** Every command grows the branch count. Tests need to mock the OS. Platform-specific dependencies leak into shared code. Adding a fourth OS means editing every command.

**Fix:** Define a trait in `platform/traits.rs`. Implement it per-OS in `platform/macos.rs` etc., each gated with `#[cfg(target_os = "...")]`. Inject the impl via Tauri State.

```rust
#[tauri::command]
pub fn open_settings(
    opener: tauri::State<'_, PlatformFileOpener>,
    path: String,
) -> Result<(), String> {
    opener.open_in_default_app(Path::new(&path))
}
```

## Hand-rolled date / leap-year math

**Symptom:**

```rust
fn get_timestamp() -> String {
    let now = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_secs();
    let days_since_epoch = now / 86400;
    // ... 50 lines of leap-year arithmetic ...
}
```

**Why it's bad:** Boundary bugs are inevitable. Daylight savings, leap seconds, leap years on century boundaries, year-2038 — every special case is a future fire. The "I'll skip the dep" instinct loses to the dependency every time.

**Fix:**

```rust
use chrono::Utc;

fn get_timestamp() -> String {
    Utc::now().to_rfc3339()  // "2026-01-15T10:30:00+00:00"
}

fn parse_timestamp(s: &str) -> Option<chrono::DateTime<chrono::Utc>> {
    chrono::DateTime::parse_from_rfc3339(s).ok().map(|dt| dt.with_timezone(&Utc))
}
```

## Raw `std::fs::write(&user_supplied_path, ...)` in commands

**Symptom:**

```rust
#[tauri::command]
pub fn save_file(path: String, content: String) -> Result<(), String> {
    std::fs::write(&path, content).map_err(|e| e.to_string())
}
```

**Why it's bad:** Bypasses Tauri's capability system. A misconfigured frontend can ask the command to overwrite `~/.ssh/authorized_keys` or `/etc/hosts`. The whole point of capabilities is to gate dangerous APIs.

**Fix:** Either route through `tauri-plugin-fs` (which respects `fs:scope-*` capability scopes), or restrict raw I/O to paths derived from `app_handle.path().app_data_dir()`.

```rust
#[tauri::command]
pub fn save_app_data(
    app: AppHandle,
    filename: String,
    content: String,
) -> Result<(), String> {
    let path = crate::storage::get_storage_path(&app, &filename)?;
    std::fs::write(&path, content).map_err(|e| e.to_string())
}
```

For user-chosen paths (export, save-as), use the dialog plugin to ask the user, **then** write to the path they explicitly picked.

## Blocking I/O inside async commands without `spawn_blocking`

**Symptom:**

```rust
#[tauri::command]
pub async fn pick_file(app: AppHandle) -> Result<Option<String>, String> {
    let path = app.dialog().file().blocking_pick_file();  // BLOCKS the executor
    Ok(path.map(|p| p.to_string()))
}
```

**Why it's bad:** Tauri's IPC commands share an executor. A blocked task stalls every other in-flight command. Users see "the app froze" while one command pretends to be async.

**Fix:**

```rust
#[tauri::command]
pub async fn pick_file(app: AppHandle) -> Result<Option<String>, String> {
    let handle = app.clone();
    let path = tokio::task::spawn_blocking(move || {
        handle.dialog().file().blocking_pick_file()
    })
    .await
    .map_err(|e| format!("Join error: {}", e))?;
    Ok(path.map(|p| p.to_string()))
}
```

## Holding `std::sync::Mutex` across `.await`

**Symptom:**

```rust
let guard = state.lock().map_err(|e| e.to_string())?;
let result = some_async_fn(&guard).await?;  // 💥 blocks executor + deadlock risk
```

**Why it's bad:** `std::sync::Mutex` is not `Send`-aware in the async sense. The compiler may even refuse to compile this if the future crosses thread boundaries. When it does compile, you can deadlock the runtime: thread holds the lock, awaits a future scheduled on the same thread, future needs the lock.

**Fix:** Read what you need from the guard, drop the guard, then await.

```rust
let snapshot = {
    let guard = state.lock().map_err(|e| e.to_string())?;
    guard.settings.clone().ok_or("not loaded")?
};
let result = some_async_fn(&snapshot).await?;
```

If genuinely shared mutable state must persist across awaits, use `tokio::sync::Mutex` and call `.lock().await` instead.

## Missing `windows_subsystem = "windows"`

**Symptom:** `main.rs` lacks `#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]`.

**Why it's bad:** Windows release builds open a console window behind the Tauri window. Looks unprofessional and adds a process that can't be cleanly closed without killing the app.

**Fix:** Add the attribute as the **first line** of `main.rs`. Debug builds keep their console (useful for `println!` during development).

## No `tauri-plugin-single-instance`

**Symptom:** App allows multiple concurrent launches.

**Why it's bad:** Both instances fight for the global hotkey (one wins, the other silently registers nothing). Both try to bind the same lock files / WebSocket port. Audio device reservation may pick the wrong instance. Settings written by one are clobbered by the other.

**Fix:** Wire `tauri-plugin-single-instance` **first** in the builder chain. On second launch, focus the existing window:

```rust
.plugin(tauri_plugin_single_instance::init(|app, _args, _cwd| {
    if let Some(w) = app.get_webview_window("main") {
        let _ = w.show();
        let _ = w.set_focus();
        let _ = w.unminimize();
    }
}))
```

## `devtools: true` in production `tauri.conf.json`

**Symptom:**

```json
"windows": [{ "devtools": true }]
```

**Why it's bad:** Ships an inspect-element / network-tab surface to every user. They can read the app's state, mutate it, and reverse-engineer internal APIs trivially. Even when the app is open-source, it makes accidental data exposure easier (anyone debugging a friend's app sees their notes).

**Fix:** Omit the field (Tauri defaults to off in release) or gate via a feature flag. If you need DevTools in a built debug binary, use `#[cfg(debug_assertions)]` to open them programmatically in `.setup()`.

## Blanket capability permissions

**Symptom:**

```json
"permissions": ["core:default", "fs:default", "dialog:default"]
```

… without listing the specific scopes the app uses.

**Why it's bad:** Capability files are the audit surface for what the frontend can ask Rust to do. Blanket `default` permissions vary across plugin versions — an update can silently widen what the frontend can call.

**Fix:** List exactly the action scopes used:

```json
"permissions": [
  "core:default",
  "fs:allow-read-file",
  "fs:allow-write-file",
  "dialog:allow-open",
  "dialog:allow-save"
]
```

## CSP `null` without explanation

**Symptom:**

```json
"app": { "security": { "csp": null } }
```

**Why it's bad:** Disables every Content Security Policy protection in the WebView. Any script the WebView fetches (intentional or injected) runs with full access. CSP `null` may be necessary for some apps (e.g. those that load remote content), but it should be a documented decision.

**Fix:** Set an explicit CSP that whitelists `tauri://localhost` plus any external origins the app legitimately uses. If `null` is required, add a comment in `tauri.conf.json` (JSON doesn't support comments — put it in `CLAUDE.md` or `README.md`) explaining why.

## Bundling external binaries without listing them

**Symptom:** App calls `Command::new("ffmpeg")` but `ffmpeg` is not in `tauri.conf.json` `bundle.externalBin`.

**Why it's bad:** Works in `cargo run` (PATH finds the system ffmpeg) but the installer doesn't include the binary. Users get a "binary not found" error in production.

**Fix:**

```json
"bundle": {
  "externalBin": ["binaries/ffmpeg"]
}
```

Place the per-platform binary at `binaries/ffmpeg-<target-triple>` (e.g. `ffmpeg-aarch64-apple-darwin`). Tauri's bundler picks the right one per build target.

## macOS `Info.plist` missing usage descriptions

**Symptom:** App calls `AVAudioSession.requestRecordPermission` but `Info.plist` lacks `NSMicrophoneUsageDescription`.

**Why it's bad:** macOS refuses the permission prompt silently — the call returns "denied" without showing the user a dialog. The user has no idea the app needs the mic.

**Fix:** For every OS-level permission the app requests, add a usage description string explaining *why*:

```xml
<key>NSMicrophoneUsageDescription</key>
<string>This app needs the microphone to record voice input.</string>
<key>NSAccessibilityUsageDescription</key>
<string>This app needs Accessibility access to insert text into other windows.</string>
```

## Over-broad macOS entitlements

**Symptom:** `entitlements.plist` has `com.apple.security.cs.allow-jit` and `com.apple.security.cs.allow-unsigned-executable-memory` enabled by default.

**Why it's bad:** These weaken the hardened runtime. Apple's notarization service will reject them if they're not justified; if accepted, they expand the attack surface (allowing JIT means write+execute pages are possible).

**Fix:** Start with an empty entitlements file. Add entitlements only when a build failure or runtime error proves you need them. Common minimally-required entitlements:

- `com.apple.security.device.audio-input` — microphone access
- `com.apple.security.automation.apple-events` — sending Apple events (e.g. for keystroke insertion)

Never copy a full entitlements file from another project — audit each line.

## Two `[[bin]]` entries in one crate

**Symptom:**

```toml
[[bin]]
name = "myapp"
path = "src/main.rs"

[[bin]]
name = "myapp-sidecar"
path = "src/sidecar/main.rs"
```

**Why it's bad:** Both binaries pull the full Tauri dependency tree (compile time, binary size). Conditional compilation gets tangled. Cross-compilation for different targets per binary is awkward. The "sidecar" pattern in Tauri usually means a separate process — that separate process deserves a separate crate.

**Fix:** Use a Cargo workspace:

```
src-tauri/
  Cargo.toml            # workspace root
  app/
    Cargo.toml          # main app crate
    src/main.rs
  sidecar/
    Cargo.toml          # sidecar crate (no Tauri dep)
    src/main.rs
```

If you genuinely need only one extra bin with no Tauri deps, a single workspace with two crates is still cleaner than two `[[bin]]` entries fighting over shared deps.

## Multiple `createRoot()` calls

**Symptom:** `main.tsx` calls `createRoot(...)` more than once, or renders before the DOM root exists.

**Why it's bad:** React 18+'s strict mode hates multiple roots on the same node. Hydration warnings, "Cannot update a component while rendering" errors.

**Fix:** One entry point. Look up the root once. Render once.

```ts
// src/main.tsx
const rootElement = document.getElementById("app");
if (rootElement) {
  createRoot(rootElement).render(<App />);
}
```

## Inline `invoke()` calls in components

**Symptom:**

```tsx
function MyComponent() {
  const [data, setData] = useState(null);
  useEffect(() => {
    invoke('get_settings').then(setData).catch(console.error);
  }, []);
  // ...
}
```

**Why it's bad:** Every component reinvents loading/error handling. Refactoring a command name means grepping every file. Type safety dies — `data` is `any`.

**Fix:** Use `useTauriCommand<T>`. Per-domain hooks compose it:

```ts
// hooks/useSettings.ts
export function useSettings() {
  return useTauriLoad<Settings>({ command: "get_settings" });
}
```

```tsx
function MyComponent() {
  const { data: settings, isLoading, error } = useSettings();
  // ...
}
```

## Hardcoded user-specific config in templates

**Symptom:** A scaffold writes `"identifier": "com.acme.myapp"`, `"endpoints": ["https://cdn.example.com/manifest.json"]`, or any non-empty `"pubkey": "..."` value copied from a previous project.

**Why it's bad:** Bundle identifiers are immutable user-facing IDs (OS-level keychain, settings paths, notification permissions are all keyed on them — changing one is migration pain forever). Updater pubkeys lock the app's update channel to whoever holds the matching private key. R2/S3 URLs leak previous customers.

**Fix:** Ask the user for these values. Refuse to scaffold if they're missing or look like placeholders. Never copy them from another project.

## `.env` committed to git

**Symptom:** `.env` shows up in `git ls-files`.

**Why it's bad:** Credentials, API keys, signing certificate paths leak. GitHub scans for known token formats and may auto-revoke them — better than leaving them live, but disruptive.

**Fix:** Only `.env.example` is committed (keys only, no values). `.env` is in `.gitignore`. If `.env` was ever committed, rotate the secrets immediately — git history retains them even after deletion.

## Silent error swallowing

**Symptom:**

```rust
let _ = some_operation();
// or
if let Err(_) = some_operation() {}
```

**Why it's bad:** A future bug surfaces as "the app does nothing" with no log line to find it from. Months later, you're stepping through a debugger trying to find which silent failure broke the flow.

**Fix:** Either handle the error meaningfully or log it:

```rust
if let Err(e) = some_operation() {
    tracing::warn!("some_operation failed: {}", e);
}
```

Use `tracing::error!` for errors that should page someone, `warn!` for "something went wrong but we recovered", `info!` for normal-path state changes, `debug!` for diagnostic detail.

## Heavy startup work blocks the window

**Symptom:**

```rust
.setup(|app| {
    let model = load_huge_ml_model()?;  // 5 seconds
    let devices = enumerate_audio_devices()?;  // 2 seconds
    // ... window appears after 7+ seconds
    Ok(())
})
```

**Why it's bad:** Users see a missing window for seconds and assume the app crashed.

**Fix:** Show the window first (Tauri does this by default — don't `.hide()` it). Move heavy work to a background thread that emits events back to the frontend:

```rust
.setup(|app| {
    let handle = app.handle().clone();
    std::thread::spawn(move || {
        match load_huge_ml_model() {
            Ok(_) => { let _ = handle.emit("model-ready", ()); }
            Err(e) => { let _ = handle.emit("model-error", e.to_string()); }
        }
    });
    Ok(())
})
```

The frontend renders a "Loading model…" state until it receives `model-ready`.
