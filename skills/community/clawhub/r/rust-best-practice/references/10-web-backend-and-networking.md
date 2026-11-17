# Web Backend and Networking

## Table of contents
1. Choosing a framework: Axum vs. Actix-web vs. others
2. Request handlers and extractors
3. Middleware and layers
4. Serialization with `serde`
5. Database access
6. Error handling in HTTP handlers
7. API design (REST/gRPC)
8. Anti-patterns checklist

---

## 1. Choosing a framework: Axum vs. Actix-web vs. others

| Framework | Built on | Style | Notes |
|---|---|---|---|
| **Axum** | Tokio + `hyper` + `tower` | Extractor-based, composable via `tower::Layer`/`Service` | Maintained by the Tokio team; strong ecosystem integration with `tower` middleware (retries, timeouts, load-shedding); generally the current default recommendation for new Tokio-based services. |
| **Actix-web** | its own actor-derived runtime, now largely Tokio-compatible | Extractor-based, mature, historically very fast in benchmarks | Long track record, large middleware ecosystem; slightly more idiosyncratic actor-flavored history in older versions. |
| **Rocket** | Tokio (since v0.5) | Macro-heavy, ergonomics-first | Nice DX, smaller ecosystem than Axum/Actix. |
| **`hyper`** (low-level) | — | Raw HTTP implementation | Use directly only when building a framework or need very fine control; most applications should use Axum/Actix on top of it. |

Default recommendation for new projects without a strong existing constraint: **Axum**, due to its `tower` ecosystem integration (reusable middleware for tracing, timeouts, rate limiting, compression) and current Tokio-team maintenance.

## 2. Request handlers and extractors

Axum handlers are async functions whose parameters are **extractors** — types implementing `FromRequest`/`FromRequestParts` that pull data out of the incoming request:

```rust
use axum::{extract::{Path, State, Json}, routing::get, Router};

async fn get_user(
    Path(user_id): Path<u64>,
    State(pool): State<PgPool>,
) -> Result<Json<User>, AppError> {
    let user = sqlx::query_as!(User, "SELECT * FROM users WHERE id = $1", user_id as i64)
        .fetch_one(&pool)
        .await?;
    Ok(Json(user))
}

let app = Router::new()
    .route("/users/:id", get(get_user))
    .with_state(pool);
```

Order matters for some extractors (e.g. `Json`/body-consuming extractors must be last, since the body can only be consumed once) — the compiler will generally catch this via trait bound errors on `FromRequest`.

## 3. Middleware and layers

Cross-cutting concerns (logging, tracing, auth, compression, timeouts, rate limiting) belong in `tower::Layer`s wrapping the router, not duplicated inside every handler:

```rust
use tower_http::{trace::TraceLayer, timeout::TimeoutLayer};
use std::time::Duration;

let app = Router::new()
    .route("/users/:id", get(get_user))
    .layer(TraceLayer::new_for_http())
    .layer(TimeoutLayer::new(Duration::from_secs(10)));
```

`tower-http` provides a large library of ready-made layers (CORS, compression, request-id, sensitive-header redaction) — check there before writing custom middleware.

## 4. Serialization with `serde`

`#[derive(Serialize, Deserialize)]` is the near-universal standard. Best practices:
- Use `#[serde(deny_unknown_fields)]` on request DTOs where silently accepting typos/unexpected fields would hide client bugs — but not on types deserializing data you don't fully control (breaks forward compatibility).
- Separate your **wire types** (DTOs for request/response bodies) from your **domain types** (internal business logic) when they diverge — don't derive `Serialize` directly on internal domain structs just for convenience if it couples your public API accidentally to internal representation.
- Use `#[serde(rename_all = "camelCase")]` when the Rust `snake_case` convention needs to map to a JSON API's `camelCase` convention, rather than renaming Rust fields away from idiomatic style.
- Prefer `#[serde(default)]`/`Option<T>` for genuinely optional fields, and validate required invariants (non-empty strings, ranges) via a `TryFrom`/validation step after deserialization (see `references/04` newtype pattern) rather than trusting deserialized data blindly.

