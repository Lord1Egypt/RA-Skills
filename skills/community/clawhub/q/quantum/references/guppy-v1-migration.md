# Guppy v1 migration (read before writing any kernel)

Guppy v1.0 (Python ≥ 3.12) is a breaking release. Every pre-v1 driver fails, and two of the
failures are silent-looking: the runner aborts inside Rust rather than raising a Python error.

```bash
pip install "guppylang>=1.0" numpy scipy   # selene-sim ships inside guppylang now
```

## Rename table

| pre-v1 | v1 |
| --- | --- |
| `from guppylang.std.builtins import result` | `... import output` |
| `result("tag", value)` | `output("tag", value)` |
| `measure(q)` → `bool` | `measure(q)` → `Measurement`; call `.read()` for the bool |
| `bits = measure_array(qs); output("q", bits[i])` | `output("q", bits[i].read())` |
| `if b:` after `b = measure(a)` | `b = measure(a).read()`, then `if b:` |
| `selene_sim.build(prog.compile()).run_shots(Quest(), ...)` | `prog.emulator(...)` builder |
| `pip install guppylang selene-sim` | `pip install "guppylang>=1.0"` |

`.read()` blocks until the measurement result is available; the compiler error if you forget is
`Values of type 'Measurement' cannot be passed to 'output' directly`.

## Canonical v1 run block

```python
from guppylang import guppy, OptimizationLevel
from guppylang.std.builtins import array, output
from guppylang.std.quantum import cx, h, measure_array, qubit
from selene_sim import DepolarizingErrorModel, Quest   # error models still live here

@guppy
def program() -> None:
    qs = array(qubit() for _ in range(3))
    h(qs[0]); cx(qs[0], qs[1])
    bits = measure_array(qs)
    for i in range(3):
        output("q", bits[i].read())

result = (
    program
      .emulator(n_qubits=3)
      .with_shots(512)
      .with_seed(7)
      .with_simulator(Quest())
      .with_error_model(DepolarizingErrorModel(random_seed=1, p_1q=1e-3, p_2q=1e-2, p_meas=1e-3))
      .run()
)

for shot in result:                      # EmulatorResult is iterable
    rec = {str(tag): int(v) for tag, v in shot.entries}
```

`EmulatorInstance` builder methods: `with_shots`, `with_seed`, `with_simulator`,
`with_error_model`, `with_n_qubits`, `with_n_processes`, `with_timeout`, `with_verbose`,
`with_progress_bar`, `with_event_hook`, `with_shot_offset`, `with_shot_increment`,
`with_runtime`, plus the shortcuts `statevector_sim`, `stabilizer_sim`, `coinflip_sim`.
`EmulatorResult` also exposes `results`, `register_counts`, `collated_counts`,
`register_bitstrings`, `to_pytket`.

## Do NOT hand a compiled package to Selene

```python
compiled = program.compile()
build(compiled).run_shots(Quest(), ...)   # WRONG on v1
```

This does not raise — it aborts:
`fatal runtime error: failed to initiate panic, error 5, aborting`. The emulator builder hangs off
the **program object**, so drop `.compile()` from every call site.

## Compatibility shim (the cheap way to migrate a large repo)

Rather than rewriting 37 drivers' run loops, add one module that keeps the legacy call shape and
routes it through the v1 builder — this repo's `quantum/emulate.py`:

```python
from quantum.emulate import build, Quest      # was: from selene_sim import build, Quest

runner = build(mod.program)                   # program object, NOT .compile()
for shot in runner.run_shots(Quest(), n_qubits=n, n_shots=S, error_model=em, seed=11):
    for tag, value in shot:
        ...
```

The shim re-exports `Quest`, `Stim`, `IdealErrorModel`, `DepolarizingErrorModel`,
`SimpleLeakageErrorModel`, `OptimizationLevel`, accepts both `seed` and `random_seed`, and raises a
clear `TypeError` if handed a compiled package. Migration then reduces to a per-file import swap.

## Default optimisation

v1 runs `RemoveRedundancies` on compile. Any experiment whose point is the gate sequence — rewriter
proofs, gate-count reporting, tomographic equivalence of two spellings of the same unitary — must
pin the classical-only level:

```python
prog = program.with_opt_level(OptimizationLevel.Classical)   # Minimal | Classical | Default
```

## Migration recipe that worked

1. Reinstall: `pip install --target .pydeps "guppylang>=1.0" numpy scipy`.
2. Probe the API in a scratch script before touching the repo (builder method names, `shot.entries`).
3. Add the shim module, then regex-sweep the tree:
   - `from selene_sim import ...` → `from quantum.emulate import ...` (leave the shim itself alone —
     it is easy to rewrite its own import into a circular one).
   - `mod.program.compile()` → `mod.program`.
   - `result("` → `output("`, including inside generated-source string templates.
   - append `.read()` on every `measure(...)` that feeds an `output(...)` or an assignment, and on
     `measure_array` elements read inside `output(...)`.
   - re-export lists in `*_lib.py` and `__init__.py` (`measure, result,` → `measure, output,`).
4. Import every module as a compile check:
   `for p in Path("quantum").rglob("*.py"): importlib.import_module(...)` — catches stale `result`
   imports instantly.
5. Run each experiment's smoke script; only then re-run sweeps.

Host-side variables named `result` (e.g. `result = runner.run(spec)`) must survive the rename —
scope the regex to `result(` followed by a quote and to import lines.

## Small v1 details that cost a debugging round each

- The T gate is exported as **`t`**, not `tgate` (`from guppylang.std.quantum import t`).
  Local aliases like `t as tgate` are a repo convention, not the API.
- Emulator entrypoint arguments are **kwargs on `run()`**: `program.emulator(...)....run(**args)`.
  Never call `.compile()` for execution — that object is for inspection/gate counts.
- Run drivers as `python3 -m package.module` **from the repo root**. Invoking the file by path
  breaks relative package imports inside kernel packages.

## Living with two Guppy versions

The QIR toolchain (`hugr-qir`, `pytket-qir`) still pins the 0.21 line, so a project with a QIR
lane runs **two environments**: the certified execution env on `guppylang>=1.0`, and a
disposable pinned venv on `guppylang==0.21.16`. Under 0.21, parameterized functions go through
`compile_function()`; under 1.0 the emulator builder replaces it. Keep QIR-targeted kernels in
their own module so the version split is visible at import boundaries rather than sprinkled
through shared code. See `references/qir-lane.md`.
