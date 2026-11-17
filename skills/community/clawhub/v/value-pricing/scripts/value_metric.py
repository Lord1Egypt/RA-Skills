"""Phase 2 · which quantity does the market meter on, and how steeply? → the packaging axis.

For every `limit_<axis>` column in market/data/plans.csv: the share of priced vendors whose plans scale
on it (all / direct), and the within-vendor elasticity of price on quantity: log price on log quantity
after removing each vendor's mean (vendors with ≥2 paid plans at distinct positive limits), with a
vendor-bootstrap 90% CI and the within R². Elasticity e means doubling the quantity multiplies price
by 2^e. `co_moves` gives, per other axis, the share of these vendors whose plans step that axis up too:
when two axes rise together across tiers their slopes are confounded and belong to the bundle, not to
either axis. Read the meter off the axis vendors scale on ALONE.

Also prints the multiplier table for 1..6 units (n^elasticity): the curve phase 6 uses to price extra
units (seats, sources, accounts) and extra stores/brands.

  value_metric.py --study S [--boot 2000]
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from common import Study, merge_summary, study_arg
from hedonic import flag, is_direct, monthly


def vendor_stats(df):
    """Per-vendor demeaned sums: the within slope is Σ Sxy / Σ Sxx, so a vendor bootstrap resamples rows of this."""
    d = df.assign(lp=np.log(df.eur), lq=np.log(df.q))
    d["lp"] -= d.groupby("vendor").lp.transform("mean")
    d["lq"] -= d.groupby("vendor").lq.transform("mean")
    return d.assign(sxy=d.lq * d.lp, sxx=d.lq ** 2, syy=d.lp ** 2).groupby("vendor")[["sxy", "sxx", "syy"]].sum()


def slope(S):
    sxy, sxx, syy = (S.sum(0) if isinstance(S, np.ndarray) else S.sum().to_numpy())
    if sxx == 0:
        return np.nan, np.nan
    b = sxy / sxx
    return float(b), (float(1 - (syy - 2 * b * sxy + b * b * sxx) / syy) if syy > 0 else np.nan)


def co_moves(plans, col, vendors):
    out = {}
    for o in [c for c in plans.columns if c.startswith("limit_") and c != col]:
        g = plans[plans.vendor.isin(vendors)].groupby("vendor")[o].nunique()
        out[o[6:]] = round(float((g >= 2).mean()), 3) if len(g) else 0.0
    return out


def main():
    ap = study_arg(__doc__.splitlines()[0])
    ap.add_argument("--boot", type=int, default=2000)
    a = ap.parse_args()
    st = Study(a.study)
    D = st.root / "market" / "data"
    plans = pd.read_csv(D / "plans.csv")
    vendors = pd.read_csv(D / "vendors.csv").set_index("vendor")
    cur = st.cfg.get("currency", "EUR")
    fx = {k: v for k, v in (st.cfg.get("fx") or {}).items() if k != "date"}
    plans = plans[plans.price.notna() & ~flag(plans, "is_quote")].copy()
    plans["eur"] = [monthly(r, fx, cur) for _, r in plans.iterrows()]
    plans = plans[plans.eur > 0]
    direct = set(vendors.index[is_direct(vendors["tier"])]) if "tier" in vendors else set()
    n_all, n_dir = plans.vendor.nunique(), len(direct & set(plans.vendor))
    rng = np.random.default_rng(7)
    rows = []
    for col in [c for c in plans.columns if c.startswith("limit_")]:
        d = plans[["vendor", "eur", col]].rename(columns={col: "q"})
        d["q"] = pd.to_numeric(d.q, errors="coerce")
        d = d[d.q > 0]
        use = d.groupby("vendor").q.nunique()
        use = use[use >= 2].index
        d = d[d.vendor.isin(use)]
        rec = {"axis": col[6:], "n_vendors": int(len(use)), "share_all": len(use) / max(n_all, 1),
               "share_direct": len(set(use) & direct) / n_dir if n_dir else None}
        if len(use) >= 3:
            S = vendor_stats(d)
            b, r2 = slope(S)
            arr = S.to_numpy()
            boots = [slope(arr[rng.integers(0, len(arr), len(arr))])[0] for _ in range(a.boot)]
            Sd = S[S.index.isin(direct)]
            rec.update({"elasticity": b, "ci90": [float(np.nanquantile(boots, .05)), float(np.nanquantile(boots, .95))],
                        "elasticity_direct": slope(Sd)[0] if len(Sd) >= 3 else None, "r2_within": r2,
                        "co_moves": co_moves(plans, col, use)})
        rows.append(rec)
    out = pd.DataFrame(rows).sort_values("share_all", ascending=False)
    out.to_csv(D / "meters.csv", index=False)
    print(out.round(3).to_string(index=False))
    mult = {r["axis"]: {str(n): round(n ** r["elasticity"], 2) for n in range(1, 7)} for r in rows if r.get("elasticity") is not None}
    print("\nprice multiplier for n units (n^elasticity):")
    print(pd.DataFrame(mult).T.to_string())
    merge_summary(st, "market", {"meters": rows, "unit_multipliers": mult})


if __name__ == "__main__":
    main()
