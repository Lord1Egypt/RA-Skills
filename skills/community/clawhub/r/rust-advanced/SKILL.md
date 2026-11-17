---
name: rust-advanced
description: "Advanced Rust on Windows, macOS, and Linux: ownership and lifetimes, Result/error design, async Tokio, concurrency, serde/clap/tracing, Cargo features and profiles, testing, profiling, cross-compilation, Windows FFI, and PyO3/maturin. Use when the borrow checker, an async Send error, a linker error, a version conflict, or a production binary needs a real diagnosis."
category: software-development
---

# Rust Advanced

Audited toolchain: **rustc 1.93.1**, **cargo 1.93.1**, rustup installed. A `cargo new` + `cargo run` smoke test returned `Hello, world!` (exit 0).

## 1. Mental model

Rust's compiler is a design partner, not an obstacle. Most fights come from one of these:

- **Ownership**: one owner; moving invalidates the old binding.
- **Borrowing**: many immutable borrows OR one mutable borrow, not both.
- **Lifetimes**: a reference cannot outlive its data.
- **Send/Sync**: a value crossing threads/await points must be safe to move/share.
- **Errors are values**: `Result<T, E>` is normal control flow.

When stuck, ask:

1. Who owns this value?
2. How long must it live?
3. Does it cross a thread or an await point?
4. Can I return an owned value instead of a reference?
5. Can I narrow the borrow scope?

## 2. Toolchain and project

```powershell
rustup show
rustup update stable
rustup component add rustfmt clippy rust-src
rustup target list --installed
cargo --version
```

New project:

```powershell
cargo new app --bin
cargo new libname --lib
cargo add serde --features derive
cargo add tokio --features full
cargo add anyhow thiserror
```

Workspace:

```toml
[workspace]
members = ["app", "core", "cli"]
resolver = "2"
```

`Cargo.toml` baseline:

```toml
[package]
name = "app"
version = "0.1.0"
edition = "2024"
rust-version = "1.85"

[dependencies]
anyhow = "1"
thiserror = "2"
serde = { version = "1", features = ["derive"] }
serde_json = "1"
clap = { version = "4", features = ["derive"] }
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }

[profile.release]
opt-level = 3
lto = "thin"
codegen-units = 1
strip = "symbols"
panic = "abort"
```

Use `edition = "2024"` only if the toolchain supports it; otherwise pin 2021.

## 3. Ownership, borrowing, lifetimes

```rust
fn takes_owned(s: String) { println!("{s}"); }

fn borrows(s: &str) -> usize { s.len() }

fn main() {
    let s = String::from("hello");
    let n = borrows(&s);       // borrow ends here
    takes_owned(s);            // move is now allowed
    println!("{n}");
}
```

Rules that fix most errors:

- Return `String`/`Vec<T>` when the caller must own the data.
- Accept `&str`/`&[T]` when you only read.
- Keep mutable borrows short; do not hold one across a call that also borrows.
- Use `clone()` deliberately at boundaries, not to silence every error.
- `Cow<'a, str>` for optionally borrowed strings.
- `Arc<T>` for shared ownership across threads; `Rc<T>` is single-thread only.
- `RefCell<T>` for interior mutability in single-thread code; `Mutex`/`RwLock` across threads.

Lifetime template:

```rust
struct Parser<'a> {
    input: &'a str,
}

impl<'a> Parser<'a> {
    fn new(input: &'a str) -> Self { Self { input } }
    fn rest(&self) -> &'a str { self.input }
}
```

If a lifetime is hard, first try owning the data; optimize to borrow later.

## 4. Errors

Use `Result` for recoverable errors; `panic!` only for bugs/invariants.

```rust
use thiserror::Error;

#[derive(Debug, Error)]
pub enum AppError {
    #[error("io: {0}")]
    Io(#[from] std::io::Error),
    #[error("bad config: {0}")]
    Config(String),
}

pub fn load(path: &str) -> Result<String, AppError> {
    let s = std::fs::read_to_string(path)?;
    if s.is_empty() { return Err(AppError::Config("empty".into())); }
    Ok(s)
}
```

- Libraries: custom `thiserror` enum, no `anyhow` in public API.
- Applications: `anyhow::Result<T>` at the top; add context with `.context("...")?`.
- Never `.unwrap()` on user input, files, network, or env vars.
- `?` converts via `From`; implement `From` or use `#[from]`.
- Preserve the source chain; do not stringify and discard it.

## 5. Async and concurrency

```rust
#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let a = tokio::spawn(async { 1 + 1 });
    let b = tokio::spawn(async { 2 + 2 });
    println!("{} {}", a.await?, b.await?);
    Ok(())
}
```

Rules:

- Use Tokio for I/O concurrency; do not use it for CPU-bound work without `spawn_blocking`.
- Never block the async executor with `std::thread::sleep`, synchronous file I/O, or a long CPU loop.
- `tokio::time::timeout` around network calls.
- `tokio::select!` for cancellation/racing.
- `Arc<Mutex<T>>` or channels for shared state; prefer message passing.
- `Mutex` guard cannot be held across `.await` unless using `tokio::sync::Mutex`.
- `Send` errors usually mean an `Rc`, `RefCell`, or non-Send guard is held across await.

