"""Phase 6 · score and tune packaging proposals on CONTRIBUTION after people time, under every level lens.

Reads synthesis/proposals.yaml (templates/proposals.yaml), cost/results/summary.json, and whichever
demand sources exist:
  panel             HB posteriors (panel/data/posteriors.npz): logit share of each visible tier vs NONE
                    (and vs mapped competitors), at the silicon level (k = 1)
  panel_calibrated  the same with price sensitivity × lenses.calibration_ratio (buyers pay k× less)
  evc               the value model: a scenario buys the visible tier with the largest surplus
                    capture × EVC(tier) − price, if positive; EVC(tier) = reference-alternative cost (when the
                    tier replaces it) + value of the tier's features (value_mc.Engine, caps applied)
A tier is visible to a segment when its `segments` list includes it (usage fence) or it has none
(capability fence: buyers self-select). Contribution per customer = price × (1 − channel share) −
variable cost − people cost − the tier's extra people_hours × rate.

For each proposal it searches the tiers' price grids (ascending across capability tiers unless
--no-monotone) and reports the best prices under each lens and a ROBUST pick: the prices maximising the
worst ratio of contribution to that lens's own best. Index per 100 addressable customers; a comparison,
not a forecast. Output: synthesis/data/proposals_eval.csv, synthesis/results/packages.json.

  optimize_packages.py --study S [--draws 60] [--max-combos 4000]
"""
from __future__ import annotations

import itertools
import json

import numpy as np
import pandas as pd

from common import Study, read_summary, study_arg


class PanelDemand:
    def __init__(self, st: Study, draws: int):
        z = np.load(st.root / "panel/data/posteriors.npz", allow_pickle=False)
        b, self.cols, self.scale = z["b"], list(z["cols"]), float(z["scale"])
        self.b = b[np.linspace(0, len(b) - 1, min(draws, len(b))).astype(int)]
        self.P = len(self.cols)
        u = pd.read_csv(st.root / "panel/data/units.csv")
        self.seg, self.w = u.segment.to_numpy(), u.weight.to_numpy()

    def x(self, cfg):
        v = np.zeros(self.P)
        for a, l in (cfg or {}).items():
            if int(l) > 0 and f"{a}={int(l)}" in self.cols:
                v[self.cols.index(f"{a}={int(l)}")] = 1.0
        return v

    def shares(self, seg, offers, k=1.0, competitors=()):
        m = self.seg == seg
        if not m.any() or self.w[m].sum() == 0:
            return None
        b, w = self.b[:, m], self.w[m] / self.w[m].sum()
        U = [b[..., :self.P] @ self.x(cfg) - np.exp(b[..., self.P]) * k * p / self.scale for cfg, p in list(offers) + list(competitors)]
        U = np.stack(U + [b[..., self.P + 1]], -1)
        U -= U.max(-1, keepdims=True)
        Pr = np.exp(U)
        Pr /= Pr.sum(-1, keepdims=True)
        return np.einsum("snj,n->sj", Pr, w).mean(0)[: len(offers)]


class EvcDemand:
    def __init__(self, st: Study, capture: float):
        from value_mc import Engine
        scen = pd.read_parquet(st.root / "value/data/scenarios.parquet")
        self.eng = Engine(st, st.yaml("value_drivers.yaml"), scen, st.cfg["scenarios"].get("seed", 1))
        self.seg, self.ref = scen.segment.to_numpy(), scen.reference_cost.to_numpy()
        self.capture, self.cache = capture, {}

    def wtp(self, tier):
        feats = tier.get("features", "all")
        key = ("all" if feats == "all" else tuple(sorted(feats)), tier.get("replaces_reference", True))
        if key not in self.cache:
            en = set(self.eng.players) if feats == "all" else set(feats)
            self.cache[key] = self.capture * (self.eng.total(en) + (self.ref if key[1] else 0))
        return self.cache[key]

    def shares(self, seg, tiers, prices):
        m = self.seg == seg
        if not m.any():
            return None
        surplus = np.stack([self.wtp(t)[m] - p for t, p in zip(tiers, prices)], -1)
        best, buy = surplus.argmax(-1), surplus.max(-1) > 0
        return np.array([((best == j) & buy).mean() for j in range(len(tiers))])


