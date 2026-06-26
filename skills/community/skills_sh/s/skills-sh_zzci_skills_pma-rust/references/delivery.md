# PMA-Rust Delivery

This pack covers everything between "code compiles" and "shipped to prod": secrets, observability, testing, supply-chain, release automation, CI, and Git. Every recommendation is anchored to a verified standard-bearer; see `references/evidence.md`.

## Table of Contents

- [Security](#security)
- [Logging And Observability](#logging-and-observability)
- [Testing](#testing)
- [Supply Chain](#supply-chain)
- [Release Automation](#release-automation)
- [CI Pipeline](#ci-pipeline)
- [Git Conventions](#git-conventions)
- [Review Focus](#review-focus)

## Security

### Threat surface to review

- **TLS** — rustls only. Reject any direct or transitive `openssl` / `native-tls` (enforced via `cargo deny bans` — reth's `deny.toml:35` is the exemplar).
- **Crypto provider** — `rustls::crypto::aws_lc_rs::default_provider().install_default()` early in `main` (startup-install timing per quickwit's `main.rs:98`, which itself installs the ring provider). Without this, rustls 0.23 panics on first TLS use. Build prerequisites for the `aws-lc-rs` C/asm core: see `toolchain-and-workspace.md` "Building the `aws-lc-rs` crypto provider".
- **Outbound HTTP / SSRF** — validate destination hostnames; block link-local / loopback unless allow-listed; reuse `reqwest::Client`, never per-request.
- **Secret comparison** — use `subtle::ConstantTimeEq` for tokens, HMACs, password digests.
- **Cache correctness under contention** — `moka` over hand-rolled `Arc<Mutex<HashMap>>`; `arc-swap` for hot-reload of immutable config.
- **Secret redaction** — wrap in `secrecy::Secret<T>`; never `Debug`/`Display`-format; redact request headers via `SetSensitiveRequestHeadersLayer` (see `runtime-and-data.md`).
- **Auth boundaries** — single auth middleware; handlers receive a typed `CurrentUser` extension, never raw tokens.
- **Input validation** — `validator`/`garde` at the request boundary; never trust deserialized values without bounds.
- **Path traversal / TOCTOU** — canonicalize paths, reject `..` segments; consider `cap-std` for sandboxed file IO.

### Secret handling

```rust
use secrecy::{ExposeSecret, Secret};

#[derive(Clone, serde::Deserialize)]
pub struct DbConfig {
    pub url: Secret<String>,        // not Debug-printable, zeroized on drop
}

let url = cfg.db.url.expose_secret();   // only here, at the moment of use
```

Rules:

- secrets enter the process via env or config file, never via CLI argument in shared shells
- redact request bodies that may carry tokens **before** logging
- rotate secrets out of band; the app reloads via SIGHUP or scheduled refresh, never via redeploy alone

### Disable Core Dumps

Production Rust services **must not** produce `core` files. A core is an unredacted memory snapshot — every `secrecy::Secret` value, every JWT in flight, every cached query containing PII goes to disk in cleartext, often into a volume that backups, log shippers, or sidecars can read. Cores also fill disks fast and slow restart on crash loops.

Suppress at **all four layers** so a single config drift cannot defeat the policy.

#### Layer 1 — In-process (most reliable)

Lives in `main` before any panic-able code runs. See the canonical template in `references/runtime-and-data.md` (Tokio Runtime section). Excerpt:

```rust
#[cfg(unix)]
{
    use rlimit::{setrlimit, Resource};
    setrlimit(Resource::CORE, 0, 0).ok();
}
```

`rlimit = "0.10"` is pure Rust (no C bindings) — satisfies Hard Lock 1. This call survives container restarts, systemd reload, and outer ulimit changes; the in-process policy is the inner defense.

#### Layer 2 — systemd unit (bare-metal / VM)

```ini
# /etc/systemd/system/acme.service
[Service]
ExecStart       = /usr/local/bin/acme
LimitCORE       = 0
NoNewPrivileges = true
ProtectSystem   = strict
ProtectHome     = true
PrivateTmp      = true
ReadWritePaths  = /var/lib/acme
DynamicUser     = yes        # ephemeral uid/gid; no on-disk user account
```

`LimitCORE = 0` overrides the default `infinity` on systemd. Pair with the hardening directives so even if a core were produced, it cannot land in a writable path.

#### Layer 3 — Container runtime

**Docker / Podman:**

```bash
docker run --ulimit core=0:0 acme:v1.2.3
```

`docker compose`:

```yaml
services:
  acme:
    image: acme:v1.2.3
    ulimits:
      core:
        soft: 0
        hard: 0
```

**Kubernetes** does not expose `RLIMIT_CORE` directly via PodSpec, so the in-process Rust call (Layer 1) carries the policy. Belt-and-suspenders options at the cluster level:

```yaml
# PodSecurity / SecurityContext — limits the blast radius of a core if one slipped through
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 65532
    readOnlyRootFilesystem: true
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: acme
      image: acme:v1.2.3
      securityContext:
        allowPrivilegeEscalation: false
        capabilities:
          drop: ["ALL"]
```

`readOnlyRootFilesystem: true` plus a writable `emptyDir` only for explicit paths means the kernel has nowhere to write the core. Combined with a `core_pattern` set to `|/bin/false` on the node (Layer 4), this is sufficient.

#### Layer 4 — Kernel (node-level, ops responsibility)

Document this in the runbook so SRE/platform teams pin it on every node:

```bash
# /etc/sysctl.d/99-no-coredump.conf
kernel.core_pattern        = |/bin/false
fs.suid_dumpable           = 0

# Apply
sysctl --system
```

```bash
# /etc/security/limits.d/99-no-coredump.conf
*  hard  core  0
*  soft  core  0
```

`kernel.core_pattern = |/bin/false` pipes any core to a no-op program — even a process that bypasses ulimit cannot write to disk.

#### Verify

After deploy, confirm the policy holds:

```bash
# Inside the running pod / container:
cat /proc/$(pgrep acme)/limits | grep "Max core file size"
# Expected: "Max core file size    0    0    bytes"

# Trigger a controlled crash (staging only) and confirm no core file lands:
kill -SIGABRT $(pgrep acme)
find / -name 'core*' -newer /tmp/sentinel 2>/dev/null
# Expected: empty
```

#### What replaces post-mortem from cores

You still need crash diagnostics — just not on disk:

- **`std::panic::set_hook`** (template in `runtime-and-data.md`) emits a structured `tracing::error!` with the panic message, location, and a forced-capture `Backtrace`. The log pipeline (loki, OTLP, CloudWatch) captures it.
- **`tracing-error::SpanTrace`** attaches the active tracing span chain to errors so you see "what was the request doing" without a heap snapshot.
- **`sentry-rust`** (or self-hosted GlitchTip) for symbolicated panic capture if your org standardizes on that.
- For genuine debugging needs (rare, suspected memory corruption), enable cores **only in a debug image** and only in a non-production cluster; never in prod.

### Pre-commit checklist

- no hardcoded secrets, API keys, or fixtures with real PII
- no `unwrap`/`expect`/`panic!` in runtime paths (see `baseline.md` Lock 6)
- auth boundaries reviewed when handler shapes change
- `unsafe` is absent (`#![forbid(unsafe_code)]`) or has `// SAFETY:` justification covering aliasing + lifetimes
- new outbound calls go through the central HTTP client (so timeouts, retries, TLS config are inherited)

## Logging And Observability

Single pipeline for **logs + traces + metrics**. The fullest standard-bearer reference is quickwit's `quickwit-cli/src/logger.rs`.

### `tracing` setup (verified, quickwit's `logger.rs:122-238`)

```rust
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt, EnvFilter};

pub fn init(cfg: &TelemetryConfig, build: &BuildInfo) -> anyhow::Result<TelemetryGuards> {
    use opentelemetry::global;
    use opentelemetry_otlp::WithExportConfig;
    use opentelemetry_sdk::propagation::TraceContextPropagator;
    use opentelemetry_sdk::Resource;

    global::set_text_map_propagator(TraceContextPropagator::new());

    let filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new(&cfg.log_level));

    let fmt_layer = tracing_subscriber::fmt::layer()
        .with_target(true)
        .with_timer(tracing_subscriber::fmt::time::UtcTime::rfc_3339());

    let registry = tracing_subscriber::registry().with(filter);
    let registry = if cfg.json {
        registry.with(fmt_layer.json().boxed())
    } else {
        registry.with(fmt_layer.boxed())
    };

    if cfg.otlp_enabled {
        let resource = Resource::builder()
            .with_service_name(env!("CARGO_PKG_NAME"))
            .with_attribute(opentelemetry::KeyValue::new("service.version", build.version.clone()))
            .build();

        let exporter = opentelemetry_otlp::SpanExporter::builder()
            .with_tonic()
            .with_endpoint(&cfg.otlp_endpoint)
            .build()?;

        let tracer_provider = opentelemetry_sdk::trace::SdkTracerProvider::builder()
            .with_batch_exporter(exporter)
            .with_resource(resource)
            .build();

        let tracer = tracer_provider.tracer(env!("CARGO_PKG_NAME"));
        registry.with(tracing_opentelemetry::layer().with_tracer(tracer)).try_init()?;
        Ok(TelemetryGuards::otlp(tracer_provider))
    } else {
        registry.try_init()?;
        Ok(TelemetryGuards::stdout())
    }
}
```

### Conventions

- **JSON in prod, pretty in dev** — driven by config, not by build flag
- one **structured field** per piece of context: `tracing::info!(user_id = %id, "created user")` — never string-interpolate fields into the message
- spans wrap meaningful work; `#[tracing::instrument(skip(db, secret))]` to keep volume manageable
- logs and traces correlate via OpenTelemetry trace context — `TraceLayer` injects the current span automatically
- expose `/livez` (liveness, no deps) and `/readyz` (readiness, includes DB ping) — see `runtime-and-data.md`
- respect standard OTel env vars: `OTEL_EXPORTER_OTLP_PROTOCOL`, `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_EXPORTER_OTLP_TRACES_PROTOCOL`, `OTEL_EXPORTER_OTLP_LOGS_PROTOCOL` (quickwit's `logger.rs:47-105` pattern)

### Metrics

- **`metrics`** crate as the API; **`metrics-exporter-prometheus`** for scrape, **or** ship via OTLP metrics
- **`tokio-metrics`** for runtime visibility (worker thread parks, scheduler ticks). Quickwit's `scrape_tokio_runtime_metrics(rt.handle(), "main")` is the canonical pattern.
- standard names: `http_requests_total`, `http_request_duration_seconds`, `db_pool_size`, `task_inflight`
- histograms for latencies, gauges for resource state, counters for events
- emit a **build_info** const-label gauge so dashboards can correlate by version (quickwit's `register_build_info_metric` in `main.rs:65-78`)

### Allocator selection (binaries only)

ruff's pattern (`crates/ruff/src/main.rs:11-28`):

```rust
#[cfg(target_os = "windows")]
#[global_allocator]
static GLOBAL: mimalloc::MiMalloc = mimalloc::MiMalloc;

#[cfg(all(not(target_os = "windows"), not(target_env = "musl"), not(target_arch = "wasm32")))]
#[global_allocator]
static GLOBAL: tikv_jemallocator::Jemalloc = tikv_jemallocator::Jemalloc;
```

`mimalloc` on Windows (better than the system allocator), `jemalloc` on Linux/macOS GNU. Skip on musl (jemalloc has known issues there). Library crates **never** install global allocators.

## Testing

Layered, with a runner that scales:

| Layer | Tool | Where | Verified at |
|---|---|---|---|
| Unit | `#[test]` + `tokio::test` | inside crate `mod tests` | universal |
| Integration | `tokio::test` + `tower::ServiceExt::oneshot` or `axum::serve` | `tests/<feature>.rs` or per-crate `tests/it/` | uv (`crates/uv/tests/it/`) |
| Snapshot | **`insta`** | API responses, OpenAPI dumps, generated SQL | uv, ruff, quickwit |
| Property | **`proptest`** | parsers, encoders, invariants | quickwit |
| HTTP mocks | **`wiremock`** | external API contracts | (general convention) |
| Real deps | GHA `services:` block, or **`testcontainers-rs`** | CI integration | quickwit uses GHA `services:` (no testcontainers) |
| Bench | **`criterion`** (or **`divan`**) | regression-tracked, run on `main` | uv (`benches/`) |
| Mutation | **`cargo-mutants`** | gates on critical crates only | (general) |
| Fuzz | **`cargo-fuzz`** (libFuzzer) | parsers, deserializers | tokio CONTRIBUTING |
| Coverage | **`cargo-llvm-cov`** | report to LCOV / Codecov | (general) |
| Concurrency | **`loom`** | non-trivial atomics / lock-free code only | tokio CI |

### Runner: `cargo nextest`

The default and de-facto standard. Verified at rust-analyzer, reth, vector, tokio, uv, ruff, quickwit. Doctests are **not** supported by nextest — run separately:

```bash
cargo nextest run --workspace --all-features --locked
cargo test --doc --workspace --all-features --locked
```

`.config/nextest.toml` template (composes patterns from reth + uv + ruff):

```toml
[profile.default]
retries = 0
slow-timeout = { period = "30s", terminate-after = 2 }

[profile.ci]
retries = { count = 2, backoff = "exponential", delay = "1s" }
fail-fast = false
final-status-level = "fail"
failure-output = "immediate-final"   # ruff pattern, .config/nextest.toml
junit.path = "target/nextest/ci/junit.xml"

[test-groups.serial]
max-threads = 1                       # for tests that lock shared resources
```

### `insta` snapshot tests

Used by uv (with the `uv_snapshot!` macro wrapping `assert_cmd_snapshot!`), ruff, swc, cargo. Reviewable diffs:

```rust
#[test]
fn renders_user_response() {
    let body = render_user(User { id: 1, email: "a@b".into() });
    insta::assert_json_snapshot!(body);
}
```

CI command (ruff's exact pattern, `.github/workflows/ci.yaml:323`):

```bash
cargo insta test --all-features --unreferenced reject --test-runner nextest --disable-nextest-doctest
```

`--unreferenced reject` fails CI when there are stale `.snap` files; `--disable-nextest-doctest` because nextest can't run doctests anyway. Review locally with `cargo insta review`. Commit `*.snap` files; never commit `*.snap.new`.

### Contract & integration tests

Two equally valid approaches for tests that need real services:

**A — GHA `services:` block (quickwit pattern)** — start Postgres/Kafka/etc as part of the GitHub job, point tests at `localhost`:

```yaml
jobs:
  it:
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: password
        ports: ["5432:5432"]
```

**B — `testcontainers-rs`** — programmatic, works locally:

```rust
let pg = testcontainers_modules::postgres::Postgres::default().start().await?;
let pool = build_pool(pg.connect_url()).await;
```

Pick A when CI is the dominant test environment; pick B when developers need to run integration tests on their laptops without Docker Compose. Both are observed in production.

Common rules:

- never share state between tests; each integration test gets its own ephemeral schema or container
- avoid `#[ignore]` — gate slow tests behind a nextest profile or feature flag instead
- run doctests via `cargo test --doc` separately in CI

## Supply Chain

`deny.toml` is the single source of truth for what may enter the dependency graph. Pattern composes cargo, reth, vector, and quickwit's actual policies.

```toml
[advisories]
yanked = "warn"               # cargo, reth, vector all use "warn" — not "deny" — to avoid CI flakiness on transient yanks
ignore = []                   # explicit waivers, with comment + tracking issue + sunset date

[licenses]
version = 2
allow = [
    "Apache-2.0", "Apache-2.0 WITH LLVM-exception", "MIT", "MIT-0",
    "BSD-2-Clause", "BSD-3-Clause", "BSL-1.0", "0BSD",
    "ISC", "Unicode-3.0", "CC0-1.0", "CDLA-Permissive-2.0",
    "Zlib",
    # Add MPL-2.0 only if the project accepts file-level copyleft (vector includes it).
]
confidence-threshold = 0.93

[bans]
multiple-versions = "warn"
deny = [
    # === Hard locks from baseline.md ===
    { name = "openssl",       reason = "use rustls (Lock 1)" },
    { name = "openssl-sys",   reason = "use rustls (Lock 1)" },
    { name = "native-tls",    reason = "use rustls (Lock 1)" },
    { name = "native-tls-sys",reason = "use rustls (Lock 1)" },
    # === Discouraged ===
    { name = "git2",          reason = "use gix (gitoxide) when feasible" },
    { name = "libgit2-sys",   reason = "use gix (gitoxide) when feasible" },
    { name = "dotenv",        reason = "unmaintained — use dotenvy" },
    { name = "ring",          version = "<0.17", reason = "0.16 has known soundness issues" },
]

[sources]
unknown-registry = "deny"
unknown-git      = "deny"
allow-git        = []         # opt-in for vetted forks
```

Verified: reth's hard ban on `openssl` is exactly `bans.deny = [{ name = "openssl" }]` at `deny.toml:35`. Quickwit's `deny.toml` is 7.3K with a much larger allow-list — adapt to the project's compliance posture.

Pair with:

- **`cargo-audit`** for the RustSec advisory DB (tokio + ecosystem run this nightly)
- **`cargo-shear`** (uv + ruff) **or** **`cargo-machete`** (rust-analyzer, quickwit) — find unused dependencies. `cargo-shear` is newer and faster; both work.
- **`cargo-vet`** if your org maintains audits (heavy, only for security-critical projects).
- **`crate-ci/typos`** in CI (cargo, rust-analyzer, reth, uv all use it).

## Release Automation

| Project type | Recommended tools | Verified at |
|---|---|---|
| **Crate libraries** (publish to crates.io) | `release-plz` (changelog + version bump + publish) | (general convention; not yet used by our 10 standard-bearers) |
| **CLI binaries** (uv, ruff style) | **`cargo-dist`** + GitHub Releases | uv `release.yml` + `build-release-binaries.yml`, ruff `release.yml` |
| **Services** (quickwit, vector style) | Custom matrix workflow with `cross` for Linux, native runners for macOS/Windows | quickwit `publish_release_packages.yml`, vector `publish.yml` |

### `cargo-dist` (default for CLI distributions)

Verified at `astral-sh/uv` and `astral-sh/ruff`. Generates GitHub Actions release workflow + `dist-workspace.toml`. The 9-target matrix uv ships (verified at `uv/.github/workflows/build-release-binaries.yml:122, 195, 263, 611, 934, 1066, 1199`):

| Target triple | Use | Build host |
|---|---|---|
| `x86_64-apple-darwin` | macOS Intel | `macos-13` GHA runner |
| `aarch64-apple-darwin` | macOS Apple Silicon | `macos-14` GHA runner |
| `x86_64-unknown-linux-musl` | **static**, runs on any glibc/musl Linux | `ubuntu-latest` + `cross` |
| `aarch64-unknown-linux-musl` | **static** ARM64 Linux (Graviton, RPi 4/5, AWS GP) | `ubuntu-latest` + `cross` |
| `armv7-unknown-linux-musleabihf` | **static** 32-bit ARM (RPi 2/3, embedded) | `ubuntu-latest` + `cross` |
| `riscv64gc-unknown-linux-musl` | **static** RISC-V | `ubuntu-latest` + `cross` |
| `s390x-unknown-linux-gnu` | IBM Z mainframe (glibc, niche) | `ubuntu-latest` + `cross` |
| `x86_64-pc-windows-msvc` | Windows Intel | `windows-latest` |
| `aarch64-pc-windows-msvc` | Windows ARM | `windows-latest` (cross via MSVC) |

The musl variants are why uv works in `FROM scratch` containers and on Alpine. Same pattern is recommended for any PMA-Rust CLI.

`dist-workspace.toml` template (matches uv/ruff's posture):

```toml
[dist]
cargo-dist-version = "0.31.0"
ci                 = ["github"]
installers         = ["shell", "powershell", "homebrew"]   # add npm if Node ecosystem
targets            = [
    "x86_64-apple-darwin",
    "aarch64-apple-darwin",
    "x86_64-unknown-linux-musl",      # glibc-free, runs anywhere
    "aarch64-unknown-linux-musl",
    "x86_64-pc-windows-msvc",
    "aarch64-pc-windows-msvc",
]
include            = ["LICENSE", "README.md"]
pr-run-mode        = "plan"
unix-archive       = ".tar.gz"
windows-archive    = ".zip"
github-build-setup = "github-build-setup.yml"             # custom apt installs (musl-tools, etc.)

[dist.dependencies.apt]                                   # for the `*-musl` linux builders
musl-tools          = "*"
```

Pair with **`cargo-binstall`** so end users get prebuilt binaries automatically: `cargo binstall myapp` finds the right musl/macOS/Windows artifact based on the host.

### Cross-compilation tooling

Two valid drivers, pick one per project:

| Tool | When to pick | Notes |
|---|---|---|
| **`cross`** (`cross-rs/cross`) | Default. Docker-based, vetted toolchains for every Rust target | Requires Docker on the build host; that's CI-friendly, less so on laptops |
| **`cargo-zigbuild`** (`rust-cross/cargo-zigbuild`) | When Docker is unavailable (corporate laptops, CI without privileged containers) | Uses Zig as cross-linker; supports glibc version selection (e.g. `--target x86_64-unknown-linux-gnu.2.17`) |

Both invoke `cargo` with the right linker/sysroot pair; both honor your `[profile.dist]`. uv's release pipeline uses `cross`; quickwit uses GHA composite actions wrapping `cross`.

### Container images

**Do not mandate a single base image.** Pick by ops requirements, document the choice in `docs/decisions/<adr>.md`. The build stage is shared; the runtime stage is the variable.

#### Build stage (shared — `cargo-chef` layer caching)

```dockerfile
# === Build stage (shared across all runtime variants) ===
FROM rust:1.96.0 AS chef
RUN cargo install cargo-chef --locked
WORKDIR /src

FROM chef AS planner
COPY . .
RUN cargo chef prepare --recipe-path recipe.json

FROM chef AS builder
COPY --from=planner /src/recipe.json recipe.json
# Build deps once and cache the layer
RUN cargo chef cook --profile dist --target x86_64-unknown-linux-musl --recipe-path recipe.json
COPY . .
RUN cargo build --profile dist --target x86_64-unknown-linux-musl --locked
```

`cargo-chef` keeps the dependency graph in a separate cached layer so most rebuilds reuse it — verified across many production Rust Dockerfiles.

#### Runtime base image — pick by need

| Base | Use when | Trade-offs |
|---|---|---|
| **`FROM scratch`** | Smallest possible (just the binary). Static-musl only. | No shell, no CA bundle, no `/tmp`, no DNS resolver behavior changes — must bundle CA certs (`rustls-native-certs` won't work; ship `webpki-roots`) |
| **`gcr.io/distroless/static:nonroot`** | Static-musl runtime, want CA certs + `/tmp` + a non-root user out of the box | No shell — cannot `exec` into the container for live debugging |
| **`gcr.io/distroless/static:debug-nonroot`** | Same as above, but with a busybox shell for ops/`kubectl exec` | Slightly larger; **acceptable** for staging or services that need on-call debug access |
| **`gcr.io/distroless/cc-debian12`** | Binary needs glibc (e.g. depends on `libsqlite3-sys`, OS-level dlopen) | Larger, but still locked-down; pair with `*-unknown-linux-gnu` build, not musl |
| **`gcr.io/distroless/cc-debian12:debug`** | glibc + shell for debug | |
| **`alpine:3.20`** | Need package manager at runtime (e.g. `apk add curl` for healthcheck), or org standardizes on Alpine | musl libc; slight allocator perf hit; full shell + apk |
| **`debian:bookworm-slim`** | Org standard, glibc binary + shell + apt at runtime | Larger; still maintained; well understood by ops teams |
| **Canonical chiselled Ubuntu (`ubuntu/chiselled`)** | Compliance with corporate Ubuntu LTS support | Smaller than `debian:slim`, supported by Canonical; choose chisels per dependency |
| **`cgr.dev/chainguard/static`** / **`cgr.dev/chainguard/glibc-dynamic`** | Want continuously-rebuilt-with-zero-CVE base; FedRAMP/SOC2 contexts | Pull rate limits; learn Wolfi |

#### Runtime stage examples

**Minimal production (static-musl + distroless):**

```dockerfile
FROM gcr.io/distroless/static:nonroot
COPY --from=builder /src/target/x86_64-unknown-linux-musl/dist/acme /usr/local/bin/acme
USER nonroot:nonroot
ENTRYPOINT ["/usr/local/bin/acme"]
```

**Debug-friendly (same binary, shell available):**

```dockerfile
FROM gcr.io/distroless/static:debug-nonroot
COPY --from=builder /src/target/x86_64-unknown-linux-musl/dist/acme /usr/local/bin/acme
USER nonroot:nonroot
ENTRYPOINT ["/usr/local/bin/acme"]
```

**glibc service with shell (when binary needs libc / dlopen):**

```dockerfile
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --system --uid 1000 acme
COPY --from=builder /src/target/x86_64-unknown-linux-gnu/dist/acme /usr/local/bin/acme
USER acme
ENTRYPOINT ["/usr/local/bin/acme"]
```

#### Image-pair pattern (recommended for services)

Ship **two tags** per release:

- `acme:v1.2.3` — minimal runtime (e.g. `distroless/static:nonroot`)
- `acme:v1.2.3-debug` — same binary, debug-friendly base (`:debug-nonroot` or `bookworm-slim`)

Ops teams pick `:debug` images for incident response; production deployments default to the minimal tag. This avoids forcing a single "right" base on every consumer.

#### What to keep constant across all bases

- run as **non-root**, never `USER root`
- `ENTRYPOINT` is the binary; `CMD` only for default args
- multi-arch: build at least `amd64` + `arm64` (ARM laptops, Graviton, RPi)
- sign with `cosign sign`; ship SBOM via `syft` or `cargo cyclonedx`
- pin base image by digest in production (`@sha256:...`) — not by mutable tag
- HEALTHCHECK can call `/livez` if the runtime supports it

What **not** to do:

- target a specific image-size number — "as small as the chosen base allows" is the right answer; size depends on what ops needs from the image
- bake debug tools into the production tag and call it good — split into a `:debug` tag instead

### Custom service release pipeline

Quickwit's `publish_release_packages.yml`:

- Trigger: tag push `v*`
- Matrix: `x86_64-apple-darwin`, `aarch64-apple-darwin`, `x86_64-unknown-linux-gnu`, `aarch64-unknown-linux-gnu`
- Build: composite actions `cargo-build-macos-binary` + `cross-build-binary` (Linux via `cross`)
- Publish: GitHub Releases + Docker images (separate `publish_docker_images.yml`)
- Sign: cosign for container images; SBOM via `syft` or `cargo cyclonedx`

Rules:

- never publish from a developer machine; releases originate from a tagged CI job
- pre-release artifacts go to a separate channel (e.g. `v0.x.y-rc.1`) — never overwrite stable
- Docker images get an SBOM and are signed with cosign
- containers run as non-root, no shell (distroless final stage), with `cargo-chef` for layer caching

## CI Pipeline

Mandatory stages, runnable as `cargo xtask ci` locally and in GitHub Actions / GitLab CI. **None of these carry `-- -D warnings` on the command line** — that policy is in `[workspace.lints.rust]` (see Lock 4). Plain commands keep dev and CI on the same gate:

```text
1. fmt           : cargo fmt --all -- --check
2. clippy        : cargo clippy --workspace --all-targets --all-features --locked
3. doc-check     : cargo doc --workspace --no-deps --document-private-items
4. test          : cargo nextest run --workspace --all-features --locked
5. doctest       : cargo test --doc --workspace --all-features --locked
6. snapshot      : cargo insta test --all-features --unreferenced reject --test-runner nextest --disable-nextest-doctest
                   (only if the project uses insta — ruff's exact CI line)
7. msrv          : cargo hack check --rust-version --workspace --ignore-private --locked
                   OR cargo msrv verify
8. supply-chain  : cargo deny check  +  cargo audit  +  cargo shear (or machete)  +  typos
9. build-release : cargo build --workspace --release
10. coverage     : cargo llvm-cov nextest --workspace --lcov --output-path lcov.info
                   (when SLA requires)
11. mutants      : cargo mutants --in-place --shard ${SHARD}/${TOTAL}
                   (gated on critical crates only)
```

Caching — keep CI fast:

- **`Swatinem/rust-cache@v2`** for `target/` and registry — verified universal at reth (every job)
- separate caches per job kind (test cache != release cache != docs cache)
- **`mozilla-actions/sccache-action`** + RUSTC_WRAPPER=sccache for very large workspaces (reth pattern)
- **`rui314/setup-mold`** linker on Linux for faster builds (reth uses it on every job)

Matrix:

- always test against the **MSRV** declared in `workspace.package.rust-version`
- additionally test against current stable
- nightly is informational only — never blocking unless the project explicitly tracks it (reth runs lint on nightly because nightly clippy catches more)

### CI workflow templates

Compose these reusable steps:

```yaml
# .github/workflows/ci.yml — abridged
jobs:
  fmt:
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with: { components: rustfmt }
      - run: cargo fmt --all -- --check

  clippy:
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with: { components: clippy }
      - uses: Swatinem/rust-cache@v2
      # No `-- -D warnings` here — policy lives in [workspace.lints.rust]
      - run: cargo clippy --workspace --all-targets --all-features --locked

  test:
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - uses: Swatinem/rust-cache@v2
      - uses: taiki-e/install-action@v2
        with: { tool: cargo-nextest }
      - run: cargo nextest run --workspace --all-features --locked
      - run: cargo test --doc --workspace --all-features --locked

  msrv:
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@master
        with: { toolchain: "1.96.0" }     # match workspace.package.rust-version
      - uses: taiki-e/install-action@v2
        with: { tool: cargo-hack }
      - run: cargo hack check --rust-version --workspace --ignore-private --locked

  deny:
    steps:
      - uses: actions/checkout@v4
      - uses: EmbarkStudios/cargo-deny-action@v2
        with:
          command: check advisories bans licenses sources

  shear:
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - uses: taiki-e/install-action@v2
        with: { tool: cargo-shear }
      - run: cargo shear

  typos:
    steps:
      - uses: actions/checkout@v4
      - uses: crate-ci/typos@master
```

## Git Conventions

- English for commit messages, PR titles/bodies, and any remote-visible Git metadata
- conventional commits (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`, `perf:`, `ci:`) — `release-plz` parses these for changelog and version bump
- one logical change per PR; rebase rather than merge for linear history
- PR description: what + why + a test plan with explicit checkboxes
- never mention AI assistants, agent names, or model identifiers in remote-visible content (per global rules in `~/.claude/CLAUDE.md`)

## Review Focus

When reviewing a PR, prioritize in this order:

1. **Hard locks** — does the change re-introduce `openssl`, drop `#![forbid(unsafe_code)]`, or relax workspace deny-warnings policy?
2. **Panic boundaries** — any new `unwrap`/`expect`/`panic!` outside `tests`/`xtask`/`build.rs`?
3. **Blocking work in async** — `std::fs`, `std::sync::Mutex` across `.await`, CPU-bound work without `spawn_blocking`?
4. **Resource lifetime** — pools closed on shutdown, tasks tracked via `TaskTracker`, files/handles released?
5. **Error translation** — domain errors map to safe HTTP/CLI output without leaking internals?
6. **Security-sensitive IO** — outbound HTTP, file paths, secret comparisons, auth boundaries?
7. **Dependency drift** — new deps explainable, license OK, no native-tls/openssl regression?
8. **Test coverage** — happy path + at least one failure path; integration test if a public surface changed?
9. **Observability** — new code path emits a span / metric / log at the right level?

This list is the same heuristic used by tokio, reth, and linkerd reviewers.
