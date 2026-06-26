---
name: ganglion-synth-city
description: "Mine Bittensor Subnet 50 (Synth) with Ganglion.  Covers price-path simulation, CRPS scoring, volatility estimation, backtesting, and multi-asset forecasting."
homepage: https://github.com/TensorLink-AI/ganglion
metadata: {"openclaw": {"emoji": "\u26d3", "requires": {"anyBins": ["ganglion", "curl"]}, "always": false}}
---

# Synth City — SN50 Mining Skill

Synth (netuid 50) is a probabilistic price-forecasting subnet on Bittensor.
Miners generate 1 000 Monte Carlo price paths per asset.  Validators score
submissions using CRPS (Continuous Ranked Probability Score) across multiple
time increments.  Emissions split 50/50 between low-frequency (24 h) and
high-frequency (1 h) competitions.

This skill provides SN50 domain knowledge.  Use the `ganglion` skill for
generic Ganglion API commands.

Repo: https://github.com/mode-network/synth-subnet/tree/main/synth

## How SN50 works

```
Validator                              Miner
─────────                              ─────
1. SimulationInput ──────────────────► 2. Fetch live price (Pyth Hermes)
   (asset, start_time,                    Generate 1 000 price paths
    time_increment, time_length,
    num_simulations=1000)
                                       3. Return tuple:
                                    ◄──── (timestamp, increment,
                                           [path_1], …, [path_1000])

4. Wait for horizon to elapse
5. Fetch realised prices (Pyth Benchmarks)
6. Compute CRPS per scoring interval (basis points)
7. 90th-percentile cap → normalise (best=0) → asset coeff
   → 10-day rolling avg (5-day half-life) → softmax → weights
```

## Competitions

| | Low-frequency | High-frequency |
|---|---|---|
| Assets | BTC ETH SOL XAU SPYX NVDAX TSLAX AAPLX GOOGLX | BTC ETH SOL XAU |
| Horizon | 24 h (86 400 s) | 1 h (3 600 s) |
| Increment | 5 min (300 s) | 1 min (60 s) |
| Points / path | 289 | 61 |
| Paths | 1 000 | 1 000 |
| Scoring intervals | 5 min, 30 min, 3 h, 24 h abs | 1 min → 60 min (18 intervals) |
| Rolling window | 10 days (5-day half-life) | 3 days |
| Softmax β | −0.1 | −0.2 |
| Emission share | 50 % | 50 % |
| Cycle time | 60 min | 12 min |

## Submission format

```python
(
    start_timestamp,          # int — unix seconds, must match request
    time_increment,           # int — seconds, must match request
    [p0, p1, …, pT],         # path 1 — T = time_length / time_increment + 1
    [p0, p1, …, pT],         # path 2
    …                        # 1 000 paths total
)
# Max 8 significant digits per price value.
# Validation rejects: wrong timestamp, wrong increment, wrong path count,
# wrong path length, non-numeric values, >8 digits.
```

## CRPS scoring pipeline

1. Price changes computed in **basis points**: `(diff / price) × 10 000`
2. Intervals ending in `_abs` use absolute prices normalised by `real_price[-1] × 10 000`
3. Intervals ending in `_gap` use only the first two points in each chunk
4. NaN gaps handled by `label_observed_blocks` — only consecutive non-NaN blocks scored
5. `properscoring.crps_ensemble(real_value, simulated_ensemble)` per time step
6. Total CRPS = sum across all intervals and time steps

Post-CRPS normalisation:
1. Cap at 90th percentile; invalid scores (-1) set to p90
2. Shift so best miner = 0
3. Multiply by per-asset coefficient
4. 10-day rolling average with 5-day half-life exponential decay
5. Softmax with negative β → lower CRPS = higher weight
6. Sum low-freq + high-freq weights → `set_weights` on chain

## Per-asset coefficients (weight normalisation)

```
BTC: 1.000   ETH: 0.672   SOL: 0.588   XAU: 2.262
SPYX: 2.991  NVDAX: 1.389 TSLAX: 1.420 AAPLX: 1.865  GOOGLX: 1.431
```

XAU and equity coefficients are higher — improvements on those assets
have outsized impact on emissions.

## Reference sigma values (hourly, GBM baseline)

```
BTC: 0.00472  ETH: 0.00695  SOL: 0.00782  XAU: 0.00208
SPYX: 0.00156 NVDAX: 0.00342 TSLAX: 0.00332 AAPLX: 0.00250 GOOGLX: 0.00332
```

These are from `synth/miner/simulations.py`.  Competitive miners should
NOT use fixed sigma — estimate from recent data instead.

