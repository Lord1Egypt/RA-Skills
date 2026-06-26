# PMA-Rust Evidence Index

This file lists the **verifiable file:line citations** behind every recommendation in this skill. Every claim in `baseline.md`, `toolchain-and-workspace.md`, `runtime-and-data.md`, and `delivery.md` either points to one of these references or is marked as "general convention".

If a future change to this skill is not anchored in real code from a respected project (or in an official Rust guideline), it should be challenged.

## Table of Contents

- [Standard-Bearer Repositories](#standard-bearer-repositories)
- [Workspace, Edition, MSRV (Lock 5, Lock 7)](#workspace-edition-msrv-lock-5-lock-7)
- [Workspace Lints (Lock 4, Path A)](#workspace-lints-lock-4-path-a)
- [Build-Flag Lint Enforcement (Lock 4, Path B)](#build-flag-lint-enforcement-lock-4-path-b)
- [`[workspace.dependencies]` Inheritance](#workspacedependencies-inheritance)
- [`xtask` Patterns](#xtask-patterns)
- [Toolchain & TLS](#toolchain--tls)
- [Tokio API/Lint Policy](#tokio-apilint-policy)
- [Axum 0.8 Patterns](#axum-08-patterns)
- [Tower / Production Stacks](#tower--production-stacks)
- [Database](#database)
- [Configuration](#configuration)
- [Observability (OTLP, metrics, health)](#observability-otlp-metrics-health)
- [Allocator (binaries)](#allocator-binaries)
- [Release Profiles & Binary Size](#release-profiles--binary-size)
- [Cross-Platform / musl](#cross-platform--musl)
- [Crash Handling & Core Dump Suppression](#crash-handling--core-dump-suppression)
- [Linker (build performance)](#linker-build-performance)
- [Testing Tools](#testing-tools)
- [Supply Chain](#supply-chain)
- [Release Automation](#release-automation)
- [Caching / CI Performance](#caching--ci-performance)
- [Official Rust Resources Consulted](#official-rust-resources-consulted)
- [Known Trade-off Citations](#known-trade-off-citations)
- [How to extend this skill](#how-to-extend-this-skill)

## Standard-Bearer Repositories

The 10 projects clone-checked for this skill (paths refer to where they were cloned during research):

| Project | Path used in research |
|---|---|
| `rust-lang/cargo` | `/tmp/pma-rust-research/cargo` |
| `rust-lang/rust-analyzer` | `/tmp/pma-rust-research/rust-analyzer` |
| `paradigmxyz/reth` | `/tmp/pma-rust-research/reth` |
| `vectordotdev/vector` | `/tmp/pma-rust-research/vector` |
| `tokio-rs/tokio` | `/tmp/pma-rust-research/tokio` |
| `tokio-rs/axum` | `/tmp/pma-rust-research/axum` |
| `linkerd/linkerd2-proxy` | `/tmp/pma-rust-research/linkerd2-proxy` |
| `astral-sh/uv` | `/tmp/pma-rust-research/uv` |
| `astral-sh/ruff` | `/tmp/pma-rust-research/ruff` |
| `quickwit-oss/quickwit` | `/tmp/pma-rust-research/quickwit` |

To re-verify any claim:

```bash
git clone --depth 1 --filter=blob:none https://github.com/<org>/<repo>.git
cd <repo> && grep -n "<pattern>" <file>
```

## Workspace, Edition, MSRV (Lock 5, Lock 7)

| Claim | Evidence |
|---|---|
| Edition 2024 widespread | `cargo/Cargo.toml:15`; `rust-analyzer/Cargo.toml:8`; `reth/Cargo.toml:3`; `vector/Cargo.toml:5` |
| `rust-version` MSRV declared in workspace | `cargo/Cargo.toml:14` (`1.93`); `rust-analyzer/Cargo.toml:7` (`1.95`); `reth/Cargo.toml:4` (`1.93`); `vector/Cargo.toml:15` (`1.92`) |
| `resolver = "2"` is the common choice | `cargo/Cargo.toml:2`; `rust-analyzer/Cargo.toml:4`; `reth/Cargo.toml:160` |
| `default-members` is optional | only `reth/Cargo.toml:155` uses it (`["bin/reth"]`); cargo, rust-analyzer, vector do not |
| `rust-toolchain.toml` is optional | only `vector/rust-toolchain.toml` uses it (`channel = "1.92"`). cargo, rust-analyzer, reth do not |
| MSRV 6-month policy | `tokio/CONTRIBUTING.md:30-42` |
| MSRV CI via `cargo hack` | `cargo/.github/workflows/main.yml:320-323` |
| MSRV CI via `cargo msrv verify` | `vector/.github/workflows/msrv.yml` |

## Workspace Lints (Lock 4, Path A)

| Claim | Evidence |
|---|---|
| Workspace `[lints]` widely adopted | `cargo/Cargo.toml:131-145`; `rust-analyzer/Cargo.toml:183-243`; `reth/Cargo.toml:162-259` |
| Per-crate opt-in via `[lints] workspace = true` | `cargo/<member>/Cargo.toml:303` (sample) |
| `rust_2018_idioms = { level = "deny", priority = -1 }` | `reth/Cargo.toml:165` |
| `unsafe_op_in_unsafe_fn` deny | `rust-analyzer/Cargo.toml` (rust group); `tokio/tokio/src/lib.rs:13` |
| `unwrap_used` / `expect_used` / `panic` deny | recommended composition; reth's `[workspace.lints.clippy]` block at `Cargo.toml:173-245` |
| `cargo-cranky` not used in any standard-bearer | confirmed: no `Cranky.toml` in cargo, rust-analyzer, reth, vector, tokio, axum, linkerd2-proxy, uv, ruff, quickwit |

## Build-Flag Lint Enforcement (Lock 4, Path B)

| Claim | Evidence |
|---|---|
| Build-flag enforcement of `-D warnings` | `vector/.cargo/config.toml:9-15` |
| reth applies `-D warnings` on top via CI rustflags | `reth/.github/workflows/lint.yml:60-69` |
| rust-analyzer applies via CI workflow `RUSTFLAGS` env | `rust-analyzer/.github/workflows/ci.yaml:19` |

## `[workspace.dependencies]` Inheritance

| Claim | Evidence |
|---|---|
| Universal pattern | `cargo/Cargo.toml:19-129`; `rust-analyzer/Cargo.toml:51-181`; `reth/Cargo.toml:317+`; `vector/Cargo.toml:138+` |
| Member opts in: `dep = { workspace = true }` | spec: <https://doc.rust-lang.org/cargo/reference/workspaces.html> |

## `xtask` Patterns

| Pattern | Evidence |
|---|---|
| Single `xtask/` (`publish=false`) | `rust-analyzer/xtask/Cargo.toml:1-25` |
| Multiple `xtask-*` crates | `cargo/.cargo/config.toml:1-6` lists 5 split xtask crates |
| Published xtask | `vector/vdev/Cargo.toml:3-10` (`vdev` is on crates.io) |
| No xtask, Makefile + scripts | `reth/.github/scripts/check_wasm.sh`, `reth/Makefile` |
| Common alias pattern | `cargo`, `rust-analyzer`, `vector` all have `cargo <alias>` aliases in `.cargo/config.toml` |

## Toolchain & TLS

| Claim | Evidence |
|---|---|
| Hard ban on `openssl` in deny.toml | `reth/deny.toml:35` (`bans.deny = [{ name = "openssl" }]`) |
| Install rustls crypto provider at startup | `quickwit/quickwit-cli/src/main.rs:98` (`install_default_crypto_ring_provider()`) |
| `rust-toolchain.toml` example | `vector/rust-toolchain.toml` |
| Pinned rustc commit (advanced) | `rust-analyzer/rust-version` (commit hash, used by proc-macro-srv job in `ci.yaml:58-60`) |
| Windows linker tweak via `.cargo/config.toml` | `rust-analyzer/.cargo/config.toml:8-10` (`linker = "rust-lld"`) |
| `mold` linker every job | `reth/.github/workflows/lint.yml:11-30` (`rui314/setup-mold`) |
| `sccache` RUSTC_WRAPPER | `reth/.github/workflows/lint.yml:11-30` (`mozilla-actions/sccache-action`) |

## Tokio API/Lint Policy

| Claim | Evidence |
|---|---|
| `#![deny(unused_must_use, unsafe_op_in_unsafe_fn)]` at lib root | `tokio/tokio/src/lib.rs:13` |
| `#![warn(missing_debug_implementations, missing_docs, rust_2018_idioms, unreachable_pub)]` | `tokio/tokio/src/lib.rs:7-12` |
| MSRV: 6 months stable, only minor-version bumps | `tokio/CONTRIBUTING.md:30-42` |
| Doctest separate from nextest | `tokio/.github/workflows/ci.yml:123-125` (comment: "Cargo nextest does not support doctest") |
| nextest in CI | `tokio/.github/workflows/ci.yml:72-84` |
| `loom` test invocation | `tokio/docs/contributing/pull-requests.md:87-94` |
| `miri` via nextest | `tokio/.github/workflows/ci.yml:386-411` |

## Axum 0.8 Patterns

| Claim | Evidence |
|---|---|
| Path syntax `{name}` (not `:name`) | `axum/examples/key-value-store/src/main.rs:46`; `axum/examples/todos/src/main.rs:51` |
| `Router<S>` is **missing** state type | `axum/axum/src/docs/routing/with_state.md:106-127` |
| Function returning `Router` should not call `with_state` itself | `axum/axum/src/docs/routing/with_state.md:60-68` |
| Sub-router function uses generic `S` | `axum/axum/src/docs/routing/with_state.md:91-95` |
| `axum::serve(...).with_graceful_shutdown(...)` | `axum/examples/graceful-shutdown/src/main.rs:46-49` |
| `TimeoutLayer` paired with graceful shutdown | `axum/examples/graceful-shutdown/src/main.rs:42-44` |
| `tokio::select!` over `ctrl_c` + SIGTERM | `axum/examples/graceful-shutdown/src/main.rs:54-76` |
| Simple `IntoResponse` + blanket `From<E: Into<anyhow::Error>>` | `axum/examples/anyhow-error-response/src/main.rs:34-61` |
| Advanced `IntoResponse` with response-extension logging | `axum/examples/error-handling/src/main.rs:151-215` |
| `AppJson<T>` custom extractor | `axum/examples/error-handling/src/main.rs:136-147` |
| Logging middleware reads response extension | `axum/examples/error-handling/src/main.rs:208-215` |
| `FromRef` substate pattern | `axum/examples/sqlx-postgres/src/main.rs:75-91` |
| `tower::ServiceExt::oneshot` testing | `axum/examples/testing/src/main.rs:65-82` |
| ServiceBuilder `.load_shed().concurrency_limit()` order | `axum/examples/key-value-store/src/main.rs:65-72`; documented in linkerd2-proxy below |

## Tower / Production Stacks

| Claim | Evidence |
|---|---|
| `load-shed` outside `concurrency-limit` | `linkerd2-proxy/linkerd/app/inbound/src/http/server.rs:58-89` (concurrency-limit then `LoadShed::layer()`) |
| Inbound stack ordering: normalize → identity → conc-limit → load-shed → metrics → rescue → tracing → access-log | `linkerd2-proxy/linkerd/app/inbound/src/http/server.rs:58-89` |
| Outbound stack with retries + per-request timeout + identity | `linkerd2-proxy/linkerd/app/outbound/src/http/endpoint.rs:93-131` |
| Budget-based retries (`linkerd_retry::NewRetry::layer`) | `linkerd2-proxy/linkerd/app/outbound/src/http/retry.rs:19-26` |

## Database

| Claim | Evidence |
|---|---|
| SQLx with rustls feature, no native-tls | quickwit's `Cargo.toml` SQLx config; SQLx official docs |
| sqlx::query!/query_as! compile-time check | (general SQLx doc) |
| `cargo sqlx prepare` for offline build | (general SQLx doc) |

## Configuration

| Claim | Evidence |
|---|---|
| `figment` for layered TOML/env/CLI | (general convention; no standard-bearer uses figment specifically — quickwit rolls its own versioned config) |
| Quickwit's versioned config | `quickwit/quickwit-config/src/node_config/serialize.rs:138-149` |
| `clap` derive global flags via `#[arg(global = true)]` | `uv/crates/uv-cli/src/lib.rs:156-219`; `ruff/crates/ruff/src/args.rs:39-79` |
| `ArgAction::Count` for `--quiet` / `--verbose` mutually exclusive | `uv/crates/uv-cli/src/lib.rs:163-168` |
| `clap_complete_command` for shell completions | `uv/crates/uv-cli/Cargo.toml:42`; `ruff/crates/ruff/src/args.rs:171` |
| Custom panic hook on bin entry | `ruff/crates/ruff/src/lib.rs:143-161` |

## Observability (OTLP, metrics, health)

| Claim | Evidence |
|---|---|
| Full tracing + OTLP setup | `quickwit/quickwit-cli/src/logger.rs:122-238` |
| OTLP env-var protocol selection (gRPC/HTTP-protobuf/HTTP-JSON) | `quickwit/quickwit-cli/src/logger.rs:47-105` |
| `opentelemetry = 0.31`, `opentelemetry-otlp = 0.31`, `tracing-opentelemetry = 0.32` | `quickwit/Cargo.toml:174-178, 297` |
| Prometheus metrics with const-label build_info | `quickwit/quickwit-common/src/metrics.rs:25-65`; `quickwit/quickwit-cli/src/main.rs:65-78` |
| `tokio-metrics` runtime scraping | `quickwit/quickwit-cli/src/main.rs:60` |
| `/livez` + `/readyz` handlers | `quickwit/quickwit-serve/src/health_check_api/handler.rs:62-116` |
| `utoipa` OpenAPI annotations | `quickwit/quickwit-serve/src/openapi.rs:41-90` (and per-handler `#[utoipa::path(...)]`) |
| OTel shutdown on exit | `quickwit/quickwit-cli/src/main.rs:119-126` |

## Allocator (binaries)

| Claim | Evidence |
|---|---|
| mimalloc on Windows, jemalloc elsewhere | `ruff/crates/ruff/src/main.rs:11-28` |
| jemalloc page-size config (`JEMALLOC_SYS_WITH_LG_PAGE`) | `vector/.cargo/config.toml:7` |
| Skip jemalloc on musl (extension) | PMA recommendation; jemalloc has known issues on musl. mimalloc is the safe pick |

## Release Profiles & Binary Size

| Claim | Evidence |
|---|---|
| `lto = "fat"` for 10-20% perf | Rust Performance Book — Build Configuration, "Maximize Runtime Speed" |
| `codegen-units = 1` for cross-unit inlining | Rust Performance Book — Build Configuration |
| `panic = "abort"` for size + slight speed | Rust Performance Book — Build Configuration |
| `opt-level = "z"` (smallest) vs `"s"` (balanced) | Rust Performance Book — Minimize Binary Size |
| `strip = "symbols"` for size | Rust Performance Book — Minimize Binary Size |
| `[profile.dev.package."*"] opt-level = 1` (fast deps in dev) | widespread Rust idiom; documented in Bevy / Embark Studios guides |
| `split-debuginfo = "unpacked"` Linux/macOS default | Rust 1.84+ release notes |
| `mold` linker on Linux | `reth/.github/workflows/lint.yml` (`rui314/setup-mold` every job) |
| Custom `[profile.dist]` for cargo-dist | uv `dist-workspace.toml`, ruff `dist-workspace.toml` |

## Cross-Platform / musl

| Claim | Evidence |
|---|---|
| musl-static target list (4 architectures) | `uv/.github/workflows/build-release-binaries.yml:122, 195, 263, 611, 934, 1066, 1199` |
| `+crt-static` is musl default since Rust 1.79 | Rust 1.79 release notes; pin explicitly per PMA Lock |
| `cross` cross-compile driver | uv release pipeline; quickwit composite actions (`./.github/actions/cross-build-binary`) |
| `cargo-zigbuild` alternative | `rust-cross/cargo-zigbuild` README; growing adoption in CI without Docker |
| `gcr.io/distroless/static` (and `:debug` / `:debug-nonroot`) | Google distroless docs (`GoogleContainerTools/distroless`) — official `:debug` variants ship busybox |
| Chainguard `cgr.dev/chainguard/static` Wolfi | Chainguard docs; continuously rebuilt zero-CVE base |
| Canonical chiselled Ubuntu | Canonical chiselled containers documentation; supported on Ubuntu LTS |
| `cargo-chef` for layer caching | `LukeMathWalker/cargo-chef` README; widely adopted in production Rust Dockerfiles |
| Image-pair pattern (minimal + `:debug` tag) | Google distroless `:debug` variants exist precisely for this |
| `apk add musl-tools` for Linux musl builds | `rust:*-alpine` Dockerfile convention |
| OpenSSL/native-tls breaks musl static linking | `cross` docs; cargo-deny `[bans.deny]` recommendation |

## Crash Handling & Core Dump Suppression

| Claim | Evidence |
|---|---|
| `RLIMIT_CORE` to suppress core dumps | Linux man `getrlimit(2)` / `setrlimit(2)`: "RLIMIT_CORE — maximum size of a core file" |
| `rlimit` pure-Rust crate | <https://crates.io/crates/rlimit> — bindings-free, no `*-sys` |
| `LimitCORE=0` in systemd | systemd `systemd.exec(5)` man page: "LimitCORE=" sets `RLIMIT_CORE` |
| `--ulimit core=0:0` in Docker | Docker run reference: <https://docs.docker.com/reference/cli/docker/container/run/#ulimit> |
| `kernel.core_pattern = \|/bin/false` | Linux man `core(5)`: piping core_pattern with `|` sends the core to a program; `/bin/false` discards it |
| `fs.suid_dumpable = 0` | Linux man `proc(5)`: `/proc/sys/fs/suid_dumpable` controls whether setuid/setgid processes dump cores |
| `std::panic::set_hook` for structured panic logging | <https://doc.rust-lang.org/std/panic/fn.set_hook.html> |
| `std::backtrace::Backtrace::force_capture` | <https://doc.rust-lang.org/std/backtrace/struct.Backtrace.html#method.force_capture> |
| `tracing-error::SpanTrace` for span chains in errors | <https://docs.rs/tracing-error/> |
| Cores leak secrets (motivation) | Linux man `core(5)` + general security guidance; secrecy crate's threat model assumes no on-disk memory snapshots |

## Linker (build performance)

| Claim | Evidence |
|---|---|
| `mold` linker every CI job | `reth/.github/workflows/lint.yml` (universal `rui314/setup-mold@v1`) |
| `rust-lld` for Windows MSVC | `rust-analyzer/.cargo/config.toml:8-10` (`linker = "rust-lld"`) |
| `lld` on macOS | Rust Performance Book — Compile Times |

## Testing Tools

| Claim | Evidence |
|---|---|
| `cargo nextest` widespread | `rust-analyzer/.github/workflows/ci.yaml:116`; `reth/.github/workflows/unit.yml:57`; `vector/.config/nextest.toml`; `tokio/.github/workflows/ci.yml:72-84`; `uv/.config/nextest.toml`; `ruff/.config/nextest.toml`; `quickwit/.config/nextest.toml` |
| nextest profiles `default`/`ci` with retries | `reth/.config/nextest.toml`; `uv/.config/nextest.toml` (multi-platform profiles); `ruff/.config/nextest.toml` |
| `cargo insta test --unreferenced reject --test-runner nextest --disable-nextest-doctest` | `ruff/.github/workflows/ci.yaml:323` |
| `insta` integration | `uv/Cargo.toml:328` (`insta` with json/filters/redactions); `ruff/Cargo.toml:121` |
| `proptest` | `quickwit/Cargo.toml:191` |
| `tower::ServiceExt::oneshot` test | `axum/examples/testing/src/main.rs:65-82` |
| `loom` for concurrency tests | `tokio/docs/contributing/pull-requests.md:87-94` |
| `cargo-fuzz` policy | `tokio/docs/contributing/pull-requests.md:152-171` |
| GHA `services:` for Postgres in CI (no testcontainers) | `quickwit/.github/workflows/ci.yml:38-53` |

## Supply Chain

| Claim | Evidence |
|---|---|
| `deny.toml` advisories.yanked = "warn" | `cargo/deny.toml:70`; `reth/deny.toml:5`; `vector/deny.toml:42-54` (ignore list pattern) |
| License allow-list (mostly identical across projects) | `cargo/deny.toml:92-103`; `reth/deny.toml:51-69`; `vector/deny.toml:1-18` |
| `bans.deny = [{ name = "openssl" }]` | `reth/deny.toml:35` |
| `cargo-deny` run via `EmbarkStudios/cargo-deny-action@v2` | `cargo/.github/workflows/audit.yml:19-30`; `vector/.github/workflows/deny.yml`; `quickwit/.github/workflows/ci.yml:172-176` |
| `cargo-deny check licenses` (just licenses) | `quickwit/.github/workflows/ci.yml:191-194` |
| `cargo-shear --deny-warnings` | `uv/.github/workflows/check-lint.yml:145-157`; `ruff/.github/workflows/ci.yaml:765-776` |
| `cargo-machete` | `rust-analyzer/.github/workflows/ci.yaml:125-129`; `quickwit/.github/workflows/ci.yml:177-181` |
| `cargo-udeps` | `reth/.github/workflows/lint.yml:227` |
| `cargo-hack` for MSRV verification | `cargo/.github/workflows/main.yml:320-323` |
| `cargo-hack check --workspace --partition` | `reth/.github/workflows/lint.yml:128-144` |
| `cargo-msrv verify` | `vector/.github/workflows/msrv.yml` |
| `crate-ci/typos` | `cargo/.github/workflows/main.yml:331`; `rust-analyzer/.github/workflows/ci.yaml:319-322`; `reth/.github/workflows/lint.yml:261`; `uv/.github/workflows/check-lint.yml:159-165` |
| `zepter run check` (feature propagation) | `reth/.github/workflows/lint.yml:324` |
| `dprint/check@v2.3` (TOML formatting) | `reth/.github/workflows/lint.yml:274` |

## Release Automation

| Claim | Evidence |
|---|---|
| `cargo-dist` for prebuilt binaries | `uv/.github/workflows/release.yml` (`CARGO_DIST_VERSION`); `ruff/.github/workflows/release.yml:1-3` (autogenerated header, `CARGO_DIST_VERSION: 0.31.0`) |
| Multi-target release matrix (uv) | `uv/.github/workflows/build-release-binaries.yml:122, 195, 263, 611, 934, 1066, 1199` (9 targets) |
| Service custom release pipeline | `quickwit/.github/workflows/publish_release_packages.yml`; `vector/.github/workflows/publish.yml` |
| reth reproducible build | `reth/Dockerfile.reproducible` |
| `release-plz` not used in our 10 standard-bearers | confirmed by grep across all 10 repos |

## Caching / CI Performance

| Claim | Evidence |
|---|---|
| `Swatinem/rust-cache@v2.9.1` every job | `reth/.github/workflows/lint.yml` (universal) |
| Self-hosted runners conditional | `reth/.github/workflows/lint.yml` (`depot-ubuntu-latest` fallback) |

## Official Rust Resources Consulted

| Resource | URL |
|---|---|
| Rust API Guidelines (full checklist) | <https://rust-lang.github.io/api-guidelines/checklist.html> |
| The Cargo Book — Workspaces | <https://doc.rust-lang.org/cargo/reference/workspaces.html> |
| The Cargo Book — Lints inheritance (`[workspace.lints]`, MSRV 1.74+) | <https://doc.rust-lang.org/cargo/reference/manifest.html#the-lints-section> |
| Tokio Topics — Graceful Shutdown | <https://tokio.rs/tokio/topics/shutdown> |
| Tokio CONTRIBUTING — MSRV / SemVer | <https://github.com/tokio-rs/tokio/blob/master/CONTRIBUTING.md> |
| Rust Performance Book — Build Configuration | <https://nnethercote.github.io/perf-book/build-configuration.html> |
| cargo-deny Checks | <https://embarkstudios.github.io/cargo-deny/checks/index.html> |

## Known Trade-off Citations

| Backfire pattern | Evidence |
|---|---|
| `--cap-lints=warn` for transitive deps | Cargo Reference: <https://doc.rust-lang.org/cargo/commands/cargo-rustc.html#options> (`--cap-lints` is the per-crate cap that `RUSTFLAGS` controls workspace-wide) |
| Separate scheduled `cargo deny advisories` job | `cargo/.github/workflows/audit.yml:19-30` (matrix splits advisories from bans/licenses/sources) |
| `aws-lc-rs` as the FIPS-validated rustls provider | <https://github.com/aws/aws-lc-rs> + rustls 0.23 release notes; AWS-LC has FIPS 140-3 cert |
| Tokio enforces `missing_docs` on lib only, not all members | `tokio/tokio/src/lib.rs:7-12` shows the lib-level `#![warn(missing_docs)]`; tokio's examples and benches do not warn missing docs |
| ruff prints to stdout in normal operation (CLI tool exception) | `ruff/crates/ruff/src/main.rs` calls `eprintln!` and `println!` directly; clippy `print_stdout` not denied at workspace level for that crate |
| Vector allows `MPL-2.0` license per-crate, not globally | `vector/deny.toml:22-31` (per-crate exception list) |
| `cargo nextest` doctest gap | `tokio/.github/workflows/ci.yml:123-125` ("Cargo nextest does not support doctest, so we run them separately") |
| `panic = "abort"` breaks `catch_unwind` | Rust Reference — Panic / Unwinding: <https://doc.rust-lang.org/reference/runtime.html#the-panic_handler-attribute> (catch_unwind requires `panic = "unwind"`) |
| `+crt-static` musl + glibc NSS incompatibility | musl wiki + `cross` documentation — NSS plugins require dynamic glibc; musl-static cannot dlopen glibc NSS modules |
| `cargo sqlx prepare` and `.sqlx/` cache | <https://github.com/launchbadge/sqlx/blob/main/sqlx-cli/README.md#enable-building-in-offline-mode-with-query> |
| `secrecy::Secret<T>` does not auto-zeroize | `secrecy` README explicitly says zeroization happens "if the wrapped type implements Zeroize"; bare `Secret<String>` does not zeroize the heap allocation |
| ADR template / decision-record convention | Michael Nygard's "Documenting Architecture Decisions" + RFC tradition; widely used (e.g., adr-tools, MADR) |

## How to extend this skill

If you add a new recommendation:

1. Find a citation in one of the 10 standard-bearers, an official Rust guideline, or another widely respected project (>5k GitHub stars + active maintenance).
2. Add the citation to this file with `<repo>/<file>:<line>`.
3. Reference this file from the relevant pack so the chain of evidence is traceable.
4. If no citation exists, mark the recommendation explicitly as "general convention" or "PMA opinion".

A skill that defines acceptance criteria must be reproducible by the next reader. Citations make that possible.
