"""Phase 3 · delivered value per customer, split across features: scenarios → Monte Carlo → attribution → Sobol.

Reads study.yaml (segments, archetypes, scenarios) and value_drivers.yaml (params, types, caps, lines).
For each simulated customer-month:
  a line is ACTIVE when its feature and every feature it needs are enabled and in use for that customer
  (study.yaml scenarios.feature_in_use), and it FIRES on its trigger (an expression) or with p_fire;
  its € = the type's formula × (action_rate × realisation_rate when the type is an insight type);
  caps bound the sum of the named types per scenario.
  value = Σ lines after caps;  EVC = archetype reference-alternative cost + value.
Feature attribution: Shapley values by permutation sampling (Castro et al. 2009) over every feature that
appears as a line's feature or need (gates included), caps applied inside each coalition; plus
leave-one-out (value lost when one feature is removed, with everything it gates).
Sobol: first-order (Saltelli 2010) and total (Jansen) indices of the population-mean WTP
(EVC × capture_share) over every param with a range. Below --sobol-n 1024 S1 is noisy.

  value_mc.py --study S [--n 10000] [--perms 200] [--sobol-n 1024]

Writes value/data/{scenarios,mc_results,fire_matrix,shapley}.parquet, value/data/{feature_value,
sensitivity}.csv, value/results/summary.json.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from common import Study, evaluate_expr, per_seg, status, study_arg, write_summary


# ------------------------------------------------------------------ scenarios
def draw(spec: dict, seg: str, arch: np.ndarray, band: dict, rng, n: int, ns: dict):
    if "expr" in spec:
        v = evaluate_expr(spec["expr"], {**ns, "rng": rng, "n": n})
        return np.broadcast_to(np.asarray(v, dtype=float), (n,)).copy()
    d = spec["dist"]
    g = lambda k: per_seg(spec[k], seg)
    if d == "band":
        lo, hi = band["range"]
        hi = hi or lo * 10
        return np.exp(rng.uniform(np.log(max(lo, 1e-9)), np.log(hi), n))
    if d == "lognormal":
        return rng.lognormal(np.log(g("median")), g("sigma"), n)
    if d == "uniform":
        return rng.uniform(g("low"), g("high"), n)
    if d == "normal":
        return rng.normal(g("mean"), g("sd"), n)
    if d == "beta":
        return rng.beta(g("a"), g("b"), n)
    if d == "bernoulli":
        return (rng.random(n) < g("p")).astype(float)
    if d == "per_segment":
        return np.full(n, float(per_seg(spec["values"], seg)))
    if d == "per_archetype":
        return np.array([float(per_seg(spec["values"][x], seg)) for x in arch])
    if d == "choice":
        return rng.choice(np.asarray(spec["options"], dtype=float), n, p=spec.get("p"))
    raise SystemExit(f"unknown dist {d!r}")


def generate(st: Study, n: int, seed: int) -> pd.DataFrame:
    sc = st.cfg["scenarios"]
    rng = np.random.default_rng(seed)
    shares = st.segment_share()
    ref = {x["id"]: x.get("reference_alternative", {}) for x in st.archetypes}
    parts = []
    for b in st.bands:
        seg = b["id"]
        k = int(round(n * shares[seg]))
        if k == 0:
            continue
        ash = st.archetype_share(seg)
        arch = rng.choice(list(ash), k, p=list(ash.values())) if ash else np.array(["generic"] * k)
        ns = {}
        for name, spec in sc["variables"].items():
            ns[name] = draw(spec, seg, arch, b, rng, k, ns)
        df = pd.DataFrame(ns)
        df.insert(0, "archetype", arch)
        df.insert(0, "segment", seg)
        df["reference_cost"] = [float(per_seg(ref.get(x, {}).get("cost", 0), seg)) for x in arch]
        parts.append(df)
    out = pd.concat(parts, ignore_index=True)
    out.index.name = "scenario_id"
    return out


# ------------------------------------------------------------------ value engine
class Engine:
    def __init__(self, st: Study, drivers: dict, scen: pd.DataFrame, seed: int):
        self.d, self.s = drivers, scen
        self.params = {k: v["value"] for k, v in drivers["params"].items()}
        self.types, self.lines = drivers["types"], drivers["lines"]
        rng = np.random.default_rng(seed + 1)
        ns = {c: scen[c].to_numpy() for c in scen.columns if c not in ("segment", "archetype")}
        self.ns, N = ns, len(scen)
        use = st.cfg["scenarios"].get("feature_in_use") or {}
        self.players = sorted({l["feature"] for l in self.lines} | {x for l in self.lines for x in l.get("needs", [])})
        self.in_use = {f: (np.broadcast_to(np.asarray(evaluate_expr(use[f], ns), bool), (N,)) if f in use else np.ones(N, bool)) for f in self.players}
        self.q, self.fire, self.extra = [], [], []
        for l in self.lines:
            self.q.append(np.broadcast_to(np.asarray(evaluate_expr(l["quantity"], ns), float), (N,)))
            f = np.asarray(evaluate_expr(l["trigger"], ns), bool) if "trigger" in l else rng.random(N) < float(l.get("p_fire", 1.0))
            self.fire.append(np.broadcast_to(f, (N,)))
            self.extra.append({k: np.clip(np.broadcast_to(np.asarray(evaluate_expr(l[k], ns), float), (N,)), 0, None)
                               for k in ("at_risk", "excess") if k in l})
        self.cap_max = [np.broadcast_to(np.asarray(evaluate_expr(c["max"], ns), float), (N,)) for c in drivers.get("caps", [])]
        self.ltypes = np.array([l["type"] for l in self.lines])
        self.vals = self.line_values()

    def line_values(self, params: dict | None = None, rows=None) -> np.ndarray:
        p = {**self.params, **(params or {})}
        sl = slice(None) if rows is None else rows
        base = {k: v[sl] for k, v in self.ns.items()}
        vals = []
        for l, q, f, ex in zip(self.lines, self.q, self.fire, self.extra):
            t = self.types[l["type"]]
            v = np.asarray(evaluate_expr(t["formula"], {**base, **p, "q": q[sl], **{k: x[sl] for k, x in ex.items()}}), float) * f[sl]
            if t.get("insight"):
                v = v * p["action_rate"] * p["realisation_rate"]
            vals.append(np.clip(np.broadcast_to(v, f[sl].shape), 0, None))
        return np.vstack(vals)

    def active(self, enabled: set, rows=None) -> np.ndarray:
        n = len(self.s) if rows is None else len(rows)
        sl = slice(None) if rows is None else rows
        m = []
        for l in self.lines:
            need = [l["feature"]] + list(l.get("needs", []))
            a = np.ones(n, bool)
            if all(x in enabled for x in need):
                for x in need:
                    a = a & self.in_use[x][sl]
            else:
                a[:] = False
            m.append(a)
        return np.vstack(m)

    def total(self, enabled: set, vals=None, rows=None, by_type=False):
        vals = self.vals if vals is None else vals
        sl = slice(None) if rows is None else rows
        v = vals * self.active(enabled, rows)
        capped, used, per_type = np.zeros(v.shape[1]), np.zeros(len(self.lines), bool), {}
        for c, mx in zip(self.d.get("caps", []), self.cap_max):
            m = np.isin(self.ltypes, c["types"]) & ~used
            raw = v[m].sum(0)
            lim = np.minimum(raw, np.clip(mx[sl], 0, None))
            capped += lim
            if by_type:
                scale = np.divide(lim, raw, out=np.zeros_like(raw), where=raw > 0)
                for t in set(self.ltypes[m]):
                    per_type[t] = per_type.get(t, 0) + v[(self.ltypes == t) & m].sum(0) * scale
            used |= m
        capped += v[~used].sum(0)
        if by_type:
            for t in set(self.ltypes[~used]):
                per_type[t] = per_type.get(t, 0) + v[(self.ltypes == t) & ~used].sum(0)
            return capped, per_type
        return capped


def shapley(eng: Engine, perms: int, seed: int) -> dict:
    rng = np.random.default_rng(seed + 2)
    phi = {f: np.zeros(len(eng.s)) for f in eng.players}
    cache = {}

    def v(S):
        k = frozenset(S)
        if k not in cache:
            cache[k] = eng.total(set(k)) if k else np.zeros(len(eng.s))
        return cache[k]

    for _ in range(perms):
        S, prev = set(), v(set())
        for f in rng.permutation(eng.players):
            S = S | {f}
            cur = v(S)
            phi[f] += cur - prev
            prev = cur
    return {f: x / perms for f, x in phi.items()}


def sobol(eng: Engine, st: Study, N: int, seed: int, sub: int = 2000) -> list:
    rng = np.random.default_rng(seed + 3)
    names = [k for k, v in eng.d["params"].items() if "range" in v]
    lo = np.array([eng.d["params"][k]["range"][0] for k in names])
    hi = np.array([eng.d["params"][k]["range"][1] for k in names])
    rows = rng.choice(len(eng.s), min(sub, len(eng.s)), replace=False)
    full = set(eng.players)
    ref = eng.s["reference_cost"].to_numpy()[rows]
    w = eng.s["segment"].iloc[rows].map(st.segment_share()).to_numpy()
    w = w / w.sum()

    def f(x):
        p = dict(zip(names, x))
        tot = eng.total(full, eng.line_values(p, rows), rows)
        return float(np.sum(w * (ref + tot)) * p.get("capture_share", eng.params.get("capture_share", 0.2)))

    A = lo + (hi - lo) * rng.random((N, len(names)))
    B = lo + (hi - lo) * rng.random((N, len(names)))
    fA, fB = np.array([f(x) for x in A]), np.array([f(x) for x in B])
    var = np.var(np.concatenate([fA, fB]))
    out = []
    for i, nm in enumerate(names):
        ABi = A.copy()
        ABi[:, i] = B[:, i]
        fAB = np.array([f(x) for x in ABi])
        out.append({"parameter": nm, "S1": float(np.mean(fB * (fAB - fA)) / var) if var else None,
                    "ST": float(0.5 * np.mean((fA - fAB) ** 2) / var) if var else None, "range": [float(lo[i]), float(hi[i])]})
    return sorted(out, key=lambda r: -(r["ST"] or 0))


def main():
    ap = study_arg(__doc__.splitlines()[0])
    ap.add_argument("--n", type=int)
    ap.add_argument("--perms", type=int, default=200)
    ap.add_argument("--sobol-n", type=int, default=1024)
    a = ap.parse_args()
    st = Study(a.study)
    drivers = st.yaml("value_drivers.yaml")
    sc = st.cfg["scenarios"]
    n, seed = a.n or sc.get("n", 10000), sc.get("seed", 1)
    scen = generate(st, n, seed)
    eng = Engine(st, drivers, scen, seed)
    full = set(eng.players)
    value, by_type = eng.total(full, by_type=True)
    res = scen[["segment", "archetype", "reference_cost"]].copy()
    res["value"] = value
    for t, x in by_type.items():
        res[f"value_{t}"] = x
    res["evc"] = res.reference_cost + res.value
    D = st.root / "value" / "data"
    D.mkdir(parents=True, exist_ok=True)
    scen.to_parquet(D / "scenarios.parquet")
    res.to_parquet(D / "mc_results.parquet")
    act = eng.active(full)
    pd.DataFrame((act & (eng.vals > 0)).T, columns=[l["id"] for l in eng.lines], index=scen.index).to_parquet(D / "fire_matrix.parquet")

    phi = shapley(eng, a.perms, seed)
    sh = pd.DataFrame(phi, index=scen.index)
    sh.insert(0, "segment", scen.segment)
    sh.to_parquet(D / "shapley.parquet")
    tot = value.sum()
    tax = {f["id"]: f for f in (st.yaml("taxonomy.yaml", required=False) or {}).get("features", [])}
    fv = []
    for f in eng.players:
        own = sum((eng.vals[i] * act[i] for i, l in enumerate(eng.lines) if l["feature"] == f), np.zeros(len(scen)))
        loo = value - eng.total(full - {f})
        rec = {"feature_id": f, "ours": status(tax.get(f, {}).get("ours")),
               "share_of_scenarios_valued": float((own > 0).mean()),
               "median_eur_when_valued": float(np.median(own[own > 0])) if (own > 0).any() else 0.0,
               "shapley_share": float(phi[f].sum() / tot) if tot else 0.0,
               "shapley_eur_mean": float(phi[f].mean()),
               "leave_one_out_eur_mean": float(loo.mean()),
               "share_of_scenarios_lost_without": float((loo > 1e-9).mean())}
        for s in st.segments:
            m = (scen.segment == s).to_numpy()
            rec[f"shapley_eur_mean_{s}"] = float(phi[f][m].mean()) if m.any() else None
        rec["is_gate"] = bool(rec["share_of_scenarios_lost_without"] > 2 * rec["share_of_scenarios_valued"] + 0.05)
        fv.append(rec)
    fv.sort(key=lambda r: -r["shapley_share"])
    pd.DataFrame(fv).to_csv(D / "feature_value.csv", index=False)

    vbs, band = {}, {}
    for s in st.segments:
        r = res[res.segment == s]
        if r.empty:
            continue
        vbs[s] = {"value": {q: float(r.value.quantile(x)) for q, x in (("p10", .1), ("p50", .5), ("p90", .9))},
                  "evc": {q: float(r.evc.quantile(x)) for q, x in (("p10", .1), ("p50", .5), ("p90", .9))},
                  "by_type_share": {c[6:]: float(r[c].sum() / r.value.sum()) if r.value.sum() else 0.0 for c in r if c.startswith("value_")}}
        band[s] = {f"capture_{int(c * 100)}": float(r.evc.median() * c) for c in (0.1, 0.2, 0.3)}
    sens = sobol(eng, st, a.sobol_n, seed) if a.sobol_n else []
    pd.DataFrame(sens).to_csv(D / "sensitivity.csv", index=False)
    p = write_summary(st, "value", {"design": {"n_scenarios": len(scen), "seed": seed, "shapley_permutations": a.perms, "sobol_n": a.sobol_n},
                                    "value_by_segment": vbs, "wtp_band_evc": band, "feature_value": fv, "sensitivity": sens},
                      ["Scenario distributions are priors from study.yaml, not measurements of customers.",
                       "Insight value is multiplied by action_rate × realisation_rate; delivered work and replaced cost are not.",
                       "EVC = the archetype's reference-alternative cost + delivered value; the WTP band is EVC × 10/20/30% capture."])
    print(pd.DataFrame({k: {**v["value"], "evc_p50": v["evc"]["p50"]} for k, v in vbs.items()}).T.round(1).to_string())
    print(pd.DataFrame(fv)[["feature_id", "share_of_scenarios_valued", "shapley_share", "leave_one_out_eur_mean", "is_gate"]].round(3).to_string(index=False))
    if sens:
        print(pd.DataFrame(sens)[["parameter", "S1", "ST"]].round(3).to_string(index=False))
    print(f"→ {p}")


if __name__ == "__main__":
    main()
