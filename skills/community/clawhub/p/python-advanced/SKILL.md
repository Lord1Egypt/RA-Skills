---
name: python-advanced
description: "Advanced Python 3.13 on Windows: typed package design, pyproject/src layout, asyncio and cancellation, threads vs processes, robust subprocesses, pytest, ruff/mypy, profiling, C/PyO3 extensions, and Windows-specific failures. Use after the python-advanced basics when code must be typed, packaged, concurrent, testable, or fast."
category: software-development
---

# Python Advanced

Reference interpreter: **Python 3.13.5**; use `python` or `py -3.13`. Use `python-advanced` for interpreter/venv basics; this skill is the design and failure-mode layer.

## 1. Project layout

```text
project/
  pyproject.toml
  README.md
  LICENSE
  src/
    package_name/
      __init__.py
      cli.py
      core.py
  tests/
    test_core.py
  .venv/
```

- Use a **src layout**; it prevents importing the working tree instead of the installed package.
- One project, one distribution name, one import package.
- Do not commit `.venv`, `__pycache__`, `dist`, or `.egg-info`.
- Pin the interpreter in `requires-python`.

## 2. pyproject template

```toml
[build-system]
requires = ["hatchling>=1.27"]
build-backend = "hatchling.build"

[project]
name = "lygo-tool"
version = "0.1.0"
description = "Small typed tool"
readme = "README.md"
requires-python = ">=3.11"
license = "MIT"
dependencies = [
  "httpx>=0.27",
  "pydantic>=2.8",
]

[project.optional-dependencies]
dev = ["pytest>=8", "pytest-cov>=5", "ruff>=0.8", "mypy>=1.13"]

[project.scripts]
lygo-tool = "lygo_tool.cli:main"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.mypy]
strict = true
python_version = "3.11"
```

Build:

```powershell
python -m pip install -U build
python -m build
```

The wheel goes to `dist/`; install with the same interpreter.

## 3. Typing that pays for itself

```python
from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Literal, Protocol, TypeAlias

Mode: TypeAlias = Literal["fast", "safe"]

@dataclass(frozen=True, slots=True)
class Job:
    name: str
    retries: int = 0

class Store(Protocol):
    def put(self, key: str, value: bytes) -> None: ...
    def get(self, key: str) -> bytes | None: ...

def total(xs: Iterable[int]) -> int:
    return sum(xs)

def first(xs: Sequence[int]) -> int:
    if not xs:
        raise ValueError("empty")
    return xs[0]
```

Rules:

- `Protocol` for interfaces you do not own.
- `TypedDict` for JSON-like records; `dataclass` for domain objects.
- `Literal` for finite modes; `Annotated` for metadata.
- Avoid `Any`; isolate untyped third-party boundaries in one adapter.
- `from __future__ import annotations` makes annotations strings; good for startup and forward refs.
- Run `mypy --strict` or `pyright`; fix errors at boundaries first.

## 4. asyncio

```python
import asyncio

async def fetch(i: int) -> int:
    await asyncio.sleep(0.1)
    return i * 2

async def main() -> None:
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fetch(i)) for i in range(5)]
    print([t.result() for t in tasks])

asyncio.run(main())
```

- `asyncio.run()` is the entrypoint; do not call it inside a running loop.
- Use `TaskGroup` (3.11+) for structured concurrency; it cancels siblings on failure.
- Wrap network calls in `asyncio.timeout(10)`.
- Use `asyncio.to_thread()` for blocking libraries.
- Do not call `time.sleep`, `requests`, or CPU-heavy code directly in a coroutine.
- Cancel tasks deliberately and await cancellation.
- `async with` for clients/sessions; close them.

## 5. Threads vs processes

| Workload | Choice |
|---|---|
| Network/file I/O, waiting | threads or asyncio |
| CPU-bound pure Python | `ProcessPoolExecutor` |
| C library releasing the GIL | threads may help |
| Shared mutable state | avoid; queue/message passing |
| Windows multiprocessing | guard with `if __name__ == "__main__":` |

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

with ThreadPoolExecutor(max_workers=8) as ex:
    results = list(ex.map(fetch_url, urls))

with ProcessPoolExecutor() as ex:
    results = list(ex.map(cpu_job, items))
```

- Windows uses **spawn**; the entry module is re-imported. Guard the entrypoint.
- Do not pass unpicklable objects to processes.
- Threads share memory; processes do not.
- The GIL limits pure-Python CPU parallelism; use processes or native code.

## 6. Robust subprocesses

```python
import subprocess, sys

def run(cmd: list[str], timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        check=False,
        shell=False,
    )
