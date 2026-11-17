# Security: Capabilities, Permissions, Scopes, CSP

**Sources:**
- https://v2.tauri.app/security/
- https://github.com/tauri-apps/tauri-docs/blob/v2/src/content/docs/security/permissions.mdx
- https://github.com/tauri-apps/tauri-docs/blob/v2/src/content/docs/learn/Security/capabilities-for-windows-and-platforms.mdx
- https://deepwiki.com/tauri-apps/tauri-docs/5.8-security-and-capabilities-system
- https://v2.tauri.app/reference/acl/capability/ (capability JSON schema)

This is the single biggest architectural change from Tauri v1 → v2, and the most common source of "why doesn't this work" reports. **Internalize this before touching capability files.**

## The model, in one sentence

Tauri v2 is **default-deny**: a webview window can call *zero* commands and access *zero* plugin APIs unless a capability file explicitly grants it, scoped to that window's label.

Three layers:

1. **Permissions** — named, reusable grants (e.g. `fs:allow-read-file`, `core:default`). Defined by Tauri core and by each plugin; you can also define custom ones for your own commands.
2. **Capabilities** — JSON files under `src-tauri/capabilities/*.json` that say "these permissions apply to these windows."
3. **Scopes** — fine-grained restriction *within* a permission (e.g. which paths `fs:allow-read-file` may actually touch), expressed as allow/deny path/URL patterns.

## Capability file anatomy

```json
// src-tauri/capabilities/default.json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "description": "Capabilities for the main window",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "fs:default",
    "dialog:default",
    "shell:allow-open"
  ]
}
```

- `identifier`: unique name for this capability set (referenced from `tauri.conf.json` if not auto-loaded).
- `windows`: glob-capable list of window **labels** this applies to. `["*"]` = all windows — convenient, but defeats the purpose of per-window isolation; prefer being explicit.
- `permissions`: array of permission identifiers OR inline objects for scoped grants (see below). All `.json`/`.toml` files under `src-tauri/capabilities/` are auto-loaded unless you've restricted loading via `tauri.conf.json > app > security > capabilities`.
- By default all capability files in the folder are enabled. If you want to *selectively* enable capabilities (e.g. per build target), list them explicitly in `tauri.conf.json`.

### Scoped / fine-grained permissions

Most `*:default` permission sets are broad. For anything security-sensitive, grant the specific sub-permission and attach a scope:

```json
{
  "identifier": "default",
  "windows": ["main"],
  "permissions": [
    {
      "identifier": "fs:allow-read",
      "allow": [{ "path": "$APPDATA/**" }, { "path": "$DOCUMENT/**" }]
    },
    {
      "identifier": "fs:allow-write",
      "allow": [{ "path": "$APPDATA/**" }]
    }
  ]
}
```

Scope path variables: `$APP`, `$APPDATA`, `$APPCACHE`, `$APPLOG`, `$APPLOCALDATA`, `$AUDIO`, `$CACHE`, `$CONFIG`, `$DATA`, `$LOCALDATA`, `$DESKTOP`, `$DOCUMENT`, `$DOWNLOAD`, `$EXE`, `$FONT`, `$HOME`, `$PICTURE`, `$PUBLIC`, `$RUNTIME`, `$TEMPLATE`, `$VIDEO`, `$RESOURCE`, `$TEMP`, plus glob patterns (`**`, `*`).

**Deny always wins over allow.** If a path matches both an `allow` and a `deny` scope entry, it's denied. Use this for carve-outs: allow `$HOME/**`, deny `$HOME/.ssh/**`.

### Sidecar / shell argument allowlisting

`shell:allow-execute` scoped grants restrict which binary + which argument shapes are runnable — critical for anything that spawns processes:

```json
{
  "identifier": "shell:allow-execute",
  "allow": [
    {
      "name": "binaries/my-sidecar",
      "sidecar": true,
      "cmd": "",
      "args": ["--serve", { "validator": "\\d+" }]
    }
  ]
}
```

`args: true` allows any arguments (needed for things like an interactive terminal where argument values are inherently dynamic — but note the **executable path itself stays pinned**, which is what actually prevents command-injection-via-executable-swap). `args: false` disables all arguments. An explicit array pins the exact sequence, with `{ "validator": "<regex>" }` entries for dynamic-but-constrained values like file paths, ports, or URLs.

