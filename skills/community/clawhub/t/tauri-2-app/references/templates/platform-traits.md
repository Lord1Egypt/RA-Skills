# `src-tauri/src/platform/` — Trait-based platform abstractions

Pattern: define traits in `platform/traits.rs`, implement per-OS in `macos.rs|windows.rs|linux.rs` gated with `#[cfg(target_os = "...")]`, expose `Send + Sync` wrappers via `wrappers.rs` for Tauri State. Commands receive `State<'_, PlatformXxx>` — they never see `cfg!`.

## `platform/traits.rs`

```rust
//! Platform trait contracts. Implementations live in `macos.rs`, `windows.rs`,
//! `linux.rs` and are gated with `#[cfg(target_os = "...")]`.

use std::path::Path;

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct PermissionStatus {
    pub is_macos: bool,
    pub accessibility: bool,
    pub microphone: bool,
    pub notification: bool,
    pub all_granted: bool,
}

#[derive(Debug, thiserror::Error)]
pub enum PlatformError {
    #[error("command execution error: {0}")]
    CommandError(String),
    #[error("unsupported on this platform")]
    Unsupported,
}

/// Check OS-level permissions (mic, accessibility, notifications).
pub trait PermissionChecker: Send + Sync {
    fn check_accessibility(&self) -> bool;
    fn check_microphone(&self) -> bool;
    fn check_notification(&self) -> bool;
    fn get_status(&self) -> PermissionStatus;
    fn open_system_settings(&self, permission_type: &str) -> Result<(), String>;
}

/// Open files/folders in OS-default apps.
pub trait FileOpener: Send + Sync {
    fn open_in_default_app(&self, path: &Path) -> Result<(), String>;
    fn open_in_file_manager(&self, path: &Path) -> Result<(), String>;
    fn open_in_text_editor(&self, path: &Path) -> Result<(), String>;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn permission_status_round_trips() {
        let s = PermissionStatus {
            is_macos: true, accessibility: true, microphone: false,
            notification: true, all_granted: false,
        };
        let json = serde_json::to_string(&s).unwrap();
        let back: PermissionStatus = serde_json::from_str(&json).unwrap();
        assert_eq!(s.microphone, back.microphone);
    }
}
```

## `platform/macos.rs` (sketch)

```rust
#![cfg(target_os = "macos")]

use std::path::Path;
use std::process::Command;
use crate::platform::traits::{FileOpener, PermissionChecker, PermissionStatus};

pub struct MacOsPlatform;

impl PermissionChecker for MacOsPlatform {
    fn check_accessibility(&self) -> bool {
        // Use AXIsProcessTrusted via security-framework or objc bindings.
        // For brevity, this stub assumes a helper exists.
        unimplemented!("call AXIsProcessTrusted")
    }
    fn check_microphone(&self) -> bool {
        unimplemented!("call AVCaptureDevice.authorizationStatus")
    }
    fn check_notification(&self) -> bool { true }
    fn get_status(&self) -> PermissionStatus {
        PermissionStatus {
            is_macos: true,
            accessibility: self.check_accessibility(),
            microphone: self.check_microphone(),
            notification: self.check_notification(),
            all_granted: false, // compute from above
        }
    }
    fn open_system_settings(&self, kind: &str) -> Result<(), String> {
        let url = match kind {
            "accessibility" => "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility",
            "microphone" => "x-apple.systempreferences:com.apple.preference.security?Privacy_Microphone",
            _ => return Err(format!("unknown permission: {}", kind)),
        };
        Command::new("open").arg(url).spawn()
            .map(|_| ()).map_err(|e| e.to_string())
    }
}

