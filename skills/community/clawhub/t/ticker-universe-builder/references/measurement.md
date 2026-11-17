# Measuring the window statistics

`liquidity`, `factor_r2`, `beta_strength`, `beta_stability` and derived `independence` cannot be
judgement scores. Each eligible measured candidate requires a dated `measurement_record`, input
SHA-256 and source. This is reproducible provenance, not proof against fabricated inputs.

```bash
python scripts/universe.py measure --prices prices.csv \
  --benchmark BINANCE:BTCUSDT.P --benchmark BINANCE:ETHUSDT.P --benchmark BINANCE:SOLUSDT.P \
  --factor-model multivariate --as-of 2026-09-29 \
  --source https://api.binance.com/ --window 180 --liquidity-window 30 \
  --into snapshot.json --output snapshot.measured.json
```

## Input and time boundary

CSV columns: `date,ticker,close[,turnover][,volume]`, one ticker/session per row. Dates must be ISO;
duplicates, nonpositive/nonfinite closes and negative/nonfinite turnover fail. `close` should be
consistently adjusted; turnover should be actual notional, or a disclosed raw-close × volume proxy.
Missing turnover produces no liquidity value. `--as-of` cuts off later bars before computation.
A market percentile needs one currency and a disclosed population; never mix currencies as levels.

The optional [fetch adapter](providers.md) supplies this shape. `measure` itself remains offline.

## Statistics

| Metric | Definition |
|---|---|
| liquidity | Percentile of mean daily turnover over the latest 30 sessions, with ties averaged; population disclosed |
| factor_r2 | OLS R² over the last 180 overlapping daily returns, scaled to 0–100 |
| independence | Exactly 100 − factor_r2, derived by the builder |
| beta_strength | Positive OLS beta scaled so beta 2.0 = 100; negative beta scores zero |
| beta_stability | Agreement of beta across the two halves of the same factor window |

At least 30 overlapping returns are required. No overlap/constant gauge produces no factor score.
`--benchmark` repeats for an equal-weight daily-rebalanced basket. `--factor-model multivariate`
fits R² jointly on the individual legs with an intercept; beta strength/stability still describe
the equal-weight basket. Singular factor matrices produce no score. Crypto should declare its
actual core anchors as factor legs. These models are different and the record states which ran.

Coverage satellites use price Beta/R²/stability as optional descriptors. Missing factor statistics
do not block business-complementary admission when listing, measured liquidity, identity and
sourced cap pass; supplied statistics still require the measurement records above. Core and
legacy role requirements remain unchanged. A high-beta price claim needs actual measurements.

## Equity theme gauges

Use a researched map rather than silently substituting a broad index:

```json
{
  "schema_version": 1,
  "themes": {
    "11_A": {"members": ["NASDAQ:NVDA", "NASDAQ:AMD"], "benchmarks": ["AMEX:SOXX"]},
    "12_A": {"members": ["NASDAQ:MSFT", "NYSE:ORCL", "NASDAQ:ADBE"], "mode": "peer_basket"}
  },
  "funds": [{"ticker": "AMEX:SOXX", "themes": ["11_A"]}]
}
```

```bash
python scripts/universe.py measure --prices prices.csv --benchmark-map benchmark-map.json \
  --as-of 2026-09-29 --source https://query1.finance.yahoo.com/ --output metrics.json
```

An explicit gauge must correlate positively (>=0.30) with the theme basket over up to 252 common
returns. An unfit/missing gauge yields no factor statistics; the reason stays in `theme_checks`.
An internal `peer_basket` excludes the ticker being regressed and requires at least two other
measurable peers. It uses the actual common calendar. A source-industry basket can be a coarse
proxy: classification and gauge fit are separate research questions. Singleton industries may
remain breadth/size observations, but cannot claim unmeasured independence or beta.

Optional `funds` diagnostics compare the equal-weight theme basket with the ETF on full 252- and
495-return windows. Reproduction needs correlation >=0.90 and positive compounded excess on
both; `robust` additionally drops the largest compounded contributor and repeats those checks.
Missing full horizons produce `measured=false`, never a shortened horizon presented as two years.
These diagnostics do not remove a fund automatically: coverage, investability and research still
matter. A daily-rebalanced frictionless basket is a comparison instrument, not a strategy return.

## Outputs and refresh

A bundle carries `measurement`, per-ticker `metrics`/`records`, `coverage`, `theme_checks`,
`fund_comparisons` and `notes`. Records name actual first/last bars, factor observation counts,
liquidity counts, gauge legs/model, cutoff, source and hash of the input file (including any rows
later excluded by the cutoff). Store the original table locally to reproduce the calculation.

`--into` replaces every measured field and declaration. Missing replacement data clears stale
scores rather than retaining them under a new method label. Eligible uncovered candidates mark
the snapshot incomplete; required role metrics still gate the build. Judged fields remain as
submitted. `measurement_audit` preserves dated theme/fund diagnostics. Coverage and notes persist
in JSON; Markdown retains material limitations rather than printing per-ticker missing-factor
logs. Manual/external measurements must provide equivalent records.

`evaluate` uses the same CSV shape **after** the universe's as-of date. Measurements used to build
a universe cannot validate its future coverage.