def main():
    ap = study_arg(__doc__.splitlines()[0])
    ap.add_argument("--draws", type=int, default=60)
    ap.add_argument("--max-combos", type=int, default=4000)
    ap.add_argument("--no-monotone", action="store_true")
    a = ap.parse_args()
    st = Study(a.study)
    props = st.yaml("synthesis/proposals.yaml")
    cost = read_summary(st, "cost")
    gaps = [] if cost else ["no cost phase: contribution = revenue (zero variable, people and channel cost)"]
    chan = (cost or {}).get("channel_share_of_price", 0.0)
    var = {s: (cost or {}).get("variable_per_customer", {}).get(s, {}).get("point", 0.0) for s in st.segments}
    ppl = {s: (cost or {}).get("people_per_customer", {}).get(s, {}).get("eur", 0.0) for s in st.segments}
    rate = ((st.yaml("costs.yaml", required=False) or {}).get("people") or {}).get("hourly_rate", 0)
    fixed = (cost or {}).get("fixed_platform", 0.0)
    lens_cfg, lenses = st.cfg.get("lenses", {}), {}
    if (st.root / "panel/data/posteriors.npz").exists():
        pdm = PanelDemand(st, a.draws)
        lenses["panel"] = ("panel", 1.0)
        if lens_cfg.get("calibration_ratio"):
            lenses["panel_calibrated"] = ("panel", float(lens_cfg["calibration_ratio"]))
    if (st.root / "value/data/scenarios.parquet").exists():
        edm = EvcDemand(st, float(lens_cfg.get("evc_capture", 0.3)))
        lenses["evc"] = ("evc", None)
    if not lenses:
        raise SystemExit("no demand source: run the value phase (value_mc.py) and/or the panel (conjoint_fit.py) first")
    segw = st.segment_share()
    comps = [(c.get("config"), c["price"]) for c in props.get("competitors") or [] if c.get("config")]

    def evaluate(tiers, prices, lens):
        kind, k = lenses[lens]
        rev = con = buy = 0.0
        mix = {}
        for s in st.segments:
            vis = [j for j, t in enumerate(tiers) if not t.get("segments") or s in t["segments"]]
            if not vis:
                continue
            sh = (pdm.shares(s, [(tiers[j].get("config"), prices[j]) for j in vis], k, comps) if kind == "panel"
                  else edm.shares(s, [tiers[j] for j in vis], [prices[j] for j in vis]))
            if sh is None:
                continue
            c = [prices[j] * (1 - chan) - var[s] - ppl[s] - float(tiers[j].get("people_hours", 0)) * rate for j in vis]
            rev += segw[s] * sum(sh[i] * prices[j] for i, j in enumerate(vis))
            con += segw[s] * sum(sh[i] * c[i] for i in range(len(vis)))
            buy += segw[s] * sh.sum()
            mix[s] = {tiers[j]["name"]: round(float(sh[i]), 3) for i, j in enumerate(vis)}
        return {"revenue_per_100": 100 * rev, "contribution_per_100": 100 * con, "buy_share": buy,
                "contribution_per_buyer": con / buy if buy else 0.0, "mix": mix}

    rows, out, rng = [], {}, np.random.default_rng(11)
    for P in props["proposals"]:
        tiers = P["tiers"]
        combos = list(itertools.product(*[t["price_grid"] for t in tiers]))
        if all(not t.get("segments") for t in tiers) and not a.no_monotone:
            combos = [c for c in combos if all(c[i] < c[i + 1] for i in range(len(c) - 1))]
        if len(combos) > a.max_combos:
            combos = [combos[i] for i in rng.choice(len(combos), a.max_combos, replace=False)]
        res = {l: [evaluate(tiers, c, l) for c in combos] for l in lenses}
        best = {l: max(range(len(combos)), key=lambda i: res[l][i]["contribution_per_100"]) for l in lenses}
        ratio = np.array([[res[l][i]["contribution_per_100"] / max(res[l][best[l]]["contribution_per_100"], 1e-9) for l in lenses] for i in range(len(combos))])
        robust = int(np.argmax(ratio.min(1)))
        out[P["id"]] = {"name": P["name"], "tiers": [t["name"] for t in tiers]}
        for tag, i in [*((f"best_{l}", best[l]) for l in lenses), ("robust", robust)]:
            prices = dict(zip([t["name"] for t in tiers], combos[i]))
            out[P["id"]][tag] = {"prices": prices, **{l: res[l][i] for l in lenses}}
            for l in lenses:
                r = res[l][i]
                cpb = r["contribution_per_buyer"]
                rows.append({"proposal": P["id"], "pick": tag, "lens": l, "prices": json.dumps(prices),
                             "revenue_per_100": round(r["revenue_per_100"], 1), "contribution_per_100": round(r["contribution_per_100"], 1),
                             "buy_share": round(r["buy_share"], 3),
                             "customers_to_carry_fixed": int(np.ceil(fixed / cpb)) if cpb > 0 and fixed else None, "mix": json.dumps(r["mix"])})
    df = pd.DataFrame(rows)
    df.to_csv(st.path("synthesis", "data", "proposals_eval.csv"), index=False)
    st.path("synthesis", "results", "packages.json").write_text(json.dumps({"lenses": {k: v[1] for k, v in lenses.items()}, "gaps": gaps, "proposals": out}, indent=2, default=float))
    print(df[df.pick == "robust"].drop(columns=["mix", "pick"]).to_string(index=False))
    for g in gaps:
        print("GAP:", g)


if __name__ == "__main__":
    main()
