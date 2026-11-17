# `.github/workflows/unit-tests.yml`

Cross-platform matrix that runs `cargo test` on every push and PR. Ubuntu needs GTK system deps for Tauri to link.

```yaml
name: Unit Tests

on:
  push:
    branches: ['**']
  pull_request:

jobs:
  test:
    strategy:
      fail-fast: false
      matrix:
        platform: [macos-latest, windows-latest, ubuntu-latest]
    runs-on: ${{ matrix.platform }}

    steps:
      - uses: actions/checkout@v4

      - uses: dtolnay/rust-toolchain@stable

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Cache cargo registry + build
        uses: actions/cache@v4
        with:
          path: |
            ~/.cargo/registry
            ~/.cargo/git
            src-tauri/target
          key: ${{ runner.os }}-cargo-${{ hashFiles('src-tauri/Cargo.lock') }}
          restore-keys: |
            ${{ runner.os }}-cargo-

      - run: npm ci

      - name: Install Ubuntu system deps
        if: matrix.platform == 'ubuntu-latest'
        run: |
          sudo apt-get update
          sudo apt-get install -y \
            libgtk-3-dev \
            libayatana-appindicator3-dev \
            librsvg2-dev \
            libwebkit2gtk-4.1-dev \
            pkg-config

      - name: Run Rust tests
        run: cd src-tauri && cargo test --all-features

      - name: TypeScript build
        run: npm run build
```

## Why these choices

- **`fail-fast: false`** — Without it, a failure on macOS cancels the Windows and Ubuntu jobs. You want to see all three results to know whether the bug is platform-specific.
- **Three runners** — Tauri's behavior diverges per OS (file pickers, permissions, hotkeys). Green on one runner means little.
- **Ubuntu system deps** — Tauri's webview integration on Linux needs GTK, AppIndicator, RSVG, WebKit2GTK. Without them, `cargo build` fails with cryptic linker errors.
- **Cache key includes `Cargo.lock`** — Re-key the cache when dependencies change. Without the `restore-keys` fallback, a single dep bump invalidates the whole cache.
- **`npm ci`** (not `npm install`) — Faster, deterministic, fails if `package-lock.json` is out of sync.
- **`cargo test --all-features`** — If you have feature flags, run tests across them. Drop `--all-features` if you have features that intentionally conflict.

## Optional: TypeScript-only quick check

If the Rust matrix is slow and you want fast feedback on frontend changes, add a parallel job:

```yaml
  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npx tsc --noEmit
```

Runs in seconds and catches the majority of frontend regressions without spinning up the Rust toolchain.

## Optional: Tag-triggered release workflow

Skipping the full template here because the publish pipeline depends heavily on the user's distribution choice (GitHub Releases, R2, S3, custom CDN, …) and their signing setup. Key points if you generate one:

- **Never hardcode the CDN URL** or any signing identity in the workflow file — read them from `secrets.*`.
- **Build matrix typically includes only signed targets** (Windows + macOS aarch64 / x86_64). Linux builds may not need signing depending on distribution.
- **Updater manifest generation** assembles the JSON shape documented in `references/templates/tauri-conf.md` from each platform's `.sig` file outputs.
- **Notarization on macOS** (`xcrun notarytool submit ... --wait`) is mandatory for unsigned-runtime users; budget 5–15 minutes per build.

Ask the user for the distribution target (GitHub Releases, R2, S3, custom) before generating a release workflow. Don't assume.
