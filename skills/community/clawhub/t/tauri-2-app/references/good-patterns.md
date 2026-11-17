# Good Patterns

The patterns below survived real production use. Each one has a failure mode it prevents — the rationale matters more than the rule.

## Architecture

### Thin frontend, rich Rust backend

All audio, file I/O, system permissions, OS-specific behavior, and long-running computation lives in Rust. The frontend's only job is to invoke commands and render state.

**Why:** Tauri's selling point over Electron is performance and OS integration. Pushing work into the frontend reintroduces the same memory and startup costs you came to Tauri to avoid. It also makes the frontend untestable without a running Tauri instance.

**How to spot violations:**
- `import { open } from '@tauri-apps/plugin-fs'` in component code reading large files
- Frontend code parsing/processing audio buffers
- `setInterval` polling driving state that could be event-driven from Rust via `app.emit("...", payload)`

### Modular `src-tauri/src/`

One module per concern (`commands/`, `state/`, `storage/`, `platform/`, `settings/`, `error/`, plus per-feature folders). `lib.rs` re-exports a public API for tests and registers commands; `main.rs` is the tiny shim that calls `pub fn run()`.

**Why:** A monolithic `lib.rs` past ~1500 lines is unmaintainable. Splitting by feature lets `cargo test --test <feature>` target one slice and surfaces accidental cross-cutting dependencies.

### Trait-based platform abstractions

`platform/traits.rs` defines `PermissionChecker`, `FileOpener`, `AutostartManager`, etc. `platform/macos.rs|windows.rs|linux.rs` implement them gated with `#[cfg(target_os = "...")]`. Wrappers in `platform/wrappers.rs` implement `Send + Sync` and are managed in Tauri State.

**Why:** Without this, `cfg!(target_os = "...")` checks scatter through command bodies, untestable and tedious to audit. The trait gives one place to swap behavior per OS and a clean seam for mocking in tests.

```rust
// platform/traits.rs
pub trait PermissionChecker: Send + Sync {
    fn check_microphone(&self) -> bool;
    fn check_accessibility(&self) -> bool;
    fn open_system_settings(&self, kind: &str) -> Result<(), String>;
}
```

```rust
// platform/wrappers.rs
pub struct PlatformPermissionChecker {
    #[cfg(target_os = "macos")] inner: crate::platform::MacOsPlatform,
    #[cfg(target_os = "windows")] inner: crate::platform::WindowsPlatform,
    #[cfg(target_os = "linux")] inner: crate::platform::LinuxPlatform,
}
```

## Tauri runtime

### Single-instance plugin first

```rust
tauri::Builder::default()
    .plugin(tauri_plugin_single_instance::init(|app, _args, _cwd| {
        if let Some(window) = app.get_webview_window("main") {
            let _ = window.show();
            let _ = window.set_focus();
            let _ = window.unminimize();
        }
    }))
    .plugin(tauri_plugin_opener::init())
    // ...
```

**Why:** Without single-instance, double-clicking the launcher spawns a second process that competes for the global hotkey, the audio device, the lock file, and the WebSocket. The plugin must register **first** so the second instance is intercepted before any other plugin initializes resources.

### `#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]` in `main.rs`

```rust
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

#[cfg(target_os = "macos")]
embed_plist::embed_info_plist!("../Info.plist");

fn main() { {{app_name}}_lib::run() }
```

**Why:** Without it, Windows release builds open a console window behind the Tauri window. With it, debug builds still get a console (useful for `println!` while developing) and release builds are clean.

`embed_plist` ensures macOS standalone binaries (not run via `.app` bundle) still carry their plist.

### Show window FIRST in `.setup()`

```rust
.setup(|app| {
    let main_window = app.get_webview_window("main").unwrap();
    // (window is already visible by default — don't .hide() it)

    // Reset any stuck state from a previous run (force-quit / crash)
    crate::jobs::clear_stuck_job_state();

    // Now do heavy initialization on a background thread
    let handle = app.handle().clone();
    std::thread::spawn(move || {
        // model load, audio device enumeration, etc.
        // emit events back: handle.emit("init-progress", ...);
    });

    Ok(())
})
```