## 5. Database access

- **`sqlx`** — async, compile-time-checked queries (via `query!`/`query_as!` macros connecting to a real database at compile time or an offline query cache), no ORM abstraction layer; popular for teams comfortable writing SQL directly.
- **`diesel`** — compile-time-checked query builder / ORM-like abstraction, historically sync (async support via `diesel-async`); strong compile-time guarantees about schema correctness.
- **`sea-orm`** — full async ORM built on `sqlx`, more ActiveRecord-like ergonomics.

Whichever you choose: always use connection pooling (`sqlx::PgPool`, `deadpool`, or the ORM's built-in pool) rather than opening a new connection per request; never build SQL via string concatenation (use parameterized queries — all three options above do this by default, closing off SQL injection).

## 6. Error handling in HTTP handlers

Implement `IntoResponse` (Axum) for your application error type so handlers can return `Result<T, AppError>` directly and get proper HTTP status codes, rather than manually constructing a `Response` in every handler:

```rust
#[derive(Debug, thiserror::Error)]
enum AppError {
    #[error("not found")]
    NotFound,
    #[error(transparent)]
    Sqlx(#[from] sqlx::Error),
}

impl axum::response::IntoResponse for AppError {
    fn into_response(self) -> axum::response::Response {
        let status = match &self {
            AppError::NotFound => StatusCode::NOT_FOUND,
            AppError::Sqlx(_) => StatusCode::INTERNAL_SERVER_ERROR,
        };
        (status, self.to_string()).into_response()
    }
}
```

Never leak internal error details (SQL error text, file paths, stack traces) to API clients in production responses — log the detailed error server-side (via `tracing`) and return a generic message plus a correlation/request ID the client can report back.

## 7. API design (REST/gRPC)

- Use HTTP status codes correctly (`201 Created` for successful POST creating a resource, `204 No Content` for successful DELETE, `422`/`400` for validation errors vs. `500` for genuine server faults) — this is standard REST practice, not Rust-specific, but worth enforcing in review.
- Version your API from day one (`/v1/...` prefix or a header-based scheme) — breaking changes are inevitable, and retrofitting versioning later is painful.
- For gRPC services, `tonic` (built on `hyper`+`tower`, from the same ecosystem as Axum) is the standard choice; `.proto` files remain the source of truth for the wire contract, generated Rust types via `prost`.
- Use `tracing` (not `println!`/`log` alone) for structured, request-scoped logging in async services — spans naturally follow request lifecycles across `.await` points in a way flat log lines can't.

## 8. Anti-patterns checklist

- [ ] SQL built via string formatting/concatenation instead of parameterized queries
- [ ] Opening a new DB connection per request instead of using a pool
- [ ] Internal error details (stack traces, SQL errors, file paths) leaked directly into HTTP responses
- [ ] Domain types serialized directly as wire DTOs, coupling internal structure to the public API
- [ ] Cross-cutting concerns (auth, logging, timeouts) duplicated inside every handler instead of factored into `tower` layers/middleware
- [ ] No request timeouts configured, allowing slow clients/backends to exhaust server resources
- [ ] `println!` used for logging in a service instead of `tracing`/`log`

---

## Real references

- Axum official docs and examples: https://docs.rs/axum/latest/axum/ , https://github.com/tokio-rs/axum/tree/main/examples
- Actix-web official docs: https://actix.rs/docs/
- `tower` crate docs (Service/Layer abstractions): https://docs.rs/tower/latest/tower/
- `tower-http` middleware library: https://docs.rs/tower-http/latest/tower_http/
- `serde` official book: https://serde.rs/
- `sqlx` crate docs: https://docs.rs/sqlx/latest/sqlx/
- `diesel` official guides: https://diesel.rs/guides/
- `sea-orm` docs: https://www.sea-ql.org/SeaORM/docs/index/
- `tonic` (gRPC) docs: https://docs.rs/tonic/latest/tonic/
- `tracing` crate docs: https://docs.rs/tracing/latest/tracing/
