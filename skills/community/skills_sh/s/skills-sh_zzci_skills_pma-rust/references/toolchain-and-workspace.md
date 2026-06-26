# PMA-Rust Toolchain And Workspace

This pack covers the **outside** of the code: workspace layout, edition 2024, lint enforcement, toolchain pinning, and the dev loop. Every pattern is anchored to a verified standard-bearer; see `references/evidence.md` for citations.

## Table of Contents

- [Workspace Structure](#workspace-structure)
- [Workspace `Cargo.toml`](#workspace-cargotoml)
- [Toolchain Pinning](#toolchain-pinning)
- [`.cargo/config.toml`](#cargoconfigtoml)
- [Lint And Format Configuration](#lint-and-format-configuration)
- [`xtask` Pattern (Optional - Use Only For Rust-Code Tasks)](#xtask-pattern-optional--use-only-for-rust-code-tasks)
- [`justfile` (Optional, Recommended)](#justfile-optional-recommended)
- [Local Dev Loop](#local-dev-loop)
- [Release Profiles & Binary Size](#release-profiles--binary-size)
- [Cross-Platform Static Binaries (musl)](#cross-platform-static-binaries-musl)
- [Editor / IDE Convention](#editor--ide-convention)
- [What To Reuse From Each Standard-Bearer](#what-to-reuse-from-each-standard-bearer)

## Workspace Structure

Service + CLI workspace (default for new PMA-Rust projects):

```text
.
├── Cargo.toml              # workspace root
├── Cargo.lock              # COMMIT for binaries; NOT for libraries
├── rust-toolchain.toml     # optional — see "Toolchain Pinning" below
├── rustfmt.toml
├── clippy.toml
├── deny.toml               # cargo-deny policy
├── .cargo/
│   └── config.toml         # build flags, registries, aliases
├── .config/
│   └── nextest.toml        # nextest profiles
├── crates/                 # OR direct top-level — both layouts seen in practice
│   ├── app/                # binary crate (`acme-app`)
│   ├── api/                # axum router + handlers
│   ├── core/               # domain logic, no IO
│   ├── db/                 # storage adapters (sqlx/seaorm/diesel)
│   ├── config/             # figment + clap glue
│   ├── telemetry/          # tracing + OTLP setup
│   └── common/             # error types, shared models
├── xtask/                  # see "xtask Pattern" — multiple valid shapes
├── tests/                  # workspace-level integration tests (optional)
├── benches/                # criterion / divan benches
└── justfile                # task runner (optional)
```

Layered ownership rules:

- `core` is dependency-free of IO. `db`, `api`, `app` may depend on `core`; `core` never depends on them.
- `app` is the **only** crate that wires figment + clap + telemetry + db + api. It owns `main.rs`, signal handling, and config merge.
- shared dependency versions live in `[workspace.dependencies]` — crates reference them with `dep = { workspace = true }`.
- avoid circular crate relationships; if two crates need each other, extract a third.
- single-binary projects (CLIs like ruff) may keep all code in one crate plus a `src/bin/<name>.rs` entry; multi-binary services should split.

## Workspace `Cargo.toml`

Skeleton (edition 2024, resolver `"2"`, workspace inheritance, lints):

```toml
[workspace]
resolver        = "3"              # default pairing for edition 2024 virtual workspaces
members         = ["crates/*", "xtask"]
default-members = ["crates/app"]   # OPTIONAL — only reth uses it (`Cargo.toml:155`).
                                   # Use when one bin is the canonical build target.

[workspace.package]
edition      = "2024"
rust-version = "1.96.0"            # MSRV = latest stable; bump in minor releases only (see baseline.md Lock 5)
license      = "Apache-2.0"
repository   = "https://github.com/acme/acme"
authors      = ["Acme Engineering"]

[workspace.dependencies]
# Shared deps; crates use `tokio = { workspace = true }`.
# Pin features at the workspace level so members opt into a consistent surface.
tokio       = { version = "1", features = ["macros", "rt-multi-thread", "signal", "sync", "time", "fs", "net"] }
tokio-util  = { version = "0.7", features = ["rt"] }      # for TaskTracker, CancellationToken
axum        = { version = "0.8", default-features = false, features = ["macros", "json", "tokio", "http1", "http2"] }
tower       = { version = "0.5", features = ["util", "retry", "timeout", "limit", "load-shed"] }
tower-http  = { version = "0.6", features = ["trace", "cors", "compression-gzip", "timeout", "limit", "sensitive-headers"] }
hyper       = { version = "1", features = ["server", "http1", "http2"] }
serde       = { version = "1", features = ["derive"] }
serde_json  = "1"
serde_with  = "3"
thiserror   = "2"                  # uv/ruff/quickwit confirmed thiserror 2.0
anyhow      = "1"
tracing     = "0.1"
tracing-subscriber  = { version = "0.3", features = ["env-filter", "json", "fmt"] }
tracing-opentelemetry = "0.32"
opentelemetry       = "0.31"
opentelemetry-otlp  = { version = "0.31", features = ["grpc-tonic", "http-json"] }
opentelemetry_sdk   = { version = "0.31", features = ["rt-tokio"] }
clap        = { version = "4", features = ["derive", "env"] }
clap_complete_command = "0.6"      # uv + ruff use this for shell completions
figment     = { version = "0.10", features = ["toml", "env", "yaml"] }
sqlx        = { version = "0.8", default-features = false, features = ["runtime-tokio", "tls-rustls-aws-lc-rs", "postgres", "macros", "migrate"] }
reqwest     = { version = "0.12", default-features = false, features = ["rustls-tls", "json", "stream"] }
rustls      = "0.23"
secrecy     = "0.10"
zeroize     = { version = "1", features = ["derive"] }
subtle      = "2"
validator   = { version = "0.18", features = ["derive"] }

# === Lock 4 — workspace lints (canonical place for deny-warnings policy) ===
# Rule of thumb: list only what deviates from rustc/clippy defaults.
[workspace.lints.rust]
# Catch every warn-by-default lint (current + future toolchains). priority -2 lets
# named lints below at default priority 0 override the group cleanly.
warnings    = { level = "deny", priority = -2 }
unsafe_code = "forbid"
# Opt-in lints (allow-by-default in rustc; turn on workspace-wide):
missing_debug_implementations = "warn"
missing_docs                  = "warn"
unreachable_pub               = "warn"
elided_lifetimes_in_paths     = "warn"

# Clippy defaults: correctness=deny, perf/suspicious/style/complexity=warn. We list
# only deviations — restating defaults is noise.
[workspace.lints.clippy]
# Promote allow-by-default groups to warn:
pedantic = { level = "warn", priority = -1 }
nursery  = { level = "warn", priority = -1 }
cargo    = { level = "warn", priority = -1 }
# Tighten individual lints (Lock 6):
unwrap_used        = "deny"
expect_used        = "deny"
panic              = "deny"
todo               = "warn"
dbg_macro          = "deny"
# Relax inside CLI output module(s) only via `#![allow(...)]` on that boundary:
print_stdout       = "deny"
print_stderr       = "deny"
disallowed_methods = "deny"
disallowed_types   = "deny"
# Pedantic lints with poor signal-to-noise:
module_name_repetitions = "allow"
must_use_candidate      = "allow"
missing_errors_doc      = "allow"
missing_panics_doc      = "allow"
```

Member crate `Cargo.toml` opts in:

```toml
[package]
name        = "acme-core"
version     = "0.1.0"
edition.workspace      = true
rust-version.workspace = true
license.workspace      = true
repository.workspace   = true

[lints]
workspace = true

[dependencies]
serde     = { workspace = true }
thiserror = { workspace = true }
tracing   = { workspace = true }
```

`crates/app/src/lib.rs` (or `main.rs`) starts with:

```rust
#![forbid(unsafe_code)]
```

### Path B — build-flag lint enforcement (vector pattern)

When `[workspace.lints]` is too coarse (e.g. you need different lints for build scripts vs runtime), enforce via `.cargo/config.toml`. Verified at `vector/.cargo/config.toml:9-15`:

```toml
[target.'cfg(all())']
rustflags = [
    "-D", "warnings",
    "-D", "clippy::print_stdout",
    "-D", "clippy::print_stderr",
    "-D", "clippy::dbg_macro",
]
```

This is harder to scope per-crate but easier to override locally for a single build. Pick **one path per workspace** — do not mix.

## Toolchain Pinning

Two equally valid approaches, depending on project type.

### Approach A — `rust-version` only (cargo / rust-analyzer / reth pattern)

`Cargo.toml` declares `rust-version`; CI installs via `dtolnay/rust-toolchain@stable` (or `master` for explicit pin). **No** `rust-toolchain.toml`. Lighter for libraries and CI variability.

```yaml
# .github/workflows/ci.yml
- uses: dtolnay/rust-toolchain@stable
- uses: dtolnay/rust-toolchain@master
  with:
    toolchain: "1.96.0"   # for MSRV verification job — match workspace.package.rust-version
```

### Approach B — `rust-toolchain.toml` (vector pattern)

```toml
[toolchain]
channel    = "1.96.0"           # match MSRV exactly, or pin a sliding stable
components = ["clippy", "rustfmt", "rust-src", "rust-analyzer"]
profile    = "minimal"
targets    = ["x86_64-unknown-linux-gnu"]
```

The `rust-toolchain.toml` mechanism is verified at `vector/rust-toolchain.toml` (vector itself pins `channel = "1.92"`; the `1.96.0` above is this skill's baseline, not vector's value). Use when developer environments must be byte-for-byte reproducible (services with strict deployment pipelines).

## `.cargo/config.toml`

Reproducible settings, aliases, and the rustls-only posture:

```toml
# Lint policy lives in Cargo.toml's [workspace.lints] (Lock 4), NOT here.
# This file is for build environment (linkers, registries, xtask shortcut) only.

[net]
git-fetch-with-cli = true

# Single cargo alias — `cargo xtask <subcmd>` is the standard invocation. Day-to-day
# task running (fmt/clippy/test/deny) happens via `just`; see the justfile section below.
[alias]
xtask = "run --quiet --package xtask --"

[target.x86_64-pc-windows-msvc]
linker = "rust-lld"             # rust-analyzer pattern, .cargo/config.toml:8-10

# Do NOT enable `vendored-openssl` features anywhere. rustls only.
```

The PMA-Rust convention is **`just` as the task runner, cargo aliases only for `xtask`**. `just` is cross-project standard, lower learning cost than a workspace's bespoke alias names, and composes cleanly with non-cargo tooling. Cargo aliases are reserved for invoking other Cargo packages (`xtask`, `codegen`), not for re-aliasing what `just` already covers.

## Lint And Format Configuration

| File | Purpose | Verified pattern |
|---|---|---|
| `rustfmt.toml` | formatting policy | cargo: `style_edition = "2024"` (1 line). reth/r-a add `imports_granularity = "Crate"`, `use_small_heuristics = "Max"` |
| `clippy.toml` | thresholds + disallowed methods/types | enforces project-specific anti-patterns |
| `deny.toml` | supply chain policy | see `references/delivery.md` |
| `.config/nextest.toml` | test profiles (`default`, `ci`, `slow`) | reth: retries=2, slow-timeout 30s |

Recommended `clippy.toml` (composes patterns from cargo, rust-analyzer, vector):

```toml
# from rust-analyzer/clippy.toml — discourage HashMap in hot paths
disallowed-types = [
    { path = "std::collections::HashMap",  reason = "use FxHashMap from rustc-hash" },
    { path = "std::collections::HashSet",  reason = "use FxHashSet from rustc-hash" },
    { path = "once_cell::sync::Lazy",      reason = "use std::sync::LazyLock" },
    { path = "once_cell::unsync::Lazy",    reason = "use std::cell::LazyCell" },
]

# from cargo/clippy.toml — block global mutable state via env
disallowed-methods = [
    { path = "std::env::set_var",          reason = "set env at process boot only" },
    { path = "std::process::Command::new", reason = "use the project's `command` wrapper for testability" },
]

# Permit some patterns in tests
allow-print-in-tests   = true
allow-dbg-in-tests     = true
allow-unwrap-in-tests  = true

# Tunables
cognitive-complexity-threshold  = 25
too-many-arguments-threshold    = 7
type-complexity-threshold       = 250
```

`Cranky.toml` is **not** in any of the 10 standard-bearers — do not introduce `cargo-cranky`.

## `xtask` Pattern (Optional — Use Only For Rust-Code Tasks)

**Most tasks belong in `just`, not in `xtask`.** Reach for `xtask` only when a task needs Rust code: codegen, complex release flows (version bump + sign + multi-arch dist), graph manipulation. Plain shell-equivalent work (fmt, clippy, test, deny) belongs in the `justfile` below.

Canonical shape — a single `xtask/` crate, `publish = false` (verified at `rust-analyzer/xtask/Cargo.toml:1-25`):

```toml
# xtask/Cargo.toml
[package]
name    = "xtask"
version = "0.1.0"
publish = false                        # never goes to crates.io
edition.workspace = true

[dependencies]
# "Avoid adding more dependencies to this crate" — comment in rust-analyzer's real file.
xshell = "0.2"
xflags = "0.4"
anyhow = "1"
```

`xtask/src/main.rs` skeleton — only tasks that genuinely need Rust:

```rust
use anyhow::Result;
use xshell::{cmd, Shell};

xflags::xflags! {
    cmd xtask {
        cmd codegen {}
        cmd dist { tag: String }
    }
}

fn main() -> Result<()> {
    let sh = Shell::new()?;
    match Xtask::from_env_or_exit().subcommand {
        XtaskCmd::Codegen(_) => { /* regenerate code from .proto / schema / … */ }
        XtaskCmd::Dist(d)    => { /* tag → cross-build matrix → sign → upload */ }
    }
    Ok(())
}
```

Invoked via the `cargo xtask` alias. Keep `xtask` outside `default-members` so plain `cargo build` from the root doesn't pull in dev tooling.

> **Escape hatches** (don't adopt prophylactically): cargo splits its xtask into multiple focused crates (`xtask-build-man`, `xtask-bump-check`, …); vector publishes its xtask as `vdev`; reth skips xtask entirely and drives everything from `Makefile` + `.github/scripts/*.sh`. Reach for these only after the single-crate shape genuinely outgrows itself.

## `justfile` (Optional, Recommended)

```just
default: ci

# Plain commands — deny-warnings policy lives in [workspace.lints.rust]
ci:
    cargo fmt --all -- --check
    cargo clippy --workspace --all-targets --all-features --locked
    cargo nextest run --workspace --all-features --locked
    cargo test --doc --workspace --all-features --locked
    cargo deny check
    cargo shear

watch:
    bacon

test name="":
    cargo nextest run {{name}}

cov:
    cargo llvm-cov nextest --workspace --html

fix:
    cargo clippy --fix --workspace --all-targets --allow-dirty
    cargo fmt --all
```

## Local Dev Loop

| Tool | Purpose | Verified at |
|---|---|---|
| `bacon` | background `cargo check`/`clippy`/`test` on save | (general convention; not in standard-bearers) |
| `cargo nextest` | parallel test runner | r-a, reth, vector, tokio, uv, ruff, quickwit |
| `cargo expand` | view macro-expanded code | (debug only) |
| `cargo flamegraph` | CPU profiling | |
| `tokio-console` | runtime task inspection | gate behind `tokio_unstable` cfg |
| `cargo-llvm-cov` | coverage | preferred over tarpaulin |
| `mold` linker | faster Linux linking | reth (`setup-mold` action in every CI job) |
| `sccache` | distributed build cache | reth (`mozilla-actions/sccache-action`) |

`bacon.toml` minimal:

```toml
default_job = "clippy-all"

[jobs.clippy-all]
command     = ["cargo", "clippy", "--workspace", "--all-targets", "--all-features", "--locked"]
need_stdout = false
```

## Release Profiles & Binary Size

PMA-Rust binaries ship with **two profiles** beyond the stock `release`: a balanced runtime profile and a size-optimized `dist` profile. Anchored on the Rust Performance Book (build-configuration chapter) and uv/ruff's actual `cargo-dist` settings.

**Rule of thumb: list only non-default values.** Cargo's defaults are stable and well-documented; restating them adds noise without changing behavior.

```toml
# Workspace root Cargo.toml

# === [profile.release] — runtime-speed tuned ===
# Defaults inherited: opt-level=3, strip="none", panic="unwind", incremental=false.
# Why panic="unwind" here: hyper/tokio/axum middleware assume catch_unwind works.
[profile.release]
lto           = "fat"                 # +10-20% perf vs default `false`
codegen-units = 1                     # cross-unit inlining (default 16)
debug         = "line-tables-only"    # smaller than full, keeps backtraces

# === [profile.dist] — size-tuned for shipped binaries (cargo-dist drives this) ===
# Inherits from release, overrides for size:
[profile.dist]
inherits  = "release"
opt-level = "z"                       # smallest; benchmark — may cost 5-15% runtime
strip     = "symbols"                 # 30-60% binary size reduction
panic     = "abort"                   # no unwind tables; `catch_unwind` no longer works
debug     = false

# === [profile.dev] — fast inner loop ===
# Defaults inherited: opt-level=0, incremental=true,
# split-debuginfo="unpacked" (Linux/macOS default since Rust 1.84).
[profile.dev]
debug = "line-tables-only"            # 20-40% faster compile than full debug info

# Optimize all dependency code in dev — massive speedup for test runs.
# Widely used pattern in game/graphics workspaces.
[profile.dev.package."*"]
opt-level = 1
```

Trade-offs to watch (Performance Book):
- `opt-level = "z"` may run **5-15% slower** than `3` — benchmark before adopting in `dist`
- `panic = "abort"` removes unwind tables (smaller binary) but **breaks `catch_unwind`**; verify no dep needs it before flipping. Tests still build with `unwind` (Cargo's test profile is separate)
- `strip = "symbols"` makes prod backtraces unresolvable — pair with a sourcemap upload pipeline (Sentry, Datadog) if you need crash analysis

### Linker selection (faster builds)

```toml
# .cargo/config.toml — opt-in fast linkers per platform
[target.x86_64-unknown-linux-gnu]
linker = "clang"
rustflags = ["-C", "link-arg=-fuse-ld=mold"]   # ~5-10× faster link than ld

[target.aarch64-unknown-linux-gnu]
linker = "clang"
rustflags = ["-C", "link-arg=-fuse-ld=mold"]

[target.x86_64-pc-windows-msvc]
linker = "rust-lld"        # rust-analyzer uses this; faster than link.exe

[target.aarch64-apple-darwin]
rustflags = ["-C", "link-arg=-fuse-ld=lld"]
```

reth installs `mold` on every CI job (`.github/workflows/lint.yml`, `rui314/setup-mold` action). Local devs install via package manager.

## Cross-Platform Static Binaries (musl)

Standard pattern for distributing Rust binaries that run on any Linux without a libc dependency: build against `*-unknown-linux-musl` with `+crt-static`. Verified across `astral-sh/uv` (`build-release-binaries.yml` ships 4 musl targets) and `astral-sh/ruff` (`cargo-dist` config).

### Why musl for production binaries

- **No glibc version drift** — a glibc-linked binary built on Ubuntu 24.04 fails on Debian 11; a musl-static binary runs on both
- **Containers** — drops the need for a base image with libc; works in `FROM scratch` or `FROM gcr.io/distroless/static`
- **Smaller attack surface** — no dynamic loader, no LD_PRELOAD shenanigans
- **Cross-compile friendly** — pairs naturally with `cross` or `cargo-zigbuild` from any host

### `.cargo/config.toml` — pin `+crt-static`

```toml
[target.x86_64-unknown-linux-musl]
rustflags = ["-C", "target-feature=+crt-static"]

[target.aarch64-unknown-linux-musl]
rustflags = ["-C", "target-feature=+crt-static"]

[target.armv7-unknown-linux-musleabihf]
rustflags = ["-C", "target-feature=+crt-static"]

[target.riscv64gc-unknown-linux-musl]
rustflags = ["-C", "target-feature=+crt-static"]
```

`+crt-static` is **default for musl** on Rust ≥ 1.79, but pin it explicitly so a future toolchain change cannot silently break the static guarantee.

### Build commands

```bash
# Local cross-build via cross (Docker-based, supports all listed targets)
cargo install cross --locked
cross build --profile dist --target x86_64-unknown-linux-musl
cross build --profile dist --target aarch64-unknown-linux-musl

# Or via cargo-zigbuild (newer, no Docker, uses zig as cross-linker)
cargo install cargo-zigbuild --locked
cargo zigbuild --profile dist --target x86_64-unknown-linux-musl
cargo zigbuild --profile dist --target aarch64-unknown-linux-musl.2.17  # glibc fallback option

# Verify static linkage
file       target/x86_64-unknown-linux-musl/dist/myapp
ldd        target/x86_64-unknown-linux-musl/dist/myapp     # must say "not a dynamic executable"
readelf -d target/x86_64-unknown-linux-musl/dist/myapp     # NEEDED entries should be empty
```

### Cargo features that DO NOT belong on musl

Add to `cargo deny` `bans` for static-binary projects:

```toml
# deny.toml — keep musl builds clean
[[bans.deny]]
name   = "openssl-sys"
reason = "rustls only — also breaks musl static link"

[[bans.deny]]
name   = "native-tls"
reason = "rustls only — pulls libssl on glibc, broken on musl"
```

### Allocator note for musl

The musl built-in allocator is famously slow on multi-threaded workloads. Choose one:

```rust
// Option A — mimalloc (recommended for musl, avoids jemalloc's musl issues)
#[cfg(all(target_env = "musl", not(target_arch = "wasm32")))]
#[global_allocator]
static GLOBAL: mimalloc::MiMalloc = mimalloc::MiMalloc;

// Option B — jemalloc on glibc only, default on musl
#[cfg(all(not(target_env = "musl"), not(target_os = "windows"), not(target_arch = "wasm32")))]
#[global_allocator]
static GLOBAL: tikv_jemallocator::Jemalloc = tikv_jemallocator::Jemalloc;

#[cfg(target_os = "windows")]
#[global_allocator]
static GLOBAL: mimalloc::MiMalloc = mimalloc::MiMalloc;
```

Mirrors ruff's `crates/ruff/src/main.rs:11-28` allocator switching, extended for the musl case. **Library crates never install global allocators.**

### Building the `aws-lc-rs` crypto provider

PMA standardizes on the **`aws-lc-rs`** rustls provider (Lock 2). It wraps AWS-LC (C + per-arch assembly), so unlike a pure-Rust crate it has a real build step. The constraints below are the ones that actually break CI/cross builds — get them right once and the provider is invisible thereafter.

**Default (non-FIPS) build — what is and isn't required:**

| Tool | Needed for default `aws-lc-rs`? | Notes |
|---|---|---|
| C/C++ compiler (`cc`/`clang`) | **Yes** | Only hard requirement. Present in `rust:1.96.0`, `debian`, most CI images. Distroless/`scratch` runtime is fine — AWS-LC is statically compiled into the binary at build time, nothing is needed at runtime. |
| CMake | **No** | Pre-generated build metadata ships with `aws-lc-sys`. CMake is required **only** for the `fips` feature. |
| Go | **No** | Required **only** for the `fips` feature. |
| `bindgen` / `libclang` | **No** | Pre-generated bindings ship for supported targets. Needed only if you opt into the `bindgen` or `legacy-des` feature, or build for a target without pre-generated bindings. |
| NASM (Windows x86-64 only) | Conditional | The `prebuilt-nasm` feature (or env `AWS_LC_SYS_PREBUILT_NASM=1`) ships prebuilt objects so NASM is not needed; if NASM is on PATH it is used regardless. Irrelevant to Linux server targets. |

So for the canonical Linux service target the only prerequisite beyond the Rust toolchain is a working C compiler — the old "aws-lc-rs needs cmake and slows CI" caveat no longer applies to default builds.

**musl / static (`*-unknown-linux-musl` + `+crt-static`):** `aws-lc-rs` builds and statically links cleanly on musl. The build host needs the musl C cross toolchain (`musl-gcc`, i.e. `musl-tools` on Debian) and `CC_x86_64_unknown_linux_musl` / `AR_*` pointing at it. Using **`cross`** (the PMA default for cross/musl, see `delivery.md`) handles this automatically — its images already carry the musl C toolchain. `cargo-zigbuild` also works (`zig cc` as the cross C compiler).

**Cross-compilation (e.g. building aarch64 on x86-64):** `aws-lc-sys` cross-compiles via the target C toolchain. Set per-target `CC_<target>` / `CXX_<target>` / `AR_<target>`, or just use **`cross`** so the correct C toolchain is selected per target. A missing/mismatched cross C compiler is the single most common `aws-lc-sys` build failure — the error surfaces as a `cc`/linker failure inside `aws-lc-sys`, not as a Rust error.

**FIPS (`aws-lc-rs` `fips` feature → `aws-lc-fips-sys`):** only when a compliance requirement demands it (discharge via ADR, see `baseline.md` Lock 2 backfire row). Build now also needs **CMake** and **Go**, and on some targets `bindgen`/`libclang`. It is slower and not cross-friendly — run FIPS builds on a native runner per target, not under `cross`.

**Dependency alignment:** `reqwest` (`rustls-tls` feature) and `sqlx` (`tls-rustls-aws-lc-rs` feature) both resolve to the same `aws-lc-rs` provider, so a single `install_default()` call covers every TLS path. Do **not** mix a `ring`-flavored feature on one dependency with `aws-lc-rs` on another — linking both providers makes the process default ambiguous and the explicit `install_default()` is what disambiguates it.

quickwit installs the **ring** provider at startup (`install_default_crypto_ring_provider()`); reuse its *startup-install timing* pattern but with `rustls::crypto::aws_lc_rs::default_provider()` (see `baseline.md` Lock 2).

## Editor / IDE Convention

Pin one of:

- VS Code with `rust-analyzer` extension (most common, mirrors the standard-bearer of the same name)
- IntelliJ Rust / RustRover

`.editorconfig` should match `rustfmt.toml` line widths.

## What To Reuse From Each Standard-Bearer

| Pattern | Source |
|---|---|
| `[workspace.lints]` shape | `cargo/Cargo.toml:131-145` (compact); `reth/Cargo.toml:162-259` (extensive) |
| Single `xtask/` (`publish=false`) | `rust-analyzer/xtask/Cargo.toml` |
| Build-flag enforcement | `vector/.cargo/config.toml:9-15` |
| MSRV CI via `cargo hack` | `cargo/.github/workflows/main.yml:320-323` |
| MSRV CI via `cargo msrv verify` | `vector/.github/workflows/msrv.yml` |
| `mold` + `sccache` for big workspaces | `reth/.github/workflows/lint.yml:11-30` |
| `crate-ci/typos` typo gate | `cargo`, `rust-analyzer`, `reth`, `uv` |

If migrating an existing project: adopt in this order — workspace `[lints]` → workspace `[dependencies]` → `xtask/` → `cargo nextest` → `cargo deny`. Each step lands cleanly without invasive rewrites.
