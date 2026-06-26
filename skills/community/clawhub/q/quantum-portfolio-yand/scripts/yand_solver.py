"""YAND-MVSK solver — faithful implementation of arxiv 2604.25378 Algorithm 1.

Mean-Variance-Skewness-Kurtosis (MVSK) portfolio optimization on the simplex
using Yau's Affine-Normal Descent. NEVER materializes coskewness/cokurtosis
tensors — all higher-moment derivatives are computed via sample oracle through
A = R - 1 mu^T and z = A x.
"""
from __future__ import annotations

import numpy as np
from dataclasses import dataclass


@dataclass
class YANDResult:
    x: np.ndarray
    history: list
    converged: bool
    iters: int
    final_kkt: float
    objective: float


def _simplex_basis(N: int) -> np.ndarray:
    """Orthonormal basis U (N x (N-1)) for the simplex tangent {y: 1^T y = 0}."""
    H = np.eye(N) - np.ones((N, N)) / N
    Q, _ = np.linalg.qr(H)
    return Q[:, : N - 1]


def _mvsk_objective(x: np.ndarray, mu: np.ndarray, A: np.ndarray, c: np.ndarray) -> float:
    T = A.shape[0]
    z = A @ x
    m1 = mu @ x
    m2 = (z @ z) / T
    m3 = (z ** 3).sum() / T
    m4 = (z ** 4).sum() / T
    return float(-c[0] * m1 + c[1] * m2 - c[2] * m3 + c[3] * m4)


def _mvsk_gradient(x: np.ndarray, mu: np.ndarray, A: np.ndarray, c: np.ndarray) -> np.ndarray:
    T = A.shape[0]
    z = A @ x
    g = -c[0] * mu \
        + (2.0 * c[1] / T) * (A.T @ z) \
        - (3.0 * c[2] / T) * (A.T @ (z * z)) \
        + (4.0 * c[3] / T) * (A.T @ (z ** 3))
    return g


