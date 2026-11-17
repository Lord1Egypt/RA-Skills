"""Phase 4b · hierarchical Bayes MNL on the panel's choices → WTP per level, reservation price, posteriors.

Preference space (the pre-registered primary):
  U_ijt = β_i·x_ij − exp(θ_i)·price_ij/s + ε,   NONE: U = asc_i,   s = the price scale (a power of 10)
  (β_i, θ_i, asc_i) ~ MVN(μ0 + Γ′z_i, Σ),  z_i = segment, high-anchor and paraphrase dummies,
  Σ = diag(τ) Ω diag(τ), Ω ~ LKJ(2), τ ~ HalfNormal(1); non-centred; numpyro NUTS.
A unit is one call (respondent). WTP per level = s·β/exp(θ); reservation price for our configuration
p* = max(0, s·(β·x_ours − asc)/exp(θ)). Segment summaries are archetype-post-stratified medians per draw.
--wtp-space refits with U = λ(w·x − price/s) as the check (Sonnier, Ainslie & Otter 2007).
Fallback (no numpyro, no convergence after the larger run, or --fallback): conditional logit with
segment/arm interactions by maximum likelihood; intervals from a persona bootstrap.
--recovery-check simulates respondents with known part-worths on this design (needs panel/manifest.csv)
and reports how well the estimator recovers them; run it before registering.

  conjoint_fit.py --study S [--warmup 800 --samples 800 --chains 2] [--wtp-space] [--recovery-check] [--fallback]

Writes panel/data/{posteriors.npz, units.csv}, panel/results/{conjoint.json, market_simulator.csv} and
merges the panel keys into panel/results/summary.json.
"""
from __future__ import annotations

import json
import math

import numpy as np
import pandas as pd

from common import Study, merge_summary, study_arg


class Data:
    def __init__(self, st: Study):
        cj = st.cfg["conjoint"]
        self.st, self.cj, self.attrs = st, cj, cj["attributes"]
        self.nonprice = [a for a in self.attrs if a != "price"]
        self.cols = [f"{a}={l}" for a in self.nonprice for l in range(1, len(self.attrs[a]))]
        self.P = len(self.cols)
        self.prices = np.array(self.attrs["price"], float)
        self.scale = 10 ** math.floor(math.log10(np.median(self.prices)))
        des = pd.read_csv(st.root / "panel/design.csv")
        self.T = int(des[des.task_type == "random"].task.max())
        self.A = int(des.alt.max())
        self.lv = {(int(r["version"]), int(r["task"]), int(r["alt"])): r for r in des.to_dict("records")}

    def x_of(self, levels: dict):
        v = np.zeros(self.P)
        for a in self.nonprice:
            l = int(levels.get(a, 0))
            if l > 0:
                v[self.cols.index(f"{a}={l}")] = 1.0
        return v

    def alt(self, version, task, alt):
        r = self.lv[(0 if task > self.T else int(version), int(task), alt)]
        return self.x_of({a: r[f"{a}_lvl"] for a in self.nonprice}), self.prices[r["price_lvl"]]

    def build(self, ch: pd.DataFrame):
        est = ch[ch.task_id <= self.T]
        self.units = est.rid.unique()
        idx = {u: k for k, u in enumerate(self.units)}
        N, T = len(self.units), est.groupby("rid").size().max()
        self.X, self.pr = np.zeros((N, T, self.A, self.P)), np.zeros((N, T, self.A))
        self.y, self.m = np.zeros((N, T), int), np.zeros((N, T), bool)
        pos = dict.fromkeys(self.units, 0)
        for r in est.itertuples():
            i, t = idx[r.rid], pos[r.rid]
            pos[r.rid] += 1
            for a in range(self.A):
                x, p = self.alt(r.version, r.task_id, a + 1)
                self.X[i, t, a], self.pr[i, t, a] = x, p / self.scale
            self.y[i, t], self.m[i, t] = r.chosen, True
        meta = est.groupby("rid").first().loc[self.units, ["persona", "segment", "archetype", "anchor", "paraphrase"]].reset_index()
        self.meta = meta
        segs, anchors, npar = self.st.segments, sorted(self.cj["anchors"]), self.cj.get("paraphrases", 2)
        Z = [(meta.segment == s).astype(float) for s in segs[1:]]
        Z += [(meta.anchor.astype(float) == float(x)).astype(float) for x in anchors[1:]]
        Z += [(meta.paraphrase == p).astype(float) for p in range(2, npar + 1)]
        Z = np.column_stack(Z) if Z else np.zeros((N, 0))
        self.Z = Z[:, Z.std(0) > 0] if len(Z) else Z         # drop dummies that never vary (a single-cell run)
        w = np.zeros(N)
        for (s, a), g in meta.groupby(["segment", "archetype"]):
            w[g.index] = self.st.archetype_share(s).get(a, 0) / len(g)
        self.w = w
        return self


