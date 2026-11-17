# Consensus Model

This reference defines the reproducible V2 path from timestamped bookmaker quotes to a score model and evidence score. It is an audit contract, not a promise of predictive certainty.

## 1. Normalize and Group

Each quote must include source, underlying bookmaker, market, period, line when applicable, selection, declared odds format, observed timestamp, and snapshot. Convert the price to decimal odds `d`, then raw implied probability `q = 1 / d`.

Group mutually exclusive selections from the same underlying bookmaker by market, period, canonical line, and snapshot. Opening and current checkpoints never share a group. Deduplicate mirrored aggregator records before any source count or weighting.

## 2. Remove Bookmaker Margin

For a complete three-way 1X2 market, use power de-vigging. Solve for `k > 0` by bisection so:

`sum(q_i ** k) = 1`

The fair probabilities are `p_i = q_i ** k`. If the power method cannot converge, record the fallback and use proportional normalization.

For a complete binary market such as totals or BTTS, use proportional de-vigging:

`p_i = q_i / sum(q_j)`

An incomplete group is marked unvigged/incomplete, receives at most half completeness weight, and cannot anchor the fit. Never silently synthesize a missing selection.

## 3. Weight and Aggregate

The starting quote weight is the product of:

- source tier: A `1.25`, B `1.0`, C `0.75`, D `0.0`;
- recency: under 15 minutes `1.0`, 15-60 `0.9`, 60-180 `0.7`, older current quotes `0.4`;
- completeness: full for complete de-vigged groups, at most `0.5` for incomplete groups;
- the engine's market-quality/liquidity factor.

Use the weighted median for each consensus selection rather than a simple mean. Report raw quote count, deduped independent bookmaker count, usable complete books, overround range, consensus probability, and dispersion.

## 4. Outliers and Dispersion

With at least five usable independent bookmakers, a quote is an exclusion candidate only when it differs from the median by both:

- more than six percentage points; and
- more than three scaled median absolute deviations.

Never exclude more than 20% of usable books. Preserve every exclusion and reason in diagnostics. When MAD is zero, the absolute six-point condition still prevents trivial differences from becoming outliers. Wide residual dispersion lowers confidence even if no quote is excluded.

## 5. Snapshot Movement

Track Opening, T-3h10, T-2h10, T-1h10, and T-10min independently. Movement is a change in de-vigged consensus probability and, for Asian markets, the signed line and water. Missing checkpoints remain missing. A one-book move is not consensus movement.

Compare each rolling forecast with its prior record and state:

- what changed;
- what stayed unchanged;
- whether the conclusion is retained or revised;
- the exact price, line, lineup, or news trigger that would flip it.

## 6. Score Fit and Market Separation

Fit home and away expected goals over a bounded grid. For independent Poisson rates `lambda_home` and `lambda_away`:

`P(H=h, A=a) = Poisson(h; lambda_home) * Poisson(a; lambda_away)`

Minimize the weighted residual between the score matrix and the no-vig 90-minute consensus for 1X2, totals, and BTTS. Market-family weights reflect usable coverage and dispersion and are capped so correlated derivative markets cannot dominate.

The fitted matrix must produce coherent 1X2, supplied totals, BTTS, exact-score, and win-margin probabilities. Asian handicap and correct-score prices validate margin/shape; they are not additional winner votes. Qualification remains separate because it can include extra time and penalties.

## 7. Asian and Total Settlement

Settle integer and half lines directly from every score cell. Split quarter lines into equal half-stakes on adjacent lines, for example:

- `-0.75` -> half at `-0.5`, half at `-1.0`;
- `+0.25` -> half at `0.0`, half at `+0.5`;
- over `2.25` -> half over `2.0`, half over `2.5`.

Report win, half-win, push, half-loss, and loss probabilities. Preserve home/away sign orientation; never normalize away which team is giving the handicap.

## 8. Evidence Confidence and Abstention

Confidence measures input quality, not certainty of the outcome:

| Component | Maximum |
| --- | ---: |
| Independent bookmaker coverage | 25 |
| Quote freshness | 20 |
| Trusted core market-family coverage | 20 |
| Low cross-book dispersion | 15 |
| Cross-market/score-fit agreement | 15 |
| Confirmed lineup | 5 |

Scores `75-100` are high, `50-74` medium, and below `50` low. Friendly matches receive a 10-point penalty. Qualification-only books and core families supported by only one book do not inflate 90-minute confidence.

The skill and engine require three independent underlying books for a full forecast and prefer five. Also abstain for stale near-kickoff evidence (no usable quote inside 60 minutes), ambiguous identity, invalid aggregate context, severe disagreement, or a match that has started without a separate in-play state model.

Use `no forecast edge` or `观望` when the gate fails.

## 9. Calibration Lock

`scripts/calibrate.py` reports multiclass Brier score, log loss, top-pick accuracy, totals/BTTS Brier, score error, confidence-bucket calibration, and movement to closing consensus. No source-weight change is eligible before both:

- 100 valid completed forecasts overall; and
- 30 valid observations in the affected competition/market bucket.

Invalid or internally conflicting records are quarantined atomically and cannot contribute partial metrics. Calibration can justify a later review of weights; it never changes them automatically.
