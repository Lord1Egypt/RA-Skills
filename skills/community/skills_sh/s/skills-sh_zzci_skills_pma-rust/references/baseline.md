# PMA-Rust Baseline

This is the **acceptance baseline** every PMA-Rust project must meet. It is anchored to the standard-bearer projects listed in `SKILL.md` and the official Rust API Guidelines. Citations refer to file paths under `/tmp/pma-rust-research/` (verifiable via `references/evidence.md`).

## Table of Contents

- [Hard Locks](#hard-locks)
- [Known Trade-offs (When the Locks Backfire)](#known-trade-offs-when-the-locks-backfire)
- [Other Strict Rules - When They Backfire](#other-strict-rules--when-they-backfire)
- [Meta-rule: how to add an exception cleanly](#meta-rule-how-to-add-an-exception-cleanly)
- [Tech Stack](#tech-stack)
- [Naming (Rust API Guidelines)](#naming-rust-api-guidelines)
- [Dependency Freshness (Rust)](#dependency-freshness-rust)
- [Required Conventions](#required-conventions)
- [Code Quality](#code-quality)

## Hard Locks

These rules are non-negotiable. Loosening one requires a dated decision record under `docs/decisions/`.

### Lock 1 — Pure Rust ecosystem first

Whenever a pure-Rust alternative exists, do **not** introduce a new dependency that wraps a C library or pulls in `*-sys` transitively.

| C-FFI dep | Pure-Rust alternative | Notes |
|---|---|---|
| `openssl`, `openssl-sys`, `native-tls` | **`rustls`** + `tokio-rustls` + `rustls-pemfile` + `rustls-platform-verifier` | reth bans `openssl` in `deny.toml:35`. Install the rustls **`aws-lc-rs`** provider at startup (quickwit's own code uses the `ring` provider — see Lock 2 for why PMA standardizes on `aws-lc-rs`) |
| `libgit2-sys`, `git2` | **`gix`** (gitoxide) | cargo's `audit.yml` lists `git2` as a watch item |
| `libssh2-sys` | `russh` | |
| `libpq-sys` (sync Postgres) | `tokio-postgres` / `sqlx-postgres` (rustls feature) | |
| `cmake`-built deps | a Rust port if one exists; otherwise vendor `cc` build with explicit `// JUSTIFICATION:` | |

Unavoidable C deps (e.g. `libsqlite3-sys` via `rusqlite`, system `protobuf` for `prost-build`) require a `// JUSTIFICATION:` comment in the workspace `Cargo.toml` next to the dependency, plus a CI gate that pins their versions.

**Pre-sanctioned exception — the rustls crypto core.** rustls's default crypto provider, `aws-lc-rs` (wrapping AWS-LC, a vetted C/assembly fork of BoringSSL), is the *one* C/asm core that does **not** need a per-repo `// JUSTIFICATION:`. Rationale: there is no mature, audited, FIPS-capable pure-Rust crypto primitive library — the only alternative provider, `ring`, is itself C/assembly, so the choice is never "pure Rust vs C", it is "which vetted C crypto core". rustls itself (the TLS state machine, the part that historically caused OpenSSL CVEs) remains pure, memory-safe Rust. PMA standardizes on `aws-lc-rs` because it is the rustls 0.23 default, is actively maintained by AWS, and is the only provider with a FIPS 140-3 path (`fips` feature) — so a future compliance requirement does not force a provider swap. This carve-out covers `aws-lc-rs` / `aws-lc-sys` *only*; every other `*-sys` dep still needs its own justification.

### Lock 2 — rustls only, `aws-lc-rs` provider explicit

```rust
// In `main.rs`, before any TLS use (any code path that builds a
// rustls ClientConfig/ServerConfig — directly or via reqwest/sqlx/tonic):
rustls::crypto::aws_lc_rs::default_provider()
    .install_default()
    .expect("install rustls crypto provider");
```

`aws-lc-rs` is the rustls 0.23 default crypto feature, so plain `rustls = "0.23"` (default features) already compiles it in — do **not** set `default-features = false` to swap in `ring`. Calling `install_default()` early is still mandatory: rustls 0.23 panics on the first TLS use if no process-default provider is installed, and an explicit call removes the "two providers linked, ambiguous default" failure mode.

The startup-install *pattern* is verified in `quickwit-cli/src/main.rs:98` — note quickwit calls `install_default_crypto_ring_provider()` (the **ring** provider); PMA deliberately diverges to `aws-lc-rs` for the FIPS path and default-alignment reasons in Lock 1's crypto-core carve-out. Reject any PR that lets `default-features = true` re-enable `native-tls` on dependencies like `reqwest`, `sqlx`, `tonic`, `hyper-util`.

### Lock 3 — `#![forbid(unsafe_code)]` at every crate root

Every `lib.rs` and `main.rs` starts with:

```rust
#![forbid(unsafe_code)]
```

Exceptions (very narrow):
- A crate that genuinely owns FFI or memory layout primitives may relax to `#![deny(unsafe_code)]` and place every `unsafe` block behind a `// SAFETY:` comment that covers aliasing + lifetimes + invariants.
- The pattern in `tokio/src/lib.rs:13` is `#![deny(unsafe_op_in_unsafe_fn)]` — even inside an `unsafe fn`, the `unsafe { … }` block must be explicit. Adopt this in any crate that legitimately uses `unsafe`.

### Lock 4 — Deny warnings as workspace-manifest policy (not CLI, not build flags)

**Rule: deny-warnings policy lives in `Cargo.toml`'s `[workspace.lints]` table.** This is the canonical, manifest-versioned, workspace-global place. It travels with the code, inherits to every crate member, and is visible to `cargo metadata`, crates.io, and reviewers reading the manifest.

What the rule excludes:

- **CI command lines** (`cargo clippy ... -- -D warnings`). Every "passes locally, fails in CI" headache traces to policy in shell scripts. Dev and CI must see the same gate.
- **Shell aliases** (`alias ci-clippy = "clippy ... -- -D warnings"`). Same drift problem.
- **`.cargo/config.toml [build] rustflags = ["-D", "warnings"]`** is a weaker fallback — not wrong, but `[workspace.lints]` supersedes it (priority is clearer, expressivity is higher, inheritance is automatic, future toolchains keep working).

CI scripts and aliases run plain commands:

```yaml
# Right — policy is in [workspace.lints]; CI is just the trigger:
- run: cargo clippy --workspace --all-targets --all-features --locked

# Wrong — duplicates policy on the command line; dev and CI drift:
- run: cargo clippy --workspace --all-targets --all-features --locked -- -D warnings
```

**Path A — workspace lints (canonical).** Used by `cargo`, `rust-analyzer`, `reth`. Centralizes per-lint policy in `Cargo.toml`, supports per-crate opt-out:

```toml
# workspace root Cargo.toml
[workspace.lints.rust]
# Deny every warn-by-default lint, now and forever — `warnings` is rustc's built-in
# group covering current + future warn-level lints. priority -2 lets named lints
# below override (demote noisy ones to warn/allow at default priority 0).
warnings    = { level = "deny", priority = -2 }
unsafe_code = "forbid"
# Opt-in lints (allow-by-default in rustc; we want them on):
missing_debug_implementations = "warn"
missing_docs                  = "warn"
unreachable_pub               = "warn"
elided_lifetimes_in_paths     = "warn"

# Clippy ships sensible defaults: correctness=deny, perf/suspicious/style/complexity=warn.
# We list only deviations from those defaults — restating defaults is noise.
[workspace.lints.clippy]
# Promote allow-by-default groups to warn:
pedantic = { level = "warn", priority = -1 }
nursery  = { level = "warn", priority = -1 }
cargo    = { level = "warn", priority = -1 }
# Tighten individual lints (Lock 6 — no panic in runtime):
unwrap_used        = "deny"
expect_used        = "deny"
panic              = "deny"
todo               = "warn"
dbg_macro          = "deny"
# Relax inside CLI output module(s) only via #![allow(...)] on that boundary:
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

Each crate opts in:
```toml
[lints]
workspace = true
```

Priority rules in brief: lower number is broader. `priority = -2` (the `warnings` group) is the outermost; `priority = -1` (other groups like clippy `pedantic`) wins over it; explicit named lints at default `priority = 0` win over groups. This lets one named `allow` punch through `warnings = deny` cleanly.

Path A above already covers future toolchain warnings via the `warnings` group — no rustflags fallback is needed for that case. The `warnings` group is rustc's built-in name for "every lint currently emitting at warn level", so when a new stable adds a warn-by-default lint, your `[workspace.lints.rust] warnings = "deny"` automatically catches it.

**Path B — build flags (alternative, not preferred).** `vector` uses `.cargo/config.toml:9-15` for historical reasons (pre-`[workspace.lints]` adoption). Documented here for legacy / migration cases only:

```toml
# .cargo/config.toml — older pattern; prefer [workspace.lints] in new projects
[target.'cfg(all())']
rustflags = ["-D", "warnings"]
```

Reach for this only when you cannot use `[workspace.lints]` (e.g. MSRV < 1.74) or need a build-flag scope (e.g. CI env-level override on nightly, as `reth` does via workflow `env: RUSTFLAGS: -D warnings`).

**Dependency builds are safe under deny-warnings.** Cargo automatically passes `--cap-lints=warn` (path deps) or `--cap-lints=allow` (registry / git deps) to non-local crates, so your strict policy applies to your own crates without breaking on transitive warnings. No extra config needed.

**Local opt-out for in-progress work.** A developer iterating on warning-emitting WIP code overrides per-run without changing the policy file:

```bash
RUSTFLAGS="--cap-lints=warn" cargo check     # demote workspace lints for this shell
# or per-call
cargo clippy --workspace -- --cap-lints=warn
```

Policy stays in the repo; only the developer's shell relaxes it for WIP. CI is unaffected.

### Lock 5 — MSRV declared and verified

```toml
[workspace.package]
edition      = "2024"
rust-version = "1.96.0"   # bump deliberately; minor-version cadence; never in patch releases
```

Verify in CI with `cargo hack check --rust-version --workspace --ignore-private --locked` (cargo's pattern, `main.yml:320-323`) **or** `cargo msrv verify` (vector's pattern, `msrv.yml`). PMA baseline policy: track the **latest stable Rust** (currently `1.96.0`); bump the MSRV deliberately in a minor release, never in a patch release. (This intentionally does not adopt Tokio's "support ≥6 months of stable" lag — PMA-managed services build on a controlled, current toolchain rather than guaranteeing older-toolchain compatibility.)

### Lock 6 — No `unwrap` / `expect` / `panic!` in runtime paths

Allowed only in `#[cfg(test)]`, `xtask/`, `build.rs`, and `examples/`. In runtime crates, `unwrap_used`/`expect_used`/`panic` are clippy `deny` (see Lock 4). Where an invariant cannot be expressed in the type system, write `expect("…")` with an `// INVARIANT:` comment, and only after considering whether `Result` would be cleaner.

### Lock 7 — edition 2024

Verified at all 10 standard-bearers (see `references/evidence.md`). New crates and refactors adopt edition 2024. Do not mix editions within a workspace except during a tracked migration.

### Lock 8 — Quality gates green

See `references/delivery.md` for the full CI matrix. Summary:

```
fmt → clippy with workspace deny-warnings policy → nextest run → cargo test --doc →
cargo deny check (advisories + bans + licenses + sources) →
cargo shear (or machete) → typos → release build verification
```

## Known Trade-offs (When the Locks Backfire)

A Hard Lock is the right **default**, not the answer for every project. The discharge mechanism is always the same: a dated decision record in `docs/decisions/` with a sunset condition. The table below tells each ADR what to be specific about.

| Lock | Backfires when… | Discharge |
|---|---|---|
| **1** pure-Rust ecosystem | ML/HPC (BLAS/LAPACK/ONNX/CUDA are 5-10× faster via C bindings); `zstd-safe` beats pure-Rust ports for TB/day pipelines; SQLite, HSMs, hardware codecs, OS audio have no pure-Rust equivalent. Build-time tools (`protoc`, `clang`, `bindgen`) are not Lock 1 violations — they don't ship in the binary. | `// JUSTIFICATION:` next to the dep + `cargo deny` waiver + sunset on parity check |
| **2** rustls only | FIPS 140-3 (banking/federal/health); PKCS#11 / HSM (openssl-engine maturity); TLS 1.0/1.1 legacy gear; FTPS/S/MIME openssl-only protocols. | FIPS needs **no** provider swap — enable the `aws-lc-rs` `fips` feature (uses `aws-lc-fips-sys`; requires CMake + Go at build time, see `toolchain-and-workspace.md` build section). Reach for openssl **only** for the genuinely rustls-shaped gaps (PKCS#11/HSM, legacy TLS, FTPS), scoped to **one** egress client, never the whole process |
| **3** `forbid(unsafe_code)` | Crates that own FFI, memory layout, SIMD, lock-free data structures, or cross-language interop (`pyo3`/`napi-rs`/`cxx`). | Relax to `#![deny(unsafe_code)]` + `// SAFETY:` per block. Tokio's `#![deny(unsafe_op_in_unsafe_fn)]` is the exemplar — explicit `unsafe { … }` even inside `unsafe fn` |
| **4** deny warnings | New stable rustc adds a warn-by-default lint and breaks CI on release day; macro-generated code triggers `missing_docs` even with `#[allow]` at the call site. | Cargo auto-caps deps at `warn`/`allow` — no extra config. Pin toolchain version. Run a non-blocking "newer-stable" job to surface upcoming lints before they bite production |
| **5** MSRV verified | Transitive dep MSRV creep on `cargo update`; `cargo msrv verify` is 10+ min on large monorepos. | Pin offenders in `[workspace.dependencies]` until a deliberate MSRV bump. Use `cargo hack check --rust-version` (faster) over `cargo msrv verify`. CHANGELOG every bump |
| **6** no `unwrap`/`expect`/`panic!` | Genuinely infallible expressions (`Regex::new(LITERAL)`, `OnceLock::get` after init); crashing IS the right response to a violated type-system-inexpressible invariant. | `expect("INVARIANT: <what holds>")` — `INVARIANT:` is grep-able. Reviewers still push toward type-encoding when possible |
| **7** edition 2024 | Brownfield deps that haven't migrated; private toolchains pinned older than 1.85. | Stage migration crate-by-crate. `cargo fix --edition` for the mechanical part. Hold `rust-version` one minor below the edition stabilization release until deps settle |
| **8** quality gates green | `cargo deny advisories` against a live DB fails CI on a new RUSTSEC overnight; `nextest` parallel-by-default exposes latent races that `cargo test` hid. | Split advisories to a scheduled cron, run only `bans + licenses + sources` on PRs (cargo `audit.yml:19-30` pattern). Isolate per-test temp dirs / ephemeral ports; use `[test-groups.serial]` for genuinely shared resources |

## Other Strict Rules — When They Backfire

These are not Hard Locks, but they appear elsewhere in the skill as strong defaults. Same discharge pattern.

| Rule | Backfire scenario | Discharge |
|---|---|---|
| `missing_docs = "warn"` workspace-wide | Application / `bin` crates have no public API; enforcing missing_docs is boilerplate friction. | Apply on **library crates only** via per-crate `[lints.rust] missing_docs = "warn"`. Skip on bin crates. Tokio's pattern: enforced on `tokio` lib, relaxed on examples |
| `print_stdout = "deny"` / `print_stderr = "deny"` | **CLI tools must print** — that is their output. ruff and uv use `println!` / `eprintln!` extensively in their main code. | Allow stdout in the **output module(s)** of CLI bin crates with a focused `#[allow(clippy::print_stdout)] mod output` boundary; deny everywhere else. Use `tracing::info!` over `println!` for diagnostic output that should go to logs |
| `JSON logs in prod` | A small team that tails logs by eye hates JSON without `jq`. | The mandate is "machine-readable in prod, pretty in dev" — a tracing-subscriber switch driven by config, never a build flag. Any operator can override at startup |
| `cargo nextest` (no `cargo test`) | Doctests don't run under nextest; some custom test harnesses (mdtest, cargo-test-attribute hacks) need plain `cargo test`. | Run **both** in CI: `cargo nextest run --workspace` + `cargo test --doc --workspace`. ruff additionally uses `cargo insta test --test-runner nextest --disable-nextest-doctest` |
| `panic = "abort"` in `[profile.dist]` | Code that relies on `std::panic::catch_unwind` (some plugin systems, FFI shims, web framework panic recovery) breaks. tokio task panic isolation still works. | Keep `[profile.release] panic = "unwind"` (the default). Apply `abort` **only** in `[profile.dist]` and verify no transitive dep needs `catch_unwind` (grep the dep tree) |
| `+crt-static` musl for all binaries | Binaries needing **glibc NSS modules** (LDAP user lookup, SSSD, Active Directory join), `dlopen`, or kernel features through libc may break. | Ship glibc target (`*-unknown-linux-gnu`) when these are needed; document in `docs/decisions/`. Both targets can coexist in the release matrix |
| Disable core dumps in **all** environments | Genuinely diagnosing memory corruption (suspected miscompilation, FFI bug) needs cores. | The mandate applies to **production**; dev clusters and the `:debug` image variant may keep cores enabled. Document in the runbook |
| `cargo deny` license allow-list strict | False-positives on licenses like `Apache-2.0 OR MIT` (composite expressions), `MPL-2.0` (file-level copyleft, contentious in compliance reviews), `Unicode-3.0` (replaced `Unicode-DFS-2016`). | Use `version = 2` in `deny.toml` (better SPDX expression handling). Add specific licenses with a comment explaining the legal review outcome. Vector's `deny.toml` adds `MPL-2.0` only via per-crate exception |
| SQLx with `query!` macros | Compile-time check requires either a live DB during build or a committed `.sqlx/` cache. New contributors hit "missing query" errors. | Document `cargo sqlx prepare` in CONTRIBUTING; commit `.sqlx/` to git; CI verifies cache freshness via `cargo sqlx prepare --check` |
| `secrecy::Secret<T>` everywhere | `Secret<String>` does not zeroize on drop unless the inner type is `Zeroize`. False sense of security. | Combine: `Secret<SecretString>` where `SecretString` derives `Zeroize`. Or use `secrecy = { features = ["serde"] }` + custom `Zeroizing` newtype. Audit at every `expose_secret()` call |

## Meta-rule: how to add an exception cleanly

```text
docs/decisions/2026-05-10-allow-openssl-pkcs11.md
```

```markdown
# ADR: Allow openssl for the HSM/PKCS#11 signing path

Status   : Accepted
Date     : 2026-05-10
Sunset   : 2027-06-30 (reassess when rustls PKCS#11 support matures)
Owner    : @platform-team

## Context
Hard Lock 2 mandates rustls with the `aws-lc-rs` provider. FIPS 140-3 alone does **not**
justify an exception — it is satisfied in-stack via the `aws-lc-rs` `fips` feature
(`aws-lc-fips-sys`; CMake + Go at build time). The genuine gap is the regulator-mandated
HSM: private keys never leave the device and must be used via PKCS#11, which rustls's
`aws-lc-rs`/`ring` providers cannot drive today.

## Decision
- Single egress client `crates/api/src/hsm_client.rs` may use `openssl` 0.10 with the
  `vendored` feature for the PKCS#11 engine path only.
- The rest of the process keeps rustls + `aws-lc-rs` (FIPS feature enabled).
- `deny.toml` waives `openssl` only for that one path via a `[[bans.skip]]` entry.

## Consequences
- Image size +5 MB; build now also needs the openssl C toolchain on that target.
- Sunset hard-pinned: a renewal review at 2027-06-30 must either adopt a pure-rustls
  PKCS#11 path or re-justify with a new ADR.
```

This is the discharge contract. PMA `/pma` will accept the project even with the rustls lock relaxed if a matching ADR exists; without one, it blocks merge.

## Tech Stack

### Required

| Category | Technology | Notes / Evidence |
|---|---|---|
| Toolchain | stable Rust, **edition 2024** | `rust-version` in workspace; `rust-toolchain.toml` optional (only vector uses it) |
| Async runtime | **Tokio** (multi-thread) | hand-built `Builder` for tuning (`quickwit-cli/main.rs:43-53`) |
| HTTP server | **Axum 0.8.x** + Hyper 1 + tower / tower-http | gRPC-heavy services: **Tonic** + warp/axum hybrid (quickwit) |
| TLS | **rustls** + **`aws-lc-rs`** provider (rustls 0.23 default) | `rustls::crypto::aws_lc_rs::default_provider().install_default()` early in `main`; startup-install pattern per `quickwit-cli/main.rs:98` (quickwit uses the ring provider) |
| Errors | **`thiserror` 2.x** per crate; **`anyhow`** (or `eyre`) at bin entry only | universal across uv/ruff/quickwit |
| Logging | **`tracing` + `tracing-subscriber`** | JSON in prod, pretty in dev. `quickwit-cli/logger.rs` is canonical |
| Lint policy | `[workspace.lints]` in `Cargo.toml` | Lock 4 |
| Test runner | **`cargo nextest`** + `cargo test --doc` for doctests | 5 of 10 standard-bearers |
| Secrets | **`secrecy`** + **`zeroize`** + **`subtle`** | wrap, redact, constant-time-compare |
| Supply chain | **`cargo-deny`** + **`cargo-shear`** + **`typos`** | uv/ruff use shear; r-a uses machete; cargo/r-a/reth all run typos |

### Default

| Category | Technology | Notes |
|---|---|---|
| Workspace | virtual workspace; **`resolver = "3"`** (edition 2024 pairing) | `"2"` only when stuck on older Cargo |
| Data access | **SQLx** (`default-features = false`, `tls-rustls-aws-lc-rs` feature) | compile-time-checked queries. **Never** native-tls. Alt: **SeaORM** (ActiveRecord) or **`diesel-async`** (compile-time schema) |
| Migrations | `sqlx migrate` / `sea-orm-migration` / `diesel migration` | committed; CI runs against ephemeral DB |
| CLI | **`clap` v4 derive** + **`clap_complete_command`** | quickwit uses builder API for very large CLIs |
| Serialization | **`serde`** + `serde_with` | derive-based |
| Validation | **`validator`** or **`garde`** | derive-based, post-deserialize |
| Config layering | **`figment`** (TOML/YAML + env + CLI) | quickwit rolls a versioned variant for >100-field configs |
| HTTP client | **`reqwest`** with `default-features = false, features = ["rustls-tls", "json"]` | never `native-tls` |
| Caching | **`moka`** | in-process, TTL + size bounds |
| Concurrency | `parking_lot`, `dashmap`, `arc-swap` | only when stdlib primitives don't fit |
| Observability | **`opentelemetry-otlp`** (gRPC + HTTP-JSON) + `tracing-opentelemetry` + `metrics` or `prometheus` | quickwit pins `opentelemetry = 0.31`, `tracing-opentelemetry = 0.32` |
| Runtime metrics | **`tokio-metrics`** | quickwit's `scrape_tokio_runtime_metrics` pattern |
| OpenAPI | **`utoipa`** | quickwit pattern; pin until v5 ecosystem stabilizes |
| Snapshot tests | **`insta`** (`cargo insta test --unreferenced reject --test-runner nextest --disable-nextest-doctest`) | ruff's exact CI line |
| Property tests | **`proptest`** | quickwit |
| Bench | **`criterion`** (or **`divan`** for newer projects) | |
| **Binary runtime hardening** | **`rlimit`** (suppress core dumps) + **`std::panic::set_hook`** (structured panic log) + **mimalloc** (Windows/musl) or **`tikv-jemallocator`** (glibc); `[profile.dist]` uses `panic = "abort"` while `[profile.release]` keeps `unwind` so backtraces work | see `delivery.md` "Disable Core Dumps" and `runtime-and-data.md` `main()` template |
| **Release / distribution** | dual-profile `[profile.release]` + `[profile.dist]`; **`*-unknown-linux-musl` + `+crt-static`** for portable binaries; **`cross`** (Docker) or **`cargo-zigbuild`** (no Docker); **`cargo-dist`** for prebuilt artefacts | uv ships 4 musl targets; ruff uses cargo-dist 0.31 |
| Dev loop | **`just`** as the canonical task runner (cross-project, low learning cost) + **`bacon`** for save-time checks + `cargo nextest` | xtask only when tasks need Rust code (codegen, complex release) |

### Forbidden / Discouraged

Hard bans (enforced by `cargo-deny`):
- **`openssl`, `openssl-sys`, `native-tls`, `native-tls-sys`** — use rustls (Lock 2). reth's `deny.toml:35` is canonical.
- **`git2`, `libgit2-sys`** — prefer `gix` (gitoxide). cargo lists `git2` as a watch item.

Patterns to avoid:
- **`dotenv` (unmaintained) → `dotenvy`**; **`async-trait` macro → native `async fn` in trait** (Rust 1.75+, unless object-safety needed); **`once_cell::sync::Lazy` → `std::sync::LazyLock`** (Rust 1.80+); **`std::collections::HashMap` in hot paths → `FxHashMap`**.
- **`std::sync::Mutex` held across `.await`** — use `tokio::sync::Mutex` or restructure to message passing.
- **`unwrap()` / `expect()` / `panic!`** in runtime crates — see Lock 6.
- **Crates with abandoned advisories** from `cargo-audit` — require an explicit waiver with sunset date.

## Naming (Rust API Guidelines)

| Element | Convention | Guideline ref |
|---|---|---|
| Types and traits | `PascalCase` | C-CASE |
| Functions, modules, file names | `snake_case` | C-CASE |
| Constants and statics | `SCREAMING_SNAKE_CASE` | C-CASE |
| Conversions | `as_*` (cheap ref→ref), `to_*` (expensive owned→owned), `into_*` (consuming) | C-CONV |
| Iterator methods | `iter`, `iter_mut`, `into_iter` | C-ITER |
| Crates | stable, project-prefixed names (e.g. `acme-core`, `acme-api`, `acme-cli`) | C-FEATURE |
| Cargo features | lowercase, hyphenated, **additive only** (no mutually exclusive features) | C-FEATURE |
| Test modules | `mod tests { … }` inline; integration tests under `tests/<feature>.rs` | |
| Bench files | under `benches/<scenario>.rs` | |

Pair every public item with a `Debug` impl (C-DEBUG) and a `///` rustdoc example (C-EXAMPLE). Examples use `?`, never `unwrap()` (C-QUESTION-MARK).

## Dependency Freshness (Rust)

See `/pma references/workflow.md` *Dependency Freshness* for the cross-stack rule. Rust-specific verification:

```bash
# Latest stable version on crates.io
cargo search <crate> --limit 1

# Or via the registry API
curl -s https://crates.io/api/v1/crates/<crate> | jq -r '.crate.max_stable_version'

# Show what would change against current Cargo.lock without writing
cargo update --dry-run

# Find dependencies that are behind latest compatible / latest stable
cargo install cargo-edit  # one-time
cargo upgrade --dry-run --incompatible

# Compare resolved versions vs latest published
cargo install cargo-outdated  # one-time
cargo outdated --workspace
```

When pinning to a non-latest version, add a comment next to the `Cargo.toml` entry:

```toml
[dependencies]
some-crate = "1.4"   # PINNED: 1.5 bumps MSRV to 1.97; revisit after toolchain bump
```

For MSRV-related downgrades, also note in `[workspace.package].rust-version` rationale or `docs/decisions/`.

## Required Conventions

| Area | Convention |
|---|---|
| Error types | per-crate `thiserror` enums; `#[from]` only when conversion is genuinely lossless; `anyhow`/`eyre` only at bin entry / `xtask/` / integration tests |
| Shared state | `Arc<T>` with immutable inner; `arc-swap` for hot reload; **never** `Arc<Mutex<…>>` across `.await` |
| Secrets | wrap in `secrecy::Secret<T>`; redact in `Debug`; compare with `subtle::ConstantTimeEq`; never log |
| CLI | `clap` v4 derive with `#[command(version, about)]`; subcommands as enum variants; `ArgAction::Count` for verbose/quiet (uv pattern, `uv-cli/src/lib.rs:156-219`) |
| Shutdown | `tokio::signal` for SIGINT/SIGTERM; `axum::serve(...).with_graceful_shutdown(...)` paired with `TimeoutLayer`; `CancellationToken` (or `tokio_util::task::TaskTracker`) for fan-out |
| Async traits | use native `async fn` in trait (stable since Rust 1.75); avoid `async-trait` macro for new code unless object-safety is required |
| MSRV | declare `rust-version` in workspace; bump only in minor releases; document in CHANGELOG |
| Async I/O | never call `std::fs`, `std::net`, blocking `std::sync::Mutex` from async tasks; use `tokio::fs` or `tokio::task::spawn_blocking` |

## Code Quality

- prefer immutable data and `&` borrows by default; reach for `&mut` only when mutation is truly needed
- keep files focused — split when a module exceeds ~600 lines or accrues multiple responsibilities
- keep functions small and single-purpose; complex pipelines belong behind named helpers
- prefer iterators and `?`-propagation over imperative loops with manual error tracking
- isolate `unsafe`, FFI, and platform-specific code behind a documented module boundary
- gate optional functionality with **additive** Cargo features (`#[cfg(feature = "…")]`); keep default features minimal so downstream pays only for what they use
- public types implement `Debug` and `Clone` where reasonable (Rust API Guidelines C-COMMON-TRAITS, C-DEBUG)
- newtype wrappers carry meaning that `String`/`u64`/`bool` cannot (C-NEWTYPE, C-CUSTOM-TYPE)
- builders for complex constructors (C-BUILDER); private struct fields by default (C-STRUCT-PRIVATE)