def hb_model(X, pr, y, m, Z, P, wtp_space=False):
    import jax.numpy as jnp
    import numpyro
    import numpyro.distributions as dist
    N, T, A, _ = X.shape
    Kr, Kz = P + 2, Z.shape[1]
    mu0 = numpyro.sample("mu0", dist.Normal(jnp.zeros(Kr), 2.0 * jnp.ones(Kr)))
    G = numpyro.sample("G", dist.Normal(jnp.zeros((Kz, Kr)), jnp.ones((Kz, Kr))))
    tau = numpyro.sample("tau", dist.HalfNormal(jnp.ones(Kr)))
    L = numpyro.sample("L", dist.LKJCholesky(Kr, 2.0))
    z = numpyro.sample("z", dist.Normal(jnp.zeros((N, Kr)), 1.0))
    b = mu0 + Z @ G + z @ (L * tau[:, None]).T
    beta, theta, asc = b[:, :P], b[:, P], b[:, P + 1]
    if wtp_space:
        lam = jnp.exp(theta)
        ua = lam[:, None, None] * (jnp.einsum("ntap,np->nta", X, beta) - pr)
        un = lam[:, None] * asc[:, None] * jnp.ones((N, T))
    else:
        ua = jnp.einsum("ntap,np->nta", X, beta) - jnp.exp(theta)[:, None, None] * pr
        un = asc[:, None] * jnp.ones((N, T))
    u = jnp.concatenate([ua, un[..., None]], -1)
    with numpyro.handlers.mask(mask=jnp.asarray(m)):
        numpyro.sample("y", dist.Categorical(logits=u), obs=jnp.asarray(y))


def fit_hb(d: Data, wtp_space, warmup, samples, chains, seed=0):
    import numpyro
    numpyro.set_host_device_count(chains)
    import jax
    from numpyro.diagnostics import summary
    from numpyro.infer import MCMC, NUTS
    mc = MCMC(NUTS(hb_model, target_accept_prob=0.85), num_warmup=warmup, num_samples=samples, num_chains=chains,
              chain_method="parallel", progress_bar=False)
    mc.run(jax.random.PRNGKey(seed), d.X, d.pr, d.y, d.m, d.Z, d.P, wtp_space)
    s = mc.get_samples()
    diag = summary(mc.get_samples(group_by_chain=True), group_by_chain=True)
    keys = [k for k in ("mu0", "G", "tau") if k in diag and np.size(diag[k]["r_hat"])]
    conv = {"rhat_max": float(max(np.nanmax(diag[k]["r_hat"]) for k in keys)),
            "ess_min": float(min(np.nanmin(diag[k]["n_eff"]) for k in keys)),
            "divergences": int(np.asarray(mc.get_extra_fields()["diverging"]).sum())}
    Lt = np.asarray(s["L"]) * np.asarray(s["tau"])[:, :, None]
    b = np.asarray(s["mu0"])[:, None, :] + np.einsum("nk,skr->snr", d.Z, np.asarray(s["G"])) + np.einsum("snk,srk->snr", np.asarray(s["z"]), Lt)
    return b, conv


