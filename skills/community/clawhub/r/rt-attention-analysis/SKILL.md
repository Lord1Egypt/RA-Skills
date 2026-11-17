---
name: rt-attention-analysis
description: Processes reaction-time (RT) and accuracy data from continuous-performance / sustained-attention tasks (PVT, SART, gradCPT). Computes trailing-average RT windows, cumulative mean and standard deviation, real-time fast/slow triggering thresholds (μ±σ), lapse detection, RT variability, and bootstrap / effect-size statistics; plots RT time series with trigger markers. Use when the user has RT or behavioral performance data and wants to detect attentional lapses, run real-time triggering, or analyze sustained attention.
version: 1.0.0
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    emoji: "📊"
---

# RT & Sustained-Attention Data Analysis

Analyze reaction-time (RT) data from continuous performance tasks (CPTs) such as
the PVT, SART, or gradCPT. Implements the real-time "fast/slow triggering"
procedure from deBettencourt et al. (2019) and the lapse-prediction analyses from
Shelat et al. (2024).

## When to use

- The user has a CSV/TSV/JSON of trial-by-trial RTs (and optionally accuracy) and
  wants to detect lapses, run real-time triggering, compute RT variability, or
  summarize sustained-attention performance.

## Input format

One row per trial. Minimum column: `rt` (response time in ms). Optional columns:
`trial`, `acc` (1/0 or correct/incorrect), `freq` (frequent=1, infrequent=0),
`block`, `condition`.

## Core algorithm (real-time triggering)

For each trial `i`:

1. `mu`, `sigma` = cumulative mean and standard deviation of all RTs up to trial
   `i` (initialize on the first ~80 trials).
2. `trailing` = mean of the last 3 RTs (`i-2`, `i-1`, `i`).
3. If `trailing < mu - sigma` → **fast** state (low attention) → trigger a probe.
4. If `trailing > mu + sigma` → **slow** state (high attention) → trigger a probe.
5. (Optional, experiment 2b) trigger the *next* trial `i+1` and require the three
   preceding trials to be frequent and correct.

Faster trailing RTs predict worse attention; slower RTs predict better attention.

## Scripts

- `scripts/rt_trigger.py` — pure-stdlib implementation of the triggering
  algorithm; writes per-trial state and fast/slow probe labels to CSV.
  No third-party dependencies.
- `scripts/rt_analyze.py` — full pipeline: load, clean, lapse detection, RT
  variability, Cohen's d, Spearman r, bootstrap CI, and an RT time-series plot
  (matplotlib optional).

Run:

```bash
python scripts/rt_trigger.py data.csv --out triggered.csv
python scripts/rt_analyze.py data.csv --out report/
```

## Key metrics

- **RT variability** = SD of RTs on correct frequent trials (higher ⇒ worse attention).
- **Lapse** = a fast trailing RT (e.g. below μ − σ) preceding an error.
- **Effect size** = Cohen's d; **correlation** = Spearman's r (non-parametric).
- **Bootstrap** = resample participants with replacement for CIs and p-values.

See `references/methods.md` for the methodological background and formulas.

## Notes

- Remove implausible RTs (e.g. < 100 ms or > 3 SD) before analysis and document
  any exclusions.
- Statistics default to non-parametric (matches deBettencourt et al. 2019).
