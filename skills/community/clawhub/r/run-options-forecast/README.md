# run-options-forecast

A self-contained Python tool that forecasts a stock's close at option expiration
using the Breeden-Litzenberger risk-neutral density extracted from the LSE
options flow smile, then recommends ranked options plays keyed off the
confidence-interval bands.

## Usage

```
python3 scripts/forecast_cli.py --ticker <TICKER> --expiry <YYYY-MM-DD>
```

| Argument | Required | Format | Example |
|---|---|---|---|
| `--ticker` | yes | Uppercase symbol | `MU` |
| `--expiry` | no | `YYYY-MM-DD` | `2026-07-31` (default: nearest) |

## Quick start

```bash
cd <this-skill-directory>
cp .env.example .env
# Edit .env to add your LSE API key
pip install -r requirements.txt

python3 scripts/forecast_cli.py --ticker MU --expiry 2026-07-31
```

Output is a text report with three sections: header (spot/IV/skew),
risk-neutral close forecast (median + 50/80/95% CI), and ranked options plays
with strikes, PoP, R/R, breakevens, max profit/loss.

## Layout

```
run-options-forecast/
├── SKILL.md              ← agent-facing docs
├── README.md             ← this file
├── requirements.txt      ← Python deps
├── .env.example          ← API key template
└── scripts/
    ├── forecast_cli.py        ← primary CLI (use this)
    ├── expiration_model.py    ← BL density extraction (PCHIP smile fit, no-arb check)
    ├── lse_options.py         ← LSE API client + signal calculators
    ├── recommend_plays.py     ← options strategy generator
    ├── visualize.py           ← Plotly dashboard generator
    ├── run_analysis.py        ← full dashboard CLI
    ├── ws_stream.py           ← WebSocket client for live options flow
    ├── run_streaming.py       ← live-stream CLI
    └── backtest.py            ← replay backtester + prediction-log scoring
```

**Run all commands from the skill root** (not from inside `scripts/`). Scripts
expect `cwd` to be the skill root so they can find `.env` and write outputs
(`MU_dashboard.html` etc.) next to the README.

## How it works

1. Pull the latest options flow prints from LSE (default: 5000 most recent).
2. Extract volume-weighted IV smile per strike for the target expiry.
3. Fit a PCHIP monotone cubic spline in log-forward-moneyness.
4. Compute Black-Scholes call prices on a dense ±3σ strike grid.
5. Apply Breeden-Litzenberger: `f(K) = e^((r−q)T) · ∂²C/∂K²`.
6. Enforce no-arb (density ≥ 0, mean ≈ forward).
7. Normalize to probability density, integrate to CDF, invert for CI quantiles.
8. For each candidate strategy, integrate the BL density over the profit zone
   to get risk-neutral Probability of Profit; rank by PoP × reward-to-risk.

## Caveats

- **Risk-neutral ≠ real-world.** Outputs are market-implied. The variance risk
  premium systematically inflates downside tail probability vs physical measure.
- **LSE chain has no open interest field.** GEX uses `volume_today` as an
  OI-proxy. Document limitation; integrate a real OI feed for production GEX.
- **Approximate option prices use ATM IV at grid strikes**, not the per-leg
  smile IV. Verify against live quotes before execution.
- **Historical flow for PCR z-scoring is sparse** (some days empty). The engine
  skips empty days; n<10 ⇒ unreliable z-score.

## Programmatic use

```python
import sys
sys.path.insert(0, "scripts")

from lse_options import LSEClient, _latest_spot
from expiration_model import forecast_expiration
from recommend_plays import recommend_plays

client = LSEClient()
flow = client.options_flow("MU", limit=5000)
spot = _latest_spot(flow)
fc = forecast_expiration(flow, spot, target_expiry="2026-07-31")
plays = recommend_plays(fc, top_n=4)
```

## License

Research tooling. Not investment advice.
