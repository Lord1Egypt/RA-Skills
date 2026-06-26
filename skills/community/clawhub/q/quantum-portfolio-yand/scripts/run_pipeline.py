"""End-to-end pipeline: load data -> run 3 solvers -> produce 4 figures + JSON summary.

Figures saved into ../assets/:
    qubo_heatmap.png
    energy_landscape.png
    solution_histogram.png
    efficient_frontier.png
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import minimize

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from data_loader import generate_synthetic_returns, load_csv_returns, summarize_panel
from qubo_solver import build_qubo, solve_qubo, best_selection, selection_to_weights
from yand_solver import yand_mvsk

ASSETS = HERE.parent / "assets"
ASSETS.mkdir(exist_ok=True)

plt.rcParams.update({"figure.dpi": 110, "savefig.dpi": 140, "font.size": 10})


# --------------------------- classical SLSQP baseline ---------------------------

def slsqp_mv(mu: np.ndarray, Sigma: np.ndarray, q: float = 0.5) -> np.ndarray:
    N = len(mu)
    x0 = np.full(N, 1.0 / N)
    cons = [{"type": "eq", "fun": lambda x: x.sum() - 1.0}]
    bnds = [(0.0, 1.0)] * N
    obj = lambda x: -(1 - q) * (mu @ x) + q * (x @ Sigma @ x)
    res = minimize(obj, x0, method="SLSQP", bounds=bnds, constraints=cons,
                   options={"ftol": 1e-10, "maxiter": 500})
    return res.x


# --------------------------- visualization ---------------------------

def plot_qubo_heatmap(Q: np.ndarray, tickers: list[str], path: Path):
    N = Q.shape[0]
    vmax = float(np.max(np.abs(Q)))
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    im = ax.imshow(Q, cmap="RdBu_r", vmin=-vmax, vmax=vmax)
    ax.set_xticks(range(N)); ax.set_yticks(range(N))
    ax.set_xticklabels(tickers, rotation=45, ha="right")
    ax.set_yticklabels(tickers)
    ax.set_title("QUBO Matrix Q (N×N)\ndiagonal = linear, off-diagonal = quadratic / 2")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def plot_energy_landscape(sampleset, path: Path):
    energies = np.array([rec.energy for rec in sampleset.record])
    order = np.argsort(energies)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.2))
    axes[0].scatter(np.arange(len(energies)), energies, s=8, alpha=0.5, c="steelblue")
    axes[0].axhline(energies.min(), color="red", lw=1.2, label=f"min={energies.min():.3f}")
    axes[0].axhline(energies.mean(), color="orange", lw=1.0, ls="--",
                    label=f"mean={energies.mean():.3f}")
    axes[0].set_xlabel("read index"); axes[0].set_ylabel("final energy")
    axes[0].set_title("Per-read final energy (neal SimulatedAnnealingSampler)")
    axes[0].legend()
    axes[1].plot(energies[order], lw=1.2, color="steelblue")
    axes[1].set_xlabel("rank (sorted ascending)"); axes[1].set_ylabel("energy")
    axes[1].set_title("Sorted energy distribution — quantum-style landscape probe")
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def plot_solution_histogram(sampleset, path: Path, top_k: int = 20):
    samples = sampleset.record.sample
    bitstrings = ["".join(str(int(b)) for b in row) for row in samples]
    from collections import Counter
    counts = Counter(bitstrings)
    most = counts.most_common(top_k)
    labels = [b for b, _ in most]
    vals = [v for _, v in most]
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.bar(range(len(most)), vals, color="seagreen", edgecolor="black", linewidth=0.4)
    ax.set_xticks(range(len(most)))
    ax.set_xticklabels(labels, rotation=70, fontsize=7, family="monospace")
    ax.set_ylabel("count across num_reads samples")
    ax.set_title(f"Top-{len(most)} unique solutions found by simulated annealing\n"
                 f"(total unique = {len(counts)} / {len(bitstrings)} reads)")
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def plot_efficient_frontier(R, mu, Sigma, K, c_pref, marked_q, path: Path):
    """Sweep risk-aversion q from 0 to 1; plot (sigma, return) for all 3 solvers."""
    qs = np.linspace(0.05, 0.95, 10)
    cls_pts, qubo_pts, yand_pts = [], [], []

    for q in qs:
        # classical
        w_c = slsqp_mv(mu, Sigma, q=q)
        cls_pts.append((np.sqrt(w_c @ Sigma @ w_c), mu @ w_c))
        # qubo
        bqm, _, _ = build_qubo(mu, Sigma, K=K, q=q)
        ss = solve_qubo(bqm, num_reads=300, num_sweeps=500, seed=42)
        sel = best_selection(ss, len(mu))
        w_q = selection_to_weights(sel)
        qubo_pts.append((np.sqrt(w_q @ Sigma @ w_q), mu @ w_q))
        # YAND-MVSK with c scaled by q on variance
        c_scaled = np.array([1.0 - q, q, c_pref[2], c_pref[3]])
        res = yand_mvsk(R, c=c_scaled, max_iter=200)
        w_y = res.x
        yand_pts.append((np.sqrt(w_y @ Sigma @ w_y), mu @ w_y))

    cls_pts = np.array(cls_pts); qubo_pts = np.array(qubo_pts); yand_pts = np.array(yand_pts)

    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    ax.plot(cls_pts[:, 0], cls_pts[:, 1], "o-", color="tab:blue",
            label="Classical (SLSQP)", lw=1.4)
    ax.scatter(qubo_pts[:, 0], qubo_pts[:, 1], color="tab:green", marker="s",
               s=55, label="QUBO + neal (binary)", zorder=4)
    ax.plot(yand_pts[:, 0], yand_pts[:, 1], "^-", color="tab:red",
            label="YAND-MVSK", lw=1.4)
    # Mark user's c-pref result on YAND (the one matching c_pref exactly)
    res_user = yand_mvsk(R, c=c_pref, max_iter=300)
    w_user = res_user.x
    ax.scatter([np.sqrt(w_user @ Sigma @ w_user)], [mu @ w_user],
               marker="*", s=260, color="gold", edgecolor="black",
               label=f"YAND c=({c_pref[0]:.2f},{c_pref[1]:.2f},{c_pref[2]:.2f},{c_pref[3]:.2f})", zorder=5)
    ax.set_xlabel("Portfolio std-dev σ (daily)")
    ax.set_ylabel("Portfolio mean return μ (daily)")
    ax.set_title("Efficient Frontier — Three-Way Comparison")
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


# --------------------------- main driver ---------------------------

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", type=str, default=None,
                   help="optional CSV path; rows=dates, cols=tickers, values=returns")
    p.add_argument("--c", type=float, nargs=4, default=[1.0, 0.5, 0.1, 0.05],
                   help="MVSK preference vector (mean, var, skew, kurt)")
    p.add_argument("--num-reads", type=int, default=1000)
    p.add_argument("--num-sweeps", type=int, default=1000)
    p.add_argument("--n-assets", type=int, default=10)
    args = p.parse_args()

    if args.csv:
        R, tickers = load_csv_returns(args.csv)
    else:
        R, tickers = generate_synthetic_returns(n_assets=args.n_assets)

    info = summarize_panel(R, tickers)
    N = info["N"]
    K = math.ceil(N / 3)
    mu = R.mean(axis=0)
    Sigma = np.cov(R, rowvar=False)
    c_pref = np.array(args.c, dtype=float)

    print(f"=== Data: T={info['T']}, N={N}, cond(Σ)={info['Sigma_cond_number']:.2e} ===")

    # --- (1) Classical SLSQP ---
    w_cls = slsqp_mv(mu, Sigma, q=0.5)
    obj_cls = -(0.5) * (mu @ w_cls) + 0.5 * (w_cls @ Sigma @ w_cls)

    # --- (2) QUBO + neal ---
    bqm, Q, P_used = build_qubo(mu, Sigma, K=K, q=0.5)
    ss = solve_qubo(bqm, num_reads=args.num_reads, num_sweeps=args.num_sweeps, seed=42)
    sel = best_selection(ss, N)
    w_qubo = selection_to_weights(sel)

    # --- (3) YAND-MVSK ---
    yand_res = yand_mvsk(R, c=c_pref, verbose=False)
    w_yand = yand_res.x

    # --- Visualizations ---
    plot_qubo_heatmap(Q, tickers, ASSETS / "qubo_heatmap.png")
    plot_energy_landscape(ss, ASSETS / "energy_landscape.png")
    plot_solution_histogram(ss, ASSETS / "solution_histogram.png")
    plot_efficient_frontier(R, mu, Sigma, K, c_pref, marked_q=0.5,
                            path=ASSETS / "efficient_frontier.png")

    # --- One-line JSON summary ---
    def realized(w):
        return {
            "mean": float(mu @ w),
            "vol": float(np.sqrt(w @ Sigma @ w)),
            "sharpe_daily": float((mu @ w) / max(np.sqrt(w @ Sigma @ w), 1e-12)),
        }

    summary = {
        "T": info["T"], "N": N, "K_qubo": K,
        "tickers": tickers,
        "cond_Sigma": info["Sigma_cond_number"],
        "qubo": {
            "best_energy": float(ss.first.energy),
            "penalty_P": P_used,
            "selected": [tickers[i] for i, b in enumerate(sel) if b],
            "weights": np.round(w_qubo, 4).tolist(),
            "realized": realized(w_qubo),
        },
        "classical_slsqp": {
            "objective_q0.5": obj_cls,
            "weights": np.round(w_cls, 4).tolist(),
            "realized": realized(w_cls),
        },
        "yand_mvsk": {
            "c": c_pref.tolist(),
            "converged": yand_res.converged,
            "iters": yand_res.iters,
            "final_kkt": yand_res.final_kkt,
            "objective": yand_res.objective,
            "weights": np.round(w_yand, 4).tolist(),
            "realized": realized(w_yand),
        },
        "agreement": {
            "cosine_classical_yand": float(
                (w_cls @ w_yand) / (np.linalg.norm(w_cls) * np.linalg.norm(w_yand) + 1e-12)
            ),
            "cosine_qubo_yand": float(
                (w_qubo @ w_yand) / (np.linalg.norm(w_qubo) * np.linalg.norm(w_yand) + 1e-12)
            ),
        },
        "figures": [str(ASSETS / f) for f in [
            "qubo_heatmap.png", "energy_landscape.png",
            "solution_histogram.png", "efficient_frontier.png"
        ]],
    }

    print("\n=== SUMMARY ===")
    print(json.dumps(summary, indent=2, default=str))
    return summary


if __name__ == "__main__":
    main()