def clogit(d: Data, rng, boot=200):
    """Fallback: conditional logit, every coefficient interacted with Z, by ML with the exact gradient;
    a persona bootstrap gives the intervals."""
    from scipy.optimize import minimize
    N, T, A, P = d.X.shape
    Kr, Kz = P + 2, d.Z.shape[1]
    Z1 = np.column_stack([np.ones(N), d.Z])                       # (N, 1+Kz): intercept + interactions
    Y = np.zeros((N, T, A + 1))
    np.put_along_axis(Y, d.y[..., None], 1.0, -1)

    def nll(th, rows):
        G = th.reshape(1 + Kz, Kr)
        b = Z1[rows] @ G
        sc = np.exp(b[:, P])
        u = np.concatenate([np.einsum("ntap,np->nta", d.X[rows], b[:, :P]) - sc[:, None, None] * d.pr[rows],
                            np.repeat(b[:, P + 1][:, None, None], T, 1)], -1)
        u -= u.max(-1, keepdims=True)
        pr = np.exp(u)
        pr /= pr.sum(-1, keepdims=True)
        m = d.m[rows][..., None]
        r = (Y[rows] - pr) * m                                     # d ll / d u
        ll = (np.log(np.clip(pr, 1e-300, None)) * Y[rows] * m).sum()
        gb = np.zeros((len(rows), Kr))
        gb[:, :P] = np.einsum("nta,ntap->np", r[..., :A], d.X[rows])
        gb[:, P] = -(r[..., :A] * d.pr[rows]).sum((1, 2)) * sc
        gb[:, P + 1] = r[..., A].sum(1)
        return -ll, -(Z1[rows].T @ gb).ravel()

    th0 = minimize(nll, np.zeros((1 + Kz) * Kr), args=(np.arange(N),), jac=True, method="L-BFGS-B").x
    pers = d.meta.persona.to_numpy()
    up = np.unique(pers)
    draws = []
    for _ in range(boot):
        rows = np.concatenate([np.where(pers == p)[0] for p in rng.choice(up, len(up))])
        draws.append(minimize(nll, th0, args=(rows,), jac=True, method="L-BFGS-B").x)
    G = np.array(draws).reshape(boot, 1 + Kz, Kr)
    b = np.einsum("nk,skr->snr", Z1, G)
    return b, {"method": "conditional logit fallback", "bootstrap": boot}


def wmed(v, w):
    o = np.argsort(v)
    cw = np.cumsum(w[o])
    return v[o][np.searchsorted(cw, 0.5 * cw[-1])]


def summarise(d: Data, b, wtp_space=False):
    P = d.P
    beta, theta, asc = b[..., :P], b[..., P], b[..., P + 1]
    if wtp_space:
        wl, none = d.scale * beta, d.scale * asc
    else:
        wl, none = d.scale * beta / np.exp(theta)[..., None], d.scale * asc / np.exp(theta)
    pstar = np.maximum(0.0, wl @ d.x_of(d.cj["our_config"]) - none)
    seg = d.meta.segment.to_numpy()
    res = {}
    for s in d.st.segments:
        m = seg == s
        if not m.any():
            continue
        meds = np.array([wmed(pstar[k, m], d.w[m]) for k in range(len(pstar))])
        pooled = pstar[:, m].ravel()
        res[s] = {"median": float(meds.mean()), "ci90": [float(np.quantile(meds, .05)), float(np.quantile(meds, .95))],
                  "p25": float(np.quantile(pooled, .25)), "p75": float(np.quantile(pooled, .75)),
                  "never_buy_share": float((pstar[:, m] == 0).mean())}
    segw = d.st.segment_share()
    lvl = []
    for j, c in enumerate(d.cols):
        a, l = c.split("=")
        bys = {s: np.array([wmed(wl[k, seg == s, j], d.w[seg == s]) for k in range(len(wl))]) for s in d.st.segments if (seg == s).any()}
        pooled = sum(segw[s] * v for s, v in bys.items()) / sum(segw[s] for s in bys)
        lvl.append({"attribute": a, "level": d.attrs[a][int(l)],
                    "pooled": {"mean": float(pooled.mean()), "ci90": [float(np.quantile(pooled, .05)), float(np.quantile(pooled, .95))]},
                    "by_segment": {s: float(v.mean()) for s, v in bys.items()}})
    return res, lvl, pstar


