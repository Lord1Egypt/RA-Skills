---
name: run-options-forecast
description: Forecast where a stock will close at option expiration and recommend options plays. Use when the user asks for an options forecast, expected close range, CI bands, or trade ideas for a specific ticker and expiration. Produces a Breeden-Litzenberger risk-neutral density forecast (median, 50/80/95% CI) and ranked options strategies (spreads, iron condor, butterfly, straddle) with strikes, probability of profit, and reward-to-risk.
---

# run-options-forecast

Forecasts a stock's close at option expiration using the Breeden-Litzenberger risk-neutral density extracted from the LSE options flow smile, then recommends options plays keyed off the confidence-interval bands.

## Usage

```
python3 scripts/forecast_cli.py --ticker <TICKER> --expiry <YYYY-MM-DD>
```

**Inputs:**

| Argument | Required | Format | Example |
|---|---|---|---|
| `--ticker` | **yes** | Uppercase stock symbol | `MU`, `AAPL`, `NBIS` |
| `--expiry` | no | `YYYY-MM-DD` | `2026-07-31` |

If `--expiry` is omitted, the nearest expiry in the flow data is used.

**Minimal example:**

```bash
cd <skill-root>
python3 scripts/forecast_cli.py --ticker MU --expiry 2026-07-31
```

The CLI prints an input banner at the top of every run confirming what was parsed:

```
────────────────────────────────────────────────────────────────────────
  Usage:  forecast_cli.py --ticker <TICKER> --expiry <YYYY-MM-DD>
          e.g.  --ticker MU --expiry 2026-07-31
────────────────────────────────────────────────────────────────────────
  Input received:
    ticker:           MU
    expiry requested: 2026-07-31
    expiry resolved:  2026-07-31  (4d)
    ...
```

**Self-contained.** All scripts live in `scripts/`. Config and docs live at the skill root. Copy the directory to any machine and it works.

**Driver:** `scripts/forecast_cli.py`.

**Layout:**

```
run-options-forecast/
├── SKILL.md              ← this file
├── README.md             ← user-facing quickstart
├── requirements.txt      ← Python deps
├── .env.example          ← API key template (copy to .env)
└── scripts/
    ├── forecast_cli.py   ← primary CLI driver
    ├── expiration_model.py
    ├── lse_options.py
    ├── recommend_plays.py
    ├── visualize.py
    ├── run_analysis.py   ← dashboard CLI
    ├── ws_stream.py
    ├── run_streaming.py
    └── backtest.py
```

## Prerequisites

Python 3.10+. From the skill root:

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env and replace lse_live_REPLACE_ME with your real LSE API key
```

## Run (agent path) — primary entry point

Run from the **skill root** (so `.env` is found and outputs land predictably):

```bash
cd <skill-root>
python3 scripts/forecast_cli.py --ticker MU --expiry 2026-07-31
```

Common invocations:

```bash
# Nearest expiry automatically
python3 scripts/forecast_cli.py --ticker MU

# Surface 5 plays instead of default 4
python3 scripts/forecast_cli.py --ticker MU --expiry 2026-09-18 --top-n 5

# Machine-readable output (for downstream tooling)
python3 scripts/forecast_cli.py --ticker MU --expiry 2026-09-18 --json --out /tmp/mu_forecast.json

# Override risk-free rate and dividend yield
python3 scripts/forecast_cli.py --ticker AAPL --expiry 2026-08-15 --rate 0.053 --dividend-yield 0.005
```

**Required flag:** `--ticker SYMBOL`
**Optional flags:** `--expiry YYYY-MM-DD` (default: nearest), `--top-n N` (default 4), `--json`, `--out PATH`, `--rate R`, `--dividend-yield Q`, `--realized-variance V`

Exit codes: 0 = OK, 2 = missing deps or API key, 3 = LSE API error, 4 = no flow data, 5 = spot extraction failed, 6 = forecast failed.

## What the report contains

The text output has three sections:

1. **Header** — spot, forward, ATM IV, 1σ expected move, DTE, 25Δ risk reversal
2. **Risk-neutral close forecast** — median, mean, Q(close > spot) + direction, then 50/80/95% CI bands with absolute ranges AND ±% distances from spot
3. **Recommended options plays** — top N strategies ranked by (PoP × R/R), each with:
   - Strategy name + bias (BULLISH / BEARISH / NEUTRAL / VOLATILE)
   - Net debit or credit, total per-contract dollar amount
   - Probability of Profit (risk-neutral) and reward-to-risk ratio
   - Each leg: BUY/SELL, qty, strike, type (CALL/PUT), approx BS price
   - Breakeven(s), max profit, max loss
   - Rationale tied to the forecast (CI band used, IV level, etc.)

Strategy universe: Bull Call Spread, Bull Put Spread, Bear Put Spread, Bear Call Spread, Iron Condor, Long Call Butterfly, Long Straddle. Strikes are anchored to CI quantiles (e.g. iron condor shorts at 80% CI bounds, wings at 95% CI bounds).

## Run (human path) — full dashboard

```bash
cd <skill-root>
python3 scripts/run_analysis.py MU
open MU_dashboard.html
```

The dashboard (`MU_dashboard.html`) lands at the skill root. It includes the risk-neutral density plot with 50/80/95% CI bands, the CI ladder panel, GEX walls, premium walls, IV smile, and the signal breakdown.

## Other entry points

```bash
# Live WebSocket stream (replays 24h, then live if market open)
python3 scripts/run_streaming.py MU --replay 4

