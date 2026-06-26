# Patterns: How To Build Things In This Skill

This file dictates **how** every component of the quantum-portfolio-YAND pipeline must be constructed. If a generic textbook pattern conflicts with these patterns, the patterns here win.

---

## P1. QUBO Encoding for Cardinality-Constrained Markowitz

**Decision variable**: binary `xᵢ ∈ {0,1}` indicating asset `i` is selected.

**Objective (to MINIMIZE)**:

```
H(x) = q · xᵀ Σ x  −  (1−q) · μᵀ x  +  P · ( Σxᵢ − K )²
```

where:
- `Σ` = sample covariance matrix of returns
- `μ` = sample mean return vector
- `q ∈ [0,1]` = risk aversion (default `q=0.5`)
- `K` = target cardinality (default `K = ceil(N/3)`)
- `P` = penalty coefficient (default `P = 2 · (max|μ| + λ_max(Σ))`)

**Build pattern (dimod)**:

```python
import dimod
bqm = dimod.BinaryQuadraticModel('BINARY')
# linear: q*Σ_ii  − (1−q)*μ_i  + P*(1 − 2K)
for i in range(N):
    bqm.add_linear(i, q*Sigma[i,i] - (1-q)*mu[i] + P*(1 - 2*K))
# quadratic: 2q*Σ_ij  + 2P
for i in range(N):
    for j in range(i+1, N):
        bqm.add_quadratic(i, j, 2*q*Sigma[i,j] + 2*P)
```

**Sampler pattern**: always use `neal.SimulatedAnnealingSampler` with `num_reads=1000`, `num_sweeps=1000`, `beta_range=(0.1, 50)`. Never use `ExactSolver` for `N>15` (exponential blowup).

---

## P2. YAND-MVSK Iteration (Faithful to arxiv 2604.25378, Algorithm 1)

**Inputs**: return matrix `R ∈ ℝ^{T×N}`, preference `c=(c₁,c₂,c₃,c₄)`, interior start `x⁰ ∈ ri(Δₙ)`, margin `τ`, tolerance `ε`.

**Pre-compute**: `μ = R.mean(axis=0)`, `A = R − 1·μᵀ`. Choose orthonormal basis `U ∈ ℝ^{N×(N−1)}` for the simplex tangent space `{y : 1ᵀy = 0}` (e.g., via QR of `I − (1/N)11ᵀ`).

**At each iterate `xᵏ`**:

1. **Oracle**: compute `z = A xᵏ`, then
   - `g = ∇f(xᵏ) = −c₁μ + (2c₂/T)Aᵀz − (3c₃/T)Aᵀ(z⊙z) + (4c₄/T)Aᵀ(z⊙z⊙z)`
   - reduced gradient `ḡ = Uᵀ g`
2. **Stop** if `‖ḡ‖₂ ≤ ε`.
3. **Tangent Hessian-vector oracle** (no explicit tensors!):
   - `H_T v = Uᵀ [ (2c₂/T)AᵀA + (6c₃/T)Aᵀ diag(z) A · ... ] U v` — use matrix-vector form, never materialize.
4. **Affine-normal direction** (reduced):
   - `ν(y) = ḡ / ‖ḡ‖₂`
   - Solve regularized linear system `(H_T + λI) u = h − (‖ḡ‖/n) a`, where `h, a` are the gradient-and-adjoint vectors from the equi-affine construction.
   - `d_y = −u`, `d = U d_y`.
5. **Quartic exact line search**: `α ↦ f(xᵏ + α·d)` is a quartic in `α`. Compute coefficients `(a₀,a₁,a₂,a₃,a₄)`, take derivative (cubic), find real roots via `numpy.roots`, evaluate `f` at roots ∩ `[0, α_max]` and at endpoints, take argmin.
6. **Boundary**: `α_max = max{α : xᵏ + αd ≥ τ·1}`. If the unconstrained minimizer exceeds `α_max`, clip.
7. **Update**: `x^{k+1} = xᵏ + α* d`. Repeat.

**Critical**: never construct the coskewness tensor (`O(N³)` memory) or cokurtosis tensor (`O(N⁴)`). Always go through `A` and `z`.

---

## P3. Three-Way Comparison Discipline

For every input return panel, you MUST run all three solvers and report disagreement:

| Solver | Problem | Output | Use |
|---|---|---|---|
| **SLSQP-MV** | min `−μᵀx + q·xᵀΣx` s.t. simplex | continuous weights | classical baseline |
| **QUBO+neal** | min `H(x)` (P1) | binary selection, equal-weighted | quantum-inspired baseline |
| **YAND-MVSK** | min full quartic MVSK on simplex | continuous weights | geometric/higher-moment optimum |

Report **agreement metrics**:
- Cosine similarity of weight vectors (for continuous solvers)
- Jaccard index of selected sets (binarize continuous solvers at threshold `1/N`)
- Realized Sharpe / skew / kurt on each portfolio's in-sample returns

If cosine similarity between SLSQP and YAND drops below 0.7, **flag it as "higher-moment regime" and trust YAND**. If QUBO disagrees with both, check penalty coefficient `P`.

---

## P4. Visualization Patterns

Four canonical figures (matplotlib, no seaborn dependency):

1. **`qubo_heatmap.png`**: full `Q` matrix (linear on diagonal, quadratic/2 off-diagonal). Use `cmap='RdBu_r'`, symmetric `vmin/vmax`. Title: `"QUBO Matrix Q (N×N) — diagonal=linear, off-diag=quadratic/2"`.

2. **`energy_landscape.png`**: two subplots — left: scatter of `(read_index, final_energy)` from `sampleset.record`; right: sorted ascending energy curve. Annotate `min_energy` and `mean_energy` as horizontal lines.

3. **`solution_histogram.png`**: bar chart of the top-20 most-frequent unique bitstrings across `num_reads`. X-axis labels are bitstrings (rotated). Y-axis is count.

4. **`efficient_frontier.png`**: scatter of `(σ_p, μ_p)` for each candidate portfolio across a sweep of risk-aversion `q ∈ {0.0, 0.1, ..., 1.0}`. Three series: classical (line), QUBO (dots), YAND-MVSK (line). Mark the user's chosen `c` solution with a star.

---

## P5. Reproducibility

- Always set `numpy.random.seed(42)` for synthetic data and `seed=42` for `SimulatedAnnealingSampler.sample(...)`.
- Save figures at `dpi=140`, `bbox_inches='tight'`.
- Print a one-line JSON summary at end of `run_pipeline.py` so downstream tooling can grep results.