## Price data sources

| Source | Used by | URL | Resolution |
|--------|---------|-----|------------|
| Pyth Hermes | Miners (live price) | `https://hermes.pyth.network/v2/updates/price/latest` | Real-time |
| Pyth Benchmarks | Validator (scoring) | `https://benchmarks.pyth.network/v1/shims/tradingview/history` | 1 min |

Benchmarks symbols: `Crypto.BTC/USD`, `Crypto.ETH/USD`, `Crypto.SOL/USD`,
`Crypto.XAUT/USD`, `Crypto.SPYX/USD`, `Crypto.NVDAX/USD`, `Crypto.TSLAX/USD`,
`Crypto.AAPLX/USD`, `Crypto.GOOGLX/USD`

## Tools in this project

| Tool | Category | Purpose |
|------|----------|---------|
| `run_experiment` | training | Generate Monte Carlo paths.  Docstring contains full SN50 subnet reference. |
| `fetch_price` | data | Live spot price from Pyth Hermes oracle |
| `fetch_historical_prices` | data | Historical prices from Pyth Benchmarks (same source validator uses for CRPS scoring).  Returns timestamps, prices, returns in bps, gap info. |
| `estimate_volatility` | training | Estimate sigma from recent returns (realized vol or EWMA) |
| `score_paths` | evaluation | CRPS against realised prices (single window, quick check) |
| `backtest` | evaluation | Full validator scoring pipeline replay: multi-interval CRPS at all SN50 scoring increments, per-asset coefficients, NaN handling, percentile normalisation.  Supports both low_freq and high_freq competitions. |

## Search strategies

1. Start with GBM + reference sigma as baseline — establishes a CRPS floor
2. Use `fetch_historical_prices` to pull recent data, then `estimate_volatility` with EWMA
3. `backtest` your paths against the historical window to get exact validator-equivalent CRPS
4. Try GARCH(1,1) for volatility clustering — this is what CRPS rewards
5. Add jump-diffusion (Merton) for sudden price moves GBM misses
6. Regime-switching (bull/bear/sideways) for adaptive volatility
7. Student-t or skewed-t innovations instead of normal (fat tails)
8. Ensemble: blend paths from multiple models (e.g. 500 GBM + 500 jump)
9. Calibrate per-asset: BTC and SOL need different models than XAU or SPYX
10. Target high-coefficient assets first (XAU=2.262, SPYX=2.991) for max emission impact

## Known pitfalls

- Constant sigma fails during high-volatility regimes — CRPS will spike
- Overfitting to recent action → narrow distributions that blow up on regime change
- Too few paths (< 500) → noisy CRPS estimates; use 1 000 (the required amount)
- Ignoring 24/7 BTC vol structure (weekends, overnight) degrades scores
- Neural SDE training is unstable with < 90 days of minute-level data
- Same distribution for BTC and ETH ignores different vol characteristics
- Exceeding 8 significant digits per price value → validator rejects submission
- Not matching start_timestamp or time_increment exactly → rejection

## Bootstrap workflow

```bash
# Scaffold (if using ganglion init)
ganglion init ./synth-city --subnet sn50 --netuid 50

# Or copy this example directory and run:
export GANGLION_PROJECT=./examples/synth-city
ganglion status $GANGLION_PROJECT
ganglion tools $GANGLION_PROJECT
ganglion run $GANGLION_PROJECT

# Remote mode
ganglion serve ./examples/synth-city --bot-id alpha --port 8899
export GANGLION_URL=http://127.0.0.1:8899
```

## Example workflow (remote mode)

```bash
# 1. Fetch 48h of BTC history at 5-min intervals
curl -s -X POST "$GANGLION_URL/v1/run/experiment" \
  -H "Content-Type: application/json" \
  -d '{"config": {"tool": "fetch_historical_prices", "asset": "BTC", "hours_back": 48, "time_increment": 300}}' \
  | jq .data

# 2. Run GBM baseline
curl -s -X POST "$GANGLION_URL/v1/run/experiment" \
  -H "Content-Type: application/json" \
  -d '{"config": {"asset": "BTC", "model_type": "gbm", "num_simulations": 1000}}' \
  | jq .data

# 3. Backtest against the historical window
# (pass realized_prices from step 1 into the backtest tool)

# 4. Check knowledge for patterns
curl -s "$GANGLION_URL/v1/knowledge?capability=simulate" | jq .data
```

## Key dependencies

- `numpy` — path generation, array ops
- `properscoring` — CRPS calculation (`pip install properscoring`)
- Pyth Hermes API — live prices
- Pyth Benchmarks API — historical prices (same source as validator)
