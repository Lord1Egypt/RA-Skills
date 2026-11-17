# Tauri 2 App — Canonical Folder Layout

The layout below is the source of truth for `scaffold-app`. Every rule has a reason — when in doubt, default to the structure here.

## Top-level tree

```
{{app-name}}/
├── package.json                  # frontend deps + scripts (dev, build, tauri:dev, tauri:build)
├── package-lock.json             # commit it (or pnpm-lock.yaml / bun.lockb — whichever PM)
├── tsconfig.json                 # strict TS config
├── tsconfig.node.json            # for vite.config.ts itself
├── vite.config.ts                # base: './', port 5173, ignores src-tauri
├── index.html                    # single entry; anti-flash theme script if dark/light is in scope
├── .gitignore                    # MUST include: src-tauri/target/, dist/, .env, *.backup, *.orig, *.temp
├── .env.example                  # only the keys, never the values
├── README.md
├── .github/
│   └── workflows/
│       ├── unit-tests.yml        # cross-platform cargo test on PRs + pushes
│       └── publish.yml           # (optional) tag-triggered release pipeline
├── src/                          # FRONTEND (TS / React)
│   ├── main.tsx                  # createRoot(...).render(<App />)
│   ├── App.tsx
│   ├── tauriReady.ts             # isTauriReady() guard
│   ├── types.ts                  # cross-cutting frontend types
│   ├── styles/                   # or styles.css if simple
│   ├── hooks/
│   │   ├── useTauriCommand.ts    # generic invoke() wrapper with loading/error/data
│   │   └── use<Domain>.ts        # per-domain hooks composing useTauriCommand
│   ├── components/               # PascalCase .tsx files
│   └── utils/
└── src-tauri/                    # RUST BACKEND
    ├── Cargo.toml                # [lib] name = "{{app_name}}_lib", target-cfg deps, release profile
    ├── Cargo.lock                # commit (binary crate)
    ├── build.rs                  # links Accelerate/Metal (macOS), user32 (Windows), pthread/m (Linux)
    ├── tauri.conf.json           # productName, identifier, bundle, plugins, windows
    ├── tauri.local-no-updater.conf.json  # (optional) local-only overlay disabling updater
    ├── Info.plist                # macOS bundle id + permission usage descriptions
    ├── entitlements.plist        # macOS hardened-runtime entitlements
    ├── icons/
    │   ├── icon.png              # 1024x1024 source
    │   ├── icon.ico              # Windows
    │   ├── icon.icns             # macOS
    │   ├── 32x32.png
    │   ├── 128x128.png
    │   └── 128x128@2x.png
    ├── capabilities/
    │   └── default.json          # permissions for the "main" window
    ├── binaries/                 # (optional) externalBin entries — ffmpeg, sidecar, etc.
    ├── src/
    │   ├── main.rs               # #![cfg_attr(not(debug_assertions), windows_subsystem = "windows")] + macOS embed_plist + fn main()
    │   ├── lib.rs                # pub mod ...; pub use ...; pub fn run() { tauri::Builder... }
    │   ├── commands/
    │   │   ├── mod.rs            # pub mod ...; pub use *;
    │   │   ├── system.rs         # generic: write_file, dialogs, notifications
    │   │   └── <domain>.rs       # one file per cohesive command set
    │   ├── state/
    │   │   └── mod.rs            # pub struct AppState { app_handle, settings, ... }
    │   ├── storage/
    │   │   └── mod.rs            # get_app_data_dir, get_storage_path, load_json, save_json, ids, timestamps
    │   ├── settings/
    │   │   ├── mod.rs            # Settings struct + AppHandleSettings extension trait
    │   │   ├── defaults.rs       # impl Default for Settings + sub-settings
    │   │   ├── storage.rs        # load_settings, save_settings, deserialize_settings (with migrations)
    │   │   └── commands.rs       # get_settings, save_settings_command, reset_settings_command
    │   ├── platform/
    │   │   ├── mod.rs            # re-exports + #[cfg(target_os)] gated module decls
    │   │   ├── traits.rs         # e.g. PermissionChecker, FileOpener, OverlayWindowBuilder — one trait per OS-specific behavior
    │   │   ├── macos.rs          # #[cfg(target_os = "macos")] impls
    │   │   ├── windows.rs        # #[cfg(target_os = "windows")] impls
    │   │   ├── linux.rs          # #[cfg(target_os = "linux")] impls
    │   │   └── wrappers.rs       # Send + Sync wrappers managed in Tauri State
    │   ├── error/
    │   │   └── mod.rs            # into_string_err! macro, ResultExt trait
    │   ├── encryption/           # (optional)
    │   │   └── mod.rs            # AES-256-GCM + Argon2id + machine-bound salt
    │   ├── tray.rs               # (optional) tray icon menu, click events
    │   └── <domain>/             # one folder per major feature area
    │       ├── mod.rs
    │       └── ...
    └── tests/                    # cargo integration tests (one binary per file)
        ├── common/
        │   └── mod.rs            # shared test helpers (tempfile fixtures, mock builders)
        ├── system_test.rs
        ├── storage_test.rs
        ├── settings_test.rs
        └── <domain>_test.rs
```

