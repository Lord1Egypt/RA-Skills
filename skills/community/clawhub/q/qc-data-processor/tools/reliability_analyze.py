import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy.optimize import minimize
from scipy.special import gammaln
import warnings

warnings.filterwarnings("ignore")


def _benard_ranks(n: int) -> np.ndarray:
    return (np.arange(1, n + 1) - 0.3) / (n + 0.4)


def _weibull_loglik(params, t, c):
    beta, eta = params
    if beta <= 0 or eta <= 0:
        return 1e12
    ll = 0.0
    for ti, ci in zip(t, c):
        if ci == 1:
            ll += np.log(beta) - np.log(eta) + (beta - 1) * np.log(ti / eta) - (ti / eta) ** beta
        else:
            ll += -(ti / eta) ** beta
    return -ll


def _lognormal_loglik(params, t, c):
    mu, sigma = params
    if sigma <= 0:
        return 1e12
    ll = 0.0
    for ti, ci in zip(t, c):
        z = (np.log(ti) - mu) / sigma
        if ci == 1:
            ll += -np.log(sigma * ti) + norm.logpdf(z)
        else:
            ll += norm.logsf(z)
    return -ll


def _exponential_loglik(params, t, c):
    lam = params[0]
    if lam <= 0:
        return 1e12
    ll = 0.0
    for ti, ci in zip(t, c):
        if ci == 1:
            ll += np.log(lam) - lam * ti
        else:
            ll += -lam * ti
    return -ll


def _aicc(loglik: float, k: int, n: int) -> float:
    aic = 2 * k + 2 * loglik
    if n - k - 1 <= 0:
        return aic
    return aic + (2 * k * (k + 1)) / (n - k - 1)


def _fit_weibull_mle(t, c):
    n_events = int(np.sum(c))
    if n_events == 0:
        return None
    beta_init = 1.5
    eta_init = float(np.median(t[c == 1])) if n_events > 0 else float(np.mean(t))
    res = minimize(_weibull_loglik, x0=[beta_init, eta_init], args=(t, c), bounds=[(0.1, 20), (1e-6, None)], method="L-BFGS-B")
    if res.success:
        beta, eta = res.x
        ll = -res.fun
        aicc_val = _aicc(-ll, 2, len(t))
        try:
            hess_inv = res.hess_inv.todense() if hasattr(res.hess_inv, "todense") else res.hess_inv
            se = np.sqrt(np.diag(hess_inv))
            beta_se = se[0] if se[0] > 0 else beta * 0.2
            eta_se = se[1] if se[1] > 0 else eta * 0.2
        except Exception:
            beta_se, eta_se = beta * 0.2, eta * 0.2

        beta_ci = (max(0.1, beta - 1.96 * beta_se), beta + 1.96 * beta_se)
        eta_ci = (max(1e-6, eta - 1.96 * eta_se), eta + 1.96 * eta_se)
        return {"distribution": "Weibull", "beta": beta, "eta": eta, "loglik": ll, "aicc": aicc_val,
                "beta_se": beta_se, "eta_se": eta_se, "beta_ci": beta_ci, "eta_ci": eta_ci,
                "params": [beta, eta]}
    return None


def _fit_lognormal_mle(t, c):
    n_events = int(np.sum(c))
    if n_events == 0:
        return None
    log_t = np.log(t[c == 1])
    mu_init = float(np.mean(log_t))
    sigma_init = float(np.std(log_t)) if len(log_t) > 1 else 0.5
    res = minimize(_lognormal_loglik, x0=[mu_init, sigma_init], args=(t, c), bounds=[(None, None), (0.001, None)], method="L-BFGS-B")
    if res.success:
        mu, sigma = res.x
        ll = -res.fun
        aicc_val = _aicc(-ll, 2, len(t))
        try:
            hess_inv = res.hess_inv.todense() if hasattr(res.hess_inv, "todense") else res.hess_inv
            se = np.sqrt(np.diag(hess_inv))
            mu_se = se[0] if se[0] > 0 else mu * 0.1
            sigma_se = se[1] if se[1] > 0 else sigma * 0.1
        except Exception:
            mu_se, sigma_se = mu * 0.1, sigma * 0.1

        mu_ci = (mu - 1.96 * mu_se, mu + 1.96 * mu_se)
        sigma_ci = (max(0.001, sigma - 1.96 * sigma_se), sigma + 1.96 * sigma_se)
        return {"distribution": "Lognormal", "mu": mu, "sigma": sigma, "loglik": ll, "aicc": aicc_val,
                "mu_se": mu_se, "sigma_se": sigma_se, "mu_ci": mu_ci, "sigma_ci": sigma_ci,
                "params": [mu, sigma]}
    return None


