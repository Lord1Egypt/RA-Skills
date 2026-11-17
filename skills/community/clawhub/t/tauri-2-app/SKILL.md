---
name: tauri-2-app
description: >-
    Scaffold a new Tauri 2 desktop app (Rust backend + TypeScript/React frontend) using a
    thin-frontend / rich-Rust-backend architecture with modular commands, trait-based platform
    abstractions, encrypted secrets at rest, single-instance enforcement, a self-hosted updater,
    and a cross-platform CI matrix. Three modes: full project scaffold, add a Tauri command
    slice, add a Rust module slice. Use this skill whenever the user says "create a new Tauri
    app", "scaffold a Tauri 2 project", "new desktop app with Tauri", "Tauri + React project",
    "add a Tauri command end-to-end", "add a Rust module to my Tauri app", "my Tauri
    conventions", or "/tauri-2-app" — even if they don't name the skill. Full good-pattern
    catalog and pitfall list live in the skill body.
---

# Tauri 2 App Scaffolder

Generate a production-grade Tauri 2 desktop app that keeps the **good** patterns from a battle-tested codebase (thin TS frontend that only invokes commands, rich Rust backend with modular `commands/`, `state/`, `storage/`, `platform/`, `error/`, plugin-based features wired in `lib.rs`, capability JSON per window, encrypted secrets at rest, single-instance enforcement, updater wired to a self-hosted JSON manifest, cross-platform CI matrix, target-specific Cargo dependencies, release-profile LTO, typed frontend command hooks) and eliminates the **bad** ones often seen in Tauri codebases (committed `.backup` / `.orig` / `.temp` files in `src-tauri/src/`, API keys in plaintext settings JSON, tokens in `localStorage`, `cfg!(target_os)` scattered through command bodies instead of trait-based platform code, hand-rolled date math instead of `chrono::Utc::now()`, raw `std::fs` reads/writes that bypass Tauri's capability checks, blocking I/O inside `#[tauri::command]` without `tokio::task::spawn_blocking`, missing `#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]` in `main.rs` causing a console flash on Windows, multi-instance apps without `tauri-plugin-single-instance`, `devtools: true` in release config, generic catch-all `String` errors with no `thiserror` enum at module boundaries, hardcoded company-specific bundle identifiers / R2 URLs / updater pubkeys / signing identities baked into the skill).

## When to use this skill

Trigger on any of:

- "create a new Tauri app" / "scaffold a Tauri 2 project" / "new desktop app with Tauri"
- "Tauri + React project" / "Tauri + vanilla TS project" / "Rust backend desktop app"
- "use my Tauri patterns" / "the Tauri conventions I like" (in a Tauri context)
- "add a Tauri command end-to-end" / "wire up a command from Rust to React"
- "add a Rust module to my Tauri app" / "add a state slice"
- The user pastes a feature spec for a desktop feature (hotkey, tray, file I/O, system notification, OS-specific behavior) and asks you to wire it through the Rust backend and frontend

If unsure whether the user wants a brand-new app vs. an addition to an existing one, ask once — don't guess.

## Three operating modes

Pick the mode from the user's request. If ambiguous, ask.

| Mode | Trigger | Output |
|------|---------|--------|
| **`scaffold-app`** | "new Tauri app", "scaffold Tauri 2 project", empty directory | Full Tauri 2 app: `package.json`, `vite.config.ts`, `tsconfig.json`, `index.html`, `src/` (React or vanilla TS), `src-tauri/` with modular `commands/`, `state/`, `storage/`, `platform/`, `error/`, `settings/`, capability JSON, `Info.plist` + `entitlements.plist` (macOS), `build.rs`, GitHub Actions CI, single-instance + updater plugins wired. |
| **`add-command`** | "add a `<name>` command end-to-end", "wire up a command from Rust to TS" | New `#[tauri::command]` in the right `src-tauri/src/commands/*.rs` module, registered in `lib.rs`'s `invoke_handler`, granted permissions in `capabilities/default.json` if it uses a plugin, plus a typed frontend hook in `src/hooks/` that wraps `invoke()` with loading/error state. |
| **`add-module`** | "add a `<name>` module", "add a state/storage slice for X" | New `src-tauri/src/<name>/mod.rs` (+ optional submodules), with `serde`-derived types, a `thiserror` error enum, JSON persistence via the shared `storage` module, and a unit-test module + an integration test file in `src-tauri/tests/`. |

## Workflow

### Step 1 — Resolve versions (don't hard-code)

The user does **not** want hard-coded Cargo / npm versions baked into the skill. Before writing `Cargo.toml` or `package.json`:

1. Check the user's environment first: run `cargo --version`, `rustc --version`, `node --version`, `npm --version` (or `pnpm --version`).
2. Resolve the latest stable versions of the core stack at scaffold time — never hand-paste:
   - **Rust crates** (look up on crates.io or via context7): `tauri` (must be 2.x), `tauri-build` (2.x), `tauri-plugin-opener`, `tauri-plugin-notification`, `tauri-plugin-dialog`, `tauri-plugin-fs`, `tauri-plugin-global-shortcut`, `tauri-plugin-single-instance`, `tauri-plugin-updater`, `tauri-plugin-process`, `serde`, `serde_json`, `thiserror`, `anyhow`, `tokio` (with `sync`, `rt-multi-thread`, `macros`), `tracing`, `tracing-subscriber` (with `env-filter`), `chrono` (don't hand-roll date math), `dirs`.
   - **npm packages**: `@tauri-apps/api` (2.x), `@tauri-apps/cli` (2.x), `@tauri-apps/plugin-*` matching the Rust plugins, `react` + `react-dom` (if React), `typescript`, `vite`, `@vitejs/plugin-react` (if React).
3. Pin the Rust edition to `2021` unless the user asks otherwise.
4. Quote the resolved versions back to the user before generating, so they can object.
5. Default to **npm** unless `pnpm` or `bun` is present and the user prefers it.
6. Concrete resolution commands when context7 is unavailable: `npm view @tauri-apps/api version`, `cargo search <crate> --limit 1`, or WebFetch `https://crates.io/api/v1/crates/<crate>` (`max_stable_version`). Never write a version you did not just resolve this session — no versions from memory, no invented numbers.
7. **Tauri 1.x is poison.** Training data is full of v1 patterns that look plausible and fail on v2. Never emit: `import { invoke } from '@tauri-apps/api/tauri'` (the v2 path is `@tauri-apps/api/core`), a `tauri.allowlist` or top-level `tauri` key in `tauri.conf.json` (v2 uses `app` / `bundle` / `plugins` + `capabilities/*.json`), or v1 plugin names/APIs. If you are not certain a conf key, capability permission string, or plugin API exists in Tauri 2, verify it against the installed schema (`node_modules/@tauri-apps/cli/config.schema.json`; valid permission strings appear in `src-tauri/gen/schemas/` after the first build) or the plugin's docs **before** writing code that depends on it. Capability `permissions` entries use the short plugin name (`dialog:allow-open`, `fs:allow-read-file`) — never a `tauri-plugin-` prefix. Note that `cargo check` compiles `tauri-build`, which validates `tauri.conf.json` and `capabilities/*.json` — a schema or unknown-permission error there is a JSON problem; fix the conf/capability file against the schema, don't edit Rust code to appease it.

### Step 2 — Gather inputs (ask once, in one batch)

For `scaffold-app`, use `AskUserQuestion` to collect:

- **App name** (kebab-case for the directory; the productName in `tauri.conf.json` can be Title Case).
- **Bundle identifier** in reverse-DNS form (e.g. `com.example.myapp`) — **must come from the user**, never hardcoded. This goes in `tauri.conf.json` `identifier` and the macOS `Info.plist` `CFBundleIdentifier`.
- **Frontend flavor**: React + Tailwind, React (no Tailwind), vanilla TypeScript, or "I'll wire it up myself".
- **Plugins to wire**: opener, notification, dialog, fs, global-shortcut, single-instance, updater, process. Default-ON: `opener`, `dialog`, `fs`, `single-instance`. Updater is OFF by default — only wire it if the user has (or will have) a manifest URL.
- **Tray icon** (yes/no). If yes, generate a minimal tray with Show/Hide/Quit.
- **Encrypted-secrets module** (yes/no). If yes, generate an `encryption/` module using `aes-gcm` + `argon2` for at-rest encryption of API keys/tokens. The salt-derivation source (machine UUID, keychain, etc.) is platform-specific — generate stubs, but **do not** ship a hardcoded "pepper" string.
- **Updater endpoint** (optional). If provided, write it into `tauri.conf.json` under `plugins.updater.endpoints`. **Never** invent a URL or paste a public key from another project — ask the user to generate one with `tauri signer generate` and paste it in afterwards.
- **CI** (default ON): GitHub Actions matrix building on macOS/Windows/Ubuntu.
- **First command/module** (optional) — if provided, also run the matching mode after scaffold.

For `add-command`: command name (snake_case), the module it belongs in (`commands/<module>.rs`), inputs + return type, whether it's `async`, whether it needs `AppHandle` / `State<T>` / a Tauri plugin. If the command does blocking I/O, confirm it needs `tokio::task::spawn_blocking`.

For `add-module`: module name (snake_case), the data type(s) it owns, whether it persists to JSON in `app_data_dir`, what error variants it needs.

### Step 3 — Generate files

Use the **templates in [`references/templates/`](references/templates/)** as the source of truth. Apply these rules:

- Use `Write` for new files. Never use `Edit` on files you're creating fresh.
- Replace all `{{AppName}}`, `{{app_name}}`, `{{BundleId}}`, `{{Command}}`, `{{Module}}` placeholders consistently. `{{app_name}}` is snake_case for Rust crate / lib names; `{{AppName}}` is Title Case for product name; the directory is kebab-case.
- Create directories before files. On Windows shell use PowerShell `New-Item -ItemType Directory -Force`.
- Do **not** run `create-tauri-app` to bootstrap — write the files directly from templates so the layout matches the conventions in [`references/folder-layout.md`](references/folder-layout.md). Use `npm install` after `package.json` is written, then `cargo fetch` from `src-tauri/` to seed the Cargo cache.
- For icons, run `npx @tauri-apps/cli icon <path-to-source.png>` once a source image exists, or generate a 1024×1024 placeholder with `sharp` if the user wants. Do **not** commit a placeholder square as the final icon — surface it as a TODO.
- If a generator IS run (`create-tauri-app` at the user's insistence, `npx @tauri-apps/cli icon`, `tauri signer generate`) and its output differs from this skill's layout: **Tauri wins on file locations it mandates** (`src-tauri/` shape, `capabilities/`, `gen/`, icon paths), **this skill wins on everything Tauri doesn't mandate** (the `commands/`/`state/`/`storage/`/`platform/` module split, frontend hooks layout). Reconcile deliberately and list every deviation in your report — never force the skill layout over a framework requirement, never silently abandon the skill's patterns.

### Step 4 — Verify and report

- Run `npm install` (or chosen PM).
- Run `cd src-tauri && cargo build` — must exit 0. (Don't run `tauri dev` in CI — it opens a window.) If a full `cargo build` is prohibitively slow in this environment, `cargo check` is the minimum acceptable bar — state which one you ran.
- Run `cd src-tauri && cargo test` — must exit 0 if any tests were generated.
- Run `npm run build` (frontend) — must exit 0. `cargo check` + `npm run build` together are the floor; a full `tauri build` is optional (slow).
- Optionally run `npm run tauri build -- --debug` if the user wants a debug bundle; skip in CI by default since it's slow.
- **A scaffold that hasn't compiled is not delivered.** Paste the actual proof lines in your report (cargo's `Finished` profile line, `test result: ok`, Vite's `✓ built in ...`). Never report success from memory of the steps you intended, and never report partial success as success — if something is red, say exactly what is red.
- **CLI failure protocol** (applies to `npm install`, `cargo build`/`check`/`test`, `npm run build`): read the full error output — for cargo, fix the **first** error; later ones are usually cascade. Change exactly one thing, retry once. If the same step fails twice, stop scaffolding and surface the verbatim error to the user — do not keep generating files on a broken base, and do not re-run the identical command hoping for a different result.
- Reply with a short summary: project path, versions chosen, plugins wired, bundle identifier, next steps (e.g. "fill in the macOS `Info.plist` usage descriptions for any permissions you'll request", "generate updater keys with `npx tauri signer generate`", "run `npm run tauri dev`").

## Project layout (canonical)

See [`references/folder-layout.md`](references/folder-layout.md) for the full tree, file-by-file purpose, and the rules that govern it.

Top-level shape:

```
{{app-name}}/
  package.json
  tsconfig.json                # strict: true, noUnusedLocals, noUnusedParameters
  vite.config.ts               # port 5173, ignores src-tauri, base: './'
  index.html                   # anti-flash theme script if dark/light theming is in scope
  .gitignore                   # MUST include src-tauri/target/, dist/, .env, *.backup, *.orig, *.temp
  .env.example                 # NEVER .env — only .env.example committed
  src/                         # frontend (TS / React)
    main.tsx                   # entry: createRoot + render
    App.tsx
    tauriReady.ts              # isTauriReady() guard
    hooks/
      useTauriCommand.ts       # generic typed invoke() wrapper with loading/error
      use<Domain>.ts           # per-domain hooks composing useTauriCommand
    components/
    styles/
  src-tauri/
    Cargo.toml                 # [lib] name = "{{app_name}}_lib", target-specific deps via [target.'cfg(...)']
    build.rs                   # links macOS frameworks, Windows libs, Linux pthread/m as needed
    tauri.conf.json            # productName, identifier, bundle, plugins.updater (if enabled)
    Info.plist                 # macOS bundle identifier + usage descriptions for permissions requested
    entitlements.plist         # macOS hardened-runtime entitlements (audio-input, apple-events, etc.)
    capabilities/
      default.json             # main-window capability with granular permission scopes
    icons/                     # icon.png (1024), icon.ico, icon.icns, 32x32.png, 128x128.png, 128x128@2x.png
    src/
      main.rs                  # #![cfg_attr(not(debug_assertions), windows_subsystem = "windows")] + embed_plist on macOS
      lib.rs                   # pub mod ...; pub fn run() builds Tauri, registers plugins + invoke_handler
      commands/                # ONE file per domain (recording.rs, settings.rs, system.rs, ...)
        mod.rs                 # pub mod ...; pub use *;
        system.rs              # generic commands (write_file, dialogs, notifications)
        <domain>.rs            # per-domain command modules
      state/                   # pub struct AppState { ... } managed via tauri::Manager
        mod.rs
      storage/                 # JSON-on-disk utilities: get_app_data_dir, load_json, save_json
        mod.rs
      settings/                # Settings struct (camelCase serde) + load/save + migrations
        mod.rs
        defaults.rs
        storage.rs
        commands.rs
      platform/                # trait-based platform abstractions
        mod.rs
        traits.rs              # PermissionChecker, FileOpener, AutostartManager
        macos.rs               # #[cfg(target_os = "macos")]
        windows.rs
        linux.rs
        wrappers.rs            # PlatformXxx wrappers managed in Tauri State
      error/                   # into_string_err! macro + ResultExt trait
        mod.rs
      encryption/              # (optional) AES-GCM + Argon2id for secrets at rest
        mod.rs
      tray.rs                  # (optional) tray icon, menu, click handlers
    tests/                     # integration tests; one file per domain
      common/
        mod.rs
      <domain>_test.rs
  .github/
    workflows/
      unit-tests.yml           # cross-platform matrix: cargo test on macos/windows/ubuntu
      publish.yml              # (optional) tag-triggered release pipeline; user fills in CDN secrets
```

**Dependency rules (enforced):**

- `commands/` files call into `state/`, `settings/`, `storage/`, `platform/`, `<domain>/` modules — never the other way.
- Domain modules (`export`, `history`, `sync`, …) may depend on `storage/` and `platform/traits`, but not on `commands/` or Tauri's runtime types directly (use `AppHandle` only when persisting via `storage::get_app_data_dir`).
- `platform/<os>.rs` files are gated with `#[cfg(target_os = "...")]` and **only** these files contain `cfg!(target_os)` checks. All other modules go through `platform::traits::*` and a `Platform<X>` wrapper managed in `State`.
- Frontend `hooks/use<Domain>.ts` files compose `useTauriCommand` — they never call `invoke()` directly inline in a component.

## Required code patterns

Full templates are in [`references/templates/`](references/templates/). The full Keep/Eliminate rationale is in [`references/good-patterns.md`](references/good-patterns.md) and [`references/anti-patterns.md`](references/anti-patterns.md).

### Keep

- **Thin frontend, rich Rust backend.** All file I/O, audio, system permissions, OS-specific behavior, and long-running work happen in Rust. The TS layer only invokes commands and renders state.
- **`#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]` in `main.rs`** to prevent a console window on Windows in release.
- **`embed_plist::embed_info_plist!("../Info.plist")`** in `main.rs` under `#[cfg(target_os = "macos")]` so the binary carries its plist when run standalone.
- **`tauri-plugin-single-instance` registered first** in the builder chain, with a callback that focuses the existing window when a second instance launches. See [`references/templates/lib-rs.md`](references/templates/lib-rs.md).
- **Modular `commands/`** — one file per domain, all re-exported from `commands/mod.rs`, registered in a single `tauri::generate_handler![...]` call in `lib.rs`.
- **`State<AppState>` for shared app state** managed via `app.manage(Mutex::new(AppState::new()))`. Inside async commands, hold the lock for the minimum time and drop it before any `.await`.
- **Trait-based platform abstractions** (`PermissionChecker`, `FileOpener`, `AutostartManager`) in `platform/traits.rs`, with `#[cfg(target_os = "...")]` implementations in `platform/macos.rs`, `windows.rs`, `linux.rs`, and `Send + Sync` wrappers in `platform/wrappers.rs` managed in Tauri State. Tests assert `Send + Sync` on the wrappers.
- **`storage/mod.rs` shared utilities** — `get_app_data_dir`, `get_storage_path`, `load_json<T>`, `save_json<T>`, `generate_id`, `Timestamped` trait, `prune_entries_by_age` — used by `settings/`, `history/`, `error_log/`, and any other persistent JSON store.
- **Settings with `#[serde(rename_all = "camelCase", default)]`** so the on-disk JSON matches frontend naming, and missing fields fall back to `Default`. Add a migration pass in `deserialize_settings(json: &Value) -> Settings` when fields change shape.
- **`thiserror` enums at module boundaries**; `anyhow::Result` only inside private helpers. Commands return `Result<T, String>` with errors stringified at the `#[tauri::command]` boundary — use the `into_string_err!` macro / `ResultExt::into_string()` from `error/mod.rs` to keep this clean.
- **`tokio::task::spawn_blocking`** for any synchronous I/O or CPU-bound work inside an `async` command — file pickers, native dialogs, ML inference, encryption. Awaiting blocking work directly stalls Tauri's IPC runtime.
- **`tracing` + `tracing-subscriber`** for logs, initialized in `pub fn run()` before the builder. Use `EnvFilter::from_default_env().add_directive(Level::INFO.into())` so `RUST_LOG=debug` works.
- **Encrypted secrets at rest** (`encryption/mod.rs`): AES-256-GCM ciphertext + Argon2id key derivation + platform-specific hardware-bound salt (machine UUID on macOS via `ioreg IOPlatformExpertDevice`, Windows via `wmic csproduct get uuid`, Linux via `/etc/machine-id` or `machine-uid` crate). Store `EncryptedApiKey { ciphertext, nonce, salt }` in settings. Auto-migrate legacy plaintext keys on load.
- **`capabilities/default.json` with granular permissions** — only the scopes the app actually uses (e.g. `fs:allow-read-file`, `dialog:allow-open`), not blanket `"*"`. One capability file per window (e.g. `default.json` for `main`, `<window>.json` for any auxiliary windows).
- **macOS `Info.plist` usage descriptions** for every permission the app requests (`NSMicrophoneUsageDescription`, `NSAccessibilityUsageDescription`, etc.). The app will silently fail without them.
- **macOS `entitlements.plist` for hardened runtime** with only what's needed (`com.apple.security.cs.allow-jit`, `com.apple.security.device.audio-input`, `com.apple.security.automation.apple-events` — but only if used).
- **`build.rs` that links platform frameworks** explicitly (`Accelerate`, `Metal`, `CoreGraphics`, `Foundation`, `ApplicationServices` on macOS; `user32` on Windows; `pthread`, `m` on Linux). Use `CARGO_CFG_TARGET_OS` at build time, not host OS.
- **Target-specific Cargo deps** via `[target.'cfg(target_os = "macos")'.dependencies]` for platform crates (`security-framework`, `cocoa`, `winapi`, `windows-sys`, `machine-uid`). The default deps list stays portable.
- **Release profile in `Cargo.toml`**: `lto = "fat"`, `codegen-units = 1`, `opt-level = 3`, `strip = true`, `panic = "abort"`. Dev profile: `opt-level = 1` for tolerable rebuild times.
- **Vite config tuned for Tauri**: `base: './'` (relative paths so the bundled HTML loads from `tauri://localhost`), `server.port: 5173`, `server.strictPort: true`, `server.watch.ignored: ['**/src-tauri/**']`, `clearScreen: false` so Rust errors aren't hidden.
- **TypeScript `strict: true`** with `noUnusedLocals`, `noUnusedParameters`, `noFallthroughCasesInSwitch`, and `isolatedModules`.
- **Typed frontend `useTauriCommand<T>` hook** in `src/hooks/useTauriCommand.ts` that wraps `invoke<T>(name, args)` with `data`, `isLoading`, `error`, and `execute`. Per-domain hooks (`useSettings`, `useRecording`, …) compose it; components never call `invoke()` inline. See [`references/templates/use-tauri-command.md`](references/templates/use-tauri-command.md).
- **`isTauriReady()` guard** in `src/tauriReady.ts` — frontend code that runs before the Tauri IPC bridge is ready (e.g. early auto-load) must call it.
- **GitHub Actions cross-platform matrix** that runs `cargo test` on macOS, Windows, and Ubuntu. Ubuntu needs `libgtk-3-dev libayatana-appindicator3-dev pkg-config`.
- **`tauri.conf.json` `windows[].devtools: false`** (or omitted — Tauri defaults to off in release). DevTools should be opened from a build-time feature flag, not the production config.
- **Reset-state-on-startup pattern** — in `pub fn run()`'s `.setup(|app| { ... })`, clear any in-progress / stuck state from a previous run before showing the window. Crashes leave globals in odd places; treat each startup as recovering from "the app was force-quit".
- **Show window FIRST in `.setup()`** before any blocking initialization. Heavy work (ML model loading, large config parses) goes on a background thread that emits events back to the frontend.
- **Minimal comments in generated code (Rust and TS).** Default to no comments. Only add one when the *why* is non-obvious — `// SAFETY:` on an `unsafe` block, a workaround for a specific upstream bug (with a link), a non-trivial invariant the code depends on, a platform quirk that isn't visible from the names. Never write Rust doc-comment blocks (`///`) on internal items; reserve them for genuinely public API surface (`pub` types crossing crate boundaries). Never restate *what* the next line does, never leave `// TODO` without an issue link. One short line max — no multi-line comment blocks. `// SAFETY:` on `unsafe` is the one place verbose justification is *required*; everywhere else, well-named identifiers carry the *what* and comments earn their place only when they carry *why*.

### Eliminate (anti-patterns)

Every one of these is forbidden in generated code. Rationale for each is in [`references/anti-patterns.md`](references/anti-patterns.md).

- ❌ Committed `*.backup`, `*.orig`, `*.temp` files in `src-tauri/src/` (e.g. `lib.rs.backup`, `macos.rs.orig`). Add them to `.gitignore` and never commit. These are merge-conflict / WIP artefacts, not source of truth.
- ❌ Plaintext API keys / OAuth tokens in `settings.json`. If the app stores any secret, route it through `encryption/` and persist only `EncryptedApiKey { ciphertext, nonce, salt }`. Auto-migrate any plaintext encountered on load.
- ❌ Tokens in browser `localStorage` / `sessionStorage`. Anything sensitive lives in Rust-side encrypted storage; the frontend asks for it only when needed.
- ❌ `devtools: true` in the release `tauri.conf.json`. Gate dev tools behind a build-time feature or a separate `tauri.dev.conf.json`.
- ❌ `cfg!(target_os = "...")` checks scattered through command bodies. Platform-specific behavior goes through a `platform::traits::*` impl + `cfg(target_os = "...")` modules; commands stay portable.
- ❌ Hand-rolled date / leap-year / ISO-8601 parsing. Use `chrono::Utc::now()`, `DateTime::parse_from_rfc3339`, `Duration::days(n)`. The "hand-rolled time math" pattern is an anti-pattern even when it works.
- ❌ Raw `std::fs::read` / `std::fs::write` against user-chosen paths from inside a `#[tauri::command]`. Either go through `tauri-plugin-fs` (which respects capability scopes) or restrict raw I/O to paths derived from `app_handle.path().app_data_dir()`.
- ❌ Blocking I/O inside `async fn` commands without `tokio::task::spawn_blocking`. The Tauri IPC runtime is shared — a blocked task stalls all command throughput.
- ❌ `#[tauri::command] fn long_running(...) -> Result<...>` that holds a `std::sync::Mutex` lock across an `.await`. Use `tokio::sync::Mutex`, or drop the guard before awaiting.
- ❌ Missing `#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]` at the top of `main.rs`. Without it, a console window flashes behind the Tauri window on Windows in release.
- ❌ App built without `tauri-plugin-single-instance`. Double-clicking the app launches a second process, both fighting over global hotkeys, audio devices, sockets, and lock files.
- ❌ Builder calls in `lib.rs` that boot `init_*` before showing the window — model loading, audio device enumeration, network calls — block the user from seeing UI for seconds.
- ❌ Empty `catch {}` / `let _ = result;` swallowing errors silently. Either log via `tracing::warn!` / `error!` or propagate via `?`.
- ❌ Mutex-locking the AppState for the duration of a command. Read or clone what you need, drop the guard, then do the work.
- ❌ Hardcoded bundle identifiers, R2 / Cloudflare / S3 URLs, updater public keys, Apple Team IDs, Windows certificate thumbprints in any generated file. These are user-specific; ask, don't assume.
- ❌ Inventing a Tauri updater pubkey. The user generates one with `npx tauri signer generate -w ~/.tauri/myapp.key` and pastes the public key into `tauri.conf.json`. Never paste another project's pubkey.
- ❌ `String` errors at module boundaries (`fn foo() -> Result<T, String>`). Internal APIs use `thiserror` enums; only `#[tauri::command]` returns convert to `Result<T, String>` at the IPC boundary.
- ❌ Multiple `createRoot(...)` calls, or rendering React before the DOM root is wired. One entry point, `main.tsx`, renders into `#app` after `index.html` is parsed.
- ❌ Frontend invoking `@tauri-apps/api/core` `invoke()` inline in components instead of through a typed hook. Loses TS safety, scatters error handling, makes refactors painful.
- ❌ Capability files with blanket permissions (`"core:default"` only, no granular scopes; or `"fs:default"` without `allow-read-file` / `allow-write-file` actually being used). Capabilities should describe **exactly** what the app needs and nothing more.
- ❌ `tauri.conf.json` `app.security.csp: null` left in production without an explicit decision. If CSP is genuinely too restrictive for the app, add a CSP that whitelists `tauri://localhost` + your trusted origins, and document the choice.
- ❌ Bundling external binaries (FFmpeg, ML models) without listing them in `tauri.conf.json` `bundle.externalBin` / `bundle.resources`. They'll work in `cargo run` but be missing in the installer.
- ❌ macOS `Info.plist` missing `NSMicrophoneUsageDescription` / `NSAccessibilityUsageDescription` / `NSCameraUsageDescription` for permissions the app actually requests. The OS will refuse the prompt and the call returns "denied" silently.
- ❌ macOS `entitlements.plist` requesting entitlements the app doesn't use (`com.apple.security.cs.allow-unsigned-executable-memory`, `com.apple.security.cs.allow-jit`) — they break notarization or weaken the sandbox. Only enable what's required.
- ❌ Two binaries in `Cargo.toml` (`[[bin]]` × 2) without a clear sidecar reason. If the app has one main binary, keep one `[[bin]]`. Sidecars get their own crate inside a Cargo workspace, not a second `[[bin]]` in the same crate.
- ❌ `.env` committed to git. Only `.env.example` is tracked; `.env` is in `.gitignore`.

## Operating-mode playbooks

### Mode 1 — `scaffold-app`

1. Resolve versions per **Step 1**. Quote them.
2. Ask the inputs per **Step 2**. Wait for answers.
3. Generate, in this order:
   1. Root: `package.json`, `tsconfig.json`, `tsconfig.node.json`, `vite.config.ts`, `index.html`, `.gitignore`, `.env.example`, `README.md`, `.github/workflows/unit-tests.yml`.
   2. Frontend: `src/main.tsx` (or `main.ts`), `src/App.tsx`, `src/tauriReady.ts`, `src/hooks/useTauriCommand.ts`, `src/styles.css`. Tailwind config + `postcss.config.js` only if the user chose Tailwind.
   3. `src-tauri/Cargo.toml` (with target-specific deps + release profile), `src-tauri/build.rs`, `src-tauri/tauri.conf.json`, `src-tauri/Info.plist`, `src-tauri/entitlements.plist`, `src-tauri/capabilities/default.json`.
   4. `src-tauri/icons/` — placeholder 1024×1024 PNG **only** if the user hasn't supplied one. Surface as TODO; tell them to run `npx @tauri-apps/cli icon icons/icon.png`.
   5. `src-tauri/src/main.rs`, `src-tauri/src/lib.rs`, `src-tauri/src/error/mod.rs`, `src-tauri/src/state/mod.rs`, `src-tauri/src/storage/mod.rs`, `src-tauri/src/commands/mod.rs` + `src-tauri/src/commands/system.rs`, `src-tauri/src/platform/{mod,traits,macos,windows,linux,wrappers}.rs`, `src-tauri/src/settings/{mod,defaults,storage,commands}.rs`.

      **Checkpoint:** run `npm install` then a first `cd src-tauri && cargo check` here, before optional modules — errors localize to the core tree, and this check runs `tauri-build`, which validates `tauri.conf.json` + `capabilities/*.json` and generates `src-tauri/gen/schemas/` (the authority for valid permission strings). Fix any conf/capability error now, per the Step-4 failure protocol, before writing more capability entries.

   6. Optional: `src-tauri/src/encryption/mod.rs`, `src-tauri/src/tray.rs`, `src-tauri/src/commands/<more>.rs` based on user answers.
   7. `src-tauri/tests/common/mod.rs` + at least one integration test file (e.g. `system_test.rs`) so CI has something real to run.
4. `npm install`.
5. `cd src-tauri && cargo build && cargo test` — must succeed.
6. `npm run build` — must succeed (catches TS / Vite errors).
7. If a first command/module was requested, run **Mode 2** or **Mode 3** for it.
8. Report.

### Mode 2 — `add-command`

For command `{{command}}` (snake_case) in module `commands/{{domain}}.rs`:

1. **Rust**:
   - Add (or extend) `src-tauri/src/commands/{{domain}}.rs` with a `#[tauri::command]` async fn.
   - If the function does blocking work, wrap it in `tokio::task::spawn_blocking(move || { ... }).await.map_err(|e| e.to_string())?`.
   - If it needs `AppHandle`, take it as a parameter (Tauri injects). If it needs shared state, take `State<'_, Mutex<AppState>>`.
   - Errors: return `Result<T, String>`. Internally use `thiserror` + the `into_string_err!` macro from `error/mod.rs` to convert at the boundary.
   - Re-export from `commands/mod.rs` (`pub use {{domain}}::*;`).
   - Register in `lib.rs` inside `tauri::generate_handler![..., {{command}}]`.
2. **Capabilities**: if the command uses a plugin (notification, fs, dialog, global-shortcut), add the specific permission scope to `capabilities/default.json` (e.g. `"dialog:allow-open"`). Do **not** widen to `default` if a narrower scope works.
3. **Frontend**:
   - Add a typed wrapper in `src/hooks/use{{Domain}}.ts` that composes `useTauriCommand<ReturnType>({ command: "{{command}}" })`.
   - Export the hook. Do **not** call `invoke()` inline in a component.
4. **Test**: add an integration test in `src-tauri/tests/{{domain}}_test.rs` that exercises the command's underlying function (the `#[tauri::command]` itself is hard to call without a full Tauri context — test the inner function).

After generating: `cd src-tauri && cargo build && cargo test` then `npm run build` from the project root. Apply the Step-4 proof-and-failure protocol — paste the green lines; the same step failing twice = stop and surface the verbatim error.

### Mode 3 — `add-module`

For module `{{module}}` (snake_case):

1. Create `src-tauri/src/{{module}}/mod.rs` (split into submodules if multiple concerns).
2. Define data types with `#[derive(Debug, Clone, Serialize, Deserialize)]` + `#[serde(rename_all = "camelCase")]` so JSON matches the frontend.
3. Define a `thiserror` error enum: `#[derive(Debug, thiserror::Error)] pub enum {{Module}}Error { ... }`.
4. If the module persists JSON to disk, use the shared `storage` module — `get_app_data_dir`, `load_json`, `save_json`. Don't roll your own file I/O.
5. Add `pub mod {{module}};` to `lib.rs`. Re-export the public types you want callable from commands (`pub use {{module}}::{Type, OtherType};`).
6. Add a `#[cfg(test)]` `mod tests { ... }` block at the bottom of `mod.rs` covering pure logic (no Tauri context required).
7. Add a `src-tauri/tests/{{module}}_test.rs` integration test if the module has cross-cutting behavior.

After generating: `cd src-tauri && cargo build && cargo test` — Step-4 proof-and-failure protocol applies.

## Cargo + npm packages (resolve latest stable at scaffold time)

Look these up at scaffold time — do not hand-paste versions:

**Cargo (always)**
- `tauri` (2.x), `tauri-build` (2.x)
- `serde`, `serde_json`, `thiserror`, `anyhow`
- `tokio` (features: `sync`, `rt-multi-thread`, `macros`)
- `tracing`, `tracing-subscriber` (`env-filter`)
- `chrono`
- `dirs`

**Cargo (conditional, only if used)**
- `tauri-plugin-opener`, `tauri-plugin-notification`, `tauri-plugin-dialog`, `tauri-plugin-fs`
- `tauri-plugin-global-shortcut`, `tauri-plugin-single-instance`, `tauri-plugin-updater`, `tauri-plugin-process`
- `aes-gcm`, `argon2`, `base64`, `rand` (encryption module)
- `reqwest` (with `rustls-tls`, `json`) — only if the app makes HTTP calls
- `tokio-tungstenite` (with `rustls-tls-native-roots`) — only if WebSocket needed
- `regex` (with `default-features = false`, `features = ["std", "perf"]`)
- `embed_plist` (macOS only, gated in `main.rs`)

**Cargo (target-specific)**
- macOS: `security-framework`, `objc`, `cocoa`, `core-graphics`, `block`
- Windows: `winapi`, `windows-sys` (with the specific feature flags the code uses, not blanket)
- Linux: `machine-uid` (only if the encryption module needs a machine ID)

**Dev-dependencies**
- `mockall`, `mockito` (only if the code is structured for mocking)
- `tokio-test`, `tempfile`, `assert_matches`, `pretty_assertions`
- `proptest` (only if a domain has property-test-shaped invariants)
- `serde_yaml` (only if tests parse CI YAML)

**npm**
- `@tauri-apps/api` (2.x), `@tauri-apps/cli` (2.x)
- `@tauri-apps/plugin-*` matching the wired Rust plugins
- React stack only if chosen: `react`, `react-dom`, `@types/react`, `@types/react-dom`, `@vitejs/plugin-react`
- `vite`, `typescript`
- Tailwind only if chosen: `tailwindcss`, `postcss`, `autoprefixer`, `@fontsource/*` for any fonts used
- `rimraf` (clean scripts)
- `sharp` only if the user wants icon generation locally

## Verification checklist before reporting "done"

Run this as a **mechanical pass over the generated tree** — grep, don't recall. The Eliminate list is easy to hold at file 1 and forgotten by file 30. Start with this grep block; every command must return nothing:

```bash
grep -rn "cfg!(target_os" src-tauri/src --include='*.rs' | grep -v "src/platform/"   # platform checks outside platform/
grep -rn "@tauri-apps/api/tauri" src/                          # v1 import path (v2 is /core)
grep -n "allowlist\|systemTray" src-tauri/tauri.conf.json      # v1 config schema leaking in (v2: capabilities/, app.trayIcon)
grep -rn "tauri::api::" src-tauri/src --include='*.rs'         # v1 Rust API paths (v2 moved these to plugins)
grep -rnE "pub (api_key|token|secret)\w*: String" src-tauri/src/   # plaintext secret fields (must be EncryptedApiKey)
grep -rn "localStorage.setItem\|sessionStorage.setItem" src/   # tokens/secrets in web storage
grep -n "\"devtools\": true" src-tauri/tauri.conf.json         # devtools enabled in release config
grep -rn "std::fs::" src-tauri/src/commands/                   # raw fs in command bodies
find src-tauri/src -name "*.backup" -o -name "*.orig" -o -name "*.temp"   # WIP artefacts
```

A hit means fix it and re-run the grep — never rationalize it away. Then the full checklist:

- [ ] `npm install` succeeds.
- [ ] `cd src-tauri && cargo build` exits 0.
- [ ] `cd src-tauri && cargo test` exits 0 (if tests were generated).
- [ ] `npm run build` succeeds (frontend bundles).
- [ ] `npm run tauri build -- --debug` succeeds if the user wants a smoke check on the bundler (optional, slow).
- [ ] `main.rs` contains `#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]`.
- [ ] `lib.rs` registers `tauri_plugin_single_instance::init` **first** in the builder chain when single-instance is wired.
- [ ] `tauri.conf.json` `identifier` is not empty and matches what the user provided — not a generic `com.example.*`.
- [ ] `tauri.conf.json` `plugins.updater.pubkey` is **empty / removed** unless the user pasted a real one. Never invent a pubkey.
- [ ] `tauri.conf.json` `app.windows[].devtools` is `false` (or omitted).
- [ ] `capabilities/default.json` has granular permission scopes — no blanket allows beyond `core:default`.
- [ ] `Info.plist` has a usage description for every permission the generated code requests.
- [ ] `.gitignore` includes `src-tauri/target/`, `dist/`, `node_modules/`, `.env`, `*.backup`, `*.orig`, `*.temp`.
- [ ] No `.backup` / `.orig` / `.temp` files exist anywhere under `src-tauri/src/`.
- [ ] No `cfg!(target_os = "...")` appears in `src-tauri/src/commands/**` or `src-tauri/src/<domain>/**` — only in `src-tauri/src/platform/**`.
- [ ] No `localStorage.setItem("token"` / `sessionStorage.setItem("token"` in `src/`.
- [ ] No raw `std::fs::write(&user_supplied_path, ...)` in command bodies (must go through plugin or `app_data_dir`).
- [ ] All `#[tauri::command]` async fns that do blocking work use `tokio::task::spawn_blocking`.
- [ ] No `cfg_if!` or `#[cfg]` guard around `embed_plist::embed_info_plist!` is missing on macOS.
- [ ] `Cargo.toml` `[profile.release]` has `lto`, `codegen-units`, `opt-level`, `strip`, `panic` set.
- [ ] GitHub Actions matrix workflow has macOS, Windows, **and** Ubuntu, and Ubuntu installs the GTK/AppIndicator system deps.

If any check fails, fix before reporting. Don't claim success with a known-broken scaffold.

## Examples

### Example 1: Fresh project

**User:** "Scaffold a new Tauri 2 desktop app called `acme-notes`. React frontend with Tailwind. Bundle identifier `com.acme.notes`. Wire single-instance, dialog, fs, opener. Skip updater for now."

**Claude:**
1. Runs `cargo --version`, `rustc --version`, `node --version`. Resolves latest stable Tauri 2.x, React, Vite, Tailwind versions via context7 / crates.io.
2. Reports chosen versions; waits for confirmation if anything looks off.
3. Asks the Step-2 questions for any inputs not already provided (tray? encryption? first command?).
4. Generates the full project skeleton per Mode 1.
5. Runs `npm install`, `cargo build`, `cargo test`, `npm run build` — all must pass.
6. Reports the tree, the bundle identifier set, and next steps ("create your icon source and run `npx @tauri-apps/cli icon icons/icon.png`", "run `npm run tauri dev`").

### Example 2: Add a command

**User:** "Add a `get_disk_usage` command to my Tauri app that returns the size of a directory."

**Claude:** Runs Mode 2. Adds `#[tauri::command] pub async fn get_disk_usage(path: String) -> Result<u64, String>` to `commands/system.rs` (or a new `commands/disk.rs` if it warrants its own module), wraps the recursive walk in `tokio::task::spawn_blocking`, registers it in `lib.rs`, adds a typed hook `useDiskUsage` to `src/hooks/`, and writes a unit test for the inner function. Builds and tests.

### Example 3: Add a module

**User:** "Add a `notes` module that stores user notes as JSON in the app data dir, with create/list/delete operations."

**Claude:** Runs Mode 3. Creates `src-tauri/src/notes/mod.rs` with a `Note { id, title, body, created_at, updated_at }` struct (using `chrono::DateTime<Utc>`, not hand-rolled timestamps), a `NotesError` `thiserror` enum, and `create_note`, `list_notes`, `delete_note` functions backed by `storage::load_json` / `save_json` (file: `notes.json` in `app_data_dir`). Adds `pub mod notes;` to `lib.rs`. Generates a `#[cfg(test)] mod tests` block covering create/list/delete on a `tempfile::TempDir`. Builds and tests.

## Notes

- **Don't over-engineer**. Don't add Redux/Zustand/MobX on the frontend, Diesel/SQLx on the backend, gRPC, OpenTelemetry, Sentry, or a state-machine library unless the user asks. The default scaffold is intentionally lean.
- **Don't rewrite the user's existing project** as part of this skill. This skill is for *new* scaffolds (and additive command/module modes), not migrations. Migrations are a different conversation.
- **Tauri version**: the skill targets Tauri 2.x. If the user's environment somehow pins 1.x (legacy `tauri.conf.json` shape, `@tauri-apps/api@1`), stop and ask whether they want to upgrade — don't silently downgrade the patterns.
- **Bundle identifier**: always reverse-DNS, always provided by the user, never hardcoded. It cannot change after the app is in distribution (it's the OS-level identity for permissions, keychain entries, settings, and update channels).
- **Updater**: only wire it if the user has, or commits to setting up, a JSON manifest at a known URL and has generated a signing key. Half-wired updaters silently fail in production.
- **Icons**: a single high-res source PNG (1024×1024+) generates every platform-specific format via `npx @tauri-apps/cli icon <path>`. Don't ship the auto-generated placeholder as the real icon.
- **Naming**: kebab-case for the project directory, Title Case for the `productName`, snake_case for the Rust crate (`{{app_name}}` in `Cargo.toml`), reverse-DNS for the bundle identifier. Mismatches in casing are a top source of "works locally, broken installer" bugs.
- **Versions**: always quote the resolved versions before writing `Cargo.toml` / `package.json`. They are resolved at scaffold time, never hard-coded.
