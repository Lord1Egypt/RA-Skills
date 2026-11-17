# `src-tauri/src/lib.rs`

The single source of truth for module wiring, plugin registration, and command handler registration. Keep `run()` lean — defer initialization work to background threads.

```rust
// Module declarations
pub mod commands;
mod error;
mod platform;
mod settings;
mod state;
mod storage;
// add per-feature modules here: mod audio; mod history; ...

// Re-exports for integration tests
pub use settings::Settings;
pub use state::AppState;
pub use storage::{generate_id, get_app_data_dir, get_storage_path, load_json, save_json};
pub use error::ResultExt;

use tauri::Manager;
use tracing::info;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    // Initialize tracing FIRST so plugin init logs are captured
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::from_default_env()
                .add_directive(tracing::Level::INFO.into()),
        )
        .init();

    tauri::Builder::default()
        // Single-instance MUST register first so a second launch is intercepted
        // before any other plugin initializes resources.
        .plugin(tauri_plugin_single_instance::init(|app, _args, _cwd| {
            if let Some(window) = app.get_webview_window("main") {
                let _ = window.show();
                let _ = window.set_focus();
                let _ = window.unminimize();
            }
        }))
        .plugin(tauri_plugin_opener::init())
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_fs::init())
        .plugin(tauri_plugin_notification::init())
        .plugin(tauri_plugin_global_shortcut::Builder::new().build())
        .plugin(tauri_plugin_process::init())
        // .plugin(tauri_plugin_updater::Builder::new().build())  // enable if updater is wired
        .setup(|app| {
            info!("App setup starting");

            // Manage shared state
            let state = std::sync::Mutex::new(state::AppState::new());
            app.manage(state);

            // Load settings synchronously (small file, fast)
            let app_handle = app.handle().clone();
            let settings = settings::load_settings(&app_handle);
            if let Ok(mut s) = app.state::<std::sync::Mutex<state::AppState>>().lock() {
                s.app_handle = Some(app_handle.clone());
                s.settings = Some(settings);
            }

            // Heavy initialization on a background thread — keep .setup() fast
            // so the window appears immediately.
            std::thread::spawn(move || {
                // model load, audio device enumeration, etc.
                // emit progress back: let _ = app_handle.emit("init-progress", ...);
            });

            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            // System commands
            commands::write_file,
            commands::save_file_dialog,
            commands::open_file_dialog,
            // Settings commands
            settings::get_settings,
            settings::save_settings_command,
            settings::reset_settings_command,
            // Add per-domain commands here
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

## Why

- **Tracing initialized first** — Plugins log during their `init()` call. If `tracing_subscriber` registers later, those logs are silently dropped.
- **`tauri_plugin_single_instance::init` registers first** — The plugin's IPC hook needs to fire before any other plugin claims a resource (lock file, IPC socket, audio device). Registering it last is a known footgun.
- **`.setup()` is fast** — The window appears as soon as `.setup()` returns. Anything synchronous in there delays first paint. Synchronous settings load is OK (small JSON file); model loading / network calls are not.
- **`pub mod commands; mod error;` pattern** — `commands` is `pub` so integration tests can call individual commands directly. Domain modules (`error`, `state`) stay private with selective re-exports.
- **Re-exports for tests** — Integration tests in `src-tauri/tests/` import via `use {{app_name}}_lib::{Settings, AppState};`. Re-exporting at the crate root means tests don't need to know the internal module path.
- **`tauri::generate_handler!` is one list** — Tauri verifies the macro expansion at compile time. Splitting it across files isn't supported; keep all commands in one `generate_handler![...]` block.
