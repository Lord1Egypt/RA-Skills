# Selene runtime

Selene is Quantinuum's emulator. Since Guppy v1.0 it ships inside `guppylang` and is driven by the
`program.emulator(...)` builder. Read `references/guppy-v1-migration.md` first if you are touching
pre-v1 code.

## Imports

```python
from quantum.emulate import build, Quest   # repo shim over the v1 emulator builder
# native: program.emulator(...) with `from selene_sim import Quest`
```

`Quest` is the default statevector backend. Other backends exist but Quest is the right default for small circuits (<= ~20 qubits).

## Pipeline

```python
# Native v1: the builder hangs off the @guppy program — never off program.compile()
res = (
    my_program
      .emulator(n_qubits=5)
      .with_shots(2000)
      .with_simulator(Quest())
      .run()
)
for shot in res:
    for name, value in shot.entries:
        # name is the string from output("name", ...)
        # value is the classical bit/integer
        ...

# Shim form used by every driver in quantum/ (same iteration shape as pre-v1):
runner = build(my_program)
for shot in runner.run_shots(Quest(), n_qubits=5, n_shots=2000):
    for name, value in shot:
        ...
```

## Shot iterator

Each `shot` is an iterable of `(label, value)` pairs — one entry per `output(...)` call in the kernel. If your kernel calls `output("anc", m)` once per shot, each shot yields exactly one pair. Natively the pairs live on `shot.entries`; the shim flattens them for you.

## Counting outcomes (SWAP-test example)

```python
zeros = total = 0
for shot in runner.run_shots(Quest(), n_qubits=5, n_shots=N):
    for _, val in shot:
        total += 1
        if int(val) == 0:
            zeros += 1
p0 = zeros / total
fidelity = max(0.0, min(1.0, 2.0 * p0 - 1.0))   # SWAP-test inversion
```

## `n_qubits` argument

Pass the **maximum** number of live qubits the kernel allocates simultaneously. For the SWAP test in `qtda.py`: 1 ancilla + 2x2 patient registers = 5.

`measure(q)` releases the qubit slot, so mid-circuit-measured ancillas do NOT stack. A kernel with `n` data qubits and `k` sequential single-ancilla windows (allocate → probe → measure, then next window) still only needs `n_qubits = n + 1` live — the same slot is reused across windows. This is the pattern in `quantum/nadarasa_g2.py`. Only count ancillas that are simultaneously alive.

## Multi-result shots

When the kernel calls `output(...)` multiple times per shot (e.g. one per window plus one per final data qubit), each `shot` yields one `(label, value)` pair per call. Bin them into a dict for downstream decoding:

```python
shots = []
for shot in runner.run_shots(Quest(), n_qubits=n+1, n_shots=S):
    rec = {str(lbl): int(v) for lbl, v in shot}
    shots.append(rec)
```

## Integer decoding from per-qubit results

Kernels that emit one result per data qubit (`output("x0", measure(d0).read())`, `output("x1", ...)`, ...) reassemble into an integer host-side:

```python
x = 0
for j in range(n):
    x |= (rec.get(f"x{j}", 0) & 1) << j
```

Bucket `x` for the metric you want (residue `x % p` for G1, full histogram for collision probability — see `circuit-patterns.md`).

## Performance notes

- Quest is classical statevector — cost scales as `2^n_qubits` per shot.
- For deterministic-output circuits, classical statevector via NumPy is faster than running 2000 shots — use Selene for the *measurement statistics*, not the underlying amplitudes.

## Noise models

`selene_sim` still ships the three noise models under Guppy v1. Natively they go to
`.with_error_model(...)` on the emulator builder; through the repo shim they stay a
`runner.run_shots(..., error_model=...)` keyword. Default is `IdealErrorModel`.

```python
from selene_sim import (
    Quest,
    IdealErrorModel,
    DepolarizingErrorModel,
    SimpleLeakageErrorModel,
)
from quantum.emulate import build

runner = build(program)          # the @guppy program object, not program.compile()


# Depolarizing: per-gate Pauli-twirl + per-measure bit-flip + per-init reset error.
runner.run_shots(
    Quest(), n_qubits=N, n_shots=512,
    error_model=DepolarizingErrorModel(
        p_1q=0.01, p_2q=0.10, p_meas=0.02, p_init=0.0,
    ),
)

# Leakage: every 2-qubit gate (cphase, cx, etc.) is a leakage opportunity.
# Leaked qubits leave the computational subspace and bias subsequent measurements.
runner.run_shots(
    Quest(), n_qubits=N, n_shots=512,
    error_model=SimpleLeakageErrorModel(p_leak=0.003, leak_measurement_bias=0.5),
)
```

