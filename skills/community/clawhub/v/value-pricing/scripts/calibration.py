"""Phase 4b · level-bias calibration: replicate a published human WTP study on the panel's model.

The reference benchmark is Brand, Israeli & Ngwe (HBS WP 23-062): toothpaste, fluoride WTP $3.27 in the
pilot and $2.60 in Study 1A. Reproduce THEIR choice sets and THEIR verbatim prompt template from the
paper's web appendix; this script ships neither, because a paraphrase is a different instrument.

  calibration.py --study S build --sets sets.csv --template template.txt --reps 20
  llm_batch.py   --study S --dir panel/calibration --free-text --confirm-external-transfer
  calibration.py --study S fit --attribute fluoride --human 3.27

sets.csv: set_id, then for each option k in (a, b): k_label (the text a reply names, e.g. a brand),
k_price, k_text (the option as shown) and one 0/1 column per attribute (k_fluoride, ...). template.txt:
the verbatim prompt with {a_text} and {b_text} placeholders (and any other sets.csv column, e.g. {income}).
Replies are coded from their first sentence: the option whose label it names, or NONE for
"neither / none / would not buy". MNL with a no-purchase option: U_k = β·x_k − α·price_k;
WTP = β_attribute / α, bootstrap 90% CI over choice sets. Reports the silicon/human ratio; never apply it.
"""
from __future__ import annotations

import json
import re

import numpy as np
import pandas as pd
from scipy.optimize import minimize

from common import Study, study_arg


def main():
    ap = study_arg(__doc__.splitlines()[0])
    ap.add_argument("action", choices=["build", "fit"])
    ap.add_argument("--sets")
    ap.add_argument("--template")
    ap.add_argument("--reps", type=int, default=20)
    ap.add_argument("--attribute")
    ap.add_argument("--human", type=float)
    ap.add_argument("--name", default="calibration")
    a = ap.parse_args()
    st = Study(a.study)
    d = st.root / "panel" / a.name
    if a.action == "build":
        sets, tpl = pd.read_csv(a.sets), open(a.template).read()
        (d / "prompts").mkdir(parents=True, exist_ok=True)
        rows = []
        for r in sets.to_dict("records"):
            for k in range(a.reps):
                rid = f"s{r['set_id']}_r{k:02d}"
                (d / "prompts" / f"{rid}.txt").write_text(tpl.format(**r))
                rows.append({"rid": rid, "set_id": r["set_id"]})
        pd.DataFrame(rows).to_csv(d / "manifest.csv", index=False)
        sets.to_csv(d / "sets.csv", index=False)
        (d / "system_prompt.txt").write_text("Continue the text.")
        print(f"{len(rows)} prompts → {d}; after reviewing the data, run llm_batch.py with --free-text --confirm-external-transfer")
        return
    sets = pd.read_csv(d / "sets.csv").set_index("set_id")
    attrs = sorted({c[2:] for c in sets.columns if c.startswith("a_") and c not in ("a_label", "a_price", "a_text")})
    man = pd.read_csv(d / "manifest.csv")
    obs = []
    for r in man.itertuples():
        f = d / "responses" / f"{r.rid}.json"
        if not f.exists():
            continue
        first = re.split(r"(?<=[.!?])\s", str(json.loads(f.read_text()).get("raw", "")).strip(), maxsplit=1)[0].lower()
        s = sets.loc[r.set_id]
        hits = [k for k in ("a", "b") if str(s[f"{k}_label"]).lower() in first]
        if re.search(r"\b(neither|none|would not|wouldn't|not buy)\b", first):
            obs.append((r.set_id, 2))
        elif len(hits) == 1:
            obs.append((r.set_id, "ab".index(hits[0])))
    obs = pd.DataFrame(obs, columns=["set_id", "y"])
    if obs.empty:
        raise SystemExit("no coded replies")

    def fit(o):
        X = np.stack([[sets.loc[i, [f"{k}_{x}" for x in attrs]].to_numpy(float) for k in "ab"] for i in o.set_id])
        p = np.stack([[sets.loc[i, f"{k}_price"] for k in "ab"] for i in o.set_id]).astype(float)
        y = o.y.to_numpy()

        def nll(th):
            u = np.concatenate([X @ th[:-2] - th[-2] * p, np.full((len(y), 1), th[-1])], 1)
            u -= u.max(1, keepdims=True)
            return -(u[np.arange(len(y)), y] - np.log(np.exp(u).sum(1))).sum()

        th = minimize(nll, np.r_[np.zeros(len(attrs)), 1.0, 0.0], method="L-BFGS-B").x
        return th[attrs.index(a.attribute)] / th[-2]

    w = fit(obs)
    rng = np.random.default_rng(9)
    ids = obs.set_id.unique()
    boots = [fit(pd.concat([obs[obs.set_id == i] for i in rng.choice(ids, len(ids))])) for _ in range(500)]
    lo, hi = np.quantile(boots, [.05, .95])
    res = {"attribute": a.attribute, "silicon_wtp": float(w), "ci90": [float(lo), float(hi)], "coded_share": len(obs) / max(len(man), 1),
           "human_wtp": a.human, "ratio": float(w / a.human) if a.human else None,
           "ratio_ci90": [float(lo / a.human), float(hi / a.human)] if a.human else None, "applied": False}
    (d / "result.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
