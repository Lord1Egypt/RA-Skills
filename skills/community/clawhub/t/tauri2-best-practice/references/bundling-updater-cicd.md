# Bundling, Code Signing, Updater, CI/CD

**Sources:**
- https://v2.tauri.app/plugin/updater/
- https://v2.tauri.app/distribute/pipelines/github/
- https://docs.crabnebula.dev/cloud/guides/auto-updates-tauri/ (third-party, but a clear worked v2 example)
- https://dev.to/tomtomdu73/ship-your-tauri-v2-app-like-a-pro-github-actions-and-release-automation-part-22-2ef7

## Bundling basics

```bash
npm run tauri build   # or: cargo tauri build
```

Produces platform-native installers per `tauri.conf.json`'s `bundle` config: `.dmg`/`.app` (macOS), `.msi`/`.exe` (NSIS, Windows), `.deb`/`.rpm`/`.AppImage` (Linux). Cross-compiling installers for a different OS than the CI runner is generally **not** supported for the final installer format (though the Rust binary itself can sometimes cross-compile) — the standard approach is a CI matrix with one runner per target OS (see below).

## Code signing (do this before shipping, not as an afterthought)

- **macOS**: requires an Apple Developer ID certificate; the build step signs the `.app`, and a separate **notarization** step uploads it to Apple and waits for approval before the release is considered done — this is usually the slowest step in CI (minutes, not seconds).
- **Windows**: traditionally a code-signing certificate + `signtool`; increasingly done via cloud HSM-backed signing (e.g. Azure Key Vault) rather than a local `.pfx`, since standalone certs are being phased toward hardware-backed keys by CA/Browser Forum requirements.
- **Linux**: no OS-level code signing equivalent; package repos (if you run one) and `AppImage` signing are the closer analogs, but far less commonly enforced by the OS.
- Unsigned builds will trigger OS-level "unknown publisher" warnings (Gatekeeper on macOS, SmartScreen on Windows) that meaningfully hurt install conversion — budget for signing setup, it's not optional polish for a real release.

## The updater plugin

```rust
// Cargo.toml: tauri-plugin-updater = "2"
tauri::Builder::default()
    .plugin(tauri_plugin_updater::Builder::new().build())
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
```

```json
// capabilities/default.json — required permissions
{
  "permissions": [
    "dialog:default", "dialog:allow-ask", "dialog:allow-message",
    "updater:default", "updater:allow-check", "updater:allow-download-and-install",
    "process:allow-restart"
  ]
}
```

```ts
import { check } from '@tauri-apps/plugin-updater';
import { relaunch } from '@tauri-apps/plugin-process';

const update = await check();
if (update) {
  await update.downloadAndInstall();
  await relaunch();
}
```

### Signing keys (separate from OS code-signing certs)

```bash
npx tauri signer generate -w ~/.tauri/myapp.key
```

Generates a keypair specifically for the updater's own signature verification (checked before installing an update, independent of OS-level code signing). Set the **public** key in `tauri.conf.json`'s `plugins.updater.pubkey`; keep the **private** key + its password as CI secrets (`TAURI_SIGNING_PRIVATE_KEY`, `TAURI_SIGNING_PRIVATE_KEY_PASSWORD`) — never commit it.

### The `latest.json` manifest

The updater polls a static (or dynamic) endpoint for a JSON manifest describing the newest version, per-platform download URLs, and signatures. Using GitHub Releases as a free static host:

```json
{ "app": { "security": {} }, "plugins": { "updater": {
  "endpoints": ["https://github.com/<user>/<repo>/releases/latest/download/latest.json"]
} } }
```

`tauri-action` (below) generates this `latest.json` automatically when `includeUpdaterJson: true`. A dynamic server (your own backend) is also supported — it just needs to respond with the same manifest shape, or `204 No Content` when there's nothing newer than the client's reported version. A dynamic server can also be used to implement staged rollouts, version pinning, or rollback (serve an older version deliberately) — a static GitHub Releases endpoint can't.

## CI/CD: GitHub Actions release pipeline

The community-standard building block is `tauri-apps/tauri-action`, which builds, signs, and (optionally) drafts a GitHub Release with the updater manifest in one step:

```yaml
# .github/workflows/release.yml
name: release
on:
  push:
    tags: ['v*']

jobs:
  release:
    strategy:
      matrix:
        include:
          - platform: 'macos-latest'
            args: '--target aarch64-apple-darwin'
          - platform: 'macos-latest'
            args: '--target x86_64-apple-darwin'
          - platform: 'ubuntu-22.04'
            args: ''
          - platform: 'windows-latest'
            args: ''
    runs-on: ${{ matrix.platform }}
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - uses: actions/setup-node@v4
        with: { node-version: 'lts/*' }
      - run: npm install
      - uses: tauri-apps/tauri-action@v0
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          TAURI_SIGNING_PRIVATE_KEY: ${{ secrets.TAURI_SIGNING_PRIVATE_KEY }}
          TAURI_SIGNING_PRIVATE_KEY_PASSWORD: ${{ secrets.TAURI_SIGNING_PRIVATE_KEY_PASSWORD }}
          # + platform-specific signing secrets (Apple ID/cert, Azure Key Vault, etc.)
        with:
          tagName: v__VERSION__
          releaseName: 'App v__VERSION__'
          includeUpdaterJson: true
          releaseDraft: true
          prerelease: false
          args: ${{ matrix.args }}
```

Notes:
- One matrix job per **target OS**, not per target *architecture-within-an-OS* where avoidable — except macOS, where Intel and Apple Silicon genuinely need separate build steps (`--target x86_64-apple-darwin` / `--target aarch64-apple-darwin`) even though both run on `macos-latest`, since Tauri doesn't produce universal-binary output by default.
- `releaseDraft: true` + manual review + manual publish is the safer default over fully-automatic publish, especially early in a project's life — you get a chance to sanity-check the built artifacts before users can download them.
- Expect the macOS jobs to be the slowest in the matrix specifically because of the notarization round-trip to Apple, not the build itself.
- Real per-secret list for a fully signed, cross-platform release commonly includes (this varies by exact signing setup): `TAURI_SIGNING_PRIVATE_KEY`, `TAURI_SIGNING_PRIVATE_KEY_PASSWORD`, Apple: signing certificate + password, Apple ID + app-specific password + team ID (for notarization); Windows: Azure Key Vault client ID/secret/tenant/cert name (or a traditional `.pfx` + password if not using cloud HSM signing).

## Third-party distribution/update hosting (optional)

Services like CrabNebula Cloud exist specifically to remove the "host `latest.json` + release assets yourself" burden and add extras (staged rollouts, analytics, global CDN). Not required — GitHub Releases as a static host works fine for most indie/small-team projects — but worth mentioning if the user is scaling up distribution or wants rollout controls beyond what a static manifest supports.

## Pre-release checklist

- [ ] `tauri.conf.json` version bumped (and matches the git tag if your CI derives the release from the tag).
- [ ] Updater public key committed; private key only in CI secrets.
- [ ] CSP is a real policy, not `null` (see `references/security-capabilities.md`).
- [ ] Capabilities reviewed for least-privilege before the first public release, not just "works on my machine."
- [ ] Code signing configured for macOS + Windows (Linux: at minimum, checksums published alongside artifacts).
- [ ] `includeUpdaterJson`/manifest endpoint reachable and matches `plugins.updater.endpoints` in the shipped config — test an actual update-check against a real prior release before announcing auto-update as a feature.
