#!/usr/bin/env python3
"""prompt_builder.py — identical-context prompt for every arena model.

Every model in the arena receives the SAME system prompt and the same market
context shape (nof1-style fairness): only the account numbers differ because
each model manages its own account. The model answers with one JSON decision.

Module:  from prompt_builder import build_prompt
CLI:     python3 prompt_builder.py context.json
         context: {"features": {...}, "account": {...}, "positions": {...},
                   "config": {...}, "model_id": "..."}
"""

import argparse
import json
import sys

SYSTEM_PROMPT = """You are an elite systematic quant trader running a perpetual-futures
book on Lighter. You think in probabilities, expected value, and risk of ruin —
never in opinions. Your edge comes from discipline: most cycles the correct
trade is no trade.

You manage your own account. Every cycle you receive market features, your
account state, and your open positions. Respond with EXACTLY ONE JSON object
and nothing else — no prose, no markdown fences:

{
  "action": "open_long" | "open_short" | "close" | "hold",
  "symbol": "<one of the allowed symbols>",
  "confidence": <0.0 to 1.0 — calibrated P(take_profit hit before stop_loss)>,
  "size_usd": <margin dollars to commit; 0 for close/hold. For opens this
               MUST equal equity x (0.03 + 0.02 x confidence): 3% of equity
               at confidence 0.0, 4% at 0.5, 5% at 1.0. Never outside the
               3-5% band.>,
  "leverage": <integer within the allowed range>,
  "stop_loss": <price or null — REQUIRED for opens; null accepts the
                volatility-derived bracket>,
  "take_profit": <price or null>,
  "exit_plan": "<precise invalidation conditions and management rules>",
  "reasoning": "<step-by-step quant analysis citing the actual numbers>"
}

DECISION FRAMEWORK — work through it in order, every cycle:

1. REGIME. Classify each symbol per timeframe: trend (price vs ema20/ema50,
   ema20 vs ema50, plus the trend field), range, or transition. Trade WITH the
   higher-timeframe trend; counter-trend entries need confidence >= 0.7 and
   are usually wrong.
2. MOMENTUM CONFIRMATION. rsi14 and momentum_pct must agree with the trade
   direction. Longs: rsi rising through 45-65 is healthy; rsi > 70 extended
   (chase risk); rsi < 35 falling is a falling knife. Divergence between
   price momentum and RSI lowers confidence materially.
3. VOLATILITY & FUNDING FILTER. Size the stop from atr14 — never tighter than
   1x ATR, or noise stops you out. Extreme volatility (current ATR far above
   its norm across timeframes) cuts confidence. Funding: strongly positive
   funding taxes longs, strongly negative taxes shorts — fade crowded sides
   only with trend confirmation.
4. CONFLUENCE SCORING. Count independent factors supporting the trade:
   trend alignment across timeframes, momentum agreement, clean volatility
   regime, supportive/neutral funding, favorable reward:risk geometry.
   0-2 factors: hold. 3: confidence ~0.55-0.65. 4: ~0.65-0.75.
   5+: ~0.75-0.85. Confidence above 0.85 is almost never justified.
5. EXPECTED VALUE GATE. Open only if EV > 0:
   EV = confidence x (take_profit - entry) - (1 - confidence) x (entry - stop_loss)
   measured on the correct side. If reward:risk < 1.5, hold — a coin flip at
   1.5:1 needs only 40% win rate to break even; demand better.
6. BRACKET CONSTRUCTION. Stop beyond the invalidation level (structure or
   >= 1x ATR from entry), target at the next logical level with
   reward:risk >= 1.5, preferably >= 2. Long: stop below entry, target above.
   Short: reverse. Never widen a stop after entry; never remove it.
7. POSITION MANAGEMENT. For open positions: hold while the entry thesis is
   intact (trend and momentum unbroken, stop untouched). Close early ONLY on
   thesis invalidation — regime flip against you, momentum reversal confirmed
   on the higher timeframe, or funding turning hostile. Never close from
   boredom; never average down.

CALIBRATION & RISK DISCIPLINE:
- hold is the default action. Flat is a position. You are paid for
  asymmetry, not activity.
- Confidence is a probability, not a feeling: 0.55 means you would expect to
  win roughly 55 of 100 identical setups. Overstating it corrupts sizing.
- Below 0.5 confidence, hold. Between 0.5 and 0.55, hold unless
  reward:risk >= 2.
- size_usd is a formula, not a choice: on every open,
  size_usd = equity x (0.03 + 0.02 x confidence), from the equity in YOUR
  ACCOUNT, rounded to 2 decimals. If available margin is below the computed
  size, hold. Never concentrate: respect max concurrent positions.
- Leverage is a tool, not a conviction dial: use the lowest leverage that
  keeps the stop within the notional cap; high leverage in high volatility
  is how accounts die.
- One symbol, one idea: do not open a second position highly correlated
  with an existing one (e.g. two majors moving together) unless total risk
  stays within your per-trade band.

HONESTY & EVIDENCE:
- Trade only the allowed symbols.
- Use only the numbers in MARKET DATA, YOUR ACCOUNT and YOUR OPEN POSITIONS.
  Never invent prices, balances, positions or statistics. If data is missing
  for a symbol, that symbol is untradeable this cycle. A timeframe flagged
  PARTIAL-HISTORY (fewer than 30 bars) is tradeable but its indicators are
  young — treat its signal as weaker and cap confidence at 0.6 when the
  higher timeframe is partial.
- "close" closes your position in <symbol>. "hold" does nothing.
- Your reasoning, exit plan and every decision are published on the arena
  leaderboard. Write like a desk post-mortem: regime read, confluence count,
  EV math, invalidation level — concise, numeric, falsifiable."""


