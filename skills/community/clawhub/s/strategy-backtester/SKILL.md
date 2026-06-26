---
name: strategy-backtester
description: Validates historical behavior of stock ranking, factor, and portfolio-selection strategies using reproducible backtests, benchmark comparison, turnover, drawdown, and bias warnings.
compatibility: Requires historical signal/ranking CSVs and price history CSVs; uses local scripts and does not require network access.
---

# Strategy Backtester

## Purpose

Use this skill to test whether a ranking, factor mix, or portfolio-selection rule had useful historical behavior before treating it as an investment signal.

## Scope

- Equity ranking and selection strategies.
- Periodic rebalance backtests from local CSV inputs.
- Benchmark comparison when benchmark data is available.
- Bias and robustness review.

## Non-goals

- Do not claim that historical performance predicts future returns.
- Do not optimize parameters until a preferred result appears.
- Do not issue absolute buy/sell instructions.
- Do not fetch live market data.

## Input contract

Required inputs:
- `SIGNAL_CSV`: rows with `date`, `ticker`, and `score`.
- `PRICE_CSV`: rows with `date`, `ticker`, and `close`.
- `REBALANCE_FREQUENCY`: `monthly`, `quarterly`, or `yearly`.
- `TOP_N`: number of selected names per rebalance.

Optional inputs:
- `BENCHMARK_CSV`: rows with `date` and `close` or `return`.
- `FEE_BPS`: round-trip fee assumption in basis points.
- `SLIPPAGE_BPS`: slippage assumption in basis points.
- `UNIVERSE_HISTORY`: point-in-time membership if available.

## Execution workflow

1. Validate input files and required columns.
2. Estimate whether the test window and symbol coverage are sufficient.
3. Run `scripts/backtest_strategy.py` with explicit rebalance, fee, slippage, and top-N assumptions.
4. Review performance metrics and benchmark comparison.
5. Identify bias risks and robustness gaps.
6. Return the required output sections.

## Required output format

1. `Backtest Setup`
- Strategy name, test window, rebalance frequency, top-N, fees, slippage, benchmark.

2. `Performance Summary`
- Total return, CAGR, volatility, max drawdown, Sharpe, Sortino, turnover, hit rate when available.

3. `Benchmark Comparison`
- Relative return, relative drawdown, and tracking observations when benchmark data exists.

4. `Robustness and Bias Warnings`
- Survivorship bias, lookahead bias, data-snooping risk, liquidity assumptions, fee/slippage sensitivity.

5. `Confidence and Data Gaps`
- Confidence level and missing inputs that could change the conclusion.

6. `Handoff Bundle`
- Include `strategy_name`, `test_window`, `rebalance_frequency`, `fee_assumption`, `slippage_assumption`, `benchmark`, `metrics`, `bias_warnings`, `confidence`, and `data_gaps`.

## Shared confidence rubric

- `High`: point-in-time signals, adequate price coverage, benchmark available, fees/slippage included, and test window covers multiple market regimes.
- `Medium`: usable history and price coverage, but one major robustness input is missing.
- `Low`: short history, missing benchmark, sparse price coverage, likely survivorship/lookahead risk, or no fee/slippage assumptions.

## Guardrails

- Separate observed backtest results from assumptions and inference.
- Always state that backtests are historical simulations, not forecasts.
- Downgrade confidence if the test appears overfit or data is not point-in-time.
- Treat backtest output as one input to `stock-picker-orchestrator`, not as a trading command.

## Trigger examples

- "Backtest this VN30 value-quality ranking."
- "Check whether this stock ranking strategy beat VNINDEX historically."
- "Validate this screening rule before using it for shortlist selection."
