# layer details

the engine evaluates every coin through 9 intelligence layers.
layers 1-7 are quantitative. layer 8 is qualitative (LLM). layer 9 is cross-timeframe.
a coin must pass a consensus threshold (default 5/7 on the quantitative layers) to become a candidate.

## layer 1: regime

classifies market structure via SmartProvider's regime_classifier.

- trending: momentum strategies work
- stable: mean-reversion works
- reverting: fade strategies work
- chaotic: defense mode, most strategies blocked

each strategy declares which regimes it allows. if the current regime isn't in the allow list, the layer fails.

## layer 2: technical

RSI + MACD + EMA + Bollinger majority vote on direction.

- each indicator votes: agrees with direction or not
- needs 2/4 minimum agreement to pass
- RSI value also tracked directly (used for exit signals at extremes)

example: 3/4 indicators agree SHORT = pass.

## layer 3: funding

funding rate favorable for the trade direction.

- LONG: funding rate <= 0.01% or funding signal agrees
- SHORT: funding rate >= -0.01% or funding signal agrees
- contrarian logic: you want to be paid to hold, not pay

## layer 4: book depth

L2 order book depth ratio favorable for direction.

- bid_ratio > 0.5 for LONG, < 0.5 for SHORT
- if total depth < $1000: layer marked data_unavailable (doesn't count against consensus)
- thin books = slippage risk

## layer 5: open interest

OI confirming trade direction.

- rising OI + price moving in direction = conviction
- declining OI = caution
- no data = layer marked unavailable

## layer 6: macro

Fear & Greed index as contrarian filter.

- extreme fear blocks longs
- extreme greed blocks shorts
- moderate readings pass for both directions

## layer 7: collective

network consensus across agents.

- checks whether >60% of network agents agree on direction
- currently auto-passes (no network data yet)
- when more agents join, this becomes a real filter

## layer 8: LLM reasoning (qualitative)

local LLM provides qualitative assessment of candidate setups.

- only runs on coins that already pass 5/7+ quantitative layers (cost optimization)
- calls local Ollama model (same infra as reflection agent)
- has narrative memory: queries similar past setups from episode memory, injects context into prompt
- returns PASS or SKIP with confidence score + reasoning text
- falls back to pass-through if Ollama is unavailable (never blocks trading when LLM is down)
- can veto a 7/7 mechanical setup if the qualitative picture is bad

this is the "smell test" layer. the quantitative layers say the numbers line up. the LLM checks whether the story makes sense given recent history.

## layer 9: cross-timeframe confirmation

checks alignment between fast and slow timeframes.

- reads `bus/timeframe_signals.json` produced by the cross_timeframe_agent
- fast timeframe (15M): RSI, EMA cross, CMO, MACD cross, momentum
- slow timeframe (24H/48H): RSI, EMA, MACD, ROC, Hurst, DFA, Lyapunov
- classifies each as bullish/bearish/neutral, then detects the pattern:
  - CONFIRMATION_LONG: fast + slow both bullish (score +1.0)
  - CONFIRMATION_SHORT: fast + slow both bearish (score +1.0)
  - DIVERGENCE_BULL: fast bearish but slow bullish (score -0.5)
  - DIVERGENCE_BEAR: fast bullish but slow bearish (score -0.5)
- passes when the pattern aligns with the trade direction
- auto-passes if data is unavailable (agent hasn't run yet or file is stale)

## layer weights

an execution feedback loop adjusts layer weights based on real trade outcomes.

- after each closed trade, the system checks which layers were correct
- weight formula: `weight = clamp(0.5 + accuracy, 0.5, 1.5)`
- stored in `bus/layer_weights.json`
- examples:
  - a layer with 80% accuracy gets weight 1.3
  - a layer with 50% accuracy gets weight 1.0
  - a layer that's wrong more than right floors at 0.5

weights influence the conviction score, not the pass/fail of individual layers. a high-weight layer passing adds more to conviction than a low-weight one.

## consensus scoring

the 7 quantitative layers (1-7) determine pass/fail consensus. default threshold is 5/7.

once a coin passes the quantitative threshold:
- layer 8 (LLM) may still veto. a 7/7 quantitative setup can be rejected if the LLM flags a problem.
- layer 9 (cross-timeframe) confirms or warns. divergence doesn't veto but lowers conviction.

conviction = weighted sum of passing layers / weighted sum of available layers. layer weights from the feedback loop shape conviction, so layers with a proven track record count more.

the engine rejects ~97% of setups. the ones that survive all 9 layers: those are the trades.
