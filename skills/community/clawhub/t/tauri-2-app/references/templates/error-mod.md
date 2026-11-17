# `src-tauri/src/error/mod.rs`

The shared error-conversion utilities for Tauri commands. Internal APIs use `thiserror` enums; commands convert at the IPC boundary with `into_string_err!` or `ResultExt`.

```rust
//! Error handling utilities — keeps command boilerplate tight.

/// Convert any error to a String at the call site.
///
/// ```ignore
/// let r = into_string_err!(some_fallible());                 // "<err>"
/// let r = into_string_err!(some_fallible(), "Failed to X");  // "Failed to X: <err>"
/// let r = into_string_err!(some_fallible(), "Loading {}", path);
/// ```
#[macro_export]
macro_rules! into_string_err {
    ($expr:expr) => { $expr.map_err(|e| e.to_string()) };
    ($expr:expr, $msg:expr) => { $expr.map_err(|e| format!("{}: {}", $msg, e)) };
    ($expr:expr, $fmt:expr, $($arg:tt)*) => {
        $expr.map_err(|e| format!("{}: {}", format!($fmt, $($arg)*), e))
    };
}

/// `?`-propagating variant.
///
/// ```ignore
/// fn cmd() -> Result<T, String> {
///     let x = try_into_string_err!(some_fallible());
///     Ok(x)
/// }
/// ```
#[macro_export]
macro_rules! try_into_string_err {
    ($expr:expr) => { $expr.map_err(|e| e.to_string())? };
    ($expr:expr, $msg:expr) => { $expr.map_err(|e| format!("{}: {}", $msg, e))? };
}

/// Extension trait so you can write `result.into_string()` / `.into_string_msg("...")`.
pub trait ResultExt<T, E>: Sized {
    fn into_string(self) -> Result<T, String>;
    fn into_string_msg(self, msg: &str) -> Result<T, String>;
}

impl<T, E: std::fmt::Display> ResultExt<T, E> for Result<T, E> {
    fn into_string(self) -> Result<T, String> {
        self.map_err(|e| e.to_string())
    }
    fn into_string_msg(self, msg: &str) -> Result<T, String> {
        self.map_err(|e| format!("{}: {}", msg, e))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn macro_no_context() {
        fn f() -> Result<(), &'static str> { Err("boom") }
        let r: Result<(), String> = into_string_err!(f());
        assert_eq!(r.unwrap_err(), "boom");
    }

    #[test]
    fn macro_with_context() {
        fn f() -> Result<(), &'static str> { Err("boom") }
        let r: Result<(), String> = into_string_err!(f(), "Failed");
        assert_eq!(r.unwrap_err(), "Failed: boom");
    }

    #[test]
    fn ext_trait() {
        fn f() -> Result<(), &'static str> { Err("boom") }
        let r = f().into_string_msg("Context");
        assert_eq!(r.unwrap_err(), "Context: boom");
    }
}
```

## How to use it

Define rich internal error types with `thiserror`:

```rust
// src-tauri/src/settings/mod.rs
#[derive(Debug, thiserror::Error)]
pub enum SettingsError {
    #[error("settings file not found: {0}")]
    NotFound(std::path::PathBuf),
    #[error("invalid JSON: {0}")]
    InvalidJson(#[from] serde_json::Error),
    #[error("I/O error: {0}")]
    Io(#[from] std::io::Error),
}

pub fn load(app: &AppHandle) -> Result<Settings, SettingsError> { /* ... */ }
```

Then convert at the command boundary:

```rust
// src-tauri/src/commands/settings.rs
use crate::error::ResultExt;

#[tauri::command]
pub fn get_settings(app: tauri::AppHandle) -> Result<Settings, String> {
    crate::settings::load(&app).into_string_msg("Failed to load settings")
}
```

## Why two flavors

- `into_string_err!` is a macro because some `?`-heavy command bodies are cleaner with the macro form.
- `ResultExt` is a trait because it composes — `something.into_string().map(|v| ...)` flows naturally in chains.

Pick the one that reads better at the call site. Don't bikeshed; consistency within a single module matters more than which form you chose globally.

## Why convert at the boundary, not throughout

If every internal function returned `Result<T, String>`:
- Type information is lost (was it I/O? parsing? permissions?).
- Adding `#[from]` conversions becomes impossible.
- Tests that assert on error variants can't.
- Callers can't decide to handle some errors and propagate others — every string looks the same.

Keep `thiserror` types as long as possible, convert only when crossing into a `#[tauri::command]`.
