# Plugin Development & Sidecars

**Sources:**
- https://v2.tauri.app/develop/sidecar/
- https://v2.tauri.app/learn/sidecar-nodejs/
- https://v2.tauri.app/develop/plugins/ (plugin development overview)
- https://github.com/tauri-apps/tauri-docs/blob/v2/src/content/docs/security/permissions.mdx (plugin permission files)

## Part A — Sidecars (embedding external binaries)

A **sidecar** is a self-contained external executable (Python/Go/Rust/compiled Node app, an existing CLI tool, a bundled API server, etc.) shipped alongside your Tauri app so users don't need to separately install a runtime/dependency.

### 1. Configure in `tauri.conf.json`

```json
{
  "bundle": {
    "externalBin": ["binaries/my-sidecar"]
  }
}
```

Paths are relative to `src-tauri/`. This is the **logical name** you'll reference later — not the actual on-disk filename.

### 2. Name the binary with the target triple suffix

Tauri expects the actual file to be suffixed with the Rust target triple:

```
src-tauri/binaries/my-sidecar-x86_64-unknown-linux-gnu
src-tauri/binaries/my-sidecar-aarch64-apple-darwin
src-tauri/binaries/my-sidecar-x86_64-pc-windows-msvc.exe
```

Get your current host's triple:

```bash
rustc --print host-tuple           # Rust ≥ 1.84
rustc -Vv | grep host               # older Rust, parse the "host:" line
```

A build script that renames a freshly-compiled/bundled binary into this shape (Node example, same idea for Python/PyInstaller or a Go/Cargo cross-build):

```js
// scripts/rename-sidecar.js
const { execSync } = require('child_process');
const fs = require('fs');

const ext = process.platform === 'win32' ? '.exe' : '';
const targetTriple = execSync('rustc -Vv').toString().match(/host: (\S+)/)[1];
fs.renameSync(`src-tauri/binaries/sidecar${ext}`, `src-tauri/binaries/sidecar-${targetTriple}${ext}`);
```

This only produces a binary for the **host** you run it on — cross-compiling sidecars for other targets (e.g. building the Windows sidecar from a macOS CI runner) needs its own toolchain per target and is out of scope for a simple rename script; usually solved by building each sidecar in a matrix CI job per target OS (see `references/bundling-updater-cicd.md`).

### 3. Register the shell plugin

```rust
// Cargo.toml: tauri-plugin-shell = "2"
tauri::Builder::default()
    .plugin(tauri_plugin_shell::init())
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
```

```json
// capabilities/default.json — grant scoped shell execute for the sidecar
{
  "identifier": "shell:allow-execute",
  "allow": [{ "name": "binaries/my-sidecar", "sidecar": true, "cmd": "", "args": true }]
}
```

Use the **logical** name (`binaries/my-sidecar`, matching `externalBin`), not the suffixed filename, in both the capability and the spawn call.

### 4. Spawn and communicate — Rust side

```rust
use tauri_plugin_shell::ShellExt;
use tauri_plugin_shell::process::CommandEvent;

let sidecar_command = app.shell().sidecar("my-sidecar").unwrap();
let (mut rx, mut child) = sidecar_command.spawn().expect("failed to spawn sidecar");

tauri::async_runtime::spawn(async move {
    while let Some(event) = rx.recv().await {
        if let CommandEvent::Stdout(line_bytes) = event {
            let line = String::from_utf8_lossy(&line_bytes);
            // forward to frontend, e.g. via emit or a Channel (see ipc-commands.md)
        }
        if let CommandEvent::Terminated(payload) = event {
            // payload.code, payload.signal
        }
    }
});

// write to the sidecar's stdin
child.write("message from Rust\n".as_bytes()).unwrap();
```

### 5. Spawn from the frontend directly (no Rust command needed)

```ts
import { Command } from "@tauri-apps/plugin-shell";

const command = Command.sidecar("binaries/my-sidecar");
const output = await command.execute();
// or for streaming: command.on('close', ...); command.stdout.on('data', ...); command.spawn();
```

The string passed to `Command.sidecar()` must exactly match an entry in `bundle.externalBin`.

### 6. Argument restriction (security)

Sidecar argument allow-lists live in the `shell:allow-execute` capability grant. Use `{ "validator": "<regex>" }` for dynamic args instead of `args: true` wherever the argument shape is predictable — see `references/security-capabilities.md` for the full grant syntax. `args: true` (any arguments) should be reserved for cases like an embedded interactive terminal, where the executable path is still pinned but argument content is inherently free-form.

### 7. Language-specific notes

- **Python**: PyInstaller (or similar) to produce a single-file executable, then rename per the target-triple convention above. Documented community pattern — no first-party Tauri Python tooling, so expect to hand-roll the packaging script.
- **Node.js**: sidecars can't bundle a bare `.js` file (needs a runtime). Either ship a full Node binary as the sidecar and your script as a bundled `resource`, or compile to a standalone executable with a tool like `pkg` and treat that as the sidecar.
- **Rust/Go**: naturally produce single static(ish) binaries — usually the smoothest sidecar experience, just cross-compile per target and rename.

## Part B — Writing a Tauri Plugin

A plugin bundles Rust commands + optional JS bindings + a permission schema, reusable across projects (or published to crates.io/npm).

### Directory shape

```
tauri-plugin-foo/
├── Cargo.toml
├── build.rs
├── permissions/
│   ├── default.json      # special: auto-added to consuming app's config via `tauri plugin add`
│   └── <identifier>.json
├── src/
│   └── lib.rs
└── webview-src/           # optional JS/TS bindings, published separately to npm
    └── index.ts
```

### Command with dependency-injected app/window/channel handles

```rust
// src/commands.rs
use tauri::{command, ipc::Channel, AppHandle, Runtime, Window};

#[command]
async fn upload<R: Runtime>(
    app: AppHandle<R>,
    window: Window<R>,
    on_progress: Channel<u32>,
    url: String,
) -> Result<(), String> {
    // ... do the upload, report progress ...
    on_progress.send(100).unwrap();
    Ok(())
}
```

```ts
// webview-src/index.ts
import { invoke, Channel } from '@tauri-apps/api/core';

export async function upload(url: string, onProgressHandler: (p: number) => void): Promise<void> {
  const onProgress = new Channel<number>();
  onProgress.onmessage = onProgressHandler;
  await invoke('plugin:<plugin-name>|upload', { url, onProgress });
}
```

Plugin commands are invoked with the `plugin:<name>|<command>` prefix — that's what routes the IPC call to the plugin's handler rather than the app's own `invoke_handler`.

### The `default` permission is special

`permissions/default.json` (or `.toml`) is automatically merged into a consuming app's capability set when the app adds the plugin via `tauri plugin add` (or the equivalent manual Cargo/npm install + registration) — it's the "reasonable baseline" grant a plugin author ships. Anything beyond that baseline still needs the consuming app to explicitly opt in via its own capability files, same as any other permission.

### Plugin lifecycle hooks

Plugins can hook `on_page_load`, `on_event` (app exit, etc.), `on_drop` (plugin teardown), and `setup`. Use these for things like: cleaning up a background process the plugin spawned, persisting plugin-owned state on shutdown, or lazily initializing a connection on first page load rather than at app startup.

## When to reach for a full plugin vs. just commands in the main app

- **Just commands in `src-tauri/src/`**: the functionality is specific to this one app and won't be reused.
- **A plugin (even if kept private/in-repo, not published)**: you want the permission-scoping benefits of a separate `permissions/` schema, you're wrapping a piece of platform-specific native functionality that deserves isolation, or you genuinely expect to reuse it across more than one Tauri project (including a future rewrite).