Threads:

```rust
use std::sync::{Arc, Mutex};
let state = Arc::new(Mutex::new(0));
let s2 = Arc::clone(&state);
std::thread::spawn(move || *s2.lock().unwrap() += 1);
```

Use `crossbeam-channel` or `std::sync::mpsc`; for async use `tokio::sync::mpsc`.

## 6. Serde, clap, tracing

```rust
use clap::Parser;
use serde::{Deserialize, Serialize};

#[derive(Debug, Parser)]
struct Cli {
    #[arg(long)]
    input: String,
    #[arg(long, default_value = "out.json")]
    out: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct Record { id: u64, name: String }
```

- `#[serde(rename_all = "camelCase")]` for API boundaries.
- `#[serde(default)]` for optional fields.
- `serde_json::from_str` / `to_string_pretty`.
- `tracing_subscriber::fmt().with_env_filter(...).init()`.
- Do not log secrets; redact tokens.

## 7. Tests and quality

```powershell
cargo fmt --check
cargo clippy --all-targets --all-features -- -D warnings
cargo test
cargo test -- --nocapture
cargo doc --no-deps --open
```

Unit test:

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn adds() { assert_eq!(2 + 2, 4); }
}
```

Integration test in `tests/`:

```rust
#[test]
fn cli_runs() {
    let out = std::process::Command::new(env!("CARGO_BIN_EXE_app"))
        .arg("--help").output().unwrap();
    assert!(out.status.success());
}
```

Add `cargo-audit` / `cargo-deny` for dependency security; `cargo nextest` for faster test runs if installed.

## 8. Performance and binaries

- Profile before optimizing: `cargo flamegraph`, `perf`, or `samply`.
- Release profile: LTO, `codegen-units=1`, `strip`, `panic=abort` where acceptable.
- `cargo build --release`; use `--target` for cross builds.
- `cargo bloat` to find binary weight.
- Avoid unnecessary `clone`; measure allocations.
- Use `Vec::with_capacity`, iterators, and `&str` at boundaries.
- `#[inline]` only after measurement.

## 9. Windows, FFI, Python

### Windows API

```toml
[dependencies]
windows = { version = "0.62", features = ["Win32_Foundation", "Win32_System_Threading"] }
```

```rust
#[cfg(windows)]
fn pid() -> u32 { std::process::id() }
```

- Use `windows-rs` over hand-written FFI when available.
- `unsafe` blocks need a safety comment: preconditions, ownership, lifetime.
- `extern "C"` + `#[no_mangle]` for C ABI; `cbindgen` for headers.

### PyO3 / maturin

```toml
[lib]
name = "fastcore"
crate-type = ["cdylib"]

[dependencies]
pyo3 = { version = "0.26", features = ["extension-module"] }
```

```rust
use pyo3::prelude::*;

#[pyfunction]
fn add(a: i64, b: i64) -> i64 { a + b }

#[pymodule]
fn fastcore(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(add, m)?)?;
    Ok(())
}
```

```powershell
python -m pip install maturin
maturin develop --release
```

This template is not compiled here; pin versions to the current PyO3 docs.

## 10. Troubleshooting table

| Symptom | Cause | Fix |
|---|---|---|
| `cannot move out of borrowed content` | trying to move from `&T` | clone, take ownership, or use `Option::take` |
| `does not live long enough` | reference outlives owner | return owned data; narrow scope; add lifetime only if correct |
| `cannot borrow as mutable` | overlapping borrows | shorten borrow; split fields; use `RefCell`/`Mutex` deliberately |
| `future is not Send` | `Rc`/`RefCell`/guard across `.await` | use `Arc`/`tokio::sync`; drop guard before await |
| async task hangs | blocking call in executor | `spawn_blocking` or async I/O |
| `linker link.exe not found` | MSVC build tools missing | install VS Build Tools C++ workload |
| OpenSSL link error | native OpenSSL | use `rustls` or install OpenSSL |
| target not installed | missing std | `rustup target add <triple>` |
| duplicate crate versions | semver conflict | `cargo tree -d`; align versions |
| proc macro compile error | stale expansion | `cargo clean`; update macro crate |
| binary huge | debug info/LTO | release profile + strip + LTO |
| tests pass, prod fails | env/config difference | integration test; log config keys, not secrets |
| `cargo` slow | rebuild everything | sccache, narrower features, workspace |
| Windows path/encoding | non-UTF-8 | use `OsStr`, `PathBuf`; avoid `String` assumptions |

## 11. Templates

- `templates/cli.rs` — clap + serde JSON + anyhow.
- `templates/error.rs` — thiserror enum + `?`.
- `templates/async.rs` — Tokio timeout + spawn.
- `templates/lib.rs` — library API + tests.

## Sources

- The Rust Book: ownership, error handling, concurrency, async.
- Cargo Book; rustup; clippy; rustfmt.
- Tokio tutorial; serde; clap; thiserror/anyhow.
- PyO3 guide; maturin; windows-rs.

See `references/SOURCES.md`.
