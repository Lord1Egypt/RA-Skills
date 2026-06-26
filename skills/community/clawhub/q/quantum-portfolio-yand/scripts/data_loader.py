"""Data loader for the quantum-portfolio-YAND skill.

Provides:
- generate_synthetic_returns(): built-in 10-asset x 2-year daily-return panel
  with embedded factor structure (so Sigma has interesting non-trivial eigenstructure).
- load_csv_returns(path): user CSV path -> validated (T, N) ndarray + tickers.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from pathlib import Path


DEFAULT_TICKERS = [f"A{i:02d}" for i in range(1, 11)]


def generate_synthetic_returns(
    n_assets: int = 10,
    n_days: int = 504,           # ~2 trading years
    n_factors: int = 2,
    seed: int = 42,
) -> tuple[np.ndarray, list[str]]:
    """Generate correlated daily returns via a low-rank factor model.

    R_t = B f_t + eps_t,    f_t ~ N(0, I_k),   eps_t ~ N(0, diag(sigma_eps^2))
    Then add a small idiosyncratic mean drift mu_i so the mean vector is not zero.
    """
    rng = np.random.default_rng(seed)
    # Factor loadings (N x k) with mostly positive loadings (market-like first factor)
    B = rng.normal(loc=0.0, scale=1.0, size=(n_assets, n_factors))
    B[:, 0] = np.abs(B[:, 0]) * 0.8 + 0.2          # market beta in [0.2, ~1.4]
    # Factor returns
    F = rng.normal(size=(n_days, n_factors)) * 0.012   # daily vol ~1.2%
    # Idiosyncratic
    sigma_eps = 0.008 + 0.004 * rng.random(n_assets)
    E = rng.normal(size=(n_days, n_assets)) * sigma_eps
    # Mean drift (annualized 4%-15%, daily)
    mu_daily = (0.04 + 0.11 * rng.random(n_assets)) / 252.0
    R = F @ B.T + E + mu_daily[None, :]
    tickers = [f"A{i:02d}" for i in range(1, n_assets + 1)]
    return R.astype(np.float64), tickers


def load_csv_returns(path: str) -> tuple[np.ndarray, list[str]]:
    """Load user CSV. First col may be a date; remaining cols are tickers (returns)."""
    df = pd.read_csv(path)
    # Detect/drop date column
    first_col = df.columns[0]
    try:
        pd.to_datetime(df[first_col])
        df = df.drop(columns=[first_col])
    except (ValueError, TypeError):
        pass
    # Drop NaN rows; warn if too many
    n_before = len(df)
    df = df.dropna()
    if len(df) < 0.9 * n_before:
        print(f"[WARN] Dropped {n_before - len(df)}/{n_before} rows due to NaN.")
    # Validate numeric
    if not all(np.issubdtype(df[c].dtype, np.number) for c in df.columns):
        raise ValueError("All non-date columns must be numeric returns.")
    R = df.to_numpy(dtype=np.float64)
    # Sanity: looks-like-returns check (V1)
    if R.std() > 1.0 or (R.min() > 0.0 and R.mean() > 0.5):
        raise ValueError(
            "Input looks like prices, not returns. "
            "Pass R = prices.pct_change().dropna()."
        )
    return R, list(df.columns)


def summarize_panel(R: np.ndarray, tickers: list[str]) -> dict:
    """Return basic stats for logging."""
    mu = R.mean(axis=0)
    Sigma = np.cov(R, rowvar=False)
    eig = np.linalg.eigvalsh(Sigma)
    return {
        "T": R.shape[0],
        "N": R.shape[1],
        "tickers": tickers,
        "mu_annualized_pct": (mu * 252 * 100).round(2).tolist(),
        "vol_annualized_pct": (np.sqrt(np.diag(Sigma) * 252) * 100).round(2).tolist(),
        "Sigma_cond_number": float(eig.max() / max(eig.min(), 1e-18)),
        "Sigma_min_eig": float(eig.min()),
    }


if __name__ == "__main__":
    R, t = generate_synthetic_returns()
    info = summarize_panel(R, t)
    print(f"Synthetic panel: T={info['T']}, N={info['N']}, "
          f"cond(Sigma)={info['Sigma_cond_number']:.2e}")
    print(f"Annualized mu (%): {info['mu_annualized_pct']}")
    print(f"Annualized vol (%): {info['vol_annualized_pct']}")
