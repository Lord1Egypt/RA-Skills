# `src-tauri/Cargo.toml`

Pin **Rust edition** to `2021`. Resolve crate **versions** at scaffold time via crates.io / context7 — never hard-paste a version into a generated file. The version markers below are placeholders.

```toml
[package]
name = "{{app_name}}"
version = "0.1.0"
description = "{{description}}"
authors = ["{{author}}"]
license = "MIT"
edition = "2021"
default-run = "{{app_name}}"

[lib]
# The `_lib` suffix avoids a Windows linker conflict between the bin and lib targets.
# See https://github.com/rust-lang/cargo/issues/8519
name = "{{app_name}}_lib"
crate-type = ["staticlib", "cdylib", "rlib"]

[[bin]]
name = "{{app_name}}"
path = "src/main.rs"

[build-dependencies]
tauri-build = { version = "<latest 2.x>", features = [] }

[dependencies]
# Tauri core (2.x). Add features as needed: "tray-icon", "macos-private-api"
tauri = { version = "<latest 2.x>", features = [] }

# Tauri plugins — only those actually wired in lib.rs
tauri-plugin-opener = "<latest 2.x>"
tauri-plugin-dialog = "<latest 2.x>"
tauri-plugin-fs = "<latest 2.x>"
tauri-plugin-notification = "<latest 2.x>"
tauri-plugin-global-shortcut = "<latest 2.x>"
tauri-plugin-single-instance = "<latest 2.x>"
# tauri-plugin-updater = "<latest 2.x>"   # only if updater is wired
# tauri-plugin-process = "<latest 2.x>"

# Serialization
serde = { version = "<latest 1.x>", features = ["derive"] }
serde_json = "<latest 1.x>"

# Errors
thiserror = "<latest>"
anyhow = "<latest>"

# Async runtime
tokio = { version = "<latest 1.x>", features = ["sync", "rt-multi-thread", "macros"] }

# Logging
tracing = "<latest>"
tracing-subscriber = { version = "<latest>", features = ["env-filter"] }

# Date/time — DO NOT hand-roll
chrono = "<latest>"

# Paths
dirs = "<latest>"

# Optional: encrypted secrets at rest
aes-gcm = "<latest>"
argon2 = "<latest>"
base64 = "<latest>"
rand = "<latest>"

# macOS-specific
[target.'cfg(target_os = "macos")'.dependencies]
embed_plist = "<latest>"
# Add when used:
# security-framework = "<latest>"
# cocoa = "<latest>"
# objc = "<latest>"
# core-graphics = "<latest>"

# Windows-specific
[target.'cfg(target_os = "windows")'.dependencies]
# Add only the windows-sys features actually referenced in code:
# windows-sys = { version = "<latest>", features = [
#     "Win32_Foundation",
#     "Win32_System_ProcessStatus",
# ] }

# Linux-specific
[target.'cfg(target_os = "linux")'.dependencies]
# machine-uid = "<latest>"   # only if encryption module needs a stable machine ID

# Release profile — full LTO + smaller binary
[profile.release]
lto = "fat"
codegen-units = 1
opt-level = 3
strip = true
panic = "abort"

# Dev profile — light optimization keeps debug builds bearable
[profile.dev]
opt-level = 1

[dev-dependencies]
tempfile = "<latest>"          # temporary fixtures
assert_matches = "<latest>"
pretty_assertions = "<latest>" # readable diffs in test failures
tokio-test = "<latest>"        # async test helpers
# mockall = "<latest>"         # only if trait-based mocking is set up
# proptest = "<latest>"        # only if property tests are in scope
```

## Why

- **`[lib].name = "{{app_name}}_lib"`** — Without the `_lib` suffix, Windows fails to link because the bin and lib targets generate conflicting symbols.
- **`crate-type = ["staticlib", "cdylib", "rlib"]`** — `cdylib` is for mobile (Android/iOS) targets, `staticlib` for some embedded uses, `rlib` for integration tests. Tauri's mobile work needs all three.
- **Target-specific `[target.'cfg(...)'.dependencies]`** — Platform-only crates (`cocoa`, `windows-sys`) only compile on the matching target. The `[target.cfg(...)]` syntax means a `cargo build` on a different OS skips them entirely.
- **`tauri-plugin-single-instance` listed under regular deps** — It works cross-platform; the plugin internally handles per-OS specifics.
- **Release profile** — `lto = "fat"` enables cross-crate inlining (faster, smaller). `codegen-units = 1` is required for full LTO. `strip = true` drops symbols (~30% binary size reduction). `panic = "abort"` skips unwinding tables.
- **Dev profile `opt-level = 1`** — Cuts debug-build runtime by 2–3× vs. `opt-level = 0`, with only a minor compile-time hit. Especially noticeable for tests that exercise crypto or audio processing.
