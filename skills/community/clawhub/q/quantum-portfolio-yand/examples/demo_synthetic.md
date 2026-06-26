# Demo — Synthetic 10-Asset / 2-Year Portfolio

## How to run

```bash
cd quantum-portfolio-yand
pip install -r requirements.txt   # or: pip install dimod dwave-neal numpy pandas scipy matplotlib
python scripts/run_pipeline.py
```

The pipeline will:

1. Generate a synthetic factor-model panel: 504 trading days × 10 assets, with annualized vol ≈ 12–18% per asset and condition number κ(Σ) chosen to be moderately ill-conditioned (so YAND has something interesting to do).
2. Run all three solvers in sequence:
   - Classical SLSQP (mean-variance, `q=0.5`)
   - QUBO + neal SimulatedAnnealingSampler (`num_reads=1000`, `num_sweeps=1000`)
   - YAND-MVSK with default preference `c = (1.0, 0.5, 0.1, 0.05)`
3. Save four figures into `assets/`:
   - `qubo_heatmap.png` — QUBO problem encoding structure
   - `energy_landscape.png` — sampling-energy diagnostics across reads
   - `solution_histogram.png` — distribution of unique solutions
   - `efficient_frontier.png` — three-way frontier comparison
4. Print a JSON summary to stdout containing weights, realized stats, and a
   pairwise cosine-similarity agreement report.

## Calling with a user CSV

```bash
python scripts/run_pipeline.py --csv my_returns.csv --c 1.0 0.5 0.2 0.1
```

CSV format: first column may be a date (auto-detected), remaining columns are
asset tickers, values are simple daily returns (e.g. `0.0123` for +1.23%).
NaN rows are dropped; >10% drops triggers a warning.

## Reading the output

- **`agreement.cosine_classical_yand` close to 1.0** → both methods agree, the
  problem is essentially mean-variance dominated.
- **Cosine drops below 0.7** → higher-moment effects matter; trust YAND.
- **QUBO selection ≠ top-K of YAND** → either penalty `P` is mis-scaled (see
  `references/sharp_edges.md` SE1), or the binary cardinality constraint is
  pushing the solution onto a fundamentally different face of the simplex.

## Expected runtime

On a modest laptop (no GPU): ~15–25 seconds end-to-end for `N=10`.
The efficient-frontier sweep dominates (10 q-values × 3 solvers = 30 fits).