Conventions used across `quantum/pqp_frontier/noise_*.py`:

- `p_2q = 10 × p_1q` (hardware ratio Q-System / H1-2 era)
- `p_meas = 2 × p_1q`
- `p_init = 0` unless explicitly sweeping initialisation errors
- Sweep `p_1q ∈ {0, 0.001, 0.003, 0.01, 0.03, 0.1}` for the "log-spaced 6-row noise curve" used in `/nadarasa/proofs/noise`.

**No coherent / T1-T2 model ships today.** Attempting `from selene_sim import CoherentErrorModel` raises `ImportError`. If hardware-shaped noise is required, layer it host-side over `IdealErrorModel` shots, or fall back to `DepolarizingErrorModel + SimpleLeakageErrorModel` as a two-axis sweep. This is the gotcha that killed the first Track C-2q design.

### Realistic H2-2 noise-parameter targets

When calibrating a sweep against Quantinuum's own H2-2 emulator settings (published in the July 2026 SoftBank/Quantinuum white paper §3.10), use:

| Channel | Parameter | Value |
| --- | --- | --- |
| 2-qubit gate fault | `p_2q` | 1.29 × 10⁻³ |
| Readout `0 → 1` | `p_r_01` | 0.9 × 10⁻³ |
| Readout `1 → 0` | `p_r_10` | 1.8 × 10⁻³ |
| Coherent memory | `f` | 4.3 × 10⁻² rad/s |
| Incoherent memory | `g` | 2.8 × 10⁻³ /s |

Map `p_2q` directly into `DepolarizingErrorModel(p_2q=1.29e-3, p_1q=1.29e-4, p_meas=1.35e-3, ...)`. Memory noise has no first-class Selene model — capture its effect either via a proxy `p_meas` inflation or by extending idle time in the compiled circuit.

**Dominance ordering (measured, from the same source).** Under representative pFT settings, **incoherent memory noise and gate + readout errors dominate**; coherent memory noise is well-suppressed by **dynamical decoupling** even at `f = 4.3e-2 rad/s`. Practical rules:

1. In any noise-activation sweep, hit incoherent memory + gate/readout first — they are where the budget actually lives.
2. Enable DD on any encoded circuit that transports or idles qubits; coherent memory is not the enemy once DD is on.
3. Report the decoherence parameter `q` per channel (mirror-benchmark on `k = 3, 5`) rather than a scalar "logical error" to preserve the dominance signal.




## Shipping results to the frontend

Selene results ship as **committed static JSON**, never as a live server function.

### Do

```python
# In the Python driver, after all shots finish:
out = Path("src/data/demos/pqp_frontier_noise_2q.json")
out.write_text(json.dumps(payload, indent=2))
```

```tsx
// In the route file:
import data from "@/data/demos/pqp_frontier_noise_2q.json";

export const Route = createFileRoute("/nadarasa/proofs/noise-2q")({
  component: () => <Noise2QView data={data} />,
});
```

Static import → zero runtime cost, works in SSR and prerender, survives the Cloudflare Worker sandbox.

### Do NOT

- Do not write a `createServerFn` handler that shells out to Python. The Worker runtime stubs `child_process.spawn` and calls raise `[unenv] spawn is not implemented yet!` at runtime.
- Do not write a `createFileRoute` `server` handler that reads the sweep cache directory (`_cache_*/`, `/tmp/...`, etc). The Worker filesystem is a virtual bundle and arbitrary paths are not reachable in production.
- Do not build a "live status" panel that polls a server function. Every attempt at this pattern in v0.4.1 (`sweep-status.ts`, `noise-2q-status.functions.ts`, `Noise2QStatusPanel.tsx`, `auto_resume_noise_2q.sh`) had to be deleted.

### If progress visibility is needed while a sweep runs

Print row-by-row to stdout from the Python driver and watch the sandbox terminal — that's the correct progress UI during development:

```python
print(f"[{done}/{total}] {tag} p_pass={row['pass_rate']:.2f}", flush=True)
```

Ship the *finished* JSON to `src/data/demos/` when the sweep is complete, and re-render the static route.
