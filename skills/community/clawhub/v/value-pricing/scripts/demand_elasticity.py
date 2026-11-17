"""Estimate segment-level transaction quantity price elasticities with a Bayesian model.

Input is a CSV with date, product, customer, segment, realised_unit_price, and
quantity. Optional promotion, channel, and contract_duration columns are used
as controls. The model is a hierarchical zero-truncated negative-binomial regression with
partial pooling of segment price slopes and customer intercepts.

  demand_elasticity.py --study S [--csv transactions.csv] [--warmup 800] [--samples 1000]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import jax
    import jax.numpy as jnp
    import numpy as np
    import pandas as pd
    import numpyro
    import numpyro.distributions as dist
    from numpyro.infer import MCMC, NUTS
    from numpyro.diagnostics import summary as diagnostics_summary
except ImportError as exc:  # pragma: no cover - depends on the selected environment
    raise SystemExit(
        "demand_elasticity.py needs the analysis dependencies plus optional "
        "numpyro and jax; install scripts/requirements.txt"
    ) from exc

from common import Study, merge_summary, study_arg

REQUIRED = ("date", "product", "customer", "segment", "realised_unit_price", "quantity")
OPTIONAL = ("promotion", "channel", "contract_duration")


def load_transactions(path: Path) -> tuple[pd.DataFrame, dict]:
    raw = pd.read_csv(path)
    missing_columns = [c for c in REQUIRED if c not in raw.columns]
    if missing_columns:
        raise ValueError("CSV is missing required columns: " + ", ".join(missing_columns))
    d = raw.copy()
    d["date"] = pd.to_datetime(d["date"], errors="coerce", utc=True)
    for c in ("realised_unit_price", "quantity", "contract_duration", "promotion"):
        if c in d:
            d[c] = pd.to_numeric(d[c], errors="coerce")
    d["product"] = d["product"].astype("string").str.strip()
    d["customer"] = d["customer"].astype("string").str.strip()
    d["segment"] = d["segment"].astype("string").str.strip()
    required_mask = d[list(REQUIRED)].notna().all(axis=1)
    required_mask &= d["product"].ne("") & d["customer"].ne("") & d["segment"].ne("")
    valid_domain = ((d["realised_unit_price"] > 0) & (d["quantity"] > 0)
                    & np.isclose(d["quantity"], np.round(d["quantity"]), equal_nan=False))
    valid = required_mask & valid_domain
    counts = {
        "rows_received": int(len(raw)),
        "rows_used": int(valid.sum()),
        "rows_dropped_missing_or_invalid": int((~valid).sum()),
        "rows_missing_required_values": int((~required_mask).sum()),
        "rows_with_invalid_price_or_quantity": int((required_mask & ~valid_domain).sum()),
        "missing_optional_fields": [c for c in OPTIONAL if c not in d.columns],
        "optional_field_missing_values": {c: int(d[c].isna().sum()) for c in OPTIONAL if c in d.columns},
    }
    d = d.loc[valid].copy()
    if d.empty:
        raise ValueError("No valid transaction rows remain after date, ID, price, and quantity validation")
    return d, counts


def design_controls(d: pd.DataFrame) -> tuple[np.ndarray, list[str], dict]:
    """Build bounded, interpretable controls; reference categories are alphabetical."""
    pieces, names = [], []
    meta = {"optional_field_missing_values": {c: int(d[c].isna().sum()) for c in OPTIONAL if c in d.columns}}
    if "promotion" in d and d["promotion"].notna().any():
        x = d["promotion"].fillna(d["promotion"].median()).to_numpy(float)
        # Promotions are usually indicators; preserve their 0/1 scale when possible.
        if set(np.unique(x)).issubset({0.0, 1.0}):
            pieces.append(x[:, None]); names.append("promotion")
        else:
            sd = float(np.std(x))
            if sd > 0:
                pieces.append(((x - x.mean()) / sd)[:, None]); names.append("promotion_standardized")
        meta["promotion_missing_filled"] = int(d["promotion"].isna().sum())
    if "contract_duration" in d and d["contract_duration"].notna().any():
        x = d["contract_duration"].fillna(d["contract_duration"].median()).to_numpy(float)
        sd = float(np.std(x))
        if sd > 0:
            pieces.append(((x - x.mean()) / sd)[:, None]); names.append("contract_duration_standardized")
        meta["contract_duration_missing_filled"] = int(d["contract_duration"].isna().sum())
    if "channel" in d and d["channel"].notna().any():
        values = d["channel"].fillna("unknown").astype(str)
        levels = sorted(values.unique())
        for level in levels[1:]:
            pieces.append((values.to_numpy() == level).astype(float)[:, None])
            names.append(f"channel[{level}]")
        meta["channel_reference"] = levels[0]
        meta["channel_levels"] = levels
        meta["channel_missing_filled"] = int(d["channel"].isna().sum())
    month = d["date"].dt.month.to_numpy(float)
    pieces.extend([np.sin(2 * np.pi * (month - 1) / 12)[:, None],
                   np.cos(2 * np.pi * (month - 1) / 12)[:, None]])
    names.extend(["season_sin_annual", "season_cos_annual"])
    return np.concatenate(pieces, axis=1), names, meta


def price_variation_diagnostics(d: pd.DataFrame) -> dict:
    """Report overall and segment price support before fitting."""
    by_segment = {}
    for seg in sorted(d["segment"].astype(str).unique()):
        mask = d["segment"].astype(str) == seg
        q = d.loc[mask, "realised_unit_price"]
        by_segment[seg] = {"n_rows": int(len(q)),
                           "n_customers": int(d.loc[mask, "customer"].nunique()),
                           "n_unique_prices": int(q.nunique()),
                           "log_price_sd": float(np.std(np.log(q.to_numpy(float))))}
    prices = d["realised_unit_price"].to_numpy(float)
    return {"n_unique_prices": int(d["realised_unit_price"].nunique()),
            "log_price_sd": float(np.std(np.log(prices))), "by_segment": by_segment}


def price_control_diagnostics(log_price: np.ndarray, X: np.ndarray, names: list[str]) -> dict:
    """Flag measured price/control correlations; this is not a test for endogeneity."""
    correlations = {}
    price_sd = float(np.std(log_price))
    for i, name in enumerate(names):
        x = X[:, i]
        correlations[name] = (float(np.corrcoef(log_price, x)[0, 1])
                              if price_sd > 1e-12 and np.std(x) > 1e-12 else None)
    high = [{"control": name, "correlation": corr}
            for name, corr in correlations.items() if corr is not None and abs(corr) >= 0.8]
    predictors = np.column_stack([log_price, X])
    spread = np.std(predictors, axis=0)
    predictors = predictors[:, spread > 1e-12]
    predictors = (predictors - predictors.mean(axis=0)) / np.std(predictors, axis=0)
    raw_condition = float(np.linalg.cond(predictors)) if predictors.shape[1] else None
    condition = raw_condition if raw_condition is not None and np.isfinite(raw_condition) else None
    return {"price_control_correlations": correlations, "high_correlation_threshold": 0.8,
            "high_price_control_correlations": high, "standardized_predictor_condition_number": condition,
            "condition_number_nonfinite": raw_condition is not None and not np.isfinite(raw_condition),
            "interpretation": "Measured overlap can flag confounding or weak separation; these diagnostics do not establish price exogeneity or remove unmeasured confounding."}


def _model(y, log_price, X, segment_idx, customer_idx, n_segments, n_customers):
    n, k = X.shape
    alpha = numpyro.sample("alpha", dist.Normal(0.0, 2.0))
    sigma_segment_intercept = numpyro.sample("sigma_segment_intercept", dist.HalfNormal(0.5))
    alpha_segment = alpha + sigma_segment_intercept * numpyro.sample(
        "z_segment_intercept", dist.Normal(jnp.zeros(n_segments), 1.0)
    )
    numpyro.deterministic("alpha_segment", alpha_segment)
    beta_price = numpyro.sample("beta_price", dist.Normal(0.0, 1.0))
    sigma_segment_slope = numpyro.sample("sigma_segment_slope", dist.HalfNormal(0.35))
    beta_segment = beta_price + sigma_segment_slope * numpyro.sample(
        "z_segment_slope", dist.Normal(jnp.zeros(n_segments), 1.0)
    )
    numpyro.deterministic("beta_segment", beta_segment)
    beta_controls = numpyro.sample("beta_controls", dist.Normal(jnp.zeros(k), 0.5))
    sigma_customer = numpyro.sample("sigma_customer", dist.HalfNormal(0.5))
    customer_effect = sigma_customer * numpyro.sample(
        "z_customer", dist.Normal(jnp.zeros(n_customers), 1.0)
    )
    log_concentration = numpyro.sample("log_concentration", dist.Normal(1.4, 0.7))
    eta = (alpha_segment[segment_idx] + beta_segment[segment_idx] * log_price
           + X @ beta_controls + customer_effect[customer_idx])
    mean = jnp.exp(jnp.clip(eta, -15, 15))
    concentration = jnp.exp(log_concentration)
    likelihood = dist.NegativeBinomial2(mean=mean, concentration=concentration)
    # The CSV contains transactions, so quantity is positive by construction.
    # Condition the likelihood on a positive count rather than pretending zero-sale
    # periods were observed; this still cannot estimate purchase incidence.
    log_p_zero = concentration * (jnp.log(concentration) - jnp.log(concentration + mean))
    numpyro.factor("positive_quantity_truncation", -jnp.sum(jnp.log1p(-jnp.exp(log_p_zero))))
    numpyro.sample("quantity", likelihood, obs=y)


def posterior_predictive_check(draws: dict, y: np.ndarray, log_price: np.ndarray, X: np.ndarray,
                               segment_idx: np.ndarray, customer_idx: np.ndarray, seed: int,
                               max_draws: int = 160) -> dict:
    """Replicate positive transaction quantities under posterior draws and compare moments."""
    flat = {k: np.asarray(v).reshape((-1,) + np.asarray(v).shape[2:]) for k, v in draws.items()}
    total = len(flat["beta_price"])
    rng = np.random.default_rng(seed)
    chosen = rng.choice(total, size=min(max_draws, total), replace=False)
    rep = np.empty((len(chosen), len(y)), dtype=float)
    for row, draw_i in enumerate(chosen):
        eta = (flat["alpha_segment"][draw_i, segment_idx]
               + flat["beta_segment"][draw_i, segment_idx] * log_price
               + X @ flat["beta_controls"][draw_i]
               + flat["sigma_customer"][draw_i] * flat["z_customer"][draw_i, customer_idx])
        mu = np.exp(np.clip(eta, -15, 15))
        concentration = np.exp(flat["log_concentration"][draw_i])
        lam = rng.gamma(shape=concentration, scale=mu / concentration)
        simulated = rng.poisson(lam)
        zero = simulated == 0
        attempts = 0
        while np.any(zero) and attempts < 20:
            lam_new = rng.gamma(shape=concentration, scale=mu[zero] / concentration)
            simulated[zero] = rng.poisson(lam_new)
            zero = simulated == 0
            attempts += 1
        if np.any(zero):
            # A positive count is guaranteed by the transaction-row likelihood.
            simulated[zero] = 1
        rep[row] = simulated
    obs_quantiles = np.quantile(y, [0.5, 0.9]).tolist()
    rep_means = rep.mean(axis=1)
    rep_medians = np.median(rep, axis=1)
    rep_p90 = np.quantile(rep, 0.9, axis=1)
    mean_ci = np.quantile(rep_means, [0.05, 0.95]).tolist()
    median_ci = np.quantile(rep_medians, [0.05, 0.95]).tolist()
    p90_ci = np.quantile(rep_p90, [0.05, 0.95]).tolist()
    return {"replicated_draws": int(len(chosen)), "observed_mean": float(np.mean(y)),
            "observed_median": float(obs_quantiles[0]), "observed_p90": float(obs_quantiles[1]),
            "replicated_mean_ci90": mean_ci, "replicated_median_ci90": median_ci,
            "replicated_p90_ci90": p90_ci,
            "observed_mean_inside_rep_ci90": bool(mean_ci[0] <= np.mean(y) <= mean_ci[1]),
            "observed_median_inside_rep_ci90": bool(median_ci[0] <= obs_quantiles[0] <= median_ci[1]),
            "observed_p90_inside_rep_ci90": bool(p90_ci[0] <= obs_quantiles[1] <= p90_ci[1]),
            "interpretation": "Posterior predictive checks compare the positive transaction quantities modeled here; they do not test purchase incidence or causal identification."}


def fit_product(d: pd.DataFrame, warmup: int, samples: int, chains: int, seed: int) -> dict:
    d = d.copy().reset_index(drop=True)
    segments = sorted(d["segment"].astype(str).unique())
    customers = sorted(d["customer"].astype(str).unique())
    seg_idx = pd.Categorical(d["segment"].astype(str), categories=segments).codes
    cust_idx = pd.Categorical(d["customer"].astype(str), categories=customers).codes
    log_price = np.log(d["realised_unit_price"].to_numpy(float))
    log_price -= log_price.mean()
    X, control_names, control_meta = design_controls(d)
    price_support = price_variation_diagnostics(d)
    variation = price_support["by_segment"]
    overall_unique = price_support["n_unique_prices"]
    overall_sd = price_support["log_price_sd"]
    confounding = price_control_diagnostics(log_price, X, control_names)
    if overall_unique < 3 or overall_sd < 0.03:
        return {"status": "insufficient_price_variation", "n_rows": int(len(d)), "n_customers": len(customers),
                "n_segments": len(segments), "price_variation": price_support,
                "confounding_diagnostics": confounding, "estimates": [], "diagnostics": {"converged": False,
                "warning": "At least three distinct prices and log-price SD >= 0.03 are required."}}
    kernel = NUTS(_model, target_accept_prob=0.99, max_tree_depth=8)
    mcmc = MCMC(kernel, num_warmup=warmup, num_samples=samples, num_chains=chains,
                chain_method="sequential", progress_bar=False)
    mcmc.run(jax.random.PRNGKey(seed), d["quantity"].to_numpy(float), log_price, X,
             seg_idx, cust_idx, len(segments), len(customers))
    draws = mcmc.get_samples(group_by_chain=True)
    diag = diagnostics_summary(draws, group_by_chain=True)
    divergences = int(np.asarray(mcmc.get_extra_fields(group_by_chain=True)["diverging"]).sum())
    beta_draws = np.asarray(draws["beta_segment"]).reshape(-1, len(segments))
    alpha_draws = np.asarray(draws["alpha_segment"]).reshape(-1, len(segments))
    concentration_draws = np.exp(np.asarray(draws["log_concentration"]).reshape(-1))
    ppc = posterior_predictive_check(draws, d["quantity"].to_numpy(float), log_price, X,
                                     seg_idx, cust_idx, seed + 1000)
    # Posterior expected transaction quantity at median price and reference controls.
    ref_price = float(np.exp(np.mean(np.log(d["realised_unit_price"].to_numpy(float)))))
    estimates = []
    for i, seg in enumerate(segments):
        el = beta_draws[:, i]
        # Predict a typical customer at average controls, conditional on a positive transaction.
        latent_mu = np.exp(np.clip(alpha_draws[:, i], -15, 15))
        base_p0 = (concentration_draws / (concentration_draws + latent_mu)) ** concentration_draws
        base_mu = latent_mu / np.maximum(1 - base_p0, 1e-12)
        scenario_rows = []
        for factor in (0.8, 1.0, 1.2):
            scenario_latent_mu = latent_mu * np.exp(el * np.log(factor))
            scenario_p0 = (concentration_draws / (concentration_draws + scenario_latent_mu)) ** concentration_draws
            quantity_mean = scenario_latent_mu / np.maximum(1 - scenario_p0, 1e-12)
            scenario_rows.append({"price_factor": factor, "price": ref_price * factor,
                                  "expected_quantity": float(np.median(quantity_mean)),
                                  "expected_quantity_ci90": np.quantile(quantity_mean, [0.05, 0.95]).tolist(),
                                  "quantity_change_pct": float(100 * (np.median(quantity_mean) / np.median(base_mu) - 1))})
        estimates.append({"segment": seg, "elasticity": float(np.median(el)),
                          "ci90": np.quantile(el, [0.05, 0.95]).tolist(), "n_rows": variation[seg]["n_rows"],
                          "n_customers": variation[seg]["n_customers"], "price_variation_sufficient":
                          variation[seg]["n_unique_prices"] >= 3 and variation[seg]["log_price_sd"] >= 0.03,
                          "scenarios": scenario_rows})
    rhat = np.concatenate([np.asarray(v["r_hat"], dtype=float).reshape(-1) for v in diag.values()])
    ess = np.concatenate([np.asarray(v["n_eff"], dtype=float).reshape(-1) for v in diag.values()])
    finite_rhat, finite_ess = rhat[np.isfinite(rhat)], ess[np.isfinite(ess)]
    rhat_max = float(finite_rhat.max()) if len(finite_rhat) else None
    ess_min = float(finite_ess.min()) if len(finite_ess) else None
    convergence = {"rhat_max": rhat_max, "ess_min": ess_min, "divergences": divergences,
                   "converged": bool(divergences == 0 and len(finite_rhat) == len(rhat)
                                     and np.all(finite_rhat <= 1.05) and ess_min is not None and ess_min >= 100)}
    return {"status": "ok", "n_rows": int(len(d)), "n_customers": len(customers), "n_segments": len(segments),
            "price_variation": price_support, "confounding_diagnostics": confounding,
            "controls": control_meta, "control_coefficients": {name: float(np.median(np.asarray(draws["beta_controls"])[..., i]))
                                                                  for i, name in enumerate(control_names)},
            "estimates": estimates, "diagnostics": convergence,
            "model_fit": {"posterior_predictive_check": ppc}}


def main():
    ap = study_arg(__doc__.splitlines()[0])
    ap.add_argument("--csv", help="transaction CSV; defaults to <study>/demand/data/transactions.csv")
    ap.add_argument("--warmup", type=int, default=800)
    ap.add_argument("--samples", type=int, default=1000)
    ap.add_argument("--chains", type=int, default=4)
    ap.add_argument("--seed", type=int, default=29)
    a = ap.parse_args()
    if min(a.warmup, a.samples, a.chains) < 1:
        ap.error("--warmup, --samples, and --chains must be positive")
    st = Study(a.study)
    csv_path = Path(a.csv).expanduser().resolve() if a.csv else st.root / "demand/data/transactions.csv"
    if not csv_path.exists():
        raise SystemExit(f"Transaction CSV not found: {csv_path}")
    try:
        data, counts = load_transactions(csv_path)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    products = {}
    for i, (product, group) in enumerate(data.groupby("product", sort=True)):
        products[str(product)] = fit_product(group, a.warmup, a.samples, a.chains, a.seed + i)
    gaps = []
    for product, result in products.items():
        if result["status"] != "ok":
            gaps.append({"what": f"{product} elasticity", "why": "insufficient price variation", "blocked_on": "data"})
        elif not result["diagnostics"]["converged"]:
            gaps.append({"what": f"{product} posterior diagnostics", "why": "convergence criteria not met; treat estimates as provisional", "blocked_on": None})
        for estimate in result.get("estimates", []):
            if not estimate.get("price_variation_sufficient", False):
                gaps.append({"what": f"{product}/{estimate['segment']} elasticity",
                             "why": "segment price variation is insufficient; partial pooling does not supply segment-specific identification",
                             "blocked_on": "data"})
    assumptions = [
        "The outcome is transaction quantity conditional on an observed transaction; without customer-period rows including zero purchases or exposure, this is not purchase incidence or total market demand.",
        "Realised prices are denominated in the study currency per unit; no FX conversion is applied.",
        "A zero-truncated negative-binomial log-link is adequate for positive transaction quantity conditional on observed covariates.",
        "Segment price slopes are exchangeable around a common population slope, enabling partial pooling.",
        "The estimates are observational associations unless price variation comes from a defensible randomized or quasi-experimental design; included controls do not by themselves remove price endogeneity.",
        "Price scenarios are model-based associations holding included controls and the transaction composition fixed.",
    ]
    merge_summary(st, "demand", {"demand_elasticity": {"status": "observational", "input": str(csv_path),
                "input_validation": counts, "price_currency": st.cfg.get("currency", "EUR"),
                "model": "hierarchical zero-truncated negative-binomial regression with segment-varying price slopes, customer intercepts, annual seasonality, and available controls",
                "interval": "90% posterior credible interval", "price_scenarios": [0.8, 1.0, 1.2],
                "products": products, "assumptions": assumptions,
                "identification": {"causal": False,
                                    "statement": "Observational transaction-price/quantity association; causal interpretation requires justified exogenous price variation and an explicit design.",
                                    "price_endogeneity_risk": "Prices may respond to expected demand or customer value; this CSV model cannot rule that out.",
                                    "available_design_metadata": ("promotion", "channel", "contract_duration")}},
                "input_csv": str(csv_path)}, assumptions, gaps)
    print(json.dumps(products, indent=2, allow_nan=False))
    print(f"Demand elasticity summary written under {st.root / 'demand/results/summary.json'}")


if __name__ == "__main__":
    main()