impl FileOpener for MacOsPlatform {
    fn open_in_default_app(&self, path: &Path) -> Result<(), String> {
        Command::new("open").arg(path).spawn().map(|_| ()).map_err(|e| e.to_string())
    }
    fn open_in_file_manager(&self, path: &Path) -> Result<(), String> {
        Command::new("open").arg("-R").arg(path).spawn().map(|_| ()).map_err(|e| e.to_string())
    }
    fn open_in_text_editor(&self, path: &Path) -> Result<(), String> {
        Command::new("open").arg("-t").arg(path).spawn().map(|_| ()).map_err(|e| e.to_string())
    }
}
```

`platform/windows.rs` and `platform/linux.rs` follow the same shape with `Command::new("explorer")` / `Command::new("xdg-open")` etc.

## `platform/wrappers.rs`

Wrappers exist so Tauri's `State<T>` (which requires `T: Send + Sync`) can hold the platform impl regardless of OS.

```rust
use crate::platform::traits::{FileOpener, PermissionChecker, PermissionStatus};
use std::path::Path;

pub struct PlatformPermissionChecker {
    #[cfg(target_os = "macos")] inner: super::MacOsPlatform,
    #[cfg(target_os = "windows")] inner: super::WindowsPlatform,
    #[cfg(target_os = "linux")] inner: super::LinuxPlatform,
}

impl PlatformPermissionChecker {
    pub fn new() -> Self {
        Self {
            #[cfg(target_os = "macos")] inner: super::MacOsPlatform,
            #[cfg(target_os = "windows")] inner: super::WindowsPlatform,
            #[cfg(target_os = "linux")] inner: super::LinuxPlatform,
        }
    }
}

impl PermissionChecker for PlatformPermissionChecker {
    fn check_accessibility(&self) -> bool { self.inner.check_accessibility() }
    fn check_microphone(&self) -> bool { self.inner.check_microphone() }
    fn check_notification(&self) -> bool { self.inner.check_notification() }
    fn get_status(&self) -> PermissionStatus { self.inner.get_status() }
    fn open_system_settings(&self, k: &str) -> Result<(), String> {
        self.inner.open_system_settings(k)
    }
}

pub struct PlatformFileOpener { /* same shape */ }
// ... impl FileOpener for PlatformFileOpener ...
```

## `platform/mod.rs`

```rust
pub mod traits;
pub mod wrappers;

#[cfg(target_os = "macos")] mod macos;
#[cfg(target_os = "windows")] mod windows;
#[cfg(target_os = "linux")] mod linux;

#[cfg(target_os = "macos")] pub use macos::MacOsPlatform;
#[cfg(target_os = "windows")] pub use windows::WindowsPlatform;
#[cfg(target_os = "linux")] pub use linux::LinuxPlatform;

pub use traits::{PermissionChecker, PermissionStatus, FileOpener};
pub use wrappers::{PlatformPermissionChecker, PlatformFileOpener};

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn wrappers_are_send_sync() {
        fn assert_send_sync<T: Send + Sync>() {}
        assert_send_sync::<PlatformPermissionChecker>();
        assert_send_sync::<PlatformFileOpener>();
    }
}
```

## Usage in `lib.rs`

```rust
.setup(|app| {
    app.manage(PlatformPermissionChecker::new());
    app.manage(PlatformFileOpener::new());
    Ok(())
})
```

## Usage in commands

```rust
#[tauri::command]
pub fn open_in_finder(
    opener: tauri::State<'_, PlatformFileOpener>,
    path: String,
) -> Result<(), String> {
    use crate::platform::FileOpener;
    opener.open_in_file_manager(std::path::Path::new(&path))
}
```

The command is **portable** — no `cfg!` checks, no `#[cfg(target_os = "...")]` attributes, no platform-specific imports.

## Why this is worth the structural overhead

- **Adding a fourth OS** (BSD, mobile) is one new `platform/<os>.rs` file plus a `#[cfg]` arm in the wrapper. Commands don't change.
- **Mocking in tests** is trivial — define a `MockPermissionChecker` that implements `PermissionChecker`, register it in the test setup via `app.manage(...)`.
- **Audit surface** — all OS-specific code is in `platform/<os>.rs`. A security review of "what does the macOS build do differently?" reads one file.
- **Build times** — Cargo skips compiling `platform/windows.rs` on macOS targets entirely (the `#[cfg]` gate). No wasted work.
