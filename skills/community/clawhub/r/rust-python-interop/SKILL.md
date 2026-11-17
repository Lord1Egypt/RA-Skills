---
name: rust-python-interop
description: "Advanced Rust + Python engineering: choose the right language per layer, build typed Python around a Rust core, use subprocess JSON or PyO3/maturin, share errors and tests, profile both, and ship Windows binaries. Use when Python is fast enough to orchestrate but Rust is needed for CPU, memory, concurrency, or distribution — or when a Python/Rust boundary is failing."
category: software-development
---

# Advanced Rust + Python

This is the **combined** skill. It teaches the boundary, not just two syntaxes. Deep references:

- `rust-advanced`
- `python-advanced`
- `python-advanced` (Windows interpreter basics)
- `powershell-advanced` (orchestration)

Audited toolchain:

```text
rustc 1.93.1
cargo 1.93.1
Python 3.13.5
PowerShell 7.6.7
```

## 1. Choose the layer

| Need | Python | Rust |
|---|---|---|
| Glue, scripting, file/API work | **best** | possible, more code |
| Typed domain model | good | better for invariants |
| CPU-bound loops | slow | **best** |
| Memory control / no GC | no | **best** |
| Async I/O | asyncio/httpx | Tokio, more control |
| Fast iteration | **best** | slower |
| Single binary distribution | difficult | **best** |
| ML/data ecosystem | **best** | limited |
| Python extension | — | **PyO3** |

Decision rule:

> Start in Python. Move a **measured** hot path to Rust. Keep the boundary boring: JSON over stdin/stdout first, PyO3 only when call overhead matters.

## 2. Four integration patterns

| Pattern | Use when | Cost |
|---|---|---|
| **Sidecar JSON** | batch jobs, CLIs, isolation | process startup + serialize |
| **PyO3/maturin** | many small calls from Python | ABI/build complexity |
| **C ABI + ctypes** | existing C/Rust library | manual memory/type safety |
| **Local HTTP/socket** | long-running service | protocol/lifecycle |

Start with sidecar JSON. It is testable from PowerShell, Python, and CI.

## 3. Learning path — 8 labs

### Lab 1 — Python contract first

```python
from dataclasses import dataclass
import json

@dataclass(frozen=True)
class Job:
    id: int
    text: str

def encode(job: Job) -> str:
    return json.dumps({"id": job.id, "text": job.text})
```

Define the JSON schema before writing Rust. Test it in Python.

### Lab 2 — Rust sidecar

```rust
use std::io::{self, Read, Write};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input)?;
    let v: serde_json::Value = serde_json::from_str(&input)?;
    let out = serde_json::json!({ "ok": true, "echo": v });
    writeln!(io::stdout(), "{}", serde_json::to_string(&out)?)?;
    Ok(())
}
```

Cargo:

```toml
[dependencies]
serde_json = "1"
```

Build:

```powershell
cargo build --release
```

### Lab 3 — Python subprocess bridge

```python
import json, subprocess

def call_rust(exe: str, payload: dict) -> dict:
    p = subprocess.run(
        [exe],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
        check=False,
    )
    if p.returncode != 0:
        raise RuntimeError(f"rust exit {p.returncode}: {p.stderr}")
    return json.loads(p.stdout)
```

Rules:

- Pass JSON on stdin; read JSON on stdout; logs on stderr.
- Never parse human-readable text as the contract.
- Set a timeout and cap output size.
- Do not use a shell.

### Lab 4 — Rust library + tests

```rust
pub fn normalize(s: &str) -> Result<String, &'static str> {
    let t = s.trim();
    if t.is_empty() { return Err("empty"); }
    Ok(t.to_lowercase())
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn trims() { assert_eq!(normalize(" Hi ").unwrap(), "hi"); }
}
```

Run:

```powershell
cargo test
cargo clippy --all-targets -- -D warnings
cargo fmt --check
```

### Lab 5 — Python tests around the sidecar

```python
import json, subprocess
from pathlib import Path

EXE = Path("target/release/sidecar.exe")

def test_roundtrip():
    p = subprocess.run(
        [str(EXE)], input=json.dumps({"x": 1}),
        capture_output=True, text=True, encoding="utf-8", timeout=10,
    )
    assert p.returncode == 0
    assert json.loads(p.stdout)["ok"] is True
```

- Mark integration tests so they can be skipped if the binary is absent.
- Test malformed JSON, empty stdin, huge input, and non-zero exit.
- Compare Python and Rust results on the same fixtures.

### Lab 6 — PyO3 when calls are hot

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

```toml
[lib]
name = "fastcore"
crate-type = ["cdylib"]

[dependencies]
pyo3 = { version = "0.26", features = ["extension-module"] }
```

```powershell
python -m pip install maturin
maturin develop --release
```

This is a shape, not a compiled test. Pin PyO3 to the version in its current guide.

### Lab 7 — Async and concurrency

- Python: `asyncio.TaskGroup`, `asyncio.timeout`, `to_thread`.
- Rust: Tokio `spawn`, `timeout`, `select!`, `spawn_blocking`.
- Never block a Python event loop or a Tokio worker with synchronous CPU work.
- Pass results through channels/queues, not shared mutable state.

### Lab 8 — Package and ship

- Rust: `cargo build --release`, strip, LTO; sign if distributing.
- Python: build a wheel; pin `requires-python`.
- Ship the sidecar binary beside the Python package or resolve it via an env var.
- Test on a clean machine; do not assume `cargo` or Rust is installed for end users.
- For PyO3, build wheels per Python version/platform.

## 4. Cross-language error contract

Use a stable JSON error shape:

```json
{"ok":false,"code":"INVALID_INPUT","message":"...","retryable":false}
```

Rules:

- Rust exit code 0 = success; non-zero = failure.
- Python raises a typed exception on non-zero.
- Do not leak secrets or full stack traces to the caller; log them separately.
- Include a `request_id` for correlation.
- Map Rust `thiserror` variants to stable `code` values.

## 5. Performance method

1. Measure Python with `cProfile`, `timeit`, or `py-spy`.
2. Identify one hot function with a stable contract.
3. Write Rust with the same fixtures.
4. Compare wall time, memory, and startup.
5. Keep the Python fallback; switch behind a flag.
6. Do not rewrite I/O or glue in Rust unless measured.

## 6. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Python can't find sidecar | path resolution | resolve relative to package, or env var |
| Rust binary exits instantly | stdin closed / panic | log stderr; handle empty input |
| JSON parse mismatch | schema drift | one shared schema + fixture tests |
| Unicode mojibake | Windows console encoding | UTF-8 on both sides; `errors="replace"` |
| Rust `link.exe` missing | MSVC missing | install VS Build Tools C++ |
| PyO3 import fails | ABI/Python mismatch | rebuild with maturin for this interpreter |
| Python hangs on child | pipe full | read streams; cap output |
| Rust async not Send | non-Send across await | Arc/tokio sync; drop guard |
| slow calls | per-call process spawn | batch JSON or PyO3 |
| binary too large | debug/LTO | release profile + strip |
| Python packaging misses binary | package data | include sidecar as package data/wheel |
| tests pass locally, fail CI | toolchain missing | install Rust/Python versions explicitly |

## 7. Templates

- `templates/rust_json.rs`
- `templates/python_bridge.py`
- `templates/pyo3_lib.rs`
- `templates/pyproject_maturin.toml`
- `templates/powershell_runner.ps1`

## 8. Sources

- Rust Book ownership/errors/concurrency/async.
- Python asyncio/packaging/subprocess docs.
- PyO3 guide and maturin.
- Tokio tutorial; serde.

See `references/SOURCES.md`.
