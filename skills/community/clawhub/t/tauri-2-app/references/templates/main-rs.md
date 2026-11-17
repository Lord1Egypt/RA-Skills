# `src-tauri/src/main.rs`

The tiny shim that calls into `lib.rs`. Keep it short — all logic lives in `lib.rs`.

```rust
// Prevents additional console window on Windows in release. DO NOT REMOVE.
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

#[cfg(target_os = "macos")]
embed_plist::embed_info_plist!("../Info.plist");

fn main() {
    {{app_name}}_lib::run()
}
```

## Why

- `#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]` — Without this attribute, Windows release builds open a console window behind the Tauri window. Debug builds keep their console for `println!`.
- `embed_plist::embed_info_plist!` — Ensures macOS standalone binaries (run directly, not through the `.app` bundle) still carry the plist. Gated to macOS via `#[cfg(target_os = "macos")]`.
- `{{app_name}}_lib::run()` — The `_lib` suffix on the crate name avoids a Windows linker conflict between the bin and lib targets. The actual function is defined in `lib.rs`.