# Backtest an expiry (requires realized close callback — see scripts/backtest.py)
python3 scripts/backtest.py --score-log
```

## Gotchas

- **Risk-neutral ≠ real-world.** All PoP numbers come from the BL density, which is tilted by the variance risk premium. Real-world PoP is typically HIGHER for short-vol credit plays (condors, credit spreads) and LOWER for long-vol plays (straddle). Treat as a ranking tool, not a calibrated probability.
- **LSE chain has no open interest field**, only `volume_today`. GEX is therefore a volume-based proxy, not true OI-based dealer positioning.
- **Historical flow for PCR z-scoring is sparse** — some days return 0 rows. The engine skips empty days and z-scores against whatever history survives.
- **Approximate option prices use ATM IV at grid strikes** (not the full smile per-leg). Verify against live quotes before execution.
- **0-DTE expiries** still work — `T` is floored to 1/365 to avoid div-by-zero. The CIs become narrow; this is correct behavior.
- **Dividend-paying stocks**: pass `--dividend-yield`. MU's annual yield is ~0.3-0.5%. The forward `F = S · e^((r−q)T)` adjusts accordingly.
- **No-arb check**: every report shows `arb_status` (OK or FAIL). If it fails (`μ/F` outside [0.97, 1.03]), the smile fit produced arbitrage — distrust the tails.
- **SSL on macOS**: `LSEClient` uses `certifi` to avoid the "unable to get local issuer certificate" error. If you skip `pip install certifi` you will hit SSL errors.
- **Run from skill root, not `scripts/`**: `python-dotenv`'s `load_dotenv()` looks for `.env` in the cwd. If you `cd scripts/` first, `.env` won't be found at the skill root and the API key will be missing.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `SSL: CERTIFICATE_VERIFY_FAILED` | `pip install --upgrade certifi`. Verify with `python3 -c "import certifi; print(certifi.where())"`. |
| `LONDON_STRATEGIC_EDGE_API_KEY not set` | `cp .env.example .env` at the skill root, add your key. You must run from the skill root, not from `scripts/`. |
| `No flow data for MU` | Either the symbol is wrong, or the LSE vault has no recent prints. Try a different ticker or check market hours. |
| `Insufficient IV data for <expiry>: only N strikes` | That expiry doesn't have enough OTM prints to fit a smile. Try a more liquid expiry or omit `--expiry` to use the nearest. |
| `arb_status: FAIL` | Smile fit is producing negative density somewhere. Re-run with a different expiry or check whether spot has moved significantly since the flow snapshot. |
| `ModuleNotFoundError: No module named 'plotly'` | Only needed for the dashboard, not the CLI. `pip install plotly`. |
| `ImportError: No module named 'recommend_plays'` | You ran the script from outside the skill root with the wrong path. Use `python3 scripts/forecast_cli.py ...` from the skill root. |
| PCR z-score seems off | Historical flow is sparse. Check the printed `n=` in the PCR interpretation — if n<10, the z-score is unreliable. |

## Programmatic use

The driver is a thin wrapper. For custom workflows, add `scripts/` to your path and import:

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
plays = recommend_plays(fc, top_n=3)

print(f"Median close: ${fc.median:,.2f}")
print(f"Q(close > spot) = {fc.prob_above_spot:.1%}")
print(f"CI bands: 50% {fc.ci_50}, 80% {fc.ci_80}, 95% {fc.ci_95}")
```

The `ExpirationForecast` dataclass carries the full density (`density_strikes`, `density_values`) for custom integration.

## Files in this skill

| File | Purpose |
|---|---|
| `SKILL.md` | This document. |
| `README.md` | User-facing README (same content, different framing). |
| `requirements.txt` | Python deps. |
| `.env.example` | Template for LSE API key. Copy to `.env`. |
| `scripts/forecast_cli.py` | Primary CLI driver. |
| `scripts/expiration_model.py` | BL density extraction. |
| `scripts/lse_options.py` | LSE client + signal calculators. |
| `scripts/recommend_plays.py` | Options strategy generator. |
| `scripts/visualize.py` | Plotly dashboard. |
| `scripts/run_analysis.py` | Dashboard CLI. |
| `scripts/ws_stream.py` | WebSocket flow client. |
| `scripts/run_streaming.py` | Live stream CLI. |
| `scripts/backtest.py` | Replay backtester + prediction-log scorer. |
