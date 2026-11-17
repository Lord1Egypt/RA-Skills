# Rust + Python Advanced — Sources

Official references used for the combined track:

- Rust Book ownership: https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html
- Rust Book errors: https://doc.rust-lang.org/book/ch09-00-error-handling.html
- Rust Book async: https://doc.rust-lang.org/book/ch17-00-async-await.html
- Cargo Book: https://doc.rust-lang.org/cargo/
- Tokio tutorial: https://tokio.rs/tokio/tutorial
- serde: https://serde.rs/
- PyO3 guide: https://pyo3.rs/
- maturin: https://www.maturin.rs/
- Python asyncio: https://docs.python.org/3/library/asyncio.html
- Python subprocess: https://docs.python.org/3/library/subprocess.html
- Python packaging: https://packaging.python.org/en/latest/tutorials/packaging-projects/
- Python typing: https://docs.python.org/3/library/typing.html

Local tests:

```text
rustc 1.93.1 / cargo 1.93.1 — cargo new + cargo run: Hello, world! exit 0
Python 3.13.5 — async_tasks.py exit 0; run_subprocess.py exit 0
PowerShell 7.6.7 — Invoke-SafeProcess.ps1 exit 0
```

Not verified in this run:

- The serde_json sidecar was not compiled.
- The PyO3/maturin template was not built.
- The Python bridge template expects `target/release/sidecar.exe` to exist.

Use the `rust-advanced` and `python-advanced` skills for the language-specific deep material.