**Why:** Users perceive a Tauri app as broken if the window doesn't appear within ~500ms. Synchronous setup work (model loading, device enumeration, network calls) blocks the window from drawing.

### Reset state on startup

```rust
// In .setup(), before any "ready" event:
let was_in_progress = crate::jobs::has_running_job();
crate::jobs::clear_stuck_job_state();
if was_in_progress {
    tracing::warn!("Cleared stuck state from previous session (app likely force-quit)");
}
```

**Why:** Crashes and force-quits leave `static` / global state in odd places. Treating startup as recovery makes the app robust to ungraceful shutdowns.

## Commands

### `#[tauri::command]` shape

```rust
#[tauri::command]
pub async fn save_user_setting(
    state: State<'_, std::sync::Mutex<AppState>>,
    app_handle: AppHandle,
    key: String,
    value: String,
) -> Result<(), String> {
    // Hold the lock for the minimum time
    let mut settings = {
        let guard = state.lock().map_err(|e| e.to_string())?;
        guard.settings.clone().ok_or("settings not loaded")?
    };

    settings.set(&key, &value);

    // Persist outside the lock
    crate::settings::save_settings(&app_handle, &settings)?;

    // Re-take the lock to commit the in-memory copy
    state.lock().map_err(|e| e.to_string())?.settings = Some(settings);

    Ok(())
}
```

**Why:** Holding `std::sync::Mutex` across `.await` deadlocks the Tauri runtime. Clone what you need, drop the guard, do the work, re-take the guard to commit.

### `spawn_blocking` for sync work inside async commands

```rust
#[tauri::command]
pub async fn open_file_dialog(app: AppHandle) -> Result<Option<String>, String> {
    let app_handle = app.clone();
    let path = tokio::task::spawn_blocking(move || {
        app_handle
            .dialog()
            .file()
            .add_filter("Audio", &["mp3", "wav"])
            .blocking_pick_file()
    })
    .await
    .map_err(|e| format!("Join error: {}", e))?;

    Ok(path.map(|fp| fp.to_string()))
}
```

**Why:** `blocking_pick_file()` blocks the calling thread. Awaiting it inside an `async fn` stalls Tauri's IPC executor and any other in-flight command queues up.

### Error conversion at the IPC boundary

```rust
// error/mod.rs
#[macro_export]
macro_rules! into_string_err {
    ($expr:expr) => { $expr.map_err(|e| e.to_string()) };
    ($expr:expr, $msg:expr) => { $expr.map_err(|e| format!("{}: {}", $msg, e)) };
}

pub trait ResultExt<T, E>: Sized {
    fn into_string(self) -> Result<T, String>;
    fn into_string_msg(self, msg: &str) -> Result<T, String>;
}

impl<T, E: std::fmt::Display> ResultExt<T, E> for Result<T, E> {
    fn into_string(self) -> Result<T, String> { self.map_err(|e| e.to_string()) }
    fn into_string_msg(self, msg: &str) -> Result<T, String> {
        self.map_err(|e| format!("{}: {}", msg, e))
    }
}
```

```rust
// commands/<domain>.rs
use crate::error::ResultExt;

#[tauri::command]
pub fn write_file(path: String, content: String) -> Result<(), String> {
    std::fs::write(&path, content).into_string_msg("Failed to write file")
}
```

**Why:** Tauri commands must return `Result<T, String>` because the error crosses an IPC boundary. Internal APIs use `thiserror` enums for type safety. The macro / trait keeps the conversion one-line at the boundary.

## State & storage

### Shared `AppState` managed in a `Mutex`

```rust
// state/mod.rs
pub struct AppState {
    pub app_handle: Option<AppHandle>,
    pub settings: Option<Settings>,
    // domain-specific managers
}

// lib.rs, inside .setup():
let state = std::sync::Mutex::new(AppState::new());
app.manage(state);
```

**Why:** Tauri's `State<T>` is a managed singleton accessible from every command. Using `std::sync::Mutex` (not `tokio::sync::Mutex`) is fine **as long as** you never hold the lock across an `.await` — which is the pattern enforced above.

