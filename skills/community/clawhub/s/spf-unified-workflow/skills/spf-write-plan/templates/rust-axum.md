# Rust Axum Web Template

When planning a Rust web service with Axum, ensure the following standards are met:

## Project Structure
- `Cargo.toml` with `axum`, `tokio` (full), `serde` (derive).
- `src/main.rs`: Setup the Router and Task spawning.
- `src/routes/`: Modularize route handlers.
- `src/models/`: Shared data structures.

## Patterns
- **State Management**: Use `axum::extract::State` for shared resources (DB pools, config).
- **Error Handling**: Implement `IntoResponse` for a custom `AppError` enum.
- **Middleware**: Use `tower-http` for logging (TraceLayer), CORS, and compression.
- **Graceful Shutdown**: Implement tokio signal handling for SIGINT/SIGTERM.

## Code Preview
```rust
use axum::{routing::get, Router};

#[tokio::main]
async fn main() {
    let app = Router::new().route("/", get(|| async { "Hello, Axum!" }));
    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

---
*Last Updated: 2026-03-06 06:36 UTC*
