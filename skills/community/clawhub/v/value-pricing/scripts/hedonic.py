"""Phase 2 · hedonic model of the market and the implied price of our feature vector, per segment.

Inputs (under <study>/market/data/):
  vendors.csv          vendor, tier (direct|adjacent), category, optional target_customer, numeric ctl_* controls.
                       A row with vendor "__ours__" supplies our own controls (else corpus medians).
  plans.csv            plan cards (templates/plans.csv); reference prices are built from them unless
                       reference_prices.csv already exists.
  vendor_features.csv  vendor + one 0/1 column per taxonomy id (code_features.py collect)
  kappa.csv            optional; ids with drop=True are excluded
Our vector: taxonomy.yaml `ours` (yes = 1; --with-partial also counts partial).

Spec: log(reference price) ~ features + category FE + controls. Lasso selects features (controls and FE
always kept); post-double-selection (Belloni, Chernozhukov & Hansen 2014) gives honest 90% CIs per feature;
HC3 errors; a 20% holdout gives out-of-sample R² and MAPE. Our price per segment three ways: OLS on the
selected spec, lasso shrinkage with out-of-fold residual intervals, and coverage neighbours (the K priced
vendors covering most of our features). Writes market/data/{reference_prices,coefficients,implied_price,
nearest_competitors}.csv and market/results/summary.json.

  hedonic.py --study S [--with-partial] [--direct-only] [--neighbours 15]
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LassoCV
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler

from common import Study, merge_summary, status, study_arg

warnings.filterwarnings("ignore")
SEED = 20261021
MIN_PREV = 0.02
MIN_CLUSTER = 15


def flag(df: pd.DataFrame, col: str) -> pd.Series:
    return df[col].fillna(0).astype(int).astype(bool) if col in df else pd.Series(False, index=df.index)


def is_direct(s: pd.Series) -> pd.Series:
    return s.astype(str).str.lower().str.startswith(("direct", "10"))


# ------------------------------------------------------------------ reference prices from plan cards
def monthly(row, fx: dict, cur: str) -> float:
    p = float(row["price"])
    if str(row.get("period") or "month").lower().startswith("y"):
        p /= 12
    c = str(row.get("currency") or cur).upper()
    if c in ("NAN", "NONE", ""):
        c = cur
    if c != cur:
        if c not in fx:
            raise SystemExit(f"no fx rate for {c}: add it to study.yaml fx (1 {c} = x {cur})")
        p *= float(fx[c])
    return p


def reference_prices(st: Study, plans: pd.DataFrame) -> pd.DataFrame:
    cur = st.cfg.get("currency", "EUR")
    fx = {k: v for k, v in (st.cfg.get("fx") or {}).items() if k != "date"}
    axis = f"limit_{st.cfg['segments']['axis']}"
    rows = []
    for v, g in plans.groupby("vendor"):
        quote, free_f, rec_f = flag(g, "is_quote"), flag(g, "is_free"), flag(g, "is_recommended")
        eur = pd.Series([monthly(r, fx, cur) if pd.notna(r["price"]) and not q else np.nan for (_, r), q in zip(g.iterrows(), quote)], index=g.index)
        paid = g.assign(eur=eur)[eur > 0].sort_values("eur")
        free = g[(eur == 0) | free_f]
        state = "priced" if len(paid) else "free_only" if len(free) else "quote_only" if quote.any() else "undisclosed"
        rec = {"vendor": v, "price_state": state, "n_paid_plans": len(paid), "has_free_plan": bool(len(free)), "has_quote_plan": bool(quote.any())}
        if len(paid):
            recd = paid[rec_f.loc[paid.index]]
            main = recd.iloc[0] if len(recd) else paid.iloc[(len(paid) - 1) // 2]
            rec["ref_main"], rec["ref_cheapest"] = main.eur, paid.eur.iloc[0]
            scaled = axis in paid and pd.to_numeric(paid[axis], errors="coerce").notna().any()
            rec["scales_on_axis"] = bool(scaled)
            for b in st.bands:
                if scaled:
                    lim = pd.to_numeric(paid[axis], errors="coerce").fillna(np.inf)
                    ok = paid[lim >= b["reference_volume"]]
                    rec[f"ref_{b['id']}"] = ok.eur.iloc[0] if len(ok) else paid.eur.iloc[-1]
                    rec[f"ref_{b['id']}_exceeds_top"] = not len(ok)
                else:
                    rec[f"ref_{b['id']}"], rec[f"ref_{b['id']}_exceeds_top"] = main.eur, False
        rows.append(rec)
    return pd.DataFrame(rows).set_index("vendor")


# ------------------------------------------------------------------ design matrix
def design(vendors: pd.DataFrame, feats: pd.DataFrame, ref: pd.DataFrame, fids: list[str]):
    idx = vendors.index.intersection(feats.index)
    X = pd.DataFrame(index=idx)
    ctl = [c for c in vendors.columns if c.startswith("ctl_")]
    for c in ctl:
        X[c] = pd.to_numeric(vendors.loc[idx, c], errors="coerce").fillna(pd.to_numeric(vendors[c], errors="coerce").median())
    X["direct"] = is_direct(vendors.loc[idx, "tier"]).astype(int) if "tier" in vendors else 0
    controls = ctl + ["direct"]
    if "target_customer" in vendors:
        tc = vendors.loc[idx, "target_customer"].fillna("unclear").astype(str)
        for t in tc.value_counts().index[1:]:
            X[f"tc_{t}"] = tc.eq(t).astype(int)
            controls.append(f"tc_{t}")
    r = ref.reindex(idx)
    X["free_plan"] = r["has_free_plan"].fillna(False).astype(int)
    X["quote_tier"] = r["has_quote_plan"].fillna(False).astype(int)
    controls += ["free_plan", "quote_tier"]
    fe = []
    if "category" in vendors:
        cat = vendors.loc[idx, "category"].fillna("other").astype(str)
        cat = cat.where(cat.map(cat.value_counts()) >= MIN_CLUSTER, "other")
        for c in sorted(set(cat) - {cat.value_counts().index[0]}):
            X[f"cat_{c}"] = cat.eq(c).astype(int)
            fe.append(f"cat_{c}")
    fcols = []
    for f in fids:
        if f in feats:
            X[f"f_{f}"] = feats.loc[idx, f].astype(int)
            fcols.append(f"f_{f}")
    return X, controls, fe, fcols


def lasso_select(X, y, cols):
    cols = [c for c in cols if X[c].std() > 0]
    if not cols or len(y) < 20:
        return cols
    Z = StandardScaler().fit_transform(X[cols].astype(float))
    m = LassoCV(cv=5, random_state=SEED, max_iter=50000).fit(Z, y)
    return [c for c, b in zip(cols, m.coef_) if abs(b) > 1e-8]


def ols(X, y, cols):
    cols = [c for c in dict.fromkeys(cols) if X[c].std() > 0]
    return sm.OLS(y, sm.add_constant(X[cols].astype(float), has_constant="add")).fit(cov_type="HC3"), cols


def pds(X, y, target, always, pool):
    others = [c for c in pool if c != target]
    s1, s2 = lasso_select(X, y, others), lasso_select(X, X[target].astype(float), others)
    fit, _ = ols(X, y, [target] + always + s1 + s2)
    b, se = fit.params[target], fit.bse[target]
    return {"coef": float(b), "se": float(se), "ci90": [float(b - 1.645 * se), float(b + 1.645 * se)],
            "pct_price_effect": float(np.exp(b) - 1), "p": float(fit.pvalues[target])}


def predict(fit, row):
    xr = sm.add_constant(pd.DataFrame([row]), has_constant="add").reindex(columns=fit.params.index, fill_value=0).astype(float)
    pr = fit.get_prediction(xr).summary_frame(alpha=0.10)
    return float(np.exp(pr["mean"].iloc[0])), [float(np.exp(pr["obs_ci_lower"].iloc[0])), float(np.exp(pr["obs_ci_upper"].iloc[0]))]


def lasso_pred(X, y, cols, row):
    cols = [c for c in cols if X[c].std() > 0]
    sc = StandardScaler().fit(X[cols].astype(float))
    Z = sc.transform(X[cols].astype(float))
    m = LassoCV(cv=5, random_state=SEED, max_iter=50000).fit(Z, y)
    res = []
    for tr, te in KFold(5, shuffle=True, random_state=SEED).split(Z):
        mm = LassoCV(cv=5, random_state=SEED, max_iter=50000).fit(Z[tr], y.iloc[tr])
        res += list(y.iloc[te] - mm.predict(Z[te]))
    pt = float(m.predict(sc.transform(pd.DataFrame([row[cols].astype(float)])))[0])
    lo, hi = np.quantile(res, [0.05, 0.95])
    return float(np.exp(pt)), [float(np.exp(pt + lo)), float(np.exp(pt + hi))]


def main():
    ap = study_arg(__doc__.splitlines()[0])
    ap.add_argument("--with-partial", action="store_true", help="count partial features as present in our vector")
    ap.add_argument("--neighbours", type=int, default=15)
    ap.add_argument("--direct-only", action="store_true", help="robustness: direct competitors only")
    a = ap.parse_args()
    st = Study(a.study)
    D = st.root / "market" / "data"
    tax = st.yaml("taxonomy.yaml")
    fids = [f["id"] for f in tax["features"] if not f.get("deprecated")]
    ours = {f["id"]: status(f.get("ours", "no")) for f in tax["features"]}
    vendors = pd.read_csv(D / "vendors.csv").set_index("vendor")
    feats = pd.read_csv(D / "vendor_features.csv").set_index("vendor")
    if (D / "reference_prices.csv").exists():
        ref = pd.read_csv(D / "reference_prices.csv").set_index("vendor")
    else:
        ref = reference_prices(st, pd.read_csv(D / "plans.csv"))
        ref.to_csv(D / "reference_prices.csv")
    dropped = []
    if (D / "kappa.csv").exists():
        k = pd.read_csv(D / "kappa.csv")
        dropped = k.loc[k["drop"].astype(bool), "feature_id"].tolist()
    ours_ctl = vendors.loc["__ours__"] if "__ours__" in vendors.index else None
    vendors = vendors.drop(index="__ours__", errors="ignore")
    feats = feats.drop(index="__ours__", errors="ignore")
    if a.direct_only and "tier" in vendors:
        vendors = vendors[is_direct(vendors.tier)]
    for feature in fids:
        for suffix in ("__unclear", "__missing"):
            flag_column = feature + suffix
            if feature in feats and flag_column in feats:
                feats.loc[feats[flag_column].fillna(0).astype(bool), feature] = np.nan
    unresolved = feats.reindex(vendors.index.drop("__ours__", errors="ignore")).reindex(columns=fids).isna()
    if unresolved.any(axis=None):
        n_rows = int(unresolved.any(axis=1).sum())
        n_cells = int(unresolved.sum().sum())
        raise SystemExit(
            f"{n_cells} competitor feature codings are unclear or missing across {n_rows} vendors. "
            "Resolve those cells from source evidence before fitting; unknown is not absence."
        )
    X, controls, fe, fcols_all = design(vendors, feats, ref, fids)
    priced = ref.index[(ref.get("price_state") == "priced") & (ref["ref_main"] > 0)].intersection(X.index)
    if len(priced) < 30:
        raise SystemExit(f"only {len(priced)} priced vendors: too few for a hedonic model (aim for 100+)")
    Xp = X.loc[priced]
    prev = Xp[fcols_all].mean()
    fcols = [c for c in fcols_all if prev[c] >= MIN_PREV and c[2:] not in dropped]
    y = np.log(ref.loc[priced, "ref_main"].astype(float))

    row = pd.Series(0.0, index=X.columns)
    for c in controls:
        if ours_ctl is not None and c in ours_ctl.index and pd.notna(ours_ctl[c]):
            row[c] = float(ours_ctl[c])
        elif c == "direct":
            row[c] = 1.0
        elif c.startswith("tc_") and ours_ctl is not None and "target_customer" in ours_ctl.index:
            row[c] = float(str(ours_ctl["target_customer"]) == c[3:])
        else:
            row[c] = float(Xp[c].median())
    if ours_ctl is not None and "category" in ours_ctl.index and f"cat_{ours_ctl['category']}" in row.index:
        row[f"cat_{ours_ctl['category']}"] = 1.0
    row["free_plan"], row["quote_tier"] = 0.0, 0.0
    ok = {"yes", "partial"} if a.with_partial else {"yes"}
    for c in fcols_all:
        row[c] = 1.0 if ours.get(c[2:]) in ok else 0.0

    rng = np.random.default_rng(SEED)
    test = rng.random(len(Xp)) < 0.2
    fit_tr, cols_tr = ols(Xp[~test], y[~test], controls + fe + lasso_select(Xp[~test], y[~test], fcols))
    xte = sm.add_constant(Xp.loc[test, cols_tr].astype(float), has_constant="add").reindex(columns=fit_tr.params.index, fill_value=0)
    pred, yte = fit_tr.predict(xte), y[test]
    r2 = float(1 - ((yte - pred) ** 2).sum() / ((yte - yte.mean()) ** 2).sum())
    mape = float((np.abs(np.exp(pred) - np.exp(yte)) / np.exp(yte)).mean())

    sel = lasso_select(Xp, y, fcols)
    fit, cols = ols(Xp, y, controls + fe + sel)
    fv = []
    for c in fcols:
        r = pds(Xp, y, c, controls + fe, controls + fe + fcols)
        fv.append({"feature_id": c[2:], **r, "prevalence": float(Xp[c].mean()), "ours": ours.get(c[2:]),
                   "ci_excludes_zero": bool(r["ci90"][0] > 0 or r["ci90"][1] < 0), "selected_by_lasso": c in sel})
    pd.DataFrame(fv).sort_values("pct_price_effect", ascending=False).to_csv(D / "coefficients.csv", index=False)

    oy = [c for c in fcols_all if row[c] == 1]
    cov = X[oy].sum(1) / len(oy) if oy else pd.Series(0.0, index=X.index)
    near = pd.DataFrame({"vendor": X.index, "coverage": cov.values, "price_state": ref.reindex(X.index)["price_state"].values,
                         "ref_main": ref.reindex(X.index)["ref_main"].values})
    near["missing_our_features"] = [";".join(c[2:] for c in oy if not X.loc[v, c]) for v in X.index]
    near = near.sort_values("coverage", ascending=False)
    near.head(40).to_csv(D / "nearest_competitors.csv", index=False)
    nb = near[near.vendor.isin(priced)].head(a.neighbours)

    implied, rows = {}, []
    for s in st.segments + ["pooled"]:
        col = "ref_main" if s == "pooled" else f"ref_{s}"
        ys = np.log(ref.loc[priced, col].replace(0, np.nan).dropna().astype(float))
        f_s, c_s = ols(Xp.loc[ys.index], ys, cols)
        o_pt, o_ci = predict(f_s, row[c_s])
        l_pt, l_ci = lasso_pred(Xp.loc[ys.index], ys, controls + fe + fcols, row)
        npr = ref.loc[nb.vendor, col].dropna().astype(float)
        w = nb.set_index("vendor").loc[npr.index, "coverage"].clip(lower=1e-3)
        k_pt = float(np.exp(np.average(np.log(npr), weights=w))) if len(npr) else None
        implied[s] = {"ols": {"point": o_pt, "ci90": o_ci}, "lasso": {"point": l_pt, "ci90": l_ci},
                      "neighbours": {"point": k_pt, "p10_p90": [float(npr.quantile(.1)), float(npr.quantile(.9))] if len(npr) else None},
                      "n_vendors": int(len(ys)),
                      "share_exceeds_top": float(ref.loc[ys.index, f"ref_{s}_exceeds_top"].fillna(False).astype(bool).mean()) if s != "pooled" else None}
        rows.append({"segment": s, "ols": o_pt, "ols_lo": o_ci[0], "ols_hi": o_ci[1], "lasso": l_pt, "lasso_lo": l_ci[0], "lasso_hi": l_ci[1], "neighbours": k_pt})
    pd.DataFrame(rows).to_csv(D / "implied_price.csv", index=False)

    cnt = X.loc[priced, fcols_all].sum(1)
    our_cnt = int(row[fcols_all].sum())
    support = {"our_feature_count": our_cnt, "priced_feature_count_quantiles": {str(q): float(v) for q, v in cnt.quantile([.5, .9, .99, 1.0]).items()},
               "share_priced_at_or_above_us": float((cnt >= our_cnt).mean())}
    oos = [c[2:] for c in fcols_all if row[c] == 1 and c not in fcols]
    assumptions = ["Listed prices reflect delivered value; they don't fully (strategic pricing, disequilibrium, survivorship): this is a market reference, not value.",
                   "Reference price = the recommended plan, else the middle paid tier; plans with limits on the segment axis priced at each segment's reference_volume.",
                   f"Our vector = taxonomy `ours` {'yes+partial' if a.with_partial else 'yes'}; our controls from vendors.csv __ours__, else corpus medians."]
    if support["share_priced_at_or_above_us"] < 0.05:
        assumptions.append("We have more coded features than almost every priced vendor, so OLS extrapolates; read the lasso and neighbour prices as the in-support bound.")
    p = merge_summary(st, "market", {
        "corpus": {"n_vendors": int(len(X)), "n_priced": int(len(priced)), "price_visibility": ref.reindex(X.index)["price_state"].value_counts().to_dict(),
                   "direct_only": a.direct_only},
        "reference_price_rule": "recommended > middle paid tier; usage plans at each segment's reference_volume",
        "fit": {"r2_oos": r2, "mape_oos": mape, "n_train": int((~test).sum()), "n_test": int(test.sum()), "r2_in_sample": float(fit.rsquared)},
        "kappa": {"dropped": dropped}, "feature_values": fv, "implied_price": implied, "support": support,
        "nearest_competitors": nb[["vendor", "coverage", "ref_main", "missing_our_features"]].to_dict("records"),
        "out_of_sample_features": oos}, assumptions,
        [{"what": f, "why": "below 2% prevalence or κ-dropped: the market can't price it", "blocked_on": None} for f in oos])
    print(f"priced {len(priced)}/{len(X)} · R²oos {r2:.2f} · MAPE {mape:.2f} · features modelled {len(fcols)}")
    print(pd.DataFrame(rows).round(1).to_string(index=False))
    print(f"→ {p}")


if __name__ == "__main__":
    main()
