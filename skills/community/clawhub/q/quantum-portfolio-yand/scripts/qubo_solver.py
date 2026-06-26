"""QUBO formulation + neal simulated-annealing solver.

Implements pattern P1 (see references/patterns.md):
    H(x) = q * x^T Sigma x  -  (1-q) * mu^T x  +  P * (sum(x) - K)^2
"""
from __future__ import annotations

import argparse
import math
import numpy as np
import dimod
import neal


def build_qubo(
    mu: np.ndarray,
    Sigma: np.ndarray,
    K: int,
    q: float = 0.5,
    P: float | None = None,
) -> tuple[dimod.BinaryQuadraticModel, np.ndarray, float]:
    """Construct dimod BQM for cardinality-constrained Markowitz.

    Returns (bqm, Q_matrix, P_used). Q_matrix is the dense N x N QUBO matrix
    used for visualization (diagonal = linear, off-diag = quadratic / 2).
    """
    N = len(mu)
    if P is None:
        P = 2.0 * (np.max(np.abs(mu)) + np.linalg.eigvalsh(Sigma).max())

    # Linear: q * Sigma_ii  - (1 - q) * mu_i  + P*(1 - 2K)
    linear = q * np.diag(Sigma) - (1.0 - q) * mu + P * (1.0 - 2.0 * K)
    # Quadratic: 2q * Sigma_ij + 2P  (i < j)
    bqm = dimod.BinaryQuadraticModel("BINARY")
    Q = np.zeros((N, N))
    for i in range(N):
        bqm.add_linear(i, float(linear[i]))
        Q[i, i] = float(linear[i])
    for i in range(N):
        for j in range(i + 1, N):
            qij = 2.0 * q * Sigma[i, j] + 2.0 * P
            bqm.add_quadratic(i, j, float(qij))
            Q[i, j] = qij / 2.0
            Q[j, i] = qij / 2.0
    return bqm, Q, float(P)


def solve_qubo(
    bqm: dimod.BinaryQuadraticModel,
    num_reads: int = 1000,
    num_sweeps: int = 1000,
    beta_range: tuple[float, float] = (0.1, 50.0),
    seed: int = 42,
) -> dimod.SampleSet:
    sampler = neal.SimulatedAnnealingSampler()
    return sampler.sample(
        bqm,
        num_reads=num_reads,
        num_sweeps=num_sweeps,
        beta_range=beta_range,
        seed=seed,
    )


def best_selection(sampleset: dimod.SampleSet, N: int) -> np.ndarray:
    best = sampleset.first.sample
    return np.array([best[i] for i in range(N)], dtype=int)


def selection_to_weights(selection: np.ndarray) -> np.ndarray:
    """Equal-weight on selected assets (V7-compatible)."""
    k = int(selection.sum())
    if k == 0:
        return np.full_like(selection, 1.0 / len(selection), dtype=float)
    w = np.zeros(len(selection), dtype=float)
    w[selection.astype(bool)] = 1.0 / k
    return w


def _cli():
    p = argparse.ArgumentParser()
    p.add_argument("--n-assets", type=int, default=10)
    p.add_argument("--k", type=int, default=None)
    p.add_argument("--num-reads", type=int, default=1000)
    p.add_argument("--num-sweeps", type=int, default=1000)
    p.add_argument("--q", type=float, default=0.5)
    args = p.parse_args()

    from data_loader import generate_synthetic_returns
    R, tickers = generate_synthetic_returns(n_assets=args.n_assets)
    mu = R.mean(axis=0)
    Sigma = np.cov(R, rowvar=False)
    K = args.k or math.ceil(args.n_assets / 3)
    bqm, Q, P = build_qubo(mu, Sigma, K=K, q=args.q)
    ss = solve_qubo(bqm, num_reads=args.num_reads, num_sweeps=args.num_sweeps)
    sel = best_selection(ss, args.n_assets)
    w = selection_to_weights(sel)
    print(f"Best energy : {ss.first.energy:.6f}")
    print(f"Penalty P   : {P:.4f}")
    print(f"Selected    : {[tickers[i] for i, b in enumerate(sel) if b]}")
    print(f"Weights     : {np.round(w, 4).tolist()}")


if __name__ == "__main__":
    _cli()
