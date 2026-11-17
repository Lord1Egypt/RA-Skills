# Rust Advanced — Sources

Fetched / canonical official references:

- The Rust Programming Language — Understanding Ownership: https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html
- The Rust Programming Language — Error Handling: https://doc.rust-lang.org/book/ch09-00-error-handling.html
- The Rust Programming Language — Concurrency: https://doc.rust-lang.org/book/ch16-00-concurrency.html
- The Rust Book — Async: https://doc.rust-lang.org/book/ch17-00-async-await.html
- Cargo Book: https://doc.rust-lang.org/cargo/
- rustup: https://rust-lang.github.io/rustup/
- Clippy: https://doc.rust-lang.org/clippy/
- Tokio tutorial: https://tokio.rs/tokio/tutorial
- serde: https://serde.rs/
- clap: https://docs.rs/clap/latest/clap/
- thiserror: https://docs.rs/thiserror/latest/thiserror/
- anyhow: https://docs.rs/anyhow/latest/anyhow/
- PyO3 guide: https://pyo3.rs/
- maturin: https://www.maturin.rs/
- windows-rs: https://microsoft.github.io/windows-docs-rs/
- Rustonomicon (unsafe/FFI): https://doc.rust-lang.org/nomicon/

Local verification:

```text
rustc 1.93.1
cargo 1.93.1
cargo new + cargo run → Hello, world! exit 0
```

Not verified here:

- External-crate templates (`serde`, `clap`, `tokio`, `thiserror`, `pyo3`) were not compiled in this run.
- The PyO3 snippet is a shape, not a pinned build; use the current PyO3 guide.
