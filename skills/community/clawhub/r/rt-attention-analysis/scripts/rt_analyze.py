#!/usr/bin/env python3
"""Full reaction-time / sustained-attention analysis pipeline.

Computes, per participant and across participants:
  * descriptive statistics (mean RT, SD, accuracy);
  * RT variability (SD of RTs on correct frequent trials);
  * a real-time fast/slow triggering decomposition (deBettencourt et al. 2019);
  * lapse analysis: trailing RT preceding correct vs. incorrect responses;
  * paired Cohen's d_z and a paired bootstrap p-value / 95% CI.

Optionally plots the RT time series with thresholds and trigger markers
(requires matplotlib; the rest of the script runs on the standard library).

Example:
    python rt_analyze.py data.csv --out report/
    python rt_analyze.py data.csv --out report/ --no-plot
"""

from __future__ import annotations

import argparse
import csv
import os
import random
import sys
from statistics import fmean, mean, pstdev


# --------------------------------------------------------------------------- #
# I/O helpers
# --------------------------------------------------------------------------- #

def to_float(value):
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def load(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        header = reader.fieldnames
        return header, list(reader)


# --------------------------------------------------------------------------- #
# Statistics (standard library only)
# --------------------------------------------------------------------------- #

def cohens_dz(x, y):
    """Paired Cohen's d: mean(x - y) / SD(x - y)."""
    diffs = [xi - yi for xi, yi in zip(x, y)]
    if len(diffs) < 2:
        return float("nan")
    sd = pstdev(diffs)
    if sd == 0:
        return float("nan")
    return mean(diffs) / sd


def spearman_r(x, y):
    """Spearman rank correlation between two lists."""
    def ranks(vals):
        order = sorted(range(len(vals)), key=lambda i: vals[i])
        r = [0.0] * len(vals)
        for rank, idx in enumerate(order, start=1):
            r[idx] = rank
        return r
    rx, ry = ranks(x), ranks(y)
    return _pearson(rx, ry)


def _pearson(x, y):
    n = len(x)
    mx, my = fmean(x), fmean(y)
    num = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    dx = sum((xi - mx) ** 2 for xi in x) ** 0.5
    dy = sum((yi - my) ** 2 for yi in y) ** 0.5
    if dx == 0 or dy == 0:
        return float("nan")
    return num / (dx * dy)


def bootstrap_paired(x, y, n_iter=10000, seed=42):
    """Paired bootstrap of mean(x - y).

    Returns (mean_diff, lower_CI, upper_CI, p_value), where p is the
    proportion of resamples with a difference of the opposite sign.
    """
    diffs = [xi - yi for xi, yi in zip(x, y)]
    obs = mean(diffs)
    rng = random.Random(seed)
    n = len(diffs)
    samples = []
    for _ in range(n_iter):
        idx = [rng.randrange(n) for _ in range(n)]
        samples.append(fmean(diffs[j] for j in idx))
    samples.sort()
    lo = samples[int(0.025 * n_iter)]
    hi = samples[int(0.975 * n_iter)]
    if obs >= 0:
        p = sum(1 for s in samples if s <= 0) / n_iter
    else:
        p = sum(1 for s in samples if s >= 0) / n_iter
    return obs, lo, hi, p


# --------------------------------------------------------------------------- #
# Analysis
# --------------------------------------------------------------------------- #

def trailing_window(rts, i, window):
    lo = max(0, i - window + 1)
    vals = [r for r in rts[lo:i + 1] if r is not None]
    return fmean(vals) if vals else None


def analyze_subject(rts, accs, freqs, min_rt, max_sd, init_trials, window):
    """Run the trigger + lapse analysis for one participant's trial data.

    Returns a dict of summary metrics and per-trial state lists.
    """
    n = len(rts)

    # Cleaning: drop implausibly short RTs and > max_sd from the subject mean.
    kept = [True] * n
    base = [r for r in rts if r is not None]
    subj_mean = fmean(base) if base else 0.0
    subj_sd = pstdev(base) if len(base) > 1 else 0.0
    for i in range(n):
        rt = rts[i]
        if rt is None:
            kept[i] = False
        elif rt < min_rt:
            kept[i] = False
        elif max_sd and subj_sd > 0 and rt > subj_mean + max_sd * subj_sd:
            kept[i] = False

    # Cumulative mean/SD (Welford) and trailing average over kept trials.
    count = 0
    mean_ = 0.0
    m2 = 0.0
    states = [""] * n
    trailings = [None] * n
    for i in range(n):
        if not kept[i] or rts[i] is None:
            states[i] = "excluded"
            continue
        rt = rts[i]
        count += 1
        delta = rt - mean_
        mean_ += delta / count
        m2 += delta * (rt - mean_)
        sigma = (m2 / count) ** 0.5 if count > 1 else 0.0
        tr = trailing_window(rts, i, window)
        trailings[i] = tr
        if i < init_trials:
            states[i] = "init"
        elif sigma > 0 and tr is not None:
            if tr < mean_ - sigma:
                states[i] = "fast"
            elif tr > mean_ + sigma:
                states[i] = "slow"
            else:
                states[i] = "none"
        else:
            states[i] = "none"

    # RT variability: SD over correct frequent trials.
    freq_ok = [rts[i] for i in range(n)
               if kept[i] and (freqs[i] is None or freqs[i] == 1)
               and (accs[i] is None or accs[i] == 1)]
    rt_var = pstdev(freq_ok) if len(freq_ok) > 1 else float("nan")

    # Accuracy on frequent vs infrequent trials (if freq + acc present).
    acc = {"freq": None, "infreq": None}
    if accs is not None and freqs is not None:
        for grp, flag in (("freq", 1), ("infreq", 0)):
            vals = [accs[i] for i in range(n)
                    if kept[i] and freqs[i] == flag and accs[i] is not None]
            acc[grp] = fmean(vals) if vals else float("nan")

    # Lapse analysis: trailing RT before correct vs incorrect infrequent trials.
    err_tr, corr_tr = [], []
    if accs is not None:
        for i in range(1, n):
            if freqs is None or freqs[i] != 0:
                continue
            if accs[i] is None or not kept[i]:
                continue
            tr = trailings[i - 1]
            if tr is None:
                continue
            (err_tr if accs[i] == 0 else corr_tr).append(tr)

    summary = {
        "n_trials": n,
        "n_kept": sum(kept),
        "mean_rt": fmean([rts[i] for i in range(n) if kept[i]]) if sum(kept) else float("nan"),
        "rt_variability": rt_var,
        "acc_freq": acc["freq"],
        "acc_infreq": acc["infreq"],
        "err_trailing": fmean(err_tr) if err_tr else float("nan"),
        "corr_trailing": fmean(corr_tr) if corr_tr else float("nan"),
        "n_err": len(err_tr),
        "n_corr": len(corr_tr),
    }
    return summary, states, trailings


# --------------------------------------------------------------------------- #
# Plotting (optional)
# --------------------------------------------------------------------------- #

def plot_timeseries(path, rts, states, trailings):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed; skipping plot (install with: pip install matplotlib)")
        return

    xs = list(range(1, len(rts) + 1))
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.scatter(xs, rts, s=8, color="#9aa4b2", label="RT (per trial)")
    ax.plot(xs, trailings, color="#0f62fe", lw=1.2, label="trailing RT")
    for i, st in enumerate(states):
        if st == "fast":
            ax.scatter([xs[i]], [rts[i]], color="#e5484d", s=30, marker="v", zorder=3)
        elif st == "slow":
            ax.scatter([xs[i]], [rts[i]], color="#30a46c", s=30, marker="^", zorder=3)
    ax.set_xlabel("Trial")
    ax.set_ylabel("Response time (ms)")
    ax.set_title("Sustained-attention RT with fast/slow triggers")
    ax.legend(loc="best", frameon=False)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    print(f"Wrote {path}")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def main():
    ap = argparse.ArgumentParser(description="RT / sustained-attention analysis")
    ap.add_argument("input", help="input CSV")
    ap.add_argument("--out", "-o", default="report", help="output directory")
    ap.add_argument("--rt-col", default="rt")
    ap.add_argument("--acc-col", default="acc")
    ap.add_argument("--freq-col", default="freq")
    ap.add_argument("--subj-col", default="subject")
    ap.add_argument("--min-rt", type=float, default=100.0, help="drop RTs below this (ms)")
    ap.add_argument("--max-sd", type=float, default=3.0, help="drop RTs beyond mean + k*SD")
    ap.add_argument("--init-trials", type=int, default=80)
    ap.add_argument("--window", type=int, default=3)
    ap.add_argument("--no-plot", action="store_true")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    header, rows = load(args.input)
    for col in (args.rt_col,):
        if col not in header:
            sys.exit(f"error: column '{col}' not found; columns are {header}")

    # Group by subject if present, else treat all as one subject.
    groups = {}
    if args.subj_col in header:
        for r in rows:
            groups.setdefault(r.get(args.subj_col) or "subject", []).append(r)
    else:
        groups["subject"] = rows

    os.makedirs(args.out, exist_ok=True)

    metrics = []
    lines = []
    per_subj = {}

    for subj, subj_rows in groups.items():
        rts = [to_float(r.get(args.rt_col)) for r in subj_rows]
        accs = ([to_float(r.get(args.acc_col)) for r in subj_rows]
                if args.acc_col in header else None)
        freqs = ([to_float(r.get(args.freq_col)) for r in subj_rows]
                 if args.freq_col in header else None)

        summary, states, trailings = analyze_subject(
            rts, accs, freqs, args.min_rt, args.max_sd,
            args.init_trials, args.window)

        summary["subject"] = subj
        metrics.append(summary)
        per_subj[subj] = (rts, states, trailings)

        lines.append(
            f"{subj}: n={summary['n_kept']}/{summary['n_trials']} "
            f"meanRT={summary['mean_rt']:.1f}ms "
            f"RTvar={summary['rt_variability']:.1f} "
            f"accFreq={_fmt(summary['acc_freq'])} "
            f"accInfreq={_fmt(summary['acc_infreq'])} "
            f"errTrail={_fmt(summary['err_trailing'])} "
            f"corrTrail={_fmt(summary['corr_trailing'])}")

    # --- across-subject statistics (only if >= 2 subjects with data) ---
    stat_lines = []
    pairs = [(m["err_trailing"], m["corr_trailing"]) for m in metrics
             if m["err_trailing"] == m["err_trailing"] and m["corr_trailing"] == m["corr_trailing"]]
    if len(pairs) >= 2:
        err = [p[0] for p in pairs]
        corr = [p[1] for p in pairs]
        d = cohens_dz(err, corr)
        md, lo, hi, p = bootstrap_paired(err, corr, seed=args.seed)
        stat_lines.append(
            f"Lapse (err vs corr trailing RT): d_z={d:.2f} "
            f"meanDiff={md:.1f}ms 95%CI=[{lo:.1f},{hi:.1f}] p={p:.4f} (n={len(err)})")

    rtvar = [m["rt_variability"] for m in metrics if m["rt_variability"] == m["rt_variability"]]
    acc_inf = [m["acc_infreq"] for m in metrics if m["acc_infreq"] == m["acc_infreq"]]
    if len(rtvar) >= 2 and len(acc_inf) == len(rtvar):
        r = spearman_r(rtvar, acc_inf)
        stat_lines.append(
            f"RT variability vs infrequent accuracy: Spearman r={r:.3f} (n={len(rtvar)})")

    # --- write outputs ---
    summary_path = os.path.join(args.out, "summary.txt")
    with open(summary_path, "w", encoding="utf-8") as fh:
        fh.write("Per-subject summary\n===================\n")
        fh.write("\n".join(lines) + "\n\n")
        fh.write("Across-subject statistics\n========================\n")
        fh.write("\n".join(stat_lines) + "\n" if stat_lines else "(insufficient data)\n")
    print(f"Wrote {summary_path}")

    metrics_path = os.path.join(args.out, "metrics.csv")
    if metrics:
        fields = list(metrics[0].keys())
        with open(metrics_path, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            w.writeheader()
            for m in metrics:
                w.writerow(m)
        print(f"Wrote {metrics_path}")

    # Per-trial trigger CSV (single subject) + plot.
    if not args.no_plot or len(per_subj) == 1:
        first_subj = next(iter(per_subj))
        rts, states, trailings = per_subj[first_subj]
        if len(per_subj) == 1:
            trig_path = os.path.join(args.out, "triggered.csv")
            with open(trig_path, "w", newline="", encoding="utf-8") as fh:
                w = csv.writer(fh)
                w.writerow(["trial", "rt", "trailing", "state"])
                for i in range(len(rts)):
                    w.writerow([i + 1, rts[i], trailings[i], states[i]])
            print(f"Wrote {trig_path}")
        if not args.no_plot:
            plot_timeseries(os.path.join(args.out, "rt_timeseries.png"),
                            rts, states, trailings)

    print("Done.")


def _fmt(v):
    return "na" if v is None or v != v else f"{v:.2f}"


if __name__ == "__main__":
    main()
