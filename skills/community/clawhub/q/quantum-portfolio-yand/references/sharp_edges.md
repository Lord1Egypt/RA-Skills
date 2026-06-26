# Sharp Edges: Critical Failures And Why They Happen

Read this **before** diagnosing any unexpected portfolio behavior.

---

## SE1. QUBO Penalty Mis-scaling → Trivial Solutions

**Symptom**: every neal sample returns the same bitstring (often all-zero or all-one), or the cardinality constraint is silently violated.

**Cause**: penalty coefficient `P` in `P·(Σxᵢ − K)²` is either too small (cardinality ignored) or too large (drowns out the Markowitz objective; the sampler only sees the penalty landscape).

**Fix**: scale `P` to the same order as the objective range:
```
P = 2 · ( max(|μ|) + λ_max(Σ) )
```
If still violated, double `P` and re-run. If solutions become uniform, halve.

**Diagnostic**: plot `solution_histogram.png` — if one bitstring has >95% mass, `P` is too large.

---

## SE2. Covariance Matrix Near-Singularity → Markowitz Explodes, YAND Survives

**Symptom**: classical SLSQP returns extreme leverage-like weights (one asset at 0.99, others at ~0); YAND returns a much more balanced portfolio.

**Cause**: when assets are highly correlated, `Σ` has tiny eigenvalues. Newton/QP methods amplify noise along low-eigenvalue directions. **This is exactly the ill-conditioning that YAND's affine-invariance is designed to fix** (arxiv 2603.28448, abstract: "robust under strong anisotropic scaling").

**Fix**:
- Trust YAND in this regime.
- Optionally apply Ledoit-Wolf shrinkage to `Σ` before passing to SLSQP.
- Never apply shrinkage to YAND's input — it does not need it.

**Diagnostic**: condition number `κ(Σ) > 1e6` is the trigger.

---

## SE3. Coskewness/Cokurtosis Tensor Blow-Up → OOM Kill

**Symptom**: process killed with no error message when `N > ~50`.

**Cause**: naïve MVSK implementations build the coskewness `M₃ ∈ ℝ^{N×N×N}` and cokurtosis `M₄ ∈ ℝ^{N×N×N×N}` tensors. At `N=100`, `M₄` is `1e8` floats = **800 MB**. At `N=200`, `12.8 GB`.

**Fix**: this skill's `yand_solver.py` follows arxiv 2604.25378 §4.1 — it **never materializes higher-order tensors**. All higher-moment derivatives are computed via the sample-oracle reformulation through `A = R − 1μᵀ` and `z = Ax`. Verify by `top -p $(pgrep python)` — RSS should stay under 200 MB even at `N=500`.

**Anti-pattern (DO NOT DO THIS)**:
```python
M3 = np.einsum('ti,tj,tk->ijk', A, A, A) / T   # ← will OOM
```

---

## SE4. Simplex Boundary Collapse In YAND

**Symptom**: YAND iterate sticks at a vertex of Δₙ (one weight = 1 − τ, all others = τ), KKT residual stays > ε forever.

**Cause**: `α_max` boundary clipping repeatedly reduces step to zero on an active face. Algorithm 1 (arxiv 2604.25378) handles this via **active-face continuation** (steps 14–20): switch to a lower-dimensional simplex face when no descent direction is found in the full tangent space.

**Fix**: in `yand_solver.py`, after 5 consecutive `α* < 1e-10` steps, project iterate onto the active face and rebuild the orthonormal basis `U` for that face's tangent. If still no descent, declare local minimum.

**Diagnostic**: log `α*` per iteration; if it decays geometrically, you're on the wrong face.

---

## SE5. Fake Quantum Advantage

**Symptom**: a blog post / demo claims "quantum-simulated portfolio beats classical by 30%."

**Cause**: usually one of —
1. The classical baseline is misconfigured (no shrinkage, wrong risk aversion).
2. The QUBO is solved on a problem that classical QP solves to optimality in milliseconds — the "advantage" is just sampler noise.
3. Out-of-sample comparison is missing — the QUBO happened to fit the training set better.

**Fix**: this skill's three-way comparison (P3) makes fakes impossible to hide. Always report:
- In-sample objective values (must match within tolerance for convex problems)
- Out-of-sample Sharpe (the only honest metric)
- Wall-clock time (be honest: neal on `N=10` is slower than QP)

**Honest framing**: this skill demonstrates the **structure** of quantum-inspired optimization (QUBO encoding, energy landscape, sampling distribution) — not a runtime advantage at this scale.

---

## SE6. Quartic Line Search Returning Negative `α`

**Symptom**: YAND step makes objective increase.

**Cause**: cubic-derivative roots can include negative or complex values; if you forget to filter to `α ∈ [0, α_max]`, you may pick the wrong critical point.

**Fix**: in `_quartic_line_search`:
```python
roots = np.roots(deriv_coeffs)
real_roots = roots[np.abs(roots.imag) < 1e-10].real
candidates = [a for a in real_roots if 0 <= a <= alpha_max]
candidates += [0.0, alpha_max]   # always include endpoints
alpha_star = min(candidates, key=lambda a: f_along(a))
```

---

## SE7. neal Seed Not Reproducible Across Versions

**Symptom**: same seed, different machine, different solution.

**Cause**: `dwave-neal` random stream depends on the C++ RNG version. Major-version upgrades break reproducibility.

**Fix**: pin `dwave-neal` in `dependencies` (we pin `>=0.6,<0.7`). For exact reproducibility, additionally serialize `sampleset.record` to disk after the first run and diff against future runs.
