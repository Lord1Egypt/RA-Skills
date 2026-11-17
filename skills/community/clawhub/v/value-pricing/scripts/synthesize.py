"""Phase 6 · price corridor per segment and the feature-value table, from the phase summaries.

Corridor (per segment, money per month):
  floor      cost: floor_with_people at --margin
  reference  market: the band spanned by the OLS, lasso and coverage-neighbour implied prices
  ceiling    value: EVC × 10–30% capture; beside it the panel's reservation price p25–p75
  stated     panel Van Westendorp OPP–IPP, when the panel ran
  window     from max(floor, stated OPP or EVC×10%) up to min(reference point, ceiling high)
  order      ok | floor above ceiling | reference above ceiling | window empty
Feature table: market premium (PDS coefficient, CI) joined to value (share valued, Shapley share,
leave-one-out, gate flag) on the taxonomy id, then classed headline / underpriced differentiator /
market premium / gate / roadmap / low both. Thresholds are flags so the report can state them.

  synthesize.py --study S [--margin 0.8] [--premium 0.15] [--valued 0.30] [--shapley 0.10]
"""
from __future__ import annotations

import pandas as pd

from common import Study, read_summary, status, study_arg, write_summary


def main():
    ap = study_arg(__doc__.splitlines()[0])
    ap.add_argument("--margin", type=float, default=0.8)
    ap.add_argument("--premium", type=float, default=0.15)
    ap.add_argument("--valued", type=float, default=0.30)
    ap.add_argument("--shapley", type=float, default=0.10)
    a = ap.parse_args()
    st = Study(a.study)
    M, C, V, Pn = ((read_summary(st, p) or {}) for p in ("market", "cost", "value", "panel"))
    D = read_summary(st, "demand") or {}
    psm_p = st.root / "panel/results/psm.csv"
    psm = pd.read_csv(psm_p) if psm_p.exists() else None
    missing = [p for p, s in (("market", M), ("cost", C), ("value", V), ("panel", Pn)) if not s]
    rows = []
    for s in st.segments:
        r = {"segment": s}
        fl = [x for x in C.get("floor_price", []) if x["segment"] == s and abs(x["target_margin"] - a.margin) < 1e-9]
        if fl:
            r["floor"] = fl[0]["floor_with_people"]
        ip = M.get("implied_price", {}).get(s)
        if ip:
            pts = [ip[k]["point"] for k in ("ols", "lasso", "neighbours") if ip.get(k) and ip[k].get("point")]
            r["reference_lo"], r["reference_hi"], r["reference_point"] = min(pts), max(pts), ip["lasso"]["point"]
        band = V.get("wtp_band_evc", {}).get(s)
        if band:
            r["ceiling_lo"], r["ceiling_hi"] = band["capture_10"], band["capture_30"]
        rp = Pn.get("reservation_price", {}).get(s)
        if rp:
            r["panel_p25"], r["panel_median"], r["panel_p75"] = rp["p25"], rp["median"], rp["p75"]
        if psm is not None:
            q = psm[(psm.segment == s) & (psm.arm == "pooled")]
            if len(q):
                r["stated_opp"], r["stated_ipp"] = q.opp.iloc[0], q.ipp.iloc[0]
        lo = next((x for x in (r.get("stated_opp"), r.get("ceiling_lo")) if x is not None and x == x), None)
        ceil_hi = r.get("ceiling_hi")
        if lo is not None:
            r["window_lo"] = max(lo, r.get("floor") or 0)
        hi = [x for x in (r.get("reference_point"), ceil_hi) if x is not None]
        if hi:
            r["window_hi"] = min(hi)
        checks = []
        if r.get("floor") is not None and ceil_hi is not None and r["floor"] > ceil_hi:
            checks.append("floor above ceiling")
        if r.get("reference_lo") is not None and r.get("ceiling_hi") is not None and r["reference_lo"] > r["ceiling_hi"]:
            checks.append("reference above ceiling")
        if r.get("window_lo") is not None and r.get("window_hi") is not None and r["window_lo"] > r["window_hi"]:
            checks.append("window empty")
        r["order"] = "; ".join(checks) or ("ok" if len(r) > 3 else "insufficient inputs")
        rows.append(r)
    cor = pd.DataFrame(rows)
    cor.to_csv(st.path("synthesis", "data", "corridor.csv"), index=False)

    mv = {f["feature_id"]: f for f in M.get("feature_values", [])}
    vv = {f["feature_id"]: f for f in V.get("feature_value", [])}
    tax = {f["id"]: f for f in (st.yaml("taxonomy.yaml", required=False) or {}).get("features", [])}
    out = []
    for fid in sorted(set(mv) | set(vv) | set(tax)):
        m, v = mv.get(fid, {}), vv.get(fid, {})
        ours = status(tax.get(fid, {}).get("ours")) or status(m.get("ours")) or status(v.get("ours"))
        mk = bool(m.get("ci_excludes_zero") and (m.get("pct_price_effect") or 0) >= a.premium)
        vh = bool((v.get("share_of_scenarios_valued") or 0) >= a.valued or (v.get("shapley_share") or 0) >= a.shapley)
        gate = bool(v.get("is_gate"))
        if ours == "no":
            cls = "roadmap" if mk else "absent, no premium"
        elif mk and vh:
            cls = "headline"
        elif mk and gate:
            cls = "gate (headline fence)"
        elif gate:
            cls = "gate"
        elif vh:
            cls = "underpriced differentiator"
        elif mk:
            cls = "market premium"
        elif m or v:
            cls = "low both"
        else:
            cls = "unmeasured"
        if ours == "partial" and cls in ("headline", "underpriced differentiator", "gate (headline fence)"):
            cls += " (partial today: keep out of tier copy)"
        out.append({"feature_id": fid, "ours": ours, "market_pct_effect": m.get("pct_price_effect"), "market_ci90": m.get("ci90"),
                    "market_prevalence": m.get("prevalence"), "share_valued": v.get("share_of_scenarios_valued"),
                    "median_eur_when_valued": v.get("median_eur_when_valued"), "shapley_share": v.get("shapley_share"),
                    "leave_one_out_eur_mean": v.get("leave_one_out_eur_mean"), "is_gate": gate, "class": cls})
    fvt = pd.DataFrame(out).sort_values(["class", "shapley_share"], ascending=[True, False])
    fvt.to_csv(st.path("synthesis", "data", "feature_value.csv"), index=False)
    # Keep actual-purchase evidence in its own deliverable. It answers a different
    # question from competitor list-price meter elasticity and must not overwrite it.
    demand = D.get("demand_elasticity")
    demand_rows = []
    if demand:
        for product, result in demand.get("products", {}).items():
            for estimate in result.get("estimates", []):
                demand_rows.append({"product": product, **estimate,
                                    "model_status": result.get("status"),
                                    "diagnostics": result.get("diagnostics"),
                                    "identification": demand.get("identification")})
    pd.DataFrame(demand_rows).to_json(st.path("synthesis", "data", "demand_elasticity.json"), orient="records", indent=2)
    write_summary(st, "synthesis", {"corridor": cor.to_dict("records"), "feature_value": out,
                                    "demand_elasticity": demand,
                                    "thresholds": {"margin": a.margin, "premium": a.premium, "valued": a.valued, "shapley": a.shapley}},
                  ["Floor = variable + people + channel cost at the target margin; reference = market implied-price band; ceiling = EVC × 10–30% capture."],
                  [{"what": f"{p} phase", "why": "no summary.json", "blocked_on": None} for p in missing])
    print(cor.round(1).to_string(index=False))
    print()
    print(fvt[["feature_id", "ours", "market_pct_effect", "share_valued", "shapley_share", "class"]].round(3).to_string(index=False))
    if missing:
        print("missing phases:", ", ".join(missing))


if __name__ == "__main__":
    main()