def _fit_exponential_mle(t, c):
    n_events = int(np.sum(c))
    if n_events == 0:
        return None
    total_time = float(np.sum(t))
    lam = n_events / total_time if total_time > 0 else 0.001
    ll = 0.0
    for ti, ci in zip(t, c):
        if ci == 1:
            ll += np.log(lam) - lam * ti
        else:
            ll += -lam * ti
    aicc_val = _aicc(-ll, 1, len(t))
    lam_se = lam / np.sqrt(n_events) if n_events > 0 else lam * 0.2
    lam_ci = (max(1e-6, lam - 1.96 * lam_se), lam + 1.96 * lam_se)
    return {"distribution": "Exponential", "lambda": lam, "loglik": ll, "aicc": aicc_val,
            "lam_se": lam_se, "lam_ci": lam_ci, "params": [lam]}


def _compute_metrics_weibull(beta, eta, beta_se, eta_se):
    b10 = eta * (-np.log(0.9)) ** (1.0 / beta)
    b50 = eta * (-np.log(0.5)) ** (1.0 / beta)
    mttf = eta * np.exp(gammaln(1 + 1.0 / beta))

    b10_lo = eta * (-np.log(0.9)) ** (1.0 / (beta + 1.96 * beta_se))
    b10_hi = eta * (-np.log(0.9)) ** (1.0 / max(0.1, beta - 1.96 * beta_se))
    b50_lo = eta * (-np.log(0.5)) ** (1.0 / (beta + 1.96 * beta_se))
    b50_hi = eta * (-np.log(0.5)) ** (1.0 / max(0.1, beta - 1.96 * beta_se))

    if beta < 0.9:
        interp = "早期失效期（beta<1，失效率递减）"
    elif beta < 1.1:
        interp = "随机失效期（beta≈1，失效率恒定）"
    else:
        interp = "耗损失效期（beta>1，失效率递增）"

    return {
        "b10_life": round(b10, 2), "b10_ci": [round(b10_lo, 2), round(b10_hi, 2)],
        "b50_life": round(b50, 2), "b50_ci": [round(b50_lo, 2), round(b50_hi, 2)],
        "mttf": round(mttf, 2), "mtbf": round(mttf, 2),
        "beta_interpretation": interp,
    }


def _compute_metrics_lognormal(mu, sigma):
    mttf = np.exp(mu + sigma ** 2 / 2)
    b10 = np.exp(mu + norm.ppf(0.1) * sigma)
    b50 = np.exp(mu)
    b10_lo = np.exp((mu - 1.96 * sigma / np.sqrt(2)) + norm.ppf(0.1) * sigma)
    b10_hi = np.exp((mu + 1.96 * sigma / np.sqrt(2)) + norm.ppf(0.1) * sigma)
    b50_lo = np.exp(mu - 1.96 * sigma / np.sqrt(2))
    b50_hi = np.exp(mu + 1.96 * sigma / np.sqrt(2))
    return {
        "b10_life": round(b10, 2), "b10_ci": [round(b10_lo, 2), round(b10_hi, 2)],
        "b50_life": round(b50, 2), "b50_ci": [round(b50_lo, 2), round(b50_hi, 2)],
        "mttf": round(mttf, 2), "mtbf": round(mttf, 2),
        "beta_interpretation": "",
    }


def _compute_metrics_exponential(lam):
    mttf = 1.0 / lam
    b10 = -np.log(0.9) / lam
    b50 = -np.log(0.5) / lam
    return {
        "b10_life": round(b10, 2), "b10_ci": [round(b10 * 0.7, 2), round(b10 * 1.3, 2)],
        "b50_life": round(b50, 2), "b50_ci": [round(b50 * 0.7, 2), round(b50 * 1.3, 2)],
        "mttf": round(mttf, 2), "mtbf": round(mttf, 2),
        "beta_interpretation": "指数分布（beta=1，失效率恒定）",
    }


def _probability_plot_data_weibull(t, c, beta, eta):
    n = len(t)
    f_t = _benard_ranks(n)
    sorted_idx = np.argsort(t)
    sorted_t = t[sorted_idx]
    sorted_c = c[sorted_idx]

    pp_times = sorted_t.tolist()
    pp_censor = [int(x) for x in sorted_c]
    pp_benard = f_t.tolist()

    t_range = np.logspace(np.log10(max(1, min(t) * 0.5)), np.log10(max(t) * 1.2), 100)
    fit_f = 1 - np.exp(-(t_range / eta) ** beta)
    fit_line = [[float(x), float(y)] for x, y in zip(t_range, fit_f)]

    return {
        "times": pp_times,
        "censor": pp_censor,
        "benard_ranks": [round(x, 6) for x in pp_benard],
        "fit_line": fit_line,
        "ci_upper": [],
        "ci_lower": [],
    }