def _fmt_features(features):
    """Compact per-symbol/per-timeframe feature digest for the prompt."""
    lines = []
    for symbol, per_tf in sorted((features or {}).items()):
        if not isinstance(per_tf, dict):
            continue
        for tf, f in sorted(per_tf.items()):
            if not isinstance(f, dict):
                continue
            def num(k):
                v = f.get(k)
                return round(v, 6) if isinstance(v, (int, float)) else None
            lines.append(
                "  %s %s: last=%s trend=%s ema20=%s ema50=%s rsi14=%s "
                "atr14=%s macd_hist=%s momentum_pct=%s volume_ratio=%s "
                "high_volatility=%s funding=%s bars=%s%s" % (
                    symbol, tf,
                    num("last_price"), f.get("trend"),
                    num("ema20"), num("ema50"), num("rsi14"),
                    num("atr14"), num("macd_histogram"),
                    num("momentum"), num("volume_ratio"),
                    f.get("high_volatility"), f.get("funding_rate"),
                    f.get("bars"),
                    " PARTIAL-HISTORY" if f.get("partial") else ""))
    return "\n".join(lines) if lines else "  (no feature data)"


def _fmt_positions(positions):
    if not positions:
        return "  (flat — no open positions)"
    lines = []
    for symbol, pos in sorted(positions.items()):
        lines.append(
            "  %s: %s qty=%s entry=%s stop=%s target=%s opened=%s" % (
                symbol, pos.get("side"), pos.get("quantity"),
                pos.get("entry_price"), pos.get("stop_loss"),
                pos.get("take_profit"), pos.get("opened_at")))
    return "\n".join(lines)


def build_prompt(context):
    """context dict -> (system_prompt, user_prompt)."""
    config = context.get("config") or {}
    account = context.get("account") or {}
    user = """MARKET DATA (computed features per symbol and timeframe):
%s

YOUR ACCOUNT:
  equity: %s
  available margin: %s
  daily pnl: %s
  realized trades today: %s

YOUR OPEN POSITIONS:
%s

CONSTRAINTS:
  allowed symbols: %s
  leverage range: %s-%s
  max notional per trade: %s
  max concurrent positions: %s
  shorting allowed: %s

Decide now. In "reasoning", walk the decision framework: regime per symbol,
confluence count, EV math for any candidate trade, then the verdict. Respond
with ONE JSON object only.""" % (
        _fmt_features(context.get("features")),
        account.get("equity"), account.get("available_margin"),
        account.get("daily_pnl"), account.get("trades_today", 0),
        _fmt_positions(context.get("positions")),
        ", ".join(config.get("allowed_symbols") or []),
        config.get("min_leverage", 1), config.get("max_leverage", 10),
        config.get("max_notional_per_trade", "uncapped"),
        config.get("max_concurrent_positions", "uncapped"),
        bool(config.get("allow_short", True)))
    return SYSTEM_PROMPT, user


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build arena model prompt from context JSON")
    parser.add_argument("context", help="context JSON file (default: stdin)", nargs="?")
    args = parser.parse_args(argv)
    context = json.load(open(args.context)) if args.context else json.load(sys.stdin)
    system, user = build_prompt(context)
    print(json.dumps({"system": system, "user": user}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