### Settings with serde camelCase + migrations

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase", default)]
pub struct Settings {
    pub default_export_dir: Option<String>,
    pub launch_at_login: bool,
    pub theme: String,
    // ...
}
```

**Why:**
- `rename_all = "camelCase"` matches frontend naming, no manual key remapping.
- `default` on the struct makes every field optional — old settings files load with sensible fallbacks for new fields.
- Add migration logic in a `deserialize_settings(&Value)` pass for non-trivial shape changes (e.g. `"English"` → `"en"`).

### Shared storage utilities

```rust
// storage/mod.rs
pub fn get_app_data_dir(app: &AppHandle) -> Result<PathBuf, String> {
    let dir = app.path().app_data_dir().map_err(|e| e.to_string())?;
    fs::create_dir_all(&dir).map_err(|e| e.to_string())?;
    Ok(dir)
}

pub fn load_json<T: serde::de::DeserializeOwned>(
    app: &AppHandle, filename: &str,
) -> Vec<T> { /* read or return empty */ }

pub fn save_json<T: serde::Serialize>(
    app: &AppHandle, filename: &str, entries: &[T],
) -> Result<(), String> { /* serialize + write */ }
```

**Why:** Every persistent feature (settings, history, error log) needs the same primitives. Centralizing them ensures one consistent failure mode (empty on missing file, log + empty on parse error) and one place to add cache/locking later.

## Security

### Encrypted secrets at rest

```rust
// encryption/mod.rs
#[derive(Serialize, Deserialize)]
pub struct EncryptedApiKey {
    pub ciphertext: String,  // base64 AES-256-GCM ciphertext
    pub nonce: String,       // base64 12-byte nonce
    pub salt: String,        // base64 Argon2id salt
}

pub fn encrypt_api_key(plaintext: &str) -> Result<EncryptedApiKey, String> { /* ... */ }
pub fn decrypt_api_key(enc: &EncryptedApiKey) -> Result<String, String> { /* ... */ }
```

The key is derived from a hardware-bound machine ID:
- macOS: `IOPlatformUUID` via `ioreg -rd1 -c IOPlatformExpertDevice`
- Windows: `wmic csproduct get uuid` (use `creation_flags(CREATE_NO_WINDOW)` to avoid a flashing console)
- Linux: `/etc/machine-id` or the `machine-uid` crate

**Why:** Plaintext API keys in `settings.json` is a known liability. AES-GCM gives authenticated encryption; Argon2id is memory-hard against GPU brute-force; hardware-binding means a stolen `settings.json` file alone isn't useful — the attacker needs the machine too.

Note: this is **at-rest** protection, not perfect security. A privileged process on the same machine can still decrypt. For higher assurance, integrate the OS keychain (macOS Keychain via `security-framework`, Windows DPAPI, Linux Secret Service).

### Granular capability scopes

```json
// capabilities/default.json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "description": "Capability for the main window",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "opener:default",
    "opener:allow-open-url",
    "dialog:allow-save",
    "dialog:allow-open",
    "fs:allow-write-file",
    "fs:allow-read-file",
    "notification:default",
    "notification:allow-show",
    "global-shortcut:allow-register",
    "global-shortcut:allow-unregister",
    "process:allow-restart",
    "updater:default"
  ]
}
```

**Why:** Listing exactly what the app uses (not blanket `"*"` or `"core:*"`) means the security audit surface is the capability file. If a plugin update adds new permissions, your app doesn't silently inherit them.

## Cargo

### Release profile

```toml
[profile.release]
lto = "fat"
codegen-units = 1
opt-level = 3
strip = true
panic = "abort"

[profile.dev]
opt-level = 1   # Faster dev builds while keeping some optimization
```

**Why:**
- `lto = "fat"` + `codegen-units = 1` = full whole-program optimization, smaller and faster binaries.
- `strip = true` removes symbols (~30% smaller binary).
- `panic = "abort"` skips unwinding code (smaller binary; no panic recovery, but Tauri apps generally restart on panic anyway).
- `opt-level = 1` in dev keeps debug builds 2-3× faster than the default `opt-level = 0` while staying fast to compile.

### Target-specific dependencies

```toml
[target.'cfg(target_os = "macos")'.dependencies]
security-framework = "3.0"
cocoa = "0.25"
objc = "0.2"

