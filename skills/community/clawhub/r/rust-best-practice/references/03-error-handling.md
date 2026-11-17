# Error Handling

## Table of contents
1. `Result` vs `Option` vs `panic!`
2. The `?` operator and error propagation
3. Designing custom error types
4. `thiserror` (libraries) vs `anyhow` (applications)
5. Panics: when they're correct
6. Error context and reporting
7. Anti-patterns checklist

---

## 1. `Result` vs `Option` vs `panic!`

- `Option<T>` — absence is a normal, expected outcome (e.g. `HashMap::get`, `Vec::first`). Not an error.
- `Result<T, E>` — an operation can fail in a way the caller should be able to handle or report. This is the default for anything doing I/O, parsing, network calls, or business-rule validation.
- `panic!`/`unwrap()`/`expect()` — reserved for **programmer errors** and states that indicate a bug or a genuinely unrecoverable condition (violated invariant, corrupted internal state), not for expected failure modes like "file not found" or "invalid user input".

The Rust API Guidelines and the official book agree: library code should almost never panic on bad *input*; it should return `Result`. Applications may choose to `.unwrap()`/`?`-propagate-to-`main` and let the process exit on error, which is a legitimate top-level strategy.

## 2. The `?` operator and error propagation

`?` unwraps `Ok`/`Some` or returns early with `Err`/`None`, converting the error type via `From` automatically:

```rust
fn read_port(path: &Path) -> Result<u16, ConfigError> {
    let text = fs::read_to_string(path)?;      // io::Error -> ConfigError via From
    let port: u16 = text.trim().parse()?;      // ParseIntError -> ConfigError via From
    Ok(port)
}
```

This only works if `ConfigError: From<io::Error>` and `From<ParseIntError>` exist — either hand-written or (far more commonly) derived with `thiserror`'s `#[from]` attribute (see §4).

`?` also works in `fn main() -> Result<(), E>` and in tests (`fn test() -> Result<(), E>`), which is the idiomatic way to avoid `.unwrap()` scattered through application entry points.

## 3. Designing custom error types

A well-designed library error type is a `enum` (one variant per distinct failure category), implements `std::error::Error`, `Debug`, and `Display`, and — per API Guidelines `C-GOOD-ERR` — is `Send + Sync + 'static` so callers can box it into `Box<dyn Error + Send + Sync>` or downcast it. Never use `()` or a bare `String` as an error type (`C-GOOD-ERR` explicitly calls this out — `()` doesn't implement `Error` and loses all diagnostic information).

```rust
#[derive(Debug, thiserror::Error)]
pub enum ConfigError {
    #[error("could not read config file: {0}")]
    Io(#[from] std::io::Error),

    #[error("invalid port number: {0}")]
    InvalidPort(#[from] std::num::ParseIntError),

    #[error("config validation failed: {reason}")]
    Validation { reason: String },
}
```

Keep error variants **specific enough to act on** (callers may `match` on them) but don't over-fragment into dozens of near-identical variants — group by what a caller would realistically branch on.

## 4. `thiserror` (libraries) vs `anyhow` (applications)

This is the ecosystem-standard split, popularized by David Tolnay (author of both crates) and reflected in virtually every modern Rust project:

- **`thiserror`**: use in **library/reusable crates**. Generates `std::error::Error` impls for your own enum via `#[derive(Error)]`, preserving a concrete, matchable type for callers.
- **`anyhow`**: use in **applications/binaries** (or internal, non-public-API application code) where you don't need callers to match on specific error variants — just propagate, add context, and report. `anyhow::Error` erases the concrete type but is cheap to use with `?` everywhere and supports `.context("...")` for adding human-readable breadcrumbs.

```rust
// application code (main.rs / internal binary logic)
use anyhow::{Context, Result};

fn run() -> Result<()> {
    let cfg = load_config("app.toml").context("failed to load app.toml")?;
    start_server(cfg).context("server failed to start")?;
    Ok(())
}
```

Do **not** expose `anyhow::Error` in a public library API — it forces every downstream consumer onto `anyhow` and prevents them from matching on specific failure modes. This is one of the most common review findings in published crates.

## 5. Panics: when they're correct

Legitimate uses of `panic!`/`unwrap()`/`expect()`:
- Violated internal invariants that indicate a bug, not bad input (e.g. an index computed by your own code that "should never" be out of bounds — but consider `debug_assert!` instead if the check has real runtime cost).
- Test code and examples (`.unwrap()` is standard and encouraged in `#[test]` functions for concise failure reporting).
- Quick prototypes / scripts where correctness of error paths hasn't been designed yet — but flag this as tech debt before shipping.
- `expect("message")` over bare `unwrap()` **always**, when a panic is intentional — the message becomes the panic output and should explain the invariant that was violated, e.g. `.expect("config was validated at startup, port must be Some")`.

Never panic in a `Drop` implementation (a panic during unwind-from-panic aborts the whole process) — `Drop::drop` should log/ignore errors, not propagate them.

## 6. Error context and reporting

- `anyhow::Context::context`/`.with_context(|| ...)` to attach human-readable breadcrumbs without losing the underlying error (use `.with_context` when the message requires formatting/allocation, to avoid paying that cost on the non-error path).
- For structured/library errors, preserve the source error via `#[source]` (thiserror) or a boxed `source()` so `std::error::Error::source()` chains work with tools like `anyhow`'s `{:#}` alternate `Display` (prints the full chain) or `eyre`.
- Log errors at the point they're handled/reported, not at every level they're propagated through — propagating with `?` and logging once at the top avoids duplicate log spam for the same failure.

## 7. Anti-patterns checklist

- [ ] `Result<T, String>` or `Result<T, ()>` in public APIs instead of a proper error enum
- [ ] `.unwrap()`/`.expect()` on fallible I/O, parsing, or user-input paths outside of tests/prototypes
- [ ] `anyhow::Error` (or `Box<dyn Error>`) exposed in a published library's public function signatures
- [ ] Catching/matching all errors just to immediately `.unwrap()` or discard them (`let _ = fallible_call();` hiding real failures)
- [ ] Panicking inside `Drop::drop`
- [ ] Manually writing `impl From<X> for MyError { ... }` boilerplate for every variant instead of `#[from]` via `thiserror`
- [ ] Overly granular error enums (one variant per call site) that no caller could realistically pattern-match on meaningfully

---

## Real references

- The Rust Programming Language, ch. 9 (Error Handling): https://doc.rust-lang.org/book/ch09-00-error-handling.html
- `std::error::Error` trait docs: https://doc.rust-lang.org/std/error/trait.Error.html
- `std::result::Result` docs, including `?` operator section: https://doc.rust-lang.org/std/result/index.html
- Rust API Guidelines — Interoperability (C-GOOD-ERR, error type requirements): https://rust-lang.github.io/api-guidelines/interoperability.html#error-types-are-meaningful-and-well-behaved-c-good-err
- `thiserror` crate docs: https://docs.rs/thiserror/latest/thiserror/
- `anyhow` crate docs: https://docs.rs/anyhow/latest/anyhow/
- RFC 243 — trait-based exception handling background / `?` operator (`try` trait) RFC 3058: https://rust-lang.github.io/rfcs/3058-try-trait-v2.html
- "Error Handling In Rust" — Andrew Gallant (BurntSushi), widely cited community reference: https://blog.burntsushi.net/rust-error-handling/