def _hessian_mv(x: np.ndarray, A: np.ndarray, c: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Hessian-vector product H f(x) v, sample-oracle form (no tensor)."""
    T = A.shape[0]
    z = A @ x
    Av = A @ v
    return ((2.0 * c[1] / T) * (A.T @ Av)
            - (6.0 * c[2] / T) * (A.T @ (z * Av))
            + (12.0 * c[3] / T) * (A.T @ ((z ** 2) * Av)))


def _quartic_line_search(
    x: np.ndarray, d: np.ndarray, mu: np.ndarray, A: np.ndarray,
    c: np.ndarray, alpha_max: float
) -> float:
    """Exact quartic line search: f(x + alpha d) is quartic in alpha."""
    T = A.shape[0]
    z = A @ x
    w = A @ d
    s2_0 = (z * z).sum() / T
    s2_1 = 2 * (z * w).sum() / T
    s2_2 = (w * w).sum() / T

    s3_0 = (z ** 3).sum() / T
    s3_1 = 3 * (z * z * w).sum() / T
    s3_2 = 3 * (z * w * w).sum() / T
    s3_3 = (w ** 3).sum() / T

    s4_0 = (z ** 4).sum() / T
    s4_1 = 4 * (z ** 3 * w).sum() / T
    s4_2 = 6 * (z ** 2 * w ** 2).sum() / T
    s4_3 = 4 * (z * w ** 3).sum() / T
    s4_4 = (w ** 4).sum() / T

    m1_0, m1_1 = mu @ x, mu @ d
    a0 = -c[0] * m1_0 + c[1] * s2_0 - c[2] * s3_0 + c[3] * s4_0
    a1 = -c[0] * m1_1 + c[1] * s2_1 - c[2] * s3_1 + c[3] * s4_1
    a2 = c[1] * s2_2 - c[2] * s3_2 + c[3] * s4_2
    a3 = -c[2] * s3_3 + c[3] * s4_3
    a4 = c[3] * s4_4

    def f_at(t):
        return a0 + t * (a1 + t * (a2 + t * (a3 + t * a4)))

    deriv = [4 * a4, 3 * a3, 2 * a2, a1]
    while len(deriv) > 1 and abs(deriv[0]) < 1e-18:
        deriv = deriv[1:]
    if len(deriv) <= 1:
        candidates = [0.0, alpha_max]
    else:
        roots = np.roots(deriv)
        real_roots = roots[np.abs(roots.imag) < 1e-10].real
        candidates = [float(r) for r in real_roots if 0.0 <= r <= alpha_max]
        candidates += [0.0, alpha_max]
    return min(candidates, key=f_at)


def _max_step_to_boundary(x: np.ndarray, d: np.ndarray, tau: float) -> float:
    """Largest alpha >= 0 s.t. x + alpha d >= tau component-wise."""
    neg = d < -1e-15
    if not np.any(neg):
        return 1e6
    bounds = (x[neg] - tau) / (-d[neg])
    bounds = bounds[bounds > 0]
    return float(bounds.min()) if bounds.size else 0.0


def yand_mvsk(
    R: np.ndarray,
    c: np.ndarray = np.array([1.0, 0.5, 0.1, 0.05]),
    x0: np.ndarray | None = None,
    eps: float = 1e-6,
    max_iter: int = 500,
    lambda_tikhonov: float = 1e-8,
    tau: float = 1e-4,
    verbose: bool = False,
) -> YANDResult:
    """Yau's Affine-Normal Descent for MVSK on the simplex."""
    T, N = R.shape
    mu = R.mean(axis=0)
    A = R - mu[None, :]
    if x0 is None:
        x = np.full(N, 1.0 / N)
    else:
        x = np.array(x0, dtype=float)
    U = _simplex_basis(N)

    history = []
    converged = False
    small_step_count = 0

    for k in range(max_iter):
        g = _mvsk_gradient(x, mu, A, c)
        gbar = U.T @ g
        kkt = float(np.linalg.norm(gbar))
        f_now = _mvsk_objective(x, mu, A, c)
        history.append({"iter": k, "f": f_now, "kkt": kkt})
        if verbose:
            print(f"[YAND iter {k:3d}] f={f_now:+.6e}  ||grad_T||={kkt:.3e}")
        if kkt <= eps:
            converged = True
            break

        H_T = np.zeros((N - 1, N - 1))
        for j in range(N - 1):
            Hu = _hessian_mv(x, A, c, U[:, j])
            H_T[:, j] = U.T @ Hu
        H_T = 0.5 * (H_T + H_T.T) + lambda_tikhonov * np.eye(N - 1)

        try:
            d_y = -np.linalg.solve(H_T, gbar)
        except np.linalg.LinAlgError:
            d_y = -gbar
        d = U @ d_y

        if g @ d > -1e-14:
            d_y = -gbar
            d = U @ d_y

        # Line search (shrink slightly to stay strictly interior, SE4)
        alpha_max = 0.99 * _max_step_to_boundary(x, d, tau)
        if alpha_max <= 1e-14:
            d_y = -gbar
            d = U @ d_y
            alpha_max = 0.99 * _max_step_to_boundary(x, d, tau)
            if alpha_max <= 1e-14:
                small_step_count += 1
                if small_step_count >= 5:
                    if verbose:
                        print(f"[YAND] boundary stuck at iter {k}; stopping.")
                    break
                continue

        alpha = _quartic_line_search(x, d, mu, A, c, alpha_max)
        x_new = x + alpha * d
        f_new = _mvsk_objective(x_new, mu, A, c)

        # If no descent, fallback to steepest reduced direction
        if alpha < 1e-14 or f_new >= f_now - 1e-15:
            d_y = -gbar
            d = U @ d_y
            alpha_max2 = 0.99 * _max_step_to_boundary(x, d, tau)
            if alpha_max2 <= 1e-14:
                small_step_count += 1
                if small_step_count >= 5:
                    break
                continue
            alpha = _quartic_line_search(x, d, mu, A, c, alpha_max2)
            x_new = x + alpha * d
            if alpha < 1e-14:
                small_step_count += 1
                if small_step_count >= 5:
                    break
                continue

        small_step_count = 0
        x = np.maximum(x_new, tau * 0.5)
        x = x / x.sum()

    return YANDResult(
        x=x,
        history=history,
        converged=converged,
        iters=len(history),
        final_kkt=history[-1]["kkt"],
        objective=history[-1]["f"],
    )


if __name__ == "__main__":
    from data_loader import generate_synthetic_returns
    R, tickers = generate_synthetic_returns()
    res = yand_mvsk(R, verbose=True)
    print(f"\nConverged: {res.converged} in {res.iters} iters")
    print(f"Final objective: {res.objective:+.6e}")
    print(f"Weights: {np.round(res.x, 4).tolist()}")
