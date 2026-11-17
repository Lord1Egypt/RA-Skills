#!/usr/bin/env python3
"""Real-time fast/slow triggering for continuous-performance RT data.

Implements the adaptive, within-subject triggering procedure of
deBettencourt et al. (2019), Nature Human Behaviour 3, 808-816.

Given trial-by-trial response times (RT), it:
  1. maintains a running (cumulative) mean and standard deviation of RTs;
  2. computes a trailing average over the last `window` trials;
  3. flags each trial as FAST (trailing < mu - sigma) or SLOW
     (trailing > mu + sigma);
  4. optionally places the triggered probe on the NEXT trial and requires the
     trailing trials to be frequent + correct (experiment 2b).

Pure standard library -- no third-party dependencies.

Example:
    python rt_trigger.py data.csv --out triggered.csv
    python rt_trigger.py data.csv --out triggered2b.csv --next --require-correct
"""

from __future__ import annotations

import argparse
import csv
import sys
from statistics import fmean


def read_rows(path, rt_col):
    """Read CSV rows and return (header, rows)."""
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        header = reader.fieldnames
        if rt_col not in header:
            sys.exit(f"error: column '{rt_col}' not found; columns are {header}")
        rows = list(reader)
    return header, rows


def to_float(value):
    """Coerce a CSV cell to float or None."""
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def main():
    ap = argparse.ArgumentParser(description="RT-based fast/slow triggering")
    ap.add_argument("input", help="input CSV with an RT column")
    ap.add_argument("--out", "-o", default="triggered.csv", help="output CSV path")
    ap.add_argument("--rt-col", default="rt", help="name of the RT column (ms)")
    ap.add_argument("--acc-col", default="acc", help="name of the accuracy column (optional)")
    ap.add_argument("--freq-col", default="freq", help="name of the frequent/infrequent column (optional)")
    ap.add_argument("--init-trials", type=int, default=80,
                    help="number of trials used only to initialize mu/sigma")
    ap.add_argument("--window", type=int, default=3,
                    help="trailing-average window size (trials)")
    ap.add_argument("--next", action="store_true",
                    help="place the probe on the NEXT trial (experiment 2b)")
    ap.add_argument("--require-correct", action="store_true",
                    help="require trailing trials to be frequent and correct (2b)")
    args = ap.parse_args()

    header, rows = read_rows(args.input, args.rt_col)

    # Pre-extract numeric columns into parallel lists.
    rts = [to_float(r.get(args.rt_col)) for r in rows]
    accs = [to_float(r.get(args.acc_col)) if args.acc_col in header else None for r in rows]
    freqs = [to_float(r.get(args.freq_col)) if args.freq_col in header else None for r in rows]

    n = len(rows)
    # Welford's online algorithm for cumulative mean / population SD.
    count = 0
    mean = 0.0
    m2 = 0.0

    states = [""] * n
    mu_list = [""] * n
    sigma_list = [""] * n
    trailing_list = [""] * n

    for i in range(n):
        rt = rts[i]
        if rt is None:
            states[i] = "none"
            continue

        # --- update cumulative mean & SD (includes current trial) ---
        count += 1
        delta = rt - mean
        mean += delta / count
        delta2 = rt - mean
        m2 += delta * delta2
        sigma = (m2 / count) ** 0.5 if count > 1 else 0.0

        # --- trailing average over the last `window` trials ---
        lo = max(0, i - args.window + 1)
        window_rts = [r for r in rts[lo:i + 1] if r is not None]
        trailing = fmean(window_rts) if window_rts else rt

        mu_list[i] = f"{mean:.2f}"
        sigma_list[i] = f"{sigma:.2f}"
        trailing_list[i] = f"{trailing:.2f}"

        if i < args.init_trials:
            states[i] = "init"
            continue

        fast = trailing < (mean - sigma) if sigma > 0 else False
        slow = trailing > (mean + sigma) if sigma > 0 else False

        # Optional: require trailing window to be frequent + correct (exp 2b).
        if args.require_correct and (fast or slow):
            window_ok = True
            for j in range(lo, i + 1):
                if freqs[j] is not None and freqs[j] == 0:
                    window_ok = False
                if accs[j] is not None and accs[j] == 0:
                    window_ok = False
            if not window_ok:
                fast = slow = False

        if fast:
            states[i] = "fast"
        elif slow:
            states[i] = "slow"
        else:
            states[i] = "none"

    # --- place probes; optionally shift to the next trial (exp 2b) ---
    probes = ["none"] * n
    if args.next:
        for i in range(n - 1):
            if states[i] in ("fast", "slow"):
                probes[i + 1] = states[i]
    else:
        for i in range(n):
            if states[i] in ("fast", "slow"):
                probes[i] = states[i]

    # --- write output ---
    out_fields = list(header) + ["mu", "sigma", "trailing", "state", "probe"]
    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=out_fields)
        writer.writeheader()
        for i, row in enumerate(rows):
            out = dict(row)
            out["mu"] = mu_list[i]
            out["sigma"] = sigma_list[i]
            out["trailing"] = trailing_list[i]
            out["state"] = states[i]
            out["probe"] = probes[i]
            writer.writerow(out)

    n_fast = probes.count("fast")
    n_slow = probes.count("slow")
    print(f"Wrote {args.out}")
    print(f"Trials: {n}   fast probes: {n_fast}   slow probes: {n_slow}")


if __name__ == "__main__":
    main()