def holdout(d: Data, b, ch):
    bm, P = b.mean(0), d.P
    idx = {u: k for k, u in enumerate(d.units)}
    hit = n = 0
    for r in ch[(ch.task_id > d.T) & (ch.task_id <= d.T + 2)].itertuples():
        if r.rid not in idx:
            continue
        i = idx[r.rid]
        u = [bm[i, :P] @ x - np.exp(bm[i, P]) * p / d.scale for x, p in (d.alt(r.version, r.task_id, a + 1) for a in range(d.A))]
        hit += int(np.argmax(u + [bm[i, P + 1]]) == r.chosen)
        n += 1
    return hit / n if n else None


def arm_effects(d: Data, pstar):
    pm = pd.DataFrame({"persona": d.meta.persona, "anchor": d.meta.anchor.astype(float), "paraphrase": d.meta.paraphrase, "p": pstar.mean(0)})
    out, a = {}, sorted(pm.anchor.unique())
    if len(a) >= 2:
        w = pm.groupby(["persona", "anchor"]).p.mean().unstack()
        diff = (w[a[-1]] - w[a[0]]).dropna()
        out["anchor"] = {"low": a[0], "high": a[-1], "median_paired_diff": float(diff.median()), "share_higher": float((diff > 0).mean()),
                         "median_low": float(w[a[0]].median()), "median_high": float(w[a[-1]].median())}
    if pm.paraphrase.nunique() >= 2:
        w = pm.groupby(["persona", "paraphrase"]).p.mean().unstack()
        diff = (w[2] - w[1]).dropna()
        out["paraphrase"] = {"median_paired_diff": float(diff.median()), "relative": float(diff.median() / max(w[1].median(), 1e-9))}
    return out


def market_curve(d: Data, b):
    P, xo, seg = d.P, d.x_of(d.cj["our_config"]), d.meta.segment.to_numpy()
    grid = sorted(set(np.round(np.geomspace(d.prices.min() / 2, d.prices.max() * 2, 25), 0)))
    rows = []
    for s in d.st.segments:
        m = seg == s
        if not m.any():
            continue
        w = d.w[m] / d.w[m].sum()
        for p in grid:
            u = b[:, m, :P] @ xo - np.exp(b[:, m, P]) * p / d.scale
            buy = ((1 / (1 + np.exp(b[:, m, P + 1] - u))) * w).sum(1)
            rows.append({"segment": s, "price": p, "buy_share": float(buy.mean()), "revenue_per_respondent": float(buy.mean() * p)})
    return pd.DataFrame(rows)


def recovery(st: Study, a):
    rng = np.random.default_rng(3)
    d = Data(st)
    man = pd.read_csv(st.root / "panel/manifest.csv")
    true_beta = np.concatenate([np.linspace(0.3, 1.0, len(d.attrs[x]) - 1) for x in d.nonprice])
    rows = []
    for r in man.itertuples():
        bi, th, asc = true_beta + rng.normal(0, 0.3, d.P), rng.normal(0, 0.2), 0.5 + rng.normal(0, 0.3)
        for t in range(1, d.T + 1):
            u = [bi @ x - np.exp(th) * p / d.scale for x, p in (d.alt(r.version, t, k + 1) for k in range(d.A))] + [asc]
            rows.append({"rid": r.rid, "persona": r.persona, "segment": r.segment, "archetype": r.archetype, "anchor": r.anchor,
                         "paraphrase": r.paraphrase, "version": r.version, "task_id": t,
                         "chosen": int(np.argmax(np.array(u) + rng.gumbel(size=len(u)))), "keep": True})
    d.build(pd.DataFrame(rows))
    b, conv = fit_hb(d, False, a.warmup, a.samples, a.chains)
    err = np.abs(b[..., :d.P].mean((0, 1)) - true_beta)
    print(json.dumps({"units": int(len(d.units)), "max_abs_error_partworth": float(err.max()), "mean_abs_error": float(err.mean()), **conv}, indent=1))


