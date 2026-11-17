"""Phase 4b · panel responses → exclusions, long choices, Van Westendorp, Gabor-Granger.

Exclusion rules (the pre-registration's §6), applied mechanically:
  E1 dominance       did not pick the dominant option (B) in the check task         → all analyses
  E2 straightlining  the same letter A/B/C… in every random task (always-NONE kept)  → all analyses
  E3 GG monotonicity would_buy at a higher price but not a lower one, or likelihood
                     rising > 10 points with price                                    → Gabor-Granger only
  E4 malformed       no parseable reply after retry, or fewer valid choices than tasks → all analyses
  E5 VW order        not too_cheap ≤ cheap ≤ expensive ≤ too_expensive                → Van Westendorp only
A binary-only Gabor-Granger (E3 on would_buy alone) is written beside the registered one, labelled
exploratory: the likelihood clause drops buyers who read a low price as "too cheap to be serious".

Writes panel/data/{exclusions,choices,stated}.csv, panel/results/{psm,gabor_granger,gabor_granger_binary}.csv.

  panel_analyze.py --study S
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from common import Study, study_arg


def crossing(grid, a, b):
    """Price where decreasing curve a meets increasing curve b; the geometric midpoint if they touch over an interval."""
    d = a - b
    pos, neg = np.where(d > 1e-12)[0], np.where(d < -1e-12)[0]
    if not len(pos) or not len(neg) or not (pos < neg[0]).any():
        return None
    i, j = pos[pos < neg[0]].max(), neg[0]
    if j == i + 1:
        return float(grid[i] + (grid[j] - grid[i]) * d[i] / (d[i] - d[j]))
    return float(np.sqrt(grid[i + 1] * grid[j - 1]))


def psm(df):
    lo, hi = max(df.too_cheap.min(), 0.5), max(df.too_expensive.max(), 1)
    grid = np.exp(np.linspace(np.log(lo), np.log(hi * 1.5), 800))
    cdf = lambda c: np.array([(df[c] <= g).mean() for g in grid])
    tc, ch, ex, te = cdf("too_cheap"), cdf("cheap"), cdf("expensive"), cdf("too_expensive")
    too_cheap, cheap = 1 - tc, 1 - ch
    return {"pmc": crossing(grid, too_cheap, 1 - cheap), "pme": crossing(grid, 1 - ex, te),
            "opp": crossing(grid, too_cheap, te), "ipp": crossing(grid, cheap, ex), "n": int(len(df)),
            "median_expensive": float(df.expensive.median()), "median_too_expensive": float(df.too_expensive.median())}


def gabor(df, prices):
    curve = [{"price": p, "purchase_intent": float(df[f"gg_buy_{p}"].astype(float).mean()),
              "mean_likelihood": float(df[f"gg_lik_{p}"].mean())} for p in prices]
    return curve, max(curve, key=lambda c: c["price"] * c["purchase_intent"])["price"]


def pkey(p):
    return int(p) if float(p).is_integer() else p


def main():
    ap = study_arg(__doc__.splitlines()[0])
    a = ap.parse_args()
    st = Study(a.study)
    cj = st.cfg["conjoint"]
    prices = [pkey(p) for p in cj["attributes"]["price"]]
    des = pd.read_csv(st.root / "panel/design.csv")
    T = int(des[des.task_type == "random"].task.max())
    A = int(des.alt.max())
    letters = {chr(65 + i): i for i in range(A)} | {"NONE": A}
    man = pd.read_csv(st.root / "panel/manifest.csv")
    excl, ch, rows = [], [], []
    for r in man.itertuples():
        f = st.root / f"panel/responses/{r.rid}.json"
        body = json.loads(f.read_text()).get("response") if f.exists() else None
        if body is None:
            if f.exists() or (st.root / f"panel/responses/{r.rid}.failed.json").exists():
                excl.append({"rid": r.rid, "rule": "E4", "scope": "all", "detail": "no parseable reply after retry"})
            continue
        order = json.loads(r.task_order)
        hard, soft, c = [], [], {}
        for k, v in (body.get("choices") or {}).items():
            v = str(v).strip().upper().replace("OPTION ", "")
            if str(k).isdigit() and v in letters and 1 <= int(k) <= len(order):
                c[int(k)] = v
        if len(c) < len(order):
            hard.append(("E4", f"{len(c)} valid choices of {len(order)}"))
        by_task = {order[p - 1]: v for p, v in c.items()}
        if by_task.get(T + 3) not in (None, "B"):
            hard.append(("E1", f"chose {by_task[T + 3]} in the dominance check"))
        rnd = [by_task.get(t) for t in range(1, T + 1)]
        if all(x is not None for x in rnd) and len(set(rnd)) == 1 and rnd[0] != "NONE":
            hard.append(("E2", f"always {rnd[0]}"))
        vw = body.get("vw") or {}
        try:
            v4 = [float(vw[k]) for k in ("too_cheap", "cheap", "expensive", "too_expensive")]
        except Exception:
            v4 = None
        if v4 is None or not (v4[0] <= v4[1] <= v4[2] <= v4[3]):
            soft.append(("E5", f"VW {v4}"))
        gg = []
        for g in body.get("gg") or []:
            try:
                gg.append((float(g["price"]), bool(g["would_buy"]), float(g.get("likelihood", np.nan))))
            except Exception:
                pass
        gg.sort()
        gg_ok = len(gg) == len(prices)
        gg_bin = gg_ok
        if gg_ok:
            buys, lk = [g[1] for g in gg], [g[2] for g in gg]
            nonmono = any(buys[k] and not buys[j] for j in range(len(gg)) for k in range(j + 1, len(gg)))
            gg_bin = not nonmono
            if nonmono:
                gg_ok = False
                soft.append(("E3", "would_buy at a higher price, not at a lower"))
            elif any(lk[k] - lk[j] > 10 for j in range(len(gg)) for k in range(j + 1, len(gg))):
                gg_ok = False
                soft.append(("E3", "likelihood rises with price"))
        else:
            soft.append(("E3", f"{len(gg)} GG prices of {len(prices)}"))
        excl += [{"rid": r.rid, "rule": rule, "scope": "all", "detail": d} for rule, d in hard]
        excl += [{"rid": r.rid, "rule": rule, "scope": "VW" if rule == "E5" else "GG", "detail": d} for rule, d in soft]
        keep = not hard
        for t, v in by_task.items():
            ch.append({"rid": r.rid, "persona": r.persona, "segment": r.segment, "archetype": r.archetype, "anchor": r.anchor,
                       "paraphrase": r.paraphrase, "version": r.version, "task_id": t, "chosen": letters[v], "keep": keep})
        row = {"rid": r.rid, "persona": r.persona, "segment": r.segment, "archetype": r.archetype, "anchor": r.anchor,
               "paraphrase": r.paraphrase, "keep": keep, "vw_ok": keep and not any(s[0] == "E5" for s in soft),
               "gg_ok": keep and gg_ok, "gg_binary_ok": keep and gg_bin, "rationale": body.get("rationale", "")}
        if v4:
            row.update(dict(zip(("too_cheap", "cheap", "expensive", "too_expensive"), v4)))
        for p, b, l in gg:
            row[f"gg_buy_{pkey(p)}"], row[f"gg_lik_{pkey(p)}"] = b, l
        rows.append(row)
    pd.DataFrame(excl, columns=["rid", "rule", "scope", "detail"]).to_csv(st.path("panel", "data", "exclusions.csv"), index=False)
    pd.DataFrame(ch).to_csv(st.path("panel", "data", "choices.csv"), index=False)
    sdf = pd.DataFrame(rows)
    sdf.to_csv(st.path("panel", "data", "stated.csv"), index=False)
    out_psm, out_gg, out_bin = [], [], []
    arms = ["pooled"] + [f"a{x}" for x in cj["anchors"]] + [f"v{p}" for p in range(1, cj.get("paraphrases", 2) + 1)]
    for seg in st.segments + ["all"]:
        for arm in arms:
            d = sdf if seg == "all" else sdf[sdf.segment == seg]
            if arm.startswith("a"):
                d = d[d.anchor.astype(str) == arm[1:]]
            elif arm.startswith("v"):
                d = d[d.paraphrase == int(arm[1:])]
            dv, dg, db = d[d.vw_ok], d[d.gg_ok], d[d.gg_binary_ok]
            if len(dv) >= 10:
                out_psm.append({"segment": seg, "arm": arm, **psm(dv)})
            for src, tgt in ((dg, out_gg), (db, out_bin)):
                if len(src) >= 10:
                    curve, best = gabor(src, prices)
                    tgt += [{"segment": seg, "arm": arm, **c, "revenue_max_price": best, "n": int(len(src))} for c in curve]
    pd.DataFrame(out_psm).to_csv(st.path("panel", "results", "psm.csv"), index=False)
    pd.DataFrame(out_gg).to_csv(st.path("panel", "results", "gabor_granger.csv"), index=False)
    pd.DataFrame(out_bin).to_csv(st.path("panel", "results", "gabor_granger_binary.csv"), index=False)
    ex = pd.DataFrame(excl)
    n = len(sdf)
    print(f"{n} replies of {len(man)}; kept for choice {int(sdf.keep.sum()) if n else 0}, VW {int(sdf.vw_ok.sum()) if n else 0}, GG {int(sdf.gg_ok.sum()) if n else 0}")
    print("exclusions by rule:", ex.groupby("rule").size().to_dict() if len(ex) else "none")
    if out_psm:
        print(pd.DataFrame(out_psm).query("arm == 'pooled'").round(1).to_string(index=False))


if __name__ == "__main__":
    main()
