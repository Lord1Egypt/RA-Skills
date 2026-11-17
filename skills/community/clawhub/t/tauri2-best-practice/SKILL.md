---
name: tauri2-best-practice
description: Comprehensive best-practice guide for building, securing, testing, and shipping Tauri v2 desktop/mobile apps (Rust core + any web frontend — React, Next.js, Vue, Svelte, vanilla). Covers IPC (commands/events/channels), the v2 capabilities & permissions security model, CSP, state management (Manager/State), plugin development and sidecars, multi-window/webview management, bundling, code signing, the updater, CI/CD release pipelines, and testing (Rust unit tests, mockIPC, WebDriver/tauri-driver). ALWAYS consult this skill whenever the user mentions Tauri, tauri.conf.json, src-tauri, #[tauri::command], invoke(), capabilities/*.json, sidecar binaries, tauri-plugin-*, WebviewWindow, or is scaffolding/reviewing/debugging/shipping a Tauri v2 desktop or mobile app — even if they only say "my app" but the project clearly has a src-tauri folder or tauri.conf.json. Do NOT use for Tauri v1 (pre-2.0, allowlist-based) projects without explicitly flagging the version difference — check tauri.conf.json's `$schema` or Cargo.toml's tauri version first.
---

# Tauri v2 Best Practice

Tauri v2 is a Rust-core, webview-frontend framework for desktop (Windows/macOS/Linux) and mobile (iOS/Android) apps. This skill is deliberately **overkill**: it encodes the parts of Tauri v2 that are easy to get wrong, silently insecure, or scattered across many doc pages, so you don't have to relearn them from scratch every session.

**Every code example and claim in this skill and its reference files is grounded in the official Tauri v2 docs (`v2.tauri.app`), `docs.rs/tauri`, or the `tauri-apps/tauri-docs` GitHub source.** Reference files carry per-topic source URLs at the top — verify against them (via web search / fetch) before shipping anything security-critical, since Tauri v2 is still evolving and APIs move between minor versions.

## 0. First, orient yourself

Before writing anything, check:

1. **Version.** `src-tauri/Cargo.toml` → `tauri = "2.x"` and `tauri.conf.json`'s `$schema` pointing at a `v2`/`2.0.0` schema URL confirms v2. If you see `tauri.allowlist` in `tauri.conf.json`, that's **v1** — stop and flag it; the allowlist system was fully replaced by capabilities in v2, and the two are not interchangeable.
2. **Project shape.** `src-tauri/` (Rust core: `Cargo.toml`, `tauri.conf.json`, `src/`, `capabilities/`, optionally `binaries/` for sidecars) + a frontend root (any framework, or none — vanilla HTML/JS is fully supported).
3. **What the user actually needs.** Route to the relevant reference file below rather than dumping everything — but read `security-capabilities.md` proactively any time the task adds a new command, plugin, or filesystem/shell/network access, even if the user didn't ask about security.

## 1. Reference map — read before you write code

| If the task involves... | Read |
|---|---|
| `#[tauri::command]`, `invoke()`, `emit`/`listen`, streaming data, `Channel` | `references/ipc-commands.md` |
| `capabilities/*.json`, permissions, scopes, CSP, `withGlobalTauri`, isolation pattern, "why is invoke undefined/failing silently" | `references/security-capabilities.md` |
| `app.manage()`, `tauri::State`, sharing data across commands/threads, async mutex vs sync mutex | `references/state-management.md` |
| Writing a custom plugin, embedding an external binary (Python/Node/Go/Rust CLI) as a **sidecar**, `tauri-plugin-shell` | `references/plugins-sidecar.md` |
| Multiple windows, `WebviewWindowBuilder`, window labels, mobile multi-window, window/webview split, system tray, menus | `references/windowing-multiwindow.md` |
| `tauri build`, code signing (macOS notarization / Windows Azure Key Vault), the updater plugin, `latest.json`, GitHub Actions release pipeline | `references/bundling-updater-cicd.md` |
| Unit tests, `tauri::test::mock_builder`, `@tauri-apps/api/mocks` / `mockIPC`, WebDriver / `tauri-driver` / WebdriverIO, CI test matrices | `references/testing.md` |