[target.'cfg(target_os = "windows")'.dependencies]
windows-sys = { version = "0.59", features = [
    "Win32_System_ProcessStatus",
    "Win32_Foundation",
    "Win32_UI_Input_KeyboardAndMouse",
] }

[target.'cfg(target_os = "linux")'.dependencies]
machine-uid = "0.2"
```

**Why:** Platform crates don't compile on the wrong platform. Putting them under `[target.'cfg(...)']` makes the default `cargo build` portable. Enable only the `windows-sys` features the code actually uses — pulling all features in adds minutes to compile time.

## Frontend

### Typed `useTauriCommand` hook

```ts
// hooks/useTauriCommand.ts
export function useTauriCommand<T = unknown>(options: UseCommandOptions<T>): CommandState<T> {
  const [data, setData] = useState<T | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const execute = useCallback(async (args?: Record<string, unknown>) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await invoke<T>(options.command, args || options.args);
      setData(result);
      return result;
    } catch (err) {
      setError(String(err));
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [options.command, options.args]);

  return { data, isLoading, error, execute };
}
```

**Why:** Every component would otherwise reinvent loading/error wrappers around `invoke()`, with subtle differences. One hook = one place to add retries, debouncing, logging, telemetry. Plus type safety — `T` flows through.

### `isTauriReady()` guard

```ts
// tauriReady.ts
export function isTauriReady(): boolean {
  return typeof window !== "undefined";
}
```

Auto-loading hooks should call this before invoking. In Tauri 2 the IPC bridge is ready before React mounts, but a frontend that's ever previewed via plain `vite dev` (without Tauri) needs the guard.

### `vite.config.ts` tuned for Tauri

```ts
export default defineConfig({
  base: './',                    // relative paths so bundled HTML loads from tauri://localhost
  plugins: [react()],
  clearScreen: false,            // don't hide Rust errors
  server: {
    port: 5173,
    strictPort: true,            // fail if port is taken (Tauri expects it)
    watch: { ignored: ['**/src-tauri/**'] },  // Cargo handles its own files
  },
  esbuild: { jsx: 'automatic' },
});
```

**Why:**
- `base: './'`: without it, asset URLs are absolute (`/assets/index.css`) and break inside the `tauri://localhost` context.
- `strictPort: true`: Tauri's `devUrl` points at 5173 — if Vite silently picks 5174, Tauri shows a blank window.
- Ignoring `src-tauri/` avoids HMR loops triggered by Cargo's `target/` writes.
- `clearScreen: false`: Vite's screen-clear hides important Rust compiler errors.

### TypeScript strict config

```json
{
  "compilerOptions": {
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "isolatedModules": true,
    "allowImportingTsExtensions": true
  }
}
```

**Why:** Strict mode catches real bugs (`undefined` access, implicit `any`). `noUnusedLocals`/`noUnusedParameters` flag the kind of "I forgot to wire this up" mistakes that pass code review.

## CI

### Cross-platform matrix

```yaml
# .github/workflows/unit-tests.yml
name: Unit Tests
on:
  push: { branches: ['**'] }
  pull_request:

jobs:
  test:
    strategy:
      fail-fast: false
      matrix:
        platform: [macos-latest, windows-latest, ubuntu-latest]
    runs-on: ${{ matrix.platform }}
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci
      - name: Install Ubuntu deps
        if: matrix.platform == 'ubuntu-latest'
        run: |
          sudo apt-get update
          sudo apt-get install -y libgtk-3-dev libayatana-appindicator3-dev pkg-config
      - run: cd src-tauri && cargo test
```

**Why:** Tauri's behavior diverges per OS (file pickers, permissions, hotkeys). A green test on macOS does not imply Windows works. `fail-fast: false` lets you see all three results.