```

Rules:

- `shell=False` unless you need shell syntax; then never interpolate untrusted input.
- Pass a **list**, not a string with spaces.
- Set `timeout`; handle `subprocess.TimeoutExpired`.
- `check=True` raises `CalledProcessError`; `check=False` means inspect `returncode`.
- Use `encoding` + `errors` on Windows; console code pages are not UTF-8.
- Capture both streams; a full pipe can deadlock if the child writes a lot.
- For long-lived children, use `Popen` with explicit pipes/files and a reader thread.

## 7. Files, JSON, encoding

```python
from pathlib import Path
import json

p = Path("data") / "config.json"
data = json.loads(p.read_text(encoding="utf-8"))
p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
```

- Always specify `encoding="utf-8"` for text.
- `Path` over string concatenation.
- `json.dumps(..., ensure_ascii=False)` for Japanese/Unicode.
- Atomic write: write a temp file in the same directory, then `os.replace`.
- Use `newline=""` for CSV.

## 8. Testing and quality

```powershell
python -m pytest -q
python -m pytest --cov=package_name --cov-report=term-missing
python -m ruff check .
python -m ruff format --check .
python -m mypy src
```

Pytest patterns:

```python
import pytest
from package_name.core import normalize

def test_normalize():
    assert normalize(" Hi ") == "hi"

def test_empty():
    with pytest.raises(ValueError):
        normalize(" ")

@pytest.fixture
def tmp_config(tmp_path):
    p = tmp_path / "config.json"
    p.write_text('{"ok": true}', encoding="utf-8")
    return p
```

- `monkeypatch` for env vars and network.
- Parametrize cases; do not duplicate test bodies.
- Test the public API, not private helpers.
- Use `tmp_path`, not the repo directory.
- Avoid sleeps; use events/fakes.

## 9. Profiling and performance

```powershell
python -m cProfile -o out.prof .\script.py
python -m pstats out.prof
python -m timeit -s "x=list(range(1000))" "sum(x)"
```

- `cProfile` for call counts; `py-spy` for live processes (if installed).
- `tracemalloc` for allocations.
- Measure before changing; vectorize with NumPy only when the dependency is justified.
- Cache expensive pure functions with `functools.lru_cache`, but not functions with side effects.
- Use generators for large streams instead of building lists.

## 10. Native extensions

- `ctypes` for simple C ABI calls; define `argtypes`/`restype`.
- `cffi` for a safer C API.
- `PyO3` + `maturin` for a Rust extension:

```powershell
python -m pip install maturin
maturin develop --release
```

- Match the extension ABI to the interpreter; do not mix 32/64-bit or debug/release runtimes.
- Build wheels per platform; pure-Python wheels are not enough for C extensions.

## 11. Troubleshooting table

| Symptom | Cause | Fix |
|---|---|---|
| `python` opens Store | WindowsApps alias | use `python` or `py` |
| `ModuleNotFoundError` after install | wrong interpreter/venv | run `sys.executable`; use `-m pip` |
| `pip` installs elsewhere | pip tied to another Python | `python -m pip`, not bare `pip` |
| `asyncio.run()` error | already inside a loop | make the caller async; do not nest |
| “coroutine was never awaited” | forgot `await` | await or schedule it |
| Task hangs | blocking call in loop | `to_thread` / async library / timeout |
| `TimeoutExpired` leaves child | `subprocess.run` kills only direct child | use process group/job object; inspect |
| Windows `spawn` re-runs main | no guard | `if __name__ == "__main__":` |
| UnicodeDecodeError | default cp1252 | `encoding="utf-8", errors="replace"` |
| JSON looks escaped | `ensure_ascii=True` | `ensure_ascii=False` |
| package imports from cwd | flat layout | src layout; install editable |
| slow tests | real sleeps/network | fixtures, fakes, monkeypatch |
| `mypy` errors in third-party | no stubs | `ignore_missing_imports` for that module only |
| C extension import fails | ABI/arch mismatch | rebuild for this interpreter/arch |
| long path failure | Win32 limit | enable long paths; use `\\?\`; shorten root |
| stdlib import breaks | local file named `subprocess.py`/`asyncio.py` | rename the local module |

## 12. Templates

- `templates/pyproject.toml`
- `templates/cli_app.py`
- `templates/async_tasks.py`
- `templates/run_subprocess.py`
- `templates/test_example.py`

## Sources

- Python docs: asyncio, typing, pathlib, subprocess, venv, packaging.
- PyPA packaging tutorial.
- pytest, ruff, mypy.
- PyO3/maturin.

See `references/SOURCES.md`.