## Why this shape

### `src-tauri/src/` is modular, not monolithic

A flat `src-tauri/src/main.rs` + huge `lib.rs` becomes unmaintainable past ~1500 lines. Splitting by feature folder (`export/`, `history/`, `sync/`, …) keeps related code together and lets `cargo test --test <name>` target one slice. The pattern enforces "one purpose per module" by making bloated modules awkward — you can't easily add a tenth file to a folder that's already named for something specific.

### `commands/` is its own module, not scattered across feature folders

Tauri commands are an **IPC boundary**, not a feature concern. Keeping them all under `commands/` means:
- One place to look when grepping for "what can the frontend call?"
- `tauri::generate_handler![...]` registration is a single, reviewable list
- Capability scopes line up with command modules
- Feature modules (`audio`, `history`) can change internals without touching the frontend API

Commands are thin: they parse inputs, call into a feature module, convert errors to `String`, and return. **No business logic in command bodies.**

### `state/`, `storage/`, `settings/` are separate

- **`state/`**: in-memory shared state (the `AppState` managed by Tauri). Lives only while the app runs.
- **`storage/`**: disk persistence utilities (`load_json`, `save_json`, paths, IDs, timestamps). The shared file-I/O layer that every module uses.
- **`settings/`**: the specific shape of `settings.json` (with serde derives, migrations, defaults). Built on top of `storage/`.

Conflating these leads to "settings holds the app handle" coupling that breaks tests.

### `platform/` uses traits + `#[cfg(target_os = "...")]`, not `cfg!()` checks

Anti-pattern: a command body that branches on `cfg!(target_os = "macos")`. Every command grows the branch count, tests have to mock the OS, and platform-specific dependencies leak across the codebase.

Pattern: define a trait in `platform/traits.rs` (`PermissionChecker`, `FileOpener`, `AutostartManager`). Implement it in `platform/macos.rs`, `windows.rs`, `linux.rs` (each gated with `#[cfg(target_os = "...")]`). Expose `Send + Sync` wrappers via `platform/wrappers.rs` that Tauri's `State<>` can manage. Commands receive `State<'_, PlatformPermissionChecker>` and never see `cfg!`.

Tests can then assert `Send + Sync` on the wrappers and substitute mock impls.

### `tests/common/mod.rs` is one file per integration binary

Cargo compiles each file in `tests/` as a separate binary. That means `tests/audio_test.rs` and `tests/history_test.rs` cannot share helpers via a normal module — they need `common/mod.rs` referenced from both.

```rust
// tests/audio_test.rs
mod common;
use common::*;
```

### Capability files per window

Tauri 2 capabilities are scoped per window. `capabilities/default.json` covers the `main` window. Auxiliary windows (overlay, settings popup, tray panel) get their own capability files. This matters because each window should only have the permissions it actually uses — a transparent overlay window does not need `fs:allow-write-file`.

### Icons are in `src-tauri/icons/`, not `src/assets/`

The frontend bundle doesn't ship the icons — Tauri's bundler reads them from `src-tauri/icons/` at build time and embeds them in the platform-specific installer. Keeping them in `src/` confuses both Vite and Tauri.

## Dependency rules (enforced)

- `src-tauri/src/commands/**` may call into `state/`, `settings/`, `storage/`, `platform/`, and any `<domain>/`. The reverse is forbidden.
- `src-tauri/src/<domain>/**` may use `storage/` and `platform::traits::*`, but **must not** depend on `commands/` or hold an `AppHandle` long-term. Pass `&AppHandle` where needed and return.
- `src-tauri/src/platform/macos.rs|windows.rs|linux.rs` are the **only** files that may contain `cfg!(target_os = "...")` checks at runtime. All other modules go through the trait.
- `src/hooks/use<Domain>.ts` compose `useTauriCommand` — frontend **components** never call `invoke()` directly.
- `src/components/**` may use hooks from `src/hooks/`, but a hook may **not** import from a component.

## Files you do NOT commit

Add to `.gitignore` and verify they're absent:

- `src-tauri/target/`
- `dist/`
- `node_modules/`
- `.env` (only `.env.example` is committed)
- `*.backup`, `*.orig`, `*.temp`, `*.rej` (WIP / merge-conflict artefacts)
- `src-tauri/binaries/*` if those are downloaded at build time by CI (commit a `.gitkeep` instead)
- Generated icons output (`icons/icon.icns`, `icons/icon.ico` if you regenerate from `icon.png` each build — but most projects DO commit these, so it's a project-by-project call)

If you find `lib.rs.backup` / `macos.rs.orig` / `lib.rs.temp` in `src-tauri/src/`, that's a sign the previous developer was hand-merging in a way the VCS should have handled. Delete them; don't ship them.