def _probability_plot_data_lognormal(t, c, mu, sigma):
    n = len(t)
    f_t = _benard_ranks(n)
    sorted_idx = np.argsort(t)
    sorted_t = t[sorted_idx]
    sorted_c = c[sorted_idx]

    pp_times = sorted_t.tolist()
    pp_censor = [int(x) for x in sorted_c]
    pp_benard = f_t.tolist()

    t_range = np.logspace(np.log10(max(1, min(t) * 0.5)), np.log10(max(t) * 1.2), 100)
    fit_f = norm.cdf((np.log(t_range) - mu) / sigma)
    fit_line = [[float(x), float(y)] for x, y in zip(t_range, fit_f)]

    return {
        "times": pp_times,
        "censor": pp_censor,
        "benard_ranks": [round(x, 6) for x in pp_benard],
        "fit_line": fit_line,
        "ci_upper": [],
        "ci_lower": [],
    }


def qc_reliability_analyze(data_schema: dict, time_column: str, censor_column: str, distribution: str = "auto") -> dict:
    file_path = data_schema.get("_file_path")
    if not file_path:
        return {"error": "Cannot access original data file. Provide _file_path in data_schema."}

    df = pd.read_csv(file_path) if file_path.endswith(".csv") else pd.read_excel(file_path)

    if time_column not in df.columns or censor_column not in df.columns:
        return {"error": f"Columns {time_column} or {censor_column} not found in data."}

    t = df[time_column].values.astype(float)
    c = df[censor_column].values.astype(float)

    n = len(t)
    n_failures = int(np.sum(c))

    if n_failures == 0:
        return {"error": "All samples are censored. Cannot fit any distribution."}

    small_sample_warning = "样本量过小（n<5），置信区间极宽" if n < 5 else None

    fits = {}
    if distribution in ("auto", "Weibull"):
        w = _fit_weibull_mle(t, c)
        if w:
            fits["Weibull"] = w
    if distribution in ("auto", "Lognormal"):
        ln = _fit_lognormal_mle(t, c)
        if ln:
            fits["Lognormal"] = ln
    if distribution in ("auto", "Exponential"):
        e = _fit_exponential_mle(t, c)
        if e:
            fits["Exponential"] = e

    if not fits:
        return {"error": "Failed to fit any distribution to the data."}

    best_name = min(fits.keys(), key=lambda k: fits[k]["aicc"])
    best = fits[best_name]

    aicc_comp = {k: round(v["aicc"], 2) for k, v in fits.items()}

    parameters = {}
    metrics = {}
    pp_data = {}

    if best_name == "Weibull":
        parameters = {
            "beta": round(best["beta"], 4),
            "eta": round(best["eta"], 4),
            "beta_ci_lower": round(best["beta_ci"][0], 4),
            "beta_ci_upper": round(best["beta_ci"][1], 4),
            "eta_ci_lower": round(best["eta_ci"][0], 4),
            "eta_ci_upper": round(best["eta_ci"][1], 4),
        }
        metrics = _compute_metrics_weibull(best["beta"], best["eta"], best["beta_se"], best["eta_se"])
        parameters["beta_interpretation"] = metrics["beta_interpretation"]
        pp_data = _probability_plot_data_weibull(t, c, best["beta"], best["eta"])
    elif best_name == "Lognormal":
        parameters = {
            "mu": round(best["mu"], 4),
            "sigma": round(best["sigma"], 4),
            "mu_ci_lower": round(best["mu_ci"][0], 4),
            "mu_ci_upper": round(best["mu_ci"][1], 4),
            "sigma_ci_lower": round(best["sigma_ci"][0], 4),
            "sigma_ci_upper": round(best["sigma_ci"][1], 4),
        }
        metrics = _compute_metrics_lognormal(best["mu"], best["sigma"])
        parameters["beta_interpretation"] = ""
        pp_data = _probability_plot_data_lognormal(t, c, best["mu"], best["sigma"])
    elif best_name == "Exponential":
        parameters = {
            "lambda": round(best["lambda"], 6),
            "lambda_ci_lower": round(best["lam_ci"][0], 6),
            "lambda_ci_upper": round(best["lam_ci"][1], 6),
        }
        metrics = _compute_metrics_exponential(best["lambda"])
        parameters["beta_interpretation"] = metrics["beta_interpretation"]
        pp_data = _probability_plot_data_weibull(t, c, 1.0, 1.0 / best["lambda"])

    result = {
        "best_fit": best_name,
        "aicc_comparison": aicc_comp,
        "parameters": parameters,
        "metrics": metrics,
        "probability_plot_data": pp_data,
        "n_samples": n,
        "n_failures": n_failures,
    }

    if small_sample_warning:
        result["warning"] = small_sample_warning

    return result
