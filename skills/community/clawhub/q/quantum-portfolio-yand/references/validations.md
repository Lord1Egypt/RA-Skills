# Validations: Strict Rules and Constraints

Use this file to objectively validate user inputs. If user input violates any rule below, **politely reject and explain** — do not silently coerce.

---

## V1. Return Matrix Shape

- `R` must be 2-D, `shape == (T, N)` with `T ≥ 60` and `2 ≤ N ≤ 500`.
- Rows = time observations (typically daily), columns = assets.
- Values must be **simple returns** (e.g. `0.012` for +1.2%) — NOT log returns, NOT prices, NOT percentages (`1.2`).
- Detect price-like input: if `R.std() > 1.0` or `R.min() > 0.0` consistently, raise `ValueError("Input looks like prices, not returns. Pass R = prices.pct_change().dropna().")`.

---

## V2. Return Matrix Conditioning

- `Σ = np.cov(R, rowvar=False)` must be positive semi-definite up to numerical noise: `min(eigvals(Σ)) > -1e-10`.
- Condition number `κ(Σ)`: log it. If `κ > 1e8`, warn user that classical SLSQP is unreliable — but YAND will still run.
- If any column of `R` is constant (`std == 0`), reject: `ValueError("Asset {i} has zero variance, drop it.")`.

---

## V3. Preference Vector `c`

- `c = (c₁, c₂, c₃, c₄)` with `cᵢ ≥ 0` for all `i`.
- At least two of the four must be `> 0` (a single-moment problem is degenerate).
- Default: `c = (1.0, 0.5, 0.1, 0.05)`.
- If user passes only `c=(c₁,c₂)`, auto-fill `c₃=c₄=0` and warn that the problem reduces to mean-variance.

---

## V4. Cardinality (QUBO branch)

- `K` must satisfy `1 ≤ K ≤ N`.
- Default: `K = ceil(N/3)`.
- If `K == N`: skip QUBO entirely (no selection problem) — log a notice.
- If `K == 1`: also skip QUBO and just pick `argmax(μ)` (no combinatorial structure).

---

## V5. Solver Hyperparameters

| Parameter | Default | Valid range | Notes |
|---|---|---|---|
| `num_reads` (neal) | 1000 | [100, 100000] | < 100 risks missing global min |
| `num_sweeps` (neal) | 1000 | [100, 100000] | < 100 may not equilibrate |
| `beta_range` | (0.1, 50) | low > 0, high > low | controls inverse temp schedule |
| `eps` (YAND KKT) | 1e-6 | (0, 1e-2] | tighter rarely improves |
| `max_iter` (YAND) | 500 | [10, 10000] | typical convergence in 30–80 |
| `lambda_tikhonov` | 1e-8 | [0, 1e-2] | guards near-degenerate Hessian |
| `tau` (interior margin) | 1e-4 | (0, 1/(2N)) | strict-interior warm start |

---

## V6. KKT Stopping Criterion (YAND)

YAND has converged when:
- `‖U^T ∇f(x*)‖₂ ≤ ε`, AND
- `xᵢ* ≥ τ` for all `i` OR active-face KKT residual on the active face ≤ ε.

If reached `max_iter` without convergence, return current iterate **with a warning** including final reduced-gradient norm — do not silently claim success.

---

## V7. Output Sanity Checks

Before returning any portfolio `x*`:

- `|Σxᵢ* − 1| < 1e-6` (budget)
- `xᵢ* ≥ −1e-9` for all `i` (long-only, allow tiny numerical leak)
- For QUBO output: exactly `K` ones in the binary vector, otherwise re-run with adjusted `P`.
- Realized in-sample variance `xᵀΣx > 0` (sanity: not a degenerate corner).

---

## V8. Asset File Validation (CSV Path)

- File must be readable as CSV with a header row.
- First column may be a date column (auto-detected via `pd.to_datetime`).
- Drop rows with any NaN; if more than 10% of rows dropped, warn user.
- Reject CSVs where a column has a non-numeric dtype after the date column.

---

## V9. Reproducibility Guarantees

This skill commits to:
- `numpy.random.seed(42)` for any synthetic data generation.
- `seed=42` passed to `SimulatedAnnealingSampler.sample(...)`.
- Same `(R, c, hyperparameters, seed)` → same outputs (figures bit-identical, weights to 1e-10).
- If reproducibility fails across `dwave-neal` versions, document in `sharp_edges.md` SE7.
