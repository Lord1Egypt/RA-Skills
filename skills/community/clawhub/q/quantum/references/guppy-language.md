# Guppy language

Guppy is a Python-embedded DSL for quantum circuits. Functions decorated with `@guppy` are compiled to a quantum IR.

## Imports

```python
from guppylang import guppy
from guppylang.std.builtins import output, owned, array
from guppylang.std.quantum import qubit, h, cx, rx, ry, rz, measure, discard, t as tgate, tdg
from guppylang.std.angles import angle, pi
```

## Gate set

- Single-qubit: `h(q)`, `rx(q, angle)`, `ry(q, angle)`, `rz(q, angle)`, `tgate(q)`, `tdg(q)`
- Two-qubit: `cx(control, target)`
- Allocation: `q = qubit()` — returns a fresh `|0>`
- Measurement: `m = measure(q).read()` — collapses and returns classical bit
- Sink: `output("label", m)` — record a classical value for the host
- Cleanup: `discard(q)` — release a qubit without measuring

No native Toffoli, CSWAP, `cphase`, or `crz` — decompose manually. `cx` + `rz` are sufficient for controlled phase (see `circuit-patterns.md`).

## Angles

**`angle(x)` takes HALFTURNS (multiples of π), NOT radians.** This is the #1 silent-correctness bug in Guppy work — the kernel compiles, runs, and produces plausible-looking shot statistics that are off by a factor of π. Always read every `angle(...)` literal in that unit.

- `angle(1.0)` = π (Z gate)
- `angle(0.5)` = π/2 (S gate)
- `angle(0.25)` = π/4 (T gate)
- `angle(-0.5)` = −π/2 (Sdag)
- For an arbitrary radian value `θ`, write `angle(θ / math.pi)`.

`pi` is also available as a Guppy constant inside kernels. Float literals baked into generated kernels must be finite and ideally wrapped to `(-1, 1]` halfturns — see `driver-pattern.md` (angle hygiene).


## Function shape

```python
@guppy
def my_kernel() -> None:
    q = qubit()
    h(q)
    m = measure(q).read()
    output("m", m)
```

- Return type is usually `None`; classical outputs flow through `output(...)`.
- Helper `@guppy` functions can take `qubit` and `float` parameters and be called from other `@guppy` functions.
- Ownership: a `qubit` passed to a function is moved. Either measure, discard, or return it; do not use it again in the caller.

## File-on-disk requirement

`@guppy` uses `inspect.getsource` to read the function body. The function must be defined in a `.py` file that exists on disk and is importable. REPL / `exec()` / dynamically-built source strings all fail unless you write them to a tempfile and import via `importlib` — see `driver-pattern.md`.