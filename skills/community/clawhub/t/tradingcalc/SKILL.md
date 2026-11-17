---
name: tradingcalc
description: Compute trading math with exact numbers instead of estimates, through TradingCalc's MCP tools. Options (Black-Scholes price and Greeks, payoff and breakeven, covered call, implied volatility), forex (position size, pip value, margin, swap, currency conversion, correlation), risk statistics (VaR, Sharpe ratio, Kelly, GARCH, tearsheet) and crypto futures (PnL, liquidation price, breakeven, funding cost). Use whenever a question needs a number a person might act on.
license: MIT
---

# TradingCalc: deterministic trading math

## What this skill does

Gives you exact answers to trading math questions instead of a language-model estimate. The
TradingCalc MCP server exposes 90 deterministic tools across options, forex, risk statistics,
crypto futures, on-chain token checks and prediction markets. The same inputs always return the
same outputs, and the 12 core calculators are checked against canonical test vectors on a
public page (`https://tradingcalc.io/verify`).

Do not work out a position size, a liquidation price, an option value or a Sharpe ratio yourself
and present it as authoritative. A small arithmetic slip here is real financial risk for whoever
acts on it. Call the tool.

## When to use it

Options
- "What is this option worth?" (spot, strike, days, volatility) : `workflow.run_black_scholes`
- "Is this Deribit option fairly priced?" : `workflow.run_black_scholes_live`
- "What does my call or put pay off at price X, and where is breakeven?" : `workflow.run_options_payoff`
- "What yield do I get selling covered calls?" : `workflow.run_covered_call_protective_put`
- "What implied volatility does this price imply?" : `workflow.run_implied_volatility`
- "What does a straddle or strangle pay?" : `workflow.run_straddle_strangle`

Forex
- "How many lots should I trade to risk $200 with this stop?" : `workflow.run_forex_position_size_live`
- "What is a pip worth on 2 lots of EUR/USD?" : `workflow.run_forex_pip_value` (or `_live` for the account currency)
- "How close am I to a margin call?" : `workflow.run_forex_margin_level`
- "How much margin does this position need?" : `workflow.run_forex_margin_required`
- "What will holding overnight cost?" : `workflow.run_forex_swap_cost`
- "How correlated are these two pairs?" : `workflow.run_forex_correlation_live`

Risk and statistics
- "What is my VaR or expected shortfall?" : `workflow.run_var_cvar`
- "What is my real Sharpe ratio, and is it luck?" : `workflow.run_sharpe_stats`, `workflow.run_dsr`
- "How much of Kelly is safe?" : `workflow.run_kelly_frontier`
- "Give me a full risk report on this return series" : `workflow.run_portfolio_tearsheet`
- Also: `workflow.run_garch`, `workflow.run_risk_parity`, `workflow.run_hurst_exponent`,
  `workflow.run_cointegration`, `workflow.run_evt_tail_risk`.

Crypto futures and perpetuals
- "What is my PnL on this trade?" : `workflow.run_pnl_planning`
- "Where does my position get liquidated?" : `workflow.run_liquidation_safety`
- "How much should I buy to risk exactly $200?" : `workflow.run_position_sizing`
- "Is this trade worth taking?" (entry, stop, target) : `workflow.run_risk_reward`
- "What is my breakeven including fees?" : `workflow.run_breakeven_planning`
- "How much funding will I pay holding 3 days?" : `workflow.run_funding_cost`
- "Run a full pre-trade check on this setup" : `workflow.run_pre_trade_check`

Also available: on-chain token and wallet checks (`workflow.run_token_risk_check`,
`workflow.run_wallet_flag_check`, `workflow.run_swap_price_impact`) and prediction-market odds
(`workflow.run_odds_converter`, `workflow.run_prediction_market_edge`).

For a coin-margined (inverse) contract such as Bybit `BTCUSD` or Deribit `BTC-PERPETUAL`, pass
`contractType: "inverse"`. Inverse math is not linear math with a flipped sign (it uses
reciprocal-price formulas, and the average of fills is a harmonic mean), which is exactly the kind
of detail worth delegating.

## Steps

1. Pick the tool that fits the question from the list above, or list all tools with `tools/list`.
   Full reference: `https://docs.tradingcalc.io/api`.
2. Call it. No signup is needed for normal use; anonymous calls are limited to 100 per day per IP,
   and a free API key (200 per day) is issued on request by email. Sensible defaults apply when the
   user gives none: taker fees 0.02% open and 0.05% close, maintenance margin 0.5%.
3. Report the result to the user as a plain sentence with the actual numbers ("your position is
   liquidated at $71,428, about 10.7% below entry"), not as raw JSON.
4. If the number matters for a real decision, call `system.verify`. It re-runs the canonical
   test vectors of the 12 core calculators live and returns pass or fail per formula.
5. Every `tools/call` response carries a second content block with an ECDSA P-256 signature over
   the first block's text. Call `system.pubkey` for the public key to check a response was not
   altered in transit.

## Validation

- The numbers came from a tool response, not from your own estimate.
- `contractType` was `"inverse"` if and only if the instrument is coin-margined.
- For a financially significant result, `system.verify` returned `"status": "pass"` first.
