"""Phase 4b · D-efficient choice-based conjoint design → panel/design.csv + panel/design_stats.json.

Attributes and levels come from study.yaml conjoint.attributes (price first; every other attribute's
levels ordered worst → best). V versions × T random tasks × A alternatives + NONE, each version built by
coordinate exchange (Meyer & Nachtsheim 1995; Kuhfeld 2010) minimising the MNL D-error (Huber & Zwerina
1996) under mild utility-balance priors; no identical or dominated alternatives within a task. Plus 2 fixed
holdout tasks (task ids T+1, T+2) and 1 dominance-check task (T+3), the same for every respondent:
in the check, option B is cheapest AND best on every attribute. Seeded and idempotent.
60 versions take a few minutes on one core; --starts 1 for a quick look.

  conjoint_design.py --study S [--starts 3] [--seed 17851]
"""
from __future__ import annotations

import itertools
import json

import numpy as np
import pandas as pd

from common import Study, study_arg


class Design:
    def __init__(self, cfg: dict):
        self.attrs = cfg["attributes"]
        if list(self.attrs)[0] != "price":
            raise SystemExit("study.yaml conjoint.attributes must start with `price`")
        self.names = list(self.attrs)
        self.nlev = [len(self.attrs[a]) for a in self.names]
        self.K = sum(n - 1 for n in self.nlev) + 1
        self.V, self.T, self.A = cfg.get("versions", 60), cfg.get("tasks", 12), cfg.get("alternatives", 3)
        pr = [-0.3 * (i + 1) for i in range(self.nlev[0] - 1)]
        rest = [0.2 * (l + 1) / max(1, n - 1) for n in self.nlev[1:] for l in range(n - 1)]
        self.prior = np.array(pr + rest + [0.0])
        self.none_row = np.zeros((1, self.K))
        self.none_row[0, -1] = 1.0

    def encode(self, lv):
        out, c = np.zeros((lv.shape[0], self.K)), 0
        for j, n in enumerate(self.nlev):
            for l in range(1, n):
                out[:, c] = lv[:, j] == l
                c += 1
        return out

    def info(self, ver, beta):
        I = np.zeros((self.K, self.K))
        for t in range(ver.shape[0]):
            X = np.vstack([self.encode(ver[t]), self.none_row])
            u = X @ beta
            p = np.exp(u - u.max())
            p /= p.sum()
            Z = X - p @ X
            I += (Z * p[:, None]).T @ Z
        return I

    def d_error(self, ver, beta):
        s, ld = np.linalg.slogdet(self.info(ver, beta))
        return np.inf if s <= 0 else float(np.exp(-ld / self.K))

    @staticmethod
    def dominated(a, b):
        return a[0] >= b[0] and all(a[j] <= b[j] for j in range(1, len(a))) and not np.array_equal(a, b)

    def valid(self, task):
        for i, j in itertools.combinations(range(task.shape[0]), 2):
            if np.array_equal(task[i], task[j]) or self.dominated(task[i], task[j]) or self.dominated(task[j], task[i]):
                return False
        return True

    def random_version(self, rng):
        v = np.zeros((self.T, self.A, len(self.names)), int)
        for t in range(self.T):
            while True:
                for j, n in enumerate(self.nlev):
                    v[t, :, j] = rng.permutation(np.resize(rng.permutation(n), self.A))
                if self.valid(v[t]):
                    break
        return v

    def exchange(self, rng, max_pass=6):
        v = self.random_version(rng)
        best = self.d_error(v, self.prior)
        for _ in range(max_pass):
            improved = False
            for t in range(self.T):
                for a in range(self.A):
                    for j, n in enumerate(self.nlev):
                        cur = v[t, a, j]
                        for l in range(n):
                            if l == cur:
                                continue
                            v[t, a, j] = l
                            if not self.valid(v[t]):
                                continue
                            e = self.d_error(v, self.prior)
                            if e < best - 1e-9:
                                best, cur, improved = e, l, True
                        v[t, a, j] = cur
            if not improved:
                break
        return v, best

    def fixed_tasks(self, rng):
        top = [n - 1 for n in self.nlev]
        mid = [n // 2 for n in self.nlev]
        holdouts = []
        while len(holdouts) < 2:
            t = np.array([[rng.integers(n) for n in self.nlev] for _ in range(self.A)])
            if self.valid(t):
                holdouts.append(t.tolist())
        P = self.nlev[0]
        check = [[min(3, P - 1)] + [0] * (len(self.nlev) - 1), [min(1, P - 1)] + top[1:], [P - 1] + mid[1:]]
        return holdouts, check[: self.A]


def main():
    ap = study_arg(__doc__.splitlines()[0])
    ap.add_argument("--starts", type=int, default=3)
    ap.add_argument("--seed", type=int, default=17851)
    a = ap.parse_args()
    st = Study(a.study)
    D = Design(st.cfg["conjoint"])
    rng = np.random.default_rng(a.seed)
    rows, stats = [], []

    def put(version, task, kind, alt, lv):
        rows.append({"version": version, "task": task, "task_type": kind, "alt": alt,
                     **{n: D.attrs[n][int(lv[j])] for j, n in enumerate(D.names)}, **{f"{n}_lvl": int(lv[j]) for j, n in enumerate(D.names)}})

    for ver in range(D.V):
        v, e = min((D.exchange(rng) for _ in range(a.starts)), key=lambda x: x[1])
        stats.append({"version": ver + 1, "d_error_prior": e, "d_error_zero": D.d_error(v, np.zeros(D.K))})
        for t in range(D.T):
            for k in range(D.A):
                put(ver + 1, t + 1, "random", k + 1, v[t, k])
    holdouts, check = D.fixed_tasks(rng)
    for h, task in enumerate(holdouts):
        for k, lv in enumerate(task):
            put(0, D.T + 1 + h, "holdout", k + 1, lv)
    for k, lv in enumerate(check):
        put(0, D.T + 3, "dominance_check", k + 1, lv)
    df = pd.DataFrame(rows)
    df.to_csv(st.path("panel", "design.csv"), index=False)
    s = pd.DataFrame(stats)
    rnd = df[df.task_type == "random"]
    out = {"versions": D.V, "random_tasks": D.T, "alternatives": D.A, "none_option": True, "n_params": D.K, "seed": a.seed,
           "coding": "dummy, first level = base; + NONE ASC", "prior": D.prior.round(3).tolist(),
           "d_error_prior": {"mean": round(s.d_error_prior.mean(), 4), "min": round(s.d_error_prior.min(), 4), "max": round(s.d_error_prior.max(), 4)},
           "d_error_zero": {"mean": round(s.d_error_zero.mean(), 4), "min": round(s.d_error_zero.min(), 4), "max": round(s.d_error_zero.max(), 4)},
           "level_balance": {n: rnd[f"{n}_lvl"].value_counts(normalize=True).sort_index().round(3).tolist() for n in D.names},
           "overlap_share": {n: float(rnd.groupby(["version", "task"])[f"{n}_lvl"].nunique().lt(D.A).mean().round(3)) for n in D.names},
           "holdout_tasks": [D.T + 1, D.T + 2], "dominance_check_task": D.T + 3, "dominant_option": "B"}
    st.path("panel", "design_stats.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
