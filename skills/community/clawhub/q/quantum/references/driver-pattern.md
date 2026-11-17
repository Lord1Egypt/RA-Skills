# Driver pattern: parameterized kernels

## Problem

`@guppy` functions can take `float` parameters, but the **outer** program you `compile()` cannot easily close over Python runtime values — and Guppy reads its source via `inspect.getsource`, so you cannot build the program by `exec()`-ing a string.

If you want to sweep many parameter sets (e.g. SWAP-test every pair of patients), each program needs to be a real `.py` file on disk that Guppy can read.

## Solution

Write each parameterized program to a tempfile, then import it with `importlib.util`. The imported module's `program` attribute is a real `@guppy` function with the parameters baked in.

```python
import sys, tempfile, importlib.util, uuid
from pathlib import Path

def run_swap_test(i: int, j: int, shots: int = 2000):
    ai, bi, ci = feature_to_angles(PATIENTS[i]["features"])
    aj, bj, cj = feature_to_angles(PATIENTS[j]["features"])

    src = (
        "from quantum.qtda import guppy, swap_test\n"
        "@guppy\n"
        "def program() -> None:\n"
        f"    swap_test({ai!r}, {bi!r}, {ci!r}, {aj!r}, {bj!r}, {cj!r})\n"
    )

    tmpdir = Path(tempfile.gettempdir()) / "qtda_progs"
    tmpdir.mkdir(exist_ok=True)
    mod_name = f"qtda_prog_{i}_{j}_{uuid.uuid4().hex[:8]}"
    mod_path = tmpdir / f"{mod_name}.py"
    mod_path.write_text(src)

    spec = importlib.util.spec_from_file_location(mod_name, mod_path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)

    # Guppy v1: hand the program object to the emulator, never mod.program.compile()
    runner = build(mod.program)   # from quantum.emulate import build, Quest
    # ... run shots ...
```

## Key points

1. **One library file per experiment.** Keep `@guppy` helpers (`swap_test`, `cphase_on`, `probe_one`, …) in a stable `*_lib.py`. The generated template re-imports them by name; never inline helpers into the rendered source — Guppy needs each helper's source at a fixed importable location.
2. **`sys.path` injection before `exec_module`.** Generated files live under `tempfile.gettempdir()` but do `from quantum.<lib> import ...`. Insert your project root into `sys.path` first:
   ```python
   ROOT = Path(__file__).parent.parent
   if str(ROOT) not in sys.path:
       sys.path.insert(0, str(ROOT))
   ```
3. **Angle hygiene.** Before baking a float into source, wrap it to `(-π, π]`:
   ```python
   theta = ((theta + math.pi) % (2.0 * math.pi)) - math.pi
   ```
   Phase formulas like `2π · s · 2^j / N` grow large; the wrap avoids unreadable literals and trims floating-point noise.
4. **Use `{theta!r}` in the template.** `repr(float)` round-trips exactly into source; `str(float)` can truncate.
5. **Unique module names.** Use `uuid.uuid4().hex[:8]` to avoid `sys.modules` collisions across runs.
6. **Register in `sys.modules` BEFORE `exec_module`** so re-imports inside the generated file resolve.

## Alternatives that do not work

- `exec(src, globals())` — Guppy can't read source from string-`exec`'d functions.
- Jupyter cells — same `getsource` failure unless you use `%%writefile`.
- Closures over outer Python variables in `@guppy` functions — angles must be passed as `float` arguments or baked as literals, not closed over.

## See also

For parameter sweeps (G1, G3, G8, G9), prefer `SweepRunner` from `quantum/sweep.py` over rolling the loop above by hand — it's the same pattern factored into a `SweepSpec`. See `references/sweep-runner.md`.

A driver that can run on the hardware lane should take a `--resume-from` (gate label or job ids) and pass it straight to `SweepRunner(resume_from=…)`, so a lost process is recovered by downloading the jobs that were already billed instead of re-executing the rows. See `references/sweep-runner.md` (§Resuming a paid hardware sweep).