def main():
    ap = study_arg(__doc__.splitlines()[0])
    ap.add_argument("--warmup", type=int, default=800)
    ap.add_argument("--samples", type=int, default=800)
    ap.add_argument("--chains", type=int, default=2)
    ap.add_argument("--wtp-space", action="store_true")
    ap.add_argument("--recovery-check", action="store_true")
    ap.add_argument("--fallback", action="store_true", help="skip HB; conditional logit + persona bootstrap")
    a = ap.parse_args()
    st = Study(a.study)
    if a.recovery_check:
        return recovery(st, a)
    allch = pd.read_csv(st.root / "panel/data/choices.csv")
    allch = allch[allch.keep]
    d = Data(st).build(allch)
    try:
        if a.fallback:
            raise ImportError("fallback requested")
        import numpyro  # noqa: F401
        b, conv = fit_hb(d, False, a.warmup, a.samples, a.chains)
        if conv["rhat_max"] > 1.05 or conv["ess_min"] < 200:
            print(f"not converged {conv}; rerunning 4 chains × 1500")
            b, conv = fit_hb(d, False, 1500, 1500, 4)
        if conv["rhat_max"] > 1.05 or conv["ess_min"] < 200:
            raise RuntimeError(f"HB did not converge: {conv}")
        method = "HB-MNL preference space (numpyro NUTS)"
    except (ImportError, RuntimeError) as e:
        print(f"fallback: {e}")
        b, conv = clogit(d, np.random.default_rng(1))
        method = "conditional logit with segment/arm interactions (fallback)"
    res, lvl, pstar = summarise(d, b)
    hit = holdout(d, b, allch)
    arms = arm_effects(d, pstar)
    curve = market_curve(d, b)
    curve.to_csv(st.path("panel", "results", "market_simulator.csv"), index=False)
    keep = np.linspace(0, len(b) - 1, min(len(b), 400)).astype(int)
    np.savez_compressed(st.path("panel", "data", "posteriors.npz"), b=b[keep], cols=np.array(d.cols), scale=d.scale)
    d.meta.assign(weight=d.w).to_csv(st.path("panel", "data", "units.csv"), index=False)
    wtp_space = None
    if a.wtp_space:
        bw, _ = fit_hb(d, True, a.warmup, a.samples, a.chains)
        wtp_space = {s: v["median"] for s, v in summarise(d, bw, wtp_space=True)[0].items()}
    revmax = {s: g.loc[g.revenue_per_respondent.idxmax()].to_dict() for s, g in curve.groupby("segment")}
    body = {"method": method, "convergence": conv, "price_scale": d.scale, "n_units": int(len(d.units)),
            "reservation_price": res, "wtp_per_level": lvl, "holdout_hit_rate": hit, "holdout_chance_rate": 1 / (d.A + 1),
            "arm_effects": arms, "wtp_space_median": wtp_space, "simulator_revenue_max": revmax}
    st.path("panel", "results", "conjoint.json").write_text(json.dumps(body, indent=2, default=float))
    merge_summary(st, "panel", body, ["Simulated-response estimates are exploratory hypotheses, not observed buyer willingness to pay or a demand forecast."])
    print(method, conv)
    print(pd.DataFrame(res).T.round(1).to_string())
    print(pd.DataFrame([{"attribute": r["attribute"], "level": r["level"], "wtp": r["pooled"]["mean"]} for r in lvl]).round(1).to_string(index=False))
    print(f"holdout hit rate {hit:.3f} (chance {1 / (d.A + 1):.2f}); arms {json.dumps(arms, default=float)}")


if __name__ == "__main__":
    main()
