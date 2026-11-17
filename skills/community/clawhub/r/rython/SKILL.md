---
name: rython
description: "Compile Python to native Rust with the rython toolchain (rythonc/rypip): single files, packages, no_std embedded targets, PyO3 bindings, userspace drivers, and Linux kernel modules — output verified byte-identical to CPython."
metadata: {"openclaw": {"emoji": "🐍", "requires": {"bins": ["rythonc", "rypip"]}}}
---

# Rython: Python → Rust compilation

Convert Python source to native Rust using the **rython** toolchain. The point of the exercise is that the user writes Python and the tool does the rest — **keep all logic in `.py`, treat generated Rust as a build artifact, never hand-write Rust glue when a rython flag exists.** Minimal non-Python code shipped.

## Toolchain

- Binaries: `rythonc` and `rypip` (v1.1.0) installed at `~/.cargo/bin`
- Source: `/home/tserica/rython` (workspace: `python-ast`, `python-mod`, `rypip`, `rythonc`, `stdpython`, `rykernel-shim`)
- Reference driver project: `/home/tserica/rython-kmod` (Python driver + generated kernel module, see below)
- Published on crates.io: `stdpython` 1.1.0, `rypip` 1.1.0, `python-ast` 1.1.0
- rython docs: `/home/tserica/rython/README.md` (full compatibility list; check it before promising features)

## Commands (all verified)

```bash
# Single file → Rust source
rythonc input.py -o output.rs            # -p pretty, -n nostd, -a ast-only, -s symbols-only

# Package/file → Rust crate (lib; top-level code becomes __module_init__)
rypip convert path/to/package -o my-crate

# → runnable binary: put code under `if __name__ == "__main__":` — generates fn main + bin
# → PyO3 bindings (importable from Python, adds `python` cargo feature + cdylib)
rypip convert pkg -o crate --pyo3
# → no_std (core+alloc only, embedded/wasm; OS-needing constructs fail loudly)
rypip convert pkg -o crate --no-std
# → Linux kernel module crate (cdylib, panic=abort, printk lowering, no stdpython)
rypip convert pkg -o kernel --kernel-module
# → rust-for-linux module!-macro crate (requires --kernel-module, RFL toolchain)
rypip convert pkg -o kernel --kernel-module --rust-for-linux
# → userspace driver crate for a rython byte-ring misc device (logic lib + syscall glue)
rypip convert driver.py -o driver --driver

rypip build pkg    # convert + compile (release)
rypip install pkg  # build + install to ~/.cargo/bin
```

Lossy-conversion warnings: `-W warn` (default; bakes `#[deprecated]` notes into generated code), `-W deny` (fail), `-W allow`.

## The compatibility boundary (enforced loudly)

A program either converts and behaves like CPython, or conversion **fails with a message naming exactly what is unsupported**. Nothing silently diverges. Pinned against CPython: `str(1e16)` == `1e+16`, `hash()` matches `PYTHONHASHSEED=0`, float repr, sort stability, exception messages.

Supported: annotated functions, struct-based classes, `try/except/finally`, loop `else`, comprehensions, f-strings + literal-template `str.format`, keyword args/defaults, core builtins (`print len range open sorted min max enumerate map filter zip sum pow repr hash isinstance`), string/list/dict/set methods, `with open(...)`, `functools.partial`/`lru_cache`/`cache` (exact LRU), conversion-time `argparse`, and stdlib: `math random os sys json re datetime time itertools functools heapq copy textwrap hashlib csv collections pathlib glob subprocess tempfile`.

**Gaps:** `int` is fixed `i64` (no bignum), variables keep one type, no heterogeneous containers, no generators/`yield`, `async/await`, `eval/exec`, `*args`/`**kwargs`, multiple inheritance, or dunder protocols.

**When conversion or build fails: refactor the Python, never the generated Rust.** The error is the tool telling you the surface boundary. Fix the .py and regenerate.

## Verified pitfalls (hit these so you don't have to)

1. `sum(range(n))` → compile error `PyRange: PySum<_>`. Use an explicit `total = total + i` loop with `total: int = 0`.
2. `str` `+=` accumulation in a loop → generated type mismatch (`&str` vs `String`, E0308). Use `lines = []` + `lines.append(...)` + `"\n".join(lines)`.
3. Top-level statements without a `__main__` block → lib-only crate (`__module_init__`, no binary, `cargo run` fails). For a runnable program wrap entry logic in `if __name__ == "__main__":` → generates `fn main`.
4. Generated `Cargo.toml` pins `stdpython = { path = "/home/tserica/rython/crates/stdpython" }` — fine on this machine; for a portable/publishable crate swap to `version = "1.1.0"` or pass `--stdpython <path>` / `RYPIP_STDPYTHON_PATH`.
5. Kernels: Python can't run in-kernel — rython AOT-compiles; the module is a dumb device, the compiled Python lives in user space (UIO pattern). `--kernel-module` needs kernel build headers (`make -C kernel`); `--rust-for-linux` needs the RFL toolchain.

## Standard workflow

1. Write/collect the `.py` (single source of truth; must also run under plain `python3`).
2. `rypip convert <target> -o <out>` (flags per target above); `-W deny` first if correctness-critical, then relax.
3. `cd <out> && cargo build --release` (or `rypip build`).
4. **Verify:** `python3 input.py > py.out`, run the compiled binary, `diff` — byte-identical is the bar. The rython test suite diffs generated binaries against `python3` line-for-line; follow suit.
5. Fix failures by editing the `.py` and regenerating (never edit `src/*.rs` by hand).

## Kernel driver workflow (rython-kmod)

`/home/tserica/rython-kmod`: `driver.py` is the single source of truth — driver logic + manifest constants consumed by codegen:
- Driver manifest: `__device_path__`, `__ioc_reset__`, `__ioc_stats__`
- Kernel manifest: `__module_name__`, `__module_license__`, `__module_author__`, `__module_description__`, `__module_version__`, `__device_name__`, `__bufsz__`, `__magic__`, `__device_mode__`

`make` targets: `gen` (regenerate `driver/` + `kernel/` from `driver.py` — both are uncommitted build artifacts), `test` (CPython tests), `test-rust` (cargo tests on generated crate), `load`/`unload` (insmod/rmmod), `demo` (drive `/dev/rython0` with the compiled driver), `udev`.

## When to use this skill

Trigger on: converting Python to Rust, "compile this .py", rython/rythonc/rypip tasks, Python drivers, kernel modules written in Python, no_std/embedded Python, PyO3 wrappers around Python logic. The skill exists so the toolchain facts above are never re-discovered from scratch.
