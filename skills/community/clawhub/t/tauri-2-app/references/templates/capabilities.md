# `src-tauri/capabilities/default.json`

Capabilities are Tauri 2's permission system. The frontend can only invoke a plugin command if a capability file grants that exact scope to the current window.

```json
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

    "fs:allow-read-file",
    "fs:allow-write-file",

    "notification:default",
    "notification:allow-show",
    "notification:allow-is-permission-granted",
    "notification:allow-request-permission",

    "global-shortcut:allow-is-registered",
    "global-shortcut:allow-register",
    "global-shortcut:allow-unregister",

    "process:allow-restart",

    "updater:default"
  ]
}
```

## Per-window capability files

If the app has multiple windows (overlay, settings popup, tray panel), each one gets its own capability file scoped to just that window's needs. A transparent overlay does not need `fs:allow-write-file` or `dialog:*` — it usually only emits events.

```json
// capabilities/overlay.json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "overlay",
  "description": "Capability for the overlay window",
  "windows": ["overlay"],
  "permissions": [
    "core:default"
  ]
}
```

## Why granular over blanket

- **Granular permissions = audit surface.** The capability file is the single document a security reviewer reads to learn "what can the frontend do?". `"core:default"` only is OK; `"fs:default"` without listing specific actions is suspect.
- **Plugin updates can widen `default`.** If a plugin's `default` permission set expands in a new version, your app silently inherits the new permissions. Listing exact actions pins the contract.
- **Frontend reflection breaks at the boundary.** A malicious or buggy frontend can call any command listed in the handler, but the capability file is checked before the call ever reaches Rust. Tight capabilities are a defense in depth.

## Reading the schema

The `$schema` reference points at `../gen/schemas/desktop-schema.json`, which Tauri generates on `cargo build`. Editors with JSON schema support (VS Code, JetBrains) will autocomplete valid permission names and show inline docs for each one. If the file is missing, run `cd src-tauri && cargo build` once to generate it.

## Don't ship `"core:*"` glob

`"core:*"` exists but matches every core permission, including ones the app doesn't use. If a future Tauri release adds a new core permission (e.g. clipboard read), your app silently gains it. Either list the specific `core:allow-*` permissions, or use `"core:default"` (which is curated and stable across versions).
