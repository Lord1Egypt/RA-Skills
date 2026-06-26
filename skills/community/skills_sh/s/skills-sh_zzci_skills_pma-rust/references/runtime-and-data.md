# PMA-Rust Runtime And Data

This pack covers everything that runs at request time: errors, layered architecture, async DB access, configuration, the Axum 0.8 + tower stack, and graceful shutdown. Every code pattern below is verified against an axum example, a tokio doc, a linkerd2-proxy module, or a quickwit handler. See `references/evidence.md` for citations.

## Table of Contents

- [Error Handling](#error-handling)
- [Architecture Patterns](#architecture-patterns)
- [Database Strategy](#database-strategy)
- [Configuration](#configuration)
- [CLI Parsing (clap v4 derive)](#cli-parsing-clap-v4-derive)
- [Axum 0.8 Runtime](#axum-08-runtime)
- [Tokio Runtime](#tokio-runtime)
- [Graceful Shutdown](#graceful-shutdown)
- [Background Tasks](#background-tasks)
- [Health Endpoints](#health-endpoints)
- [Signal Handling Summary](#signal-handling-summary)

## Error Handling

### Per-crate `thiserror` 2.x (verified universal)

```rust
// crates/core/src/error.rs
#![forbid(unsafe_code)]

#[derive(Debug, thiserror::Error)]
pub enum DomainError {
    #[error("not found: {0}")]
    NotFound(String),

    #[error("invalid input: {0}")]
    Invalid(String),

    #[error(transparent)]
    Storage(#[from] crate::repo::StorageError),
}

pub type Result<T, E = DomainError> = std::result::Result<T, E>;
```

Verified at `quickwit-storage/src/error.rs:43-66`, `uv-settings/src/lib.rs:654-682`, `ruff/crates/*/src/error.rs`. All use `thiserror = "2.0"`.

Rules:

- one `Error` enum per crate or per bounded context — not one giant enum for the workspace
- `#[from]` only when conversion is unambiguous and lossless; otherwise convert manually with explicit context
- `anyhow::Error` (or `eyre::Report`) appears in `main.rs`, `xtask/`, and integration tests — nowhere else
- never panic for recoverable runtime errors; reserve `unwrap`/`expect` for invariants the type system cannot encode (and add an `// INVARIANT:` comment)
- `serde::{Serialize, Deserialize}` on error types when they cross process boundaries (quickwit's `StorageResolverError` derives both for cross-actor messaging)

### `IntoResponse` for Axum HTTP boundaries

Two valid patterns (pick one per project, do not mix). Both are official axum example code.

**Simple (`axum/examples/anyhow-error-response/src/main.rs:34-61`)** — wrap `anyhow::Error`, opaque public payload:

```rust
// crates/api/src/error.rs
use axum::{http::StatusCode, response::{IntoResponse, Response}};

pub struct AppError(anyhow::Error);

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        tracing::error!(error = ?self.0, "request failed");
        (
            StatusCode::INTERNAL_SERVER_ERROR,
            format!("Something went wrong: {}", self.0),
        ).into_response()
    }
}

impl<E> From<E> for AppError
where
    E: Into<anyhow::Error>,
{
    fn from(err: E) -> Self { Self(err.into()) }
}
```

**Advanced (`axum/examples/error-handling/src/main.rs:151-215`)** — typed errors, response-extension logging, custom JSON extractor for unified error format:

```rust
use std::sync::Arc;
use axum::{
    extract::{rejection::JsonRejection, FromRequest},
    http::StatusCode,
    response::{IntoResponse, Response},
};

#[derive(Debug, thiserror::Error)]
pub enum ApiError {
    #[error("invalid JSON: {0}")]
    JsonRejection(#[from] JsonRejection),
    #[error("not found: {0}")]
    NotFound(String),
    #[error("unauthorized")]
    Unauthorized,
    #[error("internal error")]
    Internal(#[source] anyhow::Error),
}

#[derive(serde::Serialize)]
struct ErrorBody { code: &'static str, message: String }

impl IntoResponse for ApiError {
    fn into_response(self) -> Response {
        let (status, code, message, attach_err) = match &self {
            Self::JsonRejection(r) => (r.status(), "invalid_json", r.body_text(), false),
            Self::NotFound(_)      => (StatusCode::NOT_FOUND, "not_found", self.to_string(), false),
            Self::Unauthorized     => (StatusCode::UNAUTHORIZED, "unauthorized", self.to_string(), false),
            Self::Internal(_)      => (StatusCode::INTERNAL_SERVER_ERROR, "internal", "internal error".into(), true),
        };
        let mut response = (status, AppJson(ErrorBody { code, message })).into_response();
        if attach_err {
            // Make the original error available to logging middleware
            response.extensions_mut().insert(Arc::new(self));
        }
        response
    }
}

// Custom Json extractor that funnels rejections through ApiError
#[derive(FromRequest)]
#[from_request(via(axum::Json), rejection(ApiError))]
pub struct AppJson<T>(pub T);

impl<T: serde::Serialize> IntoResponse for AppJson<T> {
    fn into_response(self) -> Response { axum::Json(self.0).into_response() }
}
```

Logging middleware then reads the extension (`error-handling/src/main.rs:208-215`):

```rust
async fn log_app_errors(req: Request, next: Next) -> Response {
    let response = next.run(req).await;
    if let Some(err) = response.extensions().get::<std::sync::Arc<ApiError>>() {
        tracing::error!(?err, "an unexpected error occurred inside a handler");
    }
    response
}
```

Use the **advanced pattern** for any service with public APIs. The simple pattern is acceptable for internal-only admin endpoints.

## Architecture Patterns

Hexagonal layout, unchanged from prior version (verified across reth, quickwit, vector):

```text
crates/core   <- pure domain types, traits, business logic. NO IO, NO HTTP, NO DB.
crates/db     <- implements core's storage traits via SQLx/SeaORM/Diesel.
crates/api    <- axum routers, handlers, request/response DTOs, IntoResponse.
crates/app    <- main(): wires figment + clap + telemetry + db + api, runs server.
```

Rules:

- `core` exposes traits (`UserRepository`, `Clock`, `IdGen`); `db` and tests provide implementations
- handlers are extract → call domain service → map to response. **No business rules in handlers.**
- shared state is `Arc<AppState>` where `AppState` is a cheap-clone struct of `Arc`s
- never hold a `std::sync::Mutex` or `parking_lot::Mutex` across `.await` — use `tokio::sync::Mutex` or restructure to message passing
- when `AppState` has multiple shared resources, derive `FromRef` and write per-resource `FromRequestParts` extractors

### `FromRef` substate pattern (axum's `sqlx-postgres` example, 75-91)

```rust
use axum::extract::{FromRef, FromRequestParts, State};
use axum::http::request::Parts;
use sqlx::PgPool;

#[derive(Clone)]
pub struct AppState {
    pub db:    PgPool,
    pub cfg:   Arc<Config>,
    pub clock: Arc<dyn Clock>,
}

impl FromRef<AppState> for PgPool {
    fn from_ref(s: &AppState) -> Self { s.db.clone() }
}

pub struct DatabaseConnection(pub sqlx::pool::PoolConnection<sqlx::Postgres>);

impl<S> FromRequestParts<S> for DatabaseConnection
where
    PgPool: FromRef<S>,
    S: Send + Sync,
{
    type Rejection = ApiError;
    async fn from_request_parts(_p: &mut Parts, state: &S) -> Result<Self, Self::Rejection> {
        let pool = PgPool::from_ref(state);
        Ok(Self(pool.acquire().await.map_err(|e| ApiError::Internal(e.into()))?))
    }
}
```

Now handlers can write `async fn h(DatabaseConnection(mut conn): DatabaseConnection)` without unpacking `AppState` themselves.

## Database Strategy

Three supported paths. Pick once per project, document in the README, do not mix in the same crate.

### SQLx (default)

```toml
sqlx = { workspace = true, default-features = false, features = [
    "runtime-tokio",
    "tls-rustls-aws-lc-rs", # rustls + aws-lc-rs — never tls-native-tls
    "postgres",
    "macros",
    "migrate",
] }
```

```rust
let pool = sqlx::postgres::PgPoolOptions::new()
    .max_connections(cfg.db.max_conns)
    .acquire_timeout(Duration::from_secs(3))
    .connect_lazy_with(cfg.db.connect_options());

sqlx::migrate!("./migrations").run(&pool).await?;

let row = sqlx::query_as!(User, "SELECT id, email FROM users WHERE id = $1", id)
    .fetch_optional(&pool).await?;
```

Rules:

- `query!`/`query_as!` macros over runtime `query` (compile-time SQL check)
- run `cargo sqlx prepare` and commit `.sqlx/` cache so CI does not need a live database
- pool creation is centralized in `crates/db`; the rest of the codebase receives `Arc<DbPool>` via `AppState`

### SeaORM (alt)

When ActiveRecord-style entities + relations dominate the design. Migrations live in a `migration/` crate generated by `sea-orm-cli`. Pair with rustls feature flags; reject `native-tls`.

### Diesel + diesel-async (alt)

When compile-time schema typing is paramount and the team is already on Diesel. Generate `schema.rs` via `diesel print-schema`, commit it, run `diesel migration` in CI. `diesel-async` is the async path.

### Common rules

- pool creation lives in `crates/db`; the rest of the code receives a cheap-clone handle
- migrations are committed; CI runs them against an ephemeral DB before integration tests
- read replicas / sharding decisions are explicit in code paths — never silently routed by query

## Configuration

Layered with `figment` (or roll your own per-project, like quickwit's `VersionedNodeConfig`):

```text
defaults (in code)  →  config file (TOML/YAML)  →  environment variables  →  CLI flags
```

```rust
use clap::Parser;
use figment::{Figment, providers::{Format, Toml, Env, Serialized}};
use serde::Deserialize;

#[derive(Parser)]
#[command(version, about)]
struct Cli {
    #[arg(long, env = "ACME_CONFIG", default_value = "config.toml")]
    config: PathBuf,
    #[arg(long, env = "ACME_LOG")]
    log: Option<String>,
}

#[derive(Debug, Deserialize, validator::Validate)]
struct Config {
    http:      HttpConfig,
    db:        DbConfig,
    telemetry: TelemetryConfig,
}

let cli = Cli::parse();
let cfg: Config = Figment::new()
    .merge(Serialized::defaults(Config::default()))
    .merge(Toml::file(&cli.config))
    .merge(Env::prefixed("ACME_").split("__"))   // ACME_DB__URL → cfg.db.url
    .merge(Serialized::defaults(&cli))
    .extract()?;

cfg.validate()?;     // post-merge validation at the boundary
```

Rules:

- secrets wrap in `secrecy::Secret<T>` so they never leak into `Debug`/logs
- run validation **after merge** with `validator` or `garde`
- document every env var (e.g. `ACME_DB__URL`) and CLI flag in the README
- never read environment variables ad-hoc inside library code; load once at startup, pass `Arc<Config>` down

For services with very large config surfaces (>100 fields), look at quickwit's versioned-config pattern (`quickwit-config/src/node_config/serialize.rs:138-149`): a `VersionedNodeConfig` enum with `#[serde(tag = "version")]` letting old configs keep loading after schema changes.

## CLI Parsing (clap v4 derive)

Standard pattern, verified at `uv/crates/uv-cli/src/lib.rs:99-219` and `ruff/crates/ruff/src/args.rs:113-127`:

```rust
use clap::Parser;

#[derive(Debug, Parser)]
#[command(
    name        = "acme",
    author,
    version,
    about       = "Acme service",
    after_help  = "For help with a specific command, see: `acme help <command>`."
)]
pub struct Cli {
    #[command(subcommand)]
    pub command: Command,

    #[command(flatten)]
    pub global: GlobalArgs,
}

#[derive(Debug, clap::Args)]
pub struct GlobalArgs {
    /// Decrease verbosity
    #[arg(global = true, short, long, action = clap::ArgAction::Count, conflicts_with = "verbose")]
    pub quiet: u8,

    /// Increase verbosity
    #[arg(global = true, short, long, action = clap::ArgAction::Count, conflicts_with = "quiet")]
    pub verbose: u8,

    #[arg(global = true, long, hide = true, conflicts_with = "color")]
    pub no_color: bool,

    #[arg(global = true, long, env = "ACME_LOG")]
    pub log: Option<String>,
}

#[derive(Debug, clap::Subcommand)]
pub enum Command {
    Run(RunArgs),
    GenerateShellCompletion(GenerateShellCompletionArgs),
}

#[derive(Debug, clap::Args)]
pub struct GenerateShellCompletionArgs {
    pub shell: clap_complete_command::Shell,
}
```

Dispatch:

```rust
use clap::CommandFactory;

match cli.command {
    Command::GenerateShellCompletion(args) => {
        args.shell.generate(&mut Cli::command(), &mut std::io::stdout());
    }
    Command::Run(args) => run(args).await?,
}
```

For very large CLIs (>200 subcommands), the **builder API** is acceptable (quickwit pattern, `quickwit-cli/src/cli.rs:26-87`): more verbose but lets you generate subcommand trees programmatically.

For binary entry points, install a custom panic hook that prints a GitHub issue template (ruff's pattern, `crates/ruff/src/lib.rs:143-161`).

## Axum 0.8 Runtime

### Path syntax

Axum 0.8 uses `{name}`, **not** `:name`. Verified at `axum/examples/key-value-store/src/main.rs:46` and `axum/examples/todos/src/main.rs:51`:

```rust
.route("/{key}", get(kv_get))
.route("/todos/{id}", get(get_todo).delete(delete_todo))
```

### Router composition

```rust
use std::time::Duration;
use axum::{Router, routing::get};
use tower::ServiceBuilder;
use tower_http::{
    compression::CompressionLayer,
    cors::CorsLayer,
    sensitive_headers::SetSensitiveRequestHeadersLayer,
    timeout::TimeoutLayer,
    trace::TraceLayer,
};

pub fn router(state: AppState) -> Router {
    Router::new()
        .route("/healthz", get(health::live))
        .route("/readyz",  get(health::ready))
        .nest("/api/v1", api_v1::router())
        .with_state(state)
        .layer(
            ServiceBuilder::new()
                // Outermost wraps innermost — TraceLayer first so it captures everything.
                .layer(TraceLayer::new_for_http())
                .layer(SetSensitiveRequestHeadersLayer::new([
                    http::header::AUTHORIZATION,
                    http::header::COOKIE,
                ]))
                .layer(TimeoutLayer::new(Duration::from_secs(30)))
                .layer(CompressionLayer::new())
                .layer(CorsLayer::permissive())   // tighten in prod
                // Load-shedding MUST sit OUTSIDE the concurrency limit so the request fails
                // fast when the limit is reached, instead of queuing.
                // (linkerd2-proxy/inbound/src/http/server.rs:65-68 documents this order.)
                .load_shed()
                .concurrency_limit(1024),
        )
}

// Functions returning routers DO NOT call `with_state` themselves —
// see axum/src/docs/routing/with_state.md.
fn api_v1::router() -> Router<AppState> {
    Router::new()
        .route("/users",      get(users::list).post(users::create))
        .route("/users/{id}", get(users::get).delete(users::delete))
}
```

`Router<S>` semantics (`axum/src/docs/routing/with_state.md:106-127`): `S` is the **missing** state type, not the injected one. After `with_state(state)`, the router becomes `Router<()>`, and only `Router<()>` exposes `into_make_service`.

### Tower middleware to reach for

| Need | Crate / Layer |
|---|---|
| Request/response tracing | `tower_http::trace::TraceLayer` |
| Timeouts | `tower_http::timeout::TimeoutLayer` |
| Compression | `tower_http::compression::CompressionLayer` |
| CORS | `tower_http::cors::CorsLayer` |
| Body limits | `tower_http::limit::RequestBodyLimitLayer` |
| Sensitive headers (redact in logs) | `tower_http::sensitive_headers::SetSensitiveRequestHeadersLayer` |
| Retry (idempotent calls only) | `tower::retry::RetryLayer` (and `linkerd_retry` for budget-based retries) |
| Concurrency / load shedding | `.load_shed().concurrency_limit(N)` — load-shed **outside** concurrency-limit |
| Auth | custom layer that inserts a `CurrentUser` into request extensions |
| Metrics | `axum-prometheus` or a custom layer over `metrics::histogram!` |

The linkerd inbound stack (production reference, `linkerd2-proxy/linkerd/app/inbound/src/http/server.rs:58-89`) confirms: normalize → identity → concurrency-limit → **load-shed** → map-err → metrics → rescue → tracing → access-log.

### Testing axum routers (no HTTP server)

Verified at `axum/examples/testing/src/main.rs:65-82`:

```rust
use http_body_util::BodyExt;
use tower::ServiceExt;     // for `oneshot`

#[tokio::test]
async fn hello_world() {
    let app = router(AppState::test());

    let response = app
        .oneshot(
            axum::http::Request::get("/")
                .body(axum::body::Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), axum::http::StatusCode::OK);
    let body = response.into_body().collect().await.unwrap().to_bytes();
    assert_eq!(&body[..], b"Hello, World!");
}
```

Use this pattern for nearly every handler test. Spin up a real `axum::serve` only when testing graceful-shutdown or middleware that depends on actual TCP behavior.

## Tokio Runtime

### Default — `#[tokio::main(flavor = "multi_thread")]`

```rust
#![forbid(unsafe_code)]

#[tokio::main(flavor = "multi_thread")]
async fn main() -> anyhow::Result<()> {
    // === 1. Suppress core dumps BEFORE anything else can crash ===
    // Cores leak secrets (the entire process heap, including secrecy::Secret values) and
    // can fill volume mounts. We disable them in-process so the policy holds even if the
    // outer ulimit/systemd config drifts. See references/delivery.md "Disable Core Dumps".
    #[cfg(unix)]
    {
        use rlimit::{setrlimit, Resource};
        setrlimit(Resource::CORE, 0, 0).ok();   // best-effort; do not fail startup on this
    }

    // === 2. Install a panic hook that produces a structured log record then aborts ===
    // Without this, panic output goes to stderr unstructured and the panic location is lost
    // in JSON-only log pipelines. With panic = "abort" + this hook + core dumps disabled,
    // the process dies fast, panic info reaches the log collector, and no on-disk artifact
    // is created.
    install_panic_hook();

    // === 3. rustls crypto provider before any TLS use ===
    rustls::crypto::aws_lc_rs::default_provider()
        .install_default()
        .map_err(|e| anyhow::anyhow!("install rustls provider: {e:?}"))?;

    let cfg     = config::load()?;
    let _guards = telemetry::init(&cfg.telemetry)?;
    let state   = AppState::new(&cfg).await?;
    serve(state, cfg.http).await
}

fn install_panic_hook() {
    let default_hook = std::panic::take_hook();
    std::panic::set_hook(Box::new(move |info| {
        let payload = info.payload();
        let message = payload
            .downcast_ref::<&str>().copied()
            .or_else(|| payload.downcast_ref::<String>().map(String::as_str))
            .unwrap_or("<non-string panic>");
        let location = info.location().map(|l| format!("{}:{}:{}", l.file(), l.line(), l.column()));

        // Structured tracing record so JSON log pipelines pick it up.
        tracing::error!(
            target  = "panic",
            message = %message,
            location = location.as_deref().unwrap_or("<unknown>"),
            backtrace = %std::backtrace::Backtrace::force_capture(),
            "process panicked",
        );

        // Also call the default hook so the message hits stderr in case logging is broken.
        default_hook(info);

        // With panic = "abort" in [profile.dist], the runtime aborts after the hook returns.
        // With panic = "unwind" (default), `catch_unwind`-aware code can still recover.
    }));
}
```

`rlimit` is a pure-Rust crate (no C bindings), satisfying Hard Lock 1. Add to `Cargo.toml`:

```toml
[target.'cfg(unix)'.dependencies]
rlimit = "0.10"
```

For containers and systemd, see `references/delivery.md` "Disable Core Dumps" for the matching outer-layer config — this in-process call is the inner belt of a belt-and-suspenders defense.

### Hand-built runtime — when tuning matters

For services that need to control thread count, park hooks, or runtime metrics, follow quickwit's pattern (`quickwit-cli/src/main.rs:42-63`):

```rust
let main_runtime_num_threads: usize =
    std::env::var("ACME_TOKIO_RUNTIME_NUM_THREADS")
        .ok()
        .and_then(|s| s.parse().ok())
        .unwrap_or_else(|| (num_cpus::get() / 2).max(2));

let rt = tokio::runtime::Builder::new_multi_thread()
    .enable_all()
    .thread_name("acme-main-rt")
    .worker_threads(main_runtime_num_threads)
    .build()?;

rt.block_on(async_main())
```

Pair with `tokio-metrics::RuntimeMonitor` and expose runtime metrics via Prometheus (quickwit's `scrape_tokio_runtime_metrics(rt.handle(), "main")`).

## Graceful Shutdown

Canonical pattern (`axum/examples/graceful-shutdown/src/main.rs:35-76`, plus official Tokio guidance from `tokio.rs/tokio/topics/shutdown`):

```rust
use std::time::Duration;
use axum::http::StatusCode;
use tokio::signal;
use tokio_util::{sync::CancellationToken, task::TaskTracker};
use tower_http::timeout::TimeoutLayer;

pub async fn serve(state: AppState, http: HttpConfig) -> anyhow::Result<()> {
    let cancel  = CancellationToken::new();
    let tracker = TaskTracker::new();

    // Spawn background tasks via the tracker so we can `wait()` them on shutdown.
    tracker.spawn(metrics_pusher(state.clone(), cancel.clone()));
    tracker.spawn(cron_runner(state.clone(),    cancel.clone()));

    let app = router(state).layer(
        // Pair TimeoutLayer with graceful_shutdown so requests don't hang forever.
        TimeoutLayer::with_status_code(StatusCode::REQUEST_TIMEOUT, Duration::from_secs(10)),
    );

    let listener = tokio::net::TcpListener::bind(http.addr).await?;
    tracing::info!(%http.addr, "serving");
    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal(cancel.clone()))
        .await?;

    // Stop accepting new background work.
    cancel.cancel();
    tracker.close();

    // Wait for tasks (with a deadline so a stuck task can't block forever).
    let drain = tokio::time::timeout(Duration::from_secs(30), tracker.wait()).await;
    if drain.is_err() {
        tracing::error!("background task drain timed out — forcing exit");
    }

    // Flush telemetry before main returns.
    opentelemetry::global::shutdown_tracer_provider();
    Ok(())
}

async fn shutdown_signal(cancel: CancellationToken) {
    let ctrl_c = async {
        signal::ctrl_c().await.expect("install ctrl_c handler");
    };
    #[cfg(unix)]
    let terminate = async {
        signal::unix::signal(signal::unix::SignalKind::terminate())
            .expect("install SIGTERM handler")
            .recv().await;
    };
    #[cfg(not(unix))]
    let terminate = std::future::pending::<()>();

    tokio::select! {
        _ = ctrl_c    => tracing::info!("received SIGINT"),
        _ = terminate => tracing::info!("received SIGTERM"),
    }
    cancel.cancel();
}
```

Key points:

- `TimeoutLayer` paired with `with_graceful_shutdown` (verified `axum/examples/graceful-shutdown/src/main.rs:42-44`)
- `tokio::select!` over `ctrl_c` and SIGTERM (Unix only; non-Unix uses `std::future::pending`)
- `tokio_util::task::TaskTracker` is the official Tokio recommendation (per `tokio.rs/tokio/topics/shutdown`) for waiting on background tasks
- `CancellationToken` fans cancellation into pools, consumers, cron tasks
- target a fixed shutdown deadline (e.g. 30s) — past that, log abandoned tasks and exit

## Background Tasks

```rust
let tracker = TaskTracker::new();
tracker.spawn(metrics_pusher(state.clone(), cancel.clone()));
tracker.spawn(cron_runner(state.clone(),    cancel.clone()));
tracker.close();   // mark "no more spawns" once startup is done
```

- spawn once at startup, owned by the `TaskTracker`
- every task takes a `CancellationToken` and respects it via `tokio::select! { _ = token.cancelled() => break, _ = work() => {} }`
- failures log and surface; never silently restart unless the design calls for it

## Health Endpoints

Quickwit's pattern (`quickwit-serve/src/health_check_api/handler.rs:62-116`) — every service exposes both:

```rust
// /livez — process is alive (no dependencies queried)
async fn live() -> StatusCode { StatusCode::OK }

// /readyz — ready to serve traffic (queries DB pool, cluster membership, etc.)
async fn ready(State(s): State<AppState>) -> Result<StatusCode, ApiError> {
    s.db.acquire().await.map_err(|e| ApiError::Internal(e.into()))?;
    Ok(StatusCode::OK)
}
```

Both are unauthenticated, both return 200/503. Document them in OpenAPI via `utoipa` annotations when applicable.

## Signal Handling Summary

- handle `SIGINT` and `SIGTERM` (Unix), `Ctrl-C` (cross-platform)
- stop accepting new work first
- drain in-flight requests via Axum graceful shutdown + `TimeoutLayer`
- cancel background tasks via `CancellationToken`; wait via `TaskTracker`
- flush telemetry (`opentelemetry::global::shutdown_tracer_provider()`) and close DB pools (`pool.close().await`)
- exit with a non-zero code only on actual failure
