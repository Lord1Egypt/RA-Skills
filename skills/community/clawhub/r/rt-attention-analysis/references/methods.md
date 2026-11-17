# Methods Background — RT-Based Lapse Detection & Real-Time Triggering

This reference explains the methods implemented by the scripts, so you can
describe and justify them when reporting results.

## The idea

Sustained attention fluctuates between "good" (focused) and "bad" (lapsing)
states. Response speed is a cheap, unobtrusive marker of these states: when
people respond *faster than usual*, they are more likely to lapse on a rare
(inhibitory) trial; when they respond *slower than usual*, they are more likely
to be on-task. This is the "speeding" marker found with PCA by Smallwood et al.
(2008) and McVay & Kane (2012), and it is the basis of the real-time triggering
procedure of deBettencourt et al. (2019).

## Real-time triggering procedure (deBettencourt et al. 2019)

The goal is to *prospectively* trigger an event (e.g. a working-memory probe)
whenever the participant is in an exceptionally fast or slow state, without any
post-hoc analysis.

Definitions, for trial `i` and RTs `r1, r2, ...`:

- **Cumulative mean and SD** over all trials seen so far:
  `mu = mean(r1..ri)`, `sigma = sd(r1..ri)`. Initialized on the first ~80 trials.
- **Trailing average** over the last 3 trials:
  `trailing = mean(r[i-2], r[i-1], r[i])`.
- **Fast threshold**: `mu - sigma`. If `trailing < mu - sigma`, the participant is
  responding unusually fast → inferred **low attention**.
- **Slow threshold**: `mu + sigma`. If `trailing > mu + sigma`, the participant is
  responding unusually slow → inferred **high attention**.

Experiment variants:

- **Experiment 2a** — the trailing window includes the to-be-probed trial `i`;
  the probe appears on trial `i`.
- **Experiment 2b** — the trailing window is computed on trials `i-2..i`, but the
  probe is placed on the *next* trial `i+1` (fully anticipatory). In addition, all
  three trailing trials and the probe trial must be frequent-category and correct.

This procedure is adaptive and within-subjects: thresholds are unique to each
participant and update every trial.

## Lapse detection (retrospective)

To identify lapses from already-collected data: sort trailing RTs, bin them, and
examine accuracy per bin. A positive slope (higher trailing RT → higher accuracy)
is evidence that fast RTs precede lapses. Compare trailing RT before correct vs.
incorrect rare-trial responses (a paired/within-subject effect).

## RT variability

`RT variability = SD of RTs over correct frequent trials` (per block, then
averaged). Higher variability indexes poorer attentional control and negatively
correlates with working-memory performance.

## Statistics (non-parametric, as in deBettencourt et al. 2019)

- **Cohen's d** — standardized mean difference for within-subject contrasts.
- **Spearman's r** — rank correlation (robust to non-normality).
- **Bootstrap** — resample participants with replacement (e.g. 100,000 times);
  the bootstrap distribution gives a 95% CI and a p-value (the proportion of
  resamples in the opposite direction).
- **Bayes factor BF₀₁** — evidence for the null (used when the prediction is that
  *no* effect exists, e.g. Experiment 3 on colour precision).

## Data-cleaning recommendations

- Drop RTs that are implausibly short (e.g. < 100 ms) — likely anticipations.
- Optionally drop RTs beyond 3 SD of the participant's mean — outliers.
- Only compute RT variability on correct frequent trials.
- Document every exclusion, and state whether analyses were pre-registered or
  exploratory.

## References

- deBettencourt, M. T., Keene, P. A., Awh, E., & Vogel, E. K. (2019). Real-time
  triggering reveals concurrent lapses of attention and working memory.
  *Nature Human Behaviour*, 3, 808–816.
- Shelat, S., Schooler, J. W., & Giesbrecht, B. (2024). Predicting attentional
  lapses using response time speed in continuous performance tasks.
  *Frontiers in Cognition*.
- Esterman, M., Noonan, S. K., Rosenberg, M., & Degutis, J. (2013). In the zone or
  zoning out? *Cerebral Cortex*, 23, 2712–2723.
