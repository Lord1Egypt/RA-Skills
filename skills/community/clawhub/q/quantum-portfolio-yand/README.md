# quantum-portfolio-yand

A **ClawHub Skill** for hybrid quantitative portfolio optimization that runs
three solvers side-by-side on the same return panel:

1. **Classical baseline** — SLSQP mean-variance
2. **Quantum-inspired** — QUBO encoding + dimod / `neal` simulated-annealing sampler
3. **Geometric / higher-moment** — Yau's Affine-Normal Descent for MVSK
   (mean-variance-skewness-kurtosis), faithful to **arxiv:2604.25378** Algorithm 1
   and the YAND framework in **arxiv:2603.28448**

…and visualizes the disagreement between them.

## Why this skill exists

- Most "quantum portfolio" demos hide the classical baseline. This one forces
  honesty: if classical wins, the JSON summary will say so.
- Most MVSK implementations OOM at `N>50` because they materialize the
  `N³` coskewness and `N⁴` cokurtosis tensors. YAND-MVSK avoids both via
  sample-oracle reformulation through `A = R − 1μᵀ` and `z = Ax`.
- The geometry of the affine normal makes YAND **invariant to ill-conditioning**
  of Σ — exactly the regime where Newton/QP misbehaves.

## Files

```
quantum-portfolio-yand/
├── SKILL.md                      # ClawHub-style identity + persona + entrypoint
├── skill.json                    # machine-readable skill manifest
├── README.md                     # this file
├── requirements.txt
├── references/
│   ├── patterns.md               # how things must be built (QUBO, YAND, viz)
│   ├── sharp_edges.md            # known failure modes and fixes
│   └── validations.md            # input/output validation rules
├── scripts/
│   ├── data_loader.py            # synthetic data + CSV loader + summary
│   ├── qubo_solver.py            # dimod BQM build + neal sampler
│   ├── yand_solver.py            # YAND-MVSK (Algorithm 1 from 2604.25378)
│   └── run_pipeline.py           # end-to-end driver, produces 4 figures + JSON
├── examples/
│   └── demo_synthetic.md         # how to run, how to read outputs
└── assets/                       # generated figures land here
    ├── qubo_heatmap.png
    ├── energy_landscape.png
    ├── solution_histogram.png
    └── efficient_frontier.png
```

## Quickstart

```bash
pip install -r requirements.txt
python scripts/run_pipeline.py
```

Open the four PNGs in `assets/`. Read `examples/demo_synthetic.md` for how to
interpret them.

## Academic provenance

- 2603.28448 — Yau's Affine Normal Descent: Algorithmic Framework and Convergence Analysis
- 2604.25378 — YAND for Large-Scale Unrestricted Higher-Moment Portfolio Optimization
- Cheng / Chen / Yau (2005) — Minimization with the Affine Normal Direction, *Comm. Math. Sci.* 3(4)