### Multi-window capability separation

Give each window only what it needs — don't reuse one blanket capability across a main window and, say, a lightweight "About" window:

```json
// capabilities/filesystem.json — only the main window needs FS
{ "identifier": "fs-read-home", "windows": ["main"], "permissions": ["fs:allow-home-read"] }

// capabilities/dialog.json — both windows can show dialogs
{ "identifier": "dialogs", "windows": ["main", "about"], "permissions": ["dialog:default"] }
```

If you add a new window (settings, onboarding, a detail view) and forget to add its label to the relevant capability files, calls from that window fail even though the *same command* works fine from `main`. This is the single most common multi-window bug.

## Permission namespacing

- Tauri **core** permissions have no prefix or use `core:` (e.g. `core:default`, `core:window:allow-set-title`).
- **Plugin** permissions are namespaced by plugin crate name minus the `tauri-plugin-` prefix, auto-prepended at compile time: `fs:allow-read-file`, `shell:allow-execute`, `dialog:allow-open`, `updater:allow-check`, `notification:default`.
- Installing a plugin's Cargo crate + npm package does **not** grant it any permissions — you must add its permission identifiers to a capability file yourself. There is no compile-time check for this; a missing permission surfaces as a runtime IPC rejection or a silently-failing frontend call. If you just added a plugin and its API "does nothing," check this before debugging the plugin itself.

## Content Security Policy (CSP)

```json
// tauri.conf.json
{
  "app": {
    "security": {
      "csp": "default-src 'self'; img-src 'self' data: https:; style-src 'self' 'unsafe-inline'"
    }
  }
}
```

- CSP is enforced by the webview and restricts what content it can *load/execute*, independent of capabilities (which restrict what it can *call into Tauri*). Both layers matter — a wide-open CSP plus locked-down capabilities still lets injected/XSS'd content read arbitrary DOM state and hit any external network endpoint the CSP allows.
- `"csp": null` **disables CSP entirely**. Only acceptable transiently during local debugging — never ship it.
- Common tightening: avoid `'unsafe-inline'`/`'unsafe-eval'` in `script-src` if your frontend build allows it (most modern bundlers do with a bit of config); it's usually needed for `style-src` with CSS-in-JS libraries.

## `remote` access (loading non-local origins)

If a capability needs to apply to a window loading a **remote** URL (e.g. `http://localhost:*` in dev, or an actual external domain), declare it explicitly:

```json
{
  "identifier": "default",
  "windows": ["main"],
  "remote": { "urls": ["http://localhost:*/**"] },
  "permissions": ["core:default", "dialog:default"]
}
```

Without a matching `remote.urls` entry, a window navigated to a non-`tauri://`/`https://tauri.localhost` origin loses its capability grants even if the window label matches — this is intentional, to stop a compromised/malicious remote page from inheriting your app's IPC access.

## The isolation pattern (advanced / high-security apps)

For apps loading any untrusted or remote content, Tauri supports an **isolation pattern**: a secure, sandboxed intermediary JS context that inspects/can-reject every IPC message before it reaches Rust, even if the main frontend context is fully compromised (e.g. via a supply-chain-compromised dependency). Reach for this only for genuinely high-risk apps (embedding third-party/remote web content) — for a typical local-first app with a first-party frontend it's not necessary, and capabilities + CSP are sufficient.

## Practical review checklist (use this when reviewing someone's Tauri v2 app)

- [ ] No capability file grants `"windows": ["*"]` with `*:default` blanket permissions unless genuinely justified.
- [ ] Every window label actually created in code (`WebviewWindowBuilder`, `tauri.conf.json` window configs) has matching capability coverage.
- [ ] Filesystem/shell/http permissions are scoped (allow-list of paths/commands/domains), not left at unscoped `*:default` where a scoped variant exists.
- [ ] `security.csp` is set and not `null` in the shipped config.
- [ ] Sidecar `shell:allow-execute` grants pin the executable name/path and constrain arguments (validator regex or fixed list), not blanket `args: true`, unless the use case genuinely needs arbitrary args (e.g. embedded terminal).
- [ ] Any window that loads a remote/dev-server origin has an explicit `remote.urls` entry, not an accidental origin-based capability leak.
