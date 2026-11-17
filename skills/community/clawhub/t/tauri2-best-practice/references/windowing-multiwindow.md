# Windows, Webviews & Multi-Window Management

**Sources:**
- https://deepwiki.com/tauri-apps/tauri/2.3-window-and-webview-management
- https://docs.rs/tauri/latest/tauri/webview/struct.WebviewWindowBuilder.html
- https://v2.tauri.app/learn/mobile-multiwindow/ (mobile-specific behavior)
- https://github.com/orgs/tauri-apps/discussions/9601 (v1→v2 API rename)

## Window vs Webview vs WebviewWindow

Tauri v2 explicitly separates these (a v1→v2 conceptual change, in preparation for multiple webviews per native window):

- **Window**: the native OS window frame (title bar, resize handles, OS-level chrome).
- **Webview**: the content container that renders web content. On desktop today it's typically 1:1 with a window; the architecture allows multiple webviews inside one window.
- **WebviewWindow**: the composite convenience type — a window with exactly one attached webview — used for the overwhelming majority of Tauri apps. When you see `WebviewWindowBuilder` in v2 docs, this is what v1's `WindowBuilder` became.

Every window/webview has a unique string **label**, chosen when created. Labels are how you look windows up later (`get_window`/`get_webview_window`, capability `windows` matching, targeted `emit_to`).

## Creating a window (Rust)

```rust
use tauri::{Manager, WebviewWindowBuilder, WebviewUrl};

#[tauri::command]
async fn open_settings(app: tauri::AppHandle) -> Result<(), String> {
    // async fn — see SKILL.md rule 7: sync window creation inside a command
    // handler can deadlock on Windows due to a WebView2 issue.
    WebviewWindowBuilder::new(&app, "settings", WebviewUrl::App("settings.html".into()))
        .title("Settings")
        .inner_size(600.0, 400.0)
        .resizable(true)
        .build()
        .map_err(|e| e.to_string())?;
    Ok(())
}
```

Building from an existing config entry (`tauri.conf.json`'s `app.windows` array), useful for a "reopen the main window" flow — but note labels must stay unique, so give the reopened/duplicated window a fresh label:

```rust
#[tauri::command]
async fn open_window_multiple(app: tauri::AppHandle) {
    let mut conf = app.config().app.windows.iter()
        .find(|c| c.label == "template-for-multiwindow").unwrap().clone();
    conf.label = format!("instance-{}", uuid_like_suffix());
    tauri::WebviewWindowBuilder::from_config(&app, &conf).unwrap().build().unwrap();
}
```

## Creating a window (frontend)

```ts
import { WebviewWindow } from '@tauri-apps/api/webviewWindow';

const settingsWindow = new WebviewWindow('settings', {
  url: 'settings.html',
  title: 'Settings',
  width: 600,
  height: 400,
});

settingsWindow.once('tauri://created', () => { /* window is ready */ });
settingsWindow.once('tauri://error', (e) => { /* creation failed, e.g. label collision */ });
```

Frontend-initiated window creation requires the `core:webview:allow-create-webview-window` permission in that window's capability file — see `references/security-capabilities.md`.

## Looking up existing windows

```rust
// Rust — requires `use tauri::Manager;`
let main = app.get_webview_window("main");
```
```ts
// Frontend
import { WebviewWindow } from '@tauri-apps/api/webviewWindow';
const main = await WebviewWindow.getByLabel('main');
```

## Cross-window communication

There's no shared in-memory frontend state across windows by default (each webview is its own JS context). Use one of:
1. **Events** (`emit_to(label, ...)` from Rust, or frontend `emit`/`listen`) — see `references/ipc-commands.md`.
2. **Rust-managed state as source of truth** — each window fetches/subscribes rather than windows talking peer-to-peer — see `references/state-management.md`.

## Capabilities are per-window-label

This bears repeating from the security reference because it's the top multi-window bug: adding a new window without adding its label to the relevant `capabilities/*.json` `windows` array means every `invoke()` from that new window fails, even for commands that work fine elsewhere. Always update capabilities in the same change that adds a window.

## Multi-window on mobile (Android/iOS)

Supported since Tauri v2, but behaves differently from desktop:

- Minimum: **Android 12L (API 32)+**, **iOS 13+**. Check availability at runtime with the `app.supportsMultipleWindows` API before assuming split-screen-style behavior.
- **Android**: a new window launches a separate Activity. On handset-sized screens (no split layout), it's pushed onto the activity back stack — pressing Back returns to the previous activity rather than "closing a floating window."
- **iOS**: opening a window creates a new Scene; on iPhone this typically *replaces* the current UI rather than showing both simultaneously. True concurrent multi-window is realistically an iPad (Stage Manager) experience.
- Both platforms require the `core:webview:allow-create-webview-window` capability permission, same as desktop.
- Platform-specific builder options exist for activity/scene relationships: `createdByActivityName` (Android — controls which activity stack the new window's activity belongs to, important for split-screen rules) and `requestedBySceneIdentifier` (iOS — which UIScene is requesting the new scene; defaults to the foreground scene).

**Design implication:** don't assume a "settings modal as a second window" pattern translates well to mobile — on handsets it behaves like navigation (a full-screen replacement/back-stack push), not a floating dialog. Consider an in-webview modal/route instead for content that must feel like a dialog on mobile, and reserve real second windows for desktop-only or genuinely-multi-screen (tablet) flows.

## System tray & menus (desktop)

Not strictly "windowing" but adjacent and commonly needed alongside multi-window apps — tray icons and native menus are configured via `tauri::menu` and `tauri::tray` modules (`Menu`, `Submenu`, `MenuItem`, `TrayIconBuilder`), registered in `setup()`, with menu-event and tray-event handlers wired via `on_menu_event`/`on_tray_icon_event` on the builder. If the task needs this, search current docs (`v2.tauri.app`) for the specific menu/tray API shape, since it's one of the more actively-iterated corners of v2 — don't rely purely on memory here.
