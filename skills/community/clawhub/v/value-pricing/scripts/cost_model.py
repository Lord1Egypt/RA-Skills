"""Phase 5 · the floor: variable, people and channel cost per customer per segment; fixed-cost carry.

Reads costs.yaml (templates/costs.yaml). Variable lines are per-segment maps (eur_per_customer) or
per_unit × the segment's reference_volume. If driver_regression.file is set, fits cost ~ drivers by OLS
across real customers (e.g. cost/data/per_customer.csv) and predicts each segment at drivers_by_segment,
with a bootstrap 90% interval; eur_per_customer lines are then taken as covered by it unless they say
covered_by_regression: false. People time = support hours (a [low, high] range → midpoint and band) +
one-off onboarding amortised.

Per segment: floor price at each margin target = cost ÷ (1 − margin − channel share). Per candidate
price (study.yaml cost.candidate_prices): customers needed to carry the fixed platform, and the support
minutes per customer per month the price affords at each margin target.

  cost_model.py --study S
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from common import Study, per_seg, study_arg, write_summary


def main():
    ap = study_arg(__doc__.splitlines()[0])
    a = ap.parse_args()
    st = Study(a.study)
    c = st.yaml("costs.yaml")
    ppl, chan = c.get("people", {}), c.get("channel", {})
    chan_share = float(chan.get("revenue_share", 0)) + float(chan.get("processing", 0))
    rate = float(ppl.get("hourly_rate", 0))
    margins = c.get("margin_targets") or st.cfg.get("cost", {}).get("margin_targets", [0.7, 0.8, 0.85])
    fixed = sum(float(l["eur_month"]) for l in c["lines"] if l["kind"] == "fixed" and l.get("eur_month") is not None)
    gaps = list(c.get("gaps") or [])
    reg, dr = None, c.get("driver_regression") or {}
    if dr.get("file"):
        df = pd.read_csv(st.root / dr["file"])
        drivers = [k for k in df.columns if k != "cost" and pd.api.types.is_numeric_dtype(df[k])]
        X = np.column_stack([np.ones(len(df))] + [df[k] for k in drivers])
        y = df.cost.to_numpy(float)
        coef = np.linalg.lstsq(X, y, rcond=None)[0]
        r2 = 1 - ((y - X @ coef) ** 2).sum() / ((y - y.mean()) ** 2).sum()
        rng = np.random.default_rng(5)
        boots = np.array([np.linalg.lstsq(X[i], y[i], rcond=None)[0] for i in (rng.integers(0, len(df), len(df)) for _ in range(2000))])
        reg = {"drivers": drivers, "coef": dict(zip(["intercept"] + drivers, map(float, coef))), "r2": float(r2), "n": int(len(df))}
    var, ppl_cost, rows = {}, {}, []
    for b in st.bands:
        s = b["id"]
        v, ci, lines = 0.0, None, []
        if reg:
            x = np.array([1.0] + [float(dr["drivers_by_segment"][s][k]) for k in reg["drivers"]])
            v = float(x @ np.array(list(reg["coef"].values())))
            pts = boots @ x
            ci = [float(np.quantile(pts, .05)), float(np.quantile(pts, .95))]
            lines.append("driver regression")
        for l in c["lines"]:
            if l["kind"] != "variable":
                continue
            if l.get("eur_per_customer") is not None:
                if reg and l.get("covered_by_regression", True):
                    continue
                add = float(per_seg(l["eur_per_customer"], s))
            elif l.get("per_unit") is not None:
                add = float(l["per_unit"]) * float(b["reference_volume"])
            else:
                gaps.append({"what": f"{l['line']} ({s})", "why": "no amount", "blocked_on": "owner"})
                continue
            v += add
            ci = [ci[0] + add, ci[1] + add] if ci else None
            lines.append(l["line"])
        ci = ci or [v, v]
        sup = per_seg(ppl.get("support_hours_per_month", 0), s)
        lo, hi = sup if isinstance(sup, list) else [sup, sup]
        onb = float(per_seg(ppl.get("onboarding_hours_one_off", 0), s)) / max(1, ppl.get("amortise_onboarding_months", 12))
        h = (lo + hi) / 2 + onb
        var[s] = {"point": v, "ci90": ci, "lines": lines}
        ppl_cost[s] = {"hours": h, "hours_range": [lo + onb, hi + onb], "eur": h * rate, "eur_range": [(lo + onb) * rate, (hi + onb) * rate]}
        for m in margins:
            den = 1 - m - chan_share
            rows.append({"segment": s, "target_margin": m, "floor_variable_only": v / den if den > 0 else None,
                         "floor_with_people": (v + h * rate) / den if den > 0 else None,
                         "floor_with_people_high": (ci[1] + (hi + onb) * rate) / den if den > 0 else None})
    floor = pd.DataFrame(rows)
    floor.to_csv(st.path("cost", "results", "floor.csv"), index=False)
    carry, minutes = [], []
    for p in st.cfg.get("cost", {}).get("candidate_prices", []):
        for s in st.segments:
            contrib = p * (1 - chan_share) - var[s]["point"] - ppl_cost[s]["eur"]
            carry.append({"price": p, "segment": s, "contribution": contrib,
                          "customers_to_carry_fixed": int(np.ceil(fixed / contrib)) if contrib > 0 else None})
            for m in margins:
                budget = p * (1 - chan_share) * (1 - m) - var[s]["point"]
                minutes.append({"segment": s, "price": p, "target_margin": m, "minutes": max(0.0, budget / rate * 60) if rate else None})
    pd.DataFrame(carry).to_csv(st.path("cost", "results", "carry.csv"), index=False)
    pd.DataFrame(minutes).to_csv(st.path("cost", "results", "support_minutes.csv"), index=False)
    n_now = c.get("customers_now")
    p = write_summary(st, "cost", {
        "lines": c["lines"], "variable_per_customer": var, "people_per_customer": ppl_cost,
        "channel_share_of_price": chan_share, "fixed_platform": fixed, "fixed_share_now": fixed / n_now if n_now else None,
        "driver_regression": reg, "floor_price": floor.to_dict("records"), "carry": carry, "support_minutes_afforded": minutes},
        ["Cost is a floor, never the price (Nagle).",
         "Fixed platform ÷ current customers is a volume target (customers needed to carry it), not a per-customer floor.",
         f"People time costed at {rate}/h; support hours at the midpoint of the owner's range."], gaps)
    print(pd.DataFrame({s: {"variable": var[s]["point"], "people": ppl_cost[s]["eur"]} for s in var}).T.round(2).to_string())
    print(floor.round(2).to_string(index=False))
    print(f"fixed platform {fixed:,.0f}/month; channel share {chan_share:.1%} → {p}")


if __name__ == "__main__":
    main()