Each reference file is self-contained with runnable code, gotchas, and a "sources" section. Files run 200–500 lines — read the whole file for the topic you're touching rather than skimming, since the gotchas are usually in the second half.

## 2. The eight rules that cause 90% of Tauri v2 bugs

These are condensed here because they're cross-cutting and worth having in working memory even before you open a reference file.

1. **Nothing is allowed by default.** Tauri v2 is default-deny. A window with no `capabilities/*.json` entry for a command cannot call it — the call fails at runtime (often silently, or as a vague `"<command> not allowed"` IPC error), not at compile time. If a frontend `invoke()` call "does nothing," check capabilities before touching the Rust code.
2. **Capabilities are matched by `windows` label.** A permission granted in a capability file only applies to windows whose label matches the `windows` array (glob-capable). Adding a new window (e.g. a settings window) without adding its label to the relevant capability is the #1 cause of "works in main window, broken in the new one."
3. **Plugin permissions are separate from core permissions**, and are namespaced `plugin-name:permission-id` (e.g. `fs:allow-read-file`, `shell:allow-execute`). Installing a plugin's crate + npm package is not enough — you must also grant its permissions in a capability file, and this has no compile-time check.
4. **State is auto-wrapped, don't double-wrap.** `app.manage(x)` makes `x` retrievable as `State<'_, X>` from any command. Tauri does not require you to wrap it in `Arc` yourself for the `State` extractor to work across threads — do that only if you're independently sharing it outside Tauri's state system. Do wrap the *inner* data in `Mutex`/`RwLock` (or an async `tokio::sync::Mutex` if you need to hold the lock across `.await`) since managed state must be `Send + Sync`.
5. **`window.__TAURI__` is opt-in.** `app.withGlobalTauri` defaults to `false` in v2. Any code (including a plain bundled `index.html` with no bundler) that references `window.__TAURI__.core.invoke` instead of importing from `@tauri-apps/api` will silently fail unless you've explicitly set `"app": {"withGlobalTauri": true}` in `tauri.conf.json`.
6. **Sidecar filenames must carry the target triple**, e.g. `my-sidecar-x86_64-pc-windows-msvc.exe`, matching `rustc -Vv | grep host` (or `rustc --print host-tuple` on Rust ≥1.84). `Command.sidecar()` on the JS side takes the *logical* name from `bundle.externalBin`, not the suffixed filename.
7. **Creating a window synchronously inside a command can deadlock on Windows** (a known WebView2 issue). Always create windows from an `async fn` command, or spawn a thread/async task, when the trigger is IPC.
8. **CSP defaults matter.** `tauri.conf.json`'s `app.security.csp` is enforced; setting it to `null` disables CSP entirely (don't, except transiently while debugging). A restrictive CSP plus a locked-down `capabilities` set is what actually makes "no Node.js/Electron-style full OS access from the webview" true in practice — don't rely on capabilities alone if the CSP is wide open.

## 3. Working style for this skill

- When reviewing existing Tauri code, actively look for capability/permission mismatches (rule 1–3) and sidecar target-triple issues (rule 6) even if not explicitly asked — these are the most common silent-failure classes.
- When scaffolding new commands/plugins/windows, always show the matching `capabilities/*.json` diff alongside the Rust/JS code — don't leave permission-wiring as an exercise for the user.
- Default to the **principle of least privilege**: prefer narrow, per-command permissions and per-window capability files over `*:default` blanket grants, and say so explicitly if you do reach for a blanket grant (e.g. rapid prototyping).
- Cross-check anything version-sensitive (plugin APIs churn between Tauri 2.0/2.1/2.2+) against current docs via web search rather than asserting from memory, and say so if something looks like it may have shifted since the reference file was written.
