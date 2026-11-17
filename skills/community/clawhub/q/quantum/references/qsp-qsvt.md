# QSP / QSVT: kernel + phase finder

Two layers, both verified in this repo:

1. **Execution layer** (`quantum/nadarasa_g10.py`) — a `qsp_sequence` Guppy kernel that interleaves signal `W(x)` rotations with parameterised phase rotations `e^{iφ_k Z}` on a single signal qubit, then measures.
2. **Synthesis layer** (`quantum/nadarasa_g10_phasefinder.py`) — a pure-NumPy / SciPy loop that recovers the phase sequence `φ = (φ_0, …, φ_d)` from a target polynomial `p(x)`.

## Kernel shape

For a degree-`d` QSP sequence on signal `x ∈ [-1, 1]`:

```python
@guppy
def qsp_sequence(x: float) -> None:
    q = qubit()
    rz(q, angle(phi_0))
    # repeated d times, with phi_k baked in as float literals:
    rx(q, angle(2.0 * math.acos(x)))   # W(x) reflection
    rz(q, angle(phi_k))
    # ...
    output("m", measure(q).read())
```

`P(m=0)` over many shots is the empirical response `|p(x)|²`. Sweep `x` across a grid (G10 uses 16 points × 2048 shots) and the histogram traces the target polynomial.

## Synthesis loop

Phase finding for low-degree polynomials is well-behaved with a generic SciPy optimiser; we don't need the full Laurent / matrix-completion machinery (Haah 2019). The pattern from `nadarasa_g10_phasefinder.py`:

```python
from scipy.optimize import minimize

def qsp_response(phi, x):
    # exact 2x2 product over the QSP unitary -> top-left amplitude
    ...

def loss(phi):
    return sum((qsp_response(phi, x) - target(x))**2 for x in grid)

res = minimize(loss, x0=np.zeros(d+1), method="Powell",
               options={"xtol": 1e-8, "ftol": 1e-10, "maxiter": 20_000})
```

Then feed `res.x` into the kernel as `phi_k` literals (via the driver template; see `driver-pattern.md`) and sweep.

## Target: Chebyshev `sign(x)`

The standard textbook test — a low-degree odd polynomial approximation of `sign(x)` on `[-0.5, 0.5]`. Degree ≤ 9 is the "easy" regime; higher degrees become numerically brittle and need the dedicated phase-finding literature.

## Acceptance gate

After the full pipeline (synthesis → kernel literals → Selene shots):

```
max over the grid of  |empirical P(m=0)^{1/2}  −  target(x)|   <  0.05
```

The repo run hits worst-case Δ ≈ 0.0169 — well under the gate.

## Common pitfalls

- **Convention drift.** "Wx convention" vs. "reflection convention" differ by overall phase factors; pick one (this repo uses reflection / Rx-by-`2 arccos x`) and stick to it across synth and kernel.
- **Powell over BFGS.** The loss surface is non-smooth at degenerate phase choices; Powell is more robust than gradient-based methods at this scale.
- **Always cross-check classically.** Compute the exact 2×2 product in NumPy at the recovered φ, plot against target, before launching Selene shots.
